import logging
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


def setup_logging(level: str = 'INFO') -> None:
    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)
    fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    root = logging.getLogger()
    root.setLevel(getattr(logging, level.upper()))
    for handler in root.handlers[:]:
        root.removeHandler(handler)
    stream = logging.StreamHandler()
    stream.setFormatter(logging.Formatter(fmt))
    root.addHandler(stream)
    main_handler = logging.FileHandler(log_dir / 'main.log', encoding='utf-8')
    main_handler.setFormatter(logging.Formatter(fmt))
    root.addHandler(main_handler)
    err_handler = logging.FileHandler(log_dir / 'errors.log', encoding='utf-8')
    err_handler.setLevel(logging.ERROR)
    err_handler.setFormatter(logging.Formatter(fmt))
    root.addHandler(err_handler)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    app_name: str = 'Тестовое для "Градиент технологии"'
    debug: bool = False
    log_level: str = 'INFO'

    database_url: str = 'postgresql+asyncpg://postgres:admin@localhost:5432/gradient_test'


def get_settings() -> Settings:
    return Settings()
