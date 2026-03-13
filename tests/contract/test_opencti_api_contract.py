from fastapi.testclient import TestClient

from mcp.opencti_mcp.app.main import app


client = TestClient(app)


def test_query_contract_returns_notification_projection() -> None:
    response = client.post(
        "/query",
        json={
            "object_id": "vulnerability--vs3",
            "projection_profile": "notification",
            "include_relationships": False,
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["source"] == "mock"
    assert payload["items"][0]["business_impact"]


def test_query_contract_rejects_unknown_field() -> None:
    response = client.post(
        "/query",
        json={
            "object_id": "vulnerability--vs3",
            "projection_profile": "summary",
            "fields": ["unknown_field"],
        },
    )
    assert response.status_code == 400
    assert response.json()["code"] == "MCP-4002"
