import hashlib
import hmac
import json


def authenticated_workspace(client):
    client.post(
        "/api/v1/auth/register",
        json={"email": "github-app@example.com", "password": "a-strong-test-password"},
    )
    token = client.post(
        "/api/v1/auth/login",
        json={"email": "github-app@example.com", "password": "a-strong-test-password"},
    ).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    workspace = client.post(
        "/api/v1/workspaces", json={"name": "GitHub App Test"}, headers=headers
    ).json()
    return workspace["id"], headers


def test_installation_start_requires_configuration(client):
    workspace_id, headers = authenticated_workspace(client)
    response = client.post(
        f"/api/v1/workspaces/{workspace_id}/github/install", headers=headers
    )
    assert response.status_code == 503


def test_webhook_rejects_missing_or_invalid_signature(client):
    assert client.post("/api/v1/github/webhook", content=b"{}").status_code == 401
    assert client.post(
        "/api/v1/github/webhook",
        content=b"{}",
        headers={"X-Hub-Signature-256": "sha256=" + "0" * 64, "X-GitHub-Event": "ping"},
    ).status_code == 401
