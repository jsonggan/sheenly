BASE_URL = "/api/v1/inventory"

CREATE_PAYLOAD = {
    "name": "Foundation",
    "category": "Face",
    "brand": "MAC",
    "value": "30ml",
    "repurchase": True,
}


class TestListInventory:
    def test_returns_empty_list(self, client):
        response = client.get(BASE_URL)
        assert response.status_code == 200
        assert response.json() == []

    def test_returns_existing_items(self, client, sample_item):
        response = client.get(BASE_URL)
        assert response.status_code == 200
        assert len(response.json()) == 1

    def test_filter_by_category(self, client, sample_item):
        response = client.get(BASE_URL, params={"category": "Face"})
        assert response.status_code == 200
        assert len(response.json()) == 1

    def test_filter_by_category_no_match(self, client, sample_item):
        response = client.get(BASE_URL, params={"category": "NonExistent"})
        assert response.status_code == 200
        assert response.json() == []

    def test_filter_by_repurchase(self, client, sample_item):
        response = client.get(BASE_URL, params={"repurchase": True})
        assert response.status_code == 200
        assert len(response.json()) == 1


class TestCreateInventoryItem:
    def test_creates_item(self, client):
        response = client.post(BASE_URL, json=CREATE_PAYLOAD)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Foundation"
        assert data["category"] == "Face"
        assert data["brand"] == "MAC"
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data

    def test_missing_required_field_returns_422(self, client):
        response = client.post(BASE_URL, json={"name": "No Category"})
        assert response.status_code == 422


class TestGetInventoryItem:
    def test_get_existing_item(self, client, sample_item):
        response = client.get(f"{BASE_URL}/{sample_item.id}")
        assert response.status_code == 200
        assert response.json()["id"] == sample_item.id

    def test_get_nonexistent_item_returns_404(self, client):
        response = client.get(f"{BASE_URL}/nonexistent-id")
        assert response.status_code == 404


class TestReplaceInventoryItem:
    def test_replaces_item(self, client, sample_item):
        payload = {
            "name": "Updated Foundation",
            "category": "Face",
            "brand": "MAC",
            "repurchase": False,
        }
        response = client.put(f"{BASE_URL}/{sample_item.id}", json=payload)
        assert response.status_code == 200
        assert response.json()["name"] == "Updated Foundation"
        assert response.json()["repurchase"] is False

    def test_replace_nonexistent_item_returns_404(self, client):
        response = client.put(f"{BASE_URL}/nonexistent-id", json=CREATE_PAYLOAD)
        assert response.status_code == 404


class TestUpdateInventoryItem:
    def test_partial_update(self, client, sample_item):
        response = client.patch(
            f"{BASE_URL}/{sample_item.id}", json={"name": "Patched Foundation"}
        )
        assert response.status_code == 200
        assert response.json()["name"] == "Patched Foundation"
        assert response.json()["brand"] == sample_item.brand

    def test_update_nonexistent_item_returns_404(self, client):
        response = client.patch(f"{BASE_URL}/nonexistent-id", json={"name": "X"})
        assert response.status_code == 404


class TestDeleteInventoryItem:
    def test_deletes_item(self, client, sample_item):
        response = client.delete(f"{BASE_URL}/{sample_item.id}")
        assert response.status_code == 204

    def test_item_gone_after_delete(self, client, sample_item):
        client.delete(f"{BASE_URL}/{sample_item.id}")
        response = client.get(f"{BASE_URL}/{sample_item.id}")
        assert response.status_code == 404

    def test_delete_nonexistent_item_returns_404(self, client):
        response = client.delete(f"{BASE_URL}/nonexistent-id")
        assert response.status_code == 404
