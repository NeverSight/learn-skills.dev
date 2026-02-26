---
name: reload
description: >
  Restart the current Claude Code session from within tmux.
  Writes a handoff file, launches a restart script in a new tmux window,
  which stops the current Claude and resumes with --resume.
  Triggers: /reload, "reload", "restart", "reboot", "再起動"
---

# /reload -- Self-Restart Claude Code

tmux 内で動作中の Claude Code を停止し、同一セッションで再起動する。
handoff.md に引き継ぎ情報を書き、別の tmux ウィンドウから元のペインを操作する。

## When to use

ユーザーが `/reload` を呼んだ時だけでなく、**エージェント自身が必要と判断したら自発的に実行する。**

### 自発的に再起動すべき場面（MUST）

以下のファイルを変更した後は、変更を反映するために再起動が必要:

- `.claude/settings.json` -- hooks、permissions 等の設定
- `.claude/hooks/` -- hook スクリプトの追加・変更・削除
- `.claude/agents/` -- エージェント定義の変更
- `**/SKILL.md` -- スキル定義の追加・変更
- `.claude/rules/` -- ルールファイルの変更
- `CLAUDE.md` -- プロジェクト指示の変更

**フロー: 設定変更 → handoff.md に変更内容と次のステップを書く → /reload 実行**

### その他の再起動場面

- コンテキストが重くなった時
- フェーズを切り替えたい時（調査 → 実装 など）
- エラーが蓄積してリセットしたい時

## Prerequisites

- tmux 内で実行していること（tmux 外では動作しない）

## Instructions

### Step 1: tmux 環境を確認

```bash
echo "TMUX_PANE=$TMUX_PANE"
```

`TMUX_PANE` が空なら、ユーザーに「tmux 内で実行してください」と伝えて中止。

### Step 2: handoff.md を書く

`.claude/self-reborn/handoff.md` に引き継ぎ情報を書く。
これが再起動後の自分が受け取る唯一のコンテキスト。具体的に書くこと。

```bash
mkdir -p .claude/self-reborn
cat > .claude/self-reborn/handoff.md << 'HANDOFF_EOF'
# Handoff

## Restart Reason
{なぜ再起動するか -- 具体的に}

## Current Task
{何をしていたか -- ファイル名、行番号、進捗}

## Next Steps
{次に何をすべきか -- 具体的なアクション}

## Important Context
{引き継ぎたい情報 -- 決定事項、注意点、ブロッカー}
HANDOFF_EOF
```

### Step 3: セッション ID を取得

```bash
SESSION_ID="${CLAUDE_SESSION_ID:-}"
echo "SESSION_ID=$SESSION_ID"
```

`$CLAUDE_SESSION_ID` は Claude Code が設定する環境変数。空の場合も `--continue` で代用できるので続行可能。

### Step 4: 再起動スクリプトを生成して実行

以下のコマンドで一時スクリプトを作成し、別の tmux ウィンドウで実行する。

```bash
REBORN_SCRIPT=$(mktemp /tmp/claude-reborn-XXXXXX.sh)
PANE="$TMUX_PANE"
PROJECT="$(pwd)"
# SESSION_ID は Step 3 で取得済み

cat > "$REBORN_SCRIPT" << REBORN_EOF
#!/bin/bash
set -eo pipefail

TARGET_PANE="$PANE"
SESSION_ID="$SESSION_ID"
PROJECT_DIR="$PROJECT"
HANDOFF="\$PROJECT_DIR/.claude/self-reborn/handoff.md"

log() { echo "[reborn] \$(date '+%H:%M:%S') \$1"; }

log "Waiting 2s before stopping Claude..."
sleep 2

# Kill Claude Code process in the target pane
PANE_PID=\$(tmux display-message -t "\$TARGET_PANE" -p '#{pane_pid}')
CLAUDE_PID=\$(pgrep -P "\$PANE_PID" | head -1)
if [ -n "\$CLAUDE_PID" ]; then
    log "Killing Claude (PID=\$CLAUDE_PID, parent=\$PANE_PID) in \$TARGET_PANE"
    kill "\$CLAUDE_PID"
else
    log "No Claude process found under PID \$PANE_PID, sending Ctrl+C"
    tmux send-keys -t "\$TARGET_PANE" C-c C-c
fi

# Wait for Claude to exit (poll pane_current_command)
log "Waiting for Claude to exit..."
for i in \$(seq 1 30); do
    sleep 1
    fg=\$(tmux display-message -t "\$TARGET_PANE" -p '#{pane_current_command}' 2>/dev/null || echo "")
    case "\$fg" in bash|zsh|sh|fish) log "Claude exited (\${i}s)"; break;; esac
    if [ "\$i" -eq 10 ]; then
        log "Still running (\$fg), sending SIGKILL..."
        kill -9 "\$CLAUDE_PID" 2>/dev/null
    fi
done

# Resume Claude
log "Restarting Claude..."
sleep 1
if [ -n "\$SESSION_ID" ]; then
    tmux send-keys -t "\$TARGET_PANE" "cd '\$PROJECT_DIR' && claude --resume '\$SESSION_ID'" Enter
else
    tmux send-keys -t "\$TARGET_PANE" "cd '\$PROJECT_DIR' && claude --continue" Enter
fi

# Phase 1: Wait for Claude process to start
log "Phase 1: Waiting for Claude process to start..."
for i in \$(seq 1 30); do
    sleep 1
    fg=\$(tmux display-message -t "\$TARGET_PANE" -p '#{pane_current_command}' 2>/dev/null || echo "")
    case "\$fg" in bash|zsh|sh|fish) ;; *)
        log "Claude process detected: \$fg (\${i}s)"
        break
    ;; esac
    if [ "\$i" -eq 30 ]; then log "Timeout waiting for process start"; fi
done

# Phase 2: Wait for UI to stabilize (content stops changing)
log "Phase 2: Waiting for Claude UI to stabilize..."
PREV_HASH=""
STABLE_COUNT=0
for i in \$(seq 1 90); do
    sleep 2
    CUR_HASH=\$(tmux capture-pane -t "\$TARGET_PANE" -p 2>/dev/null | md5 -q)
    if [ "\$CUR_HASH" = "\$PREV_HASH" ]; then
        STABLE_COUNT=\$((STABLE_COUNT + 1))
        if [ "\$STABLE_COUNT" -ge 2 ]; then
            log "Claude UI stable (content unchanged for 4s, total \$((i * 2))s)"
            break
        fi
    else
        STABLE_COUNT=0
    fi
    PREV_HASH="\$CUR_HASH"
    if [ "\$i" -eq 90 ]; then log "Timeout (180s), sending prompt anyway"; fi
done

# Send handoff prompt
if [ -f "\$HANDOFF" ]; then
    sleep 1
    tmux send-keys -t "\$TARGET_PANE" ".claude/self-reborn/handoff.md を読んで、再起動理由と次のステップを確認して作業を続けてください。"
    sleep 0.5
    tmux send-keys -t "\$TARGET_PANE" Enter
    log "Handoff prompt sent"
fi

log "Done. Closing in 3s..."
sleep 3
rm -f "\$0"
REBORN_EOF

chmod +x "$REBORN_SCRIPT"
tmux new-window -n reborn "$REBORN_SCRIPT"
```

**このコマンドの実行後、2秒以内に Ctrl+C が送られて自分は停止する。これは正常動作。**

## Arguments

| Argument | Action |
|----------|--------|
| (empty) | 再起動理由を聞いてから実行 |
| `<reason>` | 指定された理由で即座に実行 |

## Safety

- tmux 外では動作しない（Step 1 で検出）
- 一時スクリプトは実行後に自己削除
- 失敗しても元のペインのシェルは残る（手動で `claude` を再起動可能）
- ラッパーループなし -- 一発実行のみ
