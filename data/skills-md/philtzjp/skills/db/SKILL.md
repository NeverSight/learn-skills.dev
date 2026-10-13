---
name: db
description: データベースの選定、スキーマ定義、接続、マイグレーション。Postgres なら Neon、SQLite なら Cloudflare D1、ORM は Drizzle。app_migrations と app_application で接続先とロールを分ける。データ移行は件数取得、ドライラン、検証、本番実行、API 削除の順で行う。スキーマ変更、マイグレーション、既存レコードの一括変換、DB 接続設定の追加・修正・レビューを求められたときに使う。
---

# db

## 選定

- Postgres を使うなら Neon。
- SQLite を使うなら Cloudflare D1。
- ORM とマイグレーションツールは Drizzle に統一する。生 SQL を直接書くのは、Drizzle で表現できない DDL や一括変換に限る。

どちらを選ぶかは、リレーション、トランザクション、同時書き込み、拡張機能の必要性で決める。Workers 上で完結し、書き込みが軽く、SQLite の機能で足りるなら D1。それ以外は Neon。

- Drizzle https://orm.drizzle.team/docs/overview
- Drizzle Kit https://orm.drizzle.team/docs/kit-overview
- マイグレーション https://orm.drizzle.team/docs/migrations
- Neon 接続 https://orm.drizzle.team/docs/connect-neon
- D1 接続 https://orm.drizzle.team/docs/sqlite/connect-cloudflare-d1
- Neon のロール管理 https://neon.com/docs/manage/roles
- D1 のマイグレーション https://developers.cloudflare.com/d1/reference/migrations/

## 接続先を分ける

アプリケーションの通常動作とスキーマ変更を、別の接続情報で行う。

- app_application — アプリが実行時に使う。DML のみ。テーブルの作成、変更、削除の権限を持たない。
- app_migrations — マイグレーションだけが使う。DDL を実行できる。

app_admin のような曖昧な名前を作らない。何ができるロールなのかが名前から判断できなくなり、結果として全権限を持つ接続をアプリが使い続けることになる。用途ごとに1つ、用途がそのまま名前になるロールだけを作る。

環境変数も分ける。

```txt
DATABASE_URL            # app_application。アプリの実行時に読む
MIGRATION_DATABASE_URL  # app_migrations。マイグレーション時だけ読む
```

- アプリのランタイムに MIGRATION_DATABASE_URL を渡さない。
- CI やデプロイのマイグレーション工程にだけ MIGRATION_DATABASE_URL を渡す。
- 読み取り専用の用途が明確にあるなら app_readonly を足す。用途がないなら作らない。

## Neon

```sql
CREATE ROLE app_migrations LOGIN PASSWORD '...';
CREATE ROLE app_application LOGIN PASSWORD '...';

-- スキーマの所有者は app_migrations
ALTER SCHEMA public OWNER TO app_migrations;

GRANT USAGE ON SCHEMA public TO app_application;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO app_application;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO app_application;

-- 今後 app_migrations が作るテーブルにも自動で付与する
ALTER DEFAULT PRIVILEGES FOR ROLE app_migrations IN SCHEMA public
  GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO app_application;
ALTER DEFAULT PRIVILEGES FOR ROLE app_migrations IN SCHEMA public
  GRANT USAGE, SELECT ON SEQUENCES TO app_application;
```

デフォルト権限の付与を忘れると、マイグレーションで追加したテーブルにアプリがアクセスできず、デプロイ後に初めて気づくことになる。

```ts
import { neon } from '@neondatabase/serverless'
import { drizzle } from 'drizzle-orm/neon-http'
import * as schema from './schema'

export const db = drizzle(neon(process.env.DATABASE_URL!), { schema })
```

- 本番と別に開発用のブランチを作り、開発が本番へ直接つながらないようにする。
- 接続文字列に含まれる認証情報をログや例外メッセージに出さない。

## Cloudflare D1

D1 には Postgres のようなロールがない。分離は接続経路で行う。

- アプリは Workers のバインディング経由で読み書きする。
- マイグレーションは wrangler と API トークン経由で実行する。アプリのバインディングからは DDL を流さない。
- マイグレーション用のトークンは、対象データベースだけに権限を絞る。

```ts
import { drizzle } from 'drizzle-orm/d1'
import * as schema from './schema'

export const getDb = (env: Env) => drizzle(env.DB, { schema })
```

```sh
npx wrangler d1 migrations apply <DB_NAME> --local
npx wrangler d1 migrations apply <DB_NAME> --remote
```

ロールで守れない分、レビューと実行経路の制限で担保する。アプリのコードから DDL を実行できる書き方を残さない。

## スキーマとマイグレーション

スキーマは Drizzle のスキーマ定義を単一の正とする。DB を直接触って変更しない。

```sh
pnpm drizzle-kit generate   # スキーマ差分からマイグレーションファイルを生成する
pnpm drizzle-kit migrate    # 生成済みのマイグレーションを適用する
```

- 生成されたマイグレーションファイルは必ず読んでからコミットする。意図しない DROP や型変換が入っていないか確認する。
- 適用済みのマイグレーションファイルを後から書き換えない。修正は新しいマイグレーションで行う。
- `drizzle-kit push` は開発中のブランチだけに使う。本番や共有環境に使わない。履歴が残らない。
- マイグレーションは前方互換にする。新旧のアプリコードが同時に動く時間帯があるため、列の削除やリネームは、追加、二重書き込み、切り替え、削除の複数段階に分ける。
- 大きなテーブルへのロックを伴う変更は、実行時間とロック範囲を事前に見積もる。
- 実行前にバックアップまたは復旧手段を確認する。Neon ならブランチ、D1 なら export。

## データ移行

既存レコードの一括変換やスキーマ移行に伴うデータ修正は、次の順で行う。いきなり本番のレコードを書き換えない。

1. 対象レコード数を取得する API を作る。
2. 変換を実行してドライランする API を作る。実際には書き込まず、変更されるはずの件数と内容を返す。
3. 事前に取得した件数とドライランの変更件数が一致するか確認する。一致しなければ修正して再実行する。
4. 一致したら本番で実行し、その後この API を削除する。

- API は実行後に必ず削除する。一時的な運用口を残さない。
- API には認証をかける。公開経路に置かない。
- 実行結果（件数、開始と終了、失敗したレコード）をログに残す。
- 件数が多い場合はバッチに分け、途中で失敗しても再実行できるようにする。冪等にするか、処理済みを記録する。
- 変換前の値を戻せるようにしてから実行する。

## 確定前に確認する

- Postgres なら Neon、SQLite なら D1 を選んでいるか。
- アプリの接続が app_application で、DDL 権限を持っていないか。
- app_admin のような用途の曖昧なロールを作っていないか。
- DATABASE_URL と MIGRATION_DATABASE_URL が分かれ、アプリのランタイムに後者が渡っていないか。
- Neon で ALTER DEFAULT PRIVILEGES を設定したか。新しいテーブルにアプリが届くか。
- D1 でアプリのコードから DDL を実行できる箇所がないか。
- 生成されたマイグレーションを読んだか。意図しない DROP がないか。
- 適用済みのマイグレーションファイルを書き換えていないか。
- 本番に `drizzle-kit push` を使っていないか。
- 列の削除やリネームを、新旧コードが共存する前提で段階に分けたか。
- データ移行で件数取得とドライランを行い、件数が一致してから実行したか。
- 移行用 API を削除したか。
