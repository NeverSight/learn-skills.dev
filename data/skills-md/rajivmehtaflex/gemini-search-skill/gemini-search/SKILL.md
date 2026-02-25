---
name: gemini-search
description: Internet search and external information retrieval using Gemini CLI. Use when the user asks to search the internet, find current information, look up recent news, verify facts, or any task requiring real-time external data access.
---

# Gemini Search

## Overview

Perform internet searches and retrieve real-time external information using the Gemini CLI utility with the gemini-2.5-flash model.

## When to Use This Skill

Activate this skill when the user:

1. **Explicitly requests a search**: "Search for...", "Look up...", "Find information about..."
2. **Asks for current/recent information**: "What's the latest news about...", "What happened today..."
3. **Needs fact verification**: "Is it true that...", "Verify this claim..."
4. **Requires external knowledge**: "Help me understand...", "Explain how X works..."
5. **Requests research assistance**: "Research X topic", "Gather information on..."

## Usage

### Basic Search

Execute a search by calling the search script:

```bash
./scripts/search.sh "<your search query>"
```

Or directly use the gemini CLI:

```bash
gemini -p "<your search query>" -m gemini-2.5-flash
```

### Search Query Best Practices

1. **Be specific**: Include key terms and context
2. **Use quotes for exact phrases**: `"exact phrase to match"`
3. **Add time constraints if needed**: "2024", "latest", "recent"
4. **Combine with topic modifiers**: "tutorial", "documentation", "news", "research"

### Example Searches

| User Request | Search Query |
|-------------|--------------|
| "What's the latest AI news?" | `latest AI news 2026` |
| "Find Python async best practices" | `Python async await best practices tutorial` |
| "Who won the Super Bowl 2026?" | `Super Bowl 2026 winner result` |
| "Research quantum computing advances" | `quantum computing breakthroughs 2025 2026` |

## Script Reference

### scripts/search.sh

Shell script wrapper for Gemini search operations.

**Usage:**
```bash
./scripts/search.sh <query>
```

**Parameters:**
- `<query>` - The search query string (required, wrap in quotes if contains spaces)

**Returns:**
- Search results from Gemini CLI to stdout
- Exit code 1 if no query provided

## Error Handling

If the gemini CLI fails:

1. **Check installation**: Ensure `gemini` CLI is installed and in PATH
2. **Verify credentials**: Confirm API access is configured
3. **Retry with simpler query**: Complex queries may timeout
4. **Fallback**: Report the error and suggest alternative approaches

## Resources

### scripts/
- `search.sh` - Main search script using gemini CLI

### references/
- (None required - delete this directory if not needed)

### assets/
- (None required - delete this directory if not needed)
