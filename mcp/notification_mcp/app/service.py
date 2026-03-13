from __future__ import annotations

from datetime import UTC, datetime

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
        mode = "preview" if self.settings.preview_mode else "dispatch"
        return DispatchResponse(accepted=True, mode=mode, preview=preview)

    def _merge_recipients(self, requested: list[str]) -> list[str]:
        """// @ArchitectureID: 1227"""
        recipients = [self.settings.default_formal_recipient, *requested]
        return list(dict.fromkeys(recipients))

    def _build_dedup_key(self, request: NotificationRequest) -> str:
        """// @ArchitectureID: 1227"""
        object_ref = request.object_refs[0] if request.object_refs else "unknown-object"
        business_date = datetime.now(UTC).strftime("%Y-%m-%d")
        return f"{request.template_type}:{object_ref}:{request.severity_tier}:{business_date}"
