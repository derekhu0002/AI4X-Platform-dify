from mcp.notification_mcp.app.models import NotificationRequest
from mcp.notification_mcp.app.service import NotificationService
from mcp.notification_mcp.app.settings import NotificationMCPSettings


def test_notification_service_appends_formal_recipient() -> None:
    service = NotificationService(NotificationMCPSettings(default_formal_recipient="hdhscu@126.com"))
    preview = service.preview(
        NotificationRequest(
            template_type="incident-response",
            message_title="响应升级",
            message_summary="发现横向移动告警。",
            business_impact="影响生产跳板机。",
            recommended_action="执行隔离与取证。",
            event_type="ai4sec.incident-response.case-created.v1",
            object_refs=["incident--vs2"],
            primary_recipients=["soc@example.com"],
            severity_tier="high",
        )
    )
    assert preview.recipients == ["hdhscu@126.com", "soc@example.com"]
    assert preview.escalate_after_minutes == 30
