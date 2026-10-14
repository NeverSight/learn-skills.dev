---
name: bmad-os-changelog
description: "Analyzes changes since last release and drafts them directly into the project's CHANGELOG.md. Use when users requests 'update the changelog' or 'prepare changelog release notes'"
---

# Changelog

## ⚠️ IMPORTANT - READ FIRST

**This skill ONLY updates CHANGELOG.md. The changelog file IS the canvas — always write the draft into it. Never dump the proposed entry into the chat.**

- **DO** write the new version entry directly into the project's CHANGELOG.md and open it for review
- **DO** ask any clarifying questions first (version, which plugin, how to categorize an ambiguous change) — but the answer always lands in the file, not the chat
- **DO NOT** paste the full proposed changelog into the chat instead of writing it to the file
- **DO NOT** trigger any GitHub release workflows
- **DO NOT** run any other skills or workflows automatically
- **DO NOT** make any commits

Releases are handled by each repo's GitHub Actions release workflow. Your job ends once CHANGELOG.md is updated. After the user merges the changelog change, suggest they run the release workflow via `gh workflow run` (or via the Actions UI) — but never trigger it yourself.

## Input
Project path (or run from project root)

## Step 1: Identify Current State

### 1a: Check for Marketplace Plugin Metadata

Look for `.claude-plugin/marketplace.json` in the project root. If found, read it to understand plugin versioning:

```json
{
  "plugins": [
    { "name": "plugin-a", "version": "1.2.0" },
    { "name": "plugin-b", "version": "2.0.1" }
  ]
}
```

**Single plugin:** Use its version as the changelog version. Confirm with the user: *"marketplace.json shows plugin-name at vX.Y.Z. Drafting changelog for this version - correct?"*

**Multiple plugins:** Ask the user which plugin(s) need changelog entries and what the new version(s) will be. Each plugin gets its own section in the changelog (see Step 3 format).

**No marketplace.json found:** Fall back to git tags for versioning (original behavior).

### 1b: Determine Version Boundaries

- Get the latest released tag (or, for marketplace repos, the last changelog entry for the relevant plugin)
- Get current/target version
- Verify there are commits since the last release

## Step 2: Launch Explore Agent

Use `thoroughness: "very thorough"` to analyze all changes since the last release tag.

**Key: For each merge commit, look up the merged PR/issue that was closed.**
- Use `gh pr view` or git commit body to find the PR number
- Read the PR description and comments to understand full context
- Don't rely solely on commit merge messages - they lack context

**Analyze:**

1. **All merges/commits** since the last tag
2. **For each merge, read the original PR/issue** that was closed
3. **Files changed** with statistics
4. **Categorize changes:**
   - 🎁 **Features** - New functionality, new agents, new workflows, improvements
   - 💥 **Breaking Changes** - Changes that may affect users
   - Anything else that doesn't fit the above categories can be listed as "Other Changes" or similar that are interesting for users to know but don't fit the above categories.

**Provide:**
- Comprehensive summary of ALL changes with PR context
- Categorization of each change
- Identification of breaking changes
- Significance assessment (major/minor/trivial)

## Step 3: Generate Draft Changelog

**Single-plugin or tag-based repos:**
```markdown
## vX.Y.Z - [Date]

* [Change 1 - categorized by type]
* [Change 2]
```

**Multi-plugin repos** (when marketplace.json has multiple plugins):
```markdown
## plugin-name - vX.Y.Z - [Date]

* [Change 1 - categorized by type]
* [Change 2]

## other-plugin - vA.B.C - [Date]

* [Change 3]
```

Each plugin gets its own H2 section. Only include plugins that actually have changes. Changes that affect shared code or the repo generally should be listed under whichever plugin(s) they impact.

**Guidelines:**
- Present tense ("Fix bug" not "Fixed bug")
- Most significant changes first
- Group related changes
- Clear, concise language
- For breaking changes, clearly indicate impact
- **Read `references/writing-quality.md` before composing.** Apply **Tier 1 (Universal AI tells)** to every bullet — banned vocabulary ("robust", "comprehensive", "leverage", "game-changing"), stakes inflation, "it's not X, it's Y". Tier 2 (prose mechanics) governs any flowing prose you write; the bullet entries themselves stay terse (Tier 2 exempts bullets).

## Step 4: Write the Draft into CHANGELOG.md

Ask any clarifying questions first (version number, which plugin, how to categorize an ambiguous change). Once resolved, run a **writing-quality pass with a subagent** (Task tool, `subagent_type=general-purpose`): hand it the drafted entry and `references/writing-quality.md`, have it apply **Tier 1** — flag every Universal AI tell (banned vocab, stakes inflation, "it's not X, it's Y") — and return fixes, and apply them. Then write the entry — don't ask for approval of pasted-in-chat text:

1. Write the new entry directly into CHANGELOG.md (insert at top, after the `# Changelog` header) and open the file so the user reviews it **in the changelog itself**. The file is the canvas — do not paste the full entry into the chat. A one- or two-line summary of what you added ("Added v6.2.0 entry: 4 features, 1 breaking change") is all that belongs in the chat.
2. Tell the user: once the changelog branch/PR is merged to main, they can trigger the repo's release workflow to tag, bump versions, and publish. Show them the command, e.g.:
   ```bash
   gh workflow run publish.yaml --ref main
   ```
   Adjust the workflow filename to match what's in `.github/workflows/` (commonly `publish.yaml` or `release.yaml`). If the workflow takes inputs (channel, bump type), include them — e.g. `-f channel=latest -f bump=minor`.
3. STOP. Do not run the workflow yourself. Do not make any commits.

**DO NOT:**
- Paste the full proposed changelog into the chat instead of writing it to CHANGELOG.md
- Trigger any GitHub workflows
- Run any other skills
- Make any commits
- Do anything beyond updating CHANGELOG.md
