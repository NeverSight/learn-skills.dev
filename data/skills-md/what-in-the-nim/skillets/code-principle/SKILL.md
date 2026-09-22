---
name: code-principle
description: Apply surgical coding defaults when writing, modifying, or refactoring code.
---

# Code Principle

Apply all six rules to code you create or modify:

1. **Formatting.** Preserve manual formatting. Run required non-mutating checks; format files only when explicitly requested.
2. **Docstrings.** Document every new module, class, function, and method. Start with a one-line summary; expand into relevant NumPy-style sections for contracts, side effects, errors, or non-obvious decisions.
3. **Composition.** Before implementing a module or class, identify separable mechanisms with independent responsibilities, contracts, or testing value. Compose reusable components where justified; keep speculative extractions local.
4. **Comments.** Allow at most two inline comments per function or method: one line each, explaining why. Put deeper explanation in docstrings or a nearby `README.md`.
5. **Surgical scope.** Start with the smallest correct patch fitting the current design. Refactor only as the required change grows, and only enough to keep it coherent.
6. **Terse communication.** Use compact engineering prose; fragments are fine when unambiguous. Preserve decisions, risks, and verification evidence.

Before finishing, verify the diff and handoff against all six rules.
