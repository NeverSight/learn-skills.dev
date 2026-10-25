---
name: second-opinion
description: Use when the user asks for a second-opinion review from another agent (e.g., "get a second opinion", "review with pi", "review using gpt-6-astra", "/second-opinion"), or when review-code runs with `--second-opinion`. Runs a fresh pi session (or Claude Code, when already inside pi) on the review-code skill and relays its review.
argument-hint: "PR number, ref range, all, path, or model"
user-invocable: true
---

# Second Opinion

Get a code review from a different agent by running a fresh headless session of it. The user wants that agent's take, not yours — relay it, don't redo it.

When `review-code --second-opinion` runs this skill, these rules govern only the relayed review. The caller's own review still runs, and a failure here does not stop it.

## Pick the reviewer

If `PI_CODING_AGENT` is `true`, you are running in pi — the reviewer is **Claude Code** (`claude`). Otherwise the reviewer is **pi**.

Assume the reviewer is installed, its default model is configured, and the `review-code` skill is available to it. Don't probe for any of these — if it fails, surface the error and stop.

## Rules

1. **Resolve the target in `review-code`'s vocabulary.** Don't compute the diff yourself.
   - PR number → `pr <N>`
   - "PR" with no number → `pr <N>` for the current branch's PR
   - Ref range (e.g., `main...HEAD`), `all`, `codebase`, or a path → verbatim
   - Otherwise → `diff`

2. **Pass the user's model verbatim to `--model`**, or omit `--model` if they named none — the reviewer falls back to its configured default.

3. **Run the reviewer's command from the repo root**, substituting target and model. The prompt is the same for both:

   ```
   Use the review-code skill to review <target> in this repo. Do not modify any files.
   ```

   pi:

   ```bash
   pi -p \
     --model <provider/model> \
     --exclude-tools edit,write \
     --name "review: <target>" \
     "<prompt>"
   ```

   Claude Code:

   ```bash
   claude -p \
     --model <model> \
     --disallowedTools Edit Write NotebookEdit \
     --allowedTools "Bash(git *)" "Bash(gh *)" \
     --no-session-persistence \
     "<prompt>"
   ```

   - `-p` prints only the final answer, so the output is safe to read in the main session.
   - The tool flags keep the reviewer from "fixing" findings while leaving `git` and `gh` usable.
   - Reviews can take several minutes — use the longest allowed timeout or run it in the background.

4. **Never resume a session.** No `-c`, `-r`, `--resume`, `--session`, `--session-id`, or `--fork` — prior context pollutes the review.

5. **Never inline the diff in the prompt, and never pass `--second-opinion` to the reviewer.** `review-code` resolves the target itself, a large diff breaks shell quoting, and the flag would make the reviewer spawn you back.

6. **Relay the review verbatim.** Don't summarize, re-rate, or add your own findings.

7. **On non-zero exit, print the error and stop.** Never fall back to a review of your own.

## Verification procedure

1. Every reported finding has a `path:line` citation. If findings lack them, the reviewer likely never loaded `review-code` — re-run once, then report. A clean review with no findings needs no citations.
2. If pi rejects the model, check `pi --list-models <name>` and retry with a listed name.
