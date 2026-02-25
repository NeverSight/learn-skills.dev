---
name: git-workflow
description: Git version control workflow for Hytale mod development teams. Covers repository setup, branching strategies, commit conventions, pull requests, and collaboration best practices. Use when working with teams, managing mod versions, or setting up source control.
---

# Git Workflow for Mod Teams

Version control and collaboration for Hytale mod development.

## Quick Start

### Initialize New Mod Repository

```bash
cd MyMod
git init
git add .
git commit -m "Initial commit: project structure"
```

### Clone Existing Repository

```bash
git clone https://github.com/username/mymod.git
cd mymod
```

---

## Recommended .gitignore

Create `.gitignore` in your project root:

```gitignore
# Build outputs
build/
out/
*.jar

# IDE files
.idea/
*.iml
.vscode/

# Gradle
.gradle/
gradle/wrapper/gradle-wrapper.jar

# OS files
.DS_Store
Thumbs.db

# Local config
local.properties
*.local

# Dependencies
node_modules/

# Antigravity brain (personal)
.gemini/
```

---

## Branching Strategy

### Simple Model (Small Teams)

```
main ────●────●────●────●────●────  (stable releases)
          \         \
           \         └─ feature/new-mob
            \
             └─ feature/custom-items
```

### GitFlow (Larger Teams)

```
main ─────────────●─────────────●────  (releases only)
                  ↑             ↑
develop ──●───●───●───●───●───●─●────  (integration)
           \     /     \     /
            \   /       \   /
             ●─●         ●─●
          feature/a    feature/b
```

---

## Branch Naming

| Type | Pattern | Example |
|------|---------|---------|
| Feature | `feature/<name>` | `feature/dragon-mob` |
| Bugfix | `fix/<issue>` | `fix/crash-on-spawn` |
| Release | `release/<version>` | `release/1.2.0` |
| Hotfix | `hotfix/<issue>` | `hotfix/exploit-fix` |

---

## Commit Message Convention

### Format

```
<type>: <short description>

[optional body]

[optional footer]
```

### Types

| Type | Use For |
|------|---------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation |
| `style` | Formatting (no code change) |
| `refactor` | Code restructure |
| `test` | Adding tests |
| `chore` | Maintenance |

### Examples

```bash
git commit -m "feat: add dragon mob with fire breath attack"
git commit -m "fix: prevent crash when spawning in water"
git commit -m "docs: update README with installation steps"
git commit -m "refactor: simplify combat system using ECS"
```

---

## Daily Workflow

### 1. Start Your Day

```bash
# Get latest changes
git checkout main
git pull origin main

# Create feature branch
git checkout -b feature/my-feature
```

### 2. Work on Feature

```bash
# Make changes...

# Stage and commit frequently
git add .
git commit -m "feat: implement basic feature"

# Continue working...
git add .
git commit -m "feat: add configuration options"
```

### 3. Stay Updated

```bash
# Get latest main changes
git fetch origin
git rebase origin/main

# Or merge if preferred
git merge origin/main
```

### 4. Push and Create PR

```bash
# Push your branch
git push origin feature/my-feature

# Create Pull Request on GitHub
```

---

## Pull Request Checklist

Before submitting a PR:

- [ ] Code compiles without errors (`gradle build`)
- [ ] Tested in-game
- [ ] Follows project conventions
- [ ] Documentation updated if needed
- [ ] Commit messages are clear
- [ ] No sensitive data committed

---

## Resolving Conflicts

### When Conflicts Occur

```bash
# After merge/rebase shows conflicts
git status  # See conflicting files

# Edit files to resolve
# Look for <<<<<<< ======= >>>>>>>

# Mark as resolved
git add <resolved-file>

# Continue
git rebase --continue
# or
git commit  # if merging
```

---

## Useful Commands

| Task | Command |
|------|---------|
| Check status | `git status` |
| View history | `git log --oneline -10` |
| Undo last commit | `git reset --soft HEAD~1` |
| Discard changes | `git checkout -- <file>` |
| Stash work | `git stash` |
| Apply stash | `git stash pop` |
| Create tag | `git tag v1.0.0` |
| Push tag | `git push origin v1.0.0` |

---

## Version Tagging

For mod releases:

```bash
# Create annotated tag
git tag -a v1.0.0 -m "Release version 1.0.0"

# Push tag to remote
git push origin v1.0.0

# List all tags
git tag -l
```

### Versioning Convention

```
major.minor.patch
  │     │     │
  │     │     └─ Bug fixes
  │     └─────── New features (backwards compatible)
  └───────────── Breaking changes
```

---

## Team Setup

### Add Collaborators

1. Go to GitHub repository settings
2. Click "Collaborators"
3. Add team members by username

### Protect Main Branch

1. Settings → Branches → Add rule
2. Branch name pattern: `main`
3. Enable:
   - Require pull request reviews
   - Require status checks to pass
   - Require branches to be up to date

---

## Quick Reference

| Action | Command |
|--------|---------|
| Clone | `git clone <url>` |
| New branch | `git checkout -b <name>` |
| Switch branch | `git checkout <name>` |
| Stage all | `git add .` |
| Commit | `git commit -m "message"` |
| Push | `git push origin <branch>` |
| Pull | `git pull origin <branch>` |
| Merge | `git merge <branch>` |

---

## Resources

- **GitHub Docs**: [docs.github.com](https://docs.github.com)
- **Git Cheatsheet**: [education.github.com/git-cheat-sheet](https://education.github.com/git-cheat-sheet-education.pdf)
</Parameter>
<parameter name="Complexity">3
