---
name: sbs-training
description: Stronger By Science (SBS) program templates by Greg Nuckols. Activate when users ask about SBS programs, autoregulated training, training max systems, set threshold progression, reps to failure progression, last set RIR, program builder, or want to set up/run any of the 12 SBS spreadsheet programs.
---

# SBS Training Programs

Comprehensive guidance for all 12 Stronger By Science program templates by Greg Nuckols. These autoregulated programs use a training max system to calculate working weights and adjust loads based on performance.

**Source**: Stronger By Science Program Bundle by Greg Nuckols — [strongerbyscience.com](https://www.strongerbyscience.com/)

## When to Use This Skill

Activate when users:
- Want to run any SBS / Stronger By Science program
- Ask about autoregulated training with training maxes
- Want to understand set threshold, last set RIR, or reps to failure progression
- Need help setting up an SBS spreadsheet
- Ask about the SBS Program Builder
- Want to compare SBS program variants
- Ask about Greg Nuckols' programming

## Reference File Index

| File | Topic | Key Content |
|------|-------|-------------|
| `references/00-glossary.md` | Terminology | TM, RIR, RTF, RPE, aux/accessory definitions |
| `references/01-training-max-system.md` | Training max | TM concept, working weight formula, rounding, single @8 override |
| `references/02-periodization-structure.md` | Program structure | 3×7-week blocks, wave loading, deloads, late-program guidance |
| `references/03-exercise-framework.md` | Exercise setup | Main/aux/accessory categories, upper back, frequency tabs, LF variants |
| `references/04-autoregulation-set-threshold.md` | Set threshold | SBS Strength Program progression method |
| `references/05-autoregulation-last-set-rir.md` | Last set RIR | Last Set RIR progression method |
| `references/06-autoregulation-rtf.md` | Reps to failure | RTF progression for strength and hypertrophy |
| `references/07-intensity-tables.md` | Numerical tables | All intensity, rep target, RIR, and RTF lookup tables |
| `references/08-novice-programs.md` | Novice programs | Linear Progression and Novice Hypertrophy (self-contained) |
| `references/09-program-builder.md` | Program builder | Mix-and-match progressions, 5 accessory schemes, assembly |
| `references/10-tips-and-recommendations.md` | Tips & FAQ | Best results data, effort, rest periods, switching programs |
| `references/11-exercise-distribution.md` | Day layouts | Exercise-to-day mapping per frequency, Standard vs LF, per-muscle frequency |

## Decision Guide

```
Is the user a novice (0-2 years, can add weight weekly)?
├── YES → Strength focus? → SBS Linear Progression (ref 08)
│         Hypertrophy focus? → SBS Novice Hypertrophy (ref 08)
└── NO (intermediate+)
    ├── Want to mix-and-match progressions? → SBS Program Builder (ref 09)
    └── Want a pre-built program?
        ├── Goal: Strength (peaking to 1RM test)
        │   ├── Prefer counting sets to RIR cutoff? → SBS Strength Program (ref 04)
        │   ├── Prefer rating last set RIR? → SBS Strength Last Set RIR (ref 05)
        │   └── Prefer one AMRAP set per exercise? → SBS Strength RTF (ref 06)
        └── Goal: Hypertrophy (higher reps, no peaking)
            └── SBS Hypertrophy Template (ref 06)

For any of the above (except Novice Hypertrophy and Program Builder):
  Train 4-6x/week? → Use the standard (Original) version
  Train 2-3x/week? → Use the Lower Frequency (LF) version
```

## Program Catalog

---

### 1. SBS Strength Program

- **Duration**: 21 weeks (3 × 7-week blocks)
- **Goal**: Strength — peaks to 95% TM singles in week 20
- **Level**: Intermediate+
- **Autoregulation**: Set threshold (→ `references/04-autoregulation-set-threshold.md`)
- **Frequency tabs**: 2x–6x per week

**Building blocks to read**:
- `references/01-training-max-system.md` — TM, working weight, single @8
- `references/02-periodization-structure.md` — Block structure, deloads
- `references/03-exercise-framework.md` — Exercise categories, upper back
- `references/04-autoregulation-set-threshold.md` — Progression method
- `references/07-intensity-tables.md` — Strength intensity tables, rep targets, RIR cutoffs

**Defaults**:
- Main lifts: Squat, Bench Press, Deadlift, OHP
- Auxiliaries: Front Squat, Paused Squat, Close Grip Bench, Incline Press, Sumo Deadlift, Push Press
- Lower set threshold: 4 / Upper set threshold: 6
- TM increase: +2% / TM decrease: −5%
- Single @8 percentage: 90%
- Deloads (weeks 7, 14, 21): 4–6 sets at prescribed weight, no RIR cutoff, TM unchanged

---

### 2. SBS Strength Program LF

Identical to program #1 but uses **Lower Frequency** templates (exercises spread across fewer days per week). All parameters, progressions, and tables are the same.

- **Frequency tabs**: 2x–6x (same tabs, but exercises distributed for lower per-muscle frequency)
- **Building blocks**: Same as program #1

---

### 3. SBS Strength Program Last Set RIR

- **Duration**: 21 weeks (3 × 7-week blocks)
- **Goal**: Strength — peaks to 95% TM singles in week 20
- **Level**: Intermediate+
- **Autoregulation**: Last set RIR rating (→ `references/05-autoregulation-last-set-rir.md`)
- **Frequency tabs**: 2x–6x per week

**Building blocks to read**:
- `references/01-training-max-system.md`
- `references/02-periodization-structure.md`
- `references/03-exercise-framework.md`
- `references/05-autoregulation-last-set-rir.md` — Progression method
- `references/07-intensity-tables.md` — Strength intensity tables, rep targets, RIR targets

**Defaults**:
- Main lifts: Squat, Bench Press, Deadlift, OHP
- Auxiliaries: Front Squat, Paused Squat, Close Grip Bench, Incline Press, Sumo Deadlift, Push Press
- Sets per exercise: 5
- TM adjustment scale: −5%, −2%, 0%, +0.5%, +1%, +1.5%, +2%, +3%
- Single @8 percentage: 90%
- Deloads (weeks 7, 14, 21): 5 sets at prescribed weight, no RIR target, TM unchanged

---

### 4. SBS Strength Program Last Set RIR LF

Identical to program #3 but uses **Lower Frequency** templates.

- **Building blocks**: Same as program #3

---

### 5. SBS Strength Program Reps to Failure (RTF)

- **Duration**: 21 weeks (3 × 7-week blocks)
- **Goal**: Strength — peaks to 95% TM singles in week 20
- **Level**: Intermediate+
- **Autoregulation**: Reps to failure on last set (→ `references/06-autoregulation-rtf.md`)
- **Frequency tabs**: 2x–6x per week

**Building blocks to read**:
- `references/01-training-max-system.md`
- `references/02-periodization-structure.md`
- `references/03-exercise-framework.md`
- `references/06-autoregulation-rtf.md` — Progression method (strength variant)
- `references/07-intensity-tables.md` — Strength intensity tables, normal set rep targets, last set RTF targets

**Defaults**:
- Main lifts: Squat, Bench Press, Deadlift, OHP
- Auxiliaries: Front Squat, Paused Squat, Close Grip Bench, Incline Press, Sumo Deadlift, Push Press
- Sets per exercise: 5 (4 normal + 1 to failure)
- TM adjustment scale: −5%, −2%, 0%, +0.5%, +1%, +1.5%, +2%, +3%
- Single @8 percentage: 90%
- Deloads (weeks 7, 14, 21): 5 sets at prescribed weight, no rep target, TM unchanged

---

### 6. SBS Strength Program RTF LF

Identical to program #5 but uses **Lower Frequency** templates.

- **Building blocks**: Same as program #5

---

### 7. SBS Hypertrophy Template

- **Duration**: 21 weeks (3 × 7-week blocks)
- **Goal**: Hypertrophy — max intensity caps at 82.5% TM (no peaking)
- **Level**: Intermediate+
- **Autoregulation**: Reps to failure on last set (→ `references/06-autoregulation-rtf.md`)
- **Frequency tabs**: 2x–6x per week

**Building blocks to read**:
- `references/01-training-max-system.md`
- `references/02-periodization-structure.md`
- `references/03-exercise-framework.md`
- `references/06-autoregulation-rtf.md` — Progression method (hypertrophy variant)
- `references/07-intensity-tables.md` — Hypertrophy intensity tables, normal set rep targets, last set RTF targets

**Unique parameters (differ from strength programs)**:
- Main lifts: Squat, Bench Press, **Block Pulls** (not Deadlift), OHP
- Auxiliaries: Leg Press, Hack Squat, Incline Press, DB Bench, Romanian Deadlift, DB OHP
- Sets per exercise: **4** (3 normal + 1 to failure)
- Max main lift intensity: **82.5%** (vs 95% for strength)
- Auxiliary intensity = main intensity − 5%
- Normal set reps = MROUND(last_set_target × 0.8, 1) — higher reps than strength
- Higher RTF targets (25 reps at 50% down to 1 at 100%)
- TM adjustment scale: −5%, −2%, 0%, +0.5%, +1%, +1.5%, +2%, +3%
- Deloads (weeks 7, 14, 21): **4 sets** at prescribed weight, no rep target, TM unchanged
- Nuckols recommends starting with **conservative TMs** (85–90% of true max)

---

### 8. SBS Hypertrophy Template LF

Identical to program #7 but uses **Lower Frequency** templates.

- **Building blocks**: Same as program #7

---

### 9. SBS Linear Progression (Novice)

- **Duration**: Open-ended (no blocks or periodization)
- **Goal**: Strength for novice/returning lifters
- **Level**: Novice
- **Autoregulation**: Last set RIR (same logic as program #3 but with more aggressive adjustments)
- **Self-contained reference**: `references/08-novice-programs.md`

**Building blocks to read**:
- `references/08-novice-programs.md` — Complete program details
- `references/01-training-max-system.md` — TM basics
- `references/07-intensity-tables.md` — Novice LP tables

**Defaults**:
- Main lifts: Squat, Bench Press, Deadlift, Push Press
- Auxiliaries: Front Squat, Squat, Close Grip Bench, Bench Press, Deadlift, OHP
- Back exercises: Barbell rows, DB rows, Pull-downs
- Sets per exercise: 3
- Fixed intensities: Main 87.5%, Aux1 82.5%, Aux2/Back 75%
- RIR target: 0 (all lifts)
- TM adjustments: −5%, −2%, 0%, +1%, +3%, +5%, +5%, +5% (more aggressive than intermediate)
- Frequency tabs: 3x–6x (no 2x tab)

---

### 10. SBS Linear Progression LF (Novice)

Identical to program #9 but uses **Lower Frequency** templates.

- **Building blocks**: Same as program #9

---

### 11. SBS Novice Hypertrophy

- **Duration**: Open-ended
- **Goal**: Hypertrophy for novices
- **Level**: Novice
- **Autoregulation**: Double/triple progression (sets → reps → load) — **no training max system**
- **Self-contained reference**: `references/08-novice-programs.md`

**Building blocks to read**:
- `references/08-novice-programs.md` — Complete program details

**Unique parameters**:
- No training max system — uses load directly
- Per-exercise rounding increments (default 5)
- Weighted exercises: 3→5 sets, 8→12 reps, then +10% load
- Bodyweight exercises: 3→5 sets, then +1 rep per set
- 22 exercise slots covering all muscle groups
- Frequency tabs: 3x–5x
- Logging: "Were all sets completed successfully?" yes/no

---

### 12. SBS Program Builder

- **Duration**: 21 weeks (default, fully customizable)
- **Goal**: Custom — user-defined
- **Level**: Intermediate+ (assumes familiarity with SBS progressions)
- **Autoregulation**: Mix-and-match from 7 progression schemes
- **Self-contained reference**: `references/09-program-builder.md`

**Building blocks to read**:
- `references/09-program-builder.md` — Complete builder guide
- `references/01-training-max-system.md` — TM basics
- All autoregulation references (04, 05, 06) as needed for chosen progressions
- `references/07-intensity-tables.md` — All tables

**Unique parameters**:
- Up to 40 exercises
- Per-exercise rounding increments
- 7 available progressions: Set Threshold, Last Set RIR, RTF, Hypertrophy RTF, LP, and 5 accessory progressions
- 5 accessory progressions: Rep Increase, Set Increase Then Rep Increase, Classic Overload, Fixed Number of Reps, Set-by-Set/Reverse Pyramid
- Custom deload placement and parameters
- Cut-and-paste program assembly on the Program tab

## Usage Guidelines

1. **Always read referenced building blocks** before answering questions about a specific program
2. When a user asks about a specific program, identify which of the 12 programs applies, then read the listed building blocks
3. For setup questions, reference `01-training-max-system.md` and `03-exercise-framework.md`
4. For "which program should I use?" questions, use the Decision Guide above
5. For numerical details (exact percentages, rep targets), always consult `07-intensity-tables.md`
6. For novice programs, `08-novice-programs.md` is self-contained — start there

## Response Format

Always include attribution:

> **Source**: SBS Program Bundle by Greg Nuckols — [strongerbyscience.com](https://www.strongerbyscience.com/)

## Quick Reference — Key Defaults Across All Programs

| Parameter | Strength (ST/RIR/RTF) | Hypertrophy | Novice LP | Novice Hyp | Builder |
|-----------|----------------------|-------------|-----------|------------|---------|
| Duration | 21 wk (3×7) | 21 wk (3×7) | Open-ended | Open-ended | 21 wk (custom) |
| Blocks | 3 | 3 | None | None | Custom |
| Default sets | 5* | 4 | 3 | 3–5 | Per-lift |
| Max intensity (main) | 95% | 82.5% | 87.5% (fixed) | N/A | Custom |
| Aux intensity offset | −10% vs main | −5% vs main | Varies | N/A | Custom |
| Deload weeks | 7, 14, 21 | 7, 14, 21 | None | None | Custom |
| TM increase range | +0.5% to +3% | +0.5% to +3% | +1% to +5% | N/A (load %) | Per-scheme |
| TM decrease range | −2% to −5% | −2% to −5% | −2% to −5% | N/A | Per-scheme |
| Frequency tabs | 2x–6x | 2x–6x | 3x–6x | 3x–5x | Custom |
| Single @8 | Yes (90%) | Yes (90%) | Yes (90%) | No | Yes (90%) |

*ST uses 4–6 set threshold range; RIR/RTF use fixed 5 sets

---

**Source**: SBS Program Bundle by Greg Nuckols — [strongerbyscience.com](https://www.strongerbyscience.com/)
