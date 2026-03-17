import pytest

from DifyAgentWorkflow.tools.ai4sec_runtime_tools import (
    build_opencti_writeback_bundle,
    ensure_human_review_gate,
)


def test_human_review_gate_must_pass_before_writeback() -> None:
    assert ensure_human_review_gate("approved") is True
    assert ensure_human_review_gate("通过") is True
    assert ensure_human_review_gate("pending") is False


def test_writeback_bundle_requires_human_review() -> None:
    with pytest.raises(PermissionError):
        build_opencti_writeback_bundle(
            stix_object={"id": "vulnerability--vs3", "type": "vulnerability"},
            review_status="pending",
            analyst_summary="待复核结论",
        )


def test_writeback_bundle_builds_note_after_review() -> None:
    bundle = build_opencti_writeback_bundle(
        stix_object={"id": "vulnerability--vs3", "type": "vulnerability"},
        review_status="approved",
        analyst_summary="人工复核通过，建议在维护窗口修复。",
    )
    assert bundle["type"] == "bundle"
    assert bundle["objects"][0]["type"] == "note"
    assert bundle["objects"][0]["object_refs"] == ["vulnerability--vs3"]
