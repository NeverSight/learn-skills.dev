---
name: rubber-duck-review
description: Use when asked to rubber duck a change, get a second opinion, or run an independent cross-model review of code changes.
license: SEE LICENSE IN LICENSE.md
metadata:
  author: Vivswan
---

# Rubber Duck Review

Get a second opinion on code changes from a different model while you keep ownership of the task.

## When to Apply

Use this skill when someone asks for:

- `/rubber-duck-review`
- "rubber duck my changes"
- "get a second opinion on this"
- "review this with another model"

## Workflow

### 1. Pick the reviewer

- Prefer a dedicated review tool when one is available.
- Use a reviewer that is different from the current model when possible.
- If no dedicated tool exists, fall back to a read-only CLI invocation through this skill's `scripts/run-review.mts` (step 4). Pick the reviewer by which model *you* are:
  - If you are currently using **Claude** -> `codex`, fallback `copilot`.
  - If you are currently using **Codex or GitHub Copilot** -> `claude`, fallback `copilot`.
- **Never** let the reviewer write files, edit code, or run unrestricted shell commands.
  - The script enforces read-only flags: `--sandbox read-only` (codex) / `--permission-mode plan` (claude) / a read-only tool allow-list (copilot).
  - Read-only still lets the reviewer self-check: it can run read-only commands (grep, `git diff`, typecheck) but writes are blocked. copilot can only read and grep files. That self-checking makes findings concrete.
  - Note: a read-only sandbox can block temp-dir creation, so the reviewer may skip tests that need to write.

### 2. Large change sets: fan out one review per section

- A single broad review of a big diff is shallower than several focused ones. Split the change into logical **sections** (each new command/module, each script, the CI/release config, a parity pair). Run one review per section in parallel, each scoped to its files.
- **Run at most about three at a time.** Many simultaneous `codex exec` processes can saturate the backend and hang. A stalled batch gets smaller, never larger.
- **Detect & recover from hangs.** With JSON streaming, compare each review's event count over ~30-60s. If one is flat while its siblings climb, it's hung. Stop it (the task runner's stop, or `kill <the pid the launch printed>`, never a kill by pattern) and relaunch just that one.

### 3. Craft the prompt

- Ask for a review of the relevant changes and surrounding context only.
- Always include: `This is a review-only task. Do not edit, write, or modify any files. Only read and report findings.`
- Tell it how to see the change, naming the same target the convergence gate scopes to, rather than pasting diffs. It follows imports and cross-file behavior better that way.

  Before a commit, that is "run `git --no-pager diff --cached` and read the new files". For a branch or PR, it is "run `git --no-pager diff <base>...HEAD`" with the branch's actual base. `git diff HEAD` is neither: empty on a committed branch, and polluted by unstaged edits before a commit.
- Ask the reviewer to look for:
  - Correctness issues
  - Demonstrable defects: a correctness finding earns work when it names a concrete input or state and the wrong output, crash, or data loss it produces in the change under review. A maintainability finding earns work when it points at something concrete in this change, per the next bullet.
  - Naming or design choices that are already awkward in this change: a name that misleads about what the code does today, or duplication and structure introduced here
  - Workarounds propped up by long justification comments: if it takes a paragraph-long comment to argue the workaround is OK, the code is wrong. Flag both the comment and the code for fixing.
  - Hand-rolled code whose whole job a good library already does: a finding that names the library and what it covers (the `/code-standards` skill's rule).

    A large library or an unclear fit is a `non_blocking` entry whose claim begins `Ask the owner:`. The driver puts it to the user and builds nothing until they answer. A library that needs a runtime or API the repository has dropped is not a fit, and not a finding.
  - The standing test question: for each NEW test in the change, the fact it pins that the source does not already say. The reviewer never asks for a test without naming that fact.
    - A test that restates the source it reads is a finding whose fix is deletion: a workflow test asserting `needs` equals the list in the yaml, a constant pinned to its own literal.
    - The template carries the wording. The `/code-standards` skill's `references/tests.md` owns the rule, its three valid answers, and where a constant's value is pinned instead.
  - PII in anything the change publishes: anything that tells a reader who the author is, how they work, or how their machine is set up, including values measured or copied from the author's real environment. Every fixture is hand-authored. A provenance comment naming real data is a finding.

    The template carries the wording. The `/pr-and-issue-discipline` skill owns the rule and its substitutes. Paste the PR title, body, and comments into the prompt, since a sandboxed reviewer may not reach GitHub.
  - Speculative hardening (hostile callers that cannot reach the code, races in single-user tools, deadlines already bounded by an outer timeout, defensive checks for inputs the code never receives) is listed under a `Recorded, not built` heading, never as a finding. It stays unbuilt unless the user asks for it.

    In a repository with more than 100 GitHub stars it is instead surfaced to the user and built only after they confirm (step 6). A small, obvious hardening that rides along in the change under review (an exit-code check beside a version check) is fine to keep. The reviewer must not propose a wider one to replace it.
- Fold in criteria from **companion skills**: for EVERY installed skill that declares a `## Review Criteria` section in its SKILL.md, expand that section into the reviewer prompt. Triage the resulting findings with that skill's own workflow. One exception: on someone else's PR, the `/reply-and-review-discipline` skill's lens choice names which sections are expanded.
  - There is no registry. Declaring the section is what makes a skill part of the review. In this collection, `/no-invalid-states`, `/code-standards`, `/never-twice`, and `/verify-with-controls` declare it.
  - Enumerate participants by grepping installed skills, e.g. `grep -rlE '^## Review Criteria' ~/.claude/skills/*/SKILL.md .claude/skills/*/SKILL.md 2>/dev/null` (adjust the paths to wherever your harness installs skills).
  - A skill whose criteria only apply in a specific context names its heading differently (e.g. `## <Context> Review Criteria`) and folds its own criteria into the reviews it launches itself.
- Ask for **prioritized** findings (blocking vs non-blocking), and ask it to say so plainly if the code is correct. This keeps re-reviews terminable.
- The report is one JSON object: `blocking` and `non_blocking` arrays of `{where, claim, evidence}`, a `recorded_not_built` string array, and a `summary`. Paste the report-format block from the template. The script enforces the shape for codex and claude through `scripts/verdict-schema.json`, and copilot has only the prompt to go on.
- If the user has already declined or reverted something in this thread, add a short `Already decided / out of scope` section so the reviewer does not keep re-raising it.
- On a re-review, state which fixes were already applied so it focuses on what remains.

For a reusable prompt template, see `references/reviewer-prompt.md`.

### 4. Run the reviewer

This skill ships `scripts/run-review.mts` (the path is relative to the installed skill folder, not the repo under review). It encapsulates the launch pitfalls:

- spawns the reviewer from an argv array with no shell in between (backticks and `$(...)` in the prompt stay literal)
- closes stdin (both `codex exec` and `claude -p` block forever waiting on open stdin)
- captures the full stream to a scratch file under the OS tmp dir (never the working tree)
- passes each reviewer's required flags, including the verdict schema (`scripts/verdict-schema.json`) for codex and claude, so the final message cannot be free text
- extracts the verdict and refuses one with no tool call before it. codex fills its narration into the schema too, so a turn that ends at "I will review now" is a valid-looking empty verdict. The missing reads are what expose it
- prints one JSON report: the verdict, the tool-call count, the path of the kept capture, and a compact trajectory (one row per reviewer step) so you can see what the reviewer did without opening the stream

Write the step-3 prompt to a tmp file and pass the reviewer name plus that file. Several agents (or several sections of one fan-out) review at once on one machine. A predictable name such as `/tmp/rubber-duck-prompt-<section>.md` lets one writer overwrite another's prompt before the script reads it, so the script mints the path:

- `prepare <section>` creates a private directory with `mkdtemp` (atomic, so two callers can never receive the same one), leaves its marker there, and prints the section's prompt file inside it.
- A launch refuses any prompt file outside such a directory, and any symlink or hard link inside one. The marker is the proof, not the location, so the two shells need not share `TMPDIR`.

Inside an agent worktree the sandbox can refuse a Bash heredoc whose text contains git commands (it cannot verify the command stays inside the worktree). Write the prompt file with the harness's Write tool there:

```bash
# 1. Mint the prompt path, one call per review section. Shell state does not survive
#    between tool calls, so copy the printed path by hand:
bun "<skill-dir>/scripts/run-review.mts" prepare api-gateway   # prints e.g. /tmp/rubber-duck-prompt-Kq3mZp/api-gateway.md
# 2. Write the step-3 prompt to that path with your Write tool (a heredoc with a quoted
#    delimiter works only outside an agent worktree).
# 3. Then, in one shell call:
prompt_file="/tmp/rubber-duck-prompt-Kq3mZp/api-gateway.md"
bun "<skill-dir>/scripts/run-review.mts" codex "$prompt_file"  # codex|claude|copilot per step 1
```

- Reviewer argument:
  - `codex`: runs `codex exec --json --sandbox read-only --output-schema <schema>`.
  - `claude`: runs `claude -p --permission-mode plan --verbose --output-format stream-json --json-schema <schema>` (`--verbose` is required with `stream-json`).
  - `copilot`: runs `copilot -p <prompt> -s --available-tools=view,rg,glob --deny-tool=write --deny-tool=shell --disable-builtin-mcps`. Last-resort fallback, so prefer codex/claude. Its limits:
    - The read-only tool allow-list lets it read and grep files, but it cannot shell out, write, reach MCP servers, or spawn subagents.
    - No shell means no `git diff` and no typecheck, so name the files to read.
    - It does not stream JSON, so there is no liveness signal, no trajectory in the report, and no tool-call check on its verdict. It has no schema flag, so only the prompt asks it for the JSON object.
- `--stdin-prompt` (codex/claude only): add it if the environment rejects the prompt as a command argument, or the prompt is very large. The prompt file itself is served as the reviewer's stdin.

  A file fd is EOF-terminated, so it cannot hang. The stdin hang trap is an open pipe, not a used stdin.
- Foreground (the default) blocks until the reviewer exits, so give the tool call a generous timeout. Subagents (worktree builders, spawned workers) always run foreground: a worker that ends its turn waiting for a background reviewer's completion notification never gets one.
- `--background` prints exactly two lines, `output-file: <path>` and `pid: <n>`.
  - `output-file` is the captured stream. A detached monitor records the reviewer's exit status beside it.
  - Leads use it to keep working while the review runs and collect the verdict with `--extract --wait` (step 5).
  - Killing that PID cancels the review (the signal is forwarded to the reviewer).
- Progress: a foreground run prints at most two progress lines to stderr, one when the stream first shows life and one when the reviewer exits (a failure then adds its own `review FAILED` line). Silence in between is normal. A real review can take a while.
- Runtime: `bun`. `node` 24+ also works (`node "<skill-dir>/scripts/run-review.mts" ...`).
- Exit codes:
  - 0: verdict extracted and printed to stdout as the JSON report, or a `--background` launch started (that run's verdict comes later, via `--extract`).
  - 1: `review FAILED - relaunch`.
  - 2: usage error or reviewer binary not found.
- In this skill's home repository, a drift test (`tests/doc-drift.test.ts`) pins these citations (the reviewer invocations, the flags, the exit codes, the failure verdict) to `scripts/run-review.mts`. A rename on either side fails CI until doc and script move together.

### 5. Act on the printed verdict

- **Exit 0** from a foreground run or `--extract`: stdout is one JSON report. (A `--background` launch also exits 0, printing only the output path and PID. Its verdict comes from `--extract`.)
  - `verdict.blocking` and `verdict.non_blocking`: the findings, each `{where, claim, evidence}`. Triage them per steps 6-7: apply or reject each one.
  - `verdict.recorded_not_built`: speculative hardening the reviewer set aside. Step 6 says what happens to it.
  - `verdict.summary`: what was reviewed and how. Treat a plain "the code is correct" as convergence input, not a reason to skip re-review after fixes.
  - `tool_calls`, `trajectory`: how many reads and commands preceded the verdict, and a compact row per reviewer step. A verdict whose trajectory shows a single `git diff` and no reads of the changed files is a weak review. Sharpen the prompt (name the files) and relaunch.
  - `capture`: the full reviewer stream, kept for inspection. Read it when a finding or the summary looks off and you want the exact reviewer message.
- **Exit 1** (`review FAILED - relaunch`): that is no review at all, never a clean pass. Relaunch it.

  It means the stream was empty, cut mid-turn, truncated on its final line, contained error events, ended in a message that is not the verdict object, ended in a verdict with no tool call before it (a preamble), or the reviewer exited non-zero. While the captured stream still exists, its path is in the failure message if you want to inspect why.
- **Exit 2**: fix the invocation or install the missing reviewer binary. Nothing was reviewed.
- After a `--background` launch, wait for the verdict in a background shell so the harness wakes you when it lands. Never poll `review.status` or the output path by hand:
  ```bash
  out=<the path from the output-file: line>
  bun "<skill-dir>/scripts/run-review.mts" <reviewer> --extract --wait "$out" > "${out%/*}/verdict.out" 2>&1
  ```
  - `<reviewer>` is the argument the review was launched with.
  - The verdict lands in `verdict.out` inside that review's capture dir, so parallel reviews (step 2) never overwrite one another. It travels and is removed with the dir.
  - The script polls the launch record every 2 s until the monitor records the exit (`--timeout <seconds>`, default 3600), then prints the same JSON report.
  - It validates the reviewer and output file against what the launch recorded, so waiting on the wrong reviewer or file fails at once.
  - Exit codes, same as a foreground run:
    - 0: verdict printed.
    - 1: review failed or `--wait timed out` (relaunch).
    - 2: wrong reviewer or file, or no launch record beside the output file.
- `bun "<skill-dir>/scripts/run-review.mts" <reviewer> --extract <output-file>` without `--wait` reads a finished run once: it exits 1 (`no exit status recorded`) while the reviewer is still running instead of blocking.
- Every run that reached the reviewer keeps its scratch dir (under the OS tmp dir, never the working tree): the directory holding the `capture` path in the report, or the `output kept at` path in the failure (omitted when that stream is already gone). The script snapshots your prompt into that dir, so all review artifacts travel and clean up together. The prompt directory you minted remains yours to remove.
  - Remove exactly those two directories once the verdict is triaged, never a glob over the shared temp dir. One sweep of `rubber-duck-*` there deleted 53 directories and killed two other sessions' in-flight reviews.
  - A session that wants a sweepable space sets its own `TMPDIR` to a directory it created before launching. `prepare` and the launch both honor it.
  - A foreground launch whose reviewer binary is missing (exit 2) captured nothing and leaves nothing behind. A `--background` one keeps its dir so `--extract` can report the missing binary, so remove it after that.

### 6. Apply findings thoughtfully

- Treat valid "non-blocking" feedback as real work when it is a correctness or maintainability finding with a demonstrated effect in this change.
  - A small, obvious hardening that rides along in the same change is fine (an exit-code check beside a version check, a bound where a bound is one argument).
  - The stop sign is the cascade: when each review round finds one more hypothetical bypass of the last hardening, the target is widening. Keep the first round's minimal form and record the rest under `Recorded, not built`. A demonstrable defect found in a later round is still work under the first bullet.
  - Items under `Recorded, not built` are not work: leave them in the report and open no task or PR for them, unless the user asks. The other exception is a repository with more than 100 GitHub stars: surface those items to the user with the concrete risk, and build only the ones they confirm.
- Fix valid non-blocking findings as well as the blocking ones, including fixes that improve maintainability (clearer naming, removed duplication, simpler structure).
  - A `non_blocking` entry whose claim begins `Ask the owner:` is a question, not a finding: put it to the user with the library named, and build nothing on it until they answer.
  - Skip a valid finding only when the fix would conflict with the design, reach outside the change under review, or go against an explicit user decision. Record why.
  - A finding you judge incorrect or inapplicable is not skipped but rejected, per the next bullet.
- Do not blindly accept every finding. If you disagree, explain why, and watch for fixes that would conflict with the design (e.g. a suggested guard that breaks a legitimate path).
- An "add a test" finding that names no fact the test would pin beyond what the source says is rejected with that reason, whichever reviewer raised it. A deletion with no behavior of its own is proved by the census in the PR body or landing report, not a test.
- If a finding conflicts with an explicit user decision, follow the user and record that the issue was intentionally skipped.
- Re-validate after each batch of fixes before re-reviewing: typecheck plus the tests the change and its proof touch, never the full suite CI runs anyway. A long run carries an explicit timeout, and a process is stopped by the PID you spawned, never by pattern.

  A personal private repository meters CI minutes, so there the full check runs locally once before the push. If you are not sure which kind it is, ask the user, or the lead when one briefed you.

### 7. Re-review until it converges

- After applying fixes, **re-run the review** on the updated state, one review per section, not a single overall pass.
- Repeat until **no valid blocking findings remain** and every non-blocking finding has been handled per step 6: fixed, skipped for a recorded reason, or rejected as incorrect or inapplicable.

  That convergence IS the gate: nothing commits or lands until the review has converged on the exact final content of the change being landed. At commit time that is the staged diff, since Git commits the index, not the tree. At merge time it is the branch or PR diff.

  This is the single definition of review convergence. Skills that gate on it (e.g. `/pr-landing-discipline`'s Converged) point here rather than restating it.

### 8. If these instructions don't work, fix the skill

- Fix the skill when a step fails in practice and the root cause is the instructions themselves (a documented flag no longer exists, an extraction rule misses the verdict, a copy-paste block breaks in a reproducible way).
  - Work around it to finish the current review, then capture the fix so the next run doesn't rediscover it.
  - First rule out transient causes (backend outage, sandbox restriction, local tool config). Those are not skill defects.
- This applies to **you, the driving agent**. The reviewer stays read-only per step 1.
  - Fix the skill only where you can edit its canonical source: in the authoring repo, edit the affected skill sources directly (`SKILL.md`, `references/`, or `scripts/`).
  - From an installed or vendored copy, or when you're not authorized to write, report the defect and your proposed fix to the user instead.
- Fold the root cause into the relevant step rather than appending a one-off note, and keep the copy-paste blocks runnable as written.
- A skill edit is a working-tree change like any other: finish the review with the corrected instructions, and put the edit through the same validate, review, and converge gate (steps 6 and 7).
