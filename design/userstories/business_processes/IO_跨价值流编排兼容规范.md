# 跨价值流编排 I/O 兼容规范 (Cross-Value-Stream Orchestration I/O Contract)

## 目标
为所有 Business Process 提供统一的输入/输出契约，确保在多价值流编排时可直接串接，无需二次数据清洗。

## 统一输入信封 (Input Envelope)
所有 BP 的输入建议使用统一结构：

```json
{
  "context": {
    "trace_id": "uuid",
    "workflow_id": "vs1-vs2-vs3",
    "source_bp": "BP_名称",
    "target_bp": "BP_名称",
    "timestamp": "2026-02-22T10:00:00Z"
  },
  "stix_bundle": {
    "type": "bundle",
    "id": "bundle--...",
    "objects": []
  },
  "parameters": {},
  "constraints": {
    "schema_version": "1.0",
    "stix_version": "2.1"
  }
}
```

## 统一输出信封 (Output Envelope)

```json
{
  "context": {
    "trace_id": "uuid",
    "workflow_id": "vs1-vs2-vs3",
    "source_bp": "BP_名称",
    "timestamp": "2026-02-22T10:01:00Z"
  },
  "result": {
    "status": "success",
    "summary": "本环节产出摘要",
    "stix_bundle": {
      "type": "bundle",
      "id": "bundle--...",
      "objects": []
    }
  },
  "handoff": {
    "next_bp": "BP_名称",
    "required_objects": ["indicator", "attack-pattern"],
    "quality_gates": ["has_object_refs", "has_confidence_or_severity"]
  }
}
```

## 强制兼容规则
1. **对象标准**：跨 BP 传递对象优先使用 STIX 2.1 SDO/SRO（如 `vulnerability`、`indicator`、`attack-pattern`、`incident`、`course-of-action`、`report`、`relationship`）。
2. **ID 一致性**：所有对象必须有稳定 `id`，关系对象通过 `source_ref/target_ref` 引用，不允许只传展示文本。
3. **最小字段集**：
   - `vulnerability`: `id`, `name`
   - `indicator`: `id`, `pattern`
   - `attack-pattern`: `id`, `name`
   - `incident`: `id`, `name`
   - `course-of-action`: `id`, `name`
   - `report`: `id`, `description`
4. **质量门禁**：进入下游 BP 前至少满足：
   - `objects` 非空；
   - 关键对象具备 `id`；
   - 可选风险字段之一存在（`confidence` / `severity` / `risk_level`）。
5. **编排追踪**：必须携带 `trace_id` 和 `workflow_id`，便于多价值流闭环审计。

## 推荐跨流程映射（示例）
- 威胁建模 → 需求生成：`attack-pattern` + `security goal`
- 情报摄取 → 知识融合：`bundle`
- 知识融合 → 风险预警：`vulnerability` + `relationship(affects)`
- 态势感知 → 应急响应：`incident` + `sighting`
- 应急响应 → 根因分析：`incident` + `report`
- 根因分析 → 检测规则生成：`indicator` + `attack-pattern`

## 版本策略
- 当前版本：`1.0`
- 新增字段：向后兼容（只增不减）
- 破坏性变更：升级主版本并在各 BP 文档同步更新
