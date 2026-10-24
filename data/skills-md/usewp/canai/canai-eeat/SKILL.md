---
name: canai-eeat
description: >
  Audit WordPress articles, pages, and local drafts for people-first usefulness,
  E-E-A-T evidence, creator and process transparency, and search-engine-first warning signs
  using Google Search Central guidance. Use for E-E-A-T reviews, helpful-content audits,
  content quality reviews, and pre-publication checks. Does not predict rankings or replace
  qualified review of medical, financial, legal, or safety advice.
metadata:
  author: canai
  version: "1.0.0"
allowed-tools: "Read Write Edit Grep Glob"
---

# CanAI E-E-A-T Review

Evaluate the supplied content as an evidence-led editorial review. The goal is a more useful,
accurate, transparent page for its intended reader—not a score engineered for search engines.

Read [references/google-search-guidance.md](references/google-search-guidance.md) before an audit.
It records the primary-source basis, important qualifications, and the questions to apply.

## Boundaries

- Do not promise rankings, traffic, indexing, or immunity from search updates. E-E-A-T is a
  framework represented by a mix of signals, not a single ranking factor.
- Do not infer first-hand experience, qualifications, testing, human review, sources, or AI use.
  Mark missing evidence as **Not demonstrated** and ask for the real artifact or fact needed.
- Do not manufacture a byline, bio, disclosure, quotation, citation, benchmark, screenshot, or
  methodology. Suggested copy must contain explicit placeholders for facts only the owner knows.
- Treat medical, financial, legal, safety, and similarly consequential topics as YMYL. Flag claims
  needing current primary sources and qualified human review; do not present the audit as expert
  validation.
- AI disclosure is contextual. Recommend it when readers would reasonably ask how the content was
  created, or when a platform or product policy requires it—not as a universal Google requirement.
- Audit by default. Edit local files or write back to WordPress only when the user asks for
  remediation or publication. Preserve the requested status; never turn a draft into a published
  post implicitly.

## Acquire the content

Use the source the user supplied:

- **Local draft:** read the complete file and identify any adjacent author, About, methodology, or
  source material the user placed in scope.
- **CanAI Twig page/template:** use the configured CanAI MCP server. Resolve the id with
  `wpcanai-list-pages`, `wpcanai-list-templates`, or `wpcanai-resolve-content-id`, then fetch the
  relevant fields with `wpcanai-read-meta`. `wpcanai-grep-content` is useful for site-wide searches
  across `_canai_html`, `_canai_css`, and `_canai_js`; it does not search native blog-post bodies.
- **Native WordPress post or blocks page:** use a host-provided read tool if one exists. Otherwise
  ask for the body or export; `wpcanai-write-post` and `wpcanai-write-page` are write tools, not read
  tools, and `wpcanai-read-meta` is not a general post-content reader.
- **Pasted text or URL:** audit the supplied text, or retrieve the page through an available
  read/browser tool. State which surrounding evidence (byline, author page, citations, page
  experience) was and was not observable.

Do not use WP-CLI, raw REST, direct database access, or local `wp-content` edits as a substitute for
the CanAI MCP server. If the configured MCP connection is unavailable, report the missing access.

Before judging, state the page's apparent purpose, intended audience, and whether it is YMYL. If
purpose or audience is unclear, make a labeled tentative inference rather than blocking the audit.

## Audit method

Review claims in context and cite short excerpts or section names as evidence. Separate what the
page demonstrates from facts that require external verification.

1. **Reader outcome and originality**
   - Does the page satisfy the likely task without padding or forcing another search?
   - What original reporting, analysis, examples, data, or practical synthesis does it add?
   - Is the title descriptive and proportionate to what the page actually delivers?
2. **Who, How, and Why**
   - Who created or reviewed it, and can readers reach relevant background where expected?
   - How were claims, tests, comparisons, images, or recommendations produced and checked?
   - Is automation context useful to readers, and is the people-first purpose credible?
3. **E-E-A-T evidence**
   - **Experience:** observable first-hand work and concrete artifacts.
   - **Expertise:** accurate depth, limitations, edge cases, and appropriate terminology.
   - **Authoritativeness:** attributable authorship and relevant, preferably primary, sources.
   - **Trust:** factual support, transparency, corrections, conflicts, and calibrated claims.
4. **Search-engine-first warning signs**
   - Thin synthesis, mass-produced feel, arbitrary length, unrelated trend chasing, exaggerated
     certainty, fake freshness, or a title that promises an unavailable answer.
5. **Page-level quality visible in scope**
   - Readability, structure, spelling, accessibility cues, intrusive elements, and metadata accuracy.
   - Label performance, mobile behavior, and structured-data validity **Not checked** unless they
     were actually tested.

Use **Demonstrated**, **Partially demonstrated**, **Not demonstrated**, or **Not assessable** for
each area. These are evidence labels, not numerical SEO scores.

## Report

Return this compact structure:

```markdown
# People-First & E-E-A-T Audit: [title]

**Source:** [file, URL, or WordPress id]
**Audience / purpose:** [observed or inferred]
**YMYL:** [No / Yes—topic and review needed]
**Overall:** [Strong / Mixed / At risk] — [one-sentence rationale]
**Scope limits:** [what could not be inspected or verified]

## Evidence summary
| Area | Assessment | Evidence |
|---|---|---|
| Reader value and originality | ... | ... |
| Who / authorship | ... | ... |
| How / process | ... | ... |
| Why / people-first purpose | ... | ... |
| Experience | ... | ... |
| Expertise | ... | ... |
| Authoritativeness | ... | ... |
| Trust | ... | ... |

## Findings
### Keep
- [specific strength and evidence]

### Fix first
- **[finding]:** [evidence]
  - Impact: [reader or trust consequence]
  - Fix: [concrete, checkable action]
  - Needs from owner: [real fact/artifact/approval, or "Nothing"]

### Improve next
- [lower-priority improvement]

## Verification queue
- [claim] — [source or qualified reviewer needed]

## Action checklist
- [ ] [ordered remediation]
```

Quote only enough of the content to locate a finding. If there are no verification items, say so.
Do not inflate the report to fill every section; write `Not assessable` when evidence is absent.

## Remediation

When the user asks to apply fixes:

1. Confirm every owner-only fact or leave an unmistakable placeholder; never turn a suggestion into
   an asserted fact.
2. Preserve voice, intent, links, block structure, and publication status unless the user requests a
   change. Favor precise additions and deletions over generic expansion.
3. For a local draft, edit the source file and re-read the result.
4. For CanAI Twig meta, re-read immediately before writing and use `expected_hash` with
   `wpcanai-write-meta`; use `wpcanai-replace-in-meta` for safe literal replacements.
5. For native posts or block pages, write only when the complete replacement block list is available.
   `wpcanai-write-post` and `wpcanai-write-page` replace the entire body when `blocks` is sent.
6. Keep drafts as drafts unless publication was explicit. Re-fetch or preview the result with an
   available read/browser tool, then summarize exactly what changed and what still needs a human.

An audit is complete when every material conclusion points to observable evidence, every weakness
has a concrete remedy, unsupported claims are queued for verification, and no experience or
authority has been invented.
