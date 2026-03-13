# 任务执行简报

- 任务名称: ApplicationLayer
- 任务类型: ToDo
- 当前状态: Active
- 负责人: llm
- 优先级: Low
- 起止时间: 2026-3-13 ~ 2026-3-13（截止日期已由 derek 刷新确认）
- 关联架构对象名称与 ID: ApplicationLayer(1209), DIFY(1212), SKILL(1213), ai4sec_agent(1214), ai4sec_opencti_mcp(1215), OpenCTI platform(1216), 外部信息爬取AGENT(1217), 外部网站(1218), 情报分析师(1219), 各类情报消费者(1220), 支持快速的情报生产和消费(1221)

## 1. LLM执行摘要

- 目标是基于现有整体架构，将 ApplicationLayer 的实现方案细化为可执行的模块级设计与落地清单。
- 首要修改对象是应用层方案文档与实现规划，不应直接改动与当前任务无关的业务层/技术层架构定义。
- 需要优先围绕 `ai4sec_agent(1214)`、`ai4sec_opencti_mcp(1215)`、`OpenCTI platform(1216)` 三者交互链路细化边界与接口责任。
- `SKILL(1213)` 与 `DIFY(1212)` 的关系应保持现有聚合与调用语义，不可引入跨层耦合。
- 必须明确情报流向：外部采集 -> OpenCTI -> ai4sec_agent -> 情报消费者。
- 范围边界为 ApplicationLayer 视图内元素与关系；超出该视图的实现细节需标注为需人工确认。
- 验收关键条件是输出可执行、可验证、可追踪到架构元素 ID 的实施方案。
- 强制落实 Progressive Disclosure：先交付最小可运行链路，再逐步扩展能力。
- 强制落实 Separation of Concerns：采集、存储、查询、编排、消费职责必须分离。
- 当前任务工作流范围已明确：驱动用户故事为 `VS3-E2E_动态知识进化闭环_漏洞风险评估` 端到端用户故事（漏洞风险升级与预警邮件发送全流程，共五幕）。
- 本次交付形态为设计先行，不涉及代码实现。
- 当前主要风险是用户故事所需的内部资产数据（SBOM、产品关键度图谱）尚无对应架构元素定义。

## 2. 已确认事实

- `ApplicationLayer(1209)` 在 `project_info.tasks` 中存在一条状态为 `Active` 的任务。
- `ai4sec_agent(1214)` 与 `DIFY(1212)` 存在 `aggregates` 关系（关系 ID: 1079）。
- `SKILL(1213)` 与 `DIFY(1212)` 存在 `aggregates` 关系（关系 ID: 1080）。
- `ai4sec_agent(1214)` 使用 `SKILL(1213)`（关系 ID: 1081）。
- `ai4sec_agent(1214)` 访问 `ai4sec_opencti_mcp(1215)`（关系 ID: 1082）。
- `ai4sec_opencti_mcp(1215)` 访问 `OpenCTI platform(1216)`（关系 ID: 1083）。
- `OpenCTI platform(1216)` 主动推送 STIX BUNDLE 给 `ai4sec_agent(1214)`（关系 ID: 1086）。
- `OpenCTI platform(1216)` 的属性中已记录 `external_opencti/docker-compose.dev.yml` 与 `.env` 相关配置内容。
- `外部信息爬取AGENT(1217)` 与 `外部网站(1218)`、`OpenCTI platform(1216)`存在采集与同步关系（关系 ID: 1084, 1085）。
- **交付形态（derek 确认）**：本次任务先交付设计文档，不要求代码实现。
- **目录命名（derek 确认）**：`implementation/` 下的目录与文件命名由 LLM 自行定义。
- **ai4sec_opencti_mcp 接口（derek 确认）**：接口协议、认证方式、字段白名单及错误码规范由 LLM 负责设计。
- **ai4sec_agent 工作流范围（derek 确认）**：对应用户故事 `VS3-E2E_动态知识进化闭环_漏洞风险评估`，需实现以下五幕端到端流程：
  - 第一幕：OpenCTI webhook 推送漏洞 STIX BUNDLE 数据至 ai4sec_agent
  - 第二幕：ai4sec_opencti_mcp 查询完整漏洞详情并标准化为 STIX 2.1 格式
  - 第三幕：内部资产关联查询（SBOM / 资产关键度图谱）
  - 第四幕：LLM 多链推理（技术影响 → 暴露面评估 → 风险等级升级）
  - 第五幕：风险极高时触发 NotificationTool 发送预警邮件给相关负责人
- **STIX 字段策略（derek 确认）**：返回字段白名单须按用户故事目标设计，最小覆盖集包含：`vulnerability.id`、`vulnerability.name`、`x_cvss_score`、`x_severity`、`x_affected_systems`、`relationship(has-component)`、`software.x_criticality` 及 `software.x_functions`（参见 `VS3-E2E_漏洞风险评估_STIX-2.1样本数据.json`）。
- **due_date（derek 确认）**：已刷新为 `2026-3-13`，原占位值 `1899-12-30` 已清除。
- 用户故事权威来源：`design/userstories/value_stream_aligned/VS3-E2E_动态知识进化闭环_漏洞风险评估/VS3-E2E_漏洞风险评估与预警_用户故事.md`
- STIX 2.1 样本数据：`design/userstories/value_stream_aligned/VS3-E2E_动态知识进化闭环_漏洞风险评估/VS3-E2E_漏洞风险评估_STIX-2.1样本数据.json`
- **架构原则（derek 确认）**：业务流程中所有数据都必须是OPENCTI平台中的STIX2.1标准数据。
- **发送通道机制（derek 确认）**：图谱中已增加Notification MCP（ID: 1227），默认使用邮件发送通知。预警邮件模板与收件人列表在其环境配置中维护（如ALERT_RECIPIENT，支持多个收件人）。
- **Webhook 推送（derek 确认）**：OpenCTI webhook 推送模板已在图谱中的 OpenCTI platform 元素中增加推送模板脚本配置。

- **新增事项**：基于图谱中的架构原则、目标应用架构，刷新 design/userstories/value_stream_aligned 下的所有用户故事。

## 3. 需人工确认 / 未知项

- (所有未知项已清零)

## 4. 约束与边界

- 必须遵守原则: Progressive Disclosure。
- 必须遵守原则: Separation of Concerns。
- 必须保持不变: `ApplicationLayer(1209)` 已定义元素及其核心关系语义（1079-1088）不得被破坏。
- 禁止实现方式: 将 OpenCTI 访问逻辑散落到多个业务模块，或绕过 `ai4sec_opencti_mcp(1215)` 直接在编排层直连 OpenCTI。
- 禁止越界: 不得直接改写 BusinessLayer(1208) 与 TechnologyLayer(1210) 的架构结构定义。
- Progressive Disclosure 落地要求: 先定义并实现最小闭环（查询 -> 标准化 -> 消费），再增量扩展外部采集与高级分析能力。
- Separation of Concerns 落地要求: 采集、适配、编排、消费四类职责对应不同模块/文件，不得混用。
- **用户故事约束**：所有接口设计与模块划分必须能支撑且不破坏 `VS3-E2E_漏洞风险评估与预警_用户故事.md` 中定义的五幕端到端流程（webhook 推送 → 摄取归一化 → 资产关联 → LLM 推理 → 预警发送）。

## 5. 架构元素级任务拆解

- 子任务名称: 梳理应用层能力边界与责任矩阵
  - 对应架构元素: ApplicationLayer(1209), ai4sec_agent(1214), ai4sec_opencti_mcp(1215), OpenCTI platform(1216)
  - 技术目的: 明确模块职责、输入输出与依赖方向，形成统一实现蓝图
  - 依赖关系: 无前置，作为后续接口与实施顺序的基础
- 子任务名称: 定义情报查询与返回字段策略
  - 对应架构元素: ai4sec_opencti_mcp(1215), OpenCTI platform(1216)
  - 技术目的: 固化 STIX 查询接口边界、字段白名单与返回契约
  - 依赖关系: 依赖“能力边界与责任矩阵”输出
- 子任务名称: 细化编排层调用链路
  - 对应架构元素: ai4sec_agent(1214), SKILL(1213), DIFY(1212)
  - 技术目的: 将 MCP 调用和技能组合落到可执行流程
  - 依赖关系: 依赖“查询字段策略”与“能力边界”
- 子任务名称: 明确情报生产/消费闭环
  - 对应架构元素: 外部信息爬取AGENT(1217), 外部网站(1218), OpenCTI platform(1216), 各类情报消费者(1220)
  - 技术目的: 保证从采集到消费的链路可追踪、可验证
  - 依赖关系: 依赖“编排层调用链路”- 子任务名称: 设计 ai4sec_opencti_mcp 接口契约与 STIX 字段白名单
  - 对应架构元素: ai4sec_opencti_mcp(1215), OpenCTI platform(1216)
  - 技术目的: 固化 MCP 工具接口（名称、输入 schema、输出字段白名单、错误码），对照 STIX 样本数据确保用户故事所需字段全覆盖
  - 依赖关系: 依赖"能力边界与责任矩阵"与用户故事 STIX 样本数据
- 子任务名称: 设计 ai4sec_agent DIFY 工作流（覆盖五幕用户故事）
  - 对应架构元素: SKILL(1213), ai4sec_agent(1214), DIFY(1212)
  - 技术目的: 定义 DIFY 工作流节点（webhook 接收 → MCP 查询 → 资产关联 → LLM 推理链 → NotificationTool），包含每节点的提示词模板与触发条件
  - 依赖关系: 依赖"接口契约"与用户故事五幕定义
## 6. 推荐实施顺序

1. 动作说明: 输出 ApplicationLayer 责任边界清单与关系映射表。
   - 目标文件 / 模块 / 目录: 需结合代码仓进一步定位
   - 对应架构元素 ID: 1209, 1214, 1215, 1216
   - 完成判定标准: 每个模块有明确职责、输入、输出、依赖，且与关系 1079-1088 一一对齐。
2. 动作说明: 定义并评审 `ai4sec_opencti_mcp` 的查询接口契约和字段策略。
   - 目标文件 / 模块 / 目录: 需结合代码仓进一步定位
   - 对应架构元素 ID: 1215, 1216
   - 完成判定标准: 有可执行的接口定义与字段白名单，并标注异常路径处理。
3. 动作说明: 在 DIFY/agent 工作流中落实 MCP + SKILL 的调用编排。
   - 目标文件 / 模块 / 目录: 需结合代码仓进一步定位
   - 对应架构元素 ID: 1212, 1213, 1214
   - 完成判定标准: 调用链可复现，输入输出与契约一致，未出现职责混叠。
4. 动作说明: 建立最小闭环验证方案（webhook 推送 → MCP 查询 → LLM 推理 → 预警发送）。
   - 目标文件 / 模块 / 目录: 需结合代码仓进一步定位
   - 对应架构元素 ID: 1214, 1216, 1220
   - 完成判定标准: 至少 1 条端到端路径被设计覆盖，且输出满足消费者需求。
5. 动作说明: 输出 ai4sec_opencti_mcp 接口契约文档（工具名、描述、输入 schema、输出字段白名单、错误码）。
   - 目标文件 / 模块 / 目录: `implementation/design/ai4sec_opencti_mcp_contract.md`
   - 对应架构元素 ID: 1215, 1216
   - 完成判定标准: 字段白名单覆盖 STIX 样本数据的所有必要字段，错误处理路径明确。
6. 动作说明: 输出 ai4sec_agent DIFY 工作流设计文档（节点图 + 每节点输入/输出/调用工具/提示词模板）。
   - 目标文件 / 模块 / 目录: `implementation/design/ai4sec_agent_workflow_design.md`
   - 对应架构元素 ID: 1212, 1213, 1214
   - 完成判定标准: 覆盖用户故事五幕所有步骤，每个节点有明确工具调用与触发条件。

## 7. 建议修改目标

- 优先检查的文件:
  - `external_opencti/docker-compose.dev.yml`（OpenCTI 部署配置与 webhook 能力确认）
  - `design/userstories/value_stream_aligned/VS3-E2E_动态知识进化闭环_漏洞风险评估/VS3-E2E_漏洞风险评估与预警_用户故事.md`（业务五幕流程权威来源）
  - `design/userstories/value_stream_aligned/VS3-E2E_动态知识进化闭环_漏洞风险评估/VS3-E2E_漏洞风险评估_STIX-2.1样本数据.json`（STIX 字段白名单设计参考）
- 可能需要新增的文件（设计产出）:
  - `implementation/design/ApplicationLayer_module_boundary.md`（模块边界与责任矩阵）
  - `implementation/design/ai4sec_opencti_mcp_contract.md`（MCP 接口契约与字段白名单）
  - `implementation/design/ai4sec_agent_workflow_design.md`（DIFY 工作流节点设计）
- 可能需要避免修改的文件:
  - 非 ApplicationLayer 范围的 BusinessLayer、TechnologyLayer 架构定义文件
  - 用户故事原始文件（只读参考，不得修改）

## 8. 交付物与验收标准

- [ ] 交付物 1: `implementation/design/ApplicationLayer_module_boundary.md` — 模块边界、输入/输出定义、模块间依赖矩阵。
- [ ] 交付物 2: `implementation/design/ai4sec_opencti_mcp_contract.md` — MCP 工具接口契约（工具名、参数 schema、字段白名单、错误码）。
- [ ] 交付物 3: `implementation/design/ai4sec_agent_workflow_design.md` — DIFY 工作流节点设计（涵盖用户故事五幕）。
- [ ] 验收标准: 每个接口/节点定义可追溯到至少一个架构元素 ID（1212-1221）。
- [ ] 验收标准: 满足 Progressive Disclosure（最小闭环先行）与 Separation of Concerns（采集/适配/编排/消费分离）。
- [ ] 验收标准: 不破坏关系 1079-1088 的既有语义。
- [ ] 验收标准: 设计方案完整覆盖用户故事五幕（webhook 推送 → 摄取 → 资产关联 → LLM 推理 → 预警发送）。
- [ ] 验收标准: STIX 字段白名单覆盖样本数据中所有被用户故事引用的字段。

## 9. 风险、阻塞与缓解措施

- 技术风险: 接口契约未定导致实现返工。
  - 缓解措施: 先冻结 MCP 契约最小版本并评审后再编码。
- 依赖风险: OpenCTI 环境配置与运行状态不稳定。
  - 缓解措施: 先验证 `external_opencti/docker-compose.dev.yml` 与 `.env` 的最小可用性。
- 信息缺口: 内部资产关键度数据源（SBOM / 资产图谱）尚无架构元素定义。
  - 缓解措施: 在接口契约文档中以"待接入"占位接口标注，并注明 `需新增架构元素`。
- 信息缺口: OpenCTI webhook 注册流程与 NotificationTool 通道细节未知。
  - 缓解措施: 在工作流设计文档中以可替换配置参数占位，避免设计被具体实现绑定。

## 10. 下一步建议

- 先输出 `ApplicationLayer_module_boundary.md`（模块边界与责任矩阵），作为后续两份文档的基础。
- 再输出 `ai4sec_opencti_mcp_contract.md`，对照 STIX 样本数据 JSON 逐字段核对白名单。
- 最后输出 `ai4sec_agent_workflow_design.md`，覆盖用户故事五幕，逐节点定义工具调用与提示词模板，不要求代码实现。
- 所有设计文档输出至 `implementation/design/` 目录。
