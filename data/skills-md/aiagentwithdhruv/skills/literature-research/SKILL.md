---
name: literature-research
description: Search academic literature and perform deep research reviews. Use when user asks to search PubMed, find academic papers, or do literature reviews.
---

# Literature Research

## Goal
Search academic databases and perform comprehensive literature reviews.

## Scripts
- `./scripts/pubmed_literature_search.py` - Search PubMed
- `./scripts/literature_deep_review.py` - Deep review with Claude

## Usage

### Search PubMed
```bash
python3 ./scripts/pubmed_literature_search.py \
  --query "machine learning cancer diagnosis" \
  --limit 50 \
  --output .tmp/papers.json
```

### Deep Review
```bash
python3 ./scripts/literature_deep_review.py \
  --input .tmp/papers.json \
  --output .tmp/review.md
```

## Output
- JSON file with paper metadata
- Markdown review with key findings, themes, gaps

---

## Schema

### Inputs
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `query` | string | Yes | Research query (e.g., 'machine learning cancer diagnosis') |
| `limit` | integer | No | Max papers to fetch (default: 50) |

### Outputs
| Name | Type | Description |
|------|------|-------------|
| `papers_file` | file_path | JSON file with paper metadata |
| `review_file` | file_path | Markdown review with key findings, themes, gaps |

### Credentials
| Name | Source |
|------|--------|
| `ANTHROPIC_API_KEY` | .env |

### Cost
Free (PubMed API) + Claude for review
