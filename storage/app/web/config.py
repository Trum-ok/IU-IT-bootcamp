import os
import typing
from dataclasses import dataclass

from dotenv import load_dotenv

if typing.TYPE_CHECKING:
    from app.web.app import Application


def load_env(config_path: str) -> None:
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")
    load_dotenv(config_path, override=True)


@dataclass
class DataBaseConfig:
    user: str
    password: str
    host: str | None = "127.0.0.1"
    port: int | None = 5432
    db_name: str | None = "postgre"

    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}"


class Config:
    def __init__(self, config_path: str):
        load_env(config_path)
        self._db_config: DataBaseConfig | None = None

    @property
    def db(self) -> DataBaseConfig:
        if self._db_config is None:
            self._db_config = DataBaseConfig(
                user=self.__get_env_var("PG_NAME"),
                password=self.__get_env_var("PG_PASSWORD"),
                host=os.getenv("PG_HOST", "127.0.0.1"),
                port=int(os.getenv("PG_PORT", "5432")),
                db_name=self.__get_env_var("PG_DB"),
            )
        return self._db_config

    def __get_env_var(self, var_name: str) -> str:
        value = os.getenv(var_name)
        if value is None:
            raise ValueError(f"Environment variable {var_name} is not set")
        return value


def setup_alembic_config(config_path: str):
    return DataBaseConfig(config_path)


def setup_config(app: "Application", config_path: str):
    app.config = Config(
        db=DataBaseConfig(config_path),
    )
