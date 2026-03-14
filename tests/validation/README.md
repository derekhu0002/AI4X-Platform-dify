# AI4SEC 业务层人工验收测试集

## 1. 文档目的

本目录用于存放业务层人工验收测试文档，与 `tests/unit`、`tests/integration`、`tests/e2e` 下的自动化测试资产分离管理。

本测试集面向真实系统验收，覆盖 `BusinessLayer`（1208）定义的核心 capability，并围绕 VS1、VS2、VS3、VS4 四条价值流组织执行。

## 2. 执行边界

- Dify 入口：`http://localhost/apps`
- OpenCTI 入口：`http://localhost:8080/dashboard`
- OpenCTI 测试数据导入方式：使用平台导入功能导入 STIX Bundle 文件
- Notification MCP 验收方式：观察系统是否触发通知动作，邮件是否实际送达仅记录现象，不要求 mock 收件箱
- 业务负责人、安全负责人、管理层、安全运营团队共用一个测试账号，占位符统一写为 `ROLE_SHARED_ACCOUNT`
- 情报分析师测试账号占位符写为 `ANALYST_ACCOUNT`
- 当前任务若发现业务层设计与现网能力不一致，必须记录为“现网差距”，不在本任务内补实现

## 3. 执行顺序

1. 阅读 [00-virtual-test-data.md](./00-virtual-test-data.md)，准备 4 组价值流测试数据。
2. 使用 [00-capability-summary.md](./00-capability-summary.md) 选择本轮要执行的 capability 文档。
3. 按 capability 文档逐项执行人工验收。
4. 使用 [00-acceptance-record-template.md](./00-acceptance-record-template.md) 记录现场结果。
5. 汇总每条 capability 的通过/不通过结论与现网差距。

## 4. 文档清单

| 文档 | 用途 |
| --- | --- |
| `00-capability-summary.md` | capability 汇总表与文档索引 |
| `00-virtual-test-data.md` | 四条价值流的虚拟测试数据与 STIX Bundle 说明 |
| `00-acceptance-record-template.md` | 人工验收记录模板 |
| `01-情报任务受理与分流.md` | capability 测试用例 |
| `02-业务上下文归并.md` | capability 测试用例 |
| `03-威胁与影响研判.md` | capability 测试用例 |
| `04-控制缺口与处置建议生成.md` | capability 测试用例 |
| `05-事件升级与动作编排.md` | capability 测试用例 |
| `06-通知与决策协同.md` | capability 测试用例 |
| `07-证据链与知识资产沉淀.md` | capability 测试用例 |
| `08-监控与规则持续校准.md` | capability 测试用例 |
| `09-角色责任治理.md` | capability 测试用例 |
| `10-业务绩效度量.md` | capability 测试用例 |

## 5. 统一判定规则

- 通过：步骤可在既有系统入口内完成，结果满足 capability 目标且证据可在 Dify 或 OpenCTI 中核验。
- 不通过：关键步骤无法执行，或者关键结果缺失、错误、不可追溯。
- 有条件通过：主路径可执行，但存在不阻断本轮 capability 验收的轻微偏差；必须在差距栏说明。
- 现网差距：业务层设计要求存在，但现网未提供对应能力、入口、字段或协同动作；记录差距，不要求补实现。