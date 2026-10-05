---
name: phaser-release
description: This skill should be used when the user asks to "release my game", "ship it", "publish to itch.io", "prepare for launch", "is my game ready to release", "make a store page", "release checklist", "version my game", "what do I need before launching", "post-launch", "my game is live and I need to update it", or is preparing a Phaser game for players rather than for testing.
version: 0.7.0
---

# Releasing a Phaser 4 Game

Getting the build onto a host is the easy part, and `skills/phaser-build/` already covers
it. This skill covers the rest: deciding whether the game is ready, presenting it so
people play it, and running the loop after launch.

The most common release mistake is not a broken build. It is releasing something that
works, presenting it badly, and concluding the game was the problem.

---

## The readiness gate

Do not begin release preparation until all of these pass. Each one has ended a launch.

```bash
# 1. Compiles
npx tsc --noEmit

# 2. Runs — as a production build, which is what players get
node "${CLAUDE_PLUGIN_ROOT}/skills/phaser-playtest/scripts/playtest.mjs" \
  --project . --mode build

# 3. Every scenario still passes
for f in playtest/*.mjs; do
  node "${CLAUDE_PLUGIN_ROOT}/skills/phaser-playtest/scripts/playtest.mjs" \
    --project . --scenario "$f" --mode build || echo "FAILED: $f"
done

# 4. Holds up on mobile if you claim mobile support
node "${CLAUDE_PLUGIN_ROOT}/skills/phaser-playtest/scripts/playtest.mjs" \
  --project . --mode build --device iphone

# 5. No leak across a long session
node "${CLAUDE_PLUGIN_ROOT}/skills/phaser-playtest/scripts/playtest.mjs" \
  --project . --scenario playtest/long-session.mjs --heap
```

**`--mode build` is the one that matters.** Dev mode hides exactly the failures that only
players see: a wrong `base` path in `vite.config.ts` that 404s every asset on itch.io,
assets referenced from `src/` that never reached `dist/`, minification breaking code that
depends on `.name`, and tree-shaking dropping a scene that is only referenced
dynamically. A game that is perfect in dev and broken in build is the single most common
launch-day failure.

### Manual checks the harness cannot make

| Check | Why it matters |
|---|---|
| Play it start to finish yourself | You will find something. You always do. |
| Someone else plays it without instructions | The tutorial gap only appears with a real stranger |
| Audio balance on speakers *and* headphones | Mixes made on one are usually wrong on the other |
| Every settings toggle actually works | Broken settings read as a broken game |
| Save survives a page reload | And a browser restart, and a version bump |
| It works on a real phone | Emulation is not Safari |

The stranger test is the highest-value item on this list. Watch, and do not help — every
moment you want to explain something is a design problem you can still fix.

---

## Versioning

Set a version and put it in the game:

```typescript
// Read from package.json at build time; never hand-maintain two copies.
const config: Phaser.Types.Core.GameConfig = {
  gameVersion: __APP_VERSION__,   // define in vite.config.ts
  // ...
};
```

```typescript
// vite.config.ts
import pkg from './package.json';
export default defineConfig({
  define: { __APP_VERSION__: JSON.stringify(pkg.version) },
});
```

Display it somewhere unobtrusive — a corner of the title screen. When a bug report says
"it happens on the latest version", you need to know what they were actually running, and
a version they can read off the screen is the difference between a useful report and a
guess.

Semantic-ish versioning for games:

| Bump | When |
|---|---|
| `0.1.0` → `0.2.0` | New content or features |
| `0.2.0` → `0.2.1` | Fixes |
| `0.x` → `1.0.0` | The game is complete as designed |

**Version your save format separately**, and from the first release:

```typescript
interface SaveData { version: number; /* ... */ }
```

Retrofitting this after players have saves is a migration you cannot test against data
you do not have. See `skills/phaser-saveload/`.

---

## The store page

For most web games the page does more for the play count than any single feature. It is
not marketing fluff; it is where people decide.

### The essentials, in order of impact

1. **A GIF or short video, above the fold.** People watch before they read. It should show
   *play*, not a title screen — start on motion, keep it under 10 seconds, loop cleanly.
2. **One sentence that says what the game is.** Your hook, from brainstorming. Not
   "an exciting adventure" — what the player *does*.
3. **Screenshots that show different things.** Four images of the same room say the game
   has one room.
4. **Controls, stated plainly.** Web-game players will not hunt. Put them on the page
   *and* on the title screen.
5. **Honest scope.** "A 15-minute arcade game" sets the right expectation and gets better
   reception than an unlabelled short game does.

### Making the GIF

```bash
node "${CLAUDE_PLUGIN_ROOT}/skills/phaser-playtest/scripts/playtest.mjs" \
  --project . --scenario playtest/showcase.mjs --video --mode build
```

A scenario that plays the most visually interesting 10 seconds gives you a clean,
repeatable capture with no cursor and no fumbled input — and it re-records itself in one
command every time the art changes.

### itch.io specifics

- Zip the **contents** of `dist/`, not the folder. `index.html` must be at the zip root.
- Set the viewport dimensions to match your game, and enable fullscreen.
- `base: './'` in `vite.config.ts` — an absolute base 404s every asset.
- Tag accurately. Tags are how itch surfaces the game, and wrong tags bring the wrong
  players, who leave the reviews.

Deployment mechanics for itch.io, GitHub Pages, Netlify/Vercel and Capacitor are in
`skills/phaser-build/SKILL.md`.

---

## Launch day

**Set up the feedback path before you announce.** A comment thread nobody is reading, or a
Discord that does not exist yet, loses you the first day of reports — which are the most
valuable ones you will get, because they come from the least invested players.

Add an in-game way to report:

```typescript
if (this.input.keyboard) {
  this.input.keyboard.on('keydown-F8', () => {
    const state = { version: __APP_VERSION__, scene: this.scene.key, /* ... */ };
    navigator.clipboard?.writeText(JSON.stringify(state));
  });
}
```

A key that copies the current game state turns a paragraph of prose into something you can
paste straight into a playtest `eval` step. It costs ten lines and it changes what your
bug reports are worth.

**Watch, in this order:**

1. Does it load at all, for other people, on other networks?
2. Do people get past the first minute? A drop-off there is onboarding, not difficulty.
3. What do they say in the first hour? Early reports skew toward real blockers.

**Have a rollback ready.** Keep the previous build. If launch day goes wrong, restoring in
two minutes beats debugging under pressure in front of an audience.

---

## After launch: the loop

Release is the start of the interesting part. Feedback arrives, and the loop that turns it
into a better game is:

```bash
/phaser-feedback   # triage, reproduce, fix, verify, reply
```

Each reproduced bug leaves behind a `playtest/repro-*.mjs` scenario, which becomes part of
the gate for the next release. Over a few releases that suite encodes what real players
actually did to your game — which no amount of unit testing produces. See
`skills/phaser-feedback/`.

### Patch releases

Ship fixes fast and visibly. A game that gets a fix within a day of a report reads as
cared-for, and that reputation determines whether anyone bothers reporting the next one.

For each patch:

1. Fix, with a repro scenario.
2. Run the full readiness gate again — patches break things, especially under pressure.
3. Bump the patch version.
4. Write a player-facing changelog: what changed, in their words, not
   `fixed null deref in ShopScene`. See
   `skills/phaser-feedback/references/response-templates.md`.
5. Tell the people who reported it. Individually, if the numbers allow.

### Knowing when to stop

A game is finished when the remaining items are improvements rather than problems. There
is always more polish available. Two useful signals:

- Nobody has reported a *blocker* in a while, and the remaining list is preferences.
- You are making changes you cannot justify to a player.

Stop, write the postmortem, and start the next one. An unfinished game teaches far less
than a finished one, and a game polished past the point of complaints is a game not being
made.

---

## Additional Resources

### Reference Files
- **`references/release-checklist.md`** — The full gate as a checklist, per platform, plus
  the pre-launch, launch-day and post-launch sequences.
- **`references/store-presence.md`** — Store page craft: capture, screenshots,
  descriptions, tags, and the platform-specific requirements for itch.io, Newgrounds,
  Poki, and mobile stores.

### Related
- `skills/phaser-build/` — deployment mechanics and per-host configuration
- `skills/phaser-feedback/` — the post-launch loop
- `skills/phaser-playtest/` — the gate this skill depends on
- `skills/phaser-mobile/` — mobile and store packaging specifics
- `skills/phaser-saveload/` — save versioning, which must exist before the first release
