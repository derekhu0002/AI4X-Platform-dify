feat(workflows): add webhook GraphQL risk and visual summary

Commit Body

- Feature:
	- Added direct OpenCTI GraphQL querying to `DifyAgentWorkflow/ai4sec_opencti_webhook_workflow.yaml`, including one-hop relationship retrieval and richer webhook outputs for risk score, affected infrastructure, affected products, priority recommendation, and decision summary.
	- Added a visual-summary chain to `DifyAgentWorkflow/ai4sec_threat_modeling_workflow.yaml` with `prepare_visual_summary_input`, `llm_visual_summary`, and final output wiring so Mermaid and grouped Markdown tables are rendered before the JSON payload.
	- Added a realistic OpenCTI sample bundle under `design/originaldata/2026-03-18t14_39_30.193z_tlp_all_(exportfilestix2)_report-vpd design_full.json` to support iteration validation against the target vulnerability.
- Fix:
	- Fixed OpenCTI 6.9 GraphQL compatibility in the webhook workflow by aliasing fragment-local `name` fields, removing unsupported `Software.description` and `Identity.description`, and switching the HTTP node to `Authorization: Bearer {{#env.OPENCTI_ADMIN_TOKEN#}}`.
	- Fixed the webhook signal template in `external_opencti/opencti_webhook_signal_template.ejs` so default and lookup IDs fall back to `vulnerability--693c68fd-9a33-5d6d-b44e-407b6a48b05b` instead of generating invalid `vulnerability--instanceId` values.
	- Fixed YAML structure regressions introduced during workflow editing so Dify code nodes keep valid `data` blocks and import correctly.
- Refactor:
	- Refactored threat-model visual rendering to build an explicit STIX-oriented topology bundle and generate Mermaid deterministically in `format_threat_model` instead of trusting raw LLM diagram syntax.
	- Refactored webhook response shaping to compute contextual risk directly from GraphQL payloads while preserving existing summary fields.
- Build/Release:
	- Expanded `tests/e2e/test_delivery_assets.py` to assert webhook GraphQL env/header/query contracts and the full threat-model visual-summary chain.
	- Updated iteration support records in `design/tasks/taskandissues_for_LLM.md` and `implementation/taskhelpinfos/*.md` with resolver notes and manual acceptance steps for the verified 1277 and 1436 tasks.
- Drift/Unrelated:
	- `AI4X-Platform-dify.feap` changed during the iteration but is not clearly tied to the workflow/task fixes.
	- `design/userstories/value_stream_aligned/VS3-E2E_动态知识进化闭环_端到端用户故事.md` appears modified in the workspace without a corresponding content diff in the captured patch set.

Files Changed

- Feature:
	- `DifyAgentWorkflow/ai4sec_opencti_webhook_workflow.yaml`
	- `DifyAgentWorkflow/ai4sec_threat_modeling_workflow.yaml`
	- `design/originaldata/2026-03-18t14_39_30.193z_tlp_all_(exportfilestix2)_report-vpd design_full.json`
- Fix/Refactor:
	- `external_opencti/opencti_webhook_signal_template.ejs`
	- `tests/e2e/test_delivery_assets.py`
- Supporting Sync:
	- `design/tasks/taskandissues_for_LLM.md`
	- `implementation/taskhelpinfos/2026-3-18_add_a_new_llm_node_responsible_for_summarize_the_current_structure_outpu_into_a_graph_and_several_tables.md`
	- `implementation/taskhelpinfos/2026-3-18_i_need_that_the_webhook_agent_analyzes_the_infrastrctures_related_with_the_notified_vulurability_pushed_from_opencti_to_give_out_the_the_impact_on_our_product_and_the_risk_score.md`
	- `implementation/taskhelpinfos/2026-3-18_i_need_webhook_agent_access_the_opencti_platform_with_a_http_node_in_the_workflow_instead_of_the_current_seperate_opencti_mcp.md`
- Drift/Unrelated:
	- `AI4X-Platform-dify.feap`
	- `design/userstories/value_stream_aligned/VS3-E2E_动态知识进化闭环_端到端用户故事.md`

Risk Notes

- Live Dify verification is still the main uncertainty: the webhook path previously showed an empty bearer token, so runtime env injection should be confirmed after import.
- The threat-model visual summary now sends a larger derived topology payload; the remaining risk is plugin/runtime behavior in Dify rather than local YAML correctness.
- The binary `.feap` change and the user-story file should be reviewed before commit to avoid mixing unrelated drift into the iteration summary.

Suggested Follow-ups

- Re-run one live Dify webhook execution to confirm the GraphQL node now sends a non-empty bearer token and a valid vulnerability STIX id.
- Re-run one live VS1 threat-model execution in Dify to confirm Mermaid rendering and plugin stability with the derived topology payload.
