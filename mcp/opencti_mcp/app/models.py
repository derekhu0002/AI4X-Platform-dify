from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field, model_validator


ProjectionProfile = Literal["minimal", "summary", "analysis", "graph", "notification"]
ThreatModelMatchStrategy = Literal["exact-id", "exact-name", "fuzzy-id", "fuzzy-name"]


class QueryRequest(BaseModel):
    """// @ArchitectureID: 1215"""

    object_id: str = Field(min_length=1)
    object_type: str | None = None
    projection_profile: ProjectionProfile = "summary"
    fields: list[str] = Field(default_factory=list)
    exclude_fields: list[str] = Field(default_factory=list)
    include_relationships: bool = False
    relationship_depth: int = Field(default=0, ge=0, le=1)
    relationship_types: list[str] = Field(default_factory=list)
    page_size: int = Field(default=20, ge=1, le=100)
    cursor: str | None = None

    @model_validator(mode="after")
    def validate_graph_paging(self) -> "QueryRequest":
        """// @ArchitectureID: 1215"""
        if self.projection_profile == "graph" and self.page_size > 30:
            raise ValueError("MCP-4003: graph projection page_size must be <= 30")
        return self


class QueryResponse(BaseModel):
    """// @ArchitectureID: 1215"""

    items: list[dict[str, Any]]
    next_cursor: str | None = None
    has_more: bool = False
    source: Literal["mock", "opencti"]


class ThreatModelReportQueryRequest(BaseModel):
    """// @ArchitectureID: 1215"""

    report_ref: str = Field(min_length=1)


class ThreatModelReportMatch(BaseModel):
    """// @ArchitectureID: 1215"""

    report_id: str
    report_name: str
    match_strategy: ThreatModelMatchStrategy


class ThreatModelReportQueryResponse(BaseModel):
    """// @ArchitectureID: 1215"""

    matched_report: ThreatModelReportMatch
    bundle: dict[str, Any]
    analysis_input: dict[str, Any]
    download_filename: str
    source: Literal["mock", "opencti"]


class BundleWriteRequest(BaseModel):
    """// @ArchitectureID: 1215"""

    bundle: dict[str, Any]
    dry_run: bool = False


class BundleWriteResponse(BaseModel):
    """// @ArchitectureID: 1215"""

    accepted: bool
    persisted_object_ids: list[str]
    mode: Literal["mock", "opencti", "dry-run"]


class ErrorEnvelope(BaseModel):
    """// @ArchitectureID: 1215"""

    code: str
    message: str
