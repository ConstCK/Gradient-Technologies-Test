from typing import Annotated

from fastapi import APIRouter, Body, HTTPException, Path, status
from fastapi.responses import RedirectResponse

from core.constants import SHORT_LINK_PREFIX
from core.dependencies import LinkServiceDep
from schemas.link_schemas import LinkCreate, LinkRead, LinkStatsRead
from utils.link_utils import ensure_short_id_prefix


router = APIRouter(tags=['links'])


@router.post(
    '/shorten',
    description='Сократить длинную ссылку',
    response_model=LinkRead,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {'description': 'Ссылка создана'},
        status.HTTP_400_BAD_REQUEST: {'description': 'Некорректный URL'},
    },
)
async def shorten(
    body: Annotated[LinkCreate, Body()],
    service: LinkServiceDep,
) -> LinkRead:
    link = await service.shorten(str(body.url))
    return LinkRead(short_id=link.short_id, original_url=link.original_url)


@router.get(
    '/stats/{short_id}',
    description='Получить количество переходов по короткой ссылке',
    response_model=LinkStatsRead,
    responses={
        status.HTTP_200_OK: {'description': 'Статистика по ссылке'},
        status.HTTP_404_NOT_FOUND: {'description': 'Ссылка не найдена'},
    },
)
async def stats(
    short_id: Annotated[str, Path(description='Короткий идентификатор')],
    service: LinkServiceDep,
) -> LinkStatsRead:
    key = ensure_short_id_prefix(short_id)
    clicks = await service.get_stats(key)
    if clicks is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Ссылка не найдена')
    return LinkStatsRead(short_id=key, clicks=clicks)


@router.get(
    f'/{SHORT_LINK_PREFIX.rstrip("/")}/{{short_id}}',
    description='Редирект на оригинальную ссылку',
    responses={
        status.HTTP_302_FOUND: {'description': 'Редирект на оригинал'},
        status.HTTP_404_NOT_FOUND: {'description': 'Ссылка не найдена'},
    },
)
async def redirect_to_original(
    short_id: Annotated[str, Path(description='Короткий идентификатор (суффикс)')],
    service: LinkServiceDep,
) -> RedirectResponse:
    full_id = ensure_short_id_prefix(short_id)
    original_url = await service.record_click(full_id)
    if original_url is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Ссылка не найдена')
    return RedirectResponse(url=original_url, status_code=status.HTTP_302_FOUND)
