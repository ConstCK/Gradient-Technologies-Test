"""Хелперы для описания ответов в OpenAPI (Swagger)."""


def error_response(description: str, detail: str | list) -> dict:
    """Описание ответа с ошибкой для OpenAPI (description + example body)."""
    return {
        'description': description,
        'content': {'application/json': {'example': {'detail': detail}}},
    }


# Пример тела 422 от валидации Pydantic (массив ошибок)
VALIDATION_ERROR_422_EXAMPLE = [
    {
        'type': 'url_parsing',
        'loc': ['body', 'url'],
        'msg': 'Input should be a valid URL or URL string',
        'input': 'not-a-url',
    },
]
