---
name: learn
description: >
  AI systematic knowledge acquisition from unfamiliar territory — deliberate
  model-building with feedback loops. Maps spaced repetition principles to
  AI reasoning: survey the territory, hypothesize structure, explore with
  probes, integrate findings, verify understanding, and consolidate for
  future retrieval. Use when encountering an unfamiliar codebase or domain,
  when a user asks about a topic requiring genuine investigation rather than
  recall, when multiple conflicting sources require building a coherent model,
  or when preparing to teach a topic and deep understanding is required first.
license: MIT
allowed-tools: Read Grep Glob WebFetch WebSearch
metadata:
  author: Philipp Thoss
  version: "1.0"
  domain: esoteric
  complexity: intermediate
  language: natural
  tags: esoteric, learning, knowledge-acquisition, meta-cognition, model-building
---

# Learn

Conduct a structured knowledge acquisition session — surveying unfamiliar territory, building initial models, testing them through deliberate exploration, integrating findings into coherent understanding, and consolidating for durable retrieval.

## When to Use

- Encountering an unfamiliar codebase, framework, or domain with no prior context
- A user asks about a topic outside current working knowledge and the answer requires genuine investigation, not recall
- Multiple conflicting sources or patterns exist and a coherent mental model needs to be built from scratch
- After `remote-viewing` surfaces intuitive leads that need systematic validation
- Preparing to `teach` a topic — the AI must first understand it deeply enough to explain it

## Inputs

- **Required**: Learning target — a topic, codebase area, API, domain concept, or technology to understand
- **Optional**: Scope boundary — how deep to go (surface survey vs. deep expertise)
- **Optional**: User's purpose — why this knowledge matters (guides which aspects to prioritize)
- **Optional**: Known starting points — files, docs, or concepts already familiar

## Procedure

### Step 1: Survey — Map the Territory

Before attempting to understand anything, map the landscape to identify what exists.

```
Learning Modality Selection:
┌──────────────────┬──────────────────────────┬──────────────────────────┐
│ Territory Type   │ Primary Modality         │ Tool Pattern             │
├──────────────────┼──────────────────────────┼──────────────────────────┤
│ Codebase         │ Structural mapping —     │ Glob for file tree,      │
│                  │ find entry points, core  │ Grep for exports/imports,│
│                  │ modules, boundaries      │ Read for key files       │
├──────────────────┼──────────────────────────┼──────────────────────────┤
│ API / Library    │ Interface mapping —      │ WebFetch for docs,       │
│                  │ find public surface,     │ Read for examples,       │
│                  │ types, configuration     │ Grep for usage patterns  │
├──────────────────┼──────────────────────────┼──────────────────────────┤
│ Domain concept   │ Ontology mapping —       │ WebSearch for overviews,  │
│                  │ find core terms,         │ WebFetch for definitions,│
│                  │ relationships, debates   │ Read for local notes     │
├──────────────────┼──────────────────────────┼──────────────────────────┤
│ User's context   │ Conversational mapping   │ Read conversation,       │
│                  │ — find stated goals,     │ Read MEMORY.md,          │
│                  │ preferences, constraints │ Read CLAUDE.md           │
└──────────────────┴──────────────────────────┴──────────────────────────┘
```

1. Identify the territory type and select the primary modality
2. Perform a broad scan — not reading deeply, but identifying landmarks (key files, entry points, core concepts)
3. Note the boundaries: what is in scope, what is adjacent, what is out of scope
4. Identify gaps: areas that look important but are opaque from the surface
5. Create a rough map: list the major components and their apparent relationships

**Expected:** A skeletal map of the territory with 5-15 landmarks identified. A sense of which areas are clear from the surface and which require deeper investigation. No understanding yet — just a map.

**On failure:** If the territory is too large to survey, narrow scope immediately. Ask: "What is the minimum I need to understand to serve the user's purpose?" If the territory has no clear entry point, start from the output (what does this system produce?) and trace backward.

### Step 2: Hypothesize — Build Initial Models

From the survey, construct initial hypotheses about how the system works.

1. Formulate 2-3 hypotheses about the territory's structure or behavior
2. State each hypothesis clearly: "I believe X because I observed Y"
3. For each hypothesis, identify what evidence would confirm it and what would refute it
4. Rank hypotheses by confidence: which feels most supported, which is shakiest
5. Identify the highest-value hypothesis to test first (the one that, if confirmed, would unlock the most understanding)

**Expected:** Concrete, falsifiable hypotheses — not vague impressions. Each has a test that would confirm or refute it. The hypotheses collectively cover the most important aspects of the territory.

**On failure:** If no hypotheses form, the survey was too shallow — return to Step 1 and read 2-3 landmarks in depth. If all hypotheses feel equally uncertain, start with the simplest one (Occam's razor) and build from there.

### Step 3: Explore — Probe and Test

Systematically test each hypothesis through targeted investigation.

1. Select the highest-priority hypothesis
2. Design a minimal probe: what is the smallest investigation that would confirm or refute it?
3. Execute the probe (read a file, search for a pattern, test an assumption)
4. Record the result: confirmed, refuted, or modified
5. If refuted, update the hypothesis based on the new evidence
6. If confirmed, probe deeper: does the hypothesis hold at the edges, or only in the center?
7. Move to the next hypothesis and repeat

**Expected:** At least one hypothesis tested to conclusion. The mental model is beginning to take shape — some parts confirmed, some revised. Surprises are noted as particularly valuable data.

**On failure:** If probes consistently produce ambiguous results, the hypotheses may be testing the wrong things. Step back and ask: "What would someone who understands this system consider the most important fact?" Probe for that instead.

### Step 4: Integrate — Build Mental Model

Synthesize findings into a coherent model that connects the pieces.

1. Review all confirmed hypotheses and revised models
2. Identify the central organizing principle: what is the "spine" that everything connects to?
3. Map relationships: which components depend on which? What flows where?
4. Identify the surprising findings — these often contain the deepest insight
5. Look for patterns that repeat across different parts of the territory
6. Build a mental model that can predict behavior: "Given input X, I expect Y because Z"

**Expected:** A coherent mental model that explains the territory's structure and predicts its behavior. The model should be expressible in 3-5 sentences and should make specific claims, not vague generalizations.

**On failure:** If the pieces do not integrate into a coherent model, there may be a fundamental misunderstanding in one of the earlier hypotheses. Identify the piece that does not fit and re-test it. Alternatively, the territory may genuinely be incoherent (poorly designed systems exist) — note this as a finding rather than forcing coherence.

### Step 5: Verify — Challenge Understanding

Test the mental model by making predictions and checking them.

1. Use the model to make 3 specific predictions about the territory
2. Test each prediction through investigation (not by assuming it is true)
3. For each confirmed prediction, confidence increases
4. For each refuted prediction, identify where the model is wrong and correct it
5. Identify edge cases: does the model hold at the boundaries, or does it break down?
6. Ask: "What would surprise me?" — then check if that surprise is possible

**Expected:** The mental model survives at least 2 of 3 prediction tests. Where it breaks, the failure is understood and the model is corrected. The model now has both confirmed strengths and known limitations.

**On failure:** If most predictions fail, the mental model has a fundamental flaw. This is actually valuable information — it means the territory works differently than expected. Return to Step 2 with the new evidence and rebuild the hypotheses from scratch. The second attempt will be much faster because the wrong models have been eliminated.

### Step 6: Consolidate — Store for Retrieval

Capture the learning in a form that supports future retrieval and application.

1. Summarize the mental model in 3-5 sentences
2. Note the key landmarks — the 3-5 most important things to remember
3. Record any counterintuitive findings that might be forgotten
4. Identify related topics that this learning connects to
5. If the learning is durable (will be needed across sessions), update MEMORY.md
6. If the learning is session-specific, note it as context for the current conversation
7. State what remains unknown — honest gaps are more useful than false confidence

**Expected:** A concise, retrievable summary that captures the essential understanding. Future references to this topic can start from this summary rather than re-learning from scratch.

**On failure:** If the learning resists summarization, it may not yet be fully integrated — return to Step 4. If the learning seems too obvious to be worth storing, consider that what feels obvious now may not feel obvious in a fresh context. Store the non-obvious parts.

## Validation

- [ ] A survey was conducted before any deep investigation (map before dive)
- [ ] Hypotheses were explicitly stated and tested, not assumed
- [ ] At least one hypothesis was revised based on evidence (indicates genuine learning)
- [ ] The mental model makes specific, testable predictions about the territory
- [ ] Known unknowns are identified alongside known knowns
- [ ] The consolidated summary is concise enough to be useful for future retrieval

## Common Pitfalls

- **Skipping the survey**: Diving into detail before understanding the landscape wastes time on unimportant areas and misses the big picture
- **Unfalsifiable hypotheses**: "This is probably complex" cannot be tested. "This module handles authentication because it imports crypto" can be
- **Confirmation bias during exploration**: Seeking only evidence that supports the initial hypothesis while ignoring contradictions
- **Premature consolidation**: Storing a model before it has been tested leads to confidently wrong future predictions
- **Perfectionism**: Attempting to learn everything before applying any knowledge. Learning is iterative — use partial understanding, then refine
- **Learning without purpose**: Acquiring knowledge with no application in mind produces unfocused, shallow understanding

## Related Skills

- `learn-guidance` — the human-guidance variant for coaching a person through structured learning
- `teach` — knowledge transfer calibrated to a learner; builds on the model constructed here
- `remote-viewing` — intuitive exploration that surfaces leads for systematic learning to validate
- `meditate` — clearing prior context noise before entering a new learning territory
- `observe` — sustained neutral pattern recognition that feeds learning with raw data
