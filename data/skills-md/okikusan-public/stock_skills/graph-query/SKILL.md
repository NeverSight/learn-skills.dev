---
name: graph-query
description: 知識グラフへの自然言語クエリ。過去のレポート・スクリーニング・取引・リサーチ・市況を検索。
argument-hint: "自然言語クエリ（例: トヨタの前回レポートは？）"
allowed-tools: Bash(python3 *)
---

# グラフクエリスキル

知識グラフ（Neo4j）に蓄積された過去データを自然言語で検索する。

## 実行コマンド

```bash
python3 .claude/skills/graph-query/scripts/run_query.py "自然言語クエリ"
```

## 自然言語ルーティング

自然言語→スキル判定は [.claude/rules/intent-routing.md](../../rules/intent-routing.md) を参照。

## 出力

結果はMarkdown形式で表示される。データが見つからない場合はその旨を表示。
Neo4j が未接続の場合は「データが見つかりませんでした」と表示。

## 前提知識統合ルール (KIK-466)

グラフクエリ結果を表示する際、会話文脈と統合:

- クエリ結果に保有銘柄が含まれれば「保有中」マークを付記
- 過去レポートの検索結果は「最新データとの差分を確認するなら /stock-report 推奨」と促す
