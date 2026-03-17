feat(vs1): implement threat-modeling workflow loop and fix dsl runtime bugs

- Feature: Implemented live OpenCTI GraphQL fetching for `/query/threat-model-report` to resolve bundle objects directly from database rather than relying on mocks.
- Feature: Added local source-report-id-to-name alias fallback in `service.py` to transparently resolve imported mock IDs against standard OpenCTI live reports.
- Feature: Added standalone `ai4sec_threat_modeling_workflow.yaml` covering the full VS1 workflow path with real LLM invocation, schema formatting, and session data downloading.
- Fix: Replaced hyphens (`-`) with underscores (`_`) across Dify Node IDs (`resolve_report_ref`, etc.) to mitigate a Dify string interpolation bug causing raw variable payloads to trigger 404s.
- Fix: Added robust Markdown block fence stripping logic inside Python node before `json.loads` to prevent `JSONDecodeError` during LLM output transformations.
- Build/Release: Expanded `test_opencti_projection.py` and `test_opencti_api_contract.py` for exact/fuzzy matches, bundle filtering, and local ID alias resolutions.
- Build/Release: Registered derived VS1 user stories and step-by-step acceptance criteria into architecture docs.

### Files Changed
- `DifyAgentWorkflow/ai4sec_threat_modeling_workflow.yaml`: Workflow orchestration and Python data extraction fixes.
- `mcp/opencti_mcp/app/main.py`, `models.py`, `service.py`: OpenCTI live fetching, GraphQL traversal, ID matching logic.
- `tests/unit/test_opencti_projection.py`, `tests/contract/test_opencti_api_contract.py`: Assertion suites.
- `design/userstories/`, `design/tasks/`, `implementation/taskhelpinfos/`: Scope tracking and user story mappings.

### Risk Notes
- The Dify DSL engine is extremely sensitive to YAML syntax mapping and Node ID naming (forbidden characters like hyphens). Any future workflows must rigidly adhere to snake_case naming for variables.
- Direct JSON parsing of LLM outputs remains inherently volatile; fallback logic assumes standard ` ```json ` markers, which might occasionally drift if the LLM output shifts radically.

### Suggested Follow-ups
- Validate the new Threat Modeling Workflow locally in the browser by triggering an end-to-end trace with a real OpenCTI report.
- Extend markdown fence sanitation to other potential LLM format outputs (e.g. nested markdown blocks) if future crashes occur.
