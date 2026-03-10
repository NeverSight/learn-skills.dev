---
name: migrate-skill-to-agent
description: >-
  スキルディレクトリを `.claude/skills/{name}` から `.agents/skills/{name}` へ移動し、
  `.claude/skills/{name}` と `.codex/skills/{name}` の両方からシンボリックリンクを作成するマイグレーションスキル。
  スキルの実体を `.agents/skills/` に一元化し、Claude Code と Codex CLI の両方から
  参照可能にするディレクトリ構成を実現する。引数としてスキル名が必須。
  トリガー：「スキルを .agents に移動」「スキルをマイグレート」「シンボリックリンクを作成」
  「migrate skill」「スキルの配置を統一」といったスキル配置変更リクエストで起動。
---

# Migrate Skill To Agent

`.claude/skills/{name}` にあるスキルを `.agents/skills/{name}` へ移動し、
`.claude/skills/` と `.codex/skills/` の両方からシンボリックリンクを張る。

## 使い方

引数としてスキル名を受け取り、`scripts/migrate.sh` を実行する。

```bash
bash scripts/migrate.sh <skill-name> [project-root]
```

- `skill-name`（必須）: 移動対象のスキル名（ディレクトリ名）
- `project-root`（省略可）: プロジェクトルートパス。省略時はカレントディレクトリ

## 実行前の確認事項

- `.claude/skills/{name}` が実ディレクトリとして存在すること（シンボリックリンクでないこと）
- `.agents/skills/{name}` がまだ存在しないこと

## 実行結果

```
移動前:
  .claude/skills/{name}/  (実ディレクトリ)

移動後:
  .agents/skills/{name}/               (実体)
  .claude/skills/{name} -> ../../.agents/skills/{name}  (シンボリックリンク)
  .codex/skills/{name}  -> ../../.agents/skills/{name}  (シンボリックリンク)
```

## ワークフロー

1. ユーザーからスキル名を引数として受け取る
2. バリデーション（ソースの存在確認、既存リンクチェック、ターゲット重複チェック）
3. `scripts/migrate.sh` をプロジェクトルートを第2引数として実行
4. 結果を報告

## 実行例

ユーザー: 「intent-based-dedup を .agents に移動して」

```bash
bash /path/to/migrate-skill-to-agent/scripts/migrate.sh intent-based-dedup /path/to/project
```
