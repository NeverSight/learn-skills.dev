---
name: rlm
description: "Process files too large to fit in context (>100KB, >2000 lines). Uses Python REPL for structural analysis, LLM queries for semantic reasoning, and subagents for final synthesis. Triggers - large file, big document, massive log, full codebase, entire repo, long transcript, context window exceeded."
---

# rlm (Recursive Language Model)

## Core Principle

**Large content stays in the REPL environment, not in your context.**

The REPL holds the full file in memory. You write Python to analyze it. Only your `print()` output returns to your context—never raw file content.

## When to Use

- Files >100KB or >2000 lines
- Need to query the same large file multiple times in a session
- Structural or semantic analysis of logs, transcripts, codebases

## Quick Start

```bash
# 1. Initialize (loads file into REPL memory)
python3 ~/skills/rlm/scripts/rlm_repl.py init <file>
# → Returns state path like: .pi/rlm_state/myfile-20260122-093000/state.pkl

# 2. Explore with Python (zero context cost)
python3 ~/skills/rlm/scripts/rlm_repl.py --state <state_path> exec -c "
hits = grep('ERROR')
print(f'Found {count(hits)} errors')
for item in expand(hits, limit=5):
    print(item['snippet'])
"

# 3. Only escalate to LLM when semantic reasoning is needed
```

---

## The Escalation Ladder

### Level 1: REPL Analysis (Default)

**Use for:** Pattern matching, structure extraction, aggregation, JSON parsing.

**Context cost:** Only your `print()` output returns.

```bash
python3 ~/skills/rlm/scripts/rlm_repl.py --state <path> exec <<'PY'
import json

# The full file is available as `content`
lines = content.split('\n')
print(f'Total lines: {len(lines)}')

# Find patterns
hits = grep_raw('error|exception', max_matches=50)
print(f'Found {len(hits)} error lines')

# Parse specific lines
for i, line in enumerate(lines[:10]):
    if line.strip():
        data = json.loads(line)
        print(f"Line {i}: type={data.get('type')}")

# Aggregate
sizes = [(len(line), i) for i, line in enumerate(lines)]
sizes.sort(reverse=True)
print(f'Biggest lines: {sizes[:5]}')
PY
```

**When Level 1 is sufficient:**
- Finding all occurrences of a pattern
- Counting/sizing content
- Extracting fields from structured data (JSON, logs)
- Computing statistics

---

### Level 2: REPL + llm_query()

**Use for:** Semantic reasoning where you need LLM judgment, but want results to stay in the REPL.

**Context cost:** Only your `print()` output returns. The LLM call happens in a subprocess.

```bash
python3 ~/skills/rlm/scripts/rlm_repl.py --state <path> exec <<'PY'
# Extract errors with REPL (Level 1)
errors = grep_raw('ERROR', max_matches=10)

# Classify with LLM (Level 2) - reasoning stays in subprocess
for err in errors[:3]:
    snippet = err['snippet'][:2000]
    result = llm_query(f"Classify this error as critical/warning/info:\n{snippet}")
    print(f"Line {err['line_num']}: {result}")
    add_buffer(result)  # accumulate for later synthesis
PY
```

**Batch processing:**
```bash
python3 ~/skills/rlm/scripts/rlm_repl.py --state <path> exec <<'PY'
# Process multiple items in parallel
chunks = list(Path(session_dir / 'chunks').glob('chunk_*.txt'))
prompts = [f"Summarize:\n{c.read_text()[:50000]}" for c in chunks[:10]]

results, failures = llm_query_batch(prompts, concurrency=5)
for i, result in enumerate(results):
    if "[ERROR:" not in result:
        add_buffer(f"Chunk {i}: {result}")
        print(f"Chunk {i}: {result[:100]}...")
PY
```

**When to use Level 2:**
- Classifying or categorizing content
- Summarizing sections
- Semantic search ("find discussions about X")
- Any task requiring judgment, not just pattern matching

---

### Level 3: Subagent Synthesis

**Use for:**
1. Final answer generation after accumulating findings
2. Protecting main context when you'll query the same file many times
3. When synthesis itself is complex enough to warrant a fresh context

**Context cost:** ~5KB max per subagent (enforced by `max-output-chars`).

```json
{
  "agent": "rlm-subcall",
  "task": "Query: <user's question>\nChunk file: /absolute/path/to/chunk_0001.txt"
}
```

**For final synthesis of accumulated buffers:**
```bash
# First, export buffers to a file
python3 ~/skills/rlm/scripts/rlm_repl.py --state <path> export-buffers > findings.txt

# Then use subagent to synthesize
{
  "agent": "rlm-subcall",
  "task": "Synthesize these findings into a structured report:\n$(cat findings.txt)"
}
```

**Parallel chunk analysis (when Level 2 isn't sufficient):**
```json
{
  "tasks": [
    {"agent": "rlm-subcall", "task": "Query: Find security issues\nChunk file: /path/chunk_0000.txt"},
    {"agent": "rlm-subcall", "task": "Query: Find security issues\nChunk file: /path/chunk_0001.txt"}
  ]
}
```

**Limits:**
- Max 8 parallel tasks per batch
- Expected output: ~2KB per chunk (JSON)
- Total subagent returns should stay under 400KB

---

## Decision Tree

```
Is this a structural query? (find X, count Y, extract fields, parse JSON)
    └─ YES → Level 1: REPL
    └─ NO ↓

Do I need LLM judgment? (classify, summarize, interpret meaning)
    └─ YES → Does it need to return to my context immediately?
        └─ NO → Level 2: llm_query() in REPL
        └─ YES → Level 3: Subagent
    └─ NO → Level 1: REPL

Am I synthesizing final results from accumulated findings?
    └─ YES → Level 3: Subagent (protects your context for future queries)

Will I query this file multiple times in this session?
    └─ YES → Prefer Levels 1-2 (keep main context free for multiple queries)
```

---

## REPL Reference

### Initialization
```bash
python3 ~/skills/rlm/scripts/rlm_repl.py init <context_path>
python3 ~/skills/rlm/scripts/rlm_repl.py --state <path> status
python3 ~/skills/rlm/scripts/rlm_repl.py --state <path> reset
```

### Environment Variables (available in exec)
- `content` - Full file content as string
- `state_path` - Path to state.pkl
- `session_dir` - Path to session directory
- `buffers` - List of accumulated text

### Content Exploration
| Function | Returns | Description |
|----------|---------|-------------|
| `peek(start, end)` | `str` | View slice of raw content |
| `grep(pattern)` | handle | Regex search, returns handle stub |
| `grep_raw(pattern)` | `list[dict]` | Raw results with line_num, snippet |
| `write_chunks(out_dir)` | `list[str]` | Write chunks to disk |
| `add_buffer(text)` | `None` | Accumulate text for synthesis |

### Handle System
| Function | Returns | Description |
|----------|---------|-------------|
| `count(handle)` | `int` | Count items |
| `expand(handle, limit)` | `list` | Materialize items |
| `filter_handle(handle, pattern)` | handle | Filter results |
| `last_handle()` | `str` | Most recent handle name |

### LLM Queries (Level 2)
| Function | Returns | Description |
|----------|---------|-------------|
| `llm_query(prompt)` | `str` | Single LLM call in subprocess |
| `llm_query_batch(prompts)` | `(list, dict)` | Parallel calls (max 5 concurrent) |

### Finalization
| Function | Description |
|----------|-------------|
| `set_final_answer(value)` | Mark JSON-serializable result |
| `export-buffers` (CLI) | Dump accumulated buffers |

---

## Chunking (when needed)

For very large files where you need to process sections:

```bash
python3 ~/skills/rlm/scripts/rlm_repl.py --state <path> exec <<'PY'
paths = write_chunks(str(session_dir / 'chunks'), size=200000)
print(f"Created {len(paths)} chunks")
PY

# Read the manifest
cat <session_dir>/chunks/manifest.json
```

Use manifest hints to skip irrelevant chunks before processing.

---

## Context Protection

**Budget:** Assume 200K tokens (~800KB). Reserve:
- 50K for system prompt
- 50K for your reasoning
- 100K for tool returns (~400KB)

**Warning signs:**
- Single subagent returned >10KB → it misbehaved
- Total returns >400KB → stop and synthesize

**If overwhelmed:**
1. Stop dispatching more subagents
2. Synthesize from what you have
3. Use smaller batches (4 instead of 8)

---

## Anti-Patterns

❌ Reading full chunks into your context with `read` tool
❌ Jumping straight to subagents for structural queries  
❌ Dispatching subagents before exploring with REPL
❌ Ignoring manifest hints (processing all chunks blindly)

✅ Always start with REPL exploration
✅ Use `grep` to find relevant sections first
✅ Escalate only when semantic reasoning is needed
✅ Use subagents for synthesis, not initial analysis
