from fastapi import Request
from fastapi.responses import JSONResponse


class NotFoundError(Exception):
    pass


class ShortIdGenerationError(Exception):
    """Исключение при исчерпании попыток генерации уникального short_id."""

    pass


def not_found_handler(_request: Request, exc: NotFoundError) -> JSONResponse:
    return JSONResponse(status_code=404, content={'detail': str(exc)})
