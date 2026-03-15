---
name: acomo
description: >
  プラットフォーム利用者（acomo 上でワークフローモデルを使って開発する開発者）向け。
  acomo CLI および公開 API の標準的な使い方（モデル取得・プロセス操作・認証）を案内する。
  acomo 本体の内部実装は対象外。
  acomo CLI を使うとき、ワークフローやプロセスの操作・モデル定義の確認を行うときに参照する。
---

# acomo CLI / API 標準ガイド

acomo はワークフロー管理プラットフォームです。このスキルは **acomo CLI と公開 API の標準的な使い方**（モデル一覧・モデル定義取得・プロセス開始・保存・提出・承認・却下・差し戻しなど）を案内します。

## 前提・実行環境

- **acomo CLI が実行できる環境**（PATH に `acomo` が存在すること）を前提とします。
- エージェントが CLI を実行する場合、リモートサンドボックス等ではローカルの `~/.acomo/config.json` や環境変数が自動継承されないことがあります。CI・エージェント実行時は環境変数（`ACOMO_ACCESS_TOKEN`, `ACOMO_TENANT_ID`, `ACOMO_BASE_URL`）の設定を推奨します。
- 認証未設定時も API コマンドは存在し、実行時に終了コード 2 と stderr の `AUTH_REQUIRED` で失敗します。その場合はユーザーに再ログイン（または環境変数設定）を促してください。

## 認証エラー時の扱い

**認証エラー（認証未設定・401/403、終了コード 2）が出た場合は、試行錯誤で解決しようとしないこと。** 速やかにユーザーにログインを促し、処理を中断する。

- `acomo login` の実行、または環境変数 `ACOMO_ACCESS_TOKEN`, `ACOMO_TENANT_ID` の設定

## 認証

- **ローカル利用**: `acomo login` で `~/.acomo/config.json` に永続保存。
- **CI・エージェント環境**: 環境変数での認証を推奨。

アクセストークンはブラウザで acomo にログインした後に入手し、CLI で指定する。

```bash
# 環境変数で認証（非インタラクティブ向け）
export ACOMO_ACCESS_TOKEN="your-token"
export ACOMO_TENANT_ID="your-tenant-id"

# または login で保存
acomo login --tenant-id <tenantId> --access-token <accessToken>
```

| 環境変数             | 説明                                            | 必須 |
| -------------------- | ----------------------------------------------- | ---- |
| `ACOMO_ACCESS_TOKEN` | アクセストークン                                | Yes  |
| `ACOMO_TENANT_ID`    | テナント ID                                     | Yes  |
| `ACOMO_BASE_URL`     | API Base URL（省略時: `https://acomo.app`）     | No   |

CLI の出力は JSON です。パラメータは `acomo <operationId> --help` で確認する。

## 呼び出し形式

```bash
acomo <operationId> [JSON引数]
```

```bash
# 引数あり
acomo getWorkflowModel '{"modelId":"<ID>"}'

# stdin から
echo '{"modelId":"<ID>"}' | acomo getWorkflowModel
```

## 標準フロー

1. **モデル一覧**: `acomo listWorkflowModels` で対象モデルを特定する。フィルタ例: `acomo listWorkflowModels '{"filter":"{\"name\":{\"contains\":\"申請\"}}","take":10}'`
2. **モデル定義**: `acomo getWorkflowModel '{"modelId":"<ID>"}'` で definition / dataSchema / policy の JSON を取得する。
3. **プロセス操作**: 必要に応じて `startWorkflowProcess` / `saveWorkflowProcess` / `submitWorkflowProcess` / `submitWorkflowProcessWithNodeId` / `approveWorkflowProcess` / `rejectWorkflowProcess` / `revertWorkflowProcess` を使う。自分のプロセス一覧は `listMyProcesses` や `listProcessWithNodeActions` を検討する。

## 主要コマンド早見

| 用途 | コマンド |
| --- | --- |
| モデル一覧 | `listWorkflowModels` |
| モデル定義取得 | `getWorkflowModel`（modelId 必須） |
| 編集中モデル | `getWorkflowModelWithLatestModelHistory` |
| プロセス開始 | `startWorkflowProcess` |
| データ保存 | `saveWorkflowProcess` |
| 提出 | `submitWorkflowProcess` / `submitWorkflowProcessWithNodeId` |
| 承認 | `approveWorkflowProcess` |
| 却下 | `rejectWorkflowProcess` |
| 差し戻し | `revertWorkflowProcess`（processId, nodeId） |
| 自分のプロセス一覧 | `listMyProcesses` / `listProcessWithNodeActions` |
| 自分のプロセス取得 | `getMyProcesses` / `getProcessWithNodeActions` |

プロセス操作では、タスクノードでは dataSchema に沿ったデータを `saveWorkflowProcess` の `updateProcessDto.data` で送る。遷移は submit / approve / reject / revert で実行する。policy の write/read に従い、現在ノードで編集可能な項目だけを扱う。

## 補足

- データ構造（definition / dataSchema / policy / 条件式）の詳細は [reference.md](reference.md) を参照する。
- 全コマンド一覧は `acomo --help` で確認する。
