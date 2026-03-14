# 测试环境搭建指导

## 1. 适用范围

本指导用于业务层人工验收测试。目标是让测试人员在个人 PC 上准备好 Dify、OpenCTI、OpenCTI MCP、Notification MCP，以及本目录下的 STIX Bundle 测试数据。

## 2. 前置要求

- 已安装 Docker Desktop。
- 已获取本仓库代码。
- 仓库根目录 Python 虚拟环境 `.venv` 可用。
- 以下环境文件存在并已按本地环境调整：
  - `externalDify/.env`
  - `external_opencti/.env`

## 3. 启动 OpenCTI

在仓库根目录执行：

```powershell
Set-Location external_opencti
docker compose up -d
```

检查点：

- 打开 `http://localhost:8080/dashboard`。
- OpenCTI 能正常登录。
- 平台导入功能可用，后续用于导入本目录下的 STIX Bundle 文件。

## 4. 启动 Dify

在仓库根目录执行：

```powershell
Set-Location externalDify
docker compose up -d
```

检查点：

- 打开 `http://localhost/apps`。
- Dify 前台页面可访问。
- 用于本项目的工作流资产已导入，或已有等效场景入口可供测试。

## 5. 启动 MCP 服务

在仓库根目录执行：

```powershell
d:/projects/AI4X/AI4X-Platform-dify/.venv/Scripts/python.exe -m uvicorn mcp.opencti_mcp.app.main:app --host 0.0.0.0 --port 8101
```

```powershell
d:/projects/AI4X/AI4X-Platform-dify/.venv/Scripts/python.exe -m uvicorn mcp.notification_mcp.app.main:app --host 0.0.0.0 --port 8102
```

检查点：

- `http://localhost:8101/health` 可访问。
- `http://localhost:8102/health` 可访问。
- 若 Dify 运行在 Docker Desktop 容器中，工作流 HTTP 节点访问 MCP 时不能使用 `localhost`，应使用 `host.docker.internal`。

## 6. 导入 Dify 工作流

如测试环境尚未导入本项目工作流，请在 Dify 中导入以下资产：

- `DifyAgentWorkflow/ai4sec_unified_workflow.yaml`

导入后核对以下变量或等效配置：

- `OPENCTI_MCP_URL=http://host.docker.internal:8101`
- `NOTIFICATION_MCP_URL=http://host.docker.internal:8102`

说明：

- 浏览器和宿主机健康检查仍使用 `http://localhost:8101/health`、`http://localhost:8102/health`。
- 但 Dify 工作流中的 HTTP 节点运行在容器内，因此访问宿主机上的 MCP 时需要使用 `host.docker.internal`；否则会出现 `Reached maximum retries (0) for URL http://localhost:8101/query` 之类的连接错误。

## 7. 导入测试数据

在 OpenCTI 导入功能中依次导入以下文件：

- `tests/validation/test-data/vs1-payment-threat-model-bundle.json`
- `tests/validation/test-data/vs2-lateral-movement-bundle.json`
- `tests/validation/test-data/vs3-zero-day-impact-bundle.json`
- `tests/validation/test-data/vs4-bola-monitoring-bundle.json`

导入完成后，按 [00-virtual-test-data.md](./00-virtual-test-data.md) 中的核验点检查对象与关系是否可见。

## 8. 测试账号占位符

- `ANALYST_ACCOUNT`：情报分析师测试账号
- `ROLE_SHARED_ACCOUNT`：业务负责人、安全负责人、管理层、安全运营团队共用测试账号

## 9. 环境就绪判定

满足以下条件即可开始执行 capability 用例：

- Dify 可访问。
- OpenCTI 可访问。
- OpenCTI MCP 与 Notification MCP 健康检查通过。
- 4 个 STIX Bundle 已导入。
- 测试账号已分配或可用占位符临时记录。