---
name: verify-app
description: Verify a change to this app before calling it done. Use after changing the web, the server, a tool, an agent, a job or a chat (prompt, rules or output contract), when a law of docs/INVARIANTS.md is touched, or when reproducing a bug a person reported. Runs the gate, launches an isolated instance for this checkout, drives it like the person using the app, collects evidence (network, console, trace, accessibility, phone width) and writes the proof/skip report.
---

# Verify the app

The question this skill answers: **which features did this change touch, how
do I exercise them on an isolated instance, and what proves they work?**

Two parts, after Poteto's verification skills: a remote control
(`node scripts/verify.mjs`, no argument lists every command) and a feature map
(`docs/verify/`, one file per area with the same four H2s: Sub-features, How
to get to it, Driving it with verify, Gotchas). The CLI drives a running
instance; it is not a test runner. Compose its commands: never write a driver
script for a verification.

The product's part of the CLI (seed states, the server folders `doctor`
watches, extra `up` flags, the browser's locale and permissions, the report's
words) lives in `scripts/verify-app.mjs`; the rest is the same in every app.

## Pick a flow

Every checkout gets its own instance: port, data folder, browser and logs are
derived from the checkout's path and live in `.verify/<port>/`. A git worktree
(`git rev-parse --git-dir`) never fights the main checkout or another
agent's worktree.

- **Fresh worktree or clone:** `node scripts/verify.mjs setup` installs
  dependencies and Chromium if missing, builds the page, `up`, `doctor`.
- **Already set up:** `up` then `doctor`.
- **Done:** `down`; `cleanup` deletes this instance's data and logs
  (`cleanup --all` also reports, traces, screenshots). Remove a worktree
  yourself, from the main checkout, once its branch is pushed.

`doctor` must print `fresh`. Otherwise it names the problem: `STALE BUNDLE`
(run `npm run build`), `STALE SERVER` or commit changed (`down` then `up`),
`WRONG INSTANCE` (the port or the browser belongs to something else).

## Procedure

1. `node scripts/verify.mjs features`: name every area the change affects; read
   only those files (`features <area>`), plus `journeys` when the change
   crosses areas. Read the laws the change touches in `docs/INVARIANTS.md`.
2. `node scripts/verify.mjs check`: the gate, the project's check command
   (`project.md`): lint, the contracts (feature map, laws, architecture
   rules), unit tests, formal models, typecheck + build, bundle secrets,
   end-to-end journeys. It must pass before anything else counts. `check
   --fast` while iterating; `contract` alone needs no install. Formal models
   need Java: without it they are **NOT RUN**, and the gate says "incomplete",
   never "passed" (`formal/README.md`).
3. `setup` or `up` + `doctor` → `fresh`.
4. `report <area…>` writes `.verify/report-<branch>.md`, the template you fill.
5. Put the instance in the state you need with `seed <state>` instead of
   clicking through; `reset` for a blank instance. For running states (a
   reload or a switch mid-run): `down` then `up --delay 4000`.
6. `mark "<what you test>"`, then drive the feature the way a person does:
   `open`, `click`, `type`, `upload`, `press`, `wait-settle`.
7. Collect the proof: `api <route>` after the action and after a reload
   (`open "/"` reloads); `network-summary --since-mark` (the requests the
   action made, statuses, failures); `console --errors --since-mark` (no page
   error); `snapshot`, or `screenshot` for the product owner. `trace start` …
   `trace stop` when a reviewer must replay the action (`npx playwright
   show-trace <zip>`); `perf` for a page-weight question.
8. Front laws on any state: `a11y` (controls without an accessible name, tab
   order: APP-F6), `viewport 375 812` then `overflow` and `screenshot`
   (phone width: APP-F7), then `viewport 1440 900`.
9. Fake models by default: they check the plumbing, not the wording. For a
   change to what an agent writes, say that it needs `up --real`. Use `up --real` only for agent
   behaviour, with the Codex login in `CODEX_AUTH_FILE`.
10. If the change adds or changes something a person can see, update its file
    in `docs/verify/` in the same branch (and a journey in `test/e2e/` when it
    crosses areas). `check` refuses a file without the four H2s. If it changes
    how a law is proved, update `scripts/verify/VERIFY.json`: `check` refuses a law with no
    evidence and no recorded deferral.

## Proof bar

A proof exercises the production path and shows the result a skeptical
reviewer would accept.

- Drive through the page and its normal server calls. `eval` reads state after
  the user path ran; `post` only prepares a state, like `seed`: neither is the
  proof. `api`/`post --bearer <token>` act as that token's identity.
- A proof from an instance that is not `fresh` is not evidence.
- Cover every reachable entry point and the success, failure, empty,
  cancel/rerun and persistence paths the change can affect (the area file
  lists them; `page.route` in a journey, or a stopped server, makes a request fail).
- Show the trigger and the stable end state together (`mark`, the action, the
  `--since-mark` evidence).
- Side effects, not pixels: the stored record (`api /api/<route>`), the run
  row (`api /api/runs`), the state after a reload or a `down`/`up`.
- Fake models count only because they sit behind the production boundary (the
  model provider, under the same runtime, server and web). Anything that skips
  the web or the server is not coverage of the page.
- Name what you could not reach (native file picker, OS drag and drop, real
  provider, production only) and the closest real path you covered instead.

## Evidence, cheapest adequate first

```text
lint + contracts + unit tests → formal models → end-to-end journeys (fake models)
→ driven instance (verify) → real models on the instance (up --real)
→ the people's own use
```

A passing layer never proves a claim of a higher layer: a green unit test says
nothing about the page; a fake-model journey says nothing about the wording.

## Never

- Real user data anywhere in the repository, tests, fixtures, reports or
  committed screenshots: only invented data.
- Production as a test bed. The `verify up` instance is yours; production is
  the users' (`docs/verify/deploy.md` is read-only checks after a deploy).
- "Verified" from a merge, a green CI or a deployment: what ran where is the
  release skill's question, and "unknown" is a valid answer.

## Report before calling it verified

Fill `.verify/report-<branch>.md` (from `report <area…>`) and paste it in the
pull request (the evidence table of `.github/pull_request_template.md`):

- commit, `doctor` line, `check` result (and whether formal models ran), models (fake / real);
- per area: the paths driven, the commands, the observed side effect (key output);
- skipped or unreachable paths: what blocks each one, and the closest real path covered;
- what is not proved here (for instance: wording needs real models).
