---
name: Feature-Based-Layered-Architecture
description: Feature-Based Layered Architecture for Next.js (App Router) with Supabase. Use when creating API routes, services, repositories, or components with TypeScript. Covers Handler/Service/Repository/Adapter layers, Zod validation, and feature module structure.
---

# SasaTech Architecture

## 概要

Feature-Based Layered Architecture for Next.js (App Router) with Supabase のスキル。

Handler / Service / Repository / Adapter の4レイヤー構成と、機能(Features)単位のモジュール分割パターンを定義する。
ガイド（設計思想・実装方法）とルール（制約・判定基準）の2種類のドキュメントで構成する。

### ガイドとルール

| 項目 | ガイド | ルール |
|------|--------|--------|
| **目的** | アーキテクチャの理解を深める | 実装時の制約を定義する |
| **内容** | HOW/WHY — 設計思想、実装方法、コード例 | DO/DON'T — 判定基準、NG/OK例 |
| **形式** | チュートリアル形式 | 構造化されたルール形式 |
| **使用場面** | 学習時、設計判断時 | 実装時、コードレビュー時 |
| **配置** | `guides/` | `rules/` |

## How to Use

このスキルと併せて、以下の外部スキルの導入を推奨する。

```bash
npx skills add https://github.com/supabase/agent-skills --skill supabase-postgres-best-practices
npx skills add https://github.com/vercel-labs/agent-skills --skill vercel-react-best-practices
npx skills add https://github.com/vercel-labs/agent-skills --skill web-design-guidelines
```

| スキル | 用途 |
|--------|------|
| `supabase-postgres-best-practices` | Supabase / PostgreSQL のクエリ最適化、RLS、マイグレーション |
| `vercel-react-best-practices` | React / Next.js のコンポーネント設計、パフォーマンス最適化 |
| `web-design-guidelines` | アクセシビリティ、レスポンシブデザイン、UI/UX |

---

## Default Stack

| カテゴリ | 技術 |
|----------|------|
| Framework | Next.js (App Router) |
| Database / BaaS | Supabase |
| Language | TypeScript |
| Validation | Zod |
| Data Fetching | SWR |
| Logging | pino |
| Formatter | Biome |
| Linter | Biome + ESLint |

## About Feature-Based Layered Architecture

Feature-Based Layered Architecture for Next.js (App Router) with Supabase

### レイヤー構成

```
Handler                 リクエスト/レスポンス、バリデーション、楽観的認証
        ↓
Service                 ビジネスロジック、厳密な認可、複数 Repository 連携
        ↓
Repository              データアクセス
Adapter                 外部 API 連携（Stripe, Resend 等）
```

### ディレクトリ構成

```
src/
├── app/                      # Next.js App Router
│   ├── (auth)/               # 認証が必要なルートグループ
│   ├── (public)/             # 公開ルートグループ
│   └── api/                  # API Routes (薄いエントリーポイント)
│
├── features/                 # 機能単位のモジュール
│   └── [feature]/
│       ├── index.server.ts   # サーバー専用の公開API（Service, Handler）
│       ├── index.client.ts   # クライアント利用可の公開API（Fetcher, 型）
│       └── core/
│           ├── schema.ts     # Zodスキーマ + 型定義
│           ├── handler.ts    # リクエスト / レスポンス処理 (server-only)
│           ├── service.ts    # ビジネスロジック (server-only)
│           ├── repository.ts # データアクセス (server-only)
│           ├── adapter.ts    # 外部API連携 (server-only)
│           ├── fetcher.ts    # API呼び出し
│           └── hooks.ts      # SWR Hook等
│
├── components/               # 共通UIコンポーネント
├── hooks/                    # 共通Hooks
├── lib/                      # ユーティリティ
│   └── adapters/             # 外部サービス連携
└── types/                    # 共通型定義、Supabase生成型
```

---

## Guides

| ガイド | 説明 |
|--------|------|
| [architecture.md](guides/architecture.md) | Feature-based Layer Architecture の全体設計。レイヤー構成、責務分離、ディレクトリ構成 |
| [architecture/handler.md](guides/architecture/handler.md) | Handler層の実装。リクエスト処理、バリデーション、楽観的認証、エラーハンドリング |
| [architecture/service.md](guides/architecture/service.md) | Service層の実装。ビジネスロジック、厳密な認可、Repository/Adapter連携、トランザクション管理 |
| [architecture/repository.md](guides/architecture/repository.md) | Repository層の実装。データアクセスの抽象化、Supabaseクエリのカプセル化 |
| [architecture/adapter.md](guides/architecture/adapter.md) | Adapter層の実装。外部サービス（決済、メール、AI等）との連携をカプセル化 |
| [authentication.md](guides/authentication.md) | 二段階認証・認可戦略。楽観的認証(Handler)と厳密な認可(Service)の実装パターン |
| [testing.md](guides/testing.md) | レイヤーごとのテスト戦略。Unit / Integration テストの範囲とモック方針 |
| [database.md](guides/database.md) | データベース設計。コメント規約、マイグレーション、Supabase との連携 |
| [logging.md](guides/logging.md) | pino を使用した構造化ログの実装。レイヤーごとのログ出力方針 |
| [setup.md](guides/setup.md) | 新規プロジェクトのセットアップ手順。依存パッケージ、基盤ファイルの配置 |
| [fetch-strategy.md](guides/fetch-strategy.md) | データ取得戦略。SSR/CSRの選択基準と実装パターン |
| [error-handling.md](guides/error-handling.md) | AppErrorクラスとwithHTTPErrorによるエラーハンドリング設計 |
| [wrappers.md](guides/wrappers.md) | withHTTPError(Handler)のラッパーユーティリティ |

---

## Rules

### カテゴリ

| カテゴリ | Prefix |
|----------|--------|
| アーキテクチャ | `arch-` |
| データ | `data-` |
| サーバーサイド保護 | `server-` |
| スキーマ・型定義 | `schema-` |
| レスポンス | `response-` |
| テスト | `test-` |
| バリデーション | `validation-` |
| 命名規則 | `naming-` |
| フロントエンド | `frontend-` |

### インパクト

Impact は、違反時にアーキテクチャへ与える影響の深刻度で定義する。

| Impact | 基準 |
|--------|------|
| CRITICAL | アーキテクチャの根幹が壊れる。違反するとこの設計パターン自体が成立しない |
| HIGH | アーキテクチャの整合性や保守性を大きく損なう |
| MEDIUM | コードの品質や一貫性を低下させる |
| LOW | 開発体験やパターンの統一に関する推奨事項 |

---

### アーキテクチャ (`arch-`)

| ルール | Impact | 説明 |
|--------|--------|------|
| [arch-three-layers](rules/arch-three-layers.md) | CRITICAL | Handler → Service → Repository, Adapter の構成を必ず経由 |
| [arch-feature-structure](rules/arch-feature-structure.md) | CRITICAL | 機能単位で `features/` にモジュール化 |
| [arch-external-services](rules/arch-external-services.md) | HIGH | Stripe, Resend 等の外部サービスは Adapter 経由 |
| [arch-logging-strategy](rules/arch-logging-strategy.md) | MEDIUM | pino で構造化ログ、console.log 禁止 |
| [arch-fetch-strategy](rules/arch-fetch-strategy.md) | CRITICAL | SSR/CSR問わず、fetcher経由でAPI Route呼び出し |
| [arch-logging-levels](rules/arch-logging-levels.md) | MEDIUM | ログレベルをレイヤーと状況に応じて使い分け |
| [arch-auth-strategy](rules/arch-auth-strategy.md) | HIGH | Handler層で楽観的認証、Service層で厳密な認可。共有ヘルパー関数禁止 |
| [arch-auth-operations](rules/arch-auth-operations.md) | HIGH | SignOut、SignInWithOTP等の認証操作はService層に実装、Handler層での直接実行禁止 |
| [arch-public-api](rules/arch-public-api.md) | MEDIUM | Feature の公開APIは index.server.ts（Service, Handler）と index.client.ts（Fetcher, 型）で分離管理 |
| [arch-handler-route-separation](rules/arch-handler-route-separation.md) | HIGH | API Routeは薄いエントリーポイントに限定、ロジックはHandler層に分離 |
| [arch-transaction-rpc-required](rules/arch-transaction-rpc-required.md) | HIGH | 複数テーブル更新のトランザクション処理はSupabase RPC関数を使用 |
| [arch-adapter-placement](rules/arch-adapter-placement.md) | MEDIUM | 汎用Adapterは`lib/adapters/`、Feature固有Adapterは`features/*/core/`に配置 |
| [arch-feature-adapter-isolation](rules/arch-feature-adapter-isolation.md) | MEDIUM | Feature内Adapterが他Featureの内部Adapterに依存することを禁止 |

### データ (`data-`)

| ルール | Impact | 説明 |
|--------|--------|------|
| [data-pagination](rules/data-pagination.md) | HIGH | 全件取得禁止、MAX_LIMITでサーバー側上限を強制、ページネーション必須 |
| [data-comment-required](rules/data-comment-required.md) | LOW | テーブル・カラムに日本語コメント必須 |
| [data-rls-required](rules/data-rls-required.md) | CRITICAL | 全テーブルでRLS有効化必須、最低1つのポリシーを定義 |
| [data-migration-cli-required](rules/data-migration-cli-required.md) | MEDIUM | マイグレーションファイルはSupabase CLIで生成、手動作成禁止 |
| [data-update-trigger-required](rules/data-update-trigger-required.md) | MEDIUM | 全テーブルに`updated_at`/`update_user`自動更新トリガーを適用 |
| [data-select-minimal](rules/data-select-minimal.md) | MEDIUM | `select('*')`を避け、必要なカラムのみを指定 |

### サーバーサイド保護 (`server-`)

| ルール | Impact | 説明 |
|--------|--------|------|
| [server-supabase-via-api](rules/server-supabase-via-api.md) | CRITICAL | クライアントから Supabase 直接使用禁止、API Route 経由必須 |
| [server-only-directive](rules/server-only-directive.md) | HIGH | Handler/Service/Repository/Adapter に `import 'server-only'` を必須で記述 |
| [server-no-public-env](rules/server-no-public-env.md) | HIGH | 機密情報（Supabase, API キー）に `NEXT_PUBLIC_` 禁止 |
| [server-webhook-signature-validation](rules/server-webhook-signature-validation.md) | CRITICAL | Webhook署名検証必須、署名なしでのペイロードパース禁止 |

### スキーマ・型定義 (`schema-`)

| ルール | Impact | 説明 |
|--------|--------|------|
| [schema-single-source](rules/schema-single-source.md) | HIGH | 型定義は `schema.ts` に一元化、`types.ts` 作成禁止 |
| [schema-zod-infer](rules/schema-zod-infer.md) | MEDIUM | Input 型は手書きせず `z.infer<typeof schema>` で導出 |

### レスポンス (`response-`)

| ルール | Impact | 説明 |
|--------|--------|------|
| [response-with-http-error](rules/response-with-http-error.md) | HIGH | Handler関数は withHTTPError でラップ必須 |
| [response-apperror](rules/response-apperror.md) | MEDIUM | エラーは `AppError` クラスでスロー、生の Error 禁止 |
| [response-helpers](rules/response-helpers.md) | LOW | `AppResponse.ok()`, `AppResponse.created()` 等のレスポンスヘルパーを使用 |
| [response-adapter-errors](rules/response-adapter-errors.md) | HIGH | Adapter層は外部APIエラーをAppErrorに変換してスロー |

### テスト (`test-`)

| ルール | Impact | 説明 |
|--------|--------|------|
| [test-layer-mocking](rules/test-layer-mocking.md) | HIGH | 各レイヤーは直下の依存のみをモック |
| [test-server-only](rules/test-server-only.md) | MEDIUM | `server-only` はテスト環境でモック必須 |
| [test-file-location](rules/test-file-location.md) | LOW | テストファイルは `__tests__` に配置 |
| [test-naming](rules/test-naming.md) | LOW | テストは日本語で意図を明確に |

### バリデーション (`validation-`)

| ルール | Impact | 説明 |
|--------|--------|------|
| [validation-request](rules/validation-request.md) | MEDIUM | リクエスト入力値（ボディ、パスパラメータ、クエリパラメータ）をZodでバリデーション |

### 命名規則 (`naming-`)

| ルール | Impact | 説明 |
|--------|--------|------|
| [naming-files](rules/naming-files.md) | LOW | ファイル・ディレクトリ名は kebab-case（フレームワーク規約ファイルを除く） |
| [naming-methods](rules/naming-methods.md) | LOW | Repository: `findMany`/`findById`、Service: `get*`/`create*` |
| [naming-exports](rules/naming-exports.md) | MEDIUM | `_` prefix内部実装 + ファイル末尾でexport集約 |

### フロントエンド (`frontend-`)

| ルール | Impact | 説明 |
|--------|--------|------|
| [frontend-data-fetching](rules/frontend-data-fetching.md) | LOW | Featureごとに`fetcher.ts`と`hooks.ts`を作成、コンポーネントから直接fetch禁止 |
