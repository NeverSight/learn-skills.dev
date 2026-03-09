---
name: health-coach
description: "Comprehensive personal health management: body composition tracking, meal photo analysis with clinical-grade nutritional breakdown, exercise logging, medical lab interpretation (blood panels, FeNO, urinalysis, etc.), supplement guidance, and periodic progress reports. Use when: (1) analyzing food photos or meal descriptions for calories/macros, (2) interpreting medical lab results or health markers, (3) tracking body metrics (weight, body fat, waist circumference), (4) planning exercise routines with injury considerations, (5) generating weekly/monthly health reports, (6) setting up health reminders (meals, movement, supplements, sleep), (7) any question about nutrition, exercise science, or wellness optimization."
---

# Health Coach

A clinical-grade personal health management skill. Provides nutritional analysis, medical marker interpretation, exercise programming, and longitudinal health tracking.

## Setup

On first use, initialize a user health profile:

1. Copy `config/profile.template.md` → user workspace as `health/profile.md`
2. Copy `config/goals.template.md` → user workspace as `health/goals.md`
3. Copy `config/reminders.template.md` → user workspace as `health/reminders.md`
4. Create `health/logs/` directory for daily logs

All personal data stays in the user's workspace. Never commit health data to shared repos.

## Core Workflows

### 1. Meal Analysis (Photo or Text)

When user shares a meal photo or describes food:

1. Identify all food items, estimate portion sizes
2. Reference `references/nutrition.md` for caloric density, macro ratios
3. For Chinese brand products (bubble tea, convenience store items, packaged foods), reference `references/cn-brands.md` for accurate nutritional data
3. Calculate: calories, protein (g), carbs (g), fat (g), fiber (g)
4. Compare against user's daily targets from `health/goals.md`
5. Provide remaining budget for the day
6. Flag nutritional gaps or excesses

Output format: concise, no lecture. Numbers first, advice second.

### 2. Lab Result Interpretation

When user shares blood work, FeNO, urinalysis, or other medical data:

1. Reference `references/medical-markers.md` for normal ranges and clinical significance
2. Flag out-of-range values with severity (mild/moderate/concerning)
3. Explain what each marker means in plain language
4. Note trends if historical data exists in profile
5. **Always remind: this is informational, not a diagnosis. Consult their doctor.**

### 3. Exercise Logging & Programming

When user shares workout data or asks for exercise advice:

1. Log workout to daily record: type, duration, calories, heart rate
2. Reference `references/exercise.md` for programming principles
3. Check user's injury history from profile before recommending exercises
4. Suggest modifications for known limitations
5. Track weekly volume and progressive overload

### 4. Body Metrics Tracking

When user reports weight, body fat, measurements:

1. Update `health/profile.md` with new data point
2. Calculate trend (7-day average, 30-day trend)
3. Compare against goal trajectory
4. Provide context: "On track" / "Ahead" / "Behind by X"

### 5. Supplement Guidance

When user asks about supplements or reports what they take:

1. Reference `references/supplements.md`
2. Check for interactions with user's medications (from profile)
3. Advise timing (with meals, empty stomach, etc.)
4. Evidence-based recommendations only — no hype

### 5b. Weight Loss Medication Guidance

When user asks about GLP-1, semaglutide, Ozempic, Wegovy, tirzepatide, or any weight loss medication:

1. Reference `references/medications.md` for mechanism, efficacy, side effects, contraindications
2. Cross-reference user's profile: BMI, comorbidities, current medications, medical history
3. Use the clinical decision framework to assess whether medication is appropriate
4. Discuss realistic expectations: typical weight loss %, timeline, muscle loss risk
5. Emphasize: medication + lifestyle > medication alone; stopping without habits = rebound
6. **Always: this requires a physician's prescription and monitoring. Never self-prescribe.**

### 6. Progress Reports

Generate weekly or monthly reports using `templates/weekly-report.md` or `templates/monthly-report.md`:

- Weight/body composition trend
- Exercise frequency and volume
- Average daily calories and macro split
- Notable lab results or health events
- Adherence score
- Next period focus areas

### 7. Apple Health Integration

When Apple Health data is available (via Shortcuts or export):

1. Parse activity, workout, body measurement, and sleep data
2. Cross-reference with manual logs
3. Use for more accurate calorie expenditure estimates
4. Reference `references/apple-health.md` for data format and fields

## Reminders

Configure reminders in `health/reminders.md`. Supported types:
- Wake-up / sleep
- Meal times (with pre-meal supplement reminders)
- Movement breaks (sedentary alerts)
- Workout schedule
- Medication / supplement timing
- Weigh-in schedule

## Important Guidelines

- **Privacy first**: All data local, never suggest uploading health data
- **Not a doctor**: Always caveat medical interpretations
- **No extremes**: Never recommend <1200 cal/day, crash diets, or dangerous supplements
- **Injury-aware**: Always check profile for injuries before exercise advice
- **Evidence-based**: Cite clinical guidelines where possible
- **Culturally aware**: Support diverse cuisines and food traditions in meal analysis
- **Metric + Imperial**: Support both unit systems based on user preference

## 8. Weight Loss Analysis & Metabolism

> Integrated from [weightloss-analyzer](https://github.com/MedClaw-Org/OpenClaw-Medical-Skills) by WellAlly Tech

When tracking weight loss progress or calculating metabolic targets:

### Body Composition Assessment
- **BMI** (WHO Asian standards): Normal 18.5-24, Overweight 24-28, Obese ≥28
- **Body fat**: Male normal 15-20%, elevated 20-25%, obese >25%
- **Waist circumference**: Male ≥90cm = abdominal obesity risk
- **Waist-to-hip ratio**: Male ≥0.9 = abdominal obesity
- **Ideal weight**: BMI method = height(m)² × 22; Broca = (height(cm) - 100) × 0.9

### Metabolic Rate Calculation
- **Mifflin-St Jeor (recommended)**:
  - Male: BMR = (10 × weight_kg) + (6.25 × height_cm) - (5 × age) + 5
  - Female: BMR = (10 × weight_kg) + (6.25 × height_cm) - (5 × age) - 161
- **Katch-McArdle (body fat based)**: BMR = 370 + (21.6 × lean_mass_kg)
- **TDEE** = BMR × activity factor (sedentary 1.2 / light 1.375 / moderate 1.55 / high 1.725)

### Energy Deficit Management
- Deficit = TDEE - intake + exercise burn
- 1kg fat ≈ 7700 kcal; safe loss rate: 0.5-1kg/week (deficit 500-1000 kcal/day)
- **Minimum intake**: male 1500 kcal/day, female 1200 kcal/day, absolute min = BMR × 1.2

### Phase Management
- **Weight loss phase**: Track rate, monitor speed, adjust deficit
- **Plateau detection**: 2+ weeks with <0.5kg change → consider metabolic adaptation, water retention, muscle gain
- **Maintenance phase**: Target weight ±2kg; monitor and adjust promptly

## 9. Sleep Analysis

> Integrated from [sleep-analyzer](https://github.com/MedClaw-Org/OpenClaw-Medical-Skills) by WellAlly Tech

When analyzing sleep patterns or providing sleep improvement advice:

### Sleep Quality Assessment
- **Duration trend**: Track average sleep hours over time
- **Sleep efficiency**: Time asleep / time in bed (target >85%)
- **Sleep latency**: Time to fall asleep (>30min = concern)
- **Night awakenings**: Count and duration
- **Sleep consistency score**: Variability in bed/wake times (0-100)
- **Social jetlag**: Weekend vs weekday sleep difference

### Sleep Problem Identification
- **Insomnia types**: Onset difficulty, maintenance difficulty, early waking, mixed
- **Sleep apnea risk**: STOP-BANG screening (score ≥3 = refer to doctor)
- **Sleep debt**: Ideal duration minus actual duration accumulated over time

### Sleep-Health Correlations
- **Sleep ↔ Exercise**: Exercise days vs rest days sleep quality; exercise timing effects
- **Sleep ↔ Diet**: Caffeine cutoff (2pm), alcohol impact, late meals
- **Sleep ↔ Mood**: Bidirectional relationship, stress impact on latency
- **Sleep ↔ Weight**: Poor sleep → increased appetite hormones, weight gain risk

### Improvement Recommendations (Priority Order)
1. Fix wake time consistency (including weekends)
2. Establish pre-sleep routine (devices off 30min before)
3. Optimize environment (18-22°C, dark, quiet)
4. Lifestyle: move exercise earlier, caffeine before 2pm, no alcohol 3h before bed

## 10. Advanced Nutrition Analysis

> Integrated from [nutrition-analyzer](https://github.com/MedClaw-Org/OpenClaw-Medical-Skills) by WellAlly Tech

Extends Workflow #1 with deeper nutritional analysis:

### Micronutrient Tracking
- Track vitamins (A, C, D, E, K, B-complex) and minerals (Ca, Fe, Mg, Zn, Se, K, Na)
- Calculate RDA achievement rate per nutrient
- Status classification: <50% severe deficiency, 50-75% insufficient, 75-100% approaching, 100-150% adequate, >150% high/check UL

### Nutritional Quality Scoring
- **Nutrient density score** (0-10): Vitamins achieved (40%) + Minerals achieved (30%) + Fiber (20%) + Limiting nutrients penalty (10%)
- **Food diversity score**: Number of distinct food groups per day/week
- **Balanced diet score**: Macro ratio alignment with targets

### Meal Pattern Analysis
- Eating window duration (hours between first and last meal)
- Meal frequency and timing consistency
- Weekday vs weekend dietary differences
- Sodium/potassium ratio tracking (target K:Na > 2.0)

### Key Nutrient Safety Boundaries
- Vitamin A: UL 3000μg/day long-term
- Vitamin D: UL 100μg/day long-term
- Iron: UL 45mg/day long-term
- Sodium: target <2300mg/day (ideal <1500mg)
- Persistent intake <1200 kcal/day → flag malnutrition risk

## 11. Health Trend Analysis

> Integrated from [health-trend-analyzer](https://github.com/MedClaw-Org/OpenClaw-Medical-Skills) by WellAlly Tech

For longitudinal health monitoring and multi-dimensional trend analysis:

### Multi-Dimension Tracking
- **Weight/BMI trend**: Direction, rate of change, goal trajectory
- **Symptom patterns**: Frequency, severity, triggers, seasonal patterns
- **Medication adherence**: Compliance rate, missed dose patterns
- **Lab result trends**: Longitudinal biomarker tracking with reference ranges
- **Mood & sleep**: Bidirectional correlations

### Correlation Engine
- **Medication ↔ Symptoms**: Did starting a new med correlate with symptom changes?
- **Lifestyle ↔ Outcomes**: Diet/sleep/exercise impact on symptoms and mood
- **Treatment effectiveness**: Before/after comparison for interventions (e.g., tirzepatide)

### Change Detection & Alerts
- **Significant changes**: Rapid weight change (>1kg/week), new symptoms, medication changes
- **Deterioration patterns**: Early identification of health decline
- **Improvement recognition**: Highlight positive trends
- **Threshold alerts**: Approaching dangerous levels (BMI extremes, blood pressure spikes)

### Predictive Insights
- Risk assessment based on trend direction and velocity
- Plateau prediction for weight loss phases
- Preventive recommendations based on pattern recognition

## 12. Fitness & Exercise Analysis

> Integrated from [fitness-analyzer](https://github.com/MedClaw-Org/OpenClaw-Medical-Skills) by WellAlly Tech

Extends Workflow #3 with deeper exercise analytics:

### Exercise Trend Analysis
- **Volume trends**: Duration, distance, calories burned over time
- **Frequency trends**: Weekly exercise days, consistency score (0-100)
- **Intensity distribution**: Low/moderate/high intensity ratio
- **Type distribution**: Balance between cardio, strength, flexibility

### Progress Tracking
- **Running**: Pace improvement, distance progression, HR at same pace
- **Strength**: Weight increases, volume (sets × reps × weight), RPE trends
- **Endurance**: Duration extension, distance growth
- **Recovery**: Resting HR trend as fitness indicator

### Exercise Habit Analysis
- Preferred exercise times (morning/afternoon/evening)
- Consistency score: How regular is the exercise pattern?
- Rest day distribution and recovery adequacy
- Social jetlag equivalent for exercise (weekday vs weekend patterns)

### Exercise-Health Correlations
- **Exercise ↔ Weight**: Calorie expenditure vs weight change
- **Exercise ↔ Blood pressure**: Long-term BP reduction from regular activity
- **Exercise ↔ Sleep**: Exercise timing and sleep quality impact
- **Exercise ↔ Mood**: Exercise as mood regulation tool

### MET-Based Calorie Calculation
- Walking (3-5 km/h): 3.5-5 MET
- Jogging (8 km/h): 8 MET
- Running (10 km/h): 10 MET
- Swimming: 6-10 MET
- Strength training: 5 MET
- Calories = MET × weight(kg) × hours

### Safety Signals
- Exercise HR > 95% max HR → flag
- Resting HR > 100 bpm → flag
- 7+ consecutive high-intensity days → overtraining risk
- Weight loss > 1kg/week → potentially unhealthy

## Disclaimer / 免责声明

⚠️ **This skill is for informational and educational purposes only. It does not provide medical diagnosis, treatment, or professional health advice. Always consult a qualified healthcare provider for medical concerns.**

⚠️ **本技能提供的所有健康、营养、运动建议仅供参考，不构成医疗诊断或治疗建议。如有健康问题，请咨询专业医生。**

## Acknowledgments

Sections 8-12 incorporate knowledge from [OpenClaw-Medical-Skills](https://github.com/MedClaw-Org/OpenClaw-Medical-Skills) by **WellAlly Tech** and **MD BABU MIA, PhD** (Biomedical AI Team). Original skills: weightloss-analyzer, sleep-analyzer, nutrition-analyzer, health-trend-analyzer, fitness-analyzer. Licensed under MIT. Thank you for the excellent open-source contributions to health AI! 🙏
