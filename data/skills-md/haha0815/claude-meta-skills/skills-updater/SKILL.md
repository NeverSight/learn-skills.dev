---
name: skills-updater
description: Check and update installed Claude Code skills from multiple sources (Claude plugins and npx skills). Scans for available updates, supports batch or individual updates with intelligent local change merging, and recommends popular skills from skillsmp.com and skills.sh marketplaces. Use when users want to update skills, check for new versions, discover trending skills, or manage their skill collection.
---

# Skills Updater

Manage, update, and discover Claude Code skills across multiple installation sources.

## Internationalization (i18n)

All scripts automatically detect user locale from environment variables and display output in the appropriate language.

**Supported Languages:**
- English (en) - Default
- Chinese (zh) - 中文

**Auto-detection order:**
1. `LANG` environment variable
2. `LC_ALL` environment variable
3. `LANGUAGE` environment variable
4. System locale

**Manual override:**
```bash
python scripts/check_updates.py --lang zh  # Force Chinese
python scripts/check_updates.py --lang en  # Force English
```

## Supported Sources

**Claude Code Plugins** (`~/.claude/plugins/`):
- `installed_plugins.json` - Tracks installed skills with versions
- `known_marketplaces.json` - Registered marketplace sources
- `cache/` - Installed skill files

**npx skills** (`~/.skills/` if present):
- Skills installed via `npx skills add <owner/repo>`
- Managed by skills.sh infrastructure

## Update Check Workflow

### Step 1: Scan Installed Skills

```bash
python scripts/check_updates.py
```

Output format:
```
📦 Installed Skills Status
━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Up-to-date (12):
   • skill-creator@daymade-skills (1.2.2)
   • github-ops@daymade-skills (1.0.0)
   ...

⬆️ Updates Available (3):
   • planning-with-files@planning-with-files
     Local: 2.5.0 → Remote: 2.6.1
   • superpowers@superpowers-marketplace
     Local: 4.0.3 → Remote: 4.1.0
   ...

⚠️ Unknown Version (2):
   • document-skills@anthropic-agent-skills (unknown)
   ...
```

### Step 2: Confirm Update Strategy

Present options to user:
1. **Update All** - Update all skills with available updates
2. **Select Individual** - Let user choose specific skills to update
3. **Skip** - Cancel the update process

### Step 3: Handle Local Modifications

Before updating, check for local modifications:

```bash
# Check if local skill has uncommitted changes
cd ~/.claude/plugins/cache/<marketplace>/<skill>/<version>
git status --porcelain
```

**If local changes detected:**
1. Create backup of modified files
2. Pull remote updates
3. Attempt 3-way merge
4. If conflicts:
   - Show conflict files to user
   - Offer manual resolution or keep local version

### Step 4: Execute Update

For Claude Code plugins:
```bash
# Trigger marketplace refresh and skill reinstall
# This uses Claude Code's built-in update mechanism
claude /install <skill-name>@<marketplace>
```

For npx skills:
```bash
npx skills add <owner/repo> --force
```

## Auto-Install After Marketplace Update

The `update_marketplace.py` script can automatically reinstall affected skills after updating a marketplace repository.

### Usage

```bash
# Update marketplace only (show affected skills)
python scripts/update_marketplace.py anthropic-agent-skills

# Update marketplace AND auto-reinstall affected skills
python scripts/update_marketplace.py anthropic-agent-skills --auto-install

# Output as JSON
python scripts/update_marketplace.py anthropic-agent-skills --json

# Force language
python scripts/update_marketplace.py anthropic-agent-skills --lang zh
```

### Output (Chinese locale)

```
📡 正在获取远程更新...

当前提交: e5c60158df67
远程提交: 69c0b1a06741
状态: 落后 6 个提交

📝 更新内容:
   • 69c0b1a Add link to Agent Skills specification website
   • be229a5 Fix links in agent skills specification
   ...

📦 受影响的技能: document-skills

📥 正在更新市场: anthropic-agent-skills
✅ 市场更新成功

🔄 正在重新安装受影响的技能...
   正在安装: document-skills
   ✅ 已安装: document-skills

✅ 所有受影响的技能已更新
```

### Workflow

1. **Fetch remote** - Git fetch to check for updates
2. **Compare commits** - Show how many commits behind
3. **List affected skills** - Find installed skills from this marketplace
4. **Pull updates** - Git pull to update local marketplace
5. **Auto-reinstall** - (with `--auto-install`) Reinstall each affected skill

## Skill Recommendations

### Fetch Trending Skills

```bash
python scripts/recommend_skills.py --source all
```

Sources:
- **skills.sh** - Leaderboard ranked by installs
- **skillsmp.com** - Curated marketplace (if accessible)

### Output Format

```
🔥 Trending Skills
━━━━━━━━━━━━━━━━━━

From skills.sh:
1. vercel-react-best-practices (25.5K installs)
   npx skills add vercel/react-best-practices

2. web-design-guidelines (19.2K installs)
   npx skills add webdesign/guidelines

3. remotion-best-practices (2.2K installs)
   npx skills add remotion/best-practices

💡 Personalized Recommendations:
Based on your installed skills (developer-tools, productivity):
- playwright-skill - Browser automation testing
- github-ops - GitHub CLI operations
```

### Install Recommended Skill

After showing recommendations, offer to install:

```
Would you like to install any of these skills?
1. Install by number (e.g., "1" or "1,3,5")
2. Install by name
3. Skip
```

## Version Detection Methods

### Primary: marketplace.json

Read version from remote marketplace.json:
```bash
curl -s "https://raw.githubusercontent.com/<owner>/<repo>/main/.claude-plugin/marketplace.json" | jq '.plugins[] | select(.name == "<skill>") | .version'
```

### Fallback: GitHub API

If marketplace.json unavailable or version not specified:
```bash
# Get latest release tag
curl -s "https://api.github.com/repos/<owner>/<repo>/releases/latest" | jq -r '.tag_name'

# Or latest commit on main
curl -s "https://api.github.com/repos/<owner>/<repo>/commits/main" | jq -r '.sha[:7]'
```

### Commit SHA Comparison

For skills tracking by commit (e.g., `e30768372b41`):
```bash
# Compare local gitCommitSha with remote HEAD
local_sha=$(jq -r '.plugins["<key>"][0].gitCommitSha' ~/.claude/plugins/installed_plugins.json)
remote_sha=$(curl -s "https://api.github.com/repos/<owner>/<repo>/commits/main" | jq -r '.sha')

if [ "$local_sha" != "$remote_sha" ]; then
  echo "Update available"
fi
```

## Smart Merge Strategy

When local modifications exist:

1. **Identify modified files**:
   ```bash
   git diff --name-only HEAD
   ```

2. **Categorize changes**:
   - SKILL.md customizations → Preserve user sections
   - scripts/ modifications → Keep local, note for review
   - references/ additions → Merge both
   - assets/ → Keep both versions if different

3. **Merge approach**:
   ```python
   # Pseudo-code for smart merge
   for file in modified_files:
       if file == 'SKILL.md':
           merge_skill_md(local, remote)  # Preserve user customizations
       elif file.startswith('scripts/'):
           backup_and_warn(local)  # User scripts need review
       else:
           three_way_merge(base, local, remote)
   ```

## User Interaction Patterns

### Check for Updates

User says: "检查 skills 更新" / "check skill updates" / "update my skills"

→ Run `scripts/check_updates.py` and display results

### Update Specific Skill

User says: "更新 skill-creator" / "update skill-creator"

→ Check and update only the specified skill

### Discover New Skills

User says: "推荐一些好用的 skills" / "recommend skills" / "popular skills"

→ Run `scripts/recommend_skills.py` and show curated list

### Full Update Workflow

User says: "更新所有 skills" / "update all skills"

→ Scan → Confirm → Handle merges → Update → Report results

## Error Handling

**Network errors**: Retry with exponential backoff, cache last known state

**Permission errors**: Suggest running with appropriate permissions

**Merge conflicts**: Show conflict markers, offer resolution options:
- Accept local (keep your changes)
- Accept remote (use upstream)
- Manual merge (show diff)

**Missing marketplace**: Inform user if source is no longer available

## Resources

### scripts/
- `check_updates.py` - Scan and compare installed vs remote versions
- `recommend_skills.py` - Fetch trending skills from marketplaces
- `update_marketplace.py` - Update marketplace repos and auto-reinstall skills
- `i18n.py` - Internationalization module (locale detection, translations)

### references/
- `marketplaces.md` - Supported marketplace documentation

## Adding New Languages

To add a new language, edit `scripts/i18n.py`:

1. Add translations to `TRANSLATIONS` dict:
```python
TRANSLATIONS["ja"] = {
    "checking_updates": "スキルの更新を確認中...",
    # ... other translations
}
```

2. Update `detect_locale()` to recognize the new locale:
```python
if lang_lower.startswith('ja'):
    return 'ja'
```
