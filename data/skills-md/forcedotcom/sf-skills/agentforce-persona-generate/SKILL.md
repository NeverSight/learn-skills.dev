---
name: agentforce-persona-generate
description: "Use to design an AI agent persona — identity, voice, tone, behavioral style, guardrails — and encode it into Agent Script (.agent files) or Agentforce Builder field values. Runs four sequenced phases (DRAFT, REFINE, SCORE, ENCODE) plus five spokes (NAME, FILL OUT, ADJUST, CHECKLIST, WORKSHOP). Supports greenfield (brand input to a starter .agent file) and brownfield (audit an existing .agent file and re-encode persona fields only), with a 100-point evaluation rubric. Trigger when a user designs a new agent persona, retrofits persona consistency, translates brand guidelines into agent voice, defines tone/register/formality/warmth/humor/personification, encodes a persona for Agent Script or Agentforce Builder, or scores or audits an existing .agent file for persona quality. Do not trigger for building Agentforce actions/metadata, authoring Agent Script flow control without persona work, or testing agent conversations."
metadata:
  relatedSkills:
    - "agentforce-generate"
  version: "3.0"
  domains: ["Agentforce"]
  cliTools:
    - tool: ["python3"]
      semver: ">=3.10.0"
allowed-tools: Read Write AskUserQuestion Glob Grep
---

# Designing Agent Persona

## How to Use

This skill designs an AI agent persona for Salesforce Agentforce. It walks through four sequenced phases (DRAFT → REFINE → SCORE → ENCODE) and offers five spokes (NAME, FILL OUT, ADJUST, CHECKLIST, WORKSHOP) you can run any time after DRAFT.

**What it produces:**
- A persona document (`persona/[agent-name]/persona.md`) — who the agent is, how it sounds, what it never does
- A sample dialog (`persona/[agent-name]/sample-dialog.md`) — the persona in action
- An evaluation report on request (`persona/[agent-name]/evaluation.md`) — 100-point rubric, gap analysis, recommendations
- A completeness checklist on request (`persona/[agent-name]/checklist.md`) — what's filled in, what's missing
- A workshop outline on request (`persona/[agent-name]/workshop-outline.md`) — stakeholder questions, dimension cards
- An encoding artifact on request — valid Agent Script `.agent` file, OR Agentforce Builder field values

**Session resumption:** If you stop mid-phase, your progress is preserved in the conversation and can be resumed.

## When to Use This Skill

- Designing a new Agentforce agent and need to define its personality before building (greenfield)
- Auditing an existing `.agent` file's persona consistency (brownfield)
- Translating brand guidelines into a structured persona
- Producing a stakeholder workshop outline to gather design input
- Aligning teams on what an agent should sound like before development

**Scope boundary:** This skill defines WHO the agent is. It does not define dialog flows, subagents, actions, routing, or variables — those are agent design (use `agentforce-generate`). The encoding output for Use Case A produces an `.agent` skeleton with placeholders for those structures; the user fills them in.

## Framework Reference

Read `references/persona-framework.md` for the full framework. It defines:

- **Identity** — 3-5 anchoring adjectives + Negative Identity (≥2 character-level anti-patterns)
- **14 dimensions** (Personification + the 13 expression dimensions):
  - **Personification** — Talking System / Familiar Thing / Personal Assistant
  - **Register** — Subordinate / Peer / Advisor / Coach
  - **Voice** — Formality, Warmth, Personality Intensity, Reading Level
  - **Tone** — Emotional Coloring, Empathy Level (+ Tone Boundaries, Tone Flex)
  - **Delivery** — Brevity, Humor
  - **Chatting Style** — Emoji, Formatting, Punctuation, Capitalization
- **Persona Artifacts** — Identity (traits + negative identity), Expression (tone boundaries + never-say + guardrails), Phrasing (phrase book + discourse markers + lexicon)
- **Tone Flex** — how tone shifts by context (including per-subagent calibration)
- **Lexicon** — global and per-subagent vocabulary, including immutable terms
- **Guardrails** — content-level boundaries (e.g., "Don't offer medical advice"), distinct from Never-Say

Attributes are ordered by dependency. Identity → Personification → Register → Voice → Tone → Delivery → Chatting Style. Constraint notes recommend natural pairings; any combination is valid.

Attribution for the external sources this skill draws on is in `references/attributions.md`.

---

## Pre-DRAFT Triage — Greenfield or Brownfield?

**Before anything else,** ask the user which lane they're on. The two lanes diverge significantly downstream.

> Welcome. Two ways to use this skill:
>
> 1. **Starting fresh** — design a persona from scratch using brand input, audience details, and channel. **Greenfield.**
> 2. **Auditing an existing agent** — review and improve a `.agent` file you already have. **Brownfield.**
>
> Which one?

Set a `mode` flag in state: `greenfield` or `brownfield`.

**Brownfield triggers:**
- User uploads a `.agent` file → load via `scripts/parse_agent_yaml.py` (read-only)
- ADJUST spoke is immediately available (subagents and actions exist)
- SCORE includes per-subagent and per-action sub-scoring
- ENCODE produces annotated proposed-new-file + diff summary, never inventing structure

**Greenfield triggers:**
- ENCODE produces a starter `.agent` skeleton with placeholders for subagents/actions/routing
- ADJUST spoke is initially gated (offered only if user later declares subagents)

---

## Architecture: Phases and Spokes

**Phases** are sequenced — order matters. **Spokes** orbit the hub, available any time after DRAFT, in any order. The hub is presented after every phase or spoke exit.

```text
SEQUENCED PHASES (linear pipeline):
  DRAFT → REFINE → SCORE → ENCODE
                          ↑
              (loop back via phases or spokes if SCORE finds gaps)

SPOKES (radiate from the HUB; any time after DRAFT):
  ⊙ NAME              — pick or confirm the agent's name
  ⊙ FILL OUT          — phrase book, never-say, lexicon, immutable content
  ⊙ ADJUST            — subagent + action persona calibrations (gated)
  ⊙ CHECKLIST         — "What's filled in?" — completeness gap analysis
  ⊙ WORKSHOP          — stakeholder workshop outline
```

The HUB suggests the next default but lets the user pick anything, including re-running the phase or spoke they just exited.

---

## PHASE 1 — DRAFT

DRAFT applies "start small": Identity Traits before dimensions. The user can exit DRAFT after the start-small checkpoint and return later via spokes or re-enter DRAFT.

### Step 1: Input

Accept any starting input. No detection question — accept whatever the user provides.

**Accepted inputs:**
- Brand guide or tone-of-voice document (PDF, text)
- Organization URL
- Prior persona document (persona.md from a previous session)
- Free-text description (e.g., "a sales coach who talks like Crocodile Dundee")
- Existing agent system prompt or `.agent` file (brownfield mode)
- Any combination

**If the user provides nothing:**
> "Share something to get started — a brand guide, a URL, or just describe the agent in your own words."

### Step 2: Context (Essentials)

These four are required:

1. **Channel** — pick exactly **one**:
   - Web chat (text)
   - Mobile chat (text)
   - SMS (text — short-form, char-budgeted, no rich text)
   - Email
   - Telephony (voice over phone — voice selection, AI disclosure, formatting suppression)
   - Multimodal-with-audio (chat UI plus agent speaks)
   - Embedded / in-app
   - Other (free-text)

   Channel constrains Brevity defaults (SMS → Terse, Telephony → Concise, web/mobile chat → Moderate, email → Expansive) and rich-text features. Multi-channel + dynamic personas is a roadmap item — for this version, one channel.

2. **Company / Brand** — extract from input or ask. Who they are, what they do.
3. **Audience** — who the agent serves: employees, customers, partners, mixed.
4. **≥1 Use case** — drives REFINE's sample dialog. If the user can only name one, that's enough.

Conditional context — apply each rule; ask only when its condition fires:
- **Primary language** — if input does not state or imply the working language, ask (it affects formality norms).
- **Business goals + success metrics** — if input names no goal or metric, ask for one (it informs proactivity, register, empathy).
- **Legal/compliance** — if input mentions healthcare, finance, insurance, legal, or other regulated domains, OR contains language that reads like it was written by a legal team: set `regulated_industry = true` and ask about legal/compliance constraints.

**Do NOT collect:** subagents, actions, routing structure, or agent name (NAME is its own spoke).

**Working title detection:** If the user refers to the agent by a working title in input ("the quoting agent," "Flex 2.0"), capture it as `display_name_placeholder` in state. NAME spoke uses this as a default.

**Extraction before asking:** Parse input for context signals before asking. "Design an internal sales coach for Buc-ee's" already answers audience (internal), role (sales coach), and brand. Don't re-ask.

### Step 3: Identity Traits + Negative Identity

This step is the start-small anchor. Generate:
- **Identity Traits** — 3-5 adjectives with behavioral definitions (e.g., "Composed: doesn't escalate emotionally even when the user does")
- **Negative Identity** — 2-4 character-level anti-patterns ("Not a salesperson: doesn't push, recommends what fits")

Identity Traits anchor everything that follows.

### START-SMALL CHECKPOINT (explicit, spoken aloud)

After Identity Traits + Negative Identity are locked, **write the persona document to disk as it stands** and announce the off-ramp:

> "We have enough to ship a minimal persona. Here's what it has so far:
>
> - **Identity:** [traits]
> - **Negative Identity:** [anti-patterns]
> - **Channel:** [channel]
> - **Company / Audience:** [values]
> - **Use case:** [first use case]
>
> Want to keep going through Personification and the rest of the dimensions, or stop here and pick from the hub?"

If the user stops here, dimensions get framework defaults derived from Identity + Channel. The persona document is on disk; the user can see exactly what they've got.

### Step 4: Personification (the 14th dimension)

Personification slots in right after Identity. It determines whether the rest of the dimensions are doing character work or transactional work.

| Position | Description | Pulls |
|---|---|---|
| **Talking System** | Functional, predictable, no character. Fades into the background. ATM, ticketing kiosk, transactional service. | Reading Level low; Humor None; Personality Intensity Reserved; Pronouns "the agent" or brand-name only. |
| **Familiar Thing** | A recognizable category of helper, lightly characterized. "Service Agent," "Coding Assistant." | Personality Intensity Moderate; Pronouns: "I" + name OK. |
| **Personal Assistant** | A characterized, named agent with a recognizable voice. Talks in first person; identity traits show through. | Personality Intensity Reserved or Bold; Pronouns: "I" + name standard. |

Auto-suggest from Identity Traits; the user confirms or overrides.

### Step 5: Remaining Dimensions

Walk the dependency chain: Register → Voice (Formality, Warmth, Personality Intensity, Reading Level) → Tone (Emotional Coloring, Empathy Level + Tone Boundaries, Tone Flex) → Delivery (Brevity, Humor) → Chatting Style (Emoji, Formatting, Punctuation, Capitalization).

**Brevity defaults are bound to channel** — SMS → Terse, Telephony → Concise, web/mobile chat → Moderate, email → Expansive. Override only when a strong signal warrants.

For each dimension:
1. Pre-populate from input signals
2. Mark confidence (`strong` = strong signal from input; no marker = default)
3. Show the full spectrum and the recommended position

Generate at the end of Step 5:
- **Phrase Book** — 2-4 phrases per applicable category (Acknowledgement, Affirmation, Apologies-for-mistakes, Off-Topic Redirect, Welcome, Discourse Markers; conditional: Escalation/Handoff for external, Celebrating Progress for Encouraging coloring, Teaching Moments for Coach register, Humor Examples for Humor ≠ None)
- **Never-Say List** — ≥5 entries (chatbot filler + register violations + cognitive-processing markers + persona-specific)
- **Tone Boundaries** — what the agent must never sound like
- **Tone Flex** — baseline + triggers + shift rules
- **Global Lexicon** — brand name, product names, industry terms used everywhere. Distinguish editable from immutable.
- **Guardrails** — content-level boundaries; include when the domain warrants ("Don't offer medical advice"). Distinct from Never-Say.
- **Values** — include only when the user states them explicitly; never inferred.

**Cross-cutting verbatim guardrail:** Never alter content the designer marks as immutable (legal disclaimers, brand-defined terminology). If a phrase book entry or lexicon term conflicts with immutable content, the immutable content wins.

### DRAFT Exit

Persona document is on disk. State carries:
- Mode (greenfield/brownfield)
- Channel
- Company, Audience, Use cases
- Identity Traits, Negative Identity
- Personification + 13 dimensions (filled or defaulted)
- Confidence annotations
- Phrase Book, Never-Say, Tone Boundaries, Tone Flex, Lexicon
- Guardrails (if any), Values (if explicit), Immutable content blocks
- `display_name_placeholder` (working title from input, if detected)
- `name_decision: pending`

Present the HUB.

---

## PHASE 2 — REFINE

Generate sample dialog and let the user iterate.

### Sample Dialog Generation

Use the **Use cases captured in DRAFT step 2** as scenario seeds. Generate 3-5 exchanges that:
- Demonstrate the persona in action (word choice, tone, brevity, humor, formatting)
- Include at least one "interesting" turn — error, clarification, emotional moment — not just happy path
- Make the persona's impact obvious — none of these agents say "Hello! How can I help you today?"

For voice/telephony channels, start with the welcome message including AI disclosure so the user sees it in context.

### Refinement Loop

After presenting the sample dialog:

> "Tell me what to change — 'make it warmer,' 'drop the humor,' 'don't say that' — or pick:
> - Looks good — back to the hub
> - Try a different scenario
> - (free-text always available)"

When the user types a natural-language adjustment, apply it via the mapping table in **`references/refinement-mappings.md`** (e.g., "warmer" → Warmth +1, also consider Empathy +1), regenerate the sample with the change held single-axis, and re-present. When ambiguous, apply the primary mapping and narrate the change so the user can correct.

**Diff-Based Regeneration** — After a single-dimension change:
1. Show the change explicitly: "Warmth: Warm → Cool"
2. Hold ALL unchanged dimensions constant
3. Regenerate sample dialog varying only the changed dimension
4. Narrate what shifted

**Contrasting Response Comparison** — If the user asks ("show me two ways this agent could respond"), generate one user utterance from a captured use case + two contrasting agent responses varying along **one dimension or trait** (not multiple axes). Update state from the user's choice.

### REFINE Exit

Sample dialog written to `persona/[agent-name]/sample-dialog.md`. Persona document updated if dimensions shifted. Present the HUB.

---

## PHASE 3 — SCORE — "How good is it?"

Apply the 100-point rubric. Two entry points:
1. **Designed persona** (state from DRAFT/REFINE)
2. **Existing agent instructions** (brownfield mode — `.agent` file, system prompt, topic instructions, or combination)

**Key principle:** Score the substance, not whether they used the framework's vocabulary. "Personality guidelines" = Identity. "Communication rules" = dimensions. "Banned phrases" = Never-Say. Map first, then score.

### Brownfield Extraction

For brownfield mode, parse the `.agent` file via `scripts/parse_agent_yaml.py` (read-only). Walk:
- `system.instructions`, `system.messages.welcome`, `system.messages.error`
- Each subagent: name, instructions, reasoning_instructions, system_override
- Each action: name, progress_indicator_message

Map by substance, not label. Mark inferred mappings: "inferred — [source label]." Absence of a framework concept ≠ zero score; score what's present. The common-label-mapping table is in `references/scoring-rubric.md`.

### 100-Point Rubric

Apply the 100-point rubric in **`references/scoring-rubric.md`** — 11 scoring categories, the brownfield per-subagent / per-action sub-scoring rules, and the percentage bands (90-100 production-ready, 75-89 strong foundation, 50-74 needs revision, <50 significant gaps). Score the substance, not the vocabulary.

### Recommendations (required output)

For each gap surfaced:
- Cite the framework section the gap relates to
- Provide a specific, actionable fix
- For brownfield: cite the location in the source file (subagent name, line range)

### SCORE Exit

Evaluation written to `persona/[agent-name]/evaluation.md`. Total presented as percentage (90-100 production-ready, 75-89 strong foundation, 50-74 needs revision, <50 significant gaps). Present the HUB; suggested next is FILL OUT or ADJUST if gaps exist, ENCODE if scores are passing.

---

## PHASE 4 — ENCODE

Generate valid encoding output for Agent Script (default) or Agentforce Builder.

### Pre-flight Check: NAME

If `name_decision` is still `pending`, **pause ENCODE and route the user to the NAME spoke first.** Reason: Agent Script's `config.agent_label` is required; encoding with a placeholder silently inherits the working title (e.g., "the quoting agent"), which the user may not notice before deploy.

After NAME completes, ENCODE resumes.

### Decision Tree

```text
1. Confirm channel (single value from state).
2. Confirm authoring tool:
   - Greenfield: default = Agent Script.
     → "Encode for Agent Script (default), or switch to Agentforce Builder?"
   - Brownfield, source is Agent Script: default = Agent Script.
     → "Stay on Agent Script (recommended)?"
   - Brownfield, source is Builder: default = Builder, but offer the upgrade path.
     → "Stay on Builder, or switch to Agent Script (recommended for per-subagent encoding granularity)?"
3. Generate comprehensive persona block (always):
   - system.instructions — full persona content
   - system.messages.welcome — in-character welcome
   - system.messages.error — in-character error
4. Subagent-level encoding? Three answers:
   - "I have subagents defined" → enumerate them, generate per-subagent reasoning.instructions
   - "I don't have subagents yet" → skip; output is global-only (Use Case A)
   - "Generate examples" → infer 2-3 plausible subagents, label as examples
5. Action-level encoding? Same three answers; generates progress_indicator_message per action.
6. Voice encoding? Only if channel is telephony or multimodal-with-audio.
   - Voice recommendations from references/voice-catalog.json
   - Per-voice fine-tuning starting points (Speed, Stability, Similarity)
   - AI disclosure in welcome message
   - Pronunciation dictionary for brand terms
7. Diff (brownfield only): annotated proposed-new-file + diff summary.
```

The skill **never invents** subagents, actions, variables, or routing. Architecture stays the user's call.

### Output by authoring tool

Read `references/persona-encoding-guide.md` for the full field-by-field guide (block order, formatting rules, Builder field char limits, `progress_indicator_message` placement, channel adjustments). Operational essentials:

- **Agent Script (`.agent`)** — valid Agent Script syntax per `forcedotcom/sf-skills/skills/developing-agentforce/`. Greenfield: emit a minimal valid skeleton (`system` with full persona + in-character welcome/error, `config`, `language`, `start_agent` stub, one placeholder `subagent`) — a working starting point the user fleshes out; never invent subagents/actions/variables/routing. Brownfield: preserve the existing structure and modify only persona-bearing fields (`system.instructions`, `system.messages.welcome`/`error`, per-subagent `system:`/`reasoning.instructions:`, per-action `progress_indicator_message:`). Write to `persona/[agent-name]/[agent-name].agent`.
- **Agentforce Builder** — populate the config fields (Name, Role = functional summary only, Company, Welcome, Error), the global persona block, per-subagent instructions, and per-action loading text; recommend the Tone dropdown from Register + Formality; apply voice/SMS channel adjustments. Write to `persona/[agent-name]/builder-fields.md`.

### Brownfield Diff Output

When source was a `.agent` file, generate two artifacts:
1. **`persona/[agent-name]/persona-diff.md`** — annotated proposed-new-file. Each persona-bearing field shown with the proposed new content + an inline rationale ("changed because: tone-flex called for empathy bump in escalation").
2. **Diff summary** — companion section listing what changed and why, scoped to persona only. The user can run a real diff tool against the source if they want a unified view; this artifact is for human review.

The diff explicitly excludes routing, subagent structure, action contracts.

### ENCODE Exit

Encoding artifact written. Present the HUB.

---

## SPOKES

Spokes are accessory work, available any time after DRAFT, in any order, repeatable.

### ⊙ NAME

> "Does this agent get a name? Some agents work better unnamed (transactional services, talking systems, agents whose identity is the brand itself). Others benefit from a distinct name. What's right for this one?"

If a working title was detected in DRAFT (`display_name_placeholder` set):
> "I picked up '[working title]' from your input. Confirm it, or pick from suggestions?"

If yes (named):
- **Talking System** → if user still wants a name, suggest brand-aligned (e.g., "Acme Service Agent")
- **Familiar Thing** → 2-3 short candidates (functional, easy to say)
- **Personal Assistant** → up to 3 candidates that distill the identity

Apply naming principles from the framework:
- Descriptive ("Service Agent") • Evocative ("Striker") • Sticky ("Clover") • Culturally aligned ("Bug Squasher") • Brand-aligned ("Lex") • Easy to say (passes the radio test) • Obviously artificial ("Song," "Cortana") • Functional ("Scripty") • Abstract ("Koda," "Lumi") • Null (deliberate non-name)
- **Anti-pattern:** API-style names like `Tech_Assist_Agent_v2_Internal_Test` are NOT persona names.

If no (unnamed): set `name_decision: unnamed` or `brand-as-name`. Display name in encoding becomes either the brand name or null per user choice.

State update: `name_decision` ∈ {named, unnamed, brand-as-name}. Display name populated.

### ⊙ FILL OUT

> "You're in FILL OUT. What would you like to work on?
> - Phrase book additions
> - Never-say expansions
> - Lexicon additions (global or per-subagent)
> - Immutable content marking
> - I'm done with this spoke
> (Pick one; you'll come back here after each, or pick multiple by listing.)"

For each sub-activity, present current state and gather additions/edits. Update the persona document on exit.

### ⊙ ADJUST

**Gated:** only offered when subagents or actions exist (declared by user, or detected from a source `.agent` file in brownfield mode).

> "You're in ADJUST. What would you like to work on?
> - Per-subagent persona adjustment (e.g., 'in escalation subagent, drop humor to zero')
> - Per-action loading text (in voice)
> - I'm done with this spoke"

Per-subagent adjustments encode as Agent Script `system:` overrides or `reasoning.instructions` calibrations.
Per-action loading text encodes as `progress_indicator_message` strings.

### ⊙ CHECKLIST — "What's filled in?"

Reads the persona document; produces a markdown checklist marking each element as `[+]` present, `[-]` missing, or — not applicable. Definitions pulled directly from the framework.

Output template at `assets/checklist-template.md`. Each suggested next step is **quotable** (e.g., "go to NAME", "go to FILL OUT, add Lexicon") so the user can paste back rather than retype.

Useful before SCORE for a quick gap scan, and before ENCODE for a readiness check.

Write to `persona/[agent-name]/checklist.md`.

### ⊙ WORKSHOP

Generate a stakeholder-facing outline for a customer's internal workshop. Output supports FigJam / whiteboard formats.

**Question generation policy** (read `references/workshop-question-policy.md` for the full rules):
- High-leverage first (Identity, Personification, Register).
- Skip what's already known. If the brand input clearly answers a dimension, don't ask.
- Three styles: **validate** ("we assumed X — confirm or push back"), **choose between** (two genuinely different positions), **open spectrum** (place the agent on this line).

Use scenario seeds from `references/workshop-scenario-seeds.md` for would-you-rather pairs.

Output template at `assets/workshop-outline-template.md`. Output to `persona/[agent-name]/workshop-outline.md`.

**Quality over coverage.** Better to ask 4 great questions than 12 generic ones.

---

## HUB

After every phase or spoke exit, present the HUB. **Not a flat menu** — the suggested next step is rendered as a labeled primary recommendation with rationale, above the rest.

```text
HUB

  Suggested next:
  → [SUGGESTED] — [one-line rationale grounded in current state]

  Or do something else:
    Phases:
      → REFINE              [state-aware annotation, e.g., "re-run; iterate on dialog"]
      → SCORE               ["how good is it?"]
      → ENCODE              [gating note if name_decision pending]
    Spokes:
      ⊙ NAME                [annotation: "name_decision pending" or "current: [name]"]
      ⊙ FILL OUT            [annotation: what's empty, e.g., "Lexicon empty"]
      ⊙ ADJUST              [annotation: gated reason if not available]
      ⊙ CHECKLIST           ["what's filled in?"]
      ⊙ WORKSHOP            ["stakeholder workshop outline"]
  Exit:
    → I'm done
```

**Suggestion logic:**
- Just exited DRAFT → suggest REFINE
- Just exited REFINE → suggest SCORE
- Just exited SCORE with passing score → suggest ENCODE
- Just exited SCORE with failing score → suggest FILL OUT or ADJUST (whichever has the largest surfaced gaps)
- `name_decision: pending` and ENCODE was attempted → suggest NAME, then resume ENCODE
- After every phase/spoke → user can always pick anything, including the one just exited

---

## Output Files

The skill produces:

1. **Persona document** (`persona/[agent-name]/persona.md`) — DRAFT. Updated by other phases/spokes.
2. **Sample dialog** (`persona/[agent-name]/sample-dialog.md`) — REFINE.
3. **Evaluation report** (`persona/[agent-name]/evaluation.md`) — SCORE.
4. **Encoding artifact** (`persona/[agent-name]/[agent-name].agent` for Agent Script, OR `persona/[agent-name]/builder-fields.md` for Builder) — ENCODE.
5. **Persona diff** (`persona/[agent-name]/persona-diff.md`) — ENCODE in brownfield mode only.
6. **Checklist** (`persona/[agent-name]/checklist.md`) — CHECKLIST spoke.
7. **Workshop outline** (`persona/[agent-name]/workshop-outline.md`) — WORKSHOP spoke.

`persona/` is gitignored at the skill repo level so dogfooding the skill with `cwd` inside this checkout doesn't leak outputs into git. In any other working directory, the user is responsible for whatever gitignore rules they want to apply.

---

## Interaction Design Notes

Cross-surface UX guidelines (output-before-questions, batching independent questions, compact
formats, progress awareness, confidence callouts) are in **`references/interaction-design-notes.md`**. Apply them across all surfaces — CLI, TUI, web, IDE.

---

## Credits

This skill draws on published, openly-licensed conversation-design work; see `references/attributions.md`.
