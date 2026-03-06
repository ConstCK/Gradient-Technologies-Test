from core.constants import SHORT_LINK_PREFIX


def normalize_short_id(short_id: str) -> str:
    """Возвращает короткий идентификатор в едином виде — без префикса gradient-technologies/ (если был — удаляется, если не был — строка без изменений)."""
    return short_id.removeprefix(SHORT_LINK_PREFIX)
