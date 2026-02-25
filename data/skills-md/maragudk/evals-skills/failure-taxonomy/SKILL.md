---
name: failure-taxonomy
description: >
  Build a structured taxonomy of failure modes from open-coded trace annotations.
  Use this skill whenever the user has freeform annotations from reviewing LLM traces
  and wants to cluster them into a coherent, non-overlapping set of binary failure categories
  (axial coding). Also use when the user mentions "failure modes", "error taxonomy",
  "axial coding", "cluster annotations", "categorize errors", "failure analysis",
  or wants to go from raw observation notes to structured evaluation criteria.
  This skill covers the full pipeline: grouping open codes, defining failure modes,
  re-labeling traces, and quantifying error rates.
---

# Failure Taxonomy Builder

Transform raw, freeform trace annotations from open coding sessions into a structured
taxonomy of binary failure modes, following the grounded theory methodology from the
Analyze-Measure-Improve evaluation lifecycle.

## When This Skill Applies

The user has already completed **open coding** — they've read through LLM pipeline traces
and written short, freeform notes describing what went wrong (the "point of first failure").
Now they need to move from that chaotic pile of observations into an organized, actionable
taxonomy. This is the **axial coding** step.

Typical inputs look like a JSON array, CSV, or spreadsheet of objects with fields like:
- `trace_id` — identifier for the trace
- `annotation` or `note` — the freeform open-coded observation
- Optionally: `pass_fail`, `trace_summary`, `query`, or the full trace itself

## Core Workflow

### Step 1: Ingest and Understand the Annotations

1. Ask the user to provide their open-coded annotations (JSON, CSV, or pasted text).
2. Read through ALL annotations before doing anything else. This mirrors how a human
   analyst would spread out all their sticky notes before grouping.
3. Count total annotations and note how many are unique vs. near-duplicates.
4. Identify the application domain from context clues in the annotations.

### Step 2: Draft Failure Mode Clusters (Axial Coding)

Group similar annotations into a **small set of coherent, non-overlapping failure categories**.

**Key principles — these matter a lot:**

- **Small set**: Aim for 3–7 failure modes. Fewer is better. If you have more than 7,
  you're probably splitting too finely — merge related categories.
- **Binary and specific**: Each failure mode is a yes/no question: "Did this failure occur?"
  Avoid vague categories like "bad output" or "hallucination" without qualification.
- **Non-overlapping**: A single annotation should map cleanly to one failure mode. If
  annotations regularly fit two categories, the categories need rework.
- **Application-specific**: Use the vocabulary of the user's domain, not generic LLM
  research terms. "Missing SQL constraint" beats "incomplete tool use". "Persona mismatch"
  beats "tone error".
- **Actionable**: Each failure mode should suggest a clear engineering fix. If you can't
  imagine what a developer would change to address it, the category is too abstract.
- **No Likert scales**: Everything is binary. A failure mode is present (1) or absent (0).
  Numeric severity scores introduce noise and reduce inter-annotator agreement.

**Process:**

1. Read through all annotations and mentally group similar observations.
2. For each emerging group, write a **short title** (2–5 words) and a **one-line definition**
   explaining what qualifies as this failure.
3. List 2–3 representative example annotations under each group.
4. Check for overlaps — if two categories share examples, merge or split until clean.
5. Check for orphans — annotations that don't fit anywhere may signal a missing category
   or may be genuine one-offs to flag separately.

Present the draft taxonomy to the user as a table:

```
| # | Failure Mode | Definition | Example Annotations |
|---|-------------|------------|---------------------|
| 1 | [Title]     | [One-line] | [2-3 examples]      |
```

### Step 3: Refine Through Discussion

After presenting the draft, prompt the user to consider:

- Are any categories too broad? (Should they be split?)
- Are any categories too narrow? (Should they be merged?)
- Do the titles make sense to a domain expert who hasn't read the raw data?
- Are there annotations that don't fit any category?

Iterate until the user confirms the taxonomy. Typical refinement takes 1–2 rounds.

### Step 4: Re-label Traces Against the Taxonomy

Once the taxonomy is confirmed, systematically apply it back to every trace:

1. For each trace/annotation, assign a `1` or `0` for each failure mode.
2. A trace can have multiple failure modes present (they're independent binary columns).
3. If an annotation doesn't match any failure mode, flag it as "Uncategorized" for review.
4. Present the re-labeled data in a structured format (JSON or CSV).

### Step 5: Quantify and Prioritize

Compute error rates for each failure mode:

- **Count**: How many traces exhibit this failure?
- **Rate**: Count / total traces (as a percentage).
- **Rank**: Order failure modes by prevalence.

Present a summary table and recommend which failure modes to address first based on
frequency. Note: frequency alone doesn't determine priority — the user may weight
certain failures higher based on business impact. Ask them.

## Output Formats

The skill produces up to three artifacts:

1. **Taxonomy definition** (always produced) — A clean document defining each failure
   mode with its title, definition, and representative examples.

2. **Re-labeled dataset** (produced when input traces are provided) — The original
   annotations augmented with binary columns for each failure mode, as JSON or CSV.

3. **Summary statistics** (produced when re-labeling is done) — Error rates, counts,
   and a prioritized ranking.

For detailed output schemas and file format guidance, read `references/output-formats.md`.

## Anti-Patterns to Avoid

These are drawn directly from common pitfalls observed in practice:

- **Generic categories from LLM research**: Don't default to "hallucination", "staying on
  task", "verbosity" without grounding in the actual annotations. The whole point of open
  coding first is to let application-specific patterns emerge.
- **Too many categories**: If you have 10+ failure modes from 30 annotations, you're
  over-splitting. Merge until you have 3–7 crisp categories.
- **Likert scales or severity scores**: Resist any urge to rate failures on a 1–5 scale.
  Binary decisions produce more consistent, reproducible labels.
- **Freezing too early**: The taxonomy should evolve. After re-labeling, the user may
  discover that a category needs splitting or that a new pattern has emerged. This is
  normal and expected — support iteration.
- **Skipping representative examples**: Every failure mode definition needs concrete
  examples. Without them, the category is too abstract to apply consistently.

## Using an LLM to Assist Clustering

When the user has 30+ annotations, it can help to use an LLM to propose initial groupings.
If doing this, use the following prompt pattern:

```
Below is a list of open-ended annotations describing failures in [DOMAIN DESCRIPTION].
Please group them into a small set of coherent failure categories, where each category
captures similar types of mistakes. Each group should have:
- A short descriptive title (2-5 words)
- A brief one-line definition
- The annotation indices that belong to it

Do not invent new failure types; only cluster based on what is present in the notes.
Aim for 3-7 categories. If an annotation doesn't fit any group, list it separately
as "Uncategorized."

Annotations:
[PASTE ANNOTATIONS HERE]
```

**Critical**: LLM-generated groupings are a starting point, not the final answer. Always
present them to the user for review and adjustment. The user's domain expertise is what
makes the taxonomy meaningful.

## Connecting to Next Steps

After the taxonomy is built, the user typically moves to one of:

- **Building LLM-as-Judge evaluators**: Each failure mode becomes a separate binary
  evaluation prompt. The examples from the taxonomy become few-shot examples in the
  judge prompt.
- **Targeted pipeline improvements**: The highest-frequency failure modes guide where
  to invest engineering effort (prompt changes, tool improvements, guardrails).
- **Generating more failure instances**: For rare failure modes, the user may want to
  synthetically generate queries that trigger them to build a larger labeled dataset.

Mention these next steps when delivering the final taxonomy, so the user knows where
to go from here.
