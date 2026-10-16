---
name: ecom-applicability
description: Determine whether AI is appropriate for a specific e-commerce task. Use when evaluating if a problem has enough data, the right tools, or acceptable risk for AI automation. Answers 'should I use AI for X?' with boundary-aware reasoning.
---

# Applicability Skill

Determine whether AI is appropriate for a specific e-commerce task — answers "should I use AI for X?" with boundary-aware reasoning instead of a generic yes/no.

## When to Use

- The user asks "should I use AI for X?", "can AI do X?", or "is it worth automating X?".
- The user is deciding between AI, manual work, a script, a SaaS tool, or a workflow engine.
- The user is about to invest in an AI tool, agent, or pipeline and needs a feasibility/ROI sanity check.

## Routing Method

### Step 1 — Identify the Domain Chapter

Map the question to the matching chapter in `references/boundaries.md` (57 chapters, grouped by path):

| If the question is about… | Look up |
|---|---|
| Foundations: prompt quality, RAG, agents, RPA, tool choice | `## Path 0 · Foundations` |
| Listing, ads, customer service, inventory, pricing, SEO, visual content, compliance, research, brand, finance, growth, operations agent | `## Path A · Operators` |
| Data pipeline, prediction, RAG systems, agents, local models, review NLP, dashboards, image pipelines | `## Path B · Developers` |
| AI assessment, team upskilling, ROI, risk governance, competitive intel | `## Path C · Managers` |
| A specific marketplace (Amazon, Walmart, Temu, Shopify, TikTok Shop, eBay, etc.) or cross-platform strategy | `## Path D · Platforms` |
| A social channel (Meta, YouTube, 小红书, Pinterest, WhatsApp, Reddit) or cross-channel strategy | `## Path E · Social Media` |

Not sure? Grep `boundaries.md` for the domain keyword (e.g. `pricing`, `RAG`, `Temu`) — each chapter's `Source:` line gives the exact book file.

### Step 2 — Check Boundary Conditions

Read that chapter's entry. Every entry is a list of "this doesn't work when…" bullets. Evaluate the user's situation against each bullet using the three-part decision rule:

1. **Data sufficiency** — is there enough real data? (e.g. ≥1 year of sales history for inventory models, ≥hundreds of reviews for review NLP, real search-term data instead of guessed keywords). If the data is missing, estimated, or polluted, the AI cannot produce a trustworthy answer.
2. **Tool availability** — does the tool/API exist and fit the constraints? (e.g. platform API instead of fragile RPA, local model when data cannot leave the network, official API instead of scraping). If the tool doesn't exist or the constraint blocks it, the whole approach is off the table.
3. **Risk / reward** — what is the cost of being wrong, and can it be reversed? (e.g. irreversible actions like auto-pricing, auto-orders, or legal filings must have human confirmation; low-frequency tasks may not repay automation cost).

### Step 3 — Give the Verdict

- **If a boundary bullet applies** → answer **"No"** clearly, then name the *specific prerequisite* from that bullet (e.g. "not yet — you need one full year of sales history first", "no — that action is irreversible, make it suggest + human-confirm").
- **If no bullet applies** → answer **"Yes"**, then attach the caveats the chapter implies (e.g. "yes, but fix your conversion rate first", "yes, but verify the platform's current policy before scaling").
- **Ambiguous or multi-domain** → answer per domain, and state which chapter's boundary decided each part.

### Step 4 — Escalate to Execution

If the verdict is "yes", hand off to the domain-specific skill for execution (ecom-listing, ecom-advertising, ecom-pricing, ecom-inventory, ecom-research, ecom-compliance, etc.) — see `references/playbook.md`. This skill decides *whether*; the other skills decide *how*.

## Key Decision Rule

**Data sufficiency + tool availability + risk/reward.** A "yes" requires: (1) enough real data, (2) a tool that exists and fits the constraints, (3) error cost that is bounded or reversible. If any of the three fails, the answer is "no" until the prerequisite is met — not a modified prompt.

## References

- [Boundaries](references/boundaries.md) — 57 chapter-specific applicability rules (the source of truth for this skill)
- [Constraints](references/constraints.md) — why this skill uses boundary conditions instead of numeric constraints
- [Playbook](references/playbook.md) — what to do when prompts ARE needed (hand off to domain skills)
