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
    ANNOUNCE_BLANK: str = '0be54aaa-cb63-415b-8435-0d55848eee11'
    ANNOUNCE: str = 'eca370e7-c65d-44f3-b390-5c2733df02e6'
    BOOKING_G1: str = '88a23816-2be5-4faa-add9-ce3d2e3efd4c'
    BOOKING_G2: str = 'c1fb843b-de80-46c5-b0e7-95e15a88b407'
    MOVIE: str = '8f1a49f0-0319-4589-9130-08bad05a1d3b'
    USER: str = '6c162475-c7ed-4461-9184-001ef3d9f264'
    AUTHOR: str = '50760ee6-2073-445d-ad25-f665937f3b33'
    GUEST_1: str = '39e60237-83ea-4c65-9bc9-f6b47d109738'
    GUEST_2: str = 'd0c5635c-3211-4cf8-94ab-cbe6800771c4'
    SUDO: str = 'a5a8f573-3cee-4ccc-8a2b-91cb9f55250a'


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
