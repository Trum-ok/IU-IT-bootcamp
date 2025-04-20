import os

from dotenv import load_dotenv


def load_env(config_path: str) -> None:
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")
    load_dotenv(config_path, override=True)


class Config:
    def __init__(self, config_path: str):
        load_env(config_path)
        self._token: str | None = None

    @property
    def token(self):
        if self._token is None:
            self._token = os.environ["TG_TOKEN"]
        return self._token
