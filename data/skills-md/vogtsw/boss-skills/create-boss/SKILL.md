---
name: create-boss
description: Distill a real boss into an AI skill, or generate a boss skill from a famous entrepreneur archetype such as Elon Musk, Steve Jobs, Jeff Bezos, or Jensen Huang, or build a persona from free public sources (papers, GitHub, Wikipedia) for a mentor or PI. Use when the user wants boss analysis, managing-up guidance, persona extraction, decision-model distillation, or entrepreneur-style boss presets.
argument-hint: "[boss-name-or-archetype]"
version: "1.2.0"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash
---

# Create Boss

Use this skill in three modes:

1. `real boss mode`
   Turn real chat logs, meeting notes, emails, comments, and project artifacts into a boss skill.
2. `archetype mode`
   Generate a boss skill inspired by a public entrepreneur operating style.
3. `public research mode`
   Build a persona for a mentor, PI, or boss from free public sources
   (OpenAlex, Semantic Scholar, arXiv, Crossref, GitHub, Wikipedia, web search).

## Trigger phrases

- `/create-boss`
- `/list-bosses`
- `/boss-rollback`
- `/delete-boss`
- "create a boss skill"
- "analyze my boss"
- "build a Musk-style boss"
- "make a Steve Jobs style leader"
- "give me a Bezos-style management model"
- "list boss archetypes"
- "research my advisor / mentor / PI"
- "建一个我导师的画像"
- "run replay eval" / "测一下这个老板像不像"

## Tools

- Parse imported material with the files in [`tools/`](tools).
- Write or update generated boss skills with [`tools/skill_writer.py`](tools/skill_writer.py).
- Search free public sources about a person with [`tools/person_research.py`](tools/person_research.py).
- Evaluate persona fidelity with [`tools/replay_eval.py`](tools/replay_eval.py).
- Read template prompts from [`prompts/`](prompts) when working from real source material.
- Read bundled entrepreneur templates from [`archetypes/`](archetypes) when working in archetype mode.

These scripts are internal implementation details for the agent.
Do not ask the user to run Python commands manually unless they explicitly want a developer workflow.

## Workflow

### Mode 1: Real Boss

1. Ask for the boss name, baseline profile, and initial management impression.
2. Ask for source material: chats, meeting notes, docs, email, or pasted text.
3. Extract structured decision cases first, following
   [`prompts/decision_extractor.md`](prompts/decision_extractor.md).
   Each case goes into `bosses/{slug}/cases/` via
   `skill_writer.py --action add-case`.
4. Distill three narrative outputs:
   - `judgment.md`
   - `management.md`
   - `persona.md`
5. Build the decision layer from the cases:
   - `rubric.json` and `decision_rules.md`, following
     [`prompts/decision_model_builder.md`](prompts/decision_model_builder.md)
     (write with `--action set-rubric` / `--action set-rules`)
   - scene playbooks, following
     [`prompts/playbook_builder.md`](prompts/playbook_builder.md)
     (write with `--action add-playbook`)
6. Run the writer script yourself to write the boss bundle into `bosses/{slug}/`.
7. If there are 3+ cases, offer to run a decision replay eval, following
   [`prompts/replay_evaluator.md`](prompts/replay_evaluator.md).
8. Show the generated commands:
   - `/{slug}`
   - `/{slug}-judgment`
   - `/{slug}-management`
   - `/{slug}-persona`

### Mode 2: Entrepreneur Archetype

1. If the user asks for an entrepreneur-style boss, infer the best matching archetype or offer a short list:
   - `elon-musk`
   - `steve-jobs`
   - `jeff-bezos`
   - `jensen-huang`
2. Run the writer script yourself to generate the skill. Do not expose the internal command as the primary UX.
3. Tell the user the generated trigger command, for example:
   - `/elon-musk`
   - `/steve-jobs`
4. If the user asks to browse or inspect templates, summarize the available archetypes in natural language instead of telling them to run a script.

### Mode 3: Public Research (mentor / PI / public boss)

Follow [`prompts/person_researcher.md`](prompts/person_researcher.md):

1. Collect the person's real name, affiliation, and field from the user.
2. Run `tools/person_research.py --name "..." --affiliation "..." --sources all
   --save-dir bosses/{slug}/knowledge/research`.
   All sources are free and need no API key.
3. Disambiguate candidates with the affiliation hint; if still ambiguous,
   ask the user to pick. Never guess.
4. Supplement with your own web search for interviews, talks, and blog posts.
5. Distill the persona with evidence levels: `private` > `public-quote` >
   `public-inferred`. Every public-sourced claim must carry its source.
6. This mode can be combined with Mode 1: real private material always
   outranks public inference.

## Management Commands

When the user asks for boss management operations, handle them internally with the bundled scripts:

- `/list-bosses`
  Run `tools/skill_writer.py --action list` and summarize the available boss skills.
- `/boss-rollback {slug} {version}`
  Confirm the target slug and version, then run `tools/version_manager.py --action rollback`.
- `/delete-boss {slug}`
  Confirm before deletion, then run `tools/skill_writer.py --action delete --slug {slug}`.
- `/{slug}-drill {scene}`
  Roleplay the boss across multiple turns using the matching playbook's
  expected reactions and failure branches. End with a debrief against `rubric.json`.
- `/boss-eval {slug}`
  Run the decision replay eval per `prompts/replay_evaluator.md` and report
  the fidelity score.

Do not tell normal users to copy these commands manually. Execute the workflow yourself and report the result.

## Bundled Archetypes

- `elon-musk`: first-principles, speed, technical pressure
- `steve-jobs`: taste, simplicity, product clarity
- `jeff-bezos`: mechanism design, customer obsession, written thinking
- `jensen-huang`: platform strategy, technical depth, constructive intensity

## Files Created

Every generated boss skill should include:

- `SKILL.md`
- `judgment.md`
- `management.md`
- `persona.md`
- `meta.json`
- `judgment_skill.md`
- `management_skill.md`
- `persona_skill.md`

When source material contains real decisions, also create the decision layer:

- `cases/*.json` — structured decision events with original quotes and sources
- `rubric.json` — the boss's review checklist (blocker / major / minor items)
- `decision_rules.md` — IF/THEN decision rules with case evidence
- `playbooks/*.md` — scene workflows (bad news, resource request, pitch, ...)
- `eval/` — replay eval artifacts (question pack, answer key, fidelity report)

## Corrections

When the user corrects the model ("he wouldn't say that", "he cares about X more"):

1. Locate the affected rubric item, rule, case, or persona section.
2. Mark the old conclusion as overruled instead of deleting it, then add the
   corrected rule with evidence `user-correction-{date}`.
3. Follow [`prompts/correction_handler.md`](prompts/correction_handler.md).
4. After corrections accumulate, re-run the replay eval to confirm fidelity
   did not regress.

## Safety Framing

- Treat entrepreneur presets as public-style archetypes, not claims of exact private impersonation.
- Prefer management patterns, decision rules, and communication norms over catchphrases.
- If the user asks for a hybrid with a real boss, keep real evidence higher priority than the archetype.
- In public research mode, use only freely accessible public data, never bypass
  logins or paywalls, and present results as a public-style portrait with sources.
- Redact unrelated third-party names from extracted cases.
