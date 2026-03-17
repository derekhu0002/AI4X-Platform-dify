from __future__ import annotations

import asyncio
from dataclasses import dataclass
import json
from pathlib import Path
import re
from difflib import SequenceMatcher
import time
from typing import Any

import httpx

from mcp.opencti_mcp.app.models import (
    BundleWriteRequest,
    BundleWriteResponse,
    QueryRequest,
    QueryResponse,
    ThreatModelReportMatch,
    ThreatModelReportQueryRequest,
    ThreatModelReportQueryResponse,
)
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

DEFAULT_MINIMAL_STIX_FIELDS: dict[str, set[str]] = {
    "indicator": {"id", "type", "pattern", "pattern_type", "valid_from"},
    "vulnerability": {"id", "type", "name"},
    "incident": {"id", "type", "name"},
    "attack-pattern": {"id", "type", "name"},
    "grouping": {"id", "type", "name", "object_refs"},
    "note": {"id", "type", "content", "object_refs"},
    "opinion": {"id", "type", "opinion", "object_refs"},
    "relationship": {"id", "type", "relationship_type", "source_ref", "target_ref"},
}

THREAT_MODEL_BUNDLE_FIELDS: dict[str, set[str]] = {
    "report": {"id", "type", "spec_version", "name", "description", "published", "report_types", "object_refs"},
    "identity": {"id", "type", "spec_version", "name", "identity_class", "sectors"},
    "software": {"id", "type", "spec_version", "name", "version", "vendor"},
    "infrastructure": {"id", "type", "spec_version", "name", "description", "infrastructure_types"},
    "vulnerability": {"id", "type", "spec_version", "name", "description"},
    "attack-pattern": {"id", "type", "spec_version", "name", "description", "kill_chain_phases"},
    "course-of-action": {"id", "type", "spec_version", "name", "description"},
    "note": {"id", "type", "spec_version", "abstract", "content", "object_refs"},
    "opinion": {"id", "type", "spec_version", "opinion", "explanation", "object_refs"},
    "relationship": {"id", "type", "spec_version", "relationship_type", "description", "source_ref", "target_ref"},
}

THREAT_MODEL_BUNDLE_ORDER = {
    "report": 0,
    "identity": 1,
    "software": 2,
    "infrastructure": 3,
    "vulnerability": 4,
    "attack-pattern": 5,
    "course-of-action": 6,
    "note": 7,
    "opinion": 8,
    "relationship": 9,
}


@dataclass(frozen=True)
class LiveReportCandidate:
    """// @ArchitectureID: 1215"""

    internal_id: str
    report_id: str
    report_name: str
    description: str = ""
    published: str = ""


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
        self.minimal_stix_fields = self._load_minimal_field_matrix()

    async def query(self, request: QueryRequest) -> QueryResponse:
        """// @ArchitectureID: 1215"""
        stix_object = await self._load_object(request.object_id, request.object_type)
        fields = self._resolve_projection_fields(request, stix_object)
        projected = self._project_object(stix_object, fields, request)
        source = "mock" if self.settings.mock_mode else "opencti"
        return QueryResponse(items=[projected], source=source)

    async def query_threat_model_report(
        self,
        request: ThreatModelReportQueryRequest,
    ) -> ThreatModelReportQueryResponse:
        """// @ArchitectureID: 1215"""
        if self.settings.mock_mode:
            bundle = await self._load_mock_threat_model_bundle()
            matched_report = self._match_report(bundle, request.report_ref)
        else:
            matched_report, bundle = await self._load_live_threat_model_report_bundle(request.report_ref)
        filtered_bundle = self._build_threat_model_bundle(bundle, matched_report.report_id)
        analysis_input = self._build_threat_model_analysis_input(filtered_bundle, matched_report)
        source = "mock" if self.settings.mock_mode else "opencti"
        download_filename = self._build_download_filename(matched_report.report_name)
        return ThreatModelReportQueryResponse(
            matched_report=matched_report,
            bundle=filtered_bundle,
            analysis_input=analysis_input,
            download_filename=download_filename,
            source=source,
        )

    async def write_bundle(self, request: BundleWriteRequest) -> BundleWriteResponse:
        """// @ArchitectureID: 1215"""
        bundle = request.bundle
        if bundle.get("type") != "bundle":
            raise MCPContractError("MCP-4003", "Only STIX bundle payloads are accepted.")

        objects = bundle.get("objects", [])
        if not objects:
            raise MCPContractError("MCP-4003", "STIX bundle must contain at least one object.")

        self._validate_bundle_minimal_fields(objects)

        object_ids = [str(obj.get("id", "unknown")) for obj in objects]
        if request.dry_run:
            return BundleWriteResponse(accepted=True, persisted_object_ids=object_ids, mode="dry-run")
        if self.settings.mock_mode:
            return BundleWriteResponse(accepted=True, persisted_object_ids=object_ids, mode="mock")

        await self._write_bundle_to_opencti(bundle)
        await self._verify_persisted_objects(object_ids)
        return BundleWriteResponse(accepted=True, persisted_object_ids=object_ids, mode="opencti")

    async def probe_write_capability(self) -> dict[str, str]:
        """// @ArchitectureID: 1215"""
        if self.settings.mock_mode:
            return {
                "status": "skipped",
                "code": "MCP-MOCK",
                "detail": "mock mode enabled; write capability probe skipped.",
            }

        if not self.settings.opencti_api_token:
            return {
                "status": "blocked",
                "code": "CTI-AUTH0",
                "detail": "OpenCTI API token is empty; cannot verify write permission.",
            }

        mutation = """
        mutation ProbeImportPush($bundle: String!, $update: Boolean!) {
          importPush(type: "text/json", file: $bundle, update: $update)
        }
        """

        # Use an intentionally invalid probe bundle to avoid writing data during startup probe.
        invalid_probe_bundle = {"type": "bundle", "id": "bundle--startup-probe", "objects": []}

        try:
            await self._post_graphql(
                query=mutation,
                variables={"bundle": json.dumps(invalid_probe_bundle, ensure_ascii=False), "update": False},
                operation_name="probe_importPush",
            )
            return {
                "status": "ready",
                "code": "CTI-WRITE-OK",
                "detail": "OpenCTI import mutation responded successfully during startup probe.",
            }
        except MCPContractError as error:
            return self._classify_probe_error(error)

    def _load_minimal_field_matrix(self) -> dict[str, set[str]]:
        """// @ArchitectureID: 1215"""
        config_path = Path(self.settings.stix_minimal_field_matrix_path)
        if not config_path.is_absolute():
            config_path = Path(__file__).resolve().parents[3] / config_path

        if not config_path.exists():
            return DEFAULT_MINIMAL_STIX_FIELDS

        try:
            payload = json.loads(config_path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as error:
            raise MCPContractError(
                "MCP-4005",
                f"Unable to load STIX minimal field matrix from {config_path}.",
                status_code=500,
            ) from error

        matrix = payload.get("matrix", {}) if isinstance(payload, dict) else {}
        normalized: dict[str, set[str]] = {}
        for object_type, fields in matrix.items():
            if isinstance(object_type, str) and isinstance(fields, list):
                normalized[object_type.lower()] = {str(field) for field in fields}

        return normalized or DEFAULT_MINIMAL_STIX_FIELDS

    async def _load_mock_threat_model_bundle(self) -> dict[str, Any]:
        """// @ArchitectureID: 1215"""
        bundle_path = Path(__file__).resolve().parents[3] / "tests/validation/test-data/vs1-payment-threat-model-bundle.json"
        try:
            payload = json.loads(bundle_path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as error:
            raise MCPContractError(
                "MCP-4007",
                f"Unable to load threat-model bundle fixture from {bundle_path}.",
                status_code=500,
            ) from error

        if payload.get("type") != "bundle":
            raise MCPContractError("MCP-4008", "Threat-model fixture must be a STIX bundle.", status_code=500)
        return payload

    async def _load_live_threat_model_report_bundle(
        self,
        report_ref: str,
    ) -> tuple[ThreatModelReportMatch, dict[str, Any]]:
        """// @ArchitectureID: 1215"""
        candidates = await self._list_live_reports()
        matched_report, candidate = self._match_live_report_candidate(candidates, report_ref)
        bundle = await self._fetch_live_threat_model_bundle(candidate)
        return matched_report, bundle

    async def _list_live_reports(self) -> list[LiveReportCandidate]:
        """// @ArchitectureID: 1215"""
        query = """
        query ListReports($first: Int!) {
          reports(first: $first) {
            edges {
              node {
                id
                standard_id
                name
                description
                published
              }
            }
          }
        }
        """
        payload = await self._post_graphql(
            query=query,
            variables={"first": 100},
            operation_name="reports",
        )
        edges = payload.get("data", {}).get("reports", {}).get("edges", [])
        candidates: list[LiveReportCandidate] = []
        for edge in edges:
            node = edge.get("node") or {}
            internal_id = str(node.get("id") or "")
            report_id = str(node.get("standard_id") or "")
            report_name = str(node.get("name") or "")
            if not internal_id or not report_id or not report_name:
                continue
            candidates.append(
                LiveReportCandidate(
                    internal_id=internal_id,
                    report_id=report_id,
                    report_name=report_name,
                    description=str(node.get("description") or ""),
                    published=str(node.get("published") or ""),
                )
            )

        if not candidates:
            raise MCPContractError("CTI-4041", "No report object was found in OpenCTI.", status_code=404)
        return candidates

    def _match_live_report_candidate(
        self,
        candidates: list[LiveReportCandidate],
        report_ref: str,
    ) -> tuple[ThreatModelReportMatch, LiveReportCandidate]:
        """// @ArchitectureID: 1215"""
        normalized_ref = self._normalize_match_text(report_ref)
        for candidate in candidates:
            if normalized_ref in {
                self._normalize_match_text(candidate.internal_id),
                self._normalize_match_text(candidate.report_id),
            }:
                return (
                    ThreatModelReportMatch(
                        report_id=candidate.report_id,
                        report_name=candidate.report_name,
                        match_strategy="exact-id",
                    ),
                    candidate,
                )
            if normalized_ref == self._normalize_match_text(candidate.report_name):
                return (
                    ThreatModelReportMatch(
                        report_id=candidate.report_id,
                        report_name=candidate.report_name,
                        match_strategy="exact-name",
                    ),
                    candidate,
                )

        if normalized_ref.startswith("report--"):
            alias_name = self._resolve_report_name_from_local_bundles(report_ref)
            if alias_name and self._normalize_match_text(alias_name) != normalized_ref:
                for candidate in candidates:
                    if self._normalize_match_text(candidate.report_name) == self._normalize_match_text(alias_name):
                        return (
                            ThreatModelReportMatch(
                                report_id=candidate.report_id,
                                report_name=candidate.report_name,
                                match_strategy="exact-name",
                            ),
                            candidate,
                        )

        matched = self._score_live_report_candidates(candidates, normalized_ref)
        if matched is None:
            alias_name = self._resolve_report_name_from_local_bundles(report_ref)
            if alias_name and self._normalize_match_text(alias_name) != normalized_ref:
                matched = self._score_live_report_candidates(candidates, self._normalize_match_text(alias_name))
                if matched is not None:
                    strategy, candidate = matched
                    exact_strategy = "exact-name" if strategy == "fuzzy-name" else strategy
                    return (
                        ThreatModelReportMatch(
                            report_id=candidate.report_id,
                            report_name=candidate.report_name,
                            match_strategy=exact_strategy,
                        ),
                        candidate,
                    )
            raise MCPContractError(
                "CTI-4041",
                f"No report matched '{report_ref}' after exact and fuzzy lookup.",
                status_code=404,
            )

        strategy, candidate = matched
        return (
            ThreatModelReportMatch(
                report_id=candidate.report_id,
                report_name=candidate.report_name,
                match_strategy=strategy,
            ),
            candidate,
        )

    def _score_live_report_candidates(
        self,
        candidates: list[LiveReportCandidate],
        normalized_ref: str,
    ) -> tuple[str, LiveReportCandidate] | None:
        """// @ArchitectureID: 1215"""
        scored_candidates: list[tuple[float, str, LiveReportCandidate]] = []
        for candidate in candidates:
            scored_candidates.append(
                (
                    self._score_fuzzy_match(normalized_ref, self._normalize_match_text(candidate.report_id)),
                    "fuzzy-id",
                    candidate,
                )
            )
            scored_candidates.append(
                (
                    self._score_fuzzy_match(normalized_ref, self._normalize_match_text(candidate.report_name)),
                    "fuzzy-name",
                    candidate,
                )
            )

        if not scored_candidates:
            return None

        best_score, strategy, candidate = max(scored_candidates, key=lambda item: item[0])
        if best_score < 0.35:
            return None
        return strategy, candidate

    def _resolve_report_name_from_local_bundles(self, report_ref: str) -> str | None:
        """// @ArchitectureID: 1215"""
        normalized_ref = self._normalize_match_text(report_ref)
        test_data_dir = Path(__file__).resolve().parents[3] / "tests/validation/test-data"
        if not test_data_dir.exists():
            return None

        for bundle_path in sorted(test_data_dir.glob("*.json")):
            try:
                payload = json.loads(bundle_path.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                continue
            if payload.get("type") != "bundle":
                continue
            for stix_object in payload.get("objects", []):
                if str(stix_object.get("type") or "").lower() != "report":
                    continue
                object_id = self._normalize_match_text(str(stix_object.get("id") or ""))
                if object_id == normalized_ref:
                    report_name = str(stix_object.get("name") or "").strip()
                    return report_name or None
        return None

    async def _fetch_live_threat_model_bundle(self, candidate: LiveReportCandidate) -> dict[str, Any]:
        """// @ArchitectureID: 1215"""
        query = """
        query ThreatModelReportBundle($id: String!, $first: Int!) {
          stixCoreObject(id: $id) {
            id
            standard_id
            entity_type
            representative {
              main
              secondary
            }
            ... on Report {
              report_name: name
              description
              published
              report_types
              objects(first: $first) {
                edges {
                  node {
                    __typename
                    ... on BasicObject {
                      id
                      standard_id
                      entity_type
                    }
                    ... on StixObject {
                      representative {
                        main
                        secondary
                      }
                    }
                    ... on AttackPattern {
                      attack_pattern_name: name
                      description
                    }
                    ... on Indicator {
                      indicator_name: name
                      description
                      pattern_type
                      pattern
                      valid_from
                    }
                    ... on Software {
                      software_name: name
                      vendor
                      version
                    }
                    ... on Infrastructure {
                      infrastructure_name: name
                      description
                      infrastructure_types
                    }
                    ... on Identity {
                      identity_name: name
                    }
                    ... on Vulnerability {
                      vulnerability_name: name
                      description
                    }
                    ... on CourseOfAction {
                      course_of_action_name: name
                      description
                    }
                    ... on Note {
                      content
                    }
                    ... on Opinion {
                      opinion
                      explanation
                    }
                  }
                }
              }
            }
          }
        }
        """
        payload = await self._post_graphql(
            query=query,
            variables={"id": candidate.internal_id, "first": 200},
            operation_name="stixCoreObject",
        )
        report = payload.get("data", {}).get("stixCoreObject")
        if not report:
            raise MCPContractError(
                "CTI-4041",
                f"Report {candidate.report_id} was not found in OpenCTI.",
                status_code=404,
            )

        object_edges = report.get("objects", {}).get("edges", [])
        stix_objects: list[dict[str, Any]] = []
        related_internal_ids: list[str] = []
        related_standard_ids: set[str] = set()

        for edge in object_edges:
            node = edge.get("node") or {}
            stix_object = self._convert_live_node_to_stix(node)
            if stix_object is None:
                continue
            stix_objects.append(stix_object)
            internal_id = str(node.get("id") or "")
            standard_id = str(stix_object.get("id") or "")
            if internal_id and standard_id:
                related_internal_ids.append(internal_id)
                related_standard_ids.add(standard_id)

        report_object = {
            "type": "report",
            "spec_version": "2.1",
            "id": candidate.report_id,
            "name": str(report.get("report_name") or candidate.report_name),
            "description": str(report.get("description") or candidate.description),
            "published": str(report.get("published") or candidate.published),
            "report_types": list(report.get("report_types") or []),
            "object_refs": [str(stix_object.get("id")) for stix_object in stix_objects if stix_object.get("id")],
        }

        relationship_objects = await self._fetch_live_relationship_objects(
            related_internal_ids,
            related_standard_ids,
        )
        return {
            "type": "bundle",
            "id": f"bundle--{candidate.report_id.split('--', 1)[-1]}",
            "objects": [report_object, *stix_objects, *relationship_objects],
        }

    async def _fetch_live_relationship_objects(
        self,
        internal_ids: list[str],
        allowed_standard_ids: set[str],
    ) -> list[dict[str, Any]]:
        """// @ArchitectureID: 1215"""
        if not internal_ids or not allowed_standard_ids:
            return []

        query = """
        query ThreatModelRelationships($ids: [String!], $first: Int!) {
          fromRelationships: stixCoreRelationships(first: $first, fromId: $ids) {
            edges {
              node {
                id
                standard_id
                entity_type
                relationship_type
                description
                from {
                  ... on BasicObject {
                    standard_id
                  }
                }
                to {
                  ... on BasicObject {
                    standard_id
                  }
                }
              }
            }
          }
          toRelationships: stixCoreRelationships(first: $first, toId: $ids) {
            edges {
              node {
                id
                standard_id
                entity_type
                relationship_type
                description
                from {
                  ... on BasicObject {
                    standard_id
                  }
                }
                to {
                  ... on BasicObject {
                    standard_id
                  }
                }
              }
            }
          }
        }
        """
        payload = await self._post_graphql(
            query=query,
            variables={"ids": internal_ids, "first": 200},
            operation_name="stixCoreRelationships",
        )

        relationship_objects: dict[str, dict[str, Any]] = {}
        for key in ("fromRelationships", "toRelationships"):
            edges = payload.get("data", {}).get(key, {}).get("edges", [])
            for edge in edges:
                node = edge.get("node") or {}
                source_ref = str((node.get("from") or {}).get("standard_id") or "")
                target_ref = str((node.get("to") or {}).get("standard_id") or "")
                relationship_id = str(node.get("standard_id") or node.get("id") or "")
                if not relationship_id or source_ref not in allowed_standard_ids or target_ref not in allowed_standard_ids:
                    continue
                relationship_objects[relationship_id] = {
                    "type": "relationship",
                    "spec_version": "2.1",
                    "id": relationship_id,
                    "relationship_type": str(node.get("relationship_type") or "related-to"),
                    "source_ref": source_ref,
                    "target_ref": target_ref,
                    **(
                        {"description": str(node.get("description") or "")}
                        if str(node.get("description") or "")
                        else {}
                    ),
                }
        return list(relationship_objects.values())

    def _convert_live_node_to_stix(self, node: dict[str, Any]) -> dict[str, Any] | None:
        """// @ArchitectureID: 1215"""
        object_id = str(node.get("standard_id") or node.get("id") or "")
        object_type = self._normalize_entity_type(str(node.get("entity_type") or node.get("__typename") or ""))
        if not object_id or object_type not in THREAT_MODEL_BUNDLE_FIELDS or object_type == "report":
            return None

        representative = node.get("representative") or {}
        description = str(node.get("description") or representative.get("secondary") or "")
        stix_object: dict[str, Any] = {
            "type": object_type,
            "spec_version": "2.1",
            "id": object_id,
        }

        if object_type == "attack-pattern":
            stix_object["name"] = str(node.get("attack_pattern_name") or representative.get("main") or object_id)
            if description:
                stix_object["description"] = description
            kill_chain_phases = list(node.get("kill_chain_phases") or [])
            if kill_chain_phases:
                stix_object["kill_chain_phases"] = kill_chain_phases
            return stix_object

        if object_type == "indicator":
            stix_object["name"] = str(node.get("indicator_name") or representative.get("main") or object_id)
            if description:
                stix_object["description"] = description
            if node.get("pattern_type"):
                stix_object["pattern_type"] = str(node.get("pattern_type"))
            if node.get("pattern"):
                stix_object["pattern"] = str(node.get("pattern"))
            if node.get("valid_from"):
                stix_object["valid_from"] = str(node.get("valid_from"))
            return stix_object

        if object_type == "software":
            stix_object["name"] = str(node.get("software_name") or representative.get("main") or object_id)
            if node.get("vendor"):
                stix_object["vendor"] = str(node.get("vendor"))
            if node.get("version"):
                stix_object["version"] = str(node.get("version"))
            return stix_object

        if object_type == "infrastructure":
            stix_object["name"] = str(node.get("infrastructure_name") or representative.get("main") or object_id)
            if description:
                stix_object["description"] = description
            infrastructure_types = list(node.get("infrastructure_types") or [])
            if infrastructure_types:
                stix_object["infrastructure_types"] = infrastructure_types
            return stix_object

        if object_type == "identity":
            stix_object["name"] = str(node.get("identity_name") or representative.get("main") or object_id)
            if node.get("identity_class"):
                stix_object["identity_class"] = str(node.get("identity_class"))
            sectors = list(node.get("sectors") or [])
            if sectors:
                stix_object["sectors"] = sectors
            return stix_object

        if object_type == "vulnerability":
            stix_object["name"] = str(node.get("vulnerability_name") or representative.get("main") or object_id)
            if description:
                stix_object["description"] = description
            return stix_object

        if object_type == "course-of-action":
            stix_object["name"] = str(node.get("course_of_action_name") or representative.get("main") or object_id)
            if description:
                stix_object["description"] = description
            return stix_object

        if object_type == "note":
            if representative.get("main"):
                stix_object["abstract"] = str(representative.get("main"))
            if node.get("content"):
                stix_object["content"] = str(node.get("content"))
            elif description:
                stix_object["content"] = description
            return stix_object

        if object_type == "opinion":
            if node.get("opinion"):
                stix_object["opinion"] = str(node.get("opinion"))
            if node.get("explanation"):
                stix_object["explanation"] = str(node.get("explanation"))
            return stix_object

        return None

    def _normalize_entity_type(self, entity_type: str) -> str:
        """// @ArchitectureID: 1215"""
        return entity_type.strip().lower().replace("_", "-")

    def _match_report(self, bundle: dict[str, Any], report_ref: str) -> ThreatModelReportMatch:
        """// @ArchitectureID: 1215"""
        reports = [obj for obj in bundle.get("objects", []) if str(obj.get("type", "")).lower() == "report"]
        if not reports:
            raise MCPContractError("CTI-4041", "No report object was found in the threat-model bundle.", status_code=404)

        normalized_ref = self._normalize_match_text(report_ref)
        for report in reports:
            if normalized_ref == self._normalize_match_text(str(report.get("id", ""))):
                return ThreatModelReportMatch(
                    report_id=str(report.get("id", "")),
                    report_name=str(report.get("name", "")),
                    match_strategy="exact-id",
                )
            if normalized_ref == self._normalize_match_text(str(report.get("name", ""))):
                return ThreatModelReportMatch(
                    report_id=str(report.get("id", "")),
                    report_name=str(report.get("name", "")),
                    match_strategy="exact-name",
                )

        scored_candidates: list[tuple[float, str, dict[str, Any]]] = []
        for report in reports:
            report_id = str(report.get("id", ""))
            report_name = str(report.get("name", ""))
            scored_candidates.append((self._score_fuzzy_match(normalized_ref, self._normalize_match_text(report_id)), "fuzzy-id", report))
            scored_candidates.append((self._score_fuzzy_match(normalized_ref, self._normalize_match_text(report_name)), "fuzzy-name", report))

        best_score, strategy, best_report = max(scored_candidates, key=lambda item: item[0])
        if best_score < 0.35:
            raise MCPContractError(
                "CTI-4041",
                f"No report matched '{report_ref}' after exact and fuzzy lookup.",
                status_code=404,
            )

        return ThreatModelReportMatch(
            report_id=str(best_report.get("id", "")),
            report_name=str(best_report.get("name", "")),
            match_strategy=strategy,
        )

    def _normalize_match_text(self, value: str) -> str:
        """// @ArchitectureID: 1215"""
        compact = re.sub(r"\s+", " ", value or "").strip().lower()
        return compact

    def _score_fuzzy_match(self, query: str, candidate: str) -> float:
        """// @ArchitectureID: 1215"""
        if not query or not candidate:
            return 0.0
        if query in candidate or candidate in query:
            return 1.0
        return SequenceMatcher(None, query, candidate).ratio()

    def _build_threat_model_bundle(self, bundle: dict[str, Any], report_id: str) -> dict[str, Any]:
        """// @ArchitectureID: 1215"""
        objects = bundle.get("objects", [])
        objects_by_id = {str(obj.get("id", "")): obj for obj in objects}
        report = objects_by_id.get(report_id)
        if report is None:
            raise MCPContractError("CTI-4041", f"Report {report_id} was not found in the threat-model bundle.", status_code=404)

        included_ids = {report_id, *[str(object_id) for object_id in report.get("object_refs", [])]}
        changed = True
        while changed:
            changed = False
            for stix_object in objects:
                object_type = str(stix_object.get("type", "")).lower()
                object_id = str(stix_object.get("id", ""))
                if object_type == "relationship":
                    source_ref = str(stix_object.get("source_ref", ""))
                    target_ref = str(stix_object.get("target_ref", ""))
                    if object_id in included_ids or source_ref in included_ids or target_ref in included_ids:
                        for related_id in (object_id, source_ref, target_ref):
                            if related_id and related_id not in included_ids:
                                included_ids.add(related_id)
                                changed = True

        filtered_objects = []
        for stix_object in objects:
            object_id = str(stix_object.get("id", ""))
            object_type = str(stix_object.get("type", "")).lower()
            if object_id not in included_ids or object_type not in THREAT_MODEL_BUNDLE_FIELDS:
                continue
            filtered_objects.append(self._filter_threat_model_object(stix_object))

        filtered_objects.sort(
            key=lambda item: (
                THREAT_MODEL_BUNDLE_ORDER.get(str(item.get("type", "")).lower(), 99),
                str(item.get("name", item.get("id", ""))),
            )
        )
        return {
            "type": "bundle",
            "id": str(bundle.get("id", "bundle--threat-model-query")),
            "objects": filtered_objects,
        }

    def _filter_threat_model_object(self, stix_object: dict[str, Any]) -> dict[str, Any]:
        """// @ArchitectureID: 1215"""
        object_type = str(stix_object.get("type", "")).lower()
        allowed_fields = THREAT_MODEL_BUNDLE_FIELDS[object_type]
        return {field: stix_object.get(field) for field in allowed_fields if field in stix_object}

    def _build_threat_model_analysis_input(
        self,
        bundle: dict[str, Any],
        matched_report: ThreatModelReportMatch,
    ) -> dict[str, Any]:
        """// @ArchitectureID: 1215"""
        objects = bundle.get("objects", [])
        components = [
            str(obj.get("name"))
            for obj in objects
            if str(obj.get("type", "")).lower() in {"software", "infrastructure"} and obj.get("name")
        ]
        assets = [
            str(obj.get("name"))
            for obj in objects
            if str(obj.get("type", "")).lower() == "identity" and obj.get("name")
        ]
        report_object = next(
            (obj for obj in objects if str(obj.get("id", "")) == matched_report.report_id),
            {"name": matched_report.report_name, "description": ""},
        )
        return {
            "methodology": "TARA+STRIDE",
            "report": {
                "id": matched_report.report_id,
                "name": matched_report.report_name,
                "description": str(report_object.get("description", "")),
                "match_strategy": matched_report.match_strategy,
            },
            "components": components,
            "assets": assets,
            "bundle": bundle,
            "architecture_description": json.dumps(bundle, ensure_ascii=False),
        }

    def _build_download_filename(self, report_name: str) -> str:
        """// @ArchitectureID: 1215"""
        sanitized = re.sub(r"[^A-Za-z0-9._-]+", "-", report_name.strip()).strip("-") or "threat-model"
        return f"{sanitized}-threat-model.json"

    def _validate_bundle_minimal_fields(self, objects: list[dict[str, Any]]) -> None:
        """// @ArchitectureID: 1215"""
        for stix_object in objects:
            object_type = str(stix_object.get("type", "")).lower()
            object_id = str(stix_object.get("id", "unknown"))
            required_fields = self.minimal_stix_fields.get(object_type)
            if not required_fields:
                continue

            missing = sorted(field for field in required_fields if stix_object.get(field) in (None, "", []))
            if missing:
                raise MCPContractError(
                    "MCP-4006",
                    f"STIX object {object_id} is missing required fields: {', '.join(missing)}",
                )

    async def _write_bundle_to_opencti(self, bundle: dict[str, Any]) -> None:
        """// @ArchitectureID: 1215"""
        mutation = """
        mutation ImportPush($bundle: String!, $update: Boolean!) {
          importPush(type: "text/json", file: $bundle, update: $update)
        }
        """
        try:
            await self._post_graphql(
                query=mutation,
                variables={"bundle": json.dumps(bundle, ensure_ascii=False), "update": True},
                operation_name="importPush",
            )
        except MCPContractError as error:
            if self._is_missing_mutation_error(error, "importPush"):
                raise MCPContractError(
                    "CTI-5024",
                    "OpenCTI GraphQL schema does not expose mutation 'importPush'. "
                    "This is usually caused by OpenCTI version/schema differences or insufficient API token permissions. "
                    "Please verify the token role has import privileges and confirm the target OpenCTI deployment supports bundle import mutation for this integration.",
                    status_code=502,
                ) from error
            raise

    def _is_missing_mutation_error(self, error: MCPContractError, mutation_name: str) -> bool:
        """// @ArchitectureID: 1215"""
        message = (error.message or "").lower()
        return (
            error.code == "CTI-5023"
            and "cannot query field" in message
            and f'"{mutation_name.lower()}"' in message
            and "on type \"mutation\"" in message
        )

    def _classify_probe_error(self, error: MCPContractError) -> dict[str, str]:
        """// @ArchitectureID: 1215"""
        message = (error.message or "").lower()
        if self._is_missing_mutation_error(error, "importPush"):
            return {
                "status": "blocked",
                "code": "CTI-5024",
                "detail": "OpenCTI schema does not expose importPush mutation. Check version compatibility or token scope.",
            }

        permission_markers = ["not authorized", "forbidden", "permission", "access denied", "unauthorized"]
        if any(marker in message for marker in permission_markers):
            return {
                "status": "blocked",
                "code": "CTI-AUTH1",
                "detail": "OpenCTI token is reachable but appears to lack import permission.",
            }

        if error.code in {"CTI-5031", "CTI-5041", "CTI-5021"}:
            return {
                "status": "blocked",
                "code": error.code,
                "detail": "OpenCTI endpoint is unreachable or unstable during startup probe.",
            }

        if error.code == "CTI-5023":
            return {
                "status": "reachable",
                "code": "CTI-PROBE-GQL",
                "detail": "OpenCTI mutation endpoint is reachable; probe payload was rejected by GraphQL/application rule.",
            }

        return {
            "status": "blocked",
            "code": error.code,
            "detail": "OpenCTI write capability probe failed with an unclassified error.",
        }

    async def _verify_persisted_objects(self, object_ids: list[str]) -> None:
        """// @ArchitectureID: 1215"""
        deadline = time.monotonic() + max(self.settings.writeback_verify_window_seconds, 0.1)
        unresolved = set(object_ids)

        while unresolved and time.monotonic() <= deadline:
            current = list(unresolved)
            for object_id in current:
                try:
                    await self._fetch_opencti_object(object_id, object_id, None)
                    unresolved.discard(object_id)
                except MCPContractError as error:
                    if error.code != "CTI-4041":
                        raise

            if unresolved and time.monotonic() <= deadline:
                await asyncio.sleep(0.1)

        if unresolved:
            missing = ", ".join(sorted(unresolved))
            raise MCPContractError(
                "CTI-4091",
                f"Writeback verification failed within {self.settings.writeback_verify_window_seconds:.1f}s for: {missing}",
                status_code=409,
            )

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
        payload = await self._post_graphql(
            query=query,
            variables={"id": lookup_object_id},
            operation_name="stixCoreObject",
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

    def _graphql_headers(self) -> dict[str, str]:
        """// @ArchitectureID: 1215"""
        headers = {"Content-Type": "application/json"}
        if self.settings.opencti_api_token:
            headers["Authorization"] = f"Bearer {self.settings.opencti_api_token}"
        return headers

    async def _post_graphql(self, query: str, variables: dict[str, Any], operation_name: str) -> dict[str, Any]:
        """// @ArchitectureID: 1215"""
        try:
            async with httpx.AsyncClient(
                timeout=self.settings.request_timeout_seconds,
                trust_env=False,
            ) as client:
                response = await client.post(
                    self.settings.opencti_base_url,
                    json={"query": query, "variables": variables},
                    headers=self._graphql_headers(),
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
                f"OpenCTI GraphQL returned an application error in {operation_name}: {error_message}",
                status_code=502,
            )

        return payload

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
