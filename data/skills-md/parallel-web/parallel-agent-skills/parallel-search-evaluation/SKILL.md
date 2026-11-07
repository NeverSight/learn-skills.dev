---
name: parallel-search-evaluation
description: Use for search evaluation, a POC or bake-off, Parallel vs Exa/Tavily comparisons, SimpleQA/DeepSearchQA benchmarks, or diagnosing search evaluation results. For product selection use choose-your-parallel-api; for integration migration use migrate-to-parallel.
metadata:
  author: parallel
---

# Evaluate Parallel Search

Turn the user's workload into a reproducible end-to-end comparison. Deliver a runnable harness when implementation is requested, or an actionable plan when planning is requested. Reuse an existing harness before creating another one. Do not invent a Parallel CLI eval command.

For product selection without a benchmark, use `choose-your-parallel-api`; for replacing an existing search integration, use `migrate-to-parallel`. Use this skill to measure the resulting quality, cost, and latency.

## Start with the workload

Read the public [evaluation guide](https://docs.parallel.ai/search/evaluating-search), [Search best practices](https://docs.parallel.ai/search/best-practices), and [Extract best practices](https://docs.parallel.ai/extract/best-practices) before implementing requests. Check current [modes](https://docs.parallel.ai/search/modes) and [pricing](https://docs.parallel.ai/getting-started/pricing); record the documentation date and configuration rather than embedding price or latency promises.

Establish the application, question types, providers, existing agent/model, verified answers, and quality/cost/latency target. Infer these from supplied code and data; ask only for missing decisions that change the comparison. Prepare offline artifacts while credentials or a live-run budget remain unresolved. Use existing authorization for paid calls; otherwise establish scope and spend limits before execution. Never request keys in chat.

Choose the product that matches the application:

| Application | Evaluation boundary |
| --- | --- |
| User owns the agent loop | Search + Extract, including answer generation |
| One call should return a cited answer | Responses API |
| Schema-bound enrichment or asynchronous research | Task API |

Always set Search `mode` explicitly for REST requests: omitting it selects `advanced`, changing latency and price. Unless the user specifies otherwise, start with `fast` for interactive workloads or `advanced` for harder research, then test another relevant mode. The evaluation guide still recommends `basic`; record this discrepancy and the chosen rationale rather than silently inheriting that starting point. Honor workload constraints such as language support and endpoint availability. For Search MCP, consult its current routing and override rules: pin the mode for authenticated calls where supported; anonymous calls reject overrides, so record the actual server-selected mode or require authentication for a controlled mode comparison. Keep the model fixed within a comparison; a different model/mode pairing is a separate experiment.

## Build and freeze the comparison

Use [references/eval-contract.md](references/eval-contract.md) when creating dataset records, run manifests, traces, grading output, and reports. Resolve this reference relative to this skill's directory.

1. Prefer real production questions and independently verified answers. Match domain, wording, freshness, and task shape. Review synthetic labels before running. Pin question IDs and dataset version; separate pilot questions from held-out questions. Public benchmarks supplement this set and need a consistent policy for answer-key contamination.
2. Hold the model, research prompt, budgets, judge, and extraction policy constant across providers. Expose only the selected provider's search tool. Start with each provider's documented defaults and tool definition, including descriptions; change a setting only with evidence from the workload or pilot, and record the evidence and deviation in the manifest. Avoid arbitrary result caps or custom tool descriptions. If extraction differs as part of a provider stack, disclose that boundary. Keep gold answers and annotations out of agent prompts, query generation, and tool messages.
3. Have the model write an objective that restates the full information need with every relevant constraint, including entities, scope, dates, and source requirements. Pair it with focused keyword queries of 3–6 words each: one for a simple fact, up to three useful angles for richer questions. Do not duplicate the query text in the objective or copy the whole task into each query. Preserve result titles, URLs, and excerpts in the answering model's context. Use `/v1/search` and `/v1/extract` for new integrations; verify current request schemas rather than renaming old endpoints.
4. Default to multi-hop Search + Extract for applications; use single-hop only for an explicitly one-request benchmark. Fix total calls, deadline, retry policy, and spend bounds before dispatch. Use a fresh session per question, configuration, and repetition; reuse it across that trial's related Search and Extract calls.

Recommend a cost-parity comparison: align result count, content per page, product tier, and reasoning level where supported, and account for total Search/Extract/model cost including input and output tokens. Start with documented defaults as the baseline; any parity overrides need a recorded rationale and a separate configuration. Report requested and actual result counts and content volumes, residual mismatches, and settings that cannot be equated. Do not treat equal API-call counts as equal cost or imply parity when it was not achieved.

| Setting | Executor behavior |
| --- | --- |
| Single-hop | Allow exactly one Search API request, no Extract; disable tools for the final answer. Enforce the limit in code, including concurrent requests. Several keyword queries in one request still count as one call. |
| Multi-hop | Expose Search + Extract and allow evidence-driven follow-ups within the total budget. Dispatch independent calls from the same turn concurrently; reserve budget before dispatch, return results under their original call IDs, and preserve successes when siblings fail. |

Use the same research prompt across providers and settings; change tool availability and executor budgets separately. For public benchmarks, use the guide's research prompt and official grader where available. Record output-format overrides and label altered benchmark protocols as adapted evaluations.

## Pilot, grade, and interpret

Inspect a small fixed pilot: query quality, warnings, excerpt delivery, tool limits, concurrency, and trace completeness. Fix integration faults and rerun affected configurations; do not tune during a scored run. Freeze settings before evaluating held-out questions. Run each configuration at least three times and report variation.

Flag every failure to the user with affected trial IDs and impact: rate limits, HTTP errors, timeouts, partial results, token truncation, dropped results, and endpoint fallback (including `/v1` → `/v1beta`). Record each occurrence even if a retry succeeds. Never silently fall back or count a Parallel-side failure as a retrieval miss. Surface failures during execution and include their counts and trace references in the final report; preserve partial successes and the declared scoring denominator.

Grade final answers by task shape: factual correctness and citation support; list precision and recall; structured field accuracy; or an explicit research rubric. Require judge reasoning. For custom rubrics, rank honest inability to retrieve above confident misinformation. Hand-check at least 10% of judged trials, covering successes and failures. Keep citation audits separate from official benchmark scores.

Classify failures from traces: no search call, synthesis failure despite sufficient evidence, provider error, or retrieval miss despite a reasonable query. Do not attribute missing excerpts or other harness faults to retrieval quality. Distinguish account rate limits from provider capability.

Include failures and timeouts in primary results under the declared scoring policy. Bound retries and include all their time and cost. Report Search/Extract/model charges, tokens, calls, budget exhaustion, and search and end-to-end latency at p50/p95/p99. Time the whole task by wall clock, including query reformulation and answer generation; do not sum concurrent call durations. Cost per resolved task includes spend on unsuccessful trials; report it as undefined if nothing resolves.

Deliver the reproducible configuration, dataset and trace locations, grading rationale, failure breakdown, and quality versus cost/latency comparisons. Recommend configurations on the measured Pareto frontier that meet the user's targets, with uncertainty and workload slices. If calls were not run, label the deliverable as an unexecuted plan or harness and state what remains needed.

After results, propose 2–3 follow-up configurations tied to observed failures or bottlenecks: retrieval misses → `advanced`; thin excerpts → enable or increase Extract use; high latency → `fast`; high model-token cost → a smaller content budget. Change one factor per comparison, record the rationale, and use a new frozen manifest. Present these as proposals, not automatically launched runs; execute only when the user requests them within the authorized scope and spend.
