---
name: observe
description: >
  Sustained neutral pattern recognition across systems without urgency or
  intervention. Maps naturalist field study methodology to AI reasoning:
  framing the observation target, witnessing with sustained attention,
  recording patterns, categorizing findings, generating hypotheses, and
  archiving a pattern library for future reference. Use when a system's
  behavior is unclear and action would be premature, when debugging an
  unknown root cause, when a codebase change needs its effects witnessed
  before further changes, or when auditing own reasoning patterns for
  biases or recurring errors.
license: MIT
allowed-tools: Read Grep Glob
metadata:
  author: Philipp Thoss
  version: "1.0"
  domain: esoteric
  complexity: intermediate
  language: natural
  tags: esoteric, observation, pattern-recognition, naturalist, field-study, meta-cognition
---

# Observe

Conduct a structured observation session — framing the observation target, witnessing with sustained neutral attention, recording patterns without interpretation, categorizing findings, generating hypotheses from patterns, and archiving the observations for future reference.

## When to Use

- A system's behavior is unclear and action without observation would be premature
- Debugging a problem where the cause is unknown — observation before intervention prevents masking symptoms
- A codebase or system has been changed and the effects need to be witnessed before further changes are made
- Understanding user behavior patterns over a conversation to improve future interactions
- Auditing own reasoning patterns for biases, habits, or recurring errors
- After `learn` has built a model that needs validation through observation of the system in action

## Inputs

- **Required**: Observation target — a system, codebase, behavior pattern, user interaction, or reasoning process to observe
- **Optional**: Observation duration/scope — how long or deep to observe before concluding
- **Optional**: Specific question or hypothesis to guide observation focus
- **Optional**: Prior observations to compare against (detecting change over time)

## Procedure

### Step 1: Frame — Set the Observation Focus

Define what is being observed, why, and from what perspective.

```
Observation Protocol by System Type:
┌──────────────────┬──────────────────────────┬──────────────────────────┐
│ System Type      │ What to Observe          │ Categories to Watch      │
├──────────────────┼──────────────────────────┼──────────────────────────┤
│ Codebase         │ File structure, naming   │ Patterns, anti-patterns, │
│                  │ conventions, dependency  │ consistency, dead code,  │
│                  │ flow, test coverage,     │ documentation quality,   │
│                  │ error handling patterns  │ coupling between modules │
├──────────────────┼──────────────────────────┼──────────────────────────┤
│ User behavior    │ Question patterns,       │ Expertise signals, pain  │
│                  │ vocabulary evolution,    │ points, unstated needs,  │
│                  │ repeated requests,       │ learning trajectory,     │
│                  │ emotional signals        │ communication style      │
├──────────────────┼──────────────────────────┼──────────────────────────┤
│ Tool / API       │ Response patterns, error │ Rate limits, edge cases, │
│                  │ conditions, latency,     │ undocumented behavior,   │
│                  │ output format variations │ state dependencies       │
├──────────────────┼──────────────────────────┼──────────────────────────┤
│ Own reasoning    │ Decision patterns, tool  │ Biases, habits, blind    │
│                  │ selection habits, error  │ spots, strengths,        │
│                  │ recovery approaches,     │ recurring failure modes, │
│                  │ communication patterns   │ over/under-confidence    │
└──────────────────┴──────────────────────────┴──────────────────────────┘
```

1. Select the observation target and name it explicitly
2. Define the observation boundary: what is included and what is out of scope
3. State the observation stance: "I am observing, not intervening"
4. If there is a guiding question, state it — but hold it lightly; be willing to notice things outside the question's scope
5. Choose the appropriate categories from the matrix above

**Expected:** A clear frame that directs attention without constraining it. The observer knows where to look and what categories to sort observations into, but remains open to the unexpected.

**On failure:** If the observation target is too broad ("observe everything"), narrow to one subsystem or one behavior pattern. If the target is too narrow ("observe this one variable"), zoom out to the surrounding context — the interesting patterns are often at the edges.

### Step 2: Witness — Sustained Neutral Attention

Hold attention on the observation target without interpreting, judging, or intervening.

1. Begin systematic observation: read files, trace execution paths, review conversation history — whatever the target requires
2. Record what is seen, not what it means — description before interpretation
3. Resist the urge to fix problems encountered during observation — note them and continue
4. Resist the urge to explain patterns before enough observations accumulate
5. If attention drifts to a different target, note the drift (it may be meaningful) and return to the frame
6. Maintain observation for a defined period: at least 3-5 distinct data points before moving to categorization

**Expected:** A collection of raw observations — specific, concrete, and free from interpretation. Observations read like field notes: "File X imports Y but does not use function Z. File A has 300 lines; file B has 30 lines and covers similar functionality."

**On failure:** If observation immediately triggers analysis ("this is wrong because..."), the analytical habit is overriding the observational stance. Consciously separate the phases: write the observation as a fact, then write the interpretation as a separate note labeled "hypothesis." If neutrality is impossible (strong reaction to what is observed), note the reaction itself as data: "I noticed strong concern when observing X — this may indicate a significant issue or may indicate my bias."

### Step 3: Record — Capture Raw Patterns

Transcribe observations into a structured format while they are fresh.

1. List each observation as a single statement of fact (what was seen, where, when)
2. Group naturally similar observations — do not force grouping, but notice when observations cluster
3. Note frequency: did this pattern appear once, occasionally, or pervasively?
4. Note contrasts: where did the pattern break? Exceptions are often more informative than rules
5. Note temporal patterns: did the observation change over time, or was it static?
6. Capture exact evidence: file paths, line numbers, specific words, concrete examples

**Expected:** A structured record of 5-15 discrete observations, each with specific evidence. The record should be detailed enough that another observer could verify each observation independently.

**On failure:** If observations are too abstract ("the code seems messy"), they need grounding in specifics — which files, which patterns, what makes it messy? If observations are too granular ("line 47 has a space before the brace"), zoom out to the pattern level — is this a one-off or a systemic issue?

### Step 4: Categorize — Organize Findings

Sort observations into meaningful categories without yet explaining them.

1. Review all recorded observations and look for natural groupings
2. Assign each observation to a category from the Step 1 matrix, or create new categories if needed
3. Within each category, rank observations by frequency and significance
4. Identify which categories have many observations (well-documented areas) and which have few (potential blind spots)
5. Look for cross-category patterns: does the same underlying pattern manifest differently in different categories?
6. Note any observations that do not fit any category — outliers are often the most interesting data

**Expected:** A categorized observation map with clear groupings. Each category has specific observations supporting it. The map shows both patterns and gaps.

**On failure:** If categorization feels forced, the observations may not have natural groupings — they may be a collection of unrelated findings, which is itself a finding (the system may lack coherent structure). If everything fits neatly into one category, the observation scope was too narrow — zoom out.

### Step 5: Theorize — Generate Hypotheses from Patterns

Now — and only now — begin interpreting the observations.

1. For each major pattern observed, propose a hypothesis: "This pattern exists because..."
2. For each hypothesis, identify supporting evidence from the observations
3. For each hypothesis, identify what counter-evidence would disprove it
4. Rank hypotheses by explanatory power: which one explains the most observations?
5. Generate at least one contrarian hypothesis: "The obvious explanation is X, but it could also be Y because..."
6. Identify which hypotheses are testable and which are speculative

**Expected:** 2-4 hypotheses that explain the major patterns, each supported by specific observations. At least one hypothesis should be surprising or contrarian. The distinction between observation and interpretation is maintained — it is clear which parts are data and which are theory.

**On failure:** If no hypotheses form, the observations may need more time to accumulate — return to Step 2. If too many hypotheses form (everything is "maybe"), select the 2-3 with the strongest evidence and set the rest aside. If only obvious hypotheses form, force a contrarian view: "What if the opposite were true?"

### Step 6: Archive — Store the Pattern Library

Preserve the observations and hypotheses for future reference.

1. Summarize the key findings: 3-5 patterns with evidence
2. State the leading hypotheses and their confidence levels
3. Note what was not observed (potential blind spots)
4. Identify follow-up observations that would strengthen or weaken the hypotheses
5. If the patterns are durable (will be relevant across sessions), consider updating MEMORY.md
6. Tag the observations with context: when they were made, what prompted them, what scope was covered

**Expected:** An archive that future observation sessions can build on. The archive distinguishes clearly between observations (data) and hypotheses (interpretation). It is honest about confidence levels and gaps.

**On failure:** If the observations do not feel worth archiving, they may have been too shallow — or they may be genuinely routine (not every observation session produces insights). Archive even negative results: "Observed X and found no anomalies" is useful future context.

## Validation

- [ ] The observation frame was set before any observation began (not free-form wandering)
- [ ] Raw observations were recorded as facts before any interpretation
- [ ] At least 5 discrete observations were captured with specific evidence
- [ ] Interpretation (hypotheses) was clearly separated from observation (data)
- [ ] At least one surprising or contrarian finding was generated
- [ ] The archived record is specific enough for another observer to verify

## Common Pitfalls

- **Premature intervention**: Seeing a problem and fixing it immediately, losing the opportunity to understand the broader pattern it belongs to
- **Observation bias**: Seeing what is expected rather than what is present. Expectations filter perception — the clearing step in Step 1 mitigates this but does not eliminate it
- **Analysis paralysis**: Observing endlessly without ever moving to action. Set a time or data-point limit and commit to concluding
- **Narrative imposition**: Constructing a story that connects observations even when the connections are weak. Not all observations form a coherent narrative — disconnected findings are valid
- **Confusing familiarity with understanding**: "I have seen this before" is not the same as "I understand why this is here." Prior exposure can create false confidence
- **Ignoring own reactions**: The observer's emotional or cognitive reactions to observations are data. A sense of confusion, boredom, or alarm about a system often contains real signal

## Related Skills

- `observe-guidance` — the human-guidance variant for coaching a person in systematic observation
- `learn` — observation feeds learning by providing raw data for model-building
- `listen` — outward-focused attention toward user signals; observation is broader-scope attention toward any system
- `remote-viewing` — intuitive exploration that can be validated through systematic observation
- `meditate` — develops the sustained attention capacity that observation requires
- `awareness` — threat-focused situational awareness; observation is curiosity-driven rather than defense-driven
