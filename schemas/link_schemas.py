from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class LinkCreate(BaseModel):
    """Тело запроса на сокращение ссылки."""

    model_config = ConfigDict(
        json_schema_extra={
            'examples': [
                {'url': 'https://example.com/some-page'},
                {'url': 'https://github.com'},
            ],
        },
    )

    url: HttpUrl = Field(description='Исходный URL для сокращения')


class LinkRead(BaseModel):
    """Ответ с созданной короткой ссылкой."""

    model_config = ConfigDict(from_attributes=True)

    short_id: str = Field(description='Короткий идентификатор (с префиксом)')
    original_url: str = Field(description='Исходный URL')


class LinkStatsRead(BaseModel):
    """Статистика переходов по короткой ссылке."""

    model_config = ConfigDict(from_attributes=True)

    short_id: str = Field(description='Короткий идентификатор')
    clicks: int = Field(description='Количество переходов')
