---
name: solidjs-v2-reviewer
description: Review SolidJS 2.0 code for React-isms, Solid 1.x-isms, and reactivity bugs. Use when reviewing diffs, PRs, or files in a project that depends on solid-js 2.x / @solidjs/web — including self-review after generating Solid 2.0 code.
---

# Review Solid 2.0 code

Hunt the two prior-knowledge bug classes — **React reflexes** and **Solid 1.x
reflexes** — plus 2.0-specific reactivity mistakes. Severity guide:
🔴 broken behavior, 🟡 dev-mode diagnostic / lost reactivity, 🔵 style drift.

Confirm the project is actually v2 first (`solid-js` major 2 in package.json /
`@solidjs/web` in deps). Reviewing a 1.x project against this list produces
garbage findings.

## Pass 1 — greppable smells

Run these over the changed files; each hit needs a fix or a justification.

### Solid 1.x-isms

| Grep | Verdict | Fix |
|---|---|---|
| `from ['"]solid-js/(web\|store\|h\|html\|universal)` | 🔴 module not found | `@solidjs/web`, store APIs from `solid-js`, `@solidjs/h`… |
| `createResource\|useTransition\|startTransition` | 🔴 removed | async memo + `<Loading>`; built-in transitions / `isPending` |
| `\bbatch\s*\(` | 🔴 removed | delete wrapper; `flush()` only for sync read-after-write |
| `createComputed\|createMutable\|modifyMutable\|createDeferred` | 🔴 removed | memo / split effect / `createSignal(fn)`; `createStore` drafts |
| `\bon\s*\(` as effect dep helper, `onMount\|onError\|catchError` | 🔴 removed | split effect compute; `onSettled`; `<Errored>` / effect `error` |
| `<Suspense\|<SuspenseList\|<ErrorBoundary\|<Index\b` | 🔴 removed | `<Loading>` / `<Reveal>` / `<Errored>` / `<For keyed={false}>` |
| `mergeProps\|splitProps\|unwrap\s*\(\|createSelector` | 🔴 removed | `merge` / `omit` / `snapshot` / `createProjection` |
| `\.Provider\b` | 🔴 removed | `<Ctx value={...}>` — context is the provider |
| `classList=` | 🔴 removed | `class={{...}}` / `class={[...]}` |
| `use:[a-zA-Z]\|attr:\|bool:\|on:[a-z]\|oncapture:` in JSX | 🔴 removed | ref factories; standard attributes; `onClick` + ref for native opts |
| `produce\s*\(` in setters | 🟡 redundant | drafts are the default |
| `setStore\s*\(\s*["']` (path-style first arg) | 🔴 wrong API | draft setter or `storePath(...)` |
| `reconcile\([^)]*,\s*\{` | 🔴 1.x options object | pass the key directly; omit for `"id"`, use `null` for positional |
| `markRaw` imported from `solid-js` | 🔴 fake public API | no root export; use `{ shallow: true }` / replace the slot |
| `/\*@once\*/` | 🟡 ignored marker | reactive read / `defaultValue` / `untrack` |
| `\.loading\b\|\.error\b` on async values | 🔴 no such props | `<Loading>`/`isPending(() => x())` for loading (bare `refresh()` is normally quiet — pair with `affects()` for a loud reload) / `<Errored>` for error |

### React-isms

| Grep / pattern | Verdict | Fix |
|---|---|---|
| `function \w+\(\s*\{` (destructured props) | 🟡 reactivity dead + warns | `props.x` access |
| `useState\|useEffect\|useMemo\|useRef\|useCallback` | 🔴 wrong framework | Solid primitives |
| `<X value={count} />` passing an accessor where a value is expected | 🔴 child gets a function | `value={count()}` — collapse at the JSX boundary |
| `key=` prop on list items | 🟡 no-op | `<For keyed={...}>` modes |
| `` className\|`${...}` ``/`.join(" ")` class building | 🔵 reflex | `class` array/object form |
| deps-array thinking: effect re-created per "render" | 🟡 model error | components run once; compute phase = deps |

### 2.0-specific

| Pattern | Verdict | Fix |
|---|---|---|
| Single-callback `createEffect(fn)` | 🔴 throws | split `(compute, apply)` |
| `createEffect(fn, 0)` / `createMemo(fn, 0)` initial values | 🔴 wrong arg | options object; `prev` default parameter |
| Setter then immediate read of same signal/DOM | 🔴 stale read | `flush()` or restructure |
| Signal/store write inside memo/compute/component body | 🔴 throws in dev | derive, or move write to handler/action |
| `actionFn()` invoked inside memo/compute/component body | 🔴 dev error (`ACTION_CALLED_IN_OWNED_SCOPE`); may livelock in prod | invoke from handler/effect callback/`onSettled` |
| `ownedWrite: true` on app state | 🟡 escape-hatch abuse | derive instead; ownedWrite is for internal flags |
| `untrack(() => setX(...))` / action or `refresh` hidden in `untrack` | 🔴 still an owned write/call | untrack suppresses read tracking, not ownership; move to an imperative phase |
| Top-level `const x = props.x` / store read in component body | 🟡 warns, stale | read in JSX/memo; `untrack` if deliberate |
| `onCleanup` inside `onSettled`/`createTrackedEffect` | 🔴 throws | return cleanup |
| Cleanup returned from `onSettled` fired out of band (event handler/tracked effect/nested `onSettled`) | 🔴 dev error, dropped in prod | call the setup helper from the component body (owned scope) |
| Primitives created inside `onSettled`/tracked effect | 🔴 throws | create in component body |
| Store proxy passed compute→apply, read in apply | 🟡 warns, won't re-run | extract plain values / `deep(store)` in compute |
| Async read with no `<Loading>` ancestor | 🟡 root mount deferred | add boundary where fallback UI is wanted |
| `async function*` memo over a socket/emitter/observable with no up-front `onCleanup` | 🔴 leaks on dispose/re-run | `onCleanup` (before the first `await`/`yield`) that cancels the source; `try/finally`/`.return()` can't unwind a parked generator |
| `refresh()` called inside a computation | 🔴 throws | call from handlers/actions |
| `until(() => liveValue)` with no timeout/signal on a drop-prone channel | 🟡 action may stay optimistic forever | bound acknowledgement with `{ timeout }` or `{ signal }` |
| `serverFn.GET` property access, `serverFn.withOptions(` on a server function reference | 🔴 removed | `GET(fn)` / `withMeta(fn, meta)` for declaration metadata; `prepareRequest` for session state; `invoke(fn, options, ...args)` for signal/keepalive/priority |
| `fetch(serverFn.url, { body: new URLSearchParams(...) })` in browser code | 🔴 bare form-shaped scripted POST gets 400 before dispatch | call the reference; the runtime uses its `/data/` address and format |
| `GET(...)` around a mutation | 🔴 CSRF/cache contract violation | leave mutations POST-only; declared reads skip the origin gate by default |
| `patchableRaw\|registerPatch\|registerRowOps\|registerSlotPatch\|installListDriver` in app code | 🟡 compiler/runtime internals leaked into app | write normal store updates and `<For>`; compiler integration owns the patch channel |
| `<SelectedContent` | 🔴 wrong JSX intrinsic | lowercase `<selectedcontent>` |
| `renderToStringAsync` | 🔴 no such export | `await renderToStream(code, options)` |
| rich server-function args without `enableRichArguments()` | 🔴 transport throws | call it once from `@solidjs/web/server-functions/rich-args` |
| `<For>` callback shape vs keying mode mismatch (`item()` on keyed, `i()` on `keyed={false}`) | 🔴 type/runtime error | check the mode table |
| Dynamic boolean `keyed={cond()}` with function children | 🟡 ambiguous shape | literal mode or key function |
| `useX`-with-throw context wrapper hooks | 🔵 dead boilerplate | direct `useContext` (throws by itself) |
| camelCase DOM attributes (`tabIndex`, `readOnly`) | 🟡 wrong attribute | lowercase; handlers stay camelCase |
| `merge(..., maybeUndefined)` assuming skip semantics | 🔴 silently overrides | filter keys or restructure defaults |

## Pass 2 — judgement checks (not greppable)

- **Derive vs write-back**: any effect whose apply phase sets reactive state is
  suspect — usually a memo/projection in disguise.
- **Boundary ownership**: `isPending` reads placed under the `Loading` boundary
  that owns the data read? Pending indicators outside can never fire.
- **Mutation shape**: server writes wrapped in `action()` with optimistic
  state and a final `refresh()` or `until()` acknowledgement? If later code
  assumes the refresh finished, it must `await`/`yield refresh()`; ignored
  fire-and-forget is valid only when completion is intentionally unobserved.
- **Action call site**: an action may be defined in a component, but is it
  invoked only from an imperative scope? A component-body/computation call is
  a transaction-starting write and throws in dev mode.
- **Optimistic spinner off `isPending`**: a "Saving…" indicator driven by
  `isPending` on data the same action just wrote optimistically normally stays
  hidden —
  not because the optimistic write masks it (optimistic writes are
  verdict-inert), but because a bare
  `refresh()` after the write is a quiet same-question re-ask. (Published rc.5
  has a narrow held-landing one-frame pulse defect, which is another reason not
  to treat this as process state.) The flag belongs in the data (co-written
  `pending: true` or a separate `createOptimistic(false)`); if the reload
  itself should read pending, that needs an explicit `affects(target)` before
  the `refresh()`.
- **SSR setter writes**: signal/store setters in server render are deprecated
  and warn; optimistic server setters are no-ops. Model incoming changes as
  async sources instead of pushing through setters.
- **Granularity**: selection/derived caches notifying whole collections →
  `createProjection`. Fixed-slot lists diffed with `<For>` → `<Repeat>`.
- **Shallow-store writes**: with `{ shallow: true }`, are nested raw records
  mutated in place? That is inert; replace the root property/array slot by
  reference. When refreshes rebuild row objects, use consumer keying such as
  `<For keyed={row => row.id}>` if row DOM identity must survive.
- **Reconcile model**: omission means key `"id"`, `null` means fully
  positional, and missing item keys fall back positionally. Shape mismatch at
  a nested array/object slot replaces it. Do not approve claims that standalone
  `reconcile` silently swaps a different root entity (it is strict), or the
  inverse claim that projection/derived-store returned roots cannot perform an
  authoritative swap. At a shallow boundary reconciliation compares records
  by reference rather than mutating their fields.
- **Derived-store readiness**: a broad catch around async reads in a derive can
  swallow `NotReadyError`, commit a partial value, and prevent SSR retry. Let
  readiness propagate; do not "stabilize" a projection by catching it.
- **Patch-driver boundary**: published rc.5 can drive eligible ordinary,
  projection, and optimistic store arrays; projection recomputes emit row/slot
  ops and optimistic structural edits emit in-flight row ops plus revert
  resync. Explicit custom-key lists still decline to the classic path, and
  shallow arrays support multiple consumers. Application code must not force
  admission or call patch APIs.
- **Server-function wrapping**: an outer wrapper around a function-level
  directive cannot guard HTTP dispatch, so validation belongs in the body.
  A module-level server file is deliberately different: the evaluated terminal
  wrapped function is registered whole and runs on HTTP + direct SSR. Do not
  report that rc.5 module-level wrapped exports are compile errors.
- **Custom server-function fetch**: does it forward `init`, preserve same-origin,
  return an unread response, and avoid replay after any response was received?
  Dropped signals break abort/live teardown; replay can duplicate mutations.
- **Raw-object assumptions**: platform/native host objects are raw by default;
  their slot reassignment is reactive but internal mutation is not. User class
  instances remain wrappable, and `markRaw` is not a public root API.
- **Ownership**: module-scope effects/roots intentional? Detached lifetime must
  be explicit (`runWithOwner(null, ...)`).
- **Composable naming**: a `createX`/`useX` prefix should match lifecycle, not
  React habit — `createX` makes a fresh instance owned by the caller, `useX` is a
  shared singleton or accesses an already-created thing (`useContext`). `useX` is
  not wrong by itself (singletons are legit); flag only a per-call instance named
  `useX`, or every composable defaulting to `useX` out of reflex.
- **Layout lane**: DOM-geometry reads (`getBoundingClientRect`/`offset*`) belong
  in a `createRenderEffect` (render lane), not in a `ref` callback (node may be
  pre-insert/pre-layout there). Beware the inverse "fix" too: moving a layout
  measure out of `createRenderEffect` into `createEffect`/a ref on the false
  theory that render effects read a disconnected node — they don't; the trigger
  is flush-scheduled and runs after insertion.
- **Tests**: `flush()` after writes; `createRoot` wrappers; `resolve()` for
  async settling.

## Reporting

Report findings ordered by severity with `file:line`, the broken expectation
(one line), and the concrete 2.0 fix. Note clean areas that were checked.
For deep API verification during review, the `solidjs-v2` skill's references
cover signatures; installed typings in `node_modules` are the final word for a
moving prerelease API.
