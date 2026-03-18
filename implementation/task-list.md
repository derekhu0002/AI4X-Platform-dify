# 任务清单

- 报告生成日期：2026-03-18
- 总任务数：3
- 状态分布：Active 3
- 优先级分布：Low 3
- 假设说明：
  - 任务行字段以 `design/tasks/taskandissues_for_LLM.md` 为主；缺失的 `start_date`、`due_date`、`assigned_to`、`priority` 由 `design/KG/SystemArchitecture.json` 中元素 1277 与 1436 的 `project_info.tasks` 回填。
  - `due_date=1899-12-30` 视为未设置占位值，因此 `Due Date` 统一记为 `未设置`，`Days Until Due` 统一记为 `N/A`。
  - 已先生成当前任务集对应的支撑文件，因此 `Task Help Link` 使用 `implementation/taskhelpinfos` 下的相对链接；不存在 `N/A` 链接场景。
  - `Days Until Due` 需按提示词给定基准日期 2026-02-25 计算；由于当前 3 条任务的 `due_date` 均未设置，本次结果均为 `N/A`。

| Task Name | Associated Component | Assignee(s) | Priority | Status | Start Date | Due Date | Days Until Due | Key Deliverable | Task Help Link |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| i need webhook agent access the opencti platform with a http node in the workflow instead of the current seperate opencti mcp. | WEBHOOK_AGENT（1277）；ai4sec_threat_modeling_agent（1436）；ai4sec_opencti_mcp（1215）；OpenCTI Runtime Stack（1276） | llm | Low | **Active** | 2026-3-18 | 未设置 | N/A | 将 webhook 工作流改为在工作流内通过 HTTP 节点直连 OpenCTI GraphQL，并以 1436 现有直连路径为基线保持最小字段和最小关系深度。交付重点是解除该工作流对外部 MCP `/query` 的运行时依赖，同时保持现有下游投影合同兼容。 | [2026-3-18_i_need_webhook_agent_access_the_opencti_platform_with_a_http_node_in_the_workflow_instead_of_the_current_seperate_opencti_mcp.md](taskhelpinfos/2026-3-18_i_need_webhook_agent_access_the_opencti_platform_with_a_http_node_in_the_workflow_instead_of_the_current_seperate_opencti_mcp.md) |
| i need that the webhook agent analyzes the infrastrctures related with the notified vulurability pushed from opencti to give out the the impact on our product, and the risk score. | WEBHOOK_AGENT（1277）；BusinessLayer（1208）；业务上下文归并（1242）；威胁与影响研判（1243）；控制缺口与处置建议生成（1244） | llm | Low | **Active** | 2026-3-18 | 未设置 | N/A | 交付漏洞 webhook 的企业化影响分析结果，基于一跳关联对象输出影响范围、优先级建议、决策摘要与情境化风险评分。实现需遵循任务给定的 1-100 评分公式、分档阈值和缺失项降级规则，并避免扩展到自动通知协同。 | [2026-3-18_i_need_that_the_webhook_agent_analyzes_the_infrastrctures_related_with_the_notified_vulurability_pushed_from_opencti_to_give_out_the_the_impact_on_our_product_and_the_risk_score.md](taskhelpinfos/2026-3-18_i_need_that_the_webhook_agent_analyzes_the_infrastrctures_related_with_the_notified_vulurability_pushed_from_opencti_to_give_out_the_the_impact_on_our_product_and_the_risk_score.md) |
| add a new llm node responsible for summarize the current structure outpu into a graph and several tables | ai4sec_threat_modeling_agent（1436）；VS1-E2E_持续安全交付闭环_端到端用户故事（1223）；业务流程中所有数据都必须是OPENCTI平台中的STIX2.1标准数据（1226） | llm | Low | **Active** | 2026-3-18 | 未设置 | N/A | 在 VS1 独立威胁建模工作流主分析节点之后增加图表摘要 LLM 节点，输出 Mermaid 最小关系图和按实体类型分组的 Markdown 表格。图表只在会话中展示，不进入当前 JSON 下载文件，并对缺失的 `indicator` / `attack path` 做自然降级。 | [2026-3-18_add_a_new_llm_node_responsible_for_summarize_the_current_structure_outpu_into_a_graph_and_several_tables.md](taskhelpinfos/2026-3-18_add_a_new_llm_node_responsible_for_summarize_the_current_structure_outpu_into_a_graph_and_several_tables.md) |

## 汇总

### 按状态统计

- Active：3

### 按优先级统计

- Low：3

### 按负责人统计

- llm：3

### 7 天内到期任务（关键紧急）

- 无。当前 3 项任务的 `due_date` 均为占位值 `1899-12-30`，按“未设置”处理。

### 无负责人任务

- 无