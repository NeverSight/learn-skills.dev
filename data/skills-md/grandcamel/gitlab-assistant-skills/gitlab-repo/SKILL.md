---
name: "gitlab-repo"
description: "GitLab repository operations. ALWAYS use this skill when user wants to: (1) clone repositories, (2) fork projects, (3) view repo info, (4) create new projects, (5) archive/delete repos, (6) manage repo settings."
version: "1.0.0"
author: "GitLab-Assistant-Skills"
license: "MIT"
allowed-tools: ["Bash", "Read", "Glob", "Grep"]
---

# Repository Skill

Repository and project operations for GitLab using the `glab` CLI.

## Quick Reference

| Operation | Command | Risk |
|-----------|---------|:----:|
| Clone repo | `glab repo clone <repo>` | - |
| Fork repo | `glab repo fork <repo>` | ⚠️ |
| View repo | `glab repo view` | - |
| Create repo | `glab repo create` | ⚠️ |
| Search repos | `glab repo search <query>` | - |
| Archive repo | `glab repo archive` | ⚠️⚠️ |
| Delete repo | `glab repo delete` | ⚠️⚠️⚠️ |
| List contributors | `glab repo contributors` | - |

**Risk Legend**: - Safe | ⚠️ Caution | ⚠️⚠️ Warning | ⚠️⚠️⚠️ Danger

## When to Use This Skill

**ALWAYS use when:**
- User wants to clone, fork, or create repositories
- User mentions "repo", "repository", "project", "clone", "fork"
- User wants to manage project settings

**NEVER use when:**
- User wants to work with specific repo content (use git directly)
- User wants to manage deploy keys (use gitlab-deploy-key skill)

## Available Commands

### Clone Repository

```bash
glab repo clone <repo> [directory] [options]
```

**Arguments:**
- `<repo>` - Repository path, URL, or project ID
- `[directory]` - Optional local directory name

**Options:**
| Flag | Description |
|------|-------------|
| `-g, --group=<group>` | Clone all repos in a group |
| `-p, --preserve-namespace` | Clone into subdirectory based on namespace |
| `-a, --archived=<bool>` | Include/exclude archived repos (with -g) |
| `--paginate` | Fetch all pages of projects (with -g) |

**Examples:**
```bash
# Clone by path
glab repo clone gitlab-org/cli

# Clone by URL
glab repo clone https://gitlab.com/gitlab-org/cli

# Clone into specific directory
glab repo clone gitlab-org/cli my-glab

# Clone by project ID
glab repo clone 4356677

# Clone preserving namespace structure
glab repo clone gitlab-org/cli -p
# Creates: gitlab-org/cli/

# Clone all repos in a group
glab repo clone -g mygroup --paginate

# Clone only non-archived repos from group
glab repo clone -g mygroup --archived=false --paginate
```

### Fork Repository

```bash
glab repo fork <repo> [options]
```

**Options:**
| Flag | Description |
|------|-------------|
| `-c, --clone` | Clone the fork after creating |
| `-n, --name=<name>` | Name for the forked project |
| `-p, --path=<path>` | Path for the forked project |
| `--remote` | Add a remote for the fork |

**Examples:**
```bash
# Fork a repository
glab repo fork owner/repo

# Fork and clone
glab repo fork owner/repo --clone

# Fork with custom name
glab repo fork owner/repo --name="my-fork"

# Fork and add remote
glab repo fork owner/repo --remote
```

### View Repository

```bash
glab repo view [repo] [options]
```

**Options:**
| Flag | Description |
|------|-------------|
| `-w, --web` | Open repository in browser |
| `-b, --branch=<branch>` | View specific branch |

**Examples:**
```bash
# View current repository info
glab repo view

# View specific repo
glab repo view gitlab-org/cli

# Open in browser
glab repo view --web

# View specific branch
glab repo view --branch=develop
```

### Create Repository

```bash
glab repo create [name] [options]
```

**Options:**
| Flag | Description |
|------|-------------|
| `-n, --name=<name>` | Repository name |
| `-d, --description=<desc>` | Repository description |
| `-g, --group=<group>` | Create in specific group/namespace |
| `--public` | Make repository public |
| `--private` | Make repository private |
| `--internal` | Make repository internal |
| `--readme` | Initialize with README |
| `-c, --clone` | Clone after creation |

**Examples:**
```bash
# Create repository interactively
glab repo create

# Create with name and description
glab repo create my-project -d "My awesome project"

# Create public repo in group
glab repo create my-project --group=myteam --public

# Create and clone
glab repo create my-project --clone --readme
```

### Search Repositories

```bash
glab repo search <query> [options]
```

**Options:**
| Flag | Description |
|------|-------------|
| `-P, --per-page=<n>` | Results per page |
| `--all` | Get all results |

**Examples:**
```bash
# Search for repos
glab repo search "cli tools"

# Search with more results
glab repo search "gitlab" --per-page=50
```

### Archive Repository

```bash
glab repo archive [repo] [options]
```

Archives a repository (makes it read-only).

**Examples:**
```bash
# Archive current repo
glab repo archive

# Archive specific repo
glab repo archive owner/repo
```

### Delete Repository

```bash
glab repo delete [repo] [options]
```

**Warning:** This permanently deletes the repository and all its data!

**Options:**
| Flag | Description |
|------|-------------|
| `-y, --yes` | Skip confirmation prompt |

**Examples:**
```bash
# Delete repo (will prompt for confirmation)
glab repo delete owner/repo

# Delete without confirmation (dangerous!)
glab repo delete owner/repo --yes
```

### List Contributors

```bash
glab repo contributors [repo] [options]
```

**Options:**
| Flag | Description |
|------|-------------|
| `-P, --per-page=<n>` | Results per page |
| `--order=<order>` | Sort order: name, email, commits |

**Examples:**
```bash
# List contributors for current repo
glab repo contributors

# List with sorting
glab repo contributors --order=commits
```

### Transfer Repository

```bash
glab repo transfer <repo> <new-namespace>
```

Transfer a repository to another namespace.

**Examples:**
```bash
# Transfer to different group
glab repo transfer myrepo newgroup
```

## Common Workflows

### Workflow 1: Fork and Contribute

```bash
# 1. Fork the repository
glab repo fork upstream/project --clone

# 2. Add upstream remote
cd project
git remote add upstream https://gitlab.com/upstream/project.git

# 3. Create feature branch
git checkout -b feature/my-change

# 4. Make changes, commit, push
git add . && git commit -m "Add feature"
git push -u origin feature/my-change

# 5. Create MR to upstream
glab mr create --target-branch=main
```

### Workflow 2: Batch Clone Team Repos

```bash
# Clone all non-archived repos from team group
glab repo clone -g myteam --archived=false --paginate -p

# This creates:
# myteam/
#   repo1/
#   repo2/
#   ...
```

### Workflow 3: Create New Project

```bash
# 1. Create the repository
glab repo create awesome-project \
  -d "An awesome new project" \
  --group=myteam \
  --readme \
  --clone

# 2. Set up the project
cd awesome-project
# Add initial files...

# 3. View it in browser
glab repo view --web
```

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Authentication failed | Invalid/expired token | Run `glab auth login` |
| Repo not found | Invalid path or no access | Check repo path and permissions |
| Clone failed | SSH keys not configured | Use HTTPS or configure SSH keys |
| Cannot fork | Already forked or no permission | Check existing forks |
| Cannot delete | Not owner or maintainer | Request owner to delete |

## Related Documentation

- [Safeguards](../shared/docs/SAFEGUARDS.md)
- [Quick Reference](../shared/docs/QUICK_REFERENCE.md)
