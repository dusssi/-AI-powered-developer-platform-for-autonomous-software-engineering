def register(client, email="dev@example.com"):
    response = client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": "a-strong-test-password"},
    )
    assert response.status_code == 201
    return response.json()

def login(client, email="dev@example.com"):
    response = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": "a-strong-test-password"},
    )
    assert response.status_code == 200
    return response.json()["access_token"]

def test_register_login_and_current_user(client):
    register(client)
    token = login(client)
    response = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["email"] == "dev@example.com"
    assert "password_hash" not in response.json()

def test_duplicate_registration_is_rejected(client):
    register(client)
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "DEV@example.com", "password": "a-strong-test-password"},
    )
    assert response.status_code == 409

def test_workspace_routes_require_authentication(client):
    assert client.get("/api/v1/workspaces").status_code == 401

def test_workspace_crud(client):
    register(client)
    token = login(client)
    headers = {"Authorization": f"Bearer {token}"}
    created = client.post("/api/v1/workspaces", json={"name": "BuckLabs"}, headers=headers)
    assert created.status_code == 201
    workspace_id = created.json()["id"]
    listed = client.get("/api/v1/workspaces", headers=headers)
    assert [item["id"] for item in listed.json()] == [workspace_id]
    updated = client.patch(
        f"/api/v1/workspaces/{workspace_id}", json={"name": "BuckLabs Dev"}, headers=headers
    )
    assert updated.status_code == 200
    assert updated.json()["name"] == "BuckLabs Dev"
    deleted = client.delete(f"/api/v1/workspaces/{workspace_id}", headers=headers)
    assert deleted.status_code == 204
