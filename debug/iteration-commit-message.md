feat: complete business validation assets and harden MCP flow

- Feature:
  - add full business-layer manual validation pack under tests/validation, including capability summary, acceptance template, environment setup, and ten capability-specific validation guides
  - add four STIX 2.1 validation bundles for VS1-VS4 under tests/validation/test-data to support OpenCTI import and end-to-end manual acceptance
  - enrich validation guidance and task support docs, including completion checkboxes in implementation/taskhelpinfos/2026-3-14_请添加业务层的测试用例集.md
- Fix:
  - fix Dify workflow compatibility and VS1 routing in DifyAgentWorkflow/ai4sec_unified_workflow.yaml, including current-case structure updates and BL-03-01 keyword coverage for 建模结果/威胁结论/发布建议
  - fix local MCP package resolution by adding package markers under mcp/, mcp/opencti_mcp/, and mcp/notification_mcp/
  - harden OpenCTI MCP error handling in mcp/opencti_mcp/app/main.py, mcp/opencti_mcp/app/service.py, and mcp/opencti_mcp/app/settings.py with structured upstream error mapping, alias-to-real-ID resolution, schema-compatible GraphQL fields, and trust_env=False behavior
  - improve notification/opencti regression coverage in tests/unit/test_opencti_projection.py, tests/unit/test_notification_service.py, tests/contract/test_opencti_api_contract.py, and tests/integration/test_webhook_to_notification_flow.py
- Refactor:
  - normalize MCP settings and service structure across notification and opencti apps to align runtime configuration loading and contract error behavior
  - update design/tasks/taskandissues_for_LLM.md with resolver notes and verification state for the BusinessLayer 1208 work item
- Build/Release:
  - update .env.example and README.md to reflect current local runtime and iteration-delivery expectations
  - ignore Python cache artifacts in .gitignore and remove tracked __pycache__ bytecode from version control
- Drift/Unrelated:
  - AI4X-Platform-dify.feap changed during the iteration but is not directly evidenced as part of the business validation or MCP fixes

- Files Changed:
  - Workflow and routing: DifyAgentWorkflow/ai4sec_unified_workflow.yaml
  - MCP runtime: mcp/opencti_mcp/app/main.py, mcp/opencti_mcp/app/service.py, mcp/opencti_mcp/app/settings.py, mcp/notification_mcp/app/service.py, mcp/notification_mcp/app/settings.py, mcp/**/__init__.py
  - Tests: tests/unit/test_opencti_projection.py, tests/unit/test_notification_service.py, tests/contract/test_opencti_api_contract.py, tests/integration/test_webhook_to_notification_flow.py
  - Validation assets: tests/validation/README.md, tests/validation/00-*.md, tests/validation/01-10*.md, tests/validation/test-data/*.json
  - Planning and tracking: design/tasks/taskandissues_for_LLM.md, implementation/taskhelpinfos/2026-3-14_请添加业务层的测试用例集.md
  - Repo hygiene: .gitignore

- Risk Notes:
  - BL-03-01 routing fix is statically validated in workflow YAML but still depends on re-import and live verification in the local Dify UI
  - OpenCTI integration behavior depends on the local OpenCTI/Elasticsearch runtime being healthy when queries are executed
  - the FEAP binary diff should be reviewed before commit to confirm it is intentional and not tooling drift

- Suggested Follow-ups:
  - re-import the Dify workflow and execute the BL-03-01 sample request once in the UI to confirm live routing behavior
  - review whether AI4X-Platform-dify.feap should be included in this iteration commit or split out as a separate change
