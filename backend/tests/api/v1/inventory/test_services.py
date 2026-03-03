from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException

from app.api.v1.inventory.schemas import InventoryItemCreate, InventoryItemUpdate
from app.api.v1.inventory import services


class TestGetItem:
    def test_raises_404_when_not_found(self):
        mock_db = MagicMock()
        mock_db.get.return_value = None

        with pytest.raises(HTTPException) as exc:
            services.get_item(mock_db, "nonexistent-id")

        assert exc.value.status_code == 404
        assert exc.value.detail == "Item not found"

    def test_returns_item_when_found(self, db, sample_item):
        result = services.get_item(db, sample_item.id)
        assert result.id == sample_item.id


class TestCreateItem:
    def test_creates_item_in_db(self, db):
        payload = InventoryItemCreate(
            name="Lipstick",
            category="Lips",
            brand="Charlotte Tilbury",
        )
        item = services.create_item(db, payload)
        assert item.id is not None
        assert item.name == "Lipstick"

    def test_created_item_is_persisted(self, db):
        payload = InventoryItemCreate(
            name="Lipstick",
            category="Lips",
            brand="Charlotte Tilbury",
        )
        created = services.create_item(db, payload)
        fetched = services.get_item(db, created.id)
        assert fetched.name == "Lipstick"


class TestListItems:
    def test_returns_all_items(self, db, sample_item):
        result = services.list_items(db, None, None, None)
        assert len(result) == 1

    def test_filters_by_category(self, db, sample_item):
        result = services.list_items(db, "Face", None, None)
        assert len(result) == 1

        result = services.list_items(db, "NonExistent", None, None)
        assert len(result) == 0

    def test_filters_by_brand(self, db, sample_item):
        result = services.list_items(db, None, "MAC", None)
        assert len(result) == 1

    def test_filters_by_repurchase(self, db, sample_item):
        result = services.list_items(db, None, None, True)
        assert len(result) == 1

        result = services.list_items(db, None, None, False)
        assert len(result) == 0


class TestUpdateItem:
    def test_partial_update_only_changes_given_fields(self, db, sample_item):
        payload = InventoryItemUpdate(name="Updated Name")
        updated = services.update_item(db, sample_item.id, payload)
        assert updated.name == "Updated Name"
        assert updated.brand == sample_item.brand
        assert updated.category == sample_item.category

    def test_raises_404_for_missing_item(self, db):
        payload = InventoryItemUpdate(name="X")
        with pytest.raises(HTTPException) as exc:
            services.update_item(db, "nonexistent-id", payload)
        assert exc.value.status_code == 404


class TestDeleteItem:
    def test_deletes_item(self, db, sample_item):
        services.delete_item(db, sample_item.id)
        with pytest.raises(HTTPException) as exc:
            services.get_item(db, sample_item.id)
        assert exc.value.status_code == 404

    def test_raises_404_for_missing_item(self, db):
        with pytest.raises(HTTPException) as exc:
            services.delete_item(db, "nonexistent-id")
        assert exc.value.status_code == 404
