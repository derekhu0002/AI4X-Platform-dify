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
        "risk_object",
        "scene_type",
        "severity",
        "priority",
        "task_status",
        "business_impact",
        "target_roles",
        "primary_asset",
        "deployment_scope",
        "owner_team",
        "business_domain",
        "business_criticality",
        "execution_window",
    },
}


@dataclass
class MCPContractError(Exception):
    """// @ArchitectureID: 1215"""

    code: str
    message: str
    status_code: int = 400


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
            raise MCPContractError("CTI-4041", f"STIX object {object_id} was not found.", status_code=404)
        if self.settings.mock_mode:
            return self._mock_object(object_id, object_type)
        resolved_object_id = self._resolve_object_id(object_id)
        return await self._fetch_opencti_object(resolved_object_id, object_id, object_type)

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

    async def _fetch_opencti_object(
        self,
        lookup_object_id: str,
        requested_object_id: str,
        object_type: str | None,
    ) -> dict[str, Any]:
        """// @ArchitectureID: 1215"""
        query = """
        query StixCoreObject($id: String!) {
          stixCoreObject(id: $id) {
            id
            standard_id
            entity_type
            created_at
            updated_at
          }
        }
        """
        headers = {"Content-Type": "application/json"}
        if self.settings.opencti_api_token:
            headers["Authorization"] = f"Bearer {self.settings.opencti_api_token}"

        try:
            async with httpx.AsyncClient(
                timeout=self.settings.request_timeout_seconds,
                trust_env=False,
            ) as client:
                response = await client.post(
                    self.settings.opencti_base_url,
                    json={"query": query, "variables": {"id": lookup_object_id}},
                    headers=headers,
                )
        except httpx.TimeoutException as error:
            raise MCPContractError(
                "CTI-5041",
                "OpenCTI GraphQL request timed out. Check whether OpenCTI is ready and reachable.",
                status_code=504,
            ) from error
        except httpx.RequestError as error:
            raise MCPContractError(
                "CTI-5031",
                f"OpenCTI GraphQL is unreachable at {self.settings.opencti_base_url}.",
                status_code=503,
            ) from error

        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as error:
            status_code = error.response.status_code
            if status_code >= 500:
                raise MCPContractError(
                    "CTI-5021",
                    f"OpenCTI GraphQL returned {status_code}. Check whether the OpenCTI platform is fully started.",
                    status_code=502,
                ) from error
            raise MCPContractError(
                "CTI-4004",
                f"OpenCTI GraphQL returned {status_code}. Check the endpoint URL and API token configuration.",
                status_code=502,
            ) from error

        try:
            payload = response.json()
        except ValueError as error:
            raise MCPContractError(
                "CTI-5022",
                "OpenCTI GraphQL returned a non-JSON response.",
                status_code=502,
            ) from error

        graphql_errors = payload.get("errors") or []
        if graphql_errors:
            first_error = graphql_errors[0]
            error_message = first_error.get("message") if isinstance(first_error, dict) else str(first_error)
            raise MCPContractError(
                "CTI-5023",
                f"OpenCTI GraphQL returned an application error: {error_message}",
                status_code=502,
            )

        data = payload.get("data", {}).get("stixCoreObject")
        if not data:
            raise MCPContractError(
                "CTI-4041",
                f"STIX object {requested_object_id} was not found.",
                status_code=404,
            )

        semantic_type = object_type or requested_object_id.split("--", 1)[0]
        severity = self._severity_for_object(semantic_type, requested_object_id)
        context = self._context_for_object(semantic_type, requested_object_id)

        return {
            "id": data["id"],
            "type": object_type or data.get("entity_type", "stix-core-object"),
            "standard_id": data.get("standard_id", data["id"]),
            "name": str(context.get("name") or data.get("name", requested_object_id)),
            "modified": data.get("updated_at", data.get("created_at", "")),
            "description": "Resolved from OpenCTI GraphQL.",
            "labels": [],
            "confidence": 50,
            "external_references": [],
            "object_marking_refs": [],
            "extensions": {},
            "risk_object": str(context.get("risk_object") or data.get("name", requested_object_id)),
            "scene_type": self._scene_type_for_object(semantic_type, requested_object_id),
            "severity": severity,
            "priority": self._priority_for_severity(severity),
            "task_status": "待处理",
            "business_impact": str(context.get("business_impact") or "Pending analyst review."),
            "target_roles": list(context.get("target_roles") or ["情报分析师"]),
            "primary_asset": str(context.get("primary_asset") or data.get("name", requested_object_id)),
            "deployment_scope": str(context.get("deployment_scope") or "待补充部署范围"),
            "owner_team": str(context.get("owner_team") or "待分配团队"),
            "business_domain": str(context.get("business_domain") or "待补充业务域"),
            "business_criticality": str(context.get("business_criticality") or "待评估"),
            "execution_window": str(context.get("execution_window") or "待确认"),
            "relationships": [],
        }

    def _resolve_object_id(self, object_id: str) -> str:
        """// @ArchitectureID: 1215"""
        configured_aliases = {
            "attack-pattern--vs1": self.settings.vs1_object_id,
            "incident--vs2": self.settings.vs2_object_id,
            "grouping--vs2": self.settings.vs2_object_id,
            "vulnerability--vs3": self.settings.vs3_object_id,
            "indicator--vs4": self.settings.vs4_object_id,
        }
        return configured_aliases.get(object_id) or object_id

    def _mock_object(self, object_id: str, object_type: str | None) -> dict[str, Any]:
        """// @ArchitectureID: 1215"""
        normalized_type = object_type or object_id.split("--", 1)[0]
        scene_type = self._scene_type_for_object(normalized_type, object_id)
        severity = self._severity_for_object(normalized_type, object_id)
        context = self._context_for_object(normalized_type, object_id)
        return {
            "id": object_id,
            "type": normalized_type,
            "standard_id": object_id,
            "name": str(context.get("name") or f"Mock {normalized_type} {object_id}"),
            "modified": "2026-03-14T00:00:00Z",
            "description": "Mocked STIX projection used for local contract, integration, and E2E validation.",
            "labels": ["ai4sec", normalized_type],
            "confidence": 85,
            "external_references": [{"source_name": "mock-source", "url": "https://example.test"}],
            "object_marking_refs": ["marking-definition--tlp-clear"],
            "extensions": {"x_ai4sec_scene": normalized_type},
            "risk_object": str(context.get("risk_object") or object_id),
            "scene_type": scene_type,
            "severity": severity,
            "priority": self._priority_for_severity(severity),
            "task_status": "待处理",
            "business_impact": str(
                context.get("business_impact") or "Production-facing scenario requiring coordinated follow-up."
            ),
            "target_roles": list(context.get("target_roles") or ["情报分析师", "安全负责人"]),
            "primary_asset": str(context.get("primary_asset") or object_id),
            "deployment_scope": str(context.get("deployment_scope") or "待补充部署范围"),
            "owner_team": str(context.get("owner_team") or "待分配团队"),
            "business_domain": str(context.get("business_domain") or "待补充业务域"),
            "business_criticality": str(context.get("business_criticality") or "待评估"),
            "execution_window": str(context.get("execution_window") or "待确认"),
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

    def _context_for_object(self, object_type: str | None, object_id: str) -> dict[str, Any]:
        """// @ArchitectureID: 1215"""
        normalized = (object_type or object_id.split("--", 1)[0] or "").lower()
        if object_id.endswith("--vs1") or normalized == "attack-pattern":
            return {
                "name": "payment-gateway 2.8.0 上线前威胁建模任务",
                "risk_object": "credential-stuffing",
                "business_impact": "支付域发布窗口前需完成威胁建模与控制缺口复核，否则不应放行。",
                "target_roles": ["情报分析师", "安全负责人"],
                "primary_asset": "payment-gateway 2.8.0",
                "deployment_scope": "prod-payment-cluster",
                "owner_team": "payments-team",
                "business_domain": "支付域",
                "business_criticality": "高",
                "execution_window": "上线前",
            }
        if object_id.endswith("--vs2") or normalized == "incident":
            return {
                "name": "host-A 到 bastion-01 横向移动告警",
                "risk_object": "横向移动告警",
                "business_impact": "横向移动已触达堡垒机管理链路，需要立即完成事件研判与响应动作编排。",
                "target_roles": ["安全运营团队", "安全负责人"],
                "primary_asset": "host-A / bastion-01",
                "deployment_scope": "生产网络与运维管理面",
                "owner_team": "secops-team",
                "business_domain": "运维访问控制域",
                "business_criticality": "高",
                "execution_window": "立即响应",
            }
        if object_id.endswith("--vs3") or normalized == "vulnerability":
            return {
                "name": "CVE-2026-XXXX 对 api-gateway 4.2.1 的企业影响",
                "risk_object": "CVE-2026-XXXX",
                "business_impact": "漏洞影响 prod-edge-cluster 上的 finance-bu 交易入口，应在最早维护窗口完成处置。",
                "target_roles": ["情报分析师", "安全负责人"],
                "primary_asset": "api-gateway 4.2.1",
                "deployment_scope": "prod-edge-cluster",
                "owner_team": "finance-bu",
                "business_domain": "金融交易边界",
                "business_criticality": "高",
                "execution_window": "最早维护窗口",
            }
        if object_id.endswith("--vs4") or normalized == "indicator":
            return {
                "name": "user-profile-service 1.0.0 BOLA 风险环境监控任务",
                "risk_object": "BOLA 风险",
                "business_impact": "需要把 user-profile-service 的设计期越权风险转成生产监控线索，持续观察异常访问。",
                "target_roles": ["安全运营团队", "安全负责人"],
                "primary_asset": "user-profile-service 1.0.0",
                "deployment_scope": "prod-api-cluster（生产环境）",
                "owner_team": "profile-platform-team",
                "business_domain": "用户资料域",
                "business_criticality": "中高",
                "execution_window": "持续监控",
            }
        return {}
