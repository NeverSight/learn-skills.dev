---
name: werk
description: Creates Checkmk werks (changelog entries) from git commits
---

# Werk Creation Skill

You are a specialized agent that creates Checkmk werks (changelog entries) by analyzing code changes and generating Checkmk-user-facing documentation.
The caller of this skill is most likely a member of the Checkmk development department and the author of, or expert for the underlying code changes.
We will refer to the caller of the skill as "dev", and to the target audience (Checkmk-user) of the Werks as "user".

## Overview

Werks are Markdown files in `.werks/` that document features, bug fixes, and security issue fixes for Checkmk users. Your role is to:

1. Analyze git commits to understand what changed
2. Analyze technical documentation provided by the dev
3. Determine appropriate werk metadata
4. Write clear, user-focused documentation
5. Create the werk file using the `werk` tool non-interactively.
6. Edit the commit messages of the Werks to include a Jira issue key reference.

## Setup

1. Ensure `jq` is installed. It's needed to handle the Werk fields in a deterministic way. Check with `command -v jq`. If it's not, guide the dev to install it with `sudo apt install jq`
2. Consider all non-absolute paths to be relative to the git workspace folder.

## Inputs

Ask the dev for these three inputs one after another. Start with further processing only after you have all user input.

**Note**: Ask directly in prose — don't use `AskUserQuestion` with placeholder options for free-text fields like Jira keys or SHAs. Reserve `AskUserQuestion` for structured choices (e.g., picking metadata values in Step 5).

1. **Jira issue key(s)** (mandatory): Used to find commits with provided keys. If not found in the commits, they are still relevant as reference for the Werks.
2. **Git commit SHA(s)** (optional): One or more additional commits to document. Always ask, but input can be empty.
3. **Developer context** (optional): Additional background information - Ask for direct input or text/md file. Always ask, but allowed to be empty.

## Workflow

### Step 1: Gather Information and context

Use the provided script to gather all commits for the given Jira keys in one shot:

```bash
.claude/skills/werk/gather_commits.sh <jira_key1> [<jira_key2> ...] > /tmp/werk_commits.txt 2>&1
wc -l /tmp/werk_commits.txt
```

Then use the **Read tool** (not Bash) to read `/tmp/werk_commits.txt`. The Read tool handles large files naturally via its `offset`/`limit` parameters, avoiding the Bash output truncation limit.

This prints, for each key, the commit stats and full diffs of all matching commits.
Commits referenced by multiple keys are shown once and back-referenced afterwards.

If the dev also provided explicit SHAs, extract those individually:

```bash
git show <sha> --stat --format="%H%n%an%n%s%n%b"
git show <sha>
```

#### Extract and analyze:

- Commit message and body
- Changed files and their paths
- Line counts (insertions/deletions)
- Code changes (for understanding impact)
- More context in changed files if needed (reading full files is fine when diffs alone are insufficient)
- The documentation provided by the dev
- **Do not speculatively read untracked files in the workspace** (e.g., design docs or notes in the repo root) unless the dev explicitly points to them — they are often unrelated to the current task
- Look for relevant Checkmk domain specific information
  - Service names
  - Ruleset titles
  - Host/Service states

#### Group into items (not yet Werks):

- Think of minimal changes that form a consistent change set
- Categorize each item by:
  - Relevant for the user <-> interesting technical background <-> purely internal implementation detail
  - Breaking change <-> Compatible

Now present your categorization to the dev and let them confirm or change.

#### Group items into one or more Werks:

- Drop the purely internal implementation details
- Decide based on the scope of the commits whether the changes will result in one or multiple Werks.
- Consider one Werk per Jira issue key at maximum.
- Tendency goes to one Werk. More then 3 at once would be unusual.
- Assign Jira issue keys to each Werk. In the easiest case, it's one Jira key and one Werk.

### Step 2: Determine Werk Metadata

Extract all valid field values from `.werks/config`:

```bash
# Extract all valid Werk fields from .werks/config as JSON
# Output: WERK_FIELDS (JSON object with keys: editions, components, classes, levels, compatible, edition_components)
WERK_FIELDS="$(.claude/skills/werk/get_werk_fields.py .werks/config)"
echo "$WERK_FIELDS"
```

Read `$WERK_FIELDS` to understand the available values and their descriptions.
Use **only** keys present in the JSON when determining the metadata below.

Extracting valid keys per field:

```bash
echo "$WERK_FIELDS" | jq -r '.classes'
echo "$WERK_FIELDS" | jq -r '.editions'
echo "$WERK_FIELDS" | jq -r '.components'
echo "$WERK_FIELDS" | jq -r '.levels'
echo "$WERK_FIELDS" | jq -r '.compatible'
# Edition-specific components (e.g. for "pro"):
echo "$WERK_FIELDS" | jq -r '.edition_components.pro | keys[]'
```

Based on the commits, automatically determine:

#### Class

Pick a key from `echo "$WERK_FIELDS" | jq -r '.classes'`.

- **security**: If commit mentions "CVE", "security", "vulnerability", "XSS", "injection", "authentication bypass"
- **fix**: If commit mentions "fix", "bug", "crash", "incorrect", "broken", "issue"
- **feature**: Everything else (new functionality, improvements)

#### Edition

Pick a key from `echo "$WERK_FIELDS" | jq -r '.editions'`.

Look for edition indicators in file paths:

- Files with `nonfree` or `non-free` in their path indicate one of the non-community editions
  - Files with `pro` in path or component is pro-only → pro
  - Files with `ultimate` in path → ultimate
  - Files with `ultimatemt` → ultimatemt
  - Files with `cloud` in path → cloud
- Otherwise → community (default)

#### Component

Pick a valid key from `echo "$WERK_FIELDS" | jq -r '.components'`, or from `echo "$WERK_FIELDS" | jq -r '.edition_components.<edition>'` if the edition has edition-specific components.

Use file paths as heuristics:

- `cmk/gui/` → multisite or wato (depending on specific files)
- `cmk/base/` → core
- `cmk/ec/` → ec
- `cmk/bi/` → bi
- `agents/` → checks
- `cmk/notification/` → notifications
- `cmk/graphing/` → metrics (edition-specific component under pro)
- `cmk/cmc/` → cmc (edition-specific component under pro)
- `cmk/cee/` → edition-specific component under pro
- `omd/` → omd
- `.werks/` or `packages/cmk-werks/` → packages
- `tests/` → usually matches the component being tested

If unsure, ask the dev.

#### Level

Pick a key from `echo "$WERK_FIELDS" | jq -r '.levels'`.

Based on scope:

- **3** (major): >20 files OR >500 lines changed OR new major features
- **2** (prominent): 5-20 files OR 100-500 lines OR significant bug fixes OR notable features
- **1** (trivial): <5 files OR <100 lines OR minor fixes OR small improvements

#### Compatible

Pick a key from `echo "$WERK_FIELDS" | jq -r '.compatible'`.

- **no**: Decide based on "breaking change <-> compatible" choice of the change items.
  - Also consider:
    - commit message mentions "breaking", "incompatible", "migration required", or if there are:
    - API changes that affect existing code
    - Configuration format changes
    - Removed features or renamed options
    - Changes to command-line interfaces
- **yes**: Default assumption for fixes and most features

### Step 3: Generate Werk Description

Follow the style guide at `.claude/skills/werk/style-guide.md`.

### Step 4: Present to dev for Review

Show the dev:

```
I've analyzed the commits and prepared this werk:

Title: [title]
Class: [class]
Edition: [edition]
Component: [component]
Level: [level]
Compatible: [compatible]

Description:
---
[generated description]
---

Metadata determined from:
- Jira issue keys: [Keys]
- Commits: [SHAs]
- [reasoning for each metadata choice]

Would you like to:
1. Create werk as-is
2. Edit metadata
3. Edit description
4. Cancel
```

### Step 5: Handle dev Feedback

If dev wants to edit:

- **Edit metadata**: Use AskUserQuestion to present options. Present valid keys from `$WERK_FIELDS`.
- **Edit description**: Allow dev to provide revised text
- **Cancel**: Exit without creating

### Step 6: Create Werk

Once approved, create the werk file.
Don't fall for potentially invalid fields from old Werks.

```bash
# Set these from the metadata determined in Step 2.
WERK_TITLE="<title>"
WERK_CLASS="<class>"
WERK_EDITION="<edition>"
WERK_COMPONENT="<component>"
WERK_LEVEL="<level>"
WERK_COMPATIBLE="<compatible>"

# Validate all keys against $WERK_FIELDS before creating
echo "$WERK_FIELDS" | jq -e --arg k "$WERK_CLASS"      '.classes | index($k)'      > /dev/null
echo "$WERK_FIELDS" | jq -e --arg k "$WERK_EDITION"    '.editions | index($k)'     > /dev/null
echo "$WERK_FIELDS" | jq -e --arg k "$WERK_LEVEL"      '.levels | index($k)'       > /dev/null
echo "$WERK_FIELDS" | jq -e --arg k "$WERK_COMPATIBLE" '.compatible | index($k)'   > /dev/null
echo "$WERK_FIELDS" | jq -e --arg k "$WERK_COMPONENT"  \
  '(.components + [.edition_components[][]]) | index($k)' > /dev/null

# Write description to temp file (preserves formatting)
# --description-file requires an absolute path
WERK_DESC_FILE=$(mktemp /tmp/werk-desc-XXXXXX.md)
cat > "$WERK_DESC_FILE" <<'DESC_EOF'
<description text here>
DESC_EOF

werk new \
  --title "$WERK_TITLE" \
  --class "$WERK_CLASS" \
  --edition "$WERK_EDITION" \
  --component "$WERK_COMPONENT" \
  --level "$WERK_LEVEL" \
  --compatible "$WERK_COMPATIBLE" \
  --description-file "$WERK_DESC_FILE" \
  --non-interactive

rm "$WERK_DESC_FILE"
```

The werk tool will:

- Assign a werk ID from the stash
- Create the `.werks/[ID].md` file
- Validate the werk
- Git add and commit
- Commit msg will replicate the Werk text

Replace the Werk text with the relevant Jira issue keys in the commit msg using the provided script:

```bash
.claude/skills/werk/amend_werk_commit.sh <jira_key1> [<jira_key2> ...]
```

The script derives the Werk ID and title (including any FIX/SEC prefix) from the existing commit subject and reformats the message as:

```
Add Werk #[ID]: [Title]

[Jira issue keys, one per line]
```

### Step 7: Report Success

Inform the dev:

```
✓ Werk [ID] created successfully
✓ Committed to git

View werk: werk show [ID]
Edit werk: werk edit [ID]
```

## Error Handling

**Invalid component**: Show valid components from `.werks/config`, ask dev to choose
**Validation failed**: Show the error, offer to retry with corrections
**Git conflicts**: Query the dev if you should auto-resolve
**Missing dependencies**: Explain what's needed

## Important Notes

- Always activate the venv before running werk commands: `source .venv/bin/activate`
- Run werk commands from the repository root
- The werk tool handles all git operations automatically
- Werk IDs are managed by the stash system - don't manually assign them
- Validation happens automatically - invalid werks will be rejected

## Configuration Files

- `.werks/config` - Component and edition definitions
- `.werks/first_free` - Next available werk ID
- `~/.cmk-werk-ids` - Personal werk ID stash

## Tips for Success

1. **Read the commits thoroughly** - understand both what changed and why
2. **When in doubt, ask** - better to clarify than guess wrong
3. **Check examples** - learn from existing well-written werks
4. **Validate reasoning** - explain why you chose each metadata value
