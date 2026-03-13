---
name: cmd-scope-sweep
description: Final pass to identify missed items, edge cases, and risks before considering a scope done
disable-model-invocation: true
---

### Scope Sweep

Now that we've completed the core work and reviewed it, do a final pass to identify anything we missed or should address before considering this scope "done".

Please check for:

- **Incomplete tasks**: anything you planned to do but didn't get to
- **Overlooked requirements**: anything implied but not explicitly handled
- **Missing questions**: what I should have asked but didn't
- **Hidden assumptions**: any assumptions you made that could be wrong
- **Edge cases**: scenarios that could break or degrade the solution
- **Failure modes**: what happens when inputs are malformed, missing, hostile, or extreme
- **Operational concerns**: deployment, monitoring, logging, maintenance, rollback
- **Security and abuse risks**: permissions, misuse paths, data exposure
- **Performance bottlenecks**: scalability issues, worst-case behavior, cost traps
- **Testing gaps**: what still needs tests or validation
- **User experience gaps**: confusing flows, unclear outputs, poor defaults
- **Integration risks**: dependencies, external APIs, versioning, backward compatibility
- **Future-proofing**: what will become painful in 3-6 months if not handled now

Finally:

- **What is the biggest risk remaining?**
- **If you were reviewing this as a third party, what would you criticize first?**
- **What would you improve if you had one more day?**
