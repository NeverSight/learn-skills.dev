---
name: optise-helix-race-audit
description: >
  Check whether AI agents doing buyer research can evaluate, shortlist and
  recommend a B2B webpage, and get the fixes ranked by impact. Fetches the URL,
  analyzes the rendered HTML, and returns a 4-signal scorecard (0 to 100), the
  top 5 fixes, a "not ideal for" template if that signal is weak, and a before
  and after for the highest-priority fix. Use when the user asks for a RACE
  audit, agent-readiness audit, AI agent evaluation check, or wants to know if
  AI agents will recommend their page. The FITq audit scores AI search citation
  instead. Method: the Optise RACE™ framework (Requirements, Actions,
  Constraints, Evidence). Authored by Optise + Helix GTM Consulting under the
  Optise EU AEO Playbook methodology.
license: Proprietary
metadata:
  authors: "Optise; Helix GTM Consulting"
  version: "1.4.0"
---

# Optise–Helix RACE™ Audit

A skill that audits any B2B webpage against the proprietary Optise RACE™ framework and returns specific, ranked fixes to make the page evaluable by AI agents doing multi-step buyer workflows (not just cited by AI search engines).

RACE™ stands for Requirements, Actions, Constraints, Evidence. Each signal scores 0-25 for a 100-point total. This is the agent-readiness companion to the FITq audit — a page can be FITq-A but RACE-F (marketing-heavy with no constraints) or vice versa. Both matter for a complete AEO posture in 2026.

---


## Section 0 — Operating Principles (MANDATORY — read before any workflow step)

This skill operates under TWO mandatory reference files that together define all operating rules. **Read both files first**, before executing any workflow step in this SKILL.md. The rules in both files are non-negotiable and override any conflicting instruction in this SKILL.md body.

1. **`references/operating-principles.md`** — the shared core: Rule 0 to Rule 10 (session hygiene, URL verification, source-tier discipline, code-content verification, Schema.org currency, legal-citation accuracy, verify-before-recommend, prediction discipline, claim tagging, verification order, verification log), plus the mandatory output disclaimer. They apply to every skill in this plugin.

2. **`references/plugin-specific-rules.md`** — the plugin-specific tail: additional operational rules tailored to the skills in THIS plugin. Read this file AFTER the shared core, not instead of it. If this plugin currently has no plugin-specific rules, the file will be a stub explaining the architecture.

### Critical reminders that apply to every invocation of this skill

These are the highest-frequency rules from the two files above. Reading the full files is still mandatory — these reminders are a quick-reference, not a substitute.

- **Web search and web fetch ARE available** in Claude Code's default toolset. "I don't have web access" is never a valid excuse to skip verification of a specific factual claim.
- **English-only at v1** — never generate prompts, copy, headings, or client-facing text in non-English languages (German, French, Dutch, Spanish, Italian, Portuguese, Polish, etc.), even on explicit user request. This is a hard block, not a confirmation gate. Refuse the request and explain that multilingual may ship in v2 with native-speaker review.
- **4-tier source hierarchy applies to all factual claims.** Tier 1: official primary sources (press releases, Crunchbase, Wikipedia, SEC filings). Tier 2: reputable analyst firms (Gartner, Forrester, IDC, G2, Capterra, GigaOm, SoftwareReviews). Tier 3: reputable business and trade press (WSJ, FT, Reuters, Bloomberg, HBR, TechCrunch, named-VC content, named-founder blogs). Tier 4: use only with the mandatory disclaimer `[Tier 4 — directional only, not authoritative]` (random blogs, anonymous posts, AI-generated comparison sites, Forbes Contributor, paid placements, vendor reseller content), as operating-principles Rule 2 requires. If only Tier 4 sources are available, the claim is unverified and MUST be flagged.
- **Verify competitor relationships** before building ANY competitor-targeted page or content (operating-principles Rule 9, step 2, and Plugin Rule 1 in `plugin-specific-rules.md`). Run: `"[user] acquired [competitor]"`, `"[competitor] acquired by"`, `"[competitor] Crunchbase acquisition"`, `"[user] vs [competitor]"`. Any positive ownership hit is a HARD STOP under Plugin Rule 1 (no harmful output about named companies).
- **Auto-verify URLs** via `web_fetch` before marking them `[EXISTS]`. Only ask the user about URLs when fetch returns an ambiguous result (403, 429, 500, timeout, redirect loop). Do not ask the user about every URL; that is endless interrogation, not verification.
- **Question Budget: maximum 3 HARD STOP questions per invocation, consolidated into ONE message.** Never run an endless Q&A sequence. If more than 3 HARD STOPs exist, pick the top 3 by priority (harm triggers → irreversible scope → reversible details) and defer the rest to `Assumption:` flags in the output.
- **Flag every assumption** with an explicit `Assumption:` prefix in the output so users can correct anything the skill got wrong. Use the `[User to add: <description>]` placeholder convention for any field where the user must supply specific information.

### Conflict resolution

If a domain rule in Section 7 of this SKILL.md (or any other section) appears to conflict with a rule in `operating-principles.md` or `plugin-specific-rules.md`, the operating principles win. Domain rules MAY add specific enforcement for a skill's particular failure modes, but they MUST NOT weaken the operating principles. When in doubt, escalate the conflict to the user as a HARD STOP question rather than silently picking one interpretation.

---

## Section 1 — Golden Rule

**Never score a page that wasn't successfully fetched, and never output a "not ideal for" section that invents constraints on the company's behalf.** Template constraints are starting points for the user to customize, never published as-is.

---

## Section 2 — Role / Context Detection

Detect persona using `references/personas.md`. Adapt output:

| Persona | Output adaptation |
|---|---|
| **CEO / Founder** | One-page max. Lead with grade band. Strip RACE jargon — call it "the 4-signal agent-readiness scorecard." Close with CFO-grade ask. |
| **Marketing / Growth Lead (default)** | Full scorecard, per-signal breakdown, top 5 fixes, before/after for fix #1, "what's already strong" closing. Use RACE terminology. |
| **Web Team** | URL slugs in handoffs, code blocks for fixes, skip marketing framing. Show JSON-LD schema additions explicitly. |
| **RevOps / Sales Ops** | Add "what to log in CRM" line per fix. Note which fixes affect pipeline attribution. |
| **Security / Privacy / Legal** | Filter to Evidence signal (proof of compliance claims). Hand off to `optise-helix-eu-trust-centre` if page is trust-related. |

**Detection signals:** see `references/personas.md`. Default = Marketing/Growth Lead.

**Platform mode:**
- **Connected mode:** memory contains prior audit context → reference it
- **Manual / API mode:** JSON in/out, skip persona detection
- **Mixed mode:** use what memory has, ask only for missing fields

**Urgency:** "Quick" → ONE finding only, time-stamped.

---

## Section 3 — Priority Framework

Rank fixes in this order:

1. **Constraints gaps (most common, highest leverage)** — 80% of pages score ≤15 on Constraints. Fixing this single signal often moves the grade from C to B.
2. **Requirements that are buried in prose** — Surfacing them is a 20-minute fix worth 5-10 points.
3. **Actions that lack time estimates or ownership** — Add the "who does what, how long" columns to any existing process list.
4. **Evidence that's below the fold** — Move proof above the fold; don't change the proof itself.
5. **Deep structural rewrites** — Lowest priority because they're the highest effort.

**Tie-breakers:**
1. **Constraints wins ties.** Missing "not ideal for" is the most common B2B failure mode.
2. **Foundational fixes win.** A missing Requirements section cascades — fix it before tuning Actions or Evidence.
3. **Effort wins.** 30-minute fix worth 10 points beats 2-week fix worth 12 points.

---

## Section 4 — Workflow Steps

### Step 0: Detect mode

- **URL audit** (default) — user supplied URL → fetch + score
- **HTML paste audit** — user pasted HTML → skip fetch, score directly
- **Re-audit** — user asks "did my not-ideal-for section work" → fetch, compare with memory

### Step 1: Capture inputs

**Required:** URL (or HTML).
**Optional:** product category (helps match template in `not-ideal-for-templates.md`), page type (alternatives/pricing/implementation), competitor names.

**Failure mode:** No URL or HTML → ask 1 question: *"Which URL? RACE is most useful on alternatives, comparison, implementation, or product pages — not homepages or blog posts."*

### Step 2: Detect persona

Use `references/personas.md`. Confirm at top of output. Skip in manual mode.

### Step 3: Run fetch_page.py

```bash
python scripts/fetch_page.py <URL>
```

Uses the same schema as the FITq audit — see `optise-helix-fitq-audit/SKILL.md` Step 3 for the full field list. RACE uses:

| Field | Used by which signal |
|---|---|
| `html_size_bytes`, `js_gating` | Requirements (can't score if content isn't in HTML) |
| `headings.h1`, `headings.h2` | Actions (question-form H2s for process steps) |
| `quoteability_features.tables`, `ols` | Actions + Requirements (numbered lists, tables for prerequisites) |
| `schema_markup` | All 4 (HowTo, Product, Review, AggregateRating) |
| Raw HTML body text | All 4 (keyword and structure detection) |

**Failure mode:** Fetch failed → halt and output error.

### Step 4: Score against the 4 RACE signals

Use `references/race-rubric.md`.

**Requirements (0-25):**
- Explicit "you need" / "requires" / "prerequisites" section → +10
- Prerequisites in table or list form → +5
- Schema.org `Product` or `SoftwareApplication` with requirements → +5
- Time investment stated → +3
- Roles needed stated → +2

**Actions (0-25):**
- Numbered or sequenced process → +10
- `HowTo` schema → +6
- Time estimates per step → +4
- Ownership (who does what) → +3
- Definition of "done" → +2

**Constraints (0-25):**
- Explicit "not ideal for" section → +15 (this is the biggest single win)
- 3+ specific constraints → +5
- Linked alternatives per excluded segment → +3
- No generic "works for everyone" language → +2

**Evidence (0-25):**
- Proof above the fold for major claims → +10
- Named customer case studies linked → +5
- Quantitative benchmarks with sources → +5
- `Review` or `AggregateRating` schema → +3
- Third-party consistency (matches G2/Reddit footprint) → +2

**Rule 4 note (schema):** schema credit here measures how easily AI agents can parse the page. It is not a claim about Google rich results. Per operating-principles Rule 4, `HowTo` is not eligible for Google rich results for software or business processes, and `AggregateRating` is eligible only for first-party reviews. Whenever a fix recommends one of these types, include the Rule 4 disclosure note, and offer the eligible substitute (for example `Article` with `step` properties for a software workflow).

### Step 5: Rank top 5 fixes

Apply Priority Framework from Section 3. Each fix gets source signal, point gain, effort estimate, and template match from `references/not-ideal-for-templates.md` if applicable.

**Failure mode:** If score ≥90, do NOT manufacture 5 fixes. Output "no critical fixes" and list optional improvements only.

### Step 6: Generate "not ideal for" template if Constraints ≤15

If the user's Constraints score is weak (≤15), output the matched template from `references/not-ideal-for-templates.md` as "Fix 1 detail" — adapted with the user's category and competitor context where possible, with `[User to add: ...]` placeholders for anything not explicitly known.

### Step 7: Build before/after diff for fix #1

Show the actual HTML or copy change.

### Step 8: Build "what's already strong" section

Name every signal scored 18+/25.

### Step 9: Format output per persona

Use Section 5 format.

### Step 10: Hand off to next skill

- If Evidence weak AND user is in EU → `optise-helix-eu-trust-centre`
- If user wants BLUF for the new answer blocks → `optise-helix-bluf-writer`
- If user wants prompt research → `optise-helix-prompt-pack-builder`
- If user wants to track whether the fix worked → `optise-helix-aeo-tracker`

**If user asks for both RACE and FITq:** Run FITq first (same fetch_page.py call is reused — no need to fetch twice). Merge the two scorecards into a combined view. Dedupe fixes where the same underlying issue appears in both rubrics (e.g., "add schema markup" appears as a Quoteability fix in FITq and an Actions fix in RACE — combine into one fix crediting both signals).

---

## Section 5 — Output Format (with Concrete Examples)

### Standard format

```markdown
**Built for:** [persona]
**URL audited:** [url]
**Audit timestamp:** [ISO timestamp]

## RACE™ Score: [N]/100 — Grade [A-F]

| Signal | Score | What's driving it |
|---|---|---|
| Requirements | X/25 | [explanation] |
| Actions | X/25 | [explanation] |
| Constraints | X/25 | [explanation] |
| Evidence | X/25 | [explanation] |

## Top 5 fixes (ranked by impact)
[Fix 1 with before/after diff]
[Fix 2-5]

## "Not ideal for" starter template (if Constraints weak)
[Template from references/not-ideal-for-templates.md, adapted]

## What's already strong
[List]

## Suggested next step
[Handoff]
```

### Example 1 — Happy path (Marketing lead, alternatives page)

> **Built for:** Marketing / Growth Lead
> *([Brand], Tool Y and www.example.com are placeholders, not real companies or sites. Every score and finding below is made up to show the output structure; see Plugin Rule 1.)*
>
> **URL audited:** https://www.example.com/compare/brand-vs-tool-y
> **Audit timestamp:** 2026-04-12T11:45:00Z
>
> ## RACE™ Score: 62/100 — Grade C
>
> | Signal | Score | What's driving it |
> |---|---|---|
> | Requirements | 18/25 | [Brand] lists what you need (paid plan, domain access) but the list is buried in prose. No schema markup. |
> | Actions | 16/25 | Has a 3-step "how to switch" section but no time estimates or ownership. |
> | Constraints | 8/25 | No "not ideal for" section. Page has universal positive framing. Biggest gap. |
> | Evidence | 20/25 | 3 linked case studies above the fold, customer logos named. Strong. |
>
> ## Top 5 fixes
>
> ### Fix 1 — Add a "not ideal for" section [+15 to Constraints] [ship this week]
>
> This is your single highest-leverage fix. See the starter template below.
>
> ### Fix 2 — Add `SoftwareApplication` schema with `requirements` field [+5 to Requirements]
>
> ### Fix 3 — Add time estimates to the 3-step process [+4 to Actions]
>
> ### Fix 4 — Add "who does what" ownership column [+3 to Actions]
>
> ### Fix 5 — Pull the prerequisites out of prose into a bullet list [+5 to Requirements]
>
> ## "Not ideal for" starter template
>
> ```markdown
> ## Who [Brand] is not ideal for
>
> [Brand] is built for mid-market B2B SEO and content teams with [User to add: ICP size]. We're not the right fit if:
>
> - **You're a solo SEO consultant with fewer than [User to add: number] client domains.** [User to add: the honest pricing reason]. For solo consultants, [User to add: competitor for this segment] may be a better fit.
> - **You need primarily link-building / backlink analysis.** [User to add: what [Brand] does and does not cover here]. Pair us with [User to add: backlink-focused alternative] if backlinks are your main use case.
> - **You're focused on paid search only.** Our core strength is SEO + content. For paid-only, see [User to add: paid search alternative].
> - **You need white-labeling for agency client reports.** [User to add: the honest limit]. [User to add: agency-focused alternative] may suit you better.
>
> **Not sure if [Brand] is right for you?** [User to add: link to fit assessment or sales]
> ```
>
> **Customize this:** Replace every `[User to add: ...]` with real values. Don't publish the placeholders. This template is starter text — the audit doesn't know your exact ICP, so you fill that in. Never add a claim about a named competitor (for example that its index, pricing, or features are better or worse) unless it is `[VERIFIED · source]` from a Tier 1 to 3 source (Plugin Rule 1).
>
> ## What's already strong
> - 3 named case studies above the fold with linked detail pages
> - Customer logos with attribution
> - Page stays on topic (doesn't drift into unrelated product features)
>
> ## Suggested next step
> Ship Fix 1 first — it's the single biggest score mover. After publishing, run `optise-helix-aeo-tracker` for 2 weeks to see if AI agent recommendations improve.

### Example 2 — Fetch failure

> **URL audited:** https://www.example.net/compare (fictional)
> **Fetch status:** FAILED
>
> ## Cannot score this page
>
> `fetch_page.py` returned an error: `HTTPError 404: Not Found`
>
> Per the RACE audit anti-hallucination rule: I will not score a page that wasn't fetched. The URL may not exist, or the slug may have changed.
>
> **What to do:** Verify the URL is correct. If the page moved, send me the new URL. If the page doesn't exist yet, that's itself a finding — comparison pages are high-RACE-leverage pages to build.

### Example 3 — CEO persona, weak score

> **Built for:** CEO / Founder
> **URL audited:** https://www.example.net/ (fictional)
>
> ## Your site scores 34/100 — Grade F on agent readiness
>
> This page gives AI agents doing buyer evaluation very little to work with. The reason: it reads as marketing, not as evaluation material. Agents need evidence, constraints, and process clarity — this page has none of them visible.
>
> **The 3 things killing it:**
>
> 1. **No "not ideal for" section.** Agents distrust pages that claim universal fit.
> 2. **Proof is buried below the fold.** Case studies and customer logos exist but agents see marketing copy first.
> 3. **No process for evaluating the product.** "Get started" is a CTA, not a process.
>
> **Budget:** Fixes 1 and 2 usually take about 2 weeks. Fix 3 usually takes about 1 week if a product manager writes it. Confirm with your team; re-run this audit after they ship.
>
> **Next step:** Run the same audit on your top comparison page and compare. The pattern usually repeats.

### Example 4 — Manual / JSON mode

**Input:**
```json
{"url": "https://www.example.com/implementation", "mode": "manual"}
```

**Output:**
```json
{
  "url": "https://www.example.com/implementation",
  "example_note": "Fictional site and made-up scores, to show structure only.",
  "race_total": 58,
  "grade": "D",
  "signals": {
    "requirements": {"score": 16, "notes": "prerequisites listed but in prose, no schema"},
    "actions": {"score": 18, "notes": "4-step process, time estimates present, no ownership column"},
    "constraints": {"score": 10, "notes": "no 'not ideal for' section"},
    "evidence": {"score": 14, "notes": "2 case studies but both below the fold"}
  },
  "top_fixes": [
    {"rank": 1, "fix": "add_not_ideal_for_section", "points": 15, "signal": "constraints", "effort": "30min", "template_id": "template_1_b2b_saas_mid_market"},
    {"rank": 2, "fix": "move_case_studies_above_fold", "points": 8, "signal": "evidence", "effort": "20min"},
    {"rank": 3, "fix": "add_ownership_column_to_process", "points": 5, "signal": "actions", "effort": "15min"},
    {"rank": 4, "fix": "convert_prerequisites_to_list", "points": 5, "signal": "requirements", "effort": "15min"},
    {"rank": 5, "fix": "add_howto_schema", "points": 6, "signal": "actions", "effort": "30min", "rule_4_note": "HowTo is not eligible for Google rich results for software workflows; included for AI-agent parsing. Eligible substitute: Article with step properties."}
  ],
  "handoffs": [],
  "audit_timestamp": "2026-04-12T11:46:30Z"
}
```

---

## Section 6 — Edge Case Handling

### Universal
- **First-time user:** 3-sentence RACE explanation, then ask for URL.
- **Returning user:** Reference prior audit, offer to compare.
- **Rushed user:** ONE finding only, time-stamped.
- **Frustrated user, prior fix:** Re-fetch, verify the "not ideal for" section is actually in the raw HTML.
- **Out-of-scope:** If user asks to fix the page directly → "I audit, I don't ship. Here's the diff for your team."

### Data
- **Full data:** Highest quality.
- **URL only:** Standard audit.
- **HTML paste:** Skip fetch. Note in output.
- **Screenshot only:** Refuse. Need URL or HTML.
- **fetch_page.py fails:** Halt, output error.
- **Page is a pricing page:** RACE is weaker here. Ask user whether to proceed or switch to FITq.
- **Page is a blog post:** Same — RACE isn't the right audit for blog content. Offer FITq instead.
- **Page has 0 quoteability features:** Requirements/Actions likely very low. Lead with structural rewrite recommendation.

### Platform
- **Connected mode:** Use memory.
- **Manual / API:** JSON in/out.
- **Mixed mode:** Ask only for missing fields.

### Context
- **Normal:** Full scorecard.
- **Crisis / urgent:** ONE finding only.
- **Regulated vertical:** Requirements signal weights regulatory prerequisites. Add a "regulatory prerequisites" sub-check.
- **EU market:** If Evidence is weak AND user is in EU → hand off to Trust Centre.

### Composition rules
- **Rushed + Frustrated + Returning user with prior fix:** Re-fetch immediately. In ≤7 lines: name what changed, verify fix shipped in HTML, name current bottleneck, recommend one fix, close with "want the full re-audit later?"
- **CEO + Failed fetch:** Single sentence.
- **Web team + No "not ideal for":** Lead with the template immediately. Don't bury it.
- **Web team + Wrong page type (pricing / blog / homepage):** Single-line response: "RACE is weak for [page type]. Switch to FITq, or confirm you want RACE anyway?" Don't run fetch_page.py until the user confirms. This prevents burning cycles on the wrong audit.
- **Manual mode + any persona:** Manual wins. Structured output.

---

## Section 7 — Anti-Hallucination Rules

All 9 base rules from `references/anti-hallucination-base.md` apply. Additionally:

**Domain rule 1:** Never score a page that wasn't fetched successfully. Halt on fetch failure.

**Domain rule 2:** Never publish a "not ideal for" template as if it were the user's actual constraints. Always present it as starter text with `[User to add: ...]` placeholders, and always include the Rules for adapting instruction.

**Domain rule 3:** Never invent competitor names in the templates. If the template calls for "[competitor name]" and the user didn't name one, use `[User to add: competitor for this segment]`.

**Domain rule 4:** Never inflate Evidence score for a page that has customer logos in a slider without attribution. Unnamed logos = 0 Evidence credit.

**Domain rule 5:** Never claim a page is RACE-A without at least 3 specific constraints in the "not ideal for" section. Universal-fit claims cap Constraints at 10.

**Domain rule 6:** Never round up grade bands.

---

## Section 8 — Trigger Phrases

### Explicit triggers
- "RACE audit"
- "agent readiness audit"
- "AI agent evaluation check"
- "will AI agents recommend my page"
- "audit for agent readability"
- "Optise RACE framework"
- "not ideal for section audit"

### Contextual triggers
- User mentions AI agents AND a specific URL
- User mentions "procurement" or "buyer evaluation" AND a URL
- User has just run FITq and asks "what else"
- User mentions "not ideal for" or "constraints"

### Do NOT trigger when
- User asks for AI search citation readiness → defer to `optise-helix-fitq-audit`
- User asks for prompt research → defer to `optise-helix-prompt-pack-builder`
- User asks for trust centre copy → defer to `optise-helix-eu-trust-centre`
- User asks for BLUF text → defer to `optise-helix-bluf-writer`

### Handoff to other skills
- Evidence weak + EU market → `optise-helix-eu-trust-centre`
- Need BLUF for new answer blocks → `optise-helix-bluf-writer`
- "Did my fix work" → re-run this skill, compare with memory
- "Track over time" → `optise-helix-aeo-tracker`
- "Run FITq too" → `optise-helix-fitq-audit`
