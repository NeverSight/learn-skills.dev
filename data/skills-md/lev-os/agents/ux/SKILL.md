---
name: ux
description: "UX design hub: 7-step wireframe pipeline + product design (design-os) + visual prototyping (pencil) + agentic UX patterns (lev-ref). Use for wireframes, flows, IA, JTBD, product design, CLI design, agentic UX, design systems, or component architecture."
skill_type: hub
category: design-ux
related_skills:
  - work
  - lev-cdo
  - lev-research
hub_routes:
  ux-pipeline: "wireframe, flow, IA, journey, interaction, JTBD, task graph"
  design-os: "product design, vision, roadmap, data model, design system, export"
  pencil-mcp: "visual design, .pen file, mockup, design sweep"
  agentic-ux: "CLI design, progressive disclosure, prompt steering, CLI-as-prompt"
  browse: "design skill, find skill, what skills"
---

# UX Design Hub

Routes to specialist sub-skills or runs the built-in 7-step UX pipeline.

## Hub Decision Tree

```
Request arrives
|
+-- Product planning (vision, roadmap, data model, export)?
|   -> Load: skill://lev-design-os
|      (~/.agents/skills/lev-design-os/SKILL.md + references/)
|
+-- Visual design / .pen file / design sweep?
|   -> Use Pencil MCP tools (batch_design, get_screenshot, style guides)
|      Ref: skillsdb://design-ux/pencil for character/illustration work
|
+-- CLI / agentic UX patterns?
|   -> Load Phase 0.5 lev-ref patterns (below)
|
+-- UX pipeline (wireframes, flows, IA, JTBD)?
|   -> Run 7-step pipeline (this skill body)
|
+-- "What design skills exist?" / browse?
|   -> Query: ls ~/.agents/skills-db/design-ux/
|      Deep:  ~/.agents/lev-skills.sh discover "{query}" --json --category=design
|
+-- Ambiguous?
    -> Ask one clarifying question, then route
```

## Skills-DB Design Catalog (skillsdb://design-ux/*)

| Skill | Load when |
|-------|-----------|
| design-os | Product vision, roadmap, data model, design tokens, export |
| superdesign-prompt-library | AI image prompts, style/layout/component prompts |
| swiftui-* (6 skills) | SwiftUI/iOS/macOS UI work |
| metal-shaders, vfx-spell-effects | GPU graphics, visual effects |

## UX Thinking Patterns (scored, from skills-db)

Load from ~/.agents/skills-db/thinking/patterns/{name}/SKILL.md when reasoning depth needed:

| Pattern | Score | Use when |
|---------|-------|----------|
| nielsen-heuristics | 50 | Usability evaluation |
| design-of-everyday-things | 48 | Affordance/signifier analysis |
| dont-make-me-think | 48 | Simplicity audit |
| laws-of-ux | 45 | Psychology-based design |
| wcag | 45 | Accessibility compliance |
| design-systems | 45 | Component architecture |
| refactoring-ui | 44 | Developer-facing design tactics |

## Hub Shortcuts

| Key | Action | Route |
|-----|--------|-------|
| (p) | Product design wizard | skill://lev-design-os |
| (w) | Run UX pipeline | Steps 1-7 below |
| (v) | Visual design / .pen | Pencil MCP tools |
| (c) | CLI/agentic UX patterns | Phase 0.5 lev-ref |
| (b) | Browse design skills | lev-skill resolve |

---

# UX Pipeline

## Mode Parsing

Treat the user's message (including any `/ux ...` text) as the input.

- If it contains `full` or `interactive`: ask a small set of clarifying questions first, then run step-by-step.

- If it contains `step N` (N=1..7): run only that step and update artifacts.

- If it contains `continue`: resume the most recent run folder under `.lev/ux/`.

- Otherwise: AUTO mode. Run all 7 steps end-to-end and produce wireframes.

## Output Location

Create a run folder:

- `RUN_DIR=.lev/ux/{YYYYMMDD-HHMMSS}-{slug}/`

Write artifacts below. If resuming, reuse the existing `RUN_DIR`.

Artifacts (expected):

- `problem_spec.yaml`

- `routed_skills.json`

- `jobs.graph.json`

- `task_graph.json`

- `ia_schema.json`

- `interaction_fsm.json`

- `components.md`

- `wireframes.md`

- `summary.md`

## Phase -1: Setup (Deterministic)

1. Create run dir and establish shell vars:

```bash
TS="$(date +%Y%m%d-%H%M%S)"
SLUG="$(printf '%s' "$USER_MSG" | tr '[:upper:]' '[:lower:]' | rg -o "[a-z0-9]+" | head -n 6 | paste -sd- -)"
RUN_DIR=".lev/ux/${TS}-${SLUG}"
mkdir -p "$RUN_DIR"
```

2. Persist the raw request for traceability:

```bash
printf '%s\n' "$USER_MSG" > "$RUN_DIR/request.txt"
```

## Phase 0: Prior Art (Fast)

1. If `bd` exists and `.beads/` exists:

- `bd list --status=open | rg -n "ux|design|wireframe|ia|flow" -i || true`

2. Scan local UX artifacts:

- `ls -t .lev/ux 2>/dev/null | head -n 10 || true`

3. Scan UI code quickly (keep it cheap):

- `rg -n "struct\\s+.*View\\b|SwiftUI|Navigation(Stack|SplitView)|TabView" apps packages extensions 2>/dev/null | head -n 50 || true`

If you find relevant prior art, cite paths in `summary.md` and either extend it or explicitly supersede it.

## Phase 0.5: Agentic UX Patterns (lev-ref)

Apply lev-ref patterns to all UX outputs (especially `summary.md` and any routed-skill handoff).

This phase doubles as the **agentic-ux** hub route. Load directly when asked about CLI design, progressive disclosure, or prompt steering — no need to run the full 7-step pipeline.

Key patterns:
- **CLI-as-Prompt**: Every CLI surface is a prompt-steering opportunity
- **Progressive Disclosure**: Metadata first, body on trigger, references on demand
- **Every Surface a Steering Attempt**: Follow-ups, related skills, confidence inline
- **Audio Design**: Consider sonic feedback for agent interactions

1. Load lev-ref patterns:

```bash
sed -n '1,220p' docs/_inbox/lev-ref/SKILL.md
```

2. Apply inline conventions (CLI-as-Prompt):

- Add confidence lines like `[85% confident]` for key recommendations.

- Add `→ Next:` and `→ Related:` follow-ups.

- Add a short `💡 Tip:` in `summary.md` if there's a non-obvious UX lesson.

## Phase 0.6: Skills-DB Enrichment

Route to specialized skills using the Hub Decision Tree above.

1. Check hub_routes (frontmatter) for trigger match against request keywords.
   - If match -> load that skill, optionally resume pipeline at Step 3+.

2. If no hub_route match, query skills-db dynamically:

```bash
# Design-ux category first (high-signal, 12 skills)
rg -l -i "{keywords}" ~/.agents/skills-db/design-ux/*/SKILL.md

# Broader search only if design-ux returns empty
lev-skill resolve "{keywords}" --json 2>/dev/null | jq '.results[:5]'
```

3. If curated scores available, prefer higher-scored patterns:

```bash
grep -i "{keyword}" ~/.agents/skills-db/thinking/11-ui-ux/task.csv \
  | sort -t, -k8 -rn | head -3
```

4. Emit routed_skills.json (keep existing schema for compatibility):

```json
{ "request_terms": [...], "candidates": [...], "selected": [...] }
```

5. Present discovered skills:
   - 1 clear match -> propose loading it
   - 2-3 matches -> ranked list, let user choose
   - 0 matches -> continue with built-in UX pipeline

6. Continue pipeline regardless — routing enriches, never blocks.

## Step 1: Problem Framing

Write `problem_spec.yaml`:

```yaml
problem:
  statement: "{1-2 sentences}"
  for_whom: "{primary user segment}"
  constraints:
    - "{constraint}"
  success_criteria:
    - "{measurable outcome}"
  scope:
    in: ["{in}"]
    out: ["{out}"]
```

Rules:

- Make success criteria measurable.

- Keep scope boundaries crisp.

## Step 2: Jobs To Be Done (JTBD)

Write `jobs.graph.json`:

```json
{
  "jobs": [
    {
      "id": "job-1",
      "statement": "When I {situation}, I want to {motivation}, so I can {outcome}",
      "type": "functional",
      "triggers": ["{trigger}"],
      "user_types": ["{archetype}"]
    }
  ]
}
```

Rules:

- Prefer progress language over feature language.

- Include at least one emotional or social job if relevant.

## Step 3: Task Decomposition

Write `task_graph.json`:

```json
{
  "tasks": [
    {
      "id": "task-1",
      "name": "{verb} {object}",
      "entry_state": "{precondition}",
      "exit_state": "{postcondition}",
      "happy_path": ["{step}"],
      "failure_modes": ["{failure}"],
      "depends_on": []
    }
  ]
}
```

Rules:

- Include failure modes and recovery paths.

- Keep tasks at a UI-actionable granularity.

## Step 4: Information Architecture (IA)

Write `ia_schema.json`:

```json
{
  "entities": [
    {"name": "{Entity}", "attributes": ["{attr}"], "actions": ["{verb}"]}
  ],
  "relationships": [
    {"from": "{Entity}", "to": "{Entity}", "type": "has_many"}
  ],
  "navigation": {
    "primary": ["{screen}"],
    "secondary": ["{screen}"]
  }
}
```

Rules:

- Avoid navigation that doesn't map to an entity or job.

## Step 5: Interaction Models

Write `interaction_fsm.json`:

```json
{
  "screens": [
    {
      "id": "screen-1",
      "name": "{Screen Name}",
      "states": ["idle", "loading", "empty", "error", "success"],
      "transitions": [
        {"from": "idle", "event": "tap_primary", "to": "loading"}
      ],
      "feedback": ["spinner", "toast"]
    }
  ]
}
```

Rules:

- Explicitly model `loading`, `empty`, and `error` states.

- Call out accessibility considerations if there's complex interaction.

## Step 6: Components

Write `components.md`:

- Reusable components list (name, purpose, props/data).

- Screens-to-components mapping.

Rules:

- Prefer composable components over mega-views.

- Name components after user intent (not implementation).

## Step 7: Wireframes

Write `wireframes.md`:

- A short global nav map.

- For each screen:

- Purpose (one line).

- Primary actions (1-3).

- Layout: header/body/footer sections.

- State variants: idle/loading/empty/error/success.

If the user asks for a design-file deliverable, propose using the `pencil` tool to generate a `.pen` wireframe and confirm the target path under `.lev/ux/`.

## Final Summary

Write `summary.md`:

- Problem + success criteria.

- Key tradeoffs and open questions.

- The wireframe screen list (ordered).

- What to implement first (smallest shippable slice).

- Include lev-ref inline conventions: `[N% confident]`, `→ Next:`, and `💡 Tip:`.

## Technique Map

- **Identify scope** — Determine what the skill applies to before executing.
- **Follow workflow** — Use documented steps; avoid ad-hoc shortcuts.
- **Verify outputs** — Check results match expected contract.
- **Handle errors** — Graceful degradation when dependencies missing.
- **Reference docs** — Load references/ when detail needed.
- **Preserve state** — Don't overwrite user config or artifacts.

## Technique Notes

Skill-specific technique rationale. Apply patterns from the skill body. Progressive disclosure: metadata first, body on trigger, references on demand.

## Prompt Architect Overlay

**Role Definition:** Specialist for ux domain. Executes workflows, produces artifacts, routes to related skills when needed.

**Input Contract:** Context, optional config, artifacts from prior steps. Depends on skill.

**Output Contract:** Artifacts, status, next-step recommendations. Format per skill.

**Edge Cases & Fallbacks:** Missing context—ask or infer from workspace. Dependency missing—degrade gracefully; note in output. Ambiguous request—clarify before proceeding.
