---
name: teach
description: >-
  [手動専用] プロジェクトの学びをFORyusuke.mdに記録する。セッション中に得た教訓、落とし穴、
  デバッグストーリー、改善点を構造化して追記。/teach で明示的に呼び出した時のみ動作する
  （通常作業では自動発火しない）。
argument-hint: "[topic]"
allowed-tools: Read, Grep, Write
disable-model-invocation: true
user-invocable: true
---

# /teach Skill

プロジェクトの学びを FORyusuke.md に追記する。

## 使い方

```
/teach [topic]
```

例:
- `/teach Claude Code設定監査`
- `/teach E2Eテストのflaky対策`
- `/teach Stripe Webhook実装`

## 制約

- **書き込み先は FORyusuke.md のみ**（他のファイルには書き込まない）
- allowed-tools は最小限（Read/Grep で情報収集、Write で追記のみ）

## 出力フォーマット

FORyusuke.md に以下を追記:

```markdown
## [日付] [topic]

### 何を学んだか
- 技術的な学び
- 設計判断とその理由
- 使用したツール・技術

### 落とし穴
- 遭遇した問題とその原因
- 誤解していたこと
- 時間を浪費したポイント

### もう一度やるなら
- より良いアプローチ
- 最初から知っておきたかったこと
- 次回への教訓
```

## AI Assistant Instructions

1. `$ARGUMENTS` から topic を取得
2. FORyusuke.md を Read（なければ作成）
3. 現在のセッションから学びを抽出:
   - 解決した問題
   - 試行錯誤の過程
   - 最終的な解決策
   - デバッグで得た知見
4. **FORyusuke.md のみに** 指定フォーマットで追記
5. 他のファイルへの Write は行わない

## 出力例

```markdown
## 2026-01-26 Claude Code設定監査

### 何を学んだか
- hooks timeout の単位は秒（ミリ秒ではない）
- permissions.deny は `./` プレフィックスでリポジトリ相対パス
- realpath で symlink を解決してからパス検証が必要

### 落とし穴
- timeout: 5000 は 5000秒（約83分）になっていた
- `*.env*` のようなワイルドカードは広すぎて誤爆する
- 文字列 `..` の検出では symlink 経由の迂回を防げない

### もう一度やるなら
- 公式ドキュメントの単位を最初に確認する
- 設定変更後はすぐにテストで検証する
- セキュリティ設定は多層防御で設計する
```
