---
name: design-engineering
description: "Translate design intent into production components or improve collaboration between design and engineering."
license: MIT
---

# Design Engineering

Design engineering is shared responsibility for the interface in production, not a relay race between finished mockups and ticketed implementation.

## Defaults

1. Prefer handshakes over handovers: involve implementation constraints early.
2. Map design structure to code structure deliberately.
3. Prototype to learn; ship with production rigor.
4. Keep taste attached to materials knowledge (CSS, framework rendering, tokens, a11y).
5. Optimise for reduced translation loss between intent and implementation.

## Translation map

| Design concept | Code concept |
| --- | --- |
| Frame / auto layout | Stack, flex, grid |
| Component + variants | Component API + props/state |
| Local styles | Tokens + semantic classes |
| Prototype interactions | Real state, routes, and motion |
| Redlines | Defaults encoded in the component |

## Prefer / Reject

| Prefer | Reject |
| --- | --- |
| Shared ownership of quality | "Design is done" / "Dev will polish" |
| Constraints in the exploration phase | Surprising feasibility after visual lock |
| Production concerns during prototyping | Treating vibe demos as launch-ready |
| Tokenised systems | One-off values that cannot survive themes |

## Review checklist

- [ ] Did engineering constraints inform the design direction early?
- [ ] Does the component API match the variant model people design with?
- [ ] Are tokens used instead of disconnected raw values?
- [ ] Are accessibility and empty/error states designed, not deferred?
- [ ] Is the prototype honest about what still needs production work?
- [ ] Can design and engineering point to the same source of truth for behaviour?

## Source essays

- Design for handshakes, not handovers
- A manifesto on design engineering
- Thinking in design code
- The design engineer
