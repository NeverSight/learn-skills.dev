---
name: go-taskfile-workflow
description: Taskfileを使ったGoプロジェクトの標準開発ワークフロー（ビルド、テスト、Lint、フォーマット）を提供します
allowed-tools: ["Bash", "Read", "Glob", "Grep"]
---

# Go Taskfile Workflow

このskillは、Taskfile.yamlを使ったGoプロジェクトの標準開発ワークフローを提供します。

## 対象プロジェクト

- Go言語プロジェクト
- Taskfile.yamlでビルド・テスト・Lintを管理
- Nix devShell（`flake.nix`）で開発ツールを管理

## 提供機能

### ビルド

プロジェクトをビルドします。

```bash
task build
```

出力先: `bin/`ディレクトリ（Taskfile定義に依存）

**代替方法**: 直接Go CLIを使用
```bash
go build -o <output> .
```

### テスト

全パッケージのテストを実行します。

```bash
task test
```

**代替方法**: 直接Go CLIを使用
```bash
go test ./...
```

### コード品質管理

**Lint（静的解析）**:
```bash
task lint
```

通常、以下のツールを実行:
- yamllint: YAML設定ファイル検証
- golangci-lint: Go静的解析

**Format（コードフォーマット）**:
```bash
task format
```

gofmtを使用してGoコードを自動フォーマットします。

### 開発ツールの読み込み

`flake.nix`のdevShellを、nix-direnv（`.envrc`の`use flake`）で読み込みます。

```bash
direnv allow
```

### タスク一覧

```bash
task --list
```

## 使用方法

ユーザーから「ビルドして」「テストを実行」などの依頼があった場合:

1. `task build` または `task test` を実行
2. エラーがあれば内容を報告
3. 必要に応じてコードを修正

## ワークフロー例

### 新機能開発時の標準フロー

1. コードを編集
2. `task format` - コードフォーマット
3. `task lint` - 静的解析チェック
4. `task test` - テスト実行
5. `task build` - ビルド確認

### エラー修正時のフロー

1. `task test` でテスト実行し、失敗箇所を特定
2. コードを修正
3. `task test` で再テスト
4. `task lint` で静的解析チェック

## トラブルシューティング

### Task not found

```bash
# devShellが読み込まれていない場合
direnv allow

# またはTaskfileが存在しない場合
ls Taskfile.yaml
```

### ビルドエラー

```bash
# 依存関係の更新
go mod tidy
go mod download

# ビルドを再試行
task build
```

### Lintエラー

```bash
# 自動修正可能なものを修正
task format

# 再度Lint実行
task lint
```

## 関連ドキュメント

- プロジェクトのTaskfile.yaml: タスク定義の詳細
- プロジェクトのCLAUDE.md: アーキテクチャと実装詳細
