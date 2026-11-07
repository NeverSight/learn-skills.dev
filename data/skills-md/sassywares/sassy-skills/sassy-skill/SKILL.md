---
name: sassy-skill
description: >-
  Create, retune, or improve an Agent Skill. Asks where the skill should live —
  inside this suite, in a project, or for one user — then writes it there with
  the rules and release steps that location requires. Use when asked to create a
  skill, turn a workflow into a skill, fix a description or triggering,
  restructure a bloated skill, or retune an existing one.
argument-hint: "[mode:create|retune|verify] [name, idea, or skill path]"
disable-model-invocation: true
---

# Sassy Skill

**Outcome:** a well-formed Agent Skill at a location the user chose, an existing skill improved and re-verified, or a report on one — and the harness loads it with no diagnostics.

**Modes.** `mode:create` writes a new skill. `mode:retune` changes the smallest thing that fixes a named failure in an existing skill. `mode:verify` checks an existing skill against the checklist and reports — it edits nothing. Omitted, detect it from the argument: something that already resolves to a skill directory is `retune`, or `verify` when the user only asked whether it is any good; anything else is `create`. State the mode you picked and why; when both are plausible, ask instead of guessing.

**Locations are not interchangeable** — they decide who gets the skill, how it ships, and what it may be called. Ask before writing.

**Scope:** skills only — not extensions, packages, or prompt templates.

**Harness.** Loading another skill, dispatching an agent, and any command you hand the user follow the `sassy-setup` skill's `references/harness.md`. Read it once per run, before the first of those.

## One mode, one reference

Each mode's mechanics live in its own file. Read the one you were dispatched to — **and only that one**. A `create` never reads `retune`'s failure map, and a `verify` never picks up a fix from it: that adjacency is exactly how a read-only check turns into an edit.

| Mode | Load | It ends with |
|---|---|---|
| `create` | `references/create.md` | a new skill on disk, installed and verified |
| `retune` | `references/retune.md` | the smallest edit that kills one named failure, re-verified |
| `verify` | `references/verify.md` | a report, and no file touched |

Everything below is shared by all three: the location table, the Agent Skills rules, the shape rule, the checklist, and the verification run. Read it once, then your one reference.

## Agent Skills rules (the essentials)

The suite targets the **Agent Skills specification** (agentskills.io), so a skill works in any harness that loads it — pi, Claude Code, and others. Write to the spec, not to one harness.

- A skill is a **directory containing `SKILL.md`**. Discovered recursively.
- **Name:** lowercase letters, numbers, hyphens; no leading/trailing/consecutive hyphens; ≤64 chars. Match the directory name.
- **Description:** required, ≤1024 chars. The harness advertises name + description up front; the body loads only when the skill is used, so the description alone decides whether the skill ever fires. Write **what it does and when to use it**, with concrete verbs and the words a user would actually say — "can't trigger" is almost always a description that named the topic and never the moment.
- **Frontmatter fields:** `name`, `description` (required); optional `license`, `compatibility`, `metadata`, `allowed-tools`, `disable-model-invocation`.
- Use `disable-model-invocation: true` for skills that should run only when the user invokes them. Some harnesses (Claude Code) then hide the skill from the model entirely, so a skill that loads another must read its `SKILL.md` — the `sassy-setup` skill's `references/harness.md` defines that.
- **Reference other skills by name, never by absolute path.** The suite can live in `~/.agents/skills/`, a project `.agents/skills/`, or inside `node_modules/`, so "load the sassy-commit skill" is portable where a `~/…` path is not. Name a bundled file as "the sassy-setup skill's `references/config.md`".
- Harnesses **validate when they load skills**; a malformed or descriptionless skill warns or is skipped. Reloading applies changes (the command per harness is in `references/harness.md`).
- The spec at agentskills.io is authoritative when the rules here are not enough. Never rely on a field or behavior only one harness supports.
- **No harness-only machinery.** No harness-specific commands, extensions, tools, or paths in the workflow. Where harnesses genuinely differ, point at `references/harness.md` instead of naming one.

## Where the skill lives

Ask which one, unless the request already made it obvious. The answer changes the name, the sharing, and whether a release is needed.

| Location | Path | Who gets it | Extra work |
|---|---|---|---|
| **Internal** — part of this suite | `skills/<name>/` in the sassy-skills repo | Everyone, once pushed to `main` | Name it `sassy-<name>`, run `scripts/sync.sh` — it bumps the patch version, tags, and publishes |
| **Project** — team workflow | `<repo>/.agents/skills/<name>/` | Everyone who clones that repo | Commit it; prefix the project (`tap2-…`) so it can't collide with a suite skill or a harness built-in |
| **User** — personal workflow | `~/.agents/skills/<name>/` | Only this person, every repo on this machine | None — but nothing gates it either; never put something a teammate needs here |

Recommend by audience: the team needs it → **project**; only the requester → **user**; it belongs to every project using this suite → **internal**.

Internal is the only one that ships to everyone. Never choose it silently: once it lands on `main`, every consumer gets it on their next `npx skills update`. Say that out loud when you do.

Paths in the table are the defaults. `.agents/skills/` is read by pi and others; Claude Code reads only `.claude/skills/` (project) and `~/.claude/skills/` (user), so a hand-placed skill there also needs a link in those directories — `npx skills add` creates them for installed skills. Harnesses also read `skills` arrays in settings and installed packages, so a skill may live elsewhere — write down where it actually went.

## Shape rule — split on outcomes, not on topics

- **One `SKILL.md` is the default, but it is a decision, not a reflex.** Length never decides the shape; the paths do.
- **Split whenever the skill branches into paths that end differently.** A mode, trigger, or branch that writes a different thing, forbids a different thing, or is never needed in the same run as its sibling gets its own `references/<path>.md` — **even at three paragraphs**. How small each path is does not matter: what matters is that a model running path A never reads path B's instructions next to A's. Divergent outcomes sharing one file bleed into each other, and the bleed looks like helpfulness until it has already written the wrong thing. Think ahead when you write it, not after the first misfire. This skill is shaped by its own rule.
- **Never split a shared surface.** What every path needs — ids, board or table values, hard rules, API quirks, house style — stays in `SKILL.md`, or each path pays to load it and they drift apart. One reference per **outcome**, never one per **section**: `references/` holding five short topic files is the oversplit, and it makes routing vaguer, not sharper.
- **`SKILL.md` becomes routing.** State the dispatch explicitly — a table naming exactly one reference per path, plus "read that one only". That sentence is what prevents the bleed; a pointer buried in a paragraph does not.
- A reference that is read on *every* run saves nothing and may cost a little, so it belongs in the body.
- Keep `SKILL.md` an index: outcome → hard rules → workflow → explicit pointers ("read `references/x.md` before doing Y"). Never bury path-specific detail in a monolithic file.

## Self-check checklist

The gate for a new or edited skill, and the instrument in `mode:verify`.

- [ ] `name`: lowercase/hyphens, ≤64, matches the directory.
- [ ] `description`: states what **and** when, ≤1024, not vague.
- [ ] Frontmatter is valid YAML with the required fields.
- [ ] Every `references/…` path exists and is pointed to explicitly in the body.
- [ ] Each outcome path that ends differently has its own reference, and the body dispatches to exactly one of them per run.
- [ ] No reference exists merely because its content was a separate section — that is oversplitting, not shaping.
- [ ] The body is lean; no always-read detail needlessly hidden in a reference.
- [ ] No secrets, and no capability the skill cannot actually use.

## Verification — how every mode ends

- Reload the harness (command per `references/harness.md`).
- Confirm the harness lists the skill with no load warning.
- Invoke it with the harness's syntax and confirm it loads and behaves.

`create` and `retune` are not finished until this passes; `verify` exists to run it and report.

## Hard rules

| Rule | Requirement |
|------|-------------|
| Ask before writing | The location — internal, project, or user — is the user's call, never the cwd's. State the mode you inferred. |
| Verify writes nothing | `mode:verify` ends with a report. If you spot a fix while verifying, name it and let the user ask for the retune. |
| Retune is minimal | One named failure, the smallest change that kills it. No drive-by rewrites, no tidy-ups nobody asked for. |
| Split by outcome | Divergent paths get their own reference even when tiny; shared surfaces stay in the body. |
| Name skills, not paths | Reference another skill by name so the suite stays portable across install locations. |
| Internal is a release | Putting a skill in the suite ships it to every consumer on `main`. Never choose it silently. |
| Nothing untestable | No secrets, and no capability the skill cannot actually perform. |
