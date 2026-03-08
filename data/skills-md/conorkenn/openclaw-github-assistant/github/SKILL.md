---
name: github
description: Query and manage GitHub repositories - list repos, check CI status, create issues, search repos, and view recent activity.
metadata:
  openclaw:
    emoji: "🐙"
    requires:
      env:
        - GITHUB_TOKEN
        - GITHUB_USERNAME
      config:
        - github.token
        - github.username
---

# GitHub Integration Skill

Query and manage GitHub repositories directly from your AI assistant.

## Capabilities

| Capability | Description |
|------------|-------------|
| `list_repos` | List your repositories with filters |
| `get_repo` | Get detailed info about a specific repo |
| `check_ci_status` | Check CI/CD pipeline status |
| `create_issue` | Create a new issue in a repo |
| `create_repo` | Create a new repository |
| `search_repos` | Search your repositories |
| `get_recent_activity` | Get recent commits |

## Usage

```
You: List my Python repos
Bot: [lists your Python repositories]

You: Check CI status on my main project
Bot: [shows CI/CD status]

You: Create an issue about the bug
Bot: [creates the issue]
```

## Setup

### 1. Generate GitHub Personal Access Token

1. Go to https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Name: `openclaw-github-skill`
4. Scopes: `repo` (required), `read:user` (optional)
5. Copy the token

### 2. Configure Credentials

**Option A: Environment Variables (Recommended)**

Set environment variables before starting OpenClaw:

```bash
export GITHUB_TOKEN="ghp_your_token_here"
export GITHUB_USERNAME="your_github_username"
```

**Option B: OpenClaw Config**

Add to `~/.openclaw/openclaw.json`:

```json
{
  "github": {
    "token": "ghp_your_token_here",
    "username": "your_username"
  }
}
```

### 3. Restart OpenClaw

```bash
openclaw gateway restart
```

## Security Notes

⚠️ **Protect Your Token:**

- Never commit your token to git or share it publicly
- Use the minimal required scopes (`repo` for private repos, `public_repo` for public-only)
- Rotate your token if you suspect it was compromised
- Consider using a secrets manager for production use

⚠️ **Best Practices:**

- Don't store tokens in shell profiles (~/.zshrc) on shared machines
- For local development, environment variables are acceptable
- For production, use your platform's secret/credential store

## Rate Limits

- Unauthenticated requests: 60/hour
- Authenticated requests: 5,000/hour

## Requirements

- OpenClaw gateway running
- GitHub Personal Access Token with appropriate scopes
