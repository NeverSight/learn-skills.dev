---
name: atlas-motion
description: "Build interface animations and physical gestures, diagnose animation stutter or dropped frames, or identify worthwhile opportunities for motion."
disable-model-invocation: false
---

# Atlas Motion

Choose from the requested outcome and context, honoring an explicit choice. Ask only when ambiguity changes the method. Read [Scope and ownership](references/ownership.md) and the selected methods.

| Mode | Need | Read and follow |
| --- | --- | --- |
| Animate | Construct an interface animation or transition | [Animate](references/animate/animate.md) |
| Fluid | Direct manipulation, momentum and interruptible springs | [Fluid](references/fluid/apple-design.md) |
| Performance | Diagnose animation stutter, dropped frames or rendering cost | [Performance](references/performance/animation-performance.md) |
| Opportunities | Find moments that benefit from motion and reject unnecessary motion | [Opportunities](references/opportunities/index.md) |

Performance diagnoses and reports first; repairs require a request. Opportunities is read-only toward product code. A request for discovery does not authorize building its suggestions. Animate and Fluid can complement one another for authorized construction. Preserve project motion tokens and accepted visual identity, following [Motion ownership](references/motion-ownership.md).

Existing-motion audits and diff reviews belong to Atlas Review. React Native/Expo construction is outside this package; explain that gap when requested rather than apply web recipes to native code.
