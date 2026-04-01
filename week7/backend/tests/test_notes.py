def test_create_list_and_patch_notes(client):
    payload = {"title": "Test", "content": "Hello world"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["title"] == "Test"
    assert "created_at" in data and "updated_at" in data

    r = client.get("/notes/")
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    r = client.get("/notes/", params={"q": "Hello", "limit": 10, "sort": "-created_at"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    note_id = data["id"]
    r = client.patch(f"/notes/{note_id}", json={"title": "Updated"})
    assert r.status_code == 200
    patched = r.json()
    assert patched["title"] == "Updated"


def test_search_notes_valid_and_invalid_payloads(client):
    # Seed a couple of notes
    payload = {"title": "Searchable", "content": "This is a searchable note"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201, r.text

    # Happy path search
    search_payload = {"query": "searchable", "limit": 10, "sort": "-created_at"}
    r = client.post("/notes/search", json=search_payload)
    assert r.status_code == 200, r.text
    results = r.json()
    assert len(results) >= 1
    assert any("Searchable" == note["title"] for note in results)

    # Invalid sort should trigger validation error
    bad_sort_payload = {"query": "searchable", "sort": "invalid_field"}
    r = client.post("/notes/search", json=bad_sort_payload)
    assert r.status_code == 422

    # Empty query should trigger validation error
    empty_query_payload = {"query": "   "}
    r = client.post("/notes/search", json=empty_query_payload)
    assert r.status_code == 422

