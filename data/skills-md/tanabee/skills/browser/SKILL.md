---
name: browser
description: chrome-devtools-mcp の CLI (`chrome-devtools`) を使ったブラウザ操作の総合スキル。既存ブラウザへの attach / 使い捨てテストブラウザ / ログイン状態を保持する永続プロファイルのいずれかをユーザーに必ず確認した上でサーバを立ち上げ、スナップショット取得・クリック・入力・ナビゲーション・スクショ・ネットワーク監視などを行う。
allowed-tools: Bash, Read, AskUserQuestion
---

`chrome-devtools-mcp` の CLI (`chrome-devtools`) でブラウザを起動し、その後の操作までカバーする。

## 1. 接続先の確認 (毎回必須)

`chrome-devtools status` で状態を確認した後、**起動済みでも未起動でも、必ず AskUserQuestion で接続先をユーザーに確認してから操作に入る**。daemon は前回の args を保持し続け、構成が合わないまま使うと黙って隔離 headless ブラウザに落ちて `about:blank` しか見えない事故になるため、毎回 `stop` → `start` で整える。

`status` に `Update available` が出ていたら、接続まわりの修正が頻繁に入るため `npm install -g chrome-devtools-mcp@latest` での更新を勧める (勝手に更新しない)。

選択肢は **3 つ**:

- **既存ブラウザに接続**: いま開いている Chrome に attach。実セッション (ログイン状態・拡張・タブ) を使いたいとき
- **テスト用ブラウザを起動**: 使い捨ての隔離 Chrome。ログイン不要な動作確認向け
- **永続プロファイルで起動**: ログイン状態を保持する自動化・検証用。プロファイル名も選んでもらう

### 既存ブラウザに接続

前提: Chrome 144+ で `chrome://inspect/#remote-debugging` の「Allow remote debugging for this browser instance」が ON。

`DevToolsActivePort` から port (1 行目) と WS path (2 行目) を読み、`--wsEndpoint` で接続する。**CLI で動く attach 手段はこれだけ**:

- `--autoConnect` は `--help` に出るが daemon に転送されず (upstream issue #1184)、黙って隔離 headless ブラウザにフォールバックする。使わない
- `--browserUrl` はトグル方式だと `/json/version` が 404 を返すため接続できない。使わない

```bash
# macOS: ~/Library/Application Support/Google/Chrome/DevToolsActivePort
# Linux: ~/.config/google-chrome/DevToolsActivePort
# Windows: $LOCALAPPDATA/Google/Chrome/User Data/DevToolsActivePort
AP="$HOME/Library/Application Support/Google/Chrome/DevToolsActivePort"
chrome-devtools stop 2>/dev/null
chrome-devtools start --wsEndpoint "ws://127.0.0.1:$(sed -n 1p "$AP")$(sed -n 2p "$AP")"
chrome-devtools list_pages
```

**接続判定**: `list_pages` に実タブが並べば成功。`about:blank` 1 件だけなら attach できておらず隔離ブラウザが起動している → `stop` して原因を切り分ける。

| 症状 | 原因と対処 |
|---|---|
| `DevToolsActivePort` がない | トグルが OFF。ユーザーに ON を依頼。ON でも生成されない環境が報告されている (upstream issue #2283) → 永続プロファイル起動に切り替え |
| 接続タイムアウト / 拒否 | 初回は Chrome 側に承認ダイアログが出る。Allow を依頼して再試行。token が stale の可能性もあるためトグル OFF→ON でファイル再生成も試す |
| 接続できたが目的のタブがない | attach は**承認したプロファイル 1 つ**にスコープされる。他プロファイルのウィンドウ・タブは見えない (検証済み) |

**実 Chrome プロファイル (Default / Profile N) を選んでデバッグ起動することは不可**: Chrome 136+ は default user-data-dir に対する `--remote-debugging-port` / `--remote-debugging-pipe` を無視する。実セッションが必要なら attach、特定アカウントのログイン状態が必要なら永続プロファイルに該当アカウントでログインして使う。

### テスト用ブラウザを起動

CLI の headless デフォルトは **true**。画面を見せる操作では `--headless=false` を明示する。

```bash
chrome-devtools stop 2>/dev/null
chrome-devtools start --headless=false   # isolated (使い捨て) がデフォルト
chrome-devtools list_pages
```

### 永続プロファイルで起動

`--userDataDir` にプロファイル名別のディレクトリを渡す。ログイン状態・Cookie はディレクトリ単位で永続する。

```bash
PROFILES="$HOME/.cache/chrome-devtools-mcp/profiles"
ls "$PROFILES" 2>/dev/null   # 既存一覧を AskUserQuestion の選択肢にする (新規名も可)
chrome-devtools stop 2>/dev/null
chrome-devtools start --headless=false --userDataDir "$PROFILES/<name>"
chrome-devtools list_pages
```

## 2. AI ワークフロー

1. **Inspect**: `take_snapshot` で要素の `<uid>` を取得
2. **Act**: `click` / `fill` / `navigate_page` 等で操作。状態はコマンド間で永続
3. 操作後の状態が必要なら、各操作コマンドに `--includeSnapshot true` を付ける

接続確立後は同一セッション中サーバが永続するので、都度 `start` / `status` / `stop` を呼ぶ必要はない。

スナップショット例:
```
uid=1_0 RootWebArea "Example Domain" url="https://example.com/"
  uid=1_1 heading "Example Domain" level="1"
```

## 3. コマンドリファレンス

カテゴリ別の使用例は [assets/commands.md](./assets/commands.md) を参照 (Input Automation / Navigation / Emulation / Debugging / Network / Performance / Memory / Extensions / Service Management / Experimental)。各コマンドは `--help` で詳細を確認できる。

## 注意事項

- このスキルで起動したブラウザには「Chrome is being controlled by automated test software」バナーが表示される
- `navigate_page` は全てフラグ指定: `navigate_page --url "<URL>"` / `navigate_page --type reload` (positional `type` は廃止)
- Experimental ツールは `start` 時に該当フラグが必要: `click_at` → `--experimentalVision`、`screencast_*` → `--experimentalScreencast` (要 ffmpeg)、`*_webmcp_tool*` → `--categoryExperimentalWebmcp` (Chrome 149+)
