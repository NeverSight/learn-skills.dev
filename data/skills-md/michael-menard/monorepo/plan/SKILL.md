---
name: plan
description: "Create, update, or list plans in the KB. Generates metadata (slug, type, tags, summary) and upserts atomically via MCP tools."
---

# /plan — Create, Update, or List Plans

## Usage

```
/plan create <file_path> [--prefix=X] [--priority=P1-P5] [--type=X] [--feature-dir=X]
/plan update <plan_slug> [--priority=X] [--status=X] [--prefix=X] [--type=X] [--tags=a,b,c]
/plan list [args]
```

## Subcommands

### `/plan create` — Create a New Plan

Reads a plan from a text/markdown file, extracts the title, generates metadata, writes the canonical file to `~/.claude/plans/`, and upserts to the KB in one step.

#### Step 1 — Parse Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| file_path | yes | Path to a text or markdown file containing the plan |
| `--prefix=X` | no | Story prefix (e.g., `APIP`, `DASH`) |
| `--priority=P1-P5` | no | Priority level (default: `P3`) |
| `--type=X` | no | Plan type override (feature, refactor, migration, infra, tooling, workflow, audit, spike) |
| `--feature-dir=X` | no | Target feature directory |

Read the file using the Read tool. The file must exist.

#### Step 2 — Extract Title

Extract the title from the first `# Heading` line in the file. If no `#` heading exists, use the filename (without extension) as the title.

#### Step 3 — Generate Slug

1. Take the title
2. Lowercase it
3. Replace non-alphanumeric characters with hyphens
4. Collapse multiple consecutive hyphens into one
5. Trim leading/trailing hyphens
6. Truncate to 60 characters
7. Check uniqueness: call `kb_list_plans` with `limit: 100`, scan returned slugs
8. If collision: append `-2`, `-3`, etc. until unique

#### Step 4 — Infer Plan Type

If `--type` was not provided, infer from plan text using keyword matching (first match wins):

| Type | Keywords |
|------|----------|
| feature | `new feature`, `product feature`, `user-facing`, `ui component`, `gallery`, `dashboard` |
| refactor | `refactor`, `restructur`, `clean up`, `rename`, `consolidat` |
| migration | `migrat`, `import`, `move to`, `port to`, `convert` |
| infra | `infrastructure`, `deployment`, `docker`, `aws`, `lambda`, `terraform`, `ci/cd` |
| tooling | `tooling`, `developer experience`, `dx `, `cli`, `script`, `automation` |
| workflow | `workflow`, `agent`, `orchestrat`, `pipeline`, `scrum`, `story generation` |
| audit | `audit`, `coverage`, `gap analysis`, `review all`, `assess` |
| spike | `spike`, `investigation`, `experiment`, `explore`, `poc`, `proof of concept` |

Default to `feature` if no keywords match.

#### Step 5 — Infer Tags

Scan the plan text (case-insensitive) for keyword groups. If any keyword in a group matches, include that tag. Deduplicate and take the first 10.

| Tag | Keywords |
|-----|----------|
| database | `migration`, `schema`, `postgres`, `drizzle`, `sql` |
| frontend | `react`, `component`, `ui`, `tailwind`, `shadcn`, `page` |
| backend | `lambda`, `api`, `endpoint`, `handler`, `server` |
| testing | `playwright`, `vitest`, `e2e`, `test coverage`, `cucumber` |
| knowledge-base | `knowledge base`, `kb_`, `mcp`, `embedding` |
| story-generation | `story generation`, `pm-story`, `pm-generate`, `elab` |
| performance | `token usage`, `performance`, `bottleneck`, `caching`, `optimiz` |
| worktree | `worktree`, `branch`, `git` |

#### Step 6 — Extract Summary

Find the first non-heading, non-empty paragraph in the plan text (skip lines starting with `#` and blank lines). Join consecutive non-blank, non-heading lines into one string. Truncate to 500 characters.

#### Step 7 — Extract Additional Metadata

- **story_prefix**: If `--prefix` not provided, scan for the first `UPPER-NNN` pattern (e.g., `WKFL-001`) and extract the prefix
- **estimated_stories**: Scan for patterns like `N stories`, `~N stories` and extract the number
- **feature_dir**: If `--feature-dir` not provided, scan for `plans/future/platform/<dir>` or `plans/future/<dir>` patterns

#### Step 8 — Write Markdown File

Copy the plan content to `~/.claude/plans/{slug}.md` using the Write tool.

If the file content did NOT start with a `# Title` heading, prepend one:
```markdown
# {title}

{file content}
```

#### Step 9 — Upsert to KB

Load the `kb_upsert_plan` MCP tool via ToolSearch, then call it with:

```json
{
  "plan_slug": "{slug}",
  "title": "{title}",
  "raw_content": "{full markdown content}",
  "summary": "{extracted summary}",
  "plan_type": "{inferred or specified type}",
  "status": "draft",
  "priority": "{specified or P3}",
  "tags": ["{inferred tags}"],
  "source_file": "~/.claude/plans/{slug}.md",
  "story_prefix": "{if found}",
  "feature_dir": "{if found}",
  "estimated_stories": "{if found}"
}
```

#### Step 10 — Display Confirmation

Output a summary:

```
Plan created successfully.

  Slug:     {slug}
  Title:    {title}
  Type:     {plan_type}
  Priority: {priority}
  Status:   draft
  Tags:     {tags, comma-separated}
  Source:   {original file_path}
  File:     ~/.claude/plans/{slug}.md

Next steps:
  /plans                           — verify it appears in the list
  /pm-bootstrap-workflow {slug}    — generate stories from this plan
  /plan update {slug} --priority=P1  — adjust metadata
```

---

### `/plan update` — Update Plan Metadata

Lightweight update of an existing plan's metadata fields.

#### Step 1 — Parse Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| plan_slug | yes | The slug of the plan to update |
| `--priority=X` | no | New priority (P1-P5) |
| `--status=X` | no | New status (draft, accepted, stories-created, in-progress, implemented, superseded, archived) |
| `--prefix=X` | no | New story prefix |
| `--type=X` | no | New plan type |
| `--tags=a,b,c` | no | New tags (comma-separated, replaces existing) |
| `--title=X` | no | New title |
| `--feature-dir=X` | no | New feature directory (use `none` to clear) |
| `--estimated-stories=N` | no | New estimated stories count (use `none` to clear) |

At least one optional argument must be provided.

#### Step 2 — Call kb_update_plan

Load the `kb_update_plan` MCP tool via ToolSearch, then call it with the plan_slug and only the provided fields.

For `--tags`, split on commas and pass as an array.
For fields set to `none`, pass `null` to clear them.

#### Step 3 — Display Confirmation

```
Plan "{plan_slug}" updated.

  Changed: {list of changed fields with new values}
```

---

### `/plan list` — List Plans

Delegates to the `/plans` skill. Pass through any arguments.

Run: `/plans {args}`

## MCP Tools Used

- `kb_upsert_plan` — Insert or update a plan record (load via `ToolSearch` first)
- `kb_update_plan` — Lightweight metadata update (load via `ToolSearch` first)
- `kb_list_plans` — List plans for slug uniqueness check and listing (load via `ToolSearch` first)

**Important:** These tools must be loaded via `ToolSearch` before calling. Use:
- `ToolSearch({ query: "select:mcp__knowledge-base__kb_upsert_plan" })` for create
- `ToolSearch({ query: "select:mcp__knowledge-base__kb_update_plan" })` for update
- `ToolSearch({ query: "select:mcp__knowledge-base__kb_list_plans" })` for list/uniqueness check

**Fallback:** If `kb_upsert_plan` or `kb_update_plan` are not available in the deferred tools list (MCP server may need restart), inform the user:

```
The kb_upsert_plan / kb_update_plan MCP tools are not currently available in the
deferred tools registry. The MCP server likely needs a restart to pick them up.

To fix: restart the knowledge-base MCP server, then retry this command.

The plan markdown file has been written to ~/.claude/plans/{slug}.md.
You can sync it to the DB later with:
  pnpm tsx apps/api/knowledge-base/src/scripts/migrate-plans-to-kb.ts
```
