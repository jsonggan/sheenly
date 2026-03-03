from datetime import date

import pytest
from pydantic import ValidationError

from app.api.v1.inventory.schemas import (
    InventoryItemCreate,
    InventoryItemUpdate,
    InventoryItemReplace,
)


class TestInventoryItemCreate:
    def test_valid_minimal_payload(self):
        item = InventoryItemCreate(name="Bulb", category="Lighting", brand="Sheenly")
        assert item.name == "Bulb"
        assert item.repurchase is None
        assert item.expired_date is None

    def test_valid_full_payload(self):
        item = InventoryItemCreate(
            name="Bulb",
            category="Lighting",
            brand="Sheenly",
            value="10W",
            repurchase=True,
            expired_date=date(2027, 1, 1),
        )
        assert item.repurchase is True
        assert item.expired_date == date(2027, 1, 1)

    def test_missing_required_fields_raises(self):
        with pytest.raises(ValidationError):
            InventoryItemCreate(name="Bulb")

    def test_missing_brand_raises(self):
        with pytest.raises(ValidationError):
            InventoryItemCreate(name="Bulb", category="Lighting")


class TestInventoryItemUpdate:
    def test_all_fields_optional(self):
        item = InventoryItemUpdate()
        assert item.name is None
        assert item.category is None

    def test_partial_fields_accepted(self):
        item = InventoryItemUpdate(name="New Name")
        assert item.name == "New Name"
        assert item.brand is None


class TestInventoryItemReplace:
    def test_requires_all_base_fields(self):
        with pytest.raises(ValidationError):
            InventoryItemReplace(name="Bulb")

    def test_valid_replace_payload(self):
        item = InventoryItemReplace(name="Bulb", category="Lighting", brand="Sheenly")
        assert item.name == "Bulb"
