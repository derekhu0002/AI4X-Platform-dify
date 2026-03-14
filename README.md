# AI4SEC 平台实现说明

## 1. 项目概览

AI4SEC 是一个围绕安全情报生产、消费与闭环运营构建的多层架构系统。当前仓库基于战略动机层、业务层、应用层和技术层设计，落地了一套最小可运行的应用层实现骨架，目标是把外部或内部安全事件统一收敛到 OpenCTI，再通过 Dify Agent、MCP 服务与通知通道完成研判、编排和反馈。

当前实现重点覆盖以下交付：

- 一条可导入 Dify 的统一 YAML/DSL 工作流资产。
- 一个 OpenCTI MCP FastAPI 服务，用于 STIX 投影查询、Bundle 写回和 webhook 透传。
- 一个 Notification MCP FastAPI 服务，用于通知预览、正式收件人注入、升级矩阵和幂等键生成。
- 一组 Python 工具函数，用于 OpenCTI signal 回查、场景路由和通知载荷拼装。
- 覆盖单元测试、契约测试、集成测试和端到端测试四层的自动化验证基线。
- 一条 GitHub Actions CI 流程，用于安装依赖并执行测试。

## 2. 架构总览

### 2.1 战略动机层

系统的战略目标是“支持快速的情报生产和消费”，围绕四条价值流形成闭环：

- VS1：威胁建模闭环。
- VS2：威胁运营与响应闭环。
- VS3：动态知识进化闭环。
- VS4：环境感知监控闭环。

这些价值流共同约束了系统的三个核心原则：

- 所有主业务数据以 STIX 2.1 为统一语义载体。
- OpenCTI 是唯一内部情报底座。
- Dify Agent 是统一智能入口，Notification MCP 是统一通知出口。

### 2.2 业务层

业务层将价值流落成统一业务闭环，核心角色包括：

- 情报分析师：主导任务受理、研判和知识沉淀。
- 业务负责人：确认业务影响、窗口期和业务约束。
- 安全负责人：审批高风险治理动作和升级动作。
- 管理层：消费企业级摘要并做资源决策。
- 安全运营团队：执行监控和响应动作，并反馈命中结果。

业务层视角下，系统需要持续支撑：任务受理、上下文归并、风险研判、响应编排、通知协同和知识回灌。

### 2.3 应用层

应用层把业务能力映射为统一的 Dify 编排入口与场景工作流：

- Dify 作为用户交互和编排入口。
- ai4sec_agent 作为统一智能入口和工作流运行资产。
- ai4sec_opencti_mcp 作为 OpenCTI 访问面。
- Notification MCP 作为标准化通知出口。

当前仓库实现的统一工作流采用“一条资产，多场景分流”的方式：

- 可通过菜单直接选择 VS1、VS2、VS3、VS4。
- 也可通过自然语言意图识别自动路由。
- OpenCTI webhook 通过 `/webhooks/opencti/threat-intelligence` 接入。

### 2.4 技术层

技术层当前目标为单机开发测试环境，推荐运行形态是：

- `external_opencti/` 负责 OpenCTI 及其依赖容器。
- `externalDify/` 负责 Dify 及其依赖容器。
- `mcp/opencti_mcp/` 与 `mcp/notification_mcp/` 作为独立 FastAPI 服务运行。
- 本地 Python 虚拟环境用于工作流工具代码和测试执行。

## 3. 当前实现映射

### 3.1 目录说明

- `design/`: 四层架构设计文档、用户故事、任务索引和架构模型。
- `DifyAgentWorkflow/`: Dify 统一工作流 DSL 与工作流工具代码。
- `mcp/opencti_mcp/`: OpenCTI MCP 实现。
- `mcp/notification_mcp/`: Notification MCP 实现。
- `external_opencti/`: OpenCTI 本地容器编排文件。
- `externalDify/`: Dify 本地容器编排文件。
- `tests/`: 自动化测试，按 unit、contract、integration、e2e 分层。
- `.github/workflows/`: CI 配置。

### 3.2 已实现组件

#### 统一 Dify 工作流

文件：`DifyAgentWorkflow/ai4sec_unified_workflow.yaml`

实现内容：

- 定义 Dify `advanced-chat` 应用。
- 提供 `selected_flow` 菜单变量和自然语言 `user_request` 输入。
- 通过 `if-else` 节点在 VS1 到 VS4 间路由。
- 通过 HTTP 请求节点调用 OpenCTI MCP 的 `/query` 接口。
- 暴露 webhook 元数据，并明确当前链路 `auth_required: false`。

#### ai4sec_agent 工具代码

文件：`DifyAgentWorkflow/tools/ai4sec_runtime_tools.py`

实现内容：

- `resolve_opencti_signal`: 将 OpenCTI signal 对象解析为完整 STIX 对象。
- `route_entrypoint`: 根据菜单、自然语言或 webhook 入口路由场景。
- `build_notification_payload`: 基于场景结果构造通知载荷。

#### OpenCTI MCP

目录：`mcp/opencti_mcp/app/`

实现内容：

- `/health`: 服务健康检查。
- `/query`: 支持 `minimal`、`summary`、`analysis`、`graph`、`notification` 五档 STIX 投影查询。
- `/bundle`: 支持 STIX Bundle 写回和 dry-run。
- `/webhooks/opencti/threat-intelligence`: 支持无鉴权 webhook 透传。
- 支持错误码封装，如 `CTI-4041`、`MCP-4002`、`MCP-4003`。
- 默认 `mock_mode=false`，面向真实 OpenCTI 联调与验收。

#### Notification MCP

目录：`mcp/notification_mcp/app/`

实现内容：

- `/health`: 服务健康检查。
- `/preview`: 生成通知预览。
- `/dispatch`: 通过 SMTP 发送真实通知，默认 `preview_mode=false`。
- 默认正式收件人：`hdhscu@126.com`。
- 支持模板类型：`release-gate-decision`、`incident-response`、`vulnerability-alert`、`monitoring-rule-online`。
- 支持升级矩阵：`normal=240`、`high=30`、`critical=10` 分钟。

## 4. 系统实现方案

### 4.1 主链路

当前系统实现方案遵循“OpenCTI 先收敛，Dify 再编排，Notification 最后触达”的顺序：

1. 外部情报、CI/CD 变更、SIEM 告警等先进入 OpenCTI。
2. OpenCTI 通过 webhook 或事件将 signal 送到 Dify 入口。
3. `ai4sec_agent` 使用 MCP 查询完整 STIX 上下文。
4. 工作流按 VS1 至 VS4 场景完成推理、写回和通知。
5. Notification MCP 根据模板、严重级别和幂等键生成通知输出。

### 4.2 分层实现原则

- Progressive Disclosure：上层只看场景与业务结果，下层才暴露投影、写回和通知细节。
- Separation of Concerns：工作流、MCP、通知、测试和容器编排分目录实现，避免耦合。
- STIX First：主业务载荷不引入与 STIX 无关的核心数据模型。

### 4.3 当前实现边界

当前仓库已经具备最小可运行交付，但仍保留以下边界：

- OpenCTI MCP 默认走真实 GraphQL 查询，启动前必须提供可用的 OpenCTI 地址与访问令牌。
- Notification MCP 默认走真实 SMTP 派发，启动前必须提供可用的 SMTP 配置。
- Dify DSL 为可导入资产骨架，尚未在真实 Dify 实例中完成导入回归验证。
- SKILL 目录能力尚未在本轮实现中扩展。

## 5. 快速开始

### 5.1 环境要求

- Python 3.13+
- 推荐使用仓库根目录虚拟环境 `.venv`
- 如需真实联调，建议准备 Docker / Docker Desktop

### 5.2 安装依赖

在仓库根目录执行：

```powershell
d:/projects/AI4X/AI4X-Platform-dify/.venv/Scripts/python.exe -m pip install -e .[dev]
```

### 5.2.1 根目录 `.env` 配置

项目根目录下的 `.env` 是 OpenCTI MCP 和 Notification MCP 的统一配置来源。

建议先复制模板文件：

```powershell
Copy-Item .env.example .env
```

然后在根目录 `.env` 中填写真实联调参数，例如：

```dotenv
OPENCTI_MCP_OPENCTI_BASE_URL=http://localhost:8080/graphql
OPENCTI_MCP_OPENCTI_API_TOKEN=<你的OpenCTI令牌>
OPENCTI_MCP_MOCK_MODE=false
OPENCTI_MCP_REQUEST_TIMEOUT_SECONDS=15

NOTIFICATION_MCP_DEFAULT_FORMAL_RECIPIENT=hdhscu@126.com
NOTIFICATION_MCP_PREVIEW_MODE=false
NOTIFICATION_MCP_SMTP_HOST=<你的SMTP地址>
NOTIFICATION_MCP_SMTP_PORT=587
NOTIFICATION_MCP_SMTP_USERNAME=<你的SMTP账号>
NOTIFICATION_MCP_SMTP_PASSWORD=<你的SMTP密码或应用专用口令>
NOTIFICATION_MCP_SMTP_FROM_ADDRESS=<发件人地址>
NOTIFICATION_MCP_SMTP_USE_STARTTLS=true
```

两个 MCP 服务启动时会自动读取项目根目录 `.env`，无需额外在 PowerShell 中逐项设置环境变量。

### 5.3 启动 OpenCTI MCP

```powershell
d:/projects/AI4X/AI4X-Platform-dify/.venv/Scripts/python.exe -m uvicorn mcp.opencti_mcp.app.main:app --host 0.0.0.0 --port 8101
```

前提：项目根目录 `.env` 已完成配置。

可选环境变量：

- `OPENCTI_MCP_OPENCTI_BASE_URL`
- `OPENCTI_MCP_OPENCTI_API_TOKEN`
- `OPENCTI_MCP_MOCK_MODE`
- `OPENCTI_MCP_REQUEST_TIMEOUT_SECONDS`

业务层真实验收建议在根目录 `.env` 中显式设置：

- `OPENCTI_MCP_MOCK_MODE=false`

### 5.4 启动 Notification MCP

```powershell
d:/projects/AI4X/AI4X-Platform-dify/.venv/Scripts/python.exe -m uvicorn mcp.notification_mcp.app.main:app --host 0.0.0.0 --port 8102
```

前提：项目根目录 `.env` 已完成配置。

可选环境变量：

- `NOTIFICATION_MCP_DEFAULT_FORMAL_RECIPIENT`
- `NOTIFICATION_MCP_PREVIEW_MODE`
- `NOTIFICATION_MCP_SMTP_HOST`
- `NOTIFICATION_MCP_SMTP_PORT`
- `NOTIFICATION_MCP_SMTP_USERNAME`
- `NOTIFICATION_MCP_SMTP_PASSWORD`
- `NOTIFICATION_MCP_SMTP_FROM_ADDRESS`
- `NOTIFICATION_MCP_SMTP_USE_STARTTLS`

业务层真实验收建议在根目录 `.env` 中显式设置：

- `NOTIFICATION_MCP_PREVIEW_MODE=false`
- `NOTIFICATION_MCP_SMTP_HOST=<你的SMTP地址>`
- `NOTIFICATION_MCP_SMTP_PORT=587`
- `NOTIFICATION_MCP_SMTP_USERNAME=<你的SMTP账号>`
- `NOTIFICATION_MCP_SMTP_PASSWORD=<你的SMTP密码或应用专用口令>`
- `NOTIFICATION_MCP_SMTP_FROM_ADDRESS=<发件人地址>`

### 5.5 导入 Dify 工作流

将以下资产导入 Dify：

- `DifyAgentWorkflow/ai4sec_unified_workflow.yaml`

导入后需确认：

- `OPENCTI_MCP_URL` 指向 `http://host.docker.internal:8101`
- `NOTIFICATION_MCP_URL` 指向 `http://host.docker.internal:8102`
- Webhook 路径使用 `/webhooks/opencti/threat-intelligence`

说明：当 Dify 运行在 Docker Desktop 容器中时，工作流 HTTP 节点里的 `localhost` 指向容器本身，而不是宿主机，因此访问宿主机上的 MCP 服务需要使用 `host.docker.internal`。

### 5.6 启动外部平台容器

如需本地启动 OpenCTI 与 Dify 平台，可使用仓内现成容器文件：

- OpenCTI: `external_opencti/docker-compose.yml`
- Dify: `externalDify/docker-compose.yaml`

建议分别在对应目录执行 Docker Compose 命令，并根据本地环境完善 `.env`。

## 6. 使用指南

### 6.1 场景入口

用户可以通过统一 Dify 工作流进入以下场景：

- VS1 威胁建模：面向发布前建模、控制缺口与发布判定。
- VS2 运营响应：面向告警分诊、响应动作和复盘摘要。
- VS3 漏洞影响：面向外部漏洞企业化影响分析和决策摘要。
- VS4 环境监控：面向监控规则草案、发布和命中反馈。

### 6.2 Webhook 使用

当前实现保留了 OpenCTI 到 Dify 的无鉴权 webhook 基线：

- 路径：`/webhooks/opencti/threat-intelligence`
- 载荷要求：必须包含 `objects`
- signal 对象需带 `x_opencti_lookup_required` 与 `x_opencti_id`

### 6.3 OpenCTI MCP 查询

典型请求示例：

```json
{
  "object_id": "vulnerability--vs3",
  "projection_profile": "notification",
  "include_relationships": false
}
```

适用场景：

- 列表卡片：`minimal`
- 首屏摘要：`summary`
- 深度研判：`analysis`
- 图谱核验：`graph`
- 通知预览：`notification`

### 6.4 Notification MCP 使用

典型通知预览请求：

```json
{
  "template_type": "vulnerability-alert",
  "message_title": "漏洞影响预警",
  "message_summary": "发现高危组件影响生产环境。",
  "business_impact": "影响支付网关。",
  "recommended_action": "优先修补并评估窗口期。",
  "event_type": "ai4sec.vulnerability-intelligence.result.v1",
  "object_refs": ["vulnerability--vs3"],
  "severity_tier": "critical"
}
```

系统会自动：

- 注入正式收件人 `hdhscu@126.com`
- 生成升级等待时间
- 生成 `dedup_key`

## 7. 开发指南

### 7.1 推荐开发流程

1. 先更新 `design/` 中的架构或任务上下文。
2. 再调整 `DifyAgentWorkflow/` 中的 DSL 和工具代码。
3. 然后更新 `mcp/` 下对应服务的模型、服务和路由。
4. 最后补齐 `tests/` 对应分层测试。

### 7.2 测试分层

- `tests/unit/`: 面向纯函数和服务逻辑。
- `tests/contract/`: 面向 FastAPI 接口合同与错误码。
- `tests/integration/`: 面向 webhook、MCP 和通知链路联动。
- `tests/e2e/`: 面向交付资产存在性和最小流程完整性。

### 7.3 运行测试

```powershell
d:/projects/AI4X/AI4X-Platform-dify/.venv/Scripts/python.exe -m pytest
```

当前基线测试结果：

- `9 passed`

### 7.4 CI

CI 文件位于：

- `.github/workflows/ci.yml`

CI 当前做两件事：

- 安装 `.[dev]` 依赖
- 执行 `pytest`

### 7.5 配置建议

业务层和端到端验收阶段建议使用：

- `OPENCTI_MCP_MOCK_MODE=false`
- `NOTIFICATION_MCP_PREVIEW_MODE=false`

并补充真实 OpenCTI GraphQL 地址、访问令牌和 SMTP 派发配置。

## 8. 后续建议

当前 README 对应的是“架构驱动下的最小可运行实现”。如果要继续向可联调系统推进，建议优先处理以下事项：

1. 在真实 Dify 环境导入并回归验证统一 YAML/DSL 资产。
2. 为 OpenCTI MCP 接入真实 GraphQL 查询和 Bundle 写回实现。
3. 为 Notification MCP 接入真实邮件或企业消息通道。
4. 补齐 SKILL 资产、Dify 导入校验与真实 E2E 场景回放。
