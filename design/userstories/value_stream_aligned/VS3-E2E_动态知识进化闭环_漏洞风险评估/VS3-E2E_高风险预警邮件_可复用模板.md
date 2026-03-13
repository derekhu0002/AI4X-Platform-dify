# 高风险漏洞预警邮件模板

## 模板描述
这是一个可复用的高风险漏洞预警邮件模板，用于向系统负责人、安全团队和业务所有者发送漏洞风险评估结论和应急处置建议。该模板支持根据不同漏洞和影响面进行参数化定制。

---

## 邮件元数据

| 字段 | 值 |
|---|---|
| 发送人 | AIForSec Risk Assessment Engine <security-alerts@aiforeach.corp> |
| 收件人 | ${SECURITY_CHIEF_EMAIL}; ${BUSINESS_OWNER_EMAIL} |
| 抄送 | ${COMPLIANCE_OFFICER_EMAIL}; ${CTO_EMAIL} |
| 优先级 | ${PRIORITY} (取值: LOW/MEDIUM/HIGH/CRITICAL/CRITICAL+) |
| 分类标签 | Security, Risk Assessment, Vulnerability, Incident |
| 自动转发规则 | 若 CRITICAL+，自动转发给应急指挥中心和法务部门 |

---

## 邮件主题行模板

### 格式
```
${PRIORITY_EMOJI} ${PRIORITY_LABEL} [${CVE_ID}]: ${BRIEF_IMPACT} - 需要${URGENCY_ACTION}
```

### 示例
```
🚨 高风险安全预警 [CVE-2026-4141]: 支付网关审计能力受损 - 需要紧急修复
```

### 参数说明
| 参数 | 说明 | 示例 |
|---|---|---|
| `PRIORITY_EMOJI` | 根据优先级选择 emoji | 🚨 (CRITICAL+), ⚠️ (HIGH), 📢 (MEDIUM) |
| `PRIORITY_LABEL` | 中文优先级标签 | 高风险安全预警、中风险告警 |
| `CVE_ID` | CVE 编号 | CVE-2026-4141 |
| `BRIEF_IMPACT` | 简述在本系统中的影响 | 支付网关审计能力受损 |
| `URGENCY_ACTION` | 所需行动的紧急程度 | 紧急修复、立即关注、尽快计划 |

---

## 邮件正文结构

### 第一部分：风险评估摘要

```markdown
亲爱的安全和业务负责人，

系统在 ${DETECTION_TIMESTAMP} 检测到一个${PRIORITY_LABEL}的风险，需要您立即采取行动。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 风险评估结论
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【漏洞编号】${CVE_ID}
【漏洞标题】${VULNERABILITY_TITLE}
【漏洞描述】${VULNERABILITY_DESCRIPTION}
【外部评级】CVSS ${EXTERNAL_CVSS_SCORE} (${EXTERNAL_SEVERITY})
【本系统风险等级】${FINAL_RISK_LEVEL}
【评估时间】${ASSESSMENT_TIMESTAMP}

### 为什么${EXTERNAL_SEVERITY}漏洞在我们系统中升级为${FINAL_RISK_LEVEL}？

我们的系统在内部资产上下文中识别出以下信息：

**受影响的产品**：${AFFECTED_PRODUCT_NAME}
**受影响的组件**：${AFFECTED_COMPONENT_NAME}（${DEPENDENCY_NAME} ${DEPENDENCY_VERSION}）
**组件功能**：${COMPONENT_FUNCTIONS}
**组件关键度**：⭐⭐⭐⭐⭐ (CRITICAL - ${CRITICALITY_REASON})

**漏洞在本系统的影响推理**：

${IMPACT_REASONING_CHAIN}
```

### 参数说明

| 参数 | 说明 | 示例 |
|---|---|---|
| `DETECTION_TIMESTAMP` | 检测到漏洞的时间 | 2026-03-15 09:30 UTC+8 |
| `PRIORITY_LABEL` | 优先级标签 | 高风险 |
| `CVE_ID` | CVE 编号 | CVE-2026-4141 |
| `VULNERABILITY_TITLE` | 漏洞官方标题 | Improper Logging in log4j-core 2.19.0 |
| `VULNERABILITY_DESCRIPTION` | 技术描述（1-2 句） | log4j-core 版本 2.19.0 中存在日志记录不充分缺陷... |
| `EXTERNAL_CVSS_SCORE` | 外部评定分数 | 3.5 |
| `EXTERNAL_SEVERITY` | 外部评定等级 | 低危 |
| `FINAL_RISK_LEVEL` | 本系统评定风险等级 | CRITICAL+ |
| `ASSESSMENT_TIMESTAMP` | 评估完成时间 | 2026-03-15 01:35 UTC+8 |
| `AFFECTED_PRODUCT_NAME` | 受影响产品名 | 支付网关服务 |
| `AFFECTED_COMPONENT_NAME` | 受影响组件名 | 交易日志模块 |
| `DEPENDENCY_NAME` | 依赖库名 | log4j-core |
| `DEPENDENCY_VERSION` | 依赖版本 | v2.19.0 |
| `COMPONENT_FUNCTIONS` | 组件功能列表 | 记录所有支付交易、记录失败日志、支持审计... |
| `CRITICALITY_REASON` | 为何组件关键 | 业务最核心资产，直接处理用户资金 |
| `IMPACT_REASONING_CHAIN` | 推理链说明 | （见下方详细模板） |

### 第二部分：影响推理链

```markdown
1️⃣ [技术影响] ${TECHNICAL_IMPACT}
   → ${TECHNICAL_CONSEQUENCE}

2️⃣ [资产影响] ${ASSET_IMPACT}
   → ${ASSET_CONSEQUENCE}

3️⃣ [暴露面] ${EXPOSURE_DETAIL}
   → ${EXPOSURE_CONSEQUENCE}

4️⃣ [最终风险] ${FINAL_RISK_DESCRIPTION}
   → ${FINAL_CONCLUSION}
```

#### 推理链参数

| 参数 | 说明 | 示例 |
|---|---|---|
| `TECHNICAL_IMPACT` | 漏洞的直接技术影响 | 日志记录不充分 |
| `TECHNICAL_CONSEQUENCE` | 技术影响的后果 | 审计日志缺失或不完整 |
| `ASSET_IMPACT` | 对资产的影响 | 支付网关直接处理用户资金转移 |
| `ASSET_CONSEQUENCE` | 资产受影响的后果 | 审计日志缺失 = 无法追踪交易 |
| `EXPOSURE_DETAIL` | 暴露面分析 | 支付网关直接面向互联网 |
| `EXPOSURE_CONSEQUENCE` | 暴露导致的后果 | 攻击面广阔，恶意行为人易接近 |
| `FINAL_RISK_DESCRIPTION` | 综合风险描述 | 恶意行为人可能通过伪造或绕过日志来隐藏欺诈交易 |
| `FINAL_CONCLUSION` | 最终结论 | 本系统的检测和追踪能力受损 |

---

### 第三部分：立即消减措施

```markdown
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔧 立即消减措施
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【优先级】${REMEDIATION_PRIORITY}

${REMEDIATION_STEPS}
```

#### 修复步骤模板 - 渐进式改进

```markdown
1. **${REMEDIATION_TITLE_1}**
   - 目标：${REMEDIATION_GOAL_1}
   - 受影响模块：${AFFECTED_MODULE_1}
   - 预计时间：${ESTIMATED_TIME_1}
   - 测试范围：${TEST_SCOPE_1}

2. **${REMEDIATION_TITLE_2}**
   - 目标：${REMEDIATION_GOAL_2}
   - 受影响模块：${AFFECTED_MODULE_2}
   - 预计时间：${ESTIMATED_TIME_2}
   - 测试范围：${TEST_SCOPE_2}

3. **临时缓解（升级前）**
   - ${TEMPORARY_MITIGATION_1}
   - ${TEMPORARY_MITIGATION_2}
   - ${TEMPORARY_MITIGATION_3}

4. **验证步骤**
   \`\`\`bash
   ${VERIFICATION_COMMAND_1}
   ${VERIFICATION_COMMAND_2}
   \`\`\`
```

---

### 第四部分：监控与检测措施

```markdown
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📡 监控与检测措施
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

系统已启动以下持续监控，直到漏洞被修复：

✅ **${DETECTION_RULE_1_NAME}**
- ${DETECTION_RULE_1_DESCRIPTION}

✅ **${DETECTION_RULE_2_NAME}**
- ${DETECTION_RULE_2_DESCRIPTION}

✅ **${DETECTION_RULE_3_NAME}**
- ${DETECTION_RULE_3_DESCRIPTION}

✅ **监控仪表盘**
- 实时监控地址：${MONITORING_DASHBOARD_URL}
- 预警阈值：${ALERT_THRESHOLD}
```

---

### 第五部分：附件与证据链

```markdown
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📚 附件：证据链
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【追踪 ID】${ASSESSMENT_TRACKING_ID}
【风险评估报告】${RISK_REPORT_URL}
【STIX 数据模型】${STIX_DATA_URL}
【应急处置时间窗口】${REMEDIATION_TIME_WINDOW}

评估人员：AIForSec 自动化风险引擎
评估依据：STIX 2.1 威胁情报标准 + 内部资产图谱
下次评估：升级验证后自动触发再评估
```

---

### 第六部分：页脚与后续行动

```markdown
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**如果您有任何疑问，请回复此邮件或登录平台查看详细分析。**

---

**后续行动清单**:
- [ ] 收到邮件并理解风险等级
- [ ] 登录平台查看详细证据链（链接：${PLATFORM_LOGIN_URL}）
- [ ] 根据消减措施启动内部流程
- [ ] 在${REMEDIATION_TIME_WINDOW}前完成修复
- [ ] 向平台报告"漏洞已修复"以触发重新评估

**联系方式**:
- 安全响应热线：${SECURITY_HOTLINE}
- 24/7 应急值班：${EMERGENCY_ON_CALL}
- 技术支持邮箱：${TECHNICAL_SUPPORT_EMAIL}
```

---

## 参数化配置示例

### 示例 1：高风险数据库注入漏洞

```yaml
CVE_ID: CVE-2026-4142
PRIORITY: CRITICAL
AFFECTED_PRODUCT: 用户管理系统 (User Management Service)
AFFECTED_COMPONENT: 用户查询接口 (User Query API)
DEPENDENCY_NAME: ORM库 (Hibernate)
DEPENDENCY_VERSION: v5.3.0
EXTERNAL_CVSS_SCORE: 6.5
FINAL_RISK_LEVEL: CRITICAL+
REMEDIATION_PRIORITY: P0
ESTIMATED_TIME: 2 小时
```

### 示例 2：中风险认证绕过漏洞

```yaml
CVE_ID: CVE-2026-4143
PRIORITY: HIGH
AFFECTED_PRODUCT: 单点登录系统 (SSO Service)
AFFECTED_COMPONENT: Token 验证模块 (Token Validation)
DEPENDENCY_NAME: JWT库 (java-jwt)
DEPENDENCY_VERSION: v3.8.0
EXTERNAL_CVSS_SCORE: 5.3
FINAL_RISK_LEVEL: HIGH
REMEDIATION_PRIORITY: P1
ESTIMATED_TIME: 4 小时
```

---

## HTML 邮件模板（可选）

该模板也可导出为 HTML 版本，便于在邮件客户端中呈现更好的视觉效果。

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: #333; }
        .container { max-width: 900px; margin: 0 auto; padding: 20px; }
        .header { background-color: #d32f2f; color: white; padding: 20px; border-radius: 5px; }
        .section { margin: 20px 0; border-left: 4px solid #2196F3; padding: 15px; background-color: #f5f5f5; }
        .critical { border-left-color: #d32f2f; background-color: #ffebee; }
        .warning { border-left-color: #ff9800; background-color: #fff3e0; }
        .info { border-left-color: #2196F3; background-color: #e3f2fd; }
        .cta { background-color: #2196F3; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; }
        table { width: 100%; border-collapse: collapse; margin: 10px 0; }
        th, td { border: 1px solid #ddd; padding: 10px; text-align: left; }
        th { background-color: #f0f0f0; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>${PRIORITY_EMOJI} ${PRIORITY_LABEL} 安全预警</h1>
            <p>${CVE_ID}: ${BRIEF_IMPACT}</p>
        </div>
        
        <div class="section critical">
            <h2>📋 风险评估结论</h2>
            <table>
                <tr><th>漏洞编号</th><td>${CVE_ID}</td></tr>
                <tr><th>本系统风险等级</th><td><strong>${FINAL_RISK_LEVEL}</strong></td></tr>
                <tr><th>评估时间</th><td>${ASSESSMENT_TIMESTAMP}</td></tr>
            </table>
        </div>
        
        <div class="section warning">
            <h2>🔧 立即消减措施</h2>
            ${REMEDIATION_STEPS_HTML}
        </div>
        
        <div class="section info">
            <h2>📡 监控与检测</h2>
            ${MONITORING_DETAIL_HTML}
        </div>
    </div>
</body>
</html>
```

---

## 交付物检查清单

| 检查项 | 状态 |
|---|---|
| ✅ 邮件主题行格式清晰，优先级标记明显 | 完成 |
| ✅ 风险评估结论包含完整的推理链条 | 完成 |
| ✅ 消减措施可操作，包含验证步骤 | 完成 |
| ✅ 监控规则具体，包含告警方式 | 完成 |
| ✅ 证据链完整，可追溯 | 完成 |
| ✅ 支持参数化定制 | 完成 |
| ✅ 包含 HTML 备选版本 | 完成 |

---

## 使用说明

1. **配置参数**：根据实际漏洞和影响面填写上表中的所有参数
2. **生成邮件**：使用模板引擎（如 Jinja2, Handlebars）进行渲染
3. **审核**：安全团队审核内容确保准确性和完整性
4. **发送**：通过邮件系统发送给相应的收件人
5. **追踪**：保存邮件追踪 ID，便于后续查询和回溯

注：该模板可定期更新以适应新的威胁情景和组织政策变化。

