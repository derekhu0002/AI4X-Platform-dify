# 用户故事（价值闭环对齐版）

[⬅️ 返回主文档 (Back to Main)](../../../../README.md)

本目录仅保留与知识图谱中 **Value Stream + Business Process** 一一对应的核心用户故事（精简版，不额外扩展）。

来源：
- [design/KG/SystemArchitecture.json](../../KG/SystemArchitecture.json)

## 价值流 1：持续安全交付闭环
0. [VS1-E2E 持续安全交付闭环 端到端用户故事](VS1-E2E_%E6%8C%81%E7%BB%AD%E5%AE%89%E5%85%A8%E4%BA%A4%E4%BB%98%E9%97%AD%E7%8E%AF_%E7%AB%AF%E5%88%B0%E7%AB%AF%E7%94%A8%E6%88%B7%E6%95%85%E4%BA%8B.md)
1. [BP 威胁建模 TARA 分析](../business_processes/BP_威胁建模_TARA分析.md)
2. [BP 验证与修复 自动化测试与修复](../business_processes/BP_验证与修复_自动化测试与修复.md)

## 价值流 2：威胁运营与响应闭环
0. [VS2-E2E 威胁运营与响应闭环 端到端用户故事](VS2-E2E_%E5%A8%81%E8%83%81%E8%BF%90%E8%90%A5%E4%B8%8E%E5%93%8D%E5%BA%94%E9%97%AD%E7%8E%AF_%E7%AB%AF%E5%88%B0%E7%AB%AF%E7%94%A8%E6%88%B7%E6%95%85%E4%BA%8B.md)
6. [BP 态势感知 日志聚合与监控_威胁研判自动化分类](../business_processes/BP_态势感知_日志聚合与监控_威胁研判自动化分类.md)
7. [BP 应急响应 编排处置](../business_processes/BP_应急响应_编排处置.md)
8. [BP 根因分析 溯源复盘](../business_processes/BP_根因分析_溯源复盘.md)

## 价值流 3：动态知识进化闭环
0. [VS3-E2E 动态知识进化闭环 端到端用户故事](VS3-E2E_%E5%8A%A8%E6%80%81%E7%9F%A5%E8%AF%86%E8%BF%9B%E5%8C%96%E9%97%AD%E7%8E%AF_%E7%AB%AF%E5%88%B0%E7%AB%AF%E7%94%A8%E6%88%B7%E6%95%85%E4%BA%8B.md)
9. [BP 情报摄取 多源采集](../business_processes/BP_情报摄取_多源采集.md)
10. [BP 知识融合 图谱构建](../business_processes/BP_知识融合_图谱构建.md)
11. [BP 风险预警 影响面评估](../business_processes/BP_风险预警_影响面评估.md)

## 价值流 4：环境感知监控闭环
0. [VS4-E2E 环境感知监控闭环 端到端用户故事](VS4-E2E_%E7%8E%AF%E5%A2%83%E6%84%9F%E7%9F%A5%E7%9B%91%E6%8E%A7%E9%97%AD%E7%8E%AF_%E7%AB%AF%E5%88%B0%E7%AB%AF%E7%94%A8%E6%88%B7%E6%95%85%E4%BA%8B.md)
12. [BP 检测规则自动化生成](../business_processes/BP_检测规则自动化生成.md)

> 每个故事均包含：用户故事、验收标准、SHOWCASE（场景/输入/输出/业务价值）。

## 架构同步状态 (2026-03-10)
- Source of Truth：`design/KG/SystemArchitecture.json`
- 跨价值流 I/O 契约：`../business_processes/IO_跨价值流编排兼容规范.md`
- 价值流故事到 BP 的链接关系已按统一输入/输出约束进行文档同步。
- Last Verified：`2026-03-10 / commit: 2ac50a0`

