from typing import Optional

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.api.v1.inventory.schemas import (
    InventoryItemCreate,
    InventoryItemReplace,
    InventoryItemUpdate,
    InventoryItemResponse,
)
from app.api.v1.inventory import services

router = APIRouter()


@router.get("", response_model=list[InventoryItemResponse])
def list_inventory(
    category: Optional[str] = None,
    brand: Optional[str] = None,
    repurchase: Optional[bool] = None,
    db: Session = Depends(get_db),
):
    return services.list_items(db, category, brand, repurchase)


@router.post(
    "", response_model=InventoryItemResponse, status_code=status.HTTP_201_CREATED
)
def create_inventory_item(payload: InventoryItemCreate, db: Session = Depends(get_db)):
    return services.create_item(db, payload)


@router.get("/{item_id}", response_model=InventoryItemResponse)
def get_inventory_item(item_id: str, db: Session = Depends(get_db)):
    return services.get_item(db, item_id)


@router.put("/{item_id}", response_model=InventoryItemResponse)
def replace_inventory_item(
    item_id: str, payload: InventoryItemReplace, db: Session = Depends(get_db)
):
    return services.replace_item(db, item_id, payload)


@router.patch("/{item_id}", response_model=InventoryItemResponse)
def update_inventory_item(
    item_id: str, payload: InventoryItemUpdate, db: Session = Depends(get_db)
):
    return services.update_item(db, item_id, payload)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_inventory_item(item_id: str, db: Session = Depends(get_db)):
    services.delete_item(db, item_id)
