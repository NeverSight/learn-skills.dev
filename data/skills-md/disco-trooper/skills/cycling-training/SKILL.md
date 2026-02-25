---
name: cycling-training
description: Cycling training plans, power zones, FTP testing, intervals, and load management.
license: MIT
metadata:
  author: disco-trooper
  version: "1.1.1"
  last_updated: "2026-02-19"
  keywords: cycling, FTP, power zones, intervals, periodization, indoor trainer, Zwift, TrainerRoad, VO2max, threshold, sweet spot, TSS, CTL
---

# Cycling Training Skill

Evidence-based cycling training guidance grounded in peer-reviewed sports science research.

## Quick Reference

### Power Zones (Quick Reference)

| Zone | Name | % FTP | Primary Use |
|------|------|-------|-------------|
| 1 | Active Recovery | <55% | Recovery rides |
| 2 | Endurance | 55-75% | Aerobic base |
| 3 | Tempo | 76-90% | Muscular endurance |
| 4 | Threshold | 91-105% | FTP development |
| 5 | VO2max | 106-120% | Aerobic capacity |
| 6 | Anaerobic | 121-150% | AC intervals |
| 7 | Neuromuscular | Max | Sprints |

*For detailed zone models (Seiler 3-zone, iLevels, HR zones, Training Intensity Distribution), see [zones-and-testing.md](references/zones-and-testing.md)*

### Scripts (Quick Reference)

If this skill is installed locally, set `SKILLS_DIR` to the directory your tool uses for skills.

```bash
# Example only — adjust to your environment:
SKILLS_DIR="<path-to-your-skills-dir>"

python3 "$SKILLS_DIR/cycling-training/scripts/calculate_zones.py" 250 --model coggan
python3 "$SKILLS_DIR/cycling-training/scripts/calculate_zones.py" 250 --model seiler --json
python3 "$SKILLS_DIR/cycling-training/scripts/calculate_tss.py" 250 230 60 --json
python3 "$SKILLS_DIR/cycling-training/scripts/analyze_week.py" 450 65 72 --prev-week-tss 400 --daily-tss 60,80,0,70,90,80,70 --json
```

Test suite (stdlib only):

```bash
python3 -m unittest discover -s "$SKILLS_DIR/cycling-training/scripts/tests" -p 'test_*.py' -v
```

## Companion Skills

### intervals-icu (Data API)

For fetching and updating data from intervals.icu platform, use the `intervals-icu` skill:

```
┌─────────────────┐     fetch data      ┌───────────────────┐
│  intervals-icu  │ ──────────────────► │ cycling-training  │
│   (DATA API)    │                     │    (ANALYSIS)     │
│                 │ ◄────────────────── │                   │
│ • wellness      │   interpret results │ • zone calc       │
│ • activities    │                     │ • periodization   │
│ • power curves  │                     │ • workout design  │
│ • fitness       │                     │ • load management │
└─────────────────┘                     └───────────────────┘
```

**Common workflow:**
1. Fetch data: `$SKILLS_DIR/intervals-icu/scripts/api.sh wellness today`
2. Analyze with this skill (zone calculation, load management)
3. Update: `$SKILLS_DIR/intervals-icu/scripts/api.sh wellness-update today '{"readiness": 4}'`

---

### Indoor Training Essentials

**Critical Setup:**
| Component | Requirement | Why |
|-----------|-------------|-----|
| Fan | Strong airflow at torso (as much as practical) | Better cooling and higher sustainable indoor power |
| Temperature | <20°C (68°F) | Prevents overheating |
| FTP | Test indoors separately | 5-10% lower than outdoor |

**Indoor FTP Adjustment:**
- Use 95% of outdoor FTP OR
- Perform dedicated indoor FTP test (recommended)
- TrainerRoad AI FTP Detection can be a useful estimate; validate with workouts/tests

**ERG vs Slope Mode:**
| Mode | Use When | Benefit |
|------|----------|---------|
| ERG | Structured intervals | Holds exact power target |
| Slope | Race simulation, cadence drills | Natural power fluctuations |

*For complete indoor setup guide, see [indoor-training.md](references/indoor-training.md)*

### Indoor Workout Quick Examples

**Sweet Spot (ERG Mode):**
```
Warm-up: 10 min @ 55% FTP
Main: 2×20 min @ 88-92% FTP (5 min recovery)
Cool-down: 10 min easy
Total: 65 min | TSS: ~70
TrainerRoad: Carson, Geiger
Zwift: SST (Short) or custom
```

**VO2max Intervals (ERG Mode):**
```
Warm-up: 15 min progressive to 75% FTP
Main: 5×4 min @ 108-112% FTP (4 min @ 50% recovery)
Cool-down: 10 min easy
Total: 65 min | TSS: ~85
TrainerRoad: Baird, Spencer
Zwift: The Gorby or custom
```

**Threshold (Slope Mode for pacing practice):**
```
Warm-up: 15 min with 2×1 min @ 100%
Main: 2×15 min @ 95-100% FTP (8 min recovery)
Cool-down: 10 min easy
Total: 70 min | TSS: ~80
TrainerRoad: Kaweah, Darwin
```

### Weekly Training Load Guidelines
| Level | Hours/Week | Weekly TSS | CTL Target |
|-------|------------|------------|------------|
| Recreational | 5-8 | 300-500 | 40-60 |
| Enthusiast | 8-12 | 500-700 | 60-80 |
| Competitive | 12-18 | 700-1000 | 80-100 |
| Elite Amateur | 18-25 | 1000-1400 | 100-130 |
| Professional | 25-35 | 1400-2000+ | 130-160 |

### Key Metrics Formulas
```
TSS = (Duration_sec × NP × IF) / (FTP × 3600) × 100
IF = NP / FTP
VI = NP / AP
CTL = 42-day exponentially weighted average of TSS
ATL = 7-day exponentially weighted average of TSS
TSB = CTL - ATL
ACWR = ATL / CTL (heuristic range often cited: ~0.8-1.3)
```

**ACWR note:** ACWR is widely used, but it is also debated in the literature. Treat it as a heuristic and combine it with context (sleep, illness, soreness, performance trends), not as a single decision signal.

### Race Day TSB Targets
| Event Type | Optimal TSB |
|------------|-------------|
| Training race | -10 to +5 |
| B race | +5 to +15 |
| A race | +15 to +25 |
| Grand Tour stage | +5 to +15 |

## Plan Templates

Ready-to-use training plan templates:

| Template | Use Case | File |
|----------|----------|------|
| 8-Week Base Builder | Building aerobic foundation | [base-8-week.md](assets/base-8-week.md) |
| 16-Week Indoor Season | Winter trainer block (Nov-Feb) | [indoor-season.md](assets/indoor-season.md) |
| 16-Week Outdoor Season | Spring-summer race preparation (Apr-Jul) | [outdoor-season.md](assets/outdoor-season.md) |

### Using Templates

1. Copy template to user's planning location
2. Replace `[YOUR_FTP]` with athlete's current FTP
3. Replace `[YOUR_CTL]` with current CTL
4. Adjust dates and weekly structure
5. Scale TSS targets based on current fitness (×0.8 for less, ×1.2 for more)

---

## Reference Files

Load these based on specific need:

| Topic | File | Load When |
|-------|------|-----------|
| Power zones & FTP testing | [zones-and-testing.md](references/zones-and-testing.md) | Setting zones, FTP tests, CP model |
| Workout library | [workouts.md](references/workouts.md) | Prescribing specific intervals |
| Periodization | [periodization.md](references/periodization.md) | Planning phases, blocks, mesocycles |
| Indoor training | [indoor-training.md](references/indoor-training.md) | Trainer setup, heat, Zwift/TrainerRoad |
| Outdoor training | [outdoor-training.md](references/outdoor-training.md) | Outdoor execution, terrain, groups, safety |
| Nutrition & recovery | [nutrition-recovery.md](references/nutrition-recovery.md) | Fueling, supplements, sleep, recovery |
| Physiology | [physiology.md](references/physiology.md) | VO2max, lactate, CP, efficiency |
| Strength training | [strength.md](references/strength.md) | Gym work integration for cyclists |
| Special populations | [special-populations.md](references/special-populations.md) | Masters, women, beginners, time-crunched |
| Analytics | [analytics.md](references/analytics.md) | Metrics, training load, data analysis |
| Training platforms | [platforms.md](references/platforms.md) | TrainerRoad, Zwift, intervals.icu, WKO5 comparison |
| Environmental | [environmental.md](references/environmental.md) | Heat acclimation, altitude training |
| Psychology | [psychology.md](references/psychology.md) | Motivation, mental training, indoor strategies |
| Bike fit & position | [bike-fit.md](references/bike-fit.md) | Position setup, indoor adjustments, pain issues |
| Injuries & prevention | [injuries.md](references/injuries.md) | Pain diagnosis, prevention, return protocols |
| Cardiovascular risks | [injuries.md#cardiovascular-risks](references/injuries.md#cardiovascular-risks-of-endurance-training) | High-volume training concerns, screening |
| Racing tactics | [racing-tactics.md](references/racing-tactics.md) | Race strategy, pacing, drafting, criteriums |
| Equipment & gear | [equipment.md](references/equipment.md) | Trainer, fan, power meter recommendations |
| Quick reference | [quick-reference.md](references/quick-reference.md) | Common scenarios, metrics, race TSB targets |

## Core Workflows

### 1. Creating a Training Plan

```
1. ASSESS current state
   - Recent FTP test (within 4-6 weeks)
   - Current CTL and training history
   - Power duration curve / phenotype
   - Available training time
   - Health/injury status

2. DEFINE goals
   - Target event(s) with dates
   - Performance goals (power targets, placing)
   - Priority (A/B/C races)

3. SELECT periodization model
   - Block: For experienced cyclists, 1-3 peak events
   - Traditional: For beginners, year-round racing
   - Reverse: For masters, late-season peaks, indoor season

4. MAP phases backward from A event
   - Race/Peak: 1-2 weeks (taper)
   - Build: 6-8 weeks (race-specific intensity)
   - Base: 8-12 weeks (volume, aerobic development)

5. STRUCTURE mesocycles (3-4 weeks each)
   - 3:1 or 2:1 load:recovery ratio
   - Progressive overload within mesocycle
   - Deload week at end

6. PLAN microcycles (weekly)
   - Key workouts placed optimally
   - Recovery days after hard sessions
   - Long ride placement (weekend typically)

7. SET targets
   - Weekly TSS targets
   - CTL progression (3-7 pts/week max)
   - Specific workout targets
```

### 2. Analyzing Training Data

```
1. SESSION level
   - Compare NP/IF to prescription
   - Time in target zones
   - HR:power decoupling (<5% = good aerobic fitness)
   - Variability Index (race: 1.0-1.05, crit: 1.1+)

2. WEEKLY level
   - Total TSS vs target
   - Intensity distribution (TID)
   - ACWR (heuristic; avoid sharp spikes)

3. BLOCK/PHASE level
   - CTL trend
   - FTP progression
   - Power duration curve changes
   - Identify limiters

4. WARNING signs
   - HR elevated for given power
   - Performance plateau/decline
   - Elevated resting HR
   - Sleep disturbance
   - Mood changes
```

### 3. Prescribing Workouts

```
1. IDENTIFY training goal
   - Aerobic base → Endurance, Tempo
   - Threshold development → Sweet Spot, Threshold
   - VO2max → Short/Long VO2max intervals
   - Anaerobic → AC intervals, sprints
   - Race-specific → Simulation workouts

2. SELECT workout type from references/workouts.md

3. ADJUST for athlete
   - Scale duration/reps for fitness level
   - Consider current fatigue (TSB)
   - Account for weekly context

4. PROVIDE execution guidance
   - Warm-up protocol
   - Target power/HR
   - Pacing strategy
   - Recovery between intervals
   - Cool-down
```

## Key Evidence-Based Principles

### Polarized Training (Seiler Research)
- 80% of training time below LT1 (easy)
- <5% between LT1-LT2 (minimize "grey zone")
- 15-20% above LT2 (hard intervals)
- Superior to threshold-heavy approaches for trained athletes
- Exception: Time-crunched athletes may benefit from more sweet spot

### Progressive Overload
- CTL increase: 3-7 points/week (max 10 aggressive)
- Volume increase: 5-10% per week maximum
- Ramp rate = (CTL_target - CTL_current) / weeks_available
- Always follow 2-3 hard weeks with recovery week

### Recovery Integration
- Deload every 3-4 weeks (40-60% volume cut)
- Maintain some intensity during deloads
- Sleep: 8-9 hours optimal for adaptation
- Nutrition timing: Protein within 2h, carbs for glycogen

### Supercompensation Timing
| Adaptation | Recovery Time |
|------------|---------------|
| Neuromuscular | 24-72 hours |
| Glycogen stores | 24-48 hours |
| Aerobic enzymes | 7-14 days |
| Structural (muscle) | 3-6 weeks |

### Indoor vs Outdoor Training
- Power typically 5-10% lower indoors
- RPE higher for same power output
- Cooling critical: Fan essential, room temp <20°C
- Heat stress can be used for heat adaptation
- ERG mode for structured intervals
- Slope mode for race simulation / pacing practice

### Overtraining Prevention
Monitor daily:
- Morning resting HR (+5 bpm = warning)
- HRV trend (decreasing = accumulating fatigue)
- Sleep quality
- Subjective wellness (1-10 scale)

Red flags:
- Performance decline despite adequate training
- Persistent fatigue >2 weeks
- Illness frequency increase
- Mood disturbances

### Cardiovascular Risks (High Volume)

**Medical disclaimer:** Educational only — not medical advice. If you have symptoms or risk factors, seek medical evaluation.

Red flags to take seriously:
- Palpitations, unusual dyspnea, syncope, chest pain

→ See [injuries.md](references/injuries.md#cardiovascular-risks-of-endurance-training) for details and sources

## Workflow Guides

### Plan Type Decision Tree

```
Athlete's primary goal?
├── Build aerobic base
│   └── Use: Base Building workflow → base-8-week.md template
├── Increase FTP/threshold
│   └── Current CTL?
│       ├── <60: Build base first (4-6 weeks)
│       └── ≥60: Use Build workflow → FTP focus
├── Prepare for specific event
│   └── Weeks until event?
│       ├── >12 weeks: Full periodization (base → build → peak)
│       ├── 8-12 weeks: Build → peak
│       └── <8 weeks: Maintenance + race specificity
└── Indoor winter training
    └── Use: indoor-season.md template
```

### Intensity Distribution Decision

```
Available training hours/week?
├── <6 hours
│   └── Polarized approach: 80% Z1-2, 20% Z5+
│       (Skip Z3-4, maximize recovery between intensity)
├── 6-10 hours
│   └── Pyramidal approach: 75% Z1-2, 15% Z3-4, 10% Z5+
└── >10 hours
    └── Traditional periodization or pyramidal
        (More flexibility in distribution)
```

### Training Analysis Workflow

When analyzing completed training data:

1. **Weekly Review**
   - Compare actual vs planned TSS
   - Check intensity distribution (time in zones)
   - Review key workout execution (hit targets?)
   - Note subjective feedback (RPE, fatigue, mood)

2. **Performance Trends**
   - Track FTP progression (eFTP from intervals.icu)
   - Monitor Efficiency Factor (NP/HR) trend
   - Check power curve for improvements
   - Compare HR:power decoupling on endurance rides

3. **Load Management**
   - Calculate ACWR (heuristic; watch for spikes)
   - Monitor CTL ramp rate (<7 pts/week)
   - Watch for excessive negative TSB (<-30)

4. **Red Flags to Address**
   - Declining power at same HR
   - Increasing RPE for same workouts
   - Poor sleep/recovery scores
   - Missed workouts pattern

→ For detailed metrics, see [analytics.md](references/analytics.md)

## Common Scenarios

Quick answers with deep-dive links: See [quick-reference.md](references/quick-reference.md)
