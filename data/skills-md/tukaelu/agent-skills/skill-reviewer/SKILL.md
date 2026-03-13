---
name: skill-reviewer
description: >
  Claude Code スキルを公式ベストプラクティスに基づいてレビューし、
  具体的な改善提案を行います。
  「このスキルをレビューして」「スキル品質をチェック」「SKILL.md を検証」
  「このスキルを改善したい」などのリクエストで起動します。
allowed-tools:
  - AskUserQuestion
  - Glob
  - Read
  - Edit
model: sonnet
---

# Skill Reviewer

公式ベストプラクティスに基づいてスキルをレビューし、具体的な改善提案を行う。

## レビューワークフロー

### Step 1: 対象スキルの特定

レビュー対象の SKILL.md ファイルを特定する：
- ユーザーがパスを直接指定している場合はそれを使用
- カレントディレクトリで SKILL.md を検索
- 複数のスキルが存在する場合は AskUserQuestion で選択させる（最大4件。それ以上は「Other」で直接入力）

### Step 2: 読み込みと分析

1. 対象の SKILL.md ファイルを完全に読み込む
2. [best-practices.md](references/best-practices.md) でチェックリストを確認

### Step 3: ベストプラクティスとの照合

[best-practices.md](references/best-practices.md) の各カテゴリに照らして評価する。

### Step 4: レビューレポート生成

以下の形式で出力する：

```markdown
# スキルレビューレポート: {skill-name}

## サマリー
- 総合評価: {PASS | NEEDS_IMPROVEMENT | CRITICAL_ISSUES}
- Critical: {件数}
- Warning: {件数}
- Info: {件数}

## Critical（必須修正）
{修正必須の問題をリスト}

## Warning（推奨修正）
{推奨される改善をリスト}

## Info（改善提案）
{オプションの強化をリスト}

## 具体的な推奨事項
{例を含む具体的なアクションアイテム}
```

### Step 5: インタラクティブな改善

レポート提示後、AskUserQuestion で修正意向を確認する：

```javascript
AskUserQuestion({
  questions: [{
    question: "指摘された問題を修正しますか？",
    header: "修正方針",
    options: [
      { label: "順々に確認しながら修正", description: "1件ずつ提案・確認しながら進める（推奨）" },
      { label: "Critical のみ修正",      description: "必須修正のみ自動適用する" },
      { label: "すべて自動修正",         description: "全問題を確認なしで修正する" },
      { label: "修正しない",             description: "レポートのみ参照する" }
    ],
    multiSelect: false
  }]
})
```

修正時のルール：
- Critical 問題を優先する
- 段階的に修正を適用する
- 各修正後に再検証：修正済みの SKILL.md を Read で読み直し、該当項目が best-practices.md のチェックを満たしているか確認する
