from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from models.link import Link


class LinkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, original_url: str, short_id: str) -> Link:
        link = Link(original_url=original_url, short_id=short_id)
        self._session.add(link)
        await self._session.flush()
        await self._session.refresh(link)
        return link

    async def get_by_short_id(self, short_id: str) -> Link | None:
        result = await self._session.execute(select(Link).where(Link.short_id == short_id))
        return result.scalar_one_or_none()

    async def increment_clicks(self, link: Link) -> None:
        await self._session.execute(
            update(Link).where(Link.id == link.id).values(clicks=Link.clicks + 1)
        )
        await self._session.flush()
