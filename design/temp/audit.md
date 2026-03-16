### [TRACEABILITY - UPDATE]
*   **Element Name:** `DIFY`
*   **Code Paths:** `["externalDify/docker-compose.yaml"]`
*   **Reason:** `Current element metadata references externalDify/.env, but that file is not versioned in the repository. The actual traceable implementation artifact in-repo is the Docker Compose stack.`

*   **Element Name:** `ai4sec_agent`
*   **Code Paths:** `["DifyAgentWorkflow/ai4sec_unified_workflow.yaml", "DifyAgentWorkflow/tools/ai4sec_runtime_tools.py"]`
*   **Reason:** `Current code_paths points only to the folder and does not precisely recover the workflow asset and the helper runtime code that together implement the element.`

*   **Element Name:** `ai4sec_opencti_mcp`
*   **Code Paths:** `["mcp/opencti_mcp/app/main.py", "mcp/opencti_mcp/app/service.py", "mcp/opencti_mcp/app/settings.py", "mcp/opencti_mcp/app/models.py"]`
*   **Reason:** `Current code_paths points only to the package folder and does not precisely recover the FastAPI interface, service logic, settings, and request/response contract models.`

*   **Element Name:** `OpenCTI platform`
*   **Code Paths:** `["external_opencti/docker-compose.yml", "external_opencti/opencti_webhook_signal_template.ejs"]`
*   **Reason:** `Current element metadata references external_opencti/.env, but that file is not versioned in the repository. The actual traceable implementation artifacts are the Compose stack and the webhook signal template.`

*   **Element Name:** `Notification MCP`
*   **Code Paths:** `["mcp/notification_mcp/app/main.py", "mcp/notification_mcp/app/service.py", "mcp/notification_mcp/app/settings.py", "mcp/notification_mcp/app/models.py"]`
*   **Reason:** `Current code_paths points only to the package folder and does not precisely recover the HTTP interface, dispatch logic, settings, and payload contract.`

### [TRACEABILITY - ALIGNED (OMITTED)]
*   **Rule:** Do not list aligned elements one-by-one.
*   **Summary:** `0 implemented application/runtime elements were fully aligned without metadata correction; every implemented runtime element above needs traceability or element metadata updates.`

### [ELEMENT - ADD]
*   **Name:** `Dify Runtime Stack`
*   **Type:** `TechnologyNode`
*   **Parent View:** `TechnologyLayer`
*   **Description:** `Containerized Dify runtime stack defined by the repository and used to host the AI4SEC workflow application.`
*   **Attributes:** `code_paths = ["externalDify/docker-compose.yaml"]`

*   **Name:** `OpenCTI Runtime Stack`
*   **Type:** `TechnologyNode`
*   **Parent View:** `TechnologyLayer`
*   **Description:** `Containerized OpenCTI runtime stack with Elasticsearch, Redis, MinIO, RabbitMQ, workers, and connectors defined by the repository.`
*   **Attributes:** `code_paths = ["external_opencti/docker-compose.yml"]`

### [ELEMENT - MODIFY]
*   **Name:** `DIFY`
*   **Change Summary:** `The current element metadata points to a non-versioned .env file and does not describe the as-built repository boundary correctly.`
*   **TOBE Name:** `DIFY`
*   **TOBE Description:** `Containerized Dify platform runtime defined by the repository Compose stack and used to host the AI4SEC advanced-chat workflow asset. Runtime secrets are supplied outside version control, while the versioned implementation artifact in this repository is the Docker Compose stack.`
*   **TOBE Attributes:**
    *   `code_paths = ["externalDify/docker-compose.yaml"]`
    *   `.env = "N/A - runtime environment secrets for the Dify stack are not versioned in this repository."`
*   **TOBE Browser Path:** `N/A`

*   **Name:** `ai4sec_agent`
*   **Change Summary:** `The current description overstates the implemented orchestration depth. The as-built workflow performs VS1-VS4 routing and MCP query-driven first-screen summaries, while notification dispatch and bundle writeback are not wired into the Dify YAML.`
*   **TOBE Name:** `ai4sec_agent`
*   **TOBE Description:** `AI4SEC Dify advanced-chat workflow asset that routes user input across VS1-VS4 and calls ai4sec_opencti_mcp for scenario-specific context retrieval. The repository also contains helper runtime code for signal resolution, routing, and notification payload building, but the current workflow YAML does not yet orchestrate live notification dispatch or OpenCTI bundle writeback nodes.`
*   **TOBE Attributes:**
    *   `code_paths = ["DifyAgentWorkflow/ai4sec_unified_workflow.yaml", "DifyAgentWorkflow/tools/ai4sec_runtime_tools.py"]`
*   **TOBE Browser Path:** `N/A`

*   **Name:** `ai4sec_opencti_mcp`
*   **Change Summary:** `The current description is too idealized relative to the as-built service behavior. The service currently performs alias resolution, minimal GraphQL lookup, local scenario enrichment, bundle acceptance, and webhook passthrough; it does not yet implement full live STIX field projection or actual bundle persistence to OpenCTI.`
*   **TOBE Name:** `ai4sec_opencti_mcp`
*   **TOBE Description:** `FastAPI service that loads configuration from the repository root environment, resolves stable VS1-VS4 aliases to live OpenCTI object identifiers, queries a minimal OpenCTI GraphQL object envelope, enriches the response with local scenario context, accepts STIX bundle payloads, and exposes a passthrough webhook endpoint. In the current implementation, full live STIX projection and real OpenCTI bundle persistence remain partial.`
*   **TOBE Attributes:**
    *   `code_paths = ["mcp/opencti_mcp/app/main.py", "mcp/opencti_mcp/app/service.py", "mcp/opencti_mcp/app/settings.py", "mcp/opencti_mcp/app/models.py"]`
*   **TOBE Browser Path:** `N/A`

*   **Name:** `OpenCTI platform`
*   **Change Summary:** `The current element metadata references a non-versioned .env file and omits the repository-owned webhook signal template that participates in the integration contract.`
*   **TOBE Name:** `OpenCTI platform`
*   **TOBE Description:** `Local OpenCTI runtime stack defined by the repository Compose file and integrated with AI4SEC through GraphQL access, internal workers/connectors, and a repository-owned webhook signal template that emits lookup-required STIX bundle notifications for downstream processing.`
*   **TOBE Attributes:**
    *   `code_paths = ["external_opencti/docker-compose.yml", "external_opencti/opencti_webhook_signal_template.ejs"]`
    *   `evn = "N/A - local OpenCTI environment secrets are not versioned in this repository."`
*   **TOBE Browser Path:** `N/A`

*   **Name:** `Notification MCP`
*   **Change Summary:** `The current description hardcodes SMTP credentials and a recipient, while the as-built service is environment-driven and supports preview-mode dispatch behavior.`
*   **TOBE Name:** `Notification MCP`
*   **TOBE Description:** `FastAPI notification service that previews or dispatches standardized AI4SEC notifications through an environment-driven SMTP configuration. The current implementation computes escalation windows and deduplication keys, appends a default formal recipient, and performs real email dispatch only when preview mode is disabled.`
*   **TOBE Attributes:**
    *   `code_paths = ["mcp/notification_mcp/app/main.py", "mcp/notification_mcp/app/service.py", "mcp/notification_mcp/app/settings.py", "mcp/notification_mcp/app/models.py"]`
*   **TOBE Browser Path:** `N/A`

*   **Name:** `SKILL`
*   **Change Summary:** `The repository contains no Dify-wired business skill implementation that evidences this element in the current workflow asset.`
*   **TOBE Name:** `SKILL`
*   **TOBE Description:** `[PROPOSED] Future business skill capability for ai4sec_agent. The current repository does not yet contain a Dify-integrated runtime implementation that is invoked by the as-built workflow asset.`
*   **TOBE Attributes:**
    *   `code_paths = []`
*   **TOBE Browser Path:** `N/A`

*   **Name:** `外部信息爬取AGENT`
*   **Change Summary:** `No repository implementation currently evidences this external crawler as an as-built component.`
*   **TOBE Name:** `外部信息爬取AGENT`
*   **TOBE Description:** `[PROPOSED] Future external intelligence collection agent. No crawler implementation, connector runtime, or scheduled ingestion code is currently present in this repository.`
*   **TOBE Attributes:**
    *   `code_paths = []`
*   **TOBE Browser Path:** `N/A`

### [RELATIONSHIP - ADD]
*   **Source:** `OpenCTI platform`
*   **Target:** `ai4sec_opencti_mcp`
*   **Type:** `Triggering`
*   **Parent View:** `ApplicationLayer`
*   **Description:** `The as-built code exposes /webhooks/opencti/threat-intelligence inside ai4sec_opencti_mcp, so OpenCTI currently triggers this MCP endpoint directly in the implemented runtime.`

## Part 2: Business Gap Analysis
*   **Implemented Processes:** `Partial support exists for 情报任务受理与分流 through the Dify routing workflow, for 威胁与影响研判 through scenario-specific MCP projection responses, for 通知与决策协同 through Notification MCP preview/dispatch APIs, and for 证据链与知识资产沉淀 only as a bundle acceptance contract. The repository also provides a complete manual validation pack under tests/validation to audit these capability expectations from a business acceptance perspective.`
*   **Missing Capabilities:** `业务上下文归并 is not implemented as a live asset/business-context graph lookup flow and is instead synthesized from local alias-based context. 控制缺口与处置建议生成 has no executable reasoning or persistence path in the Dify workflow. 事件升级与动作编排 is represented only by first-screen answer text and no actual action orchestration. 监控与规则持续校准 has no runtime hit feedback ingestion or rule update loop. 角色责任治理 and 业务绩效度量 have zero implementation support in code. Across VS1-VS4, real OpenCTI bundle writeback is also missing because write_bundle returns accepted responses without performing persistence.`
*   **Suggestions:** `Implement real OpenCTI bundle persistence first, then wire /bundle and /dispatch nodes into the Dify workflow so VS1-VS4 can complete the designed loop. Replace alias-based synthetic business context with real OpenCTI relationship traversal for 业务上下文归并. Add explicit runtime services for action orchestration, hit feedback ingestion, and KPI/RACI evidence capture only after the writeback path is live.`

## Part 3: Documentation & README Synchronization
*   **Reviewed READMEs:**
    *   **File:** `README.md`
    *   **File:** `tests/validation/README.md`
*   **Discrepancies:** `README.md states that a GitHub Actions CI pipeline exists and points to .github/workflows/ci.yml, but no .github/workflows files are present in the repository. README.md also describes the unified workflow as if it can proceed into release decisions, response orchestration, and decision summaries, while the as-built Dify YAML currently only calls the MCP /query endpoint and renders answer nodes. README.md documents the OpenCTI webhook path but does not make clear that the implemented endpoint currently lives in ai4sec_opencti_mcp rather than inside the Dify asset boundary described by the architecture. tests/validation/README.md is materially aligned with the current validation asset set and execution boundary.`
*   **Recommended Updates (Not Applied):** `Update README.md to remove the non-existent CI claim or add the missing workflow files. Rewrite the workflow implementation section so it explicitly states that the current YAML provides routing plus MCP query-based first-screen responses only. Clarify that the present webhook ingress is implemented in ai4sec_opencti_mcp and identify this as either temporary drift or the new as-built boundary. Keep tests/validation/README.md unchanged except for future links if new validation guides are added.`

## Part 4: Strategy & Architecture Compliance Report
*   **Compliance:** `PARTIAL`
*   **Violations:** `Separation of Concerns is only partially respected because the OpenCTI webhook ingress is implemented inside ai4sec_opencti_mcp, while the as-designed ApplicationLayer places push-driven entry at ai4sec_agent. The STIX-first principle is only partially realized because live query behavior currently retrieves a minimal GraphQL object and then synthesizes business context locally rather than projecting real STIX relationships from OpenCTI. The strategic goal of a full closed loop is only partially implemented because the Dify workflow does not execute live writeback or notification dispatch nodes, and the bundle write API does not persist to OpenCTI.`
*   **Recommendations:** `Either move webhook ingress back to the ai4sec_agent boundary or update the architecture to reflect MCP-owned ingress explicitly. Implement real OpenCTI object projection and bundle persistence so the STIX-first principle is true in runtime rather than only in documentation. Extend the Dify workflow from routing-only behavior to complete the designed accept-query-reason-writeback-notify-feedback loop before claiming end-to-end value-stream realization.`

## Part 5: KG Reorganization Plan (Progressive Disclosure + SoC)

### [REORGANIZATION - PRINCIPLES CHECK]
*   **Progressive Disclosure:** `PARTIAL - Business subviews already exist, but StrategyLayerAndMotivationAspect is overloaded, ApplicationLayer mixes users, runtime components, and future ingestion concerns, and TechnologyLayer has no concrete runtime elements despite the repository containing deployment assets.`
*   **Separation of Concerns:** `PARTIAL - Workflow orchestration, OpenCTI projection, webhook ingress, notification dispatch, and future external crawling concerns are not cleanly separated in the current view structure.`
*   **Hotspots:** `StrategyLayerAndMotivationAspect`, `ApplicationLayer`, `TechnologyLayer`

### [VIEW - ADD]
*   **View Name:** `Application Runtime Flow`
*   **Target Browser Path:** `Model/System/ApplicationLayer/ApplicationLayer/Application Runtime Flow`
*   **Purpose:** `Show the implemented runtime request/response path between the Dify workflow, MCP services, OpenCTI, and notification boundary.`
*   **Description:** `Stakeholders: solution architect, application maintainer, tester. Concerns: runtime orchestration ownership, MCP boundaries, webhook drift, notification boundary. Purpose: explain the as-built runtime interaction path separately from high-level application context. Scope: DIFY, ai4sec_agent, ai4sec_opencti_mcp, OpenCTI platform, Notification MCP and their direct runtime relationships.`
*   **Included Elements:** `["1212", "1214", "1215", "1216", "1227"]`
*   **Included Relationships:** `["1079", "1082", "1083", "1086", "1089"]`
*   **Reason:** `This removes runtime interaction detail from the broader application context view and makes the current ingress/output drift visible.`

*   **View Name:** `External Intelligence Ingestion`
*   **Target Browser Path:** `Model/System/ApplicationLayer/ApplicationLayer/External Intelligence Ingestion`
*   **Purpose:** `Isolate future-state external crawling and OpenCTI ingestion concerns from the implemented runtime path.`
*   **Description:** `Stakeholders: architect, roadmap owner. Concerns: future crawler scope, external source ownership, ingestion boundary. Purpose: separate proposed external collection capability from the currently implemented MCP and workflow runtime. Scope: 外部信息爬取AGENT, 外部网站, OpenCTI platform, ai4sec_agent and their ingestion relationships.`
*   **Included Elements:** `["1217", "1218", "1216", "1214"]`
*   **Included Relationships:** `["1084", "1085", "1086"]`
*   **Reason:** `This keeps future ingestion capability visible without polluting the core runtime flow view.`

### [VIEW - MODIFY]
*   **View Name:** `ApplicationLayer`
*   **Current Browser Path:** `Model/System/ApplicationLayer/ApplicationLayer/ApplicationLayer`
*   **Target Browser Path:** `Model/System/ApplicationLayer/ApplicationLayer/Application Context Overview`
*   **Change:** `Narrow Scope`
*   **Before Scope:** `Users, runtime services, external crawler concepts, and transport relationships are all mixed in one overview.`
*   **After Scope:** `Top-level application context only: user-facing entry, core runtime components, and external boundaries at a high level.`
*   **Description Update:** `Stakeholders: architect, product owner, reviewer. Concerns: system context, top-level application ownership, actor-to-system interaction. Purpose: provide a high-level overview before drilling down into runtime flow and future ingestion views. Scope: only top-level application elements and the minimum relationships needed to understand the platform boundary.`

*   **View Name:** `TechnologyLayer`
*   **Current Browser Path:** `Model/System/TechnologyLayer/TechnologyLayer/TechnologyLayer`
*   **Target Browser Path:** `Model/System/TechnologyLayer/TechnologyLayer/Technology Runtime Overview`
*   **Change:** `Narrow Scope`
*   **Before Scope:** `An empty view backed only by narrative documentation.`
*   **After Scope:** `Concrete deployment/runtime overview anchored on repository-owned runtime stack elements and container boundaries.`
*   **Description Update:** `Stakeholders: platform engineer, maintainer, tester. Concerns: local runtime topology, containerized boundaries, dependency stacks, deployment ownership. Purpose: show the actual repository-defined runtime environment separately from application behavior. Scope: Dify Runtime Stack, OpenCTI Runtime Stack, local MCP runtime boundaries, and their hosting/dependency context.`

### [VIEW - SPLIT]
*   **Source View:** `StrategyLayerAndMotivationAspect`
*   **Source Browser Path:** `Model/System/StrategyLayerAndMotivationAspect/StrategyLayerAndMotivationAspect/StrategyLayerAndMotivationAspect`
*   **New Views:** `["Strategic Goals and Principles", "Value Stream Capability Realization"]`
*   **Target Browser Paths:** `["Model/System/StrategyLayerAndMotivationAspect/StrategyLayerAndMotivationAspect/Strategic Goals and Principles", "Model/System/StrategyLayerAndMotivationAspect/StrategyLayerAndMotivationAspect/Value Stream Capability Realization"]`
*   **Split Logic:** `Separate stable strategy objects, principles, outcomes, and courses of action from the denser value-stream-to-capability realization network.`
*   **Description Requirement:** `For each new View, include Stakeholders / Concerns / Purpose / Scope in its description`

### [VIEW - MERGE]
*   **Source Views:** `[]`
*   **Source Browser Paths:** `[]`
*   **Target View:** `N/A`
*   **Target Browser Path:** `N/A`
*   **Merge Logic:** `No clear redundant views were found. The current problem is under-separation, not duplication.`
*   **Description Requirement:** `N/A`

### [ELEMENT - MOVE]
*   **Element:** `决策与通知协同服务`
*   **Current Browser Path:** `Model/System/BusinessLayer/BusinessLayer/决策与通知协同服务`
*   **Target Browser Path:** `Model/System/StrategyLayerAndMotivationAspect/StrategyLayerAndMotivationAspect/响应协同与处置编排/决策与通知协同服务`
*   **Reason:** `Ownership is clearer when the service is placed with the capability concern it operationalizes rather than floating at the BusinessLayer root.`

### [RELATIONSHIP - MOVE]
*   **Relationship:** `ai4sec_agent --(access opencti stix data)--> ai4sec_opencti_mcp`
*   **From View:** `ApplicationLayer`
*   **To View:** `Application Runtime Flow`
*   **Reason:** `This is runtime interaction detail and should live in the runtime flow drill-down view rather than the top-level context view.`

*   **Relationship:** `ai4sec_opencti_mcp --(access情报数据)--> OpenCTI platform`
*   **From View:** `ApplicationLayer`
*   **To View:** `Application Runtime Flow`
*   **Reason:** `This is runtime data-access detail and contributes to clutter in the high-level application context view.`

*   **Relationship:** `OpenCTI platform --(主动推送STIX BUNDLE情报信息)--> ai4sec_agent`
*   **From View:** `ApplicationLayer`
*   **To View:** `Application Runtime Flow`
*   **Reason:** `This relationship needs a dedicated drill-down view because the implemented ingress boundary is currently under review and should be examined separately.`

*   **Relationship:** `ai4sec_agent --(发送预警通知)--> Notification MCP`
*   **From View:** `ApplicationLayer`
*   **To View:** `Application Runtime Flow`
*   **Reason:** `This relationship belongs with the runtime orchestration path, where its current implementation gap can be assessed alongside the rest of the value-stream loop.`