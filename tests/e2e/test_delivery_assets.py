from pathlib import Path

import yaml


def test_workflow_asset_contains_menu_and_intent_routing() -> None:
    workflow_path = Path("DifyAgentWorkflow/ai4sec_unified_workflow.yaml")
    workflow = yaml.safe_load(workflow_path.read_text(encoding="utf-8"))
    assert workflow["kind"] == "app"
    nodes = {node["id"]: node for node in workflow["workflow"]["graph"]["nodes"]}
    assert "start-node" in nodes
    assert nodes["route-intent"]["data"]["type"] == "if-else"
    assert workflow["metadata"]["webhook"]["auth_required"] is False


def test_python_tool_asset_exists() -> None:
    tool_path = Path("DifyAgentWorkflow/tools/ai4sec_runtime_tools.py")
    assert tool_path.exists()
    content = tool_path.read_text(encoding="utf-8")
    assert "resolve_opencti_signal" in content
    assert "route_entrypoint" in content
