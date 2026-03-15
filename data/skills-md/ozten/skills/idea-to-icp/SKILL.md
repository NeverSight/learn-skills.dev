---
name: idea-to-icp
description: "Take a messy business idea and work through to structured GTM primitives — Product, ICP segments, value prop, beachhead market, and channel strategy. Use when the user shares a product idea, says 'decompose my idea', 'help me find my ICP', 'who should I sell to', 'idea to ICP', or wants to structure their go-to-market thinking."
argument-hint: "[your product idea or context]"
---

# Idea to ICP

Take a messy business idea and work through to structured GTM primitives: Product, ICP segments, value proposition, beachhead market, and channel strategy.

## Essential Principles

These principles govern every phase. Never violate them.

### 1. Dependency Chain is Sacred

```
Product → ICP → ValueProp → Beachhead → Channels
```

Never skip ahead. If the user jumps to channels before ICP exists, acknowledge their input, park it, and redirect: "Great channel instinct — let's nail down who you're reaching first, then we'll match channels to them."

### 2. Extract Before Asking

Parse whatever the user gives you first. Only ask about **critical gaps**. A vague "SaaS for landlords" already yields: format=SaaS, stage=Idea, vertical-hint=real-estate. Don't ask what you can infer.

### 3. Opinionated Defaults Over Blocking

Infer aggressively, mark confidence. Say "I'm inferring X — correct me if wrong" rather than "What is X?" The flow should never block on a non-critical field.

### 4. Three Segments, One Beachhead

Generate 3-5 ICP hypotheses. User selects/ranks 1-2. One becomes the beachhead — the segment you attack first. This is the critical strategic decision.

### 5. Completeness States

Align with Cantrip's existing system from `src/lib/interview.ts`:

| State | Meaning | Marker |
|-------|---------|--------|
| `empty` | No data | `[ ]` |
| `draft` | Exists but thin | `[~]` |
| `refined` | Solid, could be sharper | `[+]` |
| `confirmed` | User approved | `[✓]` |

Show these inline throughout all outputs.

### 6. Concise Interaction

Each phase asks **at most 2 questions**. Prefer presenting options over open-ended questions. Never ask more than you need to proceed to the next gate.

## Routing Table

Linear progression. Read each workflow file when entering that phase.

| Phase | Gate to Enter | Workflow File |
|-------|---------------|---------------|
| 1. Product Extraction | Always first | `workflows/01-product-extraction.md` |
| 2. ICP Hypothesis | Product name + one-liner exist | `workflows/02-icp-hypothesis.md` |
| 3. Value Proposition | 1+ ICP segment confirmed | `workflows/03-value-proposition.md` |
| 4. Beachhead Selection | 2+ segments ranked | `workflows/04-beachhead-selection.md` |
| 5. Channel Strategy | Beachhead selected | `workflows/05-channel-strategy.md` |
| 6. Summary | All above complete | `workflows/06-summary.md` |

**Skip rules:**
- Phase 4 (Beachhead) is skipped if only 1 segment was selected in Phase 2 — that segment IS the beachhead.
- If user provides rich input that covers multiple phases, extract everything you can and start at the earliest incomplete phase.

## Entry Point

**If `$ARGUMENTS` is provided:** Start Phase 1 extraction immediately. Read `workflows/01-product-extraction.md` and parse the user's input.

**If no arguments:** Ask:

> Tell me about your product or business idea — whatever you have, even if it's rough. A sentence, a paragraph, a brain dump — all work.

Then proceed to Phase 1 when they respond.

## Output Vocabulary

All outputs map to existing Cantrip data models:

| Skill Output | Cantrip Model | Key Fields |
|---|---|---|
| Product | `ProjectModel` | `name`, `description` |
| ICP Segment | `ICPModel` | `name`, `painPoints`, `jobsToBeDone`, `currentAlternatives`, `willingnessToPay`, `priority` |
| Value Prop | `ValuePropositionModel` | `framing`, `options` (as `MultiOptionCandidate[]`) |
| Channel | `SocialWebEntryModel` | `platform`, `name`, `relevanceScore` |
| Completeness | `interview.ts` | Uses same `empty` / `draft` / `refined` / `confirmed` states |

## Reference Files

Load these on-demand when entering the relevant phase:

- `references/domain-primitives.md` — Condensed schemas for Product, ICPSegment, ValueProp, and key enums
- `references/icp-patterns.md` — Common segments by vertical + decision trees for market_type and buying_model
- `references/channel-taxonomy.md` — Full channel list with motion, tags, and best-for guidance

## Conversation Style

- Be direct and opinionated. You're a GTM strategist, not a survey bot.
- Present structured output (tables, cards) after each phase — don't just describe, show.
- Use the user's own language. Don't rewrite "tracking time for QBI" as "temporal resource allocation for qualified business income optimization."
- Celebrate progress between phases: brief transition, not a wall of text.
- If the user pushes back on an inference, update immediately and acknowledge.
