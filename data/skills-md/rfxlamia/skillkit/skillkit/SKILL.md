---
name: skillkit
description: >
  Toolkit for creating and validating skills and subagents.
  Use when: creating a new skill (fast or full mode), validating an
  existing skill, deciding Skills vs Subagents, migrating docs to skills,
  estimating token cost, or running a security scan.
  Triggers: "create skill", "build skill", "validate skill", "new subagent",
  "skills vs subagents", "estimate tokens", "security scan".
category: core
---

## Section 1: Intent Detection & Routing
**Detect user intent, route to appropriate workflow.**

| Intent | Keywords | Route To |
|--------|----------|----------|
| Full skill creation | "create skill", "build skill", "new skill" | Section 2 |
| Subagent creation | "create subagent", "build subagent", "new subagent" | Section 6 |
| Validation | "validate", "check quality" | Section 3 |
| Decision | "Skills vs Subagents", "decide", "which to use" | Section 4 |
| Migration | "convert", "migrate doc" | Section 5 |
| Single tool | "validate only", "estimate tokens", "scan" | Section 7 |

**PROCEED to corresponding section after intent detection.**

**Stop Condition (Mandatory):**
- If multiple routes match or intent is ambiguous: stop, ask user to choose one route.
- Do not proceed until user confirms the route.

**Workflow Value:** Research-driven approach validates design before building.
Sequential steps with checkpoints produce 9.0/10+ quality vs ad-hoc creation.

---

## Section 2: Creation Workflows (Dual Mode)

**Prerequisites:** Skill description provided, workspace available.

### Mode Selection (Required at Start)

Detect or prompt for workflow mode before running the creation flow.

**Stop Condition (Mandatory):**
- If mode is not explicitly provided: stop and ask "Do you want fast or full mode?"
- Do not continue until user confirms the mode.

| Mode | Steps | Validation | Quality Target | Time |
|------|-------|------------|----------------|------|
| **fast** | 10 | Structural only | >=9.0/10 | <10 min |
| **full** | 14 | Structural + Behavioral | >=9.0/10 and behavioral >=7.0 | <20 min |

No implicit default mode is allowed when mode is not explicitly known.

### Workflow A: Fast Mode (10 Steps)

Use when `.skillkit-mode` contains `fast` or marker does not exist.

**→ READ `references/section-2-fast-creation-workflow.md` IN FULL before starting.**
**Create a task for each step listed in that file, then follow them in order.**
The outline below is a summary only — the reference file is authoritative.

Phase 1: Decision & Research
- Step 0: Decide approach (`decision_helper.py`)
- Step 1: Research and proposals
- Step 2: User validation
- Stop Condition: Stop and request user approval before continuing to Step 3.

Phase 2: Creation
- Step 3: Initialize skill (`init.py skill <name> --mode fast`)
- Step 4: Create content

Phase 3: Structural Validation
- Step 5: Validate skill (`validate_skill.py`) — runs structure + security + tokens in one call

Phase 4: Packaging
- Step 6: Progressive disclosure check
- Step 7: Generate tests (`test_generator.py`)
- Step 8: Quality assessment (`quality_scorer.py`)
- Step 9: Package (`package_skill.py`)

### Workflow B: Full Mode (14 Steps)

Use when `.skillkit-mode` contains `full`.

**→ READ `references/section-2-full-creation-workflow.md` IN FULL before starting.**
**Create a task for each step listed in that file, then follow them in order.**
The outline below is a summary only — the reference file is authoritative.

Phase 1: Decision and Research
- Step 0: Decide approach (`decision_helper.py`)
- Step 1: Research and proposals
- Step 2: User validation
- Stop Condition: Stop and request user approval before continuing to Step 3.

Phase 2: Behavioral Baseline (extra vs fast)
- Step 3 (RED): Run pressure scenarios without skill
  **→ Load `references/section-2-full-creation-workflow.md` → section "Full Mode Behavioral Testing Protocol" (mandatory)**
- Step 4: Document baseline failures

Phase 3: Creation
- Step 5: Initialize skill (`init.py skill <name> --mode full`)
- Step 6: Create content addressing baseline failures

Phase 4: Behavioral Verification (extra vs fast)
- Step 7 (GREEN): Run scenarios with skill
  **→ Load `references/section-2-full-creation-workflow.md` → section "Full Mode Behavioral Testing Protocol" (mandatory)**
- Step 8: Fix gaps

Phase 5: Structural Validation
- Step 9: Validate skill (`validate_skill.py`) — runs structure + security + tokens in one call

Phase 6: Refinement (extra vs fast)
- Step 10 (REFACTOR): Combined pressure tests
  **→ Load `references/section-2-full-creation-workflow.md` → section "Full Mode Behavioral Testing Protocol" (mandatory)**
- Step 11: Close loopholes

Phase 7: Packaging
- Step 12: Quality assessment (`quality_scorer.py --format json`) — behavioral score derived from Steps 3/7/10 subagent results, not from `--behavioral` flag
- Step 13: Package (`package_skill.py`)

### Mode Detection

Priority order:
1. Explicit flag: `--mode fast` or `--mode full`
2. Skill marker: `.skillkit-mode` file content
3. If unknown: stop and ask user to choose `fast` or `full`

---

## Section 3: Validation Workflow (Overview)

**Use when:** Validating existing skill

**Steps:** Execute validation subset (Steps 3-6)
1. Validate skill — structure + security + tokens (`validate_skill.py`, no flags needed)
2. Progressive disclosure check
3. Test generation (optional)
4. Quality assessment (quality_scorer.py)

**Note:** `--security-only` and `--tokens-only` flags are available for Section 7 individual tool use, not for workflow validation steps.

**For detailed workflow:** [See references/section-3-validation-workflow-existing-skill.md](references/section-3-validation-workflow-existing-skill.md)

---

## Section 4: Decision Workflow (Overview)

**Use when:** Uncertain if Skills is right approach

**CRITICAL: Agent MUST create a temp JSON file first.** The `decision_helper.py` script does NOT accept inline JSON strings - it requires a file path to a JSON file.

**Step-by-step invocation:** See `references/section-4-decision-workflow-skills-vs-subagents.md`

**Accuracy:** Highest (90-95% confidence).

**Process:**

1. Run `decision_helper.py` with json file.
2. Answer interactive questions
3. Receive recommendation with confidence score
4. Proceed if Skills recommended (confidence >=75%)
5. If confidence <75% or recommendation is uncertain, stop and ask user whether to continue, switch route, or refine inputs.

**For detailed workflow:** [See references/section-4-decision-workflow-skills-vs-subagents.md](references/section-4-decision-workflow-skills-vs-subagents.md)

---

## Section 6: Subagent Creation Workflow (Overview)

**Use when:** Creating new subagent (user explicitly asks or decision workflow recommends)

**Prerequisites:** Role definition clear, workspace available
**Quality Target:** Clear role, comprehensive workflow, testable examples
**Time:** <15 min with template

### 8-Step Process:

**STEP 0: Requirements & Role Definition**
- Answer: Primary role? Trigger conditions? Tool requirements?
- Choose subagent_type from predefined list

**STEP 1: Initialize Subagent File**
- Tool: `python scripts/init.py subagent subagent-name --path ~/.claude/agents`
- Creates: `~/.claude/agents/subagent-name.md` with template
- **Important:** Subagents are individual `.md` files (not directories)
- Stop Condition: If target file already exists, stop and ask whether to overwrite, rename, or cancel.

**STEP 2: Define Configuration**
- Edit YAML frontmatter (name, description, type, tools, skills)
- Configure tool permissions (minimal but sufficient)

**STEP 3: Define Role and Workflow**
- Role definition section
- Trigger conditions (when to invoke)
- Multi-phase workflow

**STEP 4: Define Response Format**
- Output structure template
- Tone and style guidelines
- Error handling

**STEP 5: Add Examples**
- At least 1 complete example
- Input/Process/Output format

**STEP 6: Validation**
- YAML validity check
- Structure verification
- Completeness review

**STEP 7: Testing**
- Test invocation with Task tool
- Iterate based on results

**STEP 8: Documentation & Deployment**
- Create README.md
- Register in system
- Stop Condition: Ask for explicit user confirmation before register/deploy actions.

**For detailed workflow:** [See references/section-6-subagent-creation-workflow.md](references/section-6-subagent-creation-workflow.md)

---

## Section 5: Migration Workflow (Overview)

**Use when:** Converting document to skill

**Process:**
1. Decision check (Step 0)
2. Migration analysis (migration_helper.py)
3. Structure creation
4. Execute validation steps (5-8)
5. Package (Step 9)

**Stop Condition (Mandatory):**
- Before structure creation or any write/overwrite operation: ask user confirmation.
- Do not modify files until user confirms.

**For detailed workflow:** [See references/section-5-migration-workflow-doc-to-skill.md](references/section-5-migration-workflow-doc-to-skill.md)

---

## Section 7: Individual Tool Usage
**Use when:** User needs single tool, not full workflow

**Entry Point:** User asks for specific tool like "estimate tokens" or "security scan"

### Available Tools

**Validation Tool:**
```bash
python scripts/validate_skill.py skill-name/ --format json
```
Guide: `knowledge/tools/14-validation-tools-guide.md`

**Token Estimator:**
```bash
python scripts/validate_skill.py skill-name/ --tokens-only --format json
```
Guide: `knowledge/tools/15-cost-tools-guide.md`

**Security Scanner:**
```bash
python scripts/validate_skill.py skill-name/ --security-only --format json
```
Guide: `knowledge/tools/16-security-tools-guide.md`

**Pattern Detector:**
```bash
# Analysis mode with JSON output
python scripts/pattern_detector.py "convert PDF to Word" --format json

# List all patterns
python scripts/pattern_detector.py --list --format json

# Interactive mode (text only)
python scripts/pattern_detector.py --interactive
```
Guide: `knowledge/tools/17-pattern-tools-guide.md`

**Decision Helper:**
```bash
# Analyze use case (JSON output - agent-layer default)
python scripts/decision_helper.py --analyze "code review with validation"

# Show decision criteria (JSON output)
python scripts/decision_helper.py --show-criteria --format json

# Text mode for human reading (debugging)
python scripts/decision_helper.py --analyze "description" --format text
```
Guide: `knowledge/tools/18-decision-helper-guide.md`

**Test Generator (v1.2: Parameter update):**
```bash
python scripts/test_generator.py skill-name/ --test-format pytest --format json
```
- `--test-format`: Test framework (pytest/unittest/plain, default: pytest)
- `--format`: Output style (text/json, default: text)
- Backward compatible: Old `--output` parameter still works (deprecated)

Guide: `knowledge/tools/19-test-generator-guide.md`

**Split Skill:**
```bash
python scripts/split_skill.py skill-name/ --format json
```
Guide: `knowledge/tools/20-split-skill-guide.md`

**Quality Scorer:**
```bash
python scripts/quality_scorer.py skill-name/ --format json
```
Guide: `knowledge/tools/21-quality-scorer-guide.md`

**Migration Helper:**
```bash
python scripts/migration_helper.py doc.md --format json
```
Guide: `knowledge/tools/22-migration-helper-guide.md`

**Subagent Initializer (NEW):**
```bash
python scripts/init.py subagent subagent-name --path /path/to/subagents
```
Guide: `references/section-6-subagent-creation-workflow.md`

### Tool Output Standardization (v1.0.1+)

All 9 tools support `--format json`. Text mode still available via `--format text` (backward compatible). `decision_helper` defaults to JSON for automation.

**JSON Output Structure:**
```json
{
  "status": "success" | "error",
  "tool": "tool_name",
  "timestamp": "ISO-8601",
  "data": { /* tool-specific results */ }
}
```

### Quality Assurance Enhancements (v1.2+)

**File & Reference Validation:**
- `validate_skill.py` now comprehensively checks file references (markdown links, code refs, path patterns)
- `package_skill.py` validates references before packaging, detects orphaned files
- Prevents broken references and incomplete files in deployed skills

**Content Budget Enforcement (v1.2+):**
- Hard limits on file size: P0 ≤150 lines, P1 ≤100 lines, P2 ≤60 lines
- Real-time token counting with progress indicators
- Prevents file bloat that previously caused 4-9x target overruns

**Execution Planning (v1.2+):**
- P0/P1/P2 prioritization prevents over-scoping
- Token budget allocated per file to maintain efficiency
- Research phase respects Verbalized Sampling probability thresholds (p>0.10)

**Quality Scorer Context:**
- Scores calibrated for general skill quality heuristics
- Target: 70%+ is good, 80%+ is excellent
- Style scoring may not fit all skill types (educational vs technical)
- Use as guidance, supplement with manual review for edge cases

---

## Section 8: Mode Selection Guide

| Skill Type | Recommended Mode | Why |
|------------|------------------|-----|
| TDD or discipline skill | **full** | must resist rationalization under pressure |
| Code pattern skill | **fast** | structural checks are usually sufficient |
| API reference skill | **fast** | primarily retrieval accuracy |
| Workflow orchestration skill | **full** | complex flow benefits from pressure checks |
| Debugging technique skill | **fast** | concise technique with clear method |

Full mode adds behavioral testing (pressure scenarios). Use it when discipline enforcement is core to the skill's purpose.

---

## Section 9: Knowledge Reference Map (Overview)

**Strategic context loaded on-demand.**

### Foundation Concepts (Files 01-08):
- Why Skills exist vs alternatives
- Skills vs Subagents decision framework
- Token economics and efficiency
- Platform constraints and security
- When NOT to use Skills

### Application Knowledge (Files 09-13):
- Real-world case studies (Rakuten, Box, Notion)
- Technical architecture patterns
- Adoption and testing strategies
- Competitive landscape analysis

### Tool Guides (Files 14-22):
- One guide per automation script
- Usage patterns and parameters
- JSON output formats
- Integration examples

**For complete reference map:** [See references/section-7-knowledge-reference-map.md](references/section-7-knowledge-reference-map.md)

---

## Workflow Compliance

Follow workflows sequentially. Sequential steps with gates produce 9.0/10+ quality. Deviations are allowed with user justification.

**Flexible entry points:**
- Single tool (Section 7): skip full workflow
- Validation only (Section 3): run validation subset
- Subagent (Section 6): streamlined 8-step workflow

---

## Additional Resources

Load reference files on-demand from `references/` when detailed implementation guidance is needed.
