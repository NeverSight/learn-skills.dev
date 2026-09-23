---
name: paper-insight
description: Structured scholarly paper reading and research ideation. Use when Codex needs to read or summarize papers/PDFs, judge innovations, score paper quality and reading priority, compare related work, draft related work sections, expand a literature map with backward/forward citation chaining, identify limitations, incubate research ideas, propose feasible future research directions, map papers into the user's project, check reproducibility/code availability, or apply a general domain checklist for psychology, human-centered research, NLP, ML, AI, or other scholarly areas.
---

# Paper Insight

## Overview

Use this skill to turn one paper or a small paper set into citation-grounded research insight: structured reading notes, innovation judgment, paper scorecards, strategic citation chaining, related-work expansion and drafting, idea incubation, future directions, paper-to-project transfer plans, reproducibility checks, a general domain checklist, and literature maps. Prefer primary sources, official paper pages, PDFs, project pages, official repositories, and authoritative indexes over secondary summaries.

## Operating Principles

- Separate paper claims, evidence-supported conclusions, and your own inferences.
- Do not fabricate citations, venues, DOIs, arXiv IDs, datasets, results, page numbers, or related papers.
- If only the abstract is available, say that the assessment is abstract-only.
- Prefer fewer well-read papers over long unvetted lists.
- Stop expansion when new papers no longer change the interpretation or the user's requested scope is reached.

## Workflow

1. Clarify scope only when needed: paper(s), domain, output mode, venue/year constraints, whether preprints are acceptable, and whether code reuse matters.
2. Collect source material:
   - For local PDFs, use `pdfinfo`, `pdftotext -layout`, and visual inspection when figures/tables matter.
   - For web sources, use primary paper pages, arXiv, OpenReview, ACL Anthology, ACM/IEEE/publisher pages, PubMed, Semantic Scholar, Crossref, Papers with Code, and official repositories.
   - For recent or "latest" work, browse and record exact dates.
3. Read in layers:
   - Pass 1: title, abstract, introduction, conclusion.
   - Pass 2: method, experiments, limitations, appendix, key tables/figures.
   - Pass 3: related work and citations only if expansion is needed.
4. Produce the lightest useful output:
   - `structured_reading`: detailed paper notes.
   - `innovation_check`: contribution and novelty assessment.
   - `paper_scorecard`: quality, evidence, reproducibility, transferability, and reading-priority scoring.
   - `citation_chaining`: backward, forward, lateral, benchmark, and negative/critique literature expansion.
   - `related_work_expansion`: nearby papers and relationship types.
   - `related_work_draft`: cohesive related-work paragraphs organized by timeline, method family, problem evolution, or motivation gap.
   - `future_directions`: limitations converted into feasible research plans.
   - `idea_incubator`: research hypotheses, minimal experiments, expected outcomes, risks, and possible paper angles.
   - `paper_to_project`: reusable units, target files/modules, integration risks, and minimal project validation.
   - `reproducibility_check`: code/data/checkpoint/experiment reuse assessment.
   - `domain_checklist`: field-specific validity, evidence, and risk checks.
   - `literature_map`: graph or table of paper relationships.

## Structured Reading

For each key paper, capture:

- Full citation: title, authors, year, venue/preprint server, DOI/arXiv/PMID when available.
- Research question and target problem.
- Core idea in one sentence.
- Method: model, algorithm, data, assumptions, training/inference pipeline, or theoretical argument.
- Evidence: datasets, metrics, baselines, sample size, statistical tests, ablations, or proofs.
- Main findings and what they do not prove.
- Limitations, failure modes, threats to validity, and missing experiments.
- Relevance to the user's project or research question.

When the user wants a deeper template, read `references/output-templates.md`.

## Innovation Judgment

Classify contributions into these layers:

- Problem innovation: new task, benchmark, framing, or evaluation question.
- Method innovation: new model, objective, architecture, prompting/training strategy, inference mechanism, or algorithm.
- Data innovation: new dataset, annotation protocol, sampling strategy, or synthetic-data construction.
- Evaluation innovation: new metrics, baselines, stress tests, or analysis dimensions.
- Theory innovation: new definition, hypothesis, proof, explanation, or conceptual framework.
- Engineering innovation: improved speed, memory, deployment, robustness, reproducibility, or usability.

Then answer:

- What is genuinely new relative to the closest prior work?
- Is the contribution a new principle, a new combination, or an incremental implementation detail?
- Which experiments directly support each claimed contribution?
- What claim is under-supported or only partially tested?
- What would make the novelty claim stronger?

## Related Work Expansion

Use citation chaining, keyword search, venue search, and official indexes to find nearby work. When the user asks for how the field evolved before or after the target paper, what work builds on it, what else solves the same task, current SOTA on the same benchmark, or critiques/failed reproductions, read `references/citation-chaining.md`.

Use five complementary search paths:

- Backward chaining: read references to identify source papers and direct predecessors.
- Forward chaining: find citing papers to understand later development and work built on the target paper.
- Lateral search: search the same task/problem with different method families.
- Benchmark search: search the same datasets, metrics, leaderboards, or SOTA comparisons.
- Negative/critique search: search for reproductions, limitations, failures, critiques, or contradictory evidence.

Group papers by relationship instead of listing them flat:

- Foundational: establishes the problem, model family, dataset, or theory.
- Direct predecessor: most similar prior method or task framing.
- Competing method: solves the same problem with a different approach.
- Extension: later work that improves or generalizes the paper.
- Benchmark/dataset: defines the evaluation setting.
- Survey/meta-analysis: summarizes the area.
- Critique/negative result: challenges assumptions or reports failure modes.

Keep expansion bounded by the user's scope. Default to 5-10 high-value papers unless the user asks for a broader review.

## Future Direction Generation

Convert limitations into concrete, testable directions. For each direction, state:

- Source limitation or evidence gap.
- Proposed idea.
- Why it is plausible.
- Required data, compute, implementation effort, or domain expertise.
- Expected risk and failure mode.
- Minimal verification experiment.
- Priority score: novelty, feasibility, impact, cost, risk, and fit to the user's project.

Prefer actionable directions over generic "use more data" or "try larger models" suggestions. Mark speculative ideas clearly.

## Research Decision Workflows

When the user asks whether a paper is worth reading, how to write related work, what project direction to pursue, or how to adapt a paper into the current repository, read `references/research-workflows.md`.

Use these workflows:

- `paper_scorecard`: score novelty, evidence, reproducibility, transferability, risk, and reading priority.
- `related_work_draft`: turn a literature map into polished related-work prose.
- `idea_incubator`: generate low-cost experiments, workshop-scale ideas, main-paper directions, and high-risk/high-reward bets.
- `paper_to_project`: map paper ideas onto the user's codebase or research project with minimal integration and verification steps.

## Reproducibility Check

When code, reuse, or implementation matters, inspect official repositories before recommending reuse:

- Provenance: official author repo, benchmark repo, or third-party reproduction.
- License and citation requirements.
- Dependencies: framework, Python/CUDA versions, package constraints.
- Availability: data, checkpoints, configs, scripts, pretrained weights.
- Entry points: training, evaluation, inference, data processing.
- Metric reproduction: expected results, seeds, logs, and exact commands if available.
- Reuse fit: smallest reusable unit and integration risks.

For detailed prompts and tables, read `references/reproducibility.md`.

## Domain Checklist

For any specialized area, apply the relevant checklist in `references/domain-checklists.md`. Use the checklist to flag field-specific validity issues, evidence gaps, sample or data bias, evaluation weaknesses, privacy/ethics concerns, and whether the paper's claims exceed what its methods can support.

## Literature Map

When asked to connect papers, output a compact relationship graph, timeline, or table. Include why each edge exists, such as "uses same dataset", "extends objective", "criticizes assumption", or "introduces benchmark". For mapping templates, read `references/literature-map.md`.

## Output Standards

- Include links or identifiers for sources used.
- Use tables only when comparison or prioritization benefits from them.
- Name search limitations: paywalls, missing full text, unavailable code, weak evidence, or fast-moving preprint areas.
- For recommendations, explain why a direction is worth doing and how to test it with the smallest useful experiment.
- If evidence is insufficient, say what source or experiment would resolve the uncertainty.
