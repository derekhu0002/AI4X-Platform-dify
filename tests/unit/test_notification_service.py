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


def test_notification_dispatch_uses_smtp_when_preview_disabled(monkeypatch) -> None:
    sent: dict[str, object] = {}

    class FakeSMTP:
        def __init__(self, host: str, port: int, timeout: int):
            sent["host"] = host
            sent["port"] = port
            sent["timeout"] = timeout

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def starttls(self) -> None:
            sent["starttls"] = True

        def login(self, username: str, password: str) -> None:
            sent["username"] = username
            sent["password"] = password

        def send_message(self, message, from_addr: str, to_addrs: list[str]) -> None:
            sent["subject"] = message["Subject"]
            sent["from_addr"] = from_addr
            sent["to_addrs"] = to_addrs

    monkeypatch.setattr("mcp.notification_mcp.app.service.smtplib.SMTP", FakeSMTP)

    service = NotificationService(
        NotificationMCPSettings(
            preview_mode=False,
            default_formal_recipient="hdhscu@126.com",
            smtp_host="smtp.example.com",
            smtp_port=587,
            smtp_username="bot@example.com",
            smtp_password="secret",
            smtp_from_address="bot@example.com",
        )
    )

    response = service.dispatch(
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

    assert response.mode == "dispatch"
    assert sent["host"] == "smtp.example.com"
    assert sent["username"] == "bot@example.com"
    assert sent["from_addr"] == "bot@example.com"
    assert sent["to_addrs"] == ["hdhscu@126.com", "soc@example.com"]
