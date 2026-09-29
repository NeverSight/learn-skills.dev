---
name: yao-demand-skill
description: "Evaluate product demand from product links, product descriptions, PRDs, websites, app-store pages, white papers, sales decks, screenshots, or funding materials using the demand triangle model: lack, target object, and consumer ability. Use when asked for demand assessment, pre-investment product review, growth diagnosis, positioning validation, competitor-backed demand evidence, or a multi-format demand report. Do not use for pure market sizing, generic business-model design, UX-only review, legal/financial advice, or ad-copy ideation without demand evidence."
metadata:
  author: Yao Team
  mode: production
  model: "Demand Triangle: lack + target object + consumer ability"
  output: "Markdown, HTML, Word, PDF"
---

# Yao Demand Skill

Evidence-backed demand assessment for products, services, apps, SaaS, AI tools, consumer goods, education products, and early-stage ventures.

## Use This Skill For

- assessing whether a product has a solid demand foundation before building, investing, launching, or scaling
- diagnosing weak conversion, weak retention, vague positioning, pricing friction, trust friction, or adoption barriers
- comparing direct competitors, indirect substitutes, current user workarounds, and the option of not buying
- producing a visual demand diagnosis report with citations, scores, red flags, 10+ chart modules, experiments, forecasts, and four final formats

## Do Not Route Here

- pure TAM/SAM/SOM market sizing without product-demand diagnosis
- generic monetization or business-model option design; use a business-model skill instead
- UX heuristic review without demand, JTBD, or adoption evidence
- legal, financial, medical, or investment advice as a final decision
- manipulative marketing designed to shame, scare, addict, or exploit vulnerable users

## Workflow

1. Confirm the product input. Accept a URL, text description, PRD, website copy, docs, screenshot, app-store page, sales material, or funding deck. Ask only one concise question if no product substance is available.
2. Build the product canvas: product definition, user, scenario, features, price, promise, business model, market, source list, and unresolved assumptions.
3. Plan evidence. Prioritize official sources, third-party validation, user feedback, competitor/substitute evidence, and time-sensitive market or regulatory facts.
4. Research only evidence that can support or challenge demand. Current product, price, competitor, market, legal, or regulatory facts must be verified with sources and dates.
5. Segment users by JTBD, trigger scenario, buying role, current alternatives, and adoption blockers.
6. Analyze the three demand triangle dimensions: `lack`, `target_object`, and `consumer_ability`. Include evidence, counter-evidence, assumptions, and improvement paths.
7. Score each dimension from `0` to `10`, then calculate total score with the geometric short-board formula and confidence adjustment.
8. Produce visual diagnostics: at least 10 chart modules, each with one or two insight sentences, one recommendation, confidence, and evidence or assumption binding.
9. Produce recommendations, forecast scenarios, and a final 30/60/90 day action plan: positioning, product, pricing, onboarding, trust, channel, and validation experiments.
10. Run QA: citation coverage, time consistency, evidence diversity, at least three counter-signals, score explainability, chart completeness, ethics, and layout readiness.
11. Write a structured report JSON, then use `scripts/render_report.py` to create Markdown, HTML, Word, and PDF outputs.

## Output Contract

- Always produce the final report in four formats: `.md`, `.html`, `.docx`, and `.pdf`.
- Use one canonical `report.json` as the rendering source when possible, so the four outputs remain consistent.
- HTML must include a top follow menu bar that stays pinned while the page scrolls, with quiet anchor navigation.
- Formal reports must follow a `summary -> visual diagnostics -> deep analysis -> final plan` structure.
- Formal reports must include at least 10 chart modules. HTML/PDF render them as inline SVG. Markdown and Word must include chart-equivalent tables or images.
- All report backgrounds are pure white. Borrow Kami's editorial hierarchy, ink-blue accent, table discipline, typography, spacing, and production checks, but override Kami's parchment background.
- Every key factual claim must either cite a source ID or be labeled as an assumption.
- Every score must include evidence, reasoning, uncertainty, and a concrete improvement path.
- Forecasts must be scenario-based and labeled with assumptions and confidence. Do not present uncertain adoption outcomes as deterministic predictions.

## Reference Map

- Read `references/workflow.md` before starting an assessment.
- Read `references/evidence-policy.md` before using sources, citations, or current facts.
- Read `references/triangle-model.md` before scoring.
- Read `references/report-contract.md` before writing the report JSON or final narrative.
- Read `references/kami-white-report-layout.md` before rendering the four output formats.
- Use `templates/report.schema.json` as the report JSON target.
- Use `scripts/score_triangle.py` to calculate or verify weighted scores.
- Use `scripts/validate_report.py` before rendering.
- Use `scripts/render_report.py` to generate Markdown, HTML, Word, and PDF.
