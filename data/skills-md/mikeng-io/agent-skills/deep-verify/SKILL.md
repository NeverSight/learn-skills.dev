---
name: deep-verify
description: Generic multi-agent verification framework with balanced expert analysis. Model-agnostic and domain-agnostic - verify any work through expert analysis.
location: managed
dependencies:
  - context
  - preflight
  - domain-registry
allowed-tools:
  - ToolSearch
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash(git *)
  - Bash(ls *)
  - Bash(mkdir *)
  - Task
  - Skill
---

# Deep Verify: Multi-Agent Verification Framework

Execute this skill to verify work through balanced expert analysis.

## Execution Instructions

When invoked, you will:

0. **Resolve scope and context** — invoke context skill (always), then preflight if confidence is low
1. **Populate verification scope** from working_scope
2. **Generate expert agents** based on the extracted context:
   - Always spawn: Devil's Advocate, Integration Checker, Third-Party Reviewer
   - Dynamically spawn domain experts based on detected domains

   **Domain expert selection via domain-registry:**
   Read domain-registry/domains/*.md to match signals from working_scope.
   Minimum: 1 domain expert. No maximum.

3. **Aggregate findings** from all experts with proper weighting

4. **Generate and save report** to `.outputs/verification/`

---

## Dependency Check

Before executing any step, verify all required skills are present:

```
[skills-root]/context/SKILL.md
[skills-root]/preflight/SKILL.md
[skills-root]/domain-registry/README.md
```

Where `[skills-root]` is the parent of this skill's directory. Resolve with `ls ../` from this skill's location.

If any required file is missing → **stop immediately** and output:

```
⚠ Missing required skills for deep-verify:

  {missing-skill}
    Expected: {skills-root}/{missing-skill}/SKILL.md

Install the missing skill(s):
  git clone https://github.com/mikeng-io/agent-skills /tmp/agent-skills
  cp -r /tmp/agent-skills/skills/{missing-skill} {skills-root}/

Or install the full suite at once:
  cp -r /tmp/agent-skills/skills/ {skills-root}/
```

All dependencies present → proceed to Step 0.

---

## Step 0: Scope & Context Resolution

**Context (always required):**

Invoke `Skill("context")` first. It classifies the artifact, detects domains from domain-registry, and determines routing confidence:

```yaml
context_report:
  artifact_type: ""  # code | financial | marketing | creative | research | mixed
  domains: []        # matched domain names from domain-registry
  routing: ""        # parallel-workflow | debate-protocol | deep-council
  confidence: ""     # high | medium | low
```

**Preflight (conditional — triggered by context confidence):**

Invoke `Skill("preflight")` only if `context_report.confidence == "low"` OR one or more signals remain unresolved:
- Artifact is not clearly identified
- User's intent is unclear (what are we verifying?)
- Domains could not be detected
- Concerns or risks to verify are not stated

Preflight fills exactly the gaps context could not resolve (max 3 questions, one at a time):

```yaml
scope_clarification:
  artifact: ""       # what to verify
  intent: "verify"
  domains: []        # supplements context_report.domains
  constraints: []    # explicit risks or concerns to focus on
  confidence: ""     # high | medium
```

If `context_report.confidence == "high"` → skip preflight entirely.

**Merge into working scope:**
```yaml
working_scope:
  artifact: ""            # files, topics, or description of what to verify
  domains: []             # from context_report (authoritative), supplemented by preflight
  concerns: []            # from context signals and scope_clarification.constraints
  context_summary: ""     # combined description for expert agent prompts
```

Use `working_scope` throughout this skill.

---

## Step 1: Populate Verification Scope

Using `working_scope` from Step 0, extract the verification context:

```yaml
conversation_analysis:
  files: []        # from working_scope.artifact
  artifacts: []    # additional artifacts from working_scope
  topics: []       # key topics from context_report
  concerns: []     # from working_scope.concerns
  intent: ""       # from working_scope — what is being verified
  domain_inference: []  # from working_scope.domains
```

---

## Step 2: Spawn Expert Agents

Spawn experts with dependency-aware execution for optimal analysis quality. Domain experts analyze first, then invariant experts use those findings.

**Dependency-Aware Execution Strategy:**

Verification has natural dependencies:
- Integration Checker needs domain findings to assess cross-system impact
- Devil's Advocate is more effective challenging concrete domain findings
- Third-Party Reviewer benefits from seeing complete analysis

**Task Definitions with Dependencies:**
```yaml
tasks:
  # Wave 1: Domain analysis (foundation)
  - id: domain-experts
    description: "Domain-specific analysis"
    depends_on: []
    agents: [dynamic, based on conversation]

  # Wave 2: Critical analysis (needs domain findings)
  - id: integration-check
    description: "Assess system-wide integration impact"
    agent: "integration-checker"
    depends_on: [domain-experts]

  - id: devils-advocate
    description: "Challenge assumptions and find failure modes"
    agent: "devils-advocate"
    depends_on: [domain-experts]

  # Wave 3: Fresh perspective (needs complete analysis)
  - id: third-party-review
    description: "Fresh eyes review of all findings"
    agent: "third-party-reviewer"
    depends_on: [integration-check, devils-advocate]

execution:
  mode: dag-orchestrated
  waves:
    wave_1: [domain-experts]                        # N domain experts in parallel
    wave_2: [integration-check, devils-advocate]    # 2 tasks in parallel
    wave_3: [third-party-review]                    # 1 task
```

**Why This Order Matters:**

1. **Domain experts first** - Gather domain-specific findings and concerns
2. **Integration and critique together** - Integration Checker assesses impact, Devil's Advocate challenges assumptions, both using domain findings
3. **Fresh eyes last** - Third-Party Reviewer sees complete picture including domain analysis, integration impact, and challenges

**Performance Benefit:**
- Improves analysis quality - critics have concrete findings to work with
- Still maintains parallelism where possible (Wave 2 runs 2 tasks in parallel)
- Sequential where dependencies matter (Wave 3 needs everything)

### Invariant Experts (Always Spawn)

#### Expert 1: Devil's Advocate
```
Weight: 40%
Purpose: Counter confirmation bias through pre-mortem analysis
Capability: highest

Use this prompt:

You are the DEVIL'S ADVOCATE. Your role is to BALANCE the verification by actively seeking what could go wrong, what we're not seeing, and what assumptions might be false.

## Your Mindset: Pre-Mortem
Imagine this work has already caused a failure 6 months from now. Work backwards: What went wrong? What did we miss?

## Focus Areas
- Hidden Assumptions: What are we assuming that might not be true?
- Failure Modes: If this fails, what happens? Who is affected?
- Silent Failures: Could this fail without anyone noticing?
- Edge Cases: What edge cases might we have missed?
- Rollback Reality: Can we undo this? How difficult?
- Negative Impacts: What does this break that we're not seeing?

## Context to Analyze
{conversation_context}

## Your Scope
{scope_description}

## Output Format (JSON)
{
  "agent": "devils-advocate",
  "pre_mortem_scenarios": [
    {
      "scenario": "What went wrong",
      "likelihood": "LOW | MEDIUM | HIGH",
      "impact": "LOW | MEDIUM | HIGH | CRITICAL",
      "evidence": "What suggests this could happen",
      "mitigation": "How to prevent (if anything)"
    }
  ],
  "hidden_assumptions": [
    {
      "assumption": "What we're assuming",
      "risk_if_false": "What happens if wrong"
    }
  ]
}
```

#### Expert 2: Integration Checker
```
Weight: 15%
Purpose: Assess system-wide impact
Capability: high

Use this prompt:

You are the INTEGRATION CHECKER. Your role is to assess the system-wide impact of the proposed changes.

## Focus Areas
- What other components/systems are affected?
- What coordination is needed?
- What dependencies exist?
- What could break elsewhere?

## Context
{conversation_context}

## Output Format (JSON)
{
  "agent": "integration",
  "affected_components": ["list of affected areas"],
  "dependencies": ["list of dependencies"],
  "coordination_required": ["what needs to be coordinated"],
  "risks": [{"area": "affected area", "risk": "description"}]
}
```

#### Expert 3: Third-Party Reviewer
```
Weight: 5%
Purpose: Fresh-eyes perspective
Capability: standard

Use this prompt:

You are a THIRD-PARTY REVIEWER seeing this for the first time. Provide fresh, unbiased feedback.

## Focus Areas
- Is the intent clear?
- Are there obvious gaps or confusion?
- What questions would a newcomer ask?

## Context
{conversation_context}

## Output Format (JSON)
{
  "agent": "third-party",
  "clarity_score": "HIGH | MEDIUM | LOW",
  "questions": ["questions a newcomer would ask"],
  "suggestions": ["constructive suggestions"]
}
```

### Domain Experts (Spawn Based on Conversation)

For each domain detected in the conversation, generate a domain expert prompt:

```
Weight: 40% (shared across all domain experts)
Capability: high

Prompt Template:

You are a {DOMAIN} expert. Analyze the following work from a {DOMAIN} perspective.

## Context
{conversation_context}

## Your Focus
Identify issues, risks, and improvements specific to {DOMAIN}.

## Output Format (JSON)
{
  "agent": "{domain}",
  "findings": [
    {
      "severity": "CRITICAL | HIGH | MEDIUM | LOW",
      "description": "Issue or observation",
      "evidence": "Reference to specific content",
      "fix": "Recommendation if applicable"
    }
  ]
}
```

**Spawn domain experts for each unique domain detected.** Examples:
- "authentication" discussed → Spawn Security Expert
- "Figma design" mentioned → Spawn Design Expert
- "email campaign" discussed → Spawn Marketing Expert
- "policy update" discussed → Spawn HR/Legal Expert

Any domain can be detected - analyze the conversation and spawn appropriate experts.

---

## Step 3: Aggregate Findings

After all experts complete, aggregate their findings:

### Determine Verdict
- **FAIL**: Critical risks or blocking issues found
- **CONCERNS**: High risks identified
- **PASS**: No significant issues

### Build Summary Table
| Dimension | Result |
|-----------|--------|
| Domain Correctness | ✅ PASS / ⚠️ CONCERNS |
| Risk Assessment | Based on Devil's Advocate findings |
| Integration Impact | Based on Integration Checker findings |

---

## Step 4: Generate Report

Generate a markdown report with this structure:

```markdown
# Deep Verify Report

**Verdict:** {PASS | CONCERNS | FAIL}
**Generated:** {timestamp}
**Domains Analyzed:** {list of domains}
**Experts Consulted:** {count} experts

## Summary

| Dimension | Result |
|-----------|--------|
| Domain Correctness | {result} |
| Risk Assessment | {result} |
| Integration Impact | {result} |

---

## Risk Assessment (Devil's Advocate)

### {IMPACT} Risk: {scenario}

**Pre-mortem:** {failure scenario}
**Likelihood:** {likelihood}
**Impact:** {impact}
**Evidence:** {evidence}
**Mitigation:** {mitigation}

{repeat for each scenario}

---

## Domain Expert Findings

### {Domain Name}

{findings from domain expert}

{repeat for each domain}

---

## Integration Impact

**Affected:** {affected components}
**Dependencies:** {dependencies}
**Coordination:** {coordination needed}

---

## Third-Party Perspective

**Clarity:** {clarity score}
**Questions:** {questions raised}
**Suggestions:** {suggestions}
```

---

## Step 5: Validate Output Format

Before finalizing the report, validate it against the required format specification to ensure consistency.

### Validation Gate

Spawn an output validator sub-agent using the Task tool:

```
Capability: standard

You are an OUTPUT VALIDATOR for deep-verify reports. Your role is to ensure format compliance.

## Files to Validate
- Markdown: {path_to_markdown_file}
- JSON: {path_to_json_file}

## Validation Instructions
Follow the validation procedure defined in: skills/deep-verify/validators/output-validator.md

## Schema Location
JSON Schema: skills/deep-verify/schemas/verification-report-schema.json

## Tasks
1. Load and validate JSON against schema
2. Validate markdown structure and required sections
3. Cross-check consistency between JSON and markdown
4. Generate validation report

## Output Format
Return validation result as JSON with:
- validation_status: PASS or FAIL
- Specific errors and warnings
- Suggestions for fixes

## Strictness
FAIL on any critical errors:
- Missing required fields
- Invalid enum values
- Type mismatches
- Missing required sections
```

### Handling Validation Results

**If validation PASSES:**
- Proceed to Step 6 (Save Report)

**If validation FAILS:**
1. Display all errors and warnings to user
2. Provide specific suggestions for each violation
3. DO NOT save report as "latest"
4. Ask user if they want to:
   - Fix the issues and regenerate
   - Override validation (with explicit confirmation)
   - Cancel verification

**Example failure output:**
```
❌ Validation FAILED

JSON Errors:
- Missing required field: risk_assessment.scenarios
- Invalid verdict value: 'MAYBE' (must be PASS, CONCERNS, or FAIL)

Markdown Errors:
- Missing required section: ## Integration Impact
- Domain 'Security' listed in metadata but no findings section found

Suggestions:
1. Add risk_assessment.scenarios array with at least one scenario
2. Change verdict to one of the valid values
3. Add ## Integration Impact section
4. Add ## Security findings section or remove from domains_analyzed

Would you like to regenerate the report with corrections?
```

---

## Step 6: Save Report

## Artifact Output

Save to `.outputs/verification/{YYYYMMDD-HHMMSS}-verification-{slug}.md` with YAML frontmatter:

```yaml
---
skill: deep-verify
timestamp: {ISO-8601}
artifact_type: verification
domains: [{domain1}, {domain2}]
verdict: PASS | FAIL | CONCERNS        # if applicable
context_summary: "{brief description of what was reviewed}"
session_id: "{unique id}"
---
```

Also save JSON companion: `{timestamp}-verification-{slug}.json`

**No symlinks.** To find the latest artifact:
```bash
ls -t .outputs/verification/ | head -1
```

**QMD Integration (optional, progressive enhancement):**
```bash
qmd collection add .outputs/verification/ --name "deep-verify-artifacts" --mask "**/*.md" 2>/dev/null || true
qmd update 2>/dev/null || true
```

**Note:** Only save reports that pass validation.

---

## Step 7: Configuration (Optional)

The system uses these defaults unless overridden:

**Expert Weights:**
- Devil's Advocate: 40%
- Integration Checker: 15%
- Third-Party Reviewer: 5%
- Domain Experts: 40% (shared pool)

**Output Directory:** `.outputs/verification/`

These can be overridden via:
- Environment variables (e.g., `DEEP_VERIFY_OUTPUT_DIR`)
- Config files in `.outputs/verification/config.yaml`
- Command-line arguments

---

## Multi-Model Second Pass (Optional)

If multi-model confidence is needed after verification:

Invoke `deep-council` in fallback mode with:
- `review_scope`: same scope as this verification
- `context_summary`: paste context_summary from this verification
- `intensity`: "standard" (or match this verification's intensity)

`deep-council` will run all available bridges (bridge-claude if Task tool
accessible, plus any CLI bridges installed), providing cross-model confirmation of critical findings.
Merge `multi_model_confirmed` findings from council report into this
verification's final report.

---

## Notes

- **Model-agnostic**: Uses capability levels ("highest", "high", "standard") not specific model names
- **Domain-agnostic**: Works for any domain detected in conversation
- **Conversation-driven**: All context extracted from what was discussed
- **No triggers/keywords**: Analyzes conversation naturally, doesn't match patterns
- **Balanced**: Devil's Advocate weight equals all domain experts combined to counter confirmation bias
- **Multi-Model**: Optionally follow with `deep-council` for cross-model confidence
- **Context Routing**: If the artifact is complex or multi-domain, invoke the `context` skill first to classify artifact type and determine optimal routing (parallel-workflow vs debate-protocol vs deep-council)
- **DeepWiki (optional)**: For code artifacts, invoke `Skill("deepwiki")` before spawning domain experts if the codebase has a Devin-indexed wiki — provides architectural context that sharpens domain expert analysis. Non-blocking; skip if unavailable.
