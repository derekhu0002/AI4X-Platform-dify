from fastapi.testclient import TestClient

from mcp.notification_mcp.app.main import app


client = TestClient(app)


def test_preview_contract_returns_escalation_and_dedup_key() -> None:
    response = client.post(
        "/preview",
        json={
            "template_type": "vulnerability-alert",
            "message_title": "漏洞影响预警",
            "message_summary": "发现高危组件影响生产环境。",
            "business_impact": "影响支付网关。",
            "recommended_action": "优先修补并评估窗口期。",
            "event_type": "ai4sec.vulnerability-intelligence.result.v1",
            "object_refs": ["vulnerability--vs3"],
            "severity_tier": "critical",
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["escalate_after_minutes"] == 10
    assert payload["dedup_key"].startswith("vulnerability-alert:vulnerability--vs3:critical:")
