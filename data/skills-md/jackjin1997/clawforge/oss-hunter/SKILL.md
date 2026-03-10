---
name: oss-hunter
version: 1.0.0
description: Automatically hunt for high-impact OSS contribution opportunities.
metadata: {"openclaw":{"emoji":"🎯","category":"developer"}}
---

# OSS Hunter 🎯

A precision skill for agents to find, analyze, and strategize for high-impact Open Source contributions. This skill helps you become a top-tier contributor by identifying the most "mergeable" and influential issues in trending repositories.

## Quick Start

Ask your agent:
- "Find me some help-wanted issues in trending AI repositories."
- "Hunt for bug fixes in langchain-ai/langchain that are suitable for a quick PR."
- "Generate a contribution dossier for the most recent trending projects on GitHub."

## Workflow

When hunting for contributions, the agent follows this multi-stage protocol:

### Phase 1: Repository Discovery
Use `web_search` or `gh api` to find trending repositories.
Focus on:
- Stars > 1000
- Recent activity (pushed within 24 hours)
- Relevant topics (AI, Agentic, Web3, Tooling)

### Phase 2: Issue Extraction
Search for specific labels:
- `help wanted`
- `good first issue`
- `bug`
- `v1` / `roadmap`

```bash
gh issue list --repo owner/repo --label "help wanted" --limit 10
```

### Phase 3: Feasibility Analysis
Analyze the issue:
1. **Reproducibility**: Is there a code snippet to reproduce the bug?
2. **Impact**: How many users does this affect?
3. **Mergeability**: Check recent PR history. Does the maintainer merge community PRs quickly?
4. **Complexity**: Can this be solved by an agent with the current tools?

### Phase 4: The Dossier
Generate a structured report for the human:
- **Project Name & Stars**
- **Issue Link & Description**
- **Root Cause Analysis** (based on code inspection)
- **Proposed Fix Strategy**
- **Confidence Score** (1-10)

## Example Dossier

> ### 🦜 LangChain #35009
> **Status**: Potential Fix Identified
> **Description**: ToolMessageChunk merges None content into "NoneNone".
> **Strategy**: Modify `coerce_args` in `tool.py` to skip coercion for `NoneType`.
> **Confidence**: 9/10 (Reproducible locally).

---

## Contributing to the Matrix

Build a better hunter by adding new heuristics to Phase 3. Submit your improvements to the [ClawForge](https://github.com/jackjin1997/ClawForge).

*Powered by OpenClaw & ClawForge.*
