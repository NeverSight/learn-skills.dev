---
name: pr-triage
description: PRの変更内容をトリアージし、変更カテゴリ分類・表層チェック・必要リファレンス判定を行います。結果を`.pr-triage.json`に出力し、後続のコードレビューフェーズで活用します。CI環境でのコスト最適化に使用してください。
---

# PRトリアージ

PRの変更内容を分析し、後続のコードレビューフェーズに必要な情報を構造化して出力するスキルです。
軽量モデル（Haiku）での実行を想定しており、CI環境でのコスト最適化に寄与します。

## 手順

1. `gh pr view <PR番号> --json title,body,headRefName,baseRefName,changedFiles` でPR情報を取得
2. `gh pr diff <PR番号> --name-only` で変更ファイル一覧を取得
3. 差分の取得（**changedFilesが15以上の場合、手順3はスキップしてファイル名とPR説明のみで分析する**）：
   - changedFilesが15未満の場合のみ `gh pr diff <PR番号>` でコード差分を取得
   - 表層チェックが必要なファイル（.ts, .js, .tsx, .jsx）が多い場合は個別に `gh pr diff <PR番号> -- <file>` で取得
4. `.pr-review-state.json` が存在するか確認する（前回レビュー状態）
5. 以下の分析を行う：
   - 変更ファイルのカテゴリ分類（added/modified/deleted）
   - 使用言語・フレームワークの検出
   - 変更カテゴリの判定（認可変更、DB変更、RLS変更、API変更、テスト変更、設定変更、スキル変更）
   - 必要なリファレンスファイルの判定
   - Minor/Suggestionレベルの表層的問題の検出（インクリメンタルモード時は変更ファイルのみ）
   - 差分の要約（200文字以内）
   - レビュー時に注目すべきポイント
6. 分析結果を `.pr-triage.json` ファイルに出力する

## インクリメンタルモード（.pr-review-state.json が存在する場合）

前回のレビュー状態を活用してチェック範囲を最適化する：

1. `.pr-review-state.json` の `last_reviewed_commit` を取得する
2. `git diff <last_reviewed_commit>..HEAD --name-only` で前回レビュー以降に変更されたファイルを特定する
3. **変更のないファイル**の `surface_issues` は前回の状態からそのまま引き継ぐ（`"carried_over": true` を付与）。再チェックしない。
4. **変更があったファイル**のみ表層チェックを実行する
5. 前回の `surface_issues` と `review_comments` のうち、該当箇所が修正されたものを `resolved_issues` に含める
6. 出力の `.pr-triage.json` に `"incremental": true`、`"base_commit"`、`"changed_since_last_review"`、`"unchanged_since_last_review"`、`"resolved_issues"` フィールドを追加する

`resolved_issues` のフォーマット：
```json
{
  "comment_id": 12345678,
  "file": "<ファイルパス>",
  "line": 42,
  "issue": "<元の問題の説明>",
  "resolution": "fixed"
}
```

> `.pr-review-state.json` が存在しない場合は、通常のフルトリアージを実行する。
> `.pr-review-state.json` が不正な形式（JSONパースエラー等）の場合は、警告を出力してフルトリアージを実行する。破損した状態ファイルに基づいてインクリメンタルモードを実行してはならない。

## 必要なリファレンスの判定基準

以下の条件に該当する場合のみ、対応するリファレンスを `required_references` に含める：
- TypeScript/JavaScript ファイルの変更あり → `typescript-best-practices.md`
- 認証・認可に関わるコード変更あり（auth, permission, role, session, token等のキーワード） → `authorization-review-general.md`
- PostgreSQL RLS に関わる変更あり（RLS, row level security, policy等のキーワード） → `authorization-review-postgres-rls.md`
- SKILL.md ファイルの変更あり → `skill-review.md`
- CI環境でのGitHub投稿が必要 → `github-pr-review-actions.md`（常に含める）

## 表層チェック項目（Minor/Suggestion）

差分を確認し、以下の問題を検出する（該当するもののみ）：
- `any` 型の使用（TypeScript）
- `var` キーワードの使用（TypeScript/JavaScript）
- 空のインターフェイス定義
- マジックナンバーの使用
- 命名規則違反（camelCase/PascalCase/UPPER_CASE）
- テストの未追加（新規ファイルがあるのにテストファイルがない）

## 出力フォーマット

`.pr-triage.json` に以下のJSON構造で出力すること：

```json
{
  "pr_number": 123,
  "incremental": false,
  "base_commit": "<前回レビュー時のコミットSHA（インクリメンタル時のみ）>",
  "summary": "<変更の概要（1-2文）>",
  "files": {
    "added": ["<追加ファイルパス>"],
    "modified": ["<変更ファイルパス>"],
    "deleted": ["<削除ファイルパス>"]
  },
  "changed_since_last_review": ["<前回から変更があったファイル（インクリメンタル時のみ）>"],
  "unchanged_since_last_review": ["<前回から変更がないファイル（インクリメンタル時のみ）>"],
  "languages": ["<検出された言語>"],
  "frameworks": ["<検出されたフレームワーク>"],
  "change_categories": {
    "has_auth_changes": false,
    "has_db_changes": false,
    "has_rls_changes": false,
    "has_api_changes": false,
    "has_test_changes": false,
    "has_config_changes": true,
    "has_skill_changes": true
  },
  "required_references": ["<必要なリファレンスファイル名>"],
  "surface_issues": [
    {
      "severity": "Minor|Suggestion",
      "file": "<ファイルパス>",
      "line": 15,
      "issue": "<問題の説明>",
      "suggestion": "<改善案>",
      "carried_over": true
    }
  ],
  "resolved_issues": [
    {
      "comment_id": 12345678,
      "file": "<ファイルパス>",
      "line": 42,
      "issue": "<元の問題の説明>",
      "resolution": "fixed"
    }
  ],
  "diff_summary": "<差分の要約（200文字以内）>",
  "estimated_complexity": "low|medium|high",
  "focus_areas": ["<レビュー時の注目ポイント>"]
}
```

重要:
- テキスト出力は最小限にし、`.pr-triage.json` の出力に集中してください。
