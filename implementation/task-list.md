# 任务清单

- 报告生成日期：2026-03-17
- 总任务数：1
- 状态分布：Active 1
- 优先级分布：Low 1
- 假设说明：
  - 任务行字段以 `design/tasks/taskandissues_for_LLM.md` 为主，缺失的 `start_date`、`due_date`、`assigned_to`、`priority` 由 `design/KG/SystemArchitecture.json` 中元素 1260 的 `project_info.tasks` 回填。
  - `Days Until Due` 按提示词指定基准日期 2026-02-25 计算；当前任务 `due_date=2026-3-17`，因此剩余 20 天。

| Task Name | Associated Component | Assignee(s) | Priority | Status | Start Date | Due Date | Days Until Due | Key Deliverable | Task Help Link |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 威胁建模闭环流程 | 威胁建模闭环流程（1260）；ai4sec_threat_modeling_agent（1436）；ai4sec_opencti_mcp（1215）；OpenCTI Runtime Stack（1276）；Dify Runtime Stack（1275） | llm | Low | **Active** | 2026-3-17 | **2026-3-17** | **20** | 交付一个独立的 DIFY Workflow Agent，用于实现“威胁建模闭环流程001”对应的 VS1 场景，并完成“报告精确匹配优先、失败后双模糊匹配 -> 查询 OpenCTI -> 字段过滤 -> 威胁建模分析 -> 会话展示与 JSON 下载”的闭环。同步新增 VS1 衍生用户故事文件，不扩展到 OpenCTI 写回或 Notification MCP 完整通知分支。 | [2026-3-17_威胁建模闭环流程.md](taskhelpinfos/2026-3-17_%E5%A8%81%E8%83%81%E5%BB%BA%E6%A8%A1%E9%97%AD%E7%8E%AF%E6%B5%81%E7%A8%8B.md) |

## 汇总

### 按状态统计

- Active：1

### 按优先级统计

- Low：1

### 按负责人统计

- llm：1

### 7 天内到期任务（关键紧急）

- 无

### 无负责人任务

- 无