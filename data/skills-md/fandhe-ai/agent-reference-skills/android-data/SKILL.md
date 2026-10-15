---
name: android-data
description: >
  Android アプリ開発 (Kotlin) のデータ層リファレンス。Jetpack androidx。
  Room (Entity, Dao, Query, Migration), DataStore (Preferences/Proto),
  MediaStore, SharedPreferences, スコープ付きストレージ, Retrofit, OkHttp。
user-invocable: false
---

# Android データ層リファレンス

Android アプリ開発 (Kotlin) のデータ層公式ドキュメントを蒸留したスキル。
ユーザーのタスクに応じて適切な README.md を読み、そこから個別ファイルへ辿ること。

## ディレクトリ構成

```text
skills/android-data/
  SKILL.md
  references/
    room/
      README.md
      entity.md
      primary-key.md
      column-info.md
      ignore.md
      embedded.md
      foreign-key.md
      dao.md
      query.md
      insert.md
      update.md
      delete.md
      upsert.md
      transaction.md
      database.md
      room-database-builder.md
      callback-driver.md
      migration.md
      type-converter.md
      relation.md
      fts-database-view.md
      async-queries.md
      testing.md
    datastore/
      README.md
      datastore.md
      datastore-factory.md
      preferences-datastore.md
      preferences.md
      preferences-keys.md
      edit.md
      proto-datastore.md
      data-migration.md
      shared-preferences-migration.md
      corruption-handler.md
    files-storage/
      README.md
      storage-overview.md
      app-specific-storage.md
      internal-file-io.md
      shared-preferences.md
      auto-backup.md
      mediastore.md
      storage-access-framework.md
      photo-picker.md
      embedded-photo-picker.md
      file-provider.md
      uri-permissions.md
      blobstore-manager.md
      scoped-storage.md
      cache-management.md
      activity-result-contracts-files.md
      assets.md
    network/
      README.md
      permissions-and-threading.md
      network-security-config.md
      connectivitymanager.md
      networkcapabilities.md
      network-callback.md
      data-saver.md
      downloadmanager.md
      cronet.md
      cronet-urlrequest.md
      cronet-okhttp-interceptor.md
      retrofit.md
      okhttp.md
      okhttp-websocket.md
      kotlinx-serialization-converter.md
      httpurlconnection.md
      caching-and-retry.md
```

## 探索手順

タスクからカテゴリを引き、カテゴリの README.md で目的のページを特定する:

1. 下記マッピング表でタスクに対応するカテゴリを探す
2. そのカテゴリの `references/{category}/README.md` を参照して目的のページを特定する
3. 該当ページの `.md` を Read して詳細を確認する

## タスク → カテゴリ マッピング

| タスク | カテゴリ | 参照 README |
|--------|---------|------------|
| Room で Entity / Dao / Database を定義したい | room | [references/room/README.md](references/room/README.md) |
| @Query / @Insert / @Update / @Delete / @Upsert で SQL 操作を書きたい | room | [references/room/README.md](references/room/README.md) |
| Room の Migration / AutoMigration でスキーマを変更したい | room | [references/room/README.md](references/room/README.md) |
| @Relation / @Fts4 / @DatabaseView で関連データや全文検索を扱いたい | room | [references/room/README.md](references/room/README.md) |
| Preferences DataStore / Proto DataStore でキー値・型付きデータを永続化したい | datastore | [references/datastore/README.md](references/datastore/README.md) |
| SharedPreferences から DataStore へ移行したい | datastore | [references/datastore/README.md](references/datastore/README.md) |
| 内部/外部ストレージにファイルを保存・読み込みしたい | files-storage | [references/files-storage/README.md](references/files-storage/README.md) |
| MediaStore / Storage Access Framework / Photo Picker でメディアファイルを扱いたい | files-storage | [references/files-storage/README.md](references/files-storage/README.md) |
| FileProvider でファイルを他アプリと共有したい | files-storage | [references/files-storage/README.md](references/files-storage/README.md) |
| スコープ付きストレージや MANAGE_EXTERNAL_STORAGE の制約を確認したい | files-storage | [references/files-storage/README.md](references/files-storage/README.md) |
| ConnectivityManager でネットワーク状態を監視したい | network | [references/network/README.md](references/network/README.md) |
| Network Security Config で通信ポリシーを設定したい | network | [references/network/README.md](references/network/README.md) |
| Retrofit / OkHttp / Cronet で HTTP 通信を実装したい | network | [references/network/README.md](references/network/README.md) |

Paging 3 は `android-architecture`、WorkManager は `android-background-work`、ランタイムパーミッションは `android-platform-core` の担当。
