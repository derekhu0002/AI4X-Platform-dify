from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


TemplateType = Literal[
    "release-gate-decision",
    "incident-response",
    "vulnerability-alert",
    "monitoring-rule-online",
]
SeverityTier = Literal["normal", "high", "critical"]


class NotificationRequest(BaseModel):
    """// @ArchitectureID: 1227"""

    template_type: TemplateType
    message_title: str = Field(min_length=1)
    message_summary: str = Field(min_length=1)
    business_impact: str = Field(min_length=1)
    recommended_action: str = Field(min_length=1)
    evidence_link: str | None = None
    primary_role: str | None = None
    approver_role: str | None = None
    cc_roles: list[str] = Field(default_factory=list)
    severity_tier: SeverityTier = "normal"
    escalate_after_minutes: int | None = None
    event_type: str = Field(min_length=1)
    object_refs: list[str] = Field(default_factory=list)
    dedup_key: str | None = None
    channels: list[str] = Field(default_factory=lambda: ["email"])
    primary_recipients: list[str] = Field(default_factory=list)
    approver_recipients: list[str] = Field(default_factory=list)
    cc_recipients: list[str] = Field(default_factory=list)


class NotificationPreview(BaseModel):
    """// @ArchitectureID: 1227"""

    subject: str
    summary: str
    recipients: list[str]
    approvers: list[str]
    ccs: list[str]
    escalate_after_minutes: int
    dedup_key: str
    channels: list[str]


class DispatchResponse(BaseModel):
    """// @ArchitectureID: 1227"""

    accepted: bool
    mode: Literal["preview", "dispatch"]
    preview: NotificationPreview
