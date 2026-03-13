---
name: cleanup-package-json
description: >
  package.json のスクリプトと依存関係を整理・クリーンアップする。
  「package.jsonをきれいにしたい」「スクリプトを整理したい」「未使用の依存を削除したい」
  などのリクエストに使用する。具体的には以下を対象とする：
  (1) 冗長なスクリプト（エイリアス・パススルー）の削除や統合、
  (2) 暗黙的なライフサイクルフック（pre/post）の明示化、
  (3) スクリプト命名規則の統一、
  (4) 未使用依存パッケージの検出と削除、
  (5) スクリプト名変更に伴うドキュメント・CI 更新、
  (6) 依存削除後のロックファイル再生成。
---

# cleanup-package-json

## ワークフロー

### 1. 現状把握

`package.json` を読んで、以下の観点で問題点を洗い出す。

**スクリプトのチェックポイント:**
- **エイリアス**: 別のスクリプトを呼ぶだけのスクリプト（例: `"build": "npm run build:app"`）
- **パススルー**: コマンドをそのまま渡すだけのスクリプト（例: `"lint": "eslint"`）
- **暗黙のライフサイクルフック**: `preX` / `postX` フック（例: `"prebuild": "npm run codegen"`）
- **命名の不統一**: 関連スクリプトがグループ化されていない（例: `e2e` が `test:*` 系に混ざっていない）

**依存関係のチェックポイント:**
- `dependencies` / `devDependencies` の各パッケージをソースコード内の import 文で検索し、未使用を特定する
- 検索対象ディレクトリはプロジェクト構造に応じて判断する（`src/`、`lib/`、`app/` など）

### 2. 問題点の提示と確認

発見した問題点をユーザーに提示し、どれを修正するか確認する。選択肢を提示して合意を得てから作業に入る。

### 3. スクリプトの修正

確認が取れたら `package.json` を編集する。

**典型的な変換パターン:**

| パターン | 変換前 | 変換後 |
|---|---|---|
| エイリアス統合 | `"build": "npm run build:app"` + `"build:app": "A && B"` | `"build": "A && B"` |
| pre フック明示化 | `"prebuild": "npm run X"` + `"build": "Y"` | `"build": "npm run X && Y"` |
| パススルー削除 | `"lint": "eslint"` | 削除（直接 `eslint` を呼ぶか不要なら除去） |
| 命名統一 | `"e2e": "playwright test"` | `"test:e2e": "playwright test"` |

パッケージマネージャーは `npm run` / `yarn` / `pnpm run` のいずれが使われているかを `package.json` や lockfile の存在から判断して使い分ける。

### 4. ドキュメントの更新確認

スクリプト名を変更・削除した場合は、以下のファイルにその名前が登場していないか確認し、必要であれば修正する。

- `README.md`
- `CLAUDE.md` / `AGENTS.md` などのエージェント向けドキュメント
- `.github/workflows/` 配下のワークフローファイル
- `docs/` 配下のドキュメント

### 5. 依存削除後のロックファイル再生成

依存パッケージを削除した場合は、`node_modules` とロックファイルを削除してから install を実行する。

```bash
# npm
rm -rf node_modules package-lock.json && npm install

# yarn
rm -rf node_modules yarn.lock && yarn install

# pnpm
rm -rf node_modules pnpm-lock.yaml && pnpm install
```

## 注意事項

- **pre フックの削除**: `preX` フックを削除して明示的に呼び出す形にすると、そのスクリプトを単独で呼んだときも（意図しない）フックが走らなくなる。動作変更を伴うため、ユーザーに確認してから変換する。
- **スクリプト名の変更**: CI やドキュメントで参照されているスクリプト名を変更する場合は、必ず参照先も合わせて更新する。
- **ネイティブ連携パッケージ**: Tauri / Electron など、ネイティブ層との橋渡しをする npm パッケージは JS 側の import がなくても実際には必要なことがある。ランタイム要件を確認してから削除する。
- **間接依存**: `dependencies` に書かれていても直接 import していない場合がある（例: Babel プラグイン、ESLint プリセットなど設定ファイル経由で参照されるもの）。削除前にビルド・テストで確認する。
