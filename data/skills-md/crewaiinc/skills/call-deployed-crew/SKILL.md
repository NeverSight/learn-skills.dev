---
name: call-deployed-crew
description: "Calling a crew or flow deployed on CrewAI AMP over HTTP: the bearer token and deployment URL, GET /inputs, POST /kickoff with the {\"inputs\": {...}} body, which input keys are required ({placeholder} tokens), polling GET /status/{kickoff_id} with a deadline and backoff, terminal states and where the result lives, webhooks, POST /resume, slow first calls, and writing crews that stay correct when they are kicked off repeatedly or concurrently. Use when writing a client, script, backend or frontend that calls a deployed crew, when a kickoff returns 422 \"Missing inputs: ...\", when a status poll never ends, says \"NOT FOUND\" or the result field is empty, when /resume returns 422 for executionId, when a run's prompt shows another run's data, or when the user pastes a kickoff_id, a /kickoff curl, or 'Template variable ... not found in inputs dictionary'."
---

# Call a Deployed Crew

How to call a crew or flow that runs on CrewAI AMP from your own code, and how to write the crew so those calls stay correct.

Verified against crewai 1.15.22 and 1.15.23 on 2026-10-01.
Live-tested on CrewAI AMP and real LLMs on 2026-10-01.
Run `crewai version` first; if the major/minor differs, re-check the version-sensitive rows with the `ask-docs` skill.

---

## 1. The contract on one screen

Every deployment has its own base URL (`https://<your-deployment>.crewai.com`) and bearer token, both shown on the deployment's page in the AMP dashboard (Status tab). `crewai deploy status` prints neither. All calls send `Authorization: Bearer <token>`.

| Call | Body | Success response (live) | Docs |
|---|---|---|---|
| `GET /inputs` | - | `{"inputs": ["audience", "topic"]}` | [GET /inputs](https://docs.crewai.com/en/api-reference/inputs) |
| `POST /kickoff` | `{"inputs": {"topic": "...", ...}}` plus optional siblings (section 4) | `{"kickoff_id": "<uuid>"}` | [POST /kickoff](https://docs.crewai.com/en/api-reference/kickoff) |
| `GET /status/{kickoff_id}` | - | run state, progress, result (section 5) | [GET /status](https://docs.crewai.com/en/api-reference/status) |
| `POST /resume` | see section 5 - verify the body on your deployment | `{"kickoff_id": "<new uuid>"}` | [POST /resume](https://docs.crewai.com/en/api-reference/resume) |

Use `GET /inputs` as the readiness check; `GET /` may return `404`.

Responses to expect (handle the documented codes too - [API introduction](https://docs.crewai.com/en/api-reference/introduction)):

| Request | Live response |
|---|---|
| Wrong token | `401 {"detail":"Invalid or missing authentication credentials"}` |
| No `Authorization` header | `401 {"detail":"Not authenticated"}` |
| Crew kickoff with a required key missing, `{"inputs": {}}`, `{}` or a bare body | `422 {"detail":"Missing inputs: audience, topic"}` - a plain string, not `details.missing_inputs` |
| Body that is not valid JSON | `500 Internal Server Error` |
| `GET /status/<unknown id>` | `200` with `"state": "NOT FOUND"` - not `404` |

```bash
export CREWAI_DEPLOYMENT_URL="https://<your-deployment>.crewai.com"
export CREWAI_DEPLOYMENT_TOKEN="<your-bearer-token>"

curl -s -H "Authorization: Bearer $CREWAI_DEPLOYMENT_TOKEN" "$CREWAI_DEPLOYMENT_URL/inputs"

curl -s -X POST "$CREWAI_DEPLOYMENT_URL/kickoff" \
  -H "Authorization: Bearer $CREWAI_DEPLOYMENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"inputs": {"topic": "AI agents", "audience": "engineers"}}'

curl -s -H "Authorization: Bearer $CREWAI_DEPLOYMENT_TOKEN" \
  "$CREWAI_DEPLOYMENT_URL/status/<kickoff_id>"
```

Rules:
- Keep the URL and token in environment variables or a secret store. Never hard-code the token, commit it, log the `Authorization` header, or ship it to a browser - call the deployment from your backend.
- The dashboard shows an organization-level **Bearer Token** and a **User Bearer Token** with narrower permissions. Use the narrowest one that works for the integration.

---

## 2. Required inputs come from `{placeholder}` tokens

The keys a crew needs are the `{name}` tokens in its task `description` / `expected_output` and its agent `role` / `goal` / `backstory`. `GET /inputs` lists them for the deployed version. Read the keys from `/inputs` (or from your code) - never guess them.

Locally, `Crew.fetch_inputs()` is crewai's own scan of the same fields:

```python
from crewai import Agent, Crew, Task

agent = Agent(role="{topic} researcher", goal="Explain {topic}", backstory="Writes for {audience}.")
task = Task(description="Research {topic} for {audience}.", expected_output="A summary of {topic}.", agent=agent)
print(sorted(Crew(agents=[agent], tasks=[task]).fetch_inputs()))  # ['audience', 'topic']
```

What crewai does with the inputs it receives (verified locally on 1.15.22-1.15.23):

| You send | What happens |
|---|---|
| Every placeholder key | Values are substituted into agent and task text before the first LLM call |
| A placeholder key missing | `ValueError: Missing required template variable 'Template variable 'audience' not found in inputs dictionary' in description` - raised before any LLM call |
| An extra key with no placeholder | Silently ignored; it never reaches a prompt |
| No inputs, or `inputs={}` | Locally: **no error** - interpolation is skipped and the literal text `{topic}` reaches the model. A deployed crew rejects it with `422` (section 1) |
| int / float / bool / list / dict values | Stringified with `str()` - locally, and on a live deployment (`"audience": 3` produced `AUDIENCE=3`). The API documents every input value as a string - send strings to a crew (flows: section below) |

Consequences:
- Validate the request against `/inputs` in your client before calling `/kickoff`, and send every key. Do not rely on an empty-inputs run failing loudly - it does on AMP, not when you call `kickoff()` yourself.
- A literal JSON example inside a prompt (`Reply like {"title": "..."}`) is not interpolated, but `fetch_inputs()` reports `"title": "..."` as an input name. Any input list derived from braces will ask for it. Put output structure in `output_pydantic` / `response_model` instead of a JSON sample in the text.
- Send dates as ISO 8601 strings and structured values as JSON strings, and parse them inside the crew.

**Flows are different.** A deployed flow's `GET /inputs` lists the fields its state model declares - `{"inputs": ["topic", "count", "id", "history"]}` for a test model that declared `id` itself; a model that leaves `id` to the Flow does not list it (see the **build-flow** skill) - and none of them is required: a flow kickoff with `{"inputs": {}}` returned `200` and ran on default state. Send only the fields you mean to set, with the JSON types of the state model (a list as a list - `"[]"` as a string made the run `FAILED`), and never send `id` (section 3).

---

## 3. The kickoff body: `inputs` is a wrapper

| Bad | Good |
|---|---|
| `{"topic": "AI agents", "audience": "engineers"}` | `{"inputs": {"topic": "AI agents", "audience": "engineers"}}` |
| `{"inputs": {"topic": "...", "meta": {...}}}` | `{"inputs": {"topic": "..."}, "meta": {...}}` |
| `{"inputs": {"id": "<previous-kickoff-id>", "topic": "..."}}` (flows, deprecated) | `{"inputs": {"topic": "..."}, "restoreFromStateId": "<previous-kickoff-id>"}` |
| Retrying `POST /kickoff` after a read timeout | Treat it as "maybe started"; look for the run before sending another kickoff |

What a bare body does, live: a **crew** answers `422 {"detail":"Missing inputs: audience, topic"}` (the same as sending no inputs). A **flow** answers `200`, ignores the top-level keys and runs on default state - nothing tells you the values were dropped.

---

## 4. Optional fields beside `inputs`

All of these sit at the top level of the kickoff body, never inside `inputs`:

| Field | Purpose | Docs |
|---|---|---|
| `meta` | Free-form metadata (`{"requestId": "..."}`); echoed back in task and crew webhooks and in `/status` `last_executed_task.meta` | [POST /kickoff](https://docs.crewai.com/en/api-reference/kickoff) |
| `taskWebhookUrl` | POSTed after each task completes | same |
| `stepWebhookUrl` | Called after each agent thought/action | same |
| `crewWebhookUrl` | POSTed when the execution completes | same |
| `humanInputWebhookUrl` | POSTed when a `human_input=True` task waits for review (section 5) | [HITL Workflows](https://docs-platform.crewai.com/platform/en/guides/human-in-the-loop) |
| `webhooks` | Event streaming: `{"events": [...], "url": "...", "realtime": false, "authentication": {"strategy": "bearer", "token": "<your-webhook-secret>"}}` | [Webhook Streaming](https://docs-platform.crewai.com/platform/en/features/webhook-streaming) |
| `restoreFromStateId` | Flows with `@persist`: hydrate state from a previous run, record a new run | [inputs.id deprecation](https://docs.crewai.com/en/guides/flows/inputs-id-deprecation) |

What arrived at a receiver in a live test:

| Webhook | Payload | `Authorization` header |
|---|---|---|
| `taskWebhookUrl` | One POST per task: `name`, `description`, `expected_output`, `agent`, `output`, `output_json`, `summary`, `kickoff_id`, `meta` | none |
| `crewWebhookUrl` | One POST on success: `kickoff_id`, `meta`, `result`, `result_json`, `token_usage`. Not sent for a run that failed in `@before_kickoff` | none |
| `stepWebhookUrl` | Nothing, for a crew whose agent had no tools | - |
| `webhooks` (streaming) | `{"events": [{id, execution_id, timestamp, type, data}]}`; `realtime: false` batched 4 events into one POST, `realtime: true` sent one POST per event; `crew_kickoff_failed` arrived for a failed run | `Bearer <your-webhook-secret>` |

- The task / crew / human-input webhooks carry no secret. Treat them as a hint: match the `kickoff_id` against ones you issued, then confirm with `GET /status` before acting.
- Streamed events arrived out of order (a `task_started` before the previous `task_completed`). Sort by `timestamp` or `data.emission_sequence`. Deduplicate on `execution_id` + `id`. Reject deliveries without your bearer secret.

Store the `kickoff_id` with your own request id as soon as `/kickoff` returns. It is the only handle you have on that run.

For a flow with `@persist`, the run's `state.id` is its `kickoff_id`, so `restoreFromStateId` takes a previous `kickoff_id`. Live: restoring from run 1 gave `count=2 history=['one','two']` under a new state id; an unknown id ran from defaults with no error. The deprecated `{"inputs": {"id": "<kickoff_id>"}}` also restored the state but wrote it back under the old id.

---

## 5. Polling `/status/{kickoff_id}`

Live deployments return the [Kickoff Crew guide](https://docs-platform.crewai.com/platform/en/guides/kickoff-crew) shape. The [API reference](https://docs.crewai.com/en/api-reference/status) shows another shape; a client that reads both costs nothing:

| Source | State field | Values | Result |
|---|---|---|---|
| Live (crew and flow) | `state`; `status` is a message (`"Task is Running"`, the exception text on `FAILED`, `null` on `SUCCESS`) | seen: `PENDING`, `STARTED`, `RUNNING`, `SUCCESS`, `FAILED`, `NOT FOUND` | `result` string (`null` until done), `result_json` (`null` for plain text) |
| Kickoff Crew guide | same | also lists `PAUSED`, `REVOKED` | same |
| API reference | `status` | `running`, `completed`, `error` | `result.output`, error text in `error` |

Rules:
1. Read `state`; fall back to `status` only when `state` is absent. Compare lower-cased.
2. Terminal: success = `success` / `completed`; failure = `failed` / `error` / `revoked`; `paused` = waiting for human feedback. Anything else means keep polling.
3. Read `result_json`, then `result` (string, or `result.output` in the reference shape). A failed run has `result: null`; the reason is in `status` (for example `"ValueError: ..."`).
4. Poll with backoff (start around 2 s, grow to about 15 s, add jitter) under an **overall deadline** you choose from the crew's normal run time. Never poll in an unbounded `while True`.
5. A deadline is not a failure of the run. Report it with the `kickoff_id`, keep the id, and check again later - do not kick off a duplicate.
6. Crews report `progress.unit: "task"` with `completed` / `total`. Flows report `unit: "step"` with `total` and `remaining` `null`; show `completed` as a count.
7. An unknown id comes back as HTTP `200` with `state: "NOT FOUND"` (the docs say `404`; handle both). Check you are polling the deployment that issued the id; tolerate a few right after kickoff, then fail. A crew waiting for human input also reads `NOT FOUND` (below).
8. If `/status` keeps answering `5xx`, the run itself may have failed: stop after a few tries and check the deployment's logs instead of polling to the deadline.

Prefer webhooks (section 4) over tight polling when many runs are in flight.

### Human input and `POST /resume` - verify before relying on it

Before building on crew `human_input=True` over the API, verify the whole cycle on your own deployment: pass `humanInputWebhookUrl` (it is the only signal that a run is waiting; its body carries `execution_id` and a UUID `task_id`), handle `NOT FOUND` as well as `PAUSED` from `/status` while waiting, check which field casing (`executionId`/`taskId` or snake_case) your deployment accepts, and confirm the resumed run reaches `SUCCESS`.

For new work, consider a Flow with `@human_feedback` ([Human Feedback in Flows](https://docs.crewai.com/en/learn/human-feedback-in-flows)). The docs say webhook URLs are not carried over to `/resume`; send them again.

---

## 6. The first call

Do not assume the first request answers as fast as the rest, or that it answers `200` on the first try. Design for it:

- Give the first request a generous timeout (minutes, not seconds) and retry `502` / `503` / `504` with backoff, honoring `Retry-After`.
- Make that first request `GET /inputs`: it is read-only, so retrying it is always safe, and you need its key list anyway.
- Retry `POST /kickoff` only when the request provably never reached the server (connection refused / DNS) or got a `503`. A read timeout, `502` or `504` may mean the run started: look for it before sending another kickoff.

In the live tests, `GET /inputs` answered `200` in about 0.1-0.25 s right after each deployment showed Online, and no `5xx` was seen. That is one sample, not a promise - keep the defensive settings.

---

## 7. A small Python client

The full client (httpx, about 200 lines) is in [references/python-client.md](references/python-client.md). It does sections 2-6: validates inputs against `/inputs`, wraps them in `{"inputs": ...}`, stringifies values, retries only what is safe, polls with backoff under a deadline, and raises `RunFailed` / `RunPaused` / `RunTimeout` carrying the `kickoff_id`.

```python
import os
from deployed_crew_client import DeployedCrew, RunTimeout

crew = DeployedCrew(os.environ["CREWAI_DEPLOYMENT_URL"], os.environ["CREWAI_DEPLOYMENT_TOKEN"])
try:
    result = crew.run({"topic": "AI agents", "audience": "engineers"}, deadline_s=900)
except RunTimeout as e:
    print("still running, check later:", e.kickoff_id)
finally:
    crew.close()
```

For a flow, call `crew.run(inputs, flow=True)`: its `/inputs` lists optional state fields, and its values must keep their JSON types (section 2). All of this was run against live deployments on 2026-10-01: success, `RunFailed` with the run's exception text, client-side `MissingInputsError`, server `422`, `401` without the token in the message.

A curl polling loop with a deadline is in the same reference.

---

## 8. Write the crew so repeated and concurrent calls stay correct

Your deployment serves many kickoffs. Do not assume each one gets fresh Python objects: module globals, class attributes, tool instances and anything cached at import time can outlive a run and be visible to the next run, or to one running at the same time. The first three rows were reproduced locally on 1.15.22-1.15.23 (see [references/concurrency-safe-crews.md](references/concurrency-safe-crews.md)).

| Do not | Why | Do instead |
|---|---|---|
| Write to `task.description` (or agent `role`/`goal`/`backstory`) at runtime, e.g. in `@before_kickoff` | crewai keeps the first-seen text as the template and re-interpolates from it. Two runs on one crew object: run 2's prompt carried run 1's customer and not its own | Put per-run values in `{placeholders}` and pass them as inputs; `@before_kickoff` may add or normalise **inputs** and return them |
| Keep per-run data on a tool instance (`self.seen`, `self.customer`) | `crew.copy()` (used by `kickoff_for_each`) reuses the same tool objects, so run 2 saw run 1's data | Keep tools stateless; pass per-run values as tool arguments, or read them from a `contextvars.ContextVar` set in `@before_kickoff` |
| Run two kickoffs at once on one `Crew` object | Overlapping `akickoff()` calls: the second raised `RuntimeError: Executor is already running. Cannot invoke the same executor instance concurrently.` Overlapping `kickoff_async()` calls raised it in some runs and not others. | When you host crews yourself, build a fresh crew per request: `ResearchCrew().crew().kickoff(inputs=...)` |
| Store results, quotas, or "already processed" flags in memory or on local disk | They vanish on restart and are not shared between workers | Use storage you own (database, object store) and pass ids in inputs |
| Call `input()` in a deployed crew | Nobody is at a terminal to answer it, so the run cannot finish | A Flow with `@human_feedback`, or `human_input=True` + `POST /resume` once you have proved it works (section 5) |

In a live test, 8 concurrent kickoffs to one deployed crew each returned their own inputs in the output and in `last_executed_task`, with no cross-over. That shows the platform did not mix those runs; it does not make the patterns above safe - keep them.

Stream or chunk large inputs (large files, big dataframes, large knowledge bases) instead of loading them whole, and measure peak memory locally before deploying.

Shared external limits still apply across concurrent runs: enforce per-minute API limits by waiting, and claim any daily quota in shared storage under a lock.

---

## 9. Common mistakes

| Symptom | Cause | Fix |
|---|---|---|
| Crew: `422 {"detail":"Missing inputs: audience, topic"}` on every call | Body is `{"topic": ...}` without the `inputs` wrapper | Send `{"inputs": {...}}` |
| Flow ignores the values you sent and runs on defaults | Same bare body - a flow accepts it with `200` | Send `{"inputs": {...}}` |
| `422` listing one key | A `{placeholder}` in agent or task text has no matching input | Send every key from `GET /inputs`; check for typos and stray braces |
| Client refuses a flow kickoff: missing `count`, `history`, ... | Flow `/inputs` lists every declared state field, none required | Do not enforce `/inputs` for flows; never send `id` |
| `500 Internal Server Error` on kickoff | Body is not valid JSON | Build the body with a JSON library or `jq`, not string concatenation |
| Locally: `Missing required template variable '...' in description` | Same as above, raised by crewai before any LLM call | Same |
| Output talks about `{topic}` literally | Kicked off with no / empty inputs - interpolation was skipped, no error | Validate inputs client-side; never send `{}` to a crew with placeholders |
| `/inputs` lists a key like `"title": "..."` | A JSON sample in a prompt is read as a placeholder | Remove JSON samples from prompts; use `output_pydantic` / `response_model` |
| `401` | Wrong token, or a token from another deployment | Copy the token from this deployment's Status tab |
| Poll loop never ends | Waiting for one exact string (`"completed"`) while the API returns `SUCCESS`, or no deadline | Lower-case, accept both vocabularies, add a deadline |
| Every poll says `"state": "NOT FOUND"` | Wrong deployment URL for that id, or a crew waiting for human input | Check the URL; for HITL see section 5 |
| `GET /` returns `404` | The live deployment has no root route | Use `GET /inputs` as the health check |
| Result is empty / `None` | Reading `result` before the state is terminal, or ignoring `result_json` | Read the result only after a success state; check `result_json` first |
| Duplicate runs | `POST /kickoff` retried after a read timeout, `502` or `504` | Retry `POST /kickoff` only on connection failures and `503` |
| First call times out, the next one works | Client timeout too short for a slow first response | Long first-call timeout, retries with `Retry-After`, start with `GET /inputs` |
| A run's prompt shows another run's customer or topic | Per-run data written into task text, tool instances, or globals | Section 8 |
| Webhook events arrive out of order | HTTP delivery is not ordered | Sort by `timestamp` or `data.emission_sequence` |
| `/resume` returns `422` "executionId ... Field required" | Field casing differs from the reference page | See section 5 and test the whole pause/resume cycle first |

---

## 10. Checklist

- [ ] Base URL and token come from env vars / a secret store; the token never reaches logs or a browser
- [ ] Client calls `GET /inputs` first and refuses to kick off a crew with a missing key (not a flow)
- [ ] Kickoff body is `{"inputs": {...}}` with string values; `meta`, webhook fields and `restoreFromStateId` sit beside `inputs`
- [ ] Webhook receivers check the bearer secret (streaming) or confirm the `kickoff_id` with `/status` (task / crew webhooks carry no secret)
- [ ] `kickoff_id` is stored with your request id immediately
- [ ] Polling reads `state` then `status`, lower-cased, handles success / failure / paused / `NOT FOUND` / repeated `5xx`, uses backoff and an overall deadline
- [ ] A deadline is reported with the `kickoff_id`, not retried as a new kickoff
- [ ] First request has a long timeout and retries `502`/`503`/`504` honoring `Retry-After`
- [ ] No runtime writes to task or agent text; per-run data flows through inputs
- [ ] Tools and module globals hold no per-run state
- [ ] Large inputs are streamed or chunked, and peak memory was measured locally before deploying

---

## References

- [Python client](references/python-client.md) - the full httpx client, usage, and a curl polling loop with a deadline
- [API contract](references/api-contract.md) - every endpoint, field, state and error with its public doc link
- [Concurrency-safe crews](references/concurrency-safe-crews.md) - the shared-state failures reproduced locally and the patterns that avoid them

For related skills:

- **deploy-to-amp** - getting the project onto AMP in the first place
- **build-flow** - `@persist`, `restore_from_state_id`, `@human_feedback`
- **design-task** - writing task text with `{placeholders}`
- **test-crewai-project** - running crews offline with a stub LLM to test inputs and prompts
- **ask-docs** - query the live docs when a field here looks out of date
