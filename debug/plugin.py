"""
设计辅助插件 (Design Phase Helper Plugin)
覆盖 TARA (威胁分析)、安全需求工程、安全架构设计等设计阶段任务
"""

import sys
import os
import json
import logging
import re
import copy
from datetime import datetime
from typing import List, Dict, Any, Optional

# Ensure we can import from root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from shared.interface import BaseSecurityPlugin, PluginMetadata, PluginInput, PluginOutput, Skill
from shared.utils import generate_stix_id
try:
    from core.llm_engine import LLMEngine
except ImportError:
    LLMEngine = None

logger = logging.getLogger(__name__)

class DesignHelperPlugin(BaseSecurityPlugin):

    def _threat_model_response_format(self) -> Dict[str, Any]:
        return {
            "type": "json_schema",
            "json_schema": {
                "name": "threat_model_output",
                "strict": True,
                "schema": {
                    "type": "object",
                    "required": [
                        "methodology",
                        "attack_patterns",
                        "targets",
                        "simulated_attack_paths",
                        "observables",
                        "course_of_actions",
                        "detection_indicators",
                        "tara_stride_outputs",
                        "security_goals",
                        "summary",
                    ],
                    "properties": {
                        "methodology": {"type": "string", "enum": ["TARA+STRIDE"]},
                        "attack_patterns": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "required": ["id", "name", "description", "category", "risk_level", "likelihood", "impact", "stride", "kill_chain_phases"],
                                "properties": {
                                    "id": {"type": "string"},
                                    "name": {"type": "string"},
                                    "description": {"type": "string"},
                                    "category": {"type": "string"},
                                    "risk_level": {"type": "string"},
                                    "likelihood": {"type": "string"},
                                    "impact": {"type": "string"},
                                    "stride": {"type": "string"},
                                    "kill_chain_phases": {"type": "array", "items": {"type": "object"}},
                                },
                                "additionalProperties": True,
                            },
                        },
                        "targets": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "required": ["attack_pattern_id", "asset_name"],
                                "properties": {
                                    "attack_pattern_id": {"type": "string"},
                                    "asset_name": {"type": "string"},
                                },
                                "additionalProperties": True,
                            },
                        },
                        "simulated_attack_paths": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "required": ["id", "type", "name", "path_steps"],
                                "properties": {
                                    "id": {"type": "string"},
                                    "type": {"type": "string", "enum": ["report"]},
                                    "name": {"type": "string"},
                                    "path_steps": {"type": "array", "items": {"type": "string"}},
                                    "object_refs": {"type": "array", "items": {"type": "string"}},
                                },
                                "additionalProperties": True,
                            },
                        },
                        "observables": {"type": "array", "items": {"type": "object"}},
                        "course_of_actions": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "required": ["id", "type", "name", "description", "mitigates_attack_pattern_ids"],
                                "properties": {
                                    "id": {"type": "string"},
                                    "type": {"type": "string", "enum": ["course-of-action"]},
                                    "name": {"type": "string"},
                                    "description": {"type": "string"},
                                    "mitigates_attack_pattern_ids": {"type": "array", "items": {"type": "string"}},
                                },
                                "additionalProperties": True,
                            },
                        },
                        "detection_indicators": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "required": ["indicator", "indicates_attack_pattern_ids"],
                                "properties": {
                                    "indicator": {
                                        "type": "object",
                                        "required": ["id", "type", "name", "pattern_type", "pattern"],
                                        "properties": {
                                            "id": {"type": "string"},
                                            "type": {"type": "string", "enum": ["indicator"]},
                                            "name": {"type": "string"},
                                            "pattern_type": {"type": "string", "enum": ["EQL"]},
                                            "pattern": {"type": "string"},
                                            "x_ecs_events": {"type": "array", "items": {"type": "object"}},
                                        },
                                        "additionalProperties": True,
                                    },
                                    "indicates_attack_pattern_ids": {"type": "array", "items": {"type": "string"}},
                                },
                                "additionalProperties": True,
                            },
                        },
                        "tara_stride_outputs": {
                            "type": "object",
                            "required": ["threat_scenarios", "risk_evaluation"],
                            "properties": {
                                "threat_scenarios": {"type": "array", "items": {"type": "object"}},
                                "risk_evaluation": {"type": "array", "items": {"type": "object"}},
                            },
                            "additionalProperties": True,
                        },
                        "security_goals": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "required": ["id", "name", "goal_type", "priority", "description"],
                                "properties": {
                                    "id": {"type": "string"},
                                    "name": {"type": "string"},
                                    "goal_type": {"type": "string"},
                                    "priority": {"type": "string"},
                                    "description": {"type": "string"},
                                },
                                "additionalProperties": True,
                            },
                        },
                        "summary": {
                            "type": "object",
                            "required": [
                                "total_objects",
                                "attack_patterns",
                                "targets",
                                "simulated_attack_paths",
                                "observables",
                                "course_of_actions",
                                "detection_indicators",
                                "threat_scenarios",
                                "risk_evaluation",
                                "security_goals",
                            ],
                            "properties": {
                                "total_objects": {"type": "integer"},
                                "attack_patterns": {"type": "integer"},
                                "targets": {"type": "integer"},
                                "simulated_attack_paths": {"type": "integer"},
                                "observables": {"type": "integer"},
                                "course_of_actions": {"type": "integer"},
                                "detection_indicators": {"type": "integer"},
                                "threat_scenarios": {"type": "integer"},
                                "risk_evaluation": {"type": "integer"},
                                "security_goals": {"type": "integer"},
                            },
                            "additionalProperties": True,
                        },
                    },
                    "additionalProperties": True,
                },
            },
        }

    def generate_threat_model(self, architecture_description: str, methodology: str = "STRIDE", components: List[str] = None, assets: List[str] = None) -> PluginOutput:
        """
        生成威胁模型
        
        Args:
           architecture_description: 系统架构的自然语言描述或JSON结构
           methodology: 使用的威胁建模方法论
           components: 系统组件列表 (optional, can be in description)
           assets: 资产列表 (optional, can be in description)
        """
        # @ArchitectureID: 1095
        logger.info(f"Generating threat model using {methodology}")
        
        # If no LLM, return empty non-fabricated result without failing the pipeline
        if not self.llm:
            return PluginOutput(
                success=True,
                message="Threat modeling skipped: LLM unavailable",
                data=self._build_non_fabricated_diagnostic_payload("LLM unavailable", ""),
            )

        # 构建上下文
        context_parts = [f"Target System Description:\n{architecture_description}"]
        if components:
            context_parts.append(f"\nComponents (sdo:Software): {', '.join(components)}")
        if assets:
            context_parts.append(f"\nAssets (sdo:Identity): {', '.join(assets)}")
        
        context = "\n".join(context_parts)

        prompt = f"""
You are a security architect expert. Build a threat model using BOTH TARA and STRIDE from the architecture context.

Architecture Context:
{context}

Important rules:
1) Return a SINGLE JSON object only (no markdown, no commentary).
2) Keep all meaningful information; do not drop fields when uncertain.
3) For every indicator, pattern_type MUST be exactly \"EQL\".
4) simulated_attack_paths.path_steps MUST be natural-language sentence list with style:
   \"when <preconditions>, <subject_observable_id> <predicate> <object_observable_id>, lead to <result>.\"
5) Report names must be semantic (never numbered templates).
6) Do NOT output top-level ttps. Merge kill-chain analysis into tara_stride_outputs.threat_scenarios.
7) Avoid semantic duplicates across arrays.
8) Keep object name and description concise, avoid unnecessary verbosity.
9) Include a top-level summary object with integer counts for each output array and total_objects.
10) Every object name and description MUST be English-only text.
11) Do not output duplicate keys, duplicate arrays, or duplicate objects across sections.
12) Do not include excessive blank lines; output compact JSON only.
13) Every object name/description must be business-specific and reference concrete architecture entities, parameters, or attack intent (avoid generic placeholders).
14) Do NOT output tara_stride_outputs.stride_mapping; embed STRIDE semantics into attack_patterns.stride and threat_scenarios only.
15) Every observable type MUST be STIX 2.1 SCO type only (e.g., software, process, file, ipv4-addr, domain-name, url, artifact). Never output types like application/service/server/device/parameter.
16) Identify value assets ONLY when evidenced by architecture context/components/assets; do not invent assets.
17) For each targets item include intrinsic value fields: intrinsic_value (low/medium/high/critical), intrinsic_value_dimensions (subset of confidentiality/integrity/availability/physical_safety), and intrinsic_value_reason.
"""
        try:
            try:
                response = self.llm.chat(
                    [{"role": "user", "content": prompt}],
                    temperature=0.2,
                    max_tokens=4000,
                    response_format=self._threat_model_response_format(),
                )
            except TypeError:
                response = self.llm.chat([{"role": "user", "content": prompt}], temperature=0.2, max_tokens=4000)

            response_text = response if isinstance(response, str) else json.dumps(response, ensure_ascii=False)
            response_file = self._persist_raw_llm_response(
                response_text,
                {
                    "methodology": methodology,
                    "components_count": len(components or []),
                    "assets_count": len(assets or []),
                },
            )
            if response_file:
                logger.info("[THREAT_MODEL][RAW_LLM_RESPONSE_FILE] %s", response_file)

            try:
                data = self._coerce_threat_model_shape(self._parse_llm_json_response(response_text))
            except Exception as parse_exc:
                logger.warning("Primary threat-model JSON parse failed, returning empty non-fabricated result: %s", parse_exc)
                return PluginOutput(
                    success=True,
                    message=f"Threat modeling skipped: invalid LLM JSON ({parse_exc})",
                    data=self._build_non_fabricated_diagnostic_payload(f"invalid_json: {parse_exc}", response_text or ""),
                )

            logger.info("[THREAT_MODEL][NORMALIZED_JSON]: %s", json.dumps(data, ensure_ascii=False))
            
            return PluginOutput(
                success=True,
                message="威胁建模分析完成",
                data=data
            )
        except Exception as e:
            logger.error(f"Error in generate_threat_model: {e}")
            return PluginOutput(
                success=True,
                message=f"Threat modeling skipped: runtime error ({e})",
                data=self._build_non_fabricated_diagnostic_payload(f"runtime_error: {e}", ""),
            )