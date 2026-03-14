# BusinessLayer Capability 汇总表

## 1. 覆盖范围

本表覆盖 `BusinessLayer`（1208）在业务层设计中定义的 10 个二级通用 capability，并映射到 4 条价值流与独立测试文档。

| Capability | 一级能力域 | 关联价值流 | 关键 STIX 对象 | 主要参与账号 | 对应用例文档 |
| --- | --- | --- | --- | --- | --- |
| 情报任务受理与分流 | 情报接入与标准化 | VS1、VS2、VS3、VS4 | Task、Observed-Data、Vulnerability、Attack-Pattern | `ANALYST_ACCOUNT` | `01-情报任务受理与分流.md` |
| 业务上下文归并 | 情报接入与标准化 | VS1、VS3、VS4 | Software、Infrastructure、Identity、Relationship | `ANALYST_ACCOUNT`、`ROLE_SHARED_ACCOUNT` | `02-业务上下文归并.md` |
| 威胁与影响研判 | 情报研判与风险评估 | VS1、VS2、VS3 | Attack-Pattern、Incident、Vulnerability、Opinion | `ANALYST_ACCOUNT`、`ROLE_SHARED_ACCOUNT` | `03-威胁与影响研判.md` |
| 控制缺口与处置建议生成 | 情报研判与风险评估 | VS1、VS2、VS3 | Course-of-Action、Opinion、Note | `ANALYST_ACCOUNT`、`ROLE_SHARED_ACCOUNT` | `04-控制缺口与处置建议生成.md` |
| 事件升级与动作编排 | 响应协同与处置编排 | VS2、VS4 | Incident、Observed-Data、Course-of-Action、Indicator | `ROLE_SHARED_ACCOUNT` | `05-事件升级与动作编排.md` |
| 通知与决策协同 | 响应协同与处置编排 | VS1、VS2、VS3、VS4 | Note、Opinion、Indicator、Incident | `ROLE_SHARED_ACCOUNT` | `06-通知与决策协同.md` |
| 证据链与知识资产沉淀 | 知识沉淀与持续优化 | VS1、VS2、VS3、VS4 | Report、Relationship、Note、Observed-Data | `ANALYST_ACCOUNT`、`ROLE_SHARED_ACCOUNT` | `07-证据链与知识资产沉淀.md` |
| 监控与规则持续校准 | 知识沉淀与持续优化 | VS4、VS2 | Indicator、Attack-Pattern、Incident、Note | `ANALYST_ACCOUNT`、`ROLE_SHARED_ACCOUNT` | `08-监控与规则持续校准.md` |
| 角色责任治理 | 治理与绩效管理 | VS1、VS2、VS3、VS4 | Task、Note、Opinion | `ROLE_SHARED_ACCOUNT` | `09-角色责任治理.md` |
| 业务绩效度量 | 治理与绩效管理 | VS1、VS2、VS3、VS4 | Report、Note、Incident、Indicator | `ROLE_SHARED_ACCOUNT` | `10-业务绩效度量.md` |

## 2. 推荐执行批次

| 批次 | 推荐先后 | 目的 |
| --- | --- | --- |
| 批次 A | 01 -> 02 -> 03 -> 04 | 先验证输入标准化与研判输出是否闭环 |
| 批次 B | 05 -> 06 | 再验证动作编排、通知升级与决策协同 |
| 批次 C | 07 -> 08 | 最后验证知识沉淀和规则校准 |
| 批次 D | 09 -> 10 | 收尾验证治理、责任和指标可见性 |

## 3. 汇总结论表

测试人员执行完成后，可直接在下表填写整体结果。

| Capability | 结果（通过/不通过/有条件通过） | 主要证据位置 | 现网差距摘要 | 备注 |
| --- | --- | --- | --- | --- |
| 情报任务受理与分流 |  |  |  |  |
| 业务上下文归并 |  |  |  |  |
| 威胁与影响研判 |  |  |  |  |
| 控制缺口与处置建议生成 |  |  |  |  |
| 事件升级与动作编排 |  |  |  |  |
| 通知与决策协同 |  |  |  |  |
| 证据链与知识资产沉淀 |  |  |  |  |
| 监控与规则持续校准 |  |  |  |  |
| 角色责任治理 |  |  |  |  |
| 业务绩效度量 |  |  |  |  |