---
name: fandhe-db
description: >
  Rust 製ローカルファースト vector 特化クエリ DB fandhe-db
  (PostgreSQL wire protocol v3 互換) の
  fandhe-vector-db-engine / fandhe-vector-db-wire-server リファレンス。
  USING PLAN / USING OPERATION_ID 構文、precision・recall モード、
  HNSW / BM25 転置索引 / RRF hybrid / rerank、redb 永続化、
  tenant・RLS、SIMD / wgpu カーネル、wire_code エラー契約。
user-invocable: false
---

# fandhe-db

fandhe-db は Rust 製のローカルファースト vector 特化クエリ DB。`fandhe-vector-db-engine`（コアエンジン、SQL 表層・HNSW/BM25/hybrid 検索・redb 永続化・RLS）と `fandhe-vector-db-wire-server`（PostgreSQL wire protocol v3 互換のバイナリ）の 2 crate workspace で構成され、無改造の `psql` / `psycopg` / `pg` クライアントから接続し、`USING PLAN` / `USING OPERATION_ID` 拡張構文を含む SQL を実行できる。対象バージョンは両 crate とも crates.io **0.1.0**（tag / release なし、pin commit SHA `7022d112e79760dca916480599553fcac256b5fb`）。0.1.0 の crate 名は `fandhe-vector-db-engine` / `fandhe-vector-db-wire-server` であり、本スキルのコマンド（`cargo run -p` 等）・公開名・各ページ frontmatter の docs.rs `source:` はこの名前で記載する（`fandhe-db-engine` / `fandhe-db-wire-server` への改名は 0.2.0 から）。

公式ドキュメントサイトは存在せず、出典は公開リポジトリ https://github.com/Fandhe-AI/fandhe-db の README・`docs/design/` ADR・crate ソース（docs.rs source view。レンダリング済み rustdoc ページは 404 のため source view のみ）。

**仕様の位置づけ** — 仕様の source of truth は private リポジトリ `Fandhe-AI/fandhe-db-spec`（非公開）にあり、本スキルはそこへアクセスできないため、公開ソース・公開 ADR から追跡できる範囲に限定している。crate ソースの doc comment（rustdoc）は日本語で書かれており、references 本文はそれを日本語で要約し、シグネチャ（型・識別子）部分は英語 verbatim で転記している。private spec 参照 ID のみが残る挙動は各ページ `## Notes` に「spec 非公開のため未記載」と明記している。

**他スキルとの使い分け** — `upstash` は @upstash/vector のマネージド SaaS クライアント、`supabase` は pgvector 拡張・Postgres RLS のクライアント利用であり、いずれもベクター DB エンジン本体ではない。`mssql` / `drizzle` は SQL クライアント / ORM であり、本スキルの SQL 表層（`USING PLAN` 等の拡張構文限定）とは別物。本スキルの `performance/` は CPU SIMD（isa / dispatch）と wgpu 経由の GPU バッチカーネルを扱い、`nvidia-cuda` / `apple-silicon` / `amd-rocm` が担う GPU 言語・ランタイム層（CUDA / MSL / HIP）のリファレンスではない。`fandhe-ai` / `fandhe-backend` / `fandhe-frontend` は同じ fandhe org の別ライブラリで API は無関係、ベクター DB エンジン本体を調べる場合は本スキル（`fandhe-db`）を参照すること。

## ディレクトリ構成

```text
skills/fandhe-db/
  SKILL.md
  references/
    getting-started/
      README.md
      overview.md
      crate-layout.md
      lib.md
      core.md
      error-format.md
      development-setup.md
    sql/
      README.md
      sql-module.md
      lexer.md
      parser.md
      allowlist.md
      using-plan.md
      using-operation-id.md
      mode.md
      explain.md
      plan.md
      scan.md
    sql-execution/
      README.md
      exec.md
      aggregate.md
      group-by.md
      expr-program.md
      scalar-index.md
      scalar-plan.md
      udf-call.md
      arena-cache.md
      hnsw-cache.md
      hnsw-hybrid.md
      sparse-cache.md
      visible-cache.md
    search/
      README.md
      search-engine.md
      hnsw.md
      sparse.md
      hybrid.md
      rerank.md
      scoring-boost.md
      precision.md
      query-planner.md
      tiering.md
    storage/
      README.md
      storage.md
      row-codec.md
      catalog.md
      txn.md
      recovery.md
      incremental.md
      arena.md
      buffer-pool.md
    security/
      README.md
      policy.md
      rls.md
      tenant.md
    wire-server/
      README.md
      main-cli.md
      server.md
      handshake.md
      auth.md
      bind-guard.md
      framing.md
      protocol-dispatch.md
      simple-query.md
      result-encoder.md
      response-buffer.md
      error-response.md
      limits.md
      search-engine-opt.md
      lib.md
    performance/
      README.md
      kernel.md
      isa.md
      dispatch.md
      gpu-batch.md
      batch-search.md
      batch-fallback.md
      batch-limits.md
      parallel-search.md
      f16.md
      sq8.md
    extensions/
      README.md
      wasm-udf.md
      declarative-filter.md
      embedding.md
      chunking.md
      dictionary.md
  samples/
    README.md
    start-wire-server.md
    connect-psql.md
    connect-psycopg.md
    connect-node-pg.md
    e2e-three-client.md
    docker-compose.md
  scripts/
    README.md
    install.md
    make-targets.md
    run-wire-server.md
```

## 探索手順

タスクからカテゴリを引き、カテゴリの README.md で目的のページを特定する:

1. 下記マッピング表でタスクに対応するカテゴリを探す
2. そのカテゴリの `references/{category}/README.md` を参照して目的のページを特定する
3. 該当ページの `.md` を Read して詳細を確認する

## タスク → カテゴリ マッピング

| タスク | カテゴリ | 参照 README |
| --- | --- | --- |
| リポジトリの位置づけ・crate 構成・features・依存、engine クレートルート・`VectorCore`/`EngineCore` コア API、`ErrorClass`/`WireError` の wire_code 写像、開発環境構築・Makefile を知りたい | getting-started | [references/getting-started/README.md](references/getting-started/README.md) |
| SQL 表層のトークナイザ・意味論束縛・AST 許可リスト、`USING PLAN` / `USING OPERATION_ID` / `HINT ORDER` 拡張構文、`recall`/`precision` モード解決、`EXPLAIN` 応答、wide retrieval scan を知りたい | sql | [references/sql/README.md](references/sql/README.md) |
| SQL 実行計画本体（RLS→SCALAR→DISTANCE 順）、集計・`GROUP BY`、式ステップコンパイル、スカラー二次索引、宣言的 UDF 呼び出し、SQL 表層専用の各種世代整合キャッシュを知りたい | sql-execution | [references/sql-execution/README.md](references/sql-execution/README.md) |
| 検索エンジン選択・構築、HNSW 近似最近傍探索、BM25 転置索引、RRF hybrid 融合、リランキング、宣言的スコアリングブースト、precision 確信度ゲート、LLM クエリプランニング・ティアリングを知りたい | search | [references/search/README.md](references/search/README.md) |
| redb ベース永続化層、行エンコーダー、スキーマカタログ、トランザクションハンドル、障害回復・commit_boundary・ledger、増分インデックス反映、ベクトルアリーナ、バッファプールを知りたい | storage | [references/storage/README.md](references/storage/README.md) |
| テナント境界・可視性文脈の構築判定、RLS 暗黙適用フックと可視行限定検索、行ストア統合層の参照実装を知りたい | security | [references/security/README.md](references/security/README.md) |
| wire-server バイナリの CLI フラグ・起動、接続受け付けループ、StartupMessage/認証フロー、Argon2id 照合、メッセージフレーミング・型バイト分類、簡易クエリ実行、応答バイト列生成、ErrorResponse 横断写像、タイムアウト・同時接続数制御を知りたい | wire-server | [references/wire-server/README.md](references/wire-server/README.md) |
| 検索カーネル境界・CPU 参照実装、SIMD 実行時検出・ディスパッチ決定表、wgpu GPU バッチ検索、CPU-SIMD への縮退フォールバック、一括投入上限、並列 Top-k、f16/i8(SQ8) 量子化を知りたい | performance | [references/performance/README.md](references/performance/README.md) |
| WASM UDF サンドボックス実行契約、宣言的メタデータフィルタ、埋め込み変換注入点、チャンク分割、シンボル・タームインデックス抽出を知りたい | extensions | [references/extensions/README.md](references/extensions/README.md) |
| wire-server の起動方法、無改造 psql/psycopg/pg クライアントからの接続例、3 クライアント e2e ハーネス、Docker 開発環境など典型的な使い方を知りたい | samples | [samples/README.md](samples/README.md) |
| 開発環境構築・Makefile タスク・wire-server 起動コマンドなどインストール・CLI コマンドを知りたい | scripts | [scripts/README.md](scripts/README.md) |
