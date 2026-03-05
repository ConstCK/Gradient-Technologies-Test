import os

import pytest
from httpx import ASGITransport, AsyncClient
from main import app

# Использование in-memory SQLite для тестов (до импорта app)
os.environ['DATABASE_URL'] = 'sqlite+aiosqlite:///:memory:'




@pytest.fixture
def anyio_backend() -> str:
    return 'asyncio'


@pytest.fixture
async def client() -> AsyncClient:
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url='http://test',
    ) as ac:
        yield ac
