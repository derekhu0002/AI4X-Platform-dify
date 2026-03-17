fp = r"d:\projects\AI4X\AI4X-Platform-dify\design\tasks\taskandissues_for_LLM.md"
with open(fp, encoding="utf-8") as f:
    content = f.read()

note_1221 = (
    "<br>[2026-03-16] from LLM: Addressed the VS4 sample-input question for Object_ID 1221. "
    "Technical approach: updated the first acceptance criterion in "
    "implementation/taskhelpinfos/2026-3-16_支持快速的情报生产和消费.md to replace the vague "
    "'用 VS4 样例输入触发流程' with a concrete Dify chat input message referencing "
    "indicator--8f69cfe9-8088-411c-bb09-9a33cf0d73d8 (bola-jwt-mismatch) and "
    "infrastructure--64860cf7-f483-4a37-b4bb-bd219ec509b8 (prod-api-cluster) from "
    "tests/validation/test-data/vs4-bola-monitoring-bundle.json. "
    "Changed file: implementation/taskhelpinfos/2026-3-16_支持快速的情报生产和消费.md "
    "(step 2 of first acceptance criterion now contains an executable copy-paste user message). "
    "Verification: file updated and acceptance step now fully actionable. "
    "Remaining blocker: none for this issue; Dify human-node SLA/permission still pending. "
    "Next action: paste the sample into Dify debug chat and confirm routing reaches VS4 branch."
)

note_1226 = (
    "<br>[2026-03-16] from LLM: Addressed three acceptance-detail questions for Object_ID 1226. "
    "(1) Bundle sample data: updated 'true OpenCTI write path' criterion in "
    "implementation/taskhelpinfos/2026-3-16_业务流程中所有数据都必须是OPENCTI平台中的STIX2_1标准数据.md "
    "with an inline JSON sample (single indicator from vs4-bola-monitoring-bundle) and POST body for "
    "http://localhost:8101/bundle. "
    "(2) Log keywords: updated 'writeback verification' criterion with response error codes "
    "CTI-4091 (timeout), CTI-4041 (not-found retry), uvicorn HTTP 200/409, and env var "
    "OPENCTI_MCP_WRITEBACK_VERIFY_WINDOW_SECONDS controlling the threshold. "
    "(3) CI test steps: updated 'contract and integration tests' criterion with step-by-step commands: "
    "pytest unit/contract/integration in mock mode, then real opencti-mode POST with mock_mode=false. "
    "Changed file: implementation/taskhelpinfos/2026-3-16_业务流程中所有数据都必须是OPENCTI平台中的STIX2_1标准数据.md "
    "(three acceptance criteria enriched). "
    "Verification: all three criteria now actionable for QA in real environment. "
    "Remaining blocker: importUpload/stixCoreObjectEdit compatibility depends on OpenCTI version. "
    "Next action: run pytest locally and perform one staging mock_mode=false bundle POST."
)

def insert_after(text, anchor, note):
    idx = text.find(anchor)
    if idx == -1:
        print(f"ANCHOR NOT FOUND: {anchor[:80]}")
        return text
    insert_pos = idx + len(anchor)
    print(f"Inserting after: ...{anchor[-40:]!r}")
    return text[:insert_pos] + note + text[insert_pos:]

content = insert_after(content, '2026-03-1623:34：请给我"用 VS4 样例输入触发流程"在该验收标准下', note_1221)
content = insert_after(content, "3、在 CI 或本地执行合同测试和集成测试-- 请详细描述测试步骤细节到该验收标准下", note_1226)

with open(fp, "w", encoding="utf-8") as f:
    f.write(content)

print("Done")
