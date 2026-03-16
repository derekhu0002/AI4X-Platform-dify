# 任务清单

- 报告生成日期：2026-03-16
- 总任务数：3
- 状态分布：Active 3
- 优先级分布：Low 3
- 假设说明：
	- 任务行字段以 `design/tasks/taskandissues_for_LLM.md` 为主，缺失的 `start_date/due_date/assigned_to/priority` 由 `design/KG/SystemArchitecture.json` 的对应元素 `project_info.tasks` 回填。
	- `due_date=1899-12-30` 视为无效占位日期，因此 `Due Date` 与 `Days Until Due` 记为 `N/A`。
	- `Days Until Due` 按提示词指定基准日期 2026-02-25 计算；当前任务均无有效截止日，无法计算。

| Task Name | Associated Component | Assignee(s) | Priority | Status | Start Date | Due Date | Days Until Due | Key Deliverable | Task Help Link |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 全局情报底座：OPENCTI 平台 | 全局情报底座：OPENCTI 平台（1228） | llm | Low | **Active** | 2026-3-16 | N/A | N/A | 将 webhook ingress 回归到 `ai4sec_agent` 边界并下线 MCP 旧入口，形成“Agent 中转 webhook + 工作流调用”的可运行链路。交付 OpenCTI webhook 模板切换指引并保持 STIX Bundle 入参适配可用。 | [2026-3-16_全局情报底座_OPENCTI_平台.md](taskhelpinfos/2026-3-16_%E5%85%A8%E5%B1%80%E6%83%85%E6%8A%A5%E5%BA%95%E5%BA%A7_OPENCTI_%E5%B9%B3%E5%8F%B0.md) |
| 支持快速的情报生产和消费 | 支持快速的情报生产和消费（1221） | llm | Low | **Active** | 2026-3-16 | N/A | N/A | 将 Dify 工作流从路由能力扩展为“受理-查询-研判-写回-通知-反馈”闭环，并优先打通 VS4 主场景。反馈环节必须包含人工复核门控，确认后才写回关键对象。 | [2026-3-16_支持快速的情报生产和消费.md](taskhelpinfos/2026-3-16_%E6%94%AF%E6%8C%81%E5%BF%AB%E9%80%9F%E7%9A%84%E6%83%85%E6%8A%A5%E7%94%9F%E4%BA%A7%E5%92%8C%E6%B6%88%E8%B4%B9.md) |
| 业务流程中所有数据都必须是OPENCTI平台中的STIX2.1标准数据 | 业务流程中所有数据都必须是OPENCTI平台中的STIX2.1标准数据（1226） | llm | Low | **Active** | 2026-3-16 | N/A | N/A | 落地真实 OpenCTI 对象投影、Bundle 持久化与写回回查，确保 STIX-first 原则在运行时生效。建立独立最小字段矩阵配置并将 mock 收敛为本地合同兜底。 | [2026-3-16_业务流程中所有数据都必须是OPENCTI平台中的STIX2_1标准数据.md](taskhelpinfos/2026-3-16_%E4%B8%9A%E5%8A%A1%E6%B5%81%E7%A8%8B%E4%B8%AD%E6%89%80%E6%9C%89%E6%95%B0%E6%8D%AE%E9%83%BD%E5%BF%85%E9%A1%BB%E6%98%AFOPENCTI%E5%B9%B3%E5%8F%B0%E4%B8%AD%E7%9A%84STIX2_1%E6%A0%87%E5%87%86%E6%95%B0%E6%8D%AE.md) |

## 汇总

### 按状态统计

- Active：3

### 按优先级统计

- Low：3

### 按负责人统计

- llm：3

### 7 天内到期任务（关键紧急）

- 无（当前任务缺少有效截止日期，已标记 `N/A`）

### 无负责人任务

- 无