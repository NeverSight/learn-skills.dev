---
name: add-mod-resolver
description: Use when adding new push* resolver functions inside resolveModsForOffenseSkill to handle mod-based combat mechanics like tangles, debuffs, or conditional damage bonuses (project)
---

# Adding Mod Resolvers

## Overview

Mod resolvers are `push*` functions defined inside `resolveModsForOffenseSkill` in `src/tli/calcs/offense.ts`. They read from the `mods` array (and optionally `config`, `prenormMods`, `resourcePool`, `defenses`) and push new derived mods based on game mechanics. Each resolver handles one mechanic (e.g., frostbite, numbed, tangles, infiltrations).

## When to Use

- Adding a new combat mechanic that derives mods from existing mods or configuration
- Adding conditional damage bonuses based on presence of a flag mod (e.g., `IsTangle`, `WindStalker`)
- Adding enemy debuff calculations (e.g., numbed stacks, frostbite, frail)
- Adding buff/aura effect calculations with effect multipliers

## Project File Locations

| Purpose | File Path |
|---------|-----------|
| Resolver function location | `src/tli/calcs/offense.ts` (inside `resolveModsForOffenseSkill`) |
| Mod type definitions | `src/tli/mod.ts` (`ModDefinitions` interface) |
| Configuration interface & defaults | `src/tli/core.ts` (`Configuration`, `DEFAULT_CONFIGURATION`) |
| Mod helper utilities | `src/tli/calcs/mod-utils.ts` |
| Tests | `src/tli/calcs/offense.test.ts` |

## Architecture

`applyModFilters` preprocesses all mods into four groups:
- `mods` — non-per mods without `condThreshold` or `resolvedCond` (ready to use immediately)
- `prenormMods` — all mods without `resolvedCond` (source for per-stackable normalization)
- `condThresholdMods` — non-per mods with `condThreshold` (pushed back by `normalize()` when threshold is met)
- `resolvedCondMods` — mods with `resolvedCond` (pushed back by individual `push*` resolvers when condition is met)

**IMPORTANT: Mods with a `per` field are filtered into `prenormMods` only — they do NOT appear in `mods`.** The `per` field (from `ModBase`) triggers automatic per-stackable normalization via `normalize()`. If a mod needs custom resolver logic (e.g., applying an effect multiplier before scaling by stacks), do NOT use `per` on the mod type. Instead, store the scaling info in a custom field (e.g., `perFervorAmt: number`) so the mod stays in `mods` and the resolver can find it via `filterMods()`.

`resolveModsForOffenseSkill` then runs a sequence of `push*` resolver functions that push new derived mods into `mods` via `pm()`. Each `push*` function is a closure that captures:
- `mods: Mod[]` — the shared mutable array of resolved mods
- `prenormMods` — mods needing per-stackable normalization
- `condThresholdMods` — mods held back until their stackable threshold is evaluated by `normalize()`
- `resolvedCondMods` — mods held back until their resolved condition is evaluated by a `push*` resolver
- `config: Configuration` — user-configured combat parameters
- `resourcePool` — stats, mana, blessings, etc.
- `defenses` — armor, evasion, resistances, etc.
- `loadout: Loadout` — full parsed loadout
- Helper functions: `pm()` (push mods), `normalize()` (normalize stackables), `step()` (dependency tracking)

The execution sequence begins with `normalizeFromConfig()`, which normalizes all stackables whose values come purely from `config` fields (e.g., `level`, `num_enemies_nearby`, `enemy_numbed_stacks`). This runs before `pushStatNorms()` and all other resolvers. Normalize calls whose values depend on mods, stats, defenses, or resourcePool remain in their respective `push*` functions or inline in the execution sequence.

## Available Helpers

From closure (defined in `resolveModsForOffenseSkill`):
- `pm(...ms: Mod[])` — shorthand for `mods.push(...ms)`
- `normalize(stackable, value)` — normalizes per-stackable mods from `prenormMods` and pushes satisfied `condThresholdMods` for that stackable
- `normalizeFromConfig()` — calls `normalize()` for all stackables whose values come purely from `config` fields; called once at the start of the execution sequence before `pushStatNorms()`
- `step(stepName)` — registers a step for dependency tracking (only needed if other steps depend on this one)
- `resolvedCondMods: Mod[]` — mods with `resolvedCond`, separated out by `applyModFilters`; push matching ones into `mods` via `pm()` when the condition is met
- `condThresholdMods: Mod[]` — non-per mods with `condThreshold`, separated out by `applyModFilters`; pushed back automatically by `normalize()` when their stackable threshold is met

From `src/tli/calcs/mod-utils.ts`:
- `modExists(mods, "ModType")` — returns `boolean`, checks if any mod of that type exists
- `findMod(mods, "ModType")` — returns first mod of type or `undefined`
- `filterMods(mods, "ModType")` — returns all mods of type as `ModT<T>[]`
- `sumByValue(mods)` — sums `.value` of all mods in array
- `calcEffMult(mods, "ModType")` — calculates `(1 + sum_of_inc) * product_of_addn` multiplier
- `multModValue(mod, multiplier)` — returns new mod with `.value` multiplied

## Implementation Checklist

### 1. Ensure the Trigger Mod Type Exists

Check `src/tli/mod.ts` under `ModDefinitions`. If the flag mod (e.g., `IsTangle`) doesn't exist, add it:

```typescript
// In ModDefinitions
IsTangle: object;  // flag mod, no fields
```

For mods with data:
```typescript
NumbedEffPct: { value: number };
```

### 2. Ensure Configuration Fields Exist (if needed)

If the resolver needs user-configurable values, ensure they exist in `src/tli/core.ts`. Use the `/add-configuration` skill if they don't.

### 3. Write the push* Function

Define the function inside `resolveModsForOffenseSkill`, near related resolvers. Follow these patterns:

**Simple flag-based resolver (multiplies damage by a config value):**
```typescript
const pushTangle = (): void => {
  if (!modExists(mods, "IsTangle") || config.numActiveTangles <= 1) return;
  mods.push({
    type: "DmgPct",
    dmgModType: "global",
    addn: true,
    value: (config.numActiveTangles - 1) * 100,
    src: "Tangle",
  });
};
```

**Debuff with effect multiplier:**
```typescript
const pushNumbed = (): void => {
  if (!config.enemyNumbed) return;
  const numbedStacks = config.enemyNumbedStacks ?? 10;
  const numbedEffMult = calcEffMult(mods, "NumbedEffPct");
  const baseValPerStack = 5;
  const numbedVal = baseValPerStack * numbedEffMult * numbedStacks;
  mods.push({
    type: "DmgPct",
    value: numbedVal,
    dmgModType: "lightning",
    addn: true,
    isEnemyDebuff: true,
    src: "Numbed",
  });
};
```

**Buff with effect multiplier (e.g., aggression, mark):**
```typescript
const pushMark = (): void => {
  if (!config.targetEnemyMarked) return;
  const markEffMult = calcEffMult(mods, "MarkEffPct");
  const baseValue = 20;
  mods.push({
    type: "CritDmgPct",
    value: baseValue * markEffMult,
    addn: true,
    modType: "global",
    isEnemyDebuff: true,
    src: "Mark",
  });
};
```

**Resolver with per-stackable normalization:**
```typescript
const pushPactspirits = () => {
  const addedMaxStacks = sumByValue(filterMods(mods, "MaxPureHeartStacks"));
  const maxStacks = 5 + addedMaxStacks;
  const stacks = config.pureHeartStacks ?? maxStacks;
  normalize("pure_heart", stacks);
};
```

**Config-only normalization (add to `normalizeFromConfig`):**

If the stackable value comes purely from `config` fields (no dependency on mods, stats, defenses, or resourcePool), add the `normalize()` call inside `normalizeFromConfig()` instead of creating a separate push* function or placing it inline in the execution sequence:

```typescript
const normalizeFromConfig = (): void => {
  // ... existing config-based normalizes ...
  normalize("new_stackable", config.newStackableValue ?? defaultValue);
};
```

Only use a separate `push*` function or inline `normalize()` when the value depends on computed data (mods, stats, etc.), or when the value has a config override with a mod-computed fallback (e.g., `config.stacks ?? maxStacksFromMods`).

**Resolved condition resolver (conditions that depend on calculated values):**

Some mod conditions can't be evaluated statically from configuration — they depend on values calculated earlier in `resolveModsForOffenseSkill` (e.g., sealed mana/life percentages come from `resourcePool.sealedResources`, not config). These use `resolvedCond` on the mod (see `ResolvedCondition` in `mod.ts`) instead of `cond` (which is for static `Configuration`-based conditions evaluated in `filterModsByCond`).

Mods with `resolvedCond` are separated out by `applyModFilters` into `resolvedCondMods`. The push* resolver filters for its condition and pushes matching mods into `mods` via `pm()` when the condition is met.

```typescript
const pushHasSealedLifeAndManaCond = (): void => {
  const { sealedManaPct, sealedLifePct } = resourcePool.sealedResources;
  if (sealedManaPct <= 0 || sealedLifePct <= 0) return;
  pm(
    ...resolvedCondMods.filter(
      (m) => m.resolvedCond === "have_both_sealed_mana_and_life",
    ),
  );
};
```

To add a new resolved condition:
1. Add the condition string to `ResolvedConditions` in `src/tli/mod.ts`
2. In the mod parser template (`src/tli/mod-parser/templates.ts`), use `resolvedCond: "condition_name"` instead of `cond: "condition_name"`
3. Write a `push*` resolver that filters `resolvedCondMods` and pushes matching mods via `pm()`, and call it at the appropriate point in the execution sequence

**Resolver with step dependencies (when one resolver produces mods consumed by another):**

Use `step()` and `stepDeps` whenever a resolver pushes mods that another resolver later reads. For example, `pushFervor` generates `SkillAreaPct` mods, so `pushSkillArea` depends on it. The dependency graph is validated at test time — if `pushSkillArea` runs before `pushFervor`, an error is recorded.

1. Register both steps and their dependency in `stepDeps` (above `resolveModsForOffenseSkill`):
```typescript
const stepDeps = createSelfReferential({
  // ... existing steps ...
  fervor: [],
  skillArea: ["fervor"],  // skillArea must run after fervor
});
```

2. Call `step()` at the top of each resolver:
```typescript
const pushFervor = () => {
  step("fervor");
  if (resourcePool.hasFervor) {
    mods.push(calculateFervorCritRateMod(mods, resourcePool));
    mods.push(...calculateFervorBaseEffSkillArea(mods, resourcePool));
    normalize("fervor", resourcePool.fervorPts);
  }
};

const pushSkillArea = (): void => {
  step("skillArea");
  const skillAreaPct = sumByValue(filterMods(mods, "SkillAreaPct"));
  normalize("skill_area", skillAreaPct);
};
```

3. Ensure the call order in the execution sequence matches the dependency graph (dependent runs after dependency):
```typescript
pushFervor();    // must come first
pushSkillArea(); // depends on fervor
```

`step()` always goes at the top of the resolver, before any early returns, so the step is registered even if the resolver short-circuits.

### 4. Call the Function

Add the call in the execution sequence inside `resolveModsForOffenseSkill`. Place it near related mechanics. 

### 5. Verify

```bash
pnpm test
pnpm typecheck
pnpm check
```

## Common Patterns

| Pattern | When to Use | Key Helper |
|---------|-------------|------------|
| Check flag mod exists | Mechanic only applies when a specific support/skill mod is present | `modExists(mods, "FlagMod")` |
| Check config boolean | Mechanic depends on user toggle | `if (!config.someToggle) return` |
| Effect multiplier | Buff/debuff has mods that scale its effectiveness | `calcEffMult(mods, "SomeEffPct")` |
| Config stacks with default | User can override stack count, defaults to max | `config.someStacks ?? maxStacks` |
| Normalize stackable | Mechanic involves per-stackable scaling with computed value | `normalize("stackable_name", value)` |
| Config-only normalize | Stackable value comes purely from config | Add to `normalizeFromConfig()` |
| Filter by resolved condition | Condition depends on calculated values, not static config | `pm(...resolvedCondMods.filter(...))` |
| `addn: true` on DmgPct | More multiplier (multiplicative with other `addn: true` mods) | — |
| `addn: false` on DmgPct | Increased multiplier (additive with other `addn: false` mods) | — |
| `isEnemyDebuff: true` | Damage increase from enemy debuff (for display grouping) | — |
| `src: "Name"` | Label for debug/display panel | — |

## DmgPct addn Field

The `addn` (additional) field on `DmgPct` controls how the damage bonus stacks:

- `addn: false` — **Increased** damage. All `addn: false` mods sum together into one multiplier: `(1 + sum)`.
- `addn: true` — **More** damage. Each `addn: true` mod is its own separate multiplier: `(1 + value1) * (1 + value2) * ...`

Most resolvers use `addn: true` because their effects are multiplicative with other damage sources.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Forgetting early return when flag/config is absent | Always guard with `if (!condition) return` |
| Using `addn: false` when the mechanic should be multiplicative | Use `addn: true` for separate "more" multipliers |
| Pushing mods without `src` | Always include `src` for debug panel visibility |
| Forgetting to add config field | Use `/add-configuration` skill first |
| Missing `step()` when a resolver produces mods consumed by another | Add both steps to `stepDeps` with the dependency, and call `step()` at the top of each resolver |
| Not matching execution order to `stepDeps` | The call order must satisfy the dependency graph — dependent resolvers run after their dependencies |
| Not handling undefined config with `??` | Optional config values need fallback: `config.stacks ?? defaultMax` |
| Placing config-only normalize inline in execution sequence | Add to `normalizeFromConfig()` instead; only use inline/push* for computed values |
| Using `per` on a mod that needs custom resolver logic | Mods with `per` go to `prenormMods`, not `mods`, so `filterMods(mods, ...)` won't find them. Use a custom field (e.g., `perFervorAmt: number`) instead so the mod stays in `mods` for the resolver to read |
