---
name: interview-me
description: "Conduct an adaptive structured interview that elicits tacit knowledge, requirements, preferences, or decisions and summarizes them explicitly. Use when the needed information is in the user's head and cannot be recovered from project files. Not for adversarial oral examination; use $grill-me."
disable-model-invocation: true
argument-hint: "[brief topic or 'start fresh']"
allowed-tools: Read, Write, Edit
---

# Research Interview

Conduct a structured interview to help formalise a research idea into a concrete specification.

**Input:** `$ARGUMENTS` — a brief topic description or "start fresh" for open-ended exploration.

---

## How This Works

This is a **conversational** skill. Instead of producing a report immediately, you conduct an interview by asking questions one at a time, probing deeper based on answers, and building toward a structured research specification.

**Do NOT use the available structured-question mechanism.** Ask questions directly in your text responses, one or two at a time. Wait for the user to respond before continuing.

Before starting, read `.context/profile.md` and `.context/projects/_index.md` to understand the researcher's areas and active projects. If the topic relates to an existing project, read its context file too.

---

## Interview Structure

### Phase 1: The Big Picture (1–2 questions)
- "What phenomenon or puzzle are you trying to understand?"
- "Why does this matter? Who should care about the answer?"

### Phase 2: Theoretical Motivation (1–2 questions)
- "What's your intuition for why X happens / what drives Y?"
- "What would standard theory predict? Do you expect something different?"

### Phase 3: Data and Setting (1–2 questions)
- "What data do you have access to, or what data would you ideally want?"
- "Is there a specific context, time period, or institutional setting you're focused on?"

### Phase 4: Identification (1–2 questions)
- "Is there a natural experiment, policy change, or source of variation you can exploit?"
- "What's the biggest threat to a causal interpretation?"

### Phase 5: Expected Results (1–2 questions)
- "What would you expect to find? What would surprise you?"
- "What would the results imply for policy or theory?"

### Phase 6: Contribution (1 question)
- "How does this differ from what's already been done? What's the gap you're filling?"

---

## Adapting to the Research Area

the user's work spans multiple disciplines. Adapt the interview to the domain:

- **Human-AI collaboration / MCDM**: Focus on decision architecture, experimental design, behavioural measures, and what "better" decisions look like.
- **Multi-agent systems**: Focus on agent design, interaction protocols, equilibrium concepts, and simulation methodology.
- **Organisational behaviour**: Focus on mechanisms, field vs. lab settings, mediators/moderators, and internal validity.
- **Carbon markets / environmental**: Focus on policy variation, compliance data, market microstructure, and welfare implications.

If the research is non-quantitative (conceptual, design science, qualitative), adjust: replace "Identification" with "Analytical Framework" and "Data" with "Empirical/Evidence Strategy".

---

### Phase 7: Field Calibration (optional, auto-triggered)

**Auto-triggers when:** the project has no `.context/field-calibration.md`, or it exists but still contains `<placeholders>`.

**Skip when:** the file already exists with populated content, unless the user explicitly asks to update it.

Ask 2–3 targeted questions:

- "Which journals or conferences are you targeting? I can cross-reference venue rankings." (Use `.context/resources/venue-rankings.md` to validate and suggest alternatives.)
- "Which seminal papers would a reviewer in this subfield expect to see cited?"
- "What's the typical identification strategy in this subfield — and what do reviewers most often attack?"

After the interview, populate `.context/field-calibration.md` from answers combined with Research Spec content. Use the template at `skills/init-project-research/templates/field-calibration.md`.

If field-calibration already exists with content: ask the user whether to update specific sections or keep as-is.

---

## After the Interview

Once you have enough information (typically 5–8 exchanges), produce a **Research Specification Document**:

```markdown
# Research Specification: [Title]

**Date:** [YYYY-MM-DD]
**Researcher:** the user

## Research Question

[Clear, specific question in one sentence]

## Motivation

[2–3 paragraphs: why this matters, theoretical context, policy relevance]

## Hypothesis

[Testable prediction with expected direction]

## Empirical Strategy

- **Method:** [e.g., DiD, experiment, simulation, case study]
- **Treatment/Manipulation:** [What varies]
- **Control/Comparison:** [Comparison group or baseline]
- **Key identifying assumption:** [What must hold]
- **Robustness checks:** [Pre-trends, placebo, alternative specifications]

## Data

- **Primary dataset:** [Name, source, coverage]
- **Key variables:** [Treatment, outcome, controls]
- **Sample:** [Unit of observation, time period, N]

## Expected Results

[What the researcher expects to find and why]

## Contribution

[How this advances the literature — 2–3 sentences]

## Open Questions

[Issues raised during the interview that need further thought]
```

**Save to:** the project root or `docs/` if inside a research project, or present to the user for placement.

**Also produces** (if Phase 7 triggered): `.context/field-calibration.md` — the per-project domain profile that agents use to calibrate reviews.

---

## Interview Style

- **Be curious, not prescriptive.** Your job is to draw out the researcher's thinking, not impose your own ideas.
- **Probe weak spots gently.** If the identification strategy sounds fragile, ask "What would a sceptic say about...?" rather than "This won't work because..."
- **Build on answers.** Each question should follow from the previous response.
- **Know when to stop.** If the researcher has a clear vision after 4–5 exchanges, move to the specification. Don't over-interview.
- **Use British English** throughout (the user's preference).

---

## Cross-References

| Skill | When to use instead/alongside |
|-------|-------------------------------|
| `devils-advocate` | After the spec is written — stress-test the idea |
| `literature` | To find related work mentioned during the interview |
| `init-project-research` | To scaffold a project once the spec is approved (seeds empty field-calibration) |
