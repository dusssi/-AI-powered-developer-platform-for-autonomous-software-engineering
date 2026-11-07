def create_workspace_with_repository(client, email="task-owner@example.com"):
    registered = client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": "a-strong-test-password"},
    )
    assert registered.status_code == 201
    token = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": "a-strong-test-password"},
    ).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    workspace = client.post("/api/v1/workspaces", json={"name": "Tasks"}, headers=headers)
    workspace_id = workspace.json()["id"]
    repository = client.post(
        f"/api/v1/workspaces/{workspace_id}/repositories",
        json={"url": "https://github.com/octocat/Hello-World"},
        headers=headers,
    )
    return workspace_id, repository.json()["id"], headers


def test_create_and_read_task_with_initial_attempt(client):
    workspace_id, repository_id, headers = create_workspace_with_repository(client)
    created = client.post(
        f"/api/v1/workspaces/{workspace_id}/tasks",
        json={
            "repository_id": repository_id,
            "instruction": "  Explain the architecture  ",
            "engine": "fake",
            "read_only": True,
        },
        headers=headers,
    )
    assert created.status_code == 201
    body = created.json()
    assert body["instruction"] == "Explain the architecture"
    assert body["status"] == "queued"
    assert body["read_only"] is True

    detail = client.get(
        f"/api/v1/workspaces/{workspace_id}/tasks/{body['id']}", headers=headers
    )
    assert detail.status_code == 200
    assert len(detail.json()["attempts"]) == 1
    assert detail.json()["attempts"][0]["attempt_number"] == 1
    assert detail.json()["attempts"][0]["status"] == "queued"
    assert detail.json()["attempts"][0]["events"] == []


def test_task_rejects_repository_from_another_workspace(client):
    workspace_id, repository_id, headers = create_workspace_with_repository(client)
    other_workspace = client.post(
        "/api/v1/workspaces", json={"name": "Other"}, headers=headers
    ).json()["id"]
    response = client.post(
        f"/api/v1/workspaces/{other_workspace}/tasks",
        json={"repository_id": repository_id, "instruction": "Read files"},
        headers=headers,
    )
    assert response.status_code == 404


def test_task_workspace_is_owner_scoped(client):
    workspace_id, repository_id, _ = create_workspace_with_repository(client)
    registered = client.post(
        "/api/v1/auth/register",
        json={"email": "intruder@example.com", "password": "a-strong-test-password"},
    )
    assert registered.status_code == 201
    token = client.post(
        "/api/v1/auth/login",
        json={"email": "intruder@example.com", "password": "a-strong-test-password"},
    ).json()["access_token"]
    response = client.get(
        f"/api/v1/workspaces/{workspace_id}/tasks",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404
