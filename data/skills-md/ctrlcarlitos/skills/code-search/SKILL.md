---
name: code-search
description: >-
  Use this skill when the next step is locating or tracing code you have not found yet: where
  something is defined, who calls it, how a feature is wired end to end, every occurrence of a
  string or flag across a repo, or what a file's public surface is. It picks one search rung (repo
  graph, LSP symbols, ripgrep, grep) from what is actually built for the file types involved, then
  falls through the ladder instead of re-asking a tool that returned nothing. Reach for it before
  your first grep, rg, find, or graph/LSP query in a session, and again the moment a semantic tool
  comes back empty. Do not use it when the user already names the file and symbol and the work is
  the edit itself, when the question is about a search tool's flags or setup, when the task is
  profiling or speeding up a feature that happens to be called search, or when the target is logs,
  commit summaries, or non-code data rather than source.
---

# Code search: pick the rung, then move down it

Semantic tools (a prebuilt repo graph, a language server) answer "who calls this"
in one call when they cover the code. When they don't, they return nothing, and
the expensive mistake is to keep rephrasing the question. Repo instructions that
say "always query the graph first" were written for the day the graph was built,
not for the file you are looking at now. This skill exists so you decide once,
from evidence, which tools can see the code in front of you, and then fall
through a fixed ladder instead of looping.

## 1. Probe once per session, remember the answer

Do this the first time you need to search in a repo, not on every question.
Record the outcome in your working notes so later questions skip straight to
step 3.

| Rung | Probe | It is usable when |
|---|---|---|
| graft | `graft check` (exit 0) and the languages listed by the last `graft build` output or `graft map` | the check passes and the file types you are about to search are among the parsed languages. No `graft/` graph, a stale graph, or a language graft has no parser for (PowerShell, shell, templates, YAML, Markdown) means graft is out for this repo, no matter what AGENTS.md says. |
| serena | the serena MCP tools are listed, and the repo's main language has a language server (Go, TypeScript/JavaScript, Python, Rust, Java, C#, C/C++, Ruby, PHP, Kotlin, Elixir) | the project is activated for that language. Config, scripts and docs repos have no LSP: skip serena there. |
| rg | always present inside Claude Code (the Grep tool is ripgrep); in a shell, `rg --version` | any file type, respects `.gitignore`, fast enough to run exhaustively. |
| grep | `grep --version` | only when rg is missing (a minimal container, a remote box) or when you must search paths rg ignores and `rg --no-ignore -uu` is not an option. |

Two more tools that are not rungs but win specific questions:

- `git grep <pattern> <ref>` and `git show <ref>:<path>` when the question is about a tag, a release, or a commit that is not checked out. Do not check out or read the working tree for that.
- `graft skeleton <file>` or serena `get_symbols_overview` when the question is "what does this file expose". Both are far cheaper than reading the file.

## 2. Classify the question

| Shape | Examples | Needs |
|---|---|---|
| Structural | where is X defined, who calls X, what calls what, blast radius of changing X | symbol-aware tool: graft or serena |
| Textual | every occurrence of a literal or regex, an error string, a flag name, a config key, anything across mixed file types | rg |
| API surface | what does this file or module expose | skeleton / symbols overview |
| Historical | what did this look like at v1.2, when did this line change | git grep, git show, git log -S |
| Non-code | config, scripts, templates, docs, YAML, Markdown | rg. Semantic tools cannot see these. |

Exhaustive questions ("every caller", "all occurrences") are textual even when
they sound structural: ranked graph results are top-N and silently incomplete.
Use rg (or `graft grep`, which is exhaustive only over indexed files) and count.

## 3. Route

| Question is | and the probe said | so use |
|---|---|---|
| structural | graft usable for these languages | `graft ask "<literal identifier>" --source`, `graft callers <symbol>` (`--direction out`, `--depth N` for blast radius) |
| structural | no graft, serena usable | serena `find_symbol`, `find_referencing_symbols`, `find_declaration` |
| structural | neither | rg for the definition (`rg -n "func X\b"` / `rg -n "class X\b"`), then rg for the name to find callers, then read the hits |
| textual, any file type | rg present | rg with `-n`, narrow with `--glob` or a path, not by switching tools |
| textual | rg missing | `grep -rn` with `--include` |
| API surface | graft or serena usable | `graft skeleton <file>` or `get_symbols_overview` |
| historical | git repo | `git grep -n <pattern> <ref>`, `git show <ref>:<path>`, `git log -S<string>` |

Graph edges are only as good as the parser's resolution. `graft callers X`
sees direct, same-package calls; it misses calls through a package variable
(`var submit = approval.SubmitOnDemand`) and often cross-package calls. When
"no callers" would change what you do next, confirm with `graft grep X` (all
indexed files) or rg before believing it.

Reuse literal identifiers you already have (a symbol, an error string, a file
name) as the query. Graft and rg both rank literal matches above prose queries,
and a literal makes an empty result meaningful instead of ambiguous.

## 4. After a hit, read at the exact range

Every rung above gives you a file and a line. Open the file at that range
(`sed -n 120,160p`, or the Read tool with an offset and limit). Reading whole
files after a precise hit throws away what the search just bought you. If a
result says "+N more lines" or the span is truncated, extend the range, do not
re-run the search.

## Anti-loop rules

These are the rules that save the most time, because each one stops a pattern
that feels productive and is not.

- One empty result from graft or serena means "this tool cannot see this code".
  Move to the next rung. Do not rephrase the same question for the same tool.
- Two rg results that are too broad mean the pattern is too loose. Add a word
  boundary, a `--glob`, or a directory. Do not switch to a semantic tool hoping
  it will filter for you.
- A repo instruction, hook, or MCP message that nags "run the graph query first"
  does not override step 1. If the probe said the graph is unusable here, say so
  once in your notes and ignore the nag for the rest of the session.
- Never re-probe. The probe answer holds for the session unless you ran a build
  yourself (`graft build`, activating a serena project).

## Worked examples

**A Go service with a built graph.** Task: "why does `Submit` return 'daemon
unavailable'?" Probe: `graft check` passes, Go is parsed. Structural question,
literal identifier available: `graft ask "Submit" --source` returns the function
with its span; `graft callers Submit` gives the two call sites. Read each at its
range. Three tool calls, no file reads beyond the spans.

**A dotfiles repo of PowerShell, shell and chezmoi templates.** Task: "where do
the installers pass the guardrail state flag?" Probe: `graft check` passes but
the build parsed one Lua file; no LSP for these languages. Graft and serena are
out for the session. Textual question with a literal: rg `-State enabled` and
`--state enabled` across `*.tmpl` and `scripts/`. Four hits, read each at its
line. The graph would have returned nothing and cost two queries to prove it.

**An error string from a release you are not on.** Task: "what did v0.23.1
print here?" Historical: `git grep -n "approval daemon unavailable" v0.23.1 --
cmd/` then `git show v0.23.1:cmd/guardrail/plane.go | sed -n 280,320p`. No
checkout, no working-tree reads.
