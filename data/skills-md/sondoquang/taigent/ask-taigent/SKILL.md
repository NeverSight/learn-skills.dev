---
name: ask-taigent
description: Ask which Taigent skill, step or CLI command fits your Taiga situation. A router over the taiga-* skills and the way we work with Taiga.
disable-model-invocation: true
---

# Ask Taigent

Before stating what a skill does, or recommending a step be skipped, read that skill's `SKILL.md`: the summaries here are for orientation only. The same goes for the docs named below: they are the source of truth, this map only points at them.

The docs live in the **taigent root**: the project root when its `package.json` has `taigent` as `name`, else `node_modules/taigent/`. Invoke a skill as `/<name>` in Claude Code, `$<name>` in Codex.

Out of scope: general engineering work (specs, tickets, TDD, reviews, bugs). Say so, and point to `/ask-matt` when that skill is installed.

## The main flow: idea → Taiga

The route most work travels. Every write to Taiga goes **plan → review → apply**: the agent edits a manifest in the repo, a human reviews it, and the `taigent` CLI applies it only after an explicit yes.

1. **`taiga-setup`** once per machine and per project: the `taigent` CLI, the user's Taiga login (`npx taigent login`, typed by the user in their own terminal), the Taiga MCP server. Every other skill sends you back here when one of them is missing.
2. **`taiga-bootstrap-project`** when the Taiga project does not exist yet, or lacks modules, tags, members or custom attributes: `taiga/<slug>/project.yaml` → dry run → confirm → bootstrap. Re-running only fills gaps.
3. **`taiga-plan-backlog`** turns a spec, a PRD or a one-line request into `taiga/<slug>/backlog.yaml` (epics, stories, tasks). Files only: it reads Taiga to avoid duplicating hand-made work, and patches the existing manifest in place so every key survives.
4. **Review**: the human reads `git diff taiga/<slug>/` like a code diff.
5. **`taiga-apply-backlog`**: `taigent plan` → shows it → confirm → `taigent apply --yes`. Commit `taiga/<slug>/state.json` with the manifest.

Beside the main flow:

- **`taiga-upload-docs`**: specs, ADRs, guides and meeting notes as wiki pages and attachments, declared in `taiga/<slug>/docs.yaml`, after bootstrap (and after the backlog when attachments target item keys).
- **`taiga-status-report`**: progress by sprint and by epic, or one quick count or lookup. Read-only through the MCP server, any time.
- **`taiga-my-tickets`**: your tickets (user stories assigned to you) in a period, this week by default: closed, due and still open, with due status and effort. Read-only through `taigent tickets`, any time.
- **`taiga-update-ticket`**: move your own tickets to another status (close = `Done`) or comment on one, at once: the request is the confirmation. Through `taigent status` and `taigent comment`, never MCP.

## On-ramps

Starting situations, and where each merges onto the flow.

- **New machine, or a project that should use these skills** → `taiga-setup`. In another project: `npx skills add sondoquang/taigent` for the skills, `npm install -D github:sondoquang/taigent` for the CLI; neither registers the Taiga MCP server. `taiga-setup` checks the CLI, the login (`taigent whoami`; the user runs `npx taigent login` in their own terminal, which stores a token in the OS credential store, never the password) and the MCP server (`taigent mcp`), including a project server left pending or rejected, and names each fix (`docs/cli.md` §Using the skills in another project).
- **Brand-new Taiga project** → `taiga-bootstrap-project`, then `taiga-plan-backlog` and `taiga-upload-docs`.
- **Project already on Taiga, no manifest yet** → `taiga-plan-backlog`. Hand-made items carry no `src:` tag; it lists them and asks before adding the same work. `taiga-bootstrap-project` completes the existing project when you are its admin.
- **New or changed requirement** → `taiga-plan-backlog` with the request as the spec, then review and `taiga-apply-backlog`.
- **"How far along are we?" or "how many …?"** → `taiga-status-report`.
- **"What are my tickets this week?" or "what did I close last week?"** → `taiga-my-tickets`.
- **"Close #84", "move the login ticket to Ready for test", "comment on #84"** → `taiga-update-ticket`.
- **Daily ticket messages and chat on Telegram** → README §6 (Bun, bot, plugin, pairing, permissions, schedule), set up once per user and machine; how it works in `docs/cli.md` §Telegram.
- **Remove, rename or move items on Taiga** → the CLI never deletes. An item dropped from the manifest becomes an **orphan** that `plan` reports; a moved story keeps its old epic link, reported as `staleLinks`. A human cleans both up on Taiga. Keys never change after apply: a new key is a new item.
- **Status of your own tickets** → `taiga-update-ticket`. Assignee, sprint, points, and the status of other people's items: people set these on Taiga; manifests carry none of them.
- **A command fails** → branch on its exit code (`docs/cli.md` §Exit codes). Exit 4: the manifest breaks a convention; `taigent validate` lists each problem with its rule. Exit 2 saying `not logged in`, or exit 5 naming a refused login, `TAIGA_*` variable or expired stored login: `taiga-setup`. Never ask for a password: the user runs `npx taigent login` themselves.

## How we work

The rules every skill above follows; `docs/taiga/conventions.md` holds them in full.

- **Writes go only through the `taigent` CLI.** Taiga MCP is for reading, reports and comments (§1). Some MCP tools are broken and **banned**; the others that write skip the `src:<key>` tag that prevents duplicates (§10).
- **`--yes` only after an explicit confirmation** of the exact plan or dry run shown, re-planned just before applying. The writing skills (`taiga-apply-backlog`, `taiga-bootstrap-project`, `taiga-upload-docs`) run only when you invoke them. `taigent status`/`comment` take no `--yes`: they edit one of your own tickets that the request names.
- **Manifests follow the conventions**: project name and slug (§2), template and modules (§3), prefixed tags (§4), item keys (§5), story and task templates (§6), wiki slugs (§8), attachment names (§9). `taigent validate` checks §2–§5 and §8–§9 offline; §6 is on the author. Reports use the exact status names of §7.
- **Run `npx taigent` from the project root** whose `package.json` is taigent's own or lists `taigent` as a dependency; elsewhere npx would fetch an unrelated package.

## CLI map

Which command belongs to which step; syntax, flags and output in `docs/cli.md`.

| Command | Step | Driven by |
|---|---|---|
| `taigent validate --project <slug>` | End of every manifest edit; offline | plan-backlog, bootstrap-project, upload-docs |
| `taigent plan --project <slug>` | Review: what apply would change; read-only | plan-backlog (`--json`), apply-backlog |
| `taigent apply --project <slug> --yes` | Apply `backlog.yaml` | apply-backlog |
| `taigent bootstrap --project <slug> --dry-run\|--yes` | Create or complete the project from `project.yaml` | bootstrap-project |
| `taigent upload --project <slug> --dry-run\|--yes` | Wiki pages and attachments from `docs.yaml` | upload-docs |
| `taigent tickets --from <day> --to <day> [--project <slug>]` | Your tickets closed or due in those days and every open one, with due status and effort; read-only | my-tickets, update-ticket |
| `taigent status --project <slug> <ref> <status>` | Move your ticket to that status, at once | update-ticket |
| `taigent comment --project <slug> <ref> <text>` | Comment on your ticket, at once | update-ticket |
| `taigent notify week\|day\|eod [--dry-run]` | Your tickets of the week, of the day, or due by today and still open, to your Telegram chat | a scheduled task (Task Scheduler, cron) |
| `taigent skills sync\|check` | Skill maintenance, below | you |

## Maintaining the skills

In the taigent repository; `AGENTS.md` and `docs/cli.md` §Skills hold the full rules.

- The **Taigent skills** are every `taiga-*` skill plus this one. Edit them in `.agents/skills/`, then run `npx taigent skills sync` to refresh the `.claude/skills/` copies; `npm test` fails while they differ. The other skills are vendored from `mattpocock/skills` (`skills-lock.json`), and taigent leaves them alone.
- A skill that pre-approves `taigent apply`, `bootstrap` or `upload` is user-only on both agents.
- Adding, removing or changing a Taigent skill: update this map in the same change.
- Bumping the `taiga-mcp-server` pin: its exact version in `package.json`, then the version named in `taiga-setup`, the `taiga-*` skills' tool notes, `docs/cli.md` and `docs/taiga/conventions.md` §10, together.
