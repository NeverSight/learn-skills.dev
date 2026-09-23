---
name: seo
description: >-
  Audit and improve website discoverability across traditional search, answer
  engines, and generative search. Use for technical SEO, on-page content,
  structured data, question and entity architecture, AI citations, crawler
  controls, agent-readable content, and reproducible visibility measurement.
  Do not use for only copy-editing, writing, CMS operations, or generic AI
  marketing claims without a defined search surface and verification plan.
license: MIT
compatibility: Requires access to the target site or content for implementation and verification; bundled scripts use Python 3.9+ standard library only.
metadata:
  scope: search-answer-generative-engine-optimization
  aliases: SEO, AEO, GEO, LLMO, AI-search optimization
---

# SEO

A full-spectrum search visibility skill. It treats traditional SEO, Answer Engine Optimization (AEO), and Generative Engine Optimization (GEO) as overlapping work across different search and answer surfaces, not as separate collections of ranking hacks.

## Operating model

1. **Scope the surface and outcome.** Name the provider, product or search surface, audience, entity, questions, business outcome, and exclusions. Define whether success means crawl access, index eligibility, retrieval, mention, citation, citation correctness, share of voice, referral, or conversion.
2. **Inspect and research.** Audit the public/rendered page and technical delivery. Read current first-party provider guidance and authoritative subject sources. Treat practitioner claims and vendor studies as hypotheses unless methods and scope support more.
3. **Map intent to canonical content.** Use topics and question clusters, but avoid manufacturing near-duplicate pages. Assign one canonical answer location, entity ownership, evidence, freshness owner, and internal links.
4. **Improve people-first content and structure.** Put a concise answer near the relevant heading, then supporting evidence, qualifications, and useful detail. Preserve natural prose, distinct point of view, accessibility, and human value.
5. **Implement only supported controls.** Fix crawlability, indexability, metadata, internal links, page experience, textual content, structured-data parity, sitemaps, freshness, and provider-specific crawler or preview controls. Optional files such as `llms.txt` or Markdown representations are provider-scoped proposals, not universal requirements.
6. **Measure at the correct boundary.** Freeze prompts and versions, capture exact answers and citations, score citation correctness, and use provider-native reports where available. Separate implementation evidence from observed visibility and causal claims.
7. **Verify and learn.** Recheck the rendered/public boundary, validate structured data, inspect search-console or provider evidence, and run bounded one-variable experiments. Do not declare success from HTTP 200, parseable JSON-LD, a single answer, or a third-party score.

## Terminology and boundaries

- **SEO** is the umbrella: improving a site's eligibility, discoverability, interpretation, and useful visibility in search systems.
- **AEO** is a stakeholder label for answer-oriented work, including direct answers, snippets, knowledge surfaces, and answer-engine inclusion.
- **GEO** is a stakeholder label for visibility in generated answers, especially being selected, cited, or factually absorbed into a synthesized response. The term originated in the 2024 KDD paper by Aggarwal et al.; it does not establish a universal algorithm.
- **LLMO** and **AI-search optimization** are overlapping labels. Preserve the target organization's term, then define the measurable outcome and provider scope.
- These terms do not guarantee ranking, inclusion, citation, traffic, recommendation, or conversion. A mention is not a citation, a citation is not proof of correctness, and a citation is not a click.

## Evidence rules

Use these labels in plans and reports:

- **Primary documentation:** provider, standards body, schema vocabulary, or tool owner describes its own behavior.
- **Observed:** recorded crawl, rendered page, provider dashboard, exact answer, URL, or reproducible local result.
- **Independent study:** disclosed method and dataset, with generalization limits stated.
- **Vendor-reported:** useful for hypothesis generation, not a universal rule.
- **Inference:** reasoned interpretation beyond direct observation.
- **Unresolved:** provider-dependent, stale, contradicted, or not verified.

Reject claims such as “FAQ schema guarantees citations,” “short paragraphs are required by all engines,” “`llms.txt` is a search standard,” or “allowing a crawler guarantees inclusion.” Record source URL, access date, provider scope, exact support, what it does not prove, confidence, and refresh trigger for every material claim.

## Reference routing

| Need | Read |
|---|---|
| Crawlability, indexability, robots, sitemaps, performance, canonicals, mobile, HTTPS | `references/technical-seo.md` |
| Titles, descriptions, headings, content quality, links, images | `references/onpage-seo.md` |
| Schema.org, JSON-LD, rich-result eligibility, visible parity | `references/schema-markup.md` and `references/structured-data.md` |
| Topics, question clusters, entities, answer blocks, evidence architecture | `references/content-and-entity-architecture.md` |
| Full answer/generative implementation sequence and completion gate | `references/implementation-playbook.md` |
| Provider guidance, crawler identities, robots and preview controls | `references/platform-guidance.md` and `references/discovery-and-freshness.md` |
| `llms.txt`, Markdown delivery, content negotiation, provider support | `references/agent-readable-content.md` |
| Outcome definitions, confidence, and rejected claims | `references/evidence-boundaries.md` |
| Prompt sets, citation logs, metrics, experiments, and confounders | `references/measurement-and-experimentation.md` |
| Ghost metadata and injection | `references/ghost-metadata.md` |
| Content strategy, topic clusters, keywords, gaps, SERP features | `references/content-strategy-seo.md` |
| Source URLs, access dates, authority tiers, and refresh notes | `references/source-index.md` |

## Scripts and templates

Run from the skill directory:

```bash
python3 scripts/aeo_audit.py <page.html-or-URL> --json
python3 scripts/build_prompt_matrix.py <topics.json> --output prompt-matrix.json
python3 -m pytest scripts/test_aeo_scripts.py
```

The scripts are read-only and use the Python standard library. They inspect source HTML; they do not execute JavaScript, call an LLM, publish, submit URLs, or change crawler policy. Templates cover implementation plans, question clusters, citation observations, optional `llms.txt`, and crawler-policy decisions.

## Audit output

Use `assets/audit-report-template.md` and distinguish:

- **Observed findings:** what the inspected page, response, dashboard, or answer actually shows.
- **Recommended changes:** proposed actions with owner, risk, expected mechanism, and verification.
- **Provider scope:** which engine or search surface the evidence applies to.
- **Status:** implemented, verified, observed, inferred, or unresolved.

## When not to use

Do not use this skill alone for only mechanical copy-editing, ordinary article writing, CMS administration, or a generic request to “rank better” without a defined target, evidence boundary, or measurable outcome. Route those to the relevant writing, copy-editing, CMS, or product skill.

## Portability

Use the host agent's normal mechanisms to load references, templates, and scripts. Do not assume a particular profile system, orchestrator, memory service, CMS, search console, or provider API.
