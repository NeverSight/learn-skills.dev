---
name: cursor-hook-authoring
description: Cursor Cloud Agent 環境で Git hook 連鎖（特に commit-msg と Co-authored-by 付与・除去）を設計・実装・検証するときに参照する。Cursor 管理 hook の実行順、`commit-msg.cursor.co-author-strip` の命名規則、install スクリプト、lefthook 多層防御、テスト手順を定義する。
---

# Cursor Hook 設計

## 発火タイミング

1. Cursor Cloud Agent 環境で Git hook を追加・変更する
2. `Co-authored-by:` の自動付与と除去の連鎖を設計する
3. lefthook 等の既存 hook と Cursor 管理 hook の共存を整理する

# Git hook と Cursor Cloud の commit-msg 連鎖

## 実行順

Cursor Cloud Agent は `.git/hooks/<hook-name>` を `.dispatcher` 経由で差し替える。`commit-msg` の実行順は次のとおり:

1. **ユーザー hook** — `.cursor-original-hooks-path` が指すパス（通常 `.git/hooks`）に同名 hook があれば先に実行
2. **Cursor 管理 hook** — `$HOOKS_DIR/$HOOK_NAME.cursor*` をファイル名の辞書順で順次実行

`commit-msg` の典型例:

| 順序 | ファイル名 | 役割 |
| --- | --- | --- |
| 1 | `commit-msg.cursor` | シークレットスキャン（commit ブロック） |
| 2 | `commit-msg.cursor.co-author` | `Co-authored-by:` を自動付与 |
| 3 | `commit-msg.cursor.co-author-strip` | `Co-authored-by:` 行を除去（プロジェクト strip hook） |

MUST: strip hook のベース名は `commit-msg.cursor.co-author-strip` とし、`commit-msg.cursor.co-author` より辞書順で後になる命名にする。NEVER: `commit-msg.cursor.strip-co-author` 等、co-author より前に実行される名前を使用する。

## strip hook 実装

1. MUST: 除去ロジックは `.cursor/hooks/strip-co-authored-by.sh` に置く
2. MUST: `commit-msg.cursor.co-author-strip` は当該スクリプトを呼び出す薄いラッパーとする
3. MUST: strip 対象は `Co-authored-by:` / `Co-Authored-By:` 行（大文字小文字不問）および直前の空行
4. NEVER: コミットメッセージ本体（件名・説明）を削除しない

参考実装（`.cursor/hooks/strip-co-authored-by.sh`）:

```bash
#!/usr/bin/env bash
set -euo pipefail

COMMIT_MSG_FILE="${1:?commit message file required}"

if [ ! -f "$COMMIT_MSG_FILE" ]; then
  exit 0
fi

tmp="$(mktemp)"
trap 'rm -f "$tmp"' EXIT

awk '
  BEGIN { skip_blank = 0 }
  /^[Cc]o-[Aa]uthored-[Bb]y:/ { skip_blank = 1; next }
  skip_blank && /^[[:space:]]*$/ { next }
  { skip_blank = 0; print }
' "$COMMIT_MSG_FILE" > "$tmp"

mv "$tmp" "$COMMIT_MSG_FILE"
trap - EXIT
```

## install スクリプト

1. MUST: `scripts/install-cursor-agent-hooks.sh` で strip 連鎖を Cursor hook ディレクトリへ配置する
2. MUST: install 先は Cursor が `.git/hooks` を差し替えている実ディレクトリ（`readlink -f .git/hooks` で解決したパスの親、または `.git/hooks/.cursor-original-hooks-path` と併用）
3. MUST: `commit-msg.cursor.co-author-strip` に実行権限を付与する
4. IF: install 先が特定できない; THEN MUST: 手動で `$CURSOR_AGENT_HOOKS_DIR` を指定して実行する

## lefthook 多層防御

1. IF: リポジトリが lefthook を使用する; THEN SHOULD: `commit-msg` ジョブに strip スクリプトを追加し、Cursor hook 連鎖と二重に `Co-authored-by:` を除去する
2. IF: `git-guard.sh` 等で `git commit --no-verify` を deny する; THEN MUST: strip 連鎖で `--no-verify` なしに `Co-Authored-By` 禁止を満たす
3. IF: force push を git-guard で制限する; THEN MUST: 履歴修正が必要な場合は `GIT_GUARD_ALLOW_FORCE_PUSH=1` を一時設定し、作業後に元に戻す

## テスト手順

1. MUST: `scripts/install-cursor-agent-hooks.sh` を実行する
2. MUST: テストコミットを作成し、`git log -1 --format=%B` で `Co-authored-by:` / `Co-Authored-By:` が含まれないことを確認する
3. MUST: `github` スキルの `Co-Authored-By` 禁止ルールと矛盾しないことを確認する
4. IF: lefthook を使用する; THEN MUST: `lefthook run commit-msg --commit-msg-file /tmp/test-msg` で strip を単体検証する

## 関連スキル

- `github`: コミット author 指定、`Co-Authored-By` 禁止、Hook 迂回禁止
- `skill-escalation`: スキル改変の上流提案
- `refresh-skills`: スキル追加時の整合性検査
