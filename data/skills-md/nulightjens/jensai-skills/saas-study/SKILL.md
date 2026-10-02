---
name: saas-study
description: Systematically study a SaaS product to build a knowledge library for "should I build this?" / "how would I clone this?" decisions. Captures public surface, generates a deliberate authed-extraction gameplan, executes it against the user's real signed-in browser via the chrome-devtools MCP, fingerprints third-party providers from network traffic, and writes a token-tiered evidence folder with BRIEF + GAMEPLAN + manifest at <library-root>/<domain>/<date>/ (default ./saas-library/). Use when the user says "study saas X", "deep-dive this SaaS", "reverse engineer this app", "what's their stack", "/saas-study <url>", or asks to add a SaaS to their build-inspiration library. Does NOT replicate, scrape for resale, or evade bot management.
allowed-tools: Bash(python3:*), Bash(bash:*), Bash(ls:*), Bash(cat:*), Bash(mkdir:*), Bash(touch:*), Bash(rm:*), Read, Write, Edit, mcp__chrome-devtools__*
---

# saas-study

Study a SaaS product, build evidence-first knowledge artifacts for the user's library.

## When to use

- User says "study saas X", "/saas-study <url>", "deep-dive this SaaS", "reverse engineer this app for inspiration"
- User wants to add a SaaS to their inspiration/build library
- User asks "how does product X work mechanically?" or "what stack is this on?". First check if `<library-root>/<domain>/` already has a recent study, otherwise propose running one

## When NOT to use

- Replicating proprietary content
- Scraping for resale or competitive harm
- Evading bot management on hostile targets
- Endpoint fuzzing / unauth probing
- Studying sites the user has no legitimate interest in

## Orchestration

This skill is **you (Claude) walking the user through a four-phase study**, with Python scripts handling deterministic mechanical work and the chrome-devtools MCP driving the browser. You author GAMEPLAN.md yourself (Phase 2.5); do not skip that reasoning step.

The skill **does not drive Phase 3 clicks**. The user drives their own browser; you just record via the chrome-devtools MCP attached to their Chrome.

## Paths and parameters

Two paths matter. Resolve both before running anything.

| Name | What it is | Default |
|---|---|---|
| `$SKILL` | Where this skill is installed. Use `${CLAUDE_SKILL_DIR}` when the harness sets it, otherwise the directory containing this `SKILL.md`. | n/a |
| `$LIBRARY` | Where studies are written. Passed to `new_study.py --library-root`. | `./saas-library/` in the current working directory |

```bash
SKILL="${CLAUDE_SKILL_DIR:-$(dirname "$0")}"   # or the install path you copied the skill to
LIBRARY="./saas-library"                        # override per-run with --library-root
```

Every script path below is written as `$SKILL/scripts/<name>.py`. Every output path is under `$LIBRARY/<domain>/<YYYY-MM-DD>/`, captured as `$STUDY`.

## Pre-flight (one-time per machine)

Most scripts are stdlib-only. Three of them need packages: `extract_html.py` (trafilatura, with a beautifulsoup4 + lxml fallback), `extract_pricing.py` (beautifulsoup4 + lxml), and `render_brief.py` (jinja2).

Create an environment however you normally do. A project-local venv works fine:

```bash
python3 -m venv .venv
.venv/bin/pip install -r "$SKILL/scripts/requirements.txt"
PY=.venv/bin/python
```

Or install into whatever Python you already use:

```bash
python3 -m pip install trafilatura beautifulsoup4 lxml jinja2
PY=python3
```

`$SKILL/scripts/install.sh [venv-path]` does the venv route for you and prints the interpreter path. Optional screenshot redaction (`--redact`) additionally needs `pillow` + `pytesseract` plus a system `tesseract` binary; it skips gracefully when they are missing.

Set `PY` to the interpreter that has those packages. The rest of this file uses `$PY` for scripts that need them and `python3` for the stdlib-only ones.

### Chrome attach (this is the #1 source of friction)

Phase 2 and Phase 3 run through the **chrome-devtools MCP**, which attaches to a Chrome instance exposing a remote debugging port. Enable the MCP in your Claude Code session first (`/mcp` menu, or add the server to your MCP config; see the chrome-devtools MCP project docs for the exact server entry). Whatever port your MCP config points at is the port Chrome must be listening on.

Check the attach early via `mcp__chrome-devtools__list_pages`. Three failure modes you will hit:

1. **`Network.enable timed out`**. A stale Chrome instance is hanging on the debug port. Find and kill it (confirm with the user first, and never kill a browser they are actively using):
   ```bash
   pgrep -af "remote-debugging-port=<PORT>" | head -1   # -> root PID
   kill -9 <PID>
   ```
2. **`Failed to fetch browser webSocket URL`**. No Chrome is listening on the port. Launch one. A separate `--user-data-dir` keeps the study isolated from the user's everyday profile (no cookies or sessions leak in), which is the right default for public capture; for authed capture the user signs in inside that instance. Example using port 9222:
   ```bash
   mkdir -p /tmp/saas-study-chrome-profile
   open -na "Google Chrome" --args \
     --remote-debugging-port=9222 \
     --user-data-dir=/tmp/saas-study-chrome-profile \
     --no-first-run --no-default-browser-check &
   sleep 3
   curl -s http://127.0.0.1:9222/json/version  # verify
   ```
   On Linux, `google-chrome --remote-debugging-port=9222 --user-data-dir=/tmp/saas-study-chrome-profile &` is the equivalent. Match the port to your MCP config.
3. **MCP can't see new tabs**. Call `list_pages` again. The MCP enumerates fresh.

After launching, retry `mcp__chrome-devtools__list_pages` to confirm attach.

## Argument parsing

Standard invocation: `/saas-study <url> [flags]`

Flags:
- `--library-root PATH` (default: `./saas-library`) where the study folder is written
- `--stealth=fast|balanced|high` (default: balanced)
- `--no-authed` skip Phase 3 entirely
- `--no-screenshots` skip all screenshot capture
- `--redact "name=X,email=Y"` OCR-blur named strings in screenshots

Parse `<url>` to derive `<domain>` (strip protocol, www, path).

## Phase 1: Public harvest

1. Run `python3 "$SKILL/scripts/new_study.py" <url> --stealth <profile> [--library-root $LIBRARY]`. This creates:
   - `$LIBRARY/<domain>/<YYYY-MM-DD>/` with `.gitignore`, empty `study.json`, subfolders
   - `$LIBRARY/.gitignore` if first study
   - Prints the study folder path; capture this as `$STUDY` for later commands

2. Run `python3 "$SKILL/scripts/fetch_public.py" <url> $STUDY`. This:
   - Fetches `robots.txt` and `sitemap.xml` over stdlib urllib with realistic browser headers
   - Writes `$STUDY/raw/public/robots.txt`, `$STUDY/raw/public/sitemap.xml`
   - Writes `$STUDY/derived/public-urls.json`, a sitemap-derived URL list scored by likely interest (pricing, about, docs, blog, changelog, features, login URL)
   - Honors robots.txt; logs skipped paths

3. **First-run consent check.** If `$LIBRARY/.saas-study-consented` does not exist AND `--no-authed` was not passed, show the consent prompt verbatim (see §First-run consent below). On Y, `touch $LIBRARY/.saas-study-consented`.

## Phase 2: Public browser pass

### Fast path: bulk curl for SSG marketing sites

Before driving chrome-devtools through 10+ pages, **quickly check if the marketing site is server-rendered SSG** (Astro / Next.js static export / Hugo / Webflow / WordPress). If yes, you can skip chrome-devtools entirely for public pages and curl them all in parallel: 10x faster, fewer tool calls, no token spend on JS bundles.

How to detect: navigate to the landing page once via chrome-devtools, capture the HTML, and grep for SSG markers (`/_astro/`, `_next/static` without `__NEXT_DATA__`, `wp-content/`, `webflow`, etc.). If the page text content is present in the raw HTML without JS hydration, it's SSG and you can curl.

```bash
UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
cd $STUDY/raw/html

# All public URLs in parallel
for url in $(jq -r '.urls[] | "\(.slug)|\(.url)"' $STUDY/derived/public-urls.json); do
  slug="${url%%|*}"; url="${url#*|}"
  curl -s -A "$UA" "$url" > "$slug.html" &
done
wait
ls -la *.html | awk '{print $5, $9}'   # verify sizes
```

For chrome-devtools-only sites (auth-walled, JS-rendered), use the per-page flow below.

### Per-page browser flow (when needed)

For each URL in `$STUDY/derived/public-urls.json` (top 10 to 15 by score):

1. `mcp__chrome-devtools__new_page` (or reuse) then `navigate_page` to the URL
2. `wait_for { networkIdle: true }` (or 8s timeout). If unavailable, evaluate_script a `new Promise(r => setTimeout(() => r(document.title), 2500))` instead.
3. Apply pacing: read profile from `$STUDY/.stealth-profile`; sleep randomized [browser_nav_delay_seconds]; if `scroll_after_navigate` is true, evaluate_script to `window.scrollTo({top: window.innerHeight * 0.55, behavior: 'smooth'})`, wait 1s, scroll back to top
4. `take_screenshot { fullPage: true, filePath: "$STUDY/screenshots/<slug>.png" }`
5. **HTML capture.** DO NOT use `take_snapshot` (that returns a11y text, not HTML). Use:
   ```js
   evaluate_script: () => document.documentElement.outerHTML
   ```
   The MCP returns one of two formats. Both are handled by the helper:

   **Format A (inline, smaller pages):** the response text contains:
   ```
   Script ran on page and returned:
   ```json
   "<json-escaped-html>"
   ```
   ```
   **Format B (buffered to disk, larger pages):** the MCP saves a path to a `mcp-chrome-devtools-evaluate_script-<ts>.txt` tool-results file, and the file content is the same plain text from format A (NOT a JSON envelope on current MCP versions).

   Extract HTML via the bundled helper (handles both formats; do not use `jq`, it only worked on legacy MCP versions):
   ```bash
   python3 "$SKILL/scripts/extract_html_buffer.py" <buffer-file> $STUDY/raw/html/<slug>.html
   ```
6. After visiting each URL: `list_network_requests` (filter `resourceTypes: ["xhr", "fetch", "document"]` to skip CSS/JS/font noise), save as JSON to `$STUDY/raw/network/<slug>.json`. Format expected by the scrubber is a list of `{url, method, status}` objects (you can hand-construct from `list_network_requests` text output if HAR export isn't available).

Then extract markdown:
```bash
$PY "$SKILL/scripts/extract_html.py" $STUDY
```
This walks `raw/html/*.html` and writes `extracted/*.md` via trafilatura. **Important:** use the interpreter that has the packages installed (`$PY`), not a bare system python that lacks trafilatura.

## Phase 2.5: Author GAMEPLAN.md

This is **your** reasoning step. Do not delegate to a script.

1. Read `extracted/landing.md`, `extracted/pricing.md` (if present), `extracted/about.md` (if present), and a couple of feature pages.
2. Read `$SKILL/references/gameplan-template.md` for shape and tone calibration.
3. Author `$STUDY/GAMEPLAN.md` with sections A through E:
   - **A.1** stated value prop (verbatim from landing hero where possible)
   - **A.2** visible feature inventory as a table with "needs authed verification?" column
   - **A.3** pricing/metering model inferred (only if pricing page exists)
   - **B.1** expected provider table (one row per category you can guess from observed clues)
   - **B.2** expected own-API endpoint patterns (predictions based on feature names)
   - **B.3** interesting behaviors to watch (debouncing, streaming, rate limits, gating)
   - **C** ordered Authed Capture Plan, one numbered step per critical feature, each with goal/action/capture mode/endpoints expected/what to inspect
   - **D** out of scope (explicitly)
   - **E** done criteria (checklist)

Aim for ~2-3k tokens. Be deliberate, not exhaustive. Every Step in §C must trace back to a public-surface observation.

If user passed `--no-authed`, write a minimal GAMEPLAN.md noting auth was skipped and proceed to Phase 4.

4. Tell the user: "Gameplan written to $STUDY/GAMEPLAN.md. Review and edit if needed, then say 'go' to start authed capture."

5. **Wait for user "go"** before proceeding to Phase 3. The user may edit the file.

## Phase 3: Authed execution

### Phase 3 prelude: credit/quota budget check (do this before any gameplan step)

Many target SaaS apps gate authed actions with **credits or quota**. If you walk the gameplan without budget awareness, you can burn the user's entire trial in 5 minutes, and they'll feel it (every generation, every scrape, every AI call has a real cost). Surface the situation explicitly:

1. From the post-login bootstrap (§3a), extract the trial / quota state. Look for fields like `credits_total`, `credits_used`, `trial_credit_cap`, `daily_credits_limit`, `feature_restricted_credits`, `subscription_status: trialing`. These usually appear in `/api/.../subscription-status`, `/api/user/stats`, or direct database-backed queries to a `user_credits`-style table.
2. Walk the gameplan §C steps and try to infer or capture the credit cost per step (UI modals often show "Cost: X credits" before launching). Costs are commonly formulaic, for example a base charge plus a per-keyword or per-item charge on search, and a much larger one-time charge the first time a new entity is added and enriched.
3. **Ask the user how to allocate the budget** via `AskUserQuestion`. Offer 3-4 tiers (minimal / typical / full / no-paid-endpoints) with credit estimates. Be honest that a few features may not get an endpoint captured if budget is tight.
4. Re-check credits after every step so you can warn the user before a single action burns 20% of the remaining budget.

A typical 100-credit trial covers one search, one generation, one AI chat, one enrichment-style add, plus all the free CRUD and route probes, at roughly 40 credits with the most informative endpoints captured. Leave the rest for the user to actually try the product.

### Errors are often the richest signal

Failed requests usually leak more architecture than successful ones. In one study, a `429 quota exceeded` error from an AI chat endpoint returned an error body that named **the entire model-fallback chain in plain text**:

```
<provider>:<model-a> -> 429 ... | <provider>:<model-a-dated-snapshot> -> 404 ... | <provider>:<model-b> -> 429 ...
```

That single error answered:

- Which provider the router actually uses (one provider, not the several shown in the UI model picker)
- The exact model rotation order
- Whether they cross-provider failover (they didn't)
- That a versioned snapshot id was tried but doesn't exist (404)

**Behaviour to add to your loop:** when an authed action returns a non-200 status, *always* capture the response body via `get_network_request --responseFilePath`. Errors are free intelligence. If a feature happens to be in a quota outage during the study, don't treat it as a failure, treat it as a gift.

### 3a Login pause

Tell the user: "Sign in to <domain> in your Chrome window now. When you're on the authed surface (dashboard or equivalent), type 'continue'."

When the user says continue:

- `take_snapshot` to verify the URL changed off a public page (a11y output; just for sanity check)
- `evaluate_script: () => location.href`, record the post-login landing URL
- `take_screenshot` to `$STUDY/screenshots/post-login.png`
- `evaluate_script: () => document.documentElement.outerHTML`, extract via `extract_html_buffer.py` (see Phase 2) to `$STUDY/raw/html/post-login.html`
- `list_network_requests` since session start, filtered to xhr/fetch, dump to `$STUDY/raw/network/post-login-bootstrap.json`
- For any tRPC/GraphQL/REST endpoints that look load-bearing (`user.current`, `agency.get`, `me`, `session`, etc.), call `get_network_request { reqid, responseFilePath: "$STUDY/raw/network/sample_<name>.network-response" }` to capture **response bodies**. These feed `fingerprint_data_shapes.py` in Phase 4 to detect vendors that proxy server-side.

### 3a.1 Auth-cookie inspection (high-signal, low-effort)

Right after login, **decode the auth cookie** to identify the auth provider. This is one of the highest-signal moves in the whole study. Most apps store a session cookie named `*-auth`, `sb-*-auth-token`, `*_session`, or similar. The cookie value is often `base64-{json}` or a JWT.

Look at one of the captured `get_network_request` outputs and pull the `cookie:` header. Common patterns:

| Auth provider | Cookie / token signature |
|---|---|
| **Supabase Auth** | Cookie value is `base64-<json>` containing `access_token` (JWT). Decoded JWT `iss` field is `https://<project-id>.supabase.co/auth/v1`. Project ID is a unique fingerprint. |
| **Clerk** | Cookie name starts with `__client_uat`, `__session`, or `__clerk_*`. Domain headers reference `*.clerk.accounts.dev` or `*.clerk.com`. |
| **Auth0** | Cookie names start with `auth0.`, `a0:state`, or `auth0_compat`. Redirect URLs hit `*.auth0.com`. |
| **NextAuth / Auth.js** | Cookies `next-auth.session-token`, `next-auth.csrf-token`, `next-auth.callback-url`. JWT or DB-session. |
| **Stytch** | Cookies `stytch_session`, `stytch_session_jwt`. Calls to `*.stytch.com`. |
| **WorkOS** | Cookies often named after the app's brand; SSO flow hits `api.workos.com` with `connection_id` query. |
| **Custom JWT** | Cookie usually named after the brand (`<brand>-auth`, `<brand>_session`). Decode the JWT and check `iss`, `aud` claims. |

To decode a base64-wrapped Supabase-style cookie in Bash:
```bash
echo "<cookie-value>" | sed 's/^base64-//' | base64 -d | python3 -m json.tool | head -30
```

The decoded payload usually reveals `email`, `user_id`, JWT issuer, refresh-token. **Record only the issuer and provider** in BRIEF.md. Do NOT log the access_token or refresh_token themselves (they grant live access).

### 3a.2 Sidebar nav enumeration (MANDATORY)

**You MUST walk every left-nav item in Phase 3. Skipping items is the #1 coverage gap.** Modern SaaS apps render sidebars as `<button>` (not `<a>`), so `getAttribute('href')` returns null. Discover routes two ways:

**Approach A, programmatic click-walk:**
```js
async () => {
  const labels = ["Create Post","Inspiration","Prompts","Sources","Calendar","Published Posts","Failed Posts","Videos","API Dashboard","Settings"]; // your list
  const result = {};
  for (const label of labels) {
    const node = Array.from(document.querySelectorAll('*'))
      .find(el => el.children.length === 0 && el.textContent.trim() === label);
    if (!node) { result[label] = 'NOT_FOUND'; continue; }
    let walker = node;
    for (let i = 0; i < 10 && walker; i++) {
      if (walker.tagName === 'BUTTON' || walker.tagName === 'A' || walker.getAttribute('role') === 'button') {
        const before = location.pathname;
        walker.click();
        await new Promise(r => setTimeout(r, 1200));
        result[label] = { before, after: location.pathname };
        if (location.pathname !== before) { history.back(); await new Promise(r => setTimeout(r, 1200)); }
        break;
      }
      walker = walker.parentElement;
    }
  }
  return result;
}
```

**Approach B, HEAD-request route probing (when you already have candidate paths):**
```js
async () => {
  const candidates = ['/create','/inspiration','/prompts','/sources','/calendar','/published','/failed','/videos','/api-dashboard','/labs/viral-coach','/settings','/settings/billing','/settings/profile','/settings/api','/settings/brand'];
  const r = {};
  for (const p of candidates) { try { r[p] = (await fetch(p, {method:'HEAD',redirect:'manual'})).status; } catch(e) { r[p] = 'ERR'; } }
  return r;
}
```

After discovering routes: navigate to each, screenshot, capture `evaluate_script(main.innerText)` for content, dump `list_network_requests` filtered to xhr/fetch, and capture response bodies for any new `/api/*` or `backend.*/v2/*` endpoint with `get_network_request`. **Skip nothing.** Even an empty trial-state route reveals the endpoint shape (`/v2/failed-posts` returning `{}` is still a discovered endpoint).

### 3b Step-by-step gameplan execution

Re-read `$STUDY/GAMEPLAN.md` §C. For each numbered step:

1. Print the step block to the user verbatim (goal, action, capture mode, endpoints expected, what to inspect).
2. Print menu: `When ready, perform the action in your browser then type 'done'. Or: 'skip' | 'note <text>' | 'start window <label>' | 'capture <label>' | 'quit'`
3. **Before the user acts**: snapshot current `list_network_requests` length as `before_count`
4. When user types `done`:
   - Wait for network to settle (2-3s `evaluate_script` Promise timeout works fine)
   - `list_network_requests` filtered to `["xhr", "fetch"]`, take entries with index >= before_count
   - `list_console_messages`, take new entries
   - `take_screenshot` to `$STUDY/screenshots/step-<N>-<slug>.png`
   - **HTML**: `evaluate_script: () => document.documentElement.outerHTML`, extract via `extract_html_buffer.py` to `$STUDY/raw/html/step-<N>-<slug>.html`
   - **Response bodies**: For 1 to 3 of the most interesting new requests this step (e.g., the tRPC `.get(uuid)` or `.list(filter)` calls that match the step's goal), capture full bodies via `get_network_request { reqid, responseFilePath: "$STUDY/raw/network/sample_<router>_<procedure>.network-response" }`. These power data-shape fingerprinting.
   - **Optional:** run `append_action.py` to populate the action-trace (powers `verify_gameplan.py`). In practice most studies skip this; findings get recorded directly in BRIEF.md instead. Don't gate the loop on it.
   - Read predicted endpoints from gameplan §C for this step
   - For each predicted endpoint, check if any captured request matches the pattern, then print `HIT: <pattern>` or `MISS: <pattern>`
5. Move to next step.

On `start window <label>`: enter window mode. Snapshot `before_count`. Tell user "Window '<label>' open, interact freely. Say 'stop window' to close." When user says stop, capture full delta as one `type: window` entry.

On `capture <label>`: ad-hoc snapshot + screenshot + HTML. No network attribution.

On `note <text>`: append to `$STUDY/notes/user-notes.md` and continue.

On `skip`: log skip in action-trace with `type: skipped`. Move to next step.

On `quit`: break out of loop, proceed to Phase 4.

### 3c.1 MCP-direct path (Path A), opt-in and frequently auth-blocked

If the SaaS exposes its own MCP integration (visible in your tool list as a vendor-named MCP server), Path A is **optional and frequently blocked by auth**. Empirically it has been auth-rejected more often than not. Do not gate Phase 3 on it; treat it as a bonus that validates the browser-observed REST contract against the MCP contract.

**When Path A works:** Calling the MCP tools directly captures response shapes without burning a browser session, and you can compare the response key/value shapes against what the browser sees. Discrepancies (e.g., MCP wraps under `"data":[]` while browser uses `"items":[]`) are interesting fingerprints.

**When Path A is blocked:** You'll see `Invalid API key or auth session` or similar. Tell the user to either (a) reauthorize the vendor connector in their client settings, or (b) skip Path A and continue with Path B (browser). Default to (b), it's reliable.

**Schemas alone are signal.** Even without calling the MCP tools, their **descriptions** (visible via `ToolSearch`) often reveal: enum values (platform list, status states), required fields per platform, polling cadence, third-party provider names mentioned in tool descriptions, upload constraints, idempotency rules. Document these in BRIEF.md as "from MCP tool schemas". They're public-contract evidence even if the calls didn't succeed.

### 3c Wrap

After loop completes or quit:

- `list_network_requests`, dump full to `$STUDY/raw/network/authed.json` (or HAR)
- Tell the user the loop is done; proceeding to synthesis.

## Phase 4: Synthesis

Run these scripts in order. **Use the interpreter with the packages installed** (`$PY`), not a bare system python.

```bash
$PY "$SKILL/scripts/scrub_network.py" $STUDY
$PY "$SKILL/scripts/fingerprint_providers.py" $STUDY
$PY "$SKILL/scripts/fingerprint_csp.py" $STUDY              # parses CSP allowlist for server-proxied providers (Stripe, Supabase, PostHog, GTM, ...)
$PY "$SKILL/scripts/fingerprint_tech.py" $STUDY
$PY "$SKILL/scripts/fingerprint_data_shapes.py" $STUDY      # detects vendors via response shapes (creator-data APIs, auth providers, AI-router error leaks, ...)
$PY "$SKILL/scripts/extract_pricing.py" $STUDY
$PY "$SKILL/scripts/extract_endpoints.py" $STUDY
$PY "$SKILL/scripts/render_action_map.py" $STUDY
$PY "$SKILL/scripts/verify_gameplan.py" $STUDY
$PY "$SKILL/scripts/write_manifest.py" $STUDY
$PY "$SKILL/scripts/render_brief.py" $STUDY
```

**Tip: feed the CSP header into the CSP fingerprinter.** `fingerprint_csp.py` will scan `raw/html/*.html` and `raw/network/sample_*.network-response` automatically, but the highest-leverage signal is the actual `content-security-policy:` HTTP response header, which is in your `get_network_request` tool output (text), not saved to disk by default. Best practice: after Phase 3, grep your transcript for `content-security-policy:` and **drop one full CSP value into `$STUDY/raw/network/csp-header.txt`** before running `fingerprint_csp.py`. One CSP header from any authed `/api/*` response typically exposes the SaaS's entire third-party allowlist (payments, database, analytics, support chat, tag manager, ad pixels, affiliate tracking, asset CDNs).

If `--redact` was passed, also:
```bash
$PY "$SKILL/scripts/redact_screenshot.py" $STUDY --redact "<arg>"
```

Each script writes to stderr what it produced. Surface any errors to the user.

### Phase 4 reality check: auto-render is a starting point, not the final brief

Two important caveats based on real-world usage:

1. **`render_brief.py` only sees what's in `derived/`.** The synthesis pipeline reads `network-summary.json`, `providers.json`, `tech-fingerprint.json`, `pricing.json`, `api-endpoints.json`. Anything you captured via inline `list_network_requests` (rather than dumping to JSON files) won't show up. Authed-app endpoints captured one-by-one during Phase 3b are typically MISSING from the auto-render unless you dumped them to `raw/network/*.json` first.

2. **Expect to hand-augment BRIEF.md.** The auto-render gives you the public-surface skeleton. The rich authed findings (per-route endpoints, app surface map, list-wrapper inconsistencies, auth-provider details from JWT decode) usually go in by hand. **Read the auto-rendered BRIEF.md, then overwrite it with the full picture**, including a verified §"App surface (left-nav)" table with the routes you walked in Phase 3a.2, and observed endpoints across all routes.

3. **ANALYSIS.md is where the interpretive load-bearing insights go.** BRIEF.md is the factual record; ANALYSIS.md is "what's clone-worthy, what's the moat, what would I do differently." Sections like *"The actual moat is X, not Y"*, *"If you were to build a competitor"*, *"Surprises that weren't predicted"* belong here, not in BRIEF.md.

## Wrap-up message

Tell the user:

- Study folder: `$STUDY`
- Top-line counts (from study.json `counts`)
- Suggest: `cat $STUDY/BRIEF.md` to read the brief, or "ask me anything about $domain, I'll read the study folder"

## First-run consent (verbatim text)

```
═════════════════════════════════════════════════════════════════
  AUTHED CAPTURE NOTICE: first-run consent

  Phase 3 will capture screenshots and HTML of pages while you're
  logged in. These will show your real name, email, and any data
  visible in the app at the time of capture.

  Defaults that protect you:
  - Studies save to your library root (./saas-library/ unless you
    pass --library-root), gitignored by default
  - Network logs are auto-scrubbed for Authorization/Cookie/JWT/keys
  - Session cookies are never dumped to disk
  - You can run with --no-authed to skip Phase 3 entirely

  Defaults you can opt into:
  - --redact "name=<your name>,email=<your email>" for screenshot blur
  - --no-screenshots to skip image capture entirely

  Proceed with authed capture? [Y/n]
═════════════════════════════════════════════════════════════════
```

## Network capture notes

The chrome-devtools MCP exposes network requests via `list_network_requests` (returns a list with IDs) and `get_network_request` (returns one request's full detail). It may not expose HAR export directly. If not, dump the full list-of-detail JSON to `raw/network/<phase>.json` instead of `.har`. The synthesis scripts accept both extensions.

## Stealth rules (do not violate)

- If a captcha (hCaptcha, Cloudflare "Just a moment", Datadome challenge) appears in any snapshot, halt and ask user to solve manually.
- If the public fetcher gets 403/429, do not retry aggressively. Back off, then ask user.
- If same domain studied <24h ago (folder exists for today), warn and ask before proceeding.
- Never `evaluate_script` to modify the page. Read-only DOM queries only.
- Never dump cookies, localStorage, or sessionStorage to disk.
- Never invent subdomains, never probe paths not visible in captured content.

## Idempotency

All scripts can be re-run. They read from the same study folder and overwrite their own outputs. If user wants to re-render BRIEF after editing the gameplan, they can re-run `render_brief.py` standalone.

## Observation vs Transformation (folder discipline)

The study folder is **pure observation**: raw HTML, network captures, screenshots, factual synthesis. Anything you create FROM the study (templates, code remixes, design transformations, build plans) goes in a **sibling `-derived/` folder**:

```
$LIBRARY/<domain>/
├── <YYYY-MM-DD>/             <- raw study (observation only)
│   ├── BRIEF.md              (factual)
│   ├── ANALYSIS.md           (optional, interpretive layer, clearly demarcated)
│   ├── raw/, extracted/, derived/, screenshots/, notes/
│   └── ...
└── <YYYY-MM-DD>-derived/     <- any transformation you build (templates, etc.)
```

`new_study.py` creates both folders. Don't put templates, opinion docs, or remixes inside the dated raw-study folder. Treat the study folder as "training data source": durable, ingestable, reproducible. Treat the `-derived/` folder as scratch space.

**ANALYSIS.md** is optional. Create it (alongside BRIEF.md) when you want to layer interpretive opinions (build-recreation guidance, "things that surprised me", strategic notes) without polluting the factual BRIEF. The brief renderer references it if present.

## Failure handling

If any Python script errors:

- Show the user the error
- Suggest: "study folder still has all raw evidence at $STUDY/raw/, can re-run synthesis once the issue is fixed"
- Do not auto-retry; do not modify the script automatically
