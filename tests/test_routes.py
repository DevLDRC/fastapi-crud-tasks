import os
import pytest
from fastapi.testclient import TestClient

# Ensure secret signature is configured for tests
os.environ["SECRET_SIGNATURE"] = "ci-test-secret-signature-key-12345"

from fastapi_crud_tasks.main import app

client = TestClient(app)


def test_index_route():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


def test_auth_and_crud_flow():
    # 1. Register a new user
    user_payload = {
        "name": "CI Tester",
        "email": "ci_test_user@example.com",
        "password": "SecurePassword123!",
    }
    register_res = client.post("/auth/register", json=user_payload)
    assert register_res.status_code == 200
    reg_data = register_res.json()
    assert "id" in reg_data or "409" in reg_data

    # 2. Login to get JWT token
    login_payload = {
        "email": "ci_test_user@example.com",
        "password": "SecurePassword123!",
    }
    login_res = client.post("/auth/login", json=login_payload)
    assert login_res.status_code == 200
    token_data = login_res.json()
    assert "token" in token_data
    token = token_data["token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 3. Check /auth/me
    me_res = client.get("/auth/me", headers=headers)
    assert me_res.status_code == 200
    assert "me" in me_res.json()

    # 4. Create an item
    item_payload = {
        "name": "CI Test Task",
        "description": "Test task created by automated test suite",
    }
    create_item_res = client.post("/items/", json=item_payload, headers=headers)
    assert create_item_res.status_code == 200
    item_data = create_item_res.json()
    assert item_data["name"] == item_payload["name"]
    item_id = item_data["id"]

    # 5. List items
    list_items_res = client.get("/items/", headers=headers)
    assert list_items_res.status_code == 200
    items_list = list_items_res.json()
    assert any(i["id"] == item_id for i in items_list)

    # 6. Retrieve item by ID
    get_item_res = client.get(f"/items/{item_id}", headers=headers)
    assert get_item_res.status_code == 200
    assert get_item_res.json()["id"] == item_id

    # 7. Update item
    update_payload = {
        "name": "CI Test Task Updated",
        "description": "Updated description",
    }
    update_res = client.put(f"/items/{item_id}", json=update_payload, headers=headers)
    assert update_res.status_code == 200
    assert update_res.json()["name"] == update_payload["name"]

    # 8. Delete item
    delete_res = client.delete(f"/items/{item_id}", headers=headers)
    assert delete_res.status_code == 200
    assert delete_res.json().get("success") is True
