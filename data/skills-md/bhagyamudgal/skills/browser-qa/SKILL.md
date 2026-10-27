---
name: browser-qa
description: Drive a real browser through a UI flow, or run API and endpoint QA and report structured test results. Use when the user names a flow or an endpoint to test against a URL, when verifying filters, pagination, error handling, auth or counts on an API, or after a UI or backend change lands and needs verifying in the browser.
---

I drive a real browser through the flow and I do not call it done until I watched it work. Every step gets a screenshot, the full run gets a recording, API-triggering actions get a network check, and I read the console for new errors.

## Driver priority

1. When `t3-code_preview_snapshot` is in the tool list, I use the T3 preview tools only. I open with `t3-code_preview_open`, go to the URL with `t3-code_preview_navigate`, then loop `t3-code_preview_snapshot` followed by `t3-code_preview_click` or `t3-code_preview_type`. I re-snapshot before every interaction because refs go stale. I keep `open=true` so the user sees the run.
2. Else, when Playwright MCP `browser_navigate` exists, I use the Playwright flow unchanged.
3. Else, I use the `agent-browser` CLI (`open`, `snapshot -i`, `click @eN`, `fill @eN`). I report any evidence the CLI cannot produce as missing, never assume it.

Playwright to T3 mapping: `browser_navigate` becomes `t3-code_preview_navigate`, `browser_snapshot` becomes `t3-code_preview_snapshot`, `browser_click` becomes `t3-code_preview_click`, `browser_type` becomes `t3-code_preview_type`, `browser_press` becomes `t3-code_preview_press`, `browser_wait_for` becomes `t3-code_preview_wait_for`. Screenshots come from `t3-code_preview_snapshot` with `save=true`, which returns a `screenshotPath` to move into `.qa/`.

## Recording

I record every test flow run, not just the screenshots. On T3 I bracket the flow with `t3-code_preview_recording_start` before the first step and `t3-code_preview_recording_stop` after the last one, which saves a local evidence artifact. On the `agent-browser` CLI I bracket with `record start .qa/<flow-name>.webm` and `record stop`. Playwright MCP has no video tool, so there the screenshot sequence is the record and I report video as unavailable, never faked.

Record at minimum 1920x1080, and hold 30 fps minimum on drivers that expose frame-rate control. On T3 I set the viewport with `t3-code_preview_resize` to at least that size before recording starts. On the CLI `record start` opens a fresh context at its own size, so a prior `set viewport` does not carry over: after `record stop` I check the artifact dimensions and report when the file misses the floor instead of claiming it. Neither driver exposes a frame-rate control, so I take the recorder default and report it when the file lands.

## Input

- A natural language flow, for example "Create a recipe with 3 ingredients, verify nutrition calculates".
- A URL plus instructions, for example `http://localhost:3000/orders` plus "Click New Order, fill supplier, submit".
- An API endpoint plus a test matrix, for example `GET /v1/shop/:clientId/patients-order-overview` plus "verify the tab filters, date filters, pagination, error handling, and counts consistency". Here I exercise the endpoint directly, with curl or an in-page request under the authenticated session, and tabulate each case, then produce the QA Test Results report below.

When no URL is provided, I default to `http://localhost:3000`.

When a UI change just landed and no flow was named, I ask what flow to QA, for example "test the order creation at localhost:3000/orders".

## Step 1: Prepare

```bash
mkdir -p .qa
[ -s .gitignore ] && [ -n "$(tail -c1 .gitignore)" ] && printf '\n' >> .gitignore
grep -qxF '.qa/' .gitignore 2>/dev/null || printf '.qa/\n' >> .gitignore
```

I check whether the dev server is running with `curl -s -o /dev/null -w "%{http_code}" <url>`. When it is not reachable, I ask the user to start it.

## Step 2: Auth Check

1. I open the URL with the driver from the priority above and take a snapshot of the page.
2. I look for login form indicators, things like input[type=password], /login in the URL, or auth-related text.
3. When I find them, the session is not logged in. I tell the user to log in manually in their browser, then say "done". I re-check after.
4. When I find none, that alone proves nothing. A logged-out page can render without a visible form. I confirm a post-login marker first, an account name, a logout or profile control, or user-specific content. Only with a marker do I proceed to test execution. Without one I treat the session as unknown and ask the user to log in and confirm.

## Step 3: Execute Test Flow

I parse the user flow into numbered steps and launch a single subagent. The subagent uses the driver I picked in Step 2 and follows the driver priority above.

On T3 the prompt template below runs with each Playwright call translated through the mapping above. T3 network and console evidence comes from collectors the subagent installs before the first step and re-installs after every navigation, baselines there, then reads after each API-triggering action. When the page blocks collector installation, that evidence type is reported unavailable, never faked. On Playwright MCP the template runs unchanged. On the `agent-browser` CLI fallback, `browser_navigate` becomes `open`, `browser_snapshot` becomes `snapshot -i`, interactions become `click @eN` and `fill @eN "text"`, and screenshots, network, and console evidence use the closest `agent-browser` equivalents from `agent-browser --help`. The evidence bar does not drop. Every step still needs its screenshot, and evidence the CLI cannot produce is reported missing, never assumed.

### Mutation preflight (main agent, before dispatch)

I settle this before the subagent exists. A dispatched subagent has no channel to the user, so a `confirmation-required` verdict raised inside it would strand the run with the browser open and nobody to answer it.

When the URL is production-like or any parsed step mutates shared data, I invoke `preflight-mutations` here. I pass the exact environment URL, authenticated account and workspace, action and record IDs, ownership, pre-test record snapshot, restoration or compensation steps, and user authorization. I apply its result contract in the main agent. On `confirmation-required` I present the card and get that decision from the user before dispatching. On `blocked` I report its **Next action** and dispatch nothing. Only a `ready` card is interpolated into the prompt below as `{ready card}`.

Local flows that touch only disposable data do not use this gate. I pass `not-applicable, local flow, disposable data only` as `{ready card}`.

### Subagent prompt template

> Execute the following QA test flow at {URL} using {driver: T3 preview tools | Playwright MCP tools | agent-browser CLI}. The browser session is already open at {URL} from the auth check.
>
> Test steps. {numbered steps from the user flow description}.
>
> Mutation authorization. {ready card}.
>
> That card is already authorized. Do not invoke `preflight-mutations` yourself, since you have no way to answer what it may ask. For every shared-state interaction, re-read and compare that target current guards immediately before the write. Continue under the card while they match. When a guard changed, stop the pending interaction and return the unexecuted remainder to the main agent for re-preflight instead of writing. After the write, run the card authoritative read-back, advance the guards from the observed state, and record the item as `landed`, `failed`, or `reconcile-required`. An ambiguous result is `reconcile-required`. Stop that item and report it for resolution from authoritative state. Never retry it yourself.
>
> For EACH step, take a snapshot first (`t3-code_preview_snapshot` on T3, `browser_snapshot` on Playwright, `snapshot -i` on the CLI). Refs go stale the instant the page changes, so re-snapshot before EVERY interaction. Execute the interaction through the same driver. Capture evidence as a screenshot file at `.qa/<NN>-<step-name>.png`: on T3 call `t3-code_preview_snapshot` with `save=true` and move the returned `screenshotPath` there; on Playwright call `browser_take_screenshot` with that filename; on the CLI use `screenshot`. Run a network check after any API-triggering action and a console check for new errors: on T3 read the pre-installed collectors through `t3-code_preview_evaluate`; on Playwright use `browser_network_requests` and `browser_console_messages`; on the CLI use `network requests` and `console`. When a driver cannot produce an evidence type, report it unavailable instead of faking it. A step with no evidence is a FAIL.
>
> Evidence collectors (T3 only). Before the first test step, install network and console collectors with `t3-code_preview_evaluate` by wrapping fetch and XMLHttpRequest, listening for error and unhandledrejection events, and logging into page-global arrays, then record the pre-flow baseline. Re-install the collectors after every navigation, which destroys page globals. Every later network and console check reads those arrays; when the arrays are missing at read time, report the evidence unavailable for that step instead of clean.
>
> Recording. Start recording before the first test step and stop it after the last one, following the Recording section above. Report the result as `Recording: <path>` or, when the driver cannot record, `Recording: unavailable`.
>
> Report each step in the Step 4 format below. Every numbered step must appear with PASS or FAIL. A step you could not execute is FAIL, never omitted.
>
> Teardown. Stop the recording first when it is still running. On Playwright MCP, `browser_close`. On T3, leave the preview tab open so the user keeps what they watched. On the `agent-browser` CLI, run `agent-browser close` after `record stop`.

## Step 4: Report

```
QA: <flow description>

Step 1: <description>
  PASS: <observation>

Step 2: <description>
  PASS: <observation>
  API: POST /api/endpoint -> 201

Step 3: <description>
  FAIL: Expected X, got Y
  Screenshot: .qa/03-step-name.png

Console errors: <list or "none">
Screenshots: .qa/ (<N> files)
Recording: <path or "unavailable">

VERDICT: <ALL PASS | PARTIAL | FAIL> (N/M steps)
```

On failure I include the exact expected versus actual and reference the screenshot.

The recording path above is the handoff to `file-pr`, which attaches it at PR creation. I report the path and stop there; the late-attach rule in CLAUDE.md covers recordings that land after the PR exists.

## QA Test Results report (endpoint and API QA)

When the run tests an API or endpoint and not only a click path, I build a test matrix and report the structured results below, alongside the Step 4 browser report or in place of it. I group cases by category, filters, error handling, pagination, and consistency, then exercise each one directly and record the actual response against the expected one. A case whose request I dispatched but which captured no response is a FAIL, never an assumed pass.

Endpoint execution and auth. Steps 2 and 3 authenticate and drive only the browser, so an endpoint-only run needs its own executor and authenticated context.

Before any endpoint case runs I record the session origin, the scheme, host, and port Step 2 authenticated against. Every target is checked against that one value, and Test Environment reports it as Session origin rather than defining it. I compute the triple rather than read the URL. I accept only `http` and `https` targets and reject every other scheme, `file`, `ftp` and `gopher` among them, before any approval or dispatch and whether or not the case carries credentials, so the runner never reads a local file or opens a non-HTTP connection on my say-so. I reject any URL whose authority carries userinfo, a percent-escape, or a backslash, then lowercase the scheme and host, convert the host to ASCII punycode, drop one trailing dot, and fill in the default port, 443 for HTTPS and 80 for HTTP. Any other origin needs its own approval, an API on a separate host from the browser app included. Naming or pasting an endpoint is not approval. I show the user the normalized origin and name which credentials I would send, the session cookie and the anti-CSRF token by name and never by value, get an answer in that turn, and record the origin they approved in Test Environment. Without it the case is BLOCKED and I send no request at all, credentialed or not, so a typo or a pasted link receives neither a live session nor a seeded record ID.

A credentialed request in either lane must be HTTPS unless its host is written as a loopback literal, an address in `127.0.0.0/8`, `::1`, or `::ffff:127.0.0.0/104`, or the bare name `localhost`. I read that literal out of the URL and never accept a name I resolved myself, because curl and the browser both resolve again before they connect, so a rebind or a mixed A and AAAA answer can put the request on a public address after my check passed. A host on plain HTTP that is not one of those literals carries no credentials in either lane, so its cases are BLOCKED rather than tested in cleartext.

I get that context one of two ways, and both run those checks first:

- `curl` with the Step 2 session exported into it, its cookies plus the anti-CSRF token. I never pass `-L`, credentialed or not, so every request goes only to the origin I checked. A 3xx is the case's observed result: I record the status and `Location`, score them against the expected response, and never issue the next hop. I carry the session in a host-scoped cookie jar with `-b jar.txt`; when the jar's cookie domain does not cover an approved endpoint origin I set an explicit `Cookie` header for that one origin instead. Plain unauthenticated `curl` is enough only when the endpoint needs no session.
- An in-page request through the driver's evaluate hook. The page the hook runs in has to clear the origin check too, because a `fetch` is same-origin to whatever page is open and the browser attaches the session cookie on its own. A same-origin `fetch` adds no anti-CSRF header, so I either call the app's own request helper, the client it already uses for API calls, which attaches the token, or read the anti-CSRF token from the cookie or meta tag and set it in `RequestInit.headers`. A cross-origin request also needs `credentials: "include"` and matching CORS. `fetch` follows redirects on its own and carries the anti-CSRF header and cookies to the next hop, so I set `redirect: "error"` on every evaluate-hook request. A rejection alone proves neither a redirect nor dispatch: I record the observed error and use available network evidence to distinguish proven no-dispatch (BLOCKED) from dispatched without a response (FAIL). When dispatch remains unknown I report FAIL with that uncertainty, never an assumed redirect or pass, and do not rerun through curl because the server may already have applied the request. A case that needs redirect status or `Location` runs through the curl lane from the start.

I never accept an unauthenticated response as a case result; when I cannot obtain the authenticated context I record those cases BLOCKED instead of testing the wrong thing. An endpoint case that mutates shared data goes through the same mutation preflight as Step 3 before I dispatch it. Screenshots and the recording do not apply when no UI is exercised, so the captured request and response are the evidence for each case.

I capture the environment once so the run is reproducible, and every case row records the complete request inputs, its path, query, body, and any non-secret headers, not query params alone. Replay reuses a freshly provisioned Step 2 session for auth, so the row never carries it: before I write any request or response value I redact credentials, session tokens, auth headers, cookies, and personal data, and keep only the functional evidence a case needs, counts, IDs, statuses, and error messages. I use PASS, FAIL, or BLOCKED text in the Result column, never a check emoji.

### Report template

```
## QA Test Results - <feature or endpoint>

### Test Environment
- Date: <YYYY-MM-DD>
- Session origin: <normalized origin Step 2 authenticated against>
- Approved endpoint origin: <normalized origin and the date approved, when it differs from the session origin>
- Backend: <url> (<database>)
- Test data: <seeded records and their IDs>
- Auth: <account, role, IDs>

### API Endpoint: `<METHOD /path>`

#### <Category> Tests

| # | Test | Request | Expected | Result |
|---|------|---------|----------|--------|
| 1 | <case> | `<path, query, body, safe headers; secrets redacted>` | <expected> | PASS/FAIL/BLOCKED: <actual observed, or the blocker> |

#### Error Handling Tests

| # | Test | Request | Expected | Result |
|---|------|---------|----------|--------|
| N | <bad input> | `<path, query, body, safe headers; secrets redacted>` | <status and message> | PASS/FAIL/BLOCKED: <observed status and message, or the blocker> |

### Browser UI Testing
- <what rendered, with screenshot paths under .qa/>
- <blockers hit, stated plainly, never hidden>

### Findings
- <what passed, what failed, and any behavior that is by design>

VERDICT: <ALL PASS | PARTIAL | FAIL | BLOCKED> (<passed>/<executed> cases, <blocked> blocked)
```

I keep one table per category and add only the categories the endpoint has. A case whose request I never dispatched is BLOCKED, never PASS or FAIL, and so is a case the unauthenticated-response rule above blocks. A request counts as dispatched once its bytes left the client, so a refused connection or a failed DNS lookup is not dispatched. When dispatch cannot be determined after a fetch rejection, I count the case as executed with FAIL and state that dispatch is unknown; I never claim it was dispatched or retry it. I list a blocked case with its blocker, keep it out of the executed count, and cap the verdict at PARTIAL when other cases executed, or BLOCKED when none did. The Browser UI Testing section reuses the screenshots and recording from the browser flow above, so a mixed run reports the click path and the endpoints behind it in one place. Findings state failures and by-design behavior explicitly; a silent omission reads as a pass it never earned.
