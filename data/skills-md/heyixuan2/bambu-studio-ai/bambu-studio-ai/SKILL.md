---
name: bambu-studio-ai
description: "Bambu Lab 3D printer control and automation. Activate when user mentions: printer status, 3D printing, slice, analyze model, generate 3D, AMS filament, print monitor, Bambu Lab, or any 3D printing task. Full pipeline: search → generate → analyze → colorize → slice → print → monitor. Supports all 9 Bambu Lab printers (A1 Mini, A1, P1S, P2S, X1C, X1E, H2C, H2S, H2D)."
version: "0.22.21"
author: TieGaier
metadata:
  openclaw:
    emoji: "🖨️"
    requires:
      bins: ["python3", "pip3"]
    install:
      - id: pip-deps
        kind: pip
        packages: ["bambulabs-api", "bambu-lab-cloud-api", "requests", "trimesh", "numpy", "Pillow", "ddgs", "pygltflib"]
        required: true
      - id: ffmpeg
        kind: brew
        package: ffmpeg
        optional: true
        label: "Camera snapshots (LAN mode)"
      - id: bambu-studio
        kind: cask
        package: bambu-studio
        optional: true
        label: "Model preview and manual slicing"
      - id: blender
        kind: cask
        package: blender
        optional: true
        label: "Multi-color pipeline + HQ preview rendering"
      - id: orcaslicer
        kind: cask
        package: orcaslicer
        optional: true
        label: "CLI slicing backend"
env:
  - name: BAMBU_MODE
    required: false
    description: "Connection mode: cloud (default) or local"
  - name: BAMBU_MODEL
    required: false
    description: "Printer model (e.g., H2D, A1 Mini, X1C)"
  - name: BAMBU_EMAIL
    required: false
    description: "Bambu account email (cloud mode)"
  - name: BAMBU_IP
    required: false
    description: "Printer LAN IP (local mode)"
  - name: BAMBU_SERIAL
    required: false
    description: "Printer serial number (local mode)"
  - name: BAMBU_ACCESS_CODE
    required: false
    description: "LAN access code from printer touchscreen (local mode)"
  - name: BAMBU_VERIFY_CODE
    required: false
    description: "Cloud login verification code (one-time)"
  - name: BAMBU_DEVICE_ID
    required: false
    description: "Cloud device ID (auto-detected)"
  - name: BAMBU_3D_PROVIDER
    required: false
    description: "AI 3D gen provider: meshy, tripo, printpal, 3daistudio, rodin"
  - name: BAMBU_3D_API_KEY
    required: false
    description: "API key for chosen 3D generation provider"
secrets:
  - name: BAMBU_PASSWORD
    required_when: "mode=cloud"
    storage: ".secrets.json"
    description: "Bambu Lab account password"
  - name: BAMBU_ACCESS_CODE
    required_when: "mode=local"
    storage: ".secrets.json"
    description: "LAN access code from printer Settings → Device"
  - name: BAMBU_3D_API_KEY
    required_when: "3D generation enabled"
    storage: ".secrets.json"
    description: "API key from chosen 3D generation provider"
security:
  no_credentials_shipped: true  # X.509 cert/key downloaded on demand, not shipped
  secrets_storage: ".secrets.json (chmod 600, git-ignored)"
  config_storage: "config.json (non-sensitive printer settings, git-ignored)"
  token_cache: ".token_cache.json (cloud auth token, 90d TTL, git-ignored). User can delete to force re-auth."
  verify_code_file: ".verify_code (one-time cloud login code, git-ignored)"
  files_gitignored: [".secrets.json", "config.json", ".token_cache.json", ".verify_code"]
  persistence: "Reads config.json at startup, .secrets.json on demand (lazy, not at import). Writes .token_cache.json, .verify_code locally. No remote data exfiltration."
  shipped_credentials: "NONE — no credentials, certificates, or keys are shipped or auto-downloaded."
  x509_setup: "User provides authentication certificate during setup if they enable Developer Mode auto-print. Stored locally in references/*.pem (git-ignored, key chmod 600). Not shipped, not downloaded by code."
  x509_scope: "Signs MQTT commands for LAN auto-print only. Requires user's own access code + same network."
  network_access:
    - "Bambu Lab Cloud API (bambulab.com) — printer control, cloud mode only"
    - "Bambu Lab MQTT (LAN) — printer control, local mode only"
    - "Meshy API (api.meshy.ai) — 3D generation, optional"
    - "Tripo3D API (api.tripo3d.ai) — 3D generation, optional"
    - "Hyper3D Rodin API (hyperhuman.deemos.com) — 3D generation, optional (Business subscription)"
    - "Printpal API — 3D generation, optional"
    - "3D AI Studio API — 3D generation, optional"
    - "DuckDuckGo (via ddgs) — model search, optional"
  consent: "All network calls, file writes, printer operations, and monitoring require explicit user consent."
keywords:
  - 3d printing
  - bambu lab
  - ams
  - text to 3d
  - slicing
  - print monitoring
  - multi-color
---

# 🖨️ Bambu Studio AI

Request → Collect Info → Search/Generate → Analyze(11pt) → [Colorize] → Slice → Preview(chat) → Preview(BS) → Confirm → Print → Monitor

Pre-check: If `config.json` does not exist → run First-Time Setup before any operation.

---

## Quick Reference

| I want to... | Command |
|---|---|
| Printer status | `python3 scripts/bambu.py status` |
| Print progress | `python3 scripts/bambu.py progress` |
| Printer hardware info | `python3 scripts/bambu.py info` |
| Start a print | `python3 scripts/bambu.py print <file> --confirmed` |
| Pause / Resume / Cancel | `python3 scripts/bambu.py pause\|resume\|cancel` |
| Speed mode | `python3 scripts/bambu.py speed silent\|standard\|sport\|ludicrous` |
| Light on/off | `python3 scripts/bambu.py light on\|off` |
| AMS filament info | `python3 scripts/bambu.py ams` |
| Camera snapshot | `python3 scripts/bambu.py snapshot` |
| Send G-code | `python3 scripts/bambu.py gcode "G28"` |
| Notification | `python3 scripts/bambu.py notify --message "done"` |
| Generate 3D (text) | `python3 scripts/generate.py text "desc" --wait` (`--raw` skips auto-enhancement) |
| Generate 3D (image) | `python3 scripts/generate.py image photo.jpg --wait` |
| Download model | `python3 scripts/generate.py download <task_id>` |
| Analyze model | `python3 scripts/analyze.py model.stl --orient --repair --material PLA` |
| Multi-color | `python3 scripts/colorize.py model.glb --height 80 --max_colors 8 -o out.obj` (tunable: `--min-pct`, `--no-merge`, `--island-size`, `--smooth`) |
| Slice | `python3 scripts/slice.py model.stl --orient --arrange --quality fine` |
| Slice (specific setup) | `python3 scripts/slice.py model.stl --printer A1 --filament "Bambu PETG Basic"` |
| List slicer profiles | `python3 scripts/slice.py --list-profiles` |
| Preview (quick) | `python3 scripts/preview.py model.stl` |
| Preview (HQ Blender) | `python3 scripts/preview.py model.stl --hq` |
| Search models | `python3 scripts/search.py "phone stand" --limit 5` |
| Monitor print | `python3 scripts/monitor.py --auto-pause` |
| Check deps | `python3 scripts/doctor.py` |

All scripts support `--help`. `generate.py` auto-enhances prompts and limits size to printer build volume.

---

## Overall Flow

```
User Request
    │
    ▼
Information Collection
    │
    ▼
Decision 1: Model Source
    ├─ A: Internet Search (preferred default)
    ├─ B: AI Generate (single-color)
    ├─ C: AI Generate (multi-color)
    └─ D: User-provided file
    │
    ▼
Model Processing (analyze → repair → orient → [colorize] → slice)
    │
    ▼
Report Results to User
    │
    ▼
⛔ Open in Bambu Studio → User Inspects
    │
    ▼
User Confirms ("looks good" / "print it")
    │
    ▼
Decision 2: Print Method
    ├─ E: Auto Print (Developer Mode only, not recommended)
    └─ F: Manual Print (user handles in Bambu Studio)
    │
    ▼
Print Monitoring (both workflows, or on user request)
```

---

## Step 1: Information Collection

Collect before proceeding:

**Model requirements:**
- What to print (object description)
- Target dimensions — MUST ask before generating ("How big? e.g., 80mm tall")
- Style / appearance (optional)

**Print parameters:**
- Single-color or multi-color (AMS)
- Material (default: PLA)
- Quality: draft / standard / fine / extra (optional)
- Purpose: functional or decorative (optional, affects walls + infill)

**Model source — ask user:**
> "Do you want me to:
> 1. 🔎 Search online — existing models, usually higher quality
> 2. 🎨 AI generate — custom model from scratch
> 3. 🤷 Not sure — I'll search first, generate if nothing fits"

Default: search first. Common objects (phone stand, hook, vase) almost always exist online.

---

## Step 2: Model Source (Decision Point 1)

### Workflow A — Internet Search (preferred)

1. `search.py "query" --limit 5` → MakerWorld, Printables, Thingiverse, Thangs
2. Present results with name, source, URL
3. User selects → download → validate format (STL/OBJ/3MF)
4. → Model Processing

If no good results → offer AI generate.

### Workflow B — AI Generate (single-color)

1. First-time disclaimer (once): "AI models depend on provider + prompt. NOT production-ready — always review in Bambu Studio."
2. Confirm dimensions
3. `generate.py text "prompt" --wait` → auto-enhances, auto-limits to build volume
4. → Model Processing

### Workflow C — AI Generate (multi-color)

1. Same disclaimer as B
2. Confirm dimensions + desired colors
3. `generate.py text "prompt" --wait` → textured GLB
4. `colorize.py model.glb --height <size> --max_colors 8` → vertex-color OBJ
   - Pixel HSV classify → greedy area-based color select → CIELAB assign → vertex color
   - No shadow removal needed — HSV classification bypasses baked lighting
5. **Show quantized texture preview to user** — send the `_preview.png` image
6. **Analyze results and suggest tuning** if needed:
   - Report detected colors with names, hex codes, and percentages
   - If small but meaningful colors were lost (e.g., <1% features like eyes, accessories):
     → Suggest: `--min-pct 0` (keep all colors above 0.1%)
   - If similar colors are merged incorrectly (e.g., yellow body + brown pants):
     → Suggest: `--no-merge` (disable family mutual exclusion)
   - If too many artifact colors appear:
     → Suggest: higher `--min-pct` or `--island-size`
   - If boundaries are too noisy or too smooth:
     → Suggest: adjust `--smooth` (0=none, 5=default, higher=smoother)
7. If user requests changes → re-run colorize with adjusted params → show new preview
8. When user approves → Model Processing

**Colorize tunable parameters:**
| Parameter | Default | Effect |
|-----------|---------|--------|
| `--max_colors N` | 8 | Maximum colors (hard limit ≤8 for AMS) |
| `--min-pct X` | 0.1 | Min family % threshold (0=keep all, 5=aggressive filter) |
| `--no-merge` | off | Disable family group exclusion (all 12 families independent) |
| `--island-size N` | 1000 | Remove isolated patches < N pixels (0=disabled) |
| `--smooth N` | 5 | Majority vote boundary passes (0=raw, higher=smoother) |

### Workflow D — User-Provided File

1. Validate format (STL/OBJ/3MF/GLB), convert if needed
2. → Model Processing

---

## Step 3: Model Processing

All models MUST go through this. No exceptions.

**Analysis (11-point check):**
```
analyze.py model.stl --orient --repair --material PLA --purpose functional
```
Checks: dimensional tolerance, wall thickness, load direction, overhangs (>45°), print orientation, floating parts, layer height, infill rate, wall count, top layers, material compatibility. Also: watertight, manifold, build volume fit.

**Auto-repair:** Fix normals, fill holes, remove degenerate faces.

**Auto-orient:** Optimal stability, auto unit detection (meters→mm).

**Report to user (MANDATORY):**
- Printability score (X/10)
- Warnings and issues
- Repairs performed
- Recommended settings (layer height, infill, walls, temps, supports)

Example: "Score 8/10. Repaired 58K non-manifold edges. Walls: 1.5mm ✅ Overhangs: 3.2% ✅ Recommended: 0.20mm layers, 20% infill, PLA 210°C."

**Slice (skip if user will slice in Bambu Studio):**
```
slice.py model.stl --orient --arrange --quality standard
```
Auto-detects printer + nozzle. Quality: draft(0.24) / standard(0.20) / fine(0.12) / extra(0.08). Output: .3mf with G-code.

---

## Step 4: User Confirmation

⛔ **MANDATORY — NEVER SKIP**

1. Open in Bambu Studio: `open -a "BambuStudio" model_sliced.3mf`
2. Tell user to inspect:
   > "I've opened the model in Bambu Studio. Please check:
   > - Does it look correct? Missing or deformed parts?
   > - Floating/disconnected pieces?
   > - Correct size? (check dimensions in bottom bar)
   > - Any red warnings?
   > - Slice and check: estimated time, filament usage, supports.
   > Let me know when ready!"
3. WAIT for explicit confirmation.

⛔ NEVER auto-print. AI models frequently have errors analysis can't fully catch.

4. Ask print method:
   - Direct automatic printing → Workflow E (Developer Mode only, not recommended)
   - Manual in Bambu Studio → Workflow F

---

## Step 5: Print Execution (Decision Point 2)

### Workflow E — Auto Print (Developer Mode only, not recommended)
⚠️ Requires Developer Mode ON. Bambu Studio and Bambu Handy will disconnect.
1. `bambu.py print model.3mf --confirmed`
2. Confirm: "Print started!"
3. → Monitoring

### Workflow F — Manual Print
- Model already open in Bambu Studio
- User adjusts settings and prints manually from BS/Handy

**Print detection — two methods:**

1. **Active listen (after model handoff):** When agent opens a model in BS (Workflow B/C/D), immediately start a background MQTT listener (30 min window). If printer state changes to RUNNING → notify user and offer monitoring.
   - Implementation: background `exec` running paho-mqtt subscribe loop, poll every 30s for state change
   - Auto-stop after 30 min if no print detected
   - On detection: "🖨️ I see you started printing [filename]! Want me to monitor with live updates and snapshots?"

2. **Heartbeat fallback:** During regular heartbeats, check printer MQTT status. If RUNNING and not already monitoring → notify user.

- If user accepts → Start Monitoring (Step 6)

---

## Step 6: Print Monitoring

Trigger: Auto print (Workflow E), manual print (Workflow F), or user request. Requires LAN mode.

⚠️ Always ask: "Want me to monitor? Auto-pause on serious issues?"

**Monitoring method:** Direct MQTT subscription via paho-mqtt (NOT bambulabs_api — it has SSL issues).
Connect to `{printer_ip}:8883`, subscribe to `device/{serial}/report`, parse `print` messages.

**Camera snapshots are MANDATORY during monitoring:**
- Capture via RTSP: `bambu.py snapshot` (ffmpeg → rtsps://bblp:{code}@{ip}:322/streaming/live/1)
- Send snapshot with EVERY progress update to user
- Include snapshot in anomaly alerts

**Default monitoring schedule (milestone-based, ~5 messages per print):**
| Event | Trigger | Action |
|---|---|---|
| Print start | State → RUNNING | Notify + 📸 snapshot |
| 25% progress | mc_percent ≥ 25 | Status + 📸 snapshot |
| 50% progress | mc_percent ≥ 50 | Status + 📸 snapshot |
| 75% progress | mc_percent ≥ 75 | Status + 📸 snapshot |
| Print complete | State → FINISH/IDLE | Completion + 📸 final snapshot |
| Anomaly | Any time | Immediate alert + 📸 snapshot + auto-pause (if enabled) |

User can adjust frequency. Track reported milestones to avoid duplicates.

**Anomaly detection:**
| Anomaly | Severity | Action |
|---|---|---|
| Progress stall >10min | Warning | Alert user + snapshot |
| Temperature anomaly | Critical | Alert + snapshot + auto-pause |
| Print failure/error | Critical | Alert + snapshot + auto-pause |
| Unexpected pause | Warning | Alert user + snapshot |
| Bed detachment | Critical | Auto-pause + alert + snapshot |
| Spaghetti | Critical | Auto-pause + alert + snapshot |

**Status report format (send to user):**
```
🖨️ Print Update — {filename}
📊 Progress: {percent}% | Layer {current}/{total}
⏱️ Remaining: {time}
🔥 Nozzle: {temp}°C | 🛏️ Bed: {temp}°C
📸 [attached snapshot]
```

---

## First-Time Setup

Triggered when `config.json` doesn't exist. Conversational:

1. **Printer model** — A1 Mini, A1, P1S, P2S, X1C, X1E, H2C, H2S, H2D
2. **Connection** — LAN (recommended: IP + serial + access code) or Cloud (email + password, limited)
3. **Print mode** — MUST explain clearly to user:
   - **Option A: Recommended (safe)** — Agent generates/slices model → opens in Bambu Studio → user reviews and prints manually. No special printer settings needed.
   - **Option B: Full auto-print** — Agent controls printer directly (start/stop/monitor via MQTT). Requires:
     - ⚠️ **Developer Mode ON** (printer touchscreen → Settings → LAN Only Mode → ON → Developer Mode → ON)
     - ⚠️ Bambu Studio and Bambu Handy will **completely disconnect** (no cloud, no remote monitoring)
     - ⚠️ Only LAN access (same network only)
     - Agent still ALWAYS shows preview before printing (never auto-prints without user confirmation)
   - Save choice as `print_mode: "manual"` or `print_mode: "auto"` in config.json
4. **3D generation** (optional) — Meshy, Tripo, Printpal, 3D AI Studio + API key
5. **Notifications** — auto / Discord / iMessage / Telegram / etc.
6. **Save** — `config.json` + `.secrets.json` (chmod 600, git-ignored)
7. **Verify** (ask permission) — test connection, camera, AMS
8. **Summary**

---

## Environment & Dependencies

**Required:** `python3`, `pip3`
```bash
pip3 install bambulabs-api bambu-lab-cloud-api requests trimesh numpy Pillow ddgs cryptography paho-mqtt
```
**Optional:** `ffmpeg` (camera), Bambu Studio (preview/slicing), Blender 4.0+ (multi-color + HQ preview), OrcaSlicer (CLI slicing)

**Env vars** (override config.json): `BAMBU_MODE`, `BAMBU_MODEL`, `BAMBU_EMAIL`, `BAMBU_IP`, `BAMBU_SERIAL`, `BAMBU_3D_PROVIDER`

**Secrets** (`.secrets.json`, chmod 600): `password`, `access_code`, `3d_api_key`. All user-provided, never shipped.

---

## Common Issues

| Problem | Fix |
|---|---|
| SSL handshake error (LAN) | Normal (self-signed certs). Handled automatically. |
| API method not found | `pip3 install --upgrade bambulabs-api` (v2.6.6+) |
| Can't connect (LAN) | LAN Mode ON + correct IP + same network |
| Cloud verification code | Wait for email, enter once. Token cached 24h. |
| Camera timeout | Wake printer (tap screen), check IP. |
| AI model has holes/floating parts | Expected. Always run `analyze.py --repair`. |

---

## Known Limitations

| Feature | Status |
|---|---|
| Single-color pipeline | ✅ Stable |
| Multi-color (colorize) | ✅ Auto-detect ≤8 colors, vertex-color OBJ → BS color merge dialog |
| CLI slicing | ✅ OrcaSlicer backend (BS CLI SEGFAULT in v2.5.0) |
| End-to-end auto-print | ✅ Works with Developer Mode ON (X.509 signed MQTT + FTP upload) |

---

## Reference Documents

- `references/model-specs.md` — All 9 printer specifications
- `references/bambu_filament_colors.json` — Bambu Lab 43-color palette (reference only, colorize v4 uses texture-native colors)
- `references/bambu-mqtt-protocol.md` — MQTT protocol
- `references/bambu-cloud-api.md` — Cloud API
- `references/3d-generation-apis.md` — Provider API endpoints
- `references/3d-prompt-guide.md` — Prompt engineering for 3D

## License

MIT · GitHub: https://github.com/heyixuan2/bambu-studio-ai
