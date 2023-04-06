from collections import namedtuple
from typing import Union
from uuid import uuid4

from generator.src.models.context import NewContent, NewPromo, NewReviewsLikes
from generator.src.models.notifications import Event, EventType
from generator.src.models.task import Task
from generator.src.service.communicators import ApiConnection, AuthConnection, PGConnection, UGCConnection
from generator.src.service.connector import AuthenticatedSession


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
        context = None
        if data.event_type == EventType.new_content:
            context = NewContent(**Task)
        elif data.event_type == EventType.new_likes:
            context = NewReviewsLikes(**kwargs)
        elif data.event_type == EventType.promo:
            context = NewContent(**Task)
        return context

    @staticmethod
    def _form_event(
        task: Task,
        content: NewContent | NewPromo | NewReviewsLikes,
    ) -> Event:
        """Form Event that should be sent."""
        return Event(
            notification_id=str(uuid4()),
            event_type=task.event_type,
            source_name='Generator',
            context=content,
        )

    def _get_reviews_from_db(self) -> list[dict]:
        """Return reviews data from Notifications DB."""
        return self.connection.postgres.fetch_table('SELECT * FROM notifications_reviewinfo;')

    def _get_task(self, task_id: str) -> Task:
        return self.connection.postgres.get_task(task_id=task_id)

    def _filter_increased_likes(self) -> list[dict]:
        """
        Return all records from Notifications DB, when likes count in DB is less than current amount.
        Record ID is removed to use record for create NewReviewLikes object.
        """
        db_records = self._get_reviews_from_db()
        filtered_reviews = []
        for record in db_records:
            current_likes = self.connection.ugc.get_likes_count(record['review_id'])
            if current_likes['likes_count'] > record['likes_count']:
                # remove "pkid" key from record
                record.pop('pkid')
                filtered_reviews.append(record)
        return filtered_reviews

    def _send_new_content_events(self, task: Task) -> None:
        """Send NewContent or NewPromo events."""
        all_subscribed_users = self.connection.ugc.get_content_subscribers(task.movie_id)
        filtered_users = self.connection.auth.filter_users(all_subscribed_users, [{'TZ': True}])
        for user in filtered_users:
            content = self._get_context(task, {'movie_id': task.movie_id, 'user_id': user})
            event = self._form_event(task, content)
            self.connection.api.send_event(event)

    def _send_updated_reviews(self, task: Task) -> None:
        """Send NewReviewsLikes events."""
        reviews = self._filter_increased_likes()
        for review in reviews:
            content = self._get_context(task, review)
            event = self._form_event(task, content)
            self.connection.api.send_event(event)

    def _send_promo_events(self, task: Task) -> None:
        """Send promo events."""
        group_users = self.connection.auth.get_user_group(task.group_id)
        filtered_users = self.connection.auth.filter_users(group_users, [{'TZ': True}])
        for user in filtered_users:
            content = self._get_context(task, {'user_id': user, 'text_to_promo': task.text_to_promo})
            event = self._form_event(task, content)
            self.connection.api.send_event(event)

    def _process_email_task(self, task: Task):
        """Handle email tasks."""
        if task.event_type == EventType.new_content:
            self._send_new_content_events(task)
        elif task.event_type == EventType.new_likes:
            self._send_updated_reviews(task)
        elif task.event_type == EventType.promo:
            self._send_promo_events(task)

    def perform_task(self, task: Task):
        """
        Single entry to start generating and sending notifications to Enricher.
        Receive task from scheduler and proceed. Can be used with different source types.
        """
        self._process_email_task(task)
