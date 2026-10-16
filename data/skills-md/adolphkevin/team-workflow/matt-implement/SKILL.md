---
name: matt-implement
description: "Implement a piece of work based on a spec or set of tickets."
disable-model-invocation: true
---

Before using this method, read the [knowledge and team rules](../team-workflow/references/matt-integration.md): project knowledge comes from team-knowledge (`tw brief`).


Implement the work described by the user in the spec or tickets.

For an existing team task, read the [team delivery rules](../team-workflow/references/team-delivery.md) and use `start` to read its shared materials and actual implementation readiness before editing source or dispatching an implementer. Carry forward valid approvals and assignments; approved work starts without another kickoff confirmation. Use the task's own assessment and review path, including combined review for simple work. A standalone MATT call stays lightweight.

If the user passes a ticket reference, fetch it from the issue tracker and state its title before starting. If the reference is ambiguous, ask.

Use the bundled `matt-tdd` method when test-first development fits the task, at existing or agreed public boundaries.

Preserve known issue IDs and unresolved decisions through review and handoff. Match each acceptance to actual entrypoints and execution or manual observation evidence; retain unverified coverage explicitly. Run the appropriate focused checks, then the project-required wider checks for the actual risk. Report the actual results.

Once done, call the bundled skill `matt-code-review` to review the work.

Finish the logical task under the shared knowledge and team rules, updating `.tw` knowledge in the same change. Commit only when requested or already authorized.
