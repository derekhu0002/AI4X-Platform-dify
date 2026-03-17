# 任务清单

- 报告生成日期：2026-03-17
- 总任务数：2
- 状态分布：Active 2
- 优先级分布：Low 2
- 假设说明：
  - 任务行字段以 `design/tasks/taskandissues_for_LLM.md` 为主，缺失的 `start_date`、`due_date`、`assigned_to`、`priority` 由 `design/KG/SystemArchitecture.json` 中元素 1215 的 `project_info.tasks` 回填。
  - `due_date=1899-12-30` 视为未设置的占位值，因此 `Due Date` 统一记为 `未设置`，`Days Until Due` 记为 `N/A`。
  - 任务支撑文件已按当前任务集生成，因此 `Task Help Link` 使用 `implementation/taskhelpinfos` 下的相对链接，不使用 `N/A`。

| Task Name | Associated Component | Assignee(s) | Priority | Status | Start Date | Due Date | Days Until Due | Key Deliverable | Task Help Link |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 将该MCP功模块替换成该工作流中的节点，所有功能通过节点来实现，不再使用该外部FASTAPI服务 | ai4sec_opencti_mcp（1215）；ai4sec_threat_modeling_agent（1436）；ai4sec_agent（1214）；OpenCTI Runtime Stack（1276） | llm | Low | **Active** | 2026-3-17 | 未设置 | N/A | 将 VS1 专用工作流从外部 `ai4sec_opencti_mcp` FastAPI 依赖迁移为工作流内节点实现，保持 OpenCTI 取数与后续威胁建模输入准备能力。交付重点是仅在 `ai4sec_threat_modeling_agent` 范围内完成替换，而不扩展到其他工作流或通知链路。 | [2026-3-17_将该MCP功模块替换成该工作流中的节点_所有功能通过节点来实现_不再使用该外部FASTAPI服务.md](taskhelpinfos/2026-3-17_将该MCP功模块替换成该工作流中的节点_所有功能通过节点来实现_不再使用该外部FASTAPI服务.md) |
| 在查询和匹配OPENCTI中的report时，我希望你不要把所有report都查询回来，而是用手中的report id作为参数去查。 | ai4sec_opencti_mcp（1215）；OpenCTI Runtime Stack（1276）；ApplicationLayer（1209）；ai4sec_threat_modeling_agent（1436） | llm | Low | **Active** | 2026-3-17 | 未设置 | N/A | 交付按 `report id` 优先、精确 `name` 次之的定向 report 查询能力，移除“先查全量 report 再匹配”的实现路径。兼容层仅保留本地测试 bundle report ID 到 live 标识的必要映射，并继续遵守现有投影与分页边界。 | [2026-3-17_在查询和匹配OPENCTI中的report时_我希望你不要把所有report都查询回来_而是用手中的report_id作为参数去查.md](taskhelpinfos/2026-3-17_在查询和匹配OPENCTI中的report时_我希望你不要把所有report都查询回来_而是用手中的report_id作为参数去查.md) |

## 汇总

### 按状态统计

- Active：2

### 按优先级统计

- Low：2

### 按负责人统计

- llm：2

### 7 天内到期任务（关键紧急）

- 无。当前两项任务的 `due_date` 均为占位值 `1899-12-30`，按“未设置”处理。

### 无负责人任务

- 无