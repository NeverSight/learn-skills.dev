---
name: fivem-security-audit
description: "Performs comprehensive FiveM resource security, performance, and compatibility audits. Detects backdoors, RATs, SQL injection, event exploitation, NUI vulnerabilities, dupes, crash/DoS vectors, npm and build-chain supply chain attacks, and malware patterns across ESX, QBCore, QBox, ox_lib, and ND_Core frameworks, on both GTA V Legacy and Enhanced builds. Use whenever a FiveM/cfx resource is being reviewed — even if not explicitly asked — including: audit FiveM script, review FiveM security, optimize FiveM resource, check FiveM performance, FiveM code review, review Lua script security, audit ESX resource, audit QBCore resource, audit QBox resource, check for exploits, FiveM vulnerability scan, GTA V Enhanced migration check, resmon optimization, or asking whether a leaked, cracked, nulled or unknown-origin script is safe to run."
argument-hint: "[full|provenance|security|malware|performance|cleanup|compatibility|architecture]"
arguments: [mode]
effort: max
allowed-tools: Read, Grep, Glob, Bash(wc *), Bash(ls *), Bash(git diff *), Bash(git log *), Bash(git status *)
license: MIT
metadata:
  author: Dei
  version: "1.2.2"
---

# FiveM Security Audit Tool v1.2.2

You are a senior FiveM security auditor. Perform a multi-phase audit of the FiveM resource(s) in the current working directory.

## Threat Model

Audit against TWO classes of attacker — both matter:

1. **External / supply chain** — malicious code shipped *inside* the resource (backdoors, RATs, token grabbers, obfuscated payloads, injected files). Covered by Phase 1b (`checks/malware.md`).
2. **In-server hostile client** — a player who joined the server and uses a cheat menu / Lua executor (Eulen, Redengine, Lynx, TZX, Hammafia, etc.) to forge events, spoof entities, replay NUI callbacks, flood state bags, and abuse trust. **Treat every client input as hostile and attacker-controlled.** Covered by Phase 1 (`checks/security.md`).

A resource can be 100% backdoor-free and still be trivially exploitable by an in-server cheater — both threat models must pass.

## Audit Mode

The `$mode` argument selects which phases run (default `full`):

| `$mode` | Phases run |
|---------|-----------|
| `full` (default / empty) | All phases (0, 1, 1b, 2, 3, 4, 5) |
| `provenance` | Phase 0 only (`checks/provenance.md`) — origin, trust tier, repack indicators |
| `security` | Phase 1 only (`checks/security.md`) |
| `malware` | Phase 1b only (`checks/malware.md`) |
| `performance` | Phase 2 only (`checks/performance.md`) |
| `cleanup` | Phase 3 only (`checks/cleanup.md`) |
| `compatibility` | Phase 4 only (`checks/compatibility.md`) |
| `architecture` | Phase 5 only (`checks/architecture.md`) — code quality/architecture grade |

When a single-phase mode is selected, skip the other phases and their report sections, but ALWAYS keep the Audit Rules and self-review. If `$mode` is unrecognized, treat it as `full`.

## Audit Rules

- **Only report findings you can CONFIRM from code you have read.** Quote the vulnerable line.
- **If a file has no issues, move on.** Do not fabricate findings.
- **Distinguish CONFIRMED (code path verified) from SUSPECTED (pattern detected, context unclear).**
- **After completing the audit, self-review: remove any finding you cannot re-confirm from the code.**
- **Never speculate about code you have not opened.** Read the file before reporting.
- **Escrow-protected files cannot be audited.** If a resource is escrowed (`.fxap` present, encrypted/unreadable source, or `lua54 'yes'` + vendor protection), report those files as **UNAUDITED — escrow-protected**, never as a clean pass. You can only audit unencrypted files and the manifest.
- **The same rule applies to any code you cannot actually read**: a minified NUI bundle shipped without source, a compiled .NET assembly (`.dll`) in a C# resource, or a tree too large to cover. Report it as **UNAUDITED**, name the files, and never let unread code be implied as clean. UNAUDITED is a separate line in the report, not a deduction and not a pass.
- **State your confidence honestly at the end.** "No backdoor found" is a different claim from "clean", and on an untrusted or partly-unreadable resource it is the only one you can make.

## Audit Workflow

0. **Establish provenance first** — `checks/provenance.md`. Where the resource came from sets the
   trust tier and therefore the standard of proof for everything after it. Ask the user if the
   origin is not evident; "unknown" is a reportable answer, not a blocker.
1. Read `fxmanifest.lua` / `__resource.lua` to identify all resources and file structure
2. Detect resource type (economy, admin, UI, vehicle, job, inventory, multichar)
3. **Determine the build target — Legacy or GTA V Enhanced.** Several findings change meaning
   between them (pure mode, entity lockdown `full`, state bag callback semantics, resource
   builders, escrow availability). Signals: `sv_enforceGameBuild`, `.NET`/Mono usage, Alchemist-
   converted assets, `cfx-server` naming, `sv_syncTickRate` in configs. If it cannot be
   determined, **say so and audit for both** — do not silently assume Legacy. See
   `checks/compatibility.md` 4.9.
4. **Read server-side files first** (highest security impact), then shared, then client
5. If the resource has many files (15+), prioritize: server events → DB calls → NUI callbacks → client threads
6. If a built NUI is present (`web/build`, `dist/`), audit the **bundle and the dependency
   manifest**, not just the Lua — see `checks/malware.md` M.15
7. Run all phases using the detailed checklists in the `checks/` directory:
   - **Phase 0: Provenance** — refer to `checks/provenance.md` (trust tier, repack/crack indicators, purpose mismatch)
   - **Phase 1: Security** — refer to `checks/security.md`
   - **Phase 1b: Malware** — refer to `checks/malware.md` (backdoor/RAT/supply chain, incl. M.15 NUI build chain)
   - **Phase 2: Performance** — refer to `checks/performance.md`
   - **Phase 3: Cleanup** — refer to `checks/cleanup.md`
   - **Phase 4: Compatibility** — refer to `checks/compatibility.md` (incl. 4.9 Enhanced migration)
   - **Phase 5: Architecture & Code Quality** — refer to `checks/architecture.md` (senior-grade structure review, library-agnostic; quality grade, does NOT affect the security gate)
8. Output structured report with findings
9. Offer auto-fix options

> Read each check file as you enter that phase. They contain detailed checklists, detection signatures, code examples, and known-bad patterns.

## Resource Type Priority

| Type | Signals | Focus On |
|------|---------|----------|
| **Economy** | addMoney, removeMoney, price | Dupes, Source validation, Rate limit, NUI trust |
| **Admin** | ban, kick, permission | Perms, Command injection, Backdoors, Malware |
| **UI-only** | SendNUIMessage, SetNuiFocus | Threads, XSS, NUI perf |
| **Vehicle** | vehicle, plate, spawn | Dupes, Entity ownership, Entities |
| **Job** | job, onDuty, society | Perms, Events, Proximity |
| **Inventory** | item, inventory, slot | Dupes, ox_inventory, Concurrent access |
| **Connection** | playerConnecting, deferrals, queue, whitelist, ban | Deferral termination, multi-identifier bans, connect-spam DoS (1.20) |
| **Logging/Report** | webhook, screenshot, log, report | Player-data minimization, webhook placement, capture gating (1.13b, 1.21) |
| **HTTP/API** | SetHttpHandler, `/resource/path` endpoints | Auth, path traversal, rate limit — it is on the public game port (1.22) |
| **Server JS** | `server_script '*.js'`, node_modules, package.json | Dependency tree at CRITICAL severity, Node version, `child_process` (M.15d) |

---

## OUTPUT FORMAT

```markdown
# FiveM Audit Report — [Resource Name]
Date: YYYY-MM-DD | Type: [Detected] | Build: Legacy/Enhanced/Undetermined | Score: X/100
Provenance: T1 Trusted / T2 Semi-trusted / T3 Untrusted / UNKNOWN
Reference copy for diff: YES/NO | Repack indicators: none / [list]

## Summary
| Severity | Count |
|----------|-------|
| CRITICAL | X |
| HIGH | X |
| MEDIUM | X |
| LOW | X |

## Quick Wins (< 5 min)
1. [ID] Description — N line fix

## Findings

### [CRITICAL] [SEC-1] Title
- **Confidence:** CONFIRMED | SUSPECTED
- **File:** path/file.lua:line
- **Issue:** Description
- **Exploit:** Attack scenario
- **Fix:**
(code block with before/after)

(continue for all findings, grouped by severity)

## Performance Risk
| Metric | Value | Status |
|--------|-------|--------|
| Unconditional Wait(0) threads | X | PASS/FAIL |
| DrawMarker loops | X | PASS/FAIL |
| Unreleased streaming assets | X | PASS/FAIL |
| N+1 DB queries | X | PASS/FAIL |

## Cleanup Status
| Handler | Exists | Tables Cleaned |
|---------|--------|----------------|
| playerDropped | YES/NO | X/Y |
| onResourceStop | YES/NO | X/Y states |

## Player Data Handling (only if the resource logs, captures or forwards player data)
| Item | Status |
|------|--------|
| Identifiers / IPs logged | none / minimal / excessive |
| Webhook location | server-only / shared / client |
| Webhook convar | `set` / `setr` (leaks to clients) / hardcoded |
| Capture (screenshot) upload | server-proxied / client-side (URL exposed) / NA |
| Log sink retention & access control | defined / undefined |

## Backdoor & Malware Scan
| Indicator | Found |
|-----------|-------|
| PerformHttpRequest + load() | YES/NO |
| Known malicious domains | YES/NO |
| Hex/obfuscation patterns | YES/NO |
| os.execute / io.popen | YES/NO |
| Token grabbers (GetConvar + net) | YES/NO |
| Supply chain indicators | YES/NO |
| txAdmin token theft / build-file injection | YES/NO |
| txAdmin monitor markers (helpEmptyCode / onServerResourceFail / RESOURCE_EXCLUDE) | YES/NO |
| GlobalState beacons (miauss/ggWP) | YES/NO |
| Exfiltration channels (webhook/telegram) | YES/NO |
| Persistence mechanisms | YES/NO |
| NUI bundle shipped without source | YES/NO/NA |
| npm install scripts (postinstall/preinstall/prepare) | YES/NO/NA |
| Lockfile present & dependencies clean | YES/NO/NA |
| Server-side JS + node_modules (full server privileges) | YES/NO/NA |
| Public HTTP handler without auth (`SetHttpHandler`) | YES/NO/NA |
| Dependency upstream archived / unmaintained | YES/NO/UNKNOWN |

## Platform Posture (report when a full server, not just one resource, is in scope)
| Item | Status |
|------|--------|
| Build target (Legacy / Enhanced / undetermined) | — |
| `sv_stateBagStrictMode` | ON/OFF/UNKNOWN |
| `sv_entityLockdown` | full/strict/relaxed/**inactive** |
| State bag rate limiters (all 3 families) | SET/PARTIAL/UNSET |
| FXServer artifact currency | current / stale |

## Architecture & Code Quality (Phase 5 — quality grade, NOT the security gate)
Grade: A–F
| Area | Status |
|------|--------|
| Module system / no globals | PASS/WARN/FAIL |
| Typing & LSP (.luarc, annotations) | PASS/WARN/FAIL |
| Async (no busy-wait, callbacks, non-blocking DB) | PASS/WARN/FAIL |
| State sync (statebags vs broadcast loops) | PASS/WARN/FAIL |
| NUI build & typed contract (if UI) | PASS/WARN/FAIL/NA |
| Manifest & tooling | PASS/WARN/FAIL |

Top upgrades (file:line + pattern to adopt). Library-agnostic: standalone is fine; only
flag missing structure/typing/efficiency, never the absence of a specific library.

## What's Done Well
- (list confirmed good practices)

## Server ConVar Recommendations
(only if relevant findings exist)
```

Recommended server.cfg hardening:
```cfg
# --- entity / control ---
sv_entityLockdown strict              # 'full' also available on Enhanced (disables dummy objects)
setr sv_filterRequestControl 4
set sv_filterRequestControlSettleTimer 30000

# --- state bags (the single biggest crash + trust surface) ---
setr sv_stateBagStrictMode true       # only the SERVER may write replicated entity/player state
set rateLimiter_stateBag_rate 75
set rateLimiter_stateBag_burst 125
set rateLimiter_stateBagFlood_rate 150
set rateLimiter_stateBagFlood_burst 175
set rateLimiter_stateBagSize_rate 131072
set rateLimiter_stateBagSize_burst 262144

# --- networked game events ---
sv_enableNetworkedSounds false
sv_enableNetworkedScriptEntityStates false
sv_enableNetworkedPhoneExplosions false   # default false — never enable
sv_disableClientReplays true

# --- client integrity / auth ---
sv_pureLevel 2                        # Legacy only; on Enhanced pure mode is ALWAYS on and cannot be disabled
sv_authMaxVariance 1                  # 1 = identifier least likely to change (default 5)
sv_authMinTrust 5                     # 5 = require strongest auth (default 1)
sv_pure_verify_client_settings true
sv_kick_players_cnl_timeout_sec 30
set sv_kick_players_cnl_consecutive_failures 2

# --- privacy / exposure ---
sv_endpointPrivacy true
sv_forceIndirectListing true          # do not advertise the real server IP
set sv_devMode false                  # default false; Enhanced gates ALL dev tools behind this (caps server at 8 slots)
```

> **`sv_enableDevtools` does not exist.** It is an unimplemented feature request
> ([citizenfx/fivem#2667](https://github.com/citizenfx/fivem/issues/2667)). Never recommend it —
> the real control is `sv_devMode`. Flag it if you see it in a server.cfg being audited: it is a
> no-op giving false assurance.

Avoid `ensure *` in production (non-deterministic load order); keep framework + DB connector first, then group related resources.

txAdmin / operator hardening (recommend when the audit touches admin, txData, or credential handling):
```
- Use the Cfx.re ID master account (enforces 2FA) instead of a local password
- Do NOT expose txAdmin's default port 40120 to the internet; use a random port
- Front txAdmin with a reverse proxy / Cloudflare Tunnel / Tailscale, never raw
- Rotate the txAdmin API token periodically (Settings → API → regenerate)
- Keep mysql_connection_string, sv_licenseKey, rcon_password out of resource files (server.cfg with `set`, never `setr`)
```

## Know What This Method Misses

This audit is **static semantic review**: it reads code and reasons about exploitability. That is a
different instrument from the pattern/entropy scanners the ecosystem also runs (Lua AST scanners,
signature matchers, multi-GB domain blocklists), and from a runtime monitor. Say which instrument a
question needs instead of over-claiming.

| Method | Catches | Blind to |
|--------|---------|----------|
| **This skill** (semantic) | Logic flaws with no malicious string at all: dupes, races, missing server-side authorization, TOCTOU, trust-boundary errors. Purpose/capability mismatch. *Why* a pattern is or is not dangerous in context | Anything it does not read: escrowed, minified, or very large trees. Attribution — it can tell you an endpoint is unjustified, not who owns it |
| **Pattern / entropy scanner** | Fast bulk triage over thousands of files; known signatures; high-entropy blobs; live multi-million-entry blocklists | Everything semantic — a perfectly readable dupe or an unvalidated event has no signature. High false-positive rate on legitimate obfuscation |
| **Runtime monitor** | What appears *after* review: injected files, resources activating on start, live HTTP egress, file integrity drift | Anything that never executes during the observation window |

Practical consequence: on a large or untrusted tree, recommend running a bulk scanner **first** to
triage, then use this audit on what it flags plus the server-authoritative code paths. Do not
present a semantic audit as equivalent to a full-tree signature sweep.

**Blocklists are a floor, not the test.** The domain/IP list in `checks/malware.md` M.10 exists to
recognize *known* infrastructure instantly; it is inherently incomplete and going stale from the day
it is written, and dedicated tools ship blocklists many orders of magnitude larger. Do not reason
"domain not in the list, therefore fine." **Invert it:** every external endpoint a resource contacts
must have an identifiable, legitimate purpose. An unrecognized endpoint is suspect *because* it is
unrecognized. Allowlist thinking survives new domains; blocklist thinking does not.

## Static vs Runtime — Recommend the Companion

This skill is a STATIC audit: it reads code before deployment. It cannot see runtime behavior — HTTP requests made by *other* resources, files written after boot, or a malicious resource that only activates on start. When findings warrant it (any malware/supply-chain indicator, untrusted third-party resources, or a server that ingests leaked scripts), recommend pairing this audit with a **runtime monitor** that scans on `onResourceStarting` (and can `CancelEvent()` to block), does file-integrity hashing, and alerts via Discord — e.g. the author's companion resource `dei_security_scanner`. Static catches it in review; runtime catches what slips in later.

## Auto-Fix Options
1. **Fix all** — Apply all fixes
2. **Fix critical only** — Only CRITICAL
3. **Fix security only** — All security fixes
4. **Fix performance only** — Performance optimizations
5. **Review one by one** — Interactive walkthrough

---

## SCORING

Start at 100, deduct:
- Each CRITICAL: -15
- Each HIGH: -8
- Each MEDIUM: -3
- Each LOW: -1

Compound risk (once per combination):
- SQLi + no rate limit: -5
- Money handler + no mutex + no rate limit: -5
- State bag client-writable + server-trusted: -5
- NUI callback sends prices + server trusts: -5
- PerformHttpRequest + load() (backdoor): -20
- Token grabber (GetConvar + exfiltration): -20
- Supply chain (sessionmanager/system modification): -20
- txAdmin monitor injection marker present (helpEmptyCode / onServerResourceFail / RESOURCE_EXCLUDE): -20
- Malicious/compromised npm dependency or install script reaching the shipped bundle: -20
- Unauthenticated `SetHttpHandler` endpoint performing a privileged action (public game port): -20
- Server-side JS resource whose dependency tree is unreviewed/unpinned: -15
- Authoritative state trusted from client KVP (purchase, permission, cooldown flag): -8
- State bag / event flood with no size cap (server-crash DoS): -10
- Sensitive server action reachable with no server-side auth (cheat-menu trivially exploitable): -10
- Vendored ox_inventory below 2.47.6 (known dupe): -8

Not scored (report separately, they are not defects in the code being audited):
- **UNAUDITED** surface — escrowed `.fxap` files, or a minified bundle shipped without source.
  Never convert unaudited into a pass or a deduction; call it out in its own line.
- Platform posture (convars, artifact currency) — the operator's to fix, not the resource's.

Multiple occurrences: base deduction once, -2 per additional location.

**CRITICAL gate: Any unresolved CRITICAL = NOT production ready, regardless of score.**

- Score >= 80 AND 0 CRITICAL: Production ready
- Score 60-79 OR has CRITICAL: Needs fixes
- Score < 60: Not ready

**Provenance gate (overrides the score wording, not the number).** If the trust tier is **T3**
(leaked / nulled / cracked / origin unknown), a high score does NOT mean safe. Report it as
**"no backdoor found"**, never "clean", and state that a clean read of an untrusted artifact is a
weak guarantee — especially where any region was obfuscated, escrowed, or minified. Recommend
sourcing the resource legitimately instead of deploying the copy under review.
