---
name: editorial-quality-gate
description: Review public site content for editorial quality, source support, prompt residue, duplicate blocks, translation drift, hidden filler, and human usefulness before SEO or LLM-friendly publication. Use this skill when the user asks to quality-gate news briefs, longform explainers, blog posts, topic pages, project pages, translated content, or generated article drafts without changing the live publishing pipeline.
---

# Editorial Quality Gate

Use this skill after the site content model and publication surface are known.

Read [references/editorial-quality-checklist.md](references/editorial-quality-checklist.md)
before producing a full content quality report.

## Owns

- editorial quality checklist;
- source support and unsupported-claim review;
- prompt residue detection;
- repeated block and context leakage review;
- no SEO-filler checks;
- page-type quality gates for news, longform, blog, project, and topic pages;
- handoff backlog for content strategy, localization, and decay monitoring.

## Does Not Own

- live publishing pipelines;
- model provider credentials;
- translation implementation;
- content strategy beyond quality-gate findings;
- content decay automation;
- technical SEO/schema implementation;
- visual layout or UX design.

## Workflow

1. Identify page type: `news_brief`, `longform_article`, `blog_post`, `project_page`, `topic_page`, or `translation`.
2. Identify the intended source material and visible claims.
3. Check whether each material claim is supported by a source, artifact, or clearly marked author opinion.
4. Scan for prompt residue, editorial instructions, repeated context blocks, boilerplate padding, and low-value SEO filler.
5. For translations, compare meaning and audience fit rather than demanding literal phrasing.
6. Check that the content serves its declared page role and does not create a duplicate public story body.
7. Return a gate decision: `pass`, `revise`, or `block`.
8. Record follow-up items for content strategy, localization, or decay monitoring when they exceed this skill's scope.

## Non-Negotiables

- Do not approve unsupported factual claims.
- Do not approve hidden SEO-only content.
- Do not approve prompt residue or internal editorial instructions in public text.
- Do not approve repeated paragraphs unless repetition is explicitly justified by page structure.
- Do not create a third public story body when the declared model is one short brief plus one longform article.
- Do not claim translation quality without checking meaning, terminology, tone, and locale fit.
- Do not rewrite the whole article unless the user explicitly asks for a rewrite.
- Do not touch live publishing systems.

## Safety And Privacy Boundaries

- Do not include secrets, API keys, private analytics rows, raw IP logs, account tokens, private drafts, or admin-only URLs in public content reports.
- Do not publish or edit live content unless the user separately asks for that implementation task.
- Do not reveal private source material in public-facing recommendations.
- Do not approve claims about medical, legal, financial, ranking, crawler, or assistant-citation outcomes without appropriate evidence and scope labels.
- Do not turn editorial QA into hidden crawler-only optimization.

## Page-Type Gates

### News Brief

Must be concise, sourced, dated, and clear about what happened. It should link to the paired
longform when available. It should not become a longform explanation.

### Longform Article

Must explain context, why it matters, source trail, implications, and uncertainty. It should
remove prompt residue from generation and avoid repeating the short brief verbatim beyond a short summary.

### Blog Post

May contain author opinion, but factual claims and references still need support or clear framing.
It should not imitate news authority if it is a personal essay.

### Project Page

Must describe purpose, status, repository or artifact links if public, evidence of usefulness,
and relation to the site or workflow. It should not overclaim maturity.

### Topic Page

Must define the topic, explain why it matters, link to representative stories/projects, and avoid
thin aggregation.

### Translation

Must be localized for the target reader, preserve factual meaning, avoid literal awkwardness,
and keep names, dates, product terms, and source references consistent.

## Output Shape

Return:

1. Gate decision: `pass`, `revise`, or `block`.
2. Page type and intended role.
3. Findings grouped by severity.
4. Source-support notes.
5. Prompt-residue and duplication notes.
6. Translation/localization notes if relevant.
7. Minimal edits or revision instructions.
8. Deferred backlog items for content strategy, localization, or decay monitoring.

Use [assets/quality-gate-report.template.md](assets/quality-gate-report.template.md) when a persistent report is needed.

## Validation

Validate skill edits with:

```bash
python3 $CODEX_HOME/skills/senior-skill-architect/scripts/lint_production_skill.py $HOME/SKILL/skills/editorial-quality-gate
python3 $HOME/SKILL/plans/seo-llm-skill-cluster/scripts/lint_skill_cluster.py $HOME/SKILL
```

Forward tests live in [evals.json](evals.json).
