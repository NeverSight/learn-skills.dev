---
name: jira
description: >
  View and interact with Jira tickets using the jira CLI. Use when the user
  asks to view a ticket, list assigned issues, check sprint status, search
  issues, add comments, or change ticket status via a Jira URL or key.
---

# Jira CLI Skill

Interact with Jira tickets using the `jira` command-line tool.

## Usage

Use this skill when the user:

- Asks to view a Jira ticket
- Wants to list issues assigned to them
- Needs to check ticket status or details
- Provides a Jira URL or ticket key (e.g., `ADP-1234`)

## Common Commands

### View a Ticket

```bash
jira issue view <TICKET_KEY>
```

Example: `jira issue view ADP-6405`

If given a Jira URL like `https://aircall-product.atlassian.net/browse/ADP-6405`, extract the ticket key (`ADP-6405`) and use the view command.

### List My Issues

```bash
jira issue list -a$(jira me)
```

### List Issues in a Sprint

```bash
jira sprint list --current
jira sprint list --current -a$(jira me)
```

### Search Issues

```bash
jira issue list -q "project = ADP AND status = 'In Progress'"
```

### Add a Comment

```bash
jira issue comment add <TICKET_KEY> -b "<COMMENT_BODY>"
```

### Move Issue Status

```bash
jira issue move <TICKET_KEY> "<STATUS>"
```

## Notes

- Attachments referenced in tickets are not viewable via CLI - suggest opening the Jira URL directly
- The CLI may truncate long descriptions - recommend viewing in browser for full context
- Ticket keys are case-insensitive but conventionally uppercase (e.g., `ADP-1234`)
