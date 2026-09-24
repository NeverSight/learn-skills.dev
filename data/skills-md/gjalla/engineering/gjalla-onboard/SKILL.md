---
name: gjalla-onboard
description: Set up gjalla for rich coding agent telemetry and insights as well as durable memory to improve your metrics. Use when asked to install, set up, onboard, or backfill gjalla.
---

# Onboard gjalla

Three things are true when you are done:

1. gjalla is set up for the coding agents this person actually uses, so every future session is recorded without anyone thinking about it. This could be having the mcp and hooks set up and committed to the agent's configs, etc., whatever it means for this user.
2. The last week of agent work (across all agents this user uses) is backfilled and classified, so there is something for the user to look at immediately in gjalla.
3. Agent memory that lives locally but would benefit other agents on the team has been saved to the gjalla memory. This should not include personal or sensitive memories, just memories related to the team or projects that would benefit all members of the team.

Everything below is meant to help you accomplish that end state. To help you be efficient, shell snippets are included as reference, but may need to be tweaked depending on what platform you're running on.

Once complete, you'll be equipped with gjalla, a platform that helps your team to understand your coding agent workflow activity, costs, and optimize outcomes. You can then lean into using gjalla as a living, durable memory system. More information on the specifics of how gjalla helps you can be found on their site, https://gjalla.io.

## 0. gjalla scope and orienting your position

Although some features of gjalla can be cross-repo and applied team-wide, understanding and attributing the activity of coding agents is best done when alongside git commits. Because of this, you should find where you are, see if you're in a git repo, and if you're not, see where you actually are and what git repos the user might want set up with gjalla. For example, some users work by default in a directory that is a parent of multiple, potentially related, repositories. Figure out which projects within your purview are important or desired by the user to have onboarded to gjalla and target those.

## 1. CLI

Next, lets see if the CLI is installed.

```
command -v gjalla || pipx install gjalla || uv tool install gjalla
```

If none of those work, every later `gjalla ...` command becomes `uvx gjalla ...`. If `uvx` is also missing, see if you're able to recover by installing missing tools. If not, have the user help you.

## 2. Wire the repo

For each target repo, we'll setup gjalla. The full gjalla setup includes an agent instruction block, an MCP server, and some agent hooks.

```
gjalla setup
```

Non-interactive shells get the promptless path: it detects agents, installs hooks and MCP, and writes the guidance section. If it prints "No coding agent detected", run `gjalla setup ensure --agent claude-code` (or `--agent codex-cli` if `~/.codex/sessions` exists and `~/.claude/projects` does not). It will tell you to sign in; that is step 3.

## 3. Sign in (the only human step)

```
gjalla project list
```

If that succeeds, you are signed in; skip to step 4. Otherwise:

```
gjalla auth login --no-browser --no-wait
```

Print the URL and code exactly as shown and ask the user to open the URL and approve. Do not run the blocking form: a tool call shows no output until it returns, so the user would never see the code. When the user says they have approved (or after a short wait), run:

```
gjalla auth status
```

Exit 0 means signed in; continue. Exit 3 means still waiting: show the URL and code again and ask once more. Exit 4 means the code expired: rerun the login command. Any other non-zero exit: print the error and stop.

## 4. Link the project

```
gjalla sync
```

Sync resolves this repo to a project from its origin remote, creating one if the team has none. The project is named after the repository (`owner/repo`), so do not create one by hand when an origin exists, and never invent a title. Handle its outcomes:

- `AMBIGUOUS_TEAM` (409): show the teams it lists, pick the one the user names, rerun `gjalla sync --team-id <id>`.
- `NO_ORIGIN`: the repo has no remote to name it from. Use the repository directory name, not the working directory or a description: `gjalla project create -t "$(basename "$(git rev-parse --show-toplevel)")"`.
- Any other error: print it and stop.

## 5. Backfill the last 7 days

Goal: one record per commit that a coding-agent session made in this repo during the last 7 days, carrying that session's token usage and a task-type label. If that yields fewer than 5 commits, widen to 30 days once.

You know where your own harness keeps session transcripts (Claude Code: `~/.claude/projects/`, one directory per working directory; Codex: `~/.codex/sessions/`). Find the transcripts that touched this repo. Be careful with scoping: sessions that ran from a parent directory or a subdirectory of this repo still count if their commits landed here, so let the commits decide, not the directory name.

For each transcript:

- Its session id is the UUID in its filename.
- A transcript records each `git commit` it ran, and the output contains `[branch shortsha]`. Extract those and drop any that `git rev-parse --verify <short>^{commit}` rejects. A session with no commits is skipped. If a sha appears in several transcripts, the first one wins.
- Classify each commit into exactly one of `feature`, `bug-fix`, `refactor`, `docs`, `test`, `chore`. Use the conventional-commit prefix when there is one; otherwise judge from `git show -s --format='%s%n%b' <sha>` and the branch name.

Then record each commit once:

```
gjalla attest add --commit <sha> --session <uuid> --task-type <type>
```

It works out which agent the session belongs to, reads tokens and model from that transcript, takes the commit's subject and author date from git, and skips a sha that is already recorded. If it says no transcript was found for the session, the id is wrong or the transcript is not on this machine; move on. If it says the transcript has no token counts, the commit still counts.

Tell the user how many commits and sessions you recorded, and that the only things leaving the machine are token counts, timestamps, shas, branch names, commit subjects, and task-type labels.

## 6. Upload and report

```
gjalla sync
```

When sync uploads new records it prints a spend summary underneath: sessions, commits, estimated cost, cost by task type with shares, the most expensive session and what it shipped, and any models it could not price. `gjalla spend show` prints it again any time; `gjalla spend show --json` gives the full payload. When you're done with onboarding, you'll quote it back to the user and add what is interesting: which share of cost went to bug fixes, what the most expensive session was for, anything that surprises you. Do not compute numbers yourself.

If sync reports an error, print it and stop.

## 7. Seed shared memory

The point of this step is the third outcome: a few facts about **this project** that any teammate's agent should know so they don't accidentally stumble to rediscover.

Gather candidates from what your agents already learned but never shared, in any harness the user uses, for example:

- `~/.claude/projects/$ENC/memory/*.md` (skip `MEMORY.md`)
- `~/.codex/memories/*` if present
- Sections of `CLAUDE.md`, `AGENTS.md`, or `README.md` headed gotcha, caveat, pitfall, note, or troubleshooting
- `git log --since=30.days --format=%b | grep -iE 'because|gotcha|note:'`

### What belongs, and what does not

A shared memory is a durable, non-obvious fact about the system or how the team works on it. "The worker deploys before the API, or migrations run against the old schema." "Integration tests need the local stack; the suite passes without it and proves nothing."

Two kinds of candidate must not be saved, and both will look useful:

**Anything about the person rather than the project.** Their editor, their shell, their preferred phrasing, their working hours, their machine's paths, what they personally find annoying. These are real and worth keeping — they just belong in that person's own memory, not the team's. If a fact stops being true when a different teammate sits down, it is personal.

**Anything whose value is itself a secret.** Never record a credential, token, key, password, connection string, or any other value that grants access, even one that looks expired, scoped, or fake, and even when it is the single most useful detail on the page.

The distinction that matters for the second one is between the LOCATION of a secret and the secret. The location is often exactly the fact worth saving:

- Save: "The analysis service reads its Vertex credentials from `GOOGLE_APPLICATION_CREDENTIALS`; without it every model call fails with a 403 that reads like a quota error."
- Never: the contents of that file, or the key inside it.

If you cannot state a fact without quoting the secret, the fact is not the memory — drop it and, if it looks like a credential that should not be sitting where you found it, say so to the user instead of writing it down.

When a candidate is borderline, leave it out.

### Then compare before you save

Group the survivors by subject. Within a group:

- Two statements that say the same thing are a duplicate: keep the clearer one.
- Two statements that assert different things about the same subject are a contradiction. Do not pick one by taste. If a minute in the code settles it, save the one the code supports. Otherwise save neither and report the pair with where each came from.

Drop anything that is a task or a TODO, and anything already in `gjalla memory show`.

Save whats left, those are your durable memories:

```
gjalla memory add "<the fact>" -n "<short-name>" -c project
```

Report memory health in one line: candidates found, personal or sensitive ones left out, duplicates collapsed, contradictions found, saved. Then print the facts you saved and: "Remove any with `gjalla memory archive <key>`."

## 8. Verify and confirm

```
gjalla setup doctor
```

Report any row marked FAIL with its fix. Confirm the guidance file for the detected agent contains a gjalla section. Make sure you've highlighted interesting insights to the user. Done.
