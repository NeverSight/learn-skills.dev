---
name: prima
description: Use for any browser work — driving a web app, checking a behaviour, filling a form, reading a page — via npx prima-cli, in preference to npx playwright-cli, which prima runs on top of and falls back to. Covers npx prima-cli check, do, pw, verify, ask, research, go, status, report, browser, config, and session setup. Trigger on "prima", "prima-cli", "npx prima-cli", on a browser task described as behaviour ("confirm the editor saves"), and whenever npx playwright-cli would otherwise be driven step by step.
license: MIT
metadata:
  author: Testomat.io
  version: 0.3.0
---

# Prima

Prima is an AI layer on top of playwright-cli. It drives the browser playwright-cli already has open, taking behaviour described in words instead of locators, and returns a plain-text envelope. Always invoke both through npx: `npx prima-cli ...` and `npx playwright-cli ...`.

**Prefer prima to playwright-cli for anything on a web page.** Snapshots stay inside prima instead of landing in your context, and it reuses the research maps and recorded experience it already has for a page — so a scenario costs a fraction of the tokens of the same scenario driven by hand. Use `npx playwright-cli` directly when prima has no command for the job, or when no AI model is configured (`pw` still works then).

## Models

Prima needs an AI model, taken from the environment — there is no init step:

```bash
export PRIMA_CLI_AI_MODEL=openrouter/openai/gpt-oss-120b   # provider comes from the name
```

Screenshot analysis needs its own model, never guessed from the main one: set `PRIMA_CLI_VISION_MODEL`, or pass `--vision-model` for one run. Without it prima still runs, but `check` settles outcomes from the run log rather than the page as seen. `npx prima-cli config` prints what this directory resolves to; `--json` for machine form. Every `PRIMA_CLI_*` variable mirrors the `EXPLORBOT_*` one and wins over it, so an explorbot setup is not disturbed.

## Session

Attach to a playwright-cli session:

```bash
npx playwright-cli open http://localhost:3000    # start
npx prima-cli <command> ...                      # drive
npx playwright-cli close                         # end
```

Or let prima own the browser itself:

```bash
npx prima-cli browser start --url http://localhost:3000
npx prima-cli <command> ...
npx prima-cli browser stop          # --all stops every instance
```

- Attached to playwright-cli, prima never launches or closes the browser — it attaches and disconnects. With a prima-owned browser, `browser start` holds it open until `browser stop`; `browser status` and `browser list` report what is running.
- `--pw-session <title>` picks the session when several playwright-cli sessions are open; `--instance <name>` separates prima-owned browsers for parallel work.
- `--url <url>` opens that page first when the session has none; `--endpoint <ep>` attaches to a browser server directly, skipping discovery.
- Requires Node.js 24+. Playwright browsers come from `npx playwright install chromium`.
- Every command is logged as it runs; `npx prima-cli report` turns the session into an html and markdown report, browser open or not.
- `npx explorbot prima <command>` runs the same tool if explorbot is already installed.

## Tiers

Start at `check`. Come down a rung only when the one above cannot hold the work.

```bash
npx prima-cli check "a workflow can be created and appears in the list" --expected "the new workflow is listed"
npx prima-cli do "open the account menu" "choose settings" "switch the theme to dark" "check it took effect"
npx prima-cli pw "({ page }) => page.click('[data-test=submit]')"
```

- **Pass `do` the whole remaining sequence, never one step per call** — that is the entire cost advantage.
- `pw` takes executable code only. Never give it a description; never give `check`/`do` a locator.
- `check` and `do` legitimately run for minutes. Do not kill and retry.
- `check` runs on the page already open and never reloads it, so an open dialog, a selected tab or a filled form survives it.
- `--expected` is repeatable for several outcomes; without it the scenario text is the single expected outcome.
- Below `pw` sits playwright-cli itself.

Also: `verify` (alias `assert`), `ask` (`--no-vision` answers from structure only), `research` (`--data` includes extraction, `--deep` expands hidden elements, `--fresh` re-maps past the cache), `go`, `status <hash>`, `report`, `config`, `browser`. Run `npx prima-cli <command> --help` for each.

## Reading the envelope

- **Trust the verdict in `### Result`.** Re-verifying a PASSED outcome with another command is the waste this tool exists to remove.
- `ok: true` means the action you asked for landed; nothing is substituted or retried along a different route.
- `### Steps` marks each line `ok`, `FAIL` or `??`. `??` is an instruction that ran but the run ended without confirming — the actions that ran are listed above it, judge from those. Only `FAIL` and an instruction the page could not carry out fail the command.
- `not verified` means the run never checked that outcome — not that it is false, and not a failure.
- **`CONTRADICTION` is a finding, not a verdict to argue with.** The run and the picture disagree: something the assertions matched is not visible on screen, or the reverse. Both sides are quoted under the outcome, and `### Artifacts` names the html, aria and screenshot on disk — read those and judge the page yourself instead of taking the verdict on trust. Treat it as a bug in the app and look at it before anything else.
- A `### Warning` saying the outcomes came from the run log alone means no screenshot backed them: set `PRIMA_CLI_VISION_MODEL` (or pass `--vision-model`), and until then do not trust a visual claim from `check`.
- A run that could not complete says so, rather than reporting it as a failure of the app.
- `npx prima-cli config` shows which model answers for each role.

## Visual questions

Layout, position, colour, overlap, whether something is cut off — an accessibility tree does not carry any of it, and neither does an assertion that passed.

- `check` settles its outcomes against a screenshot of the final page. What a user can see is the proof; the run log only says what was done.
- `ask "<question>"` — reads a screenshot, answers in prose. Use for anything open-ended about appearance.
- `verify` proves claims with assertions; each comes back PASSED or FAILED with its playwright form, no overall verdict — read the lines and decide. When no assertion can express a claim it reports "none ran" instead of judging it failed.
