import logging

import psycopg2
from psycopg2.extras import DictCursor

from core.config import settings
from generator.src.models.notifications import Event
from generator.src.models.task import Task
from generator.src.models.user import User
from generator.src.service.connector import AuthenticatedSession

db_creds = settings.django.db_creds

logger = logging.getLogger(__name__)


class UGCConnection:
    def __init__(self, connector: AuthenticatedSession):
        self.connector = connector

    def get_content_subscribers(self, content_id: str) -> list[str]:
        """Return list of users, subscribed to new content events."""
        return self.connector.post(url=f'{settings.ugc.subscribers_uri}{content_id}')

    def get_likes_count(self, review_id: str) -> int:
        """Return number of current likes on review."""
        likes = self.connector.post(url=f'{settings.ugc.likes_count_uri}{review_id}')
        return likes["likes_count"]

    def close(self) -> None:
        """Close requests session."""
        self.connector.close()


class AuthConnection:
    def __init__(self, connector: AuthenticatedSession):
        self.connector = connector

    def get_user_data(self, user_id: str) -> User:
        """Return list of users, subscribed to new content events."""
        logger.info(f'get user data with id {user_id}')
        response = self.connector.post(url=f'{settings.auth.user_data_uri}{user_id}')
        return response

    def get_user_group(self, group_id: str) -> list[str]:
        """Return list of users, belong to the group."""
        logger.info(f'get user group with id {group_id}')
        response = self.connector.post(url=f'{settings.auth.group_id_uri}{group_id}')
        logger.info(f'response: {response}')
        return response

    def filter_users(self, user_ids: list[str], conditions: list) -> list[str]:
        """Filter users, that match the conditions."""
        #
        logger.info('filter users by conditions')
        return [self.get_user_data(user_id)["user_id"] for user_id in user_ids if conditions]

    # TODO: Как должна работать эта строчка? что такое self.get_user_data(user_id).user_id ?
    #

    def close(self) -> None:
        """Close requests session."""
        self.connector.close()


class ApiConnection:
    def __init__(self, connector: AuthenticatedSession):
        self.connector = connector

    def send_event(self, event: Event):
        logger.info(f'Send event. Payload: {event}')
        response = self.connector.post(url=settings.api.send_uri, payload=event)
        logger.info(f'response: {response}')
        return response

    def close(self) -> None:
        """Close requests session."""
        self.connector.close()


class PGConnection:
    def __init__(self):
        with psycopg2.connect(**db_creds) as pg_conn:
            self.cursor = pg_conn.cursor(cursor_factory=DictCursor)

    def fetch_table(self, command: str) -> list[dict]:
        """Get data from table."""
        self.cursor.execute(command)
        data = self.cursor.fetchall()
        return [dict(el) for el in data]

    def get_task_from_db(self, task_id: str) -> Task:
        logger.info(f'select notification with id {task_id}')
        command = f"""SELECT * from notifications_task \
                    WHERE notifications_task.pkid = '{task_id}';"""
        self.cursor.execute(command)
        _data = self.cursor.fetchone()
        task = Task(**_data)
        logger.info(f'Task from DB: {task}')
        return task
