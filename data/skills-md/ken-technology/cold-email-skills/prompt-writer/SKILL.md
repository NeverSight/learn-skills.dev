---
name: prompt-writer
description: Generate AI personalization prompts for cold email campaigns. Reads the AI variables from a campaign strategy and outputs detailed prompts you can run in any personalization tool or LLM to tailor each email per prospect. Use after campaign strategy, or when creating prompts for an existing sequence. Triggers on "write prompts for this campaign", "generate personalization prompts".
model: sonnet
thinking: true
---

# Prompt Writer Skill

Generate detailed AI personalization prompts based on campaign strategy AI variables. These prompts instruct your personalization tool or the LLM to create personalized content for each prospect.

## Output Contract

`prompts.md` is the handoff artifact for personalization. Hard rules this skill must honor:

- `## User Prompts (To output: true)` H2 heading - exact phrasing.
- One H3 per variable using Title Case (`### First Line`, not `### first_line`). H3 name is ≤30 chars.
- Every H3 must contain a `**Prompt**:` marker followed by the prompt text.
- Prompt text ≤4096 chars. Runs until next `### `, `## `, or `---`. Do NOT use `---` inside a prompt body - it cuts the prompt short.
- Variable names must match exactly what `emails_v2.md` uses in `{{Title Case}}` braces (e.g. `{{First Line}}`, `{{PS Line}}`, `{{Subject Line}}`).
- Optional `## Rewriting Instructions` H2 at the bottom - a short steering paragraph for a rewriter pass, if you use one.

## Plan Folder Resolution

This skill receives a `{segment_folder}` path (e.g., `{workspace}/03-15 - plan 1/1 - early-stage/`). Resolve `{plan_folder}` as the **parent directory** of `{segment_folder}` when you need plan-level files such as `plan.md`.

## Execution Tasks

**Execute these tasks in order. Do NOT skip any task unless noted.**

### Task 1: Load Context
- [ ] Read `{segment_folder}/strategy.md` - Extract AI variables section
- [ ] Read `{segment_folder}/emails_v2.md` - Reviewed email copy (fall back to `emails.md` if not found)
- [ ] Read `{workspace}/research.md` - ICP, value prop, messaging themes, product info, case studies (`{workspace}` = the client campaign workspace, default `./cold-email/{slug}/` under the current directory)
- [ ] Read `{workspace}/notes.md` (if exists) - Client-specific preferences

### Task 2: Build User Prompts
> **Note**: You write **user prompts** that generate personalized variables (`to_output: true`). Company context, base rules, and the email sequence are supporting context for the LLM - pull them from research and the sequence file rather than inventing a separate backend. The default rewriting rules (core principles, style, spam/deliverability, flow) are tool-side if your stack rewrites outputs - you SHOULD still write a short optional steering paragraph for rewriting (see Task 2b). The `to_rewrite` field on each user prompt controls whether that variable's output should go through a rewriter.

- [ ] Read `references/prompt-engineering.md` for guidance
- [ ] For each AI variable in strategy.md, expand into detailed prompt
- [ ] Use Standard Variable Templates as base (subject line, first line, PS line)
- [ ] Apply Prompt Customization Rules (no examples for standard variables)
- [ ] Ensure data sources are valid (LinkedIn and website only)

### Task 2b: Write Rewriting Instructions (Optional but Recommended)

If the campaign will run a rewrite pass on personalization outputs, write a short steering paragraph (2-10 sentences) that tunes the rewriter for this specific client/segment. See the "Rewriting Instructions" section below for what to include and what to avoid.

- [ ] Pull voice/tone cues from `{workspace}/research.md`, `emails_v2.md`, and `{workspace}/notes.md`
- [ ] Draft a 2-10 sentence steering paragraph focused on voice, sentence structure, sequence flow, or campaign-specific anti-patterns
- [ ] Do NOT duplicate generic default rules (em-dashes, spam words, AI-tells, formatting)
- [ ] Omit the section if the campaign has no distinctive voice/flow requirements

### Task 3: Internal Text Review (REQUIRED)

Run an internal text review of the drafted prompts before saving. This is a quality pass over the draft - not a live run against contacts.

Dispatch a subagent to review the drafted prompts (or run an internal review pass over the drafts). The reviewer should score and revise against these priorities:

1. HIGHEST PRIORITY - Client notes from `{workspace}/notes.md` (if exists)
2. Campaign strategy from `{segment_folder}/strategy.md`
3. CRITICAL: Prompt Customization Rules Checklist from review-workflow.md (MANDATORY)
4. Data source constraints from SKILL.md

Check:
- MANDATORY: Prompt Customization Rules Checklist (examples policy, PS line format, subject line guidelines)
- All AI variables from strategy.md have prompts
- NO invalid data sources (news, funding, events, social media, blogs)
- Prompts specify: what to generate, data sources, tone, constraints, fallbacks
- Variable names match strategy.md exactly (Title Case; same names as `{{Title Case}}` in the emails)

REJECT any prompt that:
- References news articles, press releases, funding, events, social media (except LinkedIn), or blog content
- Adds examples to First Line, PS Line, or Subject Line prompts (unless heavily customized)
- Uses wrong PS format (must be "PS: " not "PS -" or "PS." or just "PS")
- Adds "Quick question" or typical outreach messaging to subject line
- Completely rewrites PS or Subject Line templates (only slight modifications allowed)

Output a review with:
- Overall score (1-5)
- Prompt Customization Rules violations (if any)
- Data source violations (CRITICAL)
- Missing variables
- Required fixes

Then incorporate the reviewer feedback:
- [ ] Fix all data source violations
- [ ] Add missing variables
- [ ] Apply client-specific preferences
- [ ] Verify all constraints are met

If the user passed `--skip-review`, skip this task and continue to Task 4.

### Task 4: Output Final Prompts
- [ ] Write `prompts.md` to the segment folder
- [ ] Confirm to user prompts are saved and ready to run in their personalization tool or LLM

---

## Required Context

Before generating prompts, load:

1. **Read `{segment_folder}/strategy.md`** - Get AI variables section with prompt_name, prompt_location, prompt_description
2. **Read `{workspace}/research.md`** - Understand ICP, value prop, messaging themes, detailed product info, case studies

## Input: Campaign Strategy AI Variables

The strategy.md contains an AI variables section like:

```json
[
  {
    "prompt_name": "personalized_subject_line",
    "prompt_location": "subject_line",
    "prompt_description": "Short description of what this variable should do"
  },
  ...
]
```

Your job is to expand each `prompt_description` into a full, detailed prompt.

## Output Format

### What You Write

You only need to write **user prompts** (`to_output: true`) that generate personalized variables. Supporting context for the LLM (who the sender is, company overview, style rules, the full email sequence) should come from research.md and emails_v2.md when the user runs these prompts - do not re-author that stack inside every variable prompt.

### Prompt Naming Convention
Prompt names must be short, plain text with Title Case. No underscores, colons, or special characters.
- Good: "First Line", "Subject Line", "PS Line"
- Bad: "personalized_first_line", "campaign_name:company_context", "subject_line"

**One prompt = one value per LEAD, not per email (HARD).** Personalization tooling generates a single value per prompt per lead; every email that references the same token renders the identical text. If the copy reuses `{{First Line}}` in Emails 1-3, the same opening sentence sends three times (preview/approval views typically show it filled on Email 1 and blank on later emails - blank means reused, not missing). Each email that needs its own opener gets its own distinct-named prompt: "First Line", "Bump First Line", "Nudge First Line". Reuse is correct only when the identical value is wanted on every step (`{{Subject Line}}` in every subject). If emails.md reuses a body token across emails, flag it back to email-copywriting instead of writing one shared prompt.

These names must match the `{{Title Case}}` placeholders in the email copy exactly.

Generate `prompts.md` with this structure:

```markdown
# AI Personalization Prompts

Campaign: [campaign folder name]
Generated: [date]

## Variables Overview

| Variable | Location | Email(s) | Rewrite |
|----------|----------|----------|---------|
| [name] | [location] | [1/2/3/all] | [yes/no] |

## User Prompts (To output: true)

These prompts generate the actual AI variables that appear in the copy:

### [Prompt Name]
**Location**: [prompt_location]
**Email(s)**: [email_number or "all"]
**Rewrite**: [yes/no]

**Prompt**:
[Full detailed prompt text]

---

[Repeat for each variable]

## Rewriting Instructions

[2-10 sentence steering paragraph that tunes voice, tone, or sequence flow for this campaign. Omit this H2 section entirely if the campaign has no distinctive voice/flow requirements. Do NOT duplicate generic default rules - focus only on what makes THIS client/campaign distinctive.]
```

## Data Source Constraints

**CRITICAL**: Prompts may only reference data that a typical personalization run has for each prospect.

### Available by default

- **Company website main page** - products, services, target market, value prop
- **LinkedIn company page** - industry, headcount, headquarters, description
- **LinkedIn individual profile** - title, company, location, previous roles, education, skills, summary

If the user documents extra enrichments for this campaign (for example Crunchbase funding), you may reference those only when they are explicitly available. Do not assume they exist.

### Never Available (unless the user explicitly provides them)

These data sources must never be referenced in prompts by default:
- News articles or press releases
- Recent events or triggers
- Social media posts (except LinkedIn)
- Blog content or articles
- Tech stack data
- Any time-sensitive information

### Variables Are Auto-Injected by the Personalization Tool

- Lead fields like `{firstName}`, `{company}` are usually already in the tool context
- **DO NOT include variable syntax in your prompts** (no `{variable_name}` references)
- Just describe what data to use: "Based on their job title..." not "Based on {job_title}..."

When writing prompts, describe what to generate and where to look:
- Correct: "Based on their job title from LinkedIn..."
- Wrong: "Based on {job_title} from LinkedIn..."

## Prompt Writing Guidelines

Each prompt must specify:

### 1. What to Generate
Clear instruction on the output:
- "Write a subject line that..."
- "Generate a 1-sentence opening that..."
- "Create a pain point reference that..."

### 2. Tone and Style
How it should sound:
- "Conversational and curious"
- "Professional but friendly"
- "Insightful, not generic"

### 3. Constraints
Length and format rules:
- "Under 50 characters"
- "1-2 sentences max"
- "No questions or emojis"
- "Start with 'PS'"

### 4. Fallback Strategy
What to do if data is missing:
- "If not available, use their role instead"
- "Skip if no relevant data found"

## Standard Variable Templates

### Subject Line
```
Write a very short subject line that grabs attention and sparks curiosity in fewer than 6 words, ideally 3-4.
Make it relevant to a challenge, wish, hobby, or activity. Do not add emojis or punctuation. Use lowercase except for the first letter, and capitalize the first letter of company and person names.
Focus on a single, specific small detail from your research; it can be personal. The goal is to intrigue the prospect quickly and make them curious about the email's contents in just 3-4 words.
```

### First Line
```
Write the first line of the email. Refer to the template above to see where it fits in the initial message. Don't write any greeting.
The goal is to hook their attention, make the line very personalized, and lead smoothly into the rest of the email. Keep this line short, under 20 words.
It should spark curiosity, be intriguing and simple, and avoid gimmicks. Do not sound robotic. Most important: do not be boring.
Avoid emojis, exclamation marks, and questions. Don't just summarize information about them.
Aim for a pleasant, genuine tone that reflects the company: smart, concise, personalized, and straightforward, using simple language.
```

### PS Line
```
Write a PS line for this email that starts with "PS" and continues. Keep it short: one or two sentences. The goal is to be human and to reflect your personality as a creator. This line should be casual and personal - an opportunity to add more humanity to your outreach.
Make the PS about them, not about you. Include a very small personal detail that few people notice - something hidden on their website or LinkedIn profile. Don't try too hard or make broad assumptions; if you do assume something, mention that you're assuming. Humor is good but subtle - if you see something funny in their profile, you can laugh at it or lightly develop the joke.
This is also a chance to share a small, catchy idea for them. Keep it genuine and brief. Do not invent connections, invite them to anything, or offer help you can't back up. Avoid generic compliments; instead, make them feel noticed and special.
```

### Role Pain Point
```
Based on their job title from LinkedIn, reference a pain point typical for that role. Be specific to seniority: VPs/Directors - scaling, team efficiency, cross-functional alignment. C-suite - strategy, competitive positioning, board concerns. Managers - execution, reporting, resource constraints. 1 sentence max that feels like something only someone in their role would understand.
```

### Industry Context
```
Based on company industry from LinkedIn, reference a common challenge or priority in that industry. Keep evergreen - not news or events, just general industry dynamics. Example for healthcare: 'In healthcare, compliance and patient data security are always top of mind.' 1 sentence, conversational.
```

### Company Size Context
```
Based on LinkedIn company headcount, reference challenges typical to that size. 10-50: wearing multiple hats, limited resources. 50-200: scaling pains, process gaps. 200-1000: coordination complexity, tool sprawl. 1000+: enterprise complexity, change management. 1 sentence showing you understand their scale.
```

## Prompt Customization Rules

**CRITICAL RULES** for customizing the standard templates above:

### Examples Policy
- **DO NOT add examples** for: First Line, PS Line, Subject Line, unless they're heavily customized
- These types of variables should feel natural and unrestricted - examples constrain creativity
- **CAN add examples** for: Other custom prompts that need specific structure/format (e.g., industry-specific variables, complex body text)

### PS Line Guidelines
- **Use the DEFAULT PS line template** and only modify SLIGHTLY for campaign context
- Never create completely custom PS line prompts from scratch
- **Format**: Always use "PS: " (with colon and space, NOT "PS -" or "PS." or just "PS")
- Modifications should be minor adjustments, not rewrites

### Subject Line Guidelines
- **Keep subject lines close to default formula**, only customize for campaign-specific angle
- Never add "Quick question" or typical outreach messaging to subject line prompts
- Subject line prompt changes should be SLIGHT to match email sequence or client tone
- Avoid sales clichés in subject line instructions

### What You CAN Customize
- Data source references (which LinkedIn fields to prioritize)
- Tone adjustments (more casual, more professional)
- Industry-specific context or pain points
- Length constraints (shorter or longer)

### What You Should NOT Customize
- The core structure of First Line, PS Line, or Subject Line templates
- Adding example outputs that constrain the AI
- Changing the fundamental approach of these standard variables

## Rewriting Instructions

When the stack rewrites personalization outputs, it usually already has core principles, style rules, spam/deliverability rules, formatting rules, company context, audience description, and the email sequence. You do NOT need to recreate any of that.

Your job is to write a short, optional **steering paragraph** (2-10 sentences) that tunes the rewriter for this specific client/segment. Treat it as higher-priority delta instructions on top of generic defaults.

### The `to_rewrite` field
`to_rewrite` on each user prompt controls whether its output should be rewritten:
- `to_rewrite=0` - NOT rewritten (use for subject lines, short outputs)
- `to_rewrite=1` - WILL be rewritten (use for First Line, PS Line, body content)

### What to Write About

Pick 1-3 of these angles based on what's distinctive about this client/segment:
- **Voice & tone** - How should sentences sound? (punchy, technical, warm, dry, founder-to-founder, etc.)
- **Sentence structure & rhythm** - Short/long, fragments OK, pacing, whether to mirror the client's own writing style
- **Sequence flow** - How personalized lines should hand off into this segment's specific body copy
- **Campaign-specific anti-patterns** - Phrases or constructions to avoid for this client (e.g. "don't sound like a recruiter" for an HR-tech client)
- **Research signaling** - How much the rewrite should show that research was done

### What NOT to Write

- Generic rules already in default rewriter guidance (no em-dashes, no spam words, no AI-tells like "I noticed", no exclamation marks, etc.)
- Formatting instructions the tool already enforces
- Long explanations or justifications - keep it terse and directive
- Output examples - they over-constrain the rewriter

### Length

Aim for 2-10 sentences. Usually 3-6 is the sweet spot. The example below is 6 sentences.

### Writing Style

Write it conversationally. The rewriter picks up the tone of the instruction itself, so if you want punchy output, write the instruction in punchy sentences. Avoid bullet lists or numbered rules - prose works better here.

### Example

```
Make it sound as cool as possible. Show you've researched them. Use shorter sentences like I'm doing now. Better to have 2 shorter punchy sentences instead of 1 long boring one. Use power words. Sound human.
```

Notice: 6 sentences, conversational, hits voice + sentence structure + research signaling, no rules duplicated from defaults.

### Source Material

Pull voice/tone cues from:
- `{workspace}/research.md` - Tone preferences, voice guidelines, how the client talks about themselves
- `{segment_folder}/emails_v2.md` (or `emails.md`) - Style modeled in the sequence itself
- `{workspace}/notes.md` - Explicit style preferences from the client

### When to Omit

If the campaign has no distinctive voice/flow requirements, omit the `## Rewriting Instructions` H2 section entirely. Strong defaults are enough. But in practice, nearly every campaign benefits from 2-3 sentences of steering - default to including it.

### How It Gets Used

The `## Rewriting Instructions` H2 in `prompts.md` is the user-facing steering paragraph to paste into (or load as) the rewrite pass. At runtime the stack typically composes:
1. Default rewriting prompt (core principles, email flow, style, uniqueness)
2. Spam and deliverability rules
3. Company context + audience description
4. Formatting instructions
5. Email sequence context
6. **Your steering paragraph** (higher priority than the default)

## Workflow

**See Execution Tasks section at the top of this file.** Follow Tasks 1-4 in order.

Summary:
1. Load context (strategy, client docs, notes)
2. Build user prompts (expand AI variables) + write optional Rewriting Instructions steering paragraph
3. **Internal text review** of the drafted prompts (unless `--skip-review`)
4. Output final prompts

## Internal Review Process

**See Task 3 in Execution Tasks section above.** The internal text review scores and revises the draft before `prompts.md` is written. It does not require a live campaign or platform connection.

Review workflow details are in `review-workflow.md`. Key points:
- Reviewer checks: variable coverage, data source validity, prompt quality
- Reviewer does NOT check generic system/context prompts the tool may inject separately
- Priority order: Client notes > Campaign strategy > Validation rules
- CRITICAL: Reject prompts referencing invalid data sources (news, funding, events, etc.)
- Reviewer does NOT check email copy (that's handled by email-copywriting / email-review)

## User Control Options

| Flag | Effect |
|------|--------|
| `--skip-review` | Skip the internal text review and write `prompts.md` from the draft |
| `--verbose` | Show more detail during review |
| `--compact` | Minimal confirmation output |

## Resources

For detailed prompt guidance, see:

- **references/prompt-engineering.md** - Complete guide to AI personalization and prompt writing with JSON examples
- **review-workflow.md** - Automated internal review process specification

## Quality Checklist

Before outputting, verify:
- [ ] Every AI variable from strategy.md has a corresponding prompt
- [ ] All prompts specify valid data sources only
- [ ] Prompts include clear output format and length constraints
- [ ] Prompts specify fallback behavior
- [ ] Variable names match exactly between strategy, `{{Title Case}}` in emails, and prompts.md H3s
- [ ] Email numbers are specified correctly
- [ ] Each prompt has correct `to_rewrite` setting (0 for subject lines, 1 for first/PS/body)
- [ ] `## Rewriting Instructions` section included (2-10 sentences) OR deliberately omitted for a generic-voice campaign
- [ ] Rewriting instructions don't duplicate generic defaults (em-dashes, spam words, AI-tells, formatting)

## Output Handling

After generating prompts:

1. **Write to segment folder**: Save `prompts.md` to `{segment_folder}/prompts.md`
2. **Confirm**: Tell the user prompts are saved and ready to run in their personalization tool or LLM for each prospect
3. **Mode check**: If in approval mode, wait for user approval before proceeding to the next workflow step

## Edit Mode (Improvement Context)

When invoked with improvement context (`mode: "edit"`), this skill edits existing prompts.md rather than generating new prompts.

### Detecting Edit Mode

Check for improvement context in the conversation:
- `mode: "edit"` indicates edit mode
- `trigger: "analytics"` or `trigger: "feedback"` indicates source
- `improvement_instruction` contains specific changes to make

### Edit Mode Workflow

1. **Read improvement context**: Extract `improvement_instruction` object
2. **Load existing prompts.md**: Read current prompts from campaign folder
3. **Identify scope**: Which prompts to modify (see scope table below)
4. **Apply targeted changes**: Only modify specified prompts
5. **Generate diff**: Show before/after comparison
6. **Get approval**: Wait for user to confirm changes
7. **Save**: Update prompts.md with approved changes
8. **Log**: Update improvement-log.md in plan folder

### Handling Edit Scopes

| Scope | Action | What Changes |
|-------|--------|--------------|
| "subject_line prompt" | Modify subject line user prompt only | Single prompt |
| "first_line prompt" | Modify first line user prompt only | Single prompt |
| "ps_line prompt" | Modify PS line user prompt only | Single prompt |
| "system prompts" | N/A - system/context prompts are tool-side, not written here | No action needed |
| "all user prompts" | Rewrite all output-generating prompts | All user prompts |
| "add variable" | Add new AI variable prompt | New prompt added |
| "remove variable" | Remove existing prompt | Prompt removed |

### Edit Mode Output Format

```markdown
## Proposed Changes to prompts.md

### Subject Line Prompt

**Before:**
Write a very short subject line that grabs attention in fewer than 6 words...

**After:**
Write a curiosity-driven subject line under 5 words. Reference their company name or industry. Do not use AI personalization placeholders. Example: "Quick q about [company_name]"...

**Rationale:** Current AI-generated subject lines may be causing fatigue based on Email 3 performance

---

Approve these changes? [Yes/No/Modify]
```

### Preserving Context During Edits

When editing:
- **Keep unaffected prompts intact**: Only modify prompts in scope
- **Maintain prompt structure**: Keep Location, Email(s), format
- **Preserve variable names**: Names must match strategy.md and `{{Title Case}}` in the emails
- **Keep data source constraints**: Never add invalid sources

### Analytics-Informed Editing

When `analytics_context` is provided:
- Check which emails use the underperforming prompts
- Reference `sequence_stats` to identify problem areas
- Consider if personalization is helping or hurting

### Feedback-Informed Editing

When `feedback_context` is provided:
- "AI feels off" = Adjust prompt constraints and fallbacks
- "Too generic" = Add more specific data source references
- "Forced connections" = Strengthen "don't assume" rules

### Edit Mode Checklist

Before saving edits, verify:
- [ ] Only specified prompts were modified
- [ ] Variable names match strategy.md exactly
- [ ] Data source constraints respected
- [ ] Prompt structure preserved
- [ ] Diff shown and approved by user
