---
name: phaser-particles
description: This skill should be used when the user asks to "add particles", "particle effect", "explosion effect", "smoke", "fire effect", "sparks", "dust trail", "rain or snow", "confetti", "muzzle flash", "blood splatter", "magic effect", "emitter", "particles not showing", "particles killing performance", "trail behind the player", or anything involving Phaser 4 ParticleEmitter configuration, emit zones, death zones, or gravity wells.
version: 0.7.0
---

# Phaser 4 Particles

Particles are how a game reads as responsive. A hit that spawns three sparks feels twice
as solid as the same hit without them, for a fraction of the work of any other juice
technique.

They are also the most common cause of a Phaser game running at 20fps.

---

## The emitter

```typescript
const emitter = this.add.particles(x, y, 'texture', config);
```

One call creates and adds an emitter. It is a normal game object: it has depth, scroll
factor, alpha, and can go in a container.

A worked config, with every field that matters in practice:

```typescript
const sparks = this.add.particles(0, 0, 'flare', {
  // Motion
  speed: { min: 50, max: 150 },      // px/sec; a range gives natural spread
  angle: { min: 0, max: 360 },       // degrees; direction of travel
  gravityY: 300,                     // px/sec² — falling embers, debris
  accelerationX: 0,

  // Appearance over life — {start, end} interpolates across the particle's lifespan
  scale: { start: 1, end: 0 },
  alpha: { start: 1, end: 0 },
  rotate: { start: 0, end: 360 },
  tint: [0xffaa00, 0xff2200],        // an array picks randomly per particle
  blendMode: 'ADD',                  // ADD for light: fire, magic, sparks

  // Timing
  lifespan: 600,                     // ms each particle lives
  frequency: 40,                     // ms between emissions; -1 = explode mode only
  quantity: 2,                       // particles per emission

  // Budget — always set this
  maxParticles: 100,

  emitting: false,                   // create dormant; start it deliberately
});
```

**`{ start, end }` is the workhorse.** Most of what makes a particle effect look
deliberate rather than sprayed is `scale` and `alpha` shrinking and fading over the
lifespan. A particle that pops out of existence at full size looks like a bug.

---

## Emit once, or emit continuously

Two modes, and mixing them up is why an effect either never appears or never stops.

**Burst** — an explosion, a hit spark, a pickup pop:

```typescript
const burst = this.add.particles(0, 0, 'spark', {
  speed: { min: 100, max: 300 },
  lifespan: 400,
  scale: { start: 0.8, end: 0 },
  emitting: false,                    // dormant until told otherwise
});

burst.explode(20, x, y);              // 20 particles, right here, right now
```

**Continuous** — a torch, a smoke plume, rain:

```typescript
const smoke = this.add.particles(x, y, 'smoke', {
  frequency: 100,
  quantity: 1,
  lifespan: 2000,
  emitting: true,
});

smoke.stop();      // stop emitting; existing particles live out their lifespan
smoke.start();
smoke.pause();     // freeze everything, including live particles
smoke.resume();
```

`stop()` and `pause()` are different and the difference is visible: `stop()` lets the
plume dissipate naturally, `pause()` freezes it mid-air.

**Cleaning up:** an emitter created per explosion and never destroyed is a leak. Either
create one emitter and re-`explode()` it, or destroy after the last particle dies:

```typescript
// Reuse — the right default
this.hitSparks.explode(8, enemy.x, enemy.y);

// Or fire-and-forget, cleaned up properly
const e = this.add.particles(x, y, 'spark', { lifespan: 400, emitting: false });
e.explode(20);
this.time.delayedCall(500, () => e.destroy());
```

---

## Following a moving object

```typescript
emitter.startFollow(player, 0, -10);   // offsetX, offsetY
emitter.stopFollow();
```

Use this rather than setting the emitter position in `update()`. `startFollow` tracks
between frames, so a fast-moving object leaves a continuous trail instead of a dotted
line of clumps at each frame's position.

---

## Zones

**Emit zones** — where particles are born:

```typescript
// Along the edge of a shape: a ring, a magic circle
emitter.addEmitZone({
  type: 'edge',
  source: new Phaser.Geom.Circle(0, 0, 50),
  quantity: 32,
});

// Anywhere inside a shape: rain across the top of the screen
emitter.addEmitZone({
  type: 'random',
  source: new Phaser.Geom.Rectangle(0, 0, 800, 10),
});
```

**Death zones** — where particles are destroyed:

```typescript
emitter.addDeathZone({
  type: 'onEnter',                                  // or 'onLeave'
  source: new Phaser.Geom.Rectangle(0, 400, 800, 200),
});
```

`onLeave` with a screen-sized rectangle is how you stop off-screen particles costing
anything.

**Gravity wells** — attract or repel:

```typescript
emitter.createGravityWell({ x: 400, y: 300, power: 3, epsilon: 100, gravity: 100 });
```

Vortexes, black holes, a magnet pickup pulling coins in.

---

## Performance — read this before shipping

Particles are the most common cause of frame-rate collapse in a Phaser game, and the
collapse arrives long after the code was written, because it only shows up under load.

**Always set `maxParticles`.** An emitter without a cap and a short `frequency` will
happily allocate until the frame budget is gone. This is the single highest-value line in
any emitter config.

```typescript
maxParticles: 100,       // hard ceiling
```

Sizing it: `lifespan / frequency * quantity` is the steady-state count. At
`lifespan: 2000, frequency: 40, quantity: 2` that is 100 live particles from one emitter —
and if you have ten such emitters, a thousand.

**Other levers, roughly in order of payoff:**

| Lever | Why |
|---|---|
| Shorter `lifespan` | Fewer live particles for the same visual density |
| Death zones on `onLeave` | Off-screen particles cost exactly as much as visible ones |
| Fewer, larger particles | 20 big sparks read better than 200 tiny ones and cost 10× less |
| One emitter, reused | Emitter churn costs more than the particles do |
| Smaller textures | Particle textures rarely need to exceed 32×32 |
| Avoid `ADD` on mobile | Additive blending is fill-rate hungry, and mobile is fill-rate bound |
| `stopAfter` | Emits N particles then stops on its own — no cleanup logic to forget |

**Mobile budget:** a few hundred simultaneous particles across the whole game, not per
effect. Halve your desktop counts and check on a real device — see
`skills/phaser-mobile/references/device-profiles.md`.

For thousands of similar sprites, particles are the wrong tool — see `SpriteGPULayer` in
`skills/phaser-fx/references/renderer-and-shaders.md`.

---

## Why particles aren't showing

In rough order of likelihood:

| Symptom | Cause |
|---|---|
| Nothing at all | `emitting: false` and you never called `start()` or `explode()` |
| Nothing at all | The texture key does not exist — check the loader, and the playtest asset check |
| Nothing at all | `frequency: -1` (explode-only) with no `explode()` call |
| Invisible | Emitter depth is below the background — `emitter.setDepth(n)` |
| Invisible | `alpha: { start: 0 }` — the start value, not the end, is zero |
| One frame then gone | `lifespan` far too short |
| Wrong place | Emitter x/y are world coordinates; inside a container they are local |
| Not following | Position set in `update()` instead of `startFollow()` |
| Frame rate collapse | No `maxParticles` |

---

## Verifying particles at runtime

Particle bugs type-check perfectly — a wrong texture key is a string, and an emitter that
never starts is valid code. Prove it ran:

```javascript
// playtest/particles-check.mjs
export default [
  { name: 'hit sparks fire on damage', action: 'eval',
    code: `scene('GameScene').hitEnemy(scene('GameScene').enemies[0])` },
  { name: 'particles actually spawned', action: 'expect',
    expect: { expression: `scene('GameScene').hitSparks.getAliveParticleCount()`, atLeast: 1 } },

  { name: 'and they are capped', action: 'sample',
    expression: `scene('GameScene').hitSparks.getAliveParticleCount()`,
    duration: 3000, interval: 100,
    expect: { stat: 'max', atMost: 100 } },

  { name: 'frame rate survives the effect', action: 'sample',
    expression: `game.loop.actualFps`, duration: 3000, interval: 100,
    expect: { stat: 'min', atLeast: 50 } },
];
```

The `max` assertion on the alive count is the one that catches an uncapped emitter before
a player does. Run it while the game is under its heaviest particle load, not at rest.

---

## Additional Resources

### Reference Files
- **`references/particle-recipes.md`** — Complete configs for the effects games actually
  need: explosion, fire, smoke, rain, snow, sparks, blood, magic, dust, muzzle flash,
  confetti, trails — each with the reasoning for its numbers.

### Related
- `skills/phaser-fx/` — filters and blend modes; `ADD` particles plus a bloom action is
  the standard "magic" look
- `skills/phaser-analyze/references/performance-playbook.md` — when particles cost frames
- `skills/phaser-mobile/references/device-profiles.md` — mobile particle budgets
