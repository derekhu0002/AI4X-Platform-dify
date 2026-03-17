import json
raw_input = """```json
{"a": 1}
```"""
raw_input = raw_input.strip()
if raw_input.startswith("```json"):
    raw_input = raw_input[7:]
if raw_input.endswith("```"):
    raw_input = raw_input[:-3]
raw_input = raw_input.strip()
print(json.loads(raw_input))
