---
name: apk-reverse
description: "Reverse engineer, debloat, de-ad, patch, or re-sign Android APKs, and analyze their runtime and server-side behavior. Use when a task involves an .apk/.aab/.dex/.so sample, smali or dex patching, Frida/objection runtime hooking, repacking and re-signing, removing ads or SDK trackers, probing a mobile app's HTTP API, or deciding whether a client-side patch is even capable of achieving the goal. Covers recon, anti-tamper, ad removal, membership/paywall limits, dex-level surgical patching, repack pitfalls, device and emulator setup, and a hard-won failure catalogue. Load the body before planning any patch work: it opens with a symptom index and four gates that must be cleared first."
---

# APK Reverse Engineering & Patching

Goal: reach a **verified, installable, still-working artifact** fast — and avoid the whole class of
mistakes that destroy an APK while looking completely healthy.

## How to use this file

This file is a **procedure with gates**, not background reading. Three things are mandatory:

- Before you patch anything, clear the **four gates** in §Gates. They are actions with pass criteria,
  not attitudes.
- When anything fails in a way your current plan does not explain, **stop and check the symptom
  index**. If a row matches, load that file before running another command.
- When this file and your own reasoning disagree, **this file wins** until you have evidence that
  overrides it. Every rule here is the residue of a failure that cost hours; your current intuition is
  the intuition of someone who has not hit it yet.

## Four rules that override everything else

**R1 — Write the deliverable as a testable sentence before you touch the target.**
"It works" is not the goal; "it works under the stated constraint" is. Root-assisted, live-
instrumentation, host-proxy and patched-device results frequently do **not** satisfy a request for an
installable artifact that works on a normal phone — and it is easy to present such a result as
finished. Write the sentence, re-read it at every checkpoint, and if you cannot meet it, say so
plainly and label the privileged workaround a **fallback**, never the deliverable.
→ `references/long-task-discipline.md` §the most expensive drift

**R2 — Change one variable at a time, and keep a control build.**
An experiment that flips two things teaches nothing when it fails, and a failure you cannot attribute
will be attributed to the wrong cause. Every "the app rejects X" claim needs its own run, and every
patch needs a same-pipeline control that still fails the old way.
→ `references/long-task-discipline.md` §single-variable discipline

**R3 — Never ship or claim an unverified artifact.**
"It assembles" is not "it works"; "the process started" is not "the feature works"; "no error in the
log" is not "the check is gone". Install it, launch it, exercise the exact feature you changed, and
look at the screen. Prove the device is running the build you made — hash it, do not trust the
filename.
→ `references/verification.md`

**R4 — Identify the owning layer before patching, and re-classify when reality disagrees.**
Ads, paywalls, feature gates, integrity checks and update gates live in different layers (Java, dex,
native, Dart/Unity, server). Patching the wrong layer either does nothing or breaks the app. If a
patch "had no effect", the diagnosis was wrong — go back to classification instead of patching harder.
→ `references/recon.md`, then the layer-specific file the symptom index points at

## Tooling — what to reach for, in order, and how to notice what you are missing

Most wasted rounds in this domain are not bad reasoning about the target. They are **the right question
asked of a tool too weak to answer it**: an hour of `grep` over a hand-exported smali tree where one
indexed query would do, or a full manual ELF walk where a decompiler was one `pip install` away. The
failure is invisible from the inside, because the weak route still produces output.

Four obligations. These are instructions, not preferences:

- **Orient with an indexer, not with an export.** Before reading code, build the ability to *ask the
  artifact questions* — `droidasc findrefs` (string/type/method → every reference site, sub-second) or
  `ddc findrefs`. A full decompile is for reading a class you have **already located**; it is not the
  way you locate it. Treat `jadx` as a readable viewer of last resort, never as the source of truth, and
  never as the entry point of a recon. → `references/toolchain.md` §Tier 1 — dex and Java
- **When the hot layer has no working tool here, installing one is part of the task.** A missing arm64
  decompiler is not a constraint to route around; it is the next step. Route around it and you pay in
  hours for a result a decompiler gives in minutes. Ask a human only when installation is genuinely
  impossible. → `references/toolchain.md` §Closing a capability gap
- **Name the gap before you spend against it.** State the capability the current blocker requires, and
  whether this machine has it. This is a G2 item, not a note to yourself.
- **Reach for a script here before writing a new one.** The kit exists precisely so that parsing,
  hashing, alignment and hot-plug probes are not re-derived per task; a bespoke script written in place
  of `scripts/dex_find_insn.py` is how offsets get guessed instead of computed.
  → `references/toolchain.md` §Using the kit's scripts instead of writing your own

A capability you have not checked for is not a capability you lack. Run
`python skills/apk-reverse/scripts/doctor.py` and read what it finds **off-PATH** before concluding
that anything is unavailable.

## Coverage — what this skill claims, and what it does not

The failure this section prevents is not ignorance. It is **a confident wrong answer produced by
applying the nearest available procedure to a target it was never written for.** A documented method
that almost fits is more dangerous than no method at all, because it arrives with a plan, a
vocabulary and a set of reassuring numbers.

**Covered, by verified mechanisms:**

- Client-side ads, promos and splash/popup/tab configuration — including the server-issued UI config
  that has no SDK to find (`ad-removal.md`, `server-config-and-updates.md`).
- Deciding whether a membership, paywall or feature gate is *client-enforceable* at all, and saying
  so plainly when it is not (`membership-and-limits.md`, `account-gates.md`).
- dex-level surgical patching: equal-length byte edits and dexlib2 method rewrites, plus the header,
  verifier and alignment rules that decide whether the build loads at all (`dex-patching.md`,
  `byte-level-patching.md`, `patch-audit.md`).
- Repacking, signing, installing, and the install refusals that look like a broken build
  (`repack-and-sign.md`).
- Packers, custom loaders and code virtualization: identifying them, measuring the validation
  boundary, and the routes that survive it (`packers.md`,
  `code-virtualization-and-custom-linkers.md`).
- The native layer: `.so` hosts, tamper-triggered self-termination, forged ELF structure, and
  neutralising a terminate path without freezing the process (`native-and-so.md`,
  `native-tamper-and-suicide.md`).
- Flutter / Dart AOT: analysing and patching `libapp.so` **given a snapshot dump** — pool-reference
  counting, disassembly windows, caller indexing, patch-site choice (`dart-aot.md`). Measured on a
  real Dart 3.6.0 build: `dart_disasm.py` decoded identically to capstone (32/32 and 96/96), the
  caller index re-derived independently with a symmetric difference of 0, and a specific business
  logic site was located end to end. **The snapshot dump is a dependency, not a detail** — see the
  next section.
- Runtime analysis with Frida, server-side API probing, feature-scoped TLS failures, update and
  forced-upgrade neutralisation, and the verification discipline everything above rests on.

**Dependencies this skill does not ship — name them before the workflow starts:**

- **Dart AOT analysis needs a snapshot dump.** `dart-aot.md`'s workflow begins at `pp.txt`; producing
  it requires a snapshot container resolver that this skill does not contain and cannot synthesize.
  `dart_pool_strings.py` reports **file** offsets while `pp.txt` and `dart_pprefs.py` speak in **pool**
  offsets, and the mapping between those two spaces is not a constant: over the 4,241 strings present
  in both, a measured run found 4,237 distinct deltas. Ship a pinned front end (aotopsy — pure Go, no
  toolchain) or build blutter (~80 s, needs a C++ toolchain). **Say which one you are using and why,
  because the two report different Dart version labels for the same binary.** Do not describe the
  object pool as something this skill decodes on its own.

**How strong these claims are:** the Measured mechanisms below were established by running the
scripts against a real target during the verification pass recorded in
`docs/tool-verification/`. The rest are **inferred** — documented from experience, but the
repository carries no fixture, log or sample that reproduces them (its own `long-task-discipline.md`
reserves *observed* for a claim with an exact command and output behind it). Treat the distinction as
load-bearing rather than cosmetic, and label your own results the same way.

**Not covered — say so rather than improvise:**

- **Unity / IL2CPP logic recovery.** `framework-runtimes.md` identifies the runtime and establishes
  that the dex is not the battlefield; it does not carry the IL2CPP equivalent of `dart-aot.md`.
  There is no verified recipe here for locating a method inside `libil2cpp.so` plus
  `global-metadata.dat`.
- **React Native / Hermes bytecode** and Cordova/hybrid internals, beyond runtime identification and
  the generic "find the string, then find what references it" approach.
- **iOS / `.ipa` of any kind.** Every device, signing and packaging instruction here is Android.
- **Defeating a server-side authority.** `server-api.md` exists to determine *who owns a gate*, not
  to break an authorization the server performs.
- **A general unpacker, or an anti-detection arms race.** `detection-and-anti-analysis.md` decides by
  cost and often concludes "switch to static"; it is not a catalogue of evasion for every detector
  you might meet.

**Not exercised by the verification pass — do not read silence as support:** the packer, code
virtualization, custom-linker, integrity-check-redirection and tamper-triggered-suicide scenarios
were **not run** against the verification target, because that target has none of those features (no
packer, no integrity checker, ordinary application class) and its unmodified build already fails to
start, which removes the repack-and-regress loop those scenarios need. Nothing in
`docs/tool-verification/` is evidence either way about them. If you use those documents, the
claims are still on the inferred footing described above.

**Scripts this pass did not run** — so they carry no measurement at all, and any conclusion drawn
from them should be labelled accordingly: `native_crash.py`, `apk_diff.py`, `snap.py`,
`grab_crash.py`, `install_test.py`, `repack.py`, `dex_patch_bytes.py`, `dex_find_insn.py`,
`dex_check_verifier.py`, `dex_classdiff.py`, `dex_strpatch.py`, `patch_smali.py`, `smtool.py`,
`datastore_inject.py`, `probe_api.py`, `run_probe.py`, `tls_check.py`, `usb_net_proxy.py`,
`devsh.py`, and the `dexpatch/` java rewriter. Their absence from the record is not a verdict on
them. Note in particular that `grab_crash.py` claims to recover stacks hidden by a crash-reporter
SDK — the exact situation the verification target presented — and was not tried, so that claim
remains **unverified** and the pass used a purpose-written Frida probe instead.

**The fallback, as an instruction:** if the target does not match that list, or no symptom-index row
matches, **stop and classify before choosing a branch.** Answer the thirteen questions first. If the
shape still does not fit — an unknown runtime, a mechanism you cannot name — say exactly that, and
propose the cheapest experiment that would identify it, rather than taking the closest documented
route and applying it anyway. A wrong branch here does not fail loudly: it produces an artifact that
builds, runs, and does the wrong thing.

## Hand-off points — where this skill ends and another view begins

Three boundaries that are easy to walk into without noticing. Each names what the other side owns,
rather than restating it, because two copies of the same advice drift apart.

**1. JNI — a Java `native` declaration and its implementation are two different views of one function.**
This skill reads the Java side (dex) and the native side (`.so`) with different tools, so the join is
where analyses go wrong.

| Form | What you see | How to find it |
|---|---|---|
| Static linkage | symbol `Java_<pkg>_<Class>_<method>` in `.dynsym` | search the dynamic symbol table. Under R8 the class name is a short name, so the symbol deforms with it and a search for the readable original finds nothing |
| Dynamic registration | **nothing** in the symbol table — binding happens at runtime | find `RegisterNatives` call sites, or hook it to read the binding table. Obfuscated targets prefer this, and a symbol search fails **silently** on it |
| Native → Java callbacks | native code pulling data back through Java | follow `FindClass` / `GetMethodID` / `CallObjectMethod` |

`FindClass`/`RegisterNatives` in a `.so` tell you a JNI boundary exists even when no
`Java_*` symbol does. **Strength note:** the three rows above are documented behaviour, not results
from the verification pass, which did not trace a JNI boundary end to end; `FlutterJNI.loadLibrary`
appearing in a dex is the closest it came. Treat them as a map, not as a measurement.

**2. Hardening — a dex-side packer observation is a native-side implementation question.** If the dex
turns out to be a shell, the logic is behind a loader, and the analysis moves to the `.so` that
performs the unpacking. `packers.md` owns the dex-side identification; the native deep dive belongs on
the other side of this boundary. **Not exercised by the verification pass** — that target had no
packer, so this pointer carries no measurement.

**3. The existing native boundaries — read native anomalies from the APK side, not from inside.** 
`native-and-so.md` and `native-tamper-and-suicide.md` are deliberately scoped to what you can conclude
*from the APK side*: a repacked build that dies instantly with a null-looking fault, a Java-layer
check that reports success while the process dies, a terminate path you made not-return. That
judgement belongs here, because it is about deciding whether your *patch* caused the death. Deep
native work — restoring a symbol, rebuilding a call graph, reversing an OLLVM function — is a
different activity with a different toolchain. Point across rather than duplicating: if you need the
latter, say so instead of extending these two files into it.

## Symptom index — a matching row is a stop signal

You arrive at a symptom, not at a file name. Each row below is a failure that has already been paid
for. **If any row matches what you are observing, load the file before your next command** — not after
your next three attempts. Reasoning from first principles at this point is how the same hours get
spent twice; more than one entry here is a lesson that was re-derived by hand while the answer sat
unread in this repository.

| What you observe | Load first |
|---|---|
| A repackaged/re-signed build **dies before your code runs**; `SIGSEGV`, all registers zero, `pc=0`, `fault addr` near `0x0` | `native-tamper-and-suicide.md` (deliberate crash), then `code-virtualization-and-custom-linkers.md` |
| **No packer** (Application is the app's own, dex readable) **and it still dies** | `code-virtualization-and-custom-linkers.md` §a loader is still a possibility; but if the same build also dies on a *second, unrelated* device you are looking at an ordinary startup fault, not a hardened one |
| The app dies at startup on **every** device, packed or not, **and there is no tombstone** while `crash_dump` reports `already traced` and logcat says `exited cleanly (0)` | the target's launch section in the verification record under `docs/tool-verification/` — a bundled crash reporter (Sentry NDK) has taken the signal handlers, so the platform's own evidence trail is gone. Frida spawn-gating is the recovery route; it needs a working frida-server, which a disguised one may not be |
| A `FORTIFY: pthread_mutex_lock called on a destroyed mutex` abort in a Flutter app, on the **main** thread, before the first frame completes | `dart-aot.md` — check `libapp.so` is actually being loaded; Flutter's engine bootstrap is the usual place a native lifecycle fault surfaces |
| Log says a **Java-layer** signature/integrity check **passed**, yet the process dies | `code-virtualization-and-custom-linkers.md` §a Java-layer "signature killer" is a decoy |
| Deleting a library fixes validation but yields `UnsatisfiedLinkError: dlopen failed: library "X" not found` | `code-virtualization-and-custom-linkers.md` §the deadlock that eats hours |
| Whole classes appear as bare `native` declarations with no body | `code-virtualization-and-custom-linkers.md` |
| A library's **SONAME does not match its filename** | `code-virtualization-and-custom-linkers.md`, `native-and-so.md` |
| Your edit had **no effect at all**, with no error | `server-config-and-updates.md` §3 (the value may be server-sent), then `packers.md` §map the validation boundary |
| Process **hangs** with no crash record, or dies to a `uid 0` killer | `native-tamper-and-suicide.md` §the rule (you probably made a terminate path *not return*) |
| Death looks like an ordinary null dereference in a hardened library | `native-tamper-and-suicide.md` §deliberate-crash stubs |
| The app dies **only while you are attached/rooted** | `detection-and-anti-analysis.md`; run the unmodified original under identical conditions first |
| **Install fails with `[-124]` and mentions `resources.arsc` / alignment** | `repack-and-sign.md` §2a — STORED **and** 4-byte aligned, both required |
| **Install fails with a bare numeric code (e.g. `[-99]`) and no `INSTALL_FAILED_*`** | `repack-and-sign.md` §vendor install interception — a device-side interceptor, not your build. Use the root `pm install` path |
| **After an install, `am start` does nothing / screenshots show another app / `am start -W` hangs** | `repack-and-sign.md` §the installer may still own the screen |
| Log shows `Failure to verify dex file ...: Bad checksum` and a startup `ClassNotFoundException` for an ordinary class | `byte-level-patching.md` §the dex header has two integrity fields — order matters |
| An install "succeeded" but nothing changed, or the version did not move | `long-task-discipline.md` §keep the observation window clean |
| Evidence contradicts itself, or a capture looks like two states mixed | `long-task-discipline.md` §keep the observation window clean |
| You took screenshots but drew the conclusion from logs or from the patch itself | `long-task-discipline.md` §captures you never looked at are not evidence |
| You are about to re-run an experiment whose result you already recorded | `long-task-discipline.md` §long-context decay |
| A script will not start, or a tool "is missing" | `scripts/doctor.py`, then `toolchain.md` §"not on PATH" is not "not installed" |
| Feature-scoped network failure (login/register/pay) while the rest works | `tls-and-cert.md` — do not assume your patch caused it |
| Everything works but **every signed request fails** after repack | `signature-derived-keys.md` |
| A re-signed build **runs fine, renders its whole UI and logs no error — but one feature silently never loads**, and `dumpsys`/DNS/logcat show **no request for it at all** (not a rejected request: *no request*) | `code-virtualization-and-custom-linkers.md` §what the native check actually reads — a client-side integrity gate is refusing **before** the request is built. This is *not* the row above: "sent and rejected" and "never sent" have different owners and different fixes |
| You cannot tell whether a missing feature is **your patch's fault or the target's own behaviour** | `long-task-discipline.md` §single-variable discipline. Run the **zero-change control through the same pipeline**, and the decisive variant: the unmodified original with the patch applied **in memory only**, same device, same network |
| Under Frida `spawn`, the UI never appears — `mCurrentFocus` stays `null`, screenshots come back blank, the Activity stack never builds | `dynamic-frida.md` §spawn keeps the Activity stack down: write the patch into memory, **detach**, then start the Activity normally |
| `frida-server` keeps disappearing mid-experiment, or the device reboots itself while you are working | `dynamic-frida.md` §when the ROM hunts your instrumentation |
| Ads still appear after a patch that should have killed them | `server-config-and-updates.md` §6 (cached config / remote re-enable), then `ad-removal.md` §step 4 (count the SDK's own log lines; n -> 0, not "I did not see it") |
| A forced-update or "must update" gate blocks the build | `updates-and-forced-upgrade.md` §step 6 |
| The dialog is gone but the feature is still locked | `membership-and-limits.md` / `account-gates.md` — decide server vs client authority before patching again |
| You are about to discard a route as "blocked" | `packers.md` — re-read it before writing any route off; mis-attributed failures have removed viable routes for hours |
| The task has run long and you are unsure what is already proven | `long-task-discipline.md` §keep a live record |

## Gates — clear these before you patch, in order

Each gate is an **action with a pass criterion**. Do not proceed past a gate you have not cleared, and
do not treat "I understand the idea" as clearing it. Skipping a gate is not a shortcut; it is how the
work gets redone.

**G1 · Deliverable form.** State, in one sentence you could hand to someone else, what artifact must
exist at the end and under what constraints (rooted or not, installable on a stock device or not, must
survive updates or not, online or offline). *Pass:* the sentence names a testable constraint, not an
activity. *Fail:* you are solving a problem in an environment the deliverable will never see.

**G2 · Environment truth and capability inventory.** Run `scripts/doctor.py` (and `scripts/preflight.py`
if a device is in play). *Pass:* you know which toolchains and scripts can actually run here, you have
seen the environment warnings — clock skew, leftover `adb forward`/proxy, a device-side frida process
already running, a tool installed off-PATH — **and you have written down the capability this target will
demand against the capability this machine has.** Name the two or three layers the task will almost
certainly reach (for example "arm64 native decompilation", "Dart AOT snapshot dumping", "device-side
TLS inspection", "dex-wide cross-referencing") and mark each available / missing-but-installable /
genuinely out of reach. *Fail:* you are about to attribute to the target a failure caused by your own
setup — or to spend a day routing around a tool that installs in ten minutes. A layer whose tool is
missing is a **task item**, not a constraint to design around. → `references/toolchain.md` §Closing a
capability gap

**G3 · Code location.** From the manifest and dex, answer: is there a packer, where does the app's own
code live (dex / native / Dart / Unity / server), and is any of it virtualized to native. *Pass:* you
can name the class that owns the behaviour you intend to change, or you have an explicit plan to find
it. *Fail:* you are about to patch a layer you have not located. If recon says "no packer", still
check the virtualization shape — see the index rows above.

**G4 · Baseline and control.** *Pass:* you have a control run — the unmodified original, or a
zero-change repack through the same pipeline — and you have recorded the observed failure (including
**time-to-death**, if it dies). *Fail:* when the patched build misbehaves you will have nothing to
compare against, and every later measurement is unfalsifiable.


## Start here: classify the target in thirteen questions

Answer these before touching a tool. Every one of them changes the whole plan.

1. **Is the app packed/hardened?** → `references/recon.md`
   Read the manifest's `application android:name`. If it is a third-party shell class rather than the app's own Application, you have a packer and must handle it first.
2. **Where does the behavior you want to change actually live?**
   - Ad SDK (Pangle/GDT/AnyThink/Kuaishou/Baidu/Sigmob…) → usually **client-side and removable** → `references/ad-removal.md`
   - **Server-issued config for UI the client renders** (launch screen, popup, announcement, tab set, sponsored card on a home feed) → **the client decides, the server supplies the data** → `references/server-config-and-updates.md` (this is the most common shape of "ad" in a modern app, and there is no SDK to find — decide this question early, because hunting an SDK that does not exist costs hours)
   - Membership / VIP / paid content → **usually server-authorized, client patch is cosmetic** → `references/membership-and-limits.md` (read this *before* spending hours)
   - Feature flag, UI gate, debug switch → usually client-side
   - Anything decided by an API response → server-side → `references/server-api.md`
3. **Is the app's own code in plain dex, or moved to native/Flutter/Unity?**
   Plain dex → you can patch. Flutter (`libflutter.so` + `libapp.so`) / Unity (`libil2cpp.so`) / pure native → different toolchain entirely. See `references/recon.md` §Where does the app's own code live and `references/framework-runtimes.md`.
      **Runtime check (cheap -- do it before committing to a layer):** hook the obvious Java classes for the UI you care about, then reproduce that UI. If those hooks fire, the behavior is Java-owned. If they fire **zero times** while the UI is plainly on screen, the behavior is drawn by the runtime or by native code, and a dex-only plan will stall. Do not keep hunting in dex after a zero-hit probe -- that is the most expensive wrong turn in this skill's history.
4. **What must the deliverable be able to do?** Write the answer as a testable sentence before
   planning anything, then re-read it at every checkpoint. This is the drift guard, and the drift it
   guards against is the most expensive one in this skill: a runtime-only result (a data edit, a live
   hook, a blocked hostname, a host proxy) can look like success while failing the actual requirement.
   The axes that decide it: **privilege** (unrooted?), **modification form** (a rebuilt, installable
   artifact, or is live instrumentation acceptable?), **ABI/device class**, **network** (must it work
   online?), **persistence** (survives restart / upgrade / fresh install?), **distribution** (must the
   shipped file be self-contained?). → `references/long-task-discipline.md` §the most expensive drift.
5. **Does the app verify its own signature, or does the server?**
   App-side → you must bypass it. Server-side → re-signing silently breaks the app later. See `references/repack-and-sign.md` and `references/server-api.md`.
6. **What is your device situation?** → `references/environment.md`
   Rooted real device (best), emulator with root, or no device (static only). Also: this determines whether Frida is usable. **Run `scripts/preflight.py` before your first experiment**, and again whenever a failure surprises you — device state, a dead device server, a leftover proxy, and clock drift all masquerade as a broken patch (`pitfalls.md` P9).
7. **Which architecture is actually executing?** → `references/native-and-so.md` §Cross-architecture
   `getprop` reports what the device claims and `primaryCpuAbi` reports what the package manager chose — neither is what is running. Only the live mapping is ground truth (`scripts/lib_map.py`). If the library you meant to patch is not mapped, a translator is in play, or the ABI differs from your assumption, that changes the plan more than any patch will.
8. **Is one *specific feature* failing at runtime — login, registration, payment, an API-backed screen — while the rest of the app works?**
   → `references/tls-and-cert.md`. A feature-scoped network failure is very often a **TLS/certificate problem on one code path**, not a consequence of your patch. The app can even carry two independent trust chains, so "other requests work" proves nothing. Rule this out in minutes before hunting for a signature check.
9. **Was the input a build you did not produce** (a "cracked"/"modded" APK circulating online)?
   → `references/third-party-builds.md`. Audit it before adopting it: such builds are frequently re-protected (sometimes with *more* layers than the original) and may carry injected components or endpoints. Never use one as a patching workbench.

   **Long-task rule:** if this is likely to run long, open `references/long-task-discipline.md` now
   and keep its record updated as you go. Re-read the refuted-conclusions and dead-routes sections
   before starting any new experiment. Losing earlier findings is the most expensive failure in this
   skill, and it is entirely preventable.
10. **Does the client sign its requests with its own signing certificate?**
    → `references/signature-derived-keys.md`. Grep for `toCharsString()` / `signatures[0]` /
    `getPackageInfo(..., 64)` **before the first repack**. If that value feeds a native HMAC/DES
    routine, the rebuilt APK must hardcode the *original* certificate value at every read site, or
    every signed request fails while the app still launches and looks healthy. This is the single
    most expensive silent failure in a repack, and 15 minutes of grep prevents it.
11. **Does the app die on its own after a while — with no Java stack trace, or with a native
    crash that looks like a bug?**
    → `references/native-tamper-and-suicide.md`. A hardened library that decides the build is
    tampered rarely calls `kill`. It more often **arranges a fault** (load a small constant, use it
    as a pointer) so the death looks like an ordinary defect, and the system then reports it as an
    app "crash" or "abnormal" dialog. Two rules before you touch anything: **enumerate which
    mechanism actually fires** (the signal and the tombstone split them apart), and **neutralise by
    returning, never by making it not return** — a spinning stub freezes the process and produces a
    symptom that looks nothing like the cause.
12. **Will this build still be usable in a week?** → `references/updates-and-forced-upgrade.md`
    If the app has any version check, upgrade prompt, or self-update path, an unpatched build can be
    turned off remotely or replaced by the official package. This is one or two edits and it decides
    whether the work is durable — do it as part of the build, not as a follow-up. Also check for a
    **hot-update / remote-config** channel, which can restore behaviour you removed without any version
    change at all.
13. **Does the request touch sign-in or phone binding — "no login required", "skip binding", "guest ok"?**
    → `references/account-gates.md`. The whole difficulty here is separating a **client-side gate**
    (patchable) from an **account-scoped resource** (the screen is empty because the server has no
    account to answer for — not patchable). Classify first; and never fabricate a session to satisfy a
    gate, which produces a state worse than being signed out.

## The workflow, end to end

Steps are ordered. **Skip a step only when its stated skip condition is met** — "it seems
unnecessary" is not a condition, and it is the reason most of the failures in `pitfalls.md` happened.

**Two-strike rule.** If the *same kind* of attempt fails twice, stop and go back to classification.
Do not run a third variation of a hypothesis that has already failed twice. Two failures of one shape
means the model is wrong, not that the parameters need tuning — and the third attempt is where an
entire round gets spent confirming what the first two already said. Re-read the symptom index at that
point; it exists for exactly this moment.

1. **Preflight, then Recon** — `scripts/doctor.py` is the cheapest possible first command: it reports which toolchains and scripts can actually run here, and surfaces the environment facts that poison experiments (clock skew, leftover `adb forward`/proxy, a device-side frida process already running, a tool installed off-PATH). Then `scripts/preflight.py` before anything else if a device is involved (it takes seconds and prevents a whole class of false conclusions), then `references/recon.md`. Manifest, package name, version, ABI, dex count, packer, embedded SDKs, where the app's own code lives. Ten minutes here saves hours. **If it is packed, unpack before anything else** (`references/recon.md` §unpacking): you cannot patch code you cannot read, the encrypted payload lengths tell you which dumped dex is the original, and a memory dump must be de-duplicated by hash and structurally validated before any of it is trusted.
   **If recon says there is no packer but a re-signed build still dies**, you are in the layer `references/code-virtualization-and-custom-linkers.md` covers — do not proceed on the assumption that "no packer" means "editable".
   **If the app already dies on its own** — especially at a roughly constant time after launch, or with a native crash — locate the mechanism *before* planning any patch (`references/native-tamper-and-suicide.md`, `scripts/native_crash.py`). Record the observed time-to-death: it is the baseline every later attempt is measured against, and without it a surviving run cannot be told from a changed schedule.
   *Skip condition:* never skipped. G2/G3 in §Gates are cleared here or not at all.
2. **Extract strings and endpoints** — build a picture of the app's API surface and SDK inventory from the dex string tables. No decompiler needed for this, and it is fast. Scripts: `scripts/dex_strings.py`.
3. **Trace to the owning class** — find the class that wraps the behavior (the app almost always wraps third-party SDKs in one helper). Reverse-lookup instructions: `references/dex-patching.md` §finding-the-call-site.
4. **Decide the patch layer** — client SDK call / client rendering / client data consumption / server contract. See the table in `references/ad-removal.md`.
5. **Patch surgically** — `references/dex-patching.md` and `references/byte-level-patching.md`.
   Two techniques, and picking the right one is a decision, not a preference:
   **equal-length byte edits** (`scripts/dex_patch_bytes.py`, located with
   `scripts/dex_find_insn.py`) when the change fits in an existing instruction slot
   or constant — nothing moves, so no offset, try/catch block or debug pointer can
   be invalidated. **dexlib2 method rewriting** (`scripts/dexpatch/`) only when the
   change genuinely needs new instructions. Whole-tree smali round-trip damages
   R8-optimized dex in ways that only show up at runtime; a method rebuild also
   inflates the file (measured: `debug_info` 924 B -> 22.8 KB, dex 4.32 MB ->
   7.73 MB on one sample). Whichever you use, recompute the dex header integrity
   fields (**signature first, checksum last**) — `references/byte-level-patching.md`
   §the dex header has two integrity fields.
6. **Repack and sign** — `references/repack-and-sign.md`. **Do not strip the whole `META-INF/`.** This single mistake destroys otherwise-correct builds.
6b. **Neutralise the update path — before you call the build done.** If the app checks for updates at all, add the two-layer patch (`references/updates-and-forced-upgrade.md`): no-op the update routine's entry, and force the version comparison to its "no update" side. A build that can be switched off or replaced remotely is not a deliverable, and this costs minutes here versus a rebuild later. Do the same for any **remote-config or hot-update** channel that could restore the behaviour you removed.
6c. **Handle account gates only after classifying them** — if the request mentions sign-in or binding, apply `references/account-gates.md` and state plainly which guarded screens become usable and which stay empty because their content is account-scoped.
7. **Verify on device** — `references/environment.md` + `references/verification.md`. Check: launches, the changed behavior actually changed, nothing unrelated broke, and **the app reaches its normal UI with no blocking dialog**. First prove the artifact actually changed on the device -- a package manager reporting success does not prove an interposed confirmation was accepted (P18). Capture continuously for the first ~20 seconds after launch, **and look at the captures** — sampling gaps are how a blocking modal goes unseen (P20), and a burst of images that were never inspected is not evidence. If the accessibility tree is empty, the image is the primary evidence rather than a fallback.
8. **Log what you learned** — if a failure cost you more than thirty minutes, add it to `references/pitfalls.md`. That file is the most valuable artifact in this skill.

## What "done" means — do not claim it earlier

Every item below must be true before you report completion. Anything less is a **checkpoint** and must
be labelled as one, out loud, with what remains. Premature "done" is the most damaging thing you can
report, because it ends the investigation while the user believes the problem is solved.

1. **The artifact exists and its identity is recorded** — path plus hash, not a filename.
2. **It was installed and launched on the environment the deliverable sentence names** (G1/R1). If
   that environment was not available to you, say so and label the result accordingly.
3. **The behaviour you changed is verified changed** — by direct observation of the feature, not by
   the absence of an error message. "The log is clean" is not evidence; "the screen shows X" is.
4. **The features it touches still work.** You exercised them. A build that starts but whose affected
   feature is dead is not a result.
5. **The original limitation is stated if any survives** — with the coupling that causes it, so the
   next person can decide whether to accept it.
6. **Nothing you did leaves the target or the device in a broken state** unless that was the goal, and
   any privileged workaround is labelled a fallback rather than the deliverable.

If items 1–4 hold but the environment was wrong, you have a **prototype**, not a deliverable. Say
"prototype" and name the gap.

## Stop conditions — halt and re-classify, do not retry

These are moments where continuing to push forward is the wrong move. Each has cost hours somewhere.

- **The same shape of attempt failed twice.** See the two-strike rule above.
- **A patch had no effect and you were about to try a third variant of it.** No effect means the
  diagnosis was wrong, not that the patch was unlucky. Re-classify the layer.
- **A new failure has no place in your current model.** That is the symptom index's trigger condition.
- **You are about to write off a route as "blocked"** without a control build proving the block is
  the app's doing rather than your pipeline's. Mis-attributed blocks have removed viable routes.
- **You are about to claim success on absence of errors.** See §What "done" means.
- **A measurement disagrees with a conclusion you already recorded as settled.** Re-open the
  conclusion; do not explain the measurement away.

## Non-negotiable constraints

- **Read-only inputs.** Keep the original APK/dex untouched; work on copies. Always keep a known-good baseline to diff against.
- **One variable at a time.** If you change two things and it breaks, you learn nothing. Build a control (same pipeline, zero patches) and compare.
- **Verify structure after every dex edit.** `scripts/dex_classdiff.py` must report zero differences in class set and access flags for classes you did not intend to change.
- **Do not patch a method that is widely shared.** Before patching any helper, count its callers (`scripts/find_refs.py`). A `Long.valueOf` wrapper with 30 callers is not an ad-specific hook.
- **Do not make an API fail to suppress a UI element.** A 404/400 on an endpoint that other features depend on takes the whole screen down with it. Suppress at the data-consumption or render layer instead.
- **Neutralise a native terminate path by returning, never by making it not return.** A stub, stub patch, or function entry replaced with a spin or a self-branch does not suppress the check — it freezes the caller, holding whatever lock it had, and unrelated threads wedge behind it. The symptom (a hang, an external kill, a restart loop) looks nothing like the cause, and there is no crash record to explain it. Return a benign value, and prefer success (0) over failure (-1). Never touch the ordinary-path symbols (`pthread_exit`, `exit`, `abort`, `snprintf`, `closedir`). `references/native-tamper-and-suicide.md`
- **Look before you conclude — and look while you wait.** Execute, capture, and **inspect**; do not drive and sleep blind. A screen that is actually looked at answers in one step what coordinate-guessing cannot answer in five: the layout moved, a different dialog is up, a countdown is frozen, the text on screen says exactly why. Where the thing you are waiting on is visible, a sample you can inspect beats a duration you hoped was right, and byte-identical samples mean nothing is going to change. `scripts/snap.py`; `references/environment.md` §look at the screen.
- **Put a timeout on every command, and calibrate it from measurement.** An unbounded call turns a stall into "the task stopped making progress", which is indistinguishable from slow work and costs hours silently. Time the operation once, record it, then derive the bound from it — that is what makes slow and hung distinguishable. A deadline that passes is a measurement, not a verdict. `references/long-task-discipline.md` §bound every wait.
- **Every claim needs evidence.** "Probably", "should be", "in theory" are not findings. Either you observed it, or you label it unverified.
   - **"Done" means the user-visible outcome**, not an internal signal. A blocking dialog still on screen means the task is not done, however many errors disappeared from the log. Absence of a log line is absence of evidence, never evidence of success.
   - **Do not discard a route on compound evidence.** If a failure followed two simultaneous changes, the attribution is a hypothesis, not a finding. Re-run it single-variable before writing the route off -- mis-attributed failures have removed viable approaches for a long time.
   - **Prove the device changed before measuring.** Install success describes the request, not the app on disk. Confirm the artifact actually advanced, or every following observation describes the previous build.
- **Attribute a failure to the right layer before patching again.** When something stops working after a rebuild, first check whether the **unmodified original** fails the same way on the same device and network. Feature-scoped network failures in particular are frequently the app's own TLS/certificate problem (`references/tls-and-cert.md`); chasing a signature check that does not exist burns hours.

## Reference index

Load only what the current step needs.

| File | Load when |
|---|---|
| `references/recon.md` | Starting any new sample; identifying packer, SDKs, code location, ABI |
| `references/server-config-and-updates.md` | **The launch screen, a popup or the tab set is server-sent**; no ad SDK was found; a removed promo came back; anything controlled by a `*Config`/`*Popup` DTO with an `enabled` flag |
| `references/byte-level-patching.md` | You want to change behaviour by editing a few bytes rather than rebuilding a method — equal-length patches, locating an instruction's exact offset, dex header integrity fields, branch polarity, verifier legality |
| `references/packers.md` | The app is packed/hardened, or an edit makes it die before your code runs. Also load before discarding any route as "blocked by the shell" |
| `references/code-virtualization-and-custom-linkers.md` | **No packer, dex is readable, and a re-signed build still dies** — whole classes turned into `native` declarations, a private loader with a mismatched SONAME, an embedded self-decrypting payload, or a Java-layer "signature killer" that logs success while a native check kills you. Covers the keep-it/drop-it deadlock and the string-redirect escape |
| `references/framework-runtimes.md` | The UI is not native (Flutter / React Native / Unity / Cordova), or Java-layer hooks fire zero times while the UI clearly works |
| `references/dart-aot.md` | The logic lives in a Dart AOT snapshot (`libapp.so`): pinning the Dart version, building a matching decompiler, the object pool and reference indexing, register/boolean conventions, locating and patching Dart code |
| `references/native-and-so.md` | Patching in a `.so`, needing code to run before the app's own code, hand-built native payloads that crash inside the linker, or **deciding which library/ABI is actually loaded and executing** |
| `references/native-tamper-and-suicide.md` | The process dies on its own (no Java stack, or a native crash that looks like a bug); you are about to neutralise a `kill`/`exit`/`abort` path; or a hardened library's sections/function boundaries look wrong |
| `references/detection-and-anti-analysis.md` | The app fights back: it dies after you attach, refuses to run on your device, detects root/hook/debugger, or your dynamic tool simply does not work in this environment. **Read the first section before escalating** — the right answer is usually to switch to static, not to fight the detector |
| `references/toolchain.md` | Choosing or invoking tools, something is not installed (including "not on PATH but present on disk"), a tool's output smells wrong, or you need to know which tools exist only as a GUI |
| `references/ad-removal.md` | Task involves ads, trackers, sponsored cards, splash/interstitial/reward |
| `references/updates-and-forced-upgrade.md` | The patched build must **keep working over time**; the app has any version check, forced-upgrade dialog, self-update installer, or hot-update/resource channel. Load this for essentially every build you intend to ship. |
| `references/account-gates.md` | Task mentions "no login required", "don't force sign-in", "skip phone binding", "guest mode"; or a screen/feature is unreachable signed-out. Also load before promising that an account-scoped screen will show anything |
| `references/membership-and-limits.md` | Task involves VIP, subscription, paid content, unlock, "fully cracked" |
| `references/server-api.md` | The behavior is decided by a response, or you need to know if a patch can even matter |
| `references/dex-patching.md` | Any actual editing of dex/smali, choosing a patch layer, choosing a tool |
| `references/patch-audit.md` | Proving a patch **landed**, or that it is **legal**: length-vs-bytes comparison, the equal-length blind spot, verifier-level legality (`move-result*` adjacency), text-matching patch traps, and how to report a missing patch |
| `references/repack-and-sign.md` | Rebuilding, signing, installing, or a repacked app misbehaves |
| `references/signature-derived-keys.md` | The app reads `signatures[0]`/`toCharsString()`, or a rebuilt APK installs and runs but every signed request fails (`sign`/`_p`/`uth` empty or `-1`) |
| `references/runtime-data.md` | Local state matters: DataStore, SharedPreferences, SQLite, protobuf caches, tokens — **or your data edit keeps being reverted, or a stored value looks encrypted** |
| `references/dynamic-frida.md` | Frida setup, hooking strategy, tracing caller chains, finding the real call site |
| `references/environment.md` | Device/emulator setup, root, ADB, networking, offline devices, emulator console control and recovery, **the preflight check to run before every experiment block** |
| `references/verification.md` | Defining what "done" means; building the evidence chain |
| `references/tls-and-cert.md` | One feature fails at runtime (login, registration, payment, an API-backed screen) while the rest of the app works |
| `references/third-party-builds.md` | The input is a "cracked"/"modded" build you did not produce — audit it before trusting it |
| `references/long-task-discipline.md` | The task will run long, or you are resuming one. Live record, conclusion grading, drift checkpoints, **deliverable-form drift (rooted-only vs shippable)**, bound-your-waits, **captures-you-never-looked-at**, **long-context decay**, handover |
| `references/pitfalls.md` | Always worth a skim before building. This is the failure catalogue. |

## Script index

All scripts are parameterized and path-agnostic; pass paths explicitly. Run `--help` or read the header of each.

| Script | Purpose |
|---|---|
| `scripts/doctor.py` | **Run this first.** Capability report and per-script runnability: which tools exist (including ones installed off-PATH or as `java -jar` jars), which scripts can actually run here, and the environment facts that silently poison experiments — clock skew, leftover `adb forward`/proxy, a device-side frida process already running |
| `scripts/dexutil.py` | **Dependency-free dex reader**: structural walk + exact instruction decode with a verified format table, `fix_dex_header`/`verify_dex_header` (correct checksum/signature order), branch-target and operand helpers. The library the dex scripts below share; also runs standalone to dump one method with offsets |
| `scripts/dex_find_insn.py` | Locate an instruction by **decoded semantics** and get its exact byte offset, with context and both sides of any branch. This is how you find a patch site without guessing offsets or scraping listings |
| `scripts/dex_patch_bytes.py` | Apply **equal-length byte patches** from a JSON spec: matches by semantics, pins branch polarity via `expect_next`, enforces equal length, checks verifier legality, recomputes the dex header in the correct order, and re-decodes to prove the edit landed. `--dry-run` first |
| `scripts/dex_check_verifier.py` | Tier-3 check: does any **conditional branch target a `move-result*`** (bypassing its producer, so the class fails to load)? Compares two builds and distinguishes pre-existing findings from regressions your patch introduced |
| `scripts/coldstart.py` | Cold-launch an app and capture a **timed screenshot burst + logcat signals + installed-build facts + launch timing**, and warn when the foreground activity is not your app (a vendor installer left on screen is the classic cause of "evidence" that shows something else) |
| `scripts/smtool.py` | baksmali/smali wrapper with a bundled classpath (assemble/disassemble dex) |
| `scripts/patch_smali.py` | Method-body replacement in a smali tree, matched by signature |
| `scripts/dex_strpatch.py` | Byte-level string constant patch with **string_ids ordering guard** |
| `scripts/dex_classdiff.py` | Compare two dex class tables (set + access flags) to prove a patch was surgical |
| `scripts/dex_strings.py` | Dump/extract strings and endpoints from dex without a decompiler |
| `scripts/dart_pprefs.py` | Build/query the object-pool offset -> code-site index for a Dart AOT snapshot (arithmetic decode; seconds, not minutes) |
| `scripts/dart_pool_strings.py` | Recover string literals from a Dart AOT snapshot: framed entries, the one-byte vs UTF-16 split, file offsets, and a run-length noise filter |
| `scripts/dart_disasm.py` | Annotated windowed disassembly of Dart AOT code (pool + boolean annotations) plus a B/BL caller index |
| `scripts/find_refs.py` | Count and list callers of a method/field (blast-radius check) |
| `scripts/repack.py` | Rebuild an APK with replaced dex, strip only signatures, keep `META-INF/services/`, **write a 4-byte-aligned archive** (`resources.arsc` STORED+aligned, which Android R+ refuses to install without), sign, and verify |
| `scripts/dexpatch/` | dexlib2 method-level rewriter (for changes that genuinely need new instructions) + build notes |
| `scripts/devsh.py` | Quoting-safe ADB shell helper for rooted devices |
| `scripts/usb_net_proxy.py` | Give an offline device network over USB (adb reverse + local proxy) |
| `scripts/datastore_inject.py` | Encode/inject AndroidX DataStore preferences (protobuf) safely |
| `scripts/probe_api.py` | Probe an app's HTTP API with correct headers, report status/shape |
| `scripts/install_test.py` | Install a build and run a launch/health check with logcat signal extraction |
| `scripts/frida_probe.js` | Four-layer runtime probe: app network layer + OkHttp + java.net + swallowed exception messages |
| `scripts/run_probe.py` | Inject a probe, stream it to a timestamped log file, stay resident while you operate the app |
| `scripts/tls_check.py` | Strict certificate check for one or more hosts (expired / wrong host / untrusted CA) |
| `scripts/preflight.py` | Read-only environment check before every experiment block: device, root, ABI/translation, clock skew, leftover proxy/forwards, dead device server. Run this before blaming a patch. |
| `scripts/lib_map.py` | What is **actually mapped** into a live process: per-library path, base, architecture (`ELF e_machine`), and classification (system / from-APK / runtime-materialized). Answers "which library and which ABI is really executing". |
| `scripts/elf_plt.py` | Resolve a PLT stub to its imported symbol on x86_64 and aarch64 (from the **relocation table**, not from position or a comment), list a symbol's callers, and **byte-diff two libraries naming the symbol each changed stub belongs to**. Run this before patching any stub, and to audit a patch set you inherited. |
| `scripts/so_constpatch.py` | Same-length in-place rewrite of an isolated string constant, for **redirecting a library load instead of defeating a check** (`System.loadLibrary("checker")` -> a library that is already mapped). Enforces equal length, refuses to touch a substring of a longer identifier, reports whether each hit sits in a constant pool, and patches inside an APK or a bare `.so`. See `references/code-virtualization-and-custom-linkers.md`. |
| `scripts/apk_diff.py` | Entry-level diff of two APKs: what changed, what was **added** (injection candidates), what was removed — by content hash, so same-size replacements are caught. Use it to audit a third-party build and to prove your own build was surgical. |
| `scripts/native_crash.py` | Locate a native death from a logcat capture or tombstone: signal, fault address, register state, backtrace split into your libraries vs system, the faulting instruction — plus an explicit flag when the fault looks **arranged** rather than accidental. |
| `scripts/grab_crash.py` | Recover a stack that a crash-reporter SDK swallowed, when the log shows the app died but prints no backtrace of its own. |
| `scripts/blob_decode.py` | Decode an opaque stored value by searching the parameter space (base64/base64url/hex × rotation × deflate/zlib/gzip) instead of guessing, then re-encode an edited payload with the same parameters. |
| `scripts/snap.py` | Bounded burst screenshot + control-tree capture, with a stall detector and an explicit verdict on whether the accessibility tree is usable at all. Use it so you *look* at the screen instead of driving blind. |
| `scripts/sig_probe.py` | Find the exact `signatures[0].toCharsString()` value: offline candidate enumeration from an APK (`--apk`), or the authoritative value read from a live package (`--live`). Feed the result into the hardcoded constant described in `references/signature-derived-keys.md`. |
| `scripts/spawn_patch_detach.py` | **Spawn under a Frida probe, then detach before driving the UI.** Under spawn mode the Activity stack often never comes up (`mCurrentFocus` stays `null`, screenshots blank); memory writes survive detach while hooks do not, so this ordering is what makes an in-memory patch observable. Use it whenever you need to *see* a build that only runs with a memory fix. |
| `scripts/hook_patch_only.js` | The minimal probe for `spawn_patch_detach.py`: neutralise one native death site by offset and report `PATCHED`. Configure `MODULE_NAME`, `FILE_OFFSET`, `PATCH_BYTES`. The replacement must be an equal-length "recover the frame and return" epilogue, never a NOP in front of live code. |
