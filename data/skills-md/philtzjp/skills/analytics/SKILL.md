---
name: analytics
description: アクセス解析を組み込む。Google Analytics と Consent Mode の同意シグナル、Cookie バナー、Cloudflare Web Analytics による Cookie なし計測、Workers Analytics Engine、GraphQL Analytics API。計測タグの追加、同意管理、analytics_storage や ad_storage の設定、アクセス解析の選定や移行を求められたときに使う。
---

# analytics

## 選定

計測したいものと、同意取得の負担で選ぶ。

- Cloudflare Web Analytics — Cookie を使わず、クライアント側に識別子を保存しない。ページビュー、リファラ、Core Web Vitals を見たいだけならこれで足りる。Cookie バナーの負担がない。
- Google Analytics — ユーザー単位のファネル、コンバージョン、広告連携が要るなら。Cookie を使うため同意管理が必要になる。
- Workers Analytics Engine — 独自のイベントを時系列で記録したい場合。アプリ側の指標をサーバー側で持てる。
- GraphQL Analytics API — Cloudflare が持つリクエストやキャッシュの統計を取り出す。クライアント側の JavaScript を足さずに済む。

併用してよい。Web Analytics で全ページの素の数字を持ち、GA は必要な導線にだけ入れる、という分け方が同意管理の範囲を小さくする。

- GA4 https://developers.google.com/analytics/devguides/collection/ga4
- Consent Mode https://developers.google.com/tag-platform/security/guides/consent
- Cloudflare Web Analytics https://developers.cloudflare.com/web-analytics/
- Workers Analytics Engine https://developers.cloudflare.com/analytics/analytics-engine/
- GraphQL Analytics API https://developers.cloudflare.com/analytics/graphql-api/

## Google Analytics と同意

Cookie の使用について確認し、同意を得たときに同意シグナルを送る。

- analytics_storage は常に granted にする。基本的な分析は常に有効。
- ad_storage、ad_user_data、ad_personalization は既定で granted にする。
- ユーザーが「同意しない」を選んだら、広告関連の3つを denied に更新する。

事前同意が必要な地域（EEA、英国など）を対象にする場合、広告関連の既定値は granted ではなく denied にし、同意を得てから granted に更新する。対象地域を確認してから既定値を決める。

```html
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag() { dataLayer.push(arguments); }

  gtag('consent', 'default', {
    analytics_storage: 'granted',
    ad_storage: 'granted',
    ad_user_data: 'granted',
    ad_personalization: 'granted',
  });
</script>
```

```js
// 「同意しない」を選んだとき
gtag('consent', 'update', {
  ad_storage: 'denied',
  ad_user_data: 'denied',
  ad_personalization: 'denied',
});
```

- default はタグの読み込みより先に実行する。順序が逆だと既定値が効かない。
- 選択結果を保存し、再訪時に同じ状態を復元する。毎回バナーを出さない。
- 同意の取り消し導線を用意する。一度同意したら変更できない作りにしない。
- バナーで主要コンテンツを覆わない。キーボードで操作でき、フォーカスが閉じ込められる形にする。
- 計測 ID、コンバージョン設定、イベント名をコードに直書きして環境ごとに分岐させない。環境変数で切り替える。

## Cloudflare Web Analytics

Cookie もクライアント側の識別子も使わないため、多くの場合 Cookie バナーの対象にならない。ただし、対象地域の法制度と、他に入れている計測やタグを合わせて判断する。Web Analytics を入れたから同意不要と短絡しない。

導入方法は2つある。

- 自動 — Cloudflare をプロキシとして経由しているドメインで、ダッシュボードから有効にする。HTML を変更しない。
- 手動 — beacon のスクリプトを HTML に入れる。Cloudflare を経由していない配信でも使える。

見られるのはページビュー、リファラ、国、デバイス、Core Web Vitals など。ユーザー単位の追跡やファネル分析はできない。そこが必要なら GA を併用する。

## Workers Analytics Engine

アプリ固有のイベントを Workers から書き込む。

```ts
// wrangler の設定で ANALYTICS バインディングを定義しておく
env.ANALYTICS.writeDataPoint({
  blobs: ['checkout', 'card'],
  doubles: [amount],
  indexes: [tenantId],
})
```

- indexes はカーディナリティの低い値にする。ユーザー ID のような値を入れない。
- blobs と doubles に個人情報を入れない。メールアドレス、氏名、生の IP を書かない。
- 書き込みは非同期で、リクエストの応答を遅らせない範囲にとどめる。
- 集計は SQL API や GraphQL から行う。

## 共通の注意

- 計測を理由にページの表示を遅らせない。タグは非同期で読み込む。
- 個人を特定できる値を URL やイベントのパラメータに入れない。メールアドレス、会員番号、トークンを送らない。
- 内部アクセスとステージング環境を計測から除外する。数字が汚れる。
- 何を測るかを先に決める。取れるものを全部取る設定にしない。
- 計測タグを入れたことと、意思決定に使えることは別。見る指標と見る人を決めてから入れる。

## 確定前に確認する

- Cookie を使う計測を入れているなら、同意取得と取り消しの導線があるか。
- gtag の consent default が、タグの読み込みより先に実行されているか。
- 対象地域に合わせて広告関連の既定値を決めたか。
- 同意の選択が保存され、再訪時に復元されるか。
- Cookie バナーがキーボードで操作でき、主要コンテンツを覆っていないか。
- 個人を特定できる値をイベントや URL に含めていないか。
- ステージングと内部アクセスを除外したか。
- 計測 ID が環境変数で切り替わるか。直書きされていないか。
