---
name: code2skill-review-source
description: Review Code2Skill request semantics against authorized source code, including source binding, cross-Tool handoffs, deterministic transformations, invocation chains, authentication, and attachments. 从授权源码独立复核 Code2Skill 请求语义。
---

# Code2Skill Source Review

Review whether the request semantics in an existing Code2Skill-generated result match the authorized source code. This Skill answers "how closely does the generated result match the source code?" It does not re-inventory all major goals, and it does not treat the generated result's own passing tests as evidence of correctness.

The complete Chinese version is available at [references/SKILL.zh-CN.md](references/SKILL.zh-CN.md). Follow the user's language for final replies, review conclusions, and all user-facing content.

If you first need to determine whether the major goals are complete and whether the standard paths can be completed, use `code2skill-review-flow`. The two Reviews can run separately and do not depend on each other.

This Skill is read-only, offline, and source-first by default. It is not a second heavyweight audit process. It returns only concise, actionable findings and does not generate a Canonical Contract, evidence matrix, review report, or other deliverable files.

## Inputs and boundaries

Before starting, identify:

- the path to the generated package under review;
- the source roots explicitly authorized by the user;
- the Skill, major goal, Tool, or capability scope under review;
- whether the user has also authorized fixes; remain read-only unless this authorization is explicit.

Review only the default output of `code2skill-generate`. If you encounter an advanced-validation format, a legacy version, or an unrecognized directory, explain that this process does not apply rather than forcing it onto the artifact.

Search only the authorized source roots. When a client or Consumer exists, focus on the business invocation it actually triggers and the final invocation construction. When no client exists, begin from the public API, RPC, Service, message, or task entry point specified by the user. When necessary, verify public Request/Response definitions, service/method identity, message destination/key, task payload, authentication headers, or upload interfaces, but do not descend into backend Services, databases, downstream message processing, approvals, or complete business validation.

By default, do not:

- call real business interfaces or write interfaces;
- install, register, or deploy MCP for the purpose of review;
- scan the entire machine for unauthorized dependencies or backend repositories;
- modify the generated package, source code, or tests;
- write temporary deductions into review documents that remain in the repository.

When the user explicitly authorizes fixes, you may correct the generated package and add targeted offline tests. Authorization to fix does not authorize calls to real interfaces.

## Keep the review independent

Prefer an Agent that did not participate in generation, or a new session. Give the Reviewer only the source scope, generated-package path, and review targets. Do not present the Producer's field explanations, generation conclusions, or test expectations as facts.

When only the same Agent is available, perform a cold review:

1. Treat the current Function, Skill text, and test assertions as unverified hypotheses.
2. Re-derive the target capability's field sources, transformations, and terminal business invocation from source code first.
3. Form a temporary comparison in working memory; do not write it into the repository.
4. Then compare it with the Function, MCP, and Skill.
5. Only then read or run the generated package's tests.

Do not infer the expected source behavior from the current Function implementation. The README, Feature Context, Tool descriptions, mock returns, and green tests are all objects to verify; they are not source evidence.

## Review process

### 1. Identify the capability under review with minimal reading

First read `package.json`, the directory structure, and the target Skill's frontmatter/title only to identify the package type, review target, and related Tools. Do not trust detailed workflow text or test expectations at this stage.

This Skill does not re-enumerate every major goal from source code and does not output whole-scope states of `complete`, `basically usable`, `blocked`, or `unverified`. If completeness of the scope is itself in question, hand it off to `code2skill-review-flow`.

### 2. Re-derive request semantics from source code

From the target entry point, find the real API wrapper, RPC stub, Service method, message Producer, or task-submission point. Trace the data flow to the final invocation target and operation, parameters/message/task payload, runtime context, synchronous return, errors, publication receipt, or task ID. In HTTP scenarios, these appear as method, URL, query, header, body, or multipart.

Record only this minimal comparison in working memory:

```text
business meaning
→ value source
→ page, client state, or preceding response
→ deterministic transformation
→ final invocation field (method/URL/query/header/body/multipart for HTTP; service/method/arguments for RPC; destination/key/payload for messaging)
→ owning goal and conditional branch
```

At minimum, distinguish these value sources:

- user input;
- client-side constant;
- preceding interface response or a dynamic option selected by the user;
- client-computed or transformed result;
- identity, authentication, or attachment injected by the Host;
- optional, conditionally present, or genuinely unknown value.

When evidence cannot be found, record the specific missing module or symbol. Do not guess and do not expand into unrelated source code.

### 3. Check five categories of source consistency

#### Field provenance and cross-Tool handoffs

- For fields with the same name, determine their source, assignment process, and final purpose separately.
- A query filter value, entry type, user-selected value, and final write value must not be reused directly merely because the API fields have the same name.
- After a preceding Tool's response is selected, filtered, or mapped, the next Tool should receive the value it actually needs.
- When the client spreads, merges, or forwards multiple fields or the entire object from the selected record into a downstream request, verify that the Function preserves the selected-record input, source-defined merge order, and explicit override relationship. Do not check only whether an ID exists.
- Verify that the Skill's standard example actually uses the selected-record handoff exposed by the Function. If the source proves only the whole-record path and does not yet prove ID-only equivalence, the example must not hide whole-record support as an optional entry point that nobody would discover.
- Public Function/MCP parameters should use clear business names and map back to the actual API fields internally.
- Do not freeze dynamic options into a one-time sample enumeration.

Focus on comparing value provenance in source code with the values that the generated package asks the Agent to provide, not merely on comparing field names.

#### Deterministic request transformations

Check all source logic that changes a wire value, including:

- fixed time concatenation, time zones, and ISO/date formatting;
- explicit conversions among numbers, strings, booleans, and null-like values;
- array joining or splitting;
- removal of display prefixes or suffixes;
- field renaming, constants, and source-proven defaults;
- HTTP: query encoding, header assembly, and multipart fields;
- RPC: service/method selection, argument order, naming/wrapping/serialization;
- messaging/tasks: destination/key/payload construction, partition/routing keys, and task names;
- in-application Service: DI-container lookup and transaction/interceptor context injection;
- conditional addition or removal of invocation fields.

Deterministic transformations made explicit by the source should be reproduced reliably by the Function rather than requiring the Consumer Agent to guess each time. When the same business value enters multiple downstream invocations, verify the deterministic transformation and final wire representation separately at each use site; do not assume that different invocation sites use the same representation. If an upstream value is deterministically rewritten by alias or value normalization before it reaches the page, first verify the normalization itself and the normalized result used by each downstream invocation; do not treat the upstream raw representation as a usable downstream value. If a public input accepts a business value, the Function performs the transformation. If it accepts an already-transformed wire value, the Function, MCP, and Skill must all say so consistently.

#### Each goal's own invocation chain

- Each Skill describes only the Tools in the source invocation chain for its current goal.
- Shared queries, prechecks, or submission capabilities do not automatically become mandatory steps for every Skill.
- Conditional steps bind only to goals or branches proven by source code.
- A Skill must not turn page-display order into an unavoidable Workflow.

This section checks whether the selected goal's invocation chain is accurate. It does not support a claim that the entire goal scope has been covered.

#### Bounded tracing of critical imports

Continue tracing only imports that affect:

- API request construction;
- request-field transformations;
- authentication headers, public identity, or tenant injection;
- attachment credentials, upload requests, URL generation, and downstream field binding.

Do not expand pure UI, styling, or state utilities unrelated to requests. When critical implementation lies within the authorized source, read enough to reconstruct the request. When it cannot be resolved, identify the specific module or source gap.

For attachment chains, check only the source-proven business portion:

```text
trusted attachment path or reference supplied by the Host
→ business upload credential
→ actual upload invocation
→ business URL
→ downstream invocation field
```

Code2Skill is not responsible for chat integration, file reception, downloading, or a generic Host sandbox, and it must not instruct the Agent to guess local paths.

#### Runtime target and integration configuration

- Distinguish environment configuration in source code from Function runtime configuration. Business-service integration configuration belongs to Host deployment configuration, not user business input.
- A business API base URL must not become a public Tool parameter. Integration configuration such as an RPC client, Broker connection, or runtime context must not become a public Tool parameter either, and it must not default back to test, staging, or production domains found in source code. Stop before invocation when required configuration is missing.
- Environment addresses discovered in source may appear in `MCP-SETUP.md` as deployment references, but this does not justify claiming that any environment has been configured, connected, or verified.
- Do not misreport a fixed endpoint defined by a public protocol, or an object-storage, callback, or presigned address returned by the backend at runtime, as a static business base URL.

Classify a hidden default configuration that would send the current goal to the wrong environment or service as `P1`. Classify a setup that may currently work but depends on the Producer environment, a fixed test domain, or integration configuration temporarily supplied by the Agent as `P2`.

### 4. Compare the Function, MCP, and Skill

Compare in this order:

1. Does the Function construct the final business invocation according to source code?
2. Does MCP expose the same Function and public semantics directly and permissively?
3. Does the Skill accurately describe the current goal's invocation chain, dynamic information, and stop conditions?
4. Are all three consistent about field provenance, transformations, authentication, runtime integration configuration, and attachment prerequisites?

Inspect a Schema only when it would block or alter the invocation chain. Do not require strict enumerations, strict output Schemas, or duplicated backend business validation. Real responses, common type variations, and business decisions remain with the Consumer Agent and backend.

### 5. Tests are regression tools only

Read existing tests only after completing the source derivation and artifact comparison. Green tests prove only that the implementation matches the test author's expectations; they do not prove that those expectations came from source code.

You may run dry-run or mock tests that are confirmed not to access real environments, but do not install, register, or deploy MCP for review. When the user authorizes fixes, derive new tests from this review's source analysis and cover the affected final business invocation or handoff. Do not expand them into a combination matrix for every field, status code, or business rule.

The minimal counterexample test for selected-record handoff uses two anonymous records with different field values. Select each record and construct the downstream invocation; verify that the second invocation retains no fields from the first selection and that it follows the source-proven override order. If the Function already supports whole-record handoff and the upstream result exposes it, but the Skill example merely omits that usage, this is usually `P2`. Classify it as `P1` only when the generated package cannot carry record information required to form the terminal business invocation, or when it will necessarily construct the wrong invocation.

## Output conclusion

Reply directly in the current session; do not create a review file. Give the source-consistency conclusion first, then list findings by severity:

- `P1`: necessarily causes the selected goal to form an incorrect request, omit a required capability or handoff, or incorrectly add a mandatory step;
- `P2`: may currently work but depends on Agent guesswork, implicit formatting, or a non-portable prerequisite, so it is not stable enough;
- boundary note: the authorized source is insufficient to confirm the point; do not disguise it as either a defect or a pass.

For each finding, include the affected goal or Tool, source location, generated-package location, actual difference, request impact, and smallest repair.

If no issue is found, say only that no difference was found in the five categories of request semantics above within the current authorized scope. Explicitly state that real interfaces were not verified, backend business acceptance was not verified, and passing tests do not mean end-to-end usability. Do not present this Skill's result as a whole-scope main-flow completion conclusion.
