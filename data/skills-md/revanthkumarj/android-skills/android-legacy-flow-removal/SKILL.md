---
name: android-legacy-flow-removal
description: |
  Deleting a dead legacy flow end to end without breaking a live one - proving unreachability by destination id rather than class name, mapping the shared-component graph, layouts, nav-graph actions, DI, ViewModel trimming, and the repository to service to models cascade, including the trap of identically named classes in two modules. Use this skill whenever deleting an old screen, flow, or feature. Trigger on phrases like "remove the old screen", "delete this flow", "is this code dead", "clean up the legacy XML", or "can I delete this fragment".
---

# Skill: Removing a Legacy XML Flow (UI → DI → data → models)

> Apply **android-working-discipline** (verification, self-attack, final gate) while executing this skill.

## When to use this skill

When deleting an old XML screen that Compose has replaced — "remove the old XML code for X". Also read
[**android-cross-module-navigation** §3b](**android-cross-module-navigation**) when the old flow is behind a
**feature flag** — the flag and its branches come out first; this skill covers everything after that.

**The deletion is never just the Fragment.** A screen owns a tail: adapters, bottom sheets, layouts, a
ViewModel, nav-graph entries, a DI registration, repository methods, a Retrofit service endpoint, and
request/response models. Leaving that tail behind is the usual failure — it compiles fine and rots
forever. Work the layers in order, top-down.

---

## 0. Prove the screen is unreachable — before deleting anything

A `<fragment>` block in the nav graph proves nothing. What matters is whether **Kotlin** can reach it:

```bash
grep -rn "R.id.myFragment\|action_.*_to_myFragment" --include="*.kt" .
```

Check **both** forms — the destination id (`navigate(R.id.x)`) and every `action_*` id that targets
it. Actions live under the **source** destination, so grep the whole nav graph for
`app:destination="@id/myFragment"`, not just the block you are about to delete.

Three outcomes:

- **No Kotlin references** → dead, delete freely. This is the ideal case: the Compose replacement
  already took over with no flag.
- **Referenced behind a `useNewX()` flag** → still live; retire the flag first, or leave it alone.
- **Referenced unconditionally** → still live. Say so and stop; don't "fix" the caller unless asked.

> **Half a feature is usually still alive.** In one real removal, create/edit were dead (a Compose
> flow had replaced them with no flag) while the **list** screen stayed reachable from three separate
> menus and **details** stayed behind a flag. **Establish per-screen reachability, not per-package.**

---

## 1. Map the cluster before you delete one file

For each class in the old package, list its consumers:

```bash
for c in MyFragment MyViewModel MyItemAdapter MySheet; do
  echo "== $c"; grep -rln "$c" --include="*.kt" .
done
```

Read the result as a **graph**, not a list. A shared bottom sheet stays alive as long as **any**
consumer lives — so a dead sibling screen can be what is blocking a whole package. In one removal,
four bottom sheets and an adapter were shared between the create and update fragments; only deleting
**both** fragments unlocked the whole package. Deleting the sibling was in scope because it was
equally unreachable — but **say so explicitly in the report** rather than sliding it in.

Expect to find files that were **already** dead before your task, with zero references. Sweep them out
with the cluster and list them separately.

---

## 2. Layouts

For each layout the dying classes inflate, check two things:

```bash
grep -rln "MyScreenBinding" --include="*.kt" .       # view-binding class consumers
grep -rln "@layout/my_screen" app/src/main/res/       # <include>, tools:listitem, adapters
```

Item layouts are frequently **shared** between a dying screen and a living one. A layout referenced
only by other dying layouts goes; one referenced by a surviving adapter stays.

Leave orphaned `strings.xml` / `dimens.xml` entries alone unless asked — unused resources are inert,
and grepping them per key is a large, low-value sweep.

---

## 3. The navigation graph

Delete, in this order:

1. Every `<action>` **anywhere in the file** whose `app:destination` (or `app:popUpTo`) points at the
   dying id — wherever its source destination happens to be.
2. The `<fragment>` / `<dialog>` block itself.

An orphaned action referencing a deleted id is a **runtime crash, not a compile error**. After
editing, re-grep the id across the graph and confirm zero hits.

> Watch for actions whose name doesn't match their target — e.g. an action named
> `action_dashboardFragment_to_createIncomeFragment` that actually points at
> `createExpenseFragment`. **Grep by destination, never by action name.**

---

## 4. DI registrations

- The ViewModel module — the `viewModel { MyViewModel(...) }` line **and** its import.
- The app module — adapters are sometimes DI-registered too. Grep the class name across the whole
  `di/` package before assuming only the fragment referenced it.

A stale registration for a deleted class is a compile error, so this step is self-checking — but the
orphaned import is easy to leave behind.

---

## 5. ViewModel: delete or trim

Grep the ViewModel across the repo. Two cases:

- **Exclusive to the dying screen(s)** → delete the file + its DI line.
- **Shared** → keep the file and **trim to the members the survivors actually use**.

To trim safely, grep each member in each surviving consumer — don't eyeball it:

```bash
grep -n "myViewModel\." SurvivingFragment.kt | grep -E "member1|member2"
```

Then prune the imports the removed members needed.

### Shared-ViewModel fields

Old XML flows often stash their in-flight request objects on a god-object `SharedViewModel`. Those
die with the screen. Grep each field repo-wide before removing, and prune the imports left dangling —
including the incidental ones (`Constants`, `Utils`, `java.util.Date`) that existed only for the field
initialisers.

Be careful with fields that *look* the same: a `selectedX` used by three other adapters stays.

---

## 6. The data layer — repository → service (this is the step that gets skipped)

Once the ViewModel is gone or trimmed, its repository calls are dead. Walk the legacy chain **all four
levels**:

```
domain/repository/XRepository.kt              (interface declaration)
  → data/repository/.../XRepositoryImpl.kt      (override)
    → data/repository/.../XRemoteRepository.kt  (try/catch + result wrapper)
      → data/network/AppService.kt              (@POST/@GET/@DELETE + fun)
```

Removing only the interface method leaves three dead bodies behind that still compile.

Check each method against **all** remaining consumers of the repository first — a repository is
usually shared across several screens.

### ⚠️ The two-stacks trap — the most dangerous part of this whole skill

A part-migrated app has **identically named** endpoints, data sources and models in the legacy `:app`
module and in the modern `core:network` module:

| Legacy (`:app`) — deletable | Modern (`core:network`) — **never delete** |
|---|---|
| `data/network/AppService.kt` | `core/network/.../AppNetworkApi.kt` |
| `data/repository/.../XRemoteRepository.kt` | `core/network/.../RemoteDataSource(Impl).kt` |
| `com.example.app.data.model.requests/responses.*` | `com.example.core.network.model.request/response.*` |

A grep for `createX` returns **both** stacks. The `core:network` copies are what the live Compose
feature calls. **Always read the file path in every grep hit before deleting**; filter with
`grep … app/src` when you mean the legacy stack only.

The same trap applies to constants: a legacy `Constants.SOME_ID` is safe to delete only because the
Compose side holds its own copy elsewhere. Verify, don't assume.

---

## 7. Models (last layer)

After the service methods go, their request/response classes are often orphaned. Verify per class,
excluding its own file:

```bash
grep -rl "\bMyResponse\b" --include="*.kt" --include="*.xml" app/src | grep -v "MyResponse.kt"
```

Nested classes are safe to check this way — `Outer.Inner` and `import ….Outer.Inner` both contain the
outer name.

> **The subtlety that decides this:** a model can survive because one surviving class still uses it —
> and a grep hit on a model name is **not** proof of use when two stacks share the name. One real file
> imported the *core* `EditXRequest` and the *app* `CreateXRequest` in the same file. **Open the file
> and check which import each name resolves to.**

Also check `proguard-rules.pro` and the test source sets before deleting a model.

---

## 8. Verification (assuming you cannot run a build)

Run a name-based sweep over every removed symbol across all source sets:

```bash
for s in DeletedClass deletedMethod DELETED_CONSTANT; do
  r=$(grep -rn "\b$s\b" --include="*.kt" --include="*.xml" app/src core feature)
  [ -n "$r" ] && { echo "== $s"; echo "$r"; }
done
```

Every surviving hit must be **explainable** — a same-named modern twin, or an unrelated parameter name
like `createXRequest:`. Then re-grep the nav graph for the deleted ids, and ask the user to build.
Say plainly that you could not compile.

---

## Order of operations (checklist)

1. Prove unreachability (grep destination id + all `action_*` ids in Kotlin).
2. Map the cluster; identify shared members and the siblings that block them.
3. `git rm` fragments, adapters, bottom sheets, exclusive layouts.
4. Nav graph: actions targeting the id (anywhere), then the destination block.
5. DI entries + imports.
6. ViewModel: delete if exclusive, trim member-by-member if shared. Then shared-ViewModel fields + imports.
7. Data layer: interface → impl → remote repo → service, method by method, checking other consumers at each level.
8. Models: per-class grep excluding its own file; check which stack each importer resolves to.
9. Sweep + report what you kept and why; state that no build was run.

## Report format

List **deleted**, **edited**, **kept deliberately (with reason)**, and **not touched / next layer**
separately.

The "kept deliberately" section is what makes the change reviewable — a flag-gated sibling screen, a
shared item layout, and the modern same-named twins all *look* like misses otherwise.

When the next layer down is dead but outside the literal ask, name it and let the user decide, rather
than expanding scope silently.
