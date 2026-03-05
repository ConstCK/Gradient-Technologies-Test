import logging
import secrets

from sqlalchemy.ext.asyncio import AsyncSession

from core.constants import MAX_COLLISION_RETRIES, SHORT_ID_LENGTH
from models.link import Link
from repositories.link_repository import LinkRepository

logger = logging.getLogger(__name__)


class LinkService:
    def __init__(self, session: AsyncSession) -> None:
        self._repo = LinkRepository(session)

    def _generate_short_id(self) -> str:
        return secrets.token_urlsafe(SHORT_ID_LENGTH)[:SHORT_ID_LENGTH]

    async def shorten(self, original_url: str) -> Link:
        existing = await self._repo.get_by_original_url(original_url)
        if existing is not None:
            logger.info('Возвращена существующая ссылка short_id=%s', existing.short_id)
            return existing
        for _ in range(MAX_COLLISION_RETRIES):
            suffix = self._generate_short_id()
            existing = await self._repo.get_by_short_id(suffix)
            if existing is None:
                link = await self._repo.create(original_url=original_url, short_id=suffix)
                logger.info('Создана короткая ссылка short_id=%s', suffix)
                return link
        raise RuntimeError('Не удалось сгенерировать уникальный short_id')

    async def get_original_url(self, short_id: str) -> str | None:
        link = await self._repo.get_by_short_id(short_id)
        return link.original_url if link else None

    async def record_click(self, short_id: str) -> str | None:
        link = await self._repo.get_by_short_id(short_id)
        if link is None:
            return None
        await self._repo.increment_clicks(link)
        return link.original_url

    async def get_stats(self, short_id: str) -> int | None:
        link = await self._repo.get_by_short_id(short_id)
        return link.clicks if link else None
