from pathlib import Path

from pydantic import BaseSettings


class BaseConfig(BaseSettings):
    class Config:
        env_file = Path(Path(__file__).parent.parent.parent.parent.parent.parent, 'env')
        env_file_encoding = 'utf-8'


class LogingSettings(BaseConfig):
    SENTRY_DSN: str = ''
    LOGSTAH_HOST: str = 'logstash'
    LOGSTAH_PORT: int = 5044

    class Config:
        env_prefix = 'LOGGING_'


class DebugSettings(BaseConfig):
    DEBUG: bool = True

    class Config:
        env_prefix = 'DEBUG_'


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


class FastapiSetting(BaseConfig):
    HOST: str = 'localhost'
    PORT: int = 8080
    API_PREFIX: str = '/app/v1'

    class Config:
        env_prefix = 'FASTAPI_'


class ProjectSettings(BaseConfig):
    PROJECT_NAME: str = 'Graduate_work'
    BASE_DIR = Path(__file__).parent.parent
    logging: LogingSettings = LogingSettings()
    debug: DebugSettings = DebugSettings()
    postgres: PostgresSettings = PostgresSettings()
    fastapi: FastapiSetting = FastapiSetting()


settings = ProjectSettings()
