## Part 1: The Architecture Change Report

### [TRACEABILITY - UPDATE]
*   **Element Name:** `1214 / ai4sec_agent`
*   **Code Paths:** `["DifyAgentWorkflow/ai4sec_unified_workflow.yaml", "DifyAgentWorkflow/tools/ai4sec_runtime_tools.py"]`
*   **Reason:** `code_paths is missing, but the element is implemented by the unified Dify workflow asset and shared runtime tool module.`

*   **Element Name:** `1215 / ai4sec_opencti_mcp`
*   **Code Paths:** `["mcp/opencti_mcp/app/main.py", "mcp/opencti_mcp/app/service.py", "mcp/opencti_mcp/app/models.py", "mcp/opencti_mcp/app/settings.py"]`
*   **Reason:** `code_paths is missing, and the implementation has materially changed during this iteration to exact-only report lookup and compatibility-oriented threat-model support.`

*   **Element Name:** `1275 / Dify Runtime Stack`
*   **Code Paths:** `["externalDify/docker-compose.yaml", "DifyAgentWorkflow/ai4sec_unified_workflow.yaml", "DifyAgentWorkflow/ai4sec_threat_modeling_workflow.yaml"]`
*   **Reason:** `code_paths is missing, but the runtime stack is concretely represented by the Dify compose deployment and the workflow assets executed on it.`

*   **Element Name:** `1276 / OpenCTI Runtime Stack`
*   **Code Paths:** `["external_opencti/docker-compose.yml", "external_opencti/opencti_webhook_signal_template.ejs"]`
*   **Reason:** `code_paths is missing, while the stack is concretely implemented by the repository-owned OpenCTI compose deployment and webhook signal template.`

*   **Element Name:** `1277 / WEBHOOK_AGENT`
*   **Code Paths:** `["DifyAgentWorkflow/ai4sec_opencti_webhook_workflow.yaml", "DifyAgentWorkflow/tools/ai4sec_runtime_tools.py"]`
*   **Reason:** `Existing code_paths is incomplete; current metadata points only to the unified workflow and misses the dedicated webhook workflow plus the shared routing/tool logic.`

*   **Element Name:** `1436 / ai4sec_threat_modeling_agent`
*   **Code Paths:** `["DifyAgentWorkflow/ai4sec_threat_modeling_workflow.yaml"]`
*   **Reason:** `code_paths is missing, and this element now maps to a standalone VS1 workflow that directly queries OpenCTI GraphQL rather than calling ai4sec_opencti_mcp at runtime.`

### [TRACEABILITY - ALIGNED (OMITTED)]
*   **Rule:** Do not list aligned elements one-by-one.
*   **Summary:** `1 audited application element was already aligned and omitted from [TRACEABILITY - UPDATE]: 1227 / Notification MCP.`

### [ELEMENT - ADD]
*   **Name:** `N/A`
*   **Type:** `N/A`
*   **Parent View:** `N/A`
*   **Description:** `No mandatory new architecture element is required for the current as-built implementation after mapping the changed workflow, MCP, notification, and runtime files back to existing KG elements.`
*   **Attributes:** `N/A`

### [ELEMENT - MODIFY]
*   **Name:** `1215 / ai4sec_opencti_mcp`
*   **Change Summary:** `The current description still presents 1215 as the primary VS1 runtime threat-model provider and understates the now-implemented exact-only lookup behavior. After this iteration, 1215 remains an MCP compatibility service, but VS1 standalone runtime no longer depends on it.`
*   **TOBE Name:** `N/A`
*   **TOBE Description:** `Repository-local OpenCTI MCP compatibility service that loads configuration from the repository root environment, provides STIX projection queries, bundle writeback, webhook passthrough, and exact-only threat-model report resolution for compatibility use cases. After this iteration, the standalone VS1 threat-modeling workflow no longer calls this service at runtime and instead queries OpenCTI GraphQL directly, while 1215 remains the reusable application-layer OpenCTI access service for unified-agent and compatibility scenarios.`
*   **TOBE Attributes:**
    *   `code_paths = ["mcp/opencti_mcp/app/main.py", "mcp/opencti_mcp/app/service.py", "mcp/opencti_mcp/app/models.py", "mcp/opencti_mcp/app/settings.py"]`
*   **TOBE Browser Path:** `N/A`

*   **Name:** `1436 / ai4sec_threat_modeling_agent`
*   **Change Summary:** `The current description says this element queries the MCP threat-model endpoint, but the as-built workflow now performs direct GraphQL access to OpenCTI inside the Dify code node.`
*   **TOBE Name:** `N/A`
*   **TOBE Description:** `Dedicated standalone Dify advanced-chat workflow agent for VS1 that accepts report reference input, resolves exact report identifiers, queries OpenCTI GraphQL directly through an inline workflow code node, filters the returned STIX 2.1 evidence bundle, invokes structured LLM generation, and returns downloadable JSON results in-session. This runtime path no longer depends on ai4sec_opencti_mcp.`
*   **TOBE Attributes:**
    *   `code_paths = ["DifyAgentWorkflow/ai4sec_threat_modeling_workflow.yaml"]`
*   **TOBE Browser Path:** `N/A`

*   **Name:** `1218 / 外部站点`
*   **Change Summary:** `The element is modeled as implemented, but no crawler, connector adapter, or site-ingestion runtime exists in the repository. It should be marked as future scope rather than current implementation.`
*   **TOBE Name:** `N/A`
*   **TOBE Description:** `[PROPOSED] Future external source endpoint representing third-party intelligence or public-site inputs. No dedicated crawling, scraping, or connector runtime is implemented in the current repository; current integration relies on OpenCTI-side ingestion and webhook-driven delivery instead.`
*   **TOBE Attributes:**
    *   `code_paths = []`
*   **TOBE Browser Path:** `N/A`

*   **Name:** `1277 / WEBHOOK_AGENT`
*   **Change Summary:** `The element lacks description and has incomplete traceability for the dedicated webhook workflow path.`
*   **TOBE Name:** `N/A`
*   **TOBE Description:** `Webhook-oriented Dify workflow asset that receives OpenCTI-originated events, routes them into AI4SEC scenario processing, and reuses shared runtime tool logic for signal resolution, scenario routing, and downstream notification preparation.`
*   **TOBE Attributes:**
    *   `code_paths = ["DifyAgentWorkflow/ai4sec_opencti_webhook_workflow.yaml", "DifyAgentWorkflow/tools/ai4sec_runtime_tools.py"]`
*   **TOBE Browser Path:** `N/A`

### [RELATIONSHIP - ADD]
*   **Source:** `ai4sec_threat_modeling_agent`
*   **Target:** `OpenCTI Runtime Stack`
*   **Type:** `Access`
*   **Parent View:** `Model/System/ApplicationLayer/ApplicationLayer/ApplicationLayer`
*   **Description:** `The as-built VS1 standalone workflow now accesses OpenCTI directly through OPENCTI_GRAPHQL_URL from its code node, so the graph needs an explicit direct access relationship from 1436 to 1276. This relationship should supersede the old 1436 -> 1215 runtime interpretation represented by relationship 1244.`

## Part 2: Business Gap Analysis
*   **Implemented Processes:** `The repository now directly supports the VS1 threat-modeling closed loop through a standalone Dify workflow, OpenCTI live report lookup, filtered STIX evidence projection, LLM structured output, and validation assets. Shared workflow routing, OpenCTI MCP, Notification MCP, and validation collateral also provide partial support foundations for broader business-layer interaction.`
*   **Missing Capabilities:** `The BusinessLayer processes for incident response closed loop (1261), knowledge evolution closed loop (1262), and environment-aware monitoring closed loop (1263) still lack equivalent as-built dedicated workflow implementations at the same depth as VS1. The unified agent remains a routing shell rather than a fully realized end-to-end executor for VS2-VS4. Dify-side bundle writeback and human-verified UI acceptance are also incomplete for the VS1 closed loop.`
*   **Suggestions:** `Prioritize turning VS2-VS4 from routing placeholders into executable workflow assets, add explicit writeback/orchestration coverage where the business process expects closed-loop persistence, and link each business process to a concrete workflow or service artifact with code_paths-backed traceability.`

## Part 3: Documentation & README Synchronization
*   **Reviewed READMEs:**
    *   **File:** `README.md`
    *   **File:** `tests/validation/README.md`
*   **Discrepancies:** `The root README is no longer aligned with the current VS1 implementation. It still describes the standalone VS1 workflow as using an HTTP request node that calls /query/threat-model-report on OpenCTI MCP, and it still documents fuzzy fallback behavior in the MCP threat-model endpoint description. The current implementation instead uses direct GraphQL in DifyAgentWorkflow/ai4sec_threat_modeling_workflow.yaml, exact-id/exact-name lookup, schema-compatibility handling for live OpenCTI fields, and compact analysis_input without duplicated bundle payloads. The validation README remains broadly aligned because it documents manual acceptance scope and does not claim the obsolete MCP runtime path.`
*   **Recommended Updates (Not Applied):** `Update the root README sections for the standalone VS1 workflow and OpenCTI MCP so they describe direct OpenCTI GraphQL access in the workflow, exact-only report resolution, compact prompt payload construction, and the remaining human Dify UI validation step. Keep tests/validation/README.md unchanged except for optional wording that references the standalone VS1 workflow as the current deepest implemented business-layer path.`

## Part 4: Strategy & Architecture Compliance Report
*   **Compliance:** `PARTIAL`
*   **Violations:** `The implementation still respects the high-level principles that OpenCTI is the central CTI substrate, STIX 2.1 remains the primary evidence format, and Dify is the user-facing orchestration entry. However, Separation of Concerns is only partially satisfied because the standalone VS1 workflow now duplicates part of the OpenCTI query/projection logic that also exists in mcp/opencti_mcp/app/service.py. Traceability compliance is also weak because critical application and technology elements still lack or understate code_paths in the KG. Finally, the current architecture graph still implies 1436 -> 1215 runtime access, which no longer matches the as-built direct GraphQL path to 1276.`
*   **Recommendations:** `Update KG descriptions and relationships to reflect the direct VS1 runtime path, add missing code_paths for all active application and technology elements, and decide whether direct GraphQL access in workflow nodes is now the target architecture or a temporary optimization. If it is the target architecture, isolate shared projection logic into a reusable library or clearly separate workflow-resident projection from MCP-resident compatibility services to restore modularity.`

## Part 5: KG Reorganization Plan (Progressive Disclosure + SoC)

### [REORGANIZATION - PRINCIPLES CHECK]
*   **Progressive Disclosure:** `PARTIAL. The current ApplicationLayer view mixes runtime stacks, unified orchestration, standalone VS1 execution, webhook processing, notification dispatch, and external connector placeholders in a single diagram. This is too broad for readers trying to understand one runtime path at a time.`
*   **Separation of Concerns:** `PARTIAL. Responsibilities are separated in code directories, but the KG presentation still collapses orchestration, data access, webhook ingress, and notification integration into the same application-layer view, and the graph has not been updated to reflect the direct VS1 OpenCTI access path.`
*   **Hotspots:** `Model/System/ApplicationLayer/ApplicationLayer/ApplicationLayer`, `Model/System/BusinessLayer/BusinessLayer/威胁建模闭环流程/威胁建模闭环流程001`, and `Model/System/StrategyLayerAndMotivationAspect/StrategyLayerAndMotivationAspect/Strategic Goals and Principles` are the main cognitive-overload hotspots.`

### [VIEW - ADD]
*   **View Name:** `VS1 Threat Modeling Runtime Flow`
*   **Target Browser Path:** `Model/System/ApplicationLayer/ApplicationLayer/VS1 Threat Modeling Runtime Flow`
*   **Purpose:** `Explain only the standalone VS1 runtime path from user input to OpenCTI retrieval and LLM output.`
*   **Description:** `Stakeholders: security architect, intelligence analyst, application owner. Concerns: exact report lookup, direct OpenCTI access, filtered STIX payload generation, LLM threat-model output. Purpose: make the as-built VS1 runtime path readable without unrelated webhook or notification concerns. Scope: ai4sec_threat_modeling_agent, Dify Runtime Stack, OpenCTI Runtime Stack, and the direct access relationship added for this iteration.`
*   **Included Elements:** `["1436", "1275", "1276"]`
*   **Included Relationships:** `[]`
*   **Reason:** `This isolates the newly implemented direct GraphQL path and prevents the main ApplicationLayer view from mixing standalone VS1 details with unrelated platform composition.`

### [VIEW - MODIFY]
*   **View Name:** `ApplicationLayer`
*   **Current Browser Path:** `Model/System/ApplicationLayer/ApplicationLayer/ApplicationLayer`
*   **Target Browser Path:** `Model/System/ApplicationLayer/ApplicationLayer/ApplicationLayer`
*   **Change:** `Narrow Scope / Re-layout`
*   **Before Scope:** `Unified agent, standalone VS1 agent, webhook agent, external connectors, notification service, and runtime stacks are all shown together with access, aggregation, webhook, and notification relationships.`
*   **After Scope:** `Keep this view as high-level platform composition only: unified agent, standalone agent, webhook agent, Notification MCP, Dify Runtime Stack, OpenCTI Runtime Stack, and coarse-grained integration boundaries. Move scenario-specific runtime flows into focused subordinate views.`
*   **Description Update:** `Stakeholders: architects, maintainers, platform integrators. Concerns: top-level application composition and platform boundaries. Purpose: provide the entry-point overview before drilling into scenario-specific runtime views. Scope: application-layer primary components and coarse integration lines only.`

### [VIEW - SPLIT]
*   **Source View:** `ApplicationLayer`
*   **Source Browser Path:** `Model/System/ApplicationLayer/ApplicationLayer/ApplicationLayer`
*   **New Views:** `["VS1 Threat Modeling Runtime Flow", "OpenCTI MCP Compatibility Service", "Notification and Webhook Integration"]`
*   **Target Browser Paths:** `["Model/System/ApplicationLayer/ApplicationLayer/VS1 Threat Modeling Runtime Flow", "Model/System/ApplicationLayer/ApplicationLayer/OpenCTI MCP Compatibility Service", "Model/System/ApplicationLayer/ApplicationLayer/Notification and Webhook Integration"]`
*   **Split Logic:** `Separate scenario execution, compatibility data-access service behavior, and webhook/notification integration into different concerns instead of one mixed application diagram.`
*   **Description Requirement:** `For each new View, include Stakeholders / Concerns / Purpose / Scope in its description.`

### [VIEW - MERGE]
*   **Source Views:** `[]`
*   **Source Browser Paths:** `[]`
*   **Target View:** `N/A`
*   **Target Browser Path:** `N/A`
*   **Merge Logic:** `No merge is recommended in the current audit scope; the main readability problem is overloaded mixed-concern views, not redundant duplicate views.`
*   **Description Requirement:** `N/A`

### [ELEMENT - MOVE]
*   **Element:** `N/A`
*   **Current Browser Path:** `N/A`
*   **Target Browser Path:** `N/A`
*   **Reason:** `No element browser-path move is strictly required; the primary problem is missing traceability and overloaded views rather than wrong ownership folder placement.`

### [RELATIONSHIP - MOVE]
*   **Relationship:** `1082 / ai4sec_agent --(access opencti stix data)--> ai4sec_opencti_mcp`
*   **From View:** `ApplicationLayer`
*   **To View:** `OpenCTI MCP Compatibility Service`
*   **Reason:** `This relationship is a compatibility/data-access concern and should be shown in a dedicated data-access view instead of the top-level application composition view.`

*   **Relationship:** `1083 / ai4sec_opencti_mcp --(access...)--> OpenCTI Runtime Stack`
*   **From View:** `ApplicationLayer`
*   **To View:** `OpenCTI MCP Compatibility Service`
*   **Reason:** `This relationship belongs with MCP-to-OpenCTI access semantics and clutters the platform overview when shown together with unrelated notification and webhook relationships.`

*   **Relationship:** `1089 / ai4sec_agent -> Notification MCP`
*   **From View:** `ApplicationLayer`
*   **To View:** `Notification and Webhook Integration`
*   **Reason:** `Notification dispatch is a separate concern from VS1 direct OpenCTI access and should be isolated to improve readability.`

*   **Relationship:** `1244 / ai4sec_threat_modeling_agent --(access opencti stix data)--> ai4sec_opencti_mcp`
*   **From View:** `ApplicationLayer`
*   **To View:** `VS1 Threat Modeling Runtime Flow`
*   **Reason:** `This relationship is currently the closest existing model anchor for VS1 runtime data access. It should be reviewed in the dedicated VS1 runtime view and replaced there by the new direct 1436 -> 1276 access relationship so the top-level view no longer carries an outdated runtime interpretation.`## Part 1: The Architecture Change Report

### [TRACEABILITY - UPDATE]
*   **Element Name:** `1436 / ai4sec_threat_modeling_agent`
*   **Code Paths:** `[
    "DifyAgentWorkflow/ai4sec_threat_modeling_workflow.yaml"
]`
*   **Reason:** `Element exists in ApplicationLayer view semantics (relationship 1244/1245 resolved globally), but its `code_paths` attribute is missing in the KG.`

*   **Element Name:** `1437 / (unnamed object in 威胁建模闭环流程)`
*   **Code Paths:** `[
    "DifyAgentWorkflow/ai4sec_threat_modeling_workflow.yaml",
    "mcp/opencti_mcp/app/main.py",
    "mcp/opencti_mcp/app/models.py",
    "mcp/opencti_mcp/app/service.py"
]`
*   **Reason:** `Current element metadata is incomplete (empty name, no code_paths) and description embeds legacy plugin pseudocode instead of the as-built Dify LLM + MCP workflow interaction.`

*   **Element Name:** `1277 / WEBHOOK_AGENT`
*   **Code Paths:** `[
    "DifyAgentWorkflow/ai4sec_unified_workflow.yaml"
]`
*   **Reason:** `Element participates in globally resolved relationships 1086/1128/1129/1131 but has no code_paths traceability.`

### [TRACEABILITY - ALIGNED (OMITTED)]
*   **Rule:** Do not list aligned elements one-by-one.
*   **Summary:** `6 elements verified as already aligned and omitted from [TRACEABILITY - UPDATE] (1214, 1215, 1227, 1275, 1276, 1282).`

### [ELEMENT - ADD]
*   **Name:** `N/A`
*   **Type:** `N/A`
*   **Parent View:** `N/A`
*   **Description:** `No mandatory new runtime element was found for this iteration scope after reverse-checking changed code against existing KG elements.`
*   **Attributes:** `N/A`

### [ELEMENT - MODIFY]
*   **Name:** `1437 / (unnamed object in 威胁建模闭环流程)`
*   **Change Summary:** `Element currently has empty name and outdated implementation description; it should represent the as-built VS1 report-driven threat-modeling analysis contract.`
*   **TOBE Name:** `VS1 Threat Modeling Analysis Contract`
*   **TOBE Description:** `This object defines the as-built VS1 threat-modeling interaction contract: user provides report name or report ID, Dify workflow resolves effective reference, MCP endpoint /query/threat-model-report performs exact-first and fuzzy fallback matching on live OpenCTI reports, returns filtered STIX 2.1 bundle plus analysis_input, and the workflow invokes LLM structured output to generate threat-model JSON with in-session download link.`
*   **TOBE Attributes:**
    *   `code_paths = ["DifyAgentWorkflow/ai4sec_threat_modeling_workflow.yaml", "mcp/opencti_mcp/app/main.py", "mcp/opencti_mcp/app/models.py", "mcp/opencti_mcp/app/service.py"]`
*   **TOBE Browser Path:** `Model/System/BusinessLayer/BusinessLayer/威胁建模闭环流程`

*   **Name:** `1436 / ai4sec_threat_modeling_agent`
*   **Change Summary:** `Element exists but lacks traceability metadata to the standalone workflow asset.`
*   **TOBE Name:** `ai4sec_threat_modeling_agent`
*   **TOBE Description:** `Dedicated standalone Dify advanced-chat workflow agent for VS1 that accepts report reference input, queries OpenCTI MCP threat-model report endpoint, invokes real LLM structured generation, and returns downloadable JSON results in-session.`
*   **TOBE Attributes:**
    *   `code_paths = ["DifyAgentWorkflow/ai4sec_threat_modeling_workflow.yaml"]`
*   **TOBE Browser Path:** `Model/System/ApplicationLayer/ApplicationLayer/ai4sec_threat_modeling_agent`

*   **Name:** `1217 / 外部信息爬取Connector`
*   **Change Summary:** `Element is present in ApplicationLayer context but has no implementation evidence in current repository scope.`
*   **TOBE Name:** `外部信息爬取Connector`
*   **TOBE Description:** `[PROPOSED] Future external intelligence crawling connector. In current as-built scope, no crawler runtime, scheduler, or external site ingestion implementation is delivered.`
*   **TOBE Attributes:**
    *   `code_paths = []`
*   **TOBE Browser Path:** `Model/System/ApplicationLayer/ApplicationLayer/外部信息爬取Connector`

### [RELATIONSHIP - ADD]
*   **Source:** `1436 / ai4sec_threat_modeling_agent`
*   **Target:** `1437 / VS1 Threat Modeling Analysis Contract`
*   **Type:** `ArchiMate_Realization`
*   **Parent View:** `Model/System/BusinessLayer/BusinessLayer/威胁建模闭环流程/威胁建模闭环流程001`
*   **Description:** `The standalone VS1 workflow implementation realizes the analysis contract object currently represented by element 1437.`

*   **Source:** `1437 / VS1 Threat Modeling Analysis Contract`
*   **Target:** `1215 / ai4sec_opencti_mcp`
*   **Type:** `ArchiMate_Access`
*   **Parent View:** `Model/System/ApplicationLayer/ApplicationLayer/ApplicationLayer`
*   **Description:** `The contract object relies on MCP endpoint /query/threat-model-report and associated response model filtering logic.`

## Part 2: Business Gap Analysis
*   **Implemented Processes:** `威胁建模闭环流程中的“输入报告引用 -> OpenCTI查询 -> LLM结构化分析 -> 会话内下载输出”已由 standalone VS1 workflow 与 MCP API 实现；精确匹配优先、双模糊回退、STIX字段过滤均有代码与测试证据。`
*   **Missing Capabilities:** `关键业务流程中的 VS2/VS3/VS4 闭环步骤在本次迭代范围内未形成同等深度的“报告驱动+结构化输出”能力；BusinessLayer 中角色治理与绩效度量仍主要停留在文档/测试验收层，未看到运行时指标采集或闭环写回编排。`

## Part 3: Documentation & README Synchronization
*   **Reviewed READMEs:**
    *   **File:** `README.md`
    *   **File:** `tests/validation/README.md`
*   **Discrepancies:** `README.md 以统一 workflow 为核心叙述，但当前仓库已新增并实际调试了独立 VS1 workflow（ai4sec_threat_modeling_workflow.yaml）；README.md 对 Dify DSL 回归验证状态描述偏保守，未体现已完成的关键运行时缺陷修复（变量插值节点命名与 LLM JSON fence 兼容）。tests/validation/README.md 与测试目录结构基本一致。`
*   **Recommended Updates (Not Applied):** `在 README.md 的应用层实现映射中新增 standalone VS1 workflow 说明；在“实现边界”中明确：已完成 VS1 workflow 运行时缺陷修复，但最终 Dify UI 全链路验收仍依赖环境侧人工复核；补充 /query/threat-model-report 的接口能力摘要。`

## Part 4: Strategy & Architecture Compliance Report
*   **Compliance:** `PARTIAL`
*   **Violations:** `Separation of Concerns 在 KG 表达层面仍有偏差：BusinessLayer 元素 1437 描述混入历史插件代码，未与当前 Dify/MCP 运行契约对齐；Progressive Disclosure 在视图层面部分不足：ApplicationLayer 视图同时承载运行态与未来态（如外部爬取Connector）语义。`
*   **Recommendations:** `优先修正 1437 元素语义与 traceability；将当前运行态链路与未来态能力拆分建模；继续保持 STIX-first 与 OpenCTI 单一底座原则，并在后续将业务闭环覆盖扩展到 VS2/VS3/VS4 的对等实现深度。`

## Part 5: KG Reorganization Plan (Progressive Disclosure + SoC)

### [REORGANIZATION - PRINCIPLES CHECK]
*   **Progressive Disclosure:** `PARTIAL` with rationale: `层次顺序齐全（Strategy->Business->Application->Technology），但 ApplicationLayer 视图混合当前可运行链路与未来态能力，认知负载偏高。`
*   **Separation of Concerns:** `PARTIAL` with rationale: `威胁建模业务契约（1437）与实现细节表达混杂，且外部采集与核心运行流未完全分离展示。`
*   **Hotspots:** `Model/System/ApplicationLayer/ApplicationLayer/ApplicationLayer`, `Model/System/BusinessLayer/BusinessLayer/威胁建模闭环流程/威胁建模闭环流程001`

### [VIEW - ADD]
*   **View Name:** `VS1 Runtime Threat Modeling Flow`
*   **Target Browser Path:** `Model/System/ApplicationLayer/ApplicationLayer/VS1 Runtime Threat Modeling Flow`
*   **Purpose:** `Single concern this view explains: standalone VS1 runtime execution path`
*   **Description:** `Stakeholders: solution architect, security analyst, platform maintainer. Concerns: report reference resolution, MCP query contract, LLM structured generation output, runtime dependency boundaries. Purpose: provide a focused runtime drill-down for VS1 only. Scope: elements 1436, 1215, 1275, 1276, 1437 and relationships 1244, 1245, 1141, 1143, 1145, 1147 with globally resolved semantics.`
*   **Included Elements:** `["1436", "1215", "1275", "1276", "1437"]`
*   **Included Relationships:** `["1244", "1245", "1141", "1143", "1145", "1147"]`
*   **Reason:** `Reduces cognitive load by isolating VS1 runtime chain from broader application context.`

### [VIEW - MODIFY]
*   **View Name:** `Unnamed ApplicationLayer View`
*   **Current Browser Path:** `Model/System/ApplicationLayer/ApplicationLayer/ApplicationLayer`
*   **Target Browser Path:** `Model/System/ApplicationLayer/ApplicationLayer/Application Context Overview`
*   **Change:** `Narrow Scope`
*   **Before Scope:** `Core runtime, webhook branch, future connector, and stack topology mixed together.`
*   **After Scope:** `Keep only high-level component context; move detailed VS1 runtime flow to dedicated new view.`
*   **Description Update:** `Stakeholders: architect, product owner, reviewer. Concerns: top-level component boundaries and key interactions. Purpose: orientation view before drill-down. Scope: high-level application components and minimal cross-layer relationships.`

### [VIEW - SPLIT]
*   **Source View:** `Unnamed ApplicationLayer View`
*   **Source Browser Path:** `Model/System/ApplicationLayer/ApplicationLayer/ApplicationLayer`
*   **New Views:** `["Application Context Overview", "VS1 Runtime Threat Modeling Flow", "External Intelligence Ingestion (Proposed)"]`
*   **Target Browser Paths:** `["Model/System/ApplicationLayer/ApplicationLayer/Application Context Overview", "Model/System/ApplicationLayer/ApplicationLayer/VS1 Runtime Threat Modeling Flow", "Model/System/ApplicationLayer/ApplicationLayer/External Intelligence Ingestion (Proposed)"]`
*   **Split Logic:** `By concern boundary: context overview vs current runtime execution vs future external ingestion.`
*   **Description Requirement:** `For each new View, include Stakeholders / Concerns / Purpose / Scope in its description`

### [VIEW - MERGE]
*   **Source Views:** `[]`
*   **Source Browser Paths:** `[]`
*   **Target View:** `N/A`
*   **Target Browser Path:** `N/A`
*   **Merge Logic:** `No redundant parallel views were identified in current scope; main issue is overloaded single views.`
*   **Description Requirement:** `N/A`

### [ELEMENT - MOVE]
*   **Element:** `1437 / VS1 Threat Modeling Analysis Contract`
*   **Current Browser Path:** `Model/System/BusinessLayer/BusinessLayer/威胁建模闭环流程`
*   **Target Browser Path:** `Model/System/BusinessLayer/BusinessLayer/威胁建模闭环流程/VS1 Threat Modeling Analysis Contract`
*   **Reason:** `Ownership clarity and SoC for business-contract artifact under the VS1 process subtree.`

### [RELATIONSHIP - MOVE]
*   **Relationship:** `1244 (ai4sec_threat_modeling_agent -> ai4sec_opencti_mcp)`
*   **From View:** `Model/System/ApplicationLayer/ApplicationLayer/ApplicationLayer`
*   **To View:** `Model/System/ApplicationLayer/ApplicationLayer/VS1 Runtime Threat Modeling Flow`
*   **Reason:** `Readability improvement by relocating detailed VS1 runtime dependency to focused drill-down view.`

*   **Relationship:** `1141 (Business query call to OpenCTI Runtime Stack)`
*   **From View:** `Model/System/BusinessLayer/BusinessLayer/威胁建模闭环流程/威胁建模闭环流程001`
*   **To View:** `Model/System/ApplicationLayer/ApplicationLayer/VS1 Runtime Threat Modeling Flow`
*   **Reason:** `Reduce clutter in business-process storyboard and place technical call-chain relation in runtime view.`
