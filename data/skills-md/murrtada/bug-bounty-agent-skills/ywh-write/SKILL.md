---
name: ywh-write
description: Structure and per-section format reference for a YesWeHack bug bounty report. Use when the hunter is writing up a confirmed finding and needs the format. Triggers on "Here is my report", "help me write this up", "what sections do I need", "how should I structure this", "I'm writing the report now", or when reviewing a draft missing key sections.
---

<!--
  Ported from the YesWeHack Claude Kit (https://github.com/yeswehack/claude-kit)
  Licensed under GPL-3.0-or-later. See LICENSE in the upstream repo.
  Adapted from Claude Code plugin format to opencode skill format.
-->

# Write a triager-grade report

Apply this when the hunter is writing up a confirmed finding. Your job
is to help them shape the draft — propose prose from their facts,
offer alternatives for any section, push back on missing content.

Structure follows YesWeHack's official guidance
(https://www.yeswehack.com/fr/learn-bug-bounty/write-effective-bug-bounty-reports).
Platform-level fields (title, asset, severity, CVSS) are filled in
via the YesWeHack submission form, not the markdown body — see end
of this skill.

## Required body sections (in order)

1. **Description**
2. **Vulnerability discovery**
3. **Proof of Concept (PoC)**
4. **Exploitation**
5. **Impact**
6. **Remediation** *(optional)*
7. **References** *(optional)*

If a required section is missing, ask the hunter for it before
continuing.

---

## 1. Description

- 1-3 sentences. What the bug is, factual and specific.
- **Do not put a CWE ID here.** YesWeHack renders the CWE from the
  form field automatically — repeating it in the body is noise.
- No multi-paragraph OWASP intro, no "what is XSS" boilerplate.

Good: `Reflected XSS in /search via the q parameter. The parameter is
echoed unescaped into the HTML response body.`
Bad: 5-line definition of what XSS is; a `(CWE-79)` tag inline.

## 2. Vulnerability discovery

- Your testing narrative — what you tried, what you noticed, what
  made you dig in.
- Lab-notes style. Dead ends and friction are credible signals; keep
  them.
- Brief: a paragraph is usually enough.

Good: "Fuzzing the search endpoint with a custom wordlist, I noticed
`<script>` was filtered but `<svg/onload=...>` wasn't. After confirming
reflection context was the HTML body, I tested alert(document.domain)
to verify same-origin execution."
Bad: a polished narrative with no failed attempts.

## 3. Proof of Concept (PoC)

- Raw HTTP request/response — preferred. Triager pastes into Repeater.
- curl — acceptable. Complete: headers, cookies, body.
- Screenshot — when visual proof matters (alert dialog, UI
  rendering). Always paired with the request that produced it.
- Video — for multi-step flows or timing-dependent bugs.
- Strip session tokens, real user data (PII), unrelated headers. Use
  `[REDACTED]` where you removed something. Sanitize; don't fabricate.

**Include only the requests that are strictly necessary to reproduce.**
A triager wants the minimal path, not your whole session. Cut recon
noise, unrelated calls, and duplicate attempts.

**Don't wrap the PoC in a ready-made script unless it's genuinely
needed** (real multi-step chains, timing/race windows, thousands of
iterations). For a bug provable in one or two requests, a raw request
beats a Python script every time — the triager can replay it directly
without reading, trusting, or running your code. Reach for a script
only when raw requests can't express the bug.

A PoC is valid only if a triager with zero prior context can replay
it from scratch.

## 4. Exploitation

- Numbered steps, one action per step.
- Atomic: each step is a single observable action a triager performs
  verbatim, no inference required.
- State preconditions upfront: anonymous or authenticated? which
  role? required victim interaction? required browser/environment?
- Include expected vs actual at the step where the bug manifests.
- For complex bugs, a script is acceptable as a supporting artifact
  (per YesWeHack guidance) — but the markdown still needs atomic
  steps.

Good:
```
Preconditions: standard logged-in user (any role), no special
privileges. Tested in Chrome 132.

1. Send GET https://target.example.com/search?q=<svg/onload=alert(1)>
2. Observe: alert(1) fires in the response page.
   Expected: the payload HTML-encoded in the response.
```
Bad: `Go to the search page and trigger the XSS.`

## 5. Impact

- Only what was demonstrated. Never theoretical.
- Bottom-up from the PoC: "I executed X, observed Y at Z."
- No "could", "may", "potentially", "with the right conditions".
- If only reflection was proven, don't claim ATO.

Good: `Arbitrary JS execution in the victim's browser in the
target.example.com origin. I demonstrated reading document.cookie
and exfiltrating it to a controlled endpoint (PoC step 4).`
Bad: `Could lead to full account takeover, session hijacking, and
exfiltration of sensitive user data.`

## 6. Remediation (optional)

Include only if:

- You know the target's stack and have framework-specific advice, OR
- The fix is concrete and trivially correct (e.g., "HTML-encode the
  `q` parameter before reflection in `/search/index.html`").

Generic mitigations ("validate user input", "use parameterized
queries", "follow OWASP guidelines") add zero value. Omit rather than
padding.

## 7. References (optional — usually omit)

Most reports don't need this section. YesWeHack already renders the
CWE (and any CVE you set in the form) automatically, so a References
block that only links a CWE/CVE is pure padding — drop it.

Add References **only** when there's a genuinely useful external
pointer the triager would otherwise have to hunt for:

- A specific vendor advisory for the exact issue.
- A public write-up of the precise technique your chain relies on.
- One line per reference, no commentary.

Do not add a References section just because the template has a slot,
and never add it solely to restate the CWE.

---

## Platform fields (the YesWeHack form, not the markdown body)

These are filled via the submission form, not the markdown — but they
are slop-prone, so verify them in your review:

- **Title** — `<vuln class> in <location> via <param/header>`,
  < 100 chars, no marketing words.
  Good: `Reflected XSS in /search via q parameter`.
  Bad: `Critical vulnerability found in user search`.
- **Affected asset** — exact URL/component matching the program's
  scope. If multiple, list each. Verify against the wildcard.
- **Severity / CVSS** — use **CVSS 3.1** and score with **Base
  metrics only**. Give the full Base vector and justify each metric by
  what you actually verified. Leave Temporal and **Environmental**
  metrics untouched: Environmental reflects the target's own
  deployment context, which is the program's call to weigh, not the
  hunter's — setting them yourself inflates the score and reads as an
  overclaim.

---

## Sections to OMIT from the body

- **Introduction / Background** — collapse into Description.
- **Executive summary** — Description covers it.
- **Multi-paragraph CWE/OWASP explanations** — link in References,
  don't define inline.
- **Conclusion** — the report ends at References (or earlier if
  omitted).
- **Acknowledgements / About the researcher** — not the place.
- **Generic mitigation paragraphs** — see Remediation rules.

## Anti-patterns to flag in the draft

- Sections present but empty / "TBD" / "see PoC".
- Steps that say "trigger the vulnerability" — not atomic.
- Impact section longer than the PoC.
- Severity vector that doesn't match the preconditions (e.g., `PR:L`
  claimed when self-registration is open and `PR:N` applies).
- Repro steps that reference a screenshot instead of giving the URL.

Watch your own output for AI-slop patterns (theoretical impact,
structural tics, OWASP boilerplate, confidence without evidence) — this
skill structures the report, it does not exempt you from slop checks.
The full checklist lives in `ywh-triage`'s `references/ai-slop.md`.

## Hard rules

- **Draft from the hunter's facts, never around gaps.** Propose
  phrasings, convert lab notes into structured sections, offer
  alternatives — but only when the hunter has provided the underlying
  facts (URL, payload, response, observed behavior). If a fact is
  missing, ask. Do not invent or extrapolate.
- **Offer alternatives, not single answers.** 2-3 options per
  proposed phrasing. Forces the hunter to author.
- **Do not fill empty sections with plausible text.** Empty is
  honest; fabricated is a slop trap.
- **Do not auto-add Remediation or References just because the
  structure has a slot.** Optional means optional.
- **When the hunter asks "is this ready?"** → hand off to
  `ywh-triage`.
