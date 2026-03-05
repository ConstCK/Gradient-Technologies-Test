from typing import Annotated

from fastapi import APIRouter, Body, HTTPException, Path, status
from fastapi.responses import RedirectResponse

from core.constants import SHORT_LINK_PREFIX
from core.dependencies import LinkServiceDep
from schemas.link_schemas import LinkCreate, LinkRead, LinkStatsRead
from utils.link_utils import normalize_short_id


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
    return LinkRead(
        short_id=SHORT_LINK_PREFIX + link.short_id,
        original_url=link.original_url,
    )


@router.get(
    '/stats/{short_id:path}',
    description='Получить количество переходов по короткой ссылке. Идентификатор можно передать с префиксом gradient-technologies/ или без — префикс будет удалён.',
    response_model=LinkStatsRead,
    responses={
        status.HTTP_200_OK: {'description': 'Статистика по ссылке'},
        status.HTTP_404_NOT_FOUND: {'description': 'Ссылка не найдена'},
    },
)
async def stats(
    short_id: Annotated[str, Path(description='Короткий идентификатор (без префикса или gradient-technologies/...)')],
    service: LinkServiceDep,
) -> LinkStatsRead:
    key = normalize_short_id(short_id)
    clicks = await service.get_stats(key)
    if clicks is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Ссылка не найдена')
    return LinkStatsRead(short_id=SHORT_LINK_PREFIX + key, clicks=clicks)


@router.get(
    '/{short_id:path}',
    description='Редирект на оригинальную ссылку',
    responses={
        status.HTTP_302_FOUND: {'description': 'Редирект на оригинал'},
        status.HTTP_404_NOT_FOUND: {'description': 'Ссылка не найдена'},
    },
)
async def redirect_to_original(
    short_id: Annotated[str, Path(description='Короткий идентификатор (без префикса или с префиксом — будет очищен)')],
    service: LinkServiceDep,
) -> RedirectResponse:
    key = normalize_short_id(short_id)
    original_url = await service.record_click(key)
    if original_url is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Ссылка не найдена')
    return RedirectResponse(url=original_url, status_code=status.HTTP_302_FOUND)
