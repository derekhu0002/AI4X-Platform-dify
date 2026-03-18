# 任务执行简报

- 任务名称：i need webhook agent access the opencti platform with a http node in the workflow instead of the current seperate opencti mcp.
- 任务类型：ToDo
- 当前状态：Active
- 负责人：llm
- 优先级：Low
- 起止时间：2026-3-18 至 未设置
- 关联架构对象名称与 ID：WEBHOOK_AGENT（1277）；ai4sec_threat_modeling_agent（1436）；ai4sec_opencti_mcp（1215）；OpenCTI Runtime Stack（1276）；业务流程中所有数据都必须是OPENCTI平台中的STIX2.1标准数据（1226）；全局情报底座：OPENCTI 平台（1228）；统一智能入口：DIFY Agent (ai4sec_agent)（1229）

## 1. LLM执行摘要

- 当前任务要把 WEBHOOK_AGENT（1277）从调用外部 `ai4sec_opencti_mcp`（1215）改为在工作流内用 HTTP 节点直接访问 OpenCTI GraphQL。
- 首要修改对象是 `DifyAgentWorkflow/ai4sec_opencti_webhook_workflow.yaml`，其后才是为兼容返回合同做必要的轻量整理。
- 对齐基线必须采用 ai4sec_threat_modeling_agent（1436）现有的直连 GraphQL 路径、环境变量命名和最小查询语义。
- 不允许越界到统一 Agent、Notification MCP 或其他兼容路径；1215 只能解除该 webhook 工作流的运行时依赖，不能被默认删除或重写。
- 最关键验收条件是：Webhook 工作流不再依赖 `OPENCTI_MCP_URL` `/query`，但输出给下游的字段合同与当前兼容服务保持一致或差异被显式标注。
- 查询范围必须先收敛到最小字段集合和最小关系深度，只有 webhook 下游确有缺口时才允许补充字段。
- 认证注入方式优先复用 `OPENCTI_GRAPHQL_URL` 与 `OPENCTI_ADMIN_TOKEN`，若 webhook 工作流配置能力不足，需把差异写成实现假设。
- 超时、重试、错误码只能使用当前工作流实际可配置能力，不引入仓外补偿逻辑。
- 主要风险是 Dify HTTP 节点表达能力与现有 MCP 投影合同之间存在差距，可能需要在工作流内增加轻量格式转换节点。

## 2. 已确认事实

- WEBHOOK_AGENT（1277）是面向 OpenCTI 事件的 Dify webhook 工作流资产，代码路径已在 KG 中确认到 `DifyAgentWorkflow/ai4sec_opencti_webhook_workflow.yaml` 与 `DifyAgentWorkflow/tools/ai4sec_runtime_tools.py`。
- ai4sec_threat_modeling_agent（1436）已在 KG 中确认采用工作流内直连 OpenCTI GraphQL 的实现路径，代码路径为 `DifyAgentWorkflow/ai4sec_threat_modeling_workflow.yaml`。
- ai4sec_threat_modeling_agent（1436）的任务说明已明确：直连 OpenCTI 时使用 GraphQL 接口，并以 `OPENCTI_GRAPHQL_URL`、`OPENCTI_ADMIN_TOKEN` 作为命名基线。
- ai4sec_opencti_mcp（1215）仍是仓库内的兼容访问服务，KG 明确其在统一 Agent 和兼容场景中继续保留，不应因本任务被默认删除。
- OpenCTI Runtime Stack（1276）在 KG 中被定义为通过 GraphQL 接入、并通过仓库内 webhook 模板发出 lookup-required STIX bundle 通知的运行时底座。
- 原则 1226 要求业务流转中的数据保持 STIX 2.1 语义，不允许把非 STIX 业务结果直接替代 OpenCTI 事实源。
- 原则 1228 要求所有进入 Agent 的情报来自内部 OpenCTI 平台；原理上允许 webhook 工作流直接访问 OpenCTI，而不是绕过 OpenCTI 访问外部源。
- 原则 1229 要求 webhook 场景仍由 DIFY Agent 作为统一智能入口承接自动化调度。

## 3. 需人工确认 / 未知项

- 未知：Webhook 工作流最终需要复用 1436 的哪一组 GraphQL 查询片段与字段白名单。建议先按 1436 的最小查询集合落地，再仅对 webhook 响应缺失字段做增量补充。
- 未知：Dify HTTP 节点是否足以完整表达现有 MCP `/query` 的投影合同。建议默认把投影兼容逻辑保留在工作流内代码节点中，而不是重新引入外部服务。
- 未知：Webhook 场景对失败重试、超时和错误分级的具体阈值。建议先使用当前 YAML 已支持的默认 HTTP 节点配置，并在文档中把未配置项标为实现假设。
- 未知：是否需要同步调整 `external_opencti/opencti_webhook_signal_template.ejs` 的信号字段。建议仅在查询输入字段与现有 webhook 信号不兼容时再改，否则保持不变。
- 未知：工作流切换后，原有依赖 `OPENCTI_MCP_URL` 的部署说明是否需要同步更新。建议如仓内存在直接引用该环境变量的运行说明，再做最小文档修订；否则标记为需人工确认。

## 4. 约束与边界

- 必须遵守的 Principle / Constraint：1226、1228、1229；同时强制落实 Progressive Disclosure 与 Separation of Concerns。
- 必须保持不变的模块或边界：ai4sec_opencti_mcp（1215）的其他兼容路径；统一 Agent（1214）与 Notification MCP（1227）现有职责边界；OpenCTI Runtime Stack（1276）作为唯一内部情报底座。
- 明确禁止的实现方式或越界修改：禁止新增仓外 FastAPI 补偿层；禁止把 webhook 工作流改造成统一 Agent 主流程；禁止为本任务顺手删除 1215 或改写其他 workflow 的 OpenCTI 访问路径。
- Progressive Disclosure 强制要求：先实现最小 GraphQL 取数、最小关系深度、最小响应投影，再根据 webhook 下游缺口逐项扩展字段。
- Separation of Concerns 强制要求：`normalize webhook`、`query OpenCTI`、`response projection` 必须分层表达，认证注入、GraphQL 查询、响应整形不要混入同一职责块。

## 5. 架构元素级任务拆解

| 子任务名称 | 对应架构元素 | 技术目的 | 与其他子任务的依赖关系 |
| --- | --- | --- | --- |
| 对齐直连基线 | ai4sec_threat_modeling_agent（1436） | 提取可复用的 GraphQL URL、Token 命名与最小查询语义 | 后续 webhook 查询设计依赖此子任务 |
| 替换 webhook 查询入口 | WEBHOOK_AGENT（1277） | 将 webhook 工作流中的 MCP `/query` 调用替换为直连 OpenCTI 的 HTTP 请求 | 依赖“对齐直连基线” |
| 保持投影合同兼容 | WEBHOOK_AGENT（1277）；ai4sec_opencti_mcp（1215） | 对齐现有兼容服务的返回字段与错误语义，避免下游消费断裂 | 依赖“替换 webhook 查询入口” |
| 校验运行时底座边界 | OpenCTI Runtime Stack（1276）；原则 1228 | 确认查询仍面向内部 OpenCTI，且 webhook lookup 信号链路不被破坏 | 与“替换 webhook 查询入口”并行，可在收尾前完成 |

## 6. 推荐实施顺序

1. 动作说明：读取 1436 现有直连 GraphQL 节点的环境变量命名、请求头和错误处理基线。目标文件 / 模块 / 目录：`DifyAgentWorkflow/ai4sec_threat_modeling_workflow.yaml`。对应架构元素 ID：1436。完成判定标准：可列出 webhook 工作流需复用的 `OPENCTI_GRAPHQL_URL`、`OPENCTI_ADMIN_TOKEN` 和最小查询方式。
2. 动作说明：在 webhook 工作流中定位现有 MCP 查询节点，并替换为直连 OpenCTI GraphQL 的 HTTP 节点。目标文件 / 模块 / 目录：`DifyAgentWorkflow/ai4sec_opencti_webhook_workflow.yaml`。对应架构元素 ID：1277、1276。完成判定标准：工作流不再调用 `OPENCTI_MCP_URL` `/query`。
3. 动作说明：补齐响应整形，使直连 GraphQL 结果保持与当前 webhook 下游兼容的字段合同。目标文件 / 模块 / 目录：`DifyAgentWorkflow/ai4sec_opencti_webhook_workflow.yaml`；必要时 `DifyAgentWorkflow/tools/ai4sec_runtime_tools.py`。对应架构元素 ID：1277、1215。完成判定标准：Webhook 输出字段与既有消费者对齐，新增字段均有用途说明。
4. 动作说明：复核 webhook lookup-required 信号输入是否仍与查询逻辑兼容。目标文件 / 模块 / 目录：`external_opencti/opencti_webhook_signal_template.ejs`；如无需修改则保持不变。对应架构元素 ID：1276、1228。完成判定标准：lookup id、object type 与 GraphQL 查询输入匹配，且无额外外部依赖。
5. 动作说明：检查失败重试、超时与错误语义是否全部在工作流能力上限内实现。目标文件 / 模块 / 目录：`DifyAgentWorkflow/ai4sec_opencti_webhook_workflow.yaml`。对应架构元素 ID：1277。完成判定标准：不存在仓外补偿逻辑；未实现项被标记为需人工确认。

## 7. 建议修改目标

- 优先检查的文件：`DifyAgentWorkflow/ai4sec_opencti_webhook_workflow.yaml`；`DifyAgentWorkflow/ai4sec_threat_modeling_workflow.yaml`
- 可能需要新增的文件：未知；优先不新增文件，若必须新增，仅限工作流内轻量格式整理节点对应的仓内说明文件，当前结论为“无需新增”。
- 可能需要避免修改的文件：`mcp/opencti_mcp/app/main.py`；`mcp/opencti_mcp/app/service.py`；`DifyAgentWorkflow/ai4sec_unified_workflow.yaml`

## 8. 交付物与验收标准

- [ ] `DifyAgentWorkflow/ai4sec_opencti_webhook_workflow.yaml` 改为直连 OpenCTI GraphQL，不再依赖 `OPENCTI_MCP_URL` `/query`
- [ ] 环境变量命名与 1436 基线一致，优先使用 `OPENCTI_GRAPHQL_URL` 与 `OPENCTI_ADMIN_TOKEN`
- [ ] Webhook 结果保持现有下游可消费的字段合同，若有差异已显式记录
- [ ] 查询字段与关系深度先保持最小闭环，未无控制地扩大全图拉取
- [ ] 1215 的其他兼容路径未被删除、未被顺带改写
- [ ] 超时、重试、错误码实现不超出当前工作流配置能力

## 9. 风险、阻塞与缓解措施

| 风险/阻塞 | 影响 | 缓解措施 |
| --- | --- | --- |
| Dify HTTP 节点能力不足以完整替代 MCP 投影 | 下游字段合同可能断裂 | 先保留工作流内代码节点做最小响应整形 |
| 1436 基线与 webhook 场景字段诉求不完全一致 | 可能出现补字段争议 | 所有新增字段逐项注明下游用途，再决定是否扩展 |
| 现有部署仍依赖 `OPENCTI_MCP_URL` | 运行环境切换失败 | 把环境变量差异写成实现假设，并在必要时最小更新说明 |
| lookup-required 信号字段与 GraphQL 查询参数不一致 | webhook 无法解析对象 | 保持 `x_opencti_id` / object_type 输入契约不变，必要时只做模板级最小修正 |