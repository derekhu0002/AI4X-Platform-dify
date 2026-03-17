# 任务执行简报

- 任务名称：业务流程中所有数据都必须是OPENCTI平台中的STIX2.1标准数据
- 任务类型：ToDo
- 当前状态：Active
- 负责人：llm
- 优先级：Low
- 起止时间：2026-3-16 ~ 未知（KG 原值为 1899-12-30，按无效截止日处理）
- 关联架构对象名称与 ID：
  - 业务流程中所有数据都必须是OPENCTI平台中的STIX2.1标准数据（1226）
  - 建立统一情报底座与标准语义（1270）
  - ai4sec_agent（1214）
  - ai4sec_opencti_mcp（1215）
  - OpenCTI Runtime Stack（1276）

## 1. LLM执行摘要

- 本任务目标是让 STIX-first 原则在运行时真实生效，而非只停留在文档层。
- 首要修改对象是 OpenCTI 对象投影、Bundle 持久化、写回后回查链路。
- 不允许长期保留 mock 与真实路径分叉，mock 仅做本地合同兜底。
- 关键验收条件是写回对象可在 OpenCTI 真实查询到，并满足最小字段矩阵。
- 需要独立配置文件维护对象类型最小字段矩阵与说明，支持逐档位扩展。
- 生产环境 mock 开关默认关闭，核心集成验证必须覆盖 opencti 模式。
- 一致性窗口阈值要求小于 1 秒（来自任务上下文），需在验证中显式量测。
- GraphQL 可用路径优先采用 stixCoreObjectEdit/importPush/importUpload。

## 2. 已确认事实

- KG 确认原则元素：业务流程中所有数据都必须是OPENCTI平台中的STIX2.1标准数据（1226）。
- KG 关系 1125：原则 1226 关联到“建立统一情报底座与标准语义”（1270）。
- KG 关系 1082：ai4sec_agent（1214）访问 ai4sec_opencti_mcp（1215）。
- KG 关系 1083：ai4sec_opencti_mcp（1215）访问 OpenCTI Runtime Stack（1276）。
- KG 关系 1086：OpenCTI Runtime Stack（1276）主动推送 STIX Bundle 到 ai4sec_agent（1214）。
- 任务行状态为 Active，优先级为 Low，负责人为 llm（来自元素 1226 的 project_info.tasks）。

## 3. 需人工确认 / 未知项

- 各对象类型最小字段矩阵完整清单（按 VS4 业务需要）具体条目：需人工确认。
- 最终一致性窗口阈值“小于 1 秒”的统计口径与采样方式：需人工确认。
- OpenCTI 版本差异下 GraphQL 字段兼容策略：未知。
- importPush 与 importUpload 的选择准则（按数据量或类型）细节：未知。
- 生产环境失败重试与死信策略：需人工确认。

## 4. 约束与边界

- 强制原则：Progressive Disclosure。先落地最小字段矩阵与核心对象类型，再逐步扩展。
- 强制原则：Separation of Concerns。投影转换、持久化写入、回查校验、测试兜底必须解耦。
- 显式原则：业务流程中所有数据都必须是OPENCTI平台中的STIX2.1标准数据（1226）。
- 显式原则：全局情报底座：OPENCTI 平台（1228）作为语义与存储中心。
- 必须保持不变：OpenCTI Runtime Stack（1276）作为真实数据权威源。
- 明确禁止：在生产环境默认开启 mock 路径。
- 明确禁止：仅凭 mock 测试通过就宣称 STIX-first 已落地。

## 5. 架构元素级任务拆解

| 子任务名称 | 对应架构元素 | 技术目的 | 依赖关系 |
| --- | --- | --- | --- |
| 最小字段矩阵定义 | 1226, 1270 | 建立对象投影最低可用语义契约 | 起始子任务 |
| 真实写入路径实现 | 1215, 1276 | 打通 stixCoreObjectEdit/importPush/importUpload 真实写入 | 依赖最小字段矩阵定义 |
| 写回后回查校验 | 1215, 1276 | 验证对象真实存在且字段可读 | 依赖真实写入路径实现 |
| mock 路径收敛 | 1214, 1215 | 让 mock 仅用于本地合同兜底 | 依赖真实写入路径实现 |
| 合同与集成测试补齐 | 1226, 1270 | 防止字段漂移和环境偏差 | 依赖回查校验与 mock 路径收敛 |

## 6. 推荐实施顺序

1. 动作说明：定义并落盘最小字段矩阵配置（含说明注释）。目标文件 / 模块 / 目录：需结合代码仓进一步定位。对应架构元素 ID：1226, 1270。完成判定标准：配置文件可覆盖当前 VS4 必需对象类型。
2. 动作说明：实现真实 OpenCTI 写入调用路径并统一接口封装。目标文件 / 模块 / 目录：mcp/opencti_mcp/app/service.py。对应架构元素 ID：1215, 1276。完成判定标准：真实环境写入成功，返回对象标识可追踪。
3. 动作说明：增加写回后回查逻辑并记录一致性耗时。目标文件 / 模块 / 目录：mcp/opencti_mcp/app/service.py。对应架构元素 ID：1215, 1276。完成判定标准：回查通过率达标，耗时数据可审计。
4. 动作说明：收敛 mock 开关默认值并限制使用场景。目标文件 / 模块 / 目录：需结合代码仓进一步定位。对应架构元素 ID：1214, 1215。完成判定标准：生产配置默认关闭 mock，文档说明清晰。
5. 动作说明：补充合同测试与集成测试覆盖真实路径。目标文件 / 模块 / 目录：tests/contract/, tests/integration/。对应架构元素 ID：1226。完成判定标准：测试用例可区分 mock 兜底与真实集成验证。

## 7. 建议修改目标

- 优先检查的文件：
  - mcp/opencti_mcp/app/service.py
  - tests/contract/test_opencti_api_contract.py
  - tests/integration/test_webhook_to_notification_flow.py
- 可能需要新增的文件：
  - 需结合代码仓进一步定位（对象最小字段矩阵独立配置文件）。
- 可能需要避免修改的文件：
  - DifyAgentWorkflow/ai4sec_unified_workflow.yaml（非本任务核心变更面）。

## 8. 交付物与验收标准

- [x] 对象最小字段矩阵配置文件已建立并纳入版本管理。
  手工测试步骤：1) 打开 `config/stix_minimal_field_matrix.json` 检查关键对象类型字段清单；2) 在 Git 变更中确认该文件被版本管理；3) 组织一次评审确认 VS4 所需对象均有最小字段定义。
- [ ] 真实 OpenCTI 写入路径可用，支持至少一种生产可用导入方式。
  手工测试步骤：1) 设置 `OPENCTI_MCP_MOCK_MODE=false`；2) 通过 `/bundle` 提交真实 STIX Bundle，样本数据如下（POST 到 `http://localhost:8101/bundle`，Content-Type: application/json）：
  ```json
  {
    "bundle": {
      "type": "bundle",
      "id": "bundle--b2865eb1-26d2-421e-9b34-5de2042f49a1",
      "objects": [
        {
          "type": "indicator",
          "spec_version": "2.1",
          "id": "indicator--8f69cfe9-8088-411c-bb09-9a33cf0d73d8",
          "created": "2026-03-14T12:00:00.000Z",
          "modified": "2026-03-14T12:00:00.000Z",
          "name": "bola-jwt-mismatch",
          "indicator_types": ["malicious-activity"],
          "pattern": "[url:value MATCHES '^https://app.example.local/api/users/.+$']",
          "pattern_type": "stix",
          "valid_from": "2026-03-14T10:00:00.000Z"
        }
      ]
    }
  }
  ```
  完整多对象样本参见 `tests/validation/test-data/vs4-bola-monitoring-bundle.json`；3) 接口返回 `mode=opencti` 且 `accepted=true`；4) 在 OpenCTI 界面查询写入对象存在。
  排障提示：若返回 `CTI-5023`（`Cannot query field "importPush" on type "Mutation"`）或 `CTI-5024`，说明当前 OpenCTI schema 未暴露该导入 mutation（常见于版本差异或 API Token 权限不足）；需核对 OpenCTI 版本兼容性并确认 token 具备导入权限。
- [ ] 写回后回查验证默认开启并记录一致性时延。
  手工测试步骤：1) 提交一条写回请求；2) 检查 MCP 日志与响应中是否执行回查；日志关键字说明：
  - **成功**：响应体 `{"accepted": true, "mode": "opencti", ...}`，uvicorn 访问日志 `POST /bundle HTTP/1.1" 200`；
  - **超出阈值（验证失败）**：响应 HTTP 409，响应体包含 `"code": "CTI-4091"` 及 `"message": "Writeback verification failed within 1.0s for: <object_id>"`，uvicorn 日志 `POST /bundle HTTP/1.1" 409`；
  - **中间态未找到**：内部 `CTI-4041` 在窗口内自动重试，若超时则升级为 `CTI-4091`；
  - **阈值配置**：环境变量 `OPENCTI_MCP_WRITEBACK_VERIFY_WINDOW_SECONDS`（默认 `1.0`）；
  3) 若超出阈值，确认响应体中出现 `CTI-4091` 错误码；4) 将实测耗时记录到验收表。
- [ ] mock 在生产默认关闭，仅作为本地合同测试兜底。
  手工测试步骤：1) 检查生产环境变量未显式开启 mock；2) 调用 `/query` 或 `/bundle` 确认返回 `source/mode` 非 mock；3) 仅在本地测试环境打开 mock 并记录用途。
- [ ] 合同测试与集成测试覆盖真实路径，避免“测试通过但生产失效”。
  手工测试步骤（本地/CI 详细执行）：
  1) 激活虚拟环境：Windows 执行 `.venv\Scripts\Activate.ps1`，Linux/Mac 执行 `source .venv/bin/activate`；
  2) 执行单元测试：`python -m pytest tests/unit/test_opencti_projection.py -v`，预期全绿；
  3) 执行合同测试：`python -m pytest tests/contract/test_opencti_api_contract.py -v`，预期全绿（此步骤默认 mock 模式，作为本地合同兜底）；
  4) 执行集成测试：`python -m pytest tests/integration/test_webhook_to_notification_flow.py -v`，预期全绿；
  5) 联调环境真实写入验证（需 OpenCTI 实例可达）：设置 `OPENCTI_MCP_MOCK_MODE=false`、`OPENCTI_MCP_OPENCTI_BASE_URL=<真实地址>`、`OPENCTI_MCP_OPENCTI_API_TOKEN=<Token>`，再执行上方样本 `/bundle` POST，确认响应 `mode=opencti` 且对象可在 OpenCTI 界面查到；
  6) 对比"本地测试全绿"与"联调真实写入成功"两项证据均存在，归档截图与测试运行输出。

## 9. 风险、阻塞与缓解措施

- 技术风险：OpenCTI 版本 API 差异造成写入失败。缓解：引入版本能力探测和回退策略。
- 数据风险：字段矩阵不完整导致对象被拒收。缓解：先最小可用集，逐步扩展并回归。
- 运维风险：一致性窗口波动超过阈值。缓解：增加异步重试与延迟容忍配置。
- 质量风险：团队误用 mock 结果。缓解：在 CI 中将真实集成验证设为必经关卡。