---
name: jtbd-validator
description: |
  Validate JTBD (Jobs-to-be-Done) markdown files for correctness and completeness.
  Use when user says "validate JTBD", "check JTBD", "verify workflow", or "lint JTBD".
---

# JTBD Validator Skill

Validates Jobs-to-be-Done (JTBD) markdown files to ensure correct structure, valid API references, and proper step dependencies.

## What It Validates

- ✅ Frontmatter (name, description)
- ✅ Step headers (sequential, matching YAML blocks)
- ✅ YAML structure (api, operationId, inputs)
- ✅ API URNs (folder exists, spec valid)
- ✅ OperationIds (exist in API specs)
- ✅ Step dependencies (no forward references, outputs exist)

## How to Use

### Validate a Single File

```bash
python3 .claude/skills/jtbd-validator/scripts/validate_jtbd.py path/to/job.md .
```

### Validate All JTBDs in a Folder

```bash
for job in skills/*/SKILL.md; do
  python3 .claude/skills/jtbd-validator/scripts/validate_jtbd.py "$job" .
done
```

### Find All JTBD Files

```bash
find . -path "*/skills/*/SKILL.md" -type f | grep -v node_modules
```

## Workflow

### When User Requests Validation

**1. Identify files to validate:**
   - Specific file: Use the provided path
   - All JTBDs: Find all `skills/*/SKILL.md` files

**2. Run validator:**
   ```bash
   python3 .claude/skills/jtbd-validator/scripts/validate_jtbd.py <file> .
   ```

**3. Report results:**
   - ✅ PASSED: Just confirm it's valid
   - ❌ FAILED: Explain errors in plain English

**4. If errors, explain how to fix them**

### Example Interactions

```
User: Validate skills/deploy-api-with-rate-limiting/SKILL.md

You: [Runs validator]
✅ Valid - 5 steps, all references correct

User: Validate all JTBDs

You: [Finds and validates all JTBD files]
Validated 7 files:
✅ 6 passed
❌ 1 failed (broken-example.md: operation not found)
```

## Common Errors & Fixes

**Operation not found:**
- Error: `Operation 'createApis' not found in urn:api:api-manager`
- Fix: Check correct operationId in api-manager/api.yaml

**Missing output reference:**
- Error: `References unknown output 'apiId' from step 1`
- Fix: Add output to Step 1 or correct reference name

**Forward reference:**
- Error: `References step 3 which comes after step 2`
- Fix: Steps can only reference previous steps

**Invalid URN:**
- Error: `API folder not found for 'urn:api:api-mgr'`
- Fix: Use correct folder name (e.g., `urn:api:api-manager`)

---

**Exit Codes:**
- 0 = Valid
- 1 = Invalid

**Related Skills:**
- jtbd-generator (uses this validator automatically)
