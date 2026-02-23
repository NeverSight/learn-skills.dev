---
name: web-research
description: Web search with automatic Qdrant storage for building persistent knowledge
---

# Web Research Skill

Combines WebSearch with automatic Qdrant storage to build a searchable knowledge base.

## Workflow

```
1. Check Qdrant first    → qdrant-find for existing knowledge
2. Search if needed      → WebSearch for current information
3. Store valuable finds  → qdrant-store with rich metadata
4. Return synthesized    → Combine stored + new knowledge
```

## Step 1: Check Existing Knowledge

Before searching the web, check if the answer already exists:

```
Tool: qdrant-find
Query: "<user's question or topic>"
```

If sufficient information exists with recent `harvested_at`, use it directly.

## Step 2: Web Search

When stored knowledge is insufficient or stale:

```
Tool: WebSearch
Query: "<refined search query>"
```

## Step 3: Store Results

After getting valuable results, store with rich metadata:

```
Tool: qdrant-store
Information: |
  # <Topic/Question>

  ## Key Findings
  - Finding 1
  - Finding 2

  ## Details
  <Synthesized information from search results>

  ## Sources
  - [Title](URL)

Metadata:
  # Required fields
  source: "web_search"
  content_type: "text"
  harvested_at: "2025-01-04T10:30:00Z"

  # Search context
  query: "<original search query>"
  urls: ["https://example.com/1", "https://example.com/2"]

  # Classification (for filtering)
  category: "technology"
  subcategory: "databases"
  type: "documentation"

  # Technical context (when applicable)
  language: "python"
  framework: "fastapi"
  version: "0.100+"

  # Quality signals
  confidence: "high"
  freshness: "current"

  # Relationships
  related_topics: ["vector-search", "embeddings", "rag"]
  project: "reflex"
```

## Rich Metadata Schema

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| source | string | Origin: `web_search`, `api_docs`, `github`, `manual` |
| content_type | string | `text`, `code`, `image`, `video_transcript` |
| harvested_at | string | ISO 8601 timestamp |

### Search Context

| Field | Type | Description |
|-------|------|-------------|
| query | string | Original search query |
| urls | array | Source URLs (array for proper filtering) |
| domain | string | Primary domain (e.g., `github.com`) |

### Classification (Enables Filtering)

| Field | Type | Values |
|-------|------|--------|
| category | string | `technology`, `business`, `science`, `design`, `security`, `devops` |
| subcategory | string | More specific: `databases`, `frontend`, `ml`, `networking` |
| type | string | `documentation`, `tutorial`, `troubleshooting`, `reference`, `comparison`, `news` |

### Technical Context

| Field | Type | Description |
|-------|------|-------------|
| language | string | Programming language: `python`, `typescript`, `rust`, `go` |
| framework | string | Framework/library: `fastapi`, `react`, `tokio` |
| version | string | Version constraint: `3.12+`, `>=2.0`, `latest` |
| platform | string | `linux`, `macos`, `windows`, `docker`, `kubernetes` |

### Quality Signals

| Field | Type | Values |
|-------|------|--------|
| confidence | string | `high`, `medium`, `low` - how reliable is this info |
| freshness | string | `current`, `recent`, `dated`, `historical` |
| depth | string | `overview`, `detailed`, `comprehensive` |

### Relationships

| Field | Type | Description |
|-------|------|-------------|
| related_topics | array | Related concepts for discovery |
| project | string | Associated project name |
| supersedes | string | ID of entry this replaces |
| parent_topic | string | Broader topic this belongs to |

### Image References (URL only, no download)

| Field | Type | Description |
|-------|------|-------------|
| image_url | string | URL to the image |
| alt_text | string | Image description |
| image_type | string | `photo`, `diagram`, `screenshot`, `chart`, `icon` |

## Filtering Examples

**Find Python documentation:**
```
qdrant-find with filter:
  category: "technology"
  language: "python"
  type: "documentation"
```

**Find recent troubleshooting:**
```
qdrant-find with filter:
  type: "troubleshooting"
  freshness: "current"
```

**Find project-specific knowledge:**
```
qdrant-find with filter:
  project: "reflex"
```

## When to Store

**Always store:**
- Technical documentation findings
- API patterns and examples
- Error solutions and workarounds
- Best practices and recommendations
- Tool comparisons and evaluations

**Skip storing:**
- Simple factual lookups (dates, definitions)
- Ephemeral information (current weather, stock prices)
- Information already in Qdrant with same content

## Example: Full Research Flow

User asks: "How do I set up GitHub Actions for Python testing?"

```
# Step 1: Check existing
qdrant-find: "GitHub Actions Python testing setup"
→ No relevant results

# Step 2: Search
WebSearch: "GitHub Actions Python pytest workflow 2025"
→ Returns results with workflow examples

# Step 3: Store
qdrant-store:
  Information: |
    # GitHub Actions Python Testing Setup

    ## Key Findings
    - Use `actions/setup-python@v5` for Python environment
    - Matrix testing across Python versions: 3.9, 3.10, 3.11, 3.12
    - pytest with coverage using `pytest-cov`

    ## Workflow Template
    ```yaml
    name: Python Tests
    on: [push, pull_request]
    jobs:
      test:
        runs-on: ubuntu-latest
        strategy:
          matrix:
            python-version: ["3.9", "3.10", "3.11", "3.12"]
        steps:
          - uses: actions/checkout@v4
          - uses: actions/setup-python@v5
            with:
              python-version: ${{ matrix.python-version }}
          - run: pip install -e .[test]
          - run: pytest --cov
    ```

    ## Sources
    - [GitHub Actions Python Guide](https://docs.github.com/en/actions/...)

  Metadata:
    source: "web_search"
    content_type: "code"
    harvested_at: "2025-01-04T10:30:00Z"
    query: "GitHub Actions Python pytest workflow 2025"
    urls: ["https://docs.github.com/en/actions/..."]
    domain: "github.com"
    category: "technology"
    subcategory: "ci-cd"
    type: "documentation"
    language: "python"
    framework: "pytest"
    platform: "github-actions"
    confidence: "high"
    freshness: "current"
    depth: "detailed"
    related_topics: ["testing", "ci-cd", "yaml", "github"]
```

## Integration with Other Skills

- **research-patterns**: Use web-research for external searches
- **qdrant-patterns**: Follows same metadata conventions
- **knowledge-ingestion-patterns**: Compatible chunking approach
- **github-harvester**: Similar metadata schema for GitHub content
