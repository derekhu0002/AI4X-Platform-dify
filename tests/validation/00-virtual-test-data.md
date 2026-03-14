# 虚拟测试数据说明

## 1. 使用说明

本文件给出 4 条价值流对应的一组虚拟测试数据，供测试人员在 OpenCTI 中以 STIX Bundle 文件方式导入。文档目标是说明“需要准备什么数据”和“导入后应看到什么对象语义”，不要求在本任务内补写导入脚本。

## 2. 通用约束

- 所有对象使用 STIX 2.1 语义表达。
- 每条价值流至少准备 1 个 Bundle 文件。
- Bundle 文件命名建议采用 `vsX-<scenario>-bundle.json`。
- 实际数据文件已放置在 `tests/validation/test-data/` 目录下。
- 导入后需在 OpenCTI 中核验对象、关系和时间线是否可见。
- 为保持 STIX 2.1 标准，VS2 的“事件工单”测试数据使用 `Grouping` 和 `Report` 作为事件载体；VS4 的设计目标说明使用 `Note` 承载。

## 3. VS1 威胁建模数据集

| 项 | 内容 |
| --- | --- |
| 建议 Bundle 文件 | `vs1-payment-threat-model-bundle.json` |
| 文件位置 | `tests/validation/test-data/vs1-payment-threat-model-bundle.json` |
| 场景 | 支付域 `v2.8.0` 上线前威胁建模 |
| 关键对象 | `Software(payment-gateway)`、`Infrastructure(prod-payment-cluster)`、`Identity(payments-team)`、`Attack-Pattern(credential-stuffing)`、`Vulnerability(CVE-2026-1001)`、`Course-of-Action(enable-step-up-auth)`、`Opinion(strongly-disagree)` |
| 关键关系 | `Software -> Infrastructure (hosts)`、`Attack-Pattern -> Software (targets)`、`Course-of-Action -> Attack-Pattern (mitigates)` |
| 重点属性样例 | `Software.version=2.8.0`、`Infrastructure.environment=prod`、`Opinion.opinion=strongly-disagree` |
| 导入后核验点 | 支付相关资产、威胁模式、控制建议与发布判定能被同一任务链路追踪 |

## 4. VS2 威胁运营与响应数据集

| 项 | 内容 |
| --- | --- |
| 建议 Bundle 文件 | `vs2-lateral-movement-bundle.json` |
| 文件位置 | `tests/validation/test-data/vs2-lateral-movement-bundle.json` |
| 场景 | 横向移动告警进入响应闭环 |
| 关键对象 | `Observed-Data(observed=17)`、`Network-Traffic(host-A -> bastion-01)`、`Indicator(10.1.2.7)`、`Attack-Pattern(lateral-movement)`、`Grouping(possible-lateral-movement-case)`、`Course-of-Action(isolate-host-A)` |
| 关键关系 | `Indicator -> Attack-Pattern (indicates)`、`Grouping -> Observed-Data (related-to)`、`Course-of-Action -> Attack-Pattern (mitigates)` |
| 重点属性样例 | `Network-Traffic.protocols=["smb"]`、`Incident.severity=high`、`Course-of-Action.priority=P1` |
| 导入后核验点 | 告警证据、事件对象、处置动作与通知摘要可以串成闭环 |

## 5. VS3 动态知识进化数据集

| 项 | 内容 |
| --- | --- |
| 建议 Bundle 文件 | `vs3-zero-day-impact-bundle.json` |
| 文件位置 | `tests/validation/test-data/vs3-zero-day-impact-bundle.json` |
| 场景 | 外部零日转化为企业影响结论 |
| 关键对象 | `Vulnerability(CVE-2026-XXXX)`、`Report(0day-advisory)`、`Software(api-gateway)`、`Infrastructure(prod-edge-cluster)`、`Identity(finance-bu)`、`Opinion(prioritize-immediately)`、`Note(executive-summary)` |
| 关键关系 | `Vulnerability -> Software (affects)`、`Software -> Infrastructure (hosts)`、`Identity -> Infrastructure (owns)` |
| 重点属性样例 | `Vulnerability.cvss_score=9.8`、`Infrastructure.environment=prod`、`Identity.sector=finance` |
| 导入后核验点 | 受影响范围、业务关键度和管理层决策摘要可被同屏核验 |

## 6. VS4 环境感知监控数据集

| 项 | 内容 |
| --- | --- |
| 建议 Bundle 文件 | `vs4-bola-monitoring-bundle.json` |
| 文件位置 | `tests/validation/test-data/vs4-bola-monitoring-bundle.json` |
| 场景 | 设计期 BOLA 风险转化为运行期监控规则 |
| 关键对象 | `Attack-Pattern(BOLA)`、`Software(user-profile-service)`、`Indicator(bola-jwt-mismatch)`、`Infrastructure(prod-api-cluster)`、`Note(rule-rationale)` |
| 关键关系 | `Indicator -> Attack-Pattern (indicates)`、`Software -> Infrastructure (hosts)`、`Note -> Indicator (related-to)` |
| 重点属性样例 | `Indicator.pattern_type=sigma`、`Indicator.valid_from=2026-03-14T10:00:00Z` |
| 导入后核验点 | 规则来源、保护目标和命中解释可追溯到设计风险 |

## 7. 账号与占位符映射

| 占位符 | 含义 |
| --- | --- |
| `ANALYST_ACCOUNT` | 情报分析师测试账号 |
| `ROLE_SHARED_ACCOUNT` | 业务负责人、安全负责人、管理层、安全运营团队共用测试账号 |

## 8. 导入检查表

| 检查项 | 通过标准 |
| --- | --- |
| Bundle 导入成功 | OpenCTI 无格式错误或关键对象丢失 |
| 对象类型正确 | 每个场景的关键 STIX 对象都能检索到 |
| 关系可见 | 至少能看到设计中要求的一跳关系 |
| 业务语义可核验 | 对象名称、环境、优先级、结论与场景说明一致 |
| 可支持后续人工验收 | Dify 与 OpenCTI 页面能消费这些对象进行查询、分析、通知或回写 |