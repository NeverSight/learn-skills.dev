---
name: search-and-fork
description: Use this skill when the user asks to search for and fork an open source repository, "find me an open source project", "search and fork", "search-and-fork", "find a similar project on Gitee", or "fork a repository". Requires Gitee MCP Server to be configured.
version: 1.0.0
requires:
  mcp-servers:
    - gitee
---

> **Note**: If you have `mcporter` installed locally, you should use `mcporter` to invoke the MCP tool instead of directly calling the MCP tool. The `mcporter` CLI provides a more convenient interface and better error handling.

# Search and Fork via Gitee MCP

Search for open source repositories on Gitee that match the user's needs, compare candidates, and fork the chosen one to the user's account.

## Prerequisites

- Gitee MCP Server configured (tools: `search_open_source_repositories`, `fork_repository`, `get_user_info`)
- User must provide: search keywords or a description of what they need

## Steps

### Step 1: Clarify Search Requirements

Confirm with the user:
- Language preference (Go / Java / Python / JavaScript, etc.)
- Use case (web framework / database ORM / CLI tool / UI component library, etc.)
- Activity requirements (e.g., must have recent commits)
- Other preferences (license type, documentation language, etc.)

### Step 2: Search Repositories

Use `search_open_source_repositories` to search:
- Try multiple keyword combinations to cover different phrasings
- Run 2–3 searches if necessary (e.g., both Chinese and English keywords)

### Step 3: Filter and Compare

Evaluate the search results based on:

**Activity indicators**
- Star count (interest/popularity)
- Fork count (how widely it's being used)
- Last updated date (whether it's still maintained)
- Issue / PR count and response speed

**Quality indicators**
- Complete README documentation
- Test code present
- CI/CD configuration
- License suitable for the use case (MIT / Apache preferred over GPL)

**Relevance**
- Does the functionality match the requirements?
- Does the tech stack fit?
- Is there good documentation or community support?

### Step 4: Present Candidate List

```
## Search Results: [keywords]

Top candidates ranked by overall score:

### Recommendation #1: [repo name]
- **Repo**: [owner/repo]
- **Description**: [repo summary]
- **Stars / Forks**: ⭐ N / 🍴 N
- **Language**: [language]
- **Last updated**: [date]
- **License**: [license]
- **Why recommended**: [1–2 sentences]

### Recommendation #2: [repo name]
[same format]

### Recommendation #3: [repo name]
[same format]

---

**Suggested pick**: Recommendation #1, because [reason]
```

### Step 5: Fork the Selected Repository

After the user makes a selection, use `fork_repository` to fork it:
- `owner`: owner of the repository to fork
- `repo`: repository name
- Optional: specify an organization to fork into (defaults to the user's personal account)

After a successful fork, output the forked repository URL and suggest next steps:

```
Fork successful!

**Your repository**: https://gitee.com/[your-username]/[repo-name]

**Suggested next steps:**
1. `git clone` it locally
2. Read the README to learn how to contribute
3. Browse the Issues to find something to work on

Would you like me to explore this repository for you? (use the repo-explorer skill)
```

## Notes

- Search results may include archived or unmaintained repositories — filter these out
- Forking creates a copy under the user's Gitee account without affecting the original repository
- Fork is the standard approach for contributing; if the user only wants to reference the code, a plain clone is sufficient
- For commercial use, pay close attention to the license (GPL is copyleft; MIT / Apache are more permissive)
