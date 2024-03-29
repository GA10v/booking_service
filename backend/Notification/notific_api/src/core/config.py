from pathlib import Path
from random import choice
from string import ascii_letters

from pydantic import BaseSettings


class BaseConfig(BaseSettings):
    class Config:
        env_file = Path(Path(__file__).parent.parent.parent.parent, 'env')
        env_file_encoding = 'utf-8'


class FastapiSetting(BaseConfig):
    HOST: str = 'localhost'
    PORT: int = 8070
    NOTIFIC_PREFIX: str = '/app/v1/notification'

    class Config:
        env_prefix = 'FASTAPI_'


class LoggingSettings(BaseConfig):
    SENTRY_DSN: str = ''
    LOGSTASH_HOST: str = 'logstash'
    LOGSTASH_PORT: int = 5044

    class Config:
        env_prefix = 'LOGGING_'


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

    @property
    def uri(self):
        return f'amqp://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}'

    class Config:
        env_prefix = 'RABBIT_'


class JWTSettings(BaseConfig):
    SECRET_KEY: str = ''.join(choice(ascii_letters) for _ in range(200))
    JWT_TOKEN_LOCATION: list = ['headers']
    ALGORITHM: str = 'HS256'

    class Config:
        env_prefix = 'JWT_'


class DebugSettings(BaseConfig):
    DEBUG: bool = True
    TEST_EMAIL: list[str] = ['admin@admin.ru']

    class Config:
        env_prefix = 'DEBUG_'


class BookingSettings(BaseConfig):
    HOST: str = 'localhost'
    PORT: int = 8080
    API_PREFIX: str = '/app/v1'
    FAKE_ANNOUNCE: str = 'eca370e7-c65d-44f3-b390-5c2733df02e6'
    FAKE_BOOKING: str = 'c1fb843b-de80-46c5-b0e7-95e15a88b407'

    @property
    def uri(self):
        return f'http://{self.HOST}:{self.PORT}{self.API_PREFIX}'

    def announce_uri(self):
        return f'{self.uri}/announcement/'

    class Config:
        env_prefix = 'BOOKING_'


class ProjectSettings(BaseConfig):
    PROJECT_NAME: str = 'Notification_api'
    BASE_DIR = Path(__file__).parent.parent
    fastapi: FastapiSetting = FastapiSetting()
    rabbit: RabbitMQSetting = RabbitMQSetting()
    logging: LoggingSettings = LoggingSettings()
    jwt: JWTSettings = JWTSettings()
    debug: DebugSettings = DebugSettings()
    booking: BookingSettings = BookingSettings()


settings = ProjectSettings()
