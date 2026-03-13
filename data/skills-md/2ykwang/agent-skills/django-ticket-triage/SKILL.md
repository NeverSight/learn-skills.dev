---
name: django-ticket-triage
version: 0.2.0
category: integrations
description: "Analyze a Django Trac ticket and produce a triage recommendation report."
argument-hint: "<ticket_id>"
---

Analyze Django ticket and provide triage recommendations.

**Prerequisites**:
- `python3` (standard library only; no extra Python packages required)
- `gh` — GitHub CLI ([install](https://cli.github.com/)). Run `gh auth login` to authenticate.
- Django source code — `git clone https://github.com/django/django.git` in the working directory (for Step 5: source code analysis)

Before starting, verify `python3` and `gh` are available. If `gh` is missing, show the install link and stop.
If `django/` directory is missing, warn the user and skip Step 5 (source code browsing).

**Arguments**:
- `$ARGUMENTS`: Trac ticket number (required, e.g., `36812`, `2750`)

**IMPORTANT**:
- DO NOT use WebFetch or Fetch for GitHub URLs. ALWAYS use the `gh` CLI command instead.
- For commits: `gh api repos/<owner>/django/commits/<sha>`
- For PRs: `gh pr view <number> --repo django/django` or `gh api repos/django/django/pulls/<number>`
- See `references/gh-examples.md` for more examples.

**Note**: `./scripts/` paths are relative to this SKILL.md file. Use the actual resolved path when executing.

---

## Step 1: Fetch Ticket Details

```bash
python3 ./scripts/trac.py get $ARGUMENTS
```

Identify the following:
- **Basic info**: summary, reporter, owner, component, version
- **Status**: status, resolution, triage_stage, has_patch
- **Keywords**: Extract key terms from keywords field
- **Ticket type**: Bug report / Feature request / Documentation / Cleanup
- **History**: Review comments for previous discussions, related PRs, prior patch attempts

---

## Step 2: Search for Duplicates and Related Tickets

### 2-1. Trac Search (at least 2-3 queries)

```bash
# Search by key keywords
python3 ./scripts/trac.py search "<key keywords>"

# Search by error message or class/function name
python3 ./scripts/trac.py search "<error message or class name>"

# Search by component + keyword combination
python3 ./scripts/trac.py search "<component> <keyword>"
```

### 2-2. Review Potentially Related Tickets

Fetch details for related tickets found (top 3-5):

```bash
python3 ./scripts/trac.py get <related_ticket_id>
```

---

## Step 3: Search Related PRs (GitHub)

Find PRs linked to the ticket:

```bash
# Search PRs mentioning ticket number in title/body
gh search prs "Fixed #$ARGUMENTS" --repo django/django --limit 10
gh search prs "#$ARGUMENTS" --repo django/django --limit 10

# Or search by Trac ticket URL
gh search prs "code.djangoproject.com/ticket/$ARGUMENTS" --repo django/django --limit 10
```

If related PRs exist, review details:

```bash
gh pr view <pr_number> --repo django/django --json title,state,body,comments
```

---

## Step 4: Search Django Forum

Check for forum discussions related to the ticket:

```bash
# Search by ticket number
python3 ./scripts/forum.py ticket $ARGUMENTS

# If no results, search internals category by keywords
python3 ./scripts/forum.py search "<key keywords>" --category=internals
```

---

## Step 5: Browse Related Source Code (If Applicable)

For tickets requiring code changes, check related code in `django/` directory:

**Find related files:**
- Use the **Glob tool** with pattern `django/**/<relevant_file>.py` to find files by name
- Use the **Grep tool** with pattern `<class or function name>` in `django/` to search code

**Find related tests:**
- Use the **Glob tool** with pattern `tests/**/test_*.py` to find test files
- Use the **Grep tool** with pattern `<related keyword>` in `tests/` to search test code

Identify:
- Location of the problematic code
- Existing test coverage
- Scope of changes needed

---

## Step 6: Validity Assessment

### For Bug Reports

| Check | Question |
|-------|----------|
| Reproducibility | Are reproduction steps clear? Is there minimal reproduction code? |
| Version | Does it occur on latest version (main branch)? |
| Django's responsibility | Is this a Django bug or user code/configuration issue? |
| Intended behavior | Does it differ from documented behavior? Is it by design? |
| Supported version | Is this a supported Django version? |
| Security | Is this a security issue? (Should NOT be on Trac) |

### For Feature Requests

| Check | Question |
|-------|----------|
| Generality | Is this useful to enough users? |
| Django philosophy | Does it align with Django's design philosophy? |
| Alternatives | Can this be solved with a third-party package? |
| Backwards compatibility | Does it break existing code? |
| Complexity | Is the maintenance burden worth the value? |
| DEP required | Is this a large change requiring a DEP? |

### Red Flags (Likely Invalid)

- Security issue reported on public Trac (should go to security@djangoproject.com)
- Only affects unsupported Django versions
- "Only I need this" type of feature
- Works as documented (user misunderstanding)
- Third-party package issue, not Django core

---

## Step 7: Triage Decision

Read `references/triage-stages.md` for stage definitions and duplicate criteria.

---

## Step 8: Save Report and Output Summary

### 8-1. Save Full Report to File

Create directory if needed and save the full report:

```bash
mkdir -p triage-reports
```

Read `references/report-template.md` and use it as the report format. Write the full report to `triage-reports/<ticket_id>.md` using the Write tool.

### 8-2. Output Summary to Terminal

Read the terminal summary format from `references/report-template.md` and output a brief summary.
