---
name: alphaxiv
description: Search and retrieve research papers from AlphaXiv. Use when asked to search papers by title or topic, get paper details/metadata/metrics, retrieve AI overviews or summaries, find trending or top AI papers, get similar papers, browse implementations, look up SOTA benchmarks, or ask questions about a specific paper.
argument-hint: <command> [arxiv-id] [options]
---

# AlphaXiv Skill

AlphaXiv is a platform built on top of arXiv that adds social features, AI-generated overviews, benchmarks, and community engagement to research papers.

## Usage

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/alphaxiv.py <command> [options]
```

## Commands

**Search papers:**
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/alphaxiv.py search "attention is all you need" --limit 5
```

**Get paper details:**
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/alphaxiv.py paper 1706.03762
python3 ${CLAUDE_SKILL_DIR}/scripts/alphaxiv.py paper 1706.03762v1
```

**Get paper metrics (views, votes, comments):**
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/alphaxiv.py metrics 1706.03762
```

**Get AI overview:**
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/alphaxiv.py overview 1706.03762
python3 ${CLAUDE_SKILL_DIR}/scripts/alphaxiv.py overview 1706.03762 --language zh
```

**Get similar papers:**
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/alphaxiv.py similar 1706.03762 --limit 5
```

**Get top trending AI papers:**
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/alphaxiv.py top --limit 10
```

**Get feed papers:**
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/alphaxiv.py feed --sort Hot --interval "7 Days" --limit 10
```

**Get paper implementations (code repos):**
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/alphaxiv.py implementations 1706.03762
```

**Get SOTA tasks:**
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/alphaxiv.py sota
python3 ${CLAUDE_SKILL_DIR}/scripts/alphaxiv.py sota --slug image-classification
```

**Get paper authors, institutions, topics, GitHub:**
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/alphaxiv.py metadata 1706.03762
python3 ${CLAUDE_SKILL_DIR}/scripts/alphaxiv.py metadata 1706.03762 --bibtex
```

**Ask a question about a paper (requires token):**
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/alphaxiv.py ask "What is the main contribution?" --paper 1706.03762

# Continue a conversation
python3 ${CLAUDE_SKILL_DIR}/scripts/alphaxiv.py ask "How does this compare to RNNs?" --chat-id <uuid>

# Use a specific model
python3 ${CLAUDE_SKILL_DIR}/scripts/alphaxiv.py ask "Summarize the experiments" --paper 1706.03762 --model claude-4.5-sonnet
```

## Token Setup (Required for `ask` only)

1. Log in at https://www.alphaxiv.org
2. Go to Profile → User Settings → API Keys
3. Create a new API key
4. Add to `~/.zshrc`:
   ```bash
   export ALPHAXIV_TOKEN=your_api_key_here
   ```

No token needed for: `search`, `paper`, `metrics`, `metadata`, `similar`, `top`, `feed`, `implementations`, `sota`, `overview`.

## Notes

- arXiv IDs like `1706.03762` or `1706.03762v1` are accepted
- `--language` supports 50+ language codes (e.g., `zh`, `ja`, `fr`, `de`, `es`)
- Feed `--sort` options: `Hot`, `Comments`, `Views`, `Likes`, `GitHub`, `Twitter (X)`
- Feed `--interval` options: `3 Days`, `7 Days`, `30 Days`
- `ask --model` options: `gemini-2.5-flash`, `gemini-2.5-pro`, `claude-4.5-sonnet`, `grok-4`, `gpt-5`, and more
