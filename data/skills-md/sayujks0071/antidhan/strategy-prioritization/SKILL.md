---
name: strategy-prioritization
description: Analyze, rank, and prioritize trading strategies using multi-factor scoring. Use when creating prioritization plans, ranking strategies, analyzing strategy portfolios, comparing strategy performance, or making strategy selection decisions.
---

# Strategy Prioritization

## Quick Start

When prioritizing strategies:

1. Inventory all available strategies across codebase
2. Score each strategy on 4 factors (Performance, Risk, Operations, Business)
3. Rank strategies by composite score
4. Generate deployment recommendations
5. Identify gaps blocking promotion

## Scoring Framework

### Four-Factor Scoring (1-5 scale, equal weights)

**Composite Score = (Performance + Risk + Ops + Business) / 4**

#### 1. Performance (25%)
- **5**: Strong metrics (Sharpe > 2.0, Win Rate > 70%, PF > 2.5)
- **4**: Good metrics (Sharpe > 1.5, Win Rate > 65%, PF > 2.0)
- **3**: Moderate or limited data
- **2**: Weak metrics or no recent backtests
- **1**: No performance data

#### 2. Risk Readiness (25%)
- **5**: Comprehensive controls (stops, sizing, limits, correlation)
- **4**: Good controls (stops, sizing, basic limits)
- **3**: Basic controls (stops only)
- **2**: Minimal controls
- **1**: No risk management

#### 3. Operational Readiness (25%)
- **5**: Fully configured, tested, documented, monitored
- **4**: Configured and tested, minor doc gaps
- **3**: Basic config, needs testing/docs
- **2**: Code exists, not configured
- **1**: Experimental/incomplete

#### 4. Business Importance (25%)
- **5**: Explicitly recommended, high priority, proven
- **4**: Important, good business case
- **3**: Moderate value
- **2**: Low priority/experimental
- **1**: Example/research only

## Prioritization Process

### Step 1: Strategy Discovery

```bash
# Find all strategies
find openalgo/strategies/scripts -name "*.py" -type f
find openalgo_backup_*/strategies/scripts -name "*.py" -type f  
find AITRAPP/AITRAPP/packages/core/strategies -name "*.py" -type f

# Check documentation
grep -r "strategy" *.md | grep -i "priorit\|rank\|recommend"
```

### Step 2: Data Collection

For each strategy, gather:

**Performance Data:**
- Backtest results from `openalgo/strategies/backtest_results/`
- Metrics from `ALL_STRATEGIES_COMPARISON.md`
- Ranking reports and CSV files
- AITRAPP backtest engine results

**Risk Assessment:**
```python
# Check for risk controls in code
grep -r "stop_loss\|max_drawdown\|position_size\|risk_per_trade" strategy_file.py
grep -r "daily_loss_limit\|weekly_loss_limit\|correlation" strategy_file.py
```

**Operational Check:**
- Config files: `AITRAPP/AITRAPP/configs/app.yaml`
- Deployment scripts: `openalgo/strategies/scripts/`
- Documentation: Strategy `.md` files
- Monitoring: Log files, status endpoints

**Business Value:**
- Check `STRATEGY_PRIORITIZATION_REPORT.md`
- Review `ALL_STRATEGIES_COMPARISON.md` recommendations
- Look for explicit deployment recommendations

### Step 3: Scoring

```python
def score_strategy(strategy_name, performance_data, risk_data, ops_data, business_data):
    """Score strategy on 4 factors"""
    perf_score = score_performance(performance_data)  # 1-5
    risk_score = score_risk(risk_data)  # 1-5
    ops_score = score_operations(ops_data)  # 1-5
    biz_score = score_business(business_data)  # 1-5
    
    composite = (perf_score + risk_score + ops_score + biz_score) / 4.0
    
    return {
        'name': strategy_name,
        'performance': perf_score,
        'risk': risk_score,
        'operations': ops_score,
        'business': biz_score,
        'composite': composite,
        'gaps': identify_gaps(perf_score, risk_score, ops_score, biz_score)
    }
```

### Step 4: Ranking and Categorization

```python
def categorize_strategy(composite_score):
    """Categorize by action needed"""
    if composite_score >= 4.0:
        return "Deploy", "Ready for live trading"
    elif composite_score >= 3.0:
        return "Paper Trade", "Needs validation"
    elif composite_score >= 2.5:
        return "Optimize", "Needs improvements"
    else:
        return "Hold", "Experimental or incomplete"
```

### Step 5: Generate Report

Create prioritization report with:
- Ranked table (sorted by composite score)
- Detailed analysis per strategy
- Gap identification
- Deployment roadmap
- Action items

## Key Metrics Reference

### Performance Metrics

**Sharpe Ratio:**
- Excellent: > 2.0
- Good: 1.5 - 2.0
- Acceptable: 1.0 - 1.5
- Poor: < 1.0

**Win Rate:**
- Excellent: > 70%
- Good: 60-70%
- Acceptable: 50-60%
- Poor: < 50%

**Profit Factor:**
- Excellent: > 2.5
- Good: 2.0 - 2.5
- Acceptable: 1.5 - 2.0
- Poor: < 1.5

**Max Drawdown:**
- Excellent: < 10%
- Good: 10-15%
- Acceptable: 15-20%
- Poor: > 20%

### Risk Controls Checklist

- [ ] Stop loss implemented
- [ ] Position sizing based on risk
- [ ] Daily loss limit
- [ ] Weekly loss limit
- [ ] Max drawdown protection
- [ ] Correlation management
- [ ] Max positions limit
- [ ] Volatility-based sizing

### Operational Checklist

- [ ] Configuration file exists
- [ ] Parameters documented
- [ ] Deployment script available
- [ ] Logging implemented
- [ ] Monitoring integrated
- [ ] Error handling robust
- [ ] Documentation complete
- [ ] Tested in sandbox

## Integration Points

### With Backtesting
- Use backtest results to score performance
- Reference `backtesting-analysis` skill for metrics
- Check `openalgo/strategies/backtest_results/` for data

### With Strategy Management
- Coordinate deployment with `strategy-manager` subagent
- Check current running strategies before prioritizing
- Verify strategy status via web UI

### With Risk Management
- Align with `risk-management` skill requirements
- Verify risk controls meet standards
- Check portfolio-level constraints

## Common Patterns

### High-Priority Strategies
Look for:
- Documented backtests with strong metrics
- Comprehensive risk controls
- Fully configured and tested
- Explicitly recommended in docs

### Strategies Needing Work
Identify:
- Missing backtest data → Run backtests
- Weak risk controls → Add risk management
- Configuration gaps → Create configs
- Documentation gaps → Write docs

### Archived Strategies
- Check `openalgo_backup_*/strategies/` for high-performing archived strategies
- Consider porting to current location if score is high
- Verify code compatibility before promotion

## Report Template

```markdown
# Strategy Prioritization Plan - [Date]

## Executive Summary
- Total strategies: X
- Top 3: [List]
- Ready to deploy: X
- Need work: X

## Ranked Strategies

| Rank | Strategy | Perf | Risk | Ops | Biz | Score | Action | Location |
|------|----------|------|------|-----|-----|-------|--------|----------|
| 1 | Strategy A | 5 | 5 | 4 | 5 | 4.75 | Deploy | openalgo/strategies/scripts/ |

## Detailed Analysis

### Strategy A
**Performance (5/5)**: [Details]
**Risk (5/5)**: [Details]
**Operations (4/5)**: [Details]
**Business (5/5)**: [Details]
**Gaps**: None
**Next Steps**: Deploy to live trading

## Gaps Blocking Promotion
- Strategy X: Missing backtest data
- Strategy Y: No risk controls

## Deployment Roadmap
1. Week 1: Deploy top 3 strategies
2. Week 2: Paper trade next tier
3. Month 1: Optimize remaining strategies
```

## Best Practices

1. **Be Conservative**: When data is missing, score low and mark as gap
2. **Prioritize Data**: Strategies with documented performance rank higher
3. **Actionable Output**: Provide specific next steps, not just scores
4. **Regular Updates**: Re-prioritize as strategies are tested/deployed
5. **Document Gaps**: Clearly identify blockers to enable promotion
6. **Consider Context**: Market conditions and instrument types matter

## Troubleshooting

### Missing Performance Data
- Run backtests using `backtesting-analysis` skill
- Check archived backtest results
- Look for comparison reports

### Incomplete Risk Controls
- Reference `risk-management` skill for requirements
- Add missing controls before promotion
- Test risk limits in sandbox

### Configuration Issues
- Check existing configs in `AITRAPP/AITRAPP/configs/`
- Create config files following patterns
- Verify parameters are documented

## Related Resources

- Subagent: `strategy-prioritization-planner` for detailed planning
- Skill: `backtesting-analysis` for performance metrics
- Skill: `risk-management` for risk control standards
- Skill: `trading-strategy-development` for strategy structure
- Reports: `STRATEGY_PRIORITIZATION_REPORT.md`, `ALL_STRATEGIES_COMPARISON.md`
