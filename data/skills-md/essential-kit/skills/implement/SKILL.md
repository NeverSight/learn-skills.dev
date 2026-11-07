---
name: implement
description: "Implement a piece of work based on a spec or set of tickets."
disable-model-invocation: true
---

Implement the work described by the user in the spec or tickets.

If the user passes a ticket reference, fetch it from GitHub Issues with `gh issue view <number> --json number,title,body,labels,comments` (for a URL, use its number) and state its title before starting. If the reference is ambiguous, ask.

Before changing code, read `GLOSSARY.md` at the repo root (or `GLOSSARY-MAP.md` and the per-context glossaries it points at) and any ADRs under `docs/adr/` or `src/*/docs/adr/` that touch the area. If they don't exist, proceed silently. Use their vocabulary in commits and surface any ADR conflict rather than silently overriding it.

Call the Skill tool with "tdd" where possible, at pre-agreed seams.

Run typechecking regularly, single test files regularly, and the full test suite once at the end.

Once done, call the Skill tool with "code-review" to review the work.

Commit your work to the current branch.
