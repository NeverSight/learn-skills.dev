---
name: game-design
description: "Use when designing or repairing what makes a game fun — verbs and mechanics, moment-to-moment/session/meta loops, progression, economy faucets and sinks, difficulty curves, dominant strategies, juice, prototyping and scope. NOT engine code (that is `godot`), NOT story (that is `game-storytelling`), NOT level layout (that is `level-design`)."
tags: [game-design, mechanics, core-loop, balancing, progression, playtesting, scope, fun]
recommends: [level-design, game-storytelling, godot, unity, unreal]
profiles: [full]
origin: risco
---

# Design games that are fun on purpose

Engine-agnostic game design: mechanics, loops, progression, economy, balance, feel, and the discipline of prototyping and scope. No engine APIs live here — when the design is settled, the implementation belongs to [`godot`](../godot/SKILL.md), [`unity`](../unity/SKILL.md), or [`unreal`](../unreal/SKILL.md).

Two premises govern everything below. **Fun is discovered, not designed** — you cannot reason your way to a fun game on paper, you find it by building the smallest playable version and playing it, so every hour spent planning a mechanic you have not prototyped is an hour spent guessing. And **a game is the set of verbs it gives the player plus the loops those verbs live in** — art, story, and levels dress that skeleton; if the skeleton is not fun in greybox, nothing dresses it into fun.

Route elsewhere when the ask is not design:

| The ask | Route to | Why not here |
| --- | --- | --- |
| Write the movement/AI/shader/save code | [`godot`](../godot/SKILL.md) / [`unity`](../unity/SKILL.md) / [`unreal`](../unreal/SKILL.md) | This skill decides *what* to build; the engine skill builds it. |
| Author the story, dialogue, characters, lore | [`game-storytelling`](../game-storytelling/SKILL.md) | Narrative design is its own craft; this skill owns systems and verbs. |
| Lay out a level, encounter, or world map | [`level-design`](../level-design/SKILL.md) | Spatial/encounter design applies the mechanics this skill defines. |
| Netcode, prediction, lag compensation | [`gamedev-multiplayer`](../gamedev-multiplayer/SKILL.md) | A technical domain, not core design intent. |
| Ship / store page / build pipeline | [`gamedev-shipping`](../gamedev-shipping/SKILL.md) | Release logistics, not design. |

## Loops: moment-to-moment → session → meta

A game is loops nested inside loops. Each layer must reward on its own **and** feed motivation to the layer above it.

```text
moment-to-moment  (seconds)   the primary verb: aim+fire, jump, place, click, parry
        │  feeds
session loop      (minutes)   a run / match / mission: setup → tension → resolution
        │  feeds
meta loop         (sessions)  mastery, unlocks, collection, rank — why you return tomorrow
```

- **Moment-to-moment first.** The thing the player does constantly must feel good with *no* goal attached — jumping in Mario is fun in an empty room. If this layer is flat, no progression system rescues it. (Bungie's "30 seconds of fun" rule: perfect the small loop, then repeat it.)
- **Session loop** gives a run shape — a beginning, a rising middle, a payoff. It should end on a hook (almost-had-it, one-more-run).
- **Meta loop** is the reason-to-return: it spends the currency and mastery earned in sessions on lasting change (new verbs, new options, status).
- **Reward funding.** A reward at one layer should fund desire at the next. Misfunded loops fail predictably: fun moment-to-moment + empty meta = "great but I bounced"; rich meta + flat moment-to-moment = "I grind and I don't know why."

Depth vs breadth of loops, feedback-loop math, and worked loop teardowns: **[references/mechanics-and-loops.md](references/mechanics-and-loops.md)**.

## MDA: the working lens

Mechanics → Dynamics → Aesthetics. The designer authors **Mechanics** (rules, entities, numbers). At runtime those produce **Dynamics** (emergent behavior as players interact). Players only ever feel the **Aesthetics** (the emotional response). You design left-to-right; the player experiences right-to-left — so you must reason backward from the feeling you want to the rule that causes it.

- **"Fun" is not a design target — name the aesthetic.** MDA's vocabulary: sensation, fantasy, narrative, challenge, fellowship, discovery, expression, submission (relaxation). "Make it more fun" is unactionable; "raise the *challenge* and *discovery*, drop the *submission*" is a to-do list.
- **Design the verbs, not the features.** The verb set *is* the game. A tight set of verbs with deep interaction (chess, Tetris) beats a wide set of shallow ones. Before adding a feature, ask: does it add a verb, deepen an existing verb, or just add a number?
- **Second-order design.** Ask what the rule makes players *do*, not what it literally says. Every incentive is also a de-incentive for everything else — rewarding kills steals attention from exploring.

The eight aesthetics with examples, emergence vs scripted content, and interaction-depth heuristics: **[references/mechanics-and-loops.md](references/mechanics-and-loops.md)**.

## Progression & economy

Progression controls the rate at which the game reveals its depth; economy is the currency plumbing underneath it.

- **Pacing.** Interleave tension and release; teach → test → twist. Run difficulty and novelty as two curves so a lull in one is covered by the other.
- **Unlocks earn their keep.** Each unlock should add a verb or a *meaningful choice*, not just +10%. Gate content to pace the complexity the player must hold at once.
- **Currencies need distinct jobs.** Soft (earned, spent freely) vs hard/premium (scarce). Never add a currency without a distinct **sink** it exists to feed — currencies without sinks are clutter.
- **Sinks and faucets.** Faucets create currency; sinks destroy it. Balance the two or the economy drifts.

Model the drift with the core identity — no engine needed, a spreadsheet does it:

```text
net_income_rate = faucet_rate − sink_rate
time_to_afford  = cost / net_income_rate          # tune this against desired pacing
cost(n)         = base × growth^n                 # escalating sink; growth ≈ 1.07–1.15
```

- **Avoiding runaway.** If `net_income_rate` rises over time, costs must rise at least as fast or currency becomes meaningless (hyperinflation, trivialized late game). Fixes: escalating/exponential sinks, consumable sinks, caps, prestige resets.
- **Kill snowballs.** Positive feedback loops (rich-get-richer) let a leader accelerate out of reach and end matches early. Counter with negative feedback / catch-up (rubber-banding, comeback mechanics, escalating cost of dominance) — tuned so it aids without feeling like punishment for winning.

Currency taxonomies, inflation math, prestige/reset design, and a balancing-spreadsheet layout: **[references/progression-and-economy.md](references/progression-and-economy.md)**.

## Difficulty & balancing

- **The curve is a sawtooth, not a ramp.** Rising baseline with peaks (bosses, gauntlets) and valleys (recovery, reward). Aim for the *flow channel*: challenge tracking skill, between boredom (too easy) and anxiety (too hard).
- **Few high-leverage knobs.** Most balance lives in a handful of variables (damage, health, spawn rate, cost, cooldown). Identify them, tune **one at a time**, and never chase a symptom by touching five knobs at once.
- **Data-driven balance.** Externalize tunables into data (tables/config), not hard-coded constants, so designers iterate without a rebuild and you can diff and A/B numbers. (The engine skill wires the loader; this skill decides *which* numbers are tunable.)
- **Dominant strategies kill choice.** When one option strictly beats the rest, all other choices die. Hunt them in playtest data and telemetry; fix by nerfing the outlier or buffing counters toward **intransitive** balance (rock-paper-scissors: every option beaten by another).
- **Perceived ≠ actual difficulty**, and difficulty options/accessibility widen the audience — decouple challenge from exclusion.

Flow-channel tuning, dominant-strategy detection, symmetry vs asymmetry, and difficulty-option patterns: **[references/progression-and-economy.md](references/progression-and-economy.md)**.

## Feel / "juice" (as design intent)

Game feel is the tactile sensation of control — the moment-to-moment made physical. It is a **design** concern here; the engine skills implement the effects.

- **Every input needs an immediate, legible reaction** — visual, audio, and/or haptic. Perceived latency is the enemy; responsiveness beats fidelity.
- **Juice vocabulary** (specify the intent, let the engine do it): hit-stop / hit-pause (freeze a few frames on impact to sell weight), screenshake (scaled to significance, never gratuitous), anticipation & follow-through and squash-and-stretch (animation principles that read intent), particles, easing/tweening curves, and layered sound.
- **Feel is often hidden generosity.** Coyote time, input buffering, and forgiveness windows make a game feel *fair* and responsive without the player ever knowing why.
- **Design-level, not code-level here.** Decide *what* should feel weighty and *why*; specify the effect and its trigger. The keyframes, curves, and shaders belong to `godot` / `unity` / `unreal`.

## Prototyping & playtesting

- **Prototype the riskiest assumption first.** Whatever most determines whether the game works — prove or kill it before building anything else.
- **Paper → greybox → vertical slice.** Test rules and economies on paper/cards; test mechanics in an untextured blockout; only then build a polished slice. Find the fun before you buy the art.
- **Watch, don't coach.** In a playtest, shut up and observe. Note confusion, boredom, and quit points. The first-time experience is gold and you get it exactly once per tester.
- **Behavior over opinion.** Players are unreliable at saying *what* is wrong but reliable at signaling *that* something is. Weight what they do over what they say. Measure both: qualitative (struggle/quit points, think-aloud) and quantitative (completion rate, time-per-section, death heatmaps, D1/D7 retention).
- **Kill your darlings.** Cut any mechanic that does not serve the core loop, however clever. A pile of clever unrelated mechanics is not a game.
- **Scope is the #1 reason indie games die** — not talent, not tools. Cut *features*, not *quality*. A finished small game beats an unfinished ambitious one. Define the "one thing" the game is about and protect it ruthlessly; build a vertical slice, not a broad shallow map of half-features.

Playtest protocols, metrics/retention definitions, the prototyping ladder, and concrete scope-cutting tactics: **[references/playtesting-and-scope.md](references/playtesting-and-scope.md)**.

## Documenting design

- **One page that lives beats a 100-page bible that dies.** Nobody reads the bible; it is stale the day after it is written. Write a living one-pager and let it grow only where a real decision needs recording.
- **The one-pager holds:** the hook / fantasy, the core loop, the verb set, the target aesthetic (named MDA emotion), the MVP scope, and — explicitly — what is *out*.
- **Design pillars** (2–4 words each, e.g. "tense stealth", "readable chaos") are decision filters: every feature must serve a pillar or it is cut. Pillars end arguments faster than any spec.
- **Keep it a communication tool, not an archive.** A wiki page beats a locked document; version it, link it, prune it.

## Anti-patterns

| Anti-pattern | Why it bites | Do instead |
| --- | --- | --- |
| Designing on paper for months before building | Fun is only found by playing | Prototype the riskiest assumption first |
| "Make it more fun" as a task | Unactionable | Name the target MDA aesthetic and the mechanic behind it |
| Adding features instead of deepening verbs | Wide-and-shallow, no mastery | Deepen verb interaction before adding verbs |
| Currency with no sink | Meaningless clutter, inflation | Give every currency a distinct sink or cut it |
| Faucets outpacing sinks | Hyperinflation, trivial late game | Escalating/consumable sinks, caps, prestige |
| Unchecked positive feedback loop | Leader snowballs, match ends early | Add negative feedback / catch-up, tuned gently |
| One dominant strategy left standing | Choice dies, meta collapses | Nerf outlier / buff counters toward intransitive balance |
| Tuning five knobs at once | Can't attribute cause | Change one high-leverage variable at a time |
| Hard-coded balance constants | No iteration, no A/B, needs rebuild | Externalize tunables into data |
| Guiding testers during playtests | Contaminates the first-time signal | Watch silently; weight behavior over opinion |
| Scope creep / feature list as ambition | #1 indie killer | Cut features not quality; ship a vertical slice |
| 100-page design bible | Nobody reads it; goes stale | Living one-pager + pillars |

## Project grounding

If the workspace has a `02-DOCS/` harness, record the design in `02-DOCS/wiki/design/` — a `game-design.md` one-pager (hook, core loop, verbs, pillars, MVP scope, what's out) plus an `economy.md` if there is a currency system. Write each as an OKF v0.1 wiki article per the harness [`wiki-article-template.md`](../harness/references/wiki-article-template.md): YAML frontmatter with a non-empty `type:` (use `type: design`), a `timestamp` in ISO 8601, and standard markdown links — never wikilinks. Index it in `02-DOCS/wiki/index.md`. This is **recorded, not gated** — skip silently if there is no harness.

## Checklist

- [ ] The **core verb** is named and is fun in greybox with no goal attached.
- [ ] The three loops (moment-to-moment / session / meta) are identified and each is reward-funded by the layer below.
- [ ] The target **aesthetic** is named (MDA vocabulary), not "fun".
- [ ] Every currency has a distinct sink; faucets vs sinks are modeled and do not run away.
- [ ] Difficulty follows a sawtooth in the flow channel; high-leverage knobs are identified and data-driven.
- [ ] No dominant strategy survives; options are intransitively balanced.
- [ ] Feel/juice intent is specified (what + why), deferred to the engine skill for how.
- [ ] The riskiest assumption was prototyped and playtested; behavior (not just opinion) was observed.
- [ ] Scope is cut to a vertical slice; a one-page living doc + pillars exist, not a bible.
- [ ] Engine specifics were deferred to `godot`/`unity`/`unreal`; narrative to `game-storytelling`; layout to `level-design`.
