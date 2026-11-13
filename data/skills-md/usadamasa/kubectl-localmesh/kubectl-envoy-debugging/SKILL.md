---
name: kubectl-envoy-debugging
description: kubectl + Envoyベースのツールのデバッグと設定確認を支援します（Envoy設定ダンプ、オフラインモード、トラブルシューティング）
allowed-tools: ["Bash", "Read", "Write", "Glob"]
---

# kubectl + Envoy デバッグ

このskillは、kubectl + Envoyベースのツールのデバッグと設定確認を支援します。

## 対象ツール

- kubectl port-forward + Envoyを使うローカルプロキシツール
- Envoy設定を動的生成するツール

## 提供機能

### Envoy設定のダンプ

生成されたEnvoy設定をYAML形式で確認:

```bash
kubectl localmesh --dump-envoy-config -f services.yaml

# ファイルに保存
kubectl localmesh --dump-envoy-config -f services.yaml > envoy-config.yaml

# または直接実行
./kubectl-localmesh --dump-envoy-config -f services.yaml > envoy-config.yaml
```

**用途**:
- Envoy設定の理解
- ルーティング問題のデバッグ
- Envoy設定パターンの学習

### オフラインモード（モック設定）

Kubernetesクラスタに接続せずにEnvoy設定を確認:

```bash
# モック設定ファイル作成例
cat > mocks.yaml <<EOF
mocks:
  - namespace: users
    service: users-api
    port_name: grpc
    resolved_port: 50051
  - namespace: billing
    service: billing-api
    port_name: http
    resolved_port: 8080
EOF

# モック設定を使ってダンプ
kubectl localmesh --dump-envoy-config -f services.yaml --mock-config mocks.yaml
# または
./kubectl-localmesh --dump-envoy-config -f services.yaml --mock-config mocks.yaml
```

**モック設定形式**:
- `namespace`, `service`, `port_name`: サービス識別子
- `resolved_port`: kubectl呼び出しの代わりに使うポート番号

**用途**:
- クラスタアクセス不要の設定テスト
- CI/CDパイプライン
- オフライン開発

### ログレベル指定

詳細なデバッグログを出力:

```bash
sudo kubectl localmesh -f services.yaml -log debug
# または
sudo ./kubectl-localmesh -f services.yaml -log debug
```

**ログレベル**:
- `debug`: 最も詳細（デバッグ情報、内部状態）
- `info`: 標準（起動、設定読み込み、主要イベント）
- `warn`: 警告のみ

### Envoy設定の検証ポイント

生成されたEnvoy設定をレビューする際のチェックリスト:

1. **Listenerの確認**
   - `listener_port`が正しいか
   - `0.0.0.0`でリッスンしているか

2. **Virtual Hostsの確認**
   - 各サービスの`host`（例: `users-api.localhost`）が定義されているか
   - ルーティングルールが正しいか

3. **Clustersの確認**
   - 各サービスに対応するclusterが存在するか
   - `127.0.0.1:<動的ポート>`への接続設定が正しいか
   - HTTP/2設定（`http2_protocol_options`）がgRPCサービスで有効か

4. **Timeoutの確認**
   - `timeout: 0s`でストリーミング対応になっているか

## 使用方法

ユーザーから以下のような依頼があった場合:

1. **「Envoy設定を確認したい」**
   - `--dump-envoy-config`を使用
   - 出力をファイルに保存して詳細レビュー

2. **「クラスタに接続できない」**
   - `--mock-config`でオフラインモード
   - モック設定ファイルを作成

3. **「動作がおかしい」「ルーティングされない」**
   - `-log debug`で詳細ログ取得
   - Envoy設定をダンプして検証
   - virtual_hostsとclustersの対応を確認

## トラブルシューティング

### Envoy起動失敗

```bash
# 1. 設定をダンプして確認
./kubectl-localmesh --dump-envoy-config -f services.yaml > /tmp/envoy-config.yaml

# 2. Envoy設定を直接検証
envoy --mode validate -c /tmp/envoy-config.yaml
```

### ルーティングが機能しない

```bash
# 1. デバッグログで詳細を確認
sudo ./kubectl-localmesh -f services.yaml -log debug

# 2. 別ターミナルでcurlテスト
curl -v http://users-api.localhost/

# 3. Envoy管理インターフェースで状態確認（実装されている場合）
# curl http://localhost:9901/stats
```

### モック設定の作成

実際のクラスタから情報を取得してモック設定を作成:

```bash
# サービスのポート情報を取得
kubectl get svc -n users users-api -o jsonpath='{.spec.ports[?(@.name=="grpc")].targetPort}'

# 結果をmocks.yamlに記載
cat > mocks.yaml <<EOF
mocks:
  - namespace: users
    service: users-api
    port_name: grpc
    resolved_port: 50051  # 上記で取得した値
EOF
```

## 関連ドキュメント

- プロジェクトのCLAUDE.md: Envoy設定生成ロジックの詳細
- Envoy公式ドキュメント: https://www.envoyproxy.io/docs/envoy/latest/
