---
name: explain-codebase
description: Trace and explain how an existing code path or subsystem works.
---

# Explain Codebase

Explain current behavior at the level of detail the user needs. Follow what the system actually does; do not replace the explanation with annotated code, design criticism, or invented history.

## Boundaries

- This skill is read-only. Do not edit code or documentation.
- Explain observed behavior before judging it. If the request also asks for problems or improvements, finish a self-contained explanation first, then use the relevant audit skill and keep its findings separate.
- A failing, incorrect, or slow path can still be the subject of a read-only explanation. Use `diagnosing-bugs` when the user asks to investigate the cause of a reported problem or to fix it, rather than merely to explain the path. Preserve investigation-only and no-edit boundaries; a request to establish a cause does not authorize a fix.
- State historical motivation only when an ADR, issue, commit, documentation, or another authoritative record supports it. Otherwise distinguish current purpose from inferred rationale.
- Resolve minor ambiguity by stating the working interpretation and proceeding. Ask only when different interpretations would produce materially different explanations.

## Trace the System

1. **Choose the level of detail.** Identify whether the user needs a function walkthrough, a feature flow, or a subsystem overview. Read `CONTEXT.md` and relevant ADRs when they exist, but verify their claims against current code.
2. **Find the real entry point.** Start from the trigger: a caller, route, event, job, command, user action, or public function. Use repository search and runtime wiring; do not infer the starting point from filenames.
3. **Follow the execution.** Read the calls and event handlers needed to explain how the trigger produces an output, state change, side effect, or external call. Track:
   - the module and function responsible for each step
   - the data entering, leaving, and changing at that step
   - important branches, validation, errors, retries, and asynchronous handoffs
   - state ownership, persistence, caches, queues, and external dependencies
   - seams where responsibility passes to another module or system
4. **Check runtime selection.** Confirm which adapter, implementation, configuration, flag, or registration the running path actually selects. Distinguish a possible path in source from the path used in the scenario being explained.
5. **Close evidence gaps.** Use callers, implementations, tests, configuration, and wiring to verify each material connection. If a handoff cannot be established, name the gap and what evidence is missing instead of guessing.

For a genuinely broad subsystem, divide exploration into independent slices such as entry and routing, data and state, and external effects. Explore those slices in parallel when delegation is available, then reconcile overlaps and contradictions against the code before writing the explanation. Keep narrow questions in one pass.

Stop exploring when the requested path can be explained from trigger to effect without hand-waving, the important data changes and seams are accounted for, and remaining uncertainty is explicit. Do not inventory the whole repository.

## Explain the Result

Lead with the answer at the requested level of detail. Use only the sections that help explain the behavior:

- **Overview:** what the code path or subsystem does and where it begins and ends
- **Flow:** the ordered runtime path, including material data transformations and decisions
- **Key concepts:** only the types, modules, or domain terms needed to follow the flow
- **Where it lives:** the smallest useful map of entry points and implementation files
- **Gotchas and unknowns:** surprising behavior, runtime selection, sharp edges, and unresolved evidence gaps

Reference exact files and symbols so the reader can inspect the evidence. Prefer prose over code dumps. Use a small flow, sequence, or state diagram only when relationships across several modules are materially clearer visually.

Keep observed facts, supported rationale, and inference visibly distinct. The explanation should let an engineer predict what happens for a representative input and know where to begin changing or debugging it, without itself proposing the change or diagnosis.
