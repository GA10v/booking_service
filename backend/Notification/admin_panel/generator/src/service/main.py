from datetime import datetime
import logging
from collections import namedtuple
from typing import Union
from uuid import uuid4

from generator.src.models.context import NewContent, NewPromo, NewReviewsLikes
from generator.src.models.notifications import Event, EventType
from generator.src.models.task import Task
from generator.src.service.communicators import ApiConnection, AuthConnection, PGConnection, UGCConnection
from generator.src.service.connector import AuthenticatedSession

logger = logging.getLogger(__name__)


class ProcessTask:
    def __init__(self):
        self.connection = next(self._get_connect())

    @staticmethod
    def _get_connect():
        """Establish connections with other app modules and close it at the end."""
        ugc_connection = UGCConnection(AuthenticatedSession())
        auth_connection = AuthConnection(AuthenticatedSession())
        api_connection = ApiConnection(AuthenticatedSession())
        pg_connection = PGConnection()

        Connection = namedtuple('Connection', ['ugc', 'auth', 'api', 'postgres'])
        yield Connection(ugc_connection, auth_connection, api_connection, pg_connection)

        ugc_connection.close()
        auth_connection.close()
        api_connection.close()

    @staticmethod
    def _get_context(data: Task, kwargs: dict) -> Union[NewContent, NewReviewsLikes, NewPromo]:
        logger.info('get context')
        context = None
        if data.event_type == EventType.new_content:
            context = NewContent(**kwargs)
        elif data.event_type == EventType.new_likes:
            context = NewReviewsLikes(**kwargs)
        elif data.event_type == EventType.promo:
            context = NewPromo(**kwargs)
        logger.info(f'context: {context}')
        return context

    @staticmethod
    def _form_event(
        task: Task,
        content: NewContent | NewPromo | NewReviewsLikes,
    ) -> Event:
        """Form Event that should be sent."""
        event = Event(
            notification_id=str(uuid4()),
            event_type=task.event_type,
            created_at=datetime.utcnow(),
            source_name='Generator',
            context=content,
        ).dict()
        logger.info(f'prepared Event: {event}')
        return event

    def _get_reviews_from_db(self) -> list[dict]:
        """Return reviews data from Notifications DB."""
        return self.connection.postgres.fetch_table('SELECT * FROM notifications_reviewinfo;')

    def _filter_increased_likes(self) -> list[dict]:
        """
        Return all records from Notifications DB, when likes count in DB is less than current amount.
        Record ID is removed to use record for create NewReviewLikes object.
        """
        db_records = self._get_reviews_from_db()
        logger.info(f'all reviews: {[record["review_id"] for record in db_records]}')
        filtered_reviews = []
        for record in db_records:
            logger.info(f'proceed with review {record["review_id"]}')
            logger.info(f'previous likes count: {record["likes_count"]}')
            current_likes = self.connection.ugc.get_likes_count(record["review_id"])
            logger.info(f'current likes count: {current_likes}')
            if current_likes > record["likes_count"]:
                # remove "pkid" key from record
                record.pop('pkid')
                # update likes in record
                record["likes_count"] = current_likes
                filtered_reviews.append(record)
                logger.info('add to updated reviews')
        return filtered_reviews

    def _send_new_content_events(self, task: Task) -> None:
        """Send NewContent or NewPromo events."""
        logger.info('--- SEND NEW CONTENT TASK ---')
        logger.info(f'Task: {task}')
        all_subscribed_users = self.connection.ugc.get_content_subscribers(task.movie_id)
        logger.info(f'new content subscribers: {all_subscribed_users}')
        filtered_users = self.connection.auth.filter_users(all_subscribed_users, [{'TZ': True}])
        logger.info(f'filtered subscribers: {filtered_users}')
        for user in filtered_users:
            logger.info(f'proceed with user_id {user}')
            content = self._get_context(task, {'movie_id': task.movie_id, 'user_id': user})
            event = self._form_event(task, content)
            self.connection.api.send_event(event)

    def _send_updated_reviews(self, task: Task) -> None:
        """Send NewReviewsLikes events."""
        logger.info('--- SEND UPDATED REVIEWS TASK ---')
        reviews = self._filter_increased_likes()
        for review in reviews:
            logger.info(f'prepare review {review["review_id"]} to send')
            content = self._get_context(task, review)
            event = self._form_event(task, content)
            self.connection.api.send_event(event)

    def _send_promo_events(self, task: Task) -> None:
        """Send promo events."""
        logger.info('--- SEND PROMO TASK ---')
        logger.info(f'Task: {task}')
        group_users = self.connection.auth.get_user_group(task.group_id)
        filtered_users = self.connection.auth.filter_users(group_users, [{'TZ': True}])
        for user in filtered_users:
            logger.info(f'proceed with user_id {user}')
            content = self._get_context(task, {'user_id': user, 'text_to_promo': task.text_to_promo})
            event = self._form_event(task, content)
            self.connection.api.send_event(event)

    def _process_email_task(self, task):
        """Handle email tasks."""
        if task.event_type == EventType.new_content:
            self._send_new_content_events(task)
        elif task.event_type == EventType.new_likes:
            self._send_updated_reviews(task)
        elif task.event_type == EventType.promo:
            self._send_promo_events(task)

    def get_task(self, task_id: str) -> Task:
        return self.connection.postgres.get_task_from_db(task_id=task_id)

    def perform_task(self, task):
        """
        Single entry to start generating and sending notifications to Enricher.
        Receive task from scheduler and proceed. Can be used with different source types.
        """
        self._process_email_task(task)
