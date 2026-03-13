---
name: mtga-draft-helper
description: "MTG Arena draft assistant using 17Lands data and set-specific draft guides. Use when the user asks to help with an MTG Arena draft, analyze draft picks, evaluate cards for limited, fetch 17Lands card ratings, read the Arena Player.log for current draft state, suggest which card to pick, show card images, build or suggest a deck after drafting, or anything related to Magic: The Gathering Arena drafting and limited formats. Includes set-specific archetype guides and pick-order tier lists (e.g. Lorwyn Eclipsed / ECL, Through the Omenpaths / Spider-Man / OM1). Triggers on: draft, 17lands, MTGA, pick, pack, limited, sealed, deck suggestion, draft helper, card rating, GIHWR, win rate, ECL, Lorwyn Eclipsed, OM1, Through the Omenpaths, Spider-Man."
---

# MTGA Draft Helper

Assist users during MTG Arena drafts by combining 17Lands statistical data with real-time Arena log parsing.

## Core Workflow

1. **Acquire card data** — Fetch card ratings and color win rates from the 17Lands API. See [references/17lands-api.md](references/17lands-api.md).
2. **Read draft state** — Parse the Arena `Player.log` to detect the active draft, current pack/pick, and taken cards. See [references/arena-log-parsing.md](references/arena-log-parsing.md).
3. **Evaluate picks** — Use win-rate metrics (GIHWR, OHWR, IWD, ALSA, etc.) and color signals to recommend the best pick. See [references/card-evaluation.md](references/card-evaluation.md).
4. **Show card images** — Display Scryfall card images from URLs stored in the dataset.
5. **Suggest a deck** — When the draft is complete (all picks made), build an optimal 40-card deck from the pool. See [references/deck-building.md](references/deck-building.md).

## Live Draft Tracking (Active Draft Mode)

To assist during a **live draft in progress**, the agent monitors the Arena log in real time. Full details in [references/live-draft-tracking.md](references/live-draft-tracking.md).

### Quick Start

1. **Start watcher** — Run `live_watcher.py` (from the reference) as a background process. It tails `Player.log` and emits JSON-line events to stdout.
2. **Poll for events** — Periodically check the background terminal output for new lines.
3. **React to each event:**
   - `draft_start` → fetch 17Lands data for the detected set, load set guide.
   - `pack` → resolve card IDs, evaluate, present ranked pick suggestion with card images.
   - `pick_made` → record the pick, update colours and curve, confirm to user.
4. **Draft complete** (42 picks) → auto-build a 40-card deck and present it.

### Fallback: Manual Poll

If a background watcher is not available, run this on demand when the user asks:
```powershell
Get-Content "$env:LOCALAPPDATA\Low\Wizards Of The Coast\MTGA\Player.log" -Tail 200 |
  Select-String "Draft\.Notify|Event_Join|Event_PlayerDraftMakePick|BotDraft_DraftStatus|CardsInPack"
```
Parse the output for the latest pack/pick data and respond with a suggestion.

## Quick Reference

### 17Lands Card Ratings URL

```
https://www.17lands.com/card_ratings/data?expansion={SET}&format={FORMAT}&start_date={START}&end_date={END}
```
Optional: `&user_group={top|middle|bottom}`, `&colors={WU|BG|...}`

### 17Lands Color Ratings URL

```
https://www.17lands.com/color_ratings/data?expansion={SET}&event_type={FORMAT}&start_date={START}&end_date={END}&combine_splash=true
```

### Card Image URLs

Each card's dataset entry contains an `image` array with Scryfall URLs:
```
https://cards.scryfall.io/large/front/{hash}.jpg
```
For split/DFC cards, a second URL may be present for the back face.

### Arena Player.log Location

| OS | Path |
|---|---|
| Windows | `C:/Users/{USER}/AppData/LocalLow/Wizards Of The Coast/MTGA/Player.log` |
| macOS | `~/Library/Logs/Wizards of the Coast/MTGA/Player.log` |
| Linux (Steam) | `~/.local/share/Steam/steamapps/compatdata/2141910/pfx/drive_c/users/steamuser/AppData/LocalLow/Wizards Of The Coast/MTGA/Player.log` |

### Key Draft Detection Strings in the Log

| Purpose | Log prefix |
|---|---|
| Premier/Trad draft start | `[UnityCrossThreadLogger]==> Event_Join ` |
| Quick draft start | `[UnityCrossThreadLogger]==> BotDraft_DraftStatus ` |
| Premier pack data | `[UnityCrossThreadLogger]Draft.Notify ` |
| Premier pick made | `[UnityCrossThreadLogger]==> Event_PlayerDraftMakePick ` |
| Quick draft pack | `DraftPack` within BotDraft_DraftStatus |
| Quick draft pick | `[UnityCrossThreadLogger]==> BotDraft_DraftPick ` |

### Key Data Fields

| Abbreviation | Full Name | Meaning |
|---|---|---|
| GIHWR | Games In Hand Win Rate | Win rate when card is drawn — **primary pick metric** |
| OHWR | Opening Hand Win Rate | Win rate when card is in opening hand |
| GPWR | Games Played Win Rate | Win rate in games where card is in the deck |
| ALSA | Average Last Seen At | Average pick position where card is last seen |
| ATA | Average Taken At | Average pick position where card is taken |
| IWD | Improvement When Drawn | Win-rate delta between drawn and not-drawn |
| GIH | Games In Hand (count) | Sample size for GIHWR |

### Draft Suggestion Prompt Template

When making pick suggestions, provide for each pack card:
```
{Name} | Colors: {W/U/B/R/G} | CMC: {N} | Mana Cost: {cost} | Rarity: {R} | Types: {types} | GIH WR: {X.X}%
```

Recommend the pick considering:
1. Raw GIHWR (higher is better, >56% is strong, >60% is a bomb)
2. Color alignment with already-drafted cards
3. Mana curve needs (creature distribution across CMC slots)
4. Archetype synergies for the set
5. Wheel probability (cards with high ALSA may come back)

### Deck Building Summary

After all picks, build a 40-card deck:
- Target ~17 lands, ~15 creatures, ~8 non-creature spells
- Identify the 2 strongest colors from the pool using color affinity (sum of above-average GIHWR per color)
- Sort cards by GIHWR within the chosen colors, fill creature curve first, then add non-creatures
- Calculate land distribution proportional to mana symbols in the deck
- Output in Arena-importable format: `{count} {Card Name}`

## Detailed References

- **17Lands API details & data schema**: [references/17lands-api.md](references/17lands-api.md)
- **Arena log parsing procedures**: [references/arena-log-parsing.md](references/arena-log-parsing.md)
- **Card evaluation methodology**: [references/card-evaluation.md](references/card-evaluation.md)
- **Deck building algorithm**: [references/deck-building.md](references/deck-building.md)
- **Live draft tracking (active mode)**: [references/live-draft-tracking.md](references/live-draft-tracking.md)

### Set-Specific Guides

- **Lorwyn Eclipsed (ECL)**: [references/ecl-lorwyn-eclipsed.md](references/ecl-lorwyn-eclipsed.md) — Archetype tier list, top commons/uncommons, pick order, card ratings, and draft strategy tips. Sources: [Draft Guide](https://draftsim.com/mtg-ecl-draft-guide/), [Set Review](https://draftsim.com/mtg-ecl-limited-set-review/), [Pick Order](https://draftsim.com/ECL-pick-order.php).
- **Through the Omenpaths / Spider-Man (OM1)**: [references/om1-through-the-omenpaths.md](references/om1-through-the-omenpaths.md) — Archetype tier list (GW/UB best, red weak), top commons/uncommons, Pick-Two draft strategy, color identity breakdown, and format tips. Source: [Draft Guide](https://draftsim.com/mtg-om1-draft-guide/).
