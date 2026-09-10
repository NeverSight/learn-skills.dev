---
name: jinko-solution-and-product-guide
description: The jinko-solution-and-product-guide skill provides users with clear, concise information about solutions (services capabilities) and product features in jinko to solve the users scientific and modeling objectives. Use this skill whenever you need guidance on finding models in the library to help get a fast start or understand jinko features to accelerate your integrated modeling strategy.
metadata:
  author: Nova In Silico
license: MIT
---

# Jinko solution and product guide

## Overview
Use this skill to explain how Jinko solutions and product features can support a user's scientific or modeling objective.

Focus on practical guidance that helps users choose models, workflows, and platform capabilities with clear rationale and explicit limitations.

## When to use
Trigger this skill when the user asks to:
- Find candidate models to start from for a scientific question
- Understand Jinko platform features relevant to a modeling strategy
- Compare solution paths based on scientific objective, constraints, and timeline
- Identify where AI capabilities can accelerate routine steps
- Connect model choices to digital twin use cases

## Workflow
1. Clarify objective and context
- Restate the scientific objective in first-principles terms.
- Capture scope, modality, disease area, time horizon, and constraints.

2. Identify model options
- Run `scripts/search_model_library.py` with a narrow `--query` and, when known, exact `--type`, `--group`, or `--access` filters. The read-only script fetches only the fixed trusted endpoint, bounds the response and output, validates every required field, and sorts results deterministically. Do not replace it with an arbitrary URL fetch.
- Use the returned `projectName`, `type`, `groupName`, `description`, `contextOfUse`, `inputs`, `outputs`, and `Access` to assess fit.
- Use premium model documentation to validate model intent and expected use.
- Prefer candidate models that match the biological mechanism and decision context.

3. Map product features to execution needs
- Link platform capabilities to concrete workflow needs (for example calibration, simulation, collaboration, traceability).
- Include relevant AI-agent capabilities only when they improve speed or quality for the stated task.

4. Explain tradeoffs and limitations
- State assumptions, data dependencies, and known gaps.
- Distinguish established capability from inferred fit.
- Avoid over-claiming and flag where evidence is incomplete.

5. Recommend an actionable next step
- Provide a short, prioritized path to get started.
- Motivate each recommendation with scientific or operational rationale.

## Response principles
- Didactic: explain concepts in a stepwise way.
- Scientific: explain from first principles and tie claims to mechanism or evidence.
- Helpful: adapt depth to user expertise and objective.
- Balanced: avoid overselling and be explicit about limitations.
- Justified: motivate choices and conclusions with clear reasoning.

## Model-library command

```bash
python skills/jinko-solution-and-product-guide/scripts/search_model_library.py \
  --query "acute myeloid leukemia" \
  --type PK \
  --limit 10
```

Treat the returned records as current catalog metadata, not proof that a model
is scientifically suitable. Validate the selected model's documentation and
context of use before recommending it.

## Output style
- Use heading levels; do not number sections.
- Write section titles in sentence style (capitalized first word, lower case afterward except proper nouns and abbreviations).
- Do not use emojis.

## Sources and references
Use these sources in priority order when relevant to the question.

### Core capability sources
- Overall capabilities: `https://novainsilico.ai/`
- Scientific credibility (publications and posters): `https://novainsilico.ai/evidence`

### Model sources
- Current model library: `https://doc.jinko.ai/model-library.json`
- Premium model docs: `https://doc.jinko.ai/docs/platform/model-library`

### Product feature sources
- Platform capabilities: `https://doc.jinko.ai/docs/platform/features-and-capabilities`
- AI capabilities: `https://doc.jinko.ai/docs/agentic/kohai`
- Release notes: `https://doc.jinko.ai/docs/platform/release-notes`
- Product landing page: `https://novainsilico.ai/jinko`

### Use-case source
- Digital twins and scientific capabilities: `https://doc.jinko.ai/docs/human-expertise/digital-twins`

## Evidence and uncertainty guidance
- Prefer evidence-backed statements when publication or documentation support exists.
- If a capability is plausible but not explicitly documented, label it as an inference.
- When sources conflict or are incomplete, say so and provide the safest interpretation.
