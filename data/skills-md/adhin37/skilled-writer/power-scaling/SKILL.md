---
name: power-scaling
description: Hold the gap between the MC and the opposition at an entertaining width. Use when designing the advantage, planning an arc's opposition, on any capability change, and inside revision-pass.
metadata:
  type: skill
  tier: craft
  force: structural
  when: always
  role: [design, draft, gate]
  owns: [power-ladder, pressure, tier-gain, boost-debt]
---

# power-scaling

`conflict-engine` owns what is at stake · `timeline-engine` owns how hard the world hits back ·
`story-opening` owns whether the reader can price it yet · `power-system` owns the rules a power
obeys. This skill owns the **distance between the MC and the opposition**, and its shape over
hundreds of chapters.

Two opposite failures, and a long serial usually contains both, in that order:

| failure | symptom | cause |
|---|---|---|
| **Overpowered opening** | the first ten chapters have no question in them; the MC's advantage answers everything | the MC started at the top of a ladder the reader never saw anyone climb |
| **Flat middle** | around chapter 60 the fights stop mattering; the author invents a bigger sky | capability was tracked, distance was not |

The fix for both is the same and it is not "make the enemies stronger". Reader interest tracks the
**gap**, not the magnitude. Maintained in `state/power.md`.

---

## What lives in `roles/`

Section numbers are stable — other skills cite them — so the gaps are deliberate.

| § | file | open it when |
|---|---|---|
| 6, 7 | `roles/shared/power-scaling.curve-shapes.md` | choosing or changing `scaling.shape`, or the curve has to work in a genre whose conventions fight it — cultivation, litrpg, superhero, mundane |
| 8 | `roles/shared/power-scaling.failure-modes.md` | the curve is not landing and you need the named shape of what went wrong |
| — | `roles/gate/power-scaling.audit-card.md` | never, by you. `revision-pass` Pass 9e opens it |

## 1. The two ladders, and pressure

One ladder, sized `scaling.tiers` (default 7), defined once in `state/power.md` §2 and used for
**everybody** — the MC, the thug in the alley, the thing at the end of the book. Tiers are an
organising tool, never reader vocabulary (`power-system` §Tiers).

Every confrontation records three numbers. The third is the only one that matters:

> **pressure** — `P = opposition tier − MC tier`

| P | reads as | the rule |
|---|---|---|
| **+2** or worse | hopeless | the MC cannot win by force. They win by not-force, or they lose. Rare, and it opens arcs rather than closing them |
| **+1** | outmatched | the workhorse. A win here costs something that stays paid |
| **0** | even | the win comes from preparation, information or choice — the most interesting band |
| **−1** | favoured | the fight is fast, so the chapter's interest must be somewhere else, and you must be able to name where |
| **−2** or better | trivial | not a scene at all unless its point is something other than the contest. Budgeted: `scaling.trivial_per_arc` |

**This is the RPG shape, stated relatively.** The beginner village is P≈0 at tier 1. The late raid
boss is P≈+1 at tier 5. The MC gets stronger *and the fights stay hard* — that is the entire
trick, and losing it is what the flat middle is.

**Placing an opponent** is therefore a two-step decision, in this order:

1. What pressure does this chapter want? (from the arc's band, `state/power.md` §6)
2. What tier does that make the opposition? Then build a person who is that tier.

Never the reverse. An opponent designed first and priced afterwards is how a cast of
cannon fodder appears.

## 2. The edge — the advantage, bounded

The golden finger is not a tier. Keep them separate or the ladder stops meaning anything:

- **tier** — where a character sits on the world's own ladder.
- **edge** — what `mc.golden_finger` buys on top of it, recorded as `scaling.edge_worth`.

> **The edge closes a gap of at most 1.** `edge_worth` is `0` or `1`. Never 2.

So an MC one tier below the opposition fights *even* — because of the edge, and at
`scaling.edge_price`, paid every time (`power-system` §The four hard rules). This is exactly the
advantage a cultivation MC has over ordinary cultivators: real, visible, decisive at the margin,
and useless against a two-tier gap. It is what makes a tier-3 problem solvable at tier 2, and a
tier-4 problem still a wall.

Three consequences worth stating, because drafts break all three:

- **The edge is not a tier advance.** Using it well does not move the MC up §2's ladder; only a
  gain row in §4 does that.
- **Name what the edge cannot buy**, in `state/power.md` §1, and keep that sentence true. An edge
  with no stated blind side becomes a second ladder within twenty chapters.
- **`edge_worth: 0` is a real answer.** An advantage of the kind `mc-design` calls unpriced
  rather than force closes no gap at all, and those novels work.

## 3. The step rule, and boosts

### The step rule

> **A permanent tier advance is at most +1, and never arrives alone.**

Four things must be on the page. A gain missing any one of them is a defect, not a style choice:

| | requirement | why |
|---|---|---|
| 1 | a **source** with its own interests | nothing found in a cave by luck. Somebody gave, sold, taught or lost this, and they have a reason and a memory |
| 2 | a **price**, paid *before* the gain lands | paid after, it is a receipt. Paid before, it is a decision |
| 3 | a **setup** — the mechanism named at least `scaling.setup_lead` chapters earlier | a capability introduced in the chapter that needs it is a deus ex machina however well foreshadowed *within* that chapter (`power-system` §Sanderson's law) |
| 4 | a **new problem** | if it only solves things, do not grant it. Visible power identifies you; fuelled power makes you a customer; frightening power costs allies |

Cadence: `scaling.gain_gap_min` chapters minimum between advances (default 15). Closer together
and gains stop registering. Between gains, growth is in *skill* — new applications of the same
capability, which reads as intelligence and costs nothing (`competence-map`).

### Boosts

A **boost** is temporary reach above the current tier: the borrowed technique, the one-use
talisman, the rage, the thing the dying mentor hands over. These are legitimate and this skill
does not ban them. It bans the *free* ones.

Every boost row in `state/power.md` §5 carries:

- **how far above tier** it reaches, and **when it expires** — both decided before it is used;
- a **debt** — what it costs afterwards — due within `scaling.boost_debt_due` chapters and
  logged until paid. A debt is not the same as a cost during use. It is the bill;
- a **`climax?`** flag. **A boost may resolve an arc climax at most once in the novel.** The
  second time, the reader has learned that the ending of an arc is not decided by anything they
  were shown, and they are right.

The honest use of a boost is to let the MC *survive* a P≥+2 encounter, not win it. Survival buys
the next arc; winning buys nothing and costs the ladder.

## 4. The curve across a serial

### Shape

`scaling.shape`, set at init and changed only at an arc boundary:

| shape | the curve | the requirement |
|---|---|---|
| `climb` | default. Starts low, advances on the step rule | `scaling.start_tier` ≤ 2 |
| `inverted` | the MC is already at the top and the story is about something else | `scaling.substitute_tension` must be non-empty — see below |
| `regression` | starts high, loses it, reclaims it | the loss is on the page, not in backstory |
| `plateau-late` | climbs, then the ladder stops mattering and conflict moves off it | the plateau chapter is planned, not discovered |
| `none` | the novel has no capability ladder | this skill and `state/power.md` no-op entirely |

**On `inverted`.** An MC who is unbeatable from chapter 1 is a valid book — it is *One Punch Man* —
but only when the author knows what replaced the question. Write that down in
`scaling.substitute_tension`: recognition, boredom, the cost of being feared, whether anyone
will believe them, what they are for now that they have won. A blank `substitute_tension` with
`shape: inverted` is not a stylistic choice; it is an overpowered MC with no plan, and the pass
treats it as a defect.

### The first limit

The complement to `story-opening` §4's first win, and the same ordering rule the toolkit already
uses for foreknowledge:

> `opening.first_win_by_ch` **<** `scaling.first_limit_by_ch`

The advantage lands a legible win first, so the reader knows what they were promised. **Then** it
hits a wall it cannot climb, by `first_limit_by_ch` (default 8). A reader will not invest in a
climb until they have seen the ceiling. An advantage that only ever wins has no curve; one that
fails before it has ever worked was a lie in the blurb.

### The endgame

`scaling.endgame` names the final opposition and its tier in one line, written at init — the raid
boss, on day one. `scaling.ceiling_tier` caps where the MC may arrive. Together they make the
curve a route rather than a drift, and they are what `chapter-plan` distributes across the arcs
into `state/power.md` §6.

Check `scaling.endgame` against `ending.contract` whenever either changes. A curve that arrives
where the ending cannot happen is the same defect `timeline-engine` guards from the other side.

### What monitoring looks for

These are the five ways a curve dies, and all five are countable, which is why `sw curve` can find
them and why you should let it:

| | symptom | what it means |
|---|---|---|
| **Flat stretch** | no tier movement *and* no pressure variation for `scaling.flat_max` chapters | the progression reader's exit point |
| **Cadence** | advances closer together than `gain_gap_min` | gains have stopped registering |
| **Monotony** | the last ten confrontations all in one pressure band | the fights have become a texture |
| **Trivial budget** | more than `trivial_per_arc` confrontations at P ≤ −2 | the face-slap treadmill wearing a new hat (`mtl-detox`) |
| **Inverted drift** | pressure falling across an arc while tier rises | power has outrun the story. This is power creep, measured |

## 5. Where this runs

| when | do |
|---|---|
| `novel-init` round D | set the `scaling:` block; write `state/power.md` §1 and §2 |
| `mc-design` §5 | after the golden finger is chosen, set `edge_worth` and `edge_price` |
| `chapter-plan` arc step | set the arc's pressure band and its gain, into `state/power.md` §6 |
| `write-chapter` step 1 | read §1 for the MC's standing; pick this chapter's pressure from §6, then build the opposition to fit (§1) |
| `write-chapter` step 5 | append the pressure row to §3; any gain to §4 with all four requirements; any boost to §5 with its debt and due chapter; update §1 if the tier moved |
| `revision-pass` Pass 9e | the audit card |
| arc boundary | `sw curve`, then the shape check — is the curve still the one in §6? |

**Related skills.** `power-system` owns the rules a capability obeys, its cost and its counter, and
the MC's kit table · `conflict-engine` owns the stake ladder, which is a *different axis* and moves
independently — a rung-5 stake at P=0 is a better chapter than a rung-1 stake at P=+2 ·
`timeline-engine` owns how hard the world hits back and its governor, and its `Rival` profile is
the one that tracks §1 · `story-opening` owns the stakes ceiling and the first win ·
`mc-design` owns the golden finger this skill prices · `competence-map` owns skill acquisition,
which is how a character grows *between* tiers · `litrpg-system` (optional) renders tiers as
numbers · `mtl-detox` bans the rank recital and the treasure escalator.

## Self-check

- [ ] Every confrontation this chapter has a pressure value, and it was chosen before the opponent
- [ ] No opponent exists only to be beaten — each is a tier *and* a person (`conflict-engine`)
- [ ] The MC's tier on the page matches `state/power.md` §1
- [ ] The edge closed at most one tier, and it was paid for in the same scene
- [ ] Any tier advance is +1, with a source, a price paid first, a setup, and a new problem
- [ ] Any boost has an expiry, a debt and a due chapter, and did not resolve a second arc climax
- [ ] Nothing the reader has not seen fail decided the outcome (`power-system`)
- [ ] Tier names did not appear in the prose; no rank recital
- [ ] The chapter is inside the arc's planned pressure band, or the deviation is deliberate
- [ ] `state/power.md` §3 has this chapter's row, and the CCS `pwr>` line agrees with it
