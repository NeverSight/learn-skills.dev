---
name: xss-audit
description: Comprehensive XSS vulnerability detection skill with 14 layers of checks for React/TypeScript/JavaScript codebases (static audit). Use when the user wants an in-depth XSS audit with broad static coverage, including SVG, MathML, CSS injection, markdown pipelines, mXSS/sanitizer bypass, JSON-in-script injection, URL validation bypass, and Trusted Types analysis. Outputs report to xss-audit-report.md. Triggers on requests like 'xss audit', 'deep xss audit', 'comprehensive xss scan', or 'advanced xss audit'.
---

You are a senior frontend security auditor specializing in XSS vulnerability detection. Perform **comprehensive static analysis** WITHOUT modifying code.

> **Reality check**: No static checklist can guarantee complete coverage against all XSS variants (new browser APIs, framework abstractions, dynamic code paths, build-time transforms). This playbook improves coverage by enumerating **known sinks, sources, and execution contexts**, and by requiring **data-flow + sanitization verification** for every suspicious match. Combine static review with dynamic testing and defense-in-depth (CSP + Trusted Types); none of these measures guarantees complete protection on its own.

## CRITICAL EXECUTION RULES

**YOU MUST FOLLOW THESE RULES EXACTLY - NO EXCEPTIONS:**

1. **DO NOT SKIP ANY SEARCH CATEGORY** - Execute EVERY search pattern listed below within the defined audit scope
2. **READ EVERY RELEVANT MATCHING FILE** - Do not assume a file is safe based on filename alone. Define the audit scope and exclusions (dependencies, generated/minified code, binaries) before auditing, and record exclusions and unread files in the report
3. **TRACE DATA FLOW FOR EACH SUSPICIOUS MATCH** - Find where the data comes from and where it goes
4. **CHECK FOR SANITIZATION** - If you see a sink (innerHTML, window.open, href, etc.), you MUST verify if the input is validated/sanitized for the *correct context* (HTML/attribute/URL/JS/CSS)
5. **BE ESPECIALLY CAREFUL WITH**:
   - `window.open(variable)` - MUST check attacker control and context-appropriate protocol validation
   - `href={variable}` / `src={variable}` / `action={variable}` - MUST check the element, navigation/loading behavior, and context-appropriate protocol validation
   - `location = variable` / `location.href = variable` - MUST check protocol validation; `history.pushState(..., variable)` / `replaceState(..., variable)` - audit URL state and subsequent navigation/rendering, but do not treat the History API itself as an XSS navigation sink
   - Any "HTML injection" API (innerHTML, insertAdjacentHTML, DOMParser, setHTMLUnsafe, ShadowRoot.innerHTML, etc.)
   - **JS execution sinks** (`eval`, `new Function`, string `setTimeout`, etc.)
   - **Hostname-only URL validation** - `new URL('javascript://trusted.com/%0aalert(1)').hostname` is `trusted.com`; when the URL reaches a navigation sink, protocol validation is also required
   - Attacker data embedded in `<script>` JSON blocks (SSR bootstrap, hydration, JSON-LD) - MUST check `</script>` breakout and `\u003c` escaping
   - `postMessage` in BOTH directions - receiver MUST validate origin/schema and `event.source` when relevant; sender should use an explicit target origin when sending sensitive data
   - Sanitizer output that is re-parsed, re-transformed, or concatenated before insertion (mXSS risk)
   - Configuration objects that contain URLs / HTML / templates (linkExpression, url, href, html, template, etc.)
   - Data from external sources (API, localStorage, sessionStorage, cookie, postMessage, URL params, referrer)
6. **OUTPUT TO FILE ONLY** - Write ALL findings to `xss-audit-report.md` (always output report, create with timestamp suffix if exists)

## Search Strategy - 14 Layers (Execute Systematically)

### Layer 1: DOM / HTML Injection Sinks (HTML context)
- Classic HTML injection: innerHTML, outerHTML, insertAdjacentHTML, document.write
- Newer APIs: setHTMLUnsafe, ShadowRoot.innerHTML, attachShadow
- React: dangerouslySetInnerHTML, createElement, cloneElement
- HTML builders: DOMParser, template.innerHTML, createRange

### Layer 2: Attribute & Event Handler Injection (attribute/JS contexts)
- Inline event handlers, dynamic attribute names
- Dangerous attributes: on*, href, src, srcdoc, xlink:href, action, formaction, data, poster, style
- JSX props that can become dangerous

### Layer 3: URL Injection & Navigation (CRITICAL) - EXPANDED
- ALL href/src/action assignments
- ALL window.open calls
- location/document.location assignments & redirects
- History API state changes (pushState, replaceState) and subsequent consumers of the modified URL; these APIs do not themselves load the supplied URL
- Router navigation (React Router, Next.js, etc.)
- Protocol patterns: javascript:, data:, vbscript:, file:, blob: - review in context; their presence alone does not prove XSS

**URL validation anti-patterns (MUST audit for each validation found):**
1. **Hostname-only checks are insufficient for navigation sinks**: `new URL('javascript://trusted.com/%0aalert(1)').hostname` evaluates to `trusted.com`. Protocol and the eventual sink must also be checked; do not assign severity from the validator alone
2. **Substring checks**: `url.includes('trusted.com')` / `url.startsWith('https://trusted.com')` - bypassable via `https://trusted.com.evil.com`, `https://trusted.com@evil.com`, `https://evil.com/?q=trusted.com`
3. **Raw-string comparisons that ignore parser normalization**: prefer comparing the normalized components returned by `new URL()`; if raw strings are compared, check case, whitespace, and control-character handling explicitly
4. **Protocol-relative URLs**: `//evil.com` passing naive checks
5. **Backslash confusion**: `https:\\evil.com` treated as valid by browsers but mismatched by string checks
- Verdict rule: there is no universal "safe URL" rule. Parse with `new URL(input, trustedBase)` or an equivalent standards-based parser, use a protocol allowlist appropriate to the specific element and sink, and compare hostnames exactly or with a dot-boundary suffix check when a domain restriction is required. `http:`/`https:` is a common navigation allowlist, not a universal rule; relative URLs and schemes such as `mailto:`/`tel:` may be legitimate. Confirm attacker control and the final sink before classifying a finding

### Layer 4: Configuration / Content Models & JSON-in-Script (CRITICAL)
- SSR bootstraps: __INITIAL_STATE__, __NEXT_DATA__, __NUXT__, __APOLLO_STATE__
- Configuration objects with url/href/link/html/template
- UI widgets/content blocks with rich text
- External data sources flowing to render models

**JSON-in-script injection:**
- Attacker-influenced data serialized into inline `<script>` blocks (SSR bootstrap, hydration data, JSON-LD / `application/ld+json`)
- `JSON.stringify` does NOT make content safe inside a `<script>` element: a string value containing `</script>` can terminate the element early and enable markup/script injection
- Safe patterns to look for: `.replace(/</g, '\\u003c')`, `serialize-javascript`, or a framework-provided serializer documented to neutralize `<` for inline-script use
- Danger patterns: string concatenation into `<script>` bodies, `dangerouslySetInnerHTML` on `<script>` tags, template literals embedding server/API data in inline scripts
- Verdict rule: attacker-influenced data in a `<script>` block without `<`-neutralization is a high-priority lead. Confirm that the attacker can supply a breakout string and that the resulting context permits script execution before assigning severity

### Layer 5: Props Spreading & "Gadget" Components
- Props spreading: {...props, ...rest, ...otherProps}
- Anchor/button/router-link gadgets
- setAttribute for URL-bearing attributes

### Layer 6: Data Sources (Untrusted Inputs) - EXPANDED
- IndexedDB, Cookies
- Storage getters (localStorage.getItem, sessionStorage.getItem)
- URL-derived sources (URLSearchParams, window.location)
- postMessage, BroadcastChannel, MessageChannel
- **postMessage sender side**: `postMessage(payload, '*')` sends data to the target window regardless of its current origin; it does not broadcast to every origin globally. Check whether the target can be navigated or controlled by an untrusted origin and whether the payload contains tokens/PII/sensitive state
- Type models with url/html/template fields

### Layer 7: Prototype Pollution → XSS Gadgets
- merge, deepmerge, extend, defaultsDeep, cloneDeep, set, update
- Object.assign patterns
- __proto__, prototype, constructor
- Treat these as review leads: establish an attacker-controlled pollution path, the affected object/prototype, and a reachable security-sensitive gadget before reporting a vulnerability

### Layer 8: JavaScript Execution Sinks (JS context) - HIGH RISK
- Direct execution: eval, new Function, Function()
- Timers with string arguments: setTimeout, setInterval
- Blob/ObjectURL/worker-import sinks (including dynamic `importScripts` in workers/service workers) when attacker-influenced content is executed as script
- Script injection patterns

### Layer 9: CSS / Style Injection (CSS context)
- Style string sinks: style.cssText, setProperty, insertRule
- styled-components, emotion, css-in-js template literals
- url() and @import: review external requests, data exposure, and UI impact rather than assuming JavaScript execution
- behavior and expression(): legacy Internet Explorer mechanisms; report only when the supported browser threat model includes them

### Layer 10: SVG / MathML / XML Context Injection
- SVG elements: <svg, xlink:href
- createElementNS, setAttributeNS
- Animation events: onbegin, onend, onrepeat
- Namespace confusion primitives (foreignObject, MathML annotation-xml) - feed Layer 11 mXSS analysis

### Layer 11: Markdown / HTML Rendering Pipelines & Sanitizer Bypass (mXSS) (CRITICAL)
- Markdown renderers: marked, markdown-it, remark, rehype, showdown
- Sanitizers: sanitize-html, DOMPurify

**mXSS (mutation XSS):** sanitized markup is mutated by the HTML parser when re-parsed, producing active content the sanitizer never saw. Classic vectors: SVG/MathML **namespace confusion** (`<math><mtext><table><mglyph><style><!--</style><img onerror=...>`), elements moved by parser corrections (`<table>`, `<form>`, `<noscript>` inside foreign namespaces).

**Audit for:**
1. **Sanitizer version** - check the resolved version in package.json / lockfile against relevant security advisories and known-bypass versions; merely being "current" does not prove safety
2. **Sanitizer config** - `ALLOW_DATA_ATTR` (default `true` in DOMPurify; not a vulnerability by itself, but relevant to Layer 14 framework integrations), `FORBID_TAGS`/`FORBID_ATTR`, `USE_PROFILES`, custom `ALLOWED_TAGS` including svg/math
3. **Sanitize-then-transform ordering** - code that sanitizes, then concatenates/interpolates/re-parses before insertion (e.g. `el.innerHTML = sanitize(a) + b`) can invalidate sanitization. Avoid unsafe HTML transformations after sanitizing; if the final markup is transformed, sanitize the final form for the destination context
4. **Double parsing** - sanitized string passed through `DOMParser`, `createContextualFragment`, `template.innerHTML`, or markdown post-processing before DOM insertion
5. **Wrong sanitizer for context** - HTML-sanitizer output placed inside `<svg>`, `<math>`, attribute values, or JS strings
6. **sanitize-html defaults** - record the effective allowed tags, attributes, and URI schemes; do not assume either that defaults are vulnerable or that they are sufficient for the application

### Layer 12: Framework-Specific HTML Rendering & Trust Hooks
- Vue: `v-html` renders raw HTML; normal text interpolation is escaped
- Angular: ordinary `[innerHTML]` bindings are sanitized by Angular; focus on `bypassSecurityTrustHtml` and other trust bypasses, incorrect `DomSanitizer` usage, and direct DOM writes
- Svelte: `{@html}` renders raw HTML
- Lit: `unsafeHTML` renders raw HTML; ordinary `lit-html` text interpolation does not, so review the actual directive/template path rather than treating `lit-html` itself as unsafe

### Layer 13: Trusted Types & CSP (Hardening + audit signal)
- Trusted Types usage, violations, CSP directives

### Layer 14: Framework Attribute Binding & Client Template Injection (CRITICAL)
> Some frameworks evaluate attribute values or template source as expressions. These attribute families are not interchangeable: KnockoutJS `data-bind` and WinJS `data-win-*` are `data-*` attributes, while Alpine.js `x-*` and ordinary AngularJS `ng-*` attributes are not (AngularJS also supports forms such as `data-ng-*`). DOMPurify's `ALLOW_DATA_ATTR` applies to `data-*` attributes and is not a vulnerability by itself. Establish exactly which attribute or template construct survives sanitization and whether the framework subsequently processes it.

**Knockout-specific attack chain**: Untrusted HTML containing `<div data-bind="text: (alert(document.domain),'')">`
  → The sanitizer preserves `data-bind` (for example, DOMPurify allows `data-*` by default)
  → The node is included in an actual `ko.applyBindings()` / `ko.applyBindingsToDescendants()` traversal after insertion
  → Knockout parses and evaluates the attacker-controlled binding expression
  → **Arbitrary JavaScript execution in the binding context**

**Conditions for exploitability:**
1. The exact framework-specific attribute or template construct and its attacker-controlled value survive sanitization
2. The affected node is within the root of a binding/compilation pass that occurs after the node is inserted
3. The framework actually traverses and processes the node; traversal is not suppressed by `controlsDescendantBindings`, custom bindings, framework skip behavior, or other version-specific mechanics
4. The expression or template can perform a security-sensitive action in the available execution context

Search for:
- KnockoutJS: `data-bind=`, `ko.applyBindings`, `ko.applyBindingsToDescendants`, `ko.bindingHandlers`, `parseBindingsString`, `nodeHasBindings`, `controlsDescendantBindings`
- WinJS: `data-win-bind=`, `data-win-control=`, `setInnerHTMLUnsafe`, `WinJS.Binding`, `WinJS.UI.processAll`
- Alpine.js: `x-on:`, `x-bind:`, `x-html=`, `x-data=`, `x-init=`; these are not controlled by `ALLOW_DATA_ATTR`
- AngularJS 1.x: `ng-bind-html`, `ng-bind-html-unsafe`, `$sce.trustAsHtml`, `$compile()`; review `ngSanitize`/`$sce` and the exact directive semantics rather than assuming arbitrary expression execution
- **Client template injection**: attacker-controlled template source containing constructs such as `{{ expression }}` that is compiled/interpolated by AngularJS, a Vue runtime compiler, Angular JIT/dynamic template compilation, or another template engine. Ordinary Vue/Angular text interpolation escapes values; do not treat escaped text as template compilation, and do not limit CSTI review to AngularJS 1.x
- Ember.js/Handlebars: `{{{triple-stash}}}`, `SafeString()`, `htmlSafe()`
- Sanitizer config: `ALLOW_DATA_ATTR`, `FORBID_ATTR`, `ALLOWED_ATTR`, `ADD_ATTR`, `allowDataAttr`, `forbidAttr`; check the mechanism that applies to each exact attribute family
- Generic: `applyBindings`, `applyBindingsToDescendants`, `applyBindingsToNode`
- Framework-relevant `data-*` attributes in templates/HTML strings

**Audit steps for each match:**
1. **Identify framework and version** — KnockoutJS, WinJS, Alpine.js, AngularJS 1.x, Vue, Angular, Ember, etc.
2. **Identify the exact construct** — Is it a `data-*` attribute, another directive attribute, raw HTML, or attacker-controlled template source?
3. **Map the binding/compilation root** — Does it cover the user-injected nodes?
4. **Check execution timing** — Is the node present before a binding/compilation pass that actually traverses it? DOM insertion alone does not trigger every framework to rebind
5. **Check subsequent renders** — Does replacing innerHTML explicitly trigger re-binding or recompilation?
6. **Verify effective sanitizer output** — Does the exact dangerous attribute or template construct survive? Do not infer this solely from `ALLOW_DATA_ATTR`
7. **Check traversal controls** — Review `controlsDescendantBindings`, custom bindings, skip behavior, and framework/version-specific compilation rules
8. **Assess execution context and impact** — Confirm what the expression/template can access; do not require a `constructor.constructor()` chain when the binding expression itself can already execute code
9. **Verdict** — Report XSS only after establishing the complete source → surviving construct → binding/compilation → execution path; assign severity based on the demonstrated impact

## Data Flow Analysis - MANDATORY FOR EACH MATCH

For EACH suspicious match found, you MUST:

1. **READ THE FILE** - Open the file and read the relevant function
2. **FIND THE SOURCE** - Where does this data come from?
3. **TRACE THE PATH** - Follow the data through the code
4. **CHECK SANITIZATION / VALIDATION** - Is there ANY validation for the correct context?
5. **IDENTIFY THE SINK** - Where does the data end up?

## Critical Validation Checks

### 1) URL Attributes & Navigation
- Prefer a standards-based parser such as `new URL(input, trustedBase)` and validate the parsed components; the base must be fixed and trusted
- Use a protocol allowlist appropriate to the element, sink, and business requirements. `http:`/`https:` is common for web navigation, but relative URLs, `mailto:`, `tel:`, and other explicitly required schemes need a deliberate policy rather than a universal ban
- Compare normalized parser components; do not rely on raw substring/prefix checks or assume every parser component needs identical manual normalization
- **Hostname/domain checks alone are NOT sufficient for navigation validation** - see Layer 3 (`javascript://trusted.com/%0aalert(1)` has hostname `trusted.com`)
- For `target="_blank"`, explicit `rel="noopener"` is a useful compatibility/hardening measure even though modern browsers generally imply it. Add `noreferrer` only when suppressing the Referer header is also intended

### 2) HTML Injection Sinks
- Untrusted HTML MUST be handled with a well-maintained, context-appropriate sanitizer or a verified framework sanitization path
- Verify sanitizer **version and effective config**. Defaults are not automatically vulnerable: DOMPurify `ALLOW_DATA_ATTR: true` becomes relevant to Layer 14 only when a compatible framework binding/compilation chain exists
- Do not perform unsafe HTML concatenation/transformation after sanitizing; if the final markup changes, sanitize the final form for the destination context (mXSS, Layer 11)

### 3) JS Execution Sinks
- Treat attacker-influenced input reaching `eval`, `new Function`, or string timers as a high-priority lead; confirm the source-to-sink path and impact before assigning severity
- Prefer removing these sinks

### 4) postMessage - BOTH Directions
- Receiver: MUST validate `event.origin` against an exact allowlist AND validate the message schema; also validate `event.source` when the intended sender window matters
- Sender: use an explicit target origin whenever the intended recipient origin is known. For `postMessage(sensitiveData, '*')`, verify whether the target window can be navigated or controlled by an untrusted origin and report the resulting disclosure risk accordingly

### 5) JSON-in-Script (SSR bootstrap / hydration / JSON-LD)
- Attacker-influenced data serialized into `<script>` blocks MUST neutralize `<` (e.g. `\u003c`) to prevent `</script>` breakout
- `JSON.stringify` alone is NOT sufficient inside a `<script>` element

### 6) Trusted Types
- Consider CSP with `require-trusted-types-for 'script'` as defense-in-depth where browser support and application requirements allow

## 20-Point Mandatory Checklist

Execute ALL checks:
1. Rich text chain: user input → Markdown/HTML → sanitizer → DOM
2. dangerouslySetInnerHTML: source + sanitizer + config
3. **URL navigation: sink-appropriate protocol validation** ← CRITICAL
4. **URL validation anti-patterns: hostname-only checks, substring checks, and raw-string comparisons that ignore parser normalization** ← CRITICAL
5. DOM write APIs: innerHTML/outerHTML/insertAdjacentHTML/document.write
6. DOMParser / setHTMLUnsafe / ShadowRoot.innerHTML
7. JS execution sinks: eval/new Function/setTimeout(string)/setInterval(string)
8. Script injection: createElement('script') + src/text
9. Clipboard/drag/file: paste events, FileReader, drop handlers
10. Template concatenation: building tag/attribute/event names dynamically
11. iframe/srcdoc: sanitization, sandbox flags, and the embedded document's origin relationship to the parent
12. SVG/MathML/XML contexts: createElementNS / xlink:href / setAttributeNS
13. Third-party renderers: markdown engines, HTML parsers, sanitizer configs
14. Encoding correctness: HTML vs attribute vs JS vs URL vs CSS contexts
15. Protocol boundaries: context-appropriate validation for data:/javascript:/blob: and other non-default schemes
16. DOM clobbering / "gadget" components: props spreading + dynamic attribute forwarding
17. Prototype pollution leading to gadget control
18. **Framework attribute binding & client template injection: exact data-*/x-*/ng-* constructs or attacker-controlled template source surviving sanitization and reaching a subsequent binding/compilation pass** ← CRITICAL
19. **mXSS & sanitizer bypass: mutation XSS, SVG/MathML namespace confusion, sanitize-then-transform ordering, outdated/misconfigured DOMPurify** ← CRITICAL
20. **JSON-in-script injection + postMessage sender: `</script>` breakout in `<script>` JSON blocks; sensitive data sent with `postMessage(..., '*')` to a target whose origin is not reliably known** ← CRITICAL

## Output Format

**OUTPUT TO FILE ONLY**: `xss-audit-report.md` (create with timestamp suffix if exists)

### Template Structure

```markdown
# XSS Security Audit Report

**Date**: [Current date]
**Audited by**: Security Auditor
**Scope**: [Audited paths and commit/version, if available]
**Exclusions / Unread Files**: [Paths and reasons]
**Analysis Type**: Static analysis; dynamic verification is not performed unless separately documented

## Executive Summary

- Total locations examined: [Number]
- High severity vulnerabilities: [Number]
- Medium severity vulnerabilities: [Number]
- Low severity issues: [Number]
- Requires manual review: [Number]

## High Severity Vulnerabilities

### [Number]. [Component/Function] - [Vulnerability Type]

**File**: `path/to/file.tsx:123`

**Description**:
**Impact**:
**Data Flow**:
**Source**: 
**Sink**: 
**Missing Validation**: 
**Confidence**: [High/Medium/Low]
**Verification Status**: [Static data flow established / Requires dynamic verification / Dynamically verified separately]
**Reproduction Notes**: [Clearly label theoretical steps versus steps actually executed]
**Vulnerable Code**:
**Fix / Recommendation**:

## Medium/Low Severity Vulnerabilities
[Same format]

## Requires Manual Review
[Same format]

## Search Results Summary
Matches are review leads, not confirmed vulnerabilities.

| Layer | Focus | Matches Found | Vulnerabilities |
|-------|-------|---------------|-----------------|
| 1 | DOM/HTML sinks | X | X |
| 2 | Attr/event sinks | X | X |
| 3 | URL/navigation & validation bypass | X | X |
| 4 | Config/content models & JSON-in-script | X | X |
| 5 | Props spreading/gadgets | X | X |
| 6 | Untrusted sources + postMessage sender | X | X |
| 7 | Prototype pollution | X | X |
| 8 | JS execution sinks | X | X |
| 9 | CSS/style sinks | X | X |
| 10 | SVG/XML | X | X |
| 11 | Markdown/pipelines & mXSS | X | X |
| 12 | Framework HTML rendering & trust hooks | X | X |
| 13 | Trusted Types & CSP | X | X |
| 14 | Framework attribute binding & client template injection | X | X |
```

## High-Priority Review Signals

Treat the following patterns as review leads, NOT automatic vulnerabilities. Confirm attacker control, a reachable security-sensitive sink, missing context-appropriate defenses, and impact before assigning severity:

- `window.open(variable)` with attacker-influenced input and no sink-appropriate protocol validation
- `href/src/action/formAction={variable}` with attacker-influenced input and no validation appropriate to the element and URL context
- `history.pushState/replaceState` with an attacker-controlled URL: audit subsequent navigation, routing, and rendering; do not report the History API call alone as XSS
- `location = variable` / `location.href = variable` with attacker-influenced input and no context-appropriate validation
- **Hostname-only URL validation** (`new URL(url).hostname === '...'` without protocol validation) when the URL reaches a navigation sink
- `{...props}` on `<a>` / `<iframe>` / URL-handling components when an attacker can control forwarded security-sensitive props
- `dangerouslySetInnerHTML` with untrusted HTML and no verified context-appropriate sanitization path
- `innerHTML/outerHTML/insertAdjacentHTML/document.write/DOMParser/setHTMLUnsafe` with untrusted data and no context-appropriate defense
- `eval/new Function/setTimeout(string)/setInterval(string)` influenced by untrusted input
- `setAttribute('on*', ...)` or dynamic event handler construction influenced by untrusted input
- `setAttribute('href'|'src'|'srcdoc', userInput)` without validation appropriate to the destination context
- Configuration objects (linkExpression/url/href/html/markdown/template) flowing to security-sensitive sinks
- `sandbox="allow-scripts allow-same-origin"` when the embedded document is same-origin with the parent and can run attacker-controlled script; assess other origin combinations separately
- `Object.assign({}, userData)` / deep merge with an attacker-controlled `__proto__`, `prototype`, or `constructor` path: identify the affected object/prototype and prove a usable gadget rather than assuming global prototype pollution or XSS
- Attacker-influenced data in `<script>` JSON blocks without `<`-escaping (`</script>` breakout)
- Sanitizer output unsafely re-parsed, transformed, or concatenated before insertion (mXSS); separately, `ALLOW_DATA_ATTR: true` on framework-bound markup only when the exact Layer 14 binding/compilation chain is present
- `postMessage(sensitiveData, '*')` when the target window can be navigated or controlled by an untrusted origin
