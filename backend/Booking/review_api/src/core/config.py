from enum import Enum
from pathlib import Path
from random import choice
from string import ascii_letters

from pydantic import BaseSettings, MongoDsn


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


class FastapiSettings(BaseConfig):
    HOST: str = 'localhost'
    PORT: int = 8080
    API_PREFIX: str = '/app/v1'

    class Config:
        env_prefix = 'FASTAPI_'

    @property
    def uri(self):
        return f'http://{self.HOST}:{self.PORT}{self.API_PREFIX}'


class ReveiwAPISettings(BaseConfig):
    HOST: str = 'localhost'
    PORT: int = 8084
    API_PREFIX: str = '/app/v1'

    class Config:
        env_prefix = 'REVIEW_API'


class PermissionSettings(Enum):
    User = 0
    Subscriber = 1
    Vip_subscriber = 2
    Moderator = 3


class JWTSettings(BaseConfig):
    SECRET_KEY: str = ''.join(choice(ascii_letters) for _ in range(200))
    JWT_TOKEN_LOCATION: list = ['headers']
    ALGORITHM: str = 'HS256'

    class Config:
        env_prefix = 'JWT_'


class MongoSettings(BaseConfig):
    HOST: str = 'localhost'
    PORT: int = 27019
    DB: str = 'booking_reviews'
    REVIEW_COLLECTION: str = 'reviews'

    class Config:
        env_prefix = 'MONGODB_'

    @property
    def uri(self) -> MongoDsn:
        return f'mongodb://{self.HOST}:{self.PORT}'


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


class ProjectSettings(BaseConfig):
    PROJECT_NAME: str = 'Graduate_work'
    BASE_DIR = Path(__file__).parent.parent
    logging: LoggingSettings = LoggingSettings()
    debug: DebugSettings = DebugSettings()
    fastapi: FastapiSettings = FastapiSettings()
    jwt: JWTSettings = JWTSettings()
    mongo: MongoSettings = MongoSettings()
    redis: RedisSettings = RedisSettings()
    review_api: ReveiwAPISettings = ReveiwAPISettings()
    notific: NotificationSettings = NotificationSettings()


settings = ProjectSettings()
