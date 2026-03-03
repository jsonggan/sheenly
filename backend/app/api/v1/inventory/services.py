from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models import InventoryItem
from app.api.v1.inventory.schemas import (
    InventoryItemCreate,
    InventoryItemReplace,
    InventoryItemUpdate,
)


def list_items(
    db: Session,
    category: Optional[str],
    brand: Optional[str],
    repurchase: Optional[bool],
) -> list[InventoryItem]:
    query = db.query(InventoryItem)
    if category is not None:
        query = query.filter(InventoryItem.category == category)
    if brand is not None:
        query = query.filter(InventoryItem.brand == brand)
    if repurchase is not None:
        query = query.filter(InventoryItem.repurchase == repurchase)
    return query.all()


def create_item(db: Session, payload: InventoryItemCreate) -> InventoryItem:
    item = InventoryItem(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def get_item(db: Session, item_id: str) -> InventoryItem:
    item = db.get(InventoryItem, item_id)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    return item


def replace_item(
    db: Session, item_id: str, payload: InventoryItemReplace
) -> InventoryItem:
    item = get_item(db, item_id)
    for field, value in payload.model_dump().items():
        setattr(item, field, value)
    db.commit()
    db.refresh(item)
    return item


def update_item(
    db: Session, item_id: str, payload: InventoryItemUpdate
) -> InventoryItem:
    item = get_item(db, item_id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(item, field, value)
    db.commit()
    db.refresh(item)
    return item


def delete_item(db: Session, item_id: str) -> None:
    item = get_item(db, item_id)
    db.delete(item)
    db.commit()
