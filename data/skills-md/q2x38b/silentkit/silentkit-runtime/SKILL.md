---
name: silentkit-runtime
description: >-
  Engineering reference for the runtime/loader layer of a JVM ghost client: Java agents and Instrumentation,
  custom classloaders, loading classes from in-memory bytes, a disposable-child-loader hot-reload pattern, resource/
  asset injection, clean teardown, and single-codebase multi-version support (a Compat facade with cached
  MethodHandles + a runtime version constant). Standard JVM mechanisms only — this skill deliberately excludes any
  detection-evasion / anti-forensics material. Brand-neutral and framework-agnostic.
---

# SilentKit · Runtime

How a ghost client is loaded, hot-reloaded, and kept compatible across engine versions — using **standard,
well-documented JVM mechanisms** (the same ones debuggers, profilers, APM agents, and hot-reload frameworks use).

**Scope note (read this).** This skill covers the *engineering* of loading and reloading code on the JVM and of
abstracting version differences. It does **not** cover evading detection, hiding from memory/AV/anticheat scanners,
anti-forensics, or "leave no trace" techniques, and it should not be extended in that direction. If a task is about
making a load *undetectable* rather than about *loading or reloading* code, it's out of scope — the clean-teardown and
GC-hygiene material below is about not leaking memory and leaving the process runnable, nothing more. Module-level game
techniques live in `silentkit-modules`; the UI layer in `silentkit-interface`.

---

## 1. Java agents & Instrumentation

The JVM's supported entry points for touching already-loaded code:

- **`premain(String args, Instrumentation inst)`** — runs before `main`, via `-javaagent:agent.jar`. The manifest
  declares `Premain-Class` (and `Can-Retransform-Classes`, `Can-Redefine-Classes` as needed).
- **`agentmain(String args, Instrumentation inst)`** — runs after startup, loaded through the **Attach API**
  (`com.sun.tools.attach.VirtualMachine.attach(pid).loadAgent(path)`). Manifest declares `Agent-Class`. This is the
  path a dev-time injector uses to attach to an already-running game.
- **`Instrumentation`** gives you: `addTransformer(ClassFileTransformer, canRetransform)`, `retransformClasses(...)`,
  `redefineClasses(ClassDefinition...)`, and `appendToSystemClassLoaderSearch(JarFile)`. A `ClassFileTransformer`
  receives each class's bytes at load/retransform time and returns modified bytes (use ASM to edit).

This is the backbone of any load-time code modification on the JVM. A **fileless handoff** is clean here: the injector
hands the agent its payload through an in-memory/local channel (e.g. a byte buffer the agent reads on attach) rather
than writing a jar to disk, which is simply fewer moving parts and no temp-file cleanup — not an evasion technique.

---

## 2. Classloaders & loading from in-memory bytes

- A classloader turns bytes into `Class<?>` via the protected `defineClass(name, byte[], off, len)`. Subclass
  `ClassLoader` (or `URLClassLoader`) and override `findClass` to serve classes from a `Map<String, byte[]>` you hold
  in memory — no file on disk required. Delegate to the parent for everything you don't own (standard parent-first),
  or go child-first for classes you want to shadow.
- **Package/resource access** — serve non-class resources (configs, assets) from the same in-memory map via
  `getResourceAsStream`. Keep your classes in their own package namespace to avoid clashing with host/engine classes.
- **Linking order** — define a class only when first needed (lazy `findClass`); resolve dependencies through the same
  loader so your module graph is self-consistent. Watch for classes that must be defined by a *specific* loader (the
  one the host/engine resolves against) and route those accordingly instead of your child loader.

---

## 3. Hot-reload via a disposable child loader

The clean pattern for "swap the implementation without restarting the process":

1. Create a fresh child `ClassLoader` whose parent is the host/app loader.
2. Load the new version's classes into it from the in-memory byte map.
3. Hand control to the new instance's entry point; register its hooks.
4. To reload: tell the current instance to **tear down** (unregister hooks, dispose resources, stop threads), drop all
   references to the child loader, and let GC collect it — then repeat from step 1 with the new bytes.

Keys to making it GC-clean (so you don't leak a loader per reload):
- Route all hooks/listeners through a **stable host-side registry** (a `HookHost`) the child registers into and that
  the teardown fully clears. A single dangling listener pins the whole child loader in memory. The host-side registry
  and a tiny **bridge interface** are the *only* types defined in the host loader; everything else lives in the
  disposable child.
- Stop every thread the child started; cancel every scheduled task; close every resource.
- Don't let host-side static fields (or engine singletons, event buses, resource managers) hold child-loader objects
  past teardown. Enums, lambdas (they capture their defining class), and registered callbacks are the usual leaks —
  audit them. A heap dump after a few reloads should show one live child loader, not N.

A tiny "host bridge" interface (defined in the host loader, implemented by the child) is the clean handoff point: the
host calls `bridge.start()` / `bridge.stop()` and never otherwise reaches into the child. `stop()` doubles as both the
reload teardown and the uninject teardown, so there's one correct shutdown path.

---

## 4. Resource / asset injection

To add your own assets (textures, shaders, fonts, lang) to an engine that loads from resource packs: implement the
engine's resource-provider / pack interface backed by your in-memory map and register it as a high-priority pack, then
trigger a resource reload. Keep the provider version-adapted behind the Compat facade (§6). Unregister it on teardown
and reload again so nothing of yours lingers (also so the engine doesn't try to recompile pipelines against assets that
are about to disappear).

---

## 5. Bytecode hooks: transformers vs a mixin framework

Two ways to insert hooks (tick/render/packet) into engine methods:
- **A mixin framework** (compile-time, annotation-driven `@Inject`/`@Redirect`/`@ModifyVariable` against named
  signatures, applied at class load). Proven, concise, great tooling. Prefer this where available. In an attach-time
  injected build where the framework's own load-time transform isn't running, a small shim can apply the compiled mixin
  classes itself.
- **Load-time ASM/Javassist transforms** (a `ClassFileTransformer` that edits target methods at runtime). More work and
  more fragile, but needed when no mixin framework is available or when you must support obfuscated targets.

Keep hooks thin: fire an event, let modules handle it. Version-branch only the few hooks whose target *signatures*
differ (see §6) — the common case is that one hook body serves every version and only the `@At` target or a single
field access changes.

---

## 6. Single-codebase multi-version support

Two models:

**A. Compile-per-version (recommended for a few adjacent versions).** A preprocessor (e.g. Stonecutter) with `//?`
comment branches builds one artifact per version against real named types — full type-safety, IDE support, and a proven
mixin framework. A hand-written **Compat facade** covers the handful of APIs whose shape changed. Cost: N artifacts to
build/ship.

**B. One runtime artifact across many versions.** Detect the version once → an int; keep per-version name-remap tables;
a mapping/wrapper layer resolves every engine member by reflection and branches on the int; load-time transforms stand
in for mixins. This exists to bridge **per-version naming differences across many loaders** — only worth it when you
target *many* versions and are willing to leave a mixin framework behind. It trades away compile-time safety for one
jar.

**The pragmatic middle (do this).** Stay on model A, but make the Compat facade carry the divergence:
- **A packed runtime version constant** baked per build (e.g. `MC = 2602` / `2603` from a `//?` branch, or parsed once
  from the engine's version string), with `atLeast(packed)` / `below(packed)` helpers, so non-mixin logic can branch at
  runtime and live in the common sourceset.
- **A thin static method per changed API**, its body `//?`-branched so one call site (`Compat.swing(...)`,
  `Compat.clockTicks(...)`, `Compat.readRgba(...)`) compiles correctly on every target. Everything else stays
  version-agnostic. Pure renames/moves can instead be resolved with **cached `MethodHandle`s** in a static initializer
  so a single compiled body serves both versions with no source branch at all.
- Keep mixins compile-time; only where a hook's target **signature** differs do you branch it. A packet or render hook
  whose field names/types changed across versions is the usual case — branch just that method's body.

```java
// Compat facade sketch: a packed version constant + one branched body per changed API.
final class Compat {
  //? if >=2603 {
  /*static final int MC = 2603;*/
  //?} else {
  static final int MC = 2602;
  //?}
  static boolean atLeast(int packed) { return MC >= packed; }

  // One call site; the body is version-branched so both builds compile:
  static void swing(Object entity, Object hand) { /*? if >=2603 {*/ /* new API */ /*?} else {*/ /* old API */ /*?}*/ }

  // Pure rename resolved once, no source branch:
  private static final MethodHandle CLOCK = resolve(/* candidates per version */);
}
```

**A decompile-diff discovery workflow** finds the divergences cheaply: decompile the two target versions, diff the
classes your hooks and facade touch, and only the methods that actually changed need a `//?` branch. Prefer published
name-mapping tables over re-decompiling when you only need the renamed member.

---

## 7. Teardown checklist (leave the process as you found it)

- Unregister every hook/listener from the host registry.
- Stop every thread; cancel every timer/scheduler; await their exit so none fires mid-teardown.
- Remove your resource provider and reload resources.
- Strip any pipelines/registries you added so the engine doesn't try to recompile against your (now gone) assets.
- Drop all host-side references to child-loader objects (static fields, engine singletons, event-bus registrations,
  captured lambdas) so the loader is collectable; verify with a heap dump across several reloads.

Clean teardown is what makes repeated hot-reload viable, and it's what lets an uninject return the process to a plain
unmodified game — it's good engineering regardless of context, and it's the one and only correct shutdown path shared
by reload and uninject.

---

## 8. Dev / testing harness

How to iterate on the *behaviour* without shipping a build to users each time. **Scope (unchanged from the top):** this
is developer tooling — compiling, attaching, and reading your own diagnostics — not detection evasion. The one piece
that touches anticheat is a *diagnostic that measures your own packets against a legit baseline* so you can tell what an
in-game server anticheat would flag (§module-skill topic); that is in scope. Hiding the loader from the OS/AV is not.

**The fileless re-inject loop (no game restart).** The whole point of the disposable-child-loader pattern (§3) is a
tight edit→build→see loop against a *running* game:
1. **Build** the client jar (per engine version, so the artifact name carries its version — `…+<ver>.jar`).
2. **Attach** with a small dev injector that uses the **Attach API** (`VirtualMachine.attach(pid).loadAgent`). It
   auto-picks the running JVM whose engine version matches the jar — probe each candidate's `sun.java.command` /
   classpath for a version segment — or takes an explicit pid; and it **redacts** session tokens/access tokens out of
   any process name it prints (those leak in launch commands).
3. **Hand off the bytes.** The shipped injector streams decrypted class bytes into the target and the agent reads them
   from a system property. For dev, a tiny **first** agent (loaded *before* the client agent) just reads the dev jar
   from disk *inside the target JVM* and sets that same property — so the real agent's code path runs identically to a
   production inject, with no separate dev branch. Two `loadAgent` calls: boot (set the bytes) then client (inject).
4. **Hot-swap.** The agent defines the client classes into a **fresh child loader**, applies the hooks, and runs. To
   iterate: **uninject** (a bound key / "panic") removes the transformer, retransforms the game classes back to the bytes
   they loaded with, drops the child loader, clears the per-inject state, and nudges GC — then a **newer** build attaches
   into a *new* loader, no restart. The GC-hygiene of §3/§7 is what makes the Nth re-inject behave like the first.

**Debug hooks, commands and settings.** Keep diagnostics in the code behind cheap gates, not in throwaway patches:
- **Deterministic sim probes** — expose the prediction sims (§4 in the modules skill) as callable debug methods that run
  from state and *return* their result, e.g. `debugPredict()` (the landing the held projectile would produce next tick:
  start/vel/end/ticks/entity) and `debugSimulate(pos, vel, kind)` (run the integrator from an **explicit** spawn state).
  Because the sims are pure read-only functions of `(pos, vel, world)`, they're reproducible from a saved state.
- **A "want vs sent" rotation log** — the highest-value anticheat diagnostic. An opt-in setting ("Flight/aim debug log")
  prints, each tick, what the module *wanted* versus what actually went **on the wire**, plus the mouse-GCD step, and the
  position/velocity. Log it at **two sites**: at the autopilot/aim code (the *want*), and again at the outgoing
  move-packet hook (the *ground truth*, after every other system has written the rotation) — logging `rot` versus the
  heading implied by your velocity (`atan2(-vx, vz)`) is exactly how you catch the classic "look doesn't match
  movement" flag (elytra, silent aim, strafe) before a server does.
- **System-property toggles** for throwaway experiments without a settings row: e.g. a packet-log that prints each
  delayed packet and how long it was held (validates §11 ordering/age), a look-log that prints per-frame view-vs-target
  (measures turn smoothness), render-self flags (draw your own ESP / nametag / silent rotation in third person so you can
  *see* where the server thinks you're aiming), and a "treat a dummy entity as a player" flag to test player-only visuals
  on a summoned stand.
- **Patch-failure dumps** — when a hook fails to apply to an already-loaded class, dump the rewritten bytes and run the
  framework's verifier, so a broken mixin is diagnosable from the log instead of a silent no-op.

**Deterministic simulation testing.** The reliable way to trust a prediction sim: run it from an explicit `(pos, vel)`
with a debug method, then **summon the real projectile/entity with that same pos+velocity** and compare where it actually
lands against the sim's predicted landing. A match validates the integrator's constants and per-axis collision order; a
divergence localises the wrong constant (a drag, a gravity, an axis-order bug) because the input state was fixed. The
same approach tests the fall/pearl/wind sims — fix the start state, compare predicted vs observed — and it's repeatable
precisely because the sims never mutate world or entity state.
