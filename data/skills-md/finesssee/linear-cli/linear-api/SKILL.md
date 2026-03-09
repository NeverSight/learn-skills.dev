---
name: linear-api
description: Execute raw GraphQL queries and mutations against the Linear API. Use for advanced operations not covered by other commands.
allowed-tools: Bash
---

# Raw GraphQL API

```bash
# Run a query
linear-cli api query '{ viewer { id name email } }'

# Query with variables
linear-cli api query -v teamId=abc '{ team(id: $teamId) { name } }'

# Run a mutation
linear-cli api mutate -v title="Bug" '
  mutation($title: String!) {
    issueCreate(input: { title: $title, teamId: "..." }) {
      issue { id identifier }
    }
  }
'

# Pipe query from file
cat query.graphql | linear-cli api query -
```

## Flags

| Flag | Purpose |
|------|---------|
| `-v key=val` | GraphQL variables |
| `--output json` | JSON output |
| `--compact` | Compact JSON |

## Exit Codes

`0`=Success, `1`=Error, `2`=Not found, `3`=Auth error
