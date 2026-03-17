feat(ai4sec): deliver webhook ingress and OpenCTI real-data loop

Feature:
- add dedicated OpenCTI webhook workflow asset in DifyAgentWorkflow/ai4sec_opencti_webhook_workflow.yaml for signal normalization, query, and response chaining
- introduce agent-side webhook ingress service under mcp/ai4sec_agent/app/main.py and mcp/ai4sec_agent/app/models.py
- add closed-loop runtime helpers in DifyAgentWorkflow/tools/ai4sec_runtime_tools.py and corresponding unit coverage in tests/unit/test_runtime_tools_closed_loop.py
- add STIX minimal field matrix config in config/stix_minimal_field_matrix.json and operator switch guide in external_opencti/opencti_webhook_agent_switch_guide.md

Fix:
- replace hardcoded mock object ids in DifyAgentWorkflow/ai4sec_unified_workflow.yaml with start-input variables for VS1/VS2/VS3/VS4 query nodes
- fix Dify expression resolution by normalizing start node references (start_node) in DifyAgentWorkflow/ai4sec_unified_workflow.yaml and aligning tests/e2e/test_delivery_assets.py
- harden OpenCTI MCP query/write behavior in mcp/opencti_mcp/app/service.py, mcp/opencti_mcp/app/main.py, and mcp/opencti_mcp/app/settings.py (schema compatibility, write-capability probing, error mapping)
- expand regression and contract checks in tests/unit/test_opencti_projection.py and tests/contract/test_agent_webhook_contract.py

Refactor:
- update architecture and task traceability artifacts in design/KG/SystemArchitecture.json and design/tasks/taskandissues_for_LLM.md with iteration resolver context
- reorganize implementation tracking docs in implementation/task-list.md and implementation/taskhelpinfos/index.md

Build/Release:
- update environment/runtime delivery metadata in externalDify/.env and AI4X-Platform-dify.feap

Drift/Unrelated:
- add temporary/debug artifacts debug/_tmp.txt and debug/ggg.yml
- add screenshot artifacts Pasted image 20260317001921.png, Pasted image 20260317002010.png, and Pasted image 20260317002018.png

Files Changed:
- Workflow: DifyAgentWorkflow/ai4sec_unified_workflow.yaml, DifyAgentWorkflow/ai4sec_opencti_webhook_workflow.yaml
- MCP services: mcp/ai4sec_agent/app/main.py, mcp/ai4sec_agent/app/models.py, mcp/opencti_mcp/app/main.py, mcp/opencti_mcp/app/service.py, mcp/opencti_mcp/app/settings.py
- Tests: tests/e2e/test_delivery_assets.py, tests/unit/test_opencti_projection.py, tests/unit/test_runtime_tools_closed_loop.py, tests/contract/test_agent_webhook_contract.py
- Config and docs: config/stix_minimal_field_matrix.json, design/tasks/taskandissues_for_LLM.md, design/KG/SystemArchitecture.json, external_opencti/opencti_webhook_agent_switch_guide.md, implementation/taskhelpinfos/*.md
- Potential drift artifacts: debug/_tmp.txt, debug/ggg.yml, Pasted image 20260317001921.png, Pasted image 20260317002010.png, Pasted image 20260317002018.png, AI4X-Platform-dify.feap

Risk Notes:
- live Dify runtime still depends on valid opencti_object_id/object_type inputs for unified workflow query calls
- OpenCTI write/query paths may vary by deployed schema capabilities and eventual consistency windows
- drift artifacts and binary/project files may add commit noise unless intentionally included

Suggested Follow-ups:
- verify one live OpenCTI webhook trigger against DifyAgentWorkflow/ai4sec_opencti_webhook_workflow.yaml and confirm concrete object_id/object_type in query payload
- verify one VS4 unified workflow run with known valid OpenCTI object id after import/publish
- decide whether debug artifacts and pasted screenshots should be excluded from the release commit
