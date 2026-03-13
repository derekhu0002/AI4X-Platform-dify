# VS2-E2E 威胁运营与响应闭环端到端用户故事

> 前置依赖约定：本用户故事默认继承并遵循 [00_通用架构约束与工具规范.md](./00_通用架构约束与工具规范.md) 中关于 DIFY Agent、OPENCTI、Notification MCP 与 STIX 2.1 的统一约束。

## 1、概要

本故事面向情报分析师与 SOC 经理，描述告警进入系统后，DIFY Agent 如何编排 OPENCTI、处置知识和通知链路，将原始观测升级为可执行的事件响应闭环。核心目标是把处置过程中的每一步都固化为 STIX 对象与关系，确保后续复盘、二次检索和规则回灌都能复用。

## 2、执行全景图 (DIFY & OPENCTI 协作流)

```mermaid
sequenceDiagram
    actor Analyst as 情报分析师
    actor Consumer as 情报消费者(SOC经理)
    participant SIEM as SIEM/NDR
    participant Agent as DIFY Agent(ai4sec_agent)
    participant OpenCTIMCP as ai4sec_opencti_mcp
    participant CTI as OPENCTI Platform
    participant Notify as Notification MCP

    Analyst->>Agent: 预置告警分级、处置模板和升级阈值
    Note right of Analyst: 模板参数:\nIndicator{pattern, valid_from}\nCourse-of-Action{name, playbook_id}

    SIEM->>Agent: webhook 推送告警快照与流量证据
    Note right of SIEM: 输入事实:\nObserved-Data{first_observed, last_observed, number_observed}\nNetwork-Traffic{src_ref, dst_ref, protocols}\nIndicator{pattern_type, pattern}

    Agent->>OpenCTIMCP: 查询命中 IOC、攻击技战术和历史事件
    OpenCTIMCP->>CTI: 按对象与关系检索图谱
    CTI-->>OpenCTIMCP: 返回 Bundle{id, objects[]}
    Note left of CTI: 返回对象:\nAttack-Pattern{name, x_mitre_id}\nIntrusion-Set{name, aliases}\nIncident{name, severity}
    OpenCTIMCP-->>Agent: 返回处置上下文

    Agent->>Agent: 研判事件等级并生成响应动作
    Note right of Agent: 推理输出:\nIncident{name, severity, first_seen}\nCourse-of-Action{name, description, priority}

    Agent->>OpenCTIMCP: 写回事件档案与处置结果
    OpenCTIMCP->>CTI: 更新 Incident 与关联对象
    Note left of CTI: 输出对象:\nIncident{name, severity, status}\nNote{abstract, content}\nRelationship{relationship_type="related-to"}

    Agent->>Notify: 下发分诊结论、隔离动作和复盘摘要
    Notify-->>Consumer: 发送响应指令和证据链接
    Consumer->>CTI: 查看 Incident 时间线与关联图谱
```

## 3、故事：横向移动告警的运营与响应闭环

### 第一幕：告警快照进入 DIFY Agent

深夜时段，SIEM 检测到来自办公网段到生产跳板机的异常横向移动尝试，并通过 webhook 将 `Observed-Data{number_observed=17}`、`Network-Traffic{src_ref="host-A", dst_ref="bastion-01", protocols=["smb"]}` 和命中的 `Indicator{pattern="[ipv4-addr:value = '10.1.2.7']"}` 一并推送给 DIFY Agent。

### 第二幕：OPENCTI 提供事件上下文与可执行处置

DIFY Agent 通过 `ai4sec_opencti_mcp` 检索与该 IOC 相关的 `Attack-Pattern`、`Intrusion-Set` 和既有 `Incident`，发现该模式与一次历史横向移动活动高度相似。Agent 随即结合预置剧本生成新的 `Course-of-Action`，包括隔离主机、封禁 IOC、抓取关键内存证据和冻结高风险账号。

### 第三幕：SOC 经理接收结果并闭环回灌

系统把新建的 `Incident{name="possible-lateral-movement"}`、处置 `Note` 和相关 `Relationship` 写入 OPENCTI，再由 Notification MCP 把“已隔离、待复核、需复盘”的行动摘要同步给 SOC 经理。SOC 经理在 OPENCTI 中核查完整时间线，确认新产生的 IOC 是否需要转化为新的 `Indicator` 以回灌检测链路。
