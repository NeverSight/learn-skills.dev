---
name: threejs-game-generator-skill
description: Build, extend, or polish original 3D browser games and interactive prototypes with Three.js. Use when a user wants a playable WebGL game, a game-like Three.js experience, a 2D concept translated into 3D, or an existing Three.js project given a complete loop, controls, camera, collisions, UI states, audio, persistence, performance work, or production-build verification. Do not trigger for ordinary 3D product viewers, data visualizations, or decorative background scenes unless the request includes game mechanics or player interaction.
license: MIT
metadata:
  category: game-development
  engine: threejs
---

# Three.js Game Generator

Turn a game brief or an unfinished Three.js scene into a small, complete browser game. Lead with one satisfying playable loop, make the direction original, work in the user's existing stack, and verify the result in a real browser.

## Choose the operating mode

- **New game:** create the smallest maintainable project that fits the request. Default to Three.js with Vite when no stack exists.
- **Existing game:** preserve the package manager, architecture, routes, assets, controls, and working systems. Change only what the requested outcome needs.
- **Scene-to-game:** keep the useful scene, then add an explicit goal, player verbs, feedback, failure or completion, restart, and progression.
- **Polish pass:** profile and play the current build before changing it. Fix broken feedback, camera, controls, pacing, performance, and state transitions in that order.

Do not publish, buy assets, call paid services, or mutate external systems unless the user explicitly asks.

## Establish the game contract

Infer what is missing when the brief is loose, but do not silently expand a prototype into a large production.

Write a compact contract before implementation:

1. **Fantasy:** what the player should feel they are doing.
2. **Core loop:** the repeatable action, response, reward, and escalation.
3. **Win, loss, or completion:** how a run ends and how the player restarts.
4. **Camera and controls:** perspective, movement model, input devices, and touch behavior.
5. **Visual thesis:** one recognizable art direction tied to the mechanic.
6. **Scope:** the smallest content set that proves the loop, plus explicitly deferred features.

When the user names an existing title, borrow only high-level interaction ideas. Create original characters, environments, layouts, UI, names, audio, and art.

## Read references selectively

- Read [engine-patterns.md](references/engine-patterns.md) when setting up or changing the game loop, renderer, controls, camera, collisions, loading, persistence, object lifetime, or performance.
- Read [visuals.md](references/visuals.md) when choosing lighting, materials, procedural geometry, asset style, atmosphere, UI treatment, shadows, or quality tiers.
- Read [audio-recipes.md](references/audio-recipes.md) when the game needs music, feedback sounds, spatial audio, user-gesture activation, or mixing.
- Read [genres.md](references/genres.md) when the brief needs a viable mechanic set, camera/control mapping, content budget, or genre-specific risk check.

Do not load every reference by default.

## Workflow

### 1. Inspect the workspace

Identify:

- package manager, scripts, entry points, Three.js version, addons, and build tool;
- current scene graph, renderer, cameras, input, state management, physics, assets, UI, and audio;
- the production build command and any existing tests;
- local modifications that must be preserved.

Run the current project when possible. Record visible failures and browser console errors before editing. Do not replace a functioning project merely to use a preferred scaffold.

### 2. Prove a vertical slice

Build the smallest complete loop before adding breadth:

- one controllable player or primary interaction;
- one objective and one meaningful obstacle;
- visible feedback for success, damage, collection, or progress;
- start, active, paused, completed/failed, and restart states;
- a 30–180 second play session that demonstrates the intended feel.

Use graybox geometry until scale, movement, camera, and pacing work. A beautiful scene without a finishable loop is not a game.

### 3. Build stable foundations

Use the project patterns in [engine-patterns.md](references/engine-patterns.md). Keep these invariants:

- one renderer and one authoritative animation loop;
- frame-rate-independent movement with a capped delta, or a fixed simulation step when determinism matters;
- explicit game states rather than scattered booleans;
- input sampled into actions so keyboard, pointer, gamepad, and touch can share game logic;
- world units and coordinate conventions chosen once and used consistently;
- capped device pixel ratio and a resize path that updates renderer and camera;
- reusable geometry/materials and intentional disposal of GPU resources;
- HTML UI for readable menus, settings, and HUD unless 3D placement is essential;
- asset loading with progress and failure states;
- no secrets in client code.

Add a physics engine only when the mechanic genuinely needs rigid-body simulation. Use simple spheres, boxes, capsules, raycasts, or spatial partitioning for arcade movement when they are sufficient.

### 4. Implement the feel

Tune input, movement, camera, and feedback together:

- controls should respond immediately and remain predictable at low and high frame rates;
- camera follow should use damping and bounded look-ahead rather than raw player transforms;
- collisions should produce readable consequences, not silent blocking;
- actions need anticipation, impact, and recovery appropriate to the genre;
- screen shake, hit pause, particles, trails, and post-processing must remain restrained and disable cleanly for reduced motion or lower quality;
- touch targets and virtual controls must fit the actual viewport and not cover critical play space.

Add secondary systems only after the core loop is enjoyable.

### 5. Art-direct one world

Read [visuals.md](references/visuals.md). Define a small palette, lighting model, shape language, material family, and atmosphere. Prefer a coherent low-complexity world over a mixture of unrelated high-detail assets.

Keep color textures in the correct color space, cap expensive shadows, avoid per-frame allocations, and reduce pixel ratio or effects before reducing gameplay clarity. Credit and document every external asset and its license.

### 6. Add audio and persistence proportionally

Read [audio-recipes.md](references/audio-recipes.md) if audio is in scope. Start audio only after a user gesture, expose mute and volume controls, and keep critical feedback understandable without sound.

Persist only useful state such as settings, best score, unlocked level, or checkpoint. Version stored data and recover safely from missing or invalid values.

### 7. Verify the actual game

Run the production build first and fix every error. Then test the built or development version in a browser.

Check:

- start → play → pause/resume → win/lose → restart works without reloading;
- every documented control works, including touch when promised;
- resize, orientation change, backgrounding, and focus loss do not corrupt state;
- browser console has no uncaught errors or missing assets;
- UI is readable and keyboard accessible;
- audio activation and mute behavior are correct;
- save data survives a reload and invalid save data does not crash;
- the busiest scene remains responsive on the target device class;
- reduced-motion and lower-quality modes remove expensive effects without hiding essential feedback.

Play at least one complete run. Automated build success alone is insufficient.

## Quality bar

- A stranger can understand the objective and controls without reading source code.
- The first meaningful interaction arrives quickly.
- The game has a complete loop and restart flow, not only a scene or technical demo.
- Camera, movement, collision, and feedback feel like one system.
- The art direction is recognizable and original.
- Performance degrades gracefully before it becomes unplayable.
- The project remains understandable enough to extend.

## Avoid

- recreating copyrighted characters, levels, UI, music, or branded assets;
- installing a large engine or physics stack before proving it is necessary;
- one file containing rendering, input, state, UI, audio, and every entity;
- tying movement directly to frame count;
- allocating vectors, materials, geometries, or loaders inside the hot loop;
- unbounded particles, lights, shadow casters, or device pixel ratio;
- pointer lock with no escape path or touch controls with no desktop fallback;
- hiding load failures, unsupported WebGL, or missing credentials behind a blank canvas;
- shipping a polished title screen around an unfinished mechanic.

## Handoff

Lead with how to run the game. Then report:

- the implemented core loop and control map;
- build and playtest commands with results;
- asset sources and licenses;
- browser/device limitations;
- deferred features that were intentionally kept out of scope.
