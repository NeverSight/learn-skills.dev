---
name: release-notes
description: Generate user-friendly release notes for GitHub releases, app stores, or internal distribution. Triggered by requests to write release notes, draft a release, or summarize a version for users.
---

# Release Notes Generator

Generate polished release notes by analyzing code changes, PRs, and issues — not just commit messages.

## Gathering Context

### Step 1: Determine the version range

```bash
# Get the two most recent tags
CURRENT_TAG=$(git describe --tags --abbrev=0)
PREVIOUS_TAG=$(git describe --tags --abbrev=0 "$CURRENT_TAG^")

# Or if the user specifies a version:
# CURRENT_TAG="v2.4.0"
# PREVIOUS_TAG=$(git describe --tags --abbrev=0 "$CURRENT_TAG^")

# Get the date of the previous tag for filtering PRs/issues
SINCE_DATE=$(git log -1 --format=%aI "$PREVIOUS_TAG")
```

### Step 2: Gather signals (in order of usefulness)

**PRs merged since last release:**
```bash
gh pr list --state merged --search "merged:>=$SINCE_DATE" --json number,title,body,labels --limit 100
```

**Issues closed since last release:**
```bash
gh issue list --state closed --search "closed:>=$SINCE_DATE" --json number,title,body,labels --limit 100
```

**Diff between tags:**
```bash
git diff "$PREVIOUS_TAG".."$CURRENT_TAG" -- '*.ts' '*.js' '*.tsx' '*.jsx' '*.py' '*.go' '*.rs' ':!*.lock' ':!*.min.*'
```

**Files changed (reveals scope):**
```bash
git diff --name-only "$PREVIOUS_TAG".."$CURRENT_TAG"
```

**New or changed test descriptions:**
```bash
git diff "$PREVIOUS_TAG".."$CURRENT_TAG" -- '**/*.test.*' '**/*.spec.*' '**/test_*' '**/*_test.*'
```

**Config and dependency changes:**
```bash
git diff "$PREVIOUS_TAG".."$CURRENT_TAG" -- 'package.json' '*.toml' '*.yaml' '*.yml' '*.env.example' '*.config.*'
```

**Commit messages (last resort):**
```bash
git log --oneline "$PREVIOUS_TAG".."$CURRENT_TAG"
```

## Categorizing Changes

Sort changes by audience and impact:

### Audience tiers
- **All users** — features and fixes everyone will notice
- **Admins / power users** — config options, admin tools, API changes
- **Developers** — SDK changes, API additions (only if the product has a developer audience)

### Newsworthiness filter
- **Headline** — major feature, lead with this
- **Worth mentioning** — useful improvement or fix
- **Skip** — refactors, internal tooling, test changes, CI updates

Only include developer-facing changes if the product has a developer audience. Skip internal refactors, test improvements, and CI changes entirely unless they have user-facing impact.

## Writing Rules

- Lead with the most exciting change — the thing a user would want to know about
- Write for users, not developers: "You can now export reports as CSV" not "Implement CSV serialization in ReportExporter"
- Never mention file names, function names, or technical internals
- Use active voice: "Add dark mode" not "Dark mode was added"
- Be specific about the benefit: "Search results now load 3x faster" not "Improve performance"
- If you can't determine user impact, omit the change entirely
- Keep it scannable — short paragraphs or bullet points

## Output Format

Structure release notes with a highlight section and categorized details:

```markdown
# What's New in v2.4.0

**Headline:** You can now export any report as CSV — including custom reports and scheduled exports.

## New Features
- **Bulk CSV export** — Export any report type to CSV, including custom date ranges and filters
- **Keyboard shortcuts** — Navigate faster with Ctrl+K (search), Ctrl+N (new item), and more

## Improvements
- Search is noticeably faster for workspaces with 10k+ items
- The sidebar now remembers your collapsed/expanded preferences

## Bug Fixes
- Fixed a crash when opening files larger than 2GB
- Fixed billing summary showing incorrect totals for annual plans
```

## Example: Bad Commits → Good Release Notes

**Typical commit messages:**
```
fix stuff
wip
update deps
john's changes
PR #89
```

**What the skill produces by analyzing PRs, issues, diffs, and test descriptions:**

```markdown
# What's New in v3.0.0

**Headline:** Real-time collaboration is here — edit documents with your team simultaneously.

## New Features
- **Real-time collaboration** — See teammates' cursors and edits live as you work together
- **Slack integration** — Get notified in Slack when deployments fail or need approval

## Bug Fixes
- Fixed duplicate entries appearing in search results
- Fixed password reset emails not sending for accounts using SSO
```

## Publishing

After generating, ask the user where they want to publish:

- **GitHub Release** — offer to create it: `gh release create $CURRENT_TAG --title "v2.4.0" --notes-file release-notes.md`
- **Clipboard** — for pasting into app stores, Notion, email, etc.
- **File** — write to a file in the repo
