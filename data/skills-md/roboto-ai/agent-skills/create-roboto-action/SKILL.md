---
name: create-roboto-action
description: >-
  Generate a working, verified Roboto Action from a natural-language description of
  a data-processing job. Use this skill whenever the user wants to create, build, or
  scaffold a Roboto Action even if they only describe the task ("tag every dataset whose
  logs mention X", "extract video from these rosbags") without saying "action".
  Covers requirements decomposition, an ambiguity-resolving interview (skipped under
  --yolo), scaffolding, implementation, and verification by local dry-run
  invocation. Not for deploying or invoking actions that already exist, and not for
  general Roboto SDK questions.
license: MPL-2.0
compatibility: Requires the roboto CLI (authenticated) and Docker for local verification
argument-hint: <natural-language description of what the action should do> [--yolo]
---

Turn a description of a data-processing job into a Roboto Action that runs correctly the first time it is invoked, and that documents its own intent well enough for a later agent to extend it.

## What you need to run this

This skill does not know which agent is reading it, so it names the four capabilities it needs rather than assuming them:

- **Run shell commands** and read their output.
- **Read and write files.**
- **Hold a back-and-forth with the user.** Phase 1 is an interview.
- **Fetch a web page.** This is how you check SDK signatures against `docs.roboto.ai` before the project exists. Without it, say so and use the fallback described under Ground truth.

Nothing beyond that. No plugins, no external tool servers (such as MCP servers), no sub-agents, no symbol-level code intelligence. Where a step below reads like it names a specific tool, it names the capability; use whatever your harness provides for it.

`references/` throughout means the directory alongside this file. Read `references/action-api.md` and `references/authoring-rules.md` before Phase 1. They carry the API surface, the `action.json` schema, and the failure modes that Phase 1's questions exist to prevent.

## The request

The user's description of the action is the argument to this skill. Strip a `--yolo` flag from anywhere in it; what remains is the description. If the description is empty, ask the user what the action should do and stop; there is nothing to decompose.

`--yolo` suppresses the Phase 1 interview and nothing else. The preflight, the verification gates, the Phase 5 edit pass, and the recording of decisions all stand: every ambiguity resolved by judgment lands in `SPEC.md` with its rationale, so the user audits the decisions after the fact instead of before.

## Ground truth

The Roboto SDK moves faster than any file in this skill. Never write an SDK call from memory, and never write one from `references/action-api.md` alone. Confirm every signature, property, and `action.json` field you are about to use against a live source in this session. A hallucinated method name is the most likely reason a generated action fails on its first invocation.

The four sources below form a ladder, rung 1 the highest authority. Consult them in order, stopping at the first rung that can answer the kind of question you hold — rung 2, which prints no signatures, never settles a signature question:

| Rung | Source | How | When it wins |
|---|---|---|---|
| 1 | The SDK installed in the action's own venv | `.venv/bin/python -c "import roboto, inspect; print(inspect.signature(roboto.InvocationContext.get_input))"`, or read its source under `.venv/lib/python*/site-packages/roboto/` | Highest authority after Phase 2: it is the code that will run |
| 2 | The generated `DEVELOPING.md` | Read it in the project root | Rendered from the template on every scaffold, so it matches the project you just created. It explains the workflow, names SDK members, and links their reference pages, but prints no signatures, so it settles how to do something, never a signature's exact shape |
| 3 | `docs.roboto.ai` | Fetch the durable URLs listed in `references/action-api.md` | The pre-scaffold authority, and the source for worked examples |
| 4 | `references/action-api.md` | Read it | Lowest authority: a pre-scaffold map for running the interview, not a citation |

Before Phase 2 there is no venv, so rung 3 leads. After Phase 2, rung 1 leads.

If you have no way to fetch a web page, rung 3 is unavailable and rung 4 is a map written against an older SDK than the one that will run. Do not quietly fall back to it. Tell the user which pages you need (the durable URLs are in `references/action-api.md`) and ask them to paste the relevant sections, explaining that the alternative is writing SDK calls that may not exist. After Phase 2 this stops mattering: rung 1 is a local Python interpreter and answers most questions.

Check at least the following against a live source, since each is a place where a plausible-looking guess fails at runtime: the exact `InvocationContext` member you are calling, the `action.json` field names and their allowed values, and one worked example of the output surface the action writes through (dataset tags, file metadata, events, or output files).

The `roboto` CLI and the SDK in the venv are different artifacts at independent versions. The CLI is installed globally; the venv SDK is resolved from the version floor the generated `pyproject.toml` sets (a `>=`, not an exact pin) and is the code that runs inside the container. Rung 1 means the venv, never the CLI. Read the version that matters with:

```bash
.venv/bin/python -c "from roboto.version import roboto_version; print(roboto_version())"
```

`roboto.__version__` does not exist; reaching for it wastes a lookup. Record the version this command returns in `SPEC.md`'s verification section.

Where two sources disagree, prefer the higher one and mention the discrepancy in your final report so the user knows which surface you built against.

## Phase 0 — Preflight

Run this before the interview. Every check below guards a step that would otherwise fail after the user has spent time answering questions and you have written the whole action.

```bash
uname -s                                    # platform; fixes the Phase 4 pty form
command -v roboto                           # CLI on PATH
docker info                                 # daemon reachable, not merely installed
roboto --suppress-upgrade-check users orgs  # credentials valid; enumerates your orgs
```

Three of the results need more explanation than the comments carry:

- **`uname -s`** decides which `script` form Phase 4 uses. Settle it now.
- **`docker info`** must succeed, not just `command -v docker`. Local invocation builds and runs a container, so an installed-but-stopped daemon fails Phase 4.
- **`users orgs`** doubles as the credential check and the org inventory: it fails without valid credentials, and otherwise prints one JSON object per organization the user belongs to. If there is more than one, Phase 4 and Phase 6 both need `--org`; carry the list forward rather than rediscovering it. Do not read `~/.roboto/config.json` to check credentials; it holds a plaintext token.

`roboto actions init` downloads the project template from GitHub, so Phase 2 needs network access to GitHub. There is nothing useful to probe; tell the user it is a prerequisite when you report the preflight results.

If a check fails, stop and tell the user exactly what to install or run. Do not begin the interview.

## Phase 1 — Decompose and resolve

### Step 1: Decompose the description

Turn the description into a requirements table before asking anything. Each row is one testable behavior in the present tense: "tags the dataset when any log line matches the keyword", not "handles keywords".

Then classify each requirement:

- **Stated** — the description says it.
- **Implied** — the description's goal cannot be met without it, and only one reading is plausible. Record the inference.
- **Ambiguous** — more than one reading changes what gets built. These drive Step 3.

Do not pad the table with platform boilerplate. Logging setup, dry-run gating, and parameter validation are `authoring-rules.md` obligations that apply to every action; they are not requirements derived from this description.

### Step 2: Find the ambiguities

Walk these axes. Each is a decision that changes generated code, so an unresolved one becomes a guess baked into the action.

When an axis turns on a platform capability you are unsure of — whether a topic exposes a given field, what an SDK surface can write to, whether a trigger can pass the input shape the description implies — resolve it against Ground truth rung 3 or 4 before asking the user. Do not spend an interview question on something the documentation answers, and do not ask the user to confirm an API's behavior.

| Axis | What is undetermined | Consequence of guessing wrong |
|---|---|---|
| Input shape | Files, topics, or none? | Picks the scaffold variant and `requires_downloaded_inputs`; wrong choice means rewriting `main` |
| Input selection | Which files or topics — glob, RoboQL, whole dataset? | Determines whether a trigger can drive the action |
| Ingestion assumption | Is input already ingested into topics? | Un-ingested input makes `get_topic` raise (rule 8) |
| Message paths | Which columns of a topic does the logic read? | A missing column is a runtime `KeyError` (rule 9) |
| Output form | Files, tags, metadata, events, or a combination? | Decides which SDK surface the action writes through |
| Output destination | Input dataset by inference, or an explicit output dataset? | Multi-dataset input silently skips the automatic upload |
| Parameters | What must be configurable, required or optional, with what defaults? | A hardcoded threshold makes the action single-use |
| Secrets | Does it call an external service needing a credential? | Credentials must arrive as `roboto-secret://` parameters, never literals |
| Thresholds | Which numbers stand behind "high", "large", "anomalous"? | Unstated numbers are the most common silent guess |
| Invocation mode | Manual, event trigger, or schedule? | Shapes input selection and empty-input behavior (rule 7) |
| Scale | How large is the largest expected input, and how many? | Drives `compute_requirements` (rule 17) and `timeout`; an under-sized action fails partway through a long run |
| Dependencies | Third-party libraries, and system packages behind them? | An undeclared system package fails only in the container (rule 15) |
| Failure posture | Skip a bad input and continue, or fail the invocation? | Determines whether a trigger misfire pages someone |

Not every action has input. A smoke test, a template starting point, or a job that only calls an external service reads nothing from Roboto, and forcing it into the files-or-topics dichotomy produces an action that iterates over an empty collection for no reason. When the Input shape axis resolves to none, record these three consequences rather than rediscovering them later:

- The scaffolder still demands a choice; answer `1` (files). The choice only selects which example body `main.py` ships with, and you are replacing that body anyway.
- Set `requires_downloaded_inputs: false`, so no file is ever downloaded on the action's behalf even if an invocation happens to select some.
- `main` must not call `context.get_input()`, `context.input_dir`, or `context.dataset`. An action that touches none of them is valid under every invocation mode; state in `SPEC.md` that this one touches none, since that is why rules 7 and 12 do not apply.

Also settle the action name if the description does not imply one. It becomes the Roboto identifier and the directory name, so it should read as a verb phrase describing the job: `tag-high-cpu-intervals`, not `cpu-tool`.

### Step 3: Resolve

**Without `--yolo`:** interview the user. Where your harness offers a structured multiple-choice prompt, use it for the axes with a small fixed set of answers (input shape, invocation mode, failure posture, output form); otherwise ask in prose. Use free-form questions for values only the user holds — thresholds, topic and message-path names, dataset IDs, service endpoints. Ask, then wait.

Batch related questions rather than asking one axis at a time, and lead each with your own recommendation so the user can confirm rather than compose an answer. Carry anything the description already answered as a stated guess to confirm or correct, never as a settled fact.

When an answer will produce a fragile action, say so once with the concrete failure mode: a hardcoded threshold makes the action single-use; assuming ingestion makes it raise on raw uploads; failing the invocation on one unreadable file makes a trigger page someone nightly. Then record whatever the user decides.

Ask only what changes the build. Anything derivable from the description, the platform's defaults, or `authoring-rules.md` is not an interview question.

**With `--yolo`:** resolve every ambiguity yourself. Choose the option that keeps the action reusable and its failures quiet: parameterize rather than hardcode, prefer invocation-time input selection over a runtime query, tolerate empty and unreadable input rather than raising, and take the template's compute defaults unless a requirement needs more. Mark each such choice as a default rather than a requirement when you record it.

### Step 4: Confirm the plan

State, compactly: the action name, the requirements table, each resolved ambiguity with its resolution, and the file-by-file plan. Under `--yolo`, present this as what you are about to build and continue without waiting. Otherwise, get the user's go-ahead before writing files.

## Phase 2 — Scaffold

Never hand-write the project layout. Run the platform's own scaffolder so the generated tree, the shipped `DEVELOPING.md`, and the SDK version floor it pins stay consistent:

```bash
roboto --suppress-upgrade-check actions init <parent-dir>
```

`<parent-dir>` must already exist (the command errors out rather than creating it) and defaults to the current directory when omitted. Choose it deliberately: use the current working directory when it is empty or a scratch area; otherwise ask. Do not scaffold into a directory that already holds an unrelated project. The project is created in a subdirectory named after the action's slug.

The command wraps a cookiecutter template and reads four answers from stdin, in this order: action name; description; input data type, as a numbered choice (`1` = files that have been uploaded or ingested, `2` = topics created by ingestion) rather than the literal word; and whether to initialize a git repository. The third answer is the input-shape axis, and it selects the `files` or `topics` variant of `main.py` and sets `requires_downloaded_inputs`.

Answer the fourth question `y`. The project is a deliverable someone will change later, and the git repository is what makes the edit passes in Phase 5 reviewable as a diff rather than as a wall of new files. It is not an interview question.

Drive the command non-interactively by piping the Phase 1 decisions:

```bash
printf '%s\n' '<Action Name>' '<description>' '<1 for files, 2 for topics>' 'y' \
  | roboto --suppress-upgrade-check actions init <parent-dir>
```

Then, from the new project root:

```bash
./scripts/setup.sh
```

Read the generated `DEVELOPING.md` before writing any code. It is rendered from the template on every scaffold, so it, not `references/action-api.md`, is the authority on this project's workflow: how dependencies are declared, how `verify.sh` and `deploy.sh` behave, how local invocation is driven. Where the two disagree, follow `DEVELOPING.md`. It names SDK members and links their reference pages but prints no signatures; for a signature's exact shape, read the SDK installed under `.venv/` (Ground truth rung 1).

## Phase 3 — Implement

Before writing code, confirm the surface you are about to call. List every SDK member the plan depends on — each `InvocationContext` property and method, each domain-object method (`Dataset.put_tags`, `File.get_topic`, `Event.create`, `FilesChangesetFileManager.put_fields`), and each `action.json` field — and verify each against Ground truth rung 1, now that the venv exists, falling back to rung 3 for anything the installed source leaves ambiguous. Where a call needs a worked example rather than a signature, rung 3 is the place to find one. A handful of lookups here prevents a runtime `AttributeError`.

Write, in this order:

1. **`action.json`** — name, description, the parameters from Phase 1 with their `required` and `default` fields, `compute_requirements` sized per rule 17, `requires_downloaded_inputs` set per rule 6, and `timeout` in minutes when the Scale axis says the work outruns the platform default. Validate the shape against `ActionConfig` in `references/action-api.md`.

2. **`main.py`** — set the log level, parse and validate parameters, then the logic. Keep `main` an orchestrator: extract each decision worth testing into a module-level function taking plain values, in `main.py` for a small action or a sibling module for a larger one. Gate side effects on `context.is_dry_run` and log what a dry run would have done. Writing to `context.output_dir` is not a side effect for this purpose: dry run exists only on local invocation, which never uploads, so gating those writes would leave Phase 4 with nothing to inspect. Leave `src/<package>/bin/entrypoint.py` untouched.

3. **`pyproject.toml`** and **`Dockerfile`** — runtime dependencies, dev dependencies, and system packages, per rules 14–16. Keep the `roboto[analytics]` extra if the action reads topic data.

4. **`test/test_main.py`** — keep the shipped signature test and add tests for the extracted functions. No network; hand-build an `InvocationContext` on `roboto.testing.StubRobotoClient` only as a last resort after extraction has failed (rules 18–20).

5. **`SPEC.md`** — from `references/spec-template.md`. This is a deliverable, not a byproduct: it is where the requirements table, the resolved ambiguities and their rationale, the non-goals, the failure behavior, and the compute reasoning survive. Leave the verification rows pending; Phase 4 fills them.

6. **`README.md`** — replace the template's placeholder with what the action does, its parameters, its inputs and outputs, and how to invoke it. Point to `SPEC.md` for intent and `DEVELOPING.md` for the authoring workflow.

Apply every rule in `authoring-rules.md` that bears on the action. Rule 22 governs `SPEC.md` and `README.md`: the project documents itself, never the process that produced it.

## Phase 4 — Verify

Verification is the difference between a plausible action and a working one. Run both gates, from the project root.

If Phase 3 touched `pyproject.toml`, re-run `./scripts/setup.sh` first. It installs dependencies into `.venv`, and `verify.sh` runs `ruff` and `pytest` out of that venv against the editable install; a dependency that reached `pyproject.toml` but not the venv fails as an `ImportError` under `pytest`, which reads as a code bug.

```bash
./scripts/verify.sh
```

Fix what it reports and re-run until it passes. If `ruff` and the project's configured style disagree with something you wrote, change the code, not the config.

If the gate reports something in a file you never touched, do not hand-edit around it and do not treat it as a bug in your own work. Run `.venv/bin/ruff check --fix`, confirm the remaining diff is confined to your own files, and continue.

Then invoke locally, which builds the Docker image and runs against data in the user's Roboto org, exercising the network access forbidden to the unit tests (rules 18–20). Two constraints shape how you drive that command.

The command runs its container attached to a terminal, so from a non-interactive shell (which is what you have) it exits after building the image, before the container starts. Supply a pty. The two `script` implementations take their arguments differently, which is why Phase 0 recorded `uname -s`: BSD `script` on macOS takes the command as separate arguments after the typescript file, while util-linux `script` takes it as a single quoted string passed to `-c`.

```bash
case "$(uname -s)" in
  Darwin)
    script -q /dev/null \
      roboto --suppress-upgrade-check --log-level=info actions invoke-local --dry-run <args>
    ;;
  *)
    script -qec \
      "roboto --suppress-upgrade-check --log-level=info actions invoke-local --dry-run <args>" \
      /dev/null
    ;;
esac
```

Everything else about the invocation is unchanged; `script` only supplies the terminal. Its output carries a stray `^@` before the container's first log line; that is the pty, not the action.

The command also needs an explicit org when the user belongs to more than one organization, a condition Phase 0's org inventory already settled. Without `--org` it aborts and lists the candidates. A dry run creates nothing in an org, so pick one and say which you used rather than blocking on the question. Surface the choice in the final report, though: the same decision determines where a deploy lands, and that one is the user's to make.

Run the invocation from the project root, so the omitted action argument resolves to this project. Use the input-selection form matching Phase 1: `--dataset` with `--file-path`, or `--file-query` / `--topic-query`. The two groups are mutually exclusive, and only the first associates a dataset with the invocation, so an action that touches `context.dataset` raises rather than runs when verified under a query (rule 12).

`--dry-run` is safe because every side effect is gated on `not context.is_dry_run` (rule 3), so the run writes nothing; it is meaningful because the same rule requires logging what each gated write would have done, so the logs still demonstrate the action's decisions.

Unless the Input shape axis resolved to none, this gate needs a dataset in the org to read from. In order of preference: a dataset the user names; a dataset you find that matches the action's input assumptions; or, after telling the user, a scratch dataset you create and upload representative files to:

```bash
roboto --suppress-upgrade-check datasets create
roboto --suppress-upgrade-check datasets upload-files -d <ds_id> -p ./sample.log
```

When the action takes no input, none of that applies: a bare `invoke-local --dry-run` with no input selection is the correct gate, and hunting for a dataset to feed it verifies nothing. Do not create a scratch dataset an action will never read.

Run the gate more than once. One invocation exercises one path; the requirements table usually names several. At minimum, run the default path, one path with parameters overridden away from their defaults, and one that should fail: a parameter outside its valid range, or input the action is specified to reject. A validation rule you never triggered is a validation rule you never tested, and the failing run is the one that shows the error message an operator will read.

Read the log output rather than only the exit code. Confirm the action found its input, took the branch the requirements describe, and logged the side effects it would have performed. A clean exit that processed zero files has verified nothing; say so and fix the input selection.

Before invoking again, inspect `.workspace/output/` for the files the action wrote; every local invocation wipes the workspace at the start. The runtime seeds that directory with its own `.metadata/dataset_metadata_changeset.json` on every run, so the directory is never empty and that file is not evidence the action wrote anything. An action specified to produce no output files should show that stub and nothing else; count only what the action itself created.

If this gate cannot run — no credentials, no Docker, no obtainable input data — stop and tell the user what is blocking it and exactly what to run. Do not report an unverified action as working.

Record every run in `SPEC.md`'s verification table: the exact command, the input used, and what the log confirmed. One row per path exercised, including the failing one.

## Phase 5 — Edit pass

Read `references/edit-passes.md` and follow its five passes in order: API truth, naming and shape, comments, the verify script, and a final diff review. It carries the invariants that hold through every pass and the full protocol for each. Scope: the files you authored in Phase 3 (`main.py`, any sibling modules, `test/test_main.py`, `SPEC.md`, and the project `README.md`). Leave the template's own machinery alone: `bin/entrypoint.py`, `logger.py`, `scripts/`.

Fix what you find rather than listing it. Escalate to the final report only when a fix would contradict a decision the user made or would take the action beyond the scope `SPEC.md` records.

## Phase 6 — Hand off

Report:

1. **What the action does** — one paragraph, and the path to the project.
2. **Requirements coverage** — the Phase 1 table with each row's implementing symbol.
3. **Decisions made** — every resolved ambiguity, marked as either a user answer or (under `--yolo`) a judgment call, so the user knows what to audit.
4. **Verification** — what `verify.sh` and the dry-run invocation showed, with the input used. Name any gate that did not run and why.
5. **Edit pass** — what the Phase 5 passes changed, grouped by pass, and any rename that reached beyond the file it started in.
6. **Open items** — anything escalated from Phase 5, plus any interview answer you flagged as fragile.

Then give the deploy command without running it:

```bash
./scripts/deploy.sh [ROBOTO_ORG_ID]
```

Deployment creates or updates a real action in the user's organization and pushes an image to their registry, so it is theirs to trigger. `ROBOTO_ORG_ID` may be supplied as an environment variable or as the first argument; tell the user it is required when they belong to more than one organization, a fact Phase 0 established. If Phase 1 chose a trigger invocation mode, include the matching `roboto triggers create` command as a follow-on, also unrun.

Per-organization quotas apply to actions, hosted images, and active triggers, so a deploy can fail on a quota rather than on anything wrong with the action. Point the user at their organization settings for the current limits rather than quoting numbers.
