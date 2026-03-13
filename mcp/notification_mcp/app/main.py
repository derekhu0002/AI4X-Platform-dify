from fastapi import FastAPI

from mcp.notification_mcp.app.models import NotificationRequest
from mcp.notification_mcp.app.service import NotificationService
from mcp.notification_mcp.app.settings import NotificationMCPSettings

settings = NotificationMCPSettings()
service = NotificationService(settings)
app = FastAPI(title="notification_mcp", version="0.1.0")


@app.get("/health")
async def healthcheck() -> dict[str, str]:
    """// @ArchitectureID: 1227"""
    return {"status": "ok", "service": "notification_mcp"}


@app.post("/preview")
async def preview_notification(request: NotificationRequest) -> dict[str, object]:
    """// @ArchitectureID: 1227"""
    return service.preview(request).model_dump()


@app.post("/dispatch")
async def dispatch_notification(request: NotificationRequest) -> dict[str, object]:
    """// @ArchitectureID: 1227"""
    return service.dispatch(request).model_dump()
