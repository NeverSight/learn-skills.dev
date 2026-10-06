---
name: mobile-vuln-hunt
description: Hunt mobile vulnerability classes in decompiled Android (jadx/apktool) and iOS (class-dump/otool/nm) trees — ripgrep signature scan first (zero deps), optional semgrep taint analysis for dataflow classes, then triage (exported check, attacker-APK discipline) and pick the matching dynamic PoC (adb/drozer/Frida) per class from the bundled reference docs.
category: mobile-security
author: alvinhayy
license: MIT
tags: [android, ios, apk, ipa, vulnerability-detection, ipc, webview, storage, semgrep, grep, triage]
---

# mobile-vuln-hunt — vulnerability-class detection over decompiled mobile apps

Systematic pass over an **authorized** target's decompiled tree to enumerate known vulnerability
classes (IPC/intent redirection, WebView, providers, file handling, TLS, storage, crypto,
anti-analysis), using the class reference in [`docs/vuln-classes-android.md`](../../docs/vuln-classes-android.md)
and [`docs/vuln-classes-ios.md`](../../docs/vuln-classes-ios.md) — each class there has
root cause / static signature / dynamic PoC / impact / fix.

> Authorized targets only. Keep target identity and findings in the private engagement report.

## When to use

- You already ran the static pipeline (`scripts/analyze-android.sh` / `scripts/analyze-ios.sh`,
  or `/re-static`) and now want a **vuln-class hunt** on `jadx_out/`, `apktool_out/`,
  `classdump_out/`, `otool_out/`, `nm_out/` — beyond endpoints/secrets extraction.

## Inputs expected

| Platform | Required | Produced by |
|---|---|---|
| Android | `jadx_out/` (Java), `apktool_out/` (manifest + res/xml) | `scripts/analyze-android.sh` |
| iOS | decrypted binary + `classdump_out/` + `otool_out/` (cryptid must be 0) | `scripts/analyze-ios.sh` + frida-ios-dump |

Exported-component inventory first: `scripts/attack-surface.sh <apk>` — most Android classes below
only matter when the entry component is **exported** (`exported="true"` **or** has an `<intent-filter>`).

## Tier 1 — ripgrep signatures (zero dependencies, always run)

Android — run from the analysis output root:

```bash
# manifest flags & config
rg 'allowBackup|fullBackupContent|dataExtractionRules|debuggable|usesCleartextTraffic' apktool_out/AndroidManifest.xml
rg 'protectionLevel' apktool_out/AndroidManifest.xml                       # A8: normal/dangerous custom perms
rg 'grantUriPermissions' apktool_out/AndroidManifest.xml                   # A4
rg 'taskAffinity|allowTaskReparenting' apktool_out/AndroidManifest.xml     # A11
rg 'autoVerify' apktool_out/AndroidManifest.xml                            # A9
rg 'root-path|external-path' apktool_out/res/xml/                          # C5: FileProvider scope
rg 'src="user"|debug-overrides|pin-set' apktool_out/res/xml/*.xml          # D3: NSC trust anchors

# code sinks (jadx)
rg 'getParcelableExtra' jadx_out/ -l                                       # A1/A2/A5 feed
rg 'putExtras\(getIntent\(\)|setData\(getIntent\(\)\.getData\(\)\)' jadx_out/  # A2
rg 'FLAG_MUTABLE|PendingIntent\.(getActivity|getBroadcast)' jadx_out/ -l    # A3
rg 'takePersistableUriPermission|FLAG_GRANT_PERSISTABLE' jadx_out/          # A4
rg 'Class\.forName\(' jadx_out/ -l                                          # A6
rg 'sendBroadcast|sendOrderedBroadcast' jadx_out/ -l                        # A7
rg 'loadUrl\(' jadx_out/ -l                                                 # B1/B3
rg 'addJavascriptInterface' jadx_out/                                       # B2
rg 'setAllowFileAccess|setAllowFileAccessFromFileURLs|setAllowUniversalAccessFromFileURLs' jadx_out/  # B3
rg 'new FileOutputStream|openFileOutput|Files\.(write|copy)' jadx_out/ -l    # C1
rg 'openInputStream|openFileDescriptor|BitmapFactory\.decodeStream' jadx_out/ -l  # C2
rg 'rawQuery\(|selection \+' jadx_out/ -l                                   # C4
rg 'openFile\(' jadx_out/ -l                                                # C3
rg 'new URL\(|openConnection\(\)|baseUrl\(' jadx_out/ -l                     # D1
rg 'HostnameVerifier|checkServerTrusted|ALLOW_ALL_HOSTNAME_VERIFIER' jadx_out/  # D2
rg 'KeyGenParameterSpec' jadx_out/ -l                                       # E1 (check for setUserAuthenticationRequired)
rg 'DexClassLoader|PathClassLoader|InMemoryDexClassLoader' jadx_out/         # E3
rg 'Log\.[dvwie]\(' jadx_out/ -l                                            # E4 (then grep token/password/key)
```

iOS — set `APP=Payload/VulnLabApp.app/VulnLabApp` then:

```bash
otool -l "$APP" | grep -A4 LC_ENCRYPTION_INFO                  # G4: cryptid must be 0 first
plutil -convert xml1 -o stdout "$(dirname $APP)/Info.plist" | grep -A30 -iE 'NSAppTransportSecurity|CFBundleURLTypes'  # F1/C1
strings "$APP" | grep -iE 'bridge|handler|native|pasteboard'   # B2/D1
strings "$APP" | grep -E '^https?://|^/api/|^/v[0-9]+/' | sort -u          # G5
strings "$APP" | grep -iE 'api_key|secret|aws_|sk-prod|token=|password='   # G5
strings "$APP" | grep -E 'dku|pdmn'                             # A1: raw keychain attr keys
nm "$APP" | xcrun swift-demangle | grep -iE 'URLCache|CredentialStorage|KeyedUnarchiver|ASWebAuthentication|resign|openURL|handleURL|deeplink'   # A4/A5/G7/G8/C3/D2
codesign -d --entitlements - "$(dirname $APP)" | grep -E '\*|keychain-access-groups'  # G6: wildcards
```

Each hit maps to a numbered class in the reference docs — read that class entry for the exact
confirmation steps and PoC.

## Tier 2 — semgrep taint analysis (optional, needs `semgrep`)

Tier 1 finds **sinks**; taint mode proves **source→sink flow** for the classes where that is the
whole bug (intent redirection, WebView URL injection, file write, stream read):

```bash
semgrep --config skills/mobile-vuln-hunt/semgrep/android-taint.yaml jadx_out/
# or from the repo root after install:
brew install semgrep
```

Bundled rules: `android.intent-redirection`, `android.webview-url-injection`,
`android.file-write-traversal`, `android.stream-uri-read`, `android.reflection-from-intent`,
plus always-flag searches for `DexClassLoader` and ungated `sendBroadcast`. Semgrep has **no
Objective-C support** — iOS stays on Tier 1 (`nm` + `strings` + class-dump); for Swift it helps
but jadx-quality decompilation matters more.

## Triage rules (before reporting)

1. **Reachability:** is the entry component exported? (`attack-surface.sh` / manifest). No path from
   another app or web → downgrade.
2. **PoC discipline:** ADB-only PoCs get rejected in bounty triage (ADB reaches non-exported
   components too) — ship an **attacker APK** (`setClassName` + `putExtra` + `FLAG_ACTIVITY_NEW_TASK`).
3. **Guard checks:** runtime-verify debug gates (`BuildConfig.DEBUG`) and NSC `<debug-overrides>` —
   a guard in a debuggable release build is still a finding.
4. **Chain value:** single findings escalate in chains (redirect → file read → bridge RCE;
   scheme hijack ↔ broken AASA; keystore-no-binding + in-process exec). Report linked.

## Dynamic confirmation

Per class, the reference docs carry the exact PoC — adb `am start` lines, drozer modules
(`app.provider.read`, `app.provider.query`, `scanner.provider.traversal`), and Frida hooks
(`FileOutputStream.$init`, `ContentResolver.openInputStream`, `PendingIntent.getActivity`,
`CCCrypt`, `- application:openURL:options:`). Runtime helpers: `runtime/crypto-dump.js`,
`runtime/rn-frida-hook.js`, `runtime/ios-bypass.js`; long-running campaigns via
`scripts/run-in-tab.sh`.

## Output

- `findings/vuln-classes-<slug>-<date>/vuln-classes.json` — one entry per candidate:
  `{class, severity, evidence(file:line), reachable_from, confirmed, poc}`
- `report.md` — table grouped by family (IPC / WebView / Provider / File / Network / Crypto /
  Storage / Anti-analysis) with the chain narratives.

## Sources

Class reference adapted from Niraj Kharel's Mobile Pentesting series (65 posts) — commands and
patterns quoted verbatim, prose condensed, per-class source links in the two docs. Full-text
verbatim mirrors of all 65 posts (included with the author's permission for open-source use):
[`docs/research/mobile-pentesting/`](../../docs/research/mobile-pentesting/) — read the matching
post there when a Tier-1/2 hit needs deeper confirmation detail.
