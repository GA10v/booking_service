from enum import Enum
from pathlib import Path

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


class PermissionSettings(Enum):
    User = 0
    Subscriber = 1
    Vip_subscriber = 2
    Moderator = 3


class JWTSettings(BaseConfig):
    SECRET_KEY: str = '245585dbb5cbe2f151742298d61d364880575bff0bdcbf4ae383f0180e7e47dd'
    JWT_TOKEN_LOCATION: list = ['headers']
    ALGORITHM: str = 'HS256'

    class Config:
        env_prefix = 'JWT_'


class MongoSettings(BaseConfig):
    HOST: str = 'localhost'
    PORT: int = 27017
    DB: str = 'booking_reviews'
    COLLECTION: str = 'reviews'

    class Config:
        env_prefix = 'MONGO_'

    @property
    def uri(self) -> MongoDsn:
        return f'mongodb://{self.HOST}:{self.PORT}'


class ProjectSettings(BaseConfig):
    PROJECT_NAME: str = 'Graduate_work'
    BASE_DIR = Path(__file__).parent.parent
    logging: LoggingSettings = LoggingSettings()
    debug: DebugSettings = DebugSettings()
    fastapi: FastapiSettings = FastapiSettings()
    jwt: JWTSettings = JWTSettings()
    mongo: MongoSettings = MongoSettings()


settings = ProjectSettings()
