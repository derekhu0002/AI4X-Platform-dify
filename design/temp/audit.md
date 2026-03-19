# Architecture Audit & Change Report

> **Audit Date:** 2026-03-18  
> **KG Source:** `design/KG/SystemArchitecture.json`  
> **Auditor Role:** Expert Software Architect and ArchiMate Modeler  
> **Iteration Scope:** New WEBHOOK_AGENT workflow, standalone VS1 threat-modeling direct GraphQL path, risk scoring gap analysis.

---

## Part 1: The Architecture Change Report

### [TRACEABILITY - UPDATE]

*   **Element Name:** `1275 / Dify Runtime Stack`
*   **Code Paths:** `["externalDify/docker-compose.yaml", "DifyAgentWorkflow/ai4sec_unified_workflow.yaml", "DifyAgentWorkflow/ai4sec_threat_modeling_workflow.yaml", "DifyAgentWorkflow/ai4sec_opencti_webhook_workflow.yaml"]`
*   **Reason:** `The current code_paths omits DifyAgentWorkflow/ai4sec_opencti_webhook_workflow.yaml. WEBHOOK_AGENT (1277) executes on this same Dify Runtime Stack, so all three workflow DSL assets must be traceable to the node element.`

*   **Element Name:** `1277 / WEBHOOK_AGENT`
*   **Code Paths:** `["DifyAgentWorkflow/ai4sec_opencti_webhook_workflow.yaml"]`
*   **Reason:** `The current code_paths incorrectly includes DifyAgentWorkflow/tools/ai4sec_runtime_tools.py. The as-built webhook workflow (ai4sec_opencti_webhook_workflow.yaml) uses only inline code nodes and an HTTP request node pointing directly at OPENCTI_GRAPHQL_URL; it does not import or invoke ai4sec_runtime_tools at runtime. ai4sec_runtime_tools.py is correctly associated with element 1214 (ai4sec_agent) and should be removed from 1277 code_paths.`

---

### [TRACEABILITY - ALIGNED (OMITTED)]

*   **Rule:** Do not list aligned elements one-by-one.
*   **Summary:** `7 application and technology elements verified as already aligned and omitted from [TRACEABILITY - UPDATE]: 1214 (ai4sec_agent), 1215 (ai4sec_opencti_mcp), 1227 (Notification MCP), 1276 (OpenCTI Runtime Stack), 1436 (ai4sec_threat_modeling_agent), 1437 (unnamed execution object, code_paths aligned), and all non-implementable strategy/business/motivation elements (goals, principles, roles, capabilities, services, processes, objects, outcomes).`

---

### [ELEMENT - ADD]

*   **Name:** `N/A`
*   **Type:** `N/A`
*   **Parent View:** `N/A`
*   **Description:** `No orphaned code file was found without a corresponding KG element. All major workflow assets, MCP services, runtime stacks, and tool modules are already represented in the KG.`
*   **Attributes:** `N/A`

---

### [ELEMENT - MODIFY]

*   **Name:** `1437 / (unnamed Object in 威胁建模闭环流程)`
*   **Change Summary:** `Element has an empty name field which breaks view readability and lookup in 威胁建模闭环流程001 (view 181). The description also mixes execution steps in imperative prose that should be replaced with a contract-style declarative description aligned with the as-built VS1 direct GraphQL execution path.`
*   **TOBE Name:** `VS1威胁建模分析执行对象`
*   **TOBE Description:** `Business-layer execution artifact that represents the VS1 threat-modeling analysis contract as realized by the standalone Dify workflow (ai4sec_threat_modeling_workflow.yaml). The workflow accepts a report name or report ID as input, resolves the effective reference through a code node, constructs a GraphQL query targeting OPENCTI_GRAPHQL_URL directly (no MCP), filters the returned STIX 2.1 object set to retain only threat-analysis-relevant fields, invokes an LLM node for structured threat-model JSON generation, and returns the result with an in-session download link.`
*   **TOBE Attributes:**
    *   `code_paths = ["DifyAgentWorkflow/ai4sec_threat_modeling_workflow.yaml"]`
*   **TOBE Browser Path:** `Model/System/BusinessLayer/BusinessLayer/威胁建模闭环流程/VS1威胁建模分析执行对象`

---

*   **Name:** `1215 / ai4sec_opencti_mcp`
*   **Change Summary:** `The current description states that the standalone VS1 threat-modeling workflow no longer calls this service at runtime, but does not yet acknowledge that WEBHOOK_AGENT (1277) also bypasses this service. As-built, the WEBHOOK_AGENT uses an HTTP node pointing directly at OPENCTI_GRAPHQL_URL (port 8080), not at this MCP (port 8101). The description must be updated so that the scope of remaining callers is accurate: only ai4sec_agent (1214, unified general workflow) still uses this service at runtime.`
*   **TOBE Name:** `N/A`
*   **TOBE Description:** `Repository-local OpenCTI MCP compatibility service (FastAPI, default port 8101) that loads configuration from the repository root environment. Provides five STIX projection profiles (/query: minimal, summary, analysis, graph, notification), exact-priority threat-model report resolution (/query/threat-model-report), STIX bundle writeback with dry-run support (/bundle), and a health check endpoint (/health). After this iteration, both the standalone VS1 threat-modeling workflow (ai4sec_threat_modeling_agent, 1436) and the WEBHOOK_AGENT (1277) access OpenCTI GraphQL directly at OPENCTI_GRAPHQL_URL and no longer depend on this service at runtime. Only ai4sec_agent (1214, unified general workflow) continues to call this service through OPENCTI_MCP_URL (host.docker.internal:8101).`
*   **TOBE Attributes:**
    *   `code_paths = ["mcp/opencti_mcp/app/main.py", "mcp/opencti_mcp/app/service.py", "mcp/opencti_mcp/app/settings.py", "mcp/opencti_mcp/app/models.py"]`
*   **TOBE Browser Path:** `N/A`

---

*   **Name:** `1277 / WEBHOOK_AGENT`
*   **Change Summary:** `The current description states the element reuses shared runtime tool logic for signal resolution, scenario routing, and downstream notification preparation. This is inaccurate for the as-built implementation: the webhook workflow uses only inline code nodes and an HTTP request node; it does not call ai4sec_runtime_tools.py at runtime, does not route to Notification MCP, and its active ToDo task specifying direct GraphQL access has already been implemented. The description must reflect the as-built behavior.`
*   **TOBE Name:** `N/A`
*   **TOBE Description:** `Webhook-oriented Dify workflow asset that receives OpenCTI-originated STIX bundle push events, normalizes the incoming payload through an inline code node, queries related infrastructure and vulnerability context directly from OpenCTI GraphQL (OPENCTI_GRAPHQL_URL, port 8080) via an HTTP request node, analyzes one-hop asset relationships, computes a contextualized AI4SEC Risk Score (CVSS base x asset criticality x exposure x threat-intel multipliers, 1-100 range), maps the score to a severity_tier (Critical/High/Medium/Low), and returns a structured analysis output (severity_tier, risk_score, recommended_action, business_impact_summary) in-session. This workflow does not route through ai4sec_opencti_mcp and does not emit notifications via Notification MCP; per design specification, high-risk results are returned as structured inline output only.`
*   **TOBE Attributes:**
    *   `code_paths = ["DifyAgentWorkflow/ai4sec_opencti_webhook_workflow.yaml"]`
*   **TOBE Browser Path:** `N/A`

---

*   **Name:** `1217 / 外部信息爬取Connector`
*   **Change Summary:** `Element is modeled in the ApplicationLayer view without a [PROPOSED] marker, but no crawler, connector adapter, or external site ingestion runtime exists anywhere in the repository. It must be clearly marked as future scope.`
*   **TOBE Name:** `N/A`
*   **TOBE Description:** `[PROPOSED] Future external intelligence crawling connector intended to actively ingest public-site or third-party threat intelligence into OpenCTI. No implementation (crawler runtime, scheduler, or site-ingestion adapter) has been delivered in the current repository. Current external intelligence ingestion relies exclusively on OpenCTI-side connectors and webhook-driven delivery by external parties.`
*   **TOBE Attributes:**
    *   `code_paths = []`
*   **TOBE Browser Path:** `N/A`

---

### [RELATIONSHIP - ADD]

*   **Source:** `1277 / WEBHOOK_AGENT`
*   **Target:** `1276 / OpenCTI Runtime Stack`
*   **Type:** `ArchiMate_Access`
*   **Parent View:** `ApplicationLayer` (View ID 164, browser_path: Model/System/ApplicationLayer/ApplicationLayer/ApplicationLayer)
*   **Description:** `The as-built WEBHOOK_AGENT workflow queries OpenCTI directly via an HTTP request node using OPENCTI_GRAPHQL_URL (http://host.docker.internal:8080/graphql), bypassing ai4sec_opencti_mcp entirely. This direct access relationship mirrors the existing ai4sec_threat_modeling_agent to OpenCTI Runtime Stack relationship (1244) and must be explicitly modeled.`

---

### [RELATIONSHIP - DELETE]

*   **Relationship ID:** `1129`
*   **Statement:** `WEBHOOK_AGENT --(access opencti stix data)--> ai4sec_opencti_mcp (http://host.docker.internal:8101)`
*   **From View:** `ApplicationLayer` (View ID 164)
*   **Reason:** `This relationship is stale. The as-built webhook workflow (ai4sec_opencti_webhook_workflow.yaml) does not call ai4sec_opencti_mcp at runtime. It uses a direct HTTP request node targeting OPENCTI_GRAPHQL_URL at port 8080. The replacement is the new WEBHOOK_AGENT to OpenCTI Runtime Stack access relationship described in [RELATIONSHIP - ADD] above.`

---

## Part 2: Business Gap Analysis

*   **Implemented Processes:**
    *   **威胁建模闭环流程 (VS1 / 1260):** Fully implemented. `ai4sec_threat_modeling_agent` (1436) covers the complete loop: report reference input to OpenCTI GraphQL query to STIX 2.1 evidence filtering to LLM structured threat-model output to in-session JSON download. MCP compatibility service (1215) retains the `/query/threat-model-report` endpoint as a fallback for compatible clients.
    *   **Webhook Signal Processing (VS4 sub-path):** `WEBHOOK_AGENT` (1277) covers the inbound OpenCTI event path: receive webhook push, normalize bundle, query one-hop infrastructure relationships, compute AI4SEC Risk Score, return structured analysis output. This provides foundational infrastructure-impact analysis capability traceable to VS4 (environment-aware monitoring) business intent.
    *   **通用查询与编排 (unified entry):** `ai4sec_agent` (1214) provides VS1-VS4 routing through the unified workflow, MCP-mediated STIX context queries, and Notification MCP dispatch.

*   **Missing Capabilities:**
    *   **威胁运营与响应闭环 (VS2 / 1261):** Only a routing branch in the unified workflow. No dedicated incident response workflow, playbook orchestration, or cross-role coordination chain exists.
    *   **知识进化闭环流程 (VS3 / 1262):** View 200 contains only a single element (1438: 外部威胁事件情报提取) with no relationships and no implementation.
    *   **STIX Bundle Writeback in Workflow:** The `/bundle` endpoint exists in `ai4sec_opencti_mcp` but no workflow currently calls it in a closed-loop business scenario.
    *   **Risk Score to Notification Escalation:** High-risk WEBHOOK_AGENT results are returned inline but do not trigger Notification MCP dispatch. The business SLA table in element 1277 (Critical/High SLAs with team notification) has no corresponding workflow escalation path.
    *   **Graph and Table Summary Output for VS1:** The Mermaid relationship graph and per-entity Markdown tables specified in element 1436 active ToDo have not yet been added to the workflow.
    *   **外部信息爬取Connector (1217):** [PROPOSED] — no crawler, connector, or external site ingestion runtime implemented.

*   **Suggestions:**
    *   For VS2: Implement a dedicated `ai4sec_incident_response_agent` workflow that accepts an incident ID, pulls STIX Campaign/Threat-Actor context from OpenCTI, invokes LLM playbook generation, and writes back a CourseOfAction STIX object via the MCP `/bundle` endpoint.
    *   For VS3: Implement a knowledge-evolution workflow that triggers on VS1/VS2 completion, summarizes concluded analysis into STIX Note objects, and writes them back to OpenCTI to close the knowledge ingestion loop.
    *   For risk escalation: Add a conditional output branch to WEBHOOK_AGENT that triggers Notification MCP when severity_tier is Critical or High, aligned with the SLA table in element 1277 description.
    *   For the graph/table output gap in 1436: Add an LLM post-processing node that generates a Mermaid diagram from the filtered STIX bundle and Markdown tables per STIX entity type, placed after the main analysis LLM node.

---

## Part 3: Documentation & README Synchronization

*   **Reviewed READMEs:**
    *   **File:** `README.md`
    *   **File:** `tests/validation/README.md`

*   **Discrepancies:**

    1. **README Section 3.2 - standalone VS1 Threat Modeling workflow:** States "通过 HTTP 请求节点调用 OpenCTI MCP 的 /query/threat-model-report 接口，获取过滤后的 STIX 2.1 bundle 与分析输入". This is **incorrect**. The as-built `ai4sec_threat_modeling_workflow.yaml` uses an **inline code node** (Python `def main(report_ref, opencti_graphql_url, opencti_admin_token)`) that posts a GraphQL query directly to `OPENCTI_GRAPHQL_URL` (port 8080). It does **not** call the MCP `/query/threat-model-report` endpoint at runtime.

    2. **README Section 3.2 - OpenCTI MCP:** Claims the MCP exposes `/webhooks/opencti/threat-intelligence`. This endpoint is **not present** in `mcp/opencti_mcp/app/main.py`. The actual endpoints are `/health`, `/query`, `/query/threat-model-report`, and `/bundle`. The webhook ingest path is handled by the **WEBHOOK_AGENT** Dify workflow, not by the MCP service.

    3. **README Section 3.2 - Missing WEBHOOK_AGENT component:** `ai4sec_opencti_webhook_workflow.yaml` is **not documented at all** in any README section. This is a significant omission: it is a separately deployable Dify workflow asset with its own runtime path, environment variables (`OPENCTI_GRAPHQL_URL`, `OPENCTI_ADMIN_TOKEN`), node chain, and structured output contract.

    4. **README Section 4.1 - Step 3:** States `"ai4sec_agent 使用 MCP 查询完整 STIX 上下文"`. While accurate for the unified workflow (1214), this omits the two parallel runtime paths: `ai4sec_threat_modeling_agent` and `WEBHOOK_AGENT`, both of which bypass MCP and query OpenCTI GraphQL directly.

    5. **`tests/validation/README.md`:** Broadly aligned with the current test directory structure. No discrepancies identified.

*   **Recommended Updates (Not Applied):**

    1. In Section 3.2, replace the VS1 workflow implementation description with: direct OpenCTI GraphQL access via inline code node; `OPENCTI_GRAPHQL_URL` and `OPENCTI_ADMIN_TOKEN` env vars required at the Dify application level; no MCP dependency at runtime.
    2. In Section 3.2, add a new subsection **"OpenCTI Webhook 工作流 (WEBHOOK_AGENT)"** documenting `DifyAgentWorkflow/ai4sec_opencti_webhook_workflow.yaml`, its trigger path, direct GraphQL access pattern, risk-score output contract, and required env vars.
    3. In Section 3.2 "OpenCTI MCP", remove the `/webhooks/...` endpoint and add: `"Webhook ingest is handled by the dedicated WEBHOOK_AGENT Dify workflow, not by this MCP service."`
    4. In Section 4.1 Step 3, update to: `"ai4sec_agent (统一工作流) 通过 OpenCTI MCP 查询 STIX 上下文；ai4sec_threat_modeling_agent 和 WEBHOOK_AGENT 直接查询 OpenCTI GraphQL。"`
    5. In Section 4.3 "当前实现边界", add: `"WEBHOOK_AGENT 的风险评分链路已实现基础一跳查询与 AI4SEC Risk Score 输出，但高风险结果的通知升级出口尚未接入 Notification MCP。"`

---

## Part 4: Strategy & Architecture Compliance Report

*   **Compliance:** `PARTIAL`

*   **Violations:**

    1. **Principle 1229 (Dify Agent 是统一智能入口):** Three separate Dify workflow entry points now exist — `ai4sec_agent` (unified), `ai4sec_threat_modeling_agent` (VS1 dedicated), and `WEBHOOK_AGENT` (webhook ingest). All are Dify-based, satisfying the technology-layer intent, but the *unified entry* semantic is fragmented at the application level. The principle text has not been updated to acknowledge the intentional multi-entry topology.

    2. **Principle 1230 (Notification MCP 是统一通知出口):** `WEBHOOK_AGENT` returns analysis results inline and does not dispatch through Notification MCP, even for severity_tier=Critical findings. Per element 1277 ToDo specification this is intentional ("高风险结果不需要升级或通知协同出口"), but this creates an undocumented exception at the principle level.

    3. **Separation of Concerns - Stale Relationship 1129:** Relationship 1129 (WEBHOOK_AGENT to ai4sec_opencti_mcp) still exists in the KG, implying the webhook path calls the MCP service, which does not match the as-built implementation. This residual relationship introduces a false dependency in the model.

    4. **Separation of Concerns - KG Element Quality:** Element 1437 still has an empty name and imperative-prose description that mixes execution steps with implementation hints, reducing the business layer's clarity as a specification layer.

*   **Recommendations:**

    1. Update Principle 1229 description to explicitly acknowledge the intentional multi-entry design: unified entry for general interaction (1214), VS1 dedicated entry for deep threat-model analysis (1436), and event-driven ingest entry for OpenCTI webhook signals (1277). Reframe the principle as "Dify 是唯一智能编排平台" rather than "统一入口" to preserve accuracy while acknowledging the as-built topology.
    2. Update Principle 1230 or add an explicit exception note: Notification MCP is the standard outbound notification channel for proactive agent-output scenarios; passive ingest analysis results from WEBHOOK_AGENT are returned inline without notification dispatch by design.
    3. Apply all [ELEMENT - MODIFY] and [RELATIONSHIP - DELETE] / [RELATIONSHIP - ADD] changes from Part 1 to restore KG accuracy before the next iteration begins.

---

## Part 5: KG Reorganization Plan (Progressive Disclosure + SoC)

### [REORGANIZATION - PRINCIPLES CHECK]

*   **Progressive Disclosure:** `PARTIAL`

    Rationale: The four-layer stack (StrategyLayerAndMotivationAspect to BusinessLayer to ApplicationLayer to TechnologyLayer) is present and readable at the SystemArchitecture level (view 158). However, the ApplicationLayer view (view 164) collapses all 9 application-layer elements and all 11 relationships — covering three distinct runtime paths and a [PROPOSED] future connector — into a single diagram. This exceeds the 7-15 element cognitive threshold and mixes currently-running paths with future scope, obscuring the as-built execution model.

*   **Separation of Concerns:** `PARTIAL`

    Rationale: Code directories cleanly separate concerns (workflow DSL, MCP services, notification, tests, container orchestration). However, the KG model does not reflect these separations in its view structure. The single ApplicationLayer view does not distinguish between: (a) unified orchestration path via MCP, (b) VS1 dedicated analysis path with direct OpenCTI access, (c) event-driven ingest path with direct OpenCTI access, or (d) future capability scope. Stale relationship 1129 also incorrectly crosses the boundary between paths (a) and (c), creating false coupling in the model.

*   **Hotspots:**
    1. `Model/System/ApplicationLayer/ApplicationLayer/ApplicationLayer` (View 164) — 9 elements, 11 relationships, 3 distinct runtime paths plus 1 proposed element, all mixed in one diagram.
    2. `Model/System/BusinessLayer/BusinessLayer/威胁建模闭环流程/威胁建模闭环流程001` (View 181) — element 1437 has no name, making the view unnavigable in modeling tools.
    3. `Model/System/StrategyLayerAndMotivationAspect/StrategyLayerAndMotivationAspect/Strategic Goals and Principles` (View 177) — Principles 1229 and 1230 no longer accurately describe the as-built multi-entry and no-notification-escalation topology.

---

### [VIEW - ADD]

*   **View Name:** `VS1 威胁建模运行时链路`
*   **Target Browser Path:** `Model/System/ApplicationLayer/ApplicationLayer/VS1 威胁建模运行时链路`
*   **Purpose:** `Explain the end-to-end runtime execution path for the standalone VS1 threat-modeling analysis: from user input to direct OpenCTI GraphQL query to LLM output.`
*   **Description:** `Stakeholders: security architect, intelligence analyst, application maintainer. Concerns: how does the VS1 workflow resolve a report reference, query OpenCTI GraphQL directly, filter the STIX bundle, and return a structured threat-model result? Purpose: provide a focused runtime drill-down for VS1 that is readable independently of other runtime paths. Scope: ai4sec_threat_modeling_agent (1436), Dify Runtime Stack (1275), OpenCTI Runtime Stack (1276), and the direct GraphQL access relationship (1244). The VS1 威胁建模分析执行对象 (1437) may additionally be referenced from the BusinessLayer to show the business contract being realized.`
*   **Included Elements:** `["1436", "1275", "1276"]`
*   **Included Relationships:** `["1244", "1245"]`
*   **Reason:** `Isolates the VS1 direct-GraphQL runtime path so that architects reviewing the ApplicationLayer overview do not need to trace VS1-specific relationships through the same diagram used to understand the unified agent or webhook paths.`

---

*   **View Name:** `OpenCTI Webhook 事件接入链路`
*   **Target Browser Path:** `Model/System/ApplicationLayer/ApplicationLayer/OpenCTI Webhook 事件接入链路`
*   **Purpose:** `Explain the end-to-end runtime path for OpenCTI-originated event ingest: from push signal to risk-scored analysis output.`
*   **Description:** `Stakeholders: security operations engineer, platform integrator, alert-triage analyst. Concerns: how does an OpenCTI vulnerability-push event arrive, get normalized, trigger a one-hop infrastructure query against OpenCTI GraphQL, and produce a risk-scored structured response? Purpose: isolate the webhook-driven ingest runtime path from the interactive query and VS1 analysis paths. Scope: WEBHOOK_AGENT (1277), OpenCTI Runtime Stack (1276), Dify Runtime Stack (1275), and the new direct-access relationship (WEBHOOK_AGENT to OpenCTI Runtime Stack added in Part 1). Explicitly excludes ai4sec_opencti_mcp to reflect the as-built bypass.`
*   **Included Elements:** `["1277", "1275", "1276"]`
*   **Included Relationships:** `["1086", "1131", "<new WEBHOOK_AGENT to OpenCTI Runtime Stack ArchiMate_Access relationship>"]`
*   **Reason:** `Makes the WEBHOOK_AGENT runtime path independently readable and confirms that relationship 1129 (stale MCP dependency) has been removed, so the as-built direct-access design is explicit in its own view.`

---

*   **View Name:** `MCP 服务与统一工作流链路`
*   **Target Browser Path:** `Model/System/ApplicationLayer/ApplicationLayer/MCP 服务与统一工作流链路`
*   **Purpose:** `Explain the runtime path where ai4sec_agent calls ai4sec_opencti_mcp and Notification MCP for general VS1-VS4 orchestration.`
*   **Description:** `Stakeholders: platform developer, integration engineer, QA engineer. Concerns: which service does the unified agent call for STIX context queries, which endpoint does it use for notification dispatch, and how do the MCP services connect to the underlying OpenCTI and SMTP infrastructure? Purpose: isolate the MCP-mediated runtime path to contrast it clearly with the two direct-GraphQL paths in the VS1 and webhook views. Scope: ai4sec_agent (1214), ai4sec_opencti_mcp (1215), Notification MCP (1227), Dify Runtime Stack (1275), OpenCTI Runtime Stack (1276), with relationships 1079, 1082, 1083, 1089.`
*   **Included Elements:** `["1214", "1215", "1227", "1275", "1276"]`
*   **Included Relationships:** `["1079", "1082", "1083", "1089"]`
*   **Reason:** `Separates the MCP-mediated unified orchestration concern from the direct-GraphQL VS1 and webhook paths, reducing cognitive cost when reading any one runtime path.`

---

### [VIEW - MODIFY]

*   **View Name:** `ApplicationLayer`
*   **Current Browser Path:** `Model/System/ApplicationLayer/ApplicationLayer/ApplicationLayer`
*   **Target Browser Path:** `Model/System/ApplicationLayer/ApplicationLayer/ApplicationLayer`
*   **Change:** `Narrow Scope`
*   **Before Scope:** `All 9 application-layer elements and 11 relationships in one diagram, mixing three runtime paths, a placeholder connector, and runtime stack deployment topology.`
*   **After Scope:** `High-level application component inventory and coarse deployment aggregation only. Show all application-layer components (1214, 1215, 1217, 1218, 1227, 1277, 1436) and both runtime stacks (1275, 1276) with only the aggregation relationships (1079, 1130, 1131, 1245) and composition boundaries. Move all runtime access and serving relationships to the three focused scenario views added above.`
*   **Description Update:** `Stakeholders: enterprise architect, product owner, technical reviewer. Concerns: what application components exist in this system and on which runtime platforms do they deploy? Purpose: entry-point orientation view before drilling into runtime-specific scenario views. Scope: application-layer component inventory and deployment aggregation relationships only. Scenario-specific data-access and notification relationships are shown in subordinate views.`

---

### [VIEW - SPLIT]

*   **Source View:** `ApplicationLayer`
*   **Source Browser Path:** `Model/System/ApplicationLayer/ApplicationLayer/ApplicationLayer`
*   **New Views:** `["VS1 威胁建模运行时链路", "OpenCTI Webhook 事件接入链路", "MCP 服务与统一工作流链路"]`
*   **Target Browser Paths:** `["Model/System/ApplicationLayer/ApplicationLayer/VS1 威胁建模运行时链路", "Model/System/ApplicationLayer/ApplicationLayer/OpenCTI Webhook 事件接入链路", "Model/System/ApplicationLayer/ApplicationLayer/MCP 服务与统一工作流链路"]`
*   **Split Logic:** `Separate by runtime path concern boundary: (1) VS1 direct-GraphQL analysis path, (2) OpenCTI event ingest and risk-scoring path, (3) MCP-mediated unified orchestration path. The source view retains only the deployment inventory. Each new view addresses one stakeholder concern without crossover.`
*   **Description Requirement:** `Each new view must include Stakeholders / Concerns / Purpose / Scope as specified in the [VIEW - ADD] entries above.`

---

### [VIEW - MERGE]

*   **Source Views:** `[]`
*   **Source Browser Paths:** `[]`
*   **Target View:** `N/A`
*   **Target Browser Path:** `N/A`
*   **Merge Logic:** `No redundant parallel views were identified in the current audit. The primary readability problem is a single overloaded ApplicationLayer view; no two existing views duplicate each other scope.`
*   **Description Requirement:** `N/A`

---

### [ELEMENT - MOVE]

*   **Element:** `1437 / VS1威胁建模分析执行对象`
*   **Current Browser Path:** `Model/System/BusinessLayer/BusinessLayer/威胁建模闭环流程`
*   **Target Browser Path:** `Model/System/BusinessLayer/BusinessLayer/威胁建模闭环流程/VS1威胁建模分析执行对象`
*   **Reason:** `Moving the element into its parent process subtree provides ownership clarity and makes it navigable as a child artifact of the VS1 business process in modeling tools, consistent with how other process-scoped objects are nested.`

---

### [RELATIONSHIP - MOVE]

*   **Relationship:** `1244 - ai4sec_threat_modeling_agent --(access opencti stix data)--> OpenCTI Runtime Stack`
*   **From View:** `ApplicationLayer` (View 164)
*   **To View:** `VS1 威胁建模运行时链路`
*   **Reason:** `This relationship is a VS1-specific runtime access dependency. Showing it in the ApplicationLayer overview adds noise for readers who only need platform composition. It belongs in the VS1 dedicated runtime view.`

---

*   **Relationship:** `1245 - ai4sec_threat_modeling_agent aggregates Dify Runtime Stack`
*   **From View:** `ApplicationLayer` (View 164)
*   **To View:** `VS1 威胁建模运行时链路`
*   **Reason:** `Aggregation relationship tightly coupled to VS1 runtime path; relocating it to the VS1 view keeps the focused drill-down self-contained.`

---

*   **Relationship:** `1082 - ai4sec_agent --(access opencti stix data)--> ai4sec_opencti_mcp`
*   **From View:** `ApplicationLayer` (View 164)
*   **To View:** `MCP 服务与统一工作流链路`
*   **Reason:** `MCP data-access relationship belongs in the MCP service-focused view, not the platform inventory overview.`

---

*   **Relationship:** `1083 - ai4sec_opencti_mcp --(access情报数据)--> OpenCTI Runtime Stack`
*   **From View:** `ApplicationLayer` (View 164)
*   **To View:** `MCP 服务与统一工作流链路`
*   **Reason:** `MCP-to-OpenCTI access belongs with the MCP-mediated runtime path.`

---

*   **Relationship:** `1089 - ai4sec_agent --(发送预警通知)--> Notification MCP`
*   **From View:** `ApplicationLayer` (View 164)
*   **To View:** `MCP 服务与统一工作流链路`
*   **Reason:** `Notification dispatch is a unified-agent-specific concern and should be isolated to the MCP service view.`

---

*   **Relationship:** `1086 - OpenCTI Runtime Stack --(主动推送STIX BUNDLE情报信息)--> WEBHOOK_AGENT`
*   **From View:** `ApplicationLayer` (View 164)
*   **To View:** `OpenCTI Webhook 事件接入链路`
*   **Reason:** `Push trigger relationship belongs in the webhook-specific ingest view.`
