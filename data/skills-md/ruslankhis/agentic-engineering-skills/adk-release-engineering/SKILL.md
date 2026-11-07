---
name: adk-release-engineering
description: "Design, implement or audit the release lifecycle of a Python Google ADK agent: prompt and configuration versioning, pinned model and judge IDs, evaluation gates in CI with threshold, repeat and cost policy, model-version migration with re-baselining, staged promotion and joint rollback of prompt, model, tool schema and secrets, and refreshing eval sets from production samples. Use when a release, CI gate, model deprecation notice, canary, rollback or stale eval set is the concern. Do not activate for a first deployment or packaging (deploy-adk-on-google-cloud), writing eval cases or the iteration loop (adk-agent-evaluation), choosing model settings (adk-model-and-output-contracts), prompt wording (adk-agent-instructions) or production monitoring (adk-agent-observability)."
license: MIT
metadata:
  author: Ruslan Khissamiyev
  source-book: Agentic Engineering
  source-chapter: "cross-framework"
  verified-against: "google-adk 2.8.0 source and adk-python main CHANGELOG, 2026-10-07"
  version: "2026.10.28"
---

# ADK release engineering

Make every change to an ADK agent a traceable release: a prompt version, a pinned model ID, a pinned judge ID, a tool schema hash, an eval-set hash and a deploy reference that move together and roll back together. Deliver the smallest change to an existing project or a review with observable findings. Keep pins unchanged unless a version decision is requested; keep every ADK claim tied to the pinned version.

This skill complements Google's `agents-cli` deploy skill (three-stage pipeline, Cloud Run traffic rollback, eval run/grade/compare; v1.11.0, re-read 22 October 2026), which has no prompt versioning, model-migration or eval-gate-in-CI guidance. Hand first deployment, packaging and ownership journals to deploy-adk-on-google-cloud; eval case design and the measured iteration loop to adk-agent-evaluation; model settings and the lifecycle table to adk-model-and-output-contracts; prompt text to adk-agent-instructions; sampling and alerting mechanics to adk-agent-observability.

## Inspect before choosing a mode

1. Record the pinned `google-adk` and `google-genai` versions. Behaviour below is for **2.8.0**; [compatibility](references/compatibility.md) lists what changed through 2.11.0 and which hosting features are Pre-GA.
2. Inventory every release reference: model IDs (agent, fallback, judge), prompt sources (constants, `instruction=` literals, `prompts/` trees, any registry), tool declarations, eval sets (`*.evalset.json`, `*.test.json`) and eval configs (`test_config.json`, `criteria`), Dockerfiles, Cloud Build and GitHub workflows, deploy commands, requirement pins and secret references. Classify each model ID as **pinned** (dated or stable ID) or **alias** (`-latest`, `-preview`, `-exp`, or the unset ADK default). An alias is a release event you did not schedule.
3. Run the inventory helper with an available Python 3.11+ interpreter ([interpreters](references/operating-rules.md#helper-scripts-and-interpreters)) after resolving `SKILL_DIR` to this skill's directory. It reads source and manifests only; it never imports the project, calls a provider or prints prompt text (hashes only).

```bash
python "$SKILL_DIR/scripts/inventory_release_refs.py" --project .
```

The output is a release-manifest skeleton (components with version, hash or `unknown`) plus signals: judge model unset, set to `gemini-2.5-flash` or set to an alias (`JudgeModelOptions.judge_model` defaults to `gemini-2.5-flash` in 2.8.0, a model Google now serves only to prior users), alias model IDs, dynamic prompts, `latest` secret versions, legacy `.test.json` eval files, eval sets without a config, eval usage in tests, and deploy commands present. Exit 3 means a partial scan; fill `unknown` fields by hand. The helper reads ADK's own eval assets (`*.evalset.json`, `*.test.json`, `test_config.json`); an Agents CLI project's `tests/eval/eval_config.yaml` and `tests/eval/datasets/` are listed in the manifest by hand with their hashes. The sibling `audit_model_config.py` in adk-model-and-output-contracts owns lifecycle status; pass its table with `--lifecycle` when a status column is wanted.

4. Note who owns what: who edits prompts, who deploys code, who approves traffic changes, who pays for eval runs. Ownership decides git versus registry ([versioning](references/versioning.md)) and the approval points below.

## Choose the relevant mode

| Mode | Read | Produce |
| --- | --- | --- |
| (a) Version prompts and config, keep a changelog | [versioning](references/versioning.md) | Prompts in git by default, content hashes in the manifest, `PROMPT_CHANGELOG.md` rows from [the template](assets/PROMPT_CHANGELOG.md), a registry only when prompt and code owners differ |
| (b) Eval gate in CI | [CI eval gates](references/ci-eval-gates.md) | Three tiers (deterministic per PR, bounded live on label or merge, judge nightly); threshold, repeat, cache and cost ceiling policy; `check_eval_results.py` from adk-agent-evaluation as the strict gate; NOT RUN reported as a failure to produce evidence, never as a pass; [workflow asset](assets/eval-gate.github-actions.yml) |
| (b2) Capability gate for pull requests a coding agent wrote | [CI eval gates](references/ci-eval-gates.md), the capability-gate paragraph, and `adk-agent-security`'s validation reference for the CI steps | The security inspector run on base and head with `--compare`, a code-owner review label for any listed change, agents-shipgate at most advisory |
| (c) Model migration | [model migration](references/model-migration.md) | Deprecation calendar check, side-by-side on the frozen development set with the judge pinned, holdout once, token, latency and cost deltas, go/no-go record from [the checklist](assets/model-upgrade-checklist.md) |
| (d) Staged promotion and rollback | [staged rollout](references/staged-rollout.md) | Cloud Run tagged revision at 0% then stepped traffic; Agent Runtime revisions and manual traffic split (Pre-GA); shadow or A/B sample design; rollback bundle = image digest + prompt version + model ID + tool schema hash + secret versions |
| (e) Production to eval refresh | [production feedback](references/production-feedback.md) | Sampled traces reviewed into cases, freshness expiry per case, holdout replenished; sampling mechanics handed to adk-agent-observability |
| (f) Review | All of the above as needed, plus [validation](references/validation.md) | Findings with file and line, each tied to a source-verified behaviour or a dated vendor page, with the check that would prove the fix |

Modes compose. A deprecation notice is (c) then (d) then a changelog row in (a). A flaky CI gate is (b) first; if the flakiness follows a model alias, (c).

## Apply the release contract

- **One release unit.** ADK version, prompt version and hash, agent model ID, judge ID, tool schema hash, eval-set commit or hash, image digest or Agent Runtime revision ID, and secret version numbers are recorded together in the manifest for every release. Rollback restores the whole unit; a previous image with a new prompt from a registry, or an old prompt against a new model, is a new, untested combination.
- **Pins over aliases.** Use stable or dated Gemini IDs. Google logs alias traffic under the concrete model and moves aliases without notice; the Vertex lifecycle page (2026-10-07) promises at least 12 months of availability after release and that retirement dates never move earlier, so a pinned ID gives a schedule and an alias gives a surprise. The ADK default model (`gemini-3.5-flash` in 2.8.0) is a pin you did not choose: set `model=` explicitly.
- **The judge and the user simulator are dependencies.** Pin `judge_model` and `num_samples` in the eval config and the simulator model in scenario configs, and record them in the changelog. Both default to `gemini-2.5-flash` in 2.8.0 and still on main (commit ed76f94, 2026-10-21), a model that retired on Vertex on 2026-10-20 (model versions page updated 2026-10-21, read 2026-10-22; listed replacements `gemini-3.8-flash` or `gemini-3.5-flash-lite`) and is limited to prior users on the Gemini API, so an unpinned judge on the Vertex route is already failing, not merely retiring; ADK 2.2.0 moved the agent default off 2.5 and left the judge default alone. The docs examples use `gemini-flash-latest`, an alias. Changing the judge re-baselines every judge metric; do it as its own release with a side-by-side on the frozen development set.
- **A gate must fail by exit code.** `adk eval` prints "Tests failed: N" and exits 0 in every release through 2.12.0; main commit c2ff634 (2026-10-15, in no tag on 2026-10-22) changes it to `sys.exit(1 if total_failed or not eval_run_summary else 0)`, and there is still no `--num_runs` or pass threshold below 100% (`cli/cli_tools_click.py`, read 2026-10-22). On the pinned version run one deliberately failing case and record the exit code before trusting it; keep the pytest gate primary either way. Gate on `AgentEvaluator.evaluate` in pytest (it writes the CSV, then `assert not failures`), on adk-agent-evaluation's `check_eval_results.py` over that CSV, and on `adk conformance test` in replay mode, which does exit non-zero on mismatches.
- **Deterministic in the gate, judges on a schedule.** Gate pull requests on `tool_trajectory_avg_score`, `response_match_score`, scripted-model tests and conformance replay. Run judge metrics nightly or on a label, with majority vote (`num_samples`) and the judge pinned. Efficiency metrics (2.10.0 and later: tool calls, inference calls, tokens, duration) are informational and reject thresholds; track the deterministic counts as trend lines across releases and treat wall-clock as context.
- **Flakiness is a signal.** Keep the case. Controls in order: `num_samples` majority vote on judge metrics, `num_runs` repeats with a recorded pass rate, `random_seed` in environment simulation for mocked tools (`tools/environment_simulation`, 2.8.0), trajectory `match_type` and rubric criteria. When the flake is a different but correct order of calls, loosening `match_type` is not the control: grade the end state and the effective mutations instead (adk-agent-evaluation's evaluation-design reference, "Grade the end state, not the path") and gate on the unbiased pass^k over repeated trials. On Gemini 3 leave temperature at 1.0 (adk-model-and-output-contracts) and prefer these over lowering temperature.
- **Migration is a re-baseline, not a swap.** Follow Google's playbook: code regression tests, offline model-performance regression on the golden set plus online comparison, and load tests; repeat every evaluation done since launch; evaluate RAG, tool and chain components independently; expect token counts to change.
- **Promotion is a traffic change.** Deploy with no traffic, test the tagged URL or revision, step traffic up, and keep the previous revision ready. In-flight requests complete on the old revision during a Cloud Run migration. On Agent Runtime (Pre-GA) set a manual split before the first update, size instances for two warm revisions, and query the candidate revision directly before it receives traffic.
- **Eval sets expire.** Give each case a freshness date and a drift mode (dataset, tool API, prompt, retrieval corpus, user distribution, step compounding). Replace expired cases from reviewed production samples; new production failures become CI cases.

## Permissions and data boundaries

<!-- shared:consequential-operations-brief -->
Inspection is read-only, and code generation authorises no deployment, paid
call or live test. Before any consequential operation (an API, billing or
quota change, a billable resource, a secret, IAM, a data migration, a
deployment, a deletion, or a paid or destructive test), read
[consequential operations](references/operating-rules.md#consequential-operations),
present the exact scope and limits, obtain explicit approval and end the turn
to wait for it. Cleanup is a separate confirmed operation on resources this
workflow created.
<!-- /shared:consequential-operations-brief -->

For a release, present the exact project, service or Agent Runtime resource, revision, traffic percentages, eval set, case count, repeat count, model and judge IDs and a cost ceiling, then obtain approval before: changing traffic, deploying to production, running paid eval cohorts, rotating or re-pinning secrets, or archiving revisions (archived Agent Runtime revisions cannot be restored). Reuse approval already given for that exact scope. Keep prompt text, traces and secret values out of manifests, changelogs, CI logs and this skill's outputs; record hashes and version numbers.

## Validate and finish

Read [validation](references/validation.md). Observable without a live model: the manifest round trip (every component has a version or hash, none `unknown` at release time), the gate's NOT RUN behaviour (an empty CSV or a skipped job fails the check), the changelog row for the release, and a rollback rehearsal in a non-production target that restores the whole unit. Report what was inspected, which tier ran, and what remains unverified. Record every URL with its page date; lifecycle dates and Pre-GA surfaces change faster than this skill.

<!-- shared:evidence-labels-brief -->
Label each result with its tier (`offline`, `local`, `live` or `release`) and
outcome (`pass`, `fail`, `blocked` or `not run`) as
[evidence labels](references/operating-rules.md#evidence-labels) defines them;
earlier, vendor and documentation-only results are `historical`,
`vendor-measured` or `guidance`, never this session's evidence.
<!-- /shared:evidence-labels-brief -->

Independent community project; not affiliated with or endorsed by Google.
