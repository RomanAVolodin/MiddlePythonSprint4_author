import os
from logging import config as logging_config

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from core.logger import LOGGING

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GENRE_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут
PERSON_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут
FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут
SIZE_RESPONSE = 1000

logging_config.dictConfig(LOGGING)


class Redis(BaseModel):
    host: str = Field(...)
    port: int = Field(...)


class Elastic(BaseModel):
    host: str = Field(...)
    port: int = Field(default=9200)
    scheme: str = Field(default='http')

    def get_host(self):
        return f'{self.scheme}://{self.host}:{self.port}'


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env'),
        env_file_encoding='utf-8',
        env_nested_delimiter='__',
        env_prefix='FASTAPI__',
    )

    project_name: str = Field(default='Some project name')
    redis_settings: Redis
    elastic_settings: Elastic


settings = Settings()
