from datetime import datetime, timezone

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base


class Link(Base):
    __tablename__ = 'links'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    original_url: Mapped[str] = mapped_column(String(2048), unique=True, nullable=False)
    short_id: Mapped[str] = mapped_column(String(16), unique=True, index=True, nullable=False)
    clicks: Mapped[int] = mapped_column(default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc).replace(tzinfo=None),
        nullable=False,
    )

    def __repr__(self) -> str:
        return f'<Link id={self.id} short_id={self.short_id!r}>'
