---
name: write-great-skill
description: "Write or improve an agent skill (SKILL.md + scripts). Use when someone wants to create, write, build or draft a skill; turn a checklist, runbook, procedure, how-to or a prompt they keep repeating into a skill or slash command; make the agent do a task the same way every time; or fix a skill that does not fire, fires at the wrong time, or runs differently each run. Interviews first (the trigger, what the user knows that no model knows, what must never happen, which steps are mechanical), drafts the folder (a short SKILL.md, scripts/ for the mechanical steps, references/ read on demand), checks it with a script, then curates it with the user. Works for Claude Code, Codex, Cursor, Hermes and any Agent Skills tool."
---

# Write a great skill

A skill is a folder that teaches an agent one procedure it cannot know on its own. The
agent loads it when the situation comes up, and not before. Your job: get the procedure
out of the user's head, split it into judgment and mechanics, and ship a folder that fires
on the right request.

## Steps

1. **Interview.** Ask one question at a time, each with your recommended answer:
   - **Trigger:** what situation starts this task? Which exact words would the user type? Collect 3-5 real phrasings.
   - **Knowledge:** what does the user know that no model knows? Commands, paths, order of steps, system names, the usual causes.
   - **Never:** what must never happen? Each answer becomes a hard rule or a gotcha.
   - **Mechanics:** which steps are the same every run (commands, checks, files with a fixed shape)? Each one becomes a script.
   - **Home:** this repo only (`.claude/skills/<name>/`, shared through git) or every repo (`~/.claude/skills/<name>/`)? Other tools use their own skills folder with the same format.

   If the user already gave you the material (a checklist, a runbook, a doc), or nobody can
   answer (a headless run), take the answers from the material, write your assumptions
   down, and continue. Done when you can list every step and mark it judgment or mechanical.

2. **Write the description first.** The agent sees only the descriptions when it decides
   which skill to load; a vague one is never picked.
   - Write it for the model, in the user's words. The first sentence names the task in at most 57 characters (Hermes shows only that much). Then `Use when …` with the phrasings from step 1, then what it does and what it never does.
   - Keep it under 1,024 characters (the Agent Skills spec limit). Claude Code cuts the listing at 1,536.
   - Never picked: `Helps with deployments.` Picked: `Deploy to production or staging. Use when the user says deploy, ship, release, push to prod or roll back.`

   Done when every phrasing from step 1 appears in the description, or a close match does.

3. **Draft the folder** from [references/skill-template.md](references/skill-template.md).
   SKILL.md is the short entry point (aim under 100 lines); `scripts/` holds the mechanical
   steps; `references/` holds long material that only one step needs; `examples/` holds one
   worked case. The agent reads a supporting file only when a step sends it there.
   - **Judgment stays as instructions. Mechanics go into scripts.** A model is not deterministic: every step written as prose can run differently each time. Put command sequences, checks and fixed-shape files in `scripts/`, and call them from SKILL.md with the exact command line.
   - Name the script that does the skill's main action after the skill (`scripts/<name>.sh`), and each helper after its step (`scripts/<step>.sh`, for example a preflight check).
   - A script stops on the first error (`set -euo pipefail`), checks its arguments and preconditions, and prints each step. A script that pushes, tags, deploys, publishes or sends does a dry run by default and acts only with `--yes`; SKILL.md says to show the dry run and get approval first.
   - Every step: the action as an imperative sentence, the exact command, path or name, then `Done when …` with a check the agent can verify.
   - Link each reference from the step that needs it, one level deep.
   - Add `## Gotchas`, seeded with every "never" from step 1 and every trap the user named.

   Done when every mechanical step is a script call and every script passes `bash -n` (or its language's syntax check) and runs its dry run or `--help` with no side effects. To test a git push for real, point it at a local bare clone (`git clone --bare . <tmp>/origin.git`). Never test a script against the user's real accounts (cloud, password manager, payment provider, production): read the tool's `--help` instead.

4. **Cut what the agent already knows.** For each line ask: would the agent do this
   without it? Lines like "write clean code", "use meaningful names" or "follow best
   practices" change nothing: delete them. If behaviour does not change without a line, it
   was a no-op, and it costs context on every run. Spend the lines on what pushes the agent
   off its defaults: this system's facts, this team's order, the traps. Done when every
   line names a command, path, number or name, or a rule the agent would break without it.

5. **Check it.** Run `node <this-skill>/scripts/check-skill.mjs <new-skill-folder>`. It
   checks the frontmatter, the name, the description length and first sentence, links to
   missing files, scripts without the executable bit, `TODO` markers, SKILL.md length and
   filler phrases. Done when it exits 0 and every warning is fixed or has a stated reason.

6. **Curate with the user.** Show the folder tree, the description and each script. Go
   through [references/review-checklist.md](references/review-checklist.md). Ask: "Which
   words would you type when you need this?" Put missing words at the front of the
   description. Headless: list the open questions at the end of your report. Done when the
   user approves, or the open questions are listed.

7. **Test the trigger** (needs the `claude` CLI). From the folder where the skill is
   installed, run `<this-skill>/scripts/fires.sh <skill-name> "<request>" ... --not "<request>"`
   with 3 requests that do not name the skill and should fire, then `--not` and 1 that
   should not. On a miss,
   add the user's missing words to the front of the description and run it again. Done
   when the script prints PASS (3 of 3 fire, and the negative stays quiet).

## Writing for agents

- Short imperative sentences: "Run", "Stop", "Ask". One instruction per sentence.
- Concrete: `npm run build`, not "build the project"; "at most 3 retries", not "a few".
- One word per thing. If step 2 says "release branch", step 5 does not say "deploy branch".
- Examples over adjectives: show one good output instead of asking for "clear" or "robust".
- No intro, no motivation paragraph, no "this skill helps you". Start with the job.

## Gotchas

- The description is the trigger, not a summary. A perfect body under a vague description never runs.
- Rules for every conversation go in `CLAUDE.md` or `AGENTS.md`, not in a skill. A skill holds a procedure.
- The name is lowercase letters, digits and single hyphens, at most 64 characters, and equals the folder name.
- The agent does not read a file in `references/` unless a step says when to read it.
- Secrets never go in a skill. Scripts read them from the environment or the tool's credential store.
- The gotchas section grows: every time the agent gets something wrong inside a skill, add one line to that skill's gotchas.

Last verified: 2026-10-03 with Claude Code 2.1.288 (a TicketBay release skill 12/12, a key-rotation runbook from scratch 9/9, automatic picks 5/5 with 144 skills installed and 5/5 project-only)

Inspired by Matt Pocock's writing-for-agents (MIT).
