---
name: writeup-ingest
description: Reusable bug-bounty writeup / CVE ingestion pipeline for the BB-OS skill library. Converts 2024-2026 disclosed reports, CVEs, and vendor advisories into additive, cited, deduped skill sections. Use at the start of a fresh campaign when the threat landscape for a class may have changed, after a big ecosystem event (Keycloak/Spring/DOMPurify advisory wave), or whenever a fellow hunter posts a writeup for a class you work. Complements the one-shot enrichment sprints by making ingestion repeatable.
---

# Writeup & CVE Ingest (Repeatable Pipeline)

One-shot enrichment sprints (like the 2026-09 10-class pass) burn out fast. This skill is the *repeatable* one: turn a single good writeup or advisory into a durable, cited, deduped skill patch in one sitting — without bloating the library.

## When to run

- **Start of a campaign** on a class your library is weak on (spot-check the target `hunt-*` skill's `## CVE & Writeup Grounding (2024–2026)` table — if it lacks recent rows for the class, run this).
- **After an advisory wave**: Keycloak, Spring / Spring Security, DOMPurify, axios, nextjs, OData/CDS updates drop in bursts — one event usually ships several CVEs at once.
- **A peer writeup is relevant** ("I read that Shopify BOLA post and I want it in my SSRF skill").
- **An OOB/version finding on your target** matches a class you plan to spend time on (e.g., target runs Keycloak 26.x → ingest the KC CVE set before testing).

## Source queries (5 minutes, saved for replay)

Run these via websearch, in this order; keep the *primary* sources (vendor advisory / GHSA / H1 report / portswigger-research / assetnote) — not aggregator summaries.

1. `"<class>" "bug bounty" writeup 2024..2026 site:hackerone.com OR site:portswigger.net OR site:assetnote.io`
2. `<tool/framework> security advisory 2024..2026` (GHSA / vendor security page)
3. `<framework> CVE 2024 OR CVE 2025 OR CVE 2026 RCE OR XSS OR SSRF OR IDOR OR "privilege escalation"`
4. If the class is Microsoft/OAuth/Keycloak-shaped: check the vendor's *fixed-version matrix* (advisory lists the patched version — the entire "still vulnerable <= X" story maps straight to live targets).

## The 6-question extraction gate

A writeup/CVE earns a slot **only** if all six pass. One fail → leave it out (or list as raw row in the ledger only, never in a skill).

1. **Is the primary source real and fetchable?** (URL present, no `CVE-2026-99999`-style guess.) CVE IDs are hallucination-prone — re-verify the ID resolves at NVD/MITRE/GHSA before writing it.
2. **Can we state the root cause in one sentence?** (e.g., "presence-only tenant header", "OData child-entity authz gap".) Vague "auth bypass" entries get rejected.
3. **Does it teach a technique not already in the target skill?** (Check the skill's existing tables + the ledger first — no dupes.)
4. **Does it apply to *this campaign's* stack?** (Keycloak/Spring/WebFlux/CDS rows go to the top of the target-specific skill; generic rows go to the bottom.)
5. **Do we have a payload sketch the hunter can actually fire?** (Parameter name, body shape, or the exact string — not "some injection".)
6. **Can we bound severity honestly?** (Blind-only? Needs localhost presence? Requires admin? Note the precondition in the row.)

## Patch recipe (per skill)

Every patch is **additive and small**. Never rewrite existing sections.

1. Open the target `skill/SKILL.md`, go to the `## Related Skills & Chains` heading at the end of the body.
2. Insert **before** it (so it stays inline with the body, chains stay last):
   - `## CVE & Writeup Grounding (2024–2026)` — table `| Ref | Technique | Payload / data sketch | Apply where |`, rows newest-first, each row's Ref linking the primary source.
   - `## Bypass & Payload Additions (2024–2026)` — table `| Defense/filter | Bypass | Preconditions | Ref |`, only rows about *defenses a real target actually ships* (presence-only headers, IMDSv2, PKCE-enforced clients, etc.).
   - `## Chains & Compositions (Senior Hunting)` — only if the skill does not already have one. 2–4 bullet chains, each one *root cause → composed primitive → concrete target composition*.
3. Cap the whole insert at ~40–70 lines. If the source gives you more, save the excess rows in the ledger, not the skill.
4. Reference the target by *its real surface* where you can (e.g., "target identity SPA ships Bearer to `http://localhost`" — a cross-ref to a session finding, not a generic lesson).

## Dedup ledger

Every ingested source gets **one line** in `bb-ops/memory/knowledge/writeups/README.md`:

| Date | Class | Ref (CVE/H1/GHSA/URL) | Target skill | One-line technique |

Ship the row at the same time as the skill edit. The ledger is the single source of truth for "have we ingested this?", so future sprints can answer it in one grep.

## Citation-honesty rules

- Link the **primary source**. If the research pass could not fetch/verify a URL, mark the row `(unverified — re-check before cite)` in the skill or drop it to the ledger raw row — never present an unverified CVE as confirmed.
- List the **fixed version matrix** when the vendor gives one (e.g., `fixed 22.0.10 / 24.0.3`) — it tells the hunter whether a live target is actually exposed.
- State the **precondition** in the row (blind? localhost? admin-only? needs user interaction). A row without its precondition is a trap for a later hunter.
- Never invent a "payload sketch" — if the writeup doesn't show the exact string, describe the shape and note it as inferred.

## Output & handoff

- Skill patches land in `/root/.opencode/skills/<class>/SKILL.md`; ledger rows in `bb-ops/memory/knowledge/writeups/README.md`.
- Optionally append **generic new payload lines** to the matching playbook's `instruct:` field in `bb-ops/playbooks/*.yaml` (only engine/string-level payloads, no target-specific claims).
- Do **not** convert ingestion to a report — ingestion is a read/learn activity. Findings that emerge from a writeup *as applied* go through the normal router → analyzer → verifier path.

## CVE-fact hygiene (specific to this pipeline)

- CVE IDs dated ≥2026 or in the current year are more hallucination-prone; NVD/MITRE/GHSA is the tiebreaker, not the researcher's memory.
- CVEs that are about *a thing the target actually runs* (Keycloak, Spring Security, DOMPurify, axios) get priority; CVEs about adjacent products go in the ledger only.
- Every row must survive "would the original author recognize this as their work?" — if in doubt, drop the claim or the link.

## Related skills

- `bb-methodology` — the master orchestrator; this skill is the "learn from writeups" node it routes to.
- `triage-validation` / `ywh-triage` — apply when an ingested technique *becomes a live finding* (not while ingesting).
- `hunt-spa-api`, `hunt-source-leak` — the recon side that surfaces which frameworks a target runs (so you know which CVE rows to prioritize).