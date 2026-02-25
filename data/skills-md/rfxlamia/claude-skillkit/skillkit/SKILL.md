---
name: skillkit
description: >
  Professional skill AND subagent creation with research-driven workflow and automated validation.

  USE WHEN: Creating new skills OR subagents, validating existing skills, deciding between Skills
  vs Subagents, migrating documents to skills/subagents, or running individual validation tools.

  PRIMARY TRIGGERS:
  "create skill" = Full skill creation (12 steps with research + execution planning)
  "create subagent" = Subagent creation (8 steps with template-based workflow)
  "validate skill" = Validation workflow (steps 3-8)
  "Skills vs Subagents" = Decision workflow (step 0) - recommends then creates
  "convert doc to skill" = Migration workflow
  "estimate tokens" = Token optimization
  "security scan" = Security audit

  WORKFLOW COMPLIANCE: Structured workflows with validation checkpoints.
  Research phase (Step 1c-1d) ensures skills based on proven approaches.

  DIFFERENTIATOR: Research-driven creation. Web search (3-5 queries) before
  building. Multi-proposal generation. 10 automation scripts (9 skill + 1 subagent).
  Quality 9.0+/10. NOW WITH SUBAGENT CREATION SUPPORT.

  REUSED: Anthropic's init_skill.py and package_skill.py (production-tested).
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

**Workflow Value:** Research-driven approach validates design before building.
Sequential steps with checkpoints produce 9.0/10+ quality vs ad-hoc creation.

---

## Section 2: Full Creation Workflow (Overview)

**Prerequisites:** Skill description provided, workspace available
**Quality Target:** >=9.0/10
**Time:** <10 min with automation

> **💡 Quick Note:** Make sure venv exists at skillkit root, or if it already exists, activate venv before using tools:
> ```bash
> cd /home/v/.claude/skills/skillkit && source venv/bin/activate
> ```

### 12-Step Process with Validation Gates:

**STEP 0: Decide Approach**
- Tool: `decision_helper.py`
- Decides: Skills vs Subagents
- Gate: Proceed only if "Skills" recommended

**STEP 1: Understand & Research**
- 1a. Gather requirements
- 1b. Identify knowledge gaps
- 1c. Research domain (Verbalized Sampling: 3-4 web searches with diverse angles)
- 1d. Generate proposals (3-5 options evaluated with multi-criteria scoring)
- 1e. User validates and approves approach
- 1f. Execution planning: P0/P1/P2 prioritization with token budgets assigned
  - See: `references/section-2-full-creation-workflow.md` (Step 1f details)

**STEP 2: Initialize & Create Content**
- Tool: `python scripts/init_skill.py skill-name --path /path` (Anthropic)
- Alternative: `migration_helper.py` (if converting from document)
- 2.5 Checkpoint: Sequential creation (P0→P1→P2), token budget monitoring
- 2.8 Verification: P0/P1/P2 completion validation before proceeding
  - See: `references/section-2-full-creation-workflow.md` (Steps 2.5 & 2.8 details)

**STEP 3: Validate Structure**
- Tool: `validate_skill.py`
- Gate: Fix critical issues before proceeding

**STEP 4: Security Audit**
- Tool: `security_scanner.py`
- Gate: Fix critical vulnerabilities immediately

**STEP 5: Token Optimization**
- Tool: `token_estimator.py`
- Gate: Optimize if >5000 tokens

**STEP 6: Progressive Disclosure**
- Tool: `split_skill.py`
- Gate: Split if SKILL.md >350 lines

**STEP 7: Generate Tests**
- Tool: `test_generator.py`
- Creates: Automated validation tests

**STEP 8: Quality Assessment**
- Tool: `quality_scorer.py`
- Gate: Must achieve >=9.0/10 before packaging

**STEP 9: Package for Deployment**
- Tool: `python scripts/package_skill.py skill-name/` (Anthropic)
- Creates: .skill file ready to deploy

**For detailed implementation:** [See references/section-2-full-creation-workflow.md](references/section-2-full-creation-workflow.md)

---

## Section 3: Validation Workflow (Overview)

**Use when:** Validating existing skill

**Steps:** Execute validation subset (Steps 3-8)
1. Structure validation (validate_skill.py)
2. Security audit (security_scanner.py)
3. Token analysis (token_estimator.py)
4. Progressive disclosure check
5. Test generation (optional)
6. Quality assessment (quality_scorer.py)

**For detailed workflow:** [See references/section-3-validation-workflow-existing-skill.md](references/section-3-validation-workflow-existing-skill.md)

---

## Section 4: Decision Workflow (Overview)

**Use when:** Uncertain if Skills is right approach

**Process:**
1. Run `decision_helper.py`
2. Answer interactive questions
3. Receive recommendation with confidence score
4. Proceed if Skills recommended (confidence >=75%)

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
- Tool: `python scripts/init_subagent.py subagent-name --path ~/.claude/agents`
- Creates: `~/.claude/agents/subagent-name.md` with template
- **Important:** Subagents are individual `.md` files (not directories)

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

**For detailed workflow:** [See references/section-6-subagent-creation-workflow.md](references/section-6-subagent-creation-workflow.md)

---

## Section 5: Migration Workflow (Overview)

**Use when:** Converting document to skill

**Process:**
1. Decision check (Step 0)
2. Migration analysis (migration_helper.py)
3. Structure creation
4. Execute validation steps (3-8)
5. Package (Step 9)

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
python scripts/token_estimator.py skill-name/ --format json
```
Guide: `knowledge/tools/15-cost-tools-guide.md`

**Security Scanner:**
```bash
python scripts/security_scanner.py skill-name/ --format json
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

**IMPORTANT:** Before first use, read the guide for detailed 3-mode workflow:
`knowledge/tools/18-decision-helper-guide.md`

**Mode 1: Pre-Answered (PREFERRED - highest accuracy):**
```bash
# Create temp JSON file with 8 boolean answers
mkdir -p /tmp/skillkit
cat > /tmp/skillkit/decision-answers.json <<'EOF'
{
  "utility_task": false,
  "multi_step": true,
  "reusable": false,
  "specialized_personality": true,
  "missing_knowledge": false,
  "coordination": true,
  "isolated_context": true,
  "clutter_chat": true
}
EOF

# Call with file path (NOT inline JSON)
python scripts/decision_helper.py --answers /tmp/skillkit/decision-answers.json
```

**Mode 2: Keyword Inference (fallback when answers unclear):**
```bash
python scripts/decision_helper.py --analyze "code review with validation"
```

**Mode 3: Show Criteria (reference):**
```bash
python scripts/decision_helper.py --show-criteria --format json
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
python scripts/init_subagent.py subagent-name --path /path/to/subagents
```
Guide: `references/section-6-subagent-creation-workflow.md`

### Tool Output Standardization (v1.0.1+)

**All 9 tools now support `--format json` parameter:**
- ✅ Consistent JSON schema across all automation tools
- ✅ Parseable with `python -m json.tool` for validation
- ✅ Backward compatible - text mode still available as default (or via `--format text`)
- ✅ Agent-layer tools (decision_helper) default to JSON for automation

**JSON Output Structure (Standardized):**
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

## Section 8: Knowledge Reference Map (Overview)

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

## Workflow Compliance Reinforcement
**This skill works best when workflows are followed sequentially.**

**Why compliance matters:**
1. Research validation reduces iteration (validate before build)
2. Security checks prevent vulnerabilities (catch issues early)
3. Token optimization ensures efficiency (avoid bloat)
4. Quality gates maintain standards (9.0/10+ target)

**Mechanisms encouraging compliance:**
- Frontmatter priming: "WORKFLOW COMPLIANCE" statement
- Section routing: Explicit "PROCEED to Section X"
- Validation gates: IF/THEN with checkpoints
- Quality target: ">=9.0/10 requires following workflow"

**Flexible when needed:**
- Single tool usage (Section 7) skips full workflow
- Validation-only (Section 3) runs subset of steps
- Subagent creation (Section 6) has streamlined workflow
- User can request deviations with justification

**Goal:** Strong encouragement through design, not strict enforcement.

---

## Additional Resources

**Detailed implementations available in references/ directory:**

All section overviews above link to detailed reference files for deep-dive information.
Load references on-demand when detailed implementation guidance needed.
