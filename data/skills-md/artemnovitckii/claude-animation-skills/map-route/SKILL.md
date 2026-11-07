---
name: map-route
description: Makes a 3D map animation for a reel. A clean white city with parks and a river, a coloured route that draws itself from start to destination while the camera follows, a red pin that drops with a bounce, an ETA card that counts down and a destination card. Use when the user runs /map-route or asks for an animated route, a "from A to B" map, a journey or a commute animation.
---

# /map-route

```
┌──────────────────────┐
│ [▲ 9 min]            │  ETA card counts down, then "Arrived"
│      ┌Iron Yard Gym┐ │  destination card after the pin lands
│  ▒▒   ▒▒   📍  ▒▒    │  white 3D blocks, parks, a river
│  ▒▒ ━━━━━━━┛   ▒▒    │  the route draws itself, the camera rides along
│  ▒▒ ┃  ▒▒      ▒▒    │  and pulls back at the end
└──────────────────────┘
```

## First use
This skill's folder is the "Base directory" Claude Code shows when it loads it.
```bash
SKILL_DIR="<base directory of this skill>"
KIT=$(python3 -c 'import os,sys;print(os.path.realpath(os.path.join(sys.argv[1],"..","..","kit")))' "$SKILL_DIR")
[ -s "$KIT/node_modules/three/build/three.module.js" ] || bash "$KIT/setup.sh"
```
Needs ffmpeg and Node. It renders with WebGL in headless Chrome.

## Steps
1. **Trip.** Get the destination name, the minutes and the distance from the user ("home to the gym, 2.8 km, 9 min"). If they only give one of minutes or distance, estimate the other (walking about 12 min per km, cycling about 4, driving in town about 2) and say so.
2. **Spec.** Write `<name>.map.json` (below).
3. **Build.** Run `python3 "$SKILL_DIR/build.py" <spec.json>`. A 3D render takes about 1.5 minutes, most of it HyperFrames waiting on WebGL (a `sub_timeline_readiness_timeout` warning is normal). Add `--snap 3.8` to check the last frame first.
4. **Check** the sheet: the destination card is fully on screen and the street labels don't sit on the ETA card.
5. **Hand over** the mp4 path.

## Spec
```json
{
  "destination": "Iron Yard Gym", "minutes": 9, "distance": 2.8, "unit": "km",
  "places": ["North Quay", "Botanic Gardens", "Market Hall", "Elm Park", "The Canal"],
  "accent": "#2f7cf6", "seed": 7
}
```
- **`destination`**, **`minutes`**, **`distance`**: required. **`unit`**: `"km"` or `"mi"`.
- **`places`**: 5 small grey labels at fixed spots on the map. In order: near the start, a park at the far left, a block mid-route, a park at the far right, the river. Use names that fit the user's city, or `""` to hide one. They are decoration, not real geography.
- **`accent`**: the route, the moving dot and the ETA icon (hex). The pin stays red.
- **`seed`**: a different whole number gives a different arrangement of buildings and parks.
- **`hold`** (optional): extra seconds at the end. **`out`** (optional): the output path.

## Changing the route
The route shape is fixed: up, right, up, right, ending at the pin. To change it, copy `"$SKILL_DIR/template.html"` next to the spec, edit `WP` in the copy (`[x, z]` points; every corner must sit on a street, which run along multiples of 4; `x` from -36 to 36, `z` from -88 to 24, and north is negative `z`), and add `"template": "template.html"` to the spec. The camera's final pull-back target (`new THREE.Vector3(3, 0, -27)`) and the label spots (`LBL`) are tuned for the default route, so move them with it and check with `--snap`.

## Taste
- Short, real-sounding names. The destination card holds about 26 characters.
- Keep it calm: one route, one pin, no extra arrows or callouts.
