---
name: public-repo-explorer
description: Instructs the agent on how to efficiently browse public GitHub repositories using a local shallow clone. You MUST use this skill whenever the user asks you to scan, examine, clone, or extract information from a public Git repository, or whenever they provide a GitHub URL to explore.
license: MIT
metadata:
  author: eho
  version: '1.0.1'

---

# Public Repo Explorer

## Overview

Use this skill to safely and efficiently explore open-source / public repositories.

## Workflow

1. **Create a Temporary Workspace:**
   - Create a temporary directory on the user's machine to hold the repository safely without cluttering their main workspace. 
   - Command: `mkdir -p /tmp/agent-repo-scan-<repo_name> && cd /tmp/agent-repo-scan-<repo_name>`

2. **Perform a Shallow Clone:**
   - Do NOT use the GitHub API or `gh` CLI to avoid authentication blocks or rate limits.
   - Use standard git over HTTPS with the `--depth 1` flag to download only the latest commit. 
   - **Why?** Because as an AI agent, you rarely need the full git history to answer questions about the current codebase, and full clones waste massive amounts of time, bandwidth, and context window space.
   - Command: `git clone --depth 1 <REPOSITORY_URL> .`

3. **Analyze the Architecture:**
   - List the root directory contents to understand the project structure.
   - Look for standard entry points and configuration files: `README.md`, `package.json`, `requirements.txt`, `pyproject.toml`, `docker-compose.yml`, or `Makefile`.

4. **Examine Requested Content:**
   - If the user asked for a general summary, read the `README.md` and the main dependency file to determine the tech stack.
   - If the user asked for specific code (e.g., "Find how they handle database connections"), use your available search or find tools to locate relevant files, then read those specific files.

5. **Report and Clean Up:**
   - Present your findings to the user clearly and concisely based on their original request.
   - Once the user is satisfied, clean up the temporary directory to free up disk space.
   - Command: `rm -rf /tmp/agent-repo-scan-<repo_name>`

## Constraints & Rules:
- **Never** attempt to push commits or open PRs using this skill. It is strictly for read-only browsing.
- **Never** download large binary files, datasets, or LFS assets unless explicitly instructed.
- Always prefer reading files using your internal file-reading tools over standard terminal commands like `cat`, `head`, or `tail` when possible.

## Examples

**Example 1:**
*Input:* "Can you check how the express repository handles routing?"
*Action:*
1. `mkdir -p /tmp/agent-repo-scan-express && cd /tmp/agent-repo-scan-express`
2. `git clone --depth 1 https://github.com/expressjs/express.git .`
3. Use file-reading tools to study routing in the `lib/router` directory.
4. Explain findings to the user.
5. `rm -rf /tmp/agent-repo-scan-express`
