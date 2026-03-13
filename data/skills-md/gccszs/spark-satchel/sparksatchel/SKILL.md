---
name: sparksatchel
description: "Intelligent skill retrieval and recommendation system for Claude Code. Uses semantic search, intent analysis, and confidence scoring to recommend the most appropriate skills. Features: (1) Smart skill matching via bilingual embeddings (Chinese/English), (2) Prudent decision-making with three confidence tiers, (3) Historical learning from usage patterns, (4) Automatic health checking and lifecycle management, (5) Intelligent cache cleanup. Use when: User asks to find/recommend a skill, multiple skills might match a request, or skill selection requires intelligent analysis."
---

# SparkSatchel 灵犀妙计

A Meta-Skill that provides intelligent skill retrieval and recommendation for Claude Code.

## Core Philosophy

> "Think twice before acting, keep the user burden-free"

## Quick Start

```python
from src.retriever import SparkSatchel

sparksatchel = SparkSatchel()
result = sparksatchel.retrieve("process this PDF")
```

## Decision Mechanism

The system evaluates confidence and responds accordingly:

| Confidence Level | Threshold | Action |
|------------------|-----------|--------|
| **High** | >70% | Auto-recommend with reasoning |
| **Medium** | 40-70% | Recommend primary + alternatives |
| **Low** | <40% | Present candidates and ask user |

## Key Features

### 1. Semantic Retrieval

- **Bilingual embeddings**: Supports Chinese and English via paraphrase-multilingual-MiniLM-L12-v2
- **Sharded storage**: Skills organized by category for efficient retrieval
- **Vector similarity**: Matches user intent to skill descriptions

### 2. Intent Analysis

Extracts from user requests:
- Primary intent
- Keywords
- Entities (filenames, formats, etc.)

### 3. Historical Learning

- Tracks all skill calls
- Records success/failure feedback
- Calculates skill success rates
- Optimizes recommendation ranking

### 4. Health Checking

- Detects missing skills
- Identifies corrupted skills
- Handles version mismatches
- Provides fallback strategies

### 5. Cache Management

- Monitors database size
- Tracks record count
- Suggests cleanup when needed
- Supports auto/manual cleanup

## Usage Examples

### High Confidence (Auto-recommend)

```
User: "Process this PDF"
SparkSatchel: "I recommend pdf-skill because it specializes in PDF documents (92% historical success rate)"
```

### Medium Confidence (With alternatives)

```
User: "Create a document"
SparkSatchel: "I suggest docx-skill. pdf-skill is also available. Want me to compare them?"
```

### Low Confidence (Ask user)

```
User: "Process data"
SparkSatchel: "Found several matching skills. Which one fits best?
- xlsx-skill: Excel spreadsheet processing
- pandas-skill: Data analysis with Python
- csv-skill: CSV file handling"
```

## Embedding Models

### Pre-installed Model (Ready to Use)

SparkSatchel comes with a pre-downloaded bilingual embedding model:

- **Model**: `paraphrase-multilingual-MiniLM-L12-v2`
- **Size**: ~470MB
- **Languages**: 50+ including Chinese and English
- **Dimension**: 384
- **Status**: ✅ Pre-downloaded, ready to use out-of-the-box
- **Location**: `~/.cache/huggingface/hub/`

The default model provides good balance between:
- ✅ Bilingual support (Chinese + English)
- ✅ Lightweight size
- ✅ Fast inference
- ✅ Offline capability

### Model Selection Guide

Choose the right model based on your scenario:

#### Model Comparison

| Model | Size | Languages | Speed | Accuracy | Best For |
|-------|------|-----------|-------|----------|----------|
| **paraphrase-multilingual-MiniLM-L12-v2** | 470MB | 50+ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | **Default choice** - Balanced performance |
| **shibing624/text2vec-base-chinese** | 110MB | Chinese | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | **Chinese-only** - Faster & more accurate |
| **intfloat/multilingual-e5-large** | 1.3GB | 100+ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | **High accuracy** - Best for complex queries |
| **BAAI/bge-large-zh-v1.5** | 390MB | Chinese | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | **Chinese advanced** - State-of-the-art |
| **all-MiniLM-L6-v2** | 23MB | English | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | **English only** - Ultra lightweight |

#### Scenario Recommendations

**Quick Download with Script**

Use the provided download script for convenience:

```bash
# List available models
python scripts/download_model.py --list

# Download default model (already downloaded ✅)
python scripts/download_model.py default

# Download Chinese-optimized model
python scripts/download_model.py chinese

# Download high-accuracy multilingual model
python scripts/download_model.py large

# Download ultra-lightweight English model
python scripts/download_model.py english
```

**Scenario 1: Chinese-dominant environment**

```bash
# Option A: Use download script
python scripts/download_model.py chinese

# Option B: Manual download
pip install sentence-transformers
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('shibing624/text2vec-base-chinese')"
```

**Scenario 2: English-only (fastest)**

```bash
# Option A: Use download script
python scripts/download_model.py english

# Option B: Manual download
pip install sentence-transformers
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
```

**Scenario 3: Maximum accuracy (multilingual)**
```bash
# Download high-accuracy model
pip install sentence-transformers
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('intfloat/multilingual-e5-large')"
```

**Scenario 4: Cloud-based (no local storage)**
```bash
# Use OpenAI API (requires API key)
pip install openai
```

### How to Switch Models

**Option 1: Modify code (permanent)**

Edit `src/models/embedding.py`:
```python
class EmbeddingModel:
    # Change default model
    DEFAULT_MODEL = "shibing624/text2vec-base-chinese"  # Your choice
```

**Option 2: Pass model name (temporary)**

```python
from src.models.embedding import EmbeddingModel
from src.retriever import SparkSatchel

# Use custom model
custom_model = EmbeddingModel(
    model_name="shibing624/text2vec-base-chinese",
    device="cpu"  # or "cuda" for GPU acceleration
)

# Pass to SparkSatchel
sparksatchel = SparkSatchel(embedding_model=custom_model)
```

**Option 3: Use OpenAI API**

```python
import openai

def openai_embedding(text: str) -> list:
    response = openai.Embedding.create(
        model="text-embedding-3-small",
        input=text
    )
    return response['data'][0]['embedding']
```

### Model Performance Tips

1. **GPU Acceleration**: If you have NVIDIA GPU, use `device="cuda"` for 5-10x speedup
2. **Batch Processing**: Process multiple texts at once for better throughput
3. **Caching**: Models are cached after first download, no re-downloading needed
4. **Quantization**: For memory-constrained environments, use 8-bit quantized models

## Project Structure

```
SparkSatchel/
├── SKILL.md              # This file
├── requirements.txt      # Dependencies
├── src/
│   ├── retriever.py      # Main entry point
│   ├── models/           # Embedding models
│   ├── storage/          # Vector DB + history
│   ├── analysis/         # Intent + confidence
│   └── maintenance/      # Health + lifecycle + cache
└── data/                 # Data storage
    ├── collections/      # Vector databases
    └── history.db        # Call history
```

## API Reference

### Main Interface

```python
class SparkSatchel:
    def retrieve(self, user_request: str) -> RetrievalResult:
        """Search and recommend skills"""

    def feedback(self, skill_name: str, success: bool, feedback: str = ""):
        """Record user feedback"""

    def check_health(self) -> Dict:
        """Check system health"""

    def cleanup(self, strategy: dict = None):
        """Execute cache cleanup"""
```

### Retrieval Result

```python
@dataclass
class RetrievalResult:
    confidence: float              # 0-1
    recommended_skill: str         # Skill name
    reasoning: str                 # Explanation
    alternative_skills: List[str]  # For medium confidence
    candidate_skills: List[Dict]   # For low confidence
    requires_confirmation: bool    # Needs user input?
```

## Maintenance

### Check Health

```python
health = sparksatchel.check_health()
if health["cache"]["needs_cleanup"]:
    print(health["suggestion"])
```

### Cleanup Cache

```python
from src.maintenance.cache import CleanupStrategy

# By age (delete records older than 30 days)
sparksatchel.cleanup(CleanupStrategy.by_age(days=30))

# By count (keep recent 1000 records)
sparksatchel.cleanup(CleanupStrategy.by_count(keep=1000))
```

## Tech Stack

- **Python**: 3.10+
- **Vector DB**: ChromaDB
- **Embedding**: sentence-transformers
- **History**: SQLite

## Performance

| Metric | Target |
|--------|--------|
| Retrieval latency | <500ms (100k skills) |
| Memory usage | <500MB |
| Startup time | <3s |
| Accuracy | >85% |
