from core.constants import SHORT_LINK_PREFIX


def normalize_short_id(short_id: str) -> str:
    """Возвращает короткий идентификатор без префикса (для поиска в БД)."""
    if short_id.startswith(SHORT_LINK_PREFIX):
        return short_id.removeprefix(SHORT_LINK_PREFIX)
    return short_id
