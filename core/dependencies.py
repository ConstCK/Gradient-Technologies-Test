from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from services.link_service import LinkService

DbSession = Annotated[AsyncSession, Depends(get_db)]


def get_link_service(session: DbSession) -> LinkService:
    return LinkService(session)


LinkServiceDep = Annotated[LinkService, Depends(get_link_service)]
