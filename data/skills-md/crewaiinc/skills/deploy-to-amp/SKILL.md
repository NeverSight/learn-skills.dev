---
name: deploy-to-amp
description: "Getting a CrewAI crew or flow onto CrewAI AMP: the project shape the build expects (uv.lock, [tool.crewai] type, src/<pkg>/ entry points, a real Flow subclass, absolute imports, a self-contained root), `crewai deploy validate`, the three deploy paths (CLI create/push, GitHub, ZIP upload) and what each one actually uploads, env vars per deployment and what the CLI re-sends from .env, provider keys and extras, and machine-wide org selection. Use when running `crewai deploy create` / `crewai deploy push` / `crewai deploy validate`, when a deploy says Online but runs old code, old env values or lost a key, or when pasting errors like `missing_lockfile`, `Crew class annotated with @CrewBase not found`, `No Flow subclass found`, `Expected to find at least one of these files: uv.lock or poetry.lock`, `OPENAI_API_KEY is required`, `Anthropic native provider not available`, `deployment_not_found`, `git_clone_failure`, `Automation error, fix the code and deploy again`, or `pyproject.toml not found`."
---

# Deploy to CrewAI AMP

Ship a crew or flow to AMP without burning deploys on project-shape errors, stale code, stale env values, or the wrong org.

Verified against crewai 1.15.22 and 1.15.23 on 2026-10-01.
Live-tested on CrewAI AMP and real LLMs on 2026-10-01.
Run `crewai version` first; if the major/minor differs, re-verify the version-sensitive rows below with the `ask-docs` skill before trusting them.

---

## 1. Preflight - run these three every time

```bash
crewai org current        # which org will receive this deploy (machine-wide, see section 5)
uv lock && git status     # lockfile fresh, and you know what is uncommitted
crewai deploy validate    # local checks, no platform contact, exit 1 on blocking errors
```

`crewai deploy create` and `crewai deploy push` run the same validation automatically (skip with `--skip-validate` only when you know why). Every `crewai deploy` subcommand, including `status --uuid`, must run from the project root - elsewhere it stops with `Error: pyproject.toml not found.`

Exit codes are not a reliable signal in scripts or CI. `crewai deploy validate` exits 1 on errors, but `create` and `push` exit 0 when their built-in validation fails (`Pre-deploy validation failed. Fix the issues above or re-run with --skip-validate.`), and `status` / `logs` exit 0 on `deployment_not_found`. Gate CI on `crewai deploy validate` and check the command output, not only `$?`.

Validate imports your project, which creates crewai's local storage directory (on macOS `~/Library/Application Support/<pkg>/`). Set `CREWAI_STORAGE_DIR` to a scratch path when running it in CI or on a shared machine.

---

## 2. Project shape the build expects

| Requirement | Crew (classic, `crewai create crew <name> --classic`) | Flow (`crewai create flow <name>`) |
|---|---|---|
| Deployment name | `[project].name`, verbatim (the scaffold writes underscores: `research_crew`) | same |
| `[tool.crewai] type` | `"crew"` | `"flow"` |
| Lockfile | `uv.lock` (or `poetry.lock`) at the root, committed | same |
| Package dir | `src/<pkg>/`, where `<pkg>` is `[project].name` normalized (`research-crew` -> `research_crew`) | same |
| Entry code | `src/<pkg>/crew.py` with an `@CrewBase` class, plus `config/agents.yaml` and `config/tasks.yaml` | `src/<pkg>/main.py` with a `Flow` subclass that can be built with no arguments, plus `kickoff()` |
| Scripts (scaffold) | `run_crew = "<pkg>.main:run"` | `kickoff = "<pkg>.main:kickoff"` |
| Imports | absolute: `from research_crew.tools.x import Y` | absolute: `from acme_flow.crews.content_crew.content_crew import ContentCrew` |

JSON-first crews (plain `crewai create crew <name>`, no `--classic`) keep `crew.jsonc` and `agents/` at the project root instead of `src/`; `crewai deploy validate` checks that layout too.

Minimal flow `main.py` that passes validation:

```python
from crewai.flow import Flow, listen, start
from pydantic import BaseModel


class ReportState(BaseModel):
    topic: str = "AI agents"
    summary: str = ""


class ReportFlow(Flow[ReportState]):
    @start()
    def gather(self):
        return f"notes on {self.state.topic}"

    @listen(gather)
    def summarize(self, notes):
        self.state.summary = notes.upper()
        return self.state.summary


def kickoff():
    ReportFlow().kickoff()


if __name__ == "__main__":
    kickoff()
```

### Shape rules, each with the failure it prevents

| Bad | What happens | Good |
|---|---|---|
| `from .stub_tools import X` in `crew.py` / `main.py` | `crewai run` works, but `crewai deploy validate` fails with `Crew class annotated with @CrewBase not found` (the loader runs the file outside its package, and the real `attempted relative import` error is hidden). Pushed with `--skip-validate`, the AMP build fails the same way: `ImportError: attempted relative import with no known parent package` | `from research_crew.stub_tools import X` |
| Only a `def kickoff():` in `main.py`, no Flow class | `No Flow subclass found in the module` | Define `class MyFlow(Flow[...])` and call it from `kickoff()` |
| Flow `__init__(self, tenant: str)` | `No Flow subclass found` - the class must build with no arguments | Pass per-run values through `kickoff(inputs={...})` into state |
| `type = "flow"` on a crew project | `No Flow subclass found` | `type = "crew"` |
| `type = "crew"` on a flow project | `Cannot find src/<pkg>/crew.py`, `Cannot find src/<pkg>/config` | `type = "flow"` |
| Renamed `src/research_crew/` to `src/researchcrew/` | `Cannot find src/research_crew/` and `Hatchling cannot determine which files to ship` | Keep the dir equal to the normalized `[project].name` |
| `uv.lock` missing | `missing_lockfile` error | `uv lock`, then `git add uv.lock` |
| Edited `pyproject.toml` after locking | `stale_lockfile` warning (does not block) - deployed deps may differ from local. The check compares file times, and the CLI itself writes `[tool.crewai] project_id` into `pyproject.toml` when it is missing, which also triggers it | Re-run `uv lock` after every `pyproject.toml` edit. `uv lock` leaves an already-current lockfile untouched, so the warning can persist; if `uv lock --check` passes, `touch uv.lock` clears it and commit both |
| Importing code from a sibling dir (`../shared_lib`) via `sys.path` | Validate passes locally, but only the project root is uploaded: the AMP build fails with `ModuleNotFoundError: No module named 'helpers'` and status `Automation error, fix the code and deploy again.` | Move shared code inside `src/<pkg>/` or publish it as a package dependency |
| `anthropic/...` model with plain `crewai[tools]` | Locally: `Anthropic native provider not available, to install: uv add "crewai[anthropic]"`; validate reports it only as `@CrewBase not found` / `No Flow subclass found`, so `create` and `push` refuse the project | `uv add "crewai[anthropic]"` so the extra lands in `pyproject.toml` and `uv.lock`. |

Keep data files inside `src/<pkg>/` and load them as package data, not with paths built from the repo root. Files under `src/<pkg>/` go into the wheel the scaffold builds; files at the project root do not.

```python
from importlib.resources import files

rules = files("research_crew").joinpath("data/rules.json").read_text()
```

When validate says `@CrewBase not found` or `No Flow subclass found` and the class is clearly there, the loader swallowed the real error. Reproduce it with a traceback:

```bash
# 1. Run the file outside its package, as the loader does (catches relative imports and import-time errors)
uv run python -c "import runpy; runpy.run_path('src/research_crew/crew.py', run_name='deploy_check')"   # flows: src/<pkg>/main.py
# 2. Build the object with no arguments (catches missing provider extras and Flow `__init__` arguments)
uv run python -c "from research_crew.crew import ResearchCrew; ResearchCrew().crew()"
uv run python -c "from acme_flow.main import ContentFlow; ContentFlow()"
```

See [validate-checks.md](references/validate-checks.md) for every check and code.

---

## 3. The three deploy paths and what each one uploads

| Path | Code AMP builds | Env vars sent |
|---|---|---|
| `crewai deploy create`, project has an `origin` remote | AMP clones the repo; nothing is uploaded from your disk. AMP needs read access to the repo through a connection in the AMP org (Settings > Git Repositories: GitHub OAuth or Any Git Repository) - otherwise create still prints `Deployment created successfully!` and the build then fails with `git_clone_failure` (`could not read Username for 'https://github.com'`) | Every key in local `.env`, after a "Press Enter to continue with N env vars: ..." prompt (`-y` skips it) |
| `crewai deploy create`, no `origin` remote | A ZIP of your working tree (prints `No origin remote found. Deploying from a ZIP upload instead.`) | Every key in local `.env`, after the same prompt |
| `crewai deploy push`, local `origin` present | Nothing is uploaded; AMP rebuilds from the deployment's own source | None |
| `crewai deploy push`, no local `origin` | A fresh ZIP of your working tree, including uncommitted edits | Every key in local `.env`, with no prompt - and it **replaces** the deployment's variables (see section 4) |
| Dashboard, Deploy from Code (GitHub OAuth or Git Repository tab) | The repository and branch you pick from a connection (optional auto-deploy on new commits) | What you enter in the dashboard |
| Dashboard, ZIP upload | The ZIP you choose | What you enter in the dashboard |

`push` decides between a ZIP upload and a rebuild from your **local** `origin`, while AMP builds from the source the deployment was **created** with. If the two disagree, the push can succeed without shipping your changes:

| Deployment created as | Local state at `push` | Result |
|---|---|---|
| ZIP | `origin` added later | No ZIP uploaded; AMP rebuilt the **last uploaded** ZIP. Working-tree code and `.env` changes were not deployed, status went back to `Crew is Online` |
| Git | `origin` removed | CLI uploaded a ZIP and `.env`; AMP ignored the ZIP and cloned the repository again |

Rules that follow from this:

- Never add or remove `origin` on a project after `create`. For a ZIP deployment, a correct push prints `Preparing project ZIP...` and `Uploading project ZIP...`; if those lines are missing, nothing new shipped.
- Git-based: AMP builds the commit on the remote, never your disk. Uncommitted edits and local commits that are not pushed are both skipped (the build ran the previous pushed version, status `Crew is Online`). `git commit`, `git push`, then `crewai deploy push`.
- ZIP-based: the ZIP holds files Git tracks plus untracked files that are not ignored, and always drops `.env`, `.env.*` (except `.env.example` / `.env.sample`), `.git`, `.venv`, caches, `build/` and `dist/`. Add run outputs (`report.md`, `output/`) and scratch files to `.gitignore`, or they ship. Do not depend on root-level dotfiles at runtime: `.gitignore` and `.env.example` were in the ZIP but absent from the deployed project root.
- If the directory has no commits yet (the scaffold runs `git init` but does not commit), `create`/`push` commits everything not ignored as "Initial crew". If `uv.lock` is missing, validation's own `uv run` creates it before the upload (and `create`/`push` fall back to `crewai install`).
- Only the project root is packaged. Monorepo subfolders need a working directory set in the dashboard (the CLI create flow has no such option).
- `push` without `--uuid` finds the deployment by `[project].name` in the selected org. Deployment names are not unique in an org, so keep the name stable and prefer `--uuid` in scripts.
- `push` prints the deployment's full record, including its public URL and bearer **token**. Do not paste `push` output into tickets or keep it in CI logs. `crewai deploy status` prints only the name and status.
- `crewai deploy logs` fetches the deployment (build) log. When a deploy fails, read the real error there (`ModuleNotFoundError ...`, `git_clone_failure`): the status line only says `Automation error, fix the code and deploy again.`, `Provisioning Failed, try again.` or `Something went wrong, try again.` Read run output from the kickoff result or the dashboard's Executions and Traces tabs.
- `Crew is Online` means the build finished and AMP's import test of your project passed. Runtime problems (a missing provider key, a bad model name) only show at kickoff - for example status `FAILED` with `ValueError: ANTHROPIC_API_KEY is required`. After every deploy, kick off the cheapest real input and read the output (see `call-deployed-crew`).

Full matrix, exclusions, and a script to list what a ZIP deploy would contain: [what-gets-uploaded.md](references/what-gets-uploaded.md).

---

## 4. Environment variables

Env vars live on each deployment. Set provider keys (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, ...) and tool keys (`SERPER_API_KEY`, ...) as that deployment's environment variables in the AMP dashboard, and confirm them with a kickoff rather than assuming an org-level setting reaches your code.

What the CLI does with local `.env`:

| Situation | What gets sent |
|---|---|
| `.env` present on `create` | Every non-comment `KEY=VALUE` line, unfiltered - including unrelated secrets in the file |
| `.env` present on a ZIP `push` (no local `origin`) | The same, and the deployment's variables are **replaced** by exactly this set: a key missing from `.env` is deleted from the deployment |
| `.env` absent | No env fields at all (it prints `Error: .env not found.` and carries on); the deployment keeps its current variables |
| `push` with a local `origin` | Never sends env vars - change values in the dashboard. A Git-based deployment keeps the values from its `create` until you edit them there |

Values are sent verbatim: `MAX_CASES=3  # note` arrives as `3  # note` (python-dotenv locally strips the comment and gives `3`, so local runs hide this), and `QUOTED="abc"` arrives with the quotes. Write `.env` with bare values and no inline comments.

To push code without touching a ZIP deployment's variables, run `crewai deploy push` from a tree with no `.env` (move it aside) and manage values in the dashboard. Never push with a partial `.env`. Ship a `.env.example` with `<your-key>` placeholders so the required names are documented.

Provider facts that bite on deploy:

- An agent with no `llm=` uses the OpenAI default (`gpt-4.1-mini`), so it needs `OPENAI_API_KEY` even in an Anthropic-only project. Set `llm=` on every agent.
- The native providers read their key from `api_key=` or the provider variable; a missing key fails at kickoff, not at deploy: `ValueError: OPENAI_API_KEY is required`, `ValueError: ANTHROPIC_API_KEY is required`.
- Non-OpenAI providers are extras: `crewai[anthropic]`, `crewai[google-genai]`, `crewai[bedrock]`, `crewai[azure-ai-inference]`. Add them with `uv add` so they are in `pyproject.toml` and `uv.lock`; without the extra, validate (and therefore `create` / `push`) rejects the project.
- `crewai deploy validate` warns (`env_vars_not_in_dotenv`) when code calls `os.getenv("SERPER_API_KEY")` or similar for a known key that is missing from `.env` and your shell. It is a reminder to add the key to the deployment, not a blocker.

---

## 5. Org selection is machine-wide

The CLI keeps one selected org per OS user in `~/.config/crewai/settings.json`, and every platform call (`deploy create/push/status/logs/list/remove`) carries that org. Switching in one terminal switches it for every shell and project on the machine.

- Run `crewai org current` before every create, push, or remove. (Bare `crewai org` prints nothing on 1.15.22-1.15.23 - use the `current` subcommand.)
- `crewai org list` shows the orgs you belong to; `crewai org switch <org-id>` changes the selection.
- `crewai login` replaces the selection with the account's current org as reported by the platform, so re-check with `crewai org current` after every login.
- `deployment_not_found` (`Request to Enterprise API failed. Details: deployment_not_found`) means the selected org has no deployment with that UUID or name. The usual causes: the CLI is pointed at a different org than the one that owns the deployment, or `[project].name` changed since `create` (lookup is by name). Check `crewai org current` first, then the name or `--uuid`.
- Scripts and CI that drive the CLI should switch org explicitly at the start and verify it, never rely on whatever was last selected.

---

## 6. Common mistakes

| Symptom | Cause | Fix |
|---|---|---|
| Deploy is Online but runs old code | Git-based deployment and the change was not pushed; or a ZIP deployment pushed from a tree that now has an `origin` (no ZIP was uploaded) | `git push`, then `crewai deploy push`; for ZIP, remove the added `origin` and push again - check for `Uploading project ZIP...` |
| Deploy keeps old env values after editing `.env` | Push with a local `origin` never sends env vars | Edit the values in the dashboard |
| A stale value overwrites a rotated key, an unrelated secret appears on the deployment, or a key vanished | ZIP `create`/`push` uploaded exactly the keys in local `.env`, replacing the deployment's set | Deploy from a tree without `.env`, or with the complete set of this deployment's keys |
| Kickoff `FAILED` with `ValueError: ANTHROPIC_API_KEY is required` although status is Online | Key missing on the deployment (often removed by a ZIP push with a partial `.env`) | Set it in the dashboard, or push with a complete `.env` |
| `git_clone_failure`, `could not read Username for 'https://github.com'` | Git-based deployment and AMP has no access to the (private) repo | Check Settings > Git Repositories in the AMP org: if it only offers "Configure GitHub" / "Add Repository", nothing is connected. Connect GitHub (or add the repo) with access to this repository, then push again: a deployment created from the CLI picks up the connection on its next `push`, with no dashboard step and no need to recreate it. Until then every `push` re-runs the same clone and fails the same way. Or deploy from ZIP (a project with no `origin`) |
| `Automation error, fix the code and deploy again.` | The AMP build's import test failed | `crewai deploy logs` shows the real traceback |
| `MAX_CASES` parses as `3  # note` | Inline comment in `.env` sent verbatim | Bare values only |
| `Expected to find at least one of these files: uv.lock or poetry.lock` | No lockfile | `uv lock`, commit it |
| Validate passed on the second run although you never ran `uv lock` | Validate's import check ran `uv run`, which created `uv.lock` | Commit the new `uv.lock` (a Git-based build only sees committed files) |
| `Crew class annotated with @CrewBase not found` with the decorator present | Relative import, missing provider extra, or any import error in `crew.py` | Run the diagnostic commands in section 2 to see the real error |
| `No Flow subclass found in the module` | No Flow class, Flow needs constructor args, or `type = "flow"` on a crew | Add a no-arg Flow subclass; fix `type` |
| `ImportError` on AMP for code that works locally | Imports from outside the project root | Move it under `src/<pkg>/` or make it a dependency |
| `Anthropic native provider not available` | Extra missing from `pyproject.toml` | `uv add "crewai[anthropic]"` |
| `ValueError: OPENAI_API_KEY is required` at kickoff | Agent without `llm=` or OpenAI model and no key on the deployment | Set `llm=` explicitly; add the key as a deployment env var |
| `deployment_not_found` on push, status or logs | Wrong org selected, or `[project].name` no longer matches the deployment | `crewai org current`, then `crewai org switch <org-id>`; or pass `--uuid` |
| `Error: pyproject.toml not found.` from any `crewai deploy` subcommand | Run outside a project dir | `cd` to the project root |
| Deployment from a monorepo subfolder fails to find the project | Only the repo or ZIP root is used by default | Set the working directory in the dashboard |

---

## 7. Deploy checklist

- [ ] `crewai org current` shows the intended org
- [ ] `[tool.crewai] type` matches the project (crew or flow)
- [ ] `src/<pkg>/` matches `[project].name`; crew has `@CrewBase` + `config/*.yaml`, flow has a no-arg `Flow` subclass + `kickoff()`
- [ ] All project imports are absolute; nothing imported from outside the project root
- [ ] Provider extras (`crewai[anthropic]`, ...) added with `uv add`; `uv lock` run after the last `pyproject.toml` edit
- [ ] `uv.lock` committed
- [ ] `crewai deploy validate` exits 0
- [ ] Git-based: changes committed and pushed, and AMP can access the repo. ZIP-based: no `origin` added since create; run outputs and scratch files ignored
- [ ] `.env` holds exactly this deployment's complete key set with bare values - or is moved aside so nothing is sent
- [ ] Provider and tool keys set as the deployment's env vars in the dashboard
- [ ] Push output showed `Uploading project ZIP...` (ZIP) - and was not pasted anywhere (it contains the bearer token)
- [ ] After Online, one cheap kickoff returned the expected output

---

## References

- [What gets uploaded](references/what-gets-uploaded.md) - per-path matrix, ZIP include/exclude rules, env-var handling, and a script to list what a ZIP deploy would contain
- [Validate checks](references/validate-checks.md) - every `crewai deploy validate` check, its code and severity, and what it cannot catch
- Public docs: [Prepare for Deployment](https://docs-platform.crewai.com/platform/en/guides/prepare-for-deployment), [Deploy to AMP](https://docs-platform.crewai.com/platform/en/guides/deploy-to-amp), [Automations](https://docs-platform.crewai.com/platform/en/features/automations), [Monorepo Deployments](https://docs-platform.crewai.com/platform/en/guides/monorepo-deployments), [CLI](https://docs.crewai.com/en/concepts/cli)

For related skills:

- **call-deployed-crew** - `/inputs`, `/kickoff`, `/status` once the deployment is Online
- **test-crewai-project** - offline stub LLM so `crewai run` and validate work without keys
- **check-crewai-api** - current `LLM` model strings, default model, structured output
- **build-flow** - Flow state, routers, persistence
- **connect-tools-and-mcp** - which tool and MCP transports work on a hosted deployment
- **ask-docs** - query the live docs for anything not covered here
