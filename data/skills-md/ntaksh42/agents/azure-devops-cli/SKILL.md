---
name: azure-devops-cli
description: Generate Azure DevOps CLI commands for automation and scripting. Use when automating Azure DevOps operations via CLI.
---

# Azure DevOps CLI Skill

Azure DevOps CLIの使用を支援するスキルです。

## 主な機能

- **CLI コマンド生成**: よく使うコマンド
- **認証設定**: PAT、OAuth
- **パイプライン操作**: 実行、キャンセル
- **リポジトリ操作**: クローン、PR作成
- **ワークアイテム**: 作成、更新、クエリ

## セットアップ

```bash
# Azure DevOps拡張インストール
az extension add --name azure-devops

# デフォルト組織・プロジェクト設定
az devops configure --defaults organization=https://dev.azure.com/myorg project=MyProject

# PAT認証
export AZURE_DEVOPS_EXT_PAT=your-personal-access-token
```

## パイプライン操作

```bash
# パイプライン一覧
az pipelines list --output table

# パイプライン実行
az pipelines run --name "MyPipeline" --branch main

# ビルド一覧
az pipelines build list --status inProgress --output table

# ビルド詳細
az pipelines build show --id 123

# ビルドキャンセル
az pipelines build cancel --id 123

# ビルドログ
az pipelines runs artifact download --artifact-name logs --path ./logs --run-id 123
```

## リポジトリ操作

```bash
# リポジトリ一覧
az repos list --output table

# リポジトリ作成
az repos create --name "new-repo"

# PR作成
az repos pr create \
  --source-branch feature/new-feature \
  --target-branch main \
  --title "Add new feature" \
  --description "Implements feature XYZ"

# PR一覧
az repos pr list --status active

# PRレビュー
az repos pr reviewers add --id 123 --reviewers user@example.com

# PRマージ
az repos pr update --id 123 --status completed
```

## ワークアイテム操作

```bash
# ワークアイテム作成
az boards work-item create \
  --title "Implement login feature" \
  --type "User Story" \
  --assigned-to user@example.com \
  --fields "System.Tags=authentication;security"

# ワークアイテム更新
az boards work-item update --id 123 --state Active

# クエリ実行
az boards query --wiql "SELECT [System.Id], [System.Title] FROM WorkItems WHERE [System.WorkItemType] = 'Bug'"

# 関連
付け
az boards work-item relation add --id 123 --relation-type "Related" --target-id 456
```

## アーティファクト操作

```bash
# Feedリスト
az artifacts universal list --feed MyFeed

# パッケージアップロード
az artifacts universal publish \
  --organization https://dev.azure.com/myorg \
  --feed MyFeed \
  --name my-package \
  --version 1.0.0 \
  --description "Package description" \
  --path ./dist

# パッケージダウンロード
az artifacts universal download \
  --organization https://dev.azure.com/myorg \
  --feed MyFeed \
  --name my-package \
  --version 1.0.0 \
  --path ./downloads
```

## 便利なスクリプト

### 失敗したビルドを再実行

```bash
#!/bin/bash
FAILED_BUILDS=$(az pipelines build list --status failed --query "[].id" -o tsv)

for BUILD_ID in $FAILED_BUILDS; do
  echo "Retrying build $BUILD_ID"
  az pipelines build queue --definition-id $(az pipelines build show --id $BUILD_ID --query "definition.id" -o tsv)
done
```

### PRの自動承認（条件付き）

```bash
#!/bin/bash
PRS=$(az repos pr list --status active --query "[?sourceRefName=='refs/heads/dependabot/*'].pullRequestId" -o tsv)

for PR_ID in $PRS; do
  echo "Auto-approving PR $PR_ID"
  az repos pr update --id $PR_ID --vote approve
done
```

## バージョン情報
- Version: 1.0.0
