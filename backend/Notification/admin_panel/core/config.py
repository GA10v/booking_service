"""Module to store settings for django admin panel."""
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

    @property
    def uri(self):
        return f'amqp://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}'

    class Config:
        env_prefix = 'RABBIT_'


class DjangoSettings(BaseConfig):
    SECRET_KEY: str = 'sr2GPU6c5TxoEkqtnJCCNLPTs3ccyiwwBlETV2VmxfhUejVm9HlJhtHUIFANwjQbR'
    POSTGRES_PASSWORD: str = 'guest'
    POSTGRES_USER: str = 'guest'
    POSTGRES_DB: str = 'db_name'
    POSTGRES_HOST: str = 'postgres'
    POSTGRES_PORT: int = 5432
    ALLOWED_HOSTS: list[str] = ['*']  # ['127.0.0.1', 'localhost']
    DEBUG: bool = True

    @property
    def uri(self):
        return (
            f'postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}'
            f'@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}'
        )

    @property
    def db_creds(self):
        return {
            'dbname': self.POSTGRES_DB,
            'user': self.POSTGRES_USER,
            'password': self.POSTGRES_PASSWORD,
            'host': self.POSTGRES_HOST,
            'port': self.POSTGRES_PORT,
        }

    class Config:
        env_prefix = 'DJANGO_'


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

    @property
    def group_id_uri(self):
        return f'http://{self.HOST}:{self.PORT}{self.PREFIX}user_group/'

    @property
    def user_data_uri(self):
        return f'http://{self.HOST}:{self.PORT}{self.PREFIX}user_info/'

    class Config:
        env_prefix = 'AUTH_MOCK_'


class UGCMock(BaseConfig):
    HOST: str = 'localhost'
    PORT: int = 8083
    PREFIX: str = '/ugc/v1/'

    @property
    def uri(self):
        return f'http://{self.HOST}:{self.PORT}{self.PREFIX}'

    @property
    def subscribers_uri(self):
        return f'http://{self.HOST}:{self.PORT}{self.PREFIX}subscribers/'

    @property
    def likes_count_uri(self):
        return f'http://{self.HOST}:{self.PORT}{self.PREFIX}likes_count/'

    class Config:
        env_prefix = 'UGC_MOCK_'


class FastapiSetting(BaseConfig):
    HOST: str = 'localhost'
    PORT: int = 8080
    NOTIFIC_PREFIX: str = '/app/v1/notification'

    @property
    def uri(self):
        return f'http://{self.HOST}:{self.PORT}{self.NOTIFIC_PREFIX}'

    @property
    def send_uri(self):
        return f'http://{self.HOST}:{self.PORT}{self.NOTIFIC_PREFIX}/send'

    class Config:
        env_prefix = 'FASTAPI_'


class ProjectSettings(BaseConfig):
    django: DjangoSettings = DjangoSettings()
    rabbit: RabbitMQSetting = RabbitMQSetting()
    jwt: JWTSettings = JWTSettings()
    auth: AuthMock = AuthMock()
    ugc: UGCMock = UGCMock()
    api: FastapiSetting = FastapiSetting()


settings = ProjectSettings()
