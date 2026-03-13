# VS1-E2E 持续安全交付闭环（端到端用户故事）

## 价值流视角
- 价值流：价值流 1：持续安全交付闭环

## 用户故事（跨流程）
- 作为：研发安全负责人（DevSecOps Owner）
- 我希望：系统从"威胁建模→验证修复"形成自动化闭环
- 以便：每次版本交付都具备可证明的安全基线与修复验证

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
2. 自动化验证通过修复，生成整改建议。

### 输出
- 发布判定：`Pass/Blocked`
- 证据包：威胁模型、测试报告、修复建议

### 业务价值
- 把“安全检查”变成“可追溯交付标准”，减少带病上线与返工。

## 已验证的实现展示 (Verified End-to-End Implementation)

### 用户交互流程
1. **BP - 威胁建模 TARA 分析:** 用户输入系统架构，系统生成 `sdo:Attack-Pattern[]` 与 `sdo:Identity[]` 关系

### 端到端数据流
```
输入 (Attack-Pattern, SRS@要求, 源代码, 依赖, 构建产物)
  ↓
BP1 (threat_model) → sdo:Attack-Pattern[], sdo:Identity[], sdo:Relationship(threatens)
  ↓
输出 (可发布判定 + 完整审计链)
```

### 关键指标
- **链路追踪ID:** 唯一 Bundle ID 串联全部环节
- **发布禁令:** 存在高危未闭环时自动阻断
- **残余风险:** 已识别但暂未修复的漏洞等级与数量

## 推荐的UX交互模式 (Recommended UX Interaction Pattern)
| 维度 | 建议 | 理由 |
|------|------|------|
| **整体视图** | **管道/流水线图 (Pipeline Visualization)** | 展示5个BP的串联流程，支持查看各阶段的中间产物 |
| **导航方式** | 点击管道中的任一阶段进入BP详情 | 支持快速跳转到特定阶段 |
| **追踪ID** | 显示贯穿全链的Bundle/Trace ID | 用户可追踪一个版本的完整安全审计链 |
| **输出展示** | **最终仪表板** | 显示"发布判定" (Pass/Blocked) 与完整证据包链接 |
| **关键指标** | 显示高危未闭环漏洞数、测试覆盖率等 | 一眼看出风险与交付状态 |

### 交互流程图 (Interaction Diagram)
```mermaid
sequenceDiagram
    participant User as DevSecOps Owner
    participant Pipeline as 安全交付流水线 (CI/CD)
    participant TM as 威胁建模 (Design Helper)
    participant Req as 需求生成 (Compliance)
    participant Scan as 代码检测 (SAST/SCA)
    participant Sign as 供应链验证
    participant Repair as 验证修复 (Auto-Fix)
    participant Engine as VS4:规则引擎 (Rule Gen)
    participant Graph as 知识图谱 (Neo4j)

    User->>Pipeline: 启动新版本(v2.8.0)设计开发
    activate Pipeline
    
    %% 1. 威胁建模 (Discovery Feedback Loop Start)
    note over Pipeline, TM: 1. 嵌入式安全设计 (Shift-Left)
    Pipeline->>TM: 提交架构设计草稿
    TM->>Graph: 🔥 查询历史威胁情报 (Attack Patterns)
    note right of TM: 包含 VS2/VS3 发现的\n真实攻击模式
    Graph-->>TM: 返回相关威胁 + 关联漏洞
    TM->>TM: 执行 TARA 威胁分析
    TM-->>Pipeline: 返回 安全设计约束 (Threat Model)
    Pipeline->>Graph: 存证 (BP1)
    
    %% VS4 联动
    note right of Graph: 触发 VS4 规则引擎\n生成环境感知检测规则
    Graph-->>Engine: 推送新增 Attack Pattern
    Engine->>Graph: 写入监测规则 (Internal-Rule)

    %% 2. 需求生成
    note over Pipeline, Req: 2. 动态需求映射
    Pipeline->>Req: 输入 Threat Model + 合规标准
    Req->>Graph: 查询 Mitigations / CoA
    Req->>Req: 映射生成 SRS 控制项
    Req-->>Pipeline: 返回 Course-of-Action[]
    Pipeline->>Graph: 存证 (BP2)

    %% 3. 代码检测
    note over Pipeline, Scan: 3. 落地检测
    Pipeline->>Scan: 扫描源代码 + 依赖
    Scan->>Graph: 关联已知 CVE / CWE
    Scan-->>Pipeline: 返回 Vulnerability[] + Affects
    Pipeline->>Graph: 存证 (BP3)

    %% 4. 供应链验证
    note over Pipeline, Sign: 4. 完整性验证
    Pipeline->>Sign: 输入 SBOM + 签名
    Sign-->>Pipeline: 返回 Integrity Report
    Pipeline->>Graph: 存证 (BP4)

    %% 5. 验证与修复
    note over Pipeline, Repair: 5. 闭环验证
    Pipeline->>Repair: 验证漏洞修复情况
    Repair-->>Pipeline: 返回 Test Report + Remediation
    Pipeline->>Graph: 存证 (BP5)

    Pipeline-->>User: 展示全链路验收报告 & 发布判定
    deactivate Pipeline
```

