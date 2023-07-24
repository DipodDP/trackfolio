# global configs
import os

# from pydantic import Field
# from typing import Any, Callable, Set
# from pydantic import (AliasChoices, AmqpDsn, BaseModel, Field, ImportString,
#                       PostgresDsn, RedisDsn)
# from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '../.env'))


# class Settings(BaseSettings):
class Settings():
    # model_config = SettingsConfigDict(env_file=".env", extra="ignore", )
    # auth_key: str = Field(default="Secret", validation_alias="my_auth_key")
    # db_url: str = Field(
    #     default="sqlite+aiosqlite:///" + os.path.join(basedir, "app.db")
    # )
    # test_db_url: str = ""
    # invest_token: str
    # sandbox_invest_token: str
    auth_key: str = os.environ.get('AUTH_KEY') or '\xbf\xb0\x11\xb1\xcd\xf9\xba\x8bp\x0c...'
    db_url: str = os.environ.get('DB_URL') or "sqlite+aiosqlite:///" + os.path.join(basedir, "app.db")
    test_db_url: str = os.environ.get('TEST_DB_URL') or "sqlite+aiosqlite:///" + os.path.join(basedir, "test_app.db")
    invest_token = os.environ.get('INVEST_TOKEN')
    sandbox_invest_token = os.environ.get('SANDBOX_INVEST_TOKEN')
    #

    # redis_dsn: RedisDsn = Field(
    #     "redis://user:pass@localhost:6379/1",
    #     validation_alias=AliasChoices("service_redis_dsn", "redis_url"),
    # )
    # pg_dsn: PostgresDsn = "postgres://user:pass@localhost:5432/foobar"

    # to override domains:
    # export my_prefix_domains='["foo.com", "bar.com"]'
    # domains: Set[str] = set()

    # to override more_settings:
    # export my_prefix_more_settings='{"foo": "x", "apple": 1}'
    # more_settings: SubModel = SubModel()

    # model_config = SettingsConfigDict(env_prefix="my_prefix_")


settings = Settings()
# print(settings.auth_key)
