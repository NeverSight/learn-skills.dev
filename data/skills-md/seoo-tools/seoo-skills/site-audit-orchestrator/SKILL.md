---
name: site-audit-orchestrator
description: >
  Master entry point for this skill pack. Use whenever a user asks for a general SEO/content
  audit, says something like "audit my site," "how's my SEO," "help me grow my site," "help me
  publish this the right way," or any request that doesn't obviously name one specific skill in
  this pack. Reads the request, runs seo-growth-stage-strategy first to establish context, then
  routes to the correct specialist skill(s) below and sequences multi-skill requests. Not a
  replacement for the specialist skills — a router to them.
---

# Site Audit Orchestrator

This pack is a set of specialist skills, not one monolithic audit. This file's job is routing:
figure out what's actually being asked, run the one gating step every request should go
through first, then hand off to the right specialist(s) in the right order.

**Ask, but never block.** Every specialist skill in this pack has its own "Step 0 — Ask before
assuming" with clarifying questions, and every one also has an explicit fallback for when the
user can't or doesn't answer. Ask the questions when there's a chance of getting real answers,
but never stop the audit or refuse to produce output for lack of a response — fall back to
what's directly observable (the live pages, the site structure, general knowledge of the niche)
and say plainly which parts of the output are inferred versus confirmed. The same applies to
optional tool access (Search Console, Bing Webmaster Tools, backlink/keyword-data tools): treat
missing access as a reason to note reduced precision, never a reason to stop.

**Log what happened, not just what was found.** Any time work from this pack results in an
actual change, or a real judgment call gets made (e.g. deciding *not* to fix something a skill
flagged, or picking one option over another with no obviously-correct answer), apply
`change-and-decision-log`'s discipline before considering the task done — that's what lets a
future session (yours or another agent's) pick this back up without re-discovering or
re-arguing something already settled.

---

## Step 0 — Always run first: establish where the site actually is

Before recommending *any* action, use `seo-growth-stage-strategy` to establish whether this
site is in a coverage-building stage or a mature stage, and whether anything active/urgent is
happening. **Every specialist skill's recommendations should be weighted by this answer** — the
same finding (e.g. "this page could be optimized") means something different for a growing site
than a mature one. Skip this only if the user has already given this context in the same
conversation.

---

## Step 1 — Route the actual request

| The user is asking about... | Route to |
|---|---|
| Whether specific facts/figures/claims are still accurate | `verify-primary-source` |
| Whether the site has a real system for catching stale content over time | `content-freshness-audit` |
| Duplicate/cannibalizing pages, or general Google-penalty risk from templated content | `duplicate-intent-audit` |
| Whether titles/headings still match the page body after edits | `protected-field-audit` |
| Overall content quality, E-E-A-T, trust signals | `page-quality-audit` |
| Meta tags, schema, heading structure, mobile basics | `technical-seo-audit` |
| Internal links, link equity, "why isn't this page ranking" | `internal-linking-audit` |
| Backlink risk (spam/toxic links, disavow decisions) or off-page link-building opportunity | `backlink-profile-audit` |
| "What should I build next" / finding content gaps | `content-opportunity-discovery` |
| Whether/how safely to make an SEO change, or why a past change's effect is unclear | `measurement-discipline` |
| Legal/regulatory risk, affiliate disclosure, licensed-advice boundaries | `legal-regulatory-compliance` |
| Publishing new content the right way from the start | `content-creation-standards` |
| Keeping track of what changed/was decided across sessions, or a fresh session needing to catch up on prior state | `change-and-decision-log` |
| Pages not indexed; robots.txt, sitemap, noindex or canonical problems; Search Console indexing statuses | `indexing-crawl-health-audit` |
| Traffic or clicks fell, "did an update hit me," "is this a tracking issue" | `traffic-drop-diagnosis` |
| Moving a domain, changing URLs, replatforming, or merging/deleting pages (or "did my migration break SEO") | `site-migration-safety` |
| Low click-through on pages that already rank; rewriting titles and meta descriptions | `ctr-snippet-optimization` |
| Setting up ongoing monitoring, a weekly check, alerts, or a monthly SEO report | `seo-health-monitoring` |
| A broad "audit my whole site" with no narrower ask | run **all** of the above except the situation-specific ones (`traffic-drop-diagnosis`, `site-migration-safety`, `ctr-snippet-optimization`, `seo-health-monitoring`), in the order listed, after Step 0; offer those four when the findings point to them |

Multiple specialists often apply to one request — run each relevant one rather than picking
just one if the request genuinely spans several areas (e.g. "I'm about to publish 50 new pages"
should route to `content-creation-standards` for the per-page checklist *and*
`duplicate-intent-audit` for the batch-level duplicate risk *and* `seo-growth-stage-strategy` to
confirm a big batch is even the right move right now).

---

## Step 2 — Combine findings into one coherent output, not a stack of disconnected reports

When more than one specialist skill runs, synthesize: lead with the growth-stage context from
Step 0, then the highest-impact findings across all specialists run (not necessarily in the
order they were listed), then lower-priority findings. Don't just concatenate each skill's raw
output shape one after another with no synthesis — the person reading this wants one clear
picture, not several separate audits stapled together.

---

## Step 3 — Be explicit about what wasn't checked

If a request only warranted a subset of the specialists (per the routing table), say so
explicitly rather than silently running a partial audit and presenting it as complete. If a
specialist skill needs access this session doesn't have (e.g. Search Console access for
`content-opportunity-discovery` or `internal-linking-audit`), say what's missing and what the
audit could have found with it, rather than skipping the section silently.
