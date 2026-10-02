---
name: oracle
description: "Runs Oracle CLI in ChatGPT browser mode to ask an external cloud model for high-level reasoning, decomposition, review, or final evaluation. Use when an agent needs a second model to analyze complex tradeoffs, check a plan, evaluate a diff, debug a hard issue, or surface missing assumptions. Treat every Oracle run as a stateless, standalone request and send the prompt and required files explicitly because Oracle cannot access local machine resources or prior Oracle-run context unless they are provided."
metadata:
  tags: [oracle, second-model, reasoning, review, debugging]
---

# Oracle

Oracle sends a prompt and selected files to an external cloud model through ChatGPT browser mode. Treat Oracle as an externalized high-intelligence reasoning surface, not as an authority over local state.

Oracle cannot inspect the local filesystem, terminal state, running services, private databases, browser sessions, environment variables, or unprovided project files. Oracle only sees the prompt text and the files attached with `--file`. If the prompt or file set omits required facts, Oracle may infer missing premises and produce a plausible but wrong answer.

Each Oracle run is a stateless, standalone request. Do not assume a later Oracle run can see a previous Oracle prompt, answer, file attachment, local validation result, or any unprovided context. `--browser-keep-browser` preserves browser state, not reasoning context.

## Execution

Use browser execution with this command shape.

```bash
oracle --engine browser \
  --browser-manual-login \
  --browser-keep-browser \
  --browser-input-timeout 120000 \
  -p "<task>"
```

Add `--file` arguments when Oracle needs source files, documents, logs, plans, diffs, schemas, test output, or other evidence.

```bash
oracle --engine browser \
  --browser-manual-login \
  --browser-keep-browser \
  --browser-input-timeout 120000 \
  -p "<task>" \
  --file "src/target.ts" \
  --file "src/caller.ts" \
  --file "src/target.test.ts" \
  --file "docs/target-behavior.md"
```

If ChatGPT login is required, sign in through the displayed Chrome window and continue. `--browser-keep-browser` preserves browser login and window state after the run. It does not preserve the request context Oracle should use for reasoning.

Do not assume a newly released model name is already supported by Oracle's browser routing. Before adding an explicit `--model`, run the intended command with `--dry-run json` and confirm that the preview's `model` is the requested model. An unknown browser-model label may normalize to a different model instead of failing. If the intent is to keep whatever model is already selected in ChatGPT, use `--browser-model-strategy current` and verify the active model label in the browser.

## Workflow

1. Decide what judgment Oracle should provide: decomposition, option analysis, plan review, implementation review, debugging hypothesis, or final evaluation.
2. Gather the local truth needed for that judgment before writing the prompt.
3. Attach the smallest file set that contains the required truth.
4. Write a self-contained prompt that states the task, evidence, constraints, uncertainty, prior relevant Oracle output if any, local validation results if any, and required output format.
5. Run Oracle with the fixed browser command.
6. Evaluate Oracle's response against local evidence before adopting any conclusion.

Use Oracle for reasoning that benefits from another strong model: breaking down complex systems, finding weak assumptions, comparing alternatives, evaluating a plan against constraints, reviewing a diff, or checking whether a conclusion follows from the supplied evidence.

Do not use Oracle as a substitute for reading available files, running tests, checking logs, or verifying current local state. Perform those local checks first when they are necessary and feasible.

## Prompt Contract

Write the prompt so Oracle can answer correctly without hidden context.

Include:

- The exact question Oracle must answer.
- The project or domain context needed to interpret the evidence.
- The relevant current facts from local investigation.
- Confirmed facts and unconfirmed hypotheses.
- The files, logs, diffs, schemas, plans, or command outputs that are attached or quoted.
- Constraints that must not be broken.
- Known uncertainty, missing evidence, and areas where Oracle must not speculate.
- The expected output format and required level of strictness.

Ask Oracle to separate conclusions from assumptions when the answer depends on information not present in the prompt or attached files. Require Oracle to list missing information instead of filling gaps with speculation.

## Stateless Prompt Assembly

Build each Oracle prompt as a complete request packet. The prompt must be understandable even if Oracle has never seen the project, the previous request, or the previous answer.

For a first request, include:

- Objective: the decision, review, decomposition, or diagnosis Oracle must perform.
- Evidence map: the attached files and quoted command outputs Oracle should treat as evidence.
- Current facts: what local investigation has already confirmed.
- Open questions: what remains uncertain.
- Constraints: behavior, compatibility, security, scope, output, or process rules that must not be broken.
- Requested judgment: the exact reasoning task Oracle should perform.
- Output format: the sections Oracle must return.

For a follow-up or rerun, repeat the complete request packet and add:

- The prior Oracle conclusion that remains relevant.
- Local checks that validated, rejected, or refined the prior conclusion.
- New evidence gathered after the prior run.
- The revised question Oracle must answer now.

Do not write prompts that rely on implicit continuity, such as "continue," "same as before," "use the previous context," or "review it again" without restating the required context and evidence.

## Output Format

Prefer an output format that forces Oracle to expose its reasoning boundary.

Ask Oracle to separate:

- Premises used for the answer.
- Facts directly supported by the prompt or attached files.
- Missing information that prevents a stronger conclusion.
- Options considered.
- Recommended judgment.
- Risks and failure modes.
- Points the local agent must verify before adoption.

For reviews, require a strict verdict only when the supplied evidence is sufficient. For debugging, require hypotheses to include the evidence that would confirm or reject each hypothesis.

## Evidence Selection

Use `--file` for files, directories, or globs that Oracle must inspect.

- Example: `--file "src/target.ts" --file "src/caller.ts" --file "src/target.test.ts"`
- Example: `--file docs/behavior.md --file package.json --file tsconfig.json`
- Broad include: `--file "src/**"` only when the whole source tree is genuinely required.
- Exclude: `--file "!src/**/*.snap"`

Prefer precise evidence over broad attachment. Include the target implementation, callers, type definitions, tests, fixtures, generated contracts, configuration, schemas, plans, specs, and error logs when they define or constrain the behavior under review. Include command output in the prompt when the result matters and the output is not already contained in an attached file.

Attach evidence again when a later run still needs it. Do not assume Oracle can reuse files attached to an earlier run. If a prior Oracle answer matters to the new request, quote the relevant excerpt in the prompt or attach a local note that contains the exact prior answer and the local validation status.

Do not attach files merely because they are nearby. Do not attach secrets, `.env` files, credentials, private keys, tokens, or raw production data. If sensitive evidence is necessary, reduce it to the minimum redacted excerpt that preserves the relevant structure and facts.

## Evaluating Oracle Output

Treat Oracle's response as a reasoning artifact that requires local validation.

Before adopting Oracle's recommendation:

- Check whether Oracle used only facts present in the prompt or attached files.
- Check whether the answer can be derived from the current prompt and current attachments, without relying on unprovided context from another run.
- Identify assumptions Oracle introduced and decide whether local evidence supports them.
- Verify claims about code, APIs, data, tests, or behavior against the actual local artifacts.
- Separate useful decomposition or critique from unsupported factual claims.
- Reject or revise conclusions that depend on missing evidence, stale assumptions, or contradictions with local truth.

When Oracle exposes a gap in the supplied context, collect the missing evidence locally and rerun Oracle only if the additional reasoning is still useful.

## Result Integration

Use Oracle's output to improve the local decision, not to bypass responsibility for the decision.

Adopt an Oracle recommendation only after the local evidence supports it. If the recommendation is partly correct, keep the supported reasoning and discard unsupported claims. If Oracle's reasoning conflicts with local evidence, prefer the verified local evidence and document the unresolved point if it still affects the task.
