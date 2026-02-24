---
name: unity-reusable-systems
description: >-
  Use when building reusable Unity game systems, creating UPM packages, or
  designing ScriptableObject-based modular architecture for gameplay systems
  like inventory, combat, dialogue, quests, or save/load. Also use when
  connecting multiple independent Unity packages that need to communicate
  without direct dependencies.
---

# Unity Reusable Systems

Build every gameplay system as a self-contained UPM package. Data lives in
ScriptableObjects, behavior lives in small single-responsibility MonoBehaviours,
and systems talk through SO Event Channels — never direct references.

Target: Unity 6+ / C# 11.

## The Rules

| ALWAYS | NEVER |
|--------|-------|
| One system = one UPM package | Create a "shared contracts" package with interfaces |
| Data in ScriptableObjects, behavior in MonoBehaviours | Put data and behavior in the same class |
| MonoBehaviour `[SerializeField]` only for SO refs, component refs, scene refs, UnityEvents | `[SerializeField]` primitives (float, int, bool, string, LayerMask, enum, AnimationCurve) directly on MonoBehaviours — these belong in an SO Config asset |
| SO Event Channels for cross-system communication | Use singletons, service locators, or static managers |
| One assembly definition per folder (Runtime, Editor, Tests) | Ship without assembly definitions |
| Version Defines for optional cross-package awareness | Use `#if` defines without versionDefines in asmdef |
| Define Constraints for conditional integration assemblies | Create hard dependencies between gameplay packages |
| Small MonoBehaviours with `[RequireComponent]` | God classes that handle input + logic + rendering |
| ScriptableVariable for shared runtime state | Public static fields or global state holders |
| RuntimeSet for tracking active instances | FindObjectsOfType or singleton registries |
| `Awaitable` with `destroyCancellationToken` for async | Coroutines for new async work |
| `[SerializeReference]` for polymorphic serialized data | Deep inheritance hierarchies |
| Composition: many small components on one GameObject | One MonoBehaviour doing everything |
| Interfaces only at package boundaries when SO Events can't solve it | Interfaces inside a single package |
| Tests using ScriptableObject.CreateInstance in Edit Mode | Skipping tests because "it's just a SO" |
| Editor menu item that generates a fully-wired sample scene | Shipping a package without a one-click working demo scene |
| Generate `docs/packages/<package-name>.md` with full integration surface | Create a package without documenting its public events, variables, and interfaces |
| Read all `docs/packages/*.md` before designing a new package | Design a new package without checking what existing packages expose |

## Where Does This Code Belong?

- Data or config? → **ScriptableObject**
- Needs MonoBehaviour lifecycle? → **MonoBehaviour**
- Editor-only tooling? → **Editor/ folder** (EditorWindow / PropertyDrawer)
- Pure logic, no Unity deps? → **Plain C# class** in Runtime/
- Otherwise → **MonoBehaviour**

## How Should Systems Communicate?

- Same package, same GameObject/parent-child? → **C# event/delegate**
- Same package, different GameObjects? → **SO Event Channel**
- Cross-package, sharing runtime state? → **ScriptableVariable**
- Cross-package, always installed together? → **SO Event Channel**
- Cross-package, optionally installed? → **Version Defines + SO Event Channel or bridge package**

## Integration Discovery

Before designing a new package, read every file in `docs/packages/*.md`. These documents describe the integration surface of each existing package — their event channels, ScriptableVariables, RuntimeSets, and interfaces.

**Discovery steps:**

1. Read all `docs/packages/*.md` files. If the folder doesn't exist, this is the first package — skip to step 4.
2. List every event channel, ScriptableVariable, RuntimeSet, and interface from existing packages that is relevant to the new package.
3. Produce an **Integration Plan** as part of the new package design:
   - **Listen to** — existing events the new package should subscribe to (via Version Defines)
   - **Publish** — new events the new package should raise for others to consume
   - **Read/Write** — existing ScriptableVariables the new package should use
   - **Expose** — new ScriptableVariables the new package should create for shared state
   - **Implement** — existing interfaces the new package should implement
   - **Bridge needed?** — whether a Bridge Package is required for complex cross-package logic
   - **Suggested changes to existing packages** — checklist of Version Defines, listeners, or asmdef updates other packages could add to become aware of the new package
4. After building the package, generate `docs/packages/<package-name>.md` (see Package Integration Doc below).

## MonoBehaviour Field Rule

A MonoBehaviour's `[SerializeField]` fields must only be references — never raw config values.

**Allowed on a MonoBehaviour:**
- SO references: config SOs, event channels, ScriptableVariables, RuntimeSets
- Component / GameObject references (scene wiring)
- UnityEvents (designer-hookable callbacks)

**Belongs in an SO Config asset instead:**
- Primitives and value types: float, int, bool, string, enum
- Unity structs: LayerMask, Color, AnimationCurve, Vector2/3
- Arrays/lists of the above

WRONG — config on the component:

```csharp
public class GroundDetector2D : MonoBehaviour
{
    [SerializeField] private LayerMask groundLayers;   // config!
    [SerializeField] private float boxWidth = 0.9f;    // config!
    [SerializeField] private float castDistance = 0.1f; // config!
}
```

RIGHT — config in an SO, component holds one reference:

```csharp
[CreateAssetMenu(menuName = "Platformer2D/Ground Detection Config")]
public class GroundDetectionConfig : ScriptableObject
{
    public LayerMask groundLayers;
    public float boxWidthMultiplier = 0.9f;
    public float castDistance = 0.1f;
}

[RequireComponent(typeof(Collider2D))]
public class GroundDetector2D : MonoBehaviour
{
    [SerializeField] private GroundDetectionConfig config; // one SO ref
}
```

## Core SO Patterns

### SO Config

A ScriptableObject holding only serialized fields — designer-tunable settings. **Every primitive you'd put on a MonoBehaviour belongs here instead.**

```csharp
[CreateAssetMenu(menuName = "Combat/Weapon Config")]
public class WeaponConfig : ScriptableObject
{
    public float baseDamage = 10f;
    public float critMultiplier = 2f;
    public LayerMask hitLayers;
    public float attackRange = 1.5f;
}
```

### ScriptableVariable\<T\>

Shared runtime state as an asset. Any component can read/write. Resets on play mode exit.

```csharp
public abstract class ScriptableVariable<T> : ScriptableObject
{
    [SerializeField] private T initialValue;
    [System.NonSerialized] private T runtimeValue;

    public T Value
    {
        get => runtimeValue;
        set => runtimeValue = value;
    }

    private void OnEnable() => runtimeValue = initialValue;
}

// Concrete types for the serializer:
[CreateAssetMenu(menuName = "Variables/Float")]
public class FloatVariable : ScriptableVariable<float> { }
```

### SO Event Channel

Fire-and-forget broadcast. Publishers and subscribers share an asset reference — never each other.

```csharp
[CreateAssetMenu(menuName = "Events/Game Event")]
public class GameEvent : ScriptableObject
{
    private readonly List<Action> listeners = new();

    public void Raise()
    {
        for (int i = listeners.Count - 1; i >= 0; i--)
            listeners[i]?.Invoke();
    }

    public void Subscribe(Action listener) => listeners.Add(listener);
    public void Unsubscribe(Action listener) => listeners.Remove(listener);
}
```

Create one concrete SO per payload type (void, float, int, Vector3, DamageInfo, etc.). Generic SO base classes are not directly serializable — always create concrete leaf types.

### GameEventListener

Bridges SO Event Channels to the scene via UnityEvent. Designers wire responses in the Inspector.

```csharp
public class GameEventListener : MonoBehaviour
{
    [SerializeField] private GameEvent gameEvent;
    [SerializeField] private UnityEvent response;

    private void OnEnable() => gameEvent.Subscribe(OnEventRaised);
    private void OnDisable() => gameEvent.Unsubscribe(OnEventRaised);

    private void OnEventRaised() => response.Invoke();
}
```

### RuntimeSet\<T\>

Self-registering collection of active instances. Replaces `FindObjectsOfType`.

```csharp
public abstract class RuntimeSet<T> : ScriptableObject
{
    private readonly List<T> items = new();
    public IReadOnlyList<T> Items => items;

    public void Add(T item) { if (!items.Contains(item)) items.Add(item); }
    public void Remove(T item) => items.Remove(item);
}
```

## Component Composition

One entity, multiple focused components. Each MonoBehaviour references SOs — never raw config.

```csharp
[RequireComponent(typeof(HealthComponent))]
public class Mover : MonoBehaviour
{
    [SerializeField] private FloatVariable moveSpeed; // ScriptableVariable
    public void Move(Vector3 direction) =>
        transform.Translate(direction * moveSpeed.Value * Time.deltaTime);
}

public class WeaponController : MonoBehaviour
{
    [SerializeField] private WeaponConfig config;  // SO Config
    [SerializeField] private GameEvent onAttack;    // SO Event Channel
    public void Attack() => onAttack.Raise();
}
```

## Package Structure

```
com.{company}.{system}/
├── package.json
├── Runtime/
│   ├── {Company}.{System}.asmdef
│   ├── Components/          # MonoBehaviours
│   ├── Data/                # ScriptableObjects (config, definitions)
│   ├── Events/              # SO Event Channels
│   └── Variables/           # ScriptableVariables, RuntimeSets
├── Editor/
│   ├── {Company}.{System}.Editor.asmdef
│   └── SampleSceneGenerator.cs
├── Tests/
│   └── Editor/
│       └── {Company}.{System}.Tests.asmdef
└── Samples~/
    └── BasicUsage/
```

Runtime asmdef — use `versionDefines` for optional cross-package awareness:

```json
{
  "name": "MyStudio.Inventory",
  "rootNamespace": "MyStudio.Inventory",
  "references": [],
  "versionDefines": [
    {
      "name": "com.mystudio.crafting",
      "expression": "1.0.0",
      "define": "MYSTUDIO_CRAFTING"
    }
  ]
}
```

## Sample Scene Generator (Required)

Every package must include `Editor/SampleSceneGenerator.cs` with menu item `Tools/{Company}/{System}/Create Sample Scene`. The generator must:

1. Create a new scene
2. Instantiate all SO assets (config, event channels, variables, runtime sets) into a data folder
3. Create GameObjects with all components attached
4. Wire every `[SerializeField]` — SO references, event channels, variables
5. Press Play → system works without manual setup

## Package Integration Doc

Every package must have a project-level integration doc at `docs/packages/<package-name>.md`. Generate this as the final step of package creation. If the `docs/packages/` directory doesn't exist, create it.

Required sections:

```markdown
# <package-name> — Integration Surface

## Event Channels

| Event | Payload Type | Raised When | Suggested Listeners |
|-------|-------------|-------------|---------------------|
| `OnX` | `void` / concrete type | Description of trigger | Systems that should react |

## ScriptableVariables

| Variable | Type | Purpose |
|----------|------|---------|
| `VarName` | `FloatVariable` / concrete type | What this variable represents |

## RuntimeSets

| Set | Item Type | Purpose |
|-----|-----------|---------|
| `SetName` | `ComponentType` | What instances this set tracks |

## Interfaces (Package Boundary)

| Interface | Purpose | When to Implement |
|-----------|---------|-------------------|
| `IName` | What contract it defines | When another package should implement it |

## Assembly & Version Define

- **Assembly:** `{Company}.{System}`
- **Package ID:** `com.{company}.{system}`
- **Version Define symbol:** `{COMPANY}_{SYSTEM}`

## Integration Examples

- **SystemA** → listen to `OnX`, do Y
- **SystemB** → read `VarName`, display Z
```

Omit any section that has no entries (e.g., if the package exposes no interfaces, omit "Interfaces"). Never omit Event Channels or Assembly & Version Define — every package has at least one event and an assembly.

## Testing

Test asmdef in `Tests/Editor/`:

```json
{
  "name": "MyStudio.Inventory.Tests",
  "references": ["MyStudio.Inventory", "UnityEngine.TestRunner", "UnityEditor.TestRunner"],
  "includePlatforms": ["Editor"],
  "overrideReferences": true,
  "precompiledReferences": ["nunit.framework.dll"],
  "testAssemblies": true
}
```

Create SO instances in code, test, destroy. Never depend on asset files:

```csharp
[TestFixture]
public class FloatVariableTests
{
    private FloatVariable variable;

    [SetUp]
    public void SetUp() => variable = ScriptableObject.CreateInstance<FloatVariable>();

    [TearDown]
    public void TearDown() => Object.DestroyImmediate(variable);

    [Test]
    public void Value_AfterSet_ReturnsNewValue()
    {
        variable.Value = 42f;
        Assert.AreEqual(42f, variable.Value);
    }
}
```

Edit Mode unless you need MonoBehaviour lifecycle or physics. Edit Mode tests are faster and more reliable.

## New Package Checklist

Before shipping any package, verify:

- [ ] Read all `docs/packages/*.md` and produce an Integration Plan before designing
- [ ] `package.json` with correct `name`, `version`, `unity` (6000.0+), `displayName`
- [ ] `Runtime/` with `{Company}.{Package}.asmdef` — zero external references
- [ ] `Editor/` with Editor-only asmdef (if any editor code exists)
- [ ] `Tests/Editor/` with test asmdef using `overrideReferences` and `testAssemblies`
- [ ] `Samples~/` with at least one importable sample
- [ ] Editor menu item under `Tools/{Company}/{System}/Create Sample Scene` that generates a fully-wired demo scene — all SO assets instantiated, all components on GameObjects, all event channels and variables assigned, playable on first run
- [ ] `CHANGELOG.md` following SemVer
- [ ] All SOs have `[CreateAssetMenu]` with organized menu paths
- [ ] All MonoBehaviours use `[RequireComponent]` where applicable
- [ ] No `[SerializeField]` primitives on MonoBehaviours — all config in SO assets
- [ ] SO Event Channels for every output event (no direct subscriber lists)
- [ ] ScriptableVariables for any shared runtime state
- [ ] RuntimeSets for any "all active X" queries
- [ ] Version Defines in asmdef for any optional package awareness
- [ ] No `FindObjectsOfType`, no singletons, no static mutable state
- [ ] Generate `docs/packages/<package-name>.md` with all events, variables, RuntimeSets, interfaces, and integration examples

## Reference Files

For deeper details — extended code, edge cases, and advanced patterns:

- **[references/package-structure.md](references/package-structure.md)** — Sample scene generator full code, Define Constraints, SemVer rules, distribution
- **[references/so-architecture.md](references/so-architecture.md)** — Typed event channels, RuntimeSetMember, reset strategy details
- **[references/patterns.md](references/patterns.md)** — Cross-package integration table, bridge packages, SerializeReference + polymorphism, Awaitable async
- **[references/integration-discovery.md](references/integration-discovery.md)** — Full integration doc template, discovery workflow example, bridge package decision criteria
- **[references/testing.md](references/testing.md)** — SO Event Channel test patterns, Edit vs Play Mode guidance, mocking
