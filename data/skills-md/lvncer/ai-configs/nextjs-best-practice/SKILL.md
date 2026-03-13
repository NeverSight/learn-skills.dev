---
name: nextjs-best-practice
description: Next.js プロジェクトの実装方針を標準化する。ディレクトリ構造、命名規則、Server Components / Client Components の使い分け、Server Actions の配置、hooks/services/actions の責務分離をガイドする。Next.js の設計や実装方針を確認・統一したいときに使用する。
---

# Next.js Best Practice

## ディレクトリ構造

```sh
src/
├── app/ # Next.js App Router - ルーティングとページ
├── components/
│ ├── ui/      # Shadcn/ui コンポーネント - 再利用可能な UI プリミティブ
│ └── layouts/ # 一貫したページ構造のためのレイアウトコンポーネント
├── hooks/     # 共有ロジックのためのカスタム React フック
├── types/     # TypeScript 型定義
├── lib/
│ ├── constants/ # アプリケーション定数と設定
│ ├── utils/     # ユーティリティ関数とヘルパー
│ ├── actions/   # Server Actions（サーバーサイドのミューテーション）
│ └── services/  # ドメインサービス（ビジネスロジック、外部API呼び出し等）
└── tests/
├── unit/        # 個別の関数/コンポーネントのユニットテスト
├── integration/ # コンポーネント相互作用の統合テスト
└── e2e/         # 完全なユーザーフローのエンドツーエンドテスト
```

## ファイル命名規則

- **Pages**: `page.tsx` - Next.js App Router のページコンポーネント
- **Layouts**: `layout.tsx` - ルートグループの共有レイアウトコンポーネント
- **Loading**: `loading.tsx` - ルートセグメントのローディング UI
- **Errors**: `error.tsx` - ルートセグメントのエラー境界コンポーネント
- **APIs**: `route.ts` - サーバーエンドポイントの API ルートハンドラー

## コンポーネント設計原則

- **Server Components (デフォルト)**: データフェッチ、SEO 最適化、静的コンテンツのレンダリングに使用
- **Client Components (必要な場合)**: ブラウザ API、イベントリスナー、または React フックが必要な場合のみ使用
- **継承よりもコンポジション**: 小さな焦点を絞ったコンポーネントを組み合わせて複雑な UI を構築

## API 設計パターン

- **GET API なし**: API ルートの代わりに Server Components を使用してデータフェッチ
- **Server Actions を優先**: フォーム送信とミューテーションには Server Actions を使用
- **外部統合用の API ルート**: ウェブフックとサードパーティ統合にのみ POST/PATCH/PUT/DELETE を使用
- **型安全性**: リクエスト/レスポンス検証には常に Zod スキーマを使用

## Server Actions の配置方針

- 共有/ドメイン横断的な Server Actions は `lib/actions/` に配置する
- ルート専用の小さな Server Actions は、必要に応じて該当ルート直下（例: `app/(group)/feature/actions.ts`）に置いてもよい
- ファイル命名は動詞ベースで、1 ファイル = 1 概念（例: `user.ts`, `post.ts`）を原則とし、`index.ts` で再エクスポートを許容

## hooks / services / actions の使い分け

- `hooks`（クライアント専用）: React の状態・副作用・UI 連携に関するロジック。ブラウザ API、イベントハンドリング、フォーム状態など UI 寄りの責務
- `services`（サーバー/クライアント共有可）: ビジネスロジック、外部 API 呼び出し、プリミティブの組み合わせなどを純粋関数中心で実装。副作用は抽象化しテスト容易性を最優先
- `actions`（サーバー専用）: フォーム送信やミューテーションの入口。認証/認可、入力検証（Zod）、トランザクション制御、`services` のオーケストレーションを担当

ガイドライン:

- `hooks` は UI から `actions` を呼び出すための薄い橋渡しに留める
- ビジネスルールは可能な限り `services` に集約し、`actions` は I/O とオーケストレーションに専念
- `services` は副作用境界を明確化し、テストではモックで置き換え可能にする
