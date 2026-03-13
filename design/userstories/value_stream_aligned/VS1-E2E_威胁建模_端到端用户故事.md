# VS1-E2E_威胁建模_端到端用户故事
> **前置依赖约定**：本用户故事默认继承并遵循 [00_通用架构约束与工具规范.md](./00_通用架构约束与工具规范.md) 中关于 DIFY Agent 与 OPENCTI 平台的核心操作模式，以及 STIX 2.1 与 Notification 的强制架构准则。

## 价值流视角
- 价值流：价值流 1：持续安全交付闭环

## 用户故事（跨流程）
- 作为：情报消费者（研发安全负责人等）与情报分析师
- 我希望：基于情报分析师配置的自动化流机制，系统通过持续不断的情报收集串联威胁建模到验证闭环
- 以便：作为情报消费者能实时提取安全验证基准数据，支撑修复证明

## 验收标准
1. 同一版本在闭环中具有统一追踪ID（可串联全部环节产物）。
2. 输出完整链路证据：`Attack-Pattern`、`测试报告/修复方案`。
3. 任一环节失败可阻断发布并给出可执行整改项。
4. 最终生成“可发布判定”与“残余风险说明”。

## SHOWCASE（端到端）
### 场景
支付系统 `v2.8.0` 准备上线，要求在 24 小时内完成全链路安全验证。

### 输入
- 系统组件与资产清单
- 合规条款文档
- 代码仓与依赖清单

### 执行链路
1. TARA 输出关键威胁与安全目标。

### 输出
威胁模型

### 业务价值


## 已验证的实现展示 (Verified End-to-End Implementation)

### 端到端数据流
```
输入 (Attack-Pattern, SRS@要求, 源代码, 依赖, 构建产物)
  ↓
BP1 (threat_model) → sdo:Attack-Pattern[], sdo:Identity[], sdo:Relationship(threatens)
  ↓
输出 (可发布判定 + 完整审计链)
```

### 业务操作流程图 (含 DIFY 与 OPENCTI 交互)
`mermaid
sequenceDiagram
    participant Pipeline as CI/CD 流水线 (触发端)
    participant Agent as DIFY Agent (ai4sec_agent)
    participant CTI as OPENCTI 平台 (STIX 数据汇聚底座)
    participant User as 各类情报消费者 (研发安全负责人)

    Pipeline->>Agent: webhook触发新版本的架构或代码提交
    Note right of Pipeline: 输入: 原始变更单、组件依赖或系统草图

    Agent->>CTI: (ai4sec_opencti_mcp) 检索组件匹配的历史威胁与风险漏洞
    Note right of Agent: 提取 STIX (输入):<br/>Software (依赖库), Vulnerability (CVE)<br/>Attack-Pattern (常见战术)
    CTI-->>Agent: 回传标准化 STIX 关联对象实体

    Agent->>Agent: 执行 TARA 分析, 在大模型处理内将历史情报映射到当期组件

    Agent->>CTI: (ai4sec_opencti_mcp) 落盘当前架构产生的威胁模型与消减控制项
    Note left of CTI: 生成 STIX (输出):<br/>Attack-Pattern (本地化演化的特定威胁)<br/>Course-of-Action (消减措施)<br/>Relationship (mitigates)
    
    Agent-->>User: 调度 Notification MCP 下发发布拦截/验收判定结论
    Note right of User: 消费者登录 OpenCTI 直接核实该 Bundle ID 下的审计链事实
`
