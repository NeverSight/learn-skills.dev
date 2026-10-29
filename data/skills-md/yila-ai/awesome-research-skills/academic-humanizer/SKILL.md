---
name: academic-humanizer
description: Use when researchers ask to remove generic, templated, or AI-like patterns from Chinese or English academic prose, make an AI-assisted draft sound more like the author's own scholarly voice, or audit a paper for “AI味”. Preserve every scientific claim, number, equation, citation, limitation, and uncertainty. Not for detector evasion or ordinary translation and grammar-only editing.
license: Apache-2.0
---

# Academic Humanizer

Remove the template voice, not the scholarship. Make academic prose more specific, natural, and recognizably the author's while preserving the research exactly.

This Skill improves writing quality. It does not certify that text is human-written, optimize for an AI detector, or remove an author's obligation to disclose AI assistance under the relevant journal, institution, or funder policy.

## Load only what is needed

- Always read `references/preservation-and-evidence.md`, `references/pattern-catalog.md`, and `references/output-contract.md`.
- Read `references/voice-calibration.md` only when the author provides writing samples or explicitly asks to match their voice.
- When source and revision are available as local text, use `scripts/check_invariants.py` as a deterministic first check. A passing result never replaces the semantic audit.

## Use this Skill when

The user asks to:

- remove “AI味”, AI-like phrasing, template language, or generic LLM prose from academic text;
- make a paper sound less mechanical, less inflated, or more like the author;
- audit an abstract, paper section, thesis passage, rebuttal, or reviewer response for recurring AI-writing patterns;
- calibrate a draft against the author's prior academic writing.

For ordinary Chinese-to-English translation, grammar correction, or general publication polishing without a de-templating or voice-matching goal, `sci-ssci-polishing` is the better entry point.

## Inputs

Required:

- the passage or document to audit or revise.

Useful but optional:

- language, field, section type, and target venue;
- one or more genuine writing samples from the author;
- protected terminology or phrases;
- desired intensity: audit only, standard, or strong.

Do not block on optional context. Without author samples, use a neutral, precise, venue-appropriate academic voice and state that personal voice matching was not performed.

## Workflow

### 1. Classify the task

Identify:

- language: Chinese, English, or mixed;
- scope: passage, paragraph set, section, or full document;
- rhetorical function: Abstract, Introduction, Methods, Results, Discussion, Conclusion, literature review, rebuttal, or mixed;
- requested mode: audit only, standard rewrite, strong rewrite, or voice matching.

Infer missing context conservatively. Do not force a paper, thesis, rebuttal, and grant proposal into the same register.

### 2. Freeze the scholarship

Before editing, create a private preservation ledger covering:

- numbers, statistics, units, equations, variables, citations, and figure or table references;
- named methods, datasets, instruments, entities, and author-supplied terminology;
- actors, populations, comparisons, directions, time order, uncertainty, limitations, causal strength, and conclusion scope.

Follow `references/preservation-and-evidence.md`. If the source is ambiguous, keep the narrowest defensible meaning and add an author query.

### 3. Audit patterns before rewriting

Use `references/pattern-catalog.md` to locate patterns and explain why they weaken the passage.

Treat the catalog as a set of editorial diagnostics, not a detector:

- do not label a passage AI-written;
- do not flag a single word or punctuation mark as proof;
- look for repeated cues or clusters across at least two categories;
- protect legitimate disciplinary conventions and phrases that carry real information.

For each material finding, record the location, pattern category, why it weakens the text, and the smallest useful fix.

### 4. Calibrate voice when evidence is available

If the user provides prior writing, follow `references/voice-calibration.md`. Match stable habits such as information order, sentence rhythm, connective density, hedging, citation integration, and use of “we”. Do not copy distinctive phrases or introduce claims from the sample.

### 5. Rewrite with an information-first rule

Prioritize:

1. scholarly fidelity;
2. claim-evidence alignment;
3. concrete subjects and actions;
4. section-appropriate rhetoric;
5. natural rhythm and author voice;
6. concision.

Prefer cutting empty language to replacing it with new decoration. Replace abstractions with facts already present in the source. Split clause-stacked sentences only when qualifications and citation scope remain clear.

Keep legitimate passive voice, calibrated hedging, technical repetition, definitions, and first-person plural when they fit the field. Never apply a mechanical banned-word list.

When evidence is missing, flag the gap or soften the wording. Never invent a number, citation, mechanism, comparison, limitation, result, or implication.

### 6. Verify

Compare the revision with the preservation ledger. If local files are available, run:

```bash
python3 scripts/check_invariants.py case.json
```

The JSON case contains `source`, `revision`, and optional `protected_terms`. Manually verify claim direction, negation, modality, causal strength, citation attachment, limitations, and conclusion scope even when the script passes.

### 7. Report transparently

Follow `references/output-contract.md`. Return the revised text first unless the user requested audit only. Then summarize the pattern changes, fidelity checks, voice basis, and unresolved author queries.

## Editing intensity

### Audit only

Diagnose patterns and propose targeted fixes without rewriting the passage.

### Standard — default

Remove repeated template patterns and improve sentence flow while preserving paragraph order and every scientific proposition.

### Strong

Rebuild sentences and, when necessary, reorder them for information flow. Preserve every proposition, evidence pointer, citation role, limitation, and conclusion. List meaningful reorderings.

## Integrity boundary

- Do not claim or guarantee that the revision will pass an AI detector.
- Do not optimize against detector scores or help conceal prohibited AI use.
- Do not describe a revision as human-written when AI contributed to it.
- Do not remove disclosure language, limitations, uncertainty, or provenance to make a manuscript look cleaner.
- When venue rules matter, remind the author to follow the current disclosure policy without giving legal or institutional-policy assurances.

The useful outcome is clearer, less formulaic, evidence-bound academic writing—not plausible deniability.
