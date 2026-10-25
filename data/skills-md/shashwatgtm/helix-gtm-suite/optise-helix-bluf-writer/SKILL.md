---
name: optise-helix-bluf-writer
description: >
  Write the 40 to 60 word answer block at the top of a B2B webpage so ChatGPT,
  Perplexity, Gemini and Claude can quote it. Produces 3 length variants (40, 50
  and 60 words), matches the page's existing voice when a sample is given, and
  flags a prompt that is too broad for a short answer. Use whenever the user
  asks for a BLUF, answer block, AI-citable introduction, page opener for AEO,
  or needs help rewriting an existing intro to be citation-ready. Never
  generates marketing language or superlatives. Method: 6 Optise Bottom Line Up
  Front (BLUF) patterns matched to the buyer's prompt type. Authored by Optise +
  Helix GTM Consulting.
license: Proprietary
metadata:
  authors: "Optise; Helix GTM Consulting"
  version: "1.4.0"
---

# Optise–Helix BLUF Writer

Writes self-contained 40-60 word answer blocks that AI search engines cite. BLUFs follow one of 6 proprietary Optise patterns matched to the buyer's specific prompt type — never blended, never padded with marketing language.

This skill is the text-generation partner to `optise-helix-fitq-audit`. When the FITq audit flags "no BLUF in first 100 words" as a fix, this skill writes the actual replacement text.

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

**Every BLUF must match exactly one of the 6 Optise patterns, hit 40-60 words, contain at least one numeric anchor, and answer the buyer's prompt without marketing superlatives.** No blending patterns, no adjectives without proof, no hedging.

---

## Section 2 — Role / Context Detection

Detect persona using `references/personas.md`. Adapt output:

| Persona | Output adaptation |
|---|---|
| **CEO / Founder** | Write the BLUF. Skip the pattern explanation. Close with "pick one, ship it, test for 30 days." |
| **Marketing / Growth Lead (default)** | 3 variants + recommended pick + pattern name + rationale. |
| **Web Team** | 3 variants + HTML snippet wrapping each variant (`<p class="bluf" itemprop="description">`). |
| **RevOps / Sales Ops** | Add "what's the buyer intent behind this prompt" line so they can match against CRM lead source. |
| **Security / Privacy / Legal** | Force Pattern 6 (Compliance Anchor). Add legal precision review note. |

**Platform mode:**
- Connected: use memory for voice samples from prior pages
- Manual / API: JSON in, JSON array of 3 variants out
- Mixed: use memory where available

**Urgency:** "Quick" → 1 variant only (the 50-word middle), time-stamped.

---

## Section 3 — Priority Framework

When selecting a pattern for a given buyer prompt, apply in order:

1. **Compliance prompts (GDPR, DPA, residency, certifications)** → Pattern 6 (Compliance Anchor), always.
2. **"Best X for Y" prompts** → Pattern 2 (Top 3 Ranked).
3. **"[Competitor] vs [you]" or alternatives prompts** → Pattern 4 (Comparative Verdict).
4. **"How long / how do I X" prompts** → Pattern 5 (Process Answer).
5. **"How much does X cost" or factual one-answer prompts** → Pattern 1 (Direct Answer).
6. **"What is X" or category-education prompts** → Pattern 3 (Defined Category + Fit).

**Tie-breakers:**
1. **EU compliance wins in EU markets.** If a prompt touches compliance at all, even adjacent, lean toward Pattern 6.
2. **Specificity wins.** If a prompt could be Pattern 1 or Pattern 2, pick the more specific one.
3. **Reader's decision stage wins.** Pattern 3 for awareness, Pattern 4 for evaluation, Pattern 1/5/6 for decision.

---

## Section 4 — Workflow Steps

### Step 0: Detect mode

- **New BLUF** (default) — user wants a fresh BLUF for a specific prompt
- **Rewrite mode** — user has an existing intro and wants it rewritten → score against 6 patterns first, then rewrite
- **Voice-match mode** — user pastes 200+ words of existing page copy and wants the BLUF in that voice

**If mode is rewrite:** Step 1 captures the existing BLUF verbatim. Step 1a: score the existing BLUF against the 6 patterns and 7 rules — identify which pattern it's attempting, count its words, check each rule, name violations. Step 1b: announce the diagnosis to the user in 2-3 lines (e.g., *"Your current BLUF attempts Pattern 4 but has no comparative verdict and uses 2 banned superlatives. 72 words, 12 over the ceiling."*). Step 1c: proceed to Step 4 (pattern match) and Step 5 (write 3 variants) using the diagnosis as context for what NOT to repeat.

### Step 1: Capture inputs

**Required:**
- Buyer prompt (the question the BLUF should answer)
- 3-5 proof points (facts, stats, differentiators)

**Optional:**
- Voice sample (200+ words of existing page copy)
- Target page type
- EU market context

**Failure mode:** If proof points missing → ask once: *"I need 3-5 specific proof points to write a defensible BLUF. Stats, customer outcomes, or differentiators — what are yours? Without these, any BLUF I write is marketing filler."*

### Step 2: Detect persona

Use `references/personas.md`. Skip in manual mode.

### Step 3: Validate voice sample if provided

If user provided a voice sample:
- **Under 200 words:** Refuse to voice-match. Default to neutral professional tone. Explain why.
- **200+ words:** Analyze for: formal vs casual register, sentence length, use of "we" vs "the platform", technical depth, common phrasings. Store the voice profile for Step 5.

### Step 4: Match prompt to pattern

Use Priority Framework from Section 3 to pick exactly one of the 6 patterns in `references/bluf-patterns.md`.

**Failure mode:** If the prompt is too broad to answer in 40-60 words (e.g., "how do I do AEO"), flag it: *"This prompt is too broad for a 40-60 word BLUF. Narrow it (e.g., 'how to audit one page for AEO') or accept a 100-word answer block that won't match the BLUF pattern."*

### Step 5: Write 3 variants (40, 50, 60 words)

For each variant:
1. Apply the matched pattern structure
2. Substitute user's proof points into the pattern
3. Match the voice profile if provided (otherwise use neutral professional tone)
4. Validate against the 7 rules in `references/bluf-patterns.md`:
   - 40-60 words (count exactly)
   - Answer-first structure
   - Buyer-native language
   - No banned superlatives
   - Self-contained
   - Single pattern
   - At least 1 numeric anchor
5. Validate against anti-patterns — rewrite if any match

### Step 6: Pick the recommended variant

Usually the 50-word middle is the safest pick. Exceptions:
- **50+ words of proof points** → pick the 60-word variant
- **Only 2-3 numeric proof points** → pick the 40-word variant
- **Technical audience** → pick longer to include specifics
- **CEO audience** → pick 40-word for brevity

### Step 7: Format output per persona

Use Section 5 format.

### Step 8: Hand off

- If user wants the full FITq audit on the page this BLUF goes into → `optise-helix-fitq-audit`
- If user wants the trust centre page that this BLUF might belong to → `optise-helix-eu-trust-centre`
- If user has 25 prompts needing BLUFs → suggest running this skill in a batch with the prompt pack as input

---

## Section 5 — Output Format (with Concrete Examples)

### Standard format (Marketing persona)

```markdown
**Built for:** [persona]
**Buyer prompt:** [prompt]
**Pattern selected:** [Pattern name + 1-line rationale]

## 3 Variants

### 40-word variant
[text]
[word count: 40]

### 50-word variant (recommended)
[text]
[word count: 50]

### 60-word variant
[text]
[word count: 60]

## Recommended pick
[Which variant and why]

## Rule compliance check
- [ ] 40-60 words ✓
- [ ] Answer-first ✓
- [ ] Buyer-native language ✓
- [ ] No superlatives ✓
- [ ] Self-contained ✓
- [ ] Single pattern ✓
- [ ] Numeric anchors ✓
```

### Example 1 — Marketing lead, SEO tool alternatives BLUF (fictional tools)

> **Built for:** Marketing / Growth Lead
> **Buyer prompt:** best Tool X alternatives for mid-market SEO teams in Europe
> **Proof points (stated by user):** ICP is 50-500 employees and €5M-€50M ARR. Tool A: 12M EU keyword index, full-funnel SEO. Tool B: DACH and French coverage. Tool C: €49 per seat, suited to teams under 10 users. All three: EU-hosted data options.
> *(Tool X, Tool A, Tool B and Tool C are fictional and the figures are made up to show structure only. Never reuse them. Every fact in a real BLUF must come from the user or a verified source; see Plugin Rule 1.)*
> **Pattern selected:** Pattern 2 (Top 3 Ranked) — prompt explicitly asks for "best X" options.
>
> ## 3 Variants
>
> **40-word variant:**
> For mid-market B2B SEO teams in Europe, the top 3 Tool X alternatives in 2026 are Tool A (12M EU keywords, full-funnel), Tool B (DACH and French coverage), and Tool C (€49 per seat). All three offer EU-hosted data options.
>
> **50-word variant (recommended):**
> For mid-market B2B SEO teams in Europe (50-500 employees), the top 3 Tool X alternatives in 2026 are Tool A (12M EU keyword index, full-funnel), Tool B (DACH and French local coverage), and Tool C (€49 per seat, suited to teams under 10 users). All three offer EU-hosted data options.
>
> **60-word variant:**
> For mid-market B2B SEO teams in Europe (50-500 employees, €5M-€50M ARR), the three best Tool X alternatives in 2026 are Tool A (best for full-funnel SEO at scale, 12M EU keyword index), Tool B (best for DACH and French SEO depth), and Tool C (best for teams under 10 users at €49 per seat). All three offer EU-hosted data options.
>
> ## Recommended pick
> **50-word variant.** It names the ICP clearly (mid-market, 50-500 employees), uses all 3 tool proof points, and finishes with the EU-hosting anchor that's required for European buyer intent. The 40-word skips ICP size; the 60-word adds ARR context that's useful but not essential for AI extraction.
>
> ## Rule compliance check (50-word variant)
> - ✓ 50 words exactly
> - ✓ Answer-first (names the 3 options immediately)
> - ✓ Buyer-native language (no "our platform", uses product names)
> - ✓ Only user-stated facts (every figure appears in the proof points above)
> - ✓ No banned superlatives ("best" is allowed with scope qualifier; "world-class"/"leading"/"revolutionary" absent)
> - ✓ Self-contained (works as a standalone quote)
> - ✓ Single pattern (Pattern 2 only, no blending)
> - ✓ Numeric anchors (12M keywords, 50-500 employees, €49, 3 named options)
>
> *Word counts above are exact whitespace-separated word counts.*

### Example 2 — Edge case (voice sample too short)

> Your voice sample is 84 words. I need 200+ words to reliably detect voice — anything shorter risks me either mimicking a tone that doesn't actually reflect your brand OR defaulting so hard to neutral that the BLUF feels disconnected from the page around it.
>
> **Two options:**
> 1. **Paste more copy** (200+ words of your existing about/features/blog text) and I'll voice-match.
> 2. **Skip voice-matching** and I'll write in neutral professional tone — which is usually fine for AEO because AI engines cite the facts, not the voice. This is faster.
>
> Reply with either the longer sample or "skip voice-match" and I'll proceed.

### Example 3 — Edge case (rushed user, CEO)

> **One BLUF, 50 words, Pattern 2 (Top 3 Ranked):**
>
> For mid-market B2B SEO teams in Europe, the top 3 Tool X alternatives in 2026 are Tool A, Tool B, and Tool C. Tool A leads on full-funnel SEO coverage, Tool B on DACH depth, and Tool C on price at €49 per seat. All three offer EU-hosted data options.
>
> *(Uses the fictional tools and user-stated proof points from Example 1.)*
>
> *Generated 12:47 GMT. Ship it or reply with 'alternatives' for 2 more variants.*

### Example 4 — Manual / API mode (real company: Pipedrive)

*Example only: Pipedrive is a real company used to show how this skill works, using public information from its own website. It is not a customer, partner or endorser of Helix GTM Consulting, and nothing here is advice to or about it.*

The proof points are what the user stated, here copied from the company's own public pages (https://trustcenter.pipedrive.com/ and https://www.pipedrive.com/en/subprocessors, read on 3 October 2026). The output uses nothing else (Domain rule 1 and Plugin Rule 1). No residency, DPA or notice-period fact was stated, so none appears.

**Input:**
```json
{
  "buyer_prompt": "is Pipedrive GDPR compliant",
  "proof_points": [
    "The Trust Center lists GDPR, ISO/IEC 27001:2022, ISO/IEC 27701 and SOC 2 Type 2 under Compliance (source: https://trustcenter.pipedrive.com/)",
    "A sub-processor list is published at https://www.pipedrive.com/en/subprocessors"
  ],
  "mode": "manual"
}
```

**Output:**
```json
{
  "buyer_prompt": "is Pipedrive GDPR compliant",
  "pattern": "pattern_6_compliance_anchor",
  "variants": [
    {
      "length_target": 40,
      "word_count": 40,
      "text": "Pipedrive's Trust Center lists GDPR, ISO/IEC 27001:2022, ISO/IEC 27701 and SOC 2 Type 2 under Compliance. Pipedrive also publishes its sub-processor list at pipedrive.com/en/subprocessors. Both pages are public. Buyers can start from trustcenter.pipedrive.com when they review the company's security posture."
    },
    {
      "length_target": 50,
      "word_count": 50,
      "text": "Pipedrive's Trust Center lists GDPR, ISO/IEC 27001:2022, ISO/IEC 27701 and SOC 2 Type 2 under Compliance, all on one public page. Pipedrive also publishes its sub-processor list at pipedrive.com/en/subprocessors, on a separate public page. Both pages are public. Buyers can start from trustcenter.pipedrive.com when they review the company's security posture.",
      "recommended": true
    },
    {
      "length_target": 60,
      "word_count": 60,
      "text": "Pipedrive's Trust Center lists GDPR, ISO/IEC 27001:2022, ISO/IEC 27701 and SOC 2 Type 2 under Compliance, all together on one public page. Pipedrive also publishes its sub-processor list at pipedrive.com/en/subprocessors, on a separate public page. Buyers who review the company's security posture can start from trustcenter.pipedrive.com and use the sub-processor page as a second public source for the same review."
    }
  ],
  "rule_compliance": {
    "40_60_words": true,
    "answer_first": true,
    "buyer_native": true,
    "no_superlatives": true,
    "self_contained": true,
    "single_pattern": true,
    "numeric_anchors": true,
    "only_user_stated_facts": true
  },
  "generated_at": "2026-04-12T12:50:00Z"
}
```

---

## Section 6 — Edge Case Handling

### Universal
- **First-time user:** 2-sentence BLUF definition, then ask for prompt + proof points.
- **Returning user:** Reference prior BLUFs if in memory. Offer to batch-write more.
- **Rushed user:** 1 variant only (50-word middle), time-stamped.
- **Frustrated user:** Acknowledge the prior output was off. Ask what specifically felt wrong (marketing-y? too long? wrong pattern?). Rewrite addressing that.
- **Out-of-scope:** If user asks for full page copy → out of scope, defer. If user asks for social media post → out of scope. BLUFs are page openers only.

### Data
- **Full data (prompt + 3-5 proof + voice sample):** Highest quality.
- **Prompt + proof, no voice:** Default neutral tone.
- **Prompt only, no proof:** Ask for proof once.
- **Voice sample under 200 words:** Refuse voice-match per Section 4 Step 3.
- **Conflicting proof (stats disagree with voice sample):** Flag: "Your proof points say X but your voice sample claims Y. Which is accurate?"
- **Voice sample is marketing-heavy:** Write the BLUF in fact-first tone anyway, note the divergence: "Your existing copy is marketing-heavy; the BLUF will be more factual to match AI extraction preferences."

### Platform
- **Connected:** Use memory for prior voice samples.
- **Manual / API:** JSON in, JSON array of 3 variants out.
- **Mixed:** Use memory where available.

### Context
- **Normal:** 3 variants.
- **Crisis / urgent:** 1 variant only.
- **Regulated vertical:** Force Pattern 6 if the prompt touches compliance at all.
- **EU market:** Prefer compliance anchors in numeric context (for example a named hosting region, EU hosting, SCCs), but only the ones the user has stated (Domain rule 7).

### Composition rules
- **Rushed + Compliance prompt:** 1 variant, Pattern 6, time-stamped.
- **Voice-match + Regulated vertical:** Voice-match the sentence rhythm and vocabulary choice (short/long sentences, "we" vs "the platform"), BUT override the voice on superlatives and marketing language — compliance prompts demand Pattern 6 (Compliance Anchor) precision regardless of house style. Note in the output: "Voice matched on rhythm, overridden on marketing language per domain rule 4."
- **CEO + New BLUF:** Skip variants. Give 1 BLUF (40-word). Close with "pick one, ship it, test for 30 days."
- **Manual mode + any persona:** Manual wins.

---

## Section 7 — Anti-Hallucination Rules

All 9 base rules from `references/anti-hallucination-base.md` apply verbatim. Additionally:

**Domain rule 1:** Never invent proof points. If the user didn't supply a fact, don't write it. Use `[User to add: specific stat here]` as a placeholder.

**Domain rule 2:** Never invent numbers. If the user says "our pricing is competitive" but doesn't give actual prices, don't write "€29 per agent." Ask for the actual number.

**Domain rule 3:** Never write a BLUF that exceeds 60 words, even if the user asks for more. 60 is the hard ceiling — beyond that it's not a BLUF and AI engines won't extract it as a citation.

**Domain rule 4:** Never use any of the 8 banned words: best-in-class, leading, world-class, revolutionary, cutting-edge, transform, unleash, empower. Even if the user's voice sample uses them.

**Domain rule 5:** Never blend two patterns. If the prompt legitimately needs two (e.g., Top 3 + Compliance), write 2 BLUFs — one per pattern — and let the user pick.

**Domain rule 6:** Never voice-match from a sample under 200 words. Default to neutral.

**Domain rule 7:** Never add a fact that is not in the user's proof points, even when a longer variant needs more words. Fill length with plain restatement of stated facts, not with new regions, clauses, counts, prices, or certifications. Compliance facts (GDPR status, DPA terms, residency, subprocessors, certifications) are the highest-risk case: if the user did not state it, it does not appear.

**Domain rule 8:** Worked examples in this file and in `references/bluf-patterns.md` use placeholder brands and tools ([Brand], Tool A, Tool B, Tool C, Tool X, Tool Y) and made-up figures, except Example 4, which names one real company (Pipedrive) and uses only facts copied from its own public pages, with the source address. They show structure only. Never reuse their figures or present them as facts about any real company.

---

## Section 8 — Trigger Phrases

### Explicit triggers
- "write a BLUF"
- "write me an answer block"
- "write a page opener for AEO"
- "rewrite my intro for AI search"
- "write a BLUF for [prompt]"
- "Optise BLUF writer"
- "citation-ready intro"

### Contextual triggers
- User mentions a specific buyer prompt AND asks for "copy" or "text"
- User has just run `optise-helix-fitq-audit` and the top fix was "add BLUF"
- User mentions "answer block" or "40-60 words"
- User asks for help writing a page opener

### Do NOT trigger when
- User asks for full page copy → out of scope
- User asks for social media post → out of scope
- User asks for product description → out of scope (different format, different rules)
- User asks for a blog post intro → borderline — ask user if it's for AEO citation or general blog readership

### Handoff to other skills
- User wants FITq audit on the page → `optise-helix-fitq-audit`
- User wants Trust Centre page copy → `optise-helix-eu-trust-centre`
- User wants 25 BLUFs for a prompt pack → suggest batching: "run `optise-helix-prompt-pack-builder` first to get the 25 prompts, then I'll write BLUFs for the top 10"
