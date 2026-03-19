# AI4SEC 平台实现说明

## 1. 项目概览

AI4SEC 是一个围绕安全情报生产、消费与闭环运营构建的多层架构系统。当前仓库基于战略动机层、业务层、应用层和技术层设计，保留了两条最小可运行的 Dify 工作流资产：一条用于 OpenCTI webhook 驱动的漏洞影响分析，一条用于报告驱动的 VS1 威胁建模。统一入口 `ai4sec_agent`、`ai4sec_opencti_mcp` 和 `Notification MCP` 运行时资产已于 2026-03-19 从仓库实现中退役。

当前实现重点覆盖以下交付：

- 一条 OpenCTI webhook 驱动的 Dify Workflow 资产。
- 一条独立 VS1 Threat Modeling Dify Workflow 资产。
- 覆盖保留交付资产的自动化验证基线。
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
- Dify 是当前唯一保留的智能编排平台，但入口已演化为多工作流拓扑而非统一入口。
- 标准化通知出口仍是架构目标，但当前仓库内未保留独立 Notification MCP 运行时实现。

### 2.2 业务层

业务层将价值流落成统一业务闭环，核心角色包括：

- 情报分析师：主导任务受理、研判和知识沉淀。
- 业务负责人：确认业务影响、窗口期和业务约束。
- 安全负责人：审批高风险治理动作和升级动作。
- 管理层：消费企业级摘要并做资源决策。
- 安全运营团队：执行监控和响应动作，并反馈命中结果。

业务层视角下，系统需要持续支撑：任务受理、上下文归并、风险研判、响应编排、通知协同和知识回灌。

### 2.3 应用层

应用层把业务能力映射为 Dify 场景工作流与 webhook 入口：

- Dify 作为用户交互和工作流编排平台。
- `ai4sec_threat_modeling_workflow.yaml` 作为独立 VS1 威胁建模入口。
- `ai4sec_opencti_webhook_workflow.yaml` 作为 OpenCTI webhook 驱动的漏洞影响分析入口。
- 两条保留工作流都直接访问 OpenCTI GraphQL，不再经过仓库内 MCP 服务。

当前仓库不再保留统一工作流，而是以多入口保留资产对应具体场景：

- VS1 由独立 Threat Modeling Workflow 承载。
- 漏洞推送由 OpenCTI webhook Workflow 承载。
- VS2 / VS4 的统一编排与标准化通知出口当前在仓库内显式缺失。

### 2.4 技术层

技术层当前目标为单机开发测试环境，推荐运行形态是：

- `external_opencti/` 负责 OpenCTI 及其依赖容器。
- `externalDify/` 负责 Dify 及其依赖容器。
- 仓库内保留的 Workflow 通过 Dify 直接访问 OpenCTI GraphQL。
- `mcp/` 目录仅保留退役兼容命名空间，不再包含可启动的服务实现。
- 本地 Python 虚拟环境用于测试执行与仓库级辅助脚本。

## 3. 当前实现映射

### 3.1 目录说明

- `design/`: 四层架构设计文档、用户故事、任务索引和架构模型。
- `DifyAgentWorkflow/`: 当前保留的 Dify Workflow 资产。
- `mcp/`: 已退役 MCP 的兼容命名空间，当前不含可运行服务。
- `external_opencti/`: OpenCTI 本地容器编排文件。
- `externalDify/`: Dify 本地容器编排文件。
- `tests/`: 自动化测试，按 unit、contract、integration、e2e 分层。
- `.github/workflows/`: CI 配置。

### 3.2 已实现组件

#### OpenCTI Webhook Workflow

文件：`DifyAgentWorkflow/ai4sec_opencti_webhook_workflow.yaml`

实现内容：

- 定义 OpenCTI webhook 驱动的 Dify Workflow。
- 通过 HTTP 请求节点直接访问 `OPENCTI_GRAPHQL_URL`。
- 对漏洞相关基础设施做一跳关系分析，并输出结构化风险结论。
- 当前结果以内联结构化输出返回，不经过仓库内独立通知服务。

#### standalone VS1 Threat Modeling 工作流

文件：`DifyAgentWorkflow/ai4sec_threat_modeling_workflow.yaml`

实现内容：

- 定义独立 VS1 `advanced-chat` 应用，支持输入报告名称或报告 ID 发起威胁建模。
- 通过 `Resolve Report Reference` 节点合并显式输入与 `sys.query`，统一生成 `report_ref`。
- 通过代码节点和 HTTP/GraphQL 查询直接访问 OpenCTI，获取过滤后的 STIX 2.1 bundle 与分析输入。
- 通过 LLM 结构化输出节点生成威胁建模 JSON，并在会话中输出下载链接。
- 已修复运行时缺陷：变量插值节点命名兼容（下划线 ID）与 LLM 输出 Markdown fence 解析兼容。

#### 已退役兼容命名空间

目录：`mcp/opencti_mcp/`、`mcp/notification_mcp/`、`DifyAgentWorkflow/tools/`

当前状态：

- 目录仅保留命名空间与缓存残留，不再包含可启动的 MCP 服务或统一入口工具代码。
- 仓库内不再提供 `OPENCTI_MCP_URL`、`NOTIFICATION_MCP_URL` 对应的运行时实现。
- 如需恢复统一入口或通知服务，应视为新一轮实现任务，而不是当前资产的一部分。

## 4. 系统实现方案

### 4.1 主链路

当前系统实现方案遵循“OpenCTI 先收敛，Dify 工作流直接查询，再返回结构化结果”的顺序：

1. 外部情报、CI/CD 变更、SIEM 告警等先进入 OpenCTI。
2. OpenCTI 通过 webhook 触发保留的漏洞分析 Workflow，或由分析师在 Dify 中手动启动 VS1 Threat Modeling Workflow。
3. 保留工作流直接使用 `OPENCTI_GRAPHQL_URL` 和 `OPENCTI_ADMIN_TOKEN` 查询所需 STIX 上下文。
4. 工作流在 Dify 会话内或 webhook 响应中返回结构化分析结果。
5. 仓库内当前不再包含统一入口、多场景路由、MCP 写回链路和 Notification MCP 发送链路。

### 4.2 分层实现原则

- Progressive Disclosure：上层只看场景与业务结果，下层才暴露投影、写回和通知细节。
- Separation of Concerns：工作流、MCP、通知、测试和容器编排分目录实现，避免耦合。
- STIX First：主业务载荷不引入与 STIX 无关的核心数据模型。

### 4.3 当前实现边界

当前仓库已经具备最小可运行交付，但仍保留以下边界：

- 仓库内不再提供可本地启动的 OpenCTI MCP 或 Notification MCP 服务。
- 两条保留 Workflow 都要求在 Dify 环境内配置 `OPENCTI_GRAPHQL_URL` 与 `OPENCTI_ADMIN_TOKEN`。
- OpenCTI webhook Workflow 当前只返回结构化风险输出，不负责通知升级。
- VS1 standalone workflow 已完成关键运行时缺陷修复（变量插值解析与 LLM JSON fence 解析），但最终 Dify UI 全链路验收仍依赖环境侧人工复核。
- 统一入口 `ai4sec_agent`、统一工作流和共享运行时工具已退役，VS2 / VS4 的通用编排能力需后续重新建模与实现。

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

### 5.2.1 环境变量配置

项目根目录 `.env` 不再作为已退役 MCP 服务的统一配置入口。当前保留的两条 Workflow 需要在 Dify 应用环境或其容器环境中配置以下变量：

建议先复制模板文件：

```powershell
Copy-Item .env.example .env
```

建议至少提供如下真实联调参数：

```dotenv
OPENCTI_GRAPHQL_URL=http://host.docker.internal:8080/graphql
OPENCTI_ADMIN_TOKEN=<你的OpenCTI令牌>
```

如果 Dify 运行在 Docker Desktop 容器中，通常需要使用 `host.docker.internal` 指向宿主机上的 OpenCTI GraphQL 入口。

### 5.3 当前无需启动仓库内 MCP 服务

统一入口和双 MCP 服务已从仓库运行时移除，因此当前无需在本地启动 `mcp.opencti_mcp` 或 `mcp.notification_mcp`。

### 5.4 导入 Dify 工作流

将以下资产导入 Dify：

- `DifyAgentWorkflow/ai4sec_threat_modeling_workflow.yaml`
- `DifyAgentWorkflow/ai4sec_opencti_webhook_workflow.yaml`

导入后需确认：

- `OPENCTI_GRAPHQL_URL` 指向可达的 OpenCTI GraphQL 入口
- `OPENCTI_ADMIN_TOKEN` 已在 Dify 环境中配置
- Webhook Workflow 的入口地址已在 OpenCTI 侧完成配置

说明：当 Dify 运行在 Docker Desktop 容器中时，工作流 HTTP 节点里的 `localhost` 指向容器本身，而不是宿主机，因此访问宿主机上的 OpenCTI 通常需要使用 `host.docker.internal`。

### 5.5 启动外部平台容器

如需本地启动 OpenCTI 与 Dify 平台，可使用仓内现成容器文件：

- OpenCTI: `external_opencti/docker-compose.yml`
- Dify: `externalDify/docker-compose.yaml`

建议分别在对应目录执行 Docker Compose 命令，并根据本地环境完善 `.env`。

## 6. 使用指南

### 6.1 场景入口

当前仓库保留的入口如下：

- VS1 Threat Modeling Workflow：面向报告驱动的威胁建模分析。
- OpenCTI Webhook Workflow：面向漏洞推送后的影响分析和风险评分。

### 6.2 Webhook 使用

当前实现保留了 OpenCTI 到 Dify 的 webhook 驱动分析基线：

- 入口由导入后的 `ai4sec_opencti_webhook_workflow.yaml` 暴露。
- Workflow 直接依赖 `OPENCTI_GRAPHQL_URL` 与 `OPENCTI_ADMIN_TOKEN`。
- 当前结果以结构化分析输出返回，不附带仓库内通知分发。

### 6.3 OpenCTI 直接查询

当前两条 Workflow 通过 Dify 节点直接访问 OpenCTI GraphQL，而不是调用仓库内 MCP 查询接口。

典型使用方式：

- Threat Modeling Workflow 会根据 `report_ref` 查询相关 STIX 2.1 对象与关系，并输出结构化威胁建模结果。
- Webhook Workflow 会围绕漏洞对象做一跳关联分析并生成风险分数、严重级别和业务影响摘要。

### 6.4 通知出口现状

统一 Notification MCP 已退役。当前仓库中的保留 Workflow 不会直接发送邮件或调用标准化通知服务；如需通知协同，应作为后续独立实现任务恢复。

## 7. 开发指南

### 7.1 推荐开发流程

1. 先更新 `design/` 中的架构或任务上下文。
2. 再调整 `DifyAgentWorkflow/` 中的保留 YAML/DSL 资产。
3. 若需恢复统一入口或通知服务，将其作为独立新增实现而非修改现有保留工作流。
4. 最后补齐 `tests/` 中与保留资产或新增运行时对应的测试。

### 7.2 测试分层

- `tests/unit/`: 面向纯函数和服务逻辑。
- `tests/contract/`: 保留接口/合同测试目录，当前与已退役 MCP 直接相关的测试已移除。
- `tests/integration/`: 保留集成测试目录，统一入口与通知链路相关测试已移除。
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

- `OPENCTI_GRAPHQL_URL=<可达的OpenCTI GraphQL地址>`
- `OPENCTI_ADMIN_TOKEN=<可用的OpenCTI令牌>`

并在 Dify 侧补充对应环境变量。SMTP 与 Notification MCP 配置不再属于当前仓库运行时要求。

## 8. 后续建议

当前 README 对应的是“统一入口与双 MCP 已退役后的最小可运行实现”。如果要继续向更完整的可联调系统推进，建议优先处理以下事项：

1. 在真实 Dify 环境导入并回归验证两条保留 Workflow 资产。
2. 重新建模 VS2 / VS4 的运行时入口与输出链路，决定是否恢复统一入口。
3. 如业务仍需要标准化通知出口，按新边界重新实现通知服务而不是恢复旧 MCP 描述。
4. 补齐更广的回归测试、Dify 导入校验与真实 E2E 场景回放。
