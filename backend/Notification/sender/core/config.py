"""Config file to whole project."""
from pathlib import Path

from pydantic import BaseSettings


class BaseConfig(BaseSettings):
    class Config:
        env_file = Path(Path(__file__).parent.parent.parent.parent.parent, 'env')
        env_file_encoding = 'utf-8'


class RabbitMQSetting(BaseConfig):
    USER: str = 'guest'
    PASSWORD: str = 'guest'
    HOST: str = 'localhost'
    PORT: int = 5672
    EXCHENGE_INCOMING_1: str = 'Exchange_incoming_1'
    EXCHENGE_INCOMING_2: str = 'Exchange_incoming_2'
    EXCHENGE_RETRY_1: str = 'Exchange_retry_1'
    EXCHENGE_RETRY_2: str = 'Exchange_retry_2'
    QUEUE_TO_ENRICH: str = 'Queue_to_enrich'
    QUEUE_TO_SEND: str = 'Queue_to_send'
    QUEUE_RETRY_ENRICH: str = 'Queue_retry_to_enrich'
    QUEUE_RETRY_SEND: str = 'Queue_retry_to_send'
    MESSAGE_TTL_MS: int = 10000
    MAX_RETRY_COUNT: int = 3
    CONNECT_POOL_SIZE: int = 10

    @property
    def uri(self):
        return f'amqp://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}'

    class Config:
        env_prefix = 'RABBIT_'


class EmailSettings(BaseConfig):
    """Class is being used to keep all settings."""

    USER: str = ''
    PASSWORD: str = ''
    SMTP_SERVER: str = ''
    SMTP_PORT: int = 465
    SMTP_SSL: bool | None = False

    class Config:
        """Configuration plugin."""

        env_prefix = 'EMAIL_'


class PostgresSettings(BaseConfig):
    USER: str = 'guest'
    PASSWORD: str = 'guest'
    HOST: str = 'localhost'
    PORT: int = 5672
    DB: str = 'some_db'

    @property
    def uri(self):
        return f'postgresql+psycopg2://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DB}'

    class Config:
        env_prefix = 'POSTGRES_'


class RedisSettings(BaseConfig):
    HOST: str = 'localhost'
    PORT: int = 6379
    INDEX_SEND: int = 1
    EXPIRE_SEC: int = 5 * 60  # 5 minutes

    @property
    def uri(self):
        return f'redis://{self.HOST}:{self.PORT}/{self.INDEX_SEND}'

    class Config:
        env_prefix = 'REDIS_'


class ProjectSettings(BaseConfig):
    PROJECT_NAME: str = 'Notification_api'
    BASE_DIR = Path(__file__).parent.parent
    email: EmailSettings = EmailSettings()
    rabbit: RabbitMQSetting = RabbitMQSetting()
    postgres: PostgresSettings = PostgresSettings()
    redis: RedisSettings = RedisSettings()


settings = ProjectSettings()
