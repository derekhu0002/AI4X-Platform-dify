# 任务执行清单

**报告生成日期：** 2026-03-14

**概览：**
- 总任务数：1
- 状态分布：Active（1）
- 优先级分布：Low（1）

## 1. 任务列表

| Task Name | Associated Component | Assignee(s) | Priority | Status | Start Date | Due Date | Days Until Due | Key Deliverable | Task Help Link |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ApplicationLayer | ApplicationLayer（1209）；核心组件：DIFY（1212）、ai4sec_agent（1214）、ai4sec_opencti_mcp（1215）、OpenCTI platform（1216）、Notification MCP（1227） | llm | Low | Active | 2026-3-14 | 2026-3-14 | 0 | 按应用层与技术层架构交付可导入 DIFY 的统一 YAML/DSL 工作流、两个 FastAPI MCP 服务、OpenCTI webhook 联动能力，以及覆盖单元/契约/集成/E2E 的测试基线。 | [2026-3-14_ApplicationLayer.md](taskhelpinfos/2026-3-14_ApplicationLayer.md) |

## 2. 总结摘要

- 各状态任务数量：Active 1
- 各优先级任务数量：Low 1
- 各负责人任务数量：llm 1

**7 天内到期任务：**
- **ApplicationLayer：截止日期 2026-3-14，Days Until Due = 0**

**无负责人任务：**
- 无

**假设说明：**
- 已先生成并刷新 `implementation/taskhelpinfos` 下的任务支撑文件，再汇总任务总表。
- `design/tasks/taskandissues_for_LLM.md` 作为任务行与执行上下文主来源，`design/KG/SystemArchitecture.json` 作为架构元素、关系与任务字段回填主来源。
- 提示词内嵌的“current date: 2026-02-25”与当前会话日期不一致；本表按当前会话日期 2026-03-14 计算 `Days Until Due`。