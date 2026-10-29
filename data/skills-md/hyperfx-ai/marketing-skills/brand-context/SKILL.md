---
name: brand-context
description: "Create and maintain a single brand-context.md — positioning, audience, personas, pain points, customer language, voice, proof points — that every other marketing skill reads before asking the user to re-explain their business. Auto-drafts from the brand's site via Firecrawl, or builds the doc through a short interview. Use when the user wants to set up brand context, onboard a new brand, define positioning / brand voice / ICP, or complains about re-answering the same brand questions."
metadata:
  version: 1.0.0
icon: hyper
short_description: One brand-context.md per brand — the shared positioning, audience, and voice doc every other skill reads first.
---

# Brand Context

Build and maintain **one `brand-context.md` file per brand**: the single source of truth for what the business sells, who it sells to, how it talks, and what it can prove. Every other skill in this collection reads this file before asking the user brand questions, so the user explains their business once — not once per task.

This is the hub in a hub-and-spoke model. Ad copy, blog posts, cold email, social content, and landing-page work are all downstream of the same positioning and voice; when those live in one maintained doc, every downstream skill starts warm and stays consistent.

> **The file contract.** The doc lives in persistent storage at a stable path — `/files/<brand-slug>/brand-context.md` — and is reused at that SAME path every time. Create it once, then **update it in place**; never recreate it from scratch when it already exists (you would destroy verbatim customer language and proof points the user curated). If a run touches the doc, bump the `Last updated` line.

## Requirements

- **Hyper MCP connected.** https://app.hyperfx.ai/mcp — needed for the file tools that persist the doc, and for auto-draft.
- **Recommended for auto-draft**, enabled at https://app.hyperfx.ai/apps: **Firecrawl** (read the brand's site and extract visual identity). Without it, skip auto-draft and use the interview path — the skill still works.
- **Optional enrichment:** the Apify scrapers used by `customer-research` (verbatim customer language) and **HyperSEO** (competitive landscape). Both are nice-to-have; mark any section built without real data as unverified rather than inventing content.

### How to run the tools in this skill

Every tool in this skill is named by its canonical tool name. Run it with the call your surface gives you:

| Surface | Find a tool | Run it |
| --- | --- | --- |
| Hyper chat | Call the tool by its name; `search_tools(queries=["<provider> <action>"])` shows its parameters | `<name>(...)` |
| MCP client (Claude, Cursor, Codex, ChatGPT) | `search("<what you want to do>")`, then `describe("<name>")` | `call_read("<name>", {...})`, `call_write` or `call_destructive`: the one that `describe` names in `call_with` |
| Hyper CLI | `hyperai search "<what you want to do>"`, then `hyperai describe <name>` | `hyperai call <name> --json '{...}'` |

If a tool is not found: in Hyper chat, find its toolkit id with `discover_toolkits` and pass it to `enable_toolkit`. On an MCP client or the CLI, tell the user which integration to connect in Hyper.

## Tool surface

| Job | Tools |
| --- | --- |
| Read, create, update `brand-context.md` | your file tools (`read_file`, `create_file`, `edit_file`) |
| Auto-draft from the brand's site | `firecrawl_urls_scrape` (homepage, about, pricing, product pages), `web_pages_scrape` fallback |
| Visual identity (colors, logo, typography) | `firecrawl_branding_extract` |
| Verbatim customer language (optional) | defer to `customer-research` |
| Competitive landscape (optional) | defer to `competitor-intel`, `seo-research` |

## Out of scope: defer to other skills

| Request | Send them to |
| --- | --- |
| Deep voice-of-customer mining (Reddit, reviews, social) | `customer-research` |
| Full competitor research, battle cards, monitoring | `competitor-intel` |
| Blog topic strategy and the published-post log | `blog-generation` (its `blog-strategy.md` **Brand brief** should be seeded from this doc, not rebuilt) |
| Extracting brand assets for image generation | `ad-creative-generation` (`firecrawl_branding_extract` at creative time) |
| Keyword or SERP research | `seo-research` |

## The document

The full template with per-section guidance lives in `references/brand-context-template.md`. The sections, in order:

1. **Product overview** — what it is, what it does, category, one-liner.
2. **Target audience / ICP** — the specific customer, firmographics or demographics, who it is NOT for.
3. **Personas** — 2–4 buyer/user personas with role, trigger, and success criteria.
4. **Pain points** — the problems that drive purchase, ranked.
5. **Competitive landscape** — direct and indirect alternatives, including "do nothing" / spreadsheets / status quo.
6. **Differentiation** — why customers pick this brand over each alternative; what only this brand can claim.
7. **Objections & switching** — what stalls deals, what prospects fear, what switching costs them.
8. **Customer language** — verbatim quotes: how customers describe the problem and the product in their own words. The most valuable section in the doc.
9. **Brand voice** — tone, reading level, point of view, words to use, words to ban.
10. **Proof points** — real numbers, named customers, credentials, data. Only verified items belong here.
11. **Goals & current focus** — what marketing is trying to move this quarter, priority channels.
12. **Assets & channels** — site URL, blog, social handles, ad accounts in play, visual identity notes.

## Building the doc

**Step 0: check for an existing doc.** Look for `brand-context.md` at the brand's path (and reasonable legacy locations). If one exists, this is an **update** run: read it fully, then only revise the sections the user wants changed or that new evidence contradicts. Only when nothing exists do you build fresh.

**Path A — auto-draft (default when the brand has a website).**
1. Ask for the site URL if you don't have it.
2. Scrape the load-bearing pages with `firecrawl_urls_scrape`: homepage, about, pricing, 1–2 product/feature pages, and a customer-facing page with testimonials or case studies if one exists.
3. Optionally call `firecrawl_branding_extract` once to fill the visual identity notes in section 12.
4. Draft every section you have real evidence for. Where the site is silent (objections, goals, most customer language), leave the section marked `*(unverified — needs input)*` instead of guessing.
5. **Present the draft to the user section by section for correction before saving.** The site says what the brand *wants* to be true; the user knows what *is* true. Ask specifically about: the ICP ("who actually buys?"), differentiation ("why do people pick you over X?"), and proof points ("which of these numbers are real and current?").
6. Save to `/files/<brand-slug>/brand-context.md` and report the path.

**Path B — interview (no site, pre-launch, or user prefers talking).**
Walk the sections conversationally, a few questions at a time, in the order given in `references/brand-context-template.md` — not as one giant questionnaire. Start with product overview and ICP (everything else hangs off those), and let the user skip sections; an honest partial doc beats a padded complete one. Save incrementally so a broken-off interview still leaves a usable doc.

**Either path, before saving:** run the quality gate below.

## Quality gate

- **No fabrication, anywhere.** Never invent a customer quote, a stat, a competitor claim, or a persona detail. An empty section marked "needs input" is correct; a plausible invented one is corrosive — downstream skills will confidently repeat it in ads and emails.
- **Verbatim means verbatim.** Customer language is quoted exactly as customers said or wrote it, with a source (review, call, Reddit thread). Polished paraphrases go in positioning, not in section 8.
- **Specific beats complete.** "Ops managers at 20–200-person e-commerce brands drowning in carrier spreadsheets" is useful; "businesses that want to save time" is filler. Cut filler.
- **Proof points are verified.** Only numbers and names the user confirmed. Date them ("2,400 customers as of Jun 2026").
- **The one-liner passes the stranger test.** Category + audience + core value in one sentence a stranger could repeat.

## How other skills consume this doc (the spoke contract)

When any marketing skill needs brand context — positioning, audience, tone, proof:

1. **Check for `brand-context.md` first** at `/files/<brand-slug>/brand-context.md` before asking the user a single brand question. If it exists, read the whole file and ask only for what the task needs that the doc doesn't cover.
2. **Honor the voice section** — the words-to-use / words-to-ban lists are hard constraints on generated copy.
3. **Pull hooks from customer language** — verbatim phrases from section 8 outperform invented copy; prefer them for headlines, subject lines, and openers.
4. **Never cite a proof point that isn't in section 10.** If the doc has no proof for a claim, the copy doesn't make the claim.
5. **Check freshness.** If `Last updated` is more than ~6 months old, flag it and offer a refresh — but do not silently rebuild the doc mid-task.
6. **Write back nothing.** Spokes read; only this skill (with the user) writes. If a task surfaces something that belongs in the doc — a great customer quote, a new competitor — suggest the user run `brand-context` to add it.

## Maintaining the doc

The doc is alive. Update it when positioning shifts, a new competitor matters, pricing changes, or research (from `customer-research` / `competitor-intel`) yields better quotes and landscape data. On update runs: read first, edit only what changed, keep everything the user curated, bump `Last updated`, and summarize the diff back to the user. For multiple brands, keep one doc per brand under its own `<brand-slug>` directory — never mix brands in one file.

## References

- `references/brand-context-template.md`: the full copy-paste document template, per-section guidance on what good looks like, and the interview question bank for Path B.
