from __future__ import annotations

from typing import Any

from fastapi import FastAPI, HTTPException

from mcp.ai4sec_agent.app.models import AgentWorkflowEnvelope, OpenCTIWebhookRequest, OpenCTIWebhookResponse

app = FastAPI(title="ai4sec_agent", version="0.1.0")


def _infer_flow(first_object: dict[str, Any]) -> str:
    """// @ArchitectureID: 1214"""
    object_type = str(first_object.get("type", "")).lower()
    if object_type == "attack-pattern":
        return "VS1"
    if object_type in {"incident", "grouping"}:
        return "VS2"
    if object_type == "vulnerability":
        return "VS3"
    return "VS4"


@app.get("/health")
async def healthcheck() -> dict[str, str]:
    """// @ArchitectureID: 1214"""
    return {"status": "ok", "service": "ai4sec_agent"}


@app.post("/webhooks/opencti/threat-intelligence")
async def ingest_opencti_webhook(payload: OpenCTIWebhookRequest) -> dict[str, object]:
    """// @ArchitectureID: 1214"""
    if payload.type != "bundle":
        raise HTTPException(status_code=400, detail="VAL-4001: payload.type must be 'bundle'")
    if not payload.objects:
        raise HTTPException(status_code=400, detail="VAL-4002: payload.objects is required")

    selected_flow = _infer_flow(payload.objects[0])
    workflow_envelope = AgentWorkflowEnvelope(
        selected_flow=selected_flow,
        user_request="来自 OpenCTI webhook 的 STIX 事件",
        bundle=payload.model_dump(),
    )
    response = OpenCTIWebhookResponse(
        accepted=True,
        workflow_envelope=workflow_envelope,
        unresolved_governance=[
            "OpenCTI->Agent path does not require auth by current architecture notes.",
            "Signature and replay protection strategy is pending organization-level confirmation.",
        ],
    )
    return response.model_dump()
