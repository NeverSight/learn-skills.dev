---
name: seo-mastery-jp
description: 包括的なSEO最適化スキル（日本語版）。Googleの公式ガイドラインに基づく技術SEO、コンテンツSEO、構造化データ、Core Web Vitals、E-E-A-T対策を網羅し、実践的なコード生成とサイト監査ワークフローを提供
version: 1.0.0
author: pani
---

# SEO Mastery Agent Skills

Google公式ドキュメントに基づく包括的なSEO最適化スキル。技術SEO、コンテンツ最適化、構造化データ、Core Web Vitals、サイト監査を統合的にサポートします。

## このスキルを使うタイミング

### 🔧 技術SEO（Technical SEO）
- クロール・インデックス問題のデバッグ
- robots.txt / sitemap.xml の設定
- canonical URL / hreflang の実装
- JavaScript SEO対策
- モバイルファースト最適化
- サーバーサイドレンダリング（SSR）設定

### 📝 コンテンツSEO
- メタタグ（title, description）の最適化
- 見出し構造（H1-H6）の設計
- E-E-A-T（経験・専門性・権威性・信頼性）対策
- 検索意図に沿ったコンテンツ設計
- 内部リンク戦略

### 📊 構造化データ（Structured Data）
- JSON-LD形式のschema.org実装
- リッチリザルト対応（FAQ, How-to, Article, Product等）
- VideoObject, BroadcastEvent実装
- パンくずリスト（BreadcrumbList）設定
- LocalBusiness / Organization設定

### ⚡ Core Web Vitals
- LCP（Largest Contentful Paint）最適化
- INP（Interaction to Next Paint）改善
- CLS（Cumulative Layout Shift）対策
- パフォーマンス監視と改善

### 🔍 サイト監査
- 包括的なSEO監査ワークフロー
- 自動チェックリスト生成
- 問題の優先順位付け
- 改善レポート作成

## 🚀 クイックスタート

### 基本的な使い方

```
# メタタグ最適化を依頼
「このページのメタタグを最適化して」

# 構造化データ生成
「この記事にArticle構造化データを追加して」

# サイト監査実行
「このサイトのSEO監査をして」

# Core Web Vitals改善
「LCPを改善する方法を教えて」
```

---

## 📋 技術SEO チェックリスト

### クロール最適化
- [ ] robots.txt が正しく設定されている
- [ ] XML サイトマップが存在し、Search Console に送信済み
- [ ] 重要ページがnoindexになっていない
- [ ] クロール予算を無駄遣いしていない
- [ ] 404/5xx エラーがない

### インデックス最適化
- [ ] canonical URL が正しく設定されている
- [ ] 重複コンテンツが適切に処理されている
- [ ] hreflang（多言語サイトの場合）が正しい
- [ ] モバイル版とPC版で同じコンテンツ

### レンダリング最適化
- [ ] JavaScript が適切にレンダリングされる
- [ ] 重要なコンテンツがHTMLに含まれる
- [ ] 遅延読み込みが適切に実装されている

---

## 🏗️ 構造化データ テンプレート集

### Article（記事）

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "記事のタイトル（最大110文字推奨）",
  "description": "記事の説明文",
  "image": [
    "https://example.com/photos/1x1/photo.jpg",
    "https://example.com/photos/4x3/photo.jpg",
    "https://example.com/photos/16x9/photo.jpg"
  ],
  "datePublished": "2025-01-01T08:00:00+09:00",
  "dateModified": "2025-01-15T10:30:00+09:00",
  "author": {
    "@type": "Person",
    "name": "著者名",
    "url": "https://example.com/author/profile"
  },
  "publisher": {
    "@type": "Organization",
    "name": "サイト名",
    "logo": {
      "@type": "ImageObject",
      "url": "https://example.com/logo.png"
    }
  }
}
```

### FAQ（よくある質問）

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "質問1のテキスト",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "回答1のテキスト"
      }
    },
    {
      "@type": "Question",
      "name": "質問2のテキスト",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "回答2のテキスト"
      }
    }
  ]
}
```

### BreadcrumbList（パンくずリスト）

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "ホーム",
      "item": "https://example.com/"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "カテゴリ",
      "item": "https://example.com/category/"
    },
    {
      "@type": "ListItem",
      "position": 3,
      "name": "現在のページ"
    }
  ]
}
```

### Product（商品）

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "商品名",
  "image": "https://example.com/product.jpg",
  "description": "商品の説明",
  "brand": {
    "@type": "Brand",
    "name": "ブランド名"
  },
  "offers": {
    "@type": "Offer",
    "url": "https://example.com/product",
    "priceCurrency": "JPY",
    "price": "9800",
    "availability": "https://schema.org/InStock",
    "seller": {
      "@type": "Organization",
      "name": "販売者名"
    }
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.5",
    "reviewCount": "128"
  }
}
```

### LocalBusiness（ローカルビジネス）

```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "店舗名",
  "image": "https://example.com/store.jpg",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "○○区△△1-2-3",
    "addressLocality": "横浜市",
    "addressRegion": "神奈川県",
    "postalCode": "220-0001",
    "addressCountry": "JP"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": 35.4437,
    "longitude": 139.6380
  },
  "telephone": "+81-45-XXX-XXXX",
  "openingHoursSpecification": [
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
      "opens": "09:00",
      "closes": "18:00"
    }
  ],
  "priceRange": "¥¥"
}
```

### VideoObject（動画）

```json
{
  "@context": "https://schema.org",
  "@type": "VideoObject",
  "name": "動画タイトル",
  "description": "動画の説明",
  "thumbnailUrl": [
    "https://example.com/thumb-1x1.jpg",
    "https://example.com/thumb-4x3.jpg",
    "https://example.com/thumb-16x9.jpg"
  ],
  "uploadDate": "2025-01-01T08:00:00+09:00",
  "duration": "PT5M30S",
  "contentUrl": "https://example.com/video.mp4",
  "embedUrl": "https://example.com/embed/video123",
  "interactionStatistic": {
    "@type": "InteractionCounter",
    "interactionType": { "@type": "WatchAction" },
    "userInteractionCount": 12345
  },
  "hasPart": [
    {
      "@type": "Clip",
      "name": "イントロ",
      "startOffset": 0,
      "endOffset": 30,
      "url": "https://example.com/video?t=0"
    },
    {
      "@type": "Clip",
      "name": "メインコンテンツ",
      "startOffset": 30,
      "endOffset": 300,
      "url": "https://example.com/video?t=30"
    }
  ]
}
```

---

## ⚡ Core Web Vitals 最適化ガイド

### LCP（Largest Contentful Paint）- 2.5秒以下が目標

**主な原因と対策:**

| 原因 | 対策 |
|------|------|
| 遅いサーバーレスポンス | CDN導入、キャッシュ最適化、サーバースペック向上 |
| レンダーブロッキングリソース | CSS/JSの遅延読み込み、Critical CSSのインライン化 |
| 遅い画像読み込み | WebP/AVIF使用、適切なサイズ指定、preload設定 |
| クライアントサイドレンダリング | SSR/SSG導入、重要コンテンツの事前レンダリング |

**実装例: 画像のプリロード**
```html
<link rel="preload" as="image" href="hero-image.webp" fetchpriority="high">
```

### INP（Interaction to Next Paint）- 200ms以下が目標

**主な原因と対策:**

| 原因 | 対策 |
|------|------|
| 重いJavaScript | コード分割、不要なJSの削除、遅延実行 |
| 長いタスク | タスクの分割（yield to main thread） |
| 大きなDOMサイズ | DOM要素の削減、仮想スクロール導入 |
| サードパーティスクリプト | 遅延読み込み、必要性の見直し |

**実装例: 長いタスクの分割**
```javascript
async function processLargeArray(items) {
  for (const item of items) {
    processItem(item);
    // メインスレッドに制御を返す
    await new Promise(resolve => setTimeout(resolve, 0));
  }
}
```

### CLS（Cumulative Layout Shift）- 0.1以下が目標

**主な原因と対策:**

| 原因 | 対策 |
|------|------|
| サイズ未指定の画像/動画 | width/height属性を明示、aspect-ratio CSS使用 |
| 動的に挿入されるコンテンツ | 事前にスペースを確保、スケルトンUI使用 |
| Webフォント（FOUT/FOIT） | font-display: swap、フォントのプリロード |
| 広告・埋め込みコンテンツ | 固定サイズのコンテナを事前配置 |

**実装例: 画像のアスペクト比確保**
```html
<img src="image.jpg" width="800" height="600" alt="説明" 
     style="aspect-ratio: 4/3; width: 100%; height: auto;">
```

---

## 🎯 E-E-A-T 最適化チェックリスト

### Experience（経験）
- [ ] 実体験に基づくコンテンツを提供
- [ ] 実際の製品使用レビュー・写真を含む
- [ ] ケーススタディや事例を紹介

### Expertise（専門性）
- [ ] 著者情報ページが存在する
- [ ] 著者の資格・経歴を明記
- [ ] 専門分野に特化したコンテンツ
- [ ] 正確で最新の情報を提供

### Authoritativeness（権威性）
- [ ] 信頼できる外部サイトからの被リンク
- [ ] 業界団体・専門家からの引用
- [ ] ブランドメンション（言及）の獲得
- [ ] 専門家による監修・レビュー

### Trustworthiness（信頼性）
- [ ] HTTPS化されている
- [ ] プライバシーポリシーが存在
- [ ] 問い合わせ先が明確
- [ ] 会社情報・所在地が明記
- [ ] ユーザーレビュー・評価を掲載
- [ ] 情報源を明記・引用

---

## 🔍 サイト監査ワークフロー

### Phase 1: クロール診断（15分）

```bash
# robots.txtの確認
curl -s https://example.com/robots.txt

# サイトマップの確認
curl -s https://example.com/sitemap.xml | head -50

# インデックス状況（site:検索）
# Google検索で site:example.com を実行
```

**チェック項目:**
1. robots.txt で重要ページがブロックされていないか
2. sitemap.xml が存在し、主要ページを含んでいるか
3. インデックス数が想定と一致するか

### Phase 2: ページ単位診断（30分/ページ）

**HTMLヘッド要素:**
```bash
# メタ情報の抽出
curl -s https://example.com/ | grep -E '<title>|<meta name="description"|<link rel="canonical"'
```

**チェック項目:**
1. タイトルタグ（60文字以内、キーワード含む）
2. メタディスクリプション（120文字以内）
3. canonical URL
4. OGP / Twitter Cardタグ
5. 構造化データの有無

### Phase 3: パフォーマンス診断（20分）

**Lighthouse CLI:**
```bash
npx lighthouse https://example.com --output=json --output-path=./report.json
```

**チェック項目:**
1. Core Web Vitals スコア
2. アクセシビリティスコア
3. SEOスコア
4. パフォーマンス改善提案

### Phase 4: 競合分析（30分）

1. 上位表示サイトのコンテンツ量・構成
2. 被リンクプロファイル
3. 使用している構造化データ
4. ページ速度比較

### Phase 5: 改善優先度マトリクス

| 優先度 | 影響度 | 実装難易度 | 例 |
|--------|--------|------------|-----|
| 🔴 緊急 | 高 | 低 | noindex削除、404修正 |
| 🟡 高 | 高 | 中 | 構造化データ追加、メタタグ最適化 |
| 🟢 中 | 中 | 中 | Core Web Vitals改善 |
| 🔵 低 | 低 | 高 | サイト構造の大幅変更 |

---

## 📁 関連リファレンスファイル

このスキルには以下の詳細ドキュメントが含まれます：

| ファイル | 内容 | 使用場面 |
|----------|------|----------|
| [technical-seo.md](technical-seo.md) | robots.txt、sitemap、canonical、hreflang等 | 技術的なSEO設定時 |
| [content-seo.md](content-seo.md) | メタタグ、見出し構造、コンテンツ設計 | コンテンツ最適化時 |
| [structured-data.md](structured-data.md) | 全構造化データタイプの詳細 | リッチリザルト実装時 |
| [core-web-vitals.md](core-web-vitals.md) | LCP/INP/CLS詳細な最適化手法 | パフォーマンス改善時 |
| [audit-workflow.md](audit-workflow.md) | 監査手順、ツール、レポート形式 | サイト監査実施時 |

---

## 🛠️ 推奨ツール

### Google公式
- [Google Search Console](https://search.google.com/search-console) - インデックス状況・検索パフォーマンス
- [PageSpeed Insights](https://pagespeed.web.dev/) - Core Web Vitals測定
- [Rich Results Test](https://search.google.com/test/rich-results) - 構造化データ検証
- [Mobile-Friendly Test](https://search.google.com/test/mobile-friendly) - モバイル対応確認

### CLI/開発ツール
- Lighthouse CLI - パフォーマンス監査
- Screaming Frog - 大規模サイトクロール
- ahrefs / SEMrush - 競合・被リンク分析

---

## ⚠️ よくある間違いと対策

### 1. 過度なキーワード詰め込み
❌ 「SEO SEO SEO対策 SEO最適化 SEOツール」
✅ 自然な文脈でキーワードを使用

### 2. 重複コンテンツ
❌ wwwありなし、http/httpsで別URLとして存在
✅ canonical設定、301リダイレクト

### 3. 遅い画像読み込み
❌ 大きなPNG/JPGをそのまま使用
✅ WebP変換、適切なサイズ、lazy loading

### 4. 構造化データのエラー
❌ 必須フィールドの欠落、不正な形式
✅ Rich Results Testで事前検証

### 5. モバイル非対応
❌ PC版のみ、タッチ非対応
✅ レスポンシブデザイン、タップ領域確保

---

## 📚 公式リソース

- [Google Search Central](https://developers.google.com/search)
- [SEO Starter Guide](https://developers.google.com/search/docs/fundamentals/seo-starter-guide)
- [Search Essentials](https://developers.google.com/search/docs/essentials)
- [Structured Data Documentation](https://developers.google.com/search/docs/appearance/structured-data)
- [Core Web Vitals](https://web.dev/vitals/)

---

## 更新履歴

- **v1.0.0** (2025-01) - 初版リリース
  - Googleの公式SEOガイドを基に作成
  - 技術SEO、コンテンツSEO、構造化データ網羅
  - Core Web Vitals（2024年INP対応版）
  - E-E-A-T対策チェックリスト追加
  - サイト監査ワークフロー追加
