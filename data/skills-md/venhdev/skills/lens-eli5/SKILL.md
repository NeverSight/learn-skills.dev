---
name: lens-eli5
description: "Deconstruct complex technical concepts, architecture, or code into intuitive physical analogies and beginner-friendly mental models."
---

# lens-eli5 — Intuitive Mental Model Engine

## Operating Invariants

- **Jargon Grounding**: Pair every technical term immediately with an everyday physical equivalent; avoid ungrounded industry jargon.
- **Cognitive Density**: Focus strictly on core mechanics; omit historical chronology, theoretical proofs, and tangential edge cases.
- **Context Isolation**: Explain the inquiry in isolation without derailing active session tasks or mutating project scope.

## Canonical Output Contract

```markdown
# Lens [ELI5]: <Target Concept / Symbol / Mechanism>

## 1. Core Intuition (The Metaphor)
> <Tangible physical analogy anchoring the concept to an everyday real-world object or interaction>

## 2. Why Does This Exist?
- **Without It (The Pain)**: <Concrete failure, bottleneck, or bug that occurs>
- **With It (The Fix)**: <What becomes predictable, simple, or safe>

## 3. How It Works
1. **<Step N Name>**: <Mechanical phase in plain language — repeat steps as needed>

## 4. The Mental Trap
- **Common Misconception**: <What beginners wrongly assume>
- **Reality**: <The decisive distinction>
```
