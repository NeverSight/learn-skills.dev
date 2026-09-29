---
name: code-review
description: "Orchestrator. Triages a PR, local diff, patch file, or staged/branch changes into one of four review types (content, code-lite, code-deep, infra) and dispatches to the matching child skill. Use this when you don't already know which depth or type of review you want. For a known type, invoke the child skill directly."
when_to_use: "Use when the user asks for a code review in any form: /code-review, 'code review this', 'CR this', or similar, and the type is not pre-specified. Follow all steps in order; do not shortcut based on this description."
argument-hint: "[PR URL | path to diff file] [--type=<content|code-lite|code-deep|infra>] [--lint]"
effort: low
allowed-tools: Bash(git *) Bash(gh *) Bash(bash ~/.claude/skills/code-review/scripts/code-review-state.sh *) Read Grep AskUserQuestion Skill
---

## Steps

### 1. Determine source and fetch the diff

Read `~/.claude/skills/code-review/references/review-shared.md` and follow its source detection and diff fetching sections. By the end of this step you have:

- A resolved source mode: `pr` / `uncommitted` / `branch` / `both` / `file`
- The diff content
- The list of changed file paths

### 2. Compute triage signals

From the diff and the changed file list, compute:

| Signal | How |
|---|---|
| `lines_added` | count of `^+` lines (excluding `+++` headers), excluding lockfiles and build-output paths |
| `files_changed` | unique `+++ b/` paths, excluding lockfiles |
| `all_docs` | every changed path matches `\.(md\|mdx\|txt\|rst)$` or lives under `docs/`, `content/`, `posts/` |
| `has_infra` | any path under `.github/`, ends in `.tf`, matches `Dockerfile`, or matches `docker-compose*` |
| `has_security_paths` | any path matches `(auth\|crypto\|password\|token\|secret\|\.env\|sql\|migration)` |

Apply recommendation logic (first match wins):

1. `has_infra` true: recommend **code-review-infra**
2. `all_docs` true: recommend **code-review-content**
3. `has_security_paths` true OR `lines_added >= 500`: recommend **code-review-deep**
4. Default: recommend **code-review-lite**

Print this classification line before proceeding:

> Triage: <lines_added> lines / <files_changed> files / <comma-separated signals that fired, or "no special signals">.
> Recommended: **<skill name>** (<one-sentence reason citing the matching signals>).

### 3. Confirm the type

**Resolve state location.** Run:

    bash ~/.claude/skills/code-review/scripts/code-review-state.sh resolve

If output is non-empty, that's the `state_file` path. If empty, persistence is skipped for this run (no project context, or `.claude/` missing).

**Compute `source_id`:**

- PR mode: `pr:<URL>`
- File mode: `file:<absolute path>`
- Git modes: `git:<mode>:<branch>`, where `<mode>` is one of `branch`, `uncommitted`, `both`, and `<branch>` is the output of `git branch --show-current` (use `detached` if empty)

**Pick the type, in this order:**

1. **`--type=<valid>` was passed.** Use that type. If the value is not one of `content`, `code-lite`, `code-deep`, `infra`, ignore it and continue to step 2. If `state_file` is set, run:

        bash ~/.claude/skills/code-review/scripts/code-review-state.sh set <state_file> <source_id> <type>

    Skip the prompt.

2. **Stored type exists.** If `state_file` is set, run:

        bash ~/.claude/skills/code-review/scripts/code-review-state.sh get <state_file> <source_id>

    If the output is non-empty, use that type and print:

    > Using previously chosen review type: **<type>**. Pass `--type=<other>` to override.

    Skip the prompt.

3. **Prompt the user.** Call `AskUserQuestion`:

    - question: "Which review type should I run?"
    - header: "Review type"
    - multiSelect: false
    - options: the recommended type first with `(Recommended)` appended to the label, then the other three in this fixed order: code-deep, code-lite, infra, content (skipping whichever is recommended).

    After the user picks, if `state_file` is set, run the `set` command from step 1 to persist the choice.

The chosen label maps to a child skill: `content` -> `code-review-content`, `code-lite` -> `code-review-lite`, `code-deep` -> `code-review-deep`, `infra` -> `code-review-infra`.

### 4. Dispatch to the child skill

Invoke the chosen child skill via the `Skill` tool. Build the `args` string from the resolved source so the child does not re-prompt:

- PR mode: `--source=pr --pr=<URL>`
- File mode: `--source=file --file=<path>`
- Uncommitted / branch / both: `--source=<mode>`
- If the user passed `--lint`, append `--lint`

The child performs the actual review and produces all output. Do not produce any review content yourself: your job ends after dispatching.
