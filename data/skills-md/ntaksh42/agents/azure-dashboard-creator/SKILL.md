---
name: azure-dashboard-creator
description: Create Azure DevOps dashboards with widgets and metrics. Use when visualizing project metrics or creating team dashboards.
---

# Azure Dashboard Creator Skill

Azure DevOpsダッシュボードを作成するスキルです。

## 主な機能

- **ウィジェット配置**: チャート、グラフ
- **クエリベース**: WIQLクエリ結果表示
- **ビルド状況**: パイプライン状態
- **チームメトリクス**: ベロシティ、バーンダウン

## ダッシュボード作成（REST API）

```json
{
  "name": "Team Dashboard",
  "widgets": [
    {
      "name": "Build Status",
      "position": {
        "row": 1,
        "column": 1
      },
      "size": {
        "rowSpan": 1,
        "columnSpan": 2
      },
      "settings": {
        "buildDefinitionId": "123"
      },
      "contributionId": "ms.vss-build-web.build-definition-widget"
    },
    {
      "name": "Active Bugs",
      "position": {
        "row": 2,
        "column": 1
      },
      "size": {
        "rowSpan": 2,
        "columnSpan": 2
      },
      "settings": {
        "queryId": "456"
      },
      "contributionId": "ms.vss-dashboards-web.Microsoft.VisualStudioOnline.Dashboards.QueryResultsWidget"
    }
  ]
}
```

## バージョン情報
- Version: 1.0.0
