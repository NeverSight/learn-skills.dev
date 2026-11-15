---
name: doman-mahjong
description: Analyze FFXIV Doman Mahjong hands and design or debug a Riichi rules engine or solver. Use for tile notation, waits, shanten, yaku, scoring, furiten, calls, and FFXIV rule differences. Does not supply verified game memory offsets, addon callbacks, or a working plugin.
license: "MIT for authored guidance; linked external rules and data sources are not bundled and keep their own terms. See NOTICE.md."
---

# Doman Mahjong

Use the FFXIV rules profile when evaluating a hand. Generic Riichi engines
often implement a different ruleset, even when their hand calculations agree.

## Choose the reference

- For legality, tile representation, and FFXIV exceptions, read
  [rules.md](references/rules.md).
- For yaku, fu, and payments, read [scoring.md](references/scoring.md).
- For state modeling, shanten, tile availability, and recommendation design,
  read [solver.md](references/solver.md).
- For threat detection, deal-in statistics, push/fold and riichi-versus-
  undeclared comparisons, read [defense.md](references/defense.md).
- For worked cases and a plan for checking the client, read
  [verification.md](references/verification.md).
- For source authority and contradictions between sources, read
  [sources.md](references/sources.md).

## Analyze a position

Establish the hand's phase before counting tiles: after discard, after draw,
after a call, or awaiting a replacement draw. Record declared melds separately
from concealed tiles. Preserve which physical tile completed the hand.

For a win question, distinguish a complete tile shape, a yaku-bearing hand,
and a legal win in the current event. Furiten can forbid ron even when the
same tiles could win by tsumo. Dora cannot supply the required yaku.

For a discard question, identify the permitted discards, compare the resulting
shanten and available improvements, then account for yaku, value, defense, and
match position. Explain tied choices and missing observations. A probability
estimate depends on assumptions about hidden tiles and opponents.

Ask only for context needed by the answer. Exact scoring generally needs the
winning tile, ron or tsumo, seat and round winds, open/closed melds, riichi and
other event flags, dora/red tiles, honba, and the rules variant. Ron legality
also needs discard and pass history. When history is unavailable, report that
limitation instead of inferring that furiten is false.

## Evidence boundaries

The references distinguish official FFXIV rules, generic Riichi calculations,
and unresolved details. Check current in-game help or a recorded match before
promoting an unresolved detail to a default. Save a counterexample when the
client disagrees; do not patch the hand evaluator merely to match a screenshot
whose event history is incomplete.

Client tile IDs, seat indices, UI nodes, packets, and action callbacks are
unverified by this skill. Establish those mappings from the current client
source and observations when implementing the plugin. Keep logical tile
notation independent of those mappings.
