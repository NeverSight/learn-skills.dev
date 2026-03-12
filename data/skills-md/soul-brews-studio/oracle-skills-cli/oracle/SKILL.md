---
name: oracle
description: Manage Oracle skills and profiles. Use when user says "oracle", "profile", "install skill", "remove skill", "switch profile".
---

# /oracle

> Skill and profile management for Oracle instruments.

## Usage

```
/oracle prepare              # check & install git, gh, ghq; set up gh auth
/oracle profile              # list available profiles
/oracle profile <name>       # switch to a profile
/oracle install <skill>      # install one skill
/oracle remove <skill>       # remove one skill
/oracle skills               # list installed skills
```

---

## Subcommands

### /oracle prepare

Check for required tools and install any that are missing. Set up `gh` auth if needed.

**First, detect the platform** by checking the runtime environment (e.g. `uname` or `$OSTYPE`):

| Platform | Package manager |
|----------|----------------|
| macOS | `brew install <pkg>` |
| Linux (Debian/Ubuntu) | `sudo apt install <pkg>` (use official gh repo for gh) |
| Linux (Fedora/RHEL) | `sudo dnf install <pkg>` |
| Linux (Arch) | `sudo pacman -S <pkg>` |
| Windows | `winget install <pkg>` or `scoop install <pkg>` |

**Steps (run each in order):**

1. **Check git**: `git --version`
   - If missing, install with the platform's package manager
2. **Check gh**: `gh --version`
   - If missing, install:
     - macOS: `brew install gh`
     - Debian/Ubuntu: follow https://github.com/cli/cli/blob/trunk/docs/install_linux.md
     - Windows: `winget install GitHub.cli`
     - Others: platform package manager
3. **Check gh auth**: `gh auth status`
   - If not authenticated: run `gh auth login` and guide the user through it
4. **Check ghq**: `ghq --version`
   - If missing, install:
     - macOS: `brew install ghq`
     - Linux/Windows: `go install github.com/x-motemen/ghq@latest` (needs Go), or download binary from GitHub releases
5. **Check ghq root**: `ghq root`
   - If not set, suggest: `git config --global ghq.root ~/Code`

Print a summary table at the end:

```
Platform: macOS / Linux (Ubuntu) / Windows
Tool    Status
----    ------
git     ✓ installed (2.x.x)
gh      ✓ installed + authenticated
ghq     ✓ installed (root: ~/Code)
```

If everything is already set up, just print the summary — no changes needed.

### /oracle profile

List available profiles.

```bash
oracle-skills profiles
```

### /oracle profile \<name\>

Switch to a profile (installs that profile's skill set).

Profiles: `seed`/`minimal` (6 skills), `standard` (12 skills), `full` (all)

```bash
oracle-skills install -g -y --profile <name>
```

### /oracle install \<skill\>

Install a single skill.

```bash
oracle-skills install -g -y --skill <skill>
```

### /oracle remove \<skill\>

Uninstall a single skill.

```bash
oracle-skills uninstall -g -y --skill <skill>
```

### /oracle skills

List installed skills.

```bash
oracle-skills list -g
```

---

## Quick Reference

| Command | Action |
|---------|--------|
| `/oracle prepare` | Check & install git, gh, ghq; set up gh auth |
| `/oracle profile` | List available profiles |
| `/oracle profile seed` | Switch to seed profile |
| `/oracle install <skill>` | Install one skill |
| `/oracle remove <skill>` | Remove one skill |
| `/oracle skills` | List installed skills |

---

ARGUMENTS: $ARGUMENTS
