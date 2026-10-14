---
name: hono
description: Hono で HTTP API を設計・実装する。@hono/zod-openapi による OpenAPI 準拠、RFC 9457 の problem+json エラー、パスバージョニング、Bearer 認証と loopback サービスの Origin 検証、ヘルスチェック、Spectral リント、@hono/mcp。API エンドポイント、ルーティング、OpenAPI スキーマ、認証方式、エラーレスポンス、MCP サーバーの追加・変更・レビューを求められたときに使う。
---

# hono

## 方針

HTTP フレームワークはプロジェクト内で Hono に統一する。同一プロジェクトに複数の HTTP フレームワークを混在させない。

ルート定義とスキーマと OpenAPI 文書を1か所から生成する。手書きの OpenAPI YAML を実装と別に持たない。二重管理は必ずずれる。

Hono は更新が速い。API の形やミドルウェアの引数に迷ったら、記憶に頼らず下のドキュメントを引く。

- ドキュメント https://hono.dev/docs/
- Hono オブジェクトとルーティング https://hono.dev/docs/api/hono
- HTTPException https://hono.dev/docs/api/exception
- ミドルウェアの仕組みと順序 https://hono.dev/docs/guides/middleware
- バリデーション https://hono.dev/docs/guides/validation
- bearer-auth https://hono.dev/docs/middleware/builtin/bearer-auth
- cors https://hono.dev/docs/middleware/builtin/cors
- secure-headers https://hono.dev/docs/middleware/builtin/secure-headers
- zod-openapi の例 https://hono.dev/examples/zod-openapi
- @hono/zod-openapi https://github.com/honojs/middleware/tree/main/packages/zod-openapi
- @hono/mcp https://github.com/honojs/middleware/tree/main/packages/mcp
- リリースと破壊的変更 https://github.com/honojs/hono/releases

仕様の一次ソース。

- RFC 9457 Problem Details https://www.rfc-editor.org/rfc/rfc9457.html
- Health Check Response Format https://datatracker.ietf.org/doc/html/draft-inadarei-api-health-check

## URL 設計

- パスバージョニングを使う。/api/v1/ 配下に置く。
- パスはできる限り短くする。やむを得ず複数語になる場合は kebab-case。
- 名詞は単数形。/users ではなく /user。
- パスパラメータは /user/{id} の形式。OpenAPI の表記と揃える。

```ts
import { Hono } from 'hono'

const api = new Hono().basePath('/api/v1')
```

## OpenAPI

@hono/zod-openapi を使い、ルートとスキーマから OpenAPI 文書を生成する。

```ts
import { OpenAPIHono, createRoute, z } from '@hono/zod-openapi'

const UserSchema = z.object({
  id: z.string().openapi({ example: '01JABC' }),
  displayName: z.string().max(50),
}).openapi('User')

const ProblemSchema = z.object({
  type: z.string(),
  title: z.string(),
  status: z.number(),
  detail: z.string().optional(),
}).openapi('Problem')

const getUser = createRoute({
  method: 'get',
  path: '/user/{id}',
  request: {
    params: z.object({ id: z.string() }),
  },
  responses: {
    200: {
      content: { 'application/json': { schema: UserSchema } },
      description: 'ユーザーを返す',
    },
    404: {
      content: { 'application/problem+json': { schema: ProblemSchema } },
      description: '該当するユーザーがない',
    },
  },
})

const app = new OpenAPIHono().basePath('/api/v1')

app.openapi(getUser, (c) => {
  const { id } = c.req.valid('param')
  return c.json({ id, displayName: '例' })
})

app.doc('/openapi.json', {
  openapi: '3.1.0',
  info: { title: 'Example API', version: '1.0.0' },
})
```

- 成功と失敗の両方を responses に書く。エラー応答を省略しない。
- 入力は c.req.valid() で受ける。生の c.req.json() を検証なしで使わない。
- スキーマに .openapi('User') で名前を付け、コンポーネントとして再利用する。

## エラー

RFC 9457 の Problem Details を返す。Content-Type は application/problem+json。

```ts
import { HTTPException } from 'hono/http-exception'

app.onError((err, c) => {
  const status = err instanceof HTTPException ? err.status : 500
  const problem = {
    type: `https://example.com/problems/${status === 404 ? 'not-found' : 'internal'}`,
    title: status === 404 ? 'Resource not found' : 'Internal server error',
    status,
    instance: c.get('requestId'),
  }
  return c.body(JSON.stringify(problem), status, {
    'Content-Type': 'application/problem+json; charset=utf-8',
  })
})
```

- 本文の status は HTTP ステータス行と必ず一致させる。
- detail はデバッグ情報ではなく、クライアントが直すための説明にする。
- スタックトレース、内部ホスト名、DB 名、ユーザー情報を出さない。
- 未知のパスは app.notFound() で同じ形式の 404 を返す。SPA のフォールバックで 200 を返さない。errorpage スキルを参照。
- クライアントには文字列ではなく HTTP ステータスと安定した type URI で分岐させる。

## 認証

ネットワークに公開する API は Bearer 認証。

```ts
import { bearerAuth } from 'hono/bearer-auth'

app.use('/api/v1/*', bearerAuth({ verifyToken: async (token, c) => verify(token) }))
```

loopback（127.0.0.1）にのみバインドするローカルサービスは、Bearer に代えて Origin と Host ヘッダーの検証で保護してよい。DNS リバインディング対策として必要。

```ts
app.use('*', async (c, next) => {
  const origin = c.req.header('Origin')
  const host = c.req.header('Host')
  if (origin && !ALLOWED_ORIGINS.includes(origin)) return c.body(null, 403)
  if (!host || !/^(127\.0\.0\.1|\[::1\]|localhost)(:\d+)?$/.test(host)) return c.body(null, 403)
  await next()
})
```

- 認可はミドルウェアで一括せず、リソースの所有権をハンドラかサービス層で必ず確認する。
- トークン検証、所有権、レート制限をクライアント側の入力に委ねない。

## ヘルスチェック

draft-inadarei-api-health-check に準拠させる。Content-Type は application/health+json。

```ts
app.get('/health', (c) =>
  c.body(JSON.stringify({
    status: 'pass',
    version: '1',
    releaseId: process.env.RELEASE_ID,
    checks: {
      'db:responseTime': [{ componentType: 'datastore', status: 'pass' }],
    },
  }), 200, { 'Content-Type': 'application/health+json; charset=utf-8' }))
```

- status は pass、warn、fail のいずれか。
- 認証の背後に置かない。監視から到達できなくなる。
- 依存先の詳細な内部情報を出さない。公開範囲を決めてから checks の粒度を決める。

## ミドルウェアの順序

上から順に適用される。順序を誤ると認証前にハンドラが動く。

1. requestId、logger。
2. secureHeaders、cors。
3. bearerAuth などの認証。
4. ルート個別のバリデーション。
5. ハンドラ。
6. onError と notFound は最後に登録する。

cors は必要なオリジンだけを列挙する。ワイルドカードと credentials を併用しない。

## MCP サーバー

MCP サーバーを立てるなら、採用フレームワークに対応するアダプタを使う。Hono では @hono/mcp。別の HTTP サーバーを併設しない。

## リント

```sh
npx --yes @stoplight/spectral-cli lint openapi.json
```

`.spectral.yaml` に `extends: ["spectral:oas"]` を置く。生成した OpenAPI 文書に対して実行し、CI に組み込む。規則を無効化して黙らせず、指摘は設計側で直す。

## 確定前に確認する

- HTTP フレームワークが Hono に統一されているか。他のフレームワークが混ざっていないか。
- OpenAPI 文書が実装から生成されているか。手書きの定義が別に残っていないか。
- パスが /api/v1/ 配下にあり、単数形で kebab-case か。
- すべての入力が c.req.valid() を通っているか。
- エラーが application/problem+json で、本文の status が HTTP ステータスと一致しているか。
- エラー本文に内部情報が漏れていないか。
- 公開 API に Bearer 認証があるか。loopback サービスに Origin と Host の検証があるか。
- 所有権の確認がハンドラかサービス層にあるか。
- /health が認証なしで到達でき、application/health+json を返すか。
- ミドルウェアの登録順が正しいか。onError と notFound が最後か。
- Spectral が CI で走っているか。
