---
name: errorpage
description: エラー応答を設計する。404 と 410 と 301 の使い分け、soft 404 の回避、Accept に応じた HTML と Markdown と application/problem+json の出し分け、RFC 9457 Problem Details、キャッシュ方針、内部情報の漏えい防止、curl での検証。404 ページ、エラーページ、Not Found、エラーハンドリング、API のエラーレスポンスの実装・修正・レビューを求められたときに使う。
---

# errorpage

## 原則

エラーページは見た目の案内ではなく、HTTP 上の事実を正しく伝えつつ、人間・検索エンジン・API クライアント・AI エージェントを次の行動へ導くインターフェース。

最優先はステータスコード。CDN、ロードバランサ、SDK、ブラウザ、クローラは主にレスポンスのステータス行で意味を判断する。本文の「404」という文字やフィールドは補助情報にすぎない。

存在しない URL に通常画面を 200 OK で返す soft 404 を作らない。HTTP 上は「そのリソースは存在する」と宣言することになり、クローラ、監視、SDK、キャッシュが誤った前提で動く。

```http
# すべて不適切
HTTP/1.1 200 OK          ← 本文に <h1>404 Not Found</h1> があっても無意味
HTTP/1.1 200 OK          ← 本文が { "status": 404 } でも無意味
HTTP/1.1 302 Found       ← 代替がないのにトップへ飛ばす
Location: /
```

代替ページがないのにトップページや検索結果へリダイレクトしない。ユーザーには親切に見えるが、要求したリソースが移動したと誤認させる。代替が本当に等価なら 301 か 308、そうでなければ 404 か 410 の本文でナビゲーションを出す。

- https://www.rfc-editor.org/rfc/rfc9110.html
- https://www.rfc-editor.org/rfc/rfc9457.html

## コードの選択

- 404 Not Found — URL が誤っている、ルーティングされていない、存在確認ができない。現時点で表現がないという意味で、恒久削除までは明言しない。存在を明かしたくない場合にも使える。
- 410 Gone — 過去に存在し、意図して恒久的に廃止した。戻す予定も代替先もないと確定している場合だけ選ぶ。
- 301 Moved Permanently / 308 Permanent Redirect — 等価な移転先が確実にある場合のみ。
- 503 Service Unavailable — メンテナンス、過負荷、依存先障害。一時的に利用不能。
- 401 Unauthorized — 認証情報が必要、または不十分。
- 403 Forbidden — 認証済みでもアクセス不可。

権限のないリソースを 404 で隠すか 403 や 401 で明示するかは、セキュリティ方針として全体で一貫させる。ページごとに揺らさない。

## 実装順序

1. ルーティング層で、既知のページ・API・静的ファイル以外を捕捉する。
2. 旧 URL から等価な新 URL への対応表だけを 301 か 308 にする。
3. 廃止が確定した公開 URL だけを 410 にする。
4. その他の未知 URL は 404 にする。
5. Accept に応じて HTML、Markdown、application/problem+json の本文を出し分ける。
6. Vary: Accept を付け、表現ごとのキャッシュ混同を防ぐ。
7. 404 ログを収集し、参照元、頻出 URL、bot アクセスを見てリンク修正やリダイレクトに反映する。

## HTML 表現

```html
<!doctype html>
<html lang="ja">
  <head>
    <meta charset="utf-8">
    <title>ページが見つかりません | Example</title>
    <meta name="robots" content="noindex">
  </head>
  <body>
    <main>
      <h1>ページが見つかりません</h1>
      <p>URL が間違っているか、ページが移動・削除された可能性があります。</p>
      <nav aria-label="次の操作">
        <a href="/">ホームへ戻る</a>
        <a href="/search">サイト内を検索</a>
        <a href="/docs/">ドキュメント</a>
        <a href="/sitemap.xml">サイトマップ</a>
      </nav>
    </main>
  </body>
</html>
```

- 見つからないことを明記する。「エラーが起きました」だけでは原因が分からない。
- ホーム、サイト内検索、主要カテゴリ、ドキュメント、問い合わせ先へのリンクを置く。
- 要求 URL を画面に出すなら、クエリ文字列、トークン、メールアドレスをそのまま出さない。
- ブランドに沿わせつつ、通常のコンテンツページと紛らわしくしない。
- noindex は必須ではない。主目的は正しい 4xx を返すこと。404 テンプレート自体が検索結果に出るのを避けたいなら加えてよい。
- robots.txt で存在しない URL 群のクロールを全面禁止しない。アクセスできなければ 404 や 410 という状態を確認できなくなる。不要ページを消すなら、正しい 404 と 410、サイトマップからの削除、内部リンク修正が先。

## API 表現

RFC 9457 の Problem Details を使う。

```http
HTTP/1.1 404 Not Found
Content-Type: application/problem+json; charset=utf-8
Cache-Control: no-store
```

```json
{
  "type": "https://example.com/problems/resource-not-found",
  "title": "Resource not found",
  "status": 404,
  "detail": "No resource matches this URL. See https://example.com/docs/.",
  "instance": "urn:request:01JABC..."
}
```

- 本文の status は助言的。実際の HTTP ステータス行と必ず同じ値にする。
- detail はデバッグ情報ではなく、クライアントが問題を修正するための説明に集中させる。
- クライアントが文字列を解析して制御フローを作らせない。判定は HTTP ステータスと安定した type URI で行う。
- type URI には可能なら人間向けの説明文書を置く。
- 未知の拡張フィールドをクライアントが無視できる形にする。

## Markdown 表現

エージェント向け。Markdown は 404 の代わりではなく、404 の本文表現の一つ。ステータスは常に 404 のまま。

```http
HTTP/1.1 404 Not Found
Content-Type: text/markdown; charset=utf-8
Vary: Accept
Cache-Control: no-store
```

```md
# Not found

This URL does not exist.

- [Documentation index](/docs/)
- [Sitemap](/sitemap.xml)
- [LLM guidance](/llms.txt)
```

HTML を期待するブラウザに Markdown だけを返さない。Accept で出し分ける。開発者向けサイト、API サイト、プロダクト文書では、失敗したリクエストが行き止まりにならないよう探索の起点を入れる。

## HEAD

HEAD /does-not-exist は、本文を返さないだけで GET と同等のステータスを返す。HEAD レスポンスに本文は含まれない。

## キャッシュ

404 と 410 はキャッシュされ得る。存在しない URL へのアクセスが大量にあるサイトでは有効だが、公開直後や短期間で復活し得るリソースまで長く保持すると事故になる。

- 完全に廃止し復活しない URL — 410 と短〜中程度のキャッシュ。
- typo、ランダム URL、動的に出現し得る URL — 404 に no-store か短い max-age。
- 認可のために意図的に 404 を返す URL — 共有キャッシュ経由の情報漏えいを避けるため private, no-store。
- CDN がある場合、ブラウザ、CDN、アプリケーションの 404 挙動を別々に確認する。

## 漏らさない

エラー本文に次を出さない。

- スタックトレース、例外メッセージ、ソースマップ URL。
- フレームワーク名とバージョン、内部 IP、ホスト名。
- リポジトリパス、DB テーブル名、クラウドバケット名。
- ユーザー ID、メールアドレス、セッション情報。
- 「この非公開リソースは存在するが権限がない」と判別できる応答の差分。

Problem Details は実装のデバッグ情報を公開する仕組みではない。

## 検証

```sh
# ステータスだけ見る
curl -s -o /dev/null -w '%{http_code}\n' https://example.com/no-such-path

# リダイレクトを追わず最初の応答を見る
curl -sS -D - -o /dev/null https://example.com/no-such-path

# HEAD でも同じか
curl -sSI https://example.com/no-such-path

# API 表現
curl -sS -i -H 'Accept: application/problem+json' https://example.com/api/no-such-path

# Markdown 表現
curl -sS -i -H 'Accept: text/markdown' https://example.com/no-such-path
```

確認する。

- ステータス行が本当に 404、または意図した 410 か。
- 意図しない 30x がないか。
- Content-Type が本文の実体と一致しているか。JSON なら application/problem+json か。
- 本文に status を入れているなら HTTP ステータスと一致しているか。
- HTML にユーザーが復帰できる導線があるか。Markdown のリンクが有効か。
- 本文に秘密情報や内部情報がないか。
- HEAD が本文なしで同じ失敗ステータスを返すか。
- CDN やプロキシを経由した本番ドメインでも同じ結果になるか。
