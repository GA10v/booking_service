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


class JWTSettings(BaseConfig):
    SECRET_KEY: str = '245585dbb5cbe2f151742298d61d364880575bff0bdcbf4ae383f0180e7e47dd'
    JWT_TOKEN_LOCATION: list = ['headers']
    ALGORITHM: str = 'HS256'

    class Config:
        env_prefix = 'JWT_'


class TestDataSettings(BaseConfig):
    USER: str = '6c162475-c7ed-4461-9184-001ef3d9f264'
    MODERATOR: str = 'a5a8f573-3cee-4ccc-8a2b-91cb9f55250a'


class DebugSettings(BaseConfig):
    DEBUG: bool = False

    class Config:
        env_prefix = 'TEST_'


class ProjectSettings(BaseConfig):
    PROJECT_NAME: str = 'Graduate_work'
    BASE_DIR = Path(__file__).parent.parent
    fastapi: FastapiSettings = FastapiSettings()
    jwt: JWTSettings = JWTSettings()
    data: TestDataSettings = TestDataSettings()
    debug: DebugSettings = DebugSettings()


settings = ProjectSettings()
