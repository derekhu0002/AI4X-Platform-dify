from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from mcp.opencti_mcp.app.models import BundleWriteRequest, ErrorEnvelope, QueryRequest
from mcp.opencti_mcp.app.service import MCPContractError, OpenCTIProjectionService
from mcp.opencti_mcp.app.settings import OpenCTIMCPSettings

settings = OpenCTIMCPSettings()
service = OpenCTIProjectionService(settings)
app = FastAPI(title="ai4sec_opencti_mcp", version="0.1.0")


@app.exception_handler(MCPContractError)
async def handle_contract_error(_: object, error: MCPContractError) -> JSONResponse:
    """// @ArchitectureID: 1215"""
    envelope = ErrorEnvelope(code=error.code, message=error.message)
    return JSONResponse(status_code=error.status_code, content=envelope.model_dump())


@app.get("/health")
async def healthcheck() -> dict[str, str]:
    """// @ArchitectureID: 1215"""
    return {"status": "ok", "service": "ai4sec_opencti_mcp"}


@app.post("/query")
async def query_stix(request: QueryRequest) -> dict[str, object]:
    """// @ArchitectureID: 1215"""
    return (await service.query(request)).model_dump()


@app.post("/bundle")
async def write_bundle(request: BundleWriteRequest) -> dict[str, object]:
    """// @ArchitectureID: 1215"""
    return (await service.write_bundle(request)).model_dump()


@app.post("/webhooks/opencti/threat-intelligence")
async def passthrough_webhook(payload: dict[str, object]) -> dict[str, object]:
    """// @ArchitectureID: 1215"""
    if "objects" not in payload:
        raise HTTPException(status_code=400, detail="VAL-4001: payload.objects is required")
    return {"accepted": True, "auth_required": False, "payload": payload}
