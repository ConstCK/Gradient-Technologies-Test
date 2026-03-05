from core.constants import SHORT_LINK_PREFIX


def ensure_short_id_prefix(short_id: str) -> str:
    """Возвращает short_id с префиксом (для поиска в БД)."""
    return short_id if short_id.startswith(SHORT_LINK_PREFIX) else SHORT_LINK_PREFIX + short_id
