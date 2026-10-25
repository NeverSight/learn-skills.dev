---
name: chinese-metaphysics
description: Cast and interpret Chinese metaphysics charts with verified deterministic calculation - BaZi (八字 Four Pillars), Zi Wei Dou Shu (紫微斗数 Purple Star), and Qi Men Dun Jia (奇门遁甲). Use this skill whenever the user asks for a BaZi reading, four pillars, day master, 用神, Zi Wei chart, purple star astrology, Qi Men divination, Chinese astrology, fortune reading from birth date/time, auspicious timing, luck pillars, annual forecast (流年), auspicious date selection (择日), a 吉日 or auspicious day, picking a date for a business opening (开市), wedding, move, or signing, or asks to verify a chart from another app or practitioner. Also use it when the user gives a birth date + time + place and asks about personality, career timing, or compatibility in a Chinese metaphysics context. NEVER cast these charts from memory - the calendar math fails silently; always run the scripts.
license: MIT
metadata:
  version: "1.1.0"
---

# Chinese Metaphysics (BaZi / Zi Wei Dou Shu / Qi Men Dun Jia)

Casting is deterministic and runs in code. Interpretation is classical and runs through the reference files. Never compute pillars, star placements, or shensha mentally — solar-term boundaries and hour conversions are exactly where mental arithmetic fails silently.

## Scripts Reference

| Task | Script | Key flag |
|------|--------|----------|
| BaZi chart + luck pillars | `scripts/cast_bazi.py` | `--year YYYY` for annual overlay |
| Zi Wei Dou Shu chart | `scripts/cast_ziwei.py` | `--time-index 0..12` if birth time unknown |
| Qi Men Dun Jia divination | `scripts/cast_qimen.py` | use question time, not birth time |
| Date selection almanac (择日) | `scripts/cast_zeri.py` | `--natal 亥,亥,辰,巳` cross-refs the natal chart; `--hours` for 時辰 detail |
| Compatibility check | `scripts/check_compat.py` | always use this; never reason from one branch |
| Verify all engines (post-change) | `scripts/run_tests.py` | gold-chart assertions plus the 择日 almanac suite |

## Prerequisites (once per session)

```bash
pip install lunar-python py-iztro --break-system-packages          # BaZi + Zi Wei
pip install kinqimen --break-system-packages                       # Qi Men
pip install --upgrade --force-reinstall ephem --break-system-packages  # fixes kinqimen
```

> The ephem reinstall is required: kinqimen pins a stale ephem whose binary is broken on Python 3.12 (PyUnicode_GET_SIZE error). The pip warning about the version conflict is harmless. `cast_qimen.py` also contains a `sys.path` workaround for kinqimen's broken internal import — do not remove it.

## Required Inputs

Before casting, confirm you have all of the following:

- [ ] Birth date (`YYYY-MM-DD`)
- [ ] Birth time (`HH:MM`) — if unknown, BaZi runs on three pillars with reduced confidence; Zi Wei cannot run at all; say so
- [ ] Birth place (city is enough — you need its longitude and timezone meridian)
- [ ] Gender (required for luck-pillar direction and Zi Wei casting)
- [ ] For Qi Men: use the moment the question is asked, not the birth time

**Location to coordinates:** UTC+8 → meridian 120; UTC+9 → meridian 135, etc. Pass both longitude and meridian to the scripts — they apply true solar time correction internally.

## Workflow

### Step 1: Cast

Run the appropriate script(s) for the requested system:

```bash
python scripts/cast_bazi.py --date YYYY-MM-DD --time HH:MM \
  --longitude L --tz-meridian M --gender female|male [--year YYYY]

python scripts/cast_ziwei.py --date YYYY-MM-DD --time HH:MM \
  --longitude L --tz-meridian M --gender female|male

python scripts/cast_qimen.py --datetime "YYYY-MM-DD HH:MM" --longitude L
```

When both BaZi and Zi Wei are cast for the same person, cross-corroborate findings in the interpretation.

### Step 2: Check boundary cases

Before interpreting, check whether either of these applies:

- **Solar time correction changed the two-hour slot** — the BaZi script prints a clock-time VARIANT. Always tell the user which convention you are reading and why (see `references/methodology_forks.md` item 1).
- **Chart sits near a solar-term boundary or 23:00–24:00** — read `references/methodology_forks.md` before interpreting.

### Step 3: Interpret

Use only stars, gods, and interactions present in script output. Never invent shensha or interactions not printed.

| System | Reference file |
|--------|---------------|
| BaZi | `references/bazi_reading.md` |
| Zi Wei Dou Shu | `references/ziwei_and_qimen_reading.md` |
| Qi Men Dun Jia | `references/ziwei_and_qimen_reading.md` |
| Compatibility | `references/bazi_reading.md` (compatibility section) |
| Boundary / school forks | `references/methodology_forks.md` |

### Step 4: Disclose forks

The Day Master strength verdict can legitimately differ between scoring schools, and it flips the advice. When the chart is near that boundary:

- Present conclusions that survive both verdicts
- State which method you used
- See `references/methodology_forks.md` item 3 for the full protocol

## Verifying External Charts

When the user brings a chart from another app or practitioner, reproduce it with the scripts and diff. Reference `references/methodology_forks.md` before declaring a mismatch.

| Expect exact match | Expect legitimate school differences |
|--------------------|--------------------------------------|
| Pillars, hidden stems, nayin | Hour pillar (solar time vs clock time) |
| Void branches | Life lord 命主 |
| 12 palace placements | Strength verdict and 用神 |
| Four transformations | Qi Men ju near solar-term boundaries |
| Decade ranges | |

**Known external engines (audited June 2026):**
- **Engine A** (solar time school) — matches our defaults exactly
- **Engine B** (clock time school) — matches our `--no-solar-correction` mode; solar-term boundaries are ephemeris-grade and trustworthy
- **Engine C** (open-source Zi Wei) — do not use for casting; has a buggy auxiliary-star engine (misplaces 擎羊陀羅左輔右弼火星鈴星天魁, omits 祿存)

## Testing

Run after any script change or environment change (library upgrades):

```bash
python scripts/run_tests.py
```

Verifies all engines against a gold chart validated against a professional engine, and runs the date-selection almanac suite (`test_zeri.py`, 20 checks). Every case must pass.

## Honesty Requirements (non-negotiable)

- **Read every chart in isolation.** Base the reading only on the chart output.
  Do not bring in anything you know about the person from elsewhere — their job,
  studies, travel, past conversations, or any stored notes. Outside context
  contaminates the reading; the chart has to speak for itself.
- These are classical interpretive frameworks, not prediction engines. Present
  a reading as structured self-reflection — a mirror, not a forecast.
- Don't present timing as instructions for big decisions (starting a business,
  marriage, relocation, or anything medical, legal, or financial). Always point
  the user back to real-world factors.
- Explain every Chinese term the first time you use it, in plain words.
- Write "negative" flags as things to manage, never as fate.
- Keep the wording natural and direct. Skip the mystical register — say what a
  feature means for the person's actual life.
- If output from another AI or engine contains derivations, verify them with the
  scripts before endorsing them.
