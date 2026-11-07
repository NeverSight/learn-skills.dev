---
name: sassy-scout
description: >-
  Scout an area of the repo on demand and write the shared grounding brief other
  agents read, so nothing downstream re-explores the same code. Returns a short
  gist plus the brief path, never a wall of file contents. Use when a plan, fix,
  or review needs verified project evidence before it starts.
argument-hint: "[the area or question to ground]"
disable-model-invocation: true
---

# Sassy Scout

**Outcome:** a grounding brief on disk for the area you asked about, and a 3–5 line gist back in this context. Nothing else.

**Orchestrator only.** Do not read the repo yourself. One `scout` dispatch per independent area, in parallel when the areas do not overlap.

**Harness.** Loading another skill, dispatching an agent, and any command you hand the user follow the `sassy-setup` skill's `references/harness.md`. Read it once per run, before the first of those.

## When to use

- Before planning a change, to ground files, patterns, prior art, and any prior learning already written about the area.
- Before a fix, to ground the failure surface once instead of twice.
- Before a review of unfamiliar code, when the diff alone is not enough.
- Whenever more than one agent is about to explore the same area.

## Workflow

1. **Scope.** Reduce the request to one question the brief will answer, in one line. If it is really two questions, use two dispatches.
2. **Dispatch `scout`** with that scope, what the caller intends to do with it, and the paths or areas you already suspect. The brief also carries matching docs from the project's knowledge paths (`knowledge.read` in `.sassywares/config.yaml`, nearest walking up) — pass that section on to the caller rather than dropping it.
3. **Keep the gist.** Read the returned gist; do not pull the brief's bulk into this context.
4. **Report the brief path** to the caller, so downstream agents read it instead of scouting again.

## The brief

The scout writes it under `/tmp/sassywares/<harness>/grounding/` (see `references/harness.md` in the `sassy-setup` skill), keyed by the worktree root:

```bash
SW=/tmp/sassywares
HARNESS="${SASSY_HARNESS:-$(if [ -n "${CLAUDECODE:-}" ]; then echo claude; elif [ -n "${PI_CODING_AGENT:-}" ]; then echo pi; else echo other; fi)}"
ROOT="$SW/$HARNESS/grounding"
ROOT_ABS=$(cd "$(git rev-parse --show-toplevel 2>/dev/null || echo "$PWD")" && pwd -P)
KEY=$(printf '%s' "$ROOT_ABS" | shasum -a 256 | cut -d' ' -f1)
BRIEF="$ROOT/$KEY.md"
```

It is fresh only while its `head` and `dirty` lines match the working tree. After any commit or edit, re-scout.

## Hard rules

| Rule | Requirement |
|------|-------------|
| One question | A brief answers one scoped question. Split, do not sprawl. |
| Gist only | Return the gist and the brief path. Never paste the brief. |
| No edits | Scouting is read-only. It never changes code or commits. |
| Learnings are listed, not judged | Prior learnings come back as path and title. The consumer decides whether one applies; scout never ranks or recommends them. |
| Fresh or re-scout | A stale brief is worse than none. Check the header before reusing it. |
