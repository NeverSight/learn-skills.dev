---
name: traigent-setup-quickstart
description: "Install and wire the Traigent SDK in an existing project, and get first value from it. Use when the user wants to install traigent, set up their first optimization, create an evaluation dataset, or get started with @traigent.optimize; a brand-new user with an agent to optimize is better served by the guided first run (Traigent/traigent-first-run), which this skill points at. Covers pip install, API-key setup, mock mode, a linear first-value walkthrough, and running a first optimization."
license: Apache-2.0
metadata:
  traigent-audience: sdk-user
  traigent-topic: agent-optimization
  traigent-stage: setup
  traigent-maturity: stable
  author: Nimrod
  version: "1.0.27"
---

# Traigent Quickstart

## When to Use

Requires `traigent>=0.24.0` (the `traigent plan` command used below shipped in 0.17.0).

Use this skill when:

- Setting up Traigent for the first time in a new project
- Installing the SDK and configuring the environment
- Creating a first `@traigent.optimize` decorated function
- Building an evaluation dataset in JSONL format
- Verifying that the installation works correctly
- Running optimization in mock mode for development

## Optimization Economics — Read This Before Sizing a Run

**Do not default to recommending zero spend.** The canonical Traigent posture on spending,
the five characterization questions with their exact options, the tailoring rules (including
the three-option paging rule), the explanation duty, and the local survey draft contract all
live in one file that ships inside this skill:
**`references/economics-characterization.v0.md`**. Read it from this skill's own directory
before you propose, size, or decline a run — it is deliberately not restated here. It is
generated from `docs/shared/economics-characterization.v0.md` in the traigent-skills repo,
which is where any edit goes; the copy shipped here is byte-identical.

**Characterize, never compute a budget locally.** Collect the characterization and relay it;
the Traigent service authors the budget, exactly as it authors the run-plan and the next-step
decision — **budget authorship belongs to the service.** Do not compute, adjust, or recommend a
budget locally: no budget arithmetic in markdown, no floor/cap table, no "roughly $X/day" of
your own. The reference describes what the service computes; it is not a local calculator, and
when the service returns no economics result, say so plainly and continue with **no budget
number at all** rather than inventing one.

**This skill's part:** characterize the value the user's agent creates and relay it, so the
service can size a bounded first experiment to it.

**Mandatory whenever you relay any of it:** show the options, recommend exactly one, and
explain **why in the user's own numbers** — their agent, their volumes, their error costs. The
explanation is a product requirement, not decoration.

Safety is unchanged and unweakened: mock/dry-run first, **explicit user approval before any
paid run**, an explicit spend cap, and the recorded stop rule. The service sets
*how much* to invest; it never affects *whether* approval is required — it always is.

## Cold Start — First Value, One Step at a Time

**Brand-new to Traigent with an agent to optimize?** Use the guided first run, the funnel
traigent.ai hands out: `npx skills add Traigent/traigent-first-run`, then ask
`Use $traigent-first-run to run my first Traigent optimization.` It scores the project's
readiness, preserves the real agent, dataset and evaluator, and lists what it had to
generate under its Walkthrough setup. The guided run is self-contained and hands over to
these skills afterwards; `traigent-boost-agent` calls into this skill for install-and-wire,
and the path below is for when the guided run is not available.

**When there's no prior run to look at**, do not open with menus, methodology, or the
advanced sections below. Detect cold start — the user is new to Traigent, has never
viewed a run, and has no dataset or decorated function ready — and walk them to their
**first visible result** one action at a time: one question or one command, wait, then
the next. Never dump the whole pipeline at once.

The linear path:

1. **Find the agent to optimize.** Ask for (or detect from the project) the one function
   that calls an LLM. Just that — don't discuss knobs yet.
2. **Find or make the dataset.** If they already have labeled examples, hand off to
   `traigent-dataset-curate` for the one canonical dataset contract. If they have
   **nothing** ready, use the bundled fallback below — no dataset needed to see value.
3. **Mock dry-run first.** Always run keyless mock mode before anything paid (the "Your
   First Optimization" example below is exactly this). Show the ranked table so they see
   the loop work at zero cost and zero egress.
4. **Confirm the real run explicitly.** A real (paid) run happens only after the user
   sees the mock result and says go — and after the cost-gate approval. Never jump from
   mock straight to spend. Show the card in `references/run-cost-and-limits.md` first:
   `cost_limit` only bounds the calls Traigent can measure.
5. **View it in the portal.** Once a real run launches, watch the run start, watch the
   rows appear on the portal, and have the user open and inspect the run.

**Where the plan comes from — honesty rule.** When it's time to decide *what* to tune,
ask the Traigent **service** for the run plan via the `traigent-analyze-guidance` skill (its
`traigent plan` CLI / `get_optimization_plan` MCP tool). Present the **one** plan the
service returns — not a menu you invented. There is **no onboarding/phase parameter** in
the SDK or CLI today, so don't pass one or imply the client picks a phase. If the service
can't return a plan, say so plainly and fall back to a **generic, conservative knob
family** — `model` + `temperature` only, explicitly labeled as a generic fallback. Never
encode task-specific ordering (scout/pivot/routing) in these docs; the service owns that.
Tasks like text2SQL, RAG, classification, and extraction may be *named* as things the
service plans for — but the plan logic stays server-side.

**No agent or dataset yet?** Start from `references/first-value-fallback.md` — a complete
mock-first first-value path that needs neither, then gates any real-provider spend behind
explicit approval and a `cost_limit` cap.

Once the user has seen a first result, hand off to the lifecycle skills rather than
duplicating them here: `traigent-dataset-curate` (real data), `traigent-setup-decorator`
(a real decorator), and `traigent-analyze-guidance` (what to do after a run). Do **not** surface
advanced playbooks during cold start.

## Installation

> **This is the Python SDK skill.** Building in **JavaScript/TypeScript** instead? Use the
> **`traigent-js`** skill — it covers the native JS/TS optimizer (the `@traigent/sdk` package)
> with a different install and API. The rest of this page assumes Python.

### Basic Install

The fast path is the core floored install — sufficient for the entire keyless mock
quickstart because `litellm` ships in core. Install optional extras only after the mock
run succeeds.

```bash
pip install "traigent>=0.19"
python - <<'PY'
import importlib.metadata as md
import traigent
v = md.version("traigent")
if v == "0.0.1" or not hasattr(traigent, "optimize"):
    raise SystemExit(
        f"Bad Traigent install: traigent {v}. "
        'You likely got the PyPI placeholder — reinstall with: python -m pip install --upgrade "traigent>=0.19"'
    )
print(f"traigent {v} OK")
PY
```

> **Warning:** pip printing `traigent 0.0.1 does not provide the extra ...` is **FATAL** — you installed the placeholder package; reinstall with `python -m pip install --upgrade "traigent>=0.19"`. The same message with a real version (e.g. `traigent 0.27.0 does not provide the extra 'dspy'`) means that extra does not exist — reinstalling Traigent will not help; check `references/installation-extras.md`.

### Literal First Run (execution-only agents)

Run this entire block in the foreground and wait for it to finish. Do not split it,
background it, or continue after a failed command. The final expected line is
`TRAIGENT-DRY-RUN-OK`.

```bash
#!/usr/bin/env bash
set -euo pipefail

# Mock/offline env is set in bash, BEFORE python imports anything.
export TRAIGENT_OFFLINE_MODE=true
export LITELLM_LOCAL_MODEL_COST_MAP=True

python -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade --timeout 60 --retries 5 "traigent>=0.19"
python - <<'PY'
import importlib.metadata as md
import traigent
v = md.version("traigent")
if v == "0.0.1" or not hasattr(traigent, "optimize"):
    raise SystemExit(
        f"Bad Traigent install: traigent {v}. "
        'You likely got the PyPI placeholder — reinstall with: python -m pip install --upgrade "traigent>=0.19"'
    )
print(f"traigent {v} OK")
PY

cat > ticket_eval.jsonl <<'JSONL'
{"input": "I was charged twice for my subscription", "output": "billing"}
{"input": "Please update the email address on my account", "output": "account"}
{"input": "The API returns a 500 error on POST requests", "output": "technical"}
{"input": "What are your business hours?", "output": "general"}
{"input": "My invoice has the wrong tax ID", "output": "billing"}
{"input": "I cannot reset my password", "output": "account"}
JSONL

cat > ticket_classifier.py <<'PY'
import traigent, litellm
from traigent.testing import enable_mock_mode_for_quickstart

enable_mock_mode_for_quickstart()


def mock_demo_accuracy(output, expected, config=None, **_):
    # Mock-only demo scorer; delete this for real runs.
    cfg = config or traigent.get_config() or {}
    base = 0.88 if cfg.get("model") == "gpt-4o" else 0.68
    return max(0.0, base - 0.04 * float(cfg.get("temperature", 0.0)))


@traigent.optimize(
    eval_dataset="ticket_eval.jsonl",
    objectives=["accuracy"],
    configuration_space={
        "model": ["gpt-4o-mini", "gpt-4o"],
        "temperature": [0.0, 0.7],
    },
    metric_functions={"accuracy": mock_demo_accuracy},
    offline=True,
)
def classify_ticket(query: str) -> str:
    config = traigent.get_config()
    response = litellm.completion(
        model=config["model"],
        temperature=config["temperature"],
        messages=[
            {"role": "system", "content": "Classify the ticket as: billing, technical, account, or general."},
            {"role": "user", "content": query},
        ],
    )
    return response.choices[0].message.content


results = classify_ticket.optimize_sync(max_trials=4, algorithm="grid")
print(f"Stop reason: {getattr(results, 'stop_reason', None)}")
print(f"Best config: {results.best_config}")
assert results.trials, "no trials ran"
assert not getattr(results, "failed_trials", []), f"failed trials: {results.failed_trials}"
assert results.best_config is not None, "no best config selected"
print("TRAIGENT-DRY-RUN-OK")
PY

python ticket_classifier.py
```

This block is generated from `references/literal-quickstart.sh` — edit that file, not the block.

### Use a virtual environment (recommended)

Install into a project virtualenv — it's standard Python practice and it's the friction-free
path here. A **fresh** venv is enough; you do **not** need `--system-site-packages`.

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
python -m pip install --upgrade "traigent>=0.19"
```

`pip install "traigent>=0.19"` resolves from PyPI and pulls `litellm` (a **core dependency**) along with
it, so the keyless mock path — which intercepts `litellm.completion(...)` — works immediately,
with no extra install. Only the LangChain / OpenAI / Anthropic *adapter* clients live in the
`integrations` extra (below).

> **Why a venv instead of system Python?** On modern Debian/Ubuntu/Fedora the system interpreter
> is marked *externally managed* (PEP 668), so a bare `pip install` into it is refused with
> `error: externally-managed-environment`. The venv above avoids that entirely.

### With Optional Extras

Install these after the keyless mock run succeeds.

```bash
# Recommended extras after the mock run succeeds
pip install "traigent[recommended]>=0.19"

# Framework integrations (LangChain, OpenAI, Anthropic, MLflow, W&B)
pip install "traigent[integrations]>=0.19"

# Analytics (numpy, pandas, matplotlib)
pip install "traigent[analytics]>=0.19"

# All optional features
pip install "traigent[all]>=0.19"

# Enterprise bundle (all production features)
pip install "traigent[enterprise]>=0.19"
```

See `references/installation-extras.md` for the full table of extras and their contents.

### Requirements

- Python >= 3.11

## Get Your Traigent API Key

Backend-connected features (the default cloud smart optimizer, dataset synthesis, analytics dashboards, the CI gate, and portal result history) all require `TRAIGENT_API_KEY`. There are two ways to obtain it:

### Portal key (Full access preset)

1. Sign up at the Traigent portal and create a project.
2. In your project settings, go to **API Keys → Create key** and choose **Full access**. The dialog's default preset is **read-only**: a read-only key is refused at session creation (nothing spent), or, if accepted and then rejected mid-run, drops the run to local-only tracking while it keeps spending.
3. The key is `user`-type with the `uk_` prefix; with full access it covers SDK optimizations and analytics.

```bash
export TRAIGENT_API_KEY="uk_..."   # portal keys use the uk_ prefix
```

### CLI device-authorization key (project-scoped)

The CLI device-flow issues a project-scoped `sk_`-prefixed key with broader permissions (quota, dataset management, full project access). Use this when you need project-level operations beyond experiments.

Run `traigent auth login` in your terminal — it opens a browser for OAuth device authorization. The key is saved to your encrypted local credential store at `~/.traigent/secure_credentials.enc` (secured with `TRAIGENT_MASTER_PASSWORD`); the legacy plaintext `~/.traigent/credentials.json` is no longer read unless `TRAIGENT_ALLOW_PLAINTEXT_CREDENTIALS=true` is set for a one-time migration. Then export it:

```bash
export TRAIGENT_API_KEY="sk_..."
```

**Which key to use?** A Full-access portal key is sufficient for most optimization workflows. Use the device-flow key for quota management, cross-project access, or when the CLI reports permission errors.

For the standard path, set `TRAIGENT_API_KEY` once, omit `algorithm` and `offline`, and let Traigent use the default cloud smart optimizer with portal result sync. Use `algorithm="grid"` or `"random"` only when you explicitly want local search; use `offline=True` only when zero Traigent backend egress is required.

For a run the user approved *as* managed optimization, set `TRAIGENT_REQUIRE_CLOUD=1`: without it, a run that finds no key in its process, or hits a connectivity failure, 5xx or HTTP 400 at session creation, does not fail — the SDK prints one warning and runs a **local random search** whose result reads like the managed one (a key the backend rejects raises instead). After the run, check `results.cloud_url` before telling the user to open the portal; `None` (with `results.metadata.get("source") == "local_fallback"`) means the run was never tracked and is a failure to investigate, not a result to report.

> **Prereq for real (non-offline) runs: set `TRAIGENT_API_KEY`.**
> The SDK defaults to the cloud backend (`https://portal.traigent.ai`) when
> `TRAIGENT_BACKEND_URL` is unset — no env var is needed for the standard cloud path.
> Set `TRAIGENT_BACKEND_URL` only to target a dev or self-hosted backend
> (e.g. `http://localhost:5000`). Exception: the `traigent plan` CLI command resolves
> `--backend-url` as flag → `TRAIGENT_BACKEND_URL` / the URL stored by `traigent auth login` →
> a local default (`http://localhost:5000`), so for cloud use log in first or pass the
> flag/env var explicitly. `plan` honors the stored auth-login URL since 0.20.0
> (see version-matrix: `backend-url`) — on SDK <= 0.19.x it ignored the stored
> `traigent auth login` URL and always defaulted to localhost unless the flag or env var was
> passed (Traigent/Traigent#1721). (The retired `next-steps` command, absent from SDK 0.26.0,
> shared this resolution on the older versions that still ship it.)
> Portal-issued API keys use the `uk_...` prefix.
>
> ```bash
> export TRAIGENT_API_KEY="uk_..."                              # portal-issued key
> export TRAIGENT_BACKEND_URL="https://portal.traigent.ai"     # optional: cloud is already the default
> ```

### Key Hygiene — Reference Names, Never Values

Observed across multiple coding-agent CLI families (Codex, Claude, Gemini), not one tool's quirk —
treat every rule below as universal regardless of which agent is driving the session.

- **Never print, echo, or log a key value.** `echo $TRAIGENT_API_KEY`, a bare `env`/`printenv`
  dump, and `set -x`/`bash -x` wrapped around any key-touching command are all leaks — each writes
  the raw secret to stdout, which most agent harnesses capture into the visible transcript and
  often into a log file too.
- **Reference keys only by env-var name** (`TRAIGENT_API_KEY`, `OPENAI_API_KEY`, ...) in commands,
  code, and chat — never paste or reconstruct the value itself.
- **Treat transcripts and logs as shareable artifacts.** Assume anything printed to the terminal
  or written to a log may be read, copied, or shared later; keep secrets out of both.

## Environment Setup

### Development Mode (Recommended for Getting Started)

Mock mode is the keyless dev path for provider calls — LLM calls are intercepted and return canned responses. Activate it in code:

```python
from traigent.testing import enable_mock_mode_for_quickstart

enable_mock_mode_for_quickstart()
```

<!-- PROTECTED -->
- `enable_mock_mode_for_quickstart()` is the recommended activation path. It is **hard-blocked when `ENVIRONMENT=production`** and emits a once-per-process WARNING so a test that accidentally runs in a deployed system is loud and visible.
<!-- /PROTECTED -->
- **Mock scope:** only LiteLLM (`litellm.completion`) and LangChain (`ChatOpenAI`, `ChatAnthropic`, etc.) calls are intercepted. Raw `openai.OpenAI()` / `anthropic.Anthropic()` clients are **not** intercepted — a function using a raw client will make real, billable calls in mock mode. Use LiteLLM in examples that must run keyless.
- **No separate install needed for mock:** `litellm` ships with the SDK *core* (`pip install "traigent>=0.19"` pulls it), so `litellm.completion(...)` is interceptable the moment Traigent is installed — you do **not** need to `pip install litellm` yourself. (LangChain adapters do require `pip install "traigent[integrations]>=0.19"`.)
- **Mock ≠ offline.** Mock stops LLM *cost* (calls are intercepted) — it does **not** stop *backend egress*. With `TRAIGENT_API_KEY` set and the default `offline=False`, a "mock dry-run" is **still sent to the Traigent backend and appears on your portal** as a mock-data experiment (and counts against quota). For a fully local, private dry-run, also pass `offline=True` — `traigent auth login` leaves a stored key the SDK picks up even with `TRAIGENT_API_KEY` unset, so "no key" is not a state you can assert; `offline=True` is the only assertable no-egress state. `enable_mock_mode_for_quickstart()` alone does **not** make a run local.
- **Real metrics read 0.0 under mock.** Every intercepted call returns the same canned text, so exact/execution-match scorers score a uniform 0.0 across trials — expected in mock, not a broken pipeline (that is exactly why the example below wires a mock-only demo scorer).

### Legacy Env-Var Path

<!-- PROTECTED -->
The previous quickstart docs taught `export TRAIGENT_MOCK_LLM=true`. That env var still works in non-production environments for backward compatibility with existing fixtures, but it is hard-blocked when `ENVIRONMENT=production` (an `OSError` is raised at the first decoration, `optimize()` or CLI use — a bare `import traigent` still succeeds). Prefer the in-code API for new code.
`TRAIGENT_MOCK_LLM=true` is deprecated on traigent 0.27.0 (DeprecationWarning, hidden by default;
"will be removed in a future release"). Use `traigent.testing.enable_mock_mode_for_quickstart()` in code,
e.g. from a pytest fixture/conftest, for new setups.
<!-- /PROTECTED -->

### Using a .env File

Load `.env` yourself at the top of the script — `from dotenv import load_dotenv; load_dotenv()` (`python-dotenv` ships with `litellm`, so no extra is needed). The SDK does **not** read your project's `.env` (it only looks beside its own installed package); whether `litellm`'s import happens to find yours depends on where the venv sits. Create a `.env` file in your project root:

```
TRAIGENT_API_KEY=uk_...   # portal key; use your sk_... key here if you used the CLI device flow
OPENAI_API_KEY=sk-...
TRAIGENT_DEBUG=1
```

#### Recommended: have the user paste keys into `.env`, never into the chat

When a user says *"I have my key"*, do **not** ask them to type the secret into the
conversation — it would be captured in the agent transcript, logs, and context. Open the
`.env` file for them to paste into directly. This is both **more secure** (the raw key
never touches the chat) and **better UX** (they see exactly where it goes). Procedure:

1. **Create the file** from the project template if one exists (`cp .env.example .env`),
   otherwise create a minimal `.env` with key *names* pre-filled and values blank, so the
   user only pastes after each `=`:
   ```
   TRAIGENT_API_KEY=
   # provider key — fill the one(s) this project uses:
   OPENAI_API_KEY=
   # ANTHROPIC_API_KEY=
   # Bedrock: AWS_ACCESS_KEY_ID= / AWS_SECRET_ACCESS_KEY= / AWS_REGION=
   ```
2. **Always show the user the absolute path** (e.g. `/home/me/proj/.env`). This is the
   guaranteed fallback — they can open it in their own editor no matter what happens next.
   Before any key is pasted, run `chmod 600 .env`, `git ls-files --error-unmatch -- .env`
   (must exit 1 — a tracked `.env` stays tracked whatever `.gitignore` says) and
   `git check-ignore -q -- .env` (must exit 0); a key pasted into a tracked file is already
   the state these checks exist to prevent.
3. **Best-effort: pop the file open in a _standalone_ editor window, launched _detached_.**
   Pick the launcher by OS; never wrap it in `timeout`:
   - **Linux:** `setsid -f gnome-text-editor "$ENV"` — or the first of
     `kate` / `gedit` / `xed` / `mousepad` that exists; last resort `xdg-open "$ENV"`.
   - **macOS:** `open -t "$ENV"` (opens the default text editor in its own window).
   - **Windows:** `start "" notepad "%ENV%"` (Notepad is always present), or
     `Start-Process notepad "$env:ENV"` in PowerShell.

   **Pitfalls that look like success but aren't** (verified the hard way):
   - **Don't** open via the user's IDE (`code <file>` / `cursor <file>`): it can spawn a
     nested instance that *crashes*, and it hijacks whichever IDE window is focused — so
     `.env` can pop up inside an unrelated project.
   - **Don't** trust the launcher's exit code as "opened" — a crashed window can still exit 0.
     Verify the editor process is actually alive (e.g. `pgrep`) **and ask the user to confirm
     the window appeared.**
4. **Pick the provider key by detecting the vendor from the project** (its
   `openai` / `anthropic` / `litellm` / Bedrock imports or config). If the vendor is
   ambiguous, undetectable, or the project uses **multiple** providers (e.g. OpenAI *and*
   Bedrock), **ask the user which provider(s)** and label the matching key(s) in `.env`.
5. **Wait** for the user to paste and save.
6. **Fallback:** if no standalone editor opens (or the user says no window appeared), have
   them open the printed path manually; only as a last resort use a terminal `export VAR=...`
   (less private than the file).

> Never echo, log, or read back the key value. `.env` must be git-ignored — never commit real keys.

### Production Mode

For production, set your provider API keys and don't call `enable_mock_mode_for_quickstart()`:

```bash
export OPENAI_API_KEY=sk-...
# or
export ANTHROPIC_API_KEY=sk-ant-...
```

> **Before your first real run, verify your model IDs are live.** Provider catalogs change — a
> delisted or renamed ID causes a 404 or a degraded/unpriced trial. Preflight with
> `traigent models --provider <p> --check <model_id>` (see the CLI Quick Reference below) to
> catch typos and unknown ID shapes — but know its limit: the check validates against a
> **shipped model snapshot with pattern-based fallback**, so a retired-but-well-formed ID still
> passes; it does **not** detect provider-side delisting. To confirm an ID is actually live,
> query the provider's catalog directly (e.g. `curl -s https://openrouter.ai/api/v1/models`
> for OpenRouter). The `traigent-setup-integrations` skill covers multi-provider model verification.

See `references/environment-variables.md` for all available environment variables.

## Your First Optimization

> **Always dry-run first.** Before a real (paid) run, run in mock mode, review the cost estimate, and get explicit approval. See the `traigent` lifecycle skill for the mandatory dry-run-first / cost-approval workflow.
>
> **Real LLM runs require the user's approval — the SDK's cost handshake is conditional, not a
> gate you can lean on.** The SDK prompts only when its pre-run estimate exceeds
> `TRAIGENT_RUN_COST_LIMIT` (default **$2.00**) or a model is unpriced; a priced run whose
> estimate is under the cap starts real calls immediately, with no prompt. Your explicit
> approval of a stated ceiling is the gate. Set `TRAIGENT_COST_APPROVED=true` (or
> `cost_approved=True` in the decorator) only in the process of an approved run, never in
> `.env` or a shell profile — it also turns the unpriced-model refusal into a warning. The
> estimate may be high (fallback pricing is conservative); read `results.stop_reason` after
> the run.

### Tiny Real Cost and KPI Probe

After the mock dry-run passes and before any full run, run one tiny **real** optimization: 1-2 dataset examples, minimal trials, and the cheapest candidate model. Check both surfaces before scaling up: `results.total_cost` must be neither `None` nor `0.0` with real calls (both mean cost is not wired), and each trial's `metrics` must contain the declared objectives with non-degenerate values (not all `0.0`/all `1.0`). If either surface fails, wire it first — see `traigent-optimize-run` → Cost Wiring Probe for the fix ladder (custom model pricing env vars, per-trial cost metrics, `TRAIGENT_STRICT_COST_ACCOUNTING`).

> **Objective naming rule:** Default: at least one objective labeled `accuracy` (built-in objective or your `metric_functions` key). If accuracy doesn't apply to this problem, name the primary quality KPI after the product concept, for example `valid_schema`, and note why accuracy was skipped.

Here is a complete working example. This function classifies customer queries using an LLM, and Traigent will find the best model and temperature combination.

**Note on mock scope:** `enable_mock_mode_for_quickstart()` intercepts LiteLLM and LangChain calls. Raw `openai.OpenAI()` / `anthropic.Anthropic()` client calls are **not** intercepted — use `litellm.completion()` for a fully keyless dry-run (see `references/installation-extras.md` for `traigent[integrations]`).

**Why the example includes a `mock_demo_accuracy` scorer:** in mock mode every LLM call returns the *same* canned string, so a **real** accuracy metric scores every trial 0.0 — a discouraging all-zeros table that looks broken. The demo scorer below ignores the (canned) output and ranks trials by their config, so the keyless dry-run produces a meaningful table — the same approach the bundled `traigent quickstart` command uses. It is **mock-only: delete it for a real run**, where Traigent scores actual model output against your dataset labels. (Prefer not to keep a placeholder scorer in your own code? Just run `traigent quickstart` for the same ranked demo without writing one.)

```python runnable
import asyncio
import os
from pathlib import Path

# Set no-egress flags before importing Traigent or LiteLLM.
os.environ["TRAIGENT_OFFLINE_MODE"] = "true"
os.environ["LITELLM_LOCAL_MODEL_COST_MAP"] = "True"

import litellm  # pip install "traigent>=0.19"
import traigent
from traigent import Choices
from traigent.testing import enable_mock_mode_for_quickstart

# Step 1: dry-run in mock mode — no API keys required, no cost
enable_mock_mode_for_quickstart()

Path("eval_queries.jsonl").write_text(
    "\n".join(
        [
            '{"input": "I was charged twice for my subscription", "output": "billing"}',
            '{"input": "The API returns a 500 error on POST requests", "output": "technical"}',
            '{"input": "What are your business hours?", "output": "general"}',
        ]
    )
    + "\n",
    encoding="utf-8",
)


def mock_demo_accuracy(output, expected, config=None, **_):
    """Mock-only demo scorer — DELETE this for a real (paid) run.

    In mock mode every ``litellm.completion`` call returns the same canned
    string, so a real accuracy metric would score every trial 0.0 (a
    misleading all-zeros table). This placeholder ignores ``output`` and ranks
    trials by their config so the keyless dry-run produces a meaningful table —
    the same trick the bundled ``traigent quickstart`` demo uses. On a real run,
    remove it and let Traigent score actual model output against your labels.
    """
    cfg = config or traigent.get_config() or {}
    base = 0.85 if cfg.get("model") == "gpt-4o" else 0.65
    return max(0.0, base - 0.05 * float(cfg.get("temperature", 0.5)))


@traigent.optimize(
    eval_dataset="eval_queries.jsonl",
    objectives=["accuracy"],
    algorithm="random",
    offline=True,
    model=Choices(["gpt-4o-mini", "gpt-4o"]),
    temperature=Choices([0.0, 0.5, 1.0]),
    metric_functions={"accuracy": mock_demo_accuracy},  # mock-only; delete for a real run
)
def classify_query(query: str) -> str:
    config = traigent.get_config()
    # Use litellm so mock mode intercepts the call (raw openai client is NOT intercepted)
    response = litellm.completion(
        model=config["model"],
        temperature=config["temperature"],
        messages=[
            {"role": "system", "content": "Classify the query as: billing, technical, or general."},
            {"role": "user", "content": query},
        ],
    )
    return response.choices[0].message.content


async def main():
    # Step 1: dry-run (mock) — confirm the setup works and review estimated cost
    results = await classify_query.optimize(max_trials=6)

    # Inspect results
    print(f"Best config: {results.best_config}")
    print(f"Best score:  {results.best_score}")
    print(f"Trials run:  {len(results.trials)}")

    if results.best_config is None:
        print("No eligible winner; inspect trial errors before continuing.")
        return results

    # Exercise configuration application inside this mock demo only.
    # Synthetic scores cannot authorize production promotion: replace the demo
    # scorer, run the approved real experiment, then evaluate a frozen candidate
    # on an independent holdout using traigent-ci-safety-gate.
    print("Demo only: this mock-selected configuration is not approved for production.")
    classify_query.apply_best_config(results)

    # Now calling the function uses the best config
    answer = classify_query("I can't log in to my account")
    print(f"Classification: {answer}")
    return results


if __name__ == "__main__":
    asyncio.run(main())
```

> **In a notebook (Jupyter/IPython/Colab)?** `asyncio.run()` raises
> `RuntimeError: asyncio.run() cannot be called from a running event loop` there — the notebook
> already runs one. Use `await main()` directly in a cell, or the synchronous alternative below.

### Synchronous Alternative

If you prefer synchronous execution:

```python
results = classify_query.optimize_sync(max_trials=6)  # uses the offline random dry-run settings above
```

> **`expected` is a scoring label — do not put it in your agent function's signature.**
> The evaluator calls your function with the example's *input* fields only (plus any
> config-injected params). It then passes the function's *output* and the dataset's
> `expected` / `output` field to your `scoring_function` or `metric_functions`. A
> function that declares `expected` as a parameter will fail every trial with
> `TypeError: missing required argument: 'expected'`.
>
> ```python
> # WRONG — fails every trial
> def classify_query(query: str, expected: str) -> str: ...
>
> # CORRECT — function takes input fields only; scorer receives (output, expected)
> def classify_query(query: str) -> str: ...
> def score(output: str, expected: str) -> float: ...
> ```

### Key Concepts

1. **`@traigent.optimize(...)`** -- Decorator that wraps your function for optimization. Define what parameters to tune in the decorator arguments.
2. **`traigent.get_config()`** -- Call inside your function to retrieve the current trial's configuration. Works during optimization trials and after `apply_best_config()`.
3. **`func.optimize(max_trials=N)`** -- Run the optimization loop asynchronously. Returns an `OptimizationResult`.
4. **`func.apply_best_config(results)`** -- Lock in the best configuration found so that subsequent calls use it.

> **You've run your first optimization — now make it robust.** The decorator above is intentionally a *local dry-run* recipe: a small `model` + `temperature` space, `algorithm="random"`, and `offline=True`. For a real optimization, graduate to the more robust **`traigent-setup-decorator`** skill — custom evaluators / `metric_functions`, injection mode, execution policy, and weighted objectives — then launch with **`traigent-optimize-run`**, which adds what a *real* run needs beyond the basic `.optimize()` call: **cost limits** (cap a paid sweep before it overruns), **algorithm choice** (`"auto"` for connected real runs; `"grid"`/`"random"` for explicit local/offline search; named smart selectors like `bayesian`/`optuna` on authenticated connected runs, SDK 0.20.1+), **parallel trials**, and **quota-aware run sizing**. That `decorator-setup` → `run-optimization` pair is the recommended path from "first run" to a production optimization.

## Dataset Format

Traigent uses JSONL (JSON Lines) files for evaluation datasets. Each line must have an `input` field and an `output` field.

### Example: `eval_queries.jsonl`

```jsonl
{"input": "I was charged twice for my subscription", "output": "billing"}
{"input": "The API returns a 500 error on POST requests", "output": "technical"}
{"input": "What are your business hours?", "output": "general"}
```

- **`input`** -- The value passed to your function during evaluation.
- **`output`** -- The expected/ground-truth result used for scoring.

You can include additional fields for metadata, but `input` and `output` are required.

> **One canonical contract.** This flat form is the simplest case of the single Traigent dataset
> contract: `input` (or `input_data`) → your function's args, the **gold key** → the expected value,
> and **every other top-level key** → `example.metadata[...]` (how a per-example side field like a
> `db_path` reaches a scorer). Values may be **nested dicts**, and the gold key has accepted aliases
> (`output`, `expected`, `expected_output`, `answer`, `target`, `label`). See `traigent-dataset-curate`
> for the full contract and `traigent-eval-build` for an execution-scored recipe that reads a
> `metadata` field.

> **Dataset path sandbox.** The SDK enforces a `TRAIGENT_DATASET_ROOT` / CWD sandbox — an
> eval-dataset path outside the sandbox root (default: the **current working directory**) is
> rejected at load with a `ConfigurationError` ("Dataset path must reside under …"). Keep the JSONL under the directory you run from,
> or set `TRAIGENT_DATASET_ROOT` to the directory containing your datasets.

### Tips for Good Datasets

- Include at least 10-20 examples for meaningful optimization.
- Cover edge cases and diverse inputs.
- Ensure ground-truth `output` values are consistent and well-defined.
- Reserve a holdout slice before tuning; never tune and validate on the same rows.
- For evaluation dataset creation beyond this minimal JSONL, use `traigent-dataset-curate`.

## Verify Installation

### Check SDK info

```bash
traigent info
```

This prints the installed version, Python version, available integrations, and optimization defaults.

### Verify from Python

```python
import traigent
print(traigent.get_version_info())
```

### Validate an evaluation dataset

```bash
traigent validate eval_queries.jsonl
```

## CLI Quick Reference

**Start here (keyless, no API key required):**

```bash
traigent quickstart      # bundled working demo — mock mode, zero config
traigent onboard         # guided first-run setup wizard
```

| Command                    | Description                                                         |
| -------------------------- | ------------------------------------------------------------------- |
| `traigent quickstart`      | Run the bundled mock-mode demo (keyless, zero-setup, always works)  |
| `traigent onboard`         | Guided setup for Traigent in this project (API key, project, env)   |
| `traigent models`          | List/validate model IDs before a run, e.g. `traigent models --provider anthropic --check claude-3-haiku-20240307` (ID-shape preflight against a shipped snapshot; confirm liveness via the provider's catalog) |
| `traigent generate-config` | Scaffold a full `@traigent.optimize()` config for your function     |
| `traigent detect-tvars`    | Detect tuned-variable candidates in existing Python files           |
| `traigent info`            | Show SDK version, environment, and integrations                     |
| `traigent algorithms`      | List available optimization algorithms                              |
| `traigent validate`        | Validate dataset files and configuration                            |

## Next Steps

- **Configure your decorator for a real optimization** -- The example above is the *minimal* decorator. To make it optimization-ready -- custom evaluators / `metric_functions`, injection mode, execution (`algorithm`/`offline`), and weighted objectives -- use the `traigent-setup-decorator` skill, then launch with `traigent-optimize-run`. This `decorator-setup` → `run-optimization` pair is the standard two-step cycle for going from "first run" to a real optimization.
- **Dry-run before a real run** -- See the `traigent` lifecycle skill for the mandatory dry-run-first / cost-approval workflow before any paid execution.
- **Mind your plan quota** -- Cloud optimization is metered by `optimization_samples` (~`max_trials × dataset_size` per run) and `optimization_trials`, separate from dollar cost. Check usage and size large runs to fit; see the `traigent-optimize-run` skill ("Quota & Run Sizing").
- **Define parameter search spaces** -- See the `traigent-optimize-config-space` skill for `Range`, `IntRange`, `Choices`, `LogRange`, factory presets, and constraints.
- **Choose an optimization algorithm** -- For connected real runs, omit `algorithm` or use `"auto"`; use `"grid"`/`"random"` for explicit local/offline search. `traigent algorithms` lists auto + smart names since 0.20.1 (see version-matrix: `algorithms-cli`) — the full public selector surface with a local/connected availability column (on 0.20.0 the CLI omitted `auto` and the smart names: Traigent/Traigent#1751). Named smart selectors execute on connected runs since 0.20.1 (see version-matrix: `smart-selector-exec`): `bayesian`/`tpe`/`optuna`/`optuna_tpe`/`optuna_random` bind to the typed backend Optuna strategy, while unsupported smart names such as `nsga2`/`cmaes` fail fast with a capability message (Traigent/Traigent#1752, #1758; on 0.20.0 no smart name executed end-to-end). With `offline=True` every smart name still raises `ConfigurationError` at decoration time (verified on 0.21.0). The `traigent-optimize-run` skill owns the full selector contract.
- **Add multiple objectives** -- Use `objectives=["accuracy", "cost", "latency"]` for multi-objective optimization.
- **Use framework integrations** -- Install `traigent[integrations]` for LangChain, OpenAI, and Anthropic adapters.
- **Verify model IDs before a real run** -- Catalogs change; run `traigent models --provider <p> --check <id>` to catch typos and unknown ID shapes, then confirm the ID is actually live against the provider's catalog — the CLI check validates a shipped snapshot with pattern fallback and cannot detect provider-side delisting, so a retired/renamed ID can still pass and cause a 404 or a degraded, unpriced trial. See `traigent-setup-integrations`.

<!-- Reserved: managed longitudinal-guidance region. Step-level edits must not write here. -->
<!-- SLOW_UPDATE -->
<!-- /SLOW_UPDATE -->

<!-- INTERACTION_POLICY v1 (synced — do not edit inline; edit docs/shared/interaction-policy.v1.md) -->
## Traigent Interaction Policy
Track an interaction profile and adapt to it. Persona (stable): control=`delegate|guided|inspect`,
expertise=`se|ds|unknown`. Mood (this session): pace=`execute|balanced|explore`. Default when
unknown: `guided,se,balanced`. Infer from explicit user statements first, then recent behavior;
an explicit correction wins immediately. Never store or send this profile anywhere by default.

### Fetch the live profile (when available)
At session or skill start, if a configured Traigent client is available, seed the profile from the
backend with the skill name:

```python
policy = None
try: policy = await client.get_interaction_policy(skill="<this skill>")
except Exception: pass
```

Treat the returned `profile` as the STARTING seed: its control/expertise/pace axes plus
`question_budget`, `options_max`, and `jargon_level` replace the static defaults below. Explicit user
corrections in-conversation ALWAYS override the seed. If the call is unavailable or
`fallback_policy="static_v1"`, simply use the static defaults below; the SDK already fails soft.

- Always be concise.
- Match terminology to expertise. For `se`: plain engineering words; define each Traigent or
  statistics term once in plain language (no Bayesian / variance-decomposition / Pareto jargon
  unless asked). For `ds`: compact optimization and statistical terms are fine.
- Presenting options: show at most 3, mark exactly one **Recommended**, and give one short
  persona-appropriate trade-off per option.
- Autonomy. For `delegate` or `execute`: pick the recommended reversible action and proceed, asking
  only at hard gates. For `guided`: offer options with a recommendation at the key decisions. For
  `inspect` or `explore`: give brief rationale or evidence before asking, and ask before branch
  choices.
- Hard gates — always confirm regardless of persona: paid or provider model calls, sending data or
  private content off the machine, destructive edits, decisions the Traigent service is meant to
  return, and any missing fact the step truly requires.
- Recommend the next skill only after a result-bearing step (a run finishes, an analysis
  completes, a configuration validates) or an explicit decision point. Omit recommendations
  during setup or mid-walkthrough. Cap at 3 recommendations per response, each on its own line
  with a one-line eligibility reason (e.g., "traigent-analyze-results — ✓ run succeeded" or
  "traigent-optimize-run — ✓ config validated").
- Never weaken Traigent safety: dry-run before any paid run; get explicit approval before real cost
  or before any data leaves the machine; treat service-returned plans and next steps as
  authoritative. Never put the persona profile or any private content into telemetry, run metadata,
  experiment names, logs, or provenance files.
<!-- /INTERACTION_POLICY v1 -->
