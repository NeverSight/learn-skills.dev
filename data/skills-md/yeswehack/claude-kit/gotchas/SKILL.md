---
name: gotchas
description: Reference table of per-class false-positive patterns, minimum proof requirements, and impact overclaim traps. Load this when a bug bounty report claims a specific vulnerability class. Apply only the section that matches the claimed class.
---

# Vulnerability-Class Gotchas

For each class: **minimum proof** (what the PoC must show), **common N/A**
(typical false positives that get auto-closed), **overclaim traps**
(impact claims that need extra evidence).

Apply only the section matching the report's claimed class.

---

## XSS

**Minimum proof**
- JS execution on **target origin** (`alert(document.domain)` proves it).
- Injection context stated: HTML body / attribute / JS / CSS / URL / JSON.
- Type stated: reflected / stored / DOM.

**Common N/A**
- `alert(1)` on `null` origin, sandboxed iframe, `data:` / `blob:` URL.
- Self-XSS.
- HTML injection without JS execution, unless tied to a real attack.
- XSS via a Markdown / template renderer the target doesn't actually use.
- `javascript:` href requiring the victim to manually paste the URL.

**Overclaim traps**
- "Session theft" claim but cookie is `HttpOnly` — JS can't read it.
- "Account takeover" without a PoC that actually takes over an account.
- "CSP bypass" without showing the CSP header and the bypass technique.

---

## SQLi

**Minimum proof** (one of)
- Data extraction: sentinel value, table name, DB version returned.
- Time-based: controlled `SLEEP(n)` payload, multiple runs at varying `n`.
- Boolean-based: controlled true/false oracle with response differential.

**Common N/A**
- WAF blocked the payload → "SQLi confirmed". The WAF blocked; that's it.
- Error message mentioning SQL without controlled injection.
- Generic HTTP 500 on quote characters (could be many things).
- DB banner / version leaked without proving injection.

**Overclaim traps**
- "Full database compromise" without dumping a controlled sentinel row.
- Don't escalate the PoC into destructive or intrusive post-exploitation
  to "prove" impact. A confirmed injection (sentinel value, controlled
  time-delay, boolean oracle) is enough — stop there. Dumping the whole
  DB, chaining to `xp_cmdshell` / `INTO OUTFILE`, or writing files goes
  past proof into damage and can breach the program rules. Prove the
  primitive, describe the impact, don't exercise it.

---

## SSRF

**Minimum proof**
- Inbound request observed on hunter-controlled endpoint (Burp
  Collaborator, webhook.site, hunter's server). Include the inbound log.
- For blind SSRF: time-based confirmation with multiple controlled hosts.
- Reach demonstrated: at least one of internal hostname, cloud metadata
  (169.254.169.254), localhost service, or protocol smuggling (file://,
  gopher://, dict://). Collab hit alone is not enough.
- Response data exfiltrated if claimed (internal endpoint content shown).

**Common N/A**
- DNS resolution only — proves lookup, not HTTP request.
- Blind SSRF to attacker-controlled domain only, no reach demonstrated.
  Legitimate webhooks / link previews / image proxies make outbound
  HTTP too.
- SSRF to public domains only.
- Request blocked by WAF / library / network policy.

**Overclaim traps**
- "Cloud metadata access" without showing the metadata response body.
- "Internal network scan" without one successful internal hit.
- "Blind SSRF" claimed High/Critical without demonstrated reach →
  typically Low or N/A.

---

## IDOR / BOLA

**Minimum proof**
- Two hunter-controlled accounts, A and B.
- Account A reads / modifies / deletes a resource belonging to B.
- Response containing B's data shown, with B's identifier visible.

**Common N/A**
- Sequential / predictable IDs without showing actual access.
- Reading own data via someone else's ID (same effective access level).
- Resources that are public by design.
- Admin endpoints accessible only to admins (not broken).

**Overclaim traps**
- "Mass account takeover" without showing the takeover primitive on B.
- Single-account "discovery" with cross-tenant impact claims but no
  second tenant tested.
- Non-guessable identifier (random UUIDv4, HMAC, long opaque token)
  scored as if IDs were enumerable. If an attacker can't discover a
  victim's ID at scale, exploitation needs the ID to leak elsewhere —
  score `AC:H` and say where the ID would come from. Don't claim mass
  exploitation off a single self-owned resource whose ID you already
  knew. Sequential / short / predictable IDs are the ones that justify
  `AC:L`.

---

## CSRF

**Minimum proof**
- Working PoC HTML page (hosted or pasted in full) that, when visited by
  an authenticated victim, performs the sensitive action.
- The action must be sensitive (state change, privilege grant, data
  modification — not logout, not search).
- SameSite cookie status verified — `Lax` blocks most cross-site POSTs;
  the PoC must work despite it.

**Common N/A**
- CSRF on logout, search, or other low-impact actions.
- "No CSRF token present" without showing exploitation.
- `SameSite=Lax/Strict` cookies blocking the cross-site request.

**Overclaim traps**
- "Account takeover via CSRF" without a chain that actually takes over.
- Rating a CSRF by the *mechanism* rather than the *action*. The
  severity is capped by what the forced action is worth. CSRF on a
  reversible, low-value state change (add item to cart, toggle a UI
  preference, change display name) is **Low** even with a perfect PoC.
  High severity needs a genuinely sensitive action: email/password
  change, fund transfer, privilege grant, deletion of the victim's data.

---

## RCE

**Minimum proof** (one of)
- In-band command output (`id`, `whoami`, `hostname`).
- Out-of-band callback to hunter-controlled endpoint with a unique
  payload-specific marker.
- Injection point and payload shown literally.

**Common N/A**
- "Suspicious behavior on payload submission" without command execution.
- Stack trace mentioning `system()` / `exec()` without controlled execution.
- Theoretical RCE via a vulnerable dependency without proving reachability
  in the application's code path.

**Overclaim traps**
- "Full server compromise" without showing the privilege level. Prove
  execution with a harmless marker (`id`, `whoami`, `hostname`, or an
  OOB callback) and stop. Do not pivot, escalate privileges, move
  laterally, read other users' data, or run destructive commands to
  "demonstrate" reach — that's past proof and into damage, and it
  breaches most program rules. Report the execution primitive; describe
  the impact without exercising it.
- "RCE" that's actually code injection in a sandboxed context (sandboxed
  template engine, browser-side eval — that's XSS, not RCE).

---

## SSTI

**Minimum proof**
- Template syntax confirmed (`{{7*7}}` → `49`, `<%=7*7%>` → `49`, etc.).
- Template engine identified (Jinja2, Twig, Velocity, Freemarker, ...).
- Sandbox escape shown if the engine is sandboxed.
- For RCE impact: see RCE section minimum proof.

**Common N/A**
- HTML / text reflection of `{{7*7}}` as a literal string (no evaluation).
- Math eval in a sandboxed expression engine without an escape path.

**Server-side vs client-side**
- `{{7*7}}` → `49` in a **client-side** framework (Angular, Vue) is
  **CSTI**, not server-side SSTI. Its impact is **XSS** (JS execution
  in the browser), not server RCE — report it as XSS and prove JS
  execution accordingly. Don't claim server compromise from a
  client-side template evaluation.

---

## XXE

**Minimum proof**
- External entity defined and resolved.
- File read: content of a known file returned (e.g. `/etc/passwd`).
- Or OOB: callback with file content base64'd or named entity.

**Common N/A**
- XML parser accepts external DTD references but does not resolve entities.
- Error mentioning entity processing without a controlled file read.

**Do not**
- Demonstrate impact with an entity-expansion bomb (billion laughs /
  quadratic blowup). That's a DoS against the target — excluded by most
  programs and a rules violation, not an XXE proof. Prove XXE with a
  controlled file read or an OOB callback instead.

---

## Open Redirect

**Minimum proof**
- Single URL that redirects to a hunter-controlled domain.
- The redirect mechanism sits on a security-relevant path: auth callback,
  OAuth `redirect_uri`, password reset link, login flow.
- A chain showing real impact (OAuth token theft, credential phishing
  leveraging the program's domain reputation).

**Common N/A**
- Open redirect on non-security-sensitive paths with no chain.
- Redirect requiring the victim to manually paste a URL.
- Same-origin redirects.

**Overclaim traps**
- Claiming token/code theft via an OAuth/OIDC `redirect_uri` you can't
  actually PoC. If proving the token leak requires an authenticated
  account (or the IDP's real consent flow) you don't have, the impact
  is **theoretical and non-reproducible** — a triager can't replay it,
  so it isn't valid. Either obtain an account and show the token
  landing on your endpoint, or report only the redirect you can prove
  (typically Low) and state plainly the ATO chain is unverified.

---

## Auth Bypass

**Minimum proof**
- Specific endpoint or flow accessed without the required auth state.
- Endpoint is sensitive (admin, paid feature, other user's data).
- Bypass mechanism shown (request manipulation, missing header,
  modified parameter, parser confusion).

**Common N/A**
- Endpoint returns data also available unauthenticated by design.
- "Bypass" using test credentials the program intentionally exposes.
- Public endpoints documented as such in API docs.
- Reaching a protected **route** that only renders the client-side app
  shell. Loading `/admin` and seeing the SPA's JS/HTML render is not a
  bypass — the framework serves the bundle to everyone and the API
  calls behind it still return 401/403. You must show a **protected
  action or data** actually returned without auth (an admin API
  responding with real data, a privileged operation succeeding). "The
  page loads" is not an impact.

---

## Information Disclosure / Secret Leak

Covers leaked secrets found anywhere: JS bundles, HTML/source comments,
API responses, git/config exposure, and **secrets hardcoded in mobile
apps** (decompiled APK/IPA, strings, `strings.xml`, embedded config).

**Minimum proof**
- The exact location the secret was found (file, URL, decompiled path).
- The secret is **still valid** — show one authenticated call that
  succeeds with it (a `200` on an endpoint that requires it), with the
  secret redacted in the report.
- The concrete access it grants: what data or action the key/token
  unlocks. Impact = what the *valid* credential can actually do.

**Common N/A**
- **Public / publishable keys that are meant to be client-side.**
  Google Maps browser keys, Firebase `apiKey` config, Stripe
  publishable `pk_...`, Sentry DSNs, reCAPTCHA site keys, Mixpanel/
  analytics tokens. These are *designed* to ship in the client — a
  leak isn't a finding unless you prove a real, non-intended capability
  (e.g. an unrestricted Maps key billing abuse, or a Firebase config
  with wide-open security rules — and then the finding is the open
  rules, proven separately).
- Expired, revoked, or already-rotated credentials.
- "A key is present in the JS" with no test that it's live or
  privileged.
- Placeholder / example / test values (`sk_test_...`, `changeme`,
  documented sample keys).

**Overclaim traps**
- Reporting the *presence* of a secret as impact. The impact is what
  the secret does when used — if you didn't (safely) confirm it works
  and what it reaches, you haven't proven a finding.
- Treating any long random string as a "leaked secret" without
  identifying what it authenticates.

---

## Race Condition

**Minimum proof**
- A broken invariant under concurrency: the same operation, sent in
  parallel, produces a result impossible under sequential execution
  (a one-time coupon applied N times, a balance credited twice, a
  single-use token consumed more than once, a limit of 1 exceeded).
- The concurrency method stated: single-packet attack (HTTP/2
  last-byte sync), Turbo Intruder, or parallel clients — with the
  number of concurrent requests.
- Before / after state shown: the pre-state, the concurrent burst,
  and the persisted post-state that proves the invariant broke (final
  balance, ledger row, redemption count) — not just several `200`s.

**Common N/A**
- "Sent 100 requests fast, several succeeded" without showing a broken
  invariant. Multiple successes on an endpoint with no per-user limit
  are just multiple successes.
- Duplicate submissions on an idempotent endpoint (no state effect).
- Different response times / jitter mistaken for a race.
- Rate-limit bypass with no concrete state impact — that's a
  rate-limit finding, not a race, and is often out of scope on its own.
- Hammering that degrades the service — that's DoS (excluded), not a
  race PoC.

**Overclaim traps**
- Claiming double-spend / balance inflation from two `200` responses
  without showing the *persisted* state changed. The proof is the
  final ledger / balance, not the response codes.
- Reporting one lucky duplicate as reliable exploitation. A race needs
  a reproducible win — state the win rate and attempts to land it.
- Scaling the burst into thousands of requests to "prove" it. A small
  concurrent burst that breaks the invariant is the proof; volume past
  that is abuse, not evidence.

---

## CORS Misconfiguration

**Minimum proof**
- The response reflects an attacker-controlled `Origin` in
  `Access-Control-Allow-Origin` **and** returns
  `Access-Control-Allow-Credentials: true`.
- The endpoint returns **session-authenticated, sensitive data** tied
  to the victim's cookies (their profile, token, private records).
- A working PoC page hosted on the attacker origin that does
  `fetch(url, {credentials:'include'})`, reads the response
  cross-origin, and shows the victim's actual data exfiltrated — not
  just the headers.

**Common N/A** (this is where most CORS reports die)
- `ACAO: *` **without** `ACAC: true`. The browser refuses to send
  credentials to a wildcard origin, so a credentialed read is
  impossible — a public endpoint returning `*` leaks nothing an
  attacker couldn't already fetch server-side. Not a finding alone.
- Reflected `Origin` but the endpoint returns only public /
  unauthenticated data. No secret crosses the boundary.
- `ACAC: true` with a **fixed, trusted** `ACAO` (not reflected, not
  attacker-controlled).
- Preflight (`OPTIONS`) reflecting the origin while the actual
  `GET`/`POST` doesn't, or the real response body carries nothing
  sensitive.
- "`null` origin allowed" with no PoC — exploiting `null` needs a
  sandboxed iframe; show it working.
- API authenticated by a **bearer token in a header**, not cookies —
  CORS reflection doesn't hand the attacker the token, and the browser
  won't attach it cross-origin. No credentialed session to steal.

**Overclaim traps**
- "Account takeover via CORS" without a PoC page that actually reads
  victim data. The impact is exactly what the misconfigured endpoint
  returns to a credentialed cross-origin read — name the endpoint and
  show the data.
- Scoring High off header reflection alone. No credentialed
  sensitive-data read demonstrated = no impact = typically N/A.

---

## Path Traversal / LFI

**Minimum proof**
- A file **outside the intended directory** retrieved, content shown
  (`/etc/passwd`, `win.ini`, or an app config / source file the
  endpoint must not serve).
- The exact parameter and payload shown literally, including the
  encoding that worked (`../`, `%2e%2e%2f`, `....//`, absolute path,
  null-byte truncation).
- Traversal (arbitrary read via `../`) and LFI (include/execute a
  file) kept distinct. If code execution is claimed (log poisoning,
  PHP `php://filter` / wrapper chain, session-file inclusion), show
  the executed output — not just the file read.

**Common N/A**
- Reading a file **inside** the intended served directory (a download
  endpoint serving its own public files) — that's by design.
- `403` / `404` / `500` on `../` payloads with no file returned. An
  error is not a read.
- Filename reflected in an error message without content disclosure.
- Retrieving a non-sensitive file with no security value.
- Payload visibly blocked / normalized by the framework or WAF (show
  it actually resolving to file content).

**Overclaim traps**
- "Arbitrary file read = RCE" without a demonstrated execution path.
  LFI→RCE needs a proven include-and-execute primitive (log / session
  poisoning, wrapper chain); absent that, it's file disclosure, score
  it as such.
- "Any file on the server" inferred from one `/etc/passwd`. State what
  the process user can actually read — a private key or app secret
  proves impact; `/etc/passwd` alone is usually just the confirmation
  primitive.
- Dumping many sensitive files or other users' data to "prove" reach.
  One representative sensitive file proves it; mass exfiltration is
  past proof and into damage.

---

## Class not listed?

Apply general PoC and impact rigor (see `triage`). The report
should clearly explain the class and its impact model in its first
paragraph since the triager won't have a class-specific mental model
to fall back on.
