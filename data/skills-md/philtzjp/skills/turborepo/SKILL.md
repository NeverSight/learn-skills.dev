---
name: turborepo
description: Turborepo と pnpm でモノレポを構成・運用する。apps と packages の分離、workspace:* による内部依存、共有 tsconfig、責務パッケージ、turbo.json のタスク定義とキャッシュ、pnpm コマンドによる package.json 生成、Cargo や Go など非 JavaScript プロジェクトの取り込み。パッケージの追加、turbo.json や pnpm-workspace.yaml や tsconfig の編集、apps や packages の構成変更を行うときに使う。
---

# turborepo

## 方針

Turborepo と pnpm ワークスペースの組み合わせに従う。パッケージマネージャーは pnpm に統一し、ロックファイルは pnpm-lock.yaml だけをコミットする。

Turborepo は更新が速く、turbo.json のキー名も変わってきている。設定の形に迷ったら記憶に頼らず下を引く。

- ドキュメント https://turborepo.dev/docs
- turbo.json のリファレンス https://turborepo.dev/docs/reference/configuration
- タスクの構成 https://turborepo.dev/docs/crafting-your-repository/configuring-tasks
- キャッシュ https://turborepo.dev/docs/crafting-your-repository/caching
- 複数言語の扱い https://turborepo.dev/docs/guides/multi-language
- 更新情報 https://turborepo.dev/blog
- リリースと破壊的変更 https://github.com/vercel/turborepo/releases

turbo.json のタスク定義キーは v2 以降 tasks。pipeline は旧名。古い記事を写さない。

Turborepo をグローバルにインストールしない。`pnpm exec turbo` を使うか、ルートの devDependency として入れる。

## 構成

```text
my-monorepo/
  pnpm-workspace.yaml
  turbo.json
  package.json
  apps/          デプロイ可能なアプリケーション
  packages/      共有ライブラリと設定
```

- ワークスペース構成は pnpm-workspace.yaml で定義する。
- apps と packages の分離を維持する。デプロイ可能なアプリを packages に置かない。共有ライブラリを apps に置かない。
- ネストしたパッケージを作らない。

## パッケージ

- 名前は `@<org>/` プレフィックスを持つスコープ付きにする。
- 内部パッケージにはすべて `"private": true` を設定する。
- 各 package.json に exports を定義する。main より exports を優先する。
- 共有 TypeScript 設定を packages/tsconfig/ に置き、各パッケージがそれを継承する。
- 内部依存は `workspace:*` プロトコルで参照する。

## 責務パッケージ

次を packages 配下に必ず置く。

- log ログ集約
- error エラー集約
- prompt AI プロンプト集約
- env 環境変数集約
- db データベース集約

利用側は `@<org>/log` などを `workspace:*` で依存に追加する。該当する責務を呼び出し側で再実装しない。

## package.json の生成と更新

package.json をゼロから手書きしない。ルート、apps/*、packages/* のいずれでも同じ。

```sh
pnpm init                     # package.json を生成する
pnpm create <template>        # フレームワークの scaffolder を使う
```

依存関係の追加、更新、削除はコマンドで行う。

```sh
pnpm add -D -w turbo typescript                            # ルートの devDependency
pnpm add --filter @<org>/dashboard zod                     # 特定パッケージの外部依存
pnpm add --filter @<org>/dashboard --workspace @<org>/log  # 内部依存を workspace:* で解決
pnpm update --filter @<org>/dashboard
pnpm remove --filter @<org>/dashboard zod
```

- ルート以外を対象にするときは `--filter` でパッケージを指定する。
- ワークスペース内部依存には `--workspace` を併用する。
- dependencies、devDependencies、peerDependencies を直接編集しない。
- コマンドで設定できないフィールド（name のスコープ化、private、exports、scripts）だけ、生成済みの package.json に最小限の編集を加える。

## 手順例

```sh
# ルートワークスペース
mkdir my-monorepo && cd my-monorepo
pnpm init
# pnpm-workspace.yaml に apps/* と packages/* を定義する
pnpm add -D -w turbo typescript

# 責務パッケージ
mkdir -p packages/log
(cd packages/log && pnpm init)
# name を @<org>/log にし、private と exports を設定する

# アプリ
pnpm create next-app@latest apps/dashboard
pnpm add --filter @<org>/dashboard --workspace @<org>/log
```

## turbo.json

依存関係を考慮したタスクパイプラインを定義する。

```json
{
  "$schema": "https://turborepo.dev/schema.json",
  "tasks": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**", ".next/**", "!.next/cache/**"]
    },
    "lint": {},
    "test": { "dependsOn": ["^build"] },
    "dev": { "cache": false, "persistent": true }
  }
}
```

- `^build` は依存パッケージのタスクを先に走らせる指定。
- outputs を正確に書く。書き漏らすとキャッシュから復元されない。
- dev のような常駐タスクは `cache: false` と `persistent: true` にする。
- 環境変数がビルド結果に影響するなら env に列挙する。列挙しないと環境が違ってもキャッシュが当たる。

## コンパイル方針

デフォルトは JIT（Just-in-Time）コンパイルパターンを採る。tsc で dist に出すコンパイル済みパターンへの切り替えは、明示的に要求されたときだけ行う。

## 非 JavaScript プロジェクト

Turborepo は JavaScript 専用ではない。Cargo、Go、Python などのプロジェクトも同じタスクグラフに載せられる。

Rust（Cargo）と Python は、独立してキャッシュしたい単位ごとに package.json を置き、その scripts から各言語のツールチェーンを呼ぶ。Turborepo はネイティブの依存グラフを解析せず、パッケージマネージャー上の関係を使う。

```json
{
  "name": "@<org>/engine",
  "private": true,
  "scripts": {
    "build": "cargo build --release",
    "test": "cargo test",
    "lint": "cargo clippy -- -D warnings"
  }
}
```

turbo.json 側で inputs と outputs を書き、キャッシュを効かせる。

```json
{
  "tasks": {
    "build": {
      "inputs": ["src/**", "Cargo.toml", "Cargo.lock"],
      "outputs": ["target/release/**"]
    }
  }
}
```

- inputs を絞らないと、無関係なファイルの変更でキャッシュが外れる。
- outputs に target 全体を指定すると成果物が巨大になる。必要なパスだけ指定する。
- Cargo 自身のインクリメンタルキャッシュと二重になる。どちらで効かせるかを決めてから設定する。

Go は experimental なネイティブ対応がある。turbo.json で futureFlags を有効にし、go.work にモジュールを列挙する。この場合 Go パッケージ側に package.json は不要で、モジュールパスがパッケージの識別子になる。

```json
{
  "futureFlags": { "experimentalGoWorkspaces": true }
}
```

experimental なので挙動が変わり得る。採用前に上のドキュメントで現状を確認する。

## 確定前に確認する

- pnpm 以外のロックファイル（package-lock.json、yarn.lock）が混ざっていないか。
- デプロイ可能なアプリが packages に、共有ライブラリが apps に入っていないか。
- 内部依存が `workspace:*` になっているか。
- 各パッケージが private と exports を持ち、共有 tsconfig を継承しているか。
- 責務パッケージを呼び出し側で再実装していないか。
- turbo.json のキーが tasks になっているか。pipeline のまま残っていないか。
- outputs と inputs と env が正確か。キャッシュが誤って当たる、または常に外れる状態になっていないか。
- 依存の追加を手書きの package.json 編集で済ませていないか。
- turbo をグローバルインストールしていないか。
