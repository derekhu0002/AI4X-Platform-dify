feat(vs1): inline OpenCTI threat-model workflow and exact lookup

Commit Body

- Feature:
	- Replaced the VS1 external FastAPI MCP dependency with direct OpenCTI GraphQL access inside `DifyAgentWorkflow/ai4sec_threat_modeling_workflow.yaml`, including report resolution, live bundle fetch, STIX filtering, LLM invocation, and downloadable JSON output.
	- Added workflow-level exact report resolution by `report id` or exact `name`, with local test-bundle alias compatibility for imported report IDs.
	- Added task support artifacts and task-list sync for the two active `ai4sec_opencti_mcp` implementation items under `implementation/taskhelpinfos/` and `implementation/task-list.md`.
- Fix:
	- Fixed live OpenCTI schema compatibility in the workflow GraphQL query for `AttackPattern.killChainPhases` and `Organization.sectors`, and flattened connection data back into the expected STIX-like payload.
	- Removed duplicated OpenCTI bundle copies from the LLM prompt payload by shrinking `analysis_input` to report metadata, components, and assets only.
	- Repaired serialized Dify workflow Python code after YAML escape boundary regressions introduced during inline-node edits.
- Refactor:
	- Refactored `mcp/opencti_mcp/app/service.py` from list-all-plus-fuzzy report matching to exact-only live lookup via `_query_live_report_by_id` and `_query_live_report_by_exact_name`.
	- Simplified `mcp/opencti_mcp/app/models.py` threat-model match strategy contract to exact-id/exact-name only and aligned workflow/runtime behavior with the same rule set.
- Build/Release:
	- Expanded `tests/unit/test_opencti_projection.py` to cover exact-name behavior, exact-id precedence, alias compatibility, and compact `analysis_input` regression expectations.
	- Revalidated the iteration with `d:/projects/AI4X/AI4X-Platform-dify/.venv/Scripts/python.exe -m pytest tests/unit/test_opencti_projection.py tests/contract/test_opencti_api_contract.py` and additional YAML parse checks for the workflow node.
- Drift/Unrelated:
	- `AI4X-Platform-dify.feap` and current edits in `design/KG/SystemArchitecture.json` are present in the iteration scope but are not clearly required to implement the two verified `ai4sec_opencti_mcp` tasks.

Files Changed

- Feature:
	- `DifyAgentWorkflow/ai4sec_threat_modeling_workflow.yaml`
	- `implementation/task-list.md`
	- `implementation/taskhelpinfos/index.md`
	- `implementation/taskhelpinfos/2026-3-17_将该MCP功模块替换成该工作流中的节点_所有功能通过节点来实现_不再使用该外部FASTAPI服务.md`
	- `implementation/taskhelpinfos/2026-3-17_在查询和匹配OPENCTI中的report时_我希望你不要把所有report都查询回来_而是用手中的report_id作为参数去查.md`
- Fix/Refactor:
	- `mcp/opencti_mcp/app/models.py`
	- `mcp/opencti_mcp/app/service.py`
	- `tests/unit/test_opencti_projection.py`
- Supporting Sync:
	- `design/tasks/taskandissues_for_LLM.md`
- Drift/Unrelated:
	- `AI4X-Platform-dify.feap`
	- `design/KG/SystemArchitecture.json`

Risk Notes

- The Dify workflow still depends on live OpenCTI schema details; further runtime-only field mismatches may surface if additional object types are queried beyond the current VS1 scope.
- Final end-to-end confidence still requires a human Dify UI run after the last serialized-code fixes, because not every workflow-node execution path is reproducible from the local terminal.
- `AI4X-Platform-dify.feap` and `design/KG/SystemArchitecture.json` should be reviewed before commit to confirm they are intentional iteration content rather than drift.

Suggested Follow-ups

- Run one final end-to-end execution of `DifyAgentWorkflow/ai4sec_threat_modeling_workflow.yaml` inside Dify with a live report ID and confirm the answer node returns the compact non-duplicated prompt path.
- Review whether `AI4X-Platform-dify.feap` and `design/KG/SystemArchitecture.json` should remain in this iteration commit or be split into a separate change.
