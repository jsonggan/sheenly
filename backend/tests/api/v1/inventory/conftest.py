import pytest

from app.api.v1.inventory.schemas import InventoryItemCreate
from app.api.v1.inventory import services


@pytest.fixture
def sample_item(db):
    payload = InventoryItemCreate(
        name="Foundation",
        category="Face",
        brand="MAC",
        value="30ml",
        repurchase=True,
    )
    return services.create_item(db, payload)
