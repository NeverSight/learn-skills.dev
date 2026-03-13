---
name: investment-note
description: 投資メモの管理。投資テーゼ・懸念・学びなどをノートとして記録・参照・削除。
argument-hint: "[save|list|delete] [--symbol SYMBOL] [--category CATEGORY] [--type TYPE] [--content TEXT] [--id NOTE_ID]"
allowed-tools: Bash(python3 *)
---

# 投資メモ管理スキル

$ARGUMENTS を解析し、以下のコマンドを実行してください。

## 実行コマンド

```bash
python3 /Users/kikuchihiroyuki/stock-skills/.claude/skills/investment-note/scripts/manage_note.py $ARGUMENTS
```

結果をそのまま表示してください。

## コマンド一覧

### save -- メモ保存

```bash
# 銘柄メモ（従来通り）
python3 .../manage_note.py save --symbol 7203.T --type thesis --content "EV普及で部品需要増"

# PF全体メモ（KIK-429: symbolオプション化）
python3 .../manage_note.py save --category portfolio --type review --content "セクター偏重を改善"

# 市況メモ
python3 .../manage_note.py save --category market --type observation --content "日銀利上げ観測"
```

`--symbol` と `--category` のいずれかは必須（`journal` タイプを除く）。`--symbol` 指定時はカテゴリは自動で `stock`。

```bash
# 投資日記 / フリーメモ（KIK-473: symbol/category 不要）
python3 .../manage_note.py save --type journal --content "NVDAが急騰。AI需要の強さを感じた"
# → 本文中のティッカーシンボル（NVDA）を自動検出し Neo4j に紐付け
```

### list -- メモ一覧

```bash
python3 .../manage_note.py list [--symbol 7203.T] [--type concern] [--category portfolio]
```

### delete -- メモ削除

```bash
python3 .../manage_note.py delete --id note_2025-02-17_7203_T_abc12345
```

## ノートタイプ

| タイプ | 意味 | 使い方例 |
|:---|:---|:---|
| thesis | 投資テーゼ | 「EV普及で部品需要増」 |
| observation | 気づき | 「3回連続スクリーニング上位」 |
| concern | 懸念 | 「中国市場の減速リスク」 |
| review | 振り返り | 「3ヶ月保有、テーゼ通り推移」 |
| target | 目標・出口 | 「PER 15 で利確」 |
| lesson | 学び | 「バリュートラップだった」 |
| journal | 投資日記・フリーメモ | 「NVDAが急騰。AI需要を感じた」（KIK-473: symbol/category不要、本文から銘柄自動検出） |

## カテゴリ (KIK-429)

| カテゴリ | 意味 | 使い方 |
|:---|:---|:---|
| stock | 個別銘柄メモ | `--symbol` 指定時に自動設定 |
| portfolio | PF全体メモ | `--category portfolio`（PF振り返り、リバランス理由等） |
| market | 市況メモ | `--category market`（マクロ動向、金利等） |
| general | 汎用メモ | `--category general`（未分類、デフォルト） |

## 自然言語ルーティング

自然言語→スキル判定は [.claude/rules/intent-routing.md](../../rules/intent-routing.md) を参照。

## 前提知識統合ルール (KIK-466)

get_context.py の出力がある場合、メモ操作と統合:

- **save**: 保存対象銘柄の直近状態（最新レポート・ヘルスチェック結果）を参照し、メモ内容の文脈を補強
- **list**: メモ一覧表示時、対象銘柄の現在の保有状態（保有中/売却済み/ウォッチ中）を付記
