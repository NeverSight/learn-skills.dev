---
name: vc-info
description: Research any venture capital firm and produce a concise fundraising-focused briefing. Use when the user asks to look up, research, analyze, or get information about a VC firm, venture fund, or investor. Triggers on "tell me about {VC}", "research {fund}", "vc info {name}", "who is {VC}", "analyze {investor}", "{VC} fund size", "{VC} portfolio", "what does {VC} invest in". Designed for startup founders actively fundraising who need quick intel on a specific VC. Requires web search tools.
---

# VC Info

Produce a concise VC firm briefing from web research. Max 2 search rounds.

## Research

**Round 1 — run all in parallel:**

1. `{name} venture capital fund size AUM overview`
2. `{name} VC portfolio companies investments`
3. `{name} venture capital partners team`
4. `{name} VC investment thesis verticals`
5. `site:crunchbase.com/organization {name}`
6. `site:linkedin.com {name} venture capital partners`
7. Fetch the firm's website homepage, /team, /portfolio, and /about pages

**Round 2 (only if critical gaps):** Max 3 targeted follow-ups for missing fund size, partner LinkedIn URLs, or portfolio data.

## Rules

- Never fabricate. Write "Not disclosed" for missing fields.
- Use search snippets when sites block fetching (LinkedIn, Crunchbase).
- **LinkedIn links:** Extract actual `linkedin.com/in/...` URLs from search results. Never guess. Omit if not found.
- Cross-reference fund size across 2+ sources when possible.
- Prefer sources from last 12 months.
- List at least 5 portfolio companies, prioritizing well-known ones.
- Include all GPs and MDs; limit other team to notable members.

## Output

Read `references/template.md` for the exact output structure. Sections:

1. **TLDR** — 2-3 sentences + key facts table
2. **Thesis & Focus** — philosophy, sweet spot, geo, what they look for
3. **Team** — background + LinkedIn
4. **Funds** — table of funds with year, size, status
5. **Portfolio** — table with vertical, stage, status
6. **Access & Process** — how to get in, speed, founder-friendliness
7. **Value Add & Reputation** — beyond capital + founder sentiment
8. **Recent Activity** — latest fund, deals, exits
9. **Quick Take** — best fit / skip if

Keep sentences short. No filler. If data unavailable, say so.

## Edge Cases

- **Micro VC / solo GP:** Single partner, smaller portfolio, may lack fund history.
- **Corporate VC:** Note parent company, strategic vs financial, strings attached.
- **Multi-stage / mega fund:** Clarify which stage team is relevant.
- **Angel group / syndicate:** Note if formal fund or deal-by-deal.
- **Not found:** Tell the user directly.
