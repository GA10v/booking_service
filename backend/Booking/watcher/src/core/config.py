from pathlib import Path
from random import choice
from string import ascii_letters

from pydantic import BaseSettings


class BaseConfig(BaseSettings):
    class Config:
        env_file = Path(Path(__file__).parent.parent.parent.parent.parent.parent, 'env')
        env_file_encoding = 'utf-8'


class LoggingSettings(BaseConfig):
    SENTRY_DSN: str = ''
    LOGSTASH_HOST: str = 'logstash'
    LOGSTASH_PORT: int = 5044

    class Config:
        env_prefix = 'LOGGING_'


class DebugSettings(BaseConfig):
    DEBUG: bool = True

    class Config:
        env_prefix = 'DEBUG_'


class WatcherSettings(BaseConfig):
    SLEEP_MINUTES: int = 1

    @property
    def sleep(self):
        return self.SLEEP_MINUTES * 60

    class Config:
        env_prefix = 'WATCHER_'


class PostgresSettings(BaseConfig):
    DB: str = 'db_name'
    USER: str = 'guest'
    PASSWORD: str = 'guest'
    HOST: str = 'localhost'
    PORT: int = 5432

    @property
    def uri(self):
        return f'postgresql+psycopg2://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DB}'

    @property
    def a_uri(self):
        return f'postgresql+asyncpg://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DB}'

    class Config:
        env_prefix = 'POSTGRES_'


class JWTSettings(BaseConfig):
    SECRET_KEY: str = ''.join(choice(ascii_letters) for _ in range(200))
    JWT_TOKEN_LOCATION: list = ['headers']
    ALGORITHM: str = 'HS256'

    class Config:
        env_prefix = 'JWT_'


class RedisSettings(BaseConfig):
    HOST: str = 'localhost'
    PORT: int = 6379
    INDEX: int = 0
    EXPIRE_SEC: int = 5 * 60  # 5 minutes

    @property
    def uri(self):
        return f'redis://{self.HOST}:{self.PORT}/{self.INDEX}'

    class Config:
        env_prefix = 'REDIS_'


class NotificationSettings(BaseConfig):
    HOST: str = 'localhost'
    PORT: int = 8070
    NOTIFIC_PREFIX: str = '/app/v1/notification/'

    @property
    def uri(self):
        return f'http://{self.HOST}:{self.PORT}{self.NOTIFIC_PREFIX}'

    class Config:
        env_prefix = 'NOTIFIC_FASTAPI_'


class BookingSettings(BaseConfig):
    HOST: str = 'localhost'
    PORT: int = 8080
    API_PREFIX: str = '/app/v1'

    @property
    def uri(self):
        return f'http://{self.HOST}:{self.PORT}{self.API_PREFIX}'

    @property
    def announce_uri(self):
        return f'{self.uri}/announcement/'

    @property
    def all_announce_uri(self):
        return f'{self.uri}/announcements/'

    @property
    def booking_uri(self):
        return f'{self.uri}/booking/'

    class Config:
        env_prefix = 'FASTAPI_'


class ProjectSettings(BaseConfig):
    PROJECT_NAME: str = 'Graduate_work'
    BASE_DIR = Path(__file__).parent.parent
    logging: LoggingSettings = LoggingSettings()
    debug: DebugSettings = DebugSettings()
    postgres: PostgresSettings = PostgresSettings()
    jwt: JWTSettings = JWTSettings()
    redis: RedisSettings = RedisSettings()
    watcher: WatcherSettings = WatcherSettings()
    nptific: NotificationSettings = NotificationSettings()
    booking: BookingSettings = BookingSettings()


settings = ProjectSettings()
