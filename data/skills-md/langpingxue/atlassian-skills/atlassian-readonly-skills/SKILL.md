---
name: atlassian-readonly-skills
description: Read-only Python utilities for Jira, Confluence, and Bitbucket integration. Provides read access to issues, search, workflows, pages, pull requests, commit history, and more. Use when users need to query Atlassian products like "get a Jira issue", "search Confluence pages", "view pull request details", or "get commit history". This variant excludes all write operations for token efficiency and safety.
license: Complete terms in LICENSE
---

# Atlassian Readonly Skills

Read-only Python utilities for Jira, Confluence, and Bitbucket integration, supporting both Cloud and Data Center deployments.

> **Note**: This is a read-only variant that excludes all write operations (create, update, delete). For full functionality including write operations, use `atlassian-skills`.

## Configuration

Two configuration modes are supported:

### Mode 1: Environment Variables (Traditional)

Set environment variables based on your deployment type. This mode is used when `credentials` parameter is not provided to skill functions.

#### Cloud (API Token)

```bash
# Jira Cloud
JIRA_URL=https://your-company.atlassian.net
JIRA_USERNAME=your.email@company.com
JIRA_API_TOKEN=your_api_token

# Confluence Cloud
CONFLUENCE_URL=https://your-company.atlassian.net/wiki
CONFLUENCE_USERNAME=your.email@company.com
CONFLUENCE_API_TOKEN=your_api_token
```

Generate API tokens at: https://id.atlassian.com/manage-profile/security/api-tokens

#### Data Center / Server (PAT Token)

```bash
# Jira Data Center
JIRA_URL=https://jira.your-company.com
JIRA_PAT_TOKEN=your_pat_token

# Confluence Data Center
CONFLUENCE_URL=https://confluence.your-company.com
CONFLUENCE_PAT_TOKEN=your_pat_token

# Bitbucket Server/Data Center
BITBUCKET_URL=https://bitbucket.your-company.com
BITBUCKET_PAT_TOKEN=your_pat_token
```

> **Note**: PAT Token takes precedence if both are provided.

### Mode 2: Parameter-Based (Agent Environments)

When deploying skills in Agent environments where environment variables are not available, pass credentials directly to skill functions using the `AtlassianCredentials` object.

```python
from scripts._common import AtlassianCredentials, check_available_skills
from scripts.jira_issues import jira_get_issue

# Create credentials object
credentials = AtlassianCredentials(
    # Jira configuration
    jira_url="https://your-company.atlassian.net",
    jira_username="your.email@company.com",
    jira_api_token="your_api_token",
    
    # Confluence configuration (optional)
    confluence_url="https://your-company.atlassian.net/wiki",
    confluence_username="your.email@company.com",
    confluence_api_token="your_api_token",
    
    # Bitbucket configuration (optional)
    # bitbucket_url="https://bitbucket.your-company.com",
    # bitbucket_pat_token="your_pat_token"
)

# Check which services are available
availability = check_available_skills(credentials)
print(availability["available_services"])  # ["jira", "confluence"]
print(availability["unavailable_services"])  # {"bitbucket": "Missing bitbucket_url"}

# Use skills with credentials parameter
result = jira_get_issue(
    issue_key="PROJ-123",
    credentials=credentials  # Pass credentials here
)
```

#### Partial Service Configuration

You can configure only the services you need. Services without complete credentials will be unavailable:

```python
# Only configure Jira
credentials = AtlassianCredentials(
    jira_url="https://your-company.atlassian.net",
    jira_username="your.email@company.com",
    jira_api_token="your_api_token"
)

# Jira skills will work
jira_get_issue("PROJ-123", credentials=credentials)  # ✓ Works

# Confluence/Bitbucket skills will fail with ConfigurationError
confluence_get_page("Page Title", "SPACE", credentials=credentials)  # ✗ Fails
```

For credentials object fields and authentication options, see the full documentation in `atlassian-skills`.

## Core Workflow

### Using Environment Variables

```python
from scripts.jira_issues import jira_get_issue
from scripts.jira_search import jira_search
from scripts.confluence_pages import confluence_get_page
import json

# 1. Get a Jira issue
result = jira_get_issue(issue_key="PROJ-123")
issue = json.loads(result)
print(f"Issue: {issue['key']} - {issue['summary']}")

# 2. Search for issues
result = jira_search(
    jql="project = PROJ AND status = 'In Progress'",
    fields="summary,status,assignee",
    limit=50
)
issues = json.loads(result)

# 3. Get a Confluence page
result = confluence_get_page(title="Feature Documentation", space_key="DEV")
page = json.loads(result)
print(f"Page: {page['title']}")
```

### Using Credentials Parameter (Agent Mode)

```python
from scripts._common import AtlassianCredentials
from scripts.jira_issues import jira_get_issue
from scripts.jira_search import jira_search
from scripts.confluence_pages import confluence_get_page
import json

# Create credentials
credentials = AtlassianCredentials(
    jira_url="https://company.atlassian.net",
    jira_username="user@company.com",
    jira_api_token="token123",
    confluence_url="https://company.atlassian.net/wiki",
    confluence_username="user@company.com",
    confluence_api_token="token123"
)

# 1. Get a Jira issue with credentials
result = jira_get_issue(
    issue_key="PROJ-123",
    credentials=credentials
)
issue = json.loads(result)

# 2. Search for issues with credentials
result = jira_search(
    jql="project = PROJ AND status = 'In Progress'",
    fields="summary,status,assignee",
    limit=50,
    credentials=credentials
)

# 3. Get a Confluence page with credentials
result = confluence_get_page(
    title="Feature Documentation",
    space_key="DEV",
    credentials=credentials
)
```

## Available Utilities

### Jira Issue Management (`scripts.jira_issues`)

```python
from scripts.jira_issues import jira_get_issue

# Get issue by key
jira_get_issue(
    issue_key="PROJ-123",
    credentials=credentials  # Optional
)
```

### Jira Search (`scripts.jira_search`)

```python
from scripts.jira_search import jira_search, jira_search_fields

# Search with JQL
jira_search(
    jql="project = PROJ AND status = 'In Progress'",
    fields="summary,status,assignee",
    limit=50
)

# Find field definitions
jira_search_fields(keyword="custom")
```

### Jira Workflow (`scripts.jira_workflow`)

```python
from scripts.jira_workflow import jira_get_transitions

# Get available transitions for an issue
jira_get_transitions(issue_key="PROJ-123")
```

### Jira Agile (`scripts.jira_agile`)

```python
from scripts.jira_agile import (
    jira_get_agile_boards,
    jira_get_board_issues,
    jira_get_sprints_from_board,
    jira_get_sprint_issues
)

# Get boards
jira_get_agile_boards(project_key="PROJ")

# Get issues on a board
jira_get_board_issues(board_id=1, jql="status = 'In Progress'")

# Get sprints from a board
jira_get_sprints_from_board(board_id=1, state="active")

# Get issues in a sprint
jira_get_sprint_issues(sprint_id=42)
```

### Jira Links (`scripts.jira_links`)

```python
from scripts.jira_links import jira_get_link_types

# Get available link types
jira_get_link_types()
```

### Jira Worklog (`scripts.jira_worklog`)

```python
from scripts.jira_worklog import jira_get_worklog

# Get worklog entries for an issue
jira_get_worklog(issue_key="PROJ-123")
```

### Jira Projects (`scripts.jira_projects`)

```python
from scripts.jira_projects import (
    jira_get_all_projects,
    jira_get_project_issues,
    jira_get_project_versions
)

# Get all projects
jira_get_all_projects()

# Get issues in a project
jira_get_project_issues(project_key="PROJ", limit=100)

# Get project versions
jira_get_project_versions(project_key="PROJ")
```

### Jira Users (`scripts.jira_users`)

```python
from scripts.jira_users import jira_get_user_profile

# Get user profile
jira_get_user_profile(user_identifier="user@company.com")
```

### Confluence Pages (`scripts.confluence_pages`)

```python
from scripts.confluence_pages import confluence_get_page

# Get page by title
confluence_get_page(title="Meeting Notes", space_key="TEAM")

# Get page by ID
confluence_get_page(page_id="12345")
```

### Confluence Search (`scripts.confluence_search`)

```python
from scripts.confluence_search import confluence_search

# Search with CQL
confluence_search(
    query="space = DEV AND type = page AND text ~ 'API'",
    limit=25
)
```

### Confluence Comments (`scripts.confluence_comments`)

```python
from scripts.confluence_comments import confluence_get_comments

# Get comments on a page
confluence_get_comments(page_id="12345")
```

### Confluence Labels (`scripts.confluence_labels`)

```python
from scripts.confluence_labels import confluence_get_labels

# Get labels on a page
confluence_get_labels(page_id="12345")
```

### Bitbucket Projects (`scripts.bitbucket_projects`)

```python
from scripts.bitbucket_projects import (
    bitbucket_list_projects,
    bitbucket_list_repositories
)

# List all projects
bitbucket_list_projects(limit=25)

# List repositories in a project
bitbucket_list_repositories(project_key="PROJ", limit=50)
```

### Bitbucket Pull Requests (`scripts.bitbucket_pull_requests`)

```python
from scripts.bitbucket_pull_requests import (
    bitbucket_get_pull_request,
    bitbucket_get_pr_diff
)

# Get PR details
bitbucket_get_pull_request(
    project_key="PROJ",
    repository_slug="my-repo",
    pr_id=123
)

# Get PR diff
bitbucket_get_pr_diff(
    project_key="PROJ",
    repository_slug="my-repo",
    pr_id=123
)
```

### Bitbucket Files & Search (`scripts.bitbucket_files`)

```python
from scripts.bitbucket_files import (
    bitbucket_get_file_content,
    bitbucket_search
)

# Get file content
bitbucket_get_file_content(
    project_key="PROJ",
    repository_slug="my-repo",
    file_path="src/main.py",
    branch="develop"
)

# Search code
bitbucket_search(
    query="def authenticate",
    project_key="PROJ",
    search_type="code",
    limit=25
)
```

### Bitbucket Commits (`scripts.bitbucket_commits`)

```python
from scripts.bitbucket_commits import (
    bitbucket_get_commits,
    bitbucket_get_commit
)

# Get recent commits from a branch
bitbucket_get_commits(
    project_key="PROJ",
    repository_slug="my-repo",
    branch="master",
    limit=10
)

# Get details of a specific commit
bitbucket_get_commit(
    project_key="PROJ",
    repository_slug="my-repo",
    commit_id="1da11eaec25aed8b251de24841885c91493b3173"
)
```

## Response Data Structures

All functions return JSON strings with **flattened** data structures (not nested API responses).

### Jira Issue Structure

```json
{
  "key": "PROJ-123",
  "id": "10001",
  "summary": "Issue title",
  "description": "Issue description",
  "status": "In Progress",
  "issue_type": "Task",
  "priority": "High",
  "assignee": "user@company.com",
  "reporter": "reporter@company.com",
  "created": "2024-01-15T10:30:00.000+0000",
  "updated": "2024-01-16T14:20:00.000+0000",
  "labels": ["backend", "urgent"],
  "components": ["API", "Auth"],
  "custom_fields": {}
}
```

### Confluence Page Structure

```json
{
  "id": "12345",
  "title": "Page Title",
  "space_key": "DEV",
  "status": "current",
  "created": "2024-01-15T10:30:00.000Z",
  "updated": "2024-01-16T14:20:00.000Z",
  "author": "user@company.com",
  "version": 3,
  "url": "https://company.atlassian.net/wiki/spaces/DEV/pages/12345"
}
```

> **Note**: These are simplified structures. The original Jira API returns nested data like `{"key": "...", "fields": {"summary": "...", "status": {"name": "..."}}}`, but this skill flattens it for easier use.

## Error Handling

All functions return JSON strings. Check for errors:

```python
import json

result = jira_get_issue(issue_key="PROJ-999")
data = json.loads(result)

if not data.get("success", True):
    print(f"Error: {data['error']}")
    print(f"Type: {data['error_type']}")
else:
    print(f"Issue: {data['key']}")
```

### Error Types

- `ConfigurationError` - Missing environment variables
- `AuthenticationError` - Invalid credentials
- `ValidationError` - Invalid input parameters
- `NotFoundError` - Resource not found
- `APIError` - Atlassian API error
- `NetworkError` - Connection issues

## Philosophy

This skill provides:
- **Read-Only Access**: Query and retrieve data without modification
- **Token Efficiency**: Reduced context size by excluding write operations
- **Safety**: Prevents accidental data modifications
- **Flexibility**: Support for both Cloud and Data Center deployments
- **Consistency**: Unified error handling and response format

It does NOT provide:
- Write operations (create, update, delete)
- Direct API access (use the provided functions instead)
- Webhook handling or event processing
- Bulk import/export operations

**Best practices**:
- Always check return values for errors
- Use JQL/CQL for efficient searching
- For write operations, use the full `atlassian-skills` package

## Dependencies

```bash
pip install requests python-dotenv
```

Or use the requirements file:

```bash
pip install -r requirements.txt
```

