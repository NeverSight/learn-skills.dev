---
name: self-improve
description: Retrospect the current agent session (failures, user corrections, detours, token-heavy or slow turns) into lessons, shipped as minimal edits to jinsyin/skills skills — or a new skill, or a `setup-rules` convention for a heavy manually-invoked third-party skill — each as GitHub Issue + PR; nothing qualifies → closed `no-pr` record Issue. Args `[--dry-run] [focus]`. Invoke only when the user, a rule, or another skill calls for it.
---

# self-improve

Session evidence → lessons → minimal skill diffs → Issue + PR. PR = human review gate: open Issue + PR without asking approval; push only to `self-improve/*` branches, human merges.

Upstream: `jinsyin/skills` (skills in `skills/<name>/`). Keep main context lean: work from digest, open raw transcript only for specific turns.

Args: `--dry-run` report only, no Issue/PR; free text narrows focus.

## 1. Collect evidence

Current conversation + `python3 <skill-dir>/scripts/transcript.py digest --runtime <rt> [<session-id>]`. `<rt>` = own runtime: `claude`, `codex`, `cursor` (IDE or `cursor-agent`), `agy` (Antigravity); omitted → Claude Code only. Pass own session id when known; else newest session of cwd, maybe another one. Digest compact, only source of token/time data — run even if context looks complete. `[cost] unavailable` = runtime records no tokens: token figures `unknown`, cost lessons only from wall time or call counts.

Record provenance for Issue: source project name (git root basename), agent runtime, session id + name. `transcript.py meta` (same args) prints session id, name, runtime, most-used and last `model/effort` pair; improvement run = same session: reuse its id, `last` pair = run's. Copy its `unknown` as-is. Done when digest read and provenance recorded.

Digest marks `USER*` (possible correction), `ERROR`, `REJECTED`, `[retry xN]`, `[repeat-error xN]`, `SKILL`/`SKILL-LOADED` (with path), cost lines: `[cost]` totals for main agent + subagents, `[heavy-turn N]` (turn ≥15% of input) / `[skill-run N]` (other skill turn): one run's in/out tokens, calls, compactions, peak-ctx, subagents, result chars, wall time (includes waiting on user), skills; `HEAVY-AGENT` (subagent ≥200k tokens), `BIG-RESULT` (tool output >20k chars), `[skill-cost]`/`HEAVY-SKILL` (per-skill totals incl. its subagents; heavy = ≥25% of session tokens or wall time; `via=manual` = user-typed slash command, `auto` = Skill call by model or another skill). Markers = hints; judge each by context.

## 2. Scope

Candidate skills = skills used in evidence (Skill call, slash command, `SKILL-LOADED`, or reading/editing skill's own files) ∩ upstream skills: entries in project's `skills-lock.json` with `source` `jinsyin/skills` (case-insensitive), or load path inside a `jinsyin/skills` checkout. Lessons owned by no loaded skill can still justify new skill. `self-improve` always candidate (step 6). Third-party skills out of scope, except one tagged `HEAVY-SKILL via=manual`: retrospect its call details for lessons belonging in a `setup-rules` convention, since its files can't change here. Everything else (other third-party skills, project's own code) → final summary only.

## 3. Extract lessons

Look for: user corrections, rule/instruction/config that existed but didn't take effect, wrong-phase mistakes, detours + abandoned approaches, retries, tool errors, agent questions a skill should have answered, repeated manual steps.

Also waste a skill caused — cutting tokens and flow length is goal equal to correctness: no-value steps, steps that could merge or run parallel, broad reads where targeted grep would do, re-reading what's in context, oversized/over-scoped subagents (or heavy inline work a subagent should isolate), strong models on mechanical subtasks, interview rounds skill could have defaulted.

Gate each lesson:
- **Strong** (1 occurrence enough): explicit user correction or rework from skill gap or ignored rule; `heavy-turn`, `HEAVY-AGENT` or `BIG-RESULT` clearly caused by skill instruction.
- **Weak** (needs ≥2 occurrences): detours, retries, tool errors, repeated questions. Each run sees one session, so also count same observation under `## Below the gate` of earlier Issues (`gh issue list -R jinsyin/skills --label self-improve --state all --search "<skill> <keywords>"`, `no-pr` records included); cite each as evidence row with its Issue #.
- Below gate → summary only.

Done when every lesson is Strong, Weak with ≥2 occurrences, or below gate.

Keep only lessons changing *future* behavior beyond this one project. Drop one-off typos, project-specific facts, model slips a rule wouldn't have prevented.

## 4. Root-cause against latest upstream

Clone once into scratchpad (or temp dir): `gh repo clone jinsyin/skills <tmp>/skills -- --depth 1`. If cwd already `jinsyin/skills` checkout, `git fetch` + add `git worktree` on `origin/<default-branch>` instead; leave user's working tree alone. Read target skill there — not possibly stale installed copy. If installed `self-improve` differs from the clone, run the rest of this pass from the clone's `SKILL.md`: the loaded copy may predate rules it must follow (e.g. Issue language). Get `<default-branch>` via `gh repo view jinsyin/skills --json defaultBranchRef -q .defaultBranchRef.name`; never guess `main`.

Give every lesson exactly one verdict:
- **Already covered upstream** → drop (installed copy stale; note for sync). Includes corrections already fixed later same session, e.g. while authoring that skill.
- **Rule exists but did not fire** → fix *why* in that rule: wording, placement, precedence, discoverability; one rule stays single source of truth.
- **Gap** → add smallest instruction to owning section.
- **Heavy third-party skill** → rule steering how agent drives it (skip/override step, default answer, delegate, cap output), never copy of its content. Target `skills/setup-rules/assets/conventions/<ecosystem>.md` when one matches (e.g. `superpowers.md`); else create it + register in `setup-rules/SKILL.md` (convention order, file list, Workflow 2 menu).
- **No owner, reusable across projects** → new skill (`skills/<name>/SKILL.md`, matching existing skills' style).

Minimal-diff rules: edit smallest owning passage; prefer rewording over adding, deleting/merging over rewording when step is waste; fewest words that still change behavior — every word paid on every load; no restructuring; keep skill's language + tone; growth per pass ≤ ~20% of file. State target behavior positively and explain *why* in instruction itself; plain reasons steer better than ALL-CAPS MUSTs.

Dedupe before writing: `gh issue list -R jinsyin/skills --state all --search "<skill> <keywords>"`, same for `gh pr list`. Open match → add new evidence as comment, skip; closed `rejected`-labelled match (older: closed not planned, no `no-pr`) → skip unless evidence materially new; `no-pr` records feed step 3's weak count, not rejections.

`--dry-run`: skip step 5, run step 6, then print each would-be Issue body in full (filled template, step 5 language) so preview matches what would be filed.

## 5. Issue + PR, one pair per skill

Group all lessons for same skill into one pair; heavy third-party lessons join `setup-rules` pair, one extra `--label` per third-party skill. In step 4 clone/worktree:

1. Follow repo's contribution conventions (`CLAUDE.md`, `AGENTS.md`, commit style, `CHANGELOG.md` `[Unreleased]` entry in file's language). Skills its workflow names are missing from this project's skill list and gitignored upstream: run `./skillsw install` in clone/worktree to restore them from `skills-lock.json`, then run each from its `SKILL.md` under `.agents/skills/`.
   Issue + PR bodies: prose you author (field values, table cells, root cause, proposed change, change notes) in Chinese for the human reviewer; template skeleton verbatim in English so Issues read alike — headings, field keys (`Skill:`, `Source project:` …), table header, checklist items, `<model>/<effort>` pairs, Signal `strong`/`weak`. Session quotes verbatim.
2. Issue: fill `.github/ISSUE_TEMPLATE/skill-improvement.md` (drop front matter), create:
   `gh issue create -R jinsyin/skills --title "<type>(<skill>): <summary>" --label self-improve --label <skill> --body-file <file>`, one `--label` per improved skill (create missing labels first with `gh label create <name> -R jinsyin/skills`). Issue = report — provenance (step 1), evidence quotes, failing step, rule that didn't fire, proposed fix, lessons below gate. Cost lessons: one evidence row per cited run with its `[heavy-turn]`/`[skill-run]` fields, so reviewers compare runs without transcripts.
3. Branch `self-improve/<skill>-<issue#>`, apply diff, commit, `git push -u origin <branch>` unpiped so network failures surface; retry until pushed.
4. PR: fill `.github/pull_request_template.md`, `gh pr create -R jinsyin/skills --base <default-branch> --head <branch> --label self-improve --label <skill> --body-file <file>` with `Closes #<issue#>`.

## 6. Improve self-improve

Last, retrospect this `self-improve` run: ambiguous/missing instructions you guessed at, `transcript.py` errors or noisy output, wasted calls, this run's own cost in digest, any user correction to this run. Same gate, root-cause, dedupe; ship survivors as own `self-improve` Issue + PR (`--dry-run`: add to report). Judge only this skill's instructions, not lessons it produced.

## 7. Wrap up

**Record Issue**: run filed no Issue, PR or comment (every lesson below gate, covered or dropped) → still open one so every retrospective leaves a trace: title `retro(<source project>): <summary>`, labels `self-improve` + `no-pr` (create if missing), body = template's `## Context` + `## Below the gate`, each observation with why it fell short (step 5 language split). No branch, no PR. Close it at once — nothing to act on: `gh issue close <#> -R jinsyin/skills --reason "not planned" --comment "<reason>"`, Chinese reason naming why nothing qualified. `--dry-run`: print body + reason instead.

Print short table: skill · lesson · Issue · PR, plus skipped/below-gate items. Then ask whether to sync changed skills into this project. On yes, copy changed files from local PR branch (shallow clone has no `origin/<branch>` refs) over each installed copy (`.claude/skills/<name>`, `.agents/skills/<name>`, …; resolve symlinks, write real target once). Note re-running `npx skills@latest add jinsyin/skills` after merge makes it official. If convention changed, tell user run `setup-rules update` to refresh `CLAUDE.local.md` (explicit-invocation only).