from pathlib import Path

import yaml


def test_workflow_asset_contains_menu_and_intent_routing() -> None:
    workflow_path = Path("DifyAgentWorkflow/ai4sec_unified_workflow.yaml")
    workflow = yaml.safe_load(workflow_path.read_text(encoding="utf-8"))
    assert workflow["kind"] == "app"
    nodes = {node["id"]: node for node in workflow["workflow"]["graph"]["nodes"]}
    assert "start_node" in nodes
    assert nodes["route-intent"]["data"]["type"] == "if-else"
    assert workflow["metadata"]["webhook"]["auth_required"] is False


def test_python_tool_asset_exists() -> None:
    tool_path = Path("DifyAgentWorkflow/tools/ai4sec_runtime_tools.py")
    assert tool_path.exists()
    content = tool_path.read_text(encoding="utf-8")
    assert "resolve_opencti_signal" in content
    assert "route_entrypoint" in content


def test_dedicated_webhook_workflow_asset_exists() -> None:
    workflow_path = Path("DifyAgentWorkflow/ai4sec_opencti_webhook_workflow.yaml")
    workflow = yaml.safe_load(workflow_path.read_text(encoding="utf-8"))
    assert workflow["kind"] == "app"
    assert workflow["app"]["mode"] == "workflow"
    environment_names = {item["name"] for item in workflow["workflow"]["environment_variables"]}
    assert "OPENCTI_GRAPHQL_URL" in environment_names
    assert "OPENCTI_ADMIN_TOKEN" in environment_names
    assert "OPENCTI_MCP_URL" not in environment_names
    nodes = {node["id"]: node for node in workflow["workflow"]["graph"]["nodes"]}
    assert "webhook-trigger" in nodes
    assert nodes["webhook-trigger"]["data"]["type"] == "trigger-webhook"
    trigger_variables = {item["variable"] for item in nodes["webhook-trigger"]["data"]["variables"]}
    assert "_webhook_raw" in trigger_variables
    normalize_code = nodes["normalize_webhook"]["data"]["code"]
    assert "software_name: name vendor version" in normalize_code
    assert "... on Software { name description vendor version }" not in normalize_code
    assert nodes["query_opencti"]["data"]["url"] == "{{#env.OPENCTI_GRAPHQL_URL#}}"
    assert nodes["query_opencti"]["data"]["headers"] == "Authorization: Bearer {{#env.OPENCTI_ADMIN_TOKEN#}}"
    assert "Risk Score" in nodes["answer-webhook"]["data"]["answer"]


def test_threat_model_workflow_contains_visual_summary_chain() -> None:
    workflow_path = Path("DifyAgentWorkflow/ai4sec_threat_modeling_workflow.yaml")
    workflow = yaml.safe_load(workflow_path.read_text(encoding="utf-8"))
    nodes = {node["id"]: node for node in workflow["workflow"]["graph"]["nodes"]}
    assert "llm_visual_summary" in nodes
    assert "prepare_visual_summary_input" in nodes
    prepare_code = nodes["prepare_visual_summary_input"]["data"]["code"]
    assert "'topology': {" in prepare_code
    assert "_register_relationship(relationship_registry, 'mitigates'" in prepare_code
    prompt_template = nodes["llm_visual_summary"]["data"]["prompt_template"]
    assert any("prepare_visual_summary_input.visual_summary_input" in item.get("text", "") for item in prompt_template)
    assert any("STIX-compliant" in item.get("text", "") for item in prompt_template)
    format_variables = {
        item["variable"]: item["value_selector"]
        for item in nodes["format_threat_model"]["data"]["variables"]
    }
    assert format_variables["visual_summary_input_json"] == ["prepare_visual_summary_input", "visual_summary_input"]
    format_code = nodes["format_threat_model"]["data"]["code"]
    assert "def _build_mermaid(topology: dict) -> str:" in format_code
    answer_text = nodes["answer_threat_model"]["data"]["answer"]
    assert "{{#format_threat_model.visual_summary_markdown#}}" in answer_text
    assert answer_text.index("{{#format_threat_model.visual_summary_markdown#}}") < answer_text.index("{{#format_threat_model.analysis_json#}}")
