---
name: open-skill-router
description: Picks the best installed skills to run for a task, and their order, from the user's IT role and the project's state (spec-kit, BMad, superpowers, codegraph...), then starts the first step. Use when starting a new project, or work with several steps (specify, plan, build, test, review) where no skill is named; when the user asks which skill, workflow or sequence of skills to use or where to start; when more than one installed workflow could fit; or when they state their role (data engineer, frontend, SRE, product manager...). Also for "route this", "bắt đầu project", "nên dùng skill nào".
---

# Open Skill Router

Your job is to turn a request into a short, ordered chain of the right skills and start on it. The chain matters because this machine may have many overlapping skills (several build workflows, several reviewers); mixing workflows corrupts their artifacts and wastes the user's time.

`open-skill` below means the CLI. If it is not on PATH, run it as
`uvx --from git+https://github.com/VoKhoiNhon/open-skill-standard@v0.6.0 open-skill`.

## 1. Classify, then route

You have read the conversation; the CLI sees one sentence. So decide first where the work starts and how big it is.

Phase, one of:
- `discover` (an idea, "should we", "what if")
- `research` (compare options, learn how something works)
- `specify` (requirements, a spec, user stories)
- `plan` (a design or task breakdown before code)
- `build` (new or changed code or data)
- `verify` (test it, check the numbers)
- `review` (look over code, a pull request or designs)
- `release` (ship, deploy, release notes)
- `operate` (something is broken, slow, wrong, empty or down, even when nobody says "bug")
- `learn` (a retro, a postmortem, something to remember)

Size: `small` (a one-line, mechanical or clearly bounded change), `medium`, or `large` (a new app or system).

Then run, from the project root:

```bash
open-skill route "<the user's request, in their words>" --phase <phase> --size <size> --project . --model <your model id> --agent <agent id> [--role <role>]
```

Pass `--phase` and `--size` when the conversation makes them clear; leave either out when you are unsure, and the CLI falls back to keyword detection. If the output says `"phase_from": "guessed"`, no keyword matched and the phase is a default: check it against the request and route again with `--phase` if it is wrong.

`--agent` is the coding agent you are running in (`claude-code`, `codex`, `cursor`, `gemini-cli`, `github-copilot`, `opencode`, `goose`, `windsurf`, `amp`; `open-skill agents` lists them). The chain then holds only skills that agent can load, under the names it invokes them by; leave it out if you are unsure. Pass `--model` only with the exact id your runtime gives you, not a guess; without it the CLI uses a generic profile. Pass `--role` only when the user stated one; otherwise the CLI uses their saved profile or project signals. The JSON output has `chain` (ordered steps with `invoke`, `phase`, `why`, `effort`), `knowledge` (the user's lessons and preferences that apply), `missing` (useful skills that are not installed or need a project init), `advice`, and `model` (notes for the model you are running on).

## 2. Check it against the real request

The CLI ranks by your phase and size, the role, text relevance and project state; you read the request itself. Drop a step that clearly does not serve the request, or add one the user asked for. Keep one build workflow: spec-kit, BMad and superpowers build steps never appear together, and the project's own framework (`.specify/` or `_bmad/`) wins.

If `advice` is `do directly`, skip the chain and just do the task.
If a step has `ask`, the top two options are close: ask the user one question with those two options.

## 3. Announce in one line, then start

Tell the user the chain in one line, plus any `knowledge` item that changes how you will work, for example:

> Chain: speckit-plan → speckit-implement → data:validate-data → code-review. Applying your note: backfill in bounded batches.

Then invoke the first skill with the Skill tool. For `missing` items, mention the install or init command in one line; running project init commands (`specify init`, `bmad setup`, `codegraph init`) is the user's decision.

Apply the `model.addenda` lines for the rest of the session; they are prompting notes measured for the model you are running on.

## 4. Record what happened

When the chain is finished (or abandoned), record which skills actually ran, so future routes learn the user's habits:

```bash
open-skill feedback <route_id> --ran <invoke1,invoke2,...> --outcome ok|fail [--note "<why>"]
```

If the user corrected the route ("use superpowers here, not spec-kit"), that correction is exactly what feedback is for; for a lasting preference also use the `open-skill-learn` skill.

## Without the CLI

If `uv`/`uvx` is unavailable or the command fails, route by hand:

1. Identify the role from the user or the project, then read `references/roles/<role>.md` (index: `references/roles/README.md`).
2. Start at the phase you classified in step 1 and add the phases it needs: large new work starts at specify, medium at plan, both then build, verify and review; operate is followed by build and verify; release comes after verify.
3. For each phase, take the first primary skill that is installed; use an alternative only if no primary is.
4. Announce and start as above; there is no route to record feedback for.
