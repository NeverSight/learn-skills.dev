---
name: attack-surface-xss
description: Reconnaissance skill for XSS attack surface — analyzes headers, frameworks, JS libraries, and DOM patterns at a URL to map what makes XSS possible or harder. For ethical hackers preparing for XSS testing.
disable-model-invocation: true
aliases:
  - xss-recon
  - xss-surface
  - xss-attack-surface
version: 0.0.1
author: Herman Stevens
tags: [security, xss, reconnaissance, attack-surface, web-security]
allowed-tools: [Bash, WebFetch, Read, Grep, Glob]
---

# XSS Attack Surface Reconnaissance

Map the XSS attack surface of a target URL. Analyze security headers, client-side frameworks, JavaScript patterns, and DOM structure to identify what makes XSS possible, easier, or harder.

**This skill does NOT inject payloads or test for XSS.** It performs passive observation only (HTTP requests + source analysis). For active XSS testing, use `/xss-finder`.

**Target:** $ARGUMENTS (URL to analyze)

## When to Use This Skill

- Before running `/xss-finder` — understand what defenses exist
- Scoping an XSS engagement — identify highest-value test targets
- Evaluating a site's XSS posture without active testing
- Mapping client-side technology stack for exploit development
- Identifying which XSS classes (reflected, stored, DOM) are most likely

## Core Capabilities

| Capability | Description |
|------------|-------------|
| Header Assessment | CSP, X-Content-Type-Options, cookie flags, charset |
| Framework Detection | React, Angular, Vue, jQuery + version extraction |
| Vulnerable Library Detection | Known CVEs per detected library version |
| DOM XSS Source/Sink Mapping | innerHTML, eval, location.hash, postMessage |
| Input Vector Enumeration | Forms, hidden fields, URL parameter reflection |
| Attack Priority Ranking | Ordered list of where to focus XSS testing |

## Workflow

### Phase 1: Fetch Target

Retrieve response headers and page content from $ARGUMENTS:

```bash
# Response headers (follow redirects)
curl -sI -L "$URL"

# Full page body (HTML + inline JS)
curl -sL "$URL" -o /tmp/xss-recon-body.html
```

Use WebFetch as fallback for JavaScript-rendered content (SPAs that return minimal HTML).

**Extract script references:**
1. Parse all `<script>` tags — capture both inline content and external `src` URLs
2. Fetch external JS files from same-origin and known CDNs (jsdelivr, cdnjs, unpkg, googleapis)
3. Cap at 20 external files to avoid excessive fetching
4. Store fetched JS content for Phase 4 analysis

**Record metadata:**
- Final URL after redirects (HTTP → HTTPS upgrade?)
- Response status code
- Server header value
- Number of redirects

### Phase 2: Security Headers Assessment

Check each header and rate its XSS impact:

| Header | Check | XSS Impact |
|--------|-------|------------|
| `Content-Security-Policy` | Present? `unsafe-inline`? Wildcards? Bypass CDNs? | Primary XSS defense |
| `Content-Security-Policy-Report-Only` | Non-enforcing — intel only | Shows intended policy |
| `X-Content-Type-Options` | `nosniff` present? | Blocks MIME-confusion script execution |
| `X-XSS-Protection` | Deprecated; `0` = deliberately disabled | Legacy posture indicator |
| `Referrer-Policy` | Data leak control | Referer-based injection intel |
| `Permissions-Policy` | Feature restrictions | Limits attack surface |
| `Content-Type` | Charset specified? | Missing charset enables UTF-7/ISO-2022-JP XSS |
| `Set-Cookie` | HttpOnly, Secure, SameSite flags | Cookie theft feasibility |

**CSP quick assessment (inline):**
- Missing CSP → flag as critical gap, all inline injection viable
- `unsafe-inline` in script-src → inline script injection works directly
- `unsafe-eval` → eval-based payloads viable
- Wildcard `*` or `data:` in script-src → script loading from any origin
- Known bypass CDNs allowlisted (googleapis, cdnjs, jsdelivr, unpkg) → JSONP/Angular bypasses
- `strict-dynamic` present → script gadget focus, not direct injection
- Trusted Types → DOM sink restrictions active

For deep CSP analysis, recommend running `/content-security-policy $URL`.

**Cookie assessment:**
- Missing `HttpOnly` → `document.cookie` exfiltration works
- Missing `Secure` → network MITM can steal cookies
- Missing `SameSite` → CSRF + XSS chaining viable
- All flags present → cookie theft blocked, pivot to DOM-based exfiltration

### Phase 3: Framework & Library Detection

Detect client-side stack from page source, script content, and global objects.

**Frameworks — detection signatures:**

| Framework | Detection Patterns |
|-----------|--------------------|
| React | `data-reactroot`, `_reactRootContainer`, `__REACT_DEVTOOLS`, `react.production.min.js` |
| Angular | `ng-app`, `ng-version` attribute, `angular.js`/`angular.min.js` in script src |
| Vue | `data-v-` attributes, `__VUE__`, `vue.js`/`vue.min.js` in script src |
| jQuery | `jquery.min.js` in script src, `jQuery` or `$` assignment in inline scripts |
| Next.js | `__NEXT_DATA__` script tag, `_next/static` paths |
| Nuxt | `__NUXT__` global, `_nuxt/` paths |
| Svelte | `svelte` in script paths, `__svelte` |
| Ember | `ember.js` in script src, `data-ember-` attributes |
| Backbone | `backbone.js` in script src |

**Security libraries — detect sanitizers:**

| Library | Detection | Notes |
|---------|-----------|-------|
| DOMPurify | `dompurify` in script src/content, `DOMPurify.sanitize` calls | Check version — mXSS bypasses per version |
| sanitize-html | `sanitize-html` in script paths | Server-side usually, may appear in bundles |
| Helmet.js | Infer from header patterns (X-DNS-Prefetch-Control, X-Content-Type-Options set together) | Server-side only |
| Trusted Types | `require-trusted-types-for` in CSP, `trustedTypes` API usage | Browser-enforced sink protection |

**Vulnerable library detection — extract versions from filenames and CDN URLs:**

| Library | Vulnerable Versions | XSS-Relevant Issue |
|---------|--------------------|--------------------|
| jQuery < 3.5.0 | `jquery-3.2.1.min.js`, CDN path version | `$.htmlPrefilter` XSS (CVE-2020-11022, CVE-2020-11023) |
| Angular < 1.6.x | `angular.js/1.5.8/` in CDN URL | Template sandbox escape: `{{$on.constructor('alert(1)')()}}` |
| DOMPurify < 2.4.0 | `dompurify/2.3.x/` in CDN URL | mXSS via SVG+style namespace confusion |
| lodash < 4.17.21 | `lodash/4.17.x/` in CDN URL | Prototype pollution gadgets → XSS chain |
| Handlebars < 4.7.7 | `handlebars/4.7.x/` in CDN URL | Prototype pollution → template injection |
| Moment.js | Any version | ReDoS, often bundled with vulnerable deps |

For each detected library: report version, known XSS-relevant CVEs, and specific exploitation notes.

### Phase 4: JavaScript Pattern Analysis

Analyze inline scripts and fetched JS files for dangerous patterns.

**DOM XSS Sinks** (code that writes to DOM unsafely):

| Sink | Pattern | Risk Level |
|------|---------|------------|
| `innerHTML` | `el.innerHTML = ...` | High — direct HTML injection |
| `outerHTML` | `el.outerHTML = ...` | High — replaces entire element |
| `document.write()` | `document.write(...)` | High — writes to document stream |
| `document.writeln()` | `document.writeln(...)` | High — same as write with newline |
| `insertAdjacentHTML()` | `el.insertAdjacentHTML(...)` | High — injects HTML at position |
| `eval()` | `eval(...)` | Critical — arbitrary code execution |
| `Function()` | `new Function(...)` | Critical — creates function from string |
| `setTimeout(string)` | `setTimeout("...", ...)` | High — eval equivalent |
| `setInterval(string)` | `setInterval("...", ...)` | High — eval equivalent |
| `$.html()` | `$(sel).html(...)` | High — jQuery innerHTML wrapper |
| `$(user_input)` | `$(location.hash)` | Critical — jQuery selector injection |
| `v-html` | `v-html="..."` directive | High — Vue raw HTML binding |
| `dangerouslySetInnerHTML` | `dangerouslySetInnerHTML={{...}}` | High — React raw HTML |
| `location.href =` | `location.href = ...` | Medium — open redirect → XSS chain |
| `location.assign()` | `location.assign(...)` | Medium — redirect sink |
| `location.replace()` | `location.replace(...)` | Medium — redirect sink |
| `window.open()` | `window.open(...)` | Medium — navigation sink |
| `navigation.navigate()` | `navigation.navigate(...)` | Medium — Chrome navigation API |
| Dynamic `import()` | `import(...)` | High — module loading sink |

**DOM XSS Sources** (where attacker input enters):

| Source | Pattern | Notes |
|--------|---------|-------|
| `location.hash` | `location.hash`, `window.location.hash` | Fragment — not sent to server |
| `location.search` | `location.search`, `URLSearchParams` | Query string |
| `location.href` | `location.href` (read) | Full URL including fragment |
| `document.referrer` | `document.referrer` | Attacker-controlled via link |
| `window.name` | `window.name` | Persists across navigations |
| `document.cookie` | `document.cookie` (read) | If attacker can set cookies |
| `postMessage` | `addEventListener('message', ...)` | Check origin validation |
| `localStorage` | `localStorage.getItem(...)` | Persistent, attacker-settable |
| `sessionStorage` | `sessionStorage.getItem(...)` | Session-scoped |
| `URL()` constructor | `new URL(...)`, `url.searchParams` | Parameter parsing |

**Source-to-sink tracing (static approximation):**
For each detected source, trace whether it flows into a sink without sanitization. Flag direct connections (e.g., `el.innerHTML = location.hash`). Note: full taint analysis requires browser DevTools or dynamic instrumentation — this is a best-effort static scan.

**Dangerous constructs:**

| Construct | Pattern | XSS Relevance |
|-----------|---------|---------------|
| Global variable declarations | `var config = ...` on window | DOM clobbering targets (see `dom-clobbering` anti-pattern) |
| Prototype pollution gadgets | `Object.assign`, `$.extend`, `_.merge` with user input | Gadget chain → XSS |
| JSONP endpoints | `callback=` parameter in script src | Arbitrary JS execution via callback |
| postMessage without origin check | `addEventListener('message', fn)` without `event.origin` validation | Any origin can inject data |
| Template literal injection | `` `...${userInput}...` `` in dangerous contexts | String interpolation into sinks |
| `with` statements | `with(obj) { ... }` | Scope confusion, clobbering |
| Relative script loading | `<script src="./app.js">` | RPO vulnerability — path confusion |

### Phase 5: DOM & HTML Analysis

Analyze page structure for XSS-relevant features.

**Input vectors:**
- Enumerate all `<input>`, `<textarea>`, `<select>` elements (visible + hidden)
- Record `name`, `type`, `id`, `maxlength`, `pattern` attributes
- Map forms to their `action` URLs and `method` (GET/POST)
- Flag hidden fields — often unsanitized server-side (reference xss-finder hidden field methodology)
- Flag file upload forms — SVG upload → stored XSS potential

**URL parameter reflection test:**
For each URL parameter in $ARGUMENTS, check if value appears in response body. If reflected, note the reflection context (HTML body, attribute, script, comment).

**Meta tags:**

| Tag | Check | XSS Impact |
|-----|-------|------------|
| `<meta charset>` | Missing? | Enables charset-based XSS (ISO-2022-JP, UTF-7) |
| `<meta http-equiv="Content-Security-Policy">` | Present? | Meta CSP — limited (no `frame-ancestors`, no `report-uri`) |
| `<meta http-equiv="refresh">` | User-controllable URL? | Redirect vector |

**Embedding elements:**
- `<iframe>` — sandboxed? Is `src` user-controllable?
- `<object>`, `<embed>` — plugin execution vectors
- Inline `<svg>` — enables advanced XSS vectors (`onbegin`, SMIL `<animate>`)
- `<math>` — MathML namespace confusion for mXSS (reference `mutation-xss` anti-pattern)

**Inline event handlers:**
Count existing inline event handlers (`onclick`, `onerror`, `onload`, etc.) in page source. High count indicates the framework does not prohibit inline handlers — weak or absent CSP likely.

**Third-party embeds:**
- Google Tag Manager (`gtm.js`) — tag injection surface
- Analytics scripts (Google Analytics, Mixpanel, Segment) — config manipulation
- Ad network scripts — additional injection surface
- Social widgets — cross-origin messaging

### Phase 6: Report Generation

Generate a structured report organized for ethical hacker workflow:

```markdown
# XSS Attack Surface Report

**Target:** {URL}
**Date:** {date}
**Overall XSS Resistance:** {Strong | Moderate | Weak | Minimal}

## Executive Summary
{2-3 sentences: key findings, biggest weaknesses, recommended testing focus}

## Security Headers

| Header | Value | XSS Impact | Assessment |
|--------|-------|------------|------------|
| CSP | {value or MISSING} | {impact} | {Strong/Weak/Missing} |
| X-Content-Type-Options | {value or MISSING} | {impact} | {OK/Missing} |
| Set-Cookie | {flags or MISSING} | {impact} | {assessment} |
| ... | | | |

**Hacker Notes:** {Specific header weaknesses — e.g. "CSP has unsafe-inline, inline
script injection works directly" or "No HttpOnly on session cookie, document.cookie
exfiltration viable"}

## Technology Stack

| Component | Version | XSS Relevance |
|-----------|---------|---------------|
| {library} | {version} | {specific CVE or known bypass} |

**Hacker Notes:** {Which libraries have known bypasses, specific payloads to try}

## Dangerous JavaScript Patterns

### DOM XSS Sinks Found
| Sink | Location | Source Connected | Risk |
|------|----------|-----------------|------|
| innerHTML | inline script line 42 | location.hash | High — direct DOM XSS |
| $.html() | app.js:156 | AJAX response | Medium — depends on server sanitization |

### DOM XSS Sources Found
| Source | Handler | Origin Check | Risk |
|--------|---------|--------------|------|
| postMessage | addEventListener line 88 | No | High — any origin can inject |
| location.hash | hashchange handler | N/A | Medium — client-only input |

### Dangerous Constructs
{DOM clobbering targets, prototype pollution gadgets, JSONP endpoints, relative paths}

**Hacker Notes:** {Specific source→sink chains to investigate, bypass techniques from
xss-finder 5-Rotor methodology}

## Input Vectors

| Input | Type | Reflected | Hidden | Notes |
|-------|------|-----------|--------|-------|
| q | text | Yes | No | Search param reflected in <h1> |
| token | hidden | No | Yes | Likely unsanitized — test stored XSS |

**Hacker Notes:** {Which inputs to fuzz first, client-side restrictions to bypass}

## Best Practices Assessment

| Practice | Status | Hacker Implication |
|----------|--------|--------------------|
| CSP with nonce/hash | {Present/Missing} | {implication for inline injection} |
| HttpOnly cookies | {Present/Missing} | {cookie theft feasibility} |
| DOMPurify/sanitizer | {Present/Missing (version)} | {mXSS bypass options} |
| Trusted Types | {Present/Missing} | {sink restriction status} |
| Subresource Integrity | {Present/Missing} | {CDN MITM feasibility} |
| Meta charset | {Present/Missing} | {charset-based XSS feasibility} |

## Attack Vectors Summary

### High Priority (Test First)
1. {Most promising vector with technique reference}
2. {Second most promising}
3. {Third}

### Medium Priority
1. {Vector with conditional exploitability}
2. ...

### Low Priority (Hardened)
1. {Defended vector — explain what makes it hard}
2. ...

## Recommended Next Steps
1. Run `/xss-finder $URL` for automated payload testing on identified vectors
2. Run `/content-security-policy $URL` for deep CSP analysis
3. {Specific manual tests based on findings — e.g. "Test postMessage handler at
   line 88 with origin-less messages", "Fuzz hidden field 'token' for stored XSS"}
```

**Overall XSS Resistance rating:**
- **Strong** — CSP with nonce + Trusted Types + sanitizer + HttpOnly cookies + no dangerous sinks
- **Moderate** — CSP present but with gaps (e.g. unsafe-inline) OR sanitizer present but outdated
- **Weak** — Missing CSP or CSP with wildcards, dangerous sinks present, no sanitizer
- **Minimal** — No CSP, no sanitizer, dangerous sinks connected to sources, no HttpOnly

Each finding must reference specific exploitation techniques. Link to xss-finder 5-Rotor methodology where relevant (context detection, bypass cascades, encoding techniques).

## Implementation Steps

1. Validate $ARGUMENTS is a URL (starts with `http://` or `https://`)
2. Fetch headers with `curl -sI -L`; fetch body with `curl -sL`
3. Fall back to WebFetch if body is minimal (SPA detection)
4. Extract and fetch external script files (same-origin + CDNs, max 20)
5. Assess security headers per Phase 2 table
6. Detect frameworks and libraries; extract versions from filenames/CDN URLs
7. Cross-reference versions against known vulnerable ranges
8. Scan inline + external JS for DOM XSS sinks and sources
9. Trace source→sink connections (static approximation)
10. Enumerate input elements, forms, hidden fields
11. Test URL parameter reflection in response body
12. Check meta tags, embedding elements, inline event handler count
13. Calculate overall XSS resistance rating
14. Generate report with Hacker Notes per section

## Quality Checklist

Before finalizing:
- [ ] All 6 phases executed (Fetch, Headers, Frameworks, JavaScript, DOM, Report)
- [ ] Security headers table complete — every header checked or marked MISSING
- [ ] Framework/library versions extracted where detectable
- [ ] Vulnerable library versions cross-referenced with specific CVEs
- [ ] DOM XSS sinks and sources enumerated from actual page content
- [ ] Source→sink connections flagged where statically traceable
- [ ] Input vectors include hidden fields
- [ ] URL parameter reflection tested
- [ ] Overall XSS Resistance rating justified by findings
- [ ] Hacker Notes in every report section with actionable exploitation guidance
- [ ] Attack Vectors Summary prioritized by exploitability
- [ ] Next Steps reference `/xss-finder` and `/content-security-policy`
- [ ] No active exploitation performed — reconnaissance only

## Example Usage

**Single URL reconnaissance:**
```
/xss-recon https://example.com/search?q=test
```

**Application homepage:**
```
/xss-surface https://app.example.com
```

**Pre-engagement scoping:**
```
/xss-attack-surface https://target.com/login
```

## References

- [OWASP Testing Guide: XSS](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/07-Input_Validation_Testing/01-Testing_for_Reflected_Cross_Site_Scripting)
- [OWASP DOM-Based XSS Prevention](https://cheatsheetseries.owasp.org/cheatsheets/DOM_based_XSS_Prevention_Cheat_Sheet.html)
- [PortSwigger: XSS Cheat Sheet](https://portswigger.net/web-security/cross-site-scripting/cheat-sheet)
- [CWE-79: Improper Neutralization of Input During Web Page Generation](https://cwe.mitre.org/data/definitions/79.html)
- [MDN: Content-Security-Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy)
- [Gareth Heyes: JavaScript for Hackers](https://leanpub.com/javascriptforhackers)
- [Retire.js: Known Vulnerable Libraries](https://retirejs.github.io/retire.js/)
- [Snyk Vulnerability Database](https://security.snyk.io/)

## Related Skills

- [Content Security Policy](../content-security-policy/): Deep CSP analysis — delegate with `/content-security-policy $URL`
- [XSS Finder](../xss-finder/): Active XSS testing — run after reconnaissance with `/xss-finder $URL`
- [Cross-Site Scripting (XSS)](../security-anti-patterns/xss/): Reflected, stored, and DOM XSS patterns
- [DOM Clobbering](../security-anti-patterns/dom-clobbering/): Global variable clobbering detection
- [Mutation XSS](../security-anti-patterns/mutation-xss/): Sanitizer bypass via mXSS
- [Missing Security Headers](../security-anti-patterns/missing-security-headers/): Header assessment baseline
