---
name: lens-studio-scripting
description: Reference guide for the Lens Studio TypeScript component system — covering the @component, @input, @hint, @allowUndefined, and @label decorators, the BaseScriptComponent lifecycle (onAwake vs OnStartEvent, UpdateEvent, DelayedCallbackEvent one-shot and repeating timers, TurnOnEvent/TurnOffEvent, onDestroy), accessing components with getComponent (plus null-check patterns to fix 'cannot read property of null' errors), cross-TypeScript imports with getTypeName(), NativeLogger vs print, prefab instantiation (sync and async), SceneObject hierarchy queries, and enabling/disabling objects. Use this skill whenever writing or debugging any Lens Studio TypeScript script, wiring up scene objects, or fixing 'this is undefined' or null-reference errors — platform-agnostic (works for Spectacles and phone lenses).
---

# Lens Studio Scripting — Reference Guide

Lens Studio TypeScript components are classes that extend `BaseScriptComponent` and are decorated with `@component`. This guide covers the patterns you'll use in every script you write.

---

## Component Anatomy

```typescript
import { SomeModule } from 'SpectaclesInteractionKit.lspkg/SomeModule'

@component
export class MyComponent extends BaseScriptComponent {
  // --- Inspector-exposed inputs ---
  @input
  @hint('Drag a scene object here')
  targetObject: SceneObject

  @input
  speed: number = 1.0

  @input
  @allowUndefined         // makes the field optional in the inspector
  optionalAudio: AudioComponent

  @input
  @label('Display Name') // rename the field label in the inspector
  internalProp: number = 0

  // --- Private state ---
  private elapsedTime: number = 0

  // --- Lifecycle ---
  onAwake(): void {
    // Called once at construction time. Set up events here.
    this.createEvent('OnStartEvent').bind(() => this.onStart())
    this.createEvent('UpdateEvent').bind(() => this.onUpdate())
  }

  private onStart(): void {
    // Called once the scene is fully loaded.
    // Reference other components here rather than in onAwake.
    if (!this.targetObject) {
      print('[MyComponent] ERROR: targetObject not assigned')
      return
    }
  }

  private onUpdate(): void {
    // Called every frame.
    this.elapsedTime += getDeltaTime()
  }

  onDestroy(): void {
    // Called when the scene object this component belongs to is destroyed.
    // Use to unsubscribe events, clean up sessions, etc.
  }
}
```

### Lifecycle order reference

| Event name | When it fires | Typical use |
|---|---|---|
| `onAwake` | Component constructs | Wire up event listeners |
| `OnStartEvent` | Scene finishes loading | Access other components |
| `UpdateEvent` | Every rendered frame | Per-frame logic |
| `DelayedCallbackEvent` | After N seconds | Timers, deferred actions |
| `TurnOnEvent` | Object becomes enabled (`.enabled = true`) | React to visibility on |
| `TurnOffEvent` | Object becomes disabled (`.enabled = false`) | React to visibility off |
| `onDestroy` | Scene object is destroyed | Clean up resources |

---

## Decorator Reference

| Decorator | Effect |
|---|---|
| `@component` | Registers the class as a Lens Studio component |
| `@input` | Exposes the property in the Lens Studio Inspector |
| `@hint('text')` | Adds a tooltip to the inspector field |
| `@allowUndefined` | Prevents validation errors for optional inputs |
| `@label('Display Name')` | Renames the field label shown in the inspector |
| `@serializeField` | Persists a property value across hot-reloads in the editor (dev-time only) |

### Input arrays

To expose a list of assets or objects in the inspector:

```typescript
@input
myObjects: SceneObject[]  // shown as a resizable list in the inspector

@input
audioTracks: AudioTrackAsset[]
```

---

## Accessing Other Components

### On the same scene object
```typescript
const audio = this.sceneObject.getComponent('Component.AudioComponent')
const meshVisual = this.sceneObject.getComponent('Component.RenderMeshVisual')
```

### On a child scene object
```typescript
const child = this.sceneObject.getChild(0) // by index
const comp = child.getComponent('Component.AudioComponent')
```

### Accessing a custom TypeScript component on another object

**Method A — `@input` (preferred)**
```typescript
@input
otherComponent: ScriptComponent  // assign in inspector
// then cast:
const typed = otherComponent as unknown as MyOtherComponent
```

**Method B — TypeScript-to-TypeScript import**
```typescript
import { TSComponentA } from './TSComponentA'
// Then get the component and cast:
const comp = this.sceneObject.getComponent(TSComponentA.getTypeName()) as unknown as TSComponentA
```

---

## Scene Object Queries

```typescript
// Find by name across the whole scene (recursive)
const obj = scene.getRootObject(0).findChild('TargetObject', true)

// Iterate all root objects (phone lenses often have one root)
const rootCount = scene.getRootObjectsCount()
for (let i = 0; i < rootCount; i++) {
  const root = scene.getRootObject(i)
}

// Find by name (built-in alternative)
const obj = scene.findByName('TargetObject')

// Iterate children
const count = parent.getChildrenCount()
for (let i = 0; i < count; i++) {
  const child = parent.getChild(i)
}

// Create a new empty scene object
const newObj = scene.createSceneObject('NewObject')
newObj.setParent(this.sceneObject)
```

---

## Prefab Instantiation

```typescript
@input prefab: ObjectPrefab

// Synchronous instantiation
const instance = this.prefab.instantiate(parentSceneObject) // null = root
instance.name = 'SpawnedItem'
instance.getTransform().setWorldPosition(spawnPos)

// Async instantiation (non-blocking, large prefabs)
this.prefab.instantiateAsync(parentSceneObject).then((instance) => {
  instance.getTransform().setWorldPosition(spawnPos)
})

// Destroy an instance
instance.destroy()
```

---

## DelayedCallbackEvent (Timers)

```typescript
// One-shot delay
const delayedEvent = this.createEvent('DelayedCallbackEvent')
delayedEvent.bind(() => {
  print('2 seconds elapsed')
  doSomething()
})
delayedEvent.reset(2) // seconds

// Repeating timer: call reset() again at the end of the callback
delayedEvent.bind(() => {
  tick()
  delayedEvent.reset(1) // re-fire after 1 second
})
delayedEvent.reset(1)

// Cancel a scheduled event
delayedEvent.enabled = false
```

---

## Logging

### `print` (basic)
```typescript
print('Simple message: ' + value)
print(`Template literal: ${object.name}`)
```

### `NativeLogger` (prefixed, structured)
```typescript
import NativeLogger from 'SpectaclesInteractionKit.lspkg/Utils/NativeLogger'

const log = new NativeLogger('MyComponent') // prefix shown in console

log.d('Debug message')      // debug
log.i('Info message')       // info
log.w('Warning message')    // warning
log.e('Error message')      // error
```

NativeLogger messages can be filtered in the Lens Studio console by prefix, which makes debugging multi-component scenes much easier.

---

## Enabling / Disabling Scene Objects and Components

```typescript
// Show / hide a whole object and all its children
sceneObject.enabled = false

// Disable only a component without hiding the object
meshVisual.enabled = false

// Toggle
sceneObject.enabled = !sceneObject.enabled
```

`TurnOnEvent` fires after `enabled` is set to `true`; `TurnOffEvent` fires after `enabled` is set to `false`. Both fire on the object itself, not on children.

---

## Custom Events

Lens Studio allows you to create named custom events and dispatch/receive them across scripts:

```typescript
// Dispatching a custom event
const event = this.createEvent('CustomTrigger')
event.bind(() => this.onCustomTrigger())

// Sending a custom event to another script
// (use a shared EventWrapper / callback pattern instead of global events)
type OnScoreUpdate = (score: number) => void

class ScoreManager extends BaseScriptComponent {
  private listeners: OnScoreUpdate[] = []

  addScoreListener(fn: OnScoreUpdate): void {
    this.listeners.push(fn)
  }

  updateScore(score: number): void {
    this.listeners.forEach(fn => fn(score))
  }
}
```

> **Note:** Lens Studio does not have a global event bus — prefer callback arrays or direct `@input` wiring for cross-component communication.

---

## Common Gotchas

- **Never call `getComponent` in `onAwake`** — the scene may not be fully loaded yet. Use `OnStartEvent`.
- **`@input` arrays** need a matching type annotation and are assigned from the Inspector list.
- **`null` vs `undefined`**: Lens Studio uses `null` more than `undefined`; check with `isNull(val)` or `val !== null`.
- **`getDeltaTime()`** returns frame delta in seconds — always use it for frame-rate-independent motion.
- **`this` inside callbacks**: if using a plain `function() {}` callback (not an arrow function), `this` will be wrong. Either use arrow functions or assign `const self = this` before the callback.
- **Destroying objects mid-update** can cause frame errors — defer with a `DelayedCallbackEvent` set to 0 delay if needed.
- **Component caching**: call `getComponent` once in `OnStartEvent` and store the result; calling it every frame is expensive.
- **`onDestroy` fires on the scene object being destroyed**, not when only a component is removed; if you need component-level cleanup, use `TurnOffEvent` or a manual teardown method.
- **Script initialization order**: components on the same frame initialize roughly in scene-hierarchy order. If two components in the same frame need each other in `onAwake`, use `OnStartEvent` instead.
- **`@serializeField`** only persists values in the Lens Studio editor (useful during development); it does not persist values on-device at runtime — use `persistentStorageSystem` for on-device persistence.
