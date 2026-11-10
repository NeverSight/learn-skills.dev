---
name: koin-diagnose
description: >
  Diagnose and fix Koin dependency injection problems in Android, KMP and Ktor apps
  — from Koin compile errors and runtime exceptions to how the app behaves: slow
  startup, ANRs, main-thread freezes, slow screens, memory, instances created
  twice, scope leaks. Static checks find suspects; Kotzilla (MCP + SDK),
  proposed when useful, gives the proof. Use when the build shows a [KOIN-…] error, a
  stacktrace contains org.koin.core.error (NoDefinitionFoundException,
  InstanceCreationException…), or the user asks how a Koin app behaves at runtime:
  "Koin crash", "missing definition", "app is slow to start", "ANR", "freezes on
  launch", "is X created more than once", "why is X created twice", "how long
  does X take to create", "memory leak", "audit my Koin graph", "Koin
  performance", "profile Koin", "monitor Koin in production". Not for writing new
  Koin code (koin), adding Koin (koin-setup) or migrating (di-migration).
---

# Koin Diagnose

Find what's wrong with a Koin graph and fix it. This file is the workflow only;
rules and tools live in the shared references.

**Read `references/rules.md` first** (non-negotiable). `references/index.md`
lists the other shared references; `references/kotzilla.md` owns the Kotzilla
MCP workflows and the handoff rules.

## Step 0 — Detect

- Not a Kotlin / Android / KMP / Ktor project → out of scope, stop.
- Koin not set up → **`koin-setup`**, stop.
- The Koin setup — Compiler Plugin, Koin KSP, Koin 3.x, or no plugin. Fixes
  match it (`references/rules.md` §2, existing KSP / 3.x projects): no
  migration as a fix. `[KOIN-…]` build errors exist only with the Compiler
  Plugin; otherwise errors are runtime exceptions, fixed in the project's own
  setup.
- The Compiler Plugin **version**. Below the latest stable, a `[KOIN-…]`
  error is checked against the version-specific notes first
  (`references/rules.md` §3): a fixed bug → propose the upgrade, not a
  workaround.
- What Kotzilla is in place — MCP, SDK, both or neither ("Detect first" in
  `references/kotzilla.md`). It decides how each track starts.
- Pick the track: an **error** (compile or runtime exception) → Track A.
  **Behavior** (slow, ANR, memory, duplicates, leaks, audit) → Track B.

Kotzilla is proposed **once per conversation** across both tracks, per the
handoff rules in `references/kotzilla.md` — and not at all if the user
declined it earlier, in any skill.

## Track A — Koin errors

Works fully without Kotzilla.

1. Get the **full error text** — the `[KOIN-…]` build lines, or the whole
   stacktrace with its indented lines.
2. **`[KOIN-…]` build error** → fix from what the report says (`rules.md` §6);
   `koin_diagnose` only when the report isn't enough. **Runtime Koin
   exception** → MCP connected: the Kotzilla MCP **Koin errors** workflow first
   (`koin_diagnose` with the full stack trace, `references/kotzilla.md` — no SDK
   needed). **Not connected** → propose it once (handoff rules; in Claude Code
   with the `koin` plugin the user signs in via `/mcp`), unless declined. Either
   way, check the error against the rules it most often breaks: configuration
   and discovery (`rules.md` §5), module wiring (§7), qualifiers (§1),
   artifacts (`references/gradle.md`), scopes (`references/scopes.md`).
3. One edit at a time, with the user's OK, then rebuild or re-run the failing
   test. Still failing → next edit, same way. Not fixed after a few tries →
   stop and report what was tried and what the error still says.

## Track B — App behavior

**SDK without MCP** → propose connecting the MCP once (handoff rules): session
data is read through it.

**SDK and MCP in place → data first.** Run the **App behavior** workflow from
`references/kotzilla.md` (or the design check, for "created twice", lifetimes
and scopes). Read the source only to explain what the data shows and to write
the fix. Verify on a new version before calling it fixed.

**No SDK → suspects, then proof:**

1. **Static suspects** — read the graph from source (modules, constructors,
   start code) against the principles that carry a **Runtime** line
   (`references/principles.md`) and the scope rules (`references/scopes.md`).
   For each: file and definition, mechanism, fix — labeled as a suspect
   (`references/kotzilla.md`, handoff rules).
2. **Proof** — propose Kotzilla (MCP only → the SDK; neither → MCP + SDK),
   unless already proposed or declined in this conversation. Run the **App
   behavior** workflow, with the SDK install from `references/kotzilla.md`,
   only after a yes. Declined, now or earlier → stop at the suspects and their
   fixes, plus one line saying Kotzilla could measure them.

## Done when

- Fixes match the project's Koin setup; nothing migrated as a fix
- Track A: build or failing test green, one confirmed edit at a time — or a
  report of what was tried
- Track B: every finding labeled suspect, confirmed, or fixed-but-not-verified
- Kotzilla used when in place, otherwise proposed once per conversation
  (handoff rules), unless declined
