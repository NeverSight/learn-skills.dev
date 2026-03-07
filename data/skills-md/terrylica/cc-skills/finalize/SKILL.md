---
name: finalize
description: Finalize orphaned recordings - stop processes, compress, push to orphan branch. TRIGGERS - finalize recording, stop asciinema, orphaned recording, cleanup recording, push recording.
allowed-tools: Bash, AskUserQuestion, Glob, Read
argument-hint: "[file|--all] [--force] [--no-push] [--keep-local]"
---

# /asciinema-tools:finalize

Finalize orphaned asciinema recordings: stop running processes gracefully, compress, and push to the orphan branch.

## Arguments

| Argument       | Description                                |
| -------------- | ------------------------------------------ |
| `file`         | Specific .cast file to finalize            |
| `--all`        | Finalize all unhandled .cast files         |
| `--force`      | Use SIGKILL if graceful stop fails         |
| `--no-push`    | Skip pushing to orphan branch (local only) |
| `--keep-local` | Keep local .cast after compression         |

## Workflow

1. **Discovery**: Find running asciinema processes and unhandled .cast files
2. **Selection**: AskUserQuestion for which files to process
3. **Stop**: Gracefully stop running processes (SIGTERM → SIGINT → SIGKILL)
4. **Verify**: Check file integrity after stop
5. **Compress**: zstd compress .cast files
6. **Push**: Push to orphan branch (if configured)
7. **Cleanup**: Remove local .cast (optional)

## Execution

### Phase 1: Discovery

```bash
/usr/bin/env bash << 'DISCOVER_EOF'
echo "=== Running asciinema processes ==="
PROCS=$(ps aux | grep -E "asciinema rec" | grep -v grep)
if [[ -n "$PROCS" ]]; then
  echo "$PROCS" | while read -r line; do
    PID=$(echo "$line" | awk '{print $2}')
    CAST_FILE=$(echo "$line" | grep -oE '[^ ]+\.cast' | head -1)
    if [[ -n "$CAST_FILE" ]]; then
      SIZE=$(ls -lh "$CAST_FILE" 2>/dev/null | awk '{print $5}' || echo "?")
      echo "PID $PID: $CAST_FILE ($SIZE)"
    else
      echo "PID $PID: (no file detected)"
    fi
  done
else
  echo "No running asciinema processes"
fi

echo ""
echo "=== Unhandled .cast files ==="
find ~/eon -name "*.cast" -size +1M -mtime -30 2>/dev/null | while read -r f; do
  SIZE=$(ls -lh "$f" | awk '{print $5}')
  echo "$f ($SIZE)"
done
DISCOVER_EOF
```

### Phase 2: Selection

```yaml
AskUserQuestion:
  question: "Which recordings should be finalized?"
  header: "Select"
  multiSelect: true
  options:
    - label: "All running processes"
      description: "Stop all asciinema rec processes and finalize their files"
    - label: "All unhandled files"
      description: "Finalize all .cast files found in ~/eon"
    - label: "Specific file"
      description: "Enter path to specific .cast file"
```

### Phase 3: Stop Running Processes

```bash
/usr/bin/env bash << 'STOP_EOF'
# Arguments: PID list
PIDS="$@"

for PID in $PIDS; do
  echo "Stopping PID $PID..."

  # Try SIGTERM first (graceful)
  kill -TERM "$PID" 2>/dev/null
  sleep 2

  if kill -0 "$PID" 2>/dev/null; then
    echo "  SIGTERM ignored, trying SIGINT..."
    kill -INT "$PID" 2>/dev/null
    sleep 2
  fi

  if kill -0 "$PID" 2>/dev/null; then
    echo "  Process still running. Use --force for SIGKILL"
    # Only SIGKILL with --force flag
    if [[ "$FORCE" == "true" ]]; then
      echo "  Sending SIGKILL (file may be truncated)..."
      kill -9 "$PID" 2>/dev/null
      sleep 1
    fi
  fi

  if ! kill -0 "$PID" 2>/dev/null; then
    echo "  ✓ Process stopped"
  else
    echo "  ✗ Process still running"
  fi
done
STOP_EOF
```

### Phase 4: File Integrity Check

```bash
/usr/bin/env bash << 'CHECK_EOF'
CAST_FILE="$1"

echo "Checking file integrity: $CAST_FILE"

# Check if file exists
if [[ ! -f "$CAST_FILE" ]]; then
  echo "  ✗ File not found"
  exit 1
fi

# Check file size
SIZE=$(stat -f%z "$CAST_FILE" 2>/dev/null || stat -c%s "$CAST_FILE")
echo "  Size: $(numfmt --to=iec-i "$SIZE" 2>/dev/null || echo "$SIZE bytes")"

# Check last line (NDJSON should have complete JSON arrays)
LAST_LINE=$(tail -c 500 "$CAST_FILE" | tail -1)
if [[ "$LAST_LINE" == *"]"* ]]; then
  echo "  ✓ File appears complete (ends with JSON array)"
else
  echo "  ⚠ File may be truncated (incomplete JSON)"
  echo "  Note: asciinema 2.0+ streams to disk, so most data is preserved"
fi

# Test with asciinema cat (quick validation)
if timeout 5 asciinema cat "$CAST_FILE" > /dev/null 2>&1; then
  echo "  ✓ File is playable"
else
  echo "  ⚠ File may have issues (but often still usable)"
fi
CHECK_EOF
```

### Phase 5: Compress

```bash
/usr/bin/env bash << 'COMPRESS_EOF'
CAST_FILE="$1"
ZSTD_LEVEL="${2:-6}"

echo "Compressing: $CAST_FILE"

OUTPUT="${CAST_FILE}.zst"
if zstd -"$ZSTD_LEVEL" -f "$CAST_FILE" -o "$OUTPUT"; then
  ORIG_SIZE=$(stat -f%z "$CAST_FILE" 2>/dev/null || stat -c%s "$CAST_FILE")
  COMP_SIZE=$(stat -f%z "$OUTPUT" 2>/dev/null || stat -c%s "$OUTPUT")
  RATIO=$(echo "scale=1; $ORIG_SIZE / $COMP_SIZE" | bc 2>/dev/null || echo "?")
  echo "  ✓ Compressed: $(basename "$OUTPUT")"
  echo "  Compression ratio: ${RATIO}:1"
else
  echo "  ✗ Compression failed"
  exit 1
fi
COMPRESS_EOF
```

### Phase 6: Push to Orphan Branch

```bash
/usr/bin/env bash << 'PUSH_EOF'
COMPRESSED_FILE="$1"
RECORDINGS_DIR="$HOME/asciinema_recordings"

# Find the local recordings clone
REPO_DIR=$(find "$RECORDINGS_DIR" -maxdepth 1 -type d -name "*" | head -1)
if [[ -z "$REPO_DIR" ]] || [[ ! -d "$REPO_DIR/.git" ]]; then
  echo "  ⚠ No orphan branch clone found at $RECORDINGS_DIR"
  echo "  Run /asciinema-tools:bootstrap to set up orphan branch"
  exit 1
fi

echo "Pushing to orphan branch..."

# Copy compressed file
BASENAME=$(basename "$COMPRESSED_FILE")
DEST="$REPO_DIR/recordings/$BASENAME"
mkdir -p "$(dirname "$DEST")"
cp "$COMPRESSED_FILE" "$DEST"

# Commit and push
cd "$REPO_DIR"
git add -A
git commit -m "finalize: $BASENAME" 2>/dev/null || true

# Push with token (prefer env var to avoid process spawning)
GH_TOKEN="${GH_TOKEN:-${GITHUB_TOKEN:-$(gh auth token 2>/dev/null || echo "")}}"
if [[ -n "$GH_TOKEN" ]]; then
  REMOTE_URL=$(git remote get-url origin)
  # Convert to token-authenticated URL
  TOKEN_URL=$(echo "$REMOTE_URL" | sed "s|https://github.com|https://$GH_TOKEN@github.com|")
  if git push "$TOKEN_URL" HEAD 2>/dev/null; then
    echo "  ✓ Pushed to orphan branch"
  else
    echo "  ✗ Push failed (check credentials)"
  fi
else
  echo "  ⚠ No GitHub token, skipping push"
fi
PUSH_EOF
```

### Phase 7: Cleanup Confirmation

```yaml
AskUserQuestion:
  question: "Delete local .cast file after successful compression/push?"
  header: "Cleanup"
  options:
    - label: "Yes, delete local .cast"
      description: "Remove original .cast file (compressed version preserved)"
    - label: "No, keep local"
      description: "Keep both .cast and .cast.zst files"
```

## Example Usage

```bash
# Interactive mode - discover and select
/asciinema-tools:finalize

# Finalize specific file
/asciinema-tools:finalize ~/eon/project/tmp/session.cast

# Finalize all with force stop
/asciinema-tools:finalize --all --force

# Local only (no push)
/asciinema-tools:finalize session.cast --no-push
```

## Troubleshooting

| Issue                 | Cause                        | Solution                               |
| --------------------- | ---------------------------- | -------------------------------------- |
| Process won't stop    | Hung asciinema process       | Use `--force` flag for SIGKILL         |
| File may be truncated | Forced stop interrupted file | Most data preserved, try playing it    |
| zstd not found        | zstd not installed           | `brew install zstd`                    |
| Push failed           | No GitHub token              | Set GH_TOKEN or run `gh auth login`    |
| No orphan branch      | Clone not configured         | Run `/asciinema-tools:bootstrap` first |
| File not found        | Wrong path or already moved  | Check with `/daemon-status`            |

## Related Commands

- `/asciinema-tools:daemon-status` - View status and find unhandled files
- `/asciinema-tools:convert` - Convert .cast to .txt for analysis
- `/asciinema-tools:summarize` - AI-powered analysis of recordings
