# 任务执行简报

- 任务名称：ApplicationLayer
- 任务类型：ToDo
- 当前状态：Active
- 负责人：llm
- 优先级：Low
- 起止时间：2026-3-13 至 2026-3-13
- 关联架构对象名称与 ID：ApplicationLayer（1209）、StrategyLayerAndMotivationAspect（1207）、BusinessLayer（1208）、VS1-E2E_持续安全交付闭环_端到端用户故事（1223）、VS2-E2E_威胁运营与响应闭环_端到端用户故事（1225）、VS3-E2E_动态知识进化闭环_端到端用户故事（1222）、VS4-E2E_环境感知监控闭环_端到端用户故事（1224）、ai4sec_agent（1214）、ai4sec_opencti_mcp（1215）、OpenCTI platform（1216）、Notification MCP（1227）、情报分析师（1231）、业务负责人（1232）、安全负责人（1233）、管理层（1234）、安全运营团队（1235）

## 1. LLM执行摘要

- 需要输出应用层架构设计文档，目标文件为 `design/applicationlayer/AI4sec应用层架构设计.md`。
- 首要修改对象是应用层设计文档本身；当前 `design/applicationlayer` 目录为空，默认需要新建文档。
- 应用层主链路必须围绕 `ai4sec_agent`（1214）、`ai4sec_opencti_mcp`（1215）、`OpenCTI platform`（1216）和 `Notification MCP`（1227）展开。
- 消费者角色命名不得自创新名，必须沿用业务层角色：情报分析师（1231）、业务负责人（1232）、安全负责人（1233）、管理层（1234）、安全运营团队（1235）。
- 文档必须体现 Progressive Disclosure 与 Separation of Concerns，并把它们落实为信息分层和模块边界，而不是停留在口号。
- 接口契约需要下沉到 API 级别，至少覆盖接口目录、调用双方、认证方式、关键请求响应字段、异步消息体、错误语义、版本策略。
- 四条价值流都要覆盖，且每条主链路的完整七段式接口契约样板按任务要求统一选用 VS4 视角展开。
- 通知通道明确不做权限控制设计，但仍需补齐最小通知合同、模板类型、收件人分层和升级矩阵边界。
- `DifyAgentWorkflow`、`mcp/opencti_mcp`、`mcp/notification_mcp` 目录当前均为空，代码级文件落点无法从现状确认，超出本文档交付范围的实现细节需避免臆造。
- 最关键验收条件是：文档能把角色入口、UI IA、Agent 工作流、API 契约、异步回调、通知合同和价值流映射放到同一应用层叙事里，且不越界到部署、SMTP 或 RBAC 实现。

## 2. 已确认事实

- `ApplicationLayer`（1209）是当前任务关联的顶层应用层架构对象，且其 `project_info.tasks` 中存在本任务，状态为 `Active`。
- `ApplicationLayer` 视图（164）包含 `DIFY`（1212）、`SKILL`（1213）、`ai4sec_agent`（1214）、`ai4sec_opencti_mcp`（1215）、`OpenCTI platform`（1216）、`外部信息爬取AGENT`（1217）、`外部网站`（1218）、`情报分析师`（1219）、`各类情报消费者`（1220）、`Notification MCP`（1227）。
- 关系 `1082` 已确认 `ai4sec_agent`（1214）访问 `ai4sec_opencti_mcp`（1215）获取 OpenCTI STIX 数据。
- 关系 `1083` 已确认 `ai4sec_opencti_mcp`（1215）访问 `OpenCTI platform`（1216）获取情报数据。
- 关系 `1086` 已确认 `OpenCTI platform`（1216）主动向 `ai4sec_agent`（1214）推送 STIX Bundle 情报信息。
- 关系 `1088` 已确认 `各类情报消费者`（1220）通过 `ai4sec_agent`（1214）消费情报。
- 关系 `1089` 已确认 `ai4sec_agent`（1214）向 `Notification MCP`（1227）发送预警通知。
- 原则 `1226` 要求业务流程中所有数据都必须转化为 OpenCTI 中的 STIX 2.1 标准数据后再流转。
- 原则 `1228` 要求外部情报平台只能先对接内部 OpenCTI，推送到 Dify Agent 的情报来自内部 OpenCTI。
- 原则 `1229` 要求 Dify Agent 既承担主动交互入口，也承担被动事件驱动下的统一调度入口。
- 原则 `1230` 要求高级别预警统一交由 `Notification MCP`（1227）承担送达。
- 业务层已确认正式角色为 情报分析师（1231）、业务负责人（1232）、安全负责人（1233）、管理层（1234）、安全运营团队（1235）。

## 3. 需人工确认 / 未知项

- 现有 `design/applicationlayer/AI4sec应用层架构设计.md` 是否已有历史版本，KG 未提供。
- 需要复用的 Dify 工作流 YAML、MCP 接口定义或通知模板源码文件，当前目录为空，需结合代码仓进一步定位或后续补建。
- API 认证方式在任务说明中要求写入契约，但 KG 未提供现有认证机制或身份边界，需人工确认。
- OpenCTI GraphQL 查询限流的具体配额、退避参数和缓存失效策略未在 KG 中给出，只能写调用方可见合同边界。
- `ai4sec_opencti_mcp` 的字段投影参数与失败码在任务说明中给出了建议合同，但未确认代码现状已实现到何种程度，需人工确认。
- Notification MCP 的模板字段默认值、升级矩阵阈值和收件人映射是否已有现成配置文件，KG 未确认。

## 4. 约束与边界

- 必须遵守原则：Progressive Disclosure、Separation of Concerns、业务流程中所有数据都必须是 OPENCTI 平台中的 STIX2.1 标准数据（1226）、全局情报底座：OPENCTI 平台（1228）、统一智能入口：DIFY Agent（1229）、通知预警标准化通道（1230）。
- 必须保持不变的边界：OpenCTI 仍是全局情报底座；Dify Agent 仍是统一智能入口；Notification MCP 仍是预警通知统一出口。
- 禁止把外部情报源直接设计为调用 `ai4sec_agent` 的主入口；外部输入必须先落到 OpenCTI，再由内部事件或任务触发 Agent。
- 禁止把通知权限控制、组织架构同步、SMTP 配置、Webhook 代码实现、缓存结构、限流算法等实现细节写进应用层设计正文。
- Progressive Disclosure 落地要求：文档需按“角色入口与场景导航 -> 应用服务与交互流 -> API/事件契约 -> 非功能约束”逐层展开，避免在首页直接堆叠底层字段细节。
- Separation of Concerns 落地要求：UI IA、Agent 工作流、MCP 查询投影、OpenCTI 底座职责、通知合同边界分别成段描述，不得把业务角色、技术组件和部署实现混写。

## 5. 架构元素级任务拆解

| 子任务名称 | 对应架构元素 | 技术目的 | 与其他子任务的依赖关系 |
| --- | --- | --- | --- |
| 梳理应用层边界与角色入口 | ApplicationLayer（1209）、情报分析师（1231）、业务负责人（1232）、安全负责人（1233）、管理层（1234）、安全运营团队（1235） | 定义统一壳层、角色工作台、场景中心与角色默认落点 | 先于 UI IA、API 契约和通知合同章节 |
| 整理应用层主交互链路 | ai4sec_agent（1214）、ai4sec_opencti_mcp（1215）、OpenCTI platform（1216）、Notification MCP（1227） | 固化应用层核心组件职责、调用方向和异步入口分组 | 依赖已确认事实与视图 164 关系 |
| 映射四条价值流到应用层 | VS1（1223）、VS2（1225）、VS3（1222）、VS4（1224） | 把价值流转成场景中心、主链路样板和共享能力分组 | 依赖角色入口与交互链路定义 |
| 编写 API 与事件契约 | ai4sec_agent（1214）、ai4sec_opencti_mcp（1215）、OpenCTI platform（1216） | 输出共享域与场景域接口目录、异步回调、错误码与版本策略 | 依赖四条价值流映射与组件职责 |
| 编写通知合同 | Notification MCP（1227）、通知预警标准化通道（1230） | 定义模板类型、收件人分层、升级矩阵与幂等边界 | 依赖角色映射与高风险链路说明 |
| 形成最终应用层文档 | ApplicationLayer（1209） | 将以上内容沉淀为可快速理解的 Markdown 文档 | 依赖全部前置子任务完成 |

## 6. 推荐实施顺序

1. 动作说明：建立文档骨架，按角色入口、场景中心、应用服务、契约、通知合同、约束与附录分节。目标文件 / 模块 / 目录：`design/applicationlayer/AI4sec应用层架构设计.md`。对应架构元素 ID：1209。完成判定标准：文档结构能承载 Progressive Disclosure，且无实现细节章节越界。
2. 动作说明：从视图 164 和关系 1082、1083、1086、1088、1089 提炼应用层核心交互。目标文件 / 模块 / 目录：`design/applicationlayer/AI4sec应用层架构设计.md`。对应架构元素 ID：1214、1215、1216、1227。完成判定标准：组件职责、调用链路、异步回调分组和通知出口边界写清。
3. 动作说明：把业务层正式角色映射到 Dify UI 的统一壳层、角色工作台和场景中心。目标文件 / 模块 / 目录：`design/applicationlayer/AI4sec应用层架构设计.md`。对应架构元素 ID：1231、1232、1233、1234、1235。完成判定标准：角色命名完全沿用业务层，且每类角色的默认入口、可见卡片和审批动作明确。
4. 动作说明：将 VS1 至 VS4 映射到共享 API 域、场景 API 域、Webhook 分组与 Agent 工作流入口。目标文件 / 模块 / 目录：`design/applicationlayer/AI4sec应用层架构设计.md`。对应架构元素 ID：1223、1225、1222、1224。完成判定标准：四条价值流均有应用层落点，且 VS4 主链路被写成完整七段式样板。
5. 动作说明：补齐 `ai4sec_opencti_mcp` 的字段投影、分页约束、错误语义和 OpenCTI 查询边界。目标文件 / 模块 / 目录：`design/applicationlayer/AI4sec应用层架构设计.md`。对应架构元素 ID：1215、1216、1226、1228。完成判定标准：契约只写调用方可见行为，不下沉到缓存结构或 GraphQL 实现细节。
6. 动作说明：补齐 Notification MCP 的模板类型、角色映射字段、升级矩阵和去重合同。目标文件 / 模块 / 目录：`design/applicationlayer/AI4sec应用层架构设计.md`。对应架构元素 ID：1227、1230。完成判定标准：明确说明不做权限控制设计，但通知边界和最小合同完整。
7. 动作说明：复核文档中的角色命名、STIX 语义、错误码、版本策略与边界声明。目标文件 / 模块 / 目录：`design/applicationlayer/AI4sec应用层架构设计.md`。对应架构元素 ID：1209、1226、1228、1229、1230。完成判定标准：无角色命名偏差、无外部直连 Agent 的错误表达、无 RBAC/SMTP 实现越界。

## 7. 建议修改目标

- 优先检查的文件：`design/tasks/taskandissues_for_LLM.md`、`design/KG/SystemArchitecture.json`、`design/businesslayer/AI4SEC业务层架构设计.md`、`design/userstories/value_stream_aligned/VS1-E2E_威胁建模_端到端用户故事.md`、`design/userstories/value_stream_aligned/VS2-E2E_威胁运营与响应闭环_端到端用户故事.md`、`design/userstories/value_stream_aligned/VS3-E2E_动态知识进化闭环_端到端用户故事.md`、`design/userstories/value_stream_aligned/VS4-E2E_环境感知监控闭环_端到端用户故事.md`
- 可能需要新增的文件：`design/applicationlayer/AI4sec应用层架构设计.md`
- 可能需要避免修改的文件：`external_opencti/docker-compose.dev.yml`、`config/opencti_webhook_signal_template.ejs`、`SystemArchitecture.json` 本体

## 8. 交付物与验收标准

- [ ] 已生成 `design/applicationlayer/AI4sec应用层架构设计.md`
- [ ] 文档明确给出统一壳层、角色工作台、场景中心和页面级 IA
- [ ] 文档对 VS1 至 VS4 均给出应用层映射
- [ ] 文档给出共享域 API 与场景域 API 的目录分组
- [ ] 文档给出同步接口与异步事件的七段式契约样板
- [ ] 文档明确 `ai4sec_opencti_mcp` 的投影、分页、错误语义合同边界
- [ ] 文档明确 Notification MCP 的模板类型、角色映射、升级矩阵与幂等约束
- [ ] 文档显式落实 Progressive Disclosure 与 Separation of Concerns
- [ ] 文档没有下沉到 RBAC、SMTP、缓存结构、限流算法或部署实现

## 9. 风险、阻塞与缓解措施

| 风险 / 阻塞 | 类型 | 影响 | 缓解措施 |
| --- | --- | --- | --- |
| 任务说明非常细，但代码目录为空 | 信息缺口 | 容易把实现猜测写进设计文档 | 严格以契约边界表达，不臆造现有实现文件 |
| 角色命名与消费者入口容易混用旧称谓 | 一致性风险 | 文档与业务层不一致 | 全文只使用业务层正式角色名称 |
| API 契约可能越界到实现细节 | 设计边界风险 | 破坏关注点分离 | 只描述调用方可见字段、错误语义、版本策略和重试语义 |
| 通知通道容易被误写为权限设计 | 范围风险 | 偏离任务要求 | 保留“无权限控制设计”声明，仅输出最小通知合同 |
| 提示词中日期与当前会话日期不一致 | 管理信息风险 | 影响到期计算和报告口径 | 在汇总文件中显式声明按当前会话日期 2026-03-13 计算 |

## 10. 下一步建议

- 先创建应用层设计文档骨架并锁定章节顺序。
- 再补充视图 164 的组件职责和四条价值流映射。
- 最后集中编写 API 契约、通知合同与验收清单，避免中途反复改结构。