---
name: python
description: "Best practices for python code"
---

- It is not allowed to decorate comments like "---" "===" "\*\*" etc.
- Function arguments should be either argument-only or keyword-only (deterministic), by using `/` and `*` in function signature. Do not add too many argument-only arguments, make it argument-only only if it is very obvious. Ideally argument-only arguments should be 1 (best) or 2, avoid making it 0 or more than 3.
- Do not add default values unless the user told to do so. The default values must be a clear meaningful value, not just a "cool" random number, and you are not allowed to decide it. Instead make it a required argument-only argument / keyword-only argument.
- Do not import within function. If the package is not installed in the current environment, install them via `uv add <package>` or tell the user to do so.
- To run python commands, use `uv run python`, `uv run pytest`, etc. Never run `python` directly. You may run `uv run pytest` on your own.
- After the work is done, run `prek run -a`, and fix the linting errors prioritizing the ones introduced by your work.
