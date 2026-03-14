import asyncio
import importlib
import os

from fastapi.testclient import TestClient

os.environ["OPENCTI_MCP_MOCK_MODE"] = "true"
os.environ["NOTIFICATION_MCP_PREVIEW_MODE"] = "true"

from DifyAgentWorkflow.tools.ai4sec_runtime_tools import build_notification_payload, resolve_opencti_signal, route_entrypoint
from mcp.notification_mcp.app import main as notification_main
from mcp.opencti_mcp.app import main as opencti_main

notification_app = importlib.reload(notification_main).app
opencti_app = importlib.reload(opencti_main).app


opencti_client = TestClient(opencti_app)
notification_client = TestClient(notification_app)


async def _resolve_from_mcp(object_id: str) -> dict[str, object] | None:
    response = opencti_client.post(
        "/query",
        json={"object_id": object_id, "projection_profile": "summary", "include_relationships": True},
    )
    if response.status_code != 200:
        return None
    return response.json()["items"][0]


def test_signal_resolution_to_notification_flow() -> None:
    signal_bundle = {
        "type": "bundle",
        "objects": [
            {
                "id": "vulnerability--vs3",
                "x_opencti_id": "vulnerability--vs3",
                "x_opencti_lookup_required": True,
            }
        ],
    }
    resolved = asyncio.run(resolve_opencti_signal(signal_bundle, _resolve_from_mcp))
    scene = route_entrypoint("webhook", "请评估这个漏洞", None)
    payload = build_notification_payload(scene, resolved)
    response = notification_client.post("/dispatch", json=payload)
    assert response.status_code == 200
    result = response.json()
    assert result["accepted"] is True
    assert "hdhscu@126.com" in result["preview"]["recipients"]
