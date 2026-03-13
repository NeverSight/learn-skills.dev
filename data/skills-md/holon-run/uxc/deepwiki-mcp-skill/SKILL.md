---
name: deepwiki-mcp-skill
description: Ask questions and read documentation about any GitHub repository using DeepWiki MCP. Use when you need to understand a codebase, find specific APIs, or get context about a repository.
metadata:
  short-description: Query GitHub repo docs via DeepWiki
---

# DeepWiki Skill

Use this skill to query GitHub repository documentation and ask questions about codebases.

## Prerequisites

- `uxc` is installed and available in `PATH`.
- Network access to `mcp.deepwiki.com/mcp`

Note: Repositories must be indexed on DeepWiki first. Visit https://deepwiki.com to index a repository.

### Install uxc

Choose one of the following methods:

**Homebrew (macOS/Linux):**
```bash
brew tap holon-run/homebrew-tap
brew install uxc
```

**Install Script (macOS/Linux, review before running):**
```bash
curl -fsSL https://raw.githubusercontent.com/holon-run/uxc/main/scripts/install.sh -o install-uxc.sh
less install-uxc.sh
bash install-uxc.sh
```

**Cargo:**
```bash
cargo install uxc
```

## Core Workflow

1. Use fixed link command by default:
   - `command -v deepwiki-mcp-cli`
   - If missing, create it: `uxc link deepwiki-mcp-cli mcp.deepwiki.com/mcp`
   - `deepwiki-mcp-cli -h`
   - If command conflict is detected and cannot be safely reused, stop and ask skill maintainers to pick a different fixed command name.

2. Ask a question about a repository:
   - `deepwiki-mcp-cli ask_question repoName=owner/repo question='your question'`

3. Read wiki structure:
   - `deepwiki-mcp-cli read_wiki_structure repoName=owner/repo`

4. Read wiki contents:
   - `deepwiki-mcp-cli read_wiki_contents repoName=owner/repo`

## Available Tools

- **ask_question**: Ask any question about a GitHub repository and get an AI-powered response
- **read_wiki_structure**: Get a list of documentation topics for a repository
- **read_wiki_contents**: View documentation about a repository

## Usage Examples

### Ask about a codebase

```bash
deepwiki-mcp-cli ask_question repoName=facebook/react question='How does useState work?'
```

### Explore repository structure

```bash
deepwiki-mcp-cli read_wiki_structure '{"repoName":"facebook/react"}'
```

### Read documentation

```bash
deepwiki-mcp-cli read_wiki_contents repoName=facebook/react
```

## Output Parsing

The response is an MCP JSON envelope. Extract the content from `.data.content[].text`.

## Notes

- Maximum 10 repositories per question
- Some popular repositories may already be indexed
- Responses are grounded in the actual codebase
- `deepwiki-mcp-cli <operation> ...` is equivalent to `uxc mcp.deepwiki.com/mcp <operation> ...`.
- If link setup is temporarily unavailable, use direct `uxc mcp.deepwiki.com/mcp ...` calls as fallback.

## Reference Files

- Workflow details: `references/usage-patterns.md`
