# 任务清单

- 报告生成日期：2026-03-19
- 总任务数：3
- 状态分布：Active 3
- 优先级分布：Low 3
- 假设说明：
  - 任务行字段以 `design/tasks/taskandissues_for_LLM.md` 为主；`start_date`、`due_date`、`assigned_to`、`priority` 由 `design/KG/SystemArchitecture.json` 中对象 1214、1215、1227 的 `project_info.tasks` 回填。
  - `due_date=1899-12-30` 在当前仓库视为未设置占位值，因此 `Due Date` 统一记为 `未设置`，`Days Until Due` 统一记为 `N/A`。
  - 已先生成当前任务集对应的支撑文件，因此 `Task Help Link` 使用 `implementation/taskhelpinfos` 下的相对链接；不存在 `N/A` 场景。
  - `Days Until Due` 按提示词给定基准日期 2026-02-25 计算；由于当前 3 条任务的 `due_date` 均未设置，本次结果均为 `N/A`。

| Task Name | Associated Component | Assignee(s) | Priority | Status | Start Date | Due Date | Days Until Due | Key Deliverable | Task Help Link |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ai4sec_agent | ai4sec_agent（1214）；ApplicationLayer（1209）；ai4sec_opencti_mcp（1215）；Notification MCP（1227） | llm | Low | **Active** | 2026-3-19 | 未设置 | N/A | 移除统一 Dify 工作流资产及其直接运行时入口，优先清理 `ai4sec_unified_workflow.yaml` 和统一入口专属调用面，并显式记录删除后不做历史重定向的能力缺口。 | [2026-3-19_ai4sec_agent.md](taskhelpinfos/2026-3-19_ai4sec_agent.md) |
| Notification MCP | Notification MCP（1227）；ApplicationLayer（1209）；TechnologyLayer（1210）；ai4sec_agent（1214） | llm | Low | **Active** | 2026-3-19 | 未设置 | N/A | 移除 Notification MCP 运行时服务与 API 调用链，清理 `NOTIFICATION_MCP_*` 配置残留，并将模板资产保留为单独评估范围，不在本任务内混做。 | [2026-3-19_Notification_MCP.md](taskhelpinfos/2026-3-19_Notification_MCP.md) |
| ai4sec_opencti_mcp | ai4sec_opencti_mcp（1215）；ApplicationLayer（1209）；TechnologyLayer（1210）；ai4sec_agent（1214） | llm | Low | **Active** | 2026-3-19 | 未设置 | N/A | 移除 OpenCTI MCP 兼容服务及相关代码，清理统一工作流对 `OPENCTI_MCP_URL` 的最后依赖，并保留“工作流已直连 OpenCTI”但架构文档尚未同步的显式缺口。 | [2026-3-19_ai4sec_opencti_mcp.md](taskhelpinfos/2026-3-19_ai4sec_opencti_mcp.md) |

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