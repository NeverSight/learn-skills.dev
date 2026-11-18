---
name: dxe-ai-output-judgement
description: "Critique generated UI, copy, or code when the user requests a quality review of AI output."
license: MIT
---

# AI Output Judgement

Models output the median of their training data. Slop appears when that median is accepted uncritically. The job is to read the draft specifically and fix the last mile.

## Defaults

1. Treat generated output as scaffolding, never as the finished answer.
2. Review materials, not only screenshots.
3. Name concrete failures (padding, tokens, semantics, motion, identity), not vibes.
4. Prefer system references over one-off values the model invented.
5. Keep human taste on the exit path to production.

## Common median failures

- Hardcoded hex/rgb instead of semantic tokens
- `div` controls instead of native elements
- `transition: all` / linear timing for interactive motion
- Generic shadows, radii, and 24px padding
- Missing empty, error, disabled, and reduced-motion states
- React keys/identity that remount and reset state
- Accessibility bolted on after the visual pass

## Review rubric

1. **Semantics** — correct element and contract?
2. **Tokens** — colour, space, type, elevation from the system?
3. **Layout** — intentional hierarchy, not template residue?
4. **Motion** — physics/interruptibility where needed?
5. **States** — hover/focus/disabled/loading/empty/error?
6. **Fit** — matches neighbouring product surfaces?

## Prefer / Reject

| Prefer | Reject |
| --- | --- |
| Draft → critique → revise | Prompt → ship |
| Specific notes ("12px on spacing scale") | "Make it nicer" |
| System-aware replacements | Fresh one-off styling |
| Knowing when the model is wrong | Blind trust because the preview looks polished |

## Review checklist

- [ ] Did anyone read the code/CSS, not just the preview?
- [ ] Are tokens used everywhere values repeat?
- [ ] Are native semantics intact?
- [ ] Is motion intentional and interruptible?
- [ ] Do edge states exist?
- [ ] Would you defend every leftover default as deliberate?

## Source essays

- The slop isn't the models
- Force-multiplying design
- AI as pair design
- On giving AI taste
