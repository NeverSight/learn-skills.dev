---
name: pgpm-plan-format
description: Understand and fix pgpm.plan file format issues. Use when encountering "Invalid line format" parse errors or when creating/editing pgpm.plan files.
compatibility: pgpm CLI, PostgreSQL
metadata:
  author: constructive-io
  version: "1.0.0"
---

# PGPM Plan File Format

Guide to the correct format for pgpm.plan files and common format errors.

## When to Apply

Use this skill when:
- Encountering "Invalid line format" errors from pgpm
- Creating new pgpm.plan files
- Adding changes with dependencies to a plan file
- Debugging plan file parse errors

## Plan File Format

### Basic Structure

A pgpm.plan file has the following structure:

```
%syntax-version=1.0.0
%project=module-name
%uri=module-name

change_name [dependencies] timestamp planner <email> # comment
```

### Change Line Format

The correct format for a change line is:

```
change_name [dep1 dep2] 2026-01-25T00:00:00Z planner-name <email@example.org> # optional comment
```

**Order matters!** The components must appear in this exact order:
1. `change_name` - The name/path of the change (e.g., `schemas/public/tables/users`)
2. `[dependencies]` - Optional, space-separated list of dependencies in square brackets
3. `timestamp` - ISO 8601 format: `YYYY-MM-DDTHH:MM:SSZ`
4. `planner` - Name of the person/entity who planned the change
5. `<email>` - Email in angle brackets
6. `# comment` - Optional comment starting with `#`

### Common Mistake: Dependencies After Email

**Wrong:**
```
data/seed_chunks 2026-01-25T00:00:00Z city-of-san-francisco <opensource@sfgov.org> [data/create_collection] # comment
```

**Correct:**
```
data/seed_chunks [data/create_collection] 2026-01-25T00:00:00Z city-of-san-francisco <opensource@sfgov.org> # comment
```

The parser expects dependencies immediately after the change name, not after the email.

## Error Messages

### "Line N: Invalid line format"

**Symptom:**
```text
PgpmError: Failed to parse plan file /path/to/pgpm.plan: Line 6: Invalid line format
```

**Cause:** The line doesn't match the expected format. Most commonly:
- Dependencies placed in wrong position
- Missing or malformed timestamp
- Missing angle brackets around email
- Invalid characters in change name

**Solution:** Check the line format matches:
```
change_name [deps] timestamp planner <email> # comment
```

### Parser Regex

The pgpm parser uses this regex pattern for change lines:
```javascript
/^(\S+)(?:\s+\[([^\]]*)\])?(?:\s+(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)(?:\s+([^<]+?))?(?:\s+<([^>]+)>)?(?:\s+#\s+(.*))?)?$/
```

This breaks down as:
- `(\S+)` - change name (required)
- `(?:\s+\[([^\]]*)\])?` - dependencies in brackets (optional)
- `(?:\s+(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)` - ISO timestamp
- `(?:\s+([^<]+?))?` - planner name
- `(?:\s+<([^>]+)>)?` - email in angle brackets
- `(?:\s+#\s+(.*))?` - comment

## Examples

### Change Without Dependencies

```
schemas/public/tables/users 2026-01-25T00:00:00Z dan <dan@example.org> # create users table
```

### Change With Single Dependency

```
schemas/public/tables/posts [schemas/public/tables/users] 2026-01-25T00:00:00Z dan <dan@example.org> # posts table
```

### Change With Multiple Dependencies

```
schemas/public/views/user_posts [schemas/public/tables/users schemas/public/tables/posts] 2026-01-25T00:00:00Z dan <dan@example.org>
```

### Cross-Module Dependency

```
data/seed [other-module:schemas/setup] 2026-01-25T00:00:00Z dan <dan@example.org> # depends on other module
```

## SQL File Dependencies

Dependencies can also be declared in SQL deploy files using the `-- requires:` comment:

```sql
-- Deploy module-name:schemas/public/tables/posts to pg
-- requires: schemas/public/tables/users

CREATE TABLE posts (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid REFERENCES users(id),
  content text
);
```

**Note:** Do not wrap SQL in `BEGIN`/`COMMIT` transactions - pgpm handles transactions automatically.

These are used by pgpm for dependency resolution but the plan file format is what gets parsed first.

## Quick Reference

| Component | Required | Position | Format |
|-----------|----------|----------|--------|
| change_name | Yes | 1st | No spaces, use `/` for paths |
| [dependencies] | No | 2nd | Space-separated in brackets |
| timestamp | Yes* | 3rd | `YYYY-MM-DDTHH:MM:SSZ` |
| planner | Yes* | 4th | Any text without `<` |
| email | Yes* | 5th | In angle brackets `<...>` |
| comment | No | 6th | After `# ` |

*Required if any metadata is present

## References

- Related skill: `pgpm-troubleshooting` for general pgpm issues
- Related skill: `pgpm-dependencies` for dependency management
- Related skill: `pgpm-changes` for adding changes to modules
