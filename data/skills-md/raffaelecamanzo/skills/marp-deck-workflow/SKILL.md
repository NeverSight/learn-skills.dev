---
name: marp-deck-workflow
description: Interactive presentation consultant that guides users through planning, visual design, and generation consultations before delegating to sub-skills. Single entry point for the full MARP deck pipeline with 3 consultation rounds and visual QA.
---

# Marp Deck Workflow — Presentation Consultant

## Purpose

Guide the user through creating a polished MARP deck via **3 consultation rounds** (planning, visual design, generation) before each delegation to a sub-skill. This produces higher-quality decks by incorporating user intent at every stage rather than running a silent pipeline.

---

## Inputs

- `definition/deck-definition.md` — **optional** (created interactively if missing)
- `.marp/references/deck-template.md` — **required** (source of truth for style variants)

## Outputs

- `definition/deck-definition.md` (created or updated with `## Workflow Notes`)
- `planning/deck-plan.md`
- `planning/deck-visual-design.md`
- `diagrams/*.mmd` (as needed)
- `.marp/assets/*.png` (generated from Mermaid/Excalidraw)
- `slides/deck.md`
- `slides/deck-notes.md`
- `output/<slugified-title>_<date>.pdf` (from `task pdf`)

---

## Interaction Style

Throughout all consultation rounds, follow these principles:

- **Opinionated**: Lead with recommendations — "Given [context], I recommend X because..." not "Do you want X or Y?"
- **Batched**: Ask 3–5 related questions per round, not one-at-a-time or 10-at-once
- **Adaptive**: If the user gives brief answers, choose sensible defaults and confirm. If the user is engaged, go deeper.
- **Non-redundant**: Never ask what the definition or prior answers already cover
- **Consultative**: This is a conversation, not a checklist. Frame questions around the specific presentation being built.

---

## Step 1 — Establish the Deck Definition

**Two paths:**

### Path A — Definition exists

1. Read `definition/deck-definition.md`
2. Summarize your understanding back to the user: title, audience, key topics, constraints
3. Ask the user to confirm alignment or flag corrections
4. Apply any corrections before proceeding

### Path B — Definition missing

1. Tell the user no definition was found
2. Ask them to describe the presentation:
   - What is the core message?
   - Who is the audience?
   - What is the context (conference talk, boardroom, internal team meeting)?
   - What are the key topics or sections?
   - Any constraints (slide count, time limit, branding)?
3. Synthesize their answers into `definition/deck-definition.md` using the format downstream skills expect (title, sections, key messages, constraints)
4. Show the draft to the user for confirmation before saving

**Gate**: `definition/deck-definition.md` exists and is user-confirmed.

---

## Step 2 — Planning Consultation (Interactive)

Analyze the confirmed definition and ask **3–6 contextual questions**. Only ask questions relevant to THIS specific presentation — skip anything the definition already answers.

| Theme | When to ask |
|-------|-------------|
| Section structure | 3+ distinct topics without clear grouping |
| Opening / intro slide | Definition dives straight into content without setup |
| Executive summary | 15+ planned slides or complex material |
| Closing / CTA | Content implies action or decision from audience |
| Slide count constraints | Content could reasonably be 10 or 30 slides |
| Per-section depth | Sections vary significantly in complexity |
| Audience | Not stated in definition |
| Presentation context | Not stated (conference, boardroom, internal) |

For each question, lead with your recommendation and reasoning. Batch related questions together.

**Gate**: User confirms planning direction.

---

## Step 3 — Delegate to marp-deck-planner

Compile a structured prompt incorporating all planning decisions gathered in Step 2:

```
Build the deck plan for definition/deck-definition.md with these constraints:
- Section dividers for: [confirmed sections]
- Opening: [intro slide yes/no, executive summary yes/no]
- Target: [N] slides, audience: [X], context: [Y]
- Closing: [CTA / summary / none]
- Tone: [formal/conversational/technical]
```

Invoke `marp-deck-planner` via Skill tool with this compiled prompt.

**Gate**: `planning/deck-plan.md` exists and contains at least one section divider.

After the gate passes, summarize the plan to the user (section count, slide count, flow) before proceeding.

---

## Step 4 — Visual Design Consultation (Interactive)

Read `planning/deck-plan.md`, identify slides with `## Image` sections, and ask **3–5 contextual questions** focused only on visuals the plan actually calls for.

| Theme | When to ask |
|-------|-------------|
| Diagram style (Mermaid vs Excalidraw) | Plan includes process/flow visuals |
| Data visualization format | Plan references metrics or comparisons |
| Visual density | Many slides have planned visuals |
| Visual tone | Audience suggests specific aesthetic preferences |
| Brand / color guidelines | No brand guide referenced in definition |

If only 2 slides have images, ask about those 2 specifically. If 10 slides have images, ask about patterns and categories. Lead with recommendations.

**Gate**: User confirms visual direction.

---

## Step 5 — Delegate to marp-deck-visual-designer

Compile a visual design prompt incorporating all decisions from Step 4:

```
Design visuals for planning/deck-plan.md with:
- Diagram style: [Mermaid/Excalidraw/blend]
- Visual tone: [minimal/data-heavy/storytelling]
- Specific guidance for slide [X]: [user preference]
- Brand colors: [if specified]
```

Invoke `marp-deck-visual-designer` via Skill tool with this compiled prompt.

**Gate**:
- `planning/deck-visual-design.md` exists
- Slide count and order match `planning/deck-plan.md`
- Every `## Image` reference in the visual design points to an existing file in `.marp/assets/`

If any gate fails, stop and report the exact mismatch.

---

## Step 6 — Generation Consultation (Interactive)

Read `planning/deck-visual-design.md` and `.marp/references/deck-template.md`.

The template is the **source of truth** for available style variants. Parse it to discover:
- Which **cover variants** exist (names and CSS classes)
- Which **section variants** exist (names and CSS classes)

Then ask the user:

1. **Cover variant** — list the discovered options from the template, recommend one based on presentation context and audience
2. **Section variant** — list the discovered options from the template, recommend one based on content structure
3. **Final adjustments** — any last notes before generation (emphasis areas, tone tweaks, specific slide concerns)

If style preferences already exist in `deck-definition.md`, confirm briefly rather than re-asking from scratch.

After confirmation, update `definition/deck-definition.md` with the confirmed style line:
```
Style preferences: cover=cover-<n>, section=section-<n>
```

Also append the `## Workflow Notes` section to `definition/deck-definition.md` capturing all decisions from the consultation rounds:

```markdown
## Workflow Notes

### Planning Decisions
- Audience: [X], Context: [Y]
- Slide count target: [N], Sections: [list]
- Opening: [intro/exec summary], Closing: [CTA/summary/none]
- Tone: [formal/conversational/technical]

### Visual Decisions
- Diagram style: [Mermaid/Excalidraw/blend]
- Visual tone: [X]
- Specific guidance: [any per-slide notes]

### Style Preferences
Style preferences: cover=cover-<n>, section=section-<n>
```

**Gate**: User confirms ready for generation.

---

## Step 7 — Delegate to marp-deck-gen + Visual QA Loop

Compile a generation prompt with style preferences, visual decisions, and any final notes from Step 6.

Invoke `marp-deck-gen` via Skill tool.

**Gate**: `slides/deck.md` and `slides/deck-notes.md` exist.

### Visual QA Loop

1. Run `task pdf`, then invoke `marp-deck-checker` via Skill tool
2. **PASS** → pipeline complete
3. **FLAWS FOUND** → checker invokes `marp-deck-gen` with a targeted fix prompt (layout/structure fixes only; content shortened only as a last resort for unresolvable overflow)

Feedback loop:
- If `marp-deck-gen` was re-invoked: re-run `task pdf`, then re-invoke `marp-deck-checker`
- Repeat until PASS

**Hard gate**: Do not claim pipeline completion until the checker reports PASS.

---

## Non-goals

- No checklist-style questioning — maintain consultative conversation
- No proceeding without user confirmation at each gate
- No modifying artifacts produced by delegated skills (only `deck-definition.md` is workflow-editable)
- No background execution
- No partial guessing when artifacts disagree
- No diagram generation unless visual design calls for it
- No aesthetic changes not justified by template rules

---

## Error Handling

At any gate failure:
1. Report exactly what is missing or mismatched
2. Do not guess or proceed past the gate
3. Ask the user how to resolve (re-run the sub-skill, adjust inputs, or abort)
