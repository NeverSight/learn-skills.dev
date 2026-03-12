---
name: brainstorm
description: >-
  ALWAYS use this skill before answering brainstorming, ideation, prompt crafting, or open-ended exploration requests.
  Transforms vague requests into actionable outputs via adaptive guided questioning — triages into Prompt Mode (craft/improve prompts), Explore Mode (brainstorm ideas), or Focused Mode (specific problem strategies).
  Trigger when user says: "brainstorm", "ช่วยคิด", "help me think", "I have an idea", "improve this prompt", "let's explore", "I want to build", "I'm thinking about", "brainstorm วิธี", "ช่วยคิดหน่อย", "อยากทำ", "ยังไม่รู้จะทำอะไร", "not sure about the approach", "help me figure out", "what should I".
  Also trigger for: side projects, career decisions, project planning, migration strategies, architecture decisions, cost optimization, or any request where the user hasn't decided direction yet and would benefit from structured discovery.
  Do NOT skip — this skill adapts depth automatically (2-7 questions) and produces BETTER results by asking targeted questions first.
compatibility:
  environment: claude-code (primary), copilot-cli (fallback)
  tools:
    - AskUserQuestion (fallback: ask_user, plain text)
    - WebSearch
    - Agent (fallback: task, inline)
metadata:
  version: "2.1"
---

# Brainstorm

Transform vague ideas into precise, actionable outputs through adaptive structured questioning. The skill adjusts its depth and output format based on what the user actually needs — from quick idea generation to thorough prompt engineering.

## Quick Start

1. User provides a request (vague idea, brainstorm request, or prompt to improve)
2. **Triage** — Classify into one of three modes: Prompt, Explore, or Focused
3. Run the appropriate discovery flow (3–7 questions depending on mode)
4. Produce the right output type for the mode
5. Offer next steps

## Tools

| Tool | Purpose |
|------|---------|
| `AskUserQuestion` | Ask the user ONE question at a time (Claude Code). Use `options` array for multiple choice. Fallback: `ask_user` with `choices` (Copilot), then plain text. |
| `WebSearch` | Find references when the user has none and references would genuinely help. |
| `Agent` | Delegate to Plan subagent (Claude Code): `subagent_type: "Plan"`. Fallback: `task` with `agent_type: "general-purpose"` + `# Role: Planner` block (Copilot). Fallback: create plan inline. |

## Core Principles

1. **Don't answer before you understand.** The urge to help immediately produces generic output. But "understand" doesn't mean "ask 13 questions" — it means knowing enough to be specific.
2. **One question at a time via tool.** Multiple questions get shallow answers. Use `AskUserQuestion` (Claude Code), `ask_user` (Copilot), or plain text as last resort — but always ask one at a time.
3. **Prefer multiple choice.** Provide an `options` array when the answer space is predictable. Choices are faster to answer, reduce cognitive load, and reveal preferences. Use open-ended only when the answer truly can't be predicted.
4. **Mirror the user's language.** Don't introduce jargon they didn't use.
5. **Ask about life, not the domain.** Constraints, risks, and deal-breakers require zero domain knowledge but eliminate wrong paths decisively.
6. **Never re-ask what's already known.** Track information from the initial prompt and all answers.
7. **Respect the user's time.** Match question depth to request complexity. A casual "help me brainstorm" doesn't need the same rigor as "craft a detailed prompt."

## Triage — Choosing the Right Mode

Before asking any questions, read the user's request and classify it into one of three modes. This happens internally — don't ask the user which mode they want.

### Prompt Mode
**When:** User explicitly wants to create or improve a prompt, or needs a comprehensive brief for another AI/tool/person.
**Signals:** "improve this prompt", "help me write a prompt", "ช่วยคิด prompt", "I want to ask Claude to...", mentions using the output with another AI.
**Flow:** Full discovery (5–7 questions across Goal → Direction → Context → Criteria)
**Output:** Improved Prompt + Discovery Summary

### Explore Mode
**When:** User wants to brainstorm ideas, explore possibilities, or think through something open-ended.
**Signals:** "brainstorm", "help me think", "ช่วยคิดหน่อย", "I want to build something but...", "what should I...", "any ideas for..."
**Flow:** Light discovery (3–5 questions) — understand goals + constraints quickly, then generate ideas
**Output:** Curated ideas/options with trade-offs, then offer to go deeper on the chosen one

### Focused Mode
**When:** User has a specific problem with existing context and wants strategies or recommendations.
**Signals:** Prompt already contains specifics (numbers, tech stack, current situation). User says "brainstorm วิธี...", "how to reduce...", "what's the best approach to..."
**Flow:** Targeted discovery (2–4 questions) — only ask about genuine unknowns, skip what's already stated
**Output:** Actionable strategies/recommendations with priorities and estimated impact

## Workflow by Mode

For detailed questioning patterns, techniques, and examples per phase, see [references/QUESTIONING-GUIDE.md](references/QUESTIONING-GUIDE.md)

---

### Prompt Mode — Full Discovery

The most thorough path. Use all phases when the user needs a well-crafted prompt.

**Phase 1 — Receive:** Acknowledge the request. Say something like: *"I'll help you craft that prompt. Let me ask a few questions to make it specific to your situation."*

**Phase 2 — Goal:** What does the user want the prompt to achieve? Get to a one-sentence goal with at least one measurable indicator. (1–2 questions)

**Phase 3 — Direction:** What must NOT happen? What approaches exist? Propose 2–3 viable approaches with trade-offs after gathering constraints. Lead with your recommendation. (1–2 questions + proposal)

**Phase 4 — Reference (optional):** Only if references would genuinely help (e.g., style/design requests). Ask if they have examples. If none and it would help, use `WebSearch`. Skip entirely for straightforward requests. (0–1 questions)

**Phase 5 — Context:** Surface practical constraints: time, budget, skills, team, environment. Flag contradictions with the goal gently. (1–2 questions)

**Phase 6 — Criteria:** Define what "good" means. Force-rank if more than 3 criteria. (1 question)

**Phase 7 — Synthesize:** Draft the improved prompt with this structure:

```
## Improved Prompt

[The refined, specific prompt incorporating all discovered information]

---

### Discovery Summary

**Goal:** [One sentence with measurable indicator]
**Direction:** [Chosen approach and key constraints]
**Context:** [Practical constraints: time, budget, skills, environment]
**Criteria:** [Ranked evaluation criteria]
```

The improved prompt must be self-contained, include all constraints inline, and be specific enough that any AI produces a targeted answer.

Present it and ask: *"Does this capture what you need? Anything to adjust?"* Iterate if needed.

---

### Explore Mode — Light Discovery

For open-ended brainstorming where the user wants ideas, not a prompt.

**Phase 1 — Receive + Quick Goal:** Acknowledge, then ask ONE question combining goal + motivation. Example: *"What draws you to this — learning, earning, solving a personal problem, or something else?"* (1 question)

**Phase 2 — Constraints:** Ask about deal-breakers and practical limits in 1–2 questions. Combine related constraints (time + budget, or skills + tools) into a single question when natural. (1–2 questions)

**Phase 3 — Generate:** Based on what you've learned, produce **5–8 concrete ideas** organized by theme. Each idea should include:
- What it is (one sentence)
- Why it fits this user's constraints
- One potential challenge

**Phase 4 — Narrow:** Ask which ideas resonate. Then offer:
1. **Go deeper** on one idea (pivot to Prompt Mode or create a plan)
2. **Generate more** ideas in a specific direction
3. **Done** — take the ideas and go

---

### Focused Mode — Targeted Discovery

For specific problems where the user already provided good context.

**Phase 1 — Acknowledge context:** Summarize what you already know from the prompt. Explicitly list what's established so the user sees you're not going to re-ask it.

**Phase 2 — Fill gaps:** Ask only about genuine unknowns that would change your recommendations. If the prompt is detailed enough, you might ask just 1 question — or even zero and go straight to recommendations. (0–2 questions)

**Phase 3 — Strategize:** Produce actionable recommendations:
- Prioritized list (quick wins first, then bigger efforts)
- Each item: what to do, estimated impact, effort level, risks
- Clear "start here" recommendation

**Phase 4 — Refine:** Ask if anything needs adjustment. Offer to create an implementation plan via Plan subagent.

---

## Next Step

After delivering the output (regardless of mode), offer next steps using `AskUserQuestion` (or `ask_user` / plain text if unavailable):

- **Create a Plan** — Delegate to Plan subagent: `Agent(subagent_type: "Plan")` (Claude Code), or `task(agent_type: "general-purpose")` with `# Role: Planner` block (Copilot), or create the plan inline if neither is available
- **Go deeper** — Continue exploring a specific aspect
- **Done** — End the workflow

## Handling Edge Cases

**User wants to skip questions:** Respect it. Produce the best output with what you have. Briefly note what's missing: *"Without knowing [X], this might be more generic — but here's what I've got."*

**User says "I don't know":** Offer 2–3 concrete options and let them react. Reactions reveal preferences without requiring expertise.

**Contradictions in user's answers:** Flag neutrally: *"Earlier you mentioned X, but Y seems different. Which should we prioritize?"*

**Too broad for one session:** Suggest splitting. Run the workflow for each piece.

**Mode feels wrong mid-conversation:** Switch. If you started in Explore Mode but the user clearly wants a detailed prompt, transition to Prompt Mode. No need to restart — carry forward what you've learned.
