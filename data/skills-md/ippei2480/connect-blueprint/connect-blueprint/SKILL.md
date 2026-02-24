---
name: connect-blueprint
description: >
  Design and generate Amazon Connect contact flow JSON from requirements or diagrams.
  Use when: (1) designing a new contact flow from scratch by gathering requirements,
  (2) converting draw.io/Mermaid diagrams or images into flow JSON,
  (3) deploying flows to AWS via CLI, (4) updating existing flows.
  Covers IVR menus, queue routing, Lambda integration, business hours checks, and flow modules.
license: MIT
compatibility: Requires AWS CLI with a valid profile (connect:* permissions). Python 3.8+ for layout.py.
metadata:
  author: ippei2480
  version: "0.6.0"
---

# connect-blueprint

## Overview

2つのモードで Amazon Connect コンタクトフローを生成する：

- **モードA（ゼロから設計）**: 要件ヒアリング → Mermaid設計図 → フローJSON → デプロイ
- **モードB（設計図から生成）**: draw.io/Mermaid/画像 → フローJSON → デプロイ

## Prerequisites

- AWS CLI + 有効なプロファイル（`aws sts get-caller-identity --profile <profile>` で確認）
- Connect インスタンスID（`aws connect list-instances --profile <profile>` で取得可）
- 必要IAM権限: `connect:*`

## Mode A: Design from Scratch

### Step 1: 要件ヒアリング

以下を確認する：
- 電話の目的・業種・主なユースケース
- IVR選択肢（番号と対応内容）
- 営業時間分岐の有無
- 外部システム連携（Lambda/DynamoDB等）
- 既存フローとの統合有無
- 通話録音の要否と録音対象（Agent / Customer / 両方）
- Contact Lens 分析の有効/無効
- 分析言語（ja-JP, en-US 等）
- 機密情報マスキング（redaction）の要否

**環境情報を取得してユーザーに見せる：**
```bash
# キュー一覧
aws connect list-queues --instance-id $INSTANCE_ID --queue-types STANDARD --profile $PROFILE

# プロンプト一覧
aws connect list-prompts --instance-id $INSTANCE_ID --profile $PROFILE

# Lambda一覧（Connect連携済み）
aws connect list-lambda-functions --instance-id $INSTANCE_ID --profile $PROFILE

# フローモジュール一覧
aws connect list-contact-flow-modules --instance-id $INSTANCE_ID --profile $PROFILE
```

実現不可能な要件があれば**この段階で明示してユーザーに伝える**。

### Step 2: Mermaid 設計図の生成

`references/mermaid_notation.md` の記法に従ってMermaid図を生成する。

**繰り返し処理（リトライメニュー等）は、まず `Loop` ActionType の使用を検討する。**
Loop で実現できない場合のみ `UpdateContactAttributes` + `Compare` によるカウンタ方式を検討する。

**Mermaid図は `.md` ファイルとして保存する**（例: `<flow-name>-design.md`）。
保存後、必ずユーザーにレビューを依頼し承認を得てから次のステップへ。

### Step 3: フローJSON生成

Mermaidからフロー構造を解析してJSON（Actions配列 + Transitions）を生成する。
`references/flow_json_structure.md` の構造仕様に従う。

**フローの最初のアクションは必ず `UpdateFlowLoggingBehavior` とする。**
`StartAction` に `UpdateFlowLoggingBehavior` のIDを設定し、その `NextAction` を本来のエントリーアクションにする。

#### AWS MCP Parameter Validation

各ActionTypeのパラメータを設定する際、`references/action_types.md` の共通ルールを確認した上で、AWS MCP で公式ドキュメントを参照してパラメータの正確性を保証する：

1. `references/action_types.md` の AWS Docs パス対応テーブルから該当URLパスを取得
2. `aws___read_documentation` でパラメータ仕様を確認
3. ドキュメントに基づいてパラメータを設定する

> **Why:** ローカルリファレンスはパラメータの概要のみ記載。正確なフィールド名・型・制約は AWS 公式ドキュメントが信頼できるソース。

**position付与:**
```bash
python3 scripts/layout.py <flow.json>
```

### Step 4: Validate & Deploy

**IMPORTANT: Always validate before deploying. Never skip this step.**

#### ローカルバリデーション (required)
```bash
./scripts/validate.sh flow.json
```
If validation returns errors, fix the flow JSON and re-validate before proceeding.
Only deploy after validation passes with no errors.

#### APIバリデーション (recommended)
```bash
./scripts/validate.sh --api --instance-id $INSTANCE_ID --profile $PROFILE flow.json
```
ローカルチェック通過後、`create-contact-flow --status SAVED` で下書きを作成してConnect APIによるバリデーションを実行する。成功時は下書きを自動削除する。

> **Why:** ローカルチェックはJSON構造・遷移参照の整合性のみ検証する。ActionType固有のパラメータ制約やErrors/Conditionsの妥当性はConnect API側でしか検証できないため、APIバリデーションで事前にエラーを検出する。

**エラーが発生した場合:**
1. まず aws-mcp (`aws___search_documentation` / `aws___read_documentation`) で AWS 公式ドキュメントを調査する
2. AWS公式ドキュメントに基づいて修正する
3. 推測による修正は避ける

#### Deploy

```bash
# Create new flow（SAVED → ACTIVE の2ステップ）
# Step 1: SAVED状態で作成
aws connect create-contact-flow \
  --instance-id $INSTANCE_ID \
  --name "Flow Name" \
  --type CONTACT_FLOW \
  --content "$(cat flow.json)" \
  --status SAVED \
  --profile $PROFILE

# Step 2: ACTIVE状態に変更（$FLOW_ID は Step 1 の出力から取得）
aws connect update-contact-flow-metadata \
  --instance-id $INSTANCE_ID \
  --contact-flow-id $FLOW_ID \
  --contact-flow-state ACTIVE \
  --profile $PROFILE

# Update existing flow
aws connect update-contact-flow-content \
  --instance-id $INSTANCE_ID \
  --contact-flow-id $FLOW_ID \
  --content "$(cat flow.json)" \
  --profile $PROFILE
```

> **Note:** `create-contact-flow` をデフォルト（PUBLISHED）で実行すると `InvalidContactFlowException` になる場合がある。`--status SAVED` → `update-contact-flow-metadata --contact-flow-state ACTIVE` の2ステップ方式を使用する。

## Mode B: Convert from Diagram

入力形式に応じて処理：
- **Mermaid**: そのまま Step A-3 へ
- **draw.io XML**: ノード/エッジを抽出してMermaidに変換 → Step A-3 へ
- **画像**: Vision解析でフロー構造を読み取り → Mermaidに変換 → Step A-3 へ

変換後は必ずユーザーに確認してから進む。

## Key Constraints

- `position` は **`Metadata.ActionMetadata.<id>.position`** に入れる（Action直下のMetadataは Connect API が拒否する）
- `Identifier` は UUID v4 形式
- `Version` は `"2019-10-30"` 固定
- `StartAction` は必ず1つ
- **`StartAction` は `UpdateFlowLoggingBehavior` にする**（ログ記録をフロー開始時に有効化）
- 全Actionに `Transitions` 必須（`DisconnectParticipant` は空 `{}` でOK）
- **Conditions 必須 ActionType**: `Loop`（ContinueLooping + DoneLooping）、`CheckHoursOfOperation`（True + False）、`Compare`（最低1条件）
- **StoreInput 使い分け**: IVRメニュー（選択肢分岐）は `StoreInput: "False"` + Conditions、自由入力（番号保存）は `StoreInput: "True"` + Conditions なし
- **サンプルフローは提供しない** — 要件に応じてゼロから設計すること

## Security Rules

### デプロイ操作の安全ガード
- `scripts/deploy.sh` の実行、または `aws connect create-contact-flow` / `aws connect update-contact-flow-content` コマンドの実行前に、**必ずユーザーの明示的な承認を得ること**
- `.env` ファイルや AWS クレデンシャルファイル（`~/.aws/credentials` 等）を読み取らないこと

### 安全な操作（確認不要）
- `scripts/validate.sh <file>` によるローカルバリデーション（`--api` オプション含む。下書き保存は自動削除される）
- `python3 scripts/layout.py <file>` によるレイアウト座標付与
- フローJSONの作成・編集

### プレースホルダー
- `<YOUR_XXX_ARN>` プレースホルダーを実際の ARN に置き換える際は、ユーザーから提供された値のみ使用すること
- 推測や仮の値で ARN を埋めないこと

### コーディング規約
- シェルスクリプト: 変数は必ずダブルクォートで囲む。AWS CLI 引数の組み立てには bash 配列を使用する
- Python: 標準ライブラリのみ使用（外部パッケージ不可）
- JSON: テンプレートでは実際の ARN/ID を使用せず `<YOUR_XXX>` プレースホルダーを使う

## Validation

3層バリデーション構造でフローの品質を保証する：

### Layer 1: AWS MCP パラメータ検証

フローJSON生成時に AWS MCP (`aws___read_documentation`) で各ActionTypeのパラメータ仕様を確認する。

- `references/action_types.md` の AWS Docs パス対応テーブルからURLパスを取得
- パラメータ名・型・必須/任意をドキュメントで照合
- 推測によるパラメータ設定を回避

### Layer 2: ローカルバリデーション

```bash
./scripts/validate.sh flow.json
```

JSON構造・遷移参照整合性・ActionType制約・孤立ブロック・デッドエンドを検出する。

### Layer 3: Connect API バリデーション

```bash
./scripts/validate.sh --api --instance-id $INSTANCE_ID --profile $PROFILE flow.json
```

ローカルチェックでは検出できないActionType固有のパラメータ制約やErrors/Conditionsの妥当性をConnect APIが検証する。`--status SAVED`（下書き保存）で作成するため本番に影響しない。

## Troubleshooting

### よくあるエラーと対処法

| エラー | 原因 | 対処 |
|--------|------|------|
| `Invalid flow content` | JSON構造の不備 | `./scripts/validate.sh` でチェック |
| `Position metadata in wrong location` | Action直下にMetadataを配置 | `Metadata.ActionMetadata.<id>.position` に移動 |
| `StartAction not found` | StartActionのIDがActions内に存在しない | UUIDの一致を確認 |
| `Queue not found` | キューARNが不正 | `aws connect list-queues` で正しいARNを取得 |
| `Lambda function not associated` | LambdaがConnectに未連携 | Connect管理画面でLambda関数を追加 |
| `Access denied` | IAM権限不足 | `connect:*` 権限をIAMポリシーに追加 |
| `Conditions required for Loop` | Loop に ContinueLooping/DoneLooping が不足 | 両方の Conditions を追加 |
| `StoreInput + Conditions conflict` | GetParticipantInput で StoreInput=True と Conditions を併用 | StoreInput=True なら Conditions を削除、IVRメニューなら StoreInput を削除 |
| `Missing True/False conditions` | CheckHoursOfOperation に True/False の Conditions が不足 | True と False の両方の Conditions を追加 |
| `InvalidContactFlowException on create` | `create-contact-flow` デフォルト（PUBLISHED）で失敗 | `--status SAVED` → `update-contact-flow-metadata --contact-flow-state ACTIVE` の2ステップで作成 |

### エラー調査の手順

1. まず `aws-mcp` (`aws___search_documentation` / `aws___read_documentation`) で AWS 公式ドキュメントを調査する
2. `references/action_types.md` の AWS Docs パス対応テーブルで該当ActionTypeのドキュメントパスを確認
3. AWS公式ドキュメントに基づいて修正を行う
4. 推測による修正は避け、必ず公式ドキュメントで裏付けを取る

### layout.py がエラーになる場合

- Python 3.8以上が必要
- 標準ライブラリのみ使用（追加インストール不要）
- 入力JSONが正しい構造か `validate.sh` で事前確認

## References

- Action Types詳細: `references/action_types.md`
- フローJSON構造: `references/flow_json_structure.md`
- Mermaid記法: `references/mermaid_notation.md`
- AWS CLIコマンド: `references/aws_cli_commands.md`
- レイアウトルール: `references/layout_rules.md`
- エラーハンドリング: `references/error_handling_patterns.md`
