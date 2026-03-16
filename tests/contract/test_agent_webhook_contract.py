from fastapi.testclient import TestClient

from mcp.ai4sec_agent.app.main import app


client = TestClient(app)


def test_opencti_webhook_ingress_at_agent_boundary() -> None:
    response = client.post(
        "/webhooks/opencti/threat-intelligence",
        json={
            "type": "bundle",
            "objects": [
                {
                    "id": "vulnerability--demo",
                    "type": "vulnerability",
                    "name": "CVE-2026-1000",
                }
            ],
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["accepted"] is True
    assert payload["auth_required"] is False
    assert payload["workflow_envelope"]["entry_mode"] == "webhook"
    assert payload["workflow_envelope"]["selected_flow"] == "VS3"
    assert payload["workflow_envelope"]["bundle"]["type"] == "bundle"
