---
name: first-customer-finder
description: >-
  Find and qualify evidence-backed potential first customers, early adopters,
  design partners, or beta users for a startup from recent public signals.
  Trigger on "find my first customers", "who would buy this", "find early
  adopters", "find design partners", "find beta users", "find leads for my
  startup", or when given a product URL and asked who might use or pay for it.
  Research-only: defines an ICP, mines public discussions for pain and buying
  signals, scores prospects, drafts outreach openers, and generates an HTML
  report. Never sends messages or contacts anyone.
---

# First Customer Finder

Turn a startup URL or product description into a short, evidence-backed shortlist of plausible first customers. Every prospect must trace to a real public signal you have verified at the original source. The shortlist is a research hypothesis, not a customer database.

Read [references/research-framework.md](references/research-framework.md) before searching or scoring. Read [references/report-schema.md](references/report-schema.md) before generating the report.

## Workflow

### 1. Understand the product

Fetch the supplied URL (and its pricing/about pages if they exist) or read the description. Establish: what the product does, the outcome it sells, who uses it vs. who pays for it, price or buying motion, geography or language constraints, and the single strongest use case.

Commit to **one primary ICP and one adjacent ICP**, each with pain triggers, positive signals, and explicit disqualifiers. For two-sided products, pick the side with a buying motion as primary — do not hedge by mixing both sides in one shortlist. Label anything you inferred rather than observed. Ask the user one question only if the ambiguity would change where you search.

### 2. Fan out the signal search

Run the five query buckets from the research framework (explicit demand, pain, workaround, switching, timing) as **parallel research subagents** — one bucket per agent, each returning candidate signals with source URLs, dates, and verbatim-adjacent summaries. Give each agent the product brief and ICP so it can reject weak matches at the source. Instruct each agent to fetch and quote its sources — an agent may not return a URL it did not open. If the environment has no subagent support, work the buckets sequentially instead.

Vary source types across agents: forums, public social posts, product and marketplace reviews, GitHub issues and feature requests, public company pages, job posts, and changelogs.

### 3. Verify before you qualify

Fetch the original page for every candidate signal before it can enter the shortlist. A search snippet, an aggregator summary, or a subagent's unquoted paraphrase is not evidence. Confirm the page exists, the signal says what was claimed, and the date. Drop anything that fails. Record source URL, source type, visible publication date (or "date unavailable"), and what was observed versus inferred. When subagents have already fetched and quoted a source, spot-check their work — and always re-verify the top three prospects yourself.

Many high-value sources block server-side fetching (Reddit, G2/TrustRadius, Cloudflare-fronted job boards). Do not drop a candidate for that alone — verify through an alternate legitimate route: a browser session, an official API (e.g. HN Algolia), or the site's RSS feed. Third-party archives can run months stale; prefer the live page and note which route verified it.

Research boundaries (non-negotiable):

- Public, intentionally shared professional or business information only.
- Never bypass logins, paywalls, rate limits, or robots restrictions.
- No data brokers, leaked datasets, private groups, personal email or phone discovery.
- Never infer or use protected traits (health, finances, politics, sexuality, religion).
- Paraphrase by default; quote minimally; link every material signal.

### 4. Score and prune

Score each verified prospect with the weighted rubric in the research framework (pain, fit, timing, reachability, evidence quality → 0–100). Deduplicate. A prospect below 50, or without a cited pain/demand/timing signal, does not appear in the primary shortlist — a bare ICP match is speculative, not qualified.

Never state or imply that a prospect is interested, has consented, or will buy. Label everything "potential customer based on public signals."

### 5. Draft outreach — never send it

For each shortlisted prospect, suggest the most natural channel already attached to the source (reply in the thread, public profile, company contact page) and draft one opener under 90 words: mention the public context naturally, connect it to the exact problem, describe the product in one sentence, end with one low-friction question. Ground it only in the cited source — no feigned familiarity, no personal details.

Do not send messages, submit forms, comment, follow, connect, or create CRM records. If the user asks you to send, treat that as a separate request requiring their explicit authorization per message.

### 6. Generate the report

Default to a standalone HTML report (chat-only if the user asks):

1. Write the analysis as JSON per [references/report-schema.md](references/report-schema.md) to a temp/work directory.
2. Run `python3 scripts/generate_report.py <analysis.json> <output.html>` (script lives in this skill's directory; stdlib only).
3. Save the report under `outputs/` in the workspace and return a clickable absolute file path.
4. Open the HTML and verify: prospect cards render, every source link is a real URL, scores match the rubric, patterns and the seven-day plan are present.

In chat, lead with the verdict and the single strongest prospect, then the file link.

## Modes

- **quick** — up to 5 strong prospects.
- **standard** (default) — up to 10 prospects across several source types.
- **deep** — up to 20 prospects plus repeated-pain pattern mapping.
- **design-partners** — prioritize users who will test and give feedback over buyers.
- **b2b** — prioritize companies, public business triggers, and decision roles.
- **community** — prioritize public discussions and explicit "looking for a tool" requests.

## Gotchas

- **Fabrication is the failure mode that kills this skill.** A plausible prospect with a dead or mismatched link is worse than no prospect. Verification (step 3) is not optional, even in quick mode.
- **Two-sided products:** subagents will return a mixed bag of both sides. Filter to the primary ICP before scoring; note the adjacent side under patterns instead.
- **Old signals:** an explicit request from 18 months ago can still qualify, but cut its timing score and print the date next to it.
- **Ten strong beats thirty generic.** If verification leaves you with four great prospects, ship four and say why.
- **Respect impatience.** If the user asks you to hurry or wrap up mid-run, switch to quick mode immediately: stop waiting on unfinished search buckets, verify and score what you already have, and ship the report with a note about which buckets were cut short.
