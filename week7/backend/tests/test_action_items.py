def test_create_complete_list_and_patch_action_item(client):
    payload = {"description": "Ship it"}
    r = client.post("/action-items/", json=payload)
    assert r.status_code == 201, r.text
    item = r.json()
    assert item["completed"] is False
    assert "created_at" in item and "updated_at" in item

    r = client.put(f"/action-items/{item['id']}/complete")
    assert r.status_code == 200
    done = r.json()
    assert done["completed"] is True

    r = client.get("/action-items/", params={"completed": True, "limit": 5, "sort": "-created_at"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    r = client.patch(f"/action-items/{item['id']}", json={"description": "Updated"})
    assert r.status_code == 200
    patched = r.json()
    assert patched["description"] == "Updated"


def test_bulk_create_action_items_and_validation(client):
    # Happy path bulk create
    payload = {
        "items": [
            {"description": "Item 1"},
            {"description": "Item 2"},
        ]
    }
    r = client.post("/action-items/bulk-create", json=payload)
    assert r.status_code == 201, r.text
    items = r.json()
    assert len(items) == 2
    assert all(item["completed"] is False for item in items)

    # Empty list should fail validation
    empty_payload = {"items": []}
    r = client.post("/action-items/bulk-create", json=empty_payload)
    assert r.status_code == 422

    # Too many items should fail validation
    too_many_payload = {"items": [{"description": f"Item {i}"} for i in range(51)]}
    r = client.post("/action-items/bulk-create", json=too_many_payload)
    assert r.status_code == 422

