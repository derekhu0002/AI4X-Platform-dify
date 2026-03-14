from __future__ import annotations

import smtplib
from datetime import UTC, datetime
from email.message import EmailMessage

from mcp.notification_mcp.app.models import DispatchResponse, NotificationPreview, NotificationRequest
from mcp.notification_mcp.app.settings import NotificationMCPSettings


ESCALATION_MATRIX = {
    "normal": 240,
    "high": 30,
    "critical": 10,
}


class NotificationService:
    """// @ArchitectureID: 1227"""

    def __init__(self, settings: NotificationMCPSettings):
        """// @ArchitectureID: 1227"""
        self.settings = settings

    def preview(self, request: NotificationRequest) -> NotificationPreview:
        """// @ArchitectureID: 1227"""
        recipients = self._merge_recipients(request.primary_recipients)
        approvers = list(dict.fromkeys(request.approver_recipients))
        ccs = list(dict.fromkeys(request.cc_recipients))
        escalate_after_minutes = request.escalate_after_minutes or ESCALATION_MATRIX[request.severity_tier]
        dedup_key = request.dedup_key or self._build_dedup_key(request)

        return NotificationPreview(
            subject=f"[{request.template_type}] {request.message_title}",
            summary=request.message_summary,
            recipients=recipients,
            approvers=approvers,
            ccs=ccs,
            escalate_after_minutes=escalate_after_minutes,
            dedup_key=dedup_key,
            channels=request.channels,
        )

    def dispatch(self, request: NotificationRequest) -> DispatchResponse:
        """// @ArchitectureID: 1227"""
        preview = self.preview(request)
        if self.settings.preview_mode:
            return DispatchResponse(accepted=True, mode="preview", preview=preview)

        self._send_email(preview, request)
        return DispatchResponse(accepted=True, mode="dispatch", preview=preview)

    def _merge_recipients(self, requested: list[str]) -> list[str]:
        """// @ArchitectureID: 1227"""
        recipients = [self.settings.default_formal_recipient, *requested]
        return list(dict.fromkeys(recipients))

    def _build_dedup_key(self, request: NotificationRequest) -> str:
        """// @ArchitectureID: 1227"""
        object_ref = request.object_refs[0] if request.object_refs else "unknown-object"
        business_date = datetime.now(UTC).strftime("%Y-%m-%d")
        return f"{request.template_type}:{object_ref}:{request.severity_tier}:{business_date}"

    def _send_email(self, preview: NotificationPreview, request: NotificationRequest) -> None:
        """// @ArchitectureID: 1227"""
        if "email" not in preview.channels:
            raise RuntimeError("Only email channel is currently supported for real dispatch.")
        if not self.settings.smtp_host:
            raise RuntimeError("NOTIFICATION_MCP_SMTP_HOST is required when preview_mode is false.")

        sender = self.settings.smtp_from_address or self.settings.smtp_username or self.settings.default_formal_recipient
        if not sender:
            raise RuntimeError("A sender address is required for notification dispatch.")

        recipients = list(dict.fromkeys([*preview.recipients, *preview.approvers, *preview.ccs]))
        if not recipients:
            raise RuntimeError("At least one notification recipient is required for dispatch.")

        message = EmailMessage()
        message["Subject"] = preview.subject
        message["From"] = sender
        message["To"] = ", ".join(preview.recipients)
        if preview.ccs:
            message["Cc"] = ", ".join(preview.ccs)
        message.set_content(
            "\n".join(
                [
                    request.message_summary,
                    "",
                    f"Business Impact: {request.business_impact}",
                    f"Recommended Action: {request.recommended_action}",
                    f"Event Type: {request.event_type}",
                    f"Dedup Key: {preview.dedup_key}",
                    *( [f"Evidence Link: {request.evidence_link}"] if request.evidence_link else [] ),
                ]
            )
        )

        with smtplib.SMTP(self.settings.smtp_host, self.settings.smtp_port, timeout=30) as smtp:
            if self.settings.smtp_use_starttls:
                smtp.starttls()
            if self.settings.smtp_username:
                smtp.login(self.settings.smtp_username, self.settings.smtp_password)
            smtp.send_message(message, from_addr=sender, to_addrs=recipients)
