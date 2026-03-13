# 任务执行简报

- 任务名称：ApplicationLayer
- 任务类型：ToDo
- 当前状态：Active
- 负责人：llm
- 优先级：Low
- 起止时间：2026-3-14 至 2026-3-14
- 关联架构对象名称与 ID：ApplicationLayer（1209）、TechnologyLayer（1210）、DIFY（1212）、SKILL（1213）、ai4sec_agent（1214）、ai4sec_opencti_mcp（1215）、OpenCTI platform（1216）、Notification MCP（1227）、VS1（1223）、VS2（1225）、VS3（1222）、VS4（1224）、原则 1226/1228/1229/1230

## 1. LLM执行摘要

- 当前任务是按 ApplicationLayer（1209）与 TechnologyLayer（1210）的设计说明，交付可导入 DIFY 的 YAML/DSL、两个 FastAPI MCP 服务、OpenCTI webhook 联动能力以及完整多层自动化测试基线。
- 首要修改对象是 DIFY 工作流资产与 ai4sec_agent（1214）编排资产，其次是 ai4sec_opencti_mcp（1215）与 Notification MCP（1227）。
- 任务边界必须保持在应用层编排、MCP 服务、OpenCTI 接入合同、通知合同、测试与 CI 基线；不要把工作扩展成新的部署拓扑或底层数据库实现改造。
- 所有业务流转数据必须遵守 STIX 2.1 原则（1226），Agent 不能绕过 ai4sec_opencti_mcp（1215）直接耦合 OpenCTI 底层实现。
- OpenCTI 是唯一内部情报底座（1228），外部情报不得直接驱动业务流，而应经 OpenCTI 再由 webhook 或任务触发到 ai4sec_agent（1214）。
- DIFY Agent 是统一智能入口（1229），主动交互与被动 webhook 调度都要统一收敛到 ai4sec_agent（1214）与 DIFY（1212）的工作流入口。
- 高级别通知必须统一经过 Notification MCP（1227/1230），且要保留静态正式收件人、抄送、多模板和升级矩阵的运行时配置能力。
- 关键验收条件包括：DifyAgentWorkflow 目录输出可导入 YAML、两个 MCP 使用 FastAPI/Python、OpenCTI webhook 可直接联动、测试覆盖单元/契约/集成/E2E 四层。
- 主要风险是当前 KG 未给出仓内确切实现文件、测试框架定型方案、CI 目录与 DIFY DSL 具体文件名，这些需要结合代码仓进一步定位。
- 若发现当前仓内不存在承载测试或 CI 的架构元素，应显式按“需新增架构元素”处理，而不是隐式扩展职责边界。

## 2. 已确认事实

- ApplicationLayer（1209）的应用层目标是让业务角色通过 DIFY（1212）高效消费情报、执行决策、触发编排，并保持 STIX 2.1 语义一致性。
- ApplicationLayer（1209）明确核心组件为 DIFY（1212）、ai4sec_agent（1214）、ai4sec_opencti_mcp（1215）、OpenCTI platform（1216）、Notification MCP（1227）。
- 视图 164 包含元素 1212、1213、1214、1215、1216、1217、1218、1219、1220、1227，以及关系 1079 至 1089。
- 关系 1082 确认 ai4sec_agent（1214）通过 ai4sec_opencti_mcp（1215）访问 OpenCTI STIX 数据。
- 关系 1083 确认 ai4sec_opencti_mcp（1215）是访问 OpenCTI platform（1216）的统一入口。
- 关系 1086 确认 OpenCTI platform（1216）会主动向 ai4sec_agent（1214）推送 STIX BUNDLE 情报信息。
- 关系 1089 确认 ai4sec_agent（1214）向 Notification MCP（1227）发送预警通知。
- ai4sec_agent（1214）的 `code_paths` 已在 KG 中定义为 `DifyAgentWorkflow`，且包含接收 OpenCTI 推送的路由 `POST /webhooks/opencti/threat-intelligence`。
- ai4sec_opencti_mcp（1215）的 `code_paths` 已在 KG 中定义为 `mcp\\opencti_mcp`。
- Notification MCP（1227）的 `code_paths` 已在 KG 中定义为 `mcp\\notification_mcp`。
- Principle 1226 要求所有业务流程数据都必须转化为 OpenCTI 平台中的 STIX 2.1 标准数据。
- Principle 1228 要求所有推送到 DIFY Agent 的情报来自内部 OpenCTI，且通过 OpenCTI webhook 模板推送。
- Principle 1229 要求主动交互和被动流转都统一由 DIFY Agent（ai4sec_agent）承担入口与调度。
- Principle 1230 要求最终高级别预警统一交由 Notification MCP 负责发送。
- TechnologyLayer（1210）确认当前目标运行形态为单机开发测试环境，本地 Docker 容器承载 Dify、MCP 与 OpenCTI 组件。

## 3. 需人工确认 / 未知项

- DifyAgentWorkflow 下最终需要交付的一条统一 Workflow/Chatflow DSL 的确切文件名、目录层级与资源拆分方式未知。
- SKILL（1213）的仓内实现位置与具体能力边界未知，需结合代码仓确认是否已有可复用实现。
- ai4sec_opencti_mcp（1215）当前已实现的查询/写回接口范围、投影参数结构、异常模型与契约样例未知。
- Notification MCP（1227）当前是否已有模板、多收件人、抄送、升级矩阵和配置装载能力未知。
- OpenCTI webhook 到 Dify “当前不需要鉴权”是任务输入要求，但具体由哪一层负责放开校验、是否已有现成配置项，KG 未确认。
- 自动化测试框架、契约测试样例承载目录、E2E 驱动方式与 CI 工作流文件位置未知。
- 当前代码仓是否已存在针对 DIFY DSL 的导入校验脚本、schema 校验器或导出辅助工具未知。
- Notification MCP 正式收件人静态配置项的实际落点文件未知；仅可确认该能力必须存在。

## 4. 约束与边界

- 必须遵守 Principle 1226：所有读写与通知引用的业务数据都要以 STIX 2.1 对象或其业务投影表达，禁止引入脱离 STIX 的主业务对象格式。
- 必须遵守 Principle 1228：外部情报先进入 OpenCTI（1216），再由 webhook 或任务驱动 ai4sec_agent（1214）；禁止让外部源直接驱动业务工作流核心逻辑。
- 必须遵守 Principle 1229：DIFY/ai4sec_agent 是统一智能入口；禁止把业务编排分散到 MCP 或 OpenCTI 侧实现。
- 必须遵守 Principle 1230：高等级通知统一走 Notification MCP（1227）；禁止由 Agent 或其他组件直接硬编码发信替代标准化通道。
- Progressive Disclosure 强制要求：交付实现应按入口菜单/意图识别、场景编排、MCP 查询投影、通知输出、测试验证逐层展开，避免一次性暴露底层实现细节给上层调用方。
- Separation of Concerns 强制要求：DIFY DSL、Agent 工具编排、OpenCTI 数据投影、Notification 发送、测试/CI 基线必须分层实现，禁止把数据访问、通知投递和业务推理混写到同一组件。
- 必须保持不变的边界：OpenCTI（1216）仍是事实底座，ai4sec_opencti_mcp（1215）仍是数据访问面，Notification MCP（1227）仍是通知出口，TechnologyLayer（1210）仍是单机 Docker 开发测试形态。
- 明确禁止的实现方式：禁止把最终工作流资产交付为非 YAML/DSL 形态；禁止在任务范围内扩展 RBAC、底层 DB 结构、缓存算法或 GraphQL 底层实现；禁止绕过 webhook 信号回查模式直接假设 OpenCTI 推送全量对象。

## 5. 架构元素级任务拆解

| 子任务名称 | 对应架构元素 | 技术目的 | 与其他子任务的依赖关系 |
| --- | --- | --- | --- |
| 统一 DIFY 入口与场景分流 | DIFY（1212）、ai4sec_agent（1214）、VS1/VS2/VS3/VS4（1223/1225/1222/1224） | 交付一条可导入 DIFY 的统一 YAML/DSL，通过入口菜单和意图识别路由到四条价值流场景 | 依赖 OpenCTI 查询合同与通知合同定义完成 |
| 固化 Agent 工具与 webhook 编排 | ai4sec_agent（1214）、SKILL（1213）、OpenCTI platform（1216） | 让 Agent 正确消费 OpenCTI webhook 信号、回查对象、调用 SKILL 与 MCP | 依赖 ai4sec_opencti_mcp（1215）接口可用 |
| 实现 OpenCTI MCP 数据访问层 | ai4sec_opencti_mcp（1215）、OpenCTI platform（1216）、原则 1226/1228 | 提供 STIX 投影查询、写回与错误语义基线，保证 Agent 不直接耦合 OpenCTI 底层 | 被 Agent 编排与测试基线依赖 |
| 实现通知标准化通道 | Notification MCP（1227）、原则 1230、业务角色 1232/1233/1234/1235 | 支持正式收件人、抄送、升级矩阵、多模板与幂等通知投递 | 依赖 Agent 产出标准通知载荷 |
| 对齐 OpenCTI 信号模板与回查链路 | OpenCTI platform（1216）、ai4sec_agent（1214）、原则 1228 | 确保 OpenCTI webhook 模板仅传信号并支持 Agent 回查完整 STIX 对象 | 依赖 MCP 查询能力与 webhook 路由定义 |
| 建立自动化测试与 CI 基线 | ApplicationLayer（1209）、TechnologyLayer（1210）、需新增架构元素：测试基线/CI 流水线 | 覆盖单元、契约、集成、E2E 四层验证，并形成可重复执行基线 | 依赖前述编排、MCP 与通知能力基本成型 |

## 6. 推荐实施顺序

1. 动作说明：确认仓内 DIFY DSL、Agent、两个 MCP 的现有代码落点与空白区域。目标文件 / 模块 / 目录：`DifyAgentWorkflow`、`mcp/opencti_mcp`、`mcp/notification_mcp`、`external_opencti`、`externalDify`。对应架构元素 ID：1214、1215、1216、1227、1212。完成判定标准：能够定位各组件现状、入口文件与缺失实现；若无法确认具体文件，标记“需结合代码仓进一步定位”。
2. 动作说明：先定义并落地 ai4sec_opencti_mcp 的查询/写回合同、投影档位、错误语义和 FastAPI 入口。目标文件 / 模块 / 目录：`mcp/opencti_mcp`。对应架构元素 ID：1215、1216、1226、1228。完成判定标准：Agent 可通过 MCP 访问 OpenCTI，且接口输入输出满足 STIX 投影边界。
3. 动作说明：实现 Notification MCP 的模板、接收人映射、升级矩阵与运行时配置装载。目标文件 / 模块 / 目录：`mcp/notification_mcp`。对应架构元素 ID：1227、1230。完成判定标准：可按模板类型生成通知并支持正式收件人、抄送、升级与幂等字段。
4. 动作说明：在 ai4sec_agent 与 DIFY DSL 中实现统一入口、四场景分流、intent 路由、webhook 接入与 MCP/通知调用。目标文件 / 模块 / 目录：`DifyAgentWorkflow`，其余文件需结合代码仓进一步定位。对应架构元素 ID：1212、1213、1214、1222、1223、1224、1225。完成判定标准：存在一条可导入 DIFY 的 YAML/DSL 主流程，能够根据菜单或意图进入对应价值流。
5. 动作说明：对齐 OpenCTI webhook 信号模板与 Agent 回查逻辑，确保无鉴权联调链路可运行。目标文件 / 模块 / 目录：`external_opencti/opencti_webhook_signal_template.ejs`、Agent webhook 路由文件需结合代码仓进一步定位。对应架构元素 ID：1214、1216、1228。完成判定标准：OpenCTI 推送只携带信号数据，Agent 能基于对象 ID 完成回查。
6. 动作说明：补齐单元、契约、集成、E2E 四层测试与 CI 执行入口。目标文件 / 模块 / 目录：需结合代码仓进一步定位；如不存在测试目录或 CI 目录，则按“需新增架构元素：测试基线/CI 流水线”处理。对应架构元素 ID：1209、1210。完成判定标准：四层测试均有最小可运行样例，CI 能稳定执行至少核心路径。

## 7. 建议修改目标

- 优先检查的文件：`external_opencti/opencti_webhook_signal_template.ejs`、`external_opencti/docker-compose.yml`、`externalDify/docker-compose.yaml`
- 优先检查的目录：`DifyAgentWorkflow`、`mcp/opencti_mcp`、`mcp/notification_mcp`
- 可能需要新增的文件：DIFY DSL YAML、FastAPI 路由/服务/配置模块、契约测试样例、集成测试夹具、E2E 驱动脚本、CI 工作流文件；具体路径需结合代码仓进一步定位
- 可能需要避免修改的文件：OpenCTI 与 Dify 第三方镜像生成产物、与当前任务无关的业务层/战略层设计文档、底层数据库或缓存实现文件

## 8. 交付物与验收标准

- [ ] 交付一条可直接导入 DIFY 的 YAML/DSL 主工作流，支持入口菜单选择流程，并支持意图识别自动分流。
- [ ] ai4sec_agent（1214）能够通过 webhook 和人机交互两种入口统一驱动场景流程。
- [ ] ai4sec_opencti_mcp（1215）以 FastAPI/Python 实现，并提供满足 STIX 2.1 原则的查询/写回能力。
- [ ] Notification MCP（1227）以 FastAPI/Python 实现，并支持正式收件人、抄送、升级矩阵、多模板和幂等字段。
- [ ] OpenCTI 到 Dify 的 webhook 联调链路可工作，且当前不要求鉴权。
- [ ] 自动化测试覆盖单元测试、契约测试、集成测试和端到端测试四层，并能说明各层目标与执行方式。
- [ ] 至少存在一条 CI 执行路径，能够自动运行核心测试集或校验核心交付物。
- [ ] 所有关键业务对象和通知引用均基于 STIX 2.1 或其业务投影，不出现主业务流中的脱轨数据格式。

## 9. 风险、阻塞与缓解措施

- 风险：KG 对仓内实际实现文件位置覆盖不完整。缓解措施：先做代码落点盘点，再按目录分层实施，无法确认处明确标注。
- 风险：DIFY YAML/DSL 的最终导入格式与当前仓内资产形态可能不一致。缓解措施：优先验证现有资产格式，必要时增加最小导入校验样例。
- 风险：Notification MCP 运行时配置能力与静态正式收件人要求可能存在冲突。缓解措施：用静态默认值 + 可覆盖运行时配置的双层策略。
- 风险：OpenCTI webhook 只推送信号对象，若 Agent 回查或缓存逻辑不稳会导致主链路失败。缓解措施：优先实现回查、缓存和错误兜底，再接入场景编排。
- 风险：四层测试与 CI 目前没有对应架构元素。缓解措施：按“需新增架构元素：测试基线/CI 流水线”记录，并以最小闭环方案先落地。
- 风险：单机 Docker 开发测试环境资源不足可能影响联调稳定性。缓解措施：遵循 TechnologyLayer（1210）的单机环境约束，先保证核心链路可用，再逐步扩展测试矩阵。