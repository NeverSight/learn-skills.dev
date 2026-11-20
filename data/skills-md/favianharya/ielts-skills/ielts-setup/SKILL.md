---
name: ielts-setup
description: "Install, set up, check, repair, update or uninstall the IELTS coach (the ielts-preparation skill) on this machine: installs the skills, links them for Claude Code and omp, downloads the official IELTS band-descriptor PDFs, picks Claude models that work here and adds an `ielts` shell alias, then runs the learner intake to create the profile. Use when the user wants to install or set up IELTS preparation, moves to a new computer, asks to check or fix the setup, or when ielts-preparation reports its CLI or profile is missing."
---

# IELTS setup

Gets the IELTS coach working from nothing, and re-checks it later. All machine changes go through one script, `scripts/setup.py` in this skill (Python 3 standard library only). Every step is idempotent, so running it twice is safe.

## 1. Install the skills (only if missing)

Check: `ls ~/.agents/skills/ielts-preparation/scripts/ielts.py`. If it is missing:

```
npx skills add favianharya/ielts-skills -g -y
```

This installs `ielts-preparation` and `ielts-setup` into `~/.agents/skills/` (read by omp and other agents) and links them for detected agents such as Claude Code. "Failed to install" lines for agents without global-skill support (e.g. PromptScript) are harmless. Without Node, clone instead and let setup do the linking:

```
git clone https://github.com/favianharya/ielts-skills ~/.agents/ielts-skills
mkdir -p ~/.agents/skills && ln -s ~/.agents/ielts-skills/skills/* ~/.agents/skills/
```

## 2. Dry run

```
python3 <this skill>/scripts/setup.py --check
```

Show the user the output. Lines are tagged `ok`, `todo` (setup will fix), `skip` (not applicable here), `warn`, `FAIL` (needs the user).

## 3. Apply

Before running it, tell the user what will change and get a yes:

- links in `~/.claude/skills/` if Claude Code is installed;
- two official PDFs downloaded to `~/.ielts/official/`;
- if omp is installed: a few one-word test calls to find which `anthropic/` models answer through the user's own Anthropic login (best first: Opus 5.5 / 5 / 4.8 for scoring, Sonnet 5.5 / 5 / 4.6 for coaching, Haiku 5.5 / 4.5 for drills). Other providers (gateways, proxies, OpenAI) are never used, and `ANTHROPIC_BASE_URL` / `ANTHROPIC_AUTH_TOKEN` / `ANTHROPIC_API_KEY` are removed for the test calls and in the alias, so a proxy set in the shell cannot reroute requests;
- a marked block in the shell rc file (`~/.zshrc` for zsh), backed up first:

```
# >>> ielts-skills (managed by ielts-setup; re-run setup to change) >>>
alias ielts='env -u ANTHROPIC_BASE_URL -u ANTHROPIC_AUTH_TOKEN -u ANTHROPIC_API_KEY omp --model <sonnet>:medium --smol <haiku>:low --slow <opus>:high'
# <<< ielts-skills <<<
```

Then run `python3 <this skill>/scripts/setup.py`. Options:

| Flag | Use |
|---|---|
| `--no-alias` | Do not touch the rc file (the user only uses Claude Code, or does not want an alias) |
| `--alias-name NAME` | `ielts` is already taken |
| `--rc FILE` | A different rc file |
| `--slow/--default/--smol SELECTOR:EFFORT` | Force a model, e.g. `--slow anthropic/claude-opus-4-8:high` |

Why these roles: scoring needs the strongest model at high effort, and must stay on one model so calibration offsets mean something; coaching is fine on a mid model at medium; drills and vocabulary reviews need fast replies at low effort. Claude Code has no roles: tell the user to use `/model` (Opus when pasting work for a score, Sonnet otherwise, Haiku for drills).

On `FAIL`: "not found" means step 1 did not run; "no anthropic/ model" means the user must log in with their Claude account in omp (`omp login`, or `/login` inside omp) and re-run; "already defined" means pick `--alias-name`.

## 4. Learner intake (when setup reports no profile)

Ask in one short message, accepting "don't know":

1. Target overall band, and any per-paper minimum (e.g. "7, no band below 6.5").
2. Test date (or a rough month).
3. Academic or General Training.
4. Latest band per paper and where it came from (official test, mock, own guess), or none.

Then, from the ielts-preparation skill root:

```
python3 scripts/ielts.py init --target 7 --test-date 2027-03-01 --module academic --band L=6.5 R=6 W=5.5 S=6 --source mock
python3 scripts/ielts.py set --min W=6.5 S=6.5
```

Omit `--band` when there are no scores; the first practice sessions will estimate them. Never invent bands.

## 5. Finish

Run `python3 scripts/ielts.py status` and tell the user:

- open a new terminal (or `source ~/.zshrc`), then start with `ielts "help me prepare for IELTS"`;
- inside omp, cycle models with the model-cycle key: `slow` before pasting an essay or speaking transcript for a score, `smol` for drills;
- their data lives in `~/.ielts/` and survives skill updates.

## Update and uninstall

- Update: `npx skills add favianharya/ielts-skills -g -y` (re-adding overwrites with the latest version; `npx skills update -g` also walks every other installed skill and can stall), then `setup.py --check`.
- Uninstall: `npx skills remove ielts-preparation ielts-setup -g -y`, delete the marked block from the rc file (a backup sits next to it as `.zshrc.ielts-backup-*`), and delete `~/.ielts/` only if the user wants their progress gone.
