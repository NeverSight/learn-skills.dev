---
name: physical
description: Physical location awareness from FindMy. Use when user says "physical", "where am I", "location", "where is nat", or needs to check current physical location.
user-invocable: false
---

# /physical - Physical Location Awareness

Check Nat's current physical location from FindMy data.

## Usage

```
/physical
```

## Data Source

- Repo: `laris-co/nat-location-data` (GitHub)
- Files: `current.csv` (now), `history.csv` (today's log)
- Updated: Every 5 minutes via white.local cron
- Source: FindMy via Sate's iMac

## Instructions

Use a Haiku subagent to fetch and display location data:

```bash
# Locate the script (optimized search)
LOCATIONS=(
  "$HOME/.config/opencode/command/physical/scripts/location-query.ts"
  "./.opencode/command/physical/scripts/location-query.ts"
  "$HOME/.claude/skills/physical/scripts/location-query.ts"
  "./skills/physical/scripts/location-query.ts"
)

SCRIPT=""
for loc in "${LOCATIONS[@]}"; do
  if [ -f "$loc" ]; then
    SCRIPT="$loc"
    break
  fi
done

if [ -z "$SCRIPT" ]; then
  # Fallback to slow search only if explicit paths fail
  SCRIPT=$(find ~ -name location-query.ts -not -path "*/node_modules/*" 2>/dev/null | head -1)
fi

if [ -z "$SCRIPT" ]; then
  echo "Error: location-query.ts not found. Check install."
else
  bun "$SCRIPT" all
fi
```

Parse and display:

```
📍 Physical Status
═══════════════════

🏠 Currently At: [place column, or locality if empty]

| Device | Battery | Precision | Updated |
|--------|---------|-----------|---------|
[one row per device, sorted by accuracy]

📍 [address from iPhone row]
🗺️ Map: https://maps.google.com/?q=[lat],[lon]

⏱️ At this location: [X hours] (from TIME_AT_LOCATION section)
```

## Known Places (with coordinates)

| Place | Lat | Lon | Type |
|-------|-----|-----|------|
| cnx | 18.7669 | 98.9625 | airport |
| bkk | 13.6900 | 100.7501 | airport |
| dmk | 13.9126 | 100.6067 | airport |
| bitkub | 13.7563 | 100.5018 | office |
| maya | 18.8024 | 98.9676 | mall |
| central-cnx | 18.8072 | 98.9847 | mall |
| cmu | 18.8028 | 98.9531 | university |

## Directions

If user asks "how far to X":

```
🛫 To [destination]:
- Distance: [calculate km]
- 🗺️ Directions: https://maps.google.com/maps?saddr=[lat],[lon]&daddr=[dest_lat],[dest_lon]
```
