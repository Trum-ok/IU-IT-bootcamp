import os

from dotenv import load_dotenv


def load_env(config_path: str) -> None:
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")
    load_dotenv(config_path, override=True)


DEFAULT_PG_PORT = 5432
DEFAULT_PG_HOST = "127.0.0.1"


class PostgreConfig:
    user: str
    password: str
    db_name: str
    port: int = DEFAULT_PG_PORT
    host: str = DEFAULT_PG_HOST

    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}"


class Config:
    def __init__(self, config_path: str):
        load_env(config_path)
        self.config_path = config_path
        self._pg: PostgreConfig | None = None

    @property
    def pg(self):
        if self._pg is None:
            load_env(self.config_path)
            self._pg = PostgreConfig()
            self._pg.user = os.environ["PG_NAME"]
            self._pg.password = os.environ["PG_PASSWORD"]
            self._pg.db_name = os.environ["PG_DB"]
            self._pg.port = int(os.environ.get("PG_PORT", DEFAULT_PG_PORT))
            self._pg.host = os.environ.get("PG_HOST", DEFAULT_PG_HOST)
        return self._pg
