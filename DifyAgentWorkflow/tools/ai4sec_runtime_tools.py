from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any


async def resolve_opencti_signal(
    bundle: dict[str, Any],
    resolver: Callable[[str], Awaitable[dict[str, Any] | None]],
) -> dict[str, Any]:
    """// @ArchitectureID: 1214"""
    objects = bundle.get("objects", [])
    if not objects:
        raise ValueError("Signal bundle does not contain STIX objects.")

    signal = objects[0]
    if not signal.get("x_opencti_lookup_required"):
        return signal

    lookup_id = signal.get("x_opencti_id") or signal.get("id")
    if not lookup_id:
        raise ValueError("Signal object does not contain a lookup id.")

    resolved = await resolver(str(lookup_id))
    if resolved is None:
        raise LookupError(f"Unable to resolve STIX object {lookup_id}.")
    return resolved


def route_entrypoint(entry_mode: str | None, user_request: str | None, selected_flow: str | None) -> str:
    """// @ArchitectureID: 1214"""
    if selected_flow in {"VS1", "VS2", "VS3", "VS4"}:
        return selected_flow

    lowered = (user_request or "").lower()
    routing_rules = {
        "VS1": ("威胁建模", "threat modeling", "发布"),
        "VS2": ("响应", "incident", "告警"),
        "VS3": ("漏洞", "vulnerability", "cve"),
        "VS4": ("监控", "rule", "sigma"),
    }
    for flow_name, keywords in routing_rules.items():
        if any(keyword.lower() in lowered for keyword in keywords):
            return flow_name

    if entry_mode == "webhook":
        return "VS3"
    return "VS4"


def build_notification_payload(scene: str, stix_object: dict[str, Any]) -> dict[str, Any]:
    """// @ArchitectureID: 1214"""
    object_name = stix_object.get("name", "Unknown STIX Object")
    object_id = stix_object.get("id", "unknown")
    template_map = {
        "VS1": "release-gate-decision",
        "VS2": "incident-response",
        "VS3": "vulnerability-alert",
        "VS4": "monitoring-rule-online",
    }
    return {
        "template_type": template_map.get(scene, "monitoring-rule-online"),
        "message_title": f"{scene} 结果通知: {object_name}",
        "message_summary": f"AI4SEC 已完成 {scene} 场景处理。",
        "business_impact": stix_object.get("description", "待业务复核"),
        "recommended_action": "请在 OpenCTI 中复核证据并执行后续动作。",
        "object_refs": [object_id],
        "severity_tier": "high",
        "event_type": f"ai4sec.{scene.lower()}.result.v1",
    }
