---
name: e2etest
description: E2E テストを作成・実行する。agent-browser を主に使い、対応できないインタラクションに限って Playwright にフォールバックする。テストを書く条件と書かない条件、sleep によるタイミング依存の禁止、明示的な待機条件。ユーザー向け主要フローの追加、重要な UI 変更、既存フローの成功条件を変えたときに使う。
---

# e2etest

## 書くかどうか

次のいずれかに当てはまるなら、E2E テストを作成して実行する。

- 新しいユーザー向けの主要フローを追加した。
- 重要な UI を変更した。
- 既存フローの成功条件を変更した。

次には作らない。

- 純粋なバックエンドや API だけの変更。
- ドキュメントだけの変更。
- 設定や依存関係の更新。
- 動作が変わらないリファクタリング。

既存の管理画面に小さな設定項目を足しただけで、主要フローの成功条件が変わらないなら、agent-browser で手動検証する。リスクがある場合だけテストを作る。

## ツールの選択

主に agent-browser を使う。Rust 製の CLI で、出力が簡潔で、ref ベースのスナップショット（要素に @e1 のような識別子が付く）で要素を指せる。

- サイト https://agent-browser.dev/
- クイックスタート https://agent-browser.dev/quick-start
- コマンド一覧 https://agent-browser.dev/commands
- スナップショット https://agent-browser.dev/snapshots
- セレクタ https://agent-browser.dev/selectors
- ネットワーク https://agent-browser.dev/network
- デバッグ https://agent-browser.dev/debugging
- CDP モード https://agent-browser.dev/cdp-mode
- WebMCP https://agent-browser.dev/webmcp
- 変更履歴 https://agent-browser.dev/changelog
- リポジトリとリリース https://github.com/vercel-labs/agent-browser/releases

更新が速い。コマンドやオプションの形に迷ったら記憶で書かず、コマンド一覧と変更履歴を引く。

```sh
agent-browser open example.com
agent-browser snapshot -i
agent-browser click @e2
agent-browser screenshot page.png
```

## Playwright へのフォールバック

agent-browser で対応できないインタラクションに限る。

- キャンバス操作。
- 細かいマウス操作。
- タッチジェスチャー。
- ネットワーク傍受。
- 複数ページやクロスオリジンのフロー。
- WebSocket や SSE のアサーション。

フォールバックしたら、agent-browser で対応できなかった理由をテストファイルに書く。後から読む人が、単なる手癖なのか必然だったのかを判断できるようにする。

agent-browser で対応できるインタラクションに Playwright を使わない。

## 待機

`sleep` によるタイミング依存のテストを作らない。明示的な待機条件を使う。

- 要素の出現、消滅、テキストの変化を待つ。
- ネットワークの完了やレスポンスを待つ。
- 固定の秒数で「だいたい終わっているはず」を前提にしない。CI では遅くなり、ローカルでは速すぎる。

不安定なテストを `sleep` を伸ばして黙らせない。待つべき条件を特定して書き直す。

## 確定前に確認する

- 変更が主要フローや成功条件に触れているか。触れているならテストがあるか。
- agent-browser で書けるものを Playwright で書いていないか。
- Playwright を使ったなら、理由をテストファイルに書いたか。
- `sleep` が残っていないか。待機が明示的な条件になっているか。
- テストが CI で通るか。ローカルでしか通らない前提を持ち込んでいないか。
