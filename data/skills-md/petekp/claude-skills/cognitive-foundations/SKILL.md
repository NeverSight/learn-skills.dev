---
name: cognitive-foundations
description: Apply cognitive science and HCI research to design decisions. Use when you need the scientific 'why' behind usability, explaining user behavior, understanding perception/memory/attention limits, evaluating cognitive load, assessing mental model alignment, predicting performance with Fitts's/Hick's Law, or grounding interface decisions in research rather than opinion.
---

# Cognitive Foundations

The science of how minds work, and what that means for design.

## When to Use This Skill

- Explaining _why_ a design works or fails (grounded in research, not opinion)
- Evaluating cognitive load or working memory demands
- Predicting user performance (Fitts, Hick-Hyman)
- Diagnosing mental model misalignment
- Justifying design decisions to stakeholders with evidence
- Understanding attention, perception, or memory failures

## Output Contracts

### For Single-Principle Analysis

```markdown
## Cognitive Principle: [Name]

**Principle**: [1-sentence explanation]

**Evidence in Design**: [Where/how this applies]

**Implication**: [Specific, actionable recommendation]

**Confidence**: [High/Medium/Low] — [rationale]
```

### For Cognitive Audit (Comprehensive)

```markdown
## Cognitive Audit: [Screen/Flow Name]

### Working Memory Load
- Items requiring recall: [count]
- Cross-screen memory demands: [Y/N]
- Verdict: [Acceptable / High / Overloaded]

### Attention Demands
- Preattentive features for critical info: [Y/N]
- Competing attention demands: [list]
- Change blindness risk: [areas where changes may go unnoticed]

### Mental Model Alignment
- Expected user model: [what users likely think]
- System behavior: [what actually happens]
- Gap: [mismatch, if any]

### Predictive Laws
- Fitts's Law concerns: [target size/distance issues]
- Hick's Law concerns: [choice overload areas]

### Gulf Analysis
- Gulf of Execution: [unclear how to act?]
- Gulf of Evaluation: [unclear what happened?]

### Violations of Nielsen's Heuristics
| Heuristic | Violation | Severity |
|-----------|-----------|----------|
| ... | ... | 1-4 |

### Recommendations
1. [Highest priority fix]
2. [Second priority]
3. [Third priority]
```

### For Explaining a Failure

```markdown
## Failure Analysis: [What Went Wrong]

**Observed Behavior**: [What users did]

**Cognitive Explanation**: [Which principle explains this]

**Root Cause**: [Design element that caused it]

**Fix**: [Specific change]
```

---

## Quick Reference: Predictive Laws

| Law | Formula | Rule of Thumb |
|-----|---------|---------------|
| **Fitts's Law** | MT = a + b × log₂(2D/W) | Bigger + closer = faster. Screen edges are infinite. |
| **Hick-Hyman** | RT = a + b × log₂(n+1) | More choices = slower. Reduce or organize options. |
| **Steering Law** | T = a + b × (A/W) | Narrow paths are slow. Cascading menus are hard. |
| **Power Law** | T = a × N^(-b) | Practice helps. Design for learnability. |

---

## Quick Reference: Nielsen's 10 Heuristics

| # | Heuristic | Quick Test |
|---|-----------|------------|
| 1 | Visibility of system status | Can user always tell what's happening? |
| 2 | Match system ↔ real world | Language familiar? Metaphors sensible? |
| 3 | User control and freedom | Easy undo? Clear exits? |
| 4 | Consistency and standards | Same words/actions mean same things? |
| 5 | Error prevention | Constraints prevent errors before they occur? |
| 6 | Recognition over recall | Options visible? No memory required? |
| 7 | Flexibility and efficiency | Shortcuts for experts? |
| 8 | Aesthetic and minimalist | Only relevant info? No clutter? |
| 9 | Error recovery | Errors explained in plain language with fix? |
| 10 | Help and documentation | Searchable, task-focused, concise? |

---

## Quick Reference: Working Memory

- **Capacity**: ~4 chunks (not 7)
- **Duration**: ~20 seconds without rehearsal
- **Test**: Count items user must hold in mind across screens/steps

**Red flags**:
- "Remember this code and enter it on the next page"
- Multi-step forms without visible progress/state
- Complex comparisons requiring mental tracking

---

## Quick Reference: Preattentive Features

Detected in <200ms, no focused attention required:
- **Color** (hue, saturation)
- **Size** (length, area)
- **Orientation** (angle)
- **Motion** (flicker, direction)
- **Shape** (curvature, enclosure)

**Use for**: Critical info, errors, changes, status
**Don't use for**: Everything (loses signal value)

---

## Cognitive Load Checklist

Quick assessment for any interface:

| Factor | Low Load | High Load |
|--------|----------|-----------|
| Choices visible | 2-4 options | 10+ options |
| Memory demands | Recognition | Recall |
| Steps to goal | 1-3 clicks | 5+ clicks |
| Interruptions | None | Frequent modals |
| Novel elements | Familiar patterns | New conventions |
| Error recovery | Clear undo | Destructive actions |
| Visual complexity | Clean, grouped | Dense, undifferentiated |

**Scoring**: Each "High Load" = +1. Score >3 = redesign needed.

---

## Common Violations → Principle

| Symptom | Likely Violation | Fix |
|---------|------------------|-----|
| Users don't notice changes | Change blindness | Animate, highlight transitions |
| Users can't find the button | Poor Fitts's Law | Increase size, reduce distance |
| Users freeze at options | Hick's Law overload | Reduce choices, progressive disclosure |
| Users forget mid-task | Working memory exceeded | Show state, don't require recall |
| Users misunderstand state | Gulf of Evaluation | Better feedback, visibility |
| Users click wrong thing | Poor affordance/signifier | Clearer visual treatment |
| Users make same error repeatedly | Mode error | Visible mode indicators |
| Users abandon complex forms | Cognitive load | Chunk, scaffold, save progress |

---

## Process

1. **Identify cognitive demands** — What is the interface asking the user to perceive, remember, decide, or do?
2. **Match to principles** — Which cognitive constraints or laws apply?
3. **Evaluate alignment** — Does the design respect or violate these?
4. **Recommend changes** — Specific modifications grounded in the principle

---

## Deep Reference Files

For comprehensive principles and research:

- [PSYCHOLOGY.md](PSYCHOLOGY.md) — Perception, memory, attention, biases, emotion, motivation
- [HCI-THEORY.md](HCI-THEORY.md) — Norman's model, predictive laws, error theory, research methods, heuristics

### Primary Sources

- [A Feature-Integration Theory of Attention.md](A%20Feature-Integration%20Theory%20of%20Attention.md) — Treisman & Gelade on preattentive processing (informs: Quick Reference: Preattentive Features)
- [Judgment under Uncertainty- Heuristics and Biases.md](Judgment%20under%20Uncertainty-%20Heuristics%20and%20Biases.md) — Kahneman & Tversky on cognitive biases (informs: PSYCHOLOGY.md § Decision Making)

---

## Key Researchers

- **Don Norman**: Affordances, gulfs, emotional design
- **Daniel Kahneman**: Dual process theory, heuristics and biases
- **Stuart Card**: GOMS, information foraging, Fitts's Law
- **Anne Treisman**: Feature integration, preattentive processing
- **Jakob Nielsen**: Usability heuristics, discount usability
- **Ben Shneiderman**: Direct manipulation, golden rules

---

## Remember

- Cognitive science explains _why_ design principles work
- Individual differences exist—design for variability, not averages
- Lab findings may not generalize (ecological validity matters)
- Theory informs but doesn't replace observing real users
- When in doubt, reduce cognitive load—users have less capacity than you think
