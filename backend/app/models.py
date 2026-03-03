import uuid
from datetime import datetime, date

from sqlalchemy import String, Boolean, Date, DateTime, Index
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


def _now() -> datetime:
    return datetime.utcnow()


class InventoryItem(Base):
    __tablename__ = "inventory_items"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    brand: Mapped[str] = mapped_column(String(100), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    value: Mapped[str | None] = mapped_column(String(200), nullable=True)
    repurchase: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    expired_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=_now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=_now, onupdate=_now
    )

    __table_args__ = (
        Index("ix_inventory_items_category", "category"),
        Index("ix_inventory_items_brand", "brand"),
        Index("ix_inventory_items_expired_date", "expired_date"),
        Index("ix_inventory_items_repurchase", "repurchase"),
    )

    def __repr__(self) -> str:
        return (
            f"<InventoryItem id={self.id!r} "
            f"category={self.category!r} brand={self.brand!r} name={self.name!r}>"
        )
