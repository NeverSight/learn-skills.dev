---
name: skill-manager
description: Install, update, remove, create, improve or audit skills for Claude Code and Codex, on this computer, in one folder or on their server. Use when the user says "installe ce skill", gives a skill link, "supprime ce skill", "mets à jour mes skills", "fais-en un skill", or a skill misbehaves.
argument-hint: "[install|remove|update|list|create|improve|audit] [skill name or link]"
---

A skill is a folder with a `SKILL.md` that teaches the agent one workflow it then applies on its own. Talk to the user in their language, short, without jargon (say "for every folder" or "only in your brain", never "symlink", "frontmatter" or "repo").

Where a skill lives, always one source and links elsewhere, never two copies:
- For every folder (the default): `~/.agents/skills/<name>/` (Codex reads it there), linked in `~/.claude/skills/` for Claude Code.
- Only for the brain or one project: `<folder>/.agents/skills/<name>/`, read by Claude Code through `<folder>/.claude/skills`, one link to that folder. Brain workflows (`done`, `create-project`, `cleanup`, `projects`) live there; the brain path is in the `## Brain` section of `~/.agents/AGENTS.md` or `~/.claude/CLAUDE.md`.

[scripts/skills.sh](scripts/skills.sh) does every install, update and removal; never copy or delete skill folders by hand. When you got this skill from a link, download it first: `curl -fsSL https://raw.githubusercontent.com/Melvynx/ai-maxxing-skills/main/skills/skill-manager/scripts/skills.sh -o <scratch>/skills.sh`. Add `--to <folder>` to any command to work in the brain or a project instead of every folder. On Windows, run it from Git Bash.

To install: a source is skill names of the ai-maxxing kit (`create-landing lumail`), a GitHub repo (`owner/repo`), a GitHub link to a skill folder or its `SKILL.md`, or a local folder.
1. When the user asks what they can install, run `bash skills.sh available` (or `available <repo>`) and show each skill with what it lets them ask, in one short list.
2. Pick the place: every folder, unless the skill only makes sense in the brain or one project. Run `bash skills.sh install <source> [<skill>...]`. A repo with several skills and none named exits 2 with the list: ask which ones (or `all`). Exit 3 means a skill with that name is already there and was not installed this way: compare the two descriptions, replace it with `--force` when it is the same skill, otherwise ask, since it may be the user's own. Exit 4: check the name with `available` or the link.
3. Check that `~/.claude/skills/<name>/SKILL.md` (or `<folder>/.claude/skills/<name>/SKILL.md`) opens, and tell the user the skill is ready from their next session, with the sentence that starts it.

To see what is installed: `bash skills.sh list` (`own` is a skill they made or installed another way, `claude-only` one Codex cannot see; offer to move it into `~/.agents/skills`). To update: `bash skills.sh update [<skill>...]` fetches again every skill it installed. To remove: confirm the names in one line, then `bash skills.sh remove <skill>...`; it moves them to `~/.cache/removed-skills`, so a mistake is undone by moving the folder back.

On their server agent (`ssh -o BatchMode=yes hermes true < /dev/null` works), run each remote command as `ssh hermes '<command>' < /dev/null`. Skills of the kit go through the server's own manager: `hermes-setup catalog`, `hermes-setup add <skill>...`, `hermes-setup update`, `hermes-setup remove <skill>...` (the `install-skills` skill walks through it). Any other skill, their own or from another link: `ssh hermes 'bash -s -- install <source>' < skills.sh` (or `remove`, `list`). Hermes sees it from its next conversation.

To create one:
1. Ask in one message what it should do and 2 or 3 sentences the user would type to start it. When the conversation just did the workflow, propose the skill from what you did and ask them to confirm.
2. Name it in lowercase with dashes, verb first when it acts (`write-newsletter`, `check-invoices`). If a skill already does it, improve that one instead.
3. Write the frontmatter: `name`, and a `description` of 50 to 300 characters, what it does first, then `Use when` and the words the user says. The description is all the agent sees before loading the skill, so it decides when the skill runs. Add `argument-hint` when it takes an input, and `disable-model-invocation: true` when it must run only when the user types it (sending, publishing, paying).
4. Write the body in plain imperative prose (no headings, no bold, a numbered list only for ordered steps), in the order read, act, report, stop: what to read first, the steps, what to show the user at the end. Give the goal and the judgment to apply, not rigid rules; every line must change what the agent does. Put commands that always run the same way in `scripts/` and long details (API docs, templates, examples) in `references/`, and say in the body when to open each. Create the folder directly in its place (see above); for every folder, link it with `ln -sfn ~/.agents/skills/<name> ~/.claude/skills/<name>` unless `~/.claude/skills` already links to `~/.agents/skills`.
5. Test it on a real case now, or ask the user to type a trigger sentence in a new session. Fix what went wrong in the skill, not only in the result.

To improve one: read it, find the line that caused the wrong behavior (or the missing line), change the fewest lines that fix it, and run it again.

To audit: start from `bash skills.sh list` and the same with `--to <brain>`. For each line of a skill, ask whether removing it changes behavior, and delete no-ops, duplicates and stale rules. Point out skills that overlap or that the user never uses, and remove one only after they agree.

Finish with what changed (one line per skill, a check or a cross), where each one lives, the sentence that starts it, and for a skill they made, how to share it: put it in a public GitHub repo, then anyone installs it with this skill and the link, or with `npx skills add <owner>/<repo>`.
