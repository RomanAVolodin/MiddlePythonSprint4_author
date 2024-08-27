import os

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Redis(BaseModel):
    host: str = Field(default='redis')
    port: int = Field(default=6379)


class Elastic(BaseModel):
    host: str = Field(default='elastic')
    port: int = Field(default=9200)
    scheme: str = Field(default='http')

    movies_index: str = Field(default='movies')
    movies_index_filename: str = Field(default='tests/functional/testdata/indexes/movies_index.json')
    genres_index: str = Field(default='genres')
    genres_index_filename: str = Field(default='tests/functional/testdata/indexes/genres_index.json')
    persons_index: str = Field(default='persons')
    persons_index_filename: str = Field(default='tests/functional/testdata/indexes/persons_index.json')

    def get_host(self):
        return f'{self.scheme}://{self.host}:{self.port}'


class TestSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env'),
        env_file_encoding='utf-8',
        env_nested_delimiter='__',
        env_prefix='FASTAPI__',
    )

    project_name: str = Field(default='movies')
    service_url: str = Field(default='http://fastapi:8000')
    redis_settings: Redis
    elastic_settings: Elastic
    log_level: str = Field(default='DEBUG')


test_settings = TestSettings()
