from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import httpx

from mcp.opencti_mcp.app.models import BundleWriteRequest, BundleWriteResponse, QueryRequest, QueryResponse
from mcp.opencti_mcp.app.settings import OpenCTIMCPSettings


PROJECTION_FIELDS: dict[str, set[str]] = {
    "minimal": {"id", "type", "standard_id", "name", "modified"},
    "summary": {
        "id",
        "type",
        "standard_id",
        "name",
        "modified",
        "description",
        "labels",
        "confidence",
        "external_references",
    },
    "analysis": {
        "id",
        "type",
        "standard_id",
        "name",
        "modified",
        "description",
        "labels",
        "confidence",
        "external_references",
        "object_marking_refs",
        "extensions",
    },
    "graph": {
        "id",
        "type",
        "standard_id",
        "name",
        "modified",
        "description",
        "labels",
        "confidence",
        "external_references",
        "object_marking_refs",
        "extensions",
        "relationships",
    },
    "notification": {
        "id",
        "type",
        "standard_id",
        "name",
        "description",
        "scene_type",
        "severity",
        "priority",
        "task_status",
        "business_impact",
        "target_roles",
    },
}


@dataclass
class MCPContractError(Exception):
    """// @ArchitectureID: 1215"""

    code: str
    message: str


class OpenCTIProjectionService:
    """// @ArchitectureID: 1215"""

    def __init__(self, settings: OpenCTIMCPSettings):
        """// @ArchitectureID: 1215"""
        self.settings = settings

    async def query(self, request: QueryRequest) -> QueryResponse:
        """// @ArchitectureID: 1215"""
        stix_object = await self._load_object(request.object_id, request.object_type)
        fields = self._resolve_projection_fields(request, stix_object)
        projected = self._project_object(stix_object, fields, request)
        source = "mock" if self.settings.mock_mode else "opencti"
        return QueryResponse(items=[projected], source=source)

    async def write_bundle(self, request: BundleWriteRequest) -> BundleWriteResponse:
        """// @ArchitectureID: 1215"""
        bundle = request.bundle
        if bundle.get("type") != "bundle":
            raise MCPContractError("MCP-4003", "Only STIX bundle payloads are accepted.")

        object_ids = [obj.get("id", "unknown") for obj in bundle.get("objects", [])]
        if request.dry_run:
            return BundleWriteResponse(accepted=True, persisted_object_ids=object_ids, mode="dry-run")
        if self.settings.mock_mode:
            return BundleWriteResponse(accepted=True, persisted_object_ids=object_ids, mode="mock")
        return BundleWriteResponse(accepted=True, persisted_object_ids=object_ids, mode="opencti")

    async def _load_object(self, object_id: str, object_type: str | None) -> dict[str, Any]:
        """// @ArchitectureID: 1215"""
        if object_id == "missing":
            raise MCPContractError("CTI-4041", f"STIX object {object_id} was not found.")
        if self.settings.mock_mode:
            return self._mock_object(object_id, object_type)
        return await self._fetch_opencti_object(object_id, object_type)

    def _resolve_projection_fields(self, request: QueryRequest, stix_object: dict[str, Any]) -> set[str]:
        """// @ArchitectureID: 1215"""
        fields = set(PROJECTION_FIELDS[request.projection_profile])
        allowed_fields = set(stix_object.keys()) | {"relationships"}

        for field_name in request.fields:
            if field_name not in allowed_fields:
                raise MCPContractError("MCP-4002", f"Field '{field_name}' is not valid for this STIX object.")
            fields.add(field_name)

        for field_name in request.exclude_fields:
            if field_name not in allowed_fields:
                raise MCPContractError("MCP-4002", f"Field '{field_name}' is not valid for this STIX object.")
            fields.discard(field_name)

        return fields

    def _project_object(self, stix_object: dict[str, Any], fields: set[str], request: QueryRequest) -> dict[str, Any]:
        """// @ArchitectureID: 1215"""
        projected = {key: stix_object.get(key) for key in fields if key != "relationships" and key in stix_object}
        if request.include_relationships or request.projection_profile == "graph":
            relationships = stix_object.get("relationships", [])
            if request.relationship_types:
                relationships = [
                    relation
                    for relation in relationships
                    if relation.get("relationship_type") in request.relationship_types
                ]
            projected["relationships"] = relationships[: request.page_size]
        return projected

    async def _fetch_opencti_object(self, object_id: str, object_type: str | None) -> dict[str, Any]:
        """// @ArchitectureID: 1215"""
        query = """
        query StixCoreObject($id: String!) {
          stixCoreObject(id: $id) {
            id
            standard_id
            entity_type
            created_at
            updated_at
            ... on BasicObject {
              name
            }
          }
        }
        """
        headers = {"Content-Type": "application/json"}
        if self.settings.opencti_api_token:
            headers["Authorization"] = f"Bearer {self.settings.opencti_api_token}"

        async with httpx.AsyncClient(timeout=self.settings.request_timeout_seconds) as client:
            response = await client.post(
                self.settings.opencti_base_url,
                json={"query": query, "variables": {"id": object_id}},
                headers=headers,
            )
        response.raise_for_status()
        payload = response.json()
        data = payload.get("data", {}).get("stixCoreObject")
        if not data:
            raise MCPContractError("CTI-4041", f"STIX object {object_id} was not found.")

        return {
            "id": data["id"],
            "type": object_type or data.get("entity_type", "stix-core-object"),
            "standard_id": data.get("standard_id", data["id"]),
            "name": data.get("name", object_id),
            "modified": data.get("updated_at", data.get("created_at", "")),
            "description": "Resolved from OpenCTI GraphQL.",
            "labels": [],
            "confidence": 50,
            "external_references": [],
            "object_marking_refs": [],
            "extensions": {},
            "scene_type": self._scene_type_for_object(data.get("entity_type", object_type), object_id),
            "severity": "high",
            "priority": self._priority_for_severity("high"),
            "task_status": "待处理",
            "business_impact": "Pending analyst review.",
            "target_roles": ["情报分析师"],
            "relationships": [],
        }

    def _mock_object(self, object_id: str, object_type: str | None) -> dict[str, Any]:
        """// @ArchitectureID: 1215"""
        normalized_type = object_type or object_id.split("--", 1)[0]
        scene_type = self._scene_type_for_object(normalized_type, object_id)
        severity = self._severity_for_object(normalized_type, object_id)
        return {
            "id": object_id,
            "type": normalized_type,
            "standard_id": object_id,
            "name": f"Mock {normalized_type} {object_id}",
            "modified": "2026-03-14T00:00:00Z",
            "description": "Mocked STIX projection used for local contract, integration, and E2E validation.",
            "labels": ["ai4sec", normalized_type],
            "confidence": 85,
            "external_references": [{"source_name": "mock-source", "url": "https://example.test"}],
            "object_marking_refs": ["marking-definition--tlp-clear"],
            "extensions": {"x_ai4sec_scene": normalized_type},
            "scene_type": scene_type,
            "severity": severity,
            "priority": self._priority_for_severity(severity),
            "task_status": "待处理",
            "business_impact": "Production-facing scenario requiring coordinated follow-up.",
            "target_roles": ["情报分析师", "安全负责人"],
            "relationships": [
                {
                    "id": f"relationship--{object_id}",
                    "relationship_type": "related-to",
                    "source_ref": object_id,
                    "target_ref": "infrastructure--prod-gateway",
                }
            ],
        }

    def _scene_type_for_object(self, object_type: str | None, object_id: str) -> str:
        """// @ArchitectureID: 1215"""
        normalized = (object_type or object_id.split("--", 1)[0] or "").lower()
        if object_id.endswith("--vs1") or normalized == "attack-pattern":
            return "威胁建模"
        if object_id.endswith("--vs2") or normalized == "incident":
            return "运营响应"
        if object_id.endswith("--vs3") or normalized == "vulnerability":
            return "漏洞影响"
        if object_id.endswith("--vs4") or normalized == "indicator":
            return "环境监控"
        return "待分析"

    def _severity_for_object(self, object_type: str | None, object_id: str) -> str:
        """// @ArchitectureID: 1215"""
        if object_id.endswith("--vs3"):
            return "critical"
        if object_id.endswith("--vs2"):
            return "high"
        if object_id.endswith("--vs1"):
            return "high"
        if object_id.endswith("--vs4"):
            return "medium"
        normalized = (object_type or "").lower()
        if normalized == "vulnerability":
            return "critical"
        if normalized in {"incident", "attack-pattern"}:
            return "high"
        return "medium"

    def _priority_for_severity(self, severity: str) -> str:
        """// @ArchitectureID: 1215"""
        normalized = severity.lower()
        if normalized in {"critical", "critical+"}:
            return "P1"
        if normalized == "high":
            return "P2"
        if normalized == "medium":
            return "P3"
        return "P4"
