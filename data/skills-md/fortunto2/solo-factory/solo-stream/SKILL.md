---
name: solo-stream
description: Interactive decision-making wizard using STREAM 6-layer framework for founders facing high-stakes choices. Use when user says "help me decide", "should I do this", "evaluate decision", "STREAM analysis", "run decision framework", or "pros and cons". Do NOT use for idea validation with PRD (use /validate).
license: MIT
metadata:
  author: fortunto2
  version: "1.4.1"
  openclaw:
    emoji: "🌊"
allowed-tools: Read, Grep, Glob, Write, AskUserQuestion, mcp__solograph__kb_search
argument-hint: "[decision or dilemma to analyze]"
---

# /stream

Interactive wizard that walks any decision through the STREAM 6-layer framework. Designed for founders making high-stakes choices under uncertainty.

## Steps

1. **Parse the decision** from `$ARGUMENTS`. If empty, ask: "What decision or dilemma do you want to analyze?"

2. **Load framework context** (optional enhancement):
   - If MCP `kb_search` available: `kb_search(query="STREAM framework", n_results=3)` for full framework details.
   - Otherwise, the framework is embedded below.

3. **Walk through 6 layers interactively.** For each layer, explain the concept, ask a clarifying question via AskUserQuestion, then provide assessment.

### Layer 1 — Epistemological (Knowledge)
- Is this within your circle of competence?
- What assumptions are unproven?
- What would change your mind?
- **Ask:** "What do you know for certain about this space? What are you assuming?"

### Layer 2 — Temporal (Time)
- What's the time horizon for results?
- Is this Lindy-compliant (will it matter in 10 years)?
- Reversibility: can you undo this in 6 months?
- **Ask:** "What's your timeline? Is this a 3-month experiment or a 3-year commitment?"

### Layer 3 — Action (Minimum Viable)
- What's the smallest possible first step?
- What are second-order effects?
- Can you test this in a weekend?
- **Ask:** "What's the minimum viable version you could ship in 1-2 weeks?"

### Layer 4 — Stakes (Risk/Reward)
- Asymmetric upside? (small downside, large upside)
- Survivable worst case?
- Opportunity cost of NOT doing this?
- **Ask:** "What's the worst realistic outcome? Can you survive it financially and emotionally?"

### Layer 5 — Social (Network)
- Reputation impact on your network?
- Network effects or viral potential?
- Does this build social capital?
- **Ask:** "Who benefits besides you? Who might be hurt?"

### Layer 6 — Meta (Mortality Filter)
- Is this worth your finite time on earth?
- Does this align with your values?
- Will you regret NOT trying this?
- **Ask:** "If you had only 5 years left, would you still do this?"

4. **Synthesize verdict:**
   - Score each layer 1-10
   - Overall STREAM score (weighted average)
   - **GO** (score > 7) / **PAUSE** (5-7) / **NO-GO** (< 5)
   - Key risk to mitigate
   - Recommended first action

5. **Capture the decision** (optional): Offer to save the decision record. If user wants to save:
   - Write to `docs/decisions/` in the current project directory
   - Format: date + decision summary + verdict

6. **Output structured decision journal:**
   ```
   ## Decision: [topic]

   **Date:** [today]
   **Framework:** STREAM 6-layer

   ### Analysis Summary
   | Layer | Score | Key Finding |
   |-------|-------|-------------|
   | Epistemological | X/10 | ... |
   | Temporal | X/10 | ... |
   | Action | X/10 | ... |
   | Stakes | X/10 | ... |
   | Social | X/10 | ... |
   | Meta | X/10 | ... |

   **Overall STREAM Score: X/10 — GO/PAUSE/NO-GO**

   ### Recommendation
   [Clear recommendation with reasoning]

   ### Next Actions
   1. [action]
   2. [action]
   3. [action]
   ```

## Common Issues

### Questions feel too abstract
**Cause:** Decision not specific enough.
**Fix:** Start with a concrete decision statement: "Should I [action] given [context]?" not just "What should I do?"

### Score seems wrong
**Cause:** Layers weighted equally but some matter more for this decision.
**Fix:** The overall score is a starting point. Pay more attention to the layers most relevant to your situation (e.g., Stakes for financial decisions, Meta for life choices).

### Want to save the decision record
**Cause:** Running in a project without a `docs/decisions/` directory.
**Fix:** Skill saves to `docs/decisions/` in the current project. Create the directory if needed.
