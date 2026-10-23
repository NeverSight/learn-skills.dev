---
name: microcms-nextjs
description: Next.jsとmicroCMSの連携を公式情報に基づいて実装・改善する。SDKセットアップ、App Routerのデータ取得・動的ルート、キャッシュ・ISR・Webhook、Draft Mode、next/imageの実装や不具合調査で使用する。フレームワーク非依存のAPI仕様・コンテンツ設計のみの相談はmicrocms-guideを優先する。
license: MIT
---

# microCMS + Next.js

Next.jsプロジェクトでmicroCMSを適切に利用できるよう、既存コード・Next.jsのバージョン・キャッシュ構成を確認しながら具体的な実装まで支援する。

原則として日本語で回答する。ユーザーが別の言語を指定した場合は、その指定に従う。

## 基本方針

1. 既存プロジェクトが利用可能なら、コードを生成する前に構成を確認する。
2. Next.jsのバージョン、App Router / Pages Router、`cacheComponents` の有無を確認する。
3. ユーザーが求める更新反映時間、静的生成の必要性、プレビュー要件を確認する。
4. microCMS共通の詳細は、`microcms-guide` が利用可能なら関連リファレンスのみを読む。未導入・未読でも、このSkill内の説明と各リファレンスの公式情報から作業を進める。別Skillの自動読み込みを前提にしない。
5. 新規の例ではApp Routerを基本とするが、既存プロジェクトがPages Routerなら無理に移行させない。
6. APIキーはサーバー側で扱い、書き込み・下書き全取得・非公開データへアクセスできるキーをブラウザへ渡さない。CSRで直接取得する要件がある場合のみ、公開可能なAPIへのGET専用キーを検討する。Draft Keyも秘密情報として扱う。
7. Next.jsのキャッシュ仕様はバージョン依存性が高いため、古いパターンを機械的に適用しない。

## 最初にプロジェクト状態を判定する

キャッシュ・データ取得・Draft Modeに関する作業では、可能なら次を先に確認する。

- `package.json` の `next` バージョン
- `app/` または `src/app/` の有無
- `pages/` または `src/pages/` の有無
- `next.config.*` の `cacheComponents` 設定
- `microcms-js-sdk` のバージョン
- microCMSクライアントの作成場所
- APIキーの環境変数名
- ホスティング先と実行Runtime
- `output: 'export'` の有無（静的エクスポートではサーバー上のISR・Draft Mode・Webhook受信は実行できない）
- 既存の `revalidate`、`revalidatePath`、`revalidateTag`、`use cache`、`cacheLife`、`cacheTag` の利用状況

これらをコードから確認できる場合、ユーザーへ同じ情報を質問しない。

## Next.js 16以降のキャッシュモデルを区別する

Next.js 16では `cacheComponents: true` を有効にした場合と、従来のキャッシュモデルで設計が異なる。

- `cacheComponents: true` の場合は `use cache`、`cacheLife`、`cacheTag` を中心に考える。
- `cacheComponents` を利用していない場合は、`fetch` の `cache` / `next.revalidate`、Route Segment Config、`revalidatePath` / `revalidateTag` など従来モデルを確認する。

`export const revalidate = 60` をすべてのNext.jsプロジェクトへ無条件に提案しない。

詳細は [references/caching.md](references/caching.md) を読む。

## Server Componentsを基本にする

App RouterでmicroCMSの公開データをページ表示に使う場合は、特別な理由がなければServer Componentからサーバー側で取得する方法を第一候補にする。

以下の理由だけでClient Componentへしない。

- microCMSを使っているから
- API取得があるから
- ページ内に一部インタラクションがあるから

クライアント側の状態・イベント・ブラウザAPIが必要な部分だけをClient Componentへ分離する。

Server Componentから自分自身のRoute Handlerを経由してmicroCMSへアクセスする二重構成も、認証・BFF等の具体的理由がなければ作らない。

## 必要なリファレンスだけを読み込む

- **セットアップ**: `microcms-js-sdk`、環境変数、クライアント、型、安全な配置については [references/setup.md](references/setup.md) を読む。
- **データ取得**: Server Components、一覧・詳細、Dynamic Routes、`generateStaticParams`、ページネーション、大量ページのビルド時の429については [references/data-fetching.md](references/data-fetching.md) を読む。
- **キャッシュ・ISR**: Next.js 16のCache Components、従来モデル、ISR、On-demand Revalidation、Webhook、更新反映問題については [references/caching.md](references/caching.md) を読む。
- **プレビュー**: microCMSのDraft KeyとNext.js Draft Mode、プレビュー開始・終了Route Handlerについては [references/preview.md](references/preview.md) を読む。
- **画像**: `next/image`、`remotePatterns`、microCMS画像API、custom loaderの使い分けについては [references/images.md](references/images.md) を読む。

複数領域にまたがる場合は必要なリファレンスを組み合わせる。

例:

- 「Webhookで記事更新を即反映したい」 → `caching.md`
- 「下書きプレビューが古い」 → `preview.md` + `caching.md`
- 「画像転送量を減らしたい」 → `images.md` + `microcms-guide` の画像・performance原則

## 実装を変更するとき

既存プロジェクトでは次の順に進める。

1. 現在のmicroCMSクライアントとデータ取得関数を確認する。
2. キャッシュ戦略を確認する。
3. 問題を再現する経路を特定する。
4. 最小限の変更で解決する。
5. プロジェクト既存の命名・ディレクトリ・型・lint/format方針に従う。
6. 不要な依存パッケージや抽象化を追加しない。

ユーザーがコード修正を求めている場合は、説明だけで終わらせず、可能なら実際のファイルへ一貫した変更を行う。

## 更新が反映されない問題を診断する

「microCMSでは更新したのにNext.jsへ反映されない」場合は、次の順序で切り分ける。

1. microCMS Content APIを直接確認し、期待する公開データが返っているか。
2. Next.jsがどのデータ取得方式を使っているか。
3. `cacheComponents` の有無とキャッシュ設定。
4. 時間ベースのrevalidationかOn-demand Revalidationか。
5. Webhookが受信できているか。
6. `revalidatePath` / `revalidateTag` / `cacheTag` の対象が正しいか。
7. ホスティング・CDNなど別キャッシュ層があるか。

microCMSのCDNとNext.jsのキャッシュを混同しない。

## 品質基準

公式開発者ドキュメントの取得・仕様確認には、利用可能なら `microcms-docs` を併用する。設計判断や実装はこのSkillで進め、必要なページだけ確認する。未導入の場合は各referenceの公式出典を直接確認する。

- バージョン依存のNext.js挙動は、可能なら現在の公式Next.jsドキュメントを確認する。
- 新規コードも導入済みNext.js・SDKのバージョンに合わせる。最新ドキュメントのAPIを旧バージョンへそのまま持ち込まない。同梱内容と対象バージョンの公式仕様が矛盾する場合は公式仕様を優先する。
- キャッシュ戦略は更新要件から逆算する。
- 公開予約など時刻の正確性が重要な場合は、時間ベースISRだけで要件を満たせるか慎重に判断する。
- Draft Modeでは秘密情報とリダイレクト先を検証する。
- 画像最適化では、Next.js Image OptimizationとmicroCMS画像APIの役割を明確にし、二重最適化を目的なく行わない。
- microCMS固有の仕様をNext.jsの仕様として、Next.js固有の仕様をmicroCMSの仕様として説明しない。
