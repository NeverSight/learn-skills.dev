---
name: frontend-skills
description: >
  Argonauts Inc. フロントエンド開発スキル。Next.js App Router または React SPA (Vite) を使ったゼロからのプロジェクト構築、Tailwind CSS v4 + shadcn/ui によるスタイリング、render-as-you-fetch パターンのデータ取得実装を行う際に使用する。
  フロントエンドの新規プロジェクト作成、コンポーネント実装、データ取得、状態管理、スタイリングに関するタスクすべてに適用される。
  Use when: building new React/Next.js projects, implementing components with shadcn/ui, setting up data fetching, choosing state management solutions, configuring Tailwind CSS v4.
---

# Argonauts Inc. Frontend Skills

このスキルは AI エージェントが Argonauts Inc. のフロントエンド開発標準に従って、一貫した技術選定・コードパターンでプロジェクトをゼロから構築できるようにするためのガイドラインを提供します。

## 起動時に必ず確認する質問

スキル起動後、実装を始める前に以下を必ずユーザーに確認してください:

### Q1: フレームワーク選択
```
どちらのフレームワークを使用しますか？
1. Next.js (App Router) - SSR/SSG が必要、SEO 重視、フルスタック
2. React SPA (Vite) - クライアントサイドのみ、管理画面、ダッシュボード
```

### Q2: API 通信方式
```
API との通信方式はどれですか？
1. SWR + fetch (デフォルト) - REST API、シンプルな HTTP 通信
2. gRPC-connect (@connectrpc/connect) - gRPC/Connect プロトコル使用
3. OpenAPI + orval - OpenAPI スキーマからクライアント自動生成
```

### Q3: 状態管理
```
状態管理の要件を教えてください:
1. なし / 最小限 (useState + useReducer のみ)
2. 軽量グローバル状態 → Jotai を使用
3. 複雑なグローバル状態 → Zustand を使用
4. まだ決まっていない (後で references/state-management.md を参照して決定)
```

### Q4: Linting / Formatting (指定がなければ biome)
```
Linting / Formatting ツールを教えてください:
1. Biome (デフォルト推奨) - 高速、設定シンプル
2. oxlint + oxfmt - Oxide ツールチェーン
※ ESLint / Prettier は使用しません
```

---

## 技術スタック概要

| 項目 | 採用技術 |
|------|---------|
| Framework | Next.js (latest, App Router) / React SPA (Vite) |
| Language | TypeScript (strict モード必須) |
| Styling | Tailwind CSS v4 |
| UI Library | shadcn/ui |
| Data fetching | SWR + fetch (デフォルト) / gRPC-connect / orval |
| Data fetch 戦略 | render-as-you-fetch |
| Forms | react-hook-form + zod |
| Linting | Biome (デフォルト) |
| Testing | Vitest + @testing-library/react |

---

## References ナビゲーション

以下のタイミングで各 reference ファイルを参照してください:

### プロジェクト初期化時
- **[nextjs-app-router.md](references/nextjs-app-router.md)**: Next.js App Router プロジェクトを作成するとき
- **[react-spa.md](references/react-spa.md)**: Vite + React SPA プロジェクトを作成するとき
- **[npm-packages.md](references/npm-packages.md)**: 使用するパッケージを選定するとき (必ず参照)

### スタイリング・UI 実装時
- **[tailwind-shadcn.md](references/tailwind-shadcn.md)**: Tailwind CSS v4 の設定、shadcn/ui コンポーネント追加するとき
  - **重要**: Tailwind v3 と v4 は破壊的変更あり。必ずこのファイルを確認すること

### データ取得実装時
- **[data-fetching.md](references/data-fetching.md)**: API 通信の実装パターン (SWR/gRPC-connect/orval) を実装するとき
  - render-as-you-fetch パターンの実装方法

### 状態管理選択時
- **[state-management.md](references/state-management.md)**: グローバル状態管理の技術を選択するとき

### コーディング規約
- **[code-conventions.md](references/code-conventions.md)**: TypeScript、命名規則、コンポーネント構成パターン
  - Biome の設定方法も含む

### フォーム実装時
- **[form-patterns.md](references/form-patterns.md)**: react-hook-form + zod + shadcn/ui `<Form>` を使ったフォーム実装
  - 基本パターン、Server Action 連携、条件付きフィールド、useFieldArray、カスタムフック化

### テスト実装時
- **[testing.md](references/testing.md)**: Vitest + @testing-library/react を使ったテストパターン
  - vitest.config.ts 設定、コンポーネントテスト、非同期処理、MSW モック、カスタムフックのテスト

### 環境変数設定時
- **[env-vars.md](references/env-vars.md)**: Next.js / Vite の環境変数管理
  - .env ファイルの使い分け、NEXT_PUBLIC_ / VITE_ プレフィックス、zod バリデーション

### アンチパターン確認時
- **[anti-patterns.md](references/anti-patterns.md)**: 実装前・レビュー時に NG パターンを確認する

---

## ボイラープレートテンプレート

- **[assets/nextjs-template/](assets/nextjs-template/)**: Next.js App Router の最小構成テンプレート
- **[assets/react-spa-template/](assets/react-spa-template/)**: Vite + React SPA の最小構成テンプレート

---

## 重要な原則

1. **render-as-you-fetch を徹底**: `useEffect` + `fetch` の fetch-on-render は使用しない
2. **Server Component を優先**: `'use client'` は必要な場合のみ付与
3. **Tailwind v4 の記法を使用**: `tailwind.config.ts` は不要、`@import "tailwindcss"` を使う
4. **TypeScript strict モード**: `any` 型は使用しない
5. **ESLint / Prettier は使用しない**: Biome に統一
