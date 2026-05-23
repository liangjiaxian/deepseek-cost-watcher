from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    database_url: str = "sqlite+aiosqlite:///./data/monitor.db"
    master_key: str = ""
    app_secret: str = ""
    debug: bool = True

    deepseek_base_url: str = "https://api.deepseek.com"
    proxy_poll_interval_minutes: int = 30
    data_retention_days: int = 90

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

if settings.database_url.startswith("sqlite"):
    db_path = DATA_DIR / "monitor.db"
    settings.database_url = f"sqlite+aiosqlite:///{db_path}"
