import os

os.environ['DATABASE_URL'] = 'sqlite+aiosqlite:///:memory:'

import pytest
from httpx import ASGITransport, AsyncClient

from core.database import Base, engine
from main import app
import models.link  # noqa: F401 — регистрация модели в Base.metadata


@pytest.fixture
def anyio_backend() -> str:
    return 'asyncio'


@pytest.fixture
async def _ensure_tables():
    """Создание таблиц перед тестами (lifespan при ASGI-тестах не вызывается)."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture
async def client(_ensure_tables) -> AsyncClient:
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url='http://test',
    ) as ac:
        yield ac
