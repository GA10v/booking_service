from pathlib import Path

from pydantic import BaseSettings


class BaseConfig(BaseSettings):
    class Config:
        env_file = Path(Path(__file__).parent.parent.parent.parent.parent.parent, '.env')
        env_file_encoding = 'utf-8'


class FastapiSettings(BaseConfig):
    HOST: str = 'localhost'
    PORT: int = 8080
    API_PREFIX: str = '/app/v1'

    @property
    def service_url(self):
        return f'http://{self.HOST}:{self.PORT}{self.API_PREFIX}'

    @property
    def test_ok(self):
        return f'{self.service_url}/ping'

    class Config:
        env_prefix = 'TEST_FASTAPI_'


class ProjectSettings(BaseConfig):
    PROJECT_NAME: str = 'Graduate_work'
    BASE_DIR = Path(__file__).parent.parent
    fastapi: FastapiSettings = FastapiSettings()


settings = ProjectSettings()
