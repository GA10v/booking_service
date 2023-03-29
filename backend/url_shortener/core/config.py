"""Module to store settings for url shortner."""
from pathlib import Path

from pydantic import BaseSettings


class BaseConfig(BaseSettings):
    class Config:
        env_file = Path(Path(__file__).parent.parent.parent.parent, '.env')
        env_file_encoding = 'utf-8'


class DatabaseSettings(BaseConfig):
    PASSWORD: str = 'guest'
    USER: str = 'guest'
    DB: str = 'db_name'
    HOST: str = 'postgres'
    PORT: int = 5432

    @property
    def uri(self):
        return f'postgresql+psycopg2://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DB}'

    class Config:
        env_prefix = 'POSTGRES_'


class URLShortnerSettings(BaseConfig):
    HOST: str = 'localhost'
    PORT: int = 3000
    PREFIX: str = '/api/v1/shortener/'
    DEBUG: bool = True
    TESTING: bool = True
    ID_LENGTH: int = 8

    class Config:
        env_prefix = 'URLSHORT_'


class ProjectSettings(BaseConfig):
    db: DatabaseSettings = DatabaseSettings()
    url_shortner: URLShortnerSettings = URLShortnerSettings()


settings = ProjectSettings()
