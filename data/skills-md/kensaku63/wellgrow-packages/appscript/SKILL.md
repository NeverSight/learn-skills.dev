---
name: appscript
description: >
  clasp CLI を使って Google Apps Script プロジェクトをローカルで開発・デプロイする。
  TypeScript 対応、スプレッドシート関数、Web アプリ、定期実行トリガーなどを素早く作成できる。
  "GAS を作って", "Apps Script を書いて", "スプレッドシートの関数を作って", "clasp create",
  "clasp push", "clasp deploy", "GAS をデプロイ", "Webhook を GAS で作って",
  "定期実行スクリプト", "スプレッドシート自動化", "Gmail 自動化" などで使用する。
---

# clasp — Google Apps Script CLI

`clasp` CLI で Google Apps Script (GAS) プロジェクトをローカル開発・デプロイする。
TypeScript で書いて push するだけで、Google のサーバーで動くスクリプトが完成する。

- 公式ドキュメント: https://developers.google.com/apps-script/guides/clasp
- npm: https://www.npmjs.com/package/@google/clasp
- GitHub: https://github.com/google/clasp

## インストール & セットアップ

```bash
npm install -g @google/clasp
clasp login
```

Apps Script API を有効化: https://script.google.com/home/usersettings

## コマンド一覧

| コマンド | 用途 |
|----------|------|
| `clasp login` | Google アカウントで認証 |
| `clasp logout` | ログアウト |
| `clasp create --title "名前"` | 新規プロジェクト作成 |
| `clasp create --title "名前" --type sheets` | スプレッドシート紐付きで作成 |
| `clasp clone <scriptId>` | 既存プロジェクトをクローン |
| `clasp pull` | リモートからローカルへ取得 |
| `clasp push` | ローカルからリモートへアップロード |
| `clasp push --watch` | ファイル変更を監視して自動 push |
| `clasp status` | 追跡ファイルの状態表示 |
| `clasp open` | Apps Script エディタをブラウザで開く |
| `clasp open --webapp` | デプロイ済み Web アプリを開く |
| `clasp deployments` | デプロイ一覧 |
| `clasp deploy` | 新バージョンをデプロイ |
| `clasp undeploy <deploymentId>` | デプロイ削除 |
| `clasp version [description]` | バージョン作成 |
| `clasp versions` | バージョン一覧 |
| `clasp logs` | 実行ログ表示 |
| `clasp run <functionName>` | 関数をリモート実行 |
| `clasp setting` | プロジェクト設定表示 |

## プロジェクトタイプ

`clasp create --type <type>` で紐付けるコンテナを指定:

| type | 紐付け先 |
|------|---------|
| `standalone` | 独立プロジェクト（デフォルト） |
| `sheets` | Google スプレッドシート |
| `docs` | Google ドキュメント |
| `slides` | Google スライド |
| `forms` | Google フォーム |
| `webapp` | Web アプリケーション |
| `api` | API 実行可能 |

## TypeScript 対応

clasp は TypeScript をネイティブサポート。push 時に自動的に `.ts` → `.gs` に変換される。

### セットアップ

```bash
clasp create --title "My Project" --type sheets
npm init -y
npm install -D @types/google-apps-script
```

`tsconfig.json`:

```json
{
  "compilerOptions": {
    "lib": ["esnext"],
    "strict": true,
    "skipLibCheck": true
  }
}
```

`.clasp.json` に rootDir を設定してソースを分離:

```json
{
  "scriptId": "...",
  "rootDir": "src"
}
```

### ディレクトリ構成

```
my-gas-project/
├── .clasp.json
├── tsconfig.json
├── package.json
└── src/
    ├── appsscript.json
    ├── main.ts
    └── utils.ts
```

`src/appsscript.json`（マニフェスト）:

```json
{
  "timeZone": "Asia/Tokyo",
  "dependencies": {},
  "exceptionLogging": "STACKDRIVER",
  "runtimeVersion": "V8"
}
```

---

## よく作るパターン

### 1. スプレッドシートのカスタム関数

```typescript
function HELLO(name: string): string {
  return `こんにちは、${name}さん！`;
}

function FETCH_PRICE(ticker: string): number | string {
  const url = `https://api.example.com/price/${ticker}`;
  const res = UrlFetchApp.fetch(url);
  const data = JSON.parse(res.getContentText());
  return data.price ?? "取得失敗";
}
```

セルで `=HELLO("太郎")` や `=FETCH_PRICE("AAPL")` として使える。

### 2. Web アプリ（Webhook エンドポイント）

```typescript
function doPost(e: GoogleAppsScript.Events.DoPost): GoogleAppsScript.Content.TextOutput {
  const payload = JSON.parse(e.postData.contents);
  const sheet = SpreadsheetApp.openById("SHEET_ID").getActiveSheet();
  sheet.appendRow([new Date(), payload.event, JSON.stringify(payload.data)]);
  return ContentService.createTextOutput(JSON.stringify({ ok: true }))
    .setMimeType(ContentService.MimeType.JSON);
}

function doGet(): GoogleAppsScript.Content.TextOutput {
  return ContentService.createTextOutput(JSON.stringify({ status: "running" }))
    .setMimeType(ContentService.MimeType.JSON);
}
```

デプロイ手順:

```bash
clasp push
clasp deploy --description "Webhook v1"
clasp open --webapp
```

`appsscript.json` に Web アプリ設定を追加:

```json
{
  "timeZone": "Asia/Tokyo",
  "dependencies": {},
  "exceptionLogging": "STACKDRIVER",
  "runtimeVersion": "V8",
  "webapp": {
    "access": "ANYONE_ANONYMOUS",
    "executeAs": "USER_DEPLOYING"
  }
}
```

### 3. 定期実行（トリガー）

```typescript
function setupTrigger(): void {
  ScriptApp.newTrigger("dailyTask")
    .timeBased()
    .everyDays(1)
    .atHour(9)
    .create();
}

function dailyTask(): void {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Log");
  if (!sheet) return;
  sheet.appendRow([new Date(), "Daily task executed"]);
}
```

手動でトリガーを設置: `clasp run setupTrigger`
または Apps Script エディタのトリガー設定画面から設定。

### 4. Gmail 自動化

```typescript
function archiveOldThreads(): void {
  const threads = GmailApp.search("older_than:30d -is:starred label:inbox", 0, 100);
  for (const thread of threads) {
    thread.moveToArchive();
  }
}

function sendDailyDigest(): void {
  const threads = GmailApp.search("is:unread newer_than:1d", 0, 20);
  const summary = threads.map((t) => `• ${t.getFirstMessageSubject()}`).join("\n");
  if (summary) {
    GmailApp.sendEmail("you@example.com", "今日の未読メールまとめ", summary);
  }
}
```

### 5. スプレッドシート操作

```typescript
function syncDataToSheet(): void {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName("Data") ?? ss.insertSheet("Data");

  const res = UrlFetchApp.fetch("https://api.example.com/data");
  const items: Array<{ name: string; value: number }> = JSON.parse(res.getContentText());

  sheet.clear();
  sheet.appendRow(["名前", "値", "更新日時"]);
  for (const item of items) {
    sheet.appendRow([item.name, item.value, new Date()]);
  }
}
```

### 6. Slack 通知

```typescript
function notifySlack(message: string): void {
  const webhookUrl = PropertiesService.getScriptProperties().getProperty("SLACK_WEBHOOK_URL");
  if (!webhookUrl) throw new Error("SLACK_WEBHOOK_URL not set");

  UrlFetchApp.fetch(webhookUrl, {
    method: "post",
    contentType: "application/json",
    payload: JSON.stringify({ text: message }),
  });
}

function onFormSubmit(e: GoogleAppsScript.Events.SheetsOnFormSubmit): void {
  const values = e.values;
  notifySlack(`📝 新しいフォーム回答: ${values.join(", ")}`);
}
```

---

## 開発ワークフロー

### 新規プロジェクト作成

```bash
mkdir my-gas && cd my-gas
clasp create --title "My GAS Project" --type sheets
npm init -y
npm install -D @types/google-apps-script

# src/ に rootDir を変更
# .clasp.json の "rootDir" を "src" に設定
mkdir src
mv appsscript.json src/
```

### コーディング → デプロイ

```bash
# コードを書く（src/*.ts）

# push してリモートに反映
clasp push

# 動作確認
clasp open

# バージョン作成 & デプロイ
clasp deploy --description "v1.0"
```

### 既存プロジェクトの取得

```bash
clasp clone <scriptId>
# scriptId は Apps Script エディタの「プロジェクトの設定」で確認
```

## スクリプトプロパティ（環境変数）

API キーなどの秘密情報は PropertiesService で管理:

```typescript
// 設定（手動で Apps Script エディタから、または初回実行関数で）
function setProperties(): void {
  PropertiesService.getScriptProperties().setProperties({
    API_KEY: "your-api-key",
    SLACK_WEBHOOK_URL: "https://hooks.slack.com/...",
  });
}

// 取得
function getApiKey(): string {
  return PropertiesService.getScriptProperties().getProperty("API_KEY") ?? "";
}
```

## 主要な GAS サービス

| サービス | 用途 |
|---------|------|
| `SpreadsheetApp` | スプレッドシート操作 |
| `GmailApp` | Gmail 操作 |
| `CalendarApp` | カレンダー操作 |
| `DriveApp` | Google Drive 操作 |
| `DocumentApp` | ドキュメント操作 |
| `SlidesApp` | スライド操作 |
| `FormApp` | フォーム操作 |
| `UrlFetchApp` | HTTP リクエスト |
| `ContentService` | Web アプリレスポンス |
| `PropertiesService` | スクリプトプロパティ（環境変数） |
| `ScriptApp` | トリガー・権限管理 |
| `CacheService` | キャッシュ |
| `LockService` | 排他ロック |
| `Utilities` | エンコード・ハッシュ・日付 |
| `Logger` / `console` | ログ出力 |

## トラブルシューティング

| 問題 | 対処 |
|------|------|
| `clasp: command not found` | `npm install -g @google/clasp` を実行 |
| `ScriptError: Not logged in` | `clasp login` を実行 |
| `User has not enabled the Apps Script API` | https://script.google.com/home/usersettings で API を有効化 |
| `push` で型エラー | `@types/google-apps-script` がインストールされているか確認 |
| `run` で権限エラー | `clasp open` で一度エディタから手動実行して権限を承認 |
| デプロイ後に変更が反映されない | 新しいデプロイを作成する（既存デプロイは固定バージョン） |
| Web アプリの URL がわからない | `clasp deployments` でデプロイ一覧を確認 |

## 注意事項

- `clasp push` はリモートのファイルを上書きする。先に `clasp pull` で最新を取得すること
- Web アプリをデプロイするたびに新しい URL が発行される。固定 URL が必要なら `clasp deploy` の deploymentId を使い回す
- GAS の実行時間制限: 通常 6 分、Google Workspace で 30 分
- `UrlFetchApp.fetch` の同時接続数やレート制限に注意
