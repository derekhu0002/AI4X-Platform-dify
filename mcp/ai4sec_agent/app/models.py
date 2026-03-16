from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class OpenCTIWebhookRequest(BaseModel):
    """// @ArchitectureID: 1214"""

    type: str = Field(min_length=1)
    objects: list[dict[str, Any]] = Field(default_factory=list)


class AgentWorkflowEnvelope(BaseModel):
    """// @ArchitectureID: 1214"""

    entry_mode: str = "webhook"
    selected_flow: str = "VS4"
    user_request: str = ""
    bundle: dict[str, Any]


class OpenCTIWebhookResponse(BaseModel):
    """// @ArchitectureID: 1214"""

    accepted: bool
    auth_required: bool = False
    workflow_envelope: AgentWorkflowEnvelope
    unresolved_governance: list[str]
