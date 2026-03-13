# VS2-E2E 威胁运营与响应闭环（端到端用户故事）

> **前置依赖约定**：本用户故事默认继承并遵循 [00_通用架构约束与工具规范.md](./00_通用架构约束与工具规范.md) 中关于 DIFY Agent 与 OPENCTI 平台的核心操作模式，以及 STIX 2.1 与 Notification 的强制架构准则。

## 价值流视角
- 价值流：价值流 2：威胁运营与响应闭环

## 用户故事（跨流程）
- 作为：情报消费者（如 SOC 经理）与情报分析师
- 我希望：借助情报分析师的智能规则定义与处置流，将事件溯源处置全流程纳入自动化
- 以便：情报消费者消费预判结果快速闭环，并将反馈提取为新维度情报回灌提升检出率

## 验收标准
1. 从 `Observed-Data/Network-Traffic` 可生成 `Incident` 并触发处置。
2. 处置阶段输出 `Course-of-Action` 与 IR 报告。
3. 复盘阶段产出新 `Indicator`/`Attack-Pattern` 并回灌检测环节。
4. 可量化闭环指标：告警到处置耗时、处置成功率、回灌命中率。

## SHOWCASE（端到端）
### 场景
凌晨出现可疑横向移动，值班团队需在 30 分钟内完成遏制与初步复盘。

### 输入
- SIEM 日志与流量快照
- 外部威胁指标（Indicator）

### 执行链路
1. 自动分类识别高危 Sighting，并升级为 Incident。
2. 编排执行隔离主机、封禁 IOC、收集取证。
3. 输出 IR 报告与时间线。
4. 复盘提炼出 2 个新 IOC 与 1 条 TTP，回灌检测策略。

### 输出
- 处置状态：`Contained`
- 回灌状态：`Enabled`
- 关键指标：MTTD 下降、MTTR 下降

### 业务操作流程图 (含 DIFY 与 OPENCTI 交互)
`mermaid
sequenceDiagram
    participant SIEM as NDR/SIEM 集成 (外部触发)
    participant Agent as DIFY Agent (ai4sec_agent 编排大脑)
    participant CTI as OPENCTI 平台 (STIX 响应底座)
    participant SOC as 各类情报消费者 (SOC 经理)

    SIEM->>Agent: (通过预置模板 webhook) 推送安全警报快照
    Note right of SIEM: 输入: 警报描述、可疑流量和资产IP
    
    Agent->>CTI: (ai4sec_opencti_mcp) 落盘前置目击并查询上下文
    Note right of Agent: 提取/录入 STIX (输入):<br/>Observed-Data (流量快照)<br/>Indicator (IoC 匹配)
    
    CTI-->>Agent: 下发已知的高阶 APT Attack-Pattern 与 关联黑库资产
    
    Agent->>Agent: 智能流决策大模型推演遏制策略 (自动化封禁或隔离判定)
    
    Agent->>CTI: (ai4sec_opencti_mcp) 更新防御记录并建立事件档案
    Note left of CTI: 回储 STIX (输出):<br/>Incident (确认的高危事件)<br/>Course-of-Action (响应实施表)
    
    Agent-->>SOC: (Notification MCP) 发送响应分诊研判公报与复盘结论报告
    Note right of SOC: SOC 经理可通过 OpenCTI 的关联图谱反哺产出全新的威胁画像
`
