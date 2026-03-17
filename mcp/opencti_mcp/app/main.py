from __future__ import annotations

import logging

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from mcp.opencti_mcp.app.models import (
    BundleWriteRequest,
    ErrorEnvelope,
    QueryRequest,
    ThreatModelReportQueryRequest,
)
from mcp.opencti_mcp.app.service import MCPContractError, OpenCTIProjectionService
from mcp.opencti_mcp.app.settings import OpenCTIMCPSettings

settings = OpenCTIMCPSettings()
service = OpenCTIProjectionService(settings)
app = FastAPI(title="ai4sec_opencti_mcp", version="0.1.0")
logger = logging.getLogger("ai4sec.opencti_mcp")


@app.on_event("startup")
async def startup_probe_write_capability() -> None:
    """// @ArchitectureID: 1215"""
    result = await service.probe_write_capability()
    app.state.write_probe = result
    message = (
        "OpenCTI write capability probe: "
        f"status={result.get('status')} code={result.get('code')} detail={result.get('detail')}"
    )
    if result.get("status") in {"blocked"}:
        logger.warning(message)
    else:
        logger.info(message)


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


@app.post("/query/threat-model-report")
async def query_threat_model_report(request: ThreatModelReportQueryRequest) -> dict[str, object]:
    """// @ArchitectureID: 1215"""
    return (await service.query_threat_model_report(request)).model_dump()


@app.post("/bundle")
async def write_bundle(request: BundleWriteRequest) -> dict[str, object]:
    """// @ArchitectureID: 1215"""
    return (await service.write_bundle(request)).model_dump()
