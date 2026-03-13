---
name: kirikae
description: >
  KIRIKAE ローカル開発プロキシの環境管理スキル。
  curl経由でAdmin API (localhost:4000) を操作し、環境の一覧表示・追加・切り替え・リネーム・更新・削除を行う。
  使用タイミング: (1) 開発環境のプロキシ先を切り替えたい (2) 新しいポートを登録したい
  (3) 環境のラベル名を変更したい (4) 登録済み環境を確認したい (5) 環境を削除したい
  トリガーキーワード: kirikae、切替、プロキシ切替、環境切替、ポート登録、ポート切替
---

# KIRIKAE Environment Manager

Admin API (default: `http://localhost:${PROXY_ADMIN_PORT:-4000}`) を操作するスキル。

## スクリプト

`scripts/kirikae.sh` を使用する。環境変数 `PROXY_ADMIN_PORT` でポートを変更可能（デフォルト: 4000）。

## コマンド一覧

### 状態確認

```bash
# 現在のアクティブ環境を表示
bash scripts/kirikae.sh status

# 登録済み環境の一覧
bash scripts/kirikae.sh list
```

### 環境の追加

```bash
# 新しい環境を登録（label と url を指定）
bash scripts/kirikae.sh add "feature/login" "http://localhost:3001"
```

### 環境の切り替え

```bash
# ID で切り替え（list で取得した id を使用）
bash scripts/kirikae.sh switch <environment-id>

# URL 直指定で切り替え（未登録の URL も可）
bash scripts/kirikae.sh switch-url "http://localhost:3001"
```

### 環境のリネーム

```bash
# ラベル名だけ変更（URL は維持）
bash scripts/kirikae.sh rename <environment-id> "new-label"
```

### 環境の更新

```bash
# ラベルと URL を両方変更
bash scripts/kirikae.sh update <environment-id> "new-label" "http://localhost:3002"
```

### 環境の削除

```bash
bash scripts/kirikae.sh delete <environment-id>
```

## ワークフロー

1. `list` で現在の環境一覧と ID を確認
2. 必要に応じて `add` で新規登録、`rename`/`update` で編集
3. `switch` で対象環境をアクティブに設定
4. `status` で切り替え結果を確認

## 注意事項

- KIRIKAE サーバーが起動中でないとコマンドは失敗する
- スクリプトのパスはスキルディレクトリからの相対パス。Bash で実行する際はフルパスを使用すること
