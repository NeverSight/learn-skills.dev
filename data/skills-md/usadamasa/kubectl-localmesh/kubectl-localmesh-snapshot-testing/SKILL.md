---
name: kubectl-localmesh-snapshot-testing
description: kubectl-localmeshのスナップショットテスト（Envoy設定とマッピング）の実行・更新タイミングと運用ガイドラインを提供します
allowed-tools: ["Bash", "Read"]
---

# kubectl-localmesh スナップショットテスト運用ガイド

## 対象プロジェクト

kubectl-localmeshプロジェクトのスナップショットテスト運用を支援します。

## 概要

kubectl-localmeshは、Envoy設定とport-forwardマッピングを動的に生成します。スナップショットテストは、これらの生成結果が期待通りであることを検証する仕組みです。

### 検証対象

1. **Envoy設定ファイル** (`test/snapshot/testdata/snapshots/*.yaml`)
   - HTTP/gRPCリスナー設定
   - TCP proxyリスナー設定
   - Upstreamクラスタ設定
   - ルーティング設定

2. **Port-forwardマッピング** (`test/snapshot/testdata/portforward-mappings/*.txt`)
   - サービス名とローカルポートのマッピング
   - 各サービスの接続先情報

## テスト実行タイミング

### 必須実行タイミング

以下のタイミングでは**必ず**スナップショットテストを実行してください：

1. **Envoy設定生成ロジックを変更した後**
   - `internal/envoy/`配下のコード変更
   - プロトコル設定の変更（HTTP/gRPC/TCP）
   - リスナー設定の変更

2. **マッピング生成ロジックを変更した後**
   - `internal/snapshot/`配下のコード変更
   - Port-forward割り当てロジックの変更

3. **dump-envoy-config実装を変更した後**
   - `internal/dump/`配下のコード変更
   - `cmd/dump_envoy_config.go`の変更

4. **プルリクエスト作成前**
   - すべての変更が意図通りであることを確認

5. **コミット前の確認**
   - 変更が他の設定に意図しない影響を与えていないか確認

### 自動実行

- CIパイプラインで自動実行されます
- テスト失敗時はマージがブロックされます

## スナップショット更新タイミング

### 更新が適切なケース

以下の場合は、スナップショットの更新が**期待される動作**です：

1. **意図的にEnvoy設定を変更した時**
   ```bash
   # 例: 新しいプロトコルオプションを追加
   # 実装後、スナップショットを更新
   test/snapshot/scripts/update-snapshots.sh
   ```

2. **新機能追加でスナップショットが変わるべき時**
   ```bash
   # 例: TCP proxyサポート追加
   # 新しいスナップショットを生成
   test/snapshot/scripts/update-snapshots.sh
   ```

3. **テストケース追加時**
   ```bash
   # 新しいconfigファイルを追加後
   test/snapshot/scripts/update-snapshots.sh
   ```

### ⚠️ 注意: 更新してはいけないケース

以下の場合は、スナップショットを更新**してはいけません**：

1. **テストが失敗した時、原因を理解せずに更新**
   - まず差分を確認し、なぜ変わったのかを理解する
   - 意図しない変更の場合は、実装コードを修正する

2. **「とりあえず」テストを通すための更新**
   - スナップショット更新は「期待値を変更する」行為
   - 変更理由が明確でない場合は更新しない

3. **git diffを確認せずに更新**
   - 必ず差分をレビューしてから更新する

## 基本コマンド

### テスト実行

```bash
# すべてのスナップショットテストを実行
test/snapshot/scripts/run-snapshots.sh
```

**前提条件:**
- `task build`でバイナリをビルド済み
- `bin/kubectl-localmesh`が存在する

**出力例:**
```
✅ PASS: basic
✅ PASS: tcp-service
❌ FAIL: grpc-service

Summary: 2/3 tests passed
```

### スナップショット更新

```bash
# すべてのスナップショットを更新
test/snapshot/scripts/update-snapshots.sh
```

**実行後の確認:**
```bash
# 差分を必ず確認する
git diff test/snapshot/testdata/snapshots/
git diff test/snapshot/testdata/portforward-mappings/
```

### 個別テストケースの確認

```bash
# 特定のテストケースのみ確認
test/snapshot/scripts/diff-snapshot.sh basic
```

## ワークフロー例

### 新機能開発時

```bash
# 1. ビルド
task build

# 2. スナップショットテスト実行（現状確認）
test/snapshot/scripts/run-snapshots.sh

# 3. 機能実装
# ... コードを編集 ...

# 4. ビルド
task build

# 5. スナップショットテスト実行（変更確認）
test/snapshot/scripts/run-snapshots.sh

# 6. 期待通りの変更ならスナップショット更新
test/snapshot/scripts/update-snapshots.sh

# 7. 差分レビュー
git diff test/snapshot/testdata/

# 8. 変更が正しいことを確認してコミット
git add .
git commit -m "feat: 新機能を追加"
```

### バグ修正時

```bash
# 1. ビルド
task build

# 2. スナップショットテスト実行（バグ再現確認）
test/snapshot/scripts/run-snapshots.sh

# 3. バグ修正
# ... コードを編集 ...

# 4. ビルド
task build

# 5. スナップショットテスト実行（修正確認）
test/snapshot/scripts/run-snapshots.sh

# 6. テストが通れば完了（スナップショット更新不要）
# テストが失敗する場合は、期待値が変わったことを確認
git diff test/snapshot/testdata/

# 7. 必要に応じてスナップショット更新
test/snapshot/scripts/update-snapshots.sh
```

### テストケース追加時

```bash
# 1. 新しい設定ファイルを作成
cat > test/snapshot/testdata/configs/new-feature.yaml <<EOF
listener_port: 80
services:
  - kind: kubernetes
    host: new-service.localhost
    namespace: default
    service: new-service
    port: 8080
    protocol: http
EOF

# 2. モック設定ファイルを作成
cat > test/snapshot/testdata/mocks/new-feature.yaml <<EOF
namespace: default
service: new-service
port: 8080
EOF

# 3. スナップショットを生成
test/snapshot/scripts/update-snapshots.sh

# 4. 生成されたスナップショットを確認
cat test/snapshot/testdata/snapshots/new-feature.yaml
cat test/snapshot/testdata/portforward-mappings/new-feature.txt

# 5. スナップショットテスト実行
test/snapshot/scripts/run-snapshots.sh

# 6. テストが通ることを確認してコミット
git add test/snapshot/testdata/
git commit -m "test: new-feature用のスナップショットテストを追加"
```

## トラブルシューティング

### ビルドエラー

```bash
# エラー: bin/kubectl-localmesh: No such file or directory
# 解決策: ビルドを実行
task build
```

### テスト失敗時の確認手順

1. **差分を確認する**
   ```bash
   # 個別テストケースの差分を確認
   test/snapshot/scripts/diff-snapshot.sh <test-case>
   ```

2. **実際の出力を確認する**
   ```bash
   # dump-envoy-configを直接実行
   bin/kubectl-localmesh dump-envoy-config \
     -f test/snapshot/testdata/configs/<test-case>.yaml \
     --mock-config test/snapshot/testdata/mocks/<test-case>.yaml
   ```

3. **変更理由を理解する**
   - なぜスナップショットが変わったのか？
   - 意図した変更か？
   - 他のテストケースへの影響は？

4. **適切な対応を取る**
   - 意図した変更 → スナップショット更新
   - 意図しない変更 → 実装コード修正

### スナップショット差分のレビュー方法

```bash
# 1. すべての変更を確認
git diff test/snapshot/testdata/

# 2. Envoy設定の差分を確認
git diff test/snapshot/testdata/snapshots/

# 3. マッピングの差分を確認
git diff test/snapshot/testdata/portforward-mappings/

# 4. 具体的なファイルの差分を確認
git diff test/snapshot/testdata/snapshots/<test-case>.yaml
```

**確認ポイント:**
- リスナー設定の変更は意図通りか？
- クラスタ設定の変更は意図通りか？
- ルーティング設定の変更は意図通りか？
- Port-forwardマッピングの変更は意図通りか？

## テストケース追加ガイドライン

### 新しいテストケースを追加する条件

以下の場合は、新しいテストケースを追加することを検討してください：

1. **新しいプロトコルサポート追加**
   - 例: HTTP/3サポート追加

2. **新しいサービスタイプ追加**
   - 例: WebSocketサポート追加

3. **エッジケースの追加**
   - 例: 複数のSSH bastionを使用するケース

4. **バグ修正のリグレッション防止**
   - 例: 特定の設定でクラッシュしたバグ

### テストケースの命名規則

- わかりやすい名前を付ける
- 例: `basic`, `tcp-service`, `grpc-service`, `multiple-ssh-bastions`

### ディレクトリ構造

```
test/snapshot/testdata/
├── configs/
│   └── <test-case>.yaml          # テスト設定ファイル
├── mocks/
│   └── <test-case>.yaml          # モック設定ファイル
├── snapshots/
│   └── <test-case>.yaml          # Envoy設定スナップショット
└── portforward-mappings/
    └── <test-case>.txt           # マッピングスナップショット
```

## TDD（Test-Driven Development）との統合

kubectl-localmeshプロジェクトではTDDを採用しています。スナップショットテストもTDDフローに統合できます：

### TDDフロー

1. **期待される設定変更を先に定義**
   ```bash
   # 新しいスナップショットを手動で作成（期待値）
   vim test/snapshot/testdata/snapshots/new-feature.yaml
   ```

2. **実装コードを書く**
   ```bash
   # internal/envoy/ 配下のコードを編集
   ```

3. **テストを実行して確認**
   ```bash
   task build
   test/snapshot/scripts/run-snapshots.sh
   ```

4. **テストが通るまで実装を調整**
   ```bash
   # 実装コードを修正
   task build
   test/snapshot/scripts/run-snapshots.sh
   ```

## 関連ファイル

### スナップショット生成ロジック

- `internal/envoy/`: Envoy設定生成ロジック
  - `internal/envoy/envoy.go`: メイン実装
  - HTTP/gRPCリスナー設定
  - TCP proxyリスナー設定
  - Upstreamクラスタ設定

- `internal/snapshot/`: マッピング生成ロジック
  - `internal/snapshot/snapshot.go`: スナップショット構造体
  - Port-forwardマッピング生成

- `internal/dump/`: dump-envoy-config実装
  - `internal/dump/dump.go`: ダンプコマンドロジック
  - モック設定サポート

### テストスクリプト

- `test/snapshot/scripts/run-snapshots.sh`: テスト実行
- `test/snapshot/scripts/update-snapshots.sh`: スナップショット更新
- `test/snapshot/scripts/diff-snapshot.sh`: 差分チェック

### テストデータ

- `test/snapshot/testdata/configs/`: テスト設定ファイル
- `test/snapshot/testdata/mocks/`: モック設定ファイル
- `test/snapshot/testdata/snapshots/`: Envoy設定スナップショット
- `test/snapshot/testdata/portforward-mappings/`: マッピングスナップショット

## 関連Skills

- `go-taskfile-workflow`: ビルドとテスト実行
- `kubectl-envoy-debugging`: Envoy設定のデバッグ
- `kubectl-localmesh-logging-guide`: ログ出力の理解
