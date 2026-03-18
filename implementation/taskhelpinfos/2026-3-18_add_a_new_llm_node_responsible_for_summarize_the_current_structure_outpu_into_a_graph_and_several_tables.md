# 任务执行简报

- 任务名称：add a new llm node responsible for summarize the current structure outpu into a graph and several tables
- 任务类型：ToDo
- 当前状态：Active
- 负责人：llm
- 优先级：Low
- 起止时间：2026-3-18 至 未设置
- 关联架构对象名称与 ID：ai4sec_threat_modeling_agent（1436）；VS1-E2E_持续安全交付闭环_端到端用户故事（1223）；业务流程中所有数据都必须是OPENCTI平台中的STIX2.1标准数据（1226）；全局情报底座：OPENCTI 平台（1228）；统一智能入口：DIFY Agent (ai4sec_agent)（1229）

## 1. LLM执行摘要

- 当前任务要在 ai4sec_threat_modeling_agent（1436）现有主分析链路之后新增一个 LLM 节点，把当前结构化输出摘要成 Mermaid 关系图和若干 Markdown 表格。
- 首要修改对象是 `DifyAgentWorkflow/ai4sec_threat_modeling_workflow.yaml`，因为 1436 的代码路径和任务描述都指向该单一工作流资产。
- 不允许改变主分析职责归属：原有主分析节点继续产出结构化威胁建模结果，新节点只做图表摘要，必要时再加后置轻量格式整理。
- Mermaid 图必须先从最小关系图开始，只表达 STIX 对象名称与 `relationship_type`，不引入额外图建模约定。
- 表格只在会话中展示，不写回当前 JSON 下载文件，也不要求单独文件或单独变量产出。
- `indicator` 与 `attack path` 在当前 VS1 证据集中不稳定存在，缺失时直接不显示，不得补造内容。
- 最关键验收条件是：最终会话输出先给出图和表，再附上当前 JSON 结果；JSON 下载能力和原始结构不被破坏。
- 主要风险是工作流输出格式较长，若直接由 LLM 节点拼接可能引发格式漂移，因此需要保留轻量格式整理余地。

## 2. 已确认事实

- ai4sec_threat_modeling_agent（1436）在 KG 中被定义为独立的 VS1 Dify advanced-chat workflow 资产，负责接收报告引用、精确解析 report 标识、直连 OpenCTI GraphQL、过滤 STIX 2.1 证据 bundle、调用结构化 LLM 并在会话中返回结果。
- 1436 的代码路径在 KG 中已明确到 `DifyAgentWorkflow/ai4sec_threat_modeling_workflow.yaml`。
- VS1-E2E 用户故事（1223）确认该场景围绕威胁建模、控制缺口和发布判定闭环展开，核心事实载体是 OpenCTI 中的 STIX 2.1 对象与关系。
- 原则 1226 要求所有业务流转数据保持 STIX 2.1 标准语义；原则 1228 要求事实来源于 OpenCTI；原则 1229 要求智能交互由 DIFY Agent 承接。
- 任务描述已明确：关系图承载形式必须是 Mermaid；表格采用 Markdown 表格；默认最小公共列为 `name`、`id`、`type`、`description`、`relationship_count`，缺列时允许降级。

## 3. 需人工确认 / 未知项

- 未知：当前主分析节点输出的结构化 JSON 中，是否已经稳定包含可直接汇总为关系图的关系数组。建议先复用现有 bundle 或摘要中的对象/关系统计，不足时再在后置代码节点补充映射。
- 未知：Dify 当前 answer 节点是否支持把 Mermaid、Markdown 表格和原 JSON 以稳定顺序拼接。建议在新增 LLM 节点后保留一个轻量格式整理节点，确保会话输出顺序固定。
- 未知：`attack path` 在现有 VS1 结果中的数据来源是否单独建模。建议缺失即不显示，不为展示目的构造新字段。
- 未知：新增图表摘要是否需要保留多语言输出。建议保持与当前会话输出语言一致，避免引入额外翻译步骤。
- 未知：大对象集合下 Mermaid 文本是否可能超长。建议先只取最小必要关系，必要时按对象数量做截断策略并明确说明。

## 4. 约束与边界

- 必须遵守的 Principle / Constraint：1226、1228、1229；同时强制落实 Progressive Disclosure 与 Separation of Concerns。
- 必须保持不变的模块或边界：1436 的 report 精确解析、GraphQL 取数、结构化主分析、JSON 下载能力；OpenCTI 仍是事实源。
- 明确禁止的实现方式或越界修改：禁止把图表结果写入 JSON 下载文件；禁止把新增 LLM 节点前移到主分析节点之前；禁止为缺失的 `indicator` 或 `attack path` 人工补造数据。
- Progressive Disclosure 强制要求：先输出最小 Mermaid 关系图和最小公共列表格，再按稳定存在的对象类型扩展，不做复杂可视化。
- Separation of Concerns 强制要求：主分析负责威胁建模语义，新增 LLM 节点负责展示摘要，后置代码节点仅负责轻量格式整理。

## 5. 架构元素级任务拆解

| 子任务名称 | 对应架构元素 | 技术目的 | 与其他子任务的依赖关系 |
| --- | --- | --- | --- |
| 明确主分析输出接口 | ai4sec_threat_modeling_agent（1436） | 确认新增摘要节点的输入是现有结构化主分析结果还是过滤后的 bundle | 后续图表生成依赖此子任务 |
| 生成 Mermaid 关系图 | ai4sec_threat_modeling_agent（1436）；VS1（1223） | 把对象与 `relationship_type` 转成最小关系图 | 依赖“明确主分析输出接口” |
| 生成按实体类型分组的表格 | ai4sec_threat_modeling_agent（1436） | 输出按类型分组的 Markdown 表格，缺失类型不显示 | 依赖“明确主分析输出接口” |
| 整理最终会话展示顺序 | 原则 1229 | 让图表在前、JSON 在后，且不影响下载文件 | 依赖前两项子任务 |

## 6. 推荐实施顺序

1. 动作说明：定位 1436 当前主分析节点、后置格式节点和最终 answer 节点。目标文件 / 模块 / 目录：`DifyAgentWorkflow/ai4sec_threat_modeling_workflow.yaml`。对应架构元素 ID：1436。完成判定标准：明确新增 LLM 节点插入位置在主分析节点之后。
2. 动作说明：定义新摘要节点的输入，优先复用现有结构化结果或过滤后的 STIX bundle。目标文件 / 模块 / 目录：`DifyAgentWorkflow/ai4sec_threat_modeling_workflow.yaml`。对应架构元素 ID：1436、1226。完成判定标准：无需破坏现有 JSON 下载结构即可提供图表摘要输入。
3. 动作说明：新增 LLM 节点生成 Mermaid 最小关系图与实体类型表格。目标文件 / 模块 / 目录：`DifyAgentWorkflow/ai4sec_threat_modeling_workflow.yaml`。对应架构元素 ID：1436、1223。完成判定标准：输出包含 Mermaid 图和按类型分组的 Markdown 表格。
4. 动作说明：必要时增加后置轻量格式整理节点，确保图表在前、JSON 在后。目标文件 / 模块 / 目录：`DifyAgentWorkflow/ai4sec_threat_modeling_workflow.yaml`。对应架构元素 ID：1436、1229。完成判定标准：会话展示顺序稳定，原 JSON 下载结果不变。
5. 动作说明：检查缺失类型的降级策略，仅展示存在的 `indicator`、`attack path` 或其他实体类型。目标文件 / 模块 / 目录：`DifyAgentWorkflow/ai4sec_threat_modeling_workflow.yaml`。对应架构元素 ID：1436。完成判定标准：无缺失数据伪造，表格列按最小公共列或可展示列降级。

## 7. 建议修改目标

- 优先检查的文件：`DifyAgentWorkflow/ai4sec_threat_modeling_workflow.yaml`
- 可能需要新增的文件：未知；当前建议不新增文件，优先在同一 workflow YAML 内完成节点编排。
- 可能需要避免修改的文件：`mcp/opencti_mcp/app/service.py`；`DifyAgentWorkflow/ai4sec_opencti_webhook_workflow.yaml`；`DifyAgentWorkflow/ai4sec_unified_workflow.yaml`

## 8. 交付物与验收标准

- [ ] 在主分析节点之后新增图表摘要 LLM 节点
- [ ] 会话结果包含 Mermaid 最小关系图
- [ ] 会话结果包含按实体类型分组的 Markdown 表格
- [ ] `indicator`、`attack path` 缺失时不显示，不补造数据
- [ ] 图表结果不写入当前 JSON 下载文件
- [ ] 最终展示顺序为图表在前、当前 JSON 在后

## 9. 风险、阻塞与缓解措施

| 风险/阻塞 | 影响 | 缓解措施 |
| --- | --- | --- |
| 主分析输出结构不稳定 | 摘要节点难以稳定取数 | 优先复用过滤后的 bundle 或固定结构化摘要输入 |
| Mermaid 文本过长 | 会话可读性下降 | 先输出最小关系图，仅保留核心对象名称与关系类型 |
| 表格列在不同实体类型间差异大 | 表格难统一 | 默认最小公共列，缺列时按可展示列降级 |
| 新节点破坏原 JSON 输出或下载链路 | 功能回归 | 将图表摘要与 JSON 下载分离，必要时用后置节点做格式拼接 |