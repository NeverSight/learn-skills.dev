---
name: token-saviour
description: >
  Pick the most token-efficient tool for a coding task instead of reflexively reading whole
  files, dumping raw command output into context, or writing more code than asked. Use this
  skill BEFORE you explore or explain a codebase, locate a symbol/definition/callers, trace a
  call path, map an architecture, plan or implement a feature across layers, or run verbose
  commands (tests, builds, git, grep, directory listings) — and whenever context/token budget,
  cost, or "make this use fewer tokens" comes up. It routes the scenario to serena, rtk,
  caveman, Ponytail, or plain tools, with concrete commands and the combinations to use vs.
  avoid. Reach for it even when the user doesn't name a tool: if you're about to `cat`/Read
  several files, or about to generate a big implementation, that's the trigger.
---

# token-saviour: spend tokens where they matter

Reading whole files to answer a narrow question is the single most wasteful thing an agent
does. On a benchmark over a ~30-file Python app, swapping whole-file reads for **semantic
retrieval cut total tokens ~66%**; the other tools each own a narrower slice. This skill
helps you reach for the right one *before* you blow the context budget — then get back to the
actual task.

The mental model: token cost has **four independent layers**, and a different tool owns each.
Match the tool to the layer the task actually stresses. These winners were re-validated in a
9-tool benchmark (2026-07) against newer entrants (archex, Pare, lazy-cat) — every incumbent
held its layer; the runner-ups and the niches where they flip are in
`references/tool_links.md`.

| Layer | What it is | Tool | Don't bother with |
|------|------------|------|-------------------|
| Code-read **input** | Understanding code: symbols, callers, call paths, architecture | **serena** | rtk, caveman, Ponytail |
| Command-output **input** | Verbose stdout: tests, builds, git, grep, listings | **rtk** | the code-read tool |
| Generated **prose output** | Your own long, chatty replies / write-ups | **caveman** | the input tools, Ponytail |
| Generated **code output** | Implementations you write/edit | **Ponytail** | the input tools, caveman |
| — | Tiny/one-off work | plain Read/Grep/Bash | everything (overhead > benefit) |

> **First, check availability.** These are optional third-party tools. Run the relevant
> `--help`/`--version` once; if a tool isn't installed, see `references/tool_links.md` for
> install + verify commands, or fall back to the next-best option in its row (ultimately plain
> Read/Grep/Bash). Never pretend a tool ran — degrade gracefully.

> **Announce what you used.** Whenever this skill drives a task, print a one-line tag naming the
> token-saving tools actually used, joined with ` + ` — e.g. `🪙 token-saviour: serena + rtk +
> caveman`, or `🪙 token-saviour: serena + ponytail`. If you fell back to plain Read/Grep/Bash
> because nothing was installed or the task was trivial, say so: `🪙 token-saviour: plain tools
> (fallback)`. List only tools you genuinely invoked, in layer order (serena → rtk → caveman
> / ponytail).

---

## Decision guide

Work top-down. The moment a row matches, use that tool and stop.

1. **"Where is X / what calls X / how does A reach B / what breaks if I change X / explain this
   module / list its methods?"** → **serena** (semantic code retrieval). This is the dominant
   cost — code-reading was ~88% of the baseline bill — so this is the highest-value switch.
   Measured: tracing a 4-layer call path cost **65 tokens vs 1,633** reading the files (−89%);
   explaining the whole architecture **243 vs 3,250** (−85%); listing one class's methods **55
   vs 458** (−71%); finding all callers **49 vs 525** (−78%).

2. **Running something noisy — test suite, build, linter, `git`, `grep`, a big directory
   listing** → **rtk** (compresses command output). Measured: the test run **−65%**, the
   structure listing **−38%**. Its win scales with verbosity, so it's biggest on failing test
   dumps and long build logs (this clean repo is a lower bound). *Niche exception:* if your
   loop is dominated by **test runs** and Pare's MCP servers are already wired in, Pare's
   structured `pytest` posted the single best command result we measured (−72%: `pytest: 13
   passed`, 5 tokens) — but it *adds* tokens on listings/greps, so rtk keeps the layer.

3. **About to write a long, prose-heavy answer** (explanations, write-ups, status) → consider
   **caveman** (terse "caveman" reply style). It trims filler/hedging/pleasantries. Small on already-concise text and it
   can *grow* terse list/structured output by adding markdown — so use it for genuinely chatty
   output, not for short factual answers or anything where exact wording/order matters
   (warnings, irreversible steps, ordered procedures).

4. **About to generate or edit a chunk of code** (implement a feature, scaffold, refactor) →
   **Ponytail** (a "lazy senior dev" rules plugin that biases you toward minimal code). It
   applies YAGNI: skip unrequested abstractions/helpers, prefer stdlib + one-liners, delete over
   add. In our benchmark it trimmed a verbose due-date implementation by **~40% (illustrative —
   the size depends on how much scope the baseline over-built)** by dropping helpers and a derived
   property nobody asked for. It does ~nothing on prose — it's the mirror image of caveman.
   (lazy-cat performed equivalently under the identical framing; Ponytail keeps the slot for its
   intensity levels and explicit don't-simplify guardrails.)

5. **None of the above / a one-file, one-line lookup** → just use plain Read/Grep/Bash. The
   tools have setup and call overhead; on tiny tasks that overhead can cost *more* than it
   saves. Don't tool-ify trivial work.

---

## serena owns the code-read layer

serena cuts the dominant cost — *code-read input* — by returning **just the relevant
structure** instead of whole files. It's *comprehension- and edit-heavy*: broad multi-file
understanding **plus semantic edits/renames**. Best measured on listing a class's members
(−71%) and whole-architecture explanation (−85%), with strong caller and call-path lookups too.
It needs a language server and indexes once at session start.

If you reach for only one tool, make it serena — it's the only lever that moves the dominant
(code-reading) cost. (Runner-ups if serena is unavailable: graphify for call-path navigation,
CodeGraph as a zero-config single binary — see `references/tool_links.md`. Skip retrieval-bundle
tools like archex on small/medium repos: their fixed per-query overhead measured **worse than
just reading the files**, +15% on our suite.)

---

## Best combinations, and what to avoid

The four layers are independent, so combining one-per-layer is additive:

- 🥇 **Comprehension / navigation work:** **serena** + **rtk** + **caveman**. Each owns a
  distinct slice; rtk and caveman cost ~nothing to add. Measured combined: **−70%** (the best
  stack in the 9-tool re-run; the Pare variant landed at −67%).
- 🥇 **Code-generation work:** **serena** + **Ponytail** — swap caveman→Ponytail because the
  output is code, not prose. On the codegen task ≈ **−64%** (the code-read half measured, the
  Ponytail half illustrative).
- ❌ **Don't reach for rtk to fix comprehension cost** — it's ~0% there. Use it *for*
  command-heavy loops.
- ❌ **Don't run two code-read tools** (serena / graphify / CodeGraph / archex) together — two
  integrations, one benefit. Pick one.
- ❌ **Don't mix up the two output tools** — caveman shrinks prose (~0% or worse on code);
  Ponytail shrinks code (~0% on prose). Route by whether the output is prose or code.
- ❌ **Don't expect any output tool to move an input-heavy bill** — when you're reading lots of
  code, output is a small share; serena is what matters.

### Install missing tools

When a chosen tool is absent, read `references/tool_links.md` and install the smallest useful
set:

- **serena** for symbol-aware comprehension/edits — the one code-read tool.
- Add `rtk` only for noisy command loops.
- Add `caveman` only when prose-output brevity is the bottleneck.
- Add `ponytail` only when code-generation work is the bottleneck.

For network installers or shell profile changes, request approval if the environment requires it.

---

## Tool quick-reference (commands)

Use these in place of the reflexive `Read`/`Grep`/`Bash`/"write it all out" equivalents.
Install/verify details for any missing tool: `references/tool_links.md`.

### serena (MCP server, LSP) — instead of reading files to understand/edit code
Connect to the serena MCP server for the project, then call tools rather than reading files:
- `get_symbols_overview(relative_path)` — top-level symbols in a file (add `depth: 1` for methods).
- `find_symbol(name_path_pattern, relative_path, include_body=true)` — a symbol's body.
- `find_referencing_symbols(name_path, relative_path)` — every caller, with context.
- Edits too: `replace_symbol_body`, `insert_after_symbol`, `rename_symbol`.

### rtk (Rust CLI proxy) — instead of raw verbose commands
```bash
rtk test  <test cmd>     # e.g. rtk test pytest      → only failures + summary
rtk read  <files...>     # cat with filtering
rtk grep  <pattern> <p>  # compact grep (groups, truncates); -t py to scope by type
rtk find  <find args>    # compact file listing
rtk ls / rtk tree / rtk git / rtk diff / rtk log ...
```

### caveman — instead of a long, chatty prose reply
Activate terse mode (say "caveman mode" / `/caveman`, levels `lite|full|ultra`) when you're
about to emit a verbose explanation. Keep code blocks, commands, API names, error strings, and
ordered/irreversible steps **verbatim** — caveman compresses prose, not substance.

### Ponytail — instead of writing more code than the task needs
Enable the plugin (`/ponytail lite|full|ultra`) before generating an implementation — prefer those
modes so the code stays complete and readable. Its rules: don't build what wasn't requested (YAGNI),
prefer stdlib/native + one-liners, no speculative abstractions/helpers, delete over add, leave one
runnable check. It stays out of your way on input validation at real trust boundaries, error handling,
and security.

---

## Why this works (so you can adapt it)

Input dominates the bill when an agent works in a codebase (it was ~88% in the benchmark), and
most of that input is *over-reading* — pulling entire files to answer something a symbol lookup
answers in a fraction of the tokens. Semantic retrieval wins because it returns *just the
relevant structure*. rtk, caveman, and Ponytail look small in aggregate only because they target
narrow slices — but they're cheap, so stack them. The one trap is treating these as
interchangeable: each is excellent in its lane and ~useless outside it. When in doubt, ask
"which layer is this task spending tokens on — reading code, reading command output, writing
prose, or writing code?" and pick that row.

Full evidence (per-task tables, the 9-tool comparison, limitations):
`references/benchmark_results.md`.
