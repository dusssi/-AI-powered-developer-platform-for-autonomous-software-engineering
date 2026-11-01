def create_user_workspace(client):
    registered = client.post(
        "/api/v1/auth/register",
        json={"email": "repo-owner@example.com", "password": "a-strong-test-password"},
    )
    assert registered.status_code == 201
    login = client.post(
        "/api/v1/auth/login",
        json={"email": "repo-owner@example.com", "password": "a-strong-test-password"},
    )
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    workspace = client.post(
        "/api/v1/workspaces", json={"name": "Engineering"}, headers=headers
    )
    return workspace.json()["id"], headers


def test_register_and_list_github_repository(client):
    workspace_id, headers = create_user_workspace(client)
    response = client.post(
        f"/api/v1/workspaces/{workspace_id}/repositories",
        json={"url": "https://github.com/octocat/Hello-World"},
        headers=headers,
    )
    assert response.status_code == 201
    body = response.json()
    assert body["full_name"] == "octocat/Hello-World"
    assert body["clone_url"] == "https://github.com/octocat/Hello-World.git"
    assert body["connection_status"] == "pending_connection"

    listed = client.get(
        f"/api/v1/workspaces/{workspace_id}/repositories", headers=headers
    )
    assert listed.status_code == 200
    assert len(listed.json()) == 1


def test_reject_non_github_or_unsafe_repository_urls(client):
    workspace_id, headers = create_user_workspace(client)
    for url in (
        "http://github.com/octocat/Hello-World",
        "https://github.com.evil.example/octocat/Hello-World",
        "https://user:password@github.com/octocat/Hello-World",
        "https://github.com/octocat/Hello-World?redirect=https://evil.example",
    ):
        response = client.post(
            f"/api/v1/workspaces/{workspace_id}/repositories",
            json={"url": url},
            headers=headers,
        )
        assert response.status_code == 422


def test_repository_registration_is_workspace_scoped(client):
    workspace_id, headers = create_user_workspace(client)
    response = client.post(
        f"/api/v1/workspaces/{workspace_id}/repositories",
        json={"url": "https://github.com/octocat/Hello-World"},
        headers=headers,
    )
    assert response.status_code == 201
    other_user = client.post(
        "/api/v1/auth/register",
        json={"email": "other@example.com", "password": "a-strong-test-password"},
    )
    assert other_user.status_code == 201
    other_token = client.post(
        "/api/v1/auth/login",
        json={"email": "other@example.com", "password": "a-strong-test-password"},
    ).json()["access_token"]
    other_headers = {"Authorization": f"Bearer {other_token}"}
    listed = client.get(
        f"/api/v1/workspaces/{workspace_id}/repositories", headers=other_headers
    )
    assert listed.status_code == 404


def test_duplicate_repository_registration_returns_conflict(client):
    workspace_id, headers = create_user_workspace(client)
    path = f"/api/v1/workspaces/{workspace_id}/repositories"
    payload = {"url": "https://github.com/octocat/Hello-World"}
    assert client.post(path, json=payload, headers=headers).status_code == 201
    assert client.post(path, json=payload, headers=headers).status_code == 409
