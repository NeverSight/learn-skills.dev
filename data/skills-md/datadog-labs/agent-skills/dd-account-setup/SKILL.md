---
name: dd-account-setup
description: Ensure the user has an authenticated Datadog account with a valid DD_API_KEY on the right region before any Datadog setup or instrumentation. Detects existing DD_API_KEY / DD_APP_KEY / DD_SITE, validates them against the Datadog API, and fixes the common wrong-region 403. If no usable key exists, signs the user in (OAuth) or creates a new account, then obtains and validates a key. Use this whenever a user needs a Datadog account or API key, hits a 403 / wrong-region error, or is about to run any Datadog *-setup or instrumentation skill.
---

# Create / connect a Datadog account

This skill gets the user to a known-good state: **a valid API key + application key, on the right region, validated against the Datadog API.** It is the "step 0" that setup/instrumentation skills depend on — run it first, then hand off.

It is a standalone guided flow: detect what already exists, and when nothing usable is found, sign in with **OAuth** (browser, PKCE + state) or create a new account (in-terminal, with a **generated** password saved to `.env`), then turn that session into an API key. Everything runs as small **inline `bash` + `curl`** commands (OAuth also uses `openssl`) — **no bundled scripts, no node**; cross-platform (macOS, Linux, Windows via WSL/Git Bash).

This SKILL.md is the spine — it carries the short steps inline and routes to `references/` for the heavy per-step machinery. Read a reference only when you reach the step that names it.

## The flow at a glance

```
headless requested?  ──yes──▶  Step H: env keys only (OAuth needs a browser), validate, done
   │no (default — interactive)
   ▼
Step 1  Detect existing credentials (env)
   │
   ▼
Step 2  Determine region / site  (DD_SITE → validate; else ask → user picks, default US1)
   │
   ▼
Step 3  Authenticate  — ask first (even if env keys were detected)   → references/authenticate.md
   │        └─ ASK: how to connect? ↴
   │            ├─ A. Use the detected env key (only if one exists) → validate → Step 5
   │            ├─ B. Sign in (I have an account) → OAuth (browser, PKCE + state) ──▶ Bearer token
   │            └─ C. Create a new account → Path C: auto in-terminal signup, generated password ──▶ then OAuth
   ▼
Step 4  Turn the OAuth session into an API key   → references/get-api-key.md
   │        (identity + region via /current_user; OAuth→retrieve most-recent key, app-key→create → write straight to .env; else guide to UI key page)
   ▼
Step 5  Load creds from .env, validate, hand off
```

**Golden rule: never guess or fabricate an API key, app key, token, or site.** Read what's in the environment, validate it, and if it isn't there, authenticate — do not proceed on assumptions.

## Display & wording conventions — read once before Step 1

**Every step** obeys the same rules for how it talks to the user and renders progress: the clean-status-line presentation contract, asking with the host's native selector (never letter-entry), and the live progress checklist with its marker discipline. These live in **`references/conventions.md`** — read it before Step 1 and apply it throughout. Each step below ends with a `↳ Checklist:` cue telling you what to flip.

---

## Step 0 — Preflight (readiness board)

Run this once, first, so the user sees the whole path before anything happens — which tools are
present, what's already detected, and what the flow will do (including that it opens the browser
once). It writes nothing and reveals no secret. Every invocation runs the full flow from Step 1 —
there is no resume/skip-ahead; a prior run is not reused.

```bash
DDLOG="${TMPDIR:-/tmp}/dd-onboard-$(id -u).log"; : >"$DDLOG"   # fresh log for this run
mark(){ command -v "$1" >/dev/null 2>&1 && echo "✓" || echo "$2"; }
# python3 gates the auto browser-callback; fall back to python only if it's a real py3.
have_py3(){ command -v python3 >/dev/null 2>&1 && return 0; command -v python >/dev/null 2>&1 && python -c 'import sys;exit(0 if sys.version_info[0]==3 else 1)' 2>/dev/null; }
py3msg(){ have_py3 && echo '✓ (auto browser-callback)' || echo '⊘ (will paste the redirect URL)'; }
echo   "Datadog account setup — preflight"
echo   "  deps (required):  bash ✓   curl $(mark curl ✗)   openssl $(mark openssl ✗)"
echo   "  deps (optional):  python3 $(py3msg)   browser-open $( { command -v open >/dev/null 2>&1 || command -v xdg-open >/dev/null 2>&1; } && echo ✓ || echo '⊘ (open URL manually)')"
# Canonical DD_* loader — this same block is repeated verbatim in later steps because each ```bash runs a fresh shell (not drift).
# Load DD_* with precedence: shell env > .env.local > .env. A real env var is never overwritten; surrounding quotes are stripped. *_SRC records where each came from (unset ⇒ from the shell env).
for f in .env.local .env; do [ -f "$f" ] || continue; for k in DD_SITE DD_API_KEY DD_APP_KEY; do eval "[ -n \"\${$k:-}\" ]" && continue; v=$(grep -E "^$k=" "$f" | head -1 | cut -d= -f2- | sed 's/^["'\'']//;s/["'\'']$//'); [ -n "$v" ] && { export "$k=$v"; eval "${k}_SRC=$f"; }; done; done
echo   "  detected creds:   DD_SITE=${DD_SITE:-<unset>}${DD_SITE_SRC:+ [$DD_SITE_SRC]}   DD_API_KEY=$([ -n "$DD_API_KEY" ] && echo "set …${DD_API_KEY: -4}${DD_API_KEY_SRC:+ [$DD_API_KEY_SRC]}" || echo '<unset>')   DD_APP_KEY=$([ -n "$DD_APP_KEY" ] && echo "set${DD_APP_KEY_SRC:+ [$DD_APP_KEY_SRC]}" || echo '<unset>')"
echo   "  what happens:     confirm region → authenticate (opens your browser once) → get an API key → write it to .env → validate. ~2 min, one browser approval."
[ "$(mark curl ✗)" = ✗ ] || [ "$(mark openssl ✗)" = ✗ ] && echo "  ✗ missing a required dep above — install it before continuing."
```

Read the board to the user as-is (it's already clean). If a **required** dep is missing, stop and
say so. Then tick the checklist's step 1 and move on — always continue into Step 1; never skip
ahead to a later step.

> ↳ **Checklist:** post the board, then the checklist; mark **1. Detect credentials** ◔.

---

## Step H — Headless / non-interactive (no browser, no prompts)

Decide this first, because the browser + signup paths are impossible without a human. **Infer
headless from the skill's invocation, not from the environment** — the trigger is the user's
request itself: they explicitly ask to run without a browser or without interactive prompts
(e.g. "set up Datadog non-interactively", "I'm in CI, no browser").

Do **not** infer headless merely from a missing TTY — an ordinary terminal run always gets the
interactive flow. Only an explicit request switches it off.

When you've inferred a headless request, run the block below — and only then. There's no browser
for OAuth and no human to answer the signup prompts, so the one way to a valid state is with keys
already provided. Require `DD_API_KEY`, `DD_APP_KEY`, and `DD_SITE`, and fail fast otherwise:

```bash
# Run this block ONLY when you inferred a non-interactive request. It enforces the one thing
# headless needs — keys already present — and fails fast when any are missing.
# Load DD_* (env > .env.local > .env), same precedence as Step 1 — CI keys often live in .env, not exported.
for f in .env.local .env; do [ -f "$f" ] || continue; for k in DD_SITE DD_API_KEY DD_APP_KEY; do eval "[ -n \"\${$k:-}\" ]" && continue; v=$(grep -E "^$k=" "$f" | head -1 | cut -d= -f2- | sed 's/^["'\'']//;s/["'\'']$//'); [ -n "$v" ] && export "$k=$v"; done; done
missing=""
[ -z "$DD_API_KEY" ] && missing="$missing DD_API_KEY"
[ -z "$DD_APP_KEY" ] && missing="$missing DD_APP_KEY"
[ -z "$DD_SITE" ]    && missing="$missing DD_SITE"
[ -n "$missing" ] && { echo "Non-interactive mode requires:$missing — set them and re-run. Sign-in and trial signup need a browser."; exit 1; }
```

If all three are set, hand off to **Step 5**, which validates the key via `/api/v1/validate` (works with the `DD-API-KEY` header). Note: `/api/v1/validate` checks `DD_API_KEY` only — `DD_APP_KEY` is required but not independently verified here; a wrong/expired app key surfaces later at the first app-key-scoped call. There is **no OAuth or signup fallback when headless** — both need a browser — so fail with the message above and keep logs actionable.

> ↳ **Checklist (headless):** two items only — once validate passes, tick both and jump to Step 5.

---

## Step 1 — Detect existing credentials

Read the environment **and** the project's `.env` / `.env.local` files. Do not read the values back to the user in full; mask them.

```bash
# Load DD_* with precedence: shell env > .env.local > .env (real env var wins; quotes stripped). *_SRC = file it came from (unset ⇒ shell env).
for f in .env.local .env; do [ -f "$f" ] || continue; for k in DD_SITE DD_API_KEY DD_APP_KEY; do eval "[ -n \"\${$k:-}\" ]" && continue; v=$(grep -E "^$k=" "$f" | head -1 | cut -d= -f2- | sed 's/^["'\'']//;s/["'\'']$//'); [ -n "$v" ] && { export "$k=$v"; eval "${k}_SRC=$f"; }; done; done
echo "DD_SITE   = ${DD_SITE:-<unset>}${DD_SITE_SRC:+ (from $DD_SITE_SRC)}"
echo "DD_API_KEY= $( [ -n "$DD_API_KEY" ] && echo "set (…${DD_API_KEY: -4})${DD_API_KEY_SRC:+ (from $DD_API_KEY_SRC)}" || echo "<unset>" )"
echo "DD_APP_KEY= $( [ -n "$DD_APP_KEY" ] && echo "set (…${DD_APP_KEY: -4})${DD_APP_KEY_SRC:+ (from $DD_APP_KEY_SRC)}" || echo "<unset>" )"
```

- A `DD_API_KEY` is present (env **or** `.env`/`.env.local`) → go to **Step 2** (pin the site), then **Step 3** and **ask** (choice **A** = use the detected key, or **B**/**C** to authenticate / create a different account). The detected key is an option the user confirms in Step 3, not a default to use silently — they may want a different org or account.
- No `DD_API_KEY` anywhere → the user has nothing usable yet. Still do **Step 2** (so signup lands them on the right region), then go to **Step 3**, where you'll ask how to connect.

An app key without an api key is not enough; treat it as "no key." Because the shell doesn't persist between blocks, every later block that consumes `$DD_API_KEY` re-runs this same loader at its top — that's why it reappears in Path A, Step 4, and Step 5.

> ↳ **Checklist:** post the list now — tick **1. Detect credentials**, mark **2. Confirm region** ◔.

---

## Step 2 — Determine region / site

The site drives *every* URL downstream (signup, API host, key pages), so pin it before validating.
The region table lives in **`references/regions.md`**.

1. **If `DD_SITE` is set** (env or `.env`): validate it against the allowed-site list in
   `references/regions.md`. If it is **not** in that list, stop and show a clear error:
   > `DD_SITE="<value>"` isn't a recognized Datadog site. Pick one of the regions in `references/regions.md` and set `DD_SITE` accordingly.

2. **If `DD_SITE` is unset:** ask the user to pick a region from the table in `references/regions.md` — never silently commit one. **Don't try to detect the user's location** (no IP-geolocation lookups or other third-party calls): the right region is where their *infrastructure* runs, which may not be where they are. Default to **US1** (`datadoghq.com`) if they have no preference. Tell the user, e.g.:
   > Which Datadog region should this account live in? Pick the one closest to where your infrastructure runs (e.g. your cloud region) — sending data to a far-away region adds latency and egress cost, and the region **can't be changed** after the account is created. Default: **US1 (Virginia), `datadoghq.com`**.

   Use the host's native selector with **US1 (default)** first. If it caps the number of options, list as many as it allows in this order — US1, EU1, AP1, UK1 — and let the selector's free-text "Other" cover the rest.

   Wait for the user's reply before continuing. A plain acceptance ("ok", "default", "sure") means US1.

The API host is uniformly `https://api.${DD_SITE}`.

> ↳ **Checklist:** after the user confirms the region, tick **2. Confirm region**, mark **3. Authenticate** ◔.

---

## Step 3 — Authenticate

**Ask how to connect first — even when Step 1 detected env credentials** — then run the path the user picks. Present "The choice" before touching any credential: an ambient `DD_API_KEY` may belong to a different org or account than the user intends, and the region can't reveal which, so let the user decide rather than inferring it. (Headless/**Step H** is exempt — no TTY to ask, env keys only.)

The full detail — "The choice" native-selector wording plus all three paths — lives in **`references/authenticate.md`**:

| The user picks | Path | What it does |
|----------------|------|--------------|
| Use my existing credentials *(only offered if Step 1 detected a key)* | **A** | Validate the detected key (also catches a wrong-region key → back to Step 2). |
| Sign in — I already have an account | **B** | OAuth in the browser (PKCE + state), Bearer token to a `0600` file. |
| Create a new account *(default)* | **C** | Automated in-terminal signup with a generated password → then Path B. |

Read `references/authenticate.md`, present the choice via the host's native selector, and run the matching path. Re-offer the choice whenever a path dead-ends (OAuth finds no account → **C**; a wrong-region key sent the user back to Step 2 first).

> ↳ **Checklist:** keep **3. Authenticate** ◔ until a token or key is actually in hand (see the per-path cues in `references/authenticate.md`).

---

## Step 4 — Turn the OAuth session into an API key

The OAuth token authenticates the user, but downstream instrumentation needs a **`DD_API_KEY`**. Use the Bearer token to confirm identity, then obtain a key — **retrieve** the org's most-recent key on an OAuth session (OAuth tokens cannot create keys), or **create** one when authenticating with an app key; else guide the user to the UI key page.

The full branch (identity check, retrieve-vs-create, the HTTP-code-tagged block, and the outcome table for `EMPTY_ORG` / `LIST_DENIED` / `SECRET_DENIED` / `CREATE_DENIED` / `TRANSPORT_ERROR`) lives in **`references/get-api-key.md`** — follow it. The secret is written straight to `.env`, never echoed.

> ↳ **Checklist:** once a validated key is in hand, tick **4. Get & validate an API key**, mark **5** ◔.

---

## Step 5 — Confirm and hand off

The key is already in `.env`. Load it and validate (a fresh shell each call — always load `.env` first by *parsing* it, never `source` it, so a crafted `.env` can't execute; never inline the literal key):

```bash
DDLOG="${TMPDIR:-/tmp}/dd-onboard-$(id -u).log"; tf="${TMPDIR:-/tmp}/dd-oauth-$(id -u).token"
# Load DD_* (env > .env.local > .env) — parse, don't source, so a crafted .env can't execute. Covers a Path-A key that lives only in the shell env or .env.local.
for f in .env.local .env; do [ -f "$f" ] || continue; for k in DD_SITE DD_API_KEY DD_APP_KEY; do eval "[ -n \"\${$k:-}\" ]" && continue; v=$(grep -E "^$k=" "$f" | head -1 | cut -d= -f2- | sed 's/^["'\'']//;s/["'\'']$//'); [ -n "$v" ] && export "$k=$v"; done; done
vcode=$(curl -sg -o "$DDLOG" -w '%{http_code}' -H "DD-API-KEY: $DD_API_KEY" "https://api.${DD_SITE}/api/v1/validate")
# re-derive org/email for the card (fresh shell — Step 4 vars don't persist); only if a token is still around
who=""; [ -s "$tf" ] && who=$(curl -sg -H "Authorization: Bearer $(cat "$tf")" "https://api.${DD_SITE}/api/v2/current_user" 2>>"$DDLOG" | grep -oE '"email"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | cut -d'"' -f4)
cmk="${TMPDIR:-/tmp}/dd-signup-$(id -u).created"; spw=""   # marker exists only if THIS run created the account (Path C, C3) — no stale password from an earlier run
[ -f "$cmk" ] && spw=$(grep -E '^DD_SIGNUP_PASSWORD=' .env 2>/dev/null | tail -1 | cut -d= -f2-)   # newest .env entry = the password this run generated (C2 appends to .env)
# consistent 🔑 credential card — the one place credential state is summarized; secret shown only as last4
echo "🔑 Datadog credential"
[ -n "$who" ] && echo "   org:     $who"
echo "   region:  ${DD_SITE}"
echo "   api key: …${DD_API_KEY: -4}  (in .env — never printed in full)"
[ -n "$spw" ] && echo "   password: in .env as DD_SIGNUP_PASSWORD (ends …${spw: -4}) — you need it to sign in to Datadog"
echo "   status:  $([ "$vcode" = 200 ] && echo '✓ validated (HTTP 200)' || echo "✗ validate HTTP $vcode — see: tail -n 30 \"$DDLOG\"")"
```

- The card above is the canonical summary — don't also dump the raw validate response. On a non-200, surface `tail -n 30 "$DDLOG"` and treat it per the outcome table (a `403` here is usually wrong region → Step 2).
- Report the authenticated org/email from the identity call.
- Credentials all live in **`.env`** (`DD_SITE`, `DD_API_KEY`, and `DD_SIGNUP_PASSWORD` if the account was created via Path C) — written there directly, never echoed. Clean up the signup temp files and the OAuth *state* + *callback* files: `rm -f "${TMPDIR:-/tmp}"/dd-signup-$(id -u).* "${TMPDIR:-/tmp}"/dd-oauth-$(id -u).state "${TMPDIR:-/tmp}"/dd-oauth-$(id -u).cb`.
- **Downstream handoff — keep the OAuth token.** Leave `${TMPDIR:-/tmp}/dd-oauth-$(id -u).token` (`0600`) in place. Downstream instrumentation reuses this Bearer token to provision resources a plain API key can't create — notably a RUM application. It is short-lived and scoped; the onboarding caller (e.g. the orchestrator) removes it once setup finishes (`rm -f "${TMPDIR:-/tmp}"/dd-oauth-$(id -u).token`). Running instrumentation standalone? Delete it yourself when done.
- Hand back: "Account is ready. You can now run the setup / instrumentation step." (e.g. `studio-setup`, `browser-rum-setup`, `llm-observability-setup`, or any other `*-setup` skill).

> ↳ **Checklist:** tick **5. Ready — hand off** — show the fully completed list so the user sees the flow is done.

---

## Troubleshooting & reference

When a step fails, see **`references/troubleshooting.md`** — the symptom→fix table (wrong region, OAuth state mismatch, headless exit, Path-C signup errors, …) plus the design-decision and temp-state notes.
