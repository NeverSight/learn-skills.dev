---
name: app-store-aso
description: Generate optimized Apple App Store metadata recommendations with ASO best practices. Use this skill when analyzing app listings, optimizing metadata (title, subtitle, description, keywords), performing competitive analysis, or validating App Store listing requirements. Triggers on queries about App Store optimization, metadata review, or screenshot strategy.
---

# Apple App Store ASO Optimization

## Overview

This skill enables comprehensive Apple App Store Optimization (ASO) analysis and metadata generation. Analyze existing app listings, generate optimized metadata following Apple's guidelines and character limits, provide competitive insights, and recommend screenshot storyboard strategies.

## Core Workflow

When a user requests ASO optimization or metadata review:

1. **Analyze the App Context**
   - Understand the app's purpose, features, and target audience
   - Identify unique value propositions and competitive differentiators
   - Note any changes or updates the user mentions

2. **Load ASO Knowledge Base**
   - Reference `references/aso_learnings.md` for comprehensive ASO best practices
   - Apply competitive analysis strategies
   - Use proven optimization patterns

3. **Generate Optimized Metadata**
   - Create optimized app name, subtitle, and promotional text
   - Write compelling description with keyword optimization
   - Generate keyword list with strategic placement
   - Ensure all metadata follows Apple's character limits

4. **Validate Character Counts**
   - Use `scripts/validate_metadata.py` to verify all metadata meets Apple's requirements
   - Display validation results with character counts and limit compliance
   - Flag any violations with specific corrections needed

5. **Provide Screenshot Strategy**
   - Recommend screenshot storyboard sequence
   - Suggest messaging hierarchy and visual focus areas
   - Align screenshot strategy with metadata messaging

## Apple App Store Character Limits

**Critical Limits to Validate:**
- **App Name**: 30 characters maximum
- **Subtitle**: 30 characters maximum
- **Promotional Text**: 170 characters maximum
- **Description**: 4,000 characters maximum
- **Keywords**: 100 characters maximum (comma-separated, no spaces)
- **What's New**: 4,000 characters maximum

## Metadata Validation Process

After generating recommendations, always validate using the validation script:

```bash
python scripts/validate_metadata.py
```

The script will:
1. Prompt for each metadata field
2. Calculate character counts
3. Check against Apple's limits
4. Display results with ✅ (pass) or ❌ (fail) indicators
5. Show exact character counts and remaining characters

**Integration Pattern:**
- Generate metadata recommendations
- Run validation script with recommended content
- Display validation results to user
- Adjust any failing fields and re-validate

## Output Format

Structure recommendations as:

### 📱 App Metadata Recommendations

**App Name** (X/30 characters)
[optimized name]

**Subtitle** (X/30 characters)
[optimized subtitle]

**Promotional Text** (X/170 characters)
[promotional text]

**Keywords** (X/100 characters)
[keyword,list,no,spaces]

**Description** (X/4000 characters)
[full description]

### 🎯 Competitive Analysis
[Key insights and positioning recommendations]

### 📸 Screenshot Storyboard Strategy
[Ordered list of screenshot recommendations with messaging]

### ✅ Validation Results
[Output from validation script showing compliance]

## Krankie: App Store Ranking Tracker

Krankie is an agent-first CLI tool for tracking App Store keyword rankings. Use it to monitor keyword performance, track ranking changes over time, and inform ASO optimization decisions with real data.

### Installation

```bash
bun install -g krankie
# or run directly
bunx krankie
```

### Key Commands

**App Management:**
```bash
# Search for apps
krankie app search "<query>" --platform ios

# Add an app to track
krankie app create <app_id> --platform ios

# List tracked apps
krankie app list
```

**Keyword Tracking:**
```bash
# Add keywords to track for an app
krankie keyword add <app_id> "<keyword>" --store us

# List tracked keywords
krankie keyword list
```

**Ranking Checks:**
```bash
# Run ranking checks for all tracked keywords
krankie check run

# View current rankings
krankie rankings

# See biggest movers (gains/losses)
krankie rankings movers

# View ranking history for a keyword
krankie rankings history <keyword_id>

# Check status of last run
krankie check status
```

**Automation:**
```bash
# Install daily cron job (default: 6 AM)
krankie cron install --hour 6

# Check cron status
krankie cron status
```

### Agent Integration

All commands support `--json` flag for structured output:
```bash
krankie rankings --json
krankie app list --json
```

Get agent-friendly instructions:
```bash
krankie instructions --format json
```

### Data Notes

- Rankings track positions 1-200; null indicates outside this range
- Data stored locally in `~/.krankie/krankie.db` (SQLite)
- Daily re-checks are rate-limited; use `--force` to override
- Logs available at `~/.krankie/check.log`

### ASO Workflow Integration

1. **Before optimization**: Use `krankie rankings` to establish baseline keyword positions
2. **Competitive analysis**: Track competitor apps and their keyword rankings
3. **After metadata changes**: Monitor `krankie rankings movers` to measure impact
4. **Trend analysis**: Use `krankie rankings history` to identify patterns

## Resources

### scripts/validate_metadata.py
Python script that validates App Store metadata against Apple's character limits. Provides interactive validation with clear pass/fail indicators.

### references/aso_learnings.md
Comprehensive ASO knowledge base containing optimization strategies, competitive analysis frameworks, keyword research techniques, and proven best practices. Load this file to inform all ASO recommendations.
