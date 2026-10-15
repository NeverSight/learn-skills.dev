---
name: windows-data-storage
description: >
  Windows アプリ開発 (Windows App SDK / WinRT) のファイル・設定・データ保存リファレンス。
  Windows.Storage の StorageFile, StorageFolder, IStorageItem, FileIO, PathIO,
  CachedFileManager, DataReader, DataWriter。ApplicationData, ApplicationDataContainer,
  ApplicationDataCompositeValue によるローカル・ローミング設定。
  FileOpenPicker, FileSavePicker, FolderPicker, StorageApplicationPermissions,
  KnownFolders によるファイルアクセスと権限。JsonObject, JsonArray, XmlDocument,
  SQLite, EF Core によるシリアライズと永続化。
user-invocable: false
---

# Windows データ・ストレージ リファレンス

Windows App SDK / WinRT が提供するファイル操作・アプリデータ・ファイルピッカー・データシリアライズの公式ドキュメントを蒸留したリファレンス。
デスクトップアプリでのファイル読み書き、設定の永続化、ユーザー選択によるファイルアクセス、JSON / XML / SQLite を使ったデータ保存を網羅する。
ユーザーのタスクに応じて適切な README.md を読み、そこから個別ファイルへ辿ること。

## ディレクトリ構成

```text
skills/windows-data-storage/
  SKILL.md
  references/
    storage-files/
      README.md
      storage-file.md
      storage-folder.md
      istorage-item.md
      file-io.md
      path-io.md
      cached-file-manager.md
      storage-stream-transaction.md
      irandom-access-stream.md
      data-reader-writer.md
      storage-item-thumbnail.md
      storage-library.md
      storage-library-change-tracker.md
      storage-provider-sync-root-manager.md
      downloads-folder.md
      streamed-file-content.md
      access-sd-card.md
      system-io-vs-windows-storage.md
    app-data-settings/
      README.md
      application-data.md
      application-data-container.md
      application-data-composite-value.md
      windows-app-sdk-application-data.md
      settings-limits-and-roaming.md
      packaged-vs-unpackaged-app-data.md
      app-data-versioning-and-migration.md
    pickers-access/
      README.md
      file-open-picker.md
      file-save-picker.md
      folder-picker.md
      hwnd-initialization.md
      windows-app-sdk-pickers.md
      storage-application-permissions.md
      known-folders.md
      file-access-permissions.md
    data-serialization/
      README.md
      json-object.md
      json-array.md
      json-value.md
      xml-document.md
      json-vs-system-text-json.md
      sqlite-data-access.md
      ef-core-sqlite-provider.md
      application-data-storage.md
      caching-strategy.md
      storage-file-query-result.md
      query-options.md
      common-file-query.md
      storage-folder-item-query-result.md
```

## 探索手順

タスクからカテゴリを引き、カテゴリの README.md で目的のページを特定する:

1. 下記マッピング表でタスクに対応するカテゴリを探す
2. そのカテゴリの `references/{category}/README.md` を参照して目的のページを特定する
3. 該当ページの `.md` を Read して詳細を確認する

## タスク → カテゴリ マッピング

| タスク | カテゴリ | 参照 README |
|--------|---------|------------|
| StorageFile / StorageFolder でファイル・フォルダーの取得・作成・削除・列挙をしたい | storage-files | [references/storage-files/README.md](references/storage-files/README.md) |
| FileIO / PathIO / DataReader / DataWriter でテキスト・バイナリの読み書きをしたい | storage-files | [references/storage-files/README.md](references/storage-files/README.md) |
| CachedFileManager / IRandomAccessStream / StorageStreamTransaction でストリームの整合性を扱いたい | storage-files | [references/storage-files/README.md](references/storage-files/README.md) |
| System.IO と Windows.Storage のどちらを使うか判断したい | storage-files | [references/storage-files/README.md](references/storage-files/README.md) |
| ApplicationData / ApplicationDataContainer でローカル・ローミング設定を保存したい | app-data-settings | [references/app-data-settings/README.md](references/app-data-settings/README.md) |
| パッケージ化・非パッケージ化アプリでの ApplicationData の違いを知りたい | app-data-settings | [references/app-data-settings/README.md](references/app-data-settings/README.md) |
| アプリデータのバージョニング・移行・サイズ制限を扱いたい | app-data-settings | [references/app-data-settings/README.md](references/app-data-settings/README.md) |
| FileOpenPicker / FileSavePicker / FolderPicker でユーザーにファイル・フォルダーを選択させたい | pickers-access | [references/pickers-access/README.md](references/pickers-access/README.md) |
| デスクトップアプリでピッカーの HWND 初期化・WindowId 設定をしたい | pickers-access | [references/pickers-access/README.md](references/pickers-access/README.md) |
| KnownFolders / StorageApplicationPermissions でアクセス許可・既知フォルダーを扱いたい | pickers-access | [references/pickers-access/README.md](references/pickers-access/README.md) |
| JsonObject / JsonArray / JsonValue / XmlDocument で構造化データをパース・生成したい | data-serialization | [references/data-serialization/README.md](references/data-serialization/README.md) |
| SQLite / EF Core でローカルデータベースを構築したい | data-serialization | [references/data-serialization/README.md](references/data-serialization/README.md) |
| QueryOptions / CommonFileQuery / StorageFileQueryResult でファイルクエリ・キャッシュ戦略を扱いたい | data-serialization | [references/data-serialization/README.md](references/data-serialization/README.md) |
| StorageFolderQueryResult / StorageItemQueryResult でフォルダー・混在アイテムのクエリ結果を列挙したい | data-serialization | [references/data-serialization/README.md](references/data-serialization/README.md) |

このスキルは Windows App SDK / WinRT のファイル・設定・データ保存 API のみを扱う。コントロール UI は windows-winui-controls、ライフサイクル・ウィンドウ・通知は windows-app-sdk が担当し、いずれもここでは扱わない。
