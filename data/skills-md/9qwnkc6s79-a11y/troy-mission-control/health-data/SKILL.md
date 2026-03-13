---
name: health-data
description: Real-time health data integration from iPhone HealthKit. Use when Codex needs to query or analyze health metrics like weight, steps, workouts, calories, sleep, or heart rate. Supports conversational queries like "What's my weight trend this week?", "How many steps today?", "Did I work out yesterday?", trend analysis, coaching insights, and integration with nutrition tracking. Data synced via iOS Shortcuts from Apple Health app.
---

# Health Data Integration

Real-time access to iPhone health data through OpenClaw. Query your health metrics conversationally and get coaching insights.

## How It Works

1. **iOS Shortcuts** exports health data from Apple Health app
2. **Auto-sync** via iCloud to OpenClaw workspace  
3. **Query interface** allows natural language health questions
4. **Trend analysis** provides coaching insights over time

## Quick Start

**Ask conversational questions:**
```
"What's my weight today?"
"How many steps have I taken?"
"What workouts did I do this week?"
"What's my weight trend this week?"
"Any concerning health patterns?"
```

**Get current data:**
```
python scripts/query_health.py --current
```

**Generate insights:**
```
python scripts/query_health.py --insights --days 7
```

## Core Capabilities

### 1. Real-time Health Queries
- Current weight, steps, calories, heart rate
- Today's workouts and activity summary
- Sleep data and recovery metrics
- Instant answers to health questions

### 2. Trend Analysis
- 7-day, 30-day, 90-day health patterns  
- Weight loss/gain trends and rates
- Workout frequency and consistency
- Activity level changes over time

### 3. Coaching Insights
- Personalized recommendations based on data
- Health goal progress tracking
- Warning alerts for concerning patterns
- Actionable advice for improvement

### 4. Nutrition Integration
- Links health metrics with food tracking
- Calorie burn vs intake analysis
- Body composition trends
- Macro nutrient recommendations

## Data Sources

All data flows through Apple Health as the central hub:

- **Weight:** RENPHO scale → Apple Health
- **Workouts:** Fitbod app → Apple Health  
- **Steps/Activity:** iPhone + Apple Watch → Apple Health
- **Heart Rate:** Apple Watch → Apple Health
- **Sleep:** Apple Watch → Apple Health
- **Nutrition:** MyFitnessPal/other apps → Apple Health

## Query Examples

**Current Metrics:**
- "What's my weight today?"
- "How many steps have I taken today?"
- "What's my current heart rate?"
- "Did I work out today?"

**Historical Trends:**
- "What's my weight trend this week?"
- "Am I meeting my step goals consistently?"
- "How many workouts did I do this month?"
- "What's my average daily calorie burn?"

**Health Insights:**
- "Any health concerns I should know about?"
- "What should I focus on this week?"
- "How's my fitness progress?"
- "Am I losing weight too fast?"

## Resources

### scripts/
- `query_health.py` - Main query interface for conversational health questions
- `sync_health_data.py` - Sync latest data from iOS Shortcuts export
- `generate_insights.py` - Analyze trends and generate coaching recommendations

### references/
- `setup_guide.md` - Complete iOS Shortcuts setup instructions
- `healthkit_schema.md` - Apple Health data structure and available metrics
- `coaching_algorithms.md` - How health insights and recommendations are generated

---

**Setup Required:** The health sync system needs iOS Shortcuts configured. See references/setup_guide.md for 15-minute setup process.