---
name: monogame-extended-particles
description: >
  MonoGame.Extended Particle System guide — visual effects (fire, smoke, explosions,
  sparkles, magic) using zero-allocation particle emitters with pooled particle buffers.
  Use this skill whenever the user mentions particle system, particle emitter, explosion
  visual effect, smoke, fire effect, ParticleEffect extended, chispas, partículas, impact
  burst, trail effect, or wants to add a dynamic visual effect — even if they just say
  "I want an explosion when enemies die" or "how do I make fire in MonoGame".
---

# MonoGame.Extended Particle System Implementation Guide

This skill covers building visual effects with `ParticleEffect` and `ParticleEmitter`
from MonoGame.Extended. All particle state lives in a fixed-capacity buffer allocated
once — no GC pressure during gameplay. For API signatures and complete code examples
read `references/extended-particles.md`.

## Required Namespaces

```csharp
using MonoGame.Extended;                                          // HslColor
using MonoGame.Extended.Graphics;                                  // Texture2DRegion
using MonoGame.Extended.Particles;
using MonoGame.Extended.Particles.Data;                           // ParticleReleaseParameters, ParticleFloatParameter, ParticleColorParameter
using MonoGame.Extended.Particles.Profiles;
using MonoGame.Extended.Particles.Modifiers;
using MonoGame.Extended.Particles.Modifiers.Interpolators;
```

All seven must be present — forgetting any one will cause compilation errors.

## Core Structure

```
ParticleEffect
  ├── Position          (world-space position of the whole effect)
  ├── AutoTrigger       (true = emit automatically, false = emit on Trigger() call)
  ├── AutoTriggerFrequency (seconds between auto-trigger pulses; 0 = every frame)
  └── Emitters[]
        └── ParticleEmitter(capacity)
              ├── LifeSpan      (seconds each particle lives)
              ├── TextureRegion (Texture2DRegion wrapping your particle texture)
              ├── Profile       (where/how particles are spawned)
              ├── Parameters    (initial speed, color, scale, quantity)
              └── Modifiers[]   (forces and visual changes over lifetime)
```

## Frame Loop

```csharp
// Update
_particleEffect.Update(gameTime);

// Draw — uses SpriteBatch extension from MonoGame.Extended
_spriteBatch.Begin(BlendState.Additive);  // Additive for fire/glow; AlphaBlend for smoke
_spriteBatch.Draw(_particleEffect);
_spriteBatch.End();
```

`_particleEffect.Update` advances all particle lifetimes and applies modifiers.
`_spriteBatch.Draw(_particleEffect)` iterates all alive particles and draws each one.

## Continuous vs Burst Emission

| Mode | Use for | Key settings |
|------|---------|-------------|
| Continuous | Fire, smoke, trails | `AutoTrigger = true`, `AutoTriggerFrequency = 0.1f` |
| Every frame | Sparkle, aura | `AutoTrigger = true`, `AutoTriggerFrequency = 0.0f` |
| Manual burst | Explosion, impact | `AutoTrigger = false`, call `_effect.Trigger()` |

For a burst at a specific world position (e.g., on collision):

```csharp
_particleEffect.Position = collisionPoint;
_particleEffect.Trigger();
```

## Emission Profiles

Profiles control the shape from which particles spawn:

| Profile | Syntax | Best for |
|---------|--------|----------|
| Spray (cone) | `Profile.Spray(direction, spread)` | Fire, exhaust |
| Circle (outward) | `Profile.Circle(radius, CircleRadiation.Out)` | Explosion |
| Circle (inward) | `Profile.Circle(radius, CircleRadiation.In)` | Vacuum / attract |
| Point | `Profile.Point()` | Trails, pinpoint effects |
| Line | `Profile.Line(axis, length)` | Slash, rain |
| Box | `Profile.Box(width, height)` | Area emission |
| Ring | `Profile.Ring(radius)` | Circular sparkle |

```csharp
Profile = Profile.Spray(-Vector2.UnitY, spread: 2.0f)   // upward cone (fire)
Profile = Profile.Circle(20, CircleRadiation.Out)        // outward burst (explosion)
Profile = Profile.Point()                                 // exact position (trail)
```

## Key Modifiers

| Modifier | Effect |
|----------|--------|
| `LinearGravityModifier` | Pulls particles in a direction (up for fire, down for sparks) |
| `DragModifier` | Simulates air resistance; slows particles over time |
| `AgeModifier` | Drives interpolators over the particle's lifetime (opacity, scale, color) |
| `VelocityModifier` | Changes speed over time |
| `RotationModifier` | Spins each particle |

Combine `AgeModifier` with interpolators for smooth property transitions:

```csharp
emitter.Modifiers.Add(new AgeModifier
{
    Interpolators =
    {
        new OpacityInterpolator { StartValue = 1.0f, EndValue = 0.0f },   // fade out
        new ScaleInterpolator   { StartValue = new Vector2(8f, 8f),
                                  EndValue   = new Vector2(1f, 1f) }       // shrink
    }
});
```

## Color System (HSL)

Particle colors use HSL (Hue 0–360, Saturation 0–1, Lightness 0–1):

```csharp
// Single color
Color = new ParticleColorParameter(new Vector3(0f, 1f, 0.6f))   // red fire

// Random range between two colors
Color = new ParticleColorParameter(
    new Vector3(252f, 1f, 0.8f),   // light purple
    new Vector3(180f, 1f, 0.5f))   // cyan
```

## Pooling and GC Rules

- **Set capacity once** in `new ParticleEmitter(capacity)` and never change it —
  the buffer is a fixed array; no allocations happen during gameplay.
- **Capacity budget**: a capacity of 2000 means at most 2000 alive particles per emitter.
  Start with 500–1000 and raise only if the effect visually requires more.
- **Never** call `new ParticleEmitter(...)` in `Update` or `Draw` — only in
  `LoadContent` or a factory method called once.
- If you have multiple effects (fire AND smoke), each needs its own `ParticleEffect`
  with its own emitter(s). They share no state.

## Integration with GameBehaviour (monogame-ecs)

Trigger a particle burst from a `GameBehaviour` when a game event occurs (e.g., hit):

```csharp
// In a GameBehaviour (from monogame-ecs skill)
public class HitEffect : GameBehaviour
{
    private ParticleEffect _sparkEffect;  // injected or loaded in Initialize

    public void TriggerAt(Vector2 worldPosition)
    {
        _sparkEffect.Position = worldPosition;
        _sparkEffect.Trigger();
    }

    public void Update(GameTime gameTime)
    {
        _sparkEffect.Update(gameTime);
    }

    public void Draw(SpriteBatch spriteBatch)
    {
        spriteBatch.Draw(_sparkEffect);
    }
}
```

Do not use MonoGame.Extended's own entity or component system — use the project's
`GameBehaviour`/`GameEntity`/`GameWorld` system from the `monogame-ecs` skill.

## BlendState for Particles

| Effect type | BlendState |
|-------------|-----------|
| Fire, glow, sparks, magic | `BlendState.Additive` — colors stack and brighten |
| Smoke, dust, fog | `BlendState.AlphaBlend` — respects transparency |
| Mixed effects | Use separate `SpriteBatch.Begin/End` pairs per type |

## Anti-Patterns

- **Never** add modifiers inside `Update` — modifiers are configured once in the builder.
- **Never** set `AutoTriggerFrequency` to a very small positive value as a substitute
  for `0.0f` — use exactly `0.0f` for every-frame emission.
- **Avoid** mixing additive and non-additive particles in a single `Begin/End` pair —
  additive particles drawn over opaque background look wrong.
- **Do not** forget all five `using` directives — missing `Profiles` or `Interpolators`
  causes hard-to-diagnose "type not found" errors.

## Reference

For complete field declarations, fire/explosion/sparkle examples, and burst-on-collision
code, read `references/extended-particles.md`.
