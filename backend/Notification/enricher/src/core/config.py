from pathlib import Path

from pydantic import BaseSettings


class BaseConfig(BaseSettings):
    class Config:
        env_file = Path(Path(__file__).parent.parent.parent.parent.parent, 'env')
        env_file_encoding = 'utf-8'


class FastapiSetting(BaseConfig):
    HOST: str = 'localhost'
    PORT: int = 8080
    NOTIFIC_PREFIX: str = '/app/v1/notification'

    @property
    def uri(self):
        return f'http://{self.HOST}:{self.PORT}{self.NOTIFIC_PREFIX}'

    class Config:
        env_prefix = 'FASTAPI_'


class LogingSettings(BaseConfig):
    SENTRY_DSN: str = ''
    LOGSTAH_HOST: str = 'logstash'
    LOGSTAH_PORT: int = 5046

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
    MAX_RETRY_COUNT: int = 3

    @property
    def uri(self):
        return f'amqp://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}'

    class Config:
        env_prefix = 'RABBIT_'


class JWTSettings(BaseConfig):
    SECRET_KEY: str = '245585dbb5cbe2f151742298d61d364880575bff0bdcbf4ae383f0180e7e47dd'
    JWT_TOKEN_LOCATION: list = ['headers']
    ALGORITHM: str = 'HS256'

    class Config:
        env_prefix = 'JWT_'


class AuthMock(BaseConfig):
    HOST: str = 'localhost'
    PORT: int = 8081
    PREFIX: str = '/auth/v1/'

    @property
    def uri(self):
        return f'http://{self.HOST}:{self.PORT}{self.PREFIX}'

    class Config:
        env_prefix = 'AUTH_MOCK_'


class AdminPanelMock(BaseConfig):
    HOST: str = 'localhost'
    PORT: int = 8082
    PREFIX: str = '/admin_panel/v1/'

    @property
    def uri(self):
        return f'http://{self.HOST}:{self.PORT}{self.PREFIX}'

    class Config:
        env_prefix = 'ADMIN_PANEL_MOCK_'


class UGCMock(BaseConfig):
    HOST: str = 'localhost'
    PORT: int = 8083
    PREFIX: str = '/ugc/v1/'

    @property
    def uri(self):
        return f'http://{self.HOST}:{self.PORT}{self.PREFIX}'

    class Config:
        env_prefix = 'UGC_MOCK_'


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


class RedisSettings(BaseConfig):
    HOST: str = 'localhost'
    PORT: int = 6379
    INDEX_ENRICH: int = 0
    EXPIRE_SEC: int = 5 * 60  # 5 minutes

    @property
    def uri(self):
        return f'redis://{self.HOST}:{self.PORT}/{self.INDEX_ENRICH}'

    class Config:
        env_prefix = 'REDIS_'


class URLShortnerSettings(BaseConfig):
    HOST: str = 'localhost'
    PORT: int = 3000
    PREFIX: str = '/api/v1/shortener/'
    DEBUG: bool = True
    TESTING: bool = True
    ID_LENGTH: int = 8
    REDIRECT_URL: str = FastapiSetting().uri

    @property
    def uri(self):
        return f'http://{self.HOST}:{self.PORT}{self.PREFIX}'

    class Config:
        env_prefix = 'URLSHORT_'


class DebugSettings(BaseConfig):
    DEBUG: bool = True


class ProjectSettings(BaseConfig):
    PROJECT_NAME: str = 'Notification_api'
    BASE_DIR = Path(__file__).parent.parent
    fastapi: FastapiSetting = FastapiSetting()
    rabbit: RabbitMQSetting = RabbitMQSetting()
    jwt: JWTSettings = JWTSettings()
    auth: AuthMock = AuthMock()
    admin_panel: AdminPanelMock = AdminPanelMock()
    ugc: UGCMock = UGCMock()
    logging: LogingSettings = LogingSettings()
    postgres: PostgresSettings = PostgresSettings()
    redis: RedisSettings = RedisSettings()
    url_shortner: URLShortnerSettings = URLShortnerSettings()
    debug: DebugSettings = DebugSettings()


settings = ProjectSettings()
