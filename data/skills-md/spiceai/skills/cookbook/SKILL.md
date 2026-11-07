---
name: cookbook
description: Set up and run recipes from the Spice.ai cookbook (github.com/spiceai/cookbook) — pick the recipe that fits what the user wants to see, get the cookbook, check the runtime version, Docker, API keys, tools, and ports, start the runtime, walk through the README, then hand off or clean up. Use this skill whenever the user wants to try, run, set up, demo, or explore a Spice cookbook recipe, sample, or example ("run the kafka recipe", "try the text-to-sql cookbook", "show me a working Spice demo of vector search", "get the duckdb example running"), asks which recipes exist or which fits their use case, pastes a github.com/spiceai/cookbook link, wants to try a recipe from a cookbook pull request or branch, or is stuck following a cookbook README.
---

# Run Spice Cookbook Recipes

The [Spice.ai cookbook](https://github.com/spiceai/cookbook) holds 120+ self-contained recipes. Each one
is a directory with a `README.md` (steps and expected output) and usually a `spicepod.yaml`. This skill
takes a user from "I want to see X working" to a running recipe they can explore: pick it, get the code,
check prerequisites, set up keys without exposing them, start the runtime, walk the README, and hand off.

A helper script, `scripts/cookbook.sh` in this skill's directory, does the mechanical parts. Call it by
its full path from the user's working directory, since it looks for a cookbook checkout there. Status
goes to stderr; results go to stdout as JSON.

| Command | What it does |
| --- | --- |
| `cookbook.sh fetch [--dir DIR] [--pr N \| --ref BRANCH] [--no-update]` | Reuse or shallow-clone the cookbook and fast-forward it, or check out a pull request or branch. Never discards changes to tracked files |
| `cookbook.sh list [TERM...]` | Recipes with category, description, minimum version, and `needs` tags |
| `cookbook.sh inspect RECIPE` | What a recipe needs and what is in place: runtime vs. minimum version, Docker, each secret's status, tools, busy ports, plus `blockers` and `warnings`. Never prints secret values |

`fetch`, `list`, and `inspect` find the checkout in this order: `--dir`, `$SPICE_COOKBOOK_DIR`, the
current directory or a parent, `./cookbook`, `~/spice-cookbook`, `~/cookbook`. With none, `fetch` clones
to `~/spice-cookbook`, outside the user's project, so the cookbook doesn't become a nested repository in
their code. `inspect` accepts a path (`postgres/connector`), a name (`kafka`), or a GitHub URL, and lists
candidates when a name is ambiguous.

## Version Compatibility

Written for **Spice v2.4.x** (checked against v2.4.0-rc.2). Check the user's runtime version before running a recipe:

- **Find it**: `spice version` (CLI and runtime), `spiced --version`, or the image tag. Not the runtime version: `version: v1` in a recipe's `spicepod.yaml` (manifest schema; v2 still loads `v1`) or SQL `version()`. `inspect` reports it under `spice`.
- **The cookbook has no release tags**: `trunk` tracks the latest Spice release. Each README states a minimum (`Works with v1.8+`), which `inspect` compares with the installed runtime. A README that says `Deprecated in v2.0+` needs a v1.x runtime.
- **Older runtime**: if it meets the recipe's minimum, run the recipe and expect different log lines and output formatting. Otherwise choose a compatible recipe or explain the user-managed upgrade prerequisite in `setup`. For v2.1.x, read the `.env` note in step 4.
- **Newer runtime**: check the [release notes](https://spiceai.org/releases) for changes after v2.4.0-rc.2, and treat a README step the runtime rejects as a recipe bug (step 6).

| Old | Change | Use instead |
| --- | --- | --- |
| `spice run -- --http <addr>` | Fails on every v2 CLI (the CLI already passes `--http`) | `spice run --http-endpoint <addr> --flight-endpoint <addr>` |
| Real key in `.env.local` or the shell, placeholder in `.env` | Broken in v2.1.0–v2.1.1 (`.env` wins); fixed in v2.2.0 | On v2.1.x put the value in `.env`, or upgrade |
| `evals:` section, `spice eval` (`evals`, `llm-judge` recipes) | Removed in v2.0.0 | A v1.x runtime, or skip the recipe |
| Perplexity `websearch` tool (`websearch` recipe) | Removed in v2.0.0 | A v1.x runtime, or skip the recipe |
| `fused_score` column from `rrf()` | Renamed in v2.0.0 | `_fused_score` |
| `acceleration.ready_state` (`dual-dataset-registration` recipe) | Deprecated in v2.3.0 (still applies) | `ready_state` on the dataset |

## 1. Get the cookbook

Run `cookbook.sh fetch`. A new clone is about 40 MB; an existing checkout is fast-forwarded. Tell the
user where the checkout is and which commit it's on. To try unmerged changes, pass `--pr <number>` or
`--ref <branch>`. To see which recipes a pull request touches, run
`gh pr view <number> -R spiceai/cookbook --json files` (or open the PR page). `fetch --ref trunk`
returns to trunk.

If `dirty` lists files, the user has edited tracked files (often an API key typed into a recipe's `.env`),
and the checkout was not updated. Mention it; don't revert their changes.

## 2. Pick the recipe

- **A named recipe or a link**: run `cookbook.sh inspect <name>`. It resolves names, paths, and GitHub
  URLs. If it returns `candidates`, ask the user which one they mean.
- **A goal** ("vector search", "something with Postgres", "Spice with an LLM"): run
  `cookbook.sh list <terms>` and recommend one to three recipes. Every term must match, so start with one
  or two words. `list` with no terms prints all recipes (about 25 KB), so filter when you can.
- **Recommend what the user can actually run.** `needs` tags say what each recipe requires beyond Spice:

  | Tag | Meaning |
  | --- | --- |
  | (none) | Runs on a laptop with only Spice (local files, public S3 or HTTP data) |
  | `docker` | Starts dependencies with Docker Compose |
  | `keys` | Needs API keys or tokens (OpenAI, GitHub, Hugging Face, ...) |
  | `cloud-account` | Needs the user's own account (Databricks, Snowflake, AWS, Spice Cloud, ...) |
  | `own-server` | Needs a database or server the user already runs |
  | `toolchain` | Runs code in Python, Node, Go, Java, Rust, or .NET |
  | `kubernetes` | Needs a Kubernetes cluster |
  | `v1-only` | Needs a v1.x runtime |

  Say up front when a recipe needs an account or server the user may not have, since there's no way to
  fake those. When several recipes fit, give one line each (what it shows, what it needs) and let the user choose.

## 3. Check prerequisites

Run `cookbook.sh inspect <recipe>`, then read the recipe's README end to end and its spicepod(s). The
inspect output says what's missing; the README has the steps. Give the user a short checklist of what's
ready and what needs action, and clear the blockers before starting anything:

- **Spice missing or too old**: follow the `setup` installation prerequisite and link the
  [official installation documentation](https://spiceai.org/docs/installation). Installation and
  upgrades are user-managed; do not run installers or provision a runtime through another skill.
  Require `spice version` to report an installed, compatible runtime before `spice run`, which
  automatically downloads one when it is missing. On Windows the runtime needs existing WSL.
- **Docker not reachable**: ask the user to start Docker Desktop, OrbStack, or colima.
- **Missing tools** (`websocat`, `duckdb`, a language toolchain): say what to install. Install only with
  the user's OK.
- **`cloud-account` or `own-server`**: the user supplies connection details; the README says which.
- **`readme_writes_spicepod: true`**: the README builds the spicepod step by step (often in a new
  directory made with `spice init`), so follow it rather than looking for a file.
- **More than one `run_dirs` entry**: the recipe starts more than one runtime (e.g. a parent and a child
  spicepod). The README gives each its own ports.
- **Secrets**: step 4. **Busy ports**: step 5.

## 4. Set up secrets without exposing them

Missing or placeholder keys are the most common reason a recipe fails, and keys are the most sensitive
thing you'll handle here.

- **Never ask the user to paste a key into the chat, and never print one.** Don't `cat .env`, run `env`,
  or echo a key. `inspect` reports each secret's `status` (`set`, `empty`, `placeholder`, `missing`),
  the `variable` and `source` file that supplied it, and whether that file is tracked by git.
- **Where values go**: `.env.local` in the directory `spice run` starts from (gitignored in the cookbook),
  or an exported shell variable. Many recipes ship a tracked `.env` full of placeholders. A real key typed
  there shows up in `git diff`, where it's easy to commit by mistake.
- **Precedence**: from v2.2.0, an exported variable beats `.env.local`, which beats `.env`. On v2.1.x,
  `.env` beats both, so a placeholder in the recipe's `.env` hides the user's real key. On v2.1.x, put
  the value in `.env` itself or delete the placeholder line, or upgrade. `inspect` applies the installed
  runtime's precedence, and `ignored_values` names any real value that loses to a placeholder.
- **Names**: `${ secrets:NAME }` accepts `SPICE_NAME` or `NAME`. A recipe that reads `SPICE_OPENAI_API_KEY`
  therefore ignores an exported `OPENAI_API_KEY`. `inspect` flags that case as `similar_in_shell`.
- **Getting a value in without seeing it**: when the value is already in the shell or a CLI, write it
  to `.env.local` without echoing it:

  ```bash
  printf 'SPICE_OPENAI_API_KEY=%s\n' "$OPENAI_API_KEY" >> .env.local
  printf 'GITHUB_TOKEN=%s\n' "$(gh auth token)" >> .env.local
  ```

  If `.env.local` already defines the key, replace that line instead of appending: from v2.2.0 the first
  occurrence wins, so a duplicate is ignored. When the value isn't available, ask the user to add the line
  to `.env.local` in their editor or terminal and tell you when it's done. Either way, re-run `inspect`
  and confirm the status is `set`.
- **Demo credentials** for Docker services started by the recipe (`MYSQL_PASS=spice` in `.env.example`)
  aren't secrets. Copy `.env.example` to `.env` when the README says to. `inspect` marks these
  `demo_value_in_env_example`.
- **`spice login <connector>`** (Databricks, Snowflake, Dremio, S3 recipes) writes credentials to `.env`,
  or to `.env.local` when one exists. Create an empty `.env.local` first to keep them out of tracked files.

## 5. Start the recipe

Work from the recipe directory, or from the subdirectory the README names.

1. **Dependencies**: run `docker compose up -d`, or `make` after reading the Makefile target. Wait for the
   containers to be healthy (`docker compose ps`) instead of sleeping a fixed time. `inspect` lists compose
   ports that are already in use (8080 and 5432 are common collisions).
2. **Spice**: start it in the background with a log file, so you can keep working and the user can
   explore later. Use your harness's background-process feature if it has one:

   ```bash
   cd <recipe-dir>
   nohup spice run > "${TMPDIR:-/tmp}/spice-<recipe>.log" 2>&1 &
   echo $!   # the `spice run` PID; stopping it stops spiced too
   ```

   Use `spice run`, not `spiced`: `spice run` turns on spicepod hot-reload, which recipes that edit
   `spicepod.yaml` partway through rely on.
3. **Readiness**: poll `curl -s http://127.0.0.1:8090/v1/ready` until it returns `ready` (HTTP 200).
   Check the log for `ERROR` and `WARN` while you wait, and read it if the process exits. Local files
   load in seconds, public S3 datasets in up to a minute or two, and model downloads or GitHub API
   datasets in several minutes.
4. **Ports**: if 8090 (HTTP) or 50051 (Flight) is taken, don't stop a process you didn't start. If it's
   an old recipe runtime from this session, stop that one. Otherwise pick free ports:

   ```bash
   nohup spice run --http-endpoint 127.0.0.1:18090 --flight-endpoint 127.0.0.1:15051 \
     > "${TMPDIR:-/tmp}/spice-<recipe>.log" 2>&1 &
   ```

   Then point every client at those ports: `spice sql --endpoint grpc://127.0.0.1:15051`, `curl` against
   18090, and any README command or SDK sample that hardcodes 8090 or 50051.

## 6. Walk through the README

Run each step and show the user what matters: the command, the key output, and a sentence or two on what
it demonstrates. Rewrite steps meant for a person at a terminal:

- **"In a new terminal, run `spice sql`"**: pipe the query in, `echo "SELECT ...;" | spice sql` (add
  `--endpoint` if you moved ports), or use the HTTP API, which returns JSON:
  `curl -s -X POST http://127.0.0.1:8090/v1/sql -H 'Content-Type: text/plain' -d 'SELECT ...'`.
  Keep the raw SQL body. A JSON body needs exactly `Content-Type: application/json` and
  `"parameters": []`; `{"sql": "..."}` alone returns `400 Invalid JSON: missing field 'parameters'`.
- **Other REPLs** (`spice chat`): use the matching HTTP endpoint, e.g. `/v1/chat/completions`.
- **Long-running producers** (streaming data into a file, a load generator): run them in the background
  for a bounded time, then continue.
- **Edits to `spicepod.yaml`**: make the edit; `spice run` reloads it.
- **Expected output**: match exactly for static local data (columns, row counts), approximately for live
  sources (S3, APIs, streams), and only in substance for LLM output. Log lines and SQL headers vary by
  version (v2 prints a type row under the column names), so treat formatting differences as normal.
- **Destructive commands**: read cleanup steps before running them and keep them scoped to what the recipe
  created. For example, the `file` recipe's cleanup runs `rm *.md`, which would also delete its README.
  Remove only the files the recipe downloaded.
- **A step fails**: read the log first. Fix environment problems (key, port, tool, Docker) and say what
  you changed. If the recipe itself is broken (config the runtime rejects, a command that no longer
  exists), explain the problem and the workaround, apply the workaround only with the user's OK, and
  suggest reporting it at <https://github.com/spiceai/cookbook/issues>. Don't quietly rewrite recipe
  files. The checkout is a git repository, so `git -C <cookbook> status --short` lists what changed and
  `git -C <cookbook> checkout -- <file>` reverts it. Don't run a bare `git diff` there: a recipe's
  tracked `.env` may now hold the user's real key, and the diff would print it into this conversation.
  Diff a specific file you know holds no secrets (`git -C <cookbook> diff -- <file>`).

## 7. Hand off

Unless the user only asked whether the recipe works, leave it running so they can explore, and finish with:

- The recipe directory, what's running (PIDs, ports, containers), and the log path.
- How to query it themselves, e.g. `cd <recipe-dir> && spice sql` (add `--endpoint` if you moved ports),
  plus two or three follow-up queries or changes that build on the recipe.
- How to stop it: `kill <pid>`, and `docker compose down` from the recipe directory.
- Files you created (`.env.local`, downloaded data) and anything still needing attention, such as a
  placeholder key.

## 8. Clean up

When the user asks, or when they only wanted a check:

- Stop the runtime you started with `kill <pid>`. If you lost the PID, find the listener on the recipe's
  port with `lsof -nP -iTCP:8090 -sTCP:LISTEN`. Don't run `pkill spiced`, which also stops runtimes the
  user runs for other projects.
- Run `docker compose down`. Add `-v` only if the user wants the volumes gone. The README's `make clean`
  may also delete images and the recipe's `.spice/` directory.
- Offer to remove files you created, and ask before deleting a `.env.local` that holds the user's keys.
  Restore tracked files the recipe edited (`git -C <cookbook> status --short`, then
  `checkout -- <file>`; don't diff `.env` files, which may hold the user's key).
- Acceleration files in `<recipe>/.spice/` can break the next run with schema errors. Deleting that
  directory is safe; the runtime rebuilds it.

## Troubleshooting

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| `Address already in use` at startup | Another runtime or app on 8090 or 50051 | Stop your earlier recipe runtime, or use `--http-endpoint` and `--flight-endpoint` |
| `argument '--http <BIND_ADDRESS>' cannot be used multiple times` | `spice run -- --http ...` | `spice run --http-endpoint ...` |
| 401 or `Incorrect API key` from a model provider | A placeholder or empty key is being used | Re-run `inspect`; fix the variable name, the file, or the v2.1.x precedence |
| `spice sql` can't connect | Runtime still starting, crashed, or on other ports | Check `/v1/ready` and the log; pass `--endpoint` |
| `400 Invalid JSON: missing field 'parameters'` from `/v1/sql` | JSON body without `parameters` | Send raw SQL, or add `"parameters": []` |
| Unknown field or invalid parameter at startup | Runtime older than the recipe | `spice upgrade`, or a recipe within the runtime's version |
| Schema mismatch after re-running a recipe | Stale acceleration files | Delete `<recipe>/.spice/` and restart |
| `Cannot connect to the Docker daemon` | Docker isn't running | Start Docker Desktop, OrbStack, or colima |
| Container restarts or is very slow on Apple Silicon | amd64-only image under emulation | Enable Rosetta emulation in Docker settings, or expect slowness |
| GitHub dataset slow, with rate-limit warnings | GitHub API limits | Use a `GITHUB_TOKEN` and wait; the runtime retries |
| Output formatted differently from the README | Different runtime version | Not a failure; compare the data |

## Related skills

setup (installation prerequisites and CLI), spicepod (manifests), connectors and datasets
(sources), secrets (secret stores), models and chat (LLMs), search (search recipes).
