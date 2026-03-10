---
name: i18n-audit
description: >-
  i18n キー整合性チェック。messages/ja.json と messages/en.json のキー差分を検出し、
  翻訳漏れや不要キーを報告する。翻訳キーの追加・削除・変更を行った後や、
  ja/en間の同期状態が気になるとき、i18nキーの不一致を調べたいときに必ず使うこと。
  翻訳ファイルに触れる作業では、明示的に依頼されなくてもこのスキルの利用を検討すること。
argument-hint: "[--ignore-new]"
allowed-tools: Bash, Read, Grep, Glob
user-invocable: true
---

# /i18n-audit — i18n キー整合性チェック

`messages/ja.json` と `messages/en.json` のキー構造が一致するか検証する静的チェック。

## Usage

```bash
# npm script 経由
npm run audit:i18n

# 直接実行
node scripts/audit/i18n-keys.mjs
node scripts/audit/i18n-keys.mjs --ignore-new   # ja-only キーを警告扱い（en翻訳未完了時）

# Claude Code スキル
/i18n-audit
/i18n-audit --ignore-new
```

## What It Checks

1. **ja-only キー**: `ja.json` にあって `en.json` にないキー → en 翻訳が必要
2. **en-only キー**: `en.json` にあって `ja.json` にないキー → ja が欠落（通常はバグ）
3. **キー総数**: 共有キー数と差分数を表示

## Output Example

```
=== i18n Key Parity Check ===
Sources: messages/ja.json, messages/en.json
Keys: 280 shared, 12 ja-only, 0 en-only

❌ [MISSING in en.json] marketing.tryNow (12 keys):
    - marketing.tryNow.badge
    - marketing.tryNow.title
    ...

💡 Fix: 不足キーを対応する messages ファイルに追加してください。
```

## Flags

| フラグ | 効果 |
|--------|------|
| (なし) | ja-only も en-only も全て error（exit 1） |
| `--ignore-new` | ja-only は warning（exit 0）、en-only のみ error |

`--ignore-new` は「新機能を ja で先に実装し、en 翻訳は後回し」のワークフロー向け。

## CI Integration

```yaml
# GitHub Actions - 厳密モード
- name: i18n Key Check
  run: npm run audit:i18n

# GitHub Actions - 寛容モード（en翻訳は後回し許容）
- name: i18n Key Check (lenient)
  run: npm run audit:i18n -- --ignore-new
```

## Workflow: 新しい i18n キーを追加する時

1. `messages/ja.json` にキーを追加
2. `npm run audit:i18n` を実行 → ja-only キーが報告される
3. `messages/en.json` に対応する英語キーを追加
4. `npm run audit:i18n` を再実行 → ✅

## AI Assistant Instructions

このスキルが有効化された時:

1. `npm run audit:i18n` を実行して差分を把握
2. ja-only キーがあれば en.json に英語翻訳を追加
3. en-only キーがあれば ja.json に日本語翻訳を追加（または en から削除）
4. 再度 `npm run audit:i18n` で検証

Always:
- キー追加は ja.json と en.json を同時に行う
- ネストされたキー構造を維持する（フラットにしない）

Never:
- 空文字列でキーを埋めない（未翻訳なら `--ignore-new` を使う）
- 機械翻訳の品質が低い場合は TODO コメントをキー値に含めない
