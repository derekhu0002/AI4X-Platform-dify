# Business Process Design Guide (业务流程设计指南)

## 1. 概述 (Overview)
本指南定义了在 **AI Security Platform** 中设计一个新的业务流程 (Business Process, BP) 的标准方法论。
所有的业务流程必须严格遵循 **"Value Stream -> Business Process -> User Story -> STIX Objects"** 的层级结构，确保业务价值清晰且技术实现可落地。

## 2. 设计步骤 (Design Steps)

### Step 1: 价值流对齐 (Value Stream Alignment)
首先，确定你的新流程属于哪一条核心价值流：
- **VS1 持续安全交付**: 关注代码、构建与发布 (Design -> Build -> Deploy)。
- **VS2 威胁运营与响应**: 关注检测、响应与复盘 (Detect -> Respond -> Recover)。
- **VS3 动态知识进化**: 关注情报、知识与预警 (Ingest -> Enrich -> Predict)。
- **VS4 环境感知监控**: 关注从设计到监控的转化 (Model -> Monitor)。

### Step 2: 定义用户故事 (Define User Story)
使用标准的 Agile User Story 格式：
> **As a** (Role / 角色)
> **I want to** (Action / 动作)
> **So that** (Benefit / 价值)

同时，明确该流程的输入与输出对象（必须映射到 STIX 2.1）：
- **Input**: 流程启动需要的数据 (e.g., `sdo:Software`, `sdo:Indicator`)。
- **Output**: 流程产生的价值资产 (e.g., `sdo:Vulnerability`, `sdo:Course-of-Action`)。

### Step 3: 制定验收标准 (Acceptance Criteria)
列出 3-5 条可验证的验收标准 (AC)。
*包含 UX 交互要求与数据持久化要求。*

### Step 4: 设计交互模式 (UX Pattern)
定义用户如何在 ChatConsole 或 GUI 中与该流程交互。
- **Input Mode**: 表单? 对话? 文件上传?
- **Visualization**: 列表? 图谱? 时间轴?
- **Feedback Loop**: 用户如何确认或反馈结果?

### Step 5: 数据架构映射 (Data Architecture)
明确该流程涉及的核心 STIX 对象及其关系。
例如: `Attack-Pattern` --(targets)--> `Software`。

---

## 3. 模板 (Template)

请在 `design/userstories/value_stream_aligned/` 目录下创建新文件，命名规则：`VS{X}-BP{Y}_{Name}.md`。

```markdown
# VS{X}-BP{Y} {Process Name}

## 对应关系
- 价值流：{Value Stream Name}
- Business Process：{Process Name}

## 用户故事
- 作为：{Role}
- 我希望：{Action}
- 以便：{Benefit}

## 验收标准
1. 输入 {Input Object} 后，输出 {Output Object}。
2. {Specific Logic or Requirement}.
3. 结果保存为 {STIX Object} 写入知识图谱。

## SHOWCASE
- 场景：{Real-world scenario description}
- 输入：`{Concrete Input Data}`
- 输出：`{Concrete Output Data}`
- 业务价值：{Business Value Statement}

## 推荐的UX交互模式
| 维度 | 建议 | 理由 |
|------|------|------|
| **输入方式** | ... | ... |
| ... | ... | ... |
```

## 4. 评审清单 (Checklist)
- [ ] 是否明确归属于单一价值流?
- [ ] 输入输出是否使用了 STIX 2.1 标准对象?
- [ ] 是否定义了与其他 BP 的上下游关系?
- [ ] 是否包含具体的 SHOWCASE 示例?
- [ ] UX 设计是否符合 "AI-First" 原则 (自动化优先，人工辅助)?
