---
name: openclaw-memory-enhancer
description: "Edge-optimized RAG memory system for OpenClaw with semantic search. Automatically loads memory files, provides intelligent recall, and enhances conversations with relevant context. Perfect for Jetson and edge devices (<10MB memory)."
homepage: https://github.com/henryfcb/openclaw-memory-enhancer
metadata:
  openclaw:
    emoji: "🧠"
    requires:
      bins: ["python3"]
      env: []
    install: []
---

# 🧠 OpenClaw Memory Enhancer

Give OpenClaw **long-term memory** - remember important information across sessions and automatically recall relevant context for conversations.

## Core Capabilities

| Capability | Description |
|------------|-------------|
| 🔍 **Semantic Search** | Vector similarity search, understanding intent not just keywords |
| 📂 **Auto Load** | Automatically reads all files from `memory/` directory |
| 💡 **Smart Recall** | Finds relevant historical memory during conversations |
| 🔗 **Memory Graph** | Builds connections between related memories |
| 💾 **Local Storage** | 100% local, no cloud, complete privacy |
| 🚀 **Edge Optimized** | <10MB memory, runs on Jetson/Raspberry Pi |

## Quick Reference

| Task | Command (Edge Version) | Command (Standard Version) |
|------|------------------------|---------------------------|
| Load memories | `python3 memory_enhancer_edge.py --load` | `python3 memory_enhancer.py --load` |
| Search | `--search "query"` | `--search "query"` |
| Add memory | `--add "content"` | `--add "content"` |
| Export | `--export` | `--export` |
| Stats | `--stats` | `--stats` |

## When to Use

**Use this skill when:**
- You want OpenClaw to remember things across sessions
- You need to build a knowledge base from chat history
- You're working on long-term projects that need context
- You want automatic FAQ generation from conversations
- You're running on edge devices with limited memory

**Don't use when:**
- Simple note-taking apps are sufficient
- You don't need cross-session memory
- You have plenty of memory and want maximum accuracy (use standard version)

## Versions

### Edge Version ⭐ Recommended

**Best for:** Jetson, Raspberry Pi, embedded devices

```bash
python3 memory_enhancer_edge.py --load
```

**Features:**
- Zero dependencies (Python stdlib only)
- Memory usage < 10MB
- Lightweight keyword + vector matching
- Perfect for resource-constrained devices

### Standard Version

**Best for:** Desktop/server, maximum accuracy

```bash
pip install sentence-transformers numpy
python3 memory_enhancer.py --load
```

**Features:**
- Uses sentence-transformers for high-quality embeddings
- Better semantic understanding
- Memory usage 50-100MB
- Requires model download (~50MB)

## Installation

### Via ClawHub (Recommended)

```bash
clawhub install openclaw-memory-enhancer
```

### Via Git

```bash
git clone https://github.com/henryfcb/openclaw-memory-enhancer.git \
  ~/.openclaw/skills/openclaw-memory-enhancer
```

## Usage Examples

### Command Line

```bash
# Load existing OpenClaw memories
cd ~/.openclaw/skills/openclaw-memory-enhancer
python3 memory_enhancer_edge.py --load

# Search for memories
python3 memory_enhancer_edge.py --search "voice-call plugin setup"

# Add a new memory
python3 memory_enhancer_edge.py --add "User prefers dark mode"

# Show statistics
python3 memory_enhancer_edge.py --stats

# Export to Markdown
python3 memory_enhancer_edge.py --export
```

### Python API

```python
from memory_enhancer_edge import MemoryEnhancerEdge

# Initialize
memory = MemoryEnhancerEdge()

# Load existing memories
memory.load_openclaw_memory()

# Search for relevant memories
results = memory.search_memory("AI trends report", top_k=3)
for r in results:
    print(f"[{r['similarity']:.2f}] {r['content'][:100]}...")

# Recall context for a conversation
context = memory.recall_for_prompt("Help me check billing")
# Returns formatted memory context

# Add new memory
memory.add_memory(
    content="User prefers direct results",
    source="chat",
    memory_type="preference"
)
```

### OpenClaw Integration

```python
# In your OpenClaw agent
from skills.openclaw_memory_enhancer.memory_enhancer_edge import MemoryEnhancerEdge

class EnhancedAgent:
    def __init__(self):
        self.memory = MemoryEnhancerEdge()
        self.memory.load_openclaw_memory()
    
    def process(self, user_input: str) -> str:
        # 1. Recall relevant memories
        memory_context = self.memory.recall_for_prompt(user_input)
        
        # 2. Enhance prompt with context
        enhanced_prompt = f"""
{memory_context}

User: {user_input}
"""
        
        # 3. Call LLM with enhanced context
        response = call_llm(enhanced_prompt)
        
        return response
```

## Memory Types

| Type | Description | Example |
|------|-------------|---------|
| `daily_log` | Daily memory files | `memory/2026-02-22.md` |
| `capability` | Capability records | Skills, tools |
| `core_memory` | Core conventions | Important rules |
| `qa` | Question & Answer | Q: How to... A: You should... |
| `instruction` | Direct instructions | "Remember: always do X" |
| `solution` | Technical solutions | Step-by-step guides |
| `preference` | User preferences | "User likes dark mode" |

## How It Works

### Memory Encoding (Edge Version)

1. **Keyword Extraction**: Extract important words from text
2. **Hash Vector**: Map keywords to vector positions
3. **Normalization**: L2 normalize the vector
4. **Storage**: Save to local JSON file

### Memory Retrieval

1. **Query Encoding**: Convert query to same vector format
2. **Keyword Pre-filter**: Fast filter by common keywords
3. **Similarity Calculation**: Cosine similarity between vectors
4. **Ranking**: Return top-k most similar memories

### Privacy Protection

- All data stored locally in `~/.openclaw/workspace/knowledge-base/`
- No network requests
- No external API calls
- No data leaves your device

## Technical Specifications

### Edge Version

```yaml
Vector Dimensions: 128
Memory Usage: < 10MB
Dependencies: None (Python stdlib)
Storage Format: JSON
Max Memories: 1000 (configurable)
Query Latency: < 100ms
```

### Standard Version

```yaml
Vector Dimensions: 384
Memory Usage: 50-100MB
Dependencies: sentence-transformers, numpy
Storage Format: NumPy + JSON
Model Size: ~50MB download
Query Latency: < 50ms
```

## Configuration

Edit these parameters in the code:

```python
self.config = {
    "vector_dim": 128,        # Vector dimensions
    "max_memory_size": 1000,  # Max number of memories
    "chunk_size": 500,        # Content chunk size
    "min_keyword_len": 2,     # Minimum keyword length
}
```

## Troubleshooting

### No results found

```python
# Lower the threshold
results = memory.search_memory(query, threshold=0.2)  # Default 0.3

# Increase top_k
results = memory.search_memory(query, top_k=10)  # Default 5
```

### Memory limit reached

The system automatically removes oldest memories when limit is reached.

To increase limit:
```python
self.config["max_memory_size"] = 5000  # Increase from 1000
```

### Slow performance

- Use Edge version instead of Standard
- Reduce `max_memory_size`
- Use keyword pre-filtering (automatic)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a Pull Request

## License

MIT License - See LICENSE file for details.

## Acknowledgments

- Built for the OpenClaw ecosystem
- Optimized for edge computing devices
- Inspired by long-term memory systems in AI

---

**Not an official OpenClaw or Moonshot AI product.**

**Users must provide their own OpenClaw workspace and API keys.**