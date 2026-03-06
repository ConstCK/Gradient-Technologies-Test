from fastapi import APIRouter, status

router = APIRouter(prefix='/health', tags=['health'])


@router.get(
    '',
    summary='Проверка доступности',
    description='Проверка доступности сервиса',
    responses={
        status.HTTP_200_OK: {'description': 'Сервис доступен'},
    },
)
async def health_check() -> dict[str, str]:
    return {'status': 'ok'}
