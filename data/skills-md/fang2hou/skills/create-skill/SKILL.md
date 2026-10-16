---
name: create-skill
description: >
  Creates spec-compliant Agent Skills from requirements through validated delivery: intent analysis, domain research, SKILL.md authoring, and with/without-skill evals. Use when creating, drafting, or scaffolding a new Agent Skill.
license: MIT
compatibility: Requires file write access to create skill files. Works with any agent supporting the Agent Skills standard.
metadata:
  author: fang2hou
  version: "2.3"
  sources: "agentskills.io specification, best practices, evaluating-skills, and optimizing-descriptions guides; Anthropic skill authoring best practices"
---

# Create Skill

End-to-end workflow for creating spec-compliant, production-quality Agent Skills, from user intent to an evaluated skill.

## When to Use

- Creating a new Agent Skill from scratch ("create a skill", "new skill")
- Scaffolding a skill from a concept or requirement ("build a skill", "make a skill")
- Converting ad-hoc agent instructions, a repeated checklist, or a worked session into a reusable skill, or invoking this skill by name

## When NOT to Use

- Improving, auditing, or refactoring an existing skill (use improve-skill instead)
- Always-on project facts or conventions that apply to every task; those belong in the project's agent instruction file (for example `AGENTS.md`), not in an on-demand skill
- General code generation unrelated to Agent Skills

## Inputs

| Input               | Required | Format               | Example                                   |
| ------------------- | -------- | -------------------- | ----------------------------------------- |
| Invocation argument | No       | Skill name or brief  | `csv-analyzer`, "a skill that parses CSV" |
| User context        | Yes      | Requirements, domain | "Must use pandas, output markdown tables" |

**Cross-platform note**: Clients that expose an invocation argument (for example a `$ARGUMENTS` placeholder) pass the skill name or brief through it. If no such argument is available or it does not resolve to a skill concept, ask the user what skill to create before proceeding.

## Hard Rules

1. **Spec compliance**: All output conforms to the Agent Skills specification. Use only the six spec frontmatter fields unless the user names a target client that needs more; some clients reject unknown keys on upload, so client-only fields break portability.
2. **Domain-grounded**: Gather project-specific or domain-specific context before writing. A skill written from generic knowledge alone produces vague instructions the agent already knew.
3. **No empty sections**: Every section contains concrete steps or rules. Remove placeholders.
4. **Progressive disclosure**: SKILL.md stays under 500 lines and about 5,000 tokens. Move detail needed only in specific situations to `references/`.
5. **Validate before delivering**: Run the quality checklist and a trial run before presenting the skill.
6. **No vague instructions**: Every instruction states what to do, under which condition, and how to verify the result. Phrases such as "handle appropriately", "as needed", "ensure quality", or "follow best practices" are detection signals: rewrite the instruction unless the surrounding text already supplies the condition, the default, and a verifiable outcome.
7. **No surprises**: The skill does only what its description says. Do not embed secrets, hidden network calls, or destructive defaults; a skill with external side effects runs them only after an explicit confirmation step.

## Key Principles

- **Context economy**: Add what the agent lacks and omit what it already knows. Test every line: "Would the agent get this wrong without this instruction?"
- **Explain why, not louder**: Current models follow instructions precisely and over-apply emphatic wording. Write a plain instruction plus its reason ("Run the check first, because a failed migration cannot be rolled back"). Treat ALL-CAPS, "CRITICAL", or stacked MUST/NEVER as a signal to rewrite.
- **No conflicting instructions**: When two rules can collide, state which one wins. Contradictions make reasoning models spend effort reconciling them and produce inconsistent runs.
- **Coherent scope units**: Encapsulate one coherent unit of work that composes with other skills. Too narrow, and several skills load for one task; too broad, and activation becomes imprecise.
- **Calibrate to fragility**: Use high freedom (goals, heuristics, and why) when approaches are valid and variation is safe; use low freedom (exact steps) when work is fragile or destructive.
- **Moderate detail**: Prefer concise stepwise guidance plus one working example over exhaustive documentation; bloated skills make agents pursue instructions that do not apply.
- **Provide defaults, not menus**: Pick one recommended approach and mention alternatives briefly as an escape hatch.
- **Favor procedures over declarations**: Teach how to approach a class of problems, not what to produce for one instance.
- **Consistent terminology**: Choose one term per concept and reuse it verbatim across the skill and references.
- **No time-sensitive content**: State durable rules; put superseded guidance in a clearly labelled deprecated or old-patterns section.
- **Front-load critical content**: Put the workflow, hard rules, and gotchas before background material. Some clients keep only the beginning of a skill after context compaction.

## Workflow

### Phase 0: Intent Analysis and Requirements Capture

The quality of the entire skill depends on getting this phase right. Do not jump straight to structure or writing; extract only the intent details that change the skill's scope, instructions, or validation.

**Step 1: Analyze user intent.** Capture:

- **Outcome:** What should the skill reliably enable beyond the surface request?
- **Audience/context:** Who will use it, under what task conditions, and what domain knowledge do they lack?
- **Success:** What observable result proves the skill worked?
- **Boundary:** What should this skill explicitly not attempt?

If the conversation already contains a worked session of the task (steps that succeeded, corrections the user made, input and output formats), extract these answers from it first and ask the user only to fill gaps.

**Step 2: Capture requirements.**

1. **Purpose**: What problem does it solve? One sentence that would make a stranger understand the value.
2. **Triggers**: When should an agent activate this skill? List 3-5 realistic user prompts that match how users actually phrase requests. Agents usually consult a skill only for tasks they cannot handle alone, so use substantive multi-step prompts, not one-step requests.
3. **Scope boundary**: What is in scope, and what is explicitly out of scope? Name any sibling skill whose triggers overlap. Scope creep is the main cause of bloated skills.
4. **Domain type**: Workflow (step-by-step process), Expertise (domain knowledge), or Hybrid?
5. **Side effects**: Does the skill write outside the workspace, call external services, publish, or delete? If yes, it needs a confirmation gate and should run only on explicit request.

Output as a Requirements Card:

```
Intent: [why the user wants this — the real goal]
Purpose: [one sentence]
Domain: [workflow | expertise | hybrid]
Triggers: [3-5 example user prompts]
In Scope: [list]
Out of Scope: [list, including overlapping sibling skills]
Side Effects: [none | list, with confirmation point]
```

**Edge cases**:

- If the skill name already exists in the workspace, warn the user and confirm: overwrite, version, or pick a new name.
- If requirements are contradictory (for example an "expertise" domain whose trigger list implies a workflow), flag the conflict and ask for clarification.
- If the user provides only a tool name (for example "make a jq skill"), treat it as a starting concept and analyze intent before designing.
- If the content is a fact or convention every task in the repository needs, recommend the always-on instruction file instead of a skill, and stop unless the user still wants a skill.

**Gate 0 (proceed only when all are true):**

- [ ] Intent is clear (both why the skill is needed and what it produces)
- [ ] Purpose is specific (not "helps with X")
- [ ] At least 3 trigger scenarios documented
- [ ] Scope boundary and side effects explicitly defined
- [ ] No name collision with existing skills (or user confirmed overwrite)

_If gate fails_: Ask the user clarifying questions rather than assuming. If no user is reachable, record each unanswered question, proceed with the most defensible assumption, and label those assumptions in the delivered output.

### Phase 1: Context Gathering

Skipping context gathering is the main cause of weak skills. Gather the domain knowledge the target agent does not already have.

**Required actions (attempt each one and record the observable evidence or why the source class is unavailable):**

1. **Codebase exploration**: Search relevant files, patterns, conventions, and APIs; record the search scope, queries, and paths or findings. If no related codebase is available, record that fact and why.
2. **Documentation lookup**: Read official documentation and at least one real-world example for each external tool or library involved; record the URLs or identifiers and the usage detail extracted. If none is involved or docs are inaccessible, record the reason.
3. **Existing skill analysis**: Read 1–2 comparable skills in the workspace; record their paths and conventions reused, including the collection's naming pattern. If no comparable skill exists, record the search scope.
4. **High-signal expertise sources**: Read available transcripts or corrections, runbooks, style guides, API specs or schemas, review comments, version-control fixes, or failure/resolution records; record source identifiers and the concrete lesson. If none is accessible, list the classes checked and why.
5. **Gotchas hunt**: Search gathered sources for non-obvious constraints and record each gotcha with its source and consequence; if none is found, record exactly "No domain-specific gotchas identified during research" and what was checked.

**Sources priority:**

1. Hands-on corrections, real failure cases, and version-control fixes
2. Existing project files, runbooks, style guides, API specs, and schemas
3. Official documentation and code review comments
4. User-provided knowledge and corrections
5. Real-world examples from open-source projects

**Edge cases**:

- If no codebase or external docs are available and the user cannot provide domain expertise, proceed with a disclaimer: "This skill was authored from general knowledge. Review and update with domain-specific details before production use."
- If context gathering reveals the task is too broad for a single skill (for example "build a CI/CD pipeline"), suggest splitting into multiple focused skills.

**Gate 1 (proceed only when all are true):**

- [ ] At least one high-signal source consulted (or disclaimer added)
- [ ] Gotchas hunt performed; findings recorded, or "No domain-specific gotchas identified during research" stated explicitly
- [ ] Unavailable source classes recorded

_If gate fails_: Gather more context before proceeding. Search more, read more files, or ask the user; do not move to Phase 2 on generic knowledge alone.

### Phase 2: Author and Structure

Design the directory layout and write the content together.

**Step 1: Plan the structure.** Decide:

```
skill-name/
├── SKILL.md          # Always required
├── references/       # Only for detail needed in specific situations
├── scripts/          # Only if reusable executable logic is needed
└── assets/           # Only if templates/data files are needed
```

Content split:

| Location      | Content                                              |
| ------------- | ---------------------------------------------------- |
| SKILL.md body | Core workflow, hard rules, gotchas, key instructions |
| references/   | Detailed criteria, extended examples, lookup tables  |
| scripts/      | Deterministic code the agent would otherwise rewrite |
| assets/       | Templates and data files used in the output          |

#### Calibrate each section

| Freedom level    | Use when                                                               | Instruction shape                                                                       |
| ---------------- | ---------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| **High freedom** | Multiple approaches are valid and mistakes are cheap or reversible     | State goals, heuristics, and why; let the agent choose the route.                       |
| **Low freedom**  | Work is fragile, destructive, order-dependent, or consistency-critical | Give the exact sequence, command, inputs, and expected result; do not invite variation. |

Most skills mix both levels. Calibrate per section rather than applying one control level to the whole skill.

#### Instruction patterns

Use the pattern that matches the work: **Gotchas**, **output-format template**, **progress checklist**, **validation loop**, **plan-validate-execute**, **worked examples**, or **bundled script**. Load [references/instruction-patterns.md](references/instruction-patterns.md) when choosing patterns, calibrating freedom, rewriting emphatic directives, or needing concrete templates.

#### Bundled scripts

Prefer instructions; add a script only when the work must be deterministic or the agent would otherwise rewrite the same logic on every run. Only when the skill will ship `scripts/`, load [references/script-design.md](references/script-design.md) before writing a script; it defines the non-interactive interface, robustness, and packaging requirements.

**Step 2: Write frontmatter.** For complete field rules and client-specific fields, see [references/spec-quickref.md](references/spec-quickref.md).

```yaml
---
name: skill-name # Required: lowercase, hyphens, matches directory
description: > # Required: WHAT + WHEN, under 1024 chars, no angle brackets
  [What it does]. Use when [trigger scenarios].
license: MIT # Optional
compatibility: ... # Optional: only if specific env requirements exist
metadata: # Optional
  author: ...
  version: "1.0"
---
```

Choose a `name` that follows the collection's existing naming pattern; with no pattern, use a specific action-oriented name such as `processing-pdfs`. Avoid vague names (`helper`, `utils`) and the vendor-reserved words `anthropic` and `claude`.

The `description` determines whether the skill triggers at all. Put the key use case in the first sentence, cover both what and when, and include the trigger phrases from Phase 0. See [references/description-guide.md](references/description-guide.md).

**Step 3: Write body content.** Use this section order (include only sections with substantive content):

```markdown
# [Skill Title]

One-sentence summary.

## When to Use

- [Trigger scenario 1]
- [Trigger scenario 2]

## When NOT to Use

- [Out-of-scope scenario]

## Inputs

| Input | Required | Format | Example |
| ----- | -------- | ------ | ------- |

## Hard Rules

1. [Non-negotiable constraint, with its reason]

## Workflow

### Step 1: [Action]

[Instructions with expected result]

## Gotchas

- [Non-obvious fact that defies reasonable assumptions]

## Output Contract

On completion, return:

1. [Expected output]
```

**Anti-vagueness rule**: Can someone unfamiliar with this domain read the instruction and know what to do without guessing? If not, rewrite it. Bad examples and their fixes:

- ❌ "Handle errors appropriately" → ✅ "If the API returns non-200, log the status code and retry once with exponential backoff"
- ❌ "Follow the project's conventions" → ✅ "Read `src/auth/middleware.ts` and mirror its error handling pattern"
- ❌ "Optimize if needed" → ✅ "If the function processes >1000 items, use batching with batch size 100"
- ❌ "CRITICAL: NEVER touch prod" → ✅ "Run only against the staging profile; production writes cannot be reverted by this skill"

**Step 4: Create reference files** when SKILL.md would exceed ~300 lines or a detail block is only needed in specific situations. Link each one directly from SKILL.md and say when to load it:

```markdown
Read [references/api-errors.md](references/api-errors.md) when the API returns a non-200 status.
```

Give every reference file over 100 lines a contents list at the top so a partial read still shows its scope.

**Gate 2 (proceed only when all are true):**

- [ ] Frontmatter passes all spec validation rules (name matches directory, description has WHAT+WHEN)
- [ ] Body content is concrete (every instruction passes the anti-vagueness test)
- [ ] No two instructions conflict without a stated precedence
- [ ] All file references point to files that exist and are non-empty
- [ ] No placeholder or TODO sections remain
- [ ] SKILL.md is under 500 lines
- [ ] Gotchas section has at least one non-obvious insight, or explicitly states that none were identified during research

_If gate fails_: Fix the specific issue. Remove empty sections, validate frontmatter, create missing files. Maximum 2 correction cycles before escalating to the user.

### Phase 3: Validation

Run the quality checklist. For the full checklist, see [references/quality-checklist.md](references/quality-checklist.md).

If the optional `skills-ref` CLI is available, run `skills-ref validate ./skill-name` for automated spec checking; otherwise perform the quick validation below and record that the CLI was unavailable. If the project has its own skill validator (for example a `scripts/check-skills.sh`), run it as well.

**Quick validation**:

1. **Spec compliance**: Frontmatter fields valid, name matches directory, body is Markdown
2. **Description quality**: Covers both WHAT and WHEN, front-loads the key use case, includes trigger keywords from Phase 0
3. **Progressive disclosure**: SKILL.md under 500 lines, references load on demand
4. **Instruction quality**: No vague phrases, no unexplained emphatic directives, no unresolved conflicts
5. **File integrity**: All references resolve to existing, non-empty files

Present results:

```
┌──────────────────────────────┬────────┬──────────────────────────┐
│ Check                        │ Result │ Detail                   │
├──────────────────────────────┼────────┼──────────────────────────┤
│ Frontmatter spec compliance  │ PASS   │ All fields valid         │
│ Name matches directory       │ PASS   │ Both: skill-name         │
│ Description quality          │ PASS   │ WHAT + WHEN covered      │
│ Body under 500 lines         │ PASS   │ N lines                  │
│ File references valid        │ PASS   │ All resolve              │
│ No placeholder sections      │ PASS   │ All sections populated   │
│ Instruction quality          │ PASS   │ No vague or conflicting  │
└──────────────────────────────┴────────┴──────────────────────────┘
```

**Gate 3 (proceed to Phase 4 only when all are true):**

- [ ] All spec compliance checks PASS
- [ ] No vague or conflicting instructions remain
- [ ] All file references resolve

_If gate fails_: Return to Phase 2. Maximum 2 correction cycles before escalating.

### Phase 4: Trial Run and Iterate

Before delivery, run the skill on 2–3 realistic tasks. Each run happens in a **fresh context**: a session or subagent with no prior conversation about this skill. The context that authored the skill is not fresh. For each task, launch the with-skill run and a **baseline run** without the skill at the same time, so both see the same environment, then compare outcomes.

1. Record tokens and elapsed time for every run as soon as it finishes; some harnesses report them only once.
2. Read the execution trace, not only the final output. Record wasted steps, ambiguity, and unproductive paths.
3. Grade objective assertions with quoted evidence; add assertions after seeing the first outputs.
4. Turn every correction you had to make into either a Gotchas entry in `SKILL.md` or a general instruction fix. Do not patch the skill to fit one test prompt. If the run needed no corrections, state that explicitly.
5. If the baseline already succeeds, say so and consider whether the skill adds enough value to justify its context cost. If pass rates stall as rules are added, try removing instructions.
6. Repeat after fixes when the evidence shows the skill is ambiguous or incomplete. For eval storage, trigger evals, blind comparison, or multi-model targets, load [references/eval-guide.md](references/eval-guide.md).

If no fresh-context mechanism is available, state that, run the task yourself from the written skill only, and label the evidence as same-context.

**Gate 4 (deliver only when all are true):**

- [ ] With-skill and baseline runs completed in fresh contexts (or the same-context limitation is stated), with outcomes, tokens, and time recorded
- [ ] The execution trace was reviewed, not only the final output
- [ ] Every correction observed maps to a Gotchas entry or general instruction fix, or the record states that none were needed
- [ ] The comparison states whether the skill adds value; a successful baseline is not hidden

_If gate fails_: Fix the evidence-backed issue, run the trial and baseline again, and update the record. If the baseline remains as good, report that no additional value was demonstrated instead of adding needless instructions.

## Self-Correction Protocol

### Content-Level Rules

| Trigger                                                 | Automatic Action                                                                                                    |
| ------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| SKILL.md exceeds 500 lines                              | Split overflow into `references/`                                                                                   |
| Description over 250 chars (hard limit 1024)            | Front-load key use case, move details to body                                                                       |
| Description or name contains `<` or `>`                 | Remove the angle brackets; some clients reject them                                                                 |
| `name` doesn't match directory                          | Fix name field to match directory                                                                                   |
| File reference points to void                           | Create the file or remove the reference                                                                             |
| Vague instruction detected                              | Replace with specific action + expected result                                                                      |
| ALL-CAPS or stacked MUST/NEVER without a reason         | Rewrite as a plain instruction plus the reason it matters                                                           |
| Two instructions conflict                               | State which one wins, or qualify the loser's condition                                                              |
| Client-only frontmatter field in a portable skill       | Remove it, or record the target client in `compatibility` when the user requires that field                         |
| Empty section found                                     | Remove it entirely                                                                                                  |
| No gotchas identified                                   | Re-examine the domain. If none are found, explicitly state "No domain-specific gotchas identified during research." |
| Generic knowledge explains what the agent already knows | Delete or rewrite the line with domain-specific value; apply the context-economy test                               |
| Time-sensitive statement present                        | Replace it with a durable rule or label superseded material as deprecated/old patterns                              |
| Multiple options offered with no default                | Choose one default and mention alternatives in one escape clause                                                    |
| Reference chain is deeper than one level                | Link directly from `SKILL.md` or move the detail to a directly linked file                                          |
| Windows-style backslash path                            | Replace it with a forward-slash relative path                                                                       |
| Script requires interactive input                       | Accept flags, environment variables, or stdin and fail with usage guidance                                          |

### Workflow-Level Protocol

1. **Drift detection**: After each phase, compare the output against the phase's gate conditions and the Requirements Card from Phase 0. If the output doesn't serve the stated intent, you've drifted.
2. **Auto-retry**: If a gate fails, attempt the phase-specific correction documented in the gate's "If gate fails" section.
3. **Escalation**: If the same gate fails twice after correction attempts, stop and report to the user with: which gate failed, what correction was attempted, what manual input is needed.
4. **Regression guard**: If a later phase invalidates work from an earlier phase, return to the failing phase instead of silently patching.
5. **Scope lock**: If during authoring you discover the skill needs capabilities beyond the Requirements Card, do not expand scope. Note them as "Deferred Recommendations" in the output.

## Output Contract

On completion, deliver:

1. **Skill directory**: Complete skill directory with all files created, ready to use
2. **Validation results**: The check/result/detail table shown in Phase 3, one row per check
3. **Design decisions**: Brief summary of structural choices (why this layout, why these sections)
4. **Deferred recommendations**: List of ideas surfaced during creation but not included (scope limit reached, ambiguity unresolved, etc.)
5. **Trial-run evidence**: The realistic tasks run, with-skill and baseline outcomes, token and time deltas, what the execution traces revealed, and what changed as a result

Keep the human-readable report as the primary deliverable. When another skill consumes it, preserve these stable fields in this order:

```text
fields (stable order):
1. skill_directory
2. validation_results
3. design_decisions
4. deferred_recommendations
5. trial_run_evidence
```

Running this skill again with the same requirements produces an equivalent skill. If a skill directory already exists, overwrite it only after confirmation.

## References

- [Spec Quick Reference](references/spec-quickref.md): load when writing or validating frontmatter, or when the user targets a specific client
- [Description Guide](references/description-guide.md): load when writing the description or when a trigger eval fails
- [Quality Checklist](references/quality-checklist.md): load in Phase 3
- [Instruction Patterns](references/instruction-patterns.md): load when selecting patterns, calibrating instruction freedom, or rewriting emphatic directives
- [Script Design](references/script-design.md): load before adding `scripts/`
- [Evaluation Guide](references/eval-guide.md): load in Phase 4 for eval storage, trigger evals, blind comparison, or multi-model and multi-agent targets
