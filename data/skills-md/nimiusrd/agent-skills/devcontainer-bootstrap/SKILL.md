---
name: devcontainer-bootstrap
description: "Dev Container を最短で導入/更新するためのブートストラップ。stack を自動判定（node/python/rust）し、テンプレート適用または安全更新を行う。既存 .devcontainer がある場合はバックアップ後にマージ。Chat オプション: stack (auto|node|python|rust), packageManager (npm|pnpm|yarn), mode (safe|overwrite), includeTools (true|false), addCI (true|false)。"
---

# devcontainer-bootstrap

## 使いどころ
- 任意リポジトリに Dev Container を素早く導入したいとき
- 既存 `.devcontainer/` を壊さず拡張したいとき（バックアップ必須）
- Node/Python/Rust の代表的セットアップをテンプレで貼りたいとき

## ワークフロー（(1) scan → (2) detect → (3) apply/update → (4) explain）
1) **scan**: リポジトリルートを確認し、スタック候補ファイルをチェック  
2) **detect**: `scripts/detect_stack.sh` で `node|python|rust|unknown` を判定（複数命中や go.mod のみは unknown → stack を明示指定）  
3) **apply/update**: `scripts/apply_devcontainer.sh` を実行し `.devcontainer/` を生成/更新  
4) **explain**: 実行ログを読み、何がバックアップ/更新されたかをユーザーに伝える。競合や手動フォローが必要なら明示

## 実行オプション（チャットで指定可能）
- `stack`: `auto|node|python|rust`（default auto, 複数命中や go.mod のみは unknown → stack 指定を促す）
- `packageManager`: `npm|pnpm|yarn`（node のみ、postCreate で install 実行）
- `mode`: `safe|overwrite`  
  - safe: 既存 `devcontainer.json` をマージ（extensions/settings/features/postCreateCommand）。`jq` 無しでも最小追記（postCreate 実行を確実に追加）。既存 Dockerfile は保持。  
  - overwrite: stack テンプレートで `devcontainer.json` と `Dockerfile` を置換。
- `includeTools`: `true|false`（default false）  
  - true の場合、追加 feature として git / github-cli を組み込む（上書きではなくマージ）。
- `addCI`: `true|false`（default false）  
  - GitHub Actions 最小 workflow (`.github/workflows/devcontainer-bootstrap.yml`) を生成。safe で既存があればバックアップのみしてスキップ、overwrite なら置換。

## 手順（ローカル実行例）
```bash
# 1. スタック自動判定（複数命中なら unknown）
bash skills/devcontainer-bootstrap/scripts/detect_stack.sh .

# 2. safe モードで適用（自動判定 + 追記中心）
bash skills/devcontainer-bootstrap/scripts/apply_devcontainer.sh --mode safe

# 3. node + pnpm で overwrite し CI も生成
bash skills/devcontainer-bootstrap/scripts/apply_devcontainer.sh --stack node --package-manager pnpm --mode overwrite --include-tools true --add-ci true
```

## 生成/更新内容
- `.devcontainer/`（devcontainer.json, Dockerfile, postCreate.sh）。既存があれば `.devcontainer.bak-<timestamp>/` にバックアップしてから更新。
- VS Code 推奨設定と拡張は `customizations.vscode` に記述（参考: [Dev Container supporting tools](https://containers.dev/supporting#visual-studio-code)）。
- postCreate は stack に応じて依存導入をベストエフォートで実行（失敗は非致命）。
- `addCI=true` の場合、`devcontainers/ci@v0.3.1900000417` を使う最小 workflow を生成。
- Node テンプレートは `mcr.microsoft.com/devcontainers/typescript-node:<メジャー>` を使用（latest は避け、例: `24`）。LTS 更新時はメジャー番号タグを明示的に上げる。
- Node イメージタグの選定はコードベースの情報を参照して行う  
  - 優先順: `.nvmrc` → `.node-version` → `package.json` の `engines.node`  
  - いずれも無い場合はレジストリ (`https://mcr.microsoft.com/v2/devcontainers/typescript-node/tags/list`) から最新メジャーを確認し、latest は避けてメジャー番号タグを使う
- Python テンプレートは `mcr.microsoft.com/devcontainers/python:<バージョン>` を使用（latest は避け、デフォルト例: `3.14`）  
  - 優先順: `.python-version` → `pyproject.toml` の `requires-python` または `tool.poetry.dependencies.python` → `requirements.txt` に併記された Python バージョン記述  
  - いずれも無い場合はレジストリ (`https://mcr.microsoft.com/v2/devcontainers/python/tags/list`) を参照して安定版メジャー/マイナーを選ぶ（latest は避ける）

## 競合・注意
- 複数スタックが同時に検出された場合や go.mod のみの場合は `stack` を明示する。
- safe モードでマージできない部分があればログに警告を出す。壊したくない場合は safe を優先。
- 危険な `git config --global safe.directory '*'` は一切実行しない。
- 詳細な判断基準や safe/overwrite の使い分けは `docs/decision-guide.md` を参照。

## バンドル済みリソース
- `scripts/detect_stack.sh`: スタック判定（node/python/go/unknown）
- `scripts/apply_devcontainer.sh`: テンプレ適用 & 安全更新 & CI 生成
- `templates/`: stack 別 `devcontainer.json` / `Dockerfile`（node/python/rust） + 共通 `postCreate.sh`
- `docs/decision-guide.md`: 判定ルール・バックアップ方針・safe/overwrite の違い・よくある罠
