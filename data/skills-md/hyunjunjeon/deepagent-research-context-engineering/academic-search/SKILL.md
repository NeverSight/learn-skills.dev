---
name: academic-search
description: Search academic paper repositories (arXiv, Semantic Scholar) for scholarly articles in physics, mathematics, computer science, quantitative biology, AI/ML, and related fields
---

# Academic Search Skill

This skill provides access to academic paper repositories, primarily arXiv, for searching scholarly articles. arXiv is a free distribution service and open-access archive for preprints in physics, mathematics, computer science, quantitative biology, quantitative finance, statistics, electrical engineering, systems science, and economics.

## When to Use This Skill

Use this skill when you need to:

- **Find cutting-edge research**: Access preprints and recent papers before formal journal publication
- **Search AI/ML papers**: Find machine learning, deep learning, and artificial intelligence research
- **Explore computational methods**: Search for algorithms, theoretical frameworks, and mathematical foundations
- **Research interdisciplinary topics**: Find papers spanning computer science, biology, physics, and mathematics
- **Gather literature reviews**: Collect relevant papers for comprehensive topic overviews
- **Track state-of-the-art**: Find the latest advances in rapidly evolving fields

### Ideal Use Cases

| Scenario | Example Query |
|----------|---------------|
| Understanding new architectures | "transformer attention mechanism" |
| Exploring applications | "large language models code generation" |
| Finding benchmarks | "image classification benchmark ImageNet" |
| Surveying methods | "reinforcement learning robotics" |
| Technical deep-dives | "backpropagation neural networks" |

## How to Use

The skill provides a Python script that searches arXiv and returns formatted results with titles and abstracts.

### Basic Usage

**Note:** Always use the absolute path from your skills directory.

If running from a virtual environment:
```bash
.venv/bin/python [YOUR_SKILLS_DIR]/academic-search/arxiv_search.py "your search query"
```

Or for system Python:
```bash
python3 [YOUR_SKILLS_DIR]/academic-search/arxiv_search.py "your search query"
```

Replace `[YOUR_SKILLS_DIR]` with the absolute skills directory path from your system prompt.

### Command-Line Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `query` | Yes | - | The search query string |
| `--max-papers` | No | 10 | Maximum number of papers to retrieve |
| `--output-format` | No | text | Output format: `text`, `json`, or `markdown` |

### Examples

**Search for transformer architecture papers:**
```bash
python3 arxiv_search.py "attention is all you need transformer" --max-papers 5
```

**Search for reinforcement learning papers:**
```bash
python3 arxiv_search.py "deep reinforcement learning continuous control" --max-papers 10
```

**Search for LLM papers with JSON output:**
```bash
python3 arxiv_search.py "large language model reasoning" --output-format json
```

**Search for specific author or topic:**
```bash
python3 arxiv_search.py "author:Hinton deep learning"
```

**Search in specific arXiv categories:**
```bash
python3 arxiv_search.py "cat:cs.LG neural network pruning"
```

## Step-by-Step Workflow

### 1. Formulate Your Query

- Use specific, technical terms (e.g., "convolutional neural network image segmentation" not "AI for pictures")
- Include key authors if known: `author:Bengio`
- Specify arXiv categories for focused results: `cat:cs.CL` (Computation and Language)
- Combine terms for intersection: `"graph neural network" AND "molecular property"`

### 2. Execute the Search

```bash
python3 [SKILLS_DIR]/academic-search/arxiv_search.py "your refined query" --max-papers 10
```

### 3. Review Results

The output includes:
- **Title**: Full paper title
- **Authors**: List of paper authors
- **Published**: Publication date
- **arXiv ID**: Unique identifier (useful for citing)
- **URL**: Direct link to the paper
- **Summary**: Abstract text

### 4. Iterate if Needed

- Too many irrelevant results? Add more specific terms or use category filters
- Too few results? Broaden the query or remove restrictive terms
- Looking for recent work? arXiv sorts by relevance by default

### 5. Save and Synthesize

Save relevant findings to your research workspace for later synthesis:
```
research_workspace/
  papers/
    topic_findings.md
```

## Output Formats

### Text Format (Default)
```
================================================================================
Title: Attention Is All You Need
Authors: Ashish Vaswani, Noam Shazeer, Niki Parmar, ...
Published: 2017-06-12
arXiv ID: 1706.03762
URL: https://arxiv.org/abs/1706.03762
--------------------------------------------------------------------------------
Summary: The dominant sequence transduction models are based on complex
recurrent or convolutional neural networks...
================================================================================
```

### JSON Format
```json
{
  "query": "transformer attention",
  "total_results": 5,
  "papers": [
    {
      "title": "Attention Is All You Need",
      "authors": ["Ashish Vaswani", "Noam Shazeer", ...],
      "published": "2017-06-12",
      "arxiv_id": "1706.03762",
      "url": "https://arxiv.org/abs/1706.03762",
      "summary": "The dominant sequence transduction models..."
    }
  ]
}
```

### Markdown Format
```markdown
## Attention Is All You Need

**Authors:** Ashish Vaswani, Noam Shazeer, ...
**Published:** 2017-06-12
**arXiv ID:** [1706.03762](https://arxiv.org/abs/1706.03762)

### Abstract
The dominant sequence transduction models are based on complex...
```

## arXiv Category Reference

Common categories for AI/ML research:

| Category | Description |
|----------|-------------|
| `cs.LG` | Machine Learning |
| `cs.AI` | Artificial Intelligence |
| `cs.CL` | Computation and Language (NLP) |
| `cs.CV` | Computer Vision |
| `cs.NE` | Neural and Evolutionary Computing |
| `cs.RO` | Robotics |
| `stat.ML` | Machine Learning (Statistics) |
| `q-bio` | Quantitative Biology |
| `math.OC` | Optimization and Control |

## Best Practices

### Query Construction

1. **Be specific**: "graph attention network node classification" > "graph neural network"
2. **Use quotation marks**: For exact phrases: `"self-supervised learning"`
3. **Combine operators**: `cat:cs.CV AND "object detection" AND 2023`
4. **Include variations**: Search for both "LLM" and "large language model"

### Research Workflow Integration

1. **Start broad, then narrow**: Begin with general queries, refine based on initial results
2. **Track paper IDs**: Save arXiv IDs for citing and revisiting
3. **Check references**: Seminal papers often cite foundational work
4. **Note publication dates**: Preprints may be superseded by updated versions

### Limitations to Consider

- **Preprint status**: Papers may not be peer-reviewed
- **Version updates**: Check for newer versions (v2, v3, etc.)
- **Coverage gaps**: Not all fields are well-represented on arXiv
- **Rate limiting**: Avoid excessive rapid queries

## Dependencies

This skill requires the `arxiv` Python package:

```bash
# Virtual environment (recommended)
.venv/bin/python -m pip install arxiv

# System-wide
python3 -m pip install arxiv
```

The script will detect if the package is missing and display installation instructions.

## Troubleshooting

### "Error: arxiv package not installed"
Install the arxiv package as shown in Dependencies section.

### No results returned
- Try broader search terms
- Remove category restrictions
- Check for typos in technical terms

### Rate limiting errors
- Wait a few seconds between queries
- Reduce `--max-papers` value

### Connection errors
- Check internet connectivity
- arXiv API may have temporary outages

## Integration with Research Workflow

This skill works well with the web-research skill for comprehensive research:

1. **Use academic-search** for foundational/theoretical papers
2. **Use web-research** for current implementations, tutorials, and practical guides
3. **Synthesize** findings from both sources in your research report

## Notes

- arXiv is particularly strong for:
  - Computer Science (cs.*)
  - Physics (physics.*, hep-*, cond-mat.*)
  - Mathematics (math.*)
  - Quantitative Biology (q-bio.*)
  - Statistics (stat.*)
- Results are sorted by relevance by default
- The arXiv API is free and requires no authentication
- Consider checking cited papers for deeper understanding
