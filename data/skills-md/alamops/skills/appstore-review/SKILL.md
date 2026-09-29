---
name: appstore-review
description: (alamops) Use whenever the user wants their iOS app checked against Apple's App Store Review Guidelines, or asks if Apple will reject something. Triggers — "check this against the app store guidelines", "will Apple reject this?", pre-submission audit, App Store readiness, pre-flight before TestFlight or App Store Connect upload, "why does Apple keep rejecting my app", rule compliance (3.1.1, 4.8, 5.1.1, etc.), or asking if a specific change is allowed (moving subs off IAP to Stripe/external checkout, adding analytics/tracking/attribution SDKs, social login, new permission, privacy manifest, ATT, account deletion, IAP/subscriptions). Works on any iOS-shipping codebase — native Swift/SwiftUI/UIKit/Xcode, React Native, Expo, Flutter, Capacitor/Ionic, Unity. Fetches live guidelines from developer.apple.com, then returns rejection-risk findings keyed by guideline number with severity, file:line evidence, and fixes. Read-only. Not for general bug/perf code review and not for implementing features.
---

# App Store guideline review

A read-only audit skill: review a project against Apple's live App Store Review Guidelines and report whether it would survive App Review. Tone: pragmatic reviewer who has shipped apps and knows which rules actually get apps bounced.

## Why this skill exists

Apple's guidelines drift. Numbering, examples, and required disclosures change several times a year (App Tracking Transparency, required-reason API list, alternative-payment language, AI / generated-content rules, account-deletion mandates, etc.). Reviewing against a snapshot in the model's head is how teams ship rejections. **You must pull the current guidelines from the web at the start of every run.** If the fetch fails, say so plainly and stop — do not guess from training data.

## The 6-step workflow

### 1. Pull the live guidelines

Fetch (in this order; stop at the first that succeeds):

1. `https://developer.apple.com/app-store/review/guidelines/`  — the canonical, full text
2. If WebFetch returns a paywalled or truncated page, fall back to `WebSearch` with `site:developer.apple.com "App Store Review Guidelines"` and follow the top result

Then **also** fetch the supporting pages that are referenced from the guidelines and routinely cause rejections:

- App Tracking Transparency requirements (`https://developer.apple.com/documentation/apptrackingtransparency`)
- Required Reason API list (search `apple required reason api`)
- App Privacy / privacy-manifest spec (search `apple privacy manifest PrivacyInfo.xcprivacy`)
- The latest "What's new in App Review" / Apple Developer news entry, if one is current

Cache the fetched text into the skill working memory for the rest of the run — don't refetch per sub-agent. If the user passes a guideline number directly (e.g., "check rule 5.1.1"), still pull the live page once so the wording you cite is current.

If you cannot reach developer.apple.com (offline, blocked, rate-limited), **abort** with: "I couldn't fetch the live App Store guidelines. I won't review from cached knowledge — please retry when the network is reachable, or paste the relevant sections."

### 2. Detect the project shape

Before you can map rules to code, figure out what kind of app this is. Run these probes in parallel:

- If the project is a git repo: `git ls-files | head -200`. Otherwise (consultancy hand-off, tarball, snapshot): `find . -maxdepth 3 -type f | head -200` plus a top-level `ls -la`. Either way, the goal is the same: top-level shape.
- Look for the platform marker files (one or more will exist):
  - **Native iOS:** `*.xcodeproj`, `*.xcworkspace`, `Info.plist`, `*.entitlements`, `Podfile`, `Package.swift`
  - **React Native:** `package.json` with `react-native`, `ios/` folder, `Podfile`, `app.json`
  - **Expo:** `app.json` / `app.config.{js,ts}` with `expo` key, `eas.json`
  - **Flutter:** `pubspec.yaml`, `ios/Runner/Info.plist`
  - **Capacitor / Ionic:** `capacitor.config.{json,ts}`, `ios/App/App/Info.plist`
  - **Unity / other engines:** Unity project files, `ProjectSettings/`
- Surface app-level metadata: bundle ID, display name, declared capabilities, declared entitlements, declared usage descriptions (`NS*UsageDescription`), supported SKUs / IAP product IDs if visible
- Look for any store-listing artifacts in-repo: `fastlane/metadata/`, `marketing/`, `store/`, screenshots, App Privacy answers, description copy

Write a short **Project Profile** block (platform, frameworks, auth providers, payment surface, tracking SDKs, generative-AI features, UGC surfaces, kids-category signals). The sub-agents you spawn next will use this to know what *not* to flag (e.g., don't hunt for IAP issues if there are no purchases).

### 3. Orchestrate parallel sub-agents

Spawn one Agent per review lane, in a single message so they run concurrently. Each sub-agent gets:

- The relevant slice of the guideline text (don't dump all of it into each — that's wasteful and dilutes focus)
- The Project Profile from step 2
- A clear instruction: **read-only, structured findings only, cite file:line, no positive findings**

The five canonical lanes plus two cross-cutting lanes:

| Lane | Guideline section | What to look for |
| --- | --- | --- |
| Safety | 1.x | UGC moderation, reporting, blocking, child safety (1.3), medical / health claims (1.4), developer info, hateful content, physical-harm vectors, kids-category compliance |
| Performance | 2.x | Crashes, broken links, placeholder content, demo accounts, hardware compatibility, software requirements (deprecated APIs, latest SDK), accurate metadata, push-notification abuse, in-app-purchase correctness, hardware abuse, beta-only behavior in prod build, software-as-a-feature gating |
| Business | 3.x | Payments (IAP for digital goods, Reader Rule, External Link Entitlement language, anti-steering), subscriptions (auto-renew disclosure, restore, manage link), advertising, other-business-model edge cases, alternative-payment entitlement usage |
| Design | 4.x | Minimum functionality, copycats, spam, web views vs. native, sign-in (Sign in with Apple parity if other social logins present, **including Google / Facebook / X / GitHub** — 4.8), HealthKit / HomeKit / etc. interface rules, push notifications, hardware compatibility, generative-AI safety controls (4.x current wording) |
| Legal | 5.x | Privacy (5.1) — App Privacy answers, privacy policy URL, account deletion (5.1.1(v)), data collection minimization, tracking & ATT (5.1.2), kids privacy (5.1.4), location (5.1.5); intellectual property (5.2); gaming / contests; VPN / mobile device management; international laws; developer code of conduct |
| App Privacy & required-reason APIs | crosscuts 5.1, 2.5 | Privacy manifest (`PrivacyInfo.xcprivacy`) present? Each required-reason API used (UserDefaults, file timestamp, system boot time, disk space, active keyboard) declared with a valid reason? Third-party SDKs that need their own manifest accounted for? Tracking domain declarations? |
| App Tracking Transparency | 5.1.2 + ATT docs | Any tracking SDK (analytics, ads, attribution) wired up? If yes: `NSUserTrackingUsageDescription` set, ATT prompt actually called before tracking, no tracking on `denied`, no IDFA / fingerprinting fallback when denied |

Each sub-agent returns findings in a fixed JSON-ish shape (see step 5). Use the **structured-output** pattern if available; otherwise instruct them to emit a fenced JSON block.

#### Prompt template for each lane sub-agent

```
You are auditing an iOS-shipping project against ONE section of the
current App Store Review Guidelines. You are read-only — do not edit
any file. Return findings only, no praise, no commentary.

PROJECT PROFILE:
<insert profile block>

GUIDELINE SECTION (live text, fetched today):
<insert just the relevant section>

YOUR JOB:
For each rule in this section, decide whether the project plausibly
violates it. A violation requires either (a) concrete evidence in the
code/config/metadata, or (b) a structural gap (e.g., the app collects
data but has no privacy policy URL anywhere in the repo). Do not flag
rules that don't apply (e.g., don't flag IAP rules on an app with no
purchases).

For each finding, output:
{
  "rule": "<guideline number, e.g. 5.1.1(v)>",
  "title": "<one-line summary>",
  "severity": "blocker" | "risk" | "nit",
  "evidence": "<file:line(s) or 'absent: <thing>'>",
  "why_it_fails": "<one sentence — what Apple would object to>",
  "fix": "<concrete remediation, 1–3 sentences>"
}

Severity:
- blocker: this is the kind of thing App Review actively rejects
- risk:    grey area / depends on how Apple reads it / common bounce
- nit:     unlikely to reject but cleanup before submission

If you find nothing, return an empty array. Do not invent findings.
```

#### Allocation tips

- Spawn the **App Privacy / required-reason** and **ATT** lanes only if step 2 found tracking SDKs, analytics, or required-reason API usage. Otherwise skip them and say so in the report ("no tracking surface detected — ATT lane skipped").
- For very small projects, you can fold Safety+Design into one agent; for large monorepos with a mix of native and JS, give the native code and the JS code separate Performance lanes so neither agent gets overloaded.
- If the project includes generative-AI features (any LLM API client, image-gen SDK, on-device CoreML generative model), add an extra mini-lane explicitly checking the current generative-AI rules — these have changed several times and are a frequent rejection cause.

### 4. Cross-check the obvious deal-breakers

Independent of the lane sub-agents, sweep these yourself — they're cheap and Apple rejects on them constantly:

- **Account creation but no account deletion** (5.1.1(v)). If the code path that creates an account exists but no in-app deletion flow does, that's a blocker.
- **Sign in with Apple missing** (4.8) when Google / Facebook / X / Apple-competing third-party login is present.
- **Tracking SDK + no ATT prompt** or **ATT prompt + no `NSUserTrackingUsageDescription`** in Info.plist.
- **Missing usage descriptions** for any sensitive API actually used (camera, mic, photo library, location, contacts, calendars, motion, Bluetooth, local network, HealthKit, HomeKit, Face ID).
- **No `PrivacyInfo.xcprivacy`** while using known required-reason APIs (`UserDefaults`, `stat`/file timestamps, `systemBootTime`, free disk space, active keyboards).
- **Digital goods sold via Stripe / external checkout** without an applicable entitlement → IAP violation (3.1.1).
- **Auto-renewing subscription** without visible disclosure of price, period, free-trial conversion, manage / cancel link, and restore-purchases button.
- **Hardcoded "TestFlight only" / beta gates** still active in the production build path.
- **Crash-prone code paths** that obviously rely on optional unwrap or unhandled rejection on a primary screen (this is the most common 2.1 rejection).
- **Placeholder copy, lorem-ipsum, TODOs, or "Coming soon" cards** on screens the reviewer will actually see.

For each one, generate a finding in the same shape as the lane agents. Don't duplicate — if a lane agent already caught it, leave theirs.

### 5. Consolidate the report

Merge all findings. Deduplicate by `(rule, evidence)`. Sort by severity (blocker → risk → nit), then by guideline number.

Each finding inside `### Blockers` / `### Risks` / `### Nits` renders as:

```
**[<rule>] <title>** — <severity>
- *Evidence:* `<file:line>` or `absent: <thing>`
- *Why it fails:* <one sentence>
- *Fix:* <concrete remediation>
```

**Always use this exact report scaffold** (and nothing else — do not emit the rendering rubric above as a section in the report):

```
# App Store readiness report

**Guidelines fetched:** <URL> on <today's date>
**Project profile:** <one paragraph — platform, frameworks, payment surface, tracking, auth>
**Lanes run:** <list of lanes, with any skipped lanes and why>

## Verdict

<One of:>
- ✅ **Likely to pass.** No blockers found. <Optional: N nits worth cleaning up before submission.>
- ⚠️ **Risk of rejection.** N risks, M nits. No outright blockers, but at least one finding maps to a rule Apple frequently enforces.
- 🛑 **Will likely be rejected.** N blockers. Submitting in current state is a waste of a review cycle.

## Findings

### Blockers
<one finding block per blocker>

### Risks
<one finding block per risk>

### Nits
<one finding block per nit>

## Notes & limitations
<Anything the user should know — couldn't inspect X, lane Y was skipped because Z, suggest running again after adding store metadata, etc.>
```

If there are zero findings, the report is just the header + verdict + a one-line note ("Sweeps clean against today's guidelines. Re-run after any change to tracking, IAP, sign-in, or account flows."). Do **not** invent findings to fill space.

### 6. Do not modify code

This skill is strictly read-only. Even if you spot a one-line fix and feel the urge — surface it in the `fix:` field. The user runs the fixes themselves (or hands the report to a separate edit-capable session). This matches the house style of the other `(alamops)` review skills.

## Triggering & disambiguation

- "App Store review", "App Review", "App Store guidelines", "will Apple reject this?", "pre-submission audit", "App Store readiness", or any reference to a guideline number (e.g., "is this 4.8-compliant?") → use this skill.
- A request for a **general** code review (bugs, perf, security in the Anthropic / web sense) → use the `code-review` skill, not this one.
- A request to **set up** Sign in with Apple, IAP, ATT, etc. → this skill audits, it doesn't implement. Surface the gap as a finding and let the user pick an implementation path.

## Working notes

- The guideline numbering occasionally shifts. Cite by **number + short title** (e.g., "5.1.1(v) — Account sign-in and account deletion") so the user can still find the rule even if a section was renumbered between your fetch and their next read.
- Apple's wording is the source of truth. If a sub-agent paraphrases a rule in `why_it_fails`, that's fine — but the `rule` field is the anchor and must match the live text.
- When you skip a lane, **say so** in the report. A silent skip reads as "passed" and is misleading.
- Avoid the failure mode where you flag every `NSCameraUsageDescription` as "make sure the string is meaningful" — that's a nit at best and floods the report. Only flag usage descriptions that are missing, empty, generic-to-the-point-of-useless, or copy-pasted boilerplate that doesn't describe the actual feature.
- Don't flag the absence of store-listing copy / screenshots if the repo doesn't contain that artifact category at all — note it in *Limitations* instead.

## Example invocations

- "Run an App Store review on this repo before I submit." → full audit, all lanes.
- "Check this against 3.1.1 and 5.1.1." → fetch guidelines, run only Business + Legal lanes, narrow output.
- "Is my Expo app ready for App Review?" → detect Expo, audit including `app.json` plugins, EAS submit profile, and the iOS native shim.
- "I added Google sign-in — am I OK?" → narrow to 4.8 (Sign in with Apple parity) plus 5.1.1 (account deletion) — these almost always travel together.
