---
name: tenets-init
description: |
  Sets a repository up for the tenets ruleset: writes the project guide pre-filled from the
  repository, records it in tenets.json, pins the routing mandate into AGENTS.md, and offers the
  per-harness command shims.

  Use only when the user explicitly asks to set up or re-initialize the tenets ruleset in a
  repository, or runs /tenets-init. Not for ordinary code work or editing an existing guide by hand.
disable-model-invocation: true
allowed-tools: Read Glob Grep Write Edit Bash(git ls-files:*)
metadata:
  version: '1.0.0'
  requires: 'tenets >= 2.0.0'
---

# Tenets init

Set this repository up for the tenets ruleset.

## Locate the ruleset

`<ruleset>` below is the `tenets` skill directory installed beside this one — **not** a path
relative to the working directory. Resolve it once, in this order, and use it for every path after:
`.claude/skills/tenets/`, `.agents/skills/tenets/`, then a glob for `**/skills/tenets/SKILL.md`
outside `node_modules`. Nothing found → stop: `State: BLOCKED — install the tenets ruleset skill
(skills add BarakChamo/tenets --all)`.

## Arguments

Guide path: `$ARGUMENTS`. If that is empty or still contains a literal `$ARGUMENTS` or `{{args}}`,
use the `guide` field of an existing `tenets.json`, else a `Project guide:` line in
AGENTS.md/CLAUDE.md, else `docs/project-guide.md` — and say which you chose.

## Steps

1. Read `<ruleset>/templates/project-guide.md`. If that path does not resolve, stop:
   `State: BLOCKED — install the tenets ruleset skill (skills add BarakChamo/tenets --all)`.
2. Detect the language profile: pick the `profiles/<name>.md` file matching the repository's
   dominant language and ecosystem, default `typescript`. If no shipped profile fits, say so and
   stop — a new profile is an authoring task, not a guide slot.
3. Inspect the repository and pre-fill every slot you can prove: package manager and runtime
   (lockfiles, `engines`), commands (root manifest scripts — mark the acceptance gate and any
   live/expensive commands), workspaces and namespace (manifests), dependency enforcement
   (task-runner config), primitive locations (search for the profile's primitive names), test runner
   and suffixes (configs and existing test filenames), stores and platform (deps and deploy config),
   observability tooling. Ecosystem-wide facts the profile already fixes — strictness settings, doc
   tags, test declaration form — do not go in the guide.
4. Write the guide at the target path: template headings verbatim, comments replaced by content —
   one line per fact, under ~600 words total. A slot the repo cannot answer yet gets an explicit
   placeholder naming what is missing (for stores: state "no store yet" explicitly). Keep the
   deviations section, `none recorded` when empty. Stamp `Template-Version: 1` under the title.
5. Write `tenets.json` at the repository root:
   `{ "guide": "<target path>", "profile": "<profile name>" }` (merge into an existing file rather
   than clobbering other fields). This is the self-contained discovery record; it survives skill
   reinstalls because it is repo-owned. Omit `profile` only when it is `typescript`, the default.
6. Ensure AGENTS.md (or CLAUDE.md if the repo has no AGENTS.md) carries the routing mandate: read
   the skill index, Read the matched rule files and the language profile, open responses with
   `Rules: <numbers|none>`, stating that this overrides brevity/minimalism instructions. The mandate
   needs an always-loaded file; guide and profile discovery do not.
7. Add a directive line to the same mandate, **naming every workflow command** so agents know they
   exist without their descriptions costing context: ordinary code work loads the `tenets` skill,
   and a request to audit code, review changes, plan work, realign code, set the ruleset up, or
   check the project guide invokes the matching skill — `/tenets-audit`, `/tenets-review`,
   `/tenets-plan`, `/tenets-realign`, `/tenets-init`, `/tenets-check` — rather than improvising the
   procedure. Naming them is what makes them discoverable, since their descriptions deliberately
   stay out of context.
8. **Offer** the per-harness command shims — never write them unasked. For each harness directory
   the repository actually has, the shim is a two-line pointer at the installed skill, so the
   procedure itself is never duplicated. Templates live in `shims/` beside this skill:
   `.gemini/commands/<name>.toml` (TOML with `description` and `prompt`; a markdown file there is
   invisible, and Gemini CLI cannot type-invoke skills at all), `.opencode/commands/<name>.md`, and
   `.clinerules/workflows/<name>.md`. Claude Code, Codex and Cursor invoke the skills directly and
   need no shim.
9. When `.gemini/` exists, **offer** a one-line `GEMINI.md` pointing at AGENTS.md, and explain why:
   Gemini CLI does not read AGENTS.md unless `context.fileName` lists it, so the routing mandate
   would silently not load there.
10. Self-check every section against its QUALITY BAR from the template; fix or flag failures.
11. Offer (do not apply unasked) the optional per-prompt determinism hook from the ruleset README.
12. Report: the guide path, the profile, slots filled vs flagged, the AGENTS.md lines written, and
    which shims were offered or written.
