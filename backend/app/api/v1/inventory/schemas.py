from datetime import datetime, date

from pydantic import BaseModel, ConfigDict


class InventoryItemBase(BaseModel):
    category: str
    brand: str
    name: str
    value: str | None = None
    repurchase: bool | None = None
    expired_date: date | None = None


class InventoryItemCreate(InventoryItemBase):
    pass


class InventoryItemUpdate(BaseModel):
    """All fields optional — used for PATCH (partial update)."""

    category: str | None = None
    brand: str | None = None
    name: str | None = None
    value: str | None = None
    repurchase: bool | None = None
    expired_date: date | None = None


class InventoryItemReplace(InventoryItemBase):
    """All base fields required — used for PUT (full replace)."""

    pass


class InventoryItemResponse(InventoryItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: datetime
    updated_at: datetime
