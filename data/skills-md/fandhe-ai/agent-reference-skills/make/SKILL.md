---
name: make
description: >
  GNU Make / Makefile リファレンス。
  ターゲット、prerequisite、order-only、変数展開、自動変数、pattern rule、.PHONY、-j 並列・再帰 make、増分ビルド。
  Rust / Cargo / xtask、Node.js / pnpm / Turborepo、Git hooks / CI との責務分離と開発コマンド共通化。
  Makefile 設計・レビュー、Bash サンプル、診断スクリプト。
user-invocable: false
---

# GNU Make / Makefile リファレンス

GNU Make / Makefile の仕様、設計、実装、運用、検証を扱う参照 Skill。
出典基準は GNU Make Manual 4.4.1（Edition 0.77, 2023-02-26）。ローカル検証は GNU Make 3.81（macOS）で行っており、
3.82+ / 4.x 専用機能（`.RECIPEPREFIX`、`.ONESHELL`、`.WAIT` 等）は該当ページ・サンプルに最低バージョンを明記する。
Make 自動化 SaaS・CMake・cargo-make とは別の対象であることに注意する。

## ディレクトリ構成

```text
skills/make/
  SKILL.md
  references/
    architecture/
      README.md
      responsibility-boundaries.md
      command-contracts.md
      selection-and-migration.md
    fundamentals/
      README.md
      rules-and-prerequisites.md
      variables-and-expansion.md
      patterns-includes-and-functions.md
      recipes-and-shell.md
    execution/
      README.md
      special-targets-and-defaults.md
      parallel-and-recursive-make.md
      diagnostics-and-exit-codes.md
      gnu-posix-bsd-compatibility.md
    rust/
      README.md
      crate-and-workspace-profiles.md
      xtask-and-validation.md
    node/
      README.md
      package-scripts-and-mixed-repos.md
    quality/
      README.md
      ci-hooks-and-cache.md
    operations/
      README.md
      safety-and-portability.md
      parallelism-and-recovery.md
    maintenance/
      README.md
      sources-and-compatibility.md
      troubleshooting.md
  samples/
    README.md
    incremental-build.md
    rust-crate.md
    rust-workspace-xtask.md
    node-pnpm.md
    mixed.md
    ci.md
    plans.md
    projects/                        # 動く例の正本
      incremental-build/             # Make がファイル依存関係を直接管理する例
      rust-crate/                    # 薄い Makefile + Bash help/doctor/check/verify（Node 不要）
      rust-workspace-xtask/          # Makefile なし。cargo xtask が正本
      node-pnpm/                     # pnpm workspace + Turborepo 委譲
      mixed/                         # Rust + Node の受け渡しのみ Make が仲介
    ci/                              # 非アクティブな CI テンプレート（.example）
    plans/                           # 承認前の適用計画サンプル（JSON）
  scripts/
    README.md
    make-commands.md
    inspect.md
    plan-and-preview.md
    verify.md
    bin/                             # Claude が明示的に実行する補助 CLI（Node.js 標準ライブラリのみ）
      inspect-repo.mjs
      validate-plan.mjs
      preview-sample.mjs
      verify-layout.mjs
      run-checks.mjs
      lib/
  tests/
    README.md
    helpers.mjs
    fixtures/
    eval-cases.json
    *.test.mjs
```

## 公式仕様と独自設計の区別

`references/` の各ページは次の3種類を明示的に分けて記述する。

- **Source-backed behavior** — GNU Make Manual 4.4.1 等、一次情報に基づく仕様。出典 URL・対象版・確認日付き（一覧は [references/maintenance/sources-and-compatibility.md](references/maintenance/sources-and-compatibility.md)）
- **Design guidance** — この Skill が提案する構成・判断基準。採用条件・根拠・トレードオフ付き
- **Example contract** — `samples/` 内だけで定義したコマンド名・JSON 形式・終了コード・ディレクトリ構成

`help` / `doctor` / `setup` / `check` / `fix` / `verify` / `clean` という公開コマンドの共通化、および「入口は複数でも実処理の定義は一つ」という設計は、この Skill 独自の Design guidance であり、GNU Make・Cargo・Anthropic の公式仕様が要求するものではない。

## 探索手順

1. 参照だけでよい場合（consult、既定の使い方）は、下記マッピング表でタスクに対応するカテゴリを探し、そのカテゴリの `README.md` で目的のページを特定して Read する。外部プログラムは実行しない
2. 既存構成の診断・計画・検証が必要な場合は「利用パターン」の表で consult 以外のどの段階かを確認し、対応する `scripts/*.md` の手順に従う
3. 安全上の制約は必ず [references/operations/safety-and-portability.md](references/operations/safety-and-portability.md) で確認する

## タスク → カテゴリ マッピング

| タスク | カテゴリ | 参照 README |
|--------|---------|------------|
| Make と Cargo/xtask/Turborepo/CI の責務分離、コマンド契約、Make 採用可否・移行の判断基準を知りたい | architecture | [references/architecture/README.md](references/architecture/README.md) |
| target / prerequisite / recipe、order-only prerequisite、変数展開（`=` `:=` `?=` `+=`）、自動変数、Make と shell の `$` の区別を調べる | fundamentals | [references/fundamentals/README.md](references/fundamentals/README.md) |
| pattern rule、include、条件分岐、レシピと shell（tab / `.RECIPEPREFIX` / `.ONESHELL`）を調べる | fundamentals | [references/fundamentals/README.md](references/fundamentals/README.md) |
| `.PHONY`・`.DEFAULT_GOAL` 等の特殊ターゲット、`-j` 並列・再帰 make、`-n`/`-q` 診断、GNU/POSIX/BSD 互換性を調べる | execution | [references/execution/README.md](references/execution/README.md) |
| 単一 crate / workspace / virtual workspace の profile、fmt/clippy/test/doc の使い分け、cargo xtask の採否を調べる | rust | [references/rust/README.md](references/rust/README.md) |
| pnpm workspace、package.json scripts、Turborepo への委譲、Rust+Node 混在の責務境界を調べる | node | [references/node/README.md](references/node/README.md) |
| Git hooks と CI の共通コマンド契約、パイプライン定義とマージ保護の違い、キャッシュ・外部状態の境界を調べる | quality | [references/quality/README.md](references/quality/README.md) |
| consult/audit/plan/apply/verify の安全境界、再実行可能な setup、並列 worktree 分離、clean の対象範囲を調べる | operations | [references/operations/README.md](references/operations/README.md) |
| 出典台帳、GNU Make のよくある失敗パターンと診断手順を調べる | maintenance | [references/maintenance/README.md](references/maintenance/README.md) |
| 動くサンプル（増分ビルド、Rust crate/workspace、Node、混在、CI テンプレート、適用計画）を見たい | samples | [samples/README.md](samples/README.md) |
| Claude が使う調査・計画検証・プレビュー・検証スクリプトの実行方法を知りたい | scripts | [scripts/README.md](scripts/README.md) |
| 補助スクリプトの回帰テスト・終了コード契約・eval-cases を知りたい | tests | [tests/README.md](tests/README.md) |

## 利用パターン

参照しただけでは対象ファイルを変更せず、外部プログラムも自動実行しない。Skill を読み込んだこと自体は適用の承認ではない。

| パターン | 内容 | 使う script |
|---|---|---|
| consult | 設計・レビュー中の参照（既定） | なし。references / samples / scripts の文書のみ読む |
| audit | 利用者が指定した対象の静的診断。書き換え・依存導入・build は行わない | `inspect-repo.mjs`（`--root` 必須） |
| plan | 適用案・変更対象・検証計画の提示。対象ファイルは変更しない | `validate-plan.mjs`、`preview-sample.mjs`（既定は書き込まない） |
| apply | 利用者が別途承認した範囲だけの適用。既存ファイルの編集は Skill 独自のパッチ適用エンジンではなく通常の編集ツールで行う | サンプル導入のみ `preview-sample.mjs --apply --plan <計画> --approve <planDigest>`（承認した計画ファイルと一致する場合だけ、明記したファイルを書き込む） |
| verify | 承認済みの検証。静的整合性確認と実コマンド実行を分離する | `verify-layout.mjs`、`run-checks.mjs`（既定 dry-run。`--execute` は利用者が確認した計画の `--approve <planDigest>` と各 check の `approved:true` が揃う場合のみ） |

## 安全上の最小ルール

- 不審なリポジトリで `make -n` / `make -q` を安全な静的解析の代わりに使わない（設定読込時のコード実行がありうる）
- `.env` 等の秘密情報の値を表示・ログ出力・JSON へ混入させない
- ツールの自動導入、sudo、hooks / CI の回避を行わない
- 環境不足・未実行・非該当（`BLOCKED` / `SKIPPED` / `NOT_APPLICABLE`）を `PASS` に丸めない

詳細は [references/operations/safety-and-portability.md](references/operations/safety-and-portability.md) を参照。

## 補助スクリプトのパス

`scripts/bin/*.mjs` は Skill 設置位置からの相対パスで解決する。導入形態（upstream `skills/make/`、`.agents/skills/make/`、`.claude/skills/make/` の実体・symlink、グローバル導入）によって Skill 自身の絶対パスは変わるため、実行時は `<skill-dir>` をその時点の実際の Skill 設置先に置き換える。

```bash
node <skill-dir>/scripts/bin/inspect-repo.mjs --root /path/to/target-repo --json
```

対象 root は必ず `--root` で明示する。`${CLAUDE_SKILL_DIR}` のような置換は使わない（外部 shell に常に存在する環境変数ではない）。補助 CLI は Node.js 標準ライブラリのみで動作するが、これは Skill 側の依存であり、利用者プロジェクトに採用するサンプル（`rust-crate` 等）自体が Node.js を必要とするわけではない。

## 利用例

- 「make を参考に、この Rust crate の Makefile と検証コマンドの改善計画を作って」
- 「このリポジトリの Makefile を GNU Make の仕様に照らしてレビューして、`.PHONY` の抜けがないか教えて」
- 「Rust + Node の混在リポジトリで、Make・Cargo・Turborepo・CI の責務分離が適切か静的に診断して」

## 関連スキルとの使い分け

- **rust** — Cargo・rustc・rustdoc 等 Rust 言語・ツールチェーン全体の API リファレンスを担当。`make` の `references/rust/` は Cargo 標準機能と xtask パターンの Make 文脈での使い分けのみを扱い、Rust 言語仕様は複製しない
- **turborepo** — Turborepo 自体のタスクグラフ・キャッシュ・パイプライン定義を担当。`make` の `references/node/` は Turborepo への委譲境界のみを扱う
- **lefthook** — Git hooks の設定・実装を担当。`make` の `references/quality/` は hooks と CI が同じコマンド契約を共有する設計指針のみを扱う

いずれもスキル名による探索を前提とし、単独インストール時に壊れる兄弟ディレクトリへの相対リンクは使わない。
