---
name: sentiment-analyzer
description: "Analyze sentiment in text using ML models. Use when: analyzing customer reviews; processing NPS feedback; monitoring brand mentions; evaluating campaign responses; categorizing support tickets"
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# Sentiment Analyzer

> Analyze sentiment in customer feedback using transformer models - understand what your customers really feel at scale.

## When to Use This Skill

- **Review analysis** - Process hundreds of product reviews
- **NPS feedback** - Categorize open-ended survey responses
- **Social listening** - Monitor brand sentiment on social media
- **Campaign feedback** - Evaluate response to marketing campaigns
- **Support insights** - Categorize support ticket sentiment


## What Claude Does vs What You Decide

| Claude Does | You Decide |
|-------------|------------|
| Structures analysis frameworks | Metric definitions |
| Identifies patterns in data | Business interpretation |
| Creates visualization templates | Dashboard design |
| Suggests optimization areas | Action priorities |
| Calculates statistical measures | Decision thresholds |

## Dependencies

```bash
pip install transformers torch pandas click
# Or for lighter CPU-only version:
pip install textblob vaderSentiment pandas click
```

## Commands

### Analyze Text
```bash
python scripts/main.py analyze "This product exceeded my expectations!"
python scripts/main.py analyze "The service was terrible and slow."
```

### Batch Analysis
```bash
python scripts/main.py batch reviews.csv --column text
python scripts/main.py batch feedback.csv --column comment --output results.csv
```

### Generate Report
```bash
python scripts/main.py report reviews.csv --column text --output sentiment-report.html
```

## Examples

### Example 1: Analyze Product Reviews
```bash
# Process CSV of reviews
python scripts/main.py batch amazon-reviews.csv --column review_text

# Output: amazon-reviews_sentiment.csv
# review_text                    | sentiment | score  | label
# "Absolutely love this!"        | positive  | 0.95   | Very Positive
# "It's okay, nothing special"   | neutral   | 0.52   | Neutral
# "Worst purchase ever"          | negative  | 0.12   | Very Negative
```

### Example 2: NPS Feedback Categorization
```bash
# Analyze NPS survey responses
python scripts/main.py report nps-responses.csv --column feedback

# Output: sentiment-report.html
# Summary:
# - Positive: 62% (mainly: product quality, support)
# - Neutral: 23% (mainly: pricing concerns)
# - Negative: 15% (mainly: shipping delays)
```

## Sentiment Categories

| Score Range | Label | Interpretation |
|-------------|-------|----------------|
| 0.8 - 1.0 | Very Positive | Enthusiastic, recommend |
| 0.6 - 0.8 | Positive | Satisfied, happy |
| 0.4 - 0.6 | Neutral | Mixed or indifferent |
| 0.2 - 0.4 | Negative | Disappointed, frustrated |
| 0.0 - 0.2 | Very Negative | Angry, will churn |

## Skill Boundaries

### What This Skill Does Well
- Structuring data analysis
- Identifying patterns and trends
- Creating visualization frameworks
- Calculating statistical measures

### What This Skill Cannot Do
- Access your actual data
- Replace statistical expertise
- Make business decisions
- Guarantee prediction accuracy

## Related Skills

- [social-analytics](../../social/social-analytics/) - Get social data to analyze
- [content-repurposer](../../automation/content-repurposer/) - Use insights for content

## Skill Metadata


- **Mode**: centaur
```yaml
category: analytics
subcategory: nlp
dependencies: [transformers, torch, pandas]
difficulty: intermediate
time_saved: 6+ hours/week
```
