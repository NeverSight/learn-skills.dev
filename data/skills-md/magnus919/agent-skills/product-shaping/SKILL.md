---
name: product-shaping
description: >-
  Use this skill to shape product or engineering work before committing time to it:
  set appetites instead of estimates, narrow raw ideas into bounded problems, sketch
  solutions at the right level of abstraction, de-risk rabbit holes, write pitches,
  bet with capped downside (circuit breaker), and govern builds with discovered scopes
  and scope hammering. Adapted from Basecamp's Shape Up and extended for human+AI-agent
  teams. Use when a raw idea, feature request, or "redesign X" grab-bag needs to become
  a bounded project before anyone builds; when planning how much work an idea is worth;
  or when delegated agent builds need budgets, kill criteria, and non-convergence
  rules. Do not use for discovering whether a problem is real (use product-discovery),
  for portfolio-level sequencing across quarters (product-roadmapping-and-portfolio),
  for formal specification after the bet is placed (spec-driven-development), or for
  task-level prioritization frameworks like RICE (product-methodology).
license: MIT
metadata:
  tags: product-shaping, shape-up, appetite, pitch, betting, circuit-breaker, scope-hammering, hill-chart, bounded-delegation
---

# Product Shaping

Pre-commitment methodology for product and engineering work, adapted from Ryan Singer's
*Shape Up* (free edition at [basecamp.com/shapeup](https://basecamp.com/shapeup)),
extended for teams whose builders include AI agents.

The loop: **shape** a raw idea into a bounded pitch → **bet** a fixed appetite on it →
**build** by discovering scopes and hammering scope to fit the box → **move on**,
letting post-ship feedback re-enter as raw ideas.

## The core moves

1. **Set boundaries** — choose the appetite ("how much is this worth?") and narrow the
   problem to one specific story. Kill grab-bags ("redesign X", "X 2.0").
2. **Find the elements** — sketch the solution rough, solved, and bounded: breadboards
   for flows, fat-marker fidelity for visual problems, components-and-contracts for
   non-UI work.
3. **Patch rabbit holes** — attack your own sketch; settle hard decisions now, declare
   out-of-bounds cases, cut what the appetite can't afford.
4. **Write the pitch** — problem, appetite, solution, rabbit holes, no-gos.
5. **Bet** — commit the box uninterrupted, downside capped. No finish, no extension by
   default: the circuit breaker routes failure back to shaping.
6. **Build** — one integrated slice first, then discovered scopes tracked as
   uphill→downhill states; sequence scariest-first; compare down to baseline when
   deciding to stop.
7. **Move on** — scope cuts are not quality cuts; new feedback needs shaping, not
   instant yes.

## Reference files

Load only what the current step needs:

| Reference | Load when |
|---|---|
| [references/principles.md](references/principles.md) | You need the why: appetite vs estimate, fixed-time-variable-scope, rough/solved/bounded, evidence boundaries, lineage |
| [references/shaping.md](references/shaping.md) | Shaping steps 1–4 in detail, including shaping non-UI/backend/infrastructure work |
| [references/betting.md](references/betting.md) | Bets vs backlogs, circuit breaker mechanics, cycles as optional scaffolding, handling defects between bets |
| [references/building.md](references/building.md) | Hand-over-responsibility, one-piece-done, scope mapping, hill-state tracking, deciding when to stop |
| [references/hybrid-adaptation.md](references/hybrid-adaptation.md) | Any bet involving AI-agent builders: budget currencies, batched steering, verification cost inside scope, kill criteria for non-converging loops |
| [references/anti-patterns.md](references/anti-patterns.md) | Before betting anything that matters — documented field failures and their mitigations |

## Templates

| Template | Purpose |
|---|---|
| [templates/PITCH.md](templates/PITCH.md) | Fillable five-ingredient pitch document |
| [templates/SCOPE_MAP.md](templates/SCOPE_MAP.md) | Fillable scope table with hill states, chowder list, and breaker check |

## Entry points

| Situation | Start here |
|---|---|
| Raw idea or request arrived | [references/shaping.md](references/shaping.md) step 1 |
| Idea is validated but unbounded | [references/shaping.md](references/shaping.md) |
| Ready to write up the concept | [templates/PITCH.md](templates/PITCH.md) |
| Deciding what gets the next box | [references/betting.md](references/betting.md) |
| Bet placed, starting the build | [references/building.md](references/building.md) |
| Builders are AI agents | [references/hybrid-adaptation.md](references/hybrid-adaptation.md) |
| Project keeps not finishing / loops won't converge | [references/anti-patterns.md](references/anti-patterns.md), then hybrid-adaptation kill criteria |

## When not to use

- **The problem itself isn't validated yet** → `product-discovery`. Shaping narrows
  validated problems; it does not investigate whether the problem is real.
- **The question is strategic** (positioning, market entry, portfolio weight across
  quarters) → `product-strategy` or `product-roadmapping-and-portfolio`. This skill
  packages a single bet — one bounded commitment with an appetite and circuit breaker;
  roadmapping sequences many such bets across cycles with continue/pause/kill criteria.
- **The bet is already placed and the work needs a formal spec** → `spec-driven-
  development` consumes shaped output when formal specification is warranted.
- **Comparing unrelated feature proposals by score** → `product-methodology` (RICE/
  MoSCoW). Appetite replaces scoring inside this skill's scope; use one system, not both
  on the same decision.
- **An epic resists decomposition because nobody can define done** → route BACK here:
  that is an unshaped project, and force-splitting it produces disconnected tasks.
- **The work is small, routine, and fully understood** — skip shaping overhead; just do
  it.
- **The bet is placed and you need intent-to-delivery control** — classification,
  five-field intent contracts, autonomy gating, failure routing, and resumable status
  across the run. Route to `bmad`. Shaping ends at the bet; bmad carries the placed
  intent through bounded, inspectable, resumable agent work.

## Related skills

- `product-discovery` — upstream: validates the problem before narrowing begins
- `product-strategy`, `product-roadmapping-and-portfolio` — strategic context above bets
- `product-methodology` — downstream consumer of a won bet (prioritization, spec drafting)
- `spec-driven-development` — optional formal specification of shaped output post-bet
- `implementation-planning`, `subagent-driven-development` — execution after the bet;
  decompose only downhill work, never pre-shred a pitch
- `bmad` — intent-to-delivery control-plane protocol once the bet is placed:
  classification, five-field intent contracts, autonomy gating, failure routing,
  resumable spec status
- `work-tracking` — where scope/hill state lives during the build
- `qa-methodology` — edge-case QA as late-cycle level-up, not gate

## Evidence note

Every practice claim originates from one company's account (Basecamp, 2019).
Independent team records through 2026 show real adaptations and documented abandonments;
read references/anti-patterns.md before betting anything that matters, and treat six-week
cycles as tunable scaffolding rather than doctrine.
