## Part 1: The Architecture Change Report

### [TRACEABILITY - UPDATE]
*   **Element Name:** `1213 / SKILL`
*   **Code Paths:** `[]`
*   **Reason:** `ApplicationLayer view (164) includes this element and relationship 1081 (ai4sec_agent --uses--> SKILL), but repository has no Dify-wired SKILL runtime implementation.`

*   **Element Name:** `1217 / 外部信息爬取AGENT`
*   **Code Paths:** `[]`
*   **Reason:** `ApplicationLayer view (164) includes this element and relationship 1084/1085, but repository has no crawler/connector implementation code owned by this project.`

### [TRACEABILITY - ALIGNED (OMITTED)]
*   **Rule:** Do not list aligned elements one-by-one.
*   **Summary:** `5 elements verified as already aligned and omitted from [TRACEABILITY - UPDATE] (1214, 1215, 1227, 1275, 1276).`

### [ELEMENT - ADD]
*   **Name:** `ai4sec_agent_mcp`
*   **Type:** `ApplicationComponent`
*   **Parent View:** `ApplicationLayer`
*   **Description:** `Repository already contains an additional AI4SEC agent MCP service implementation under mcp/ai4sec_agent/app that is not represented in the current KG.`
*   **Attributes:** `code_paths = ["mcp/ai4sec_agent/app/main.py", "mcp/ai4sec_agent/app/models.py"]`

*   **Name:** `Testing & Validation Framework`
*   **Type:** `ApplicationComponent`
*   **Parent View:** `ProjectManagement`
*   **Description:** `Repository has a five-layer verification asset set (unit/contract/integration/e2e/validation) that should be modeled as a managed project capability.`
*   **Attributes:** `code_paths = ["tests/unit/test_runtime_tools_closed_loop.py", "tests/contract/test_agent_webhook_contract.py", "tests/integration/test_webhook_to_notification_flow.py", "tests/e2e/test_delivery_assets.py", "tests/validation/README.md"]`

### [ELEMENT - MODIFY]
*   **Name:** `ai4sec_agent`
*   **Change Summary:** `Current KG description says notification dispatch is not orchestrated in YAML, but as-built workflow now contains VS4 manual review + notification dispatch to Notification MCP.`
*   **TOBE Name:** `ai4sec_agent`
*   **TOBE Description:** `AI4SEC Dify advanced-chat workflow asset that routes user input across VS1-VS4, calls ai4sec_opencti_mcp for scenario-specific context retrieval, and includes a VS4 manual review gate followed by notification dispatch to Notification MCP. OpenCTI bundle writeback orchestration is not yet wired in the Dify workflow.`
*   **TOBE Attributes:**
    *   `code_paths = ["DifyAgentWorkflow/ai4sec_unified_workflow.yaml", "DifyAgentWorkflow/tools/ai4sec_runtime_tools.py"]`
*   **TOBE Browser Path:** `N/A`

*   **Name:** `SKILL`
*   **Change Summary:** `Element is not implemented in current repository/runtime.`
*   **TOBE Name:** `SKILL`
*   **TOBE Description:** `[PROPOSED] Future business skill capability for ai4sec_agent. The current repository does not yet contain a Dify-integrated runtime implementation invoked by the as-built workflow.`
*   **TOBE Attributes:**
    *   `code_paths = []`
*   **TOBE Browser Path:** `N/A`

*   **Name:** `外部信息爬取AGENT`
*   **Change Summary:** `Element is currently future-state only; no as-built code evidence in repository.`
*   **TOBE Name:** `外部信息爬取AGENT`
*   **TOBE Description:** `[PROPOSED] Future external intelligence collection agent. No crawler runtime, scheduler, or ingestion implementation is present in this repository version.`
*   **TOBE Attributes:**
    *   `code_paths = []`
*   **TOBE Browser Path:** `N/A`

### [RELATIONSHIP - ADD]
*   **Source:** `ProjectManagement`
*   **Target:** `Testing & Validation Framework`
*   **Type:** `ArchiMate_Composition`
*   **Parent View:** `ProjectManagement`
*   **Description:** `ProjectManagement currently has an empty view (163), while repository has explicit managed verification assets and acceptance packs.`

*   **Source:** `ai4sec_agent`
*   **Target:** `Notification MCP`
*   **Type:** `ArchiMate_Triggering`
*   **Parent View:** `ApplicationLayer`
*   **Description:** `Relationship 1089 already exists semantically; add a Triggering refinement to represent the implemented VS4 branch that triggers Notification MCP dispatch after manual approval.`

## Part 2: Business Gap Analysis
*   **Implemented Processes:** `情报任务受理与分流（VS1-VS4路由）；威胁与影响研判（MCP查询+场景化结果）；通知与决策协同（VS4 人工复核后通知派发）；验证与验收资产（tests/validation 全量能力文档）。`
*   **Missing Capabilities:** `业务上下文归并的真实图谱回查深度不足（仍以轻量投影+本地上下文为主）；控制缺口与处置建议生成未形成可执行动作编排；证据链与知识资产沉淀缺少工作流内 /bundle 写回节点；监控命中反馈与规则持续校准未形成自动闭环；角色责任治理与业务绩效度量仅文档化、无运行时采集。`

## Part 3: Documentation & README Synchronization
*   **Reviewed READMEs:**
    *   **File:** `README.md`
    *   **File:** `tests/validation/README.md`
*   **Discrepancies:** `README.md 声明存在 .github/workflows/ci.yml，但仓库未包含 .github/workflows；README.md 对“端到端闭环”表述超前于当前编排现状（当前 YAML 未接入 /bundle 写回）。tests/validation/README.md 与现有验证资产基本一致。`
*   **Recommended Updates (Not Applied):** `将 README.md 中 CI 描述改为“待补充”或补齐 workflow 文件；将工作流能力描述改为“已实现路由+查询+VS4人工复核通知，写回闭环待实现”；在实现边界章节明确说明 /bundle 未接入 Dify 编排节点。`

## Part 4: Strategy & Architecture Compliance Report
*   **Compliance:** `PARTIAL`
*   **Violations:** `原则1226（STIX2.1 全流程）仍是部分达成：写回环节未在主编排中闭环；原则1229（统一智能入口）部分达成：统一入口存在，但价值流闭环步骤并未全部运行化。`
*   **Recommendations:** `优先在统一工作流接入 OpenCTI /bundle 写回节点并与人工复核门控绑定；随后补全 VS1/VS2/VS3 的通知/反馈分支，使 1221 目标“受理-查询-研判-写回-通知-反馈”与 as-built 一致。`

## Part 5: KG Reorganization Plan (Progressive Disclosure + SoC)

### [REORGANIZATION - PRINCIPLES CHECK]
*   **Progressive Disclosure:** `PARTIAL - 现有 views 已覆盖 Strategy/Business/Application/Technology，但 ApplicationLayer(164) 混合了未来态元素与运行态关系，ProjectManagement(163)为空视图。`
*   **Separation of Concerns:** `PARTIAL - 运行态编排、未来外部采集能力、项目治理能力未充分分离展示。`
*   **Hotspots:** `ApplicationLayer (view 164), ProjectManagement (view 163), TechnologyLayer (view 162)`

### [VIEW - ADD]
*   **View Name:** `Application Runtime Flow`
*   **Target Browser Path:** `Model/System/ApplicationLayer/ApplicationLayer/Application Runtime Flow`
*   **Purpose:** `展示当前已实现的运行态交互链路`
*   **Description:** `Stakeholders: solution architect, platform maintainer, tester. Concerns: runtime orchestration ownership, MCP interaction boundary, manual review gate, notification dispatch trigger. Purpose: explain as-built runtime interaction path. Scope: ai4sec_agent, ai4sec_opencti_mcp, Notification MCP, Dify Runtime Stack, OpenCTI Runtime Stack and runtime relationships.`
*   **Included Elements:** `["1214", "1215", "1227", "1275", "1276"]`
*   **Included Relationships:** `["1079", "1082", "1083", "1086", "1089"]`
*   **Reason:** `把运行链路从总览中下钻，降低认知负担。`

*   **View Name:** `Project Verification Governance`
*   **Target Browser Path:** `Model/System/ProjectManagement/ProjectManagement/Project Verification Governance`
*   **Purpose:** `展示项目治理与验证资产`
*   **Description:** `Stakeholders: project owner, QA lead, architect reviewer. Concerns: verification ownership, acceptance evidence, quality gate traceability. Purpose: map project management to executable verification assets. Scope: ProjectManagement element and Testing & Validation Framework with key governance relationships.`
*   **Included Elements:** `["1211", "Testing & Validation Framework"]`
*   **Included Relationships:** `["ProjectManagement->Testing & Validation Framework (ArchiMate_Composition)"]`
*   **Reason:** `填补当前空视图(163)，建立治理可追溯性。`

### [VIEW - MODIFY]
*   **View Name:** `ApplicationLayer`
*   **Current Browser Path:** `Model/System/ApplicationLayer/ApplicationLayer/ApplicationLayer`
*   **Target Browser Path:** `Model/System/ApplicationLayer/ApplicationLayer/Application Context Overview`
*   **Change:** `Narrow Scope`
*   **Before Scope:** `运行态关系、未来态外部采集、角色消费关系混在一个视图中。`
*   **After Scope:** `只保留应用层高阶上下文；运行态细节下沉到 Application Runtime Flow。`
*   **Description Update:** `Stakeholders: architect, product owner, reviewer. Concerns: top-level application boundary, core components, actor interaction. Purpose: provide high-level overview before drill-down. Scope: high-level components and minimal context relationships.`

*   **View Name:** `TechnologyLayer`
*   **Current Browser Path:** `Model/System/TechnologyLayer/TechnologyLayer/TechnologyLayer`
*   **Target Browser Path:** `Model/System/TechnologyLayer/TechnologyLayer/Technology Runtime Overview`
*   **Change:** `Re-layout`
*   **Before Scope:** `仅包含两个元素，未体现部署关注点拆分。`
*   **After Scope:** `聚焦 Dify/OpenCTI 两个 runtime stack 与其托管边界，减少与应用编排语义混杂。`
*   **Description Update:** `Stakeholders: platform engineer, SRE, maintainer. Concerns: runtime topology, hosting boundaries, stack ownership. Purpose: show deployment/runtime context of the system. Scope: runtime stack nodes and hosting/access concerns.`

### [VIEW - SPLIT]
*   **Source View:** `ApplicationLayer`
*   **Source Browser Path:** `Model/System/ApplicationLayer/ApplicationLayer/ApplicationLayer`
*   **New Views:** `["Application Context Overview", "Application Runtime Flow", "External Intelligence Ingestion (Proposed)"]`
*   **Target Browser Paths:** `["Model/System/ApplicationLayer/ApplicationLayer/Application Context Overview", "Model/System/ApplicationLayer/ApplicationLayer/Application Runtime Flow", "Model/System/ApplicationLayer/ApplicationLayer/External Intelligence Ingestion (Proposed)"]`
*   **Split Logic:** `按 concern 拆分为总览、运行态、未来外部采集三类。`
*   **Description Requirement:** `每个新视图描述都包含 Stakeholders / Concerns / Purpose / Scope。`

### [VIEW - MERGE]
*   **Source Views:** `[]`
*   **Source Browser Paths:** `[]`
*   **Target View:** `N/A`
*   **Target Browser Path:** `N/A`
*   **Merge Logic:** `当前主要问题是视图过载与空视图，不是重复视图。`
*   **Description Requirement:** `N/A`

### [ELEMENT - MOVE]
*   **Element:** `Testing & Validation Framework`
*   **Current Browser Path:** `N/A (new element)`
*   **Target Browser Path:** `Model/System/ProjectManagement/ProjectManagement/Testing & Validation Framework`
*   **Reason:** `把质量治理资产明确归属到 ProjectManagement，避免散落在文件系统但模型无主。`

### [RELATIONSHIP - MOVE]
*   **Relationship:** `1084 / 外部信息爬取AGENT --(通过connector同步情报)--> OpenCTI Runtime Stack`
*   **From View:** `ApplicationLayer`
*   **To View:** `External Intelligence Ingestion (Proposed)`
*   **Reason:** `该关系属于未来态外部采集关注点，不应与当前运行态主链路混放。`

*   **Relationship:** `1085 / 外部信息爬取AGENT --(主动爬取)--> 外部网站`
*   **From View:** `ApplicationLayer`
*   **To View:** `External Intelligence Ingestion (Proposed)`
*   **Reason:** `该关系与现有实现主路径解耦，独立视图更利于渐进披露。`
