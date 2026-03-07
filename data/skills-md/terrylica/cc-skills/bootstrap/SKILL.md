---
name: bootstrap
description: Pre-session bootstrap - generates script to start recording BEFORE entering Claude Code. Chunking handled by daemon. TRIGGERS - bootstrap, pre-session, start recording, before claude.
allowed-tools: Bash, AskUserQuestion, Glob, Write, Read
argument-hint: "[-r repo] [-b branch] [--setup-orphan] [-y|--yes]"
disable-model-invocation: true
---

# /asciinema-tools:bootstrap

Generate a bootstrap script that runs OUTSIDE Claude Code CLI to start a recording session.

**Important**: Chunking is handled by the launchd daemon. Run `/asciinema-tools:daemon-setup` first if you haven't already.

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        DAEMON-BASED RECORDING WORKFLOW                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  1. ONE-TIME SETUP (if not done):                                           │
│     /asciinema-tools:daemon-setup                                           │
│     → Configures launchd daemon with Keychain credentials                   │
│                                                                             │
│  2. GENERATE BOOTSTRAP (in Claude Code):                                    │
│     /asciinema-tools:bootstrap                                              │
│     → Generates tmp/bootstrap-claude-session.sh                             │
│                                                                             │
│  3. EXIT CLAUDE and RUN BOOTSTRAP:                                          │
│     $ ./tmp/bootstrap-claude-session.sh    ← NOT source!                    │
│     → Writes config for daemon                                              │
│     → Starts asciinema recording                                            │
│                                                                             │
│  4. WORK IN RECORDING:                                                      │
│     $ claude                                                                │
│     → Daemon automatically pushes chunks to GitHub                          │
│                                                                             │
│  5. EXIT (two times):                                                       │
│     Ctrl+D (exit Claude) → exit (end recording)                             │
│     → Daemon pushes final chunk                                             │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Arguments

| Argument         | Description                                          |
| ---------------- | ---------------------------------------------------- |
| `-r, --repo`     | GitHub repository (e.g., `owner/repo`)               |
| `-b, --branch`   | Orphan branch name (default: `asciinema-recordings`) |
| `--setup-orphan` | Force create orphan branch                           |
| `-y, --yes`      | Skip confirmation prompts                            |

## Execution

### Phase 0: Preflight Check

```bash
/usr/bin/env bash << 'PREFLIGHT_EOF'
MISSING=()
for tool in asciinema zstd git; do
  command -v "$tool" &>/dev/null || MISSING+=("$tool")
done

if [[ ${#MISSING[@]} -gt 0 ]]; then
  echo "MISSING: ${MISSING[*]}"
  exit 1
fi

echo "PREFLIGHT: OK"
asciinema --version | head -1

# Check daemon status
if launchctl list 2>/dev/null | grep -q "asciinema-chunker"; then
  echo "DAEMON: RUNNING"
else
  echo "DAEMON: NOT_RUNNING"
fi
PREFLIGHT_EOF
```

**If DAEMON: NOT_RUNNING, use AskUserQuestion:**

```
Question: "The chunker daemon is not running. Chunks won't be pushed to GitHub without it."
Header: "Daemon"
Options:
  - label: "Run daemon setup (Recommended)"
    description: "Switch to /asciinema-tools:daemon-setup to configure the daemon"
  - label: "Continue anyway"
    description: "Generate bootstrap script without daemon (local recording only)"
```

### Phase 1: Detect Repository Context

**MANDATORY**: Run before AskUserQuestion to auto-populate options.

```bash
/usr/bin/env bash << 'DETECT_CONTEXT_EOF'
IN_GIT_REPO="false"
CURRENT_REPO_URL=""
CURRENT_REPO_OWNER=""
CURRENT_REPO_NAME=""
ORPHAN_BRANCH_EXISTS="false"
LOCAL_CLONE_EXISTS="false"
ORPHAN_BRANCH="asciinema-recordings"

if git rev-parse --git-dir &>/dev/null 2>&1; then
  IN_GIT_REPO="true"

  if git remote get-url origin &>/dev/null 2>&1; then
    CURRENT_REPO_URL=$(git remote get-url origin)
  elif [[ -n "$(git remote)" ]]; then
    REMOTE=$(git remote | head -1)
    CURRENT_REPO_URL=$(git remote get-url "$REMOTE")
  fi

  if [[ -n "$CURRENT_REPO_URL" ]]; then
    if [[ "$CURRENT_REPO_URL" =~ github\.com[:/]([^/]+)/([^/.]+) ]]; then
      CURRENT_REPO_OWNER="${BASH_REMATCH[1]}"
      CURRENT_REPO_NAME="${BASH_REMATCH[2]%.git}"
    fi

    if git ls-remote --heads "$CURRENT_REPO_URL" "$ORPHAN_BRANCH" 2>/dev/null | grep -q "$ORPHAN_BRANCH"; then
      ORPHAN_BRANCH_EXISTS="true"
    fi

    LOCAL_CLONE_PATH="$HOME/asciinema_recordings/$CURRENT_REPO_NAME"
    if [[ -d "$LOCAL_CLONE_PATH/.git" ]]; then
      LOCAL_CLONE_EXISTS="true"
    fi
  fi
fi

echo "IN_GIT_REPO=$IN_GIT_REPO"
echo "CURRENT_REPO_URL=$CURRENT_REPO_URL"
echo "CURRENT_REPO_OWNER=$CURRENT_REPO_OWNER"
echo "CURRENT_REPO_NAME=$CURRENT_REPO_NAME"
echo "ORPHAN_BRANCH_EXISTS=$ORPHAN_BRANCH_EXISTS"
echo "LOCAL_CLONE_EXISTS=$LOCAL_CLONE_EXISTS"
DETECT_CONTEXT_EOF
```

### Phase 2: Repository Selection (MANDATORY AskUserQuestion)

Based on detection results:

**If IN_GIT_REPO=true, ORPHAN_BRANCH_EXISTS=true:**

```
Question: "Orphan branch found in {repo}. Use it?"
Header: "Destination"
Options:
  - label: "Use existing (Recommended)"
    description: "Branch 'asciinema-recordings' already configured in {repo}"
  - label: "Use different repository"
    description: "Store recordings in a different repo"
```

**If IN_GIT_REPO=true, ORPHAN_BRANCH_EXISTS=false:**

```
Question: "No orphan branch in {repo}. Create one?"
Header: "Setup"
Options:
  - label: "Create orphan branch (Recommended)"
    description: "Initialize with GitHub Actions workflow for brotli"
  - label: "Use different repository"
    description: "Store recordings elsewhere"
```

**If IN_GIT_REPO=false:**

```
Question: "Not in a git repo. Where to store recordings?"
Header: "Destination"
Options:
  - label: "Dedicated recordings repo"
    description: "Use {owner}/asciinema-recordings"
  - label: "Enter repository"
    description: "Specify owner/repo manually"
```

### Phase 3: Create Orphan Branch (if needed)

Clear SSH caches first, then create orphan branch:

```bash
/usr/bin/env bash << 'CREATE_ORPHAN_EOF'
REPO_URL="${1:?}"
BRANCH="${2:-asciinema-recordings}"
LOCAL_PATH="$HOME/asciinema_recordings/$(basename "$REPO_URL" .git)"

# Clear SSH caches first
rm -f ~/.ssh/control-* 2>/dev/null || true
ssh -O exit git@github.com 2>/dev/null || true

# Get GitHub token for HTTPS clone (prefer env var to avoid process spawning)
GH_TOKEN="${GH_TOKEN:-${GITHUB_TOKEN:-$(gh auth token 2>/dev/null || echo "")}}"
if [[ -n "$GH_TOKEN" ]]; then
  # Parse owner/repo
  if [[ "$REPO_URL" =~ github\.com[:/]([^/]+)/([^/.]+) ]]; then
    OWNER_REPO="${BASH_REMATCH[1]}/${BASH_REMATCH[2]}"
    AUTH_URL="https://${GH_TOKEN}@github.com/${OWNER_REPO}.git"
    CLEAN_URL="https://github.com/${OWNER_REPO}.git"
  else
    AUTH_URL="$REPO_URL"
    CLEAN_URL="$REPO_URL"
  fi
else
  AUTH_URL="$REPO_URL"
  CLEAN_URL="$REPO_URL"
fi

# Clone and create orphan
TEMP_DIR=$(mktemp -d)
git clone "$AUTH_URL" "$TEMP_DIR/repo"
cd "$TEMP_DIR/repo"

# Create orphan branch
git checkout --orphan "$BRANCH"
git reset --hard
git commit --allow-empty -m "Initialize asciinema recordings"
git push origin "$BRANCH"

# Cleanup temp
rm -rf "$TEMP_DIR"

# Clone orphan branch locally
mkdir -p "$(dirname "$LOCAL_PATH")"
git clone --single-branch --branch "$BRANCH" --depth 1 "$AUTH_URL" "$LOCAL_PATH"

# Strip token from remote
git -C "$LOCAL_PATH" remote set-url origin "$CLEAN_URL"

mkdir -p "$LOCAL_PATH/chunks"

echo "ORPHAN_CREATED: $LOCAL_PATH"
CREATE_ORPHAN_EOF
```

### Phase 4: Generate Bootstrap Script

Generate the simplified bootstrap script (daemon handles chunking):

```bash
/usr/bin/env bash << 'GENERATE_SCRIPT_EOF'
REPO_URL="${1:?}"
BRANCH="${2:-asciinema-recordings}"
LOCAL_REPO="${3:-$HOME/asciinema_recordings/$(basename "$REPO_URL" .git)}"
OUTPUT_FILE="${4:-$PWD/tmp/bootstrap-claude-session.sh}"

mkdir -p "$(dirname "$OUTPUT_FILE")"

cat > "$OUTPUT_FILE" << 'SCRIPT_EOF'
#!/usr/bin/env bash
# bootstrap-claude-session.sh - Start asciinema recording session
# Generated by /asciinema-tools:bootstrap
# Chunking handled by launchd daemon

if [[ "${BASH_SOURCE[0]}" != "$0" ]]; then
    echo "ERROR: Do not source this script. Run directly: ./${BASH_SOURCE[0]##*/}"
    return 1
fi

set -uo pipefail

SCRIPT_EOF

# Append configuration
cat >> "$OUTPUT_FILE" << SCRIPT_CONFIG
REPO_URL="$REPO_URL"
BRANCH="$BRANCH"
LOCAL_REPO="$LOCAL_REPO"
SCRIPT_CONFIG

cat >> "$OUTPUT_FILE" << 'SCRIPT_BODY'
WORKSPACE="$(basename "$PWD")"
DATETIME="$(date +%Y-%m-%d_%H-%M)"
ASCIINEMA_DIR="$HOME/.asciinema"
ACTIVE_DIR="$ASCIINEMA_DIR/active"
CAST_FILE="$ACTIVE_DIR/${WORKSPACE}_${DATETIME}.cast"
CONFIG_FILE="${CAST_FILE%.cast}.json"

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  asciinema Recording Session                                   ║"
echo "╠════════════════════════════════════════════════════════════════╣"

# Check daemon
if ! launchctl list 2>/dev/null | grep -q "asciinema-chunker"; then
    echo "║  WARNING: Daemon not running! Run /asciinema-tools:daemon-start║"
    echo "╠════════════════════════════════════════════════════════════════╣"
fi

# Clear SSH caches
rm -f ~/.ssh/control-* 2>/dev/null || true
ssh -O exit git@github.com 2>/dev/null || true

# Setup
mkdir -p "$ACTIVE_DIR" "$LOCAL_REPO/chunks"

# Write config for daemon
cat > "$CONFIG_FILE" <<EOF
{
    "repo_url": "$REPO_URL",
    "branch": "$BRANCH",
    "local_repo": "$LOCAL_REPO",
    "workspace": "$WORKSPACE",
    "started": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF

cleanup() {
    echo ""
    echo "Recording ended. Daemon will push final chunk."
    echo "Check status: /asciinema-tools:daemon-status"
}
trap cleanup EXIT

echo "║  Recording to: $CAST_FILE"
echo "║  Run 'claude' inside this session. Exit twice to end.         ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

asciinema rec --stdin "$CAST_FILE"
SCRIPT_BODY

chmod +x "$OUTPUT_FILE"
echo "SCRIPT_GENERATED: $OUTPUT_FILE"
GENERATE_SCRIPT_EOF
```

### Phase 5: Display Instructions

```markdown
## Bootstrap Complete

Script generated at: `tmp/bootstrap-claude-session.sh`

### Quick Start

1. Exit Claude Code: `exit` or Ctrl+D
2. Run bootstrap: `./tmp/bootstrap-claude-session.sh` ← NOT source!
3. Inside recording, run: `claude`
4. Work normally - daemon pushes chunks to GitHub
5. Exit twice: Ctrl+D (Claude) → `exit` (recording)

### What Happens

- asciinema records to `~/.asciinema/active/{workspace}_{datetime}.cast`
- Daemon monitors for idle periods
- On idle, chunk is compressed and pushed via Keychain PAT
- Daemon sends Pushover notification on failures
- Recording is decoupled from Claude Code session

### Daemon Commands

| Command                          | Description         |
| -------------------------------- | ------------------- |
| `/asciinema-tools:daemon-status` | Check daemon health |
| `/asciinema-tools:daemon-logs`   | View logs           |
| `/asciinema-tools:daemon-start`  | Start daemon        |
| `/asciinema-tools:daemon-stop`   | Stop daemon         |
```

## Skip Logic

- If `-r` and `-b` provided -> skip repository selection
- If `-y` provided -> skip all confirmations
- If `--setup-orphan` provided -> force create orphan branch

## Troubleshooting

| Issue                 | Cause                   | Solution                            |
| --------------------- | ----------------------- | ----------------------------------- |
| asciinema not found   | asciinema not installed | `brew install asciinema`            |
| zstd not found        | zstd not installed      | `brew install zstd`                 |
| Daemon not running    | Daemon not started      | Run `/asciinema-tools:daemon-start` |
| Git clone fails       | Auth issue or wrong URL | Run `gh auth login`                 |
| Orphan branch error   | Branch already exists   | Remove `--setup-orphan` flag        |
| Script not executable | Permission issue        | Run `chmod +x tmp/bootstrap-*.sh`   |
| Source error          | Script was sourced      | Execute directly: `./script.sh`     |
