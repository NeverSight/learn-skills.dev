---
name: mac-maintainer
disable-model-invocation: true
description: >
  Mac 環境にインストールされているソフトウェアを Homebrew / anyenv でアップデートする。
  「/mac-maintainer」のように、スキル名（committer）を明示的に指定した場合のみ起動する。
allowed-tools:
  - Bash(brew *)
  - Bash(anyenv *)
---

# Mac Maintainer

Homebrew と anyenv を使って Mac 環境のソフトウェアを最新状態に保つ。

## 実行フロー

### Step 1: 環境確認

最初に対象ツールのインストール状況を確認する。両方いっぺんに確認して、
インストールされていないツールはスキップして処理を進める。

```bash
brew --version 2>/dev/null
anyenv --version 2>/dev/null
```

### Step 2: Homebrew アップデート

Homebrew がインストールされている場合、以下の順で実行する。
各コマンドの出力はそのまま表示して、ユーザーが進捗を確認できるようにする。

```bash
# Homebrew 本体とフォーミュラ情報をアップデート
brew update

# インストール済みパッケージを最新バージョンにアップグレード
brew upgrade

# 古いバージョンのキャッシュを削除してディスクを整理
brew cleanup
```

アップグレードされたパッケージ名とバージョンをリスト化しておき、サマリーで使う。

### Step 2.5: アップグレード結果の確認

`brew upgrade` 完了後、まだ未アップデートのパッケージが残っていないか確認する：

```bash
brew outdated
```

何も出力されなければ全て最新。出力がある場合（sudo 必要な cask 等）は
サマリーの「要確認パッケージ」として記録する。

### Step 3: anyenv アップデート

anyenv がインストールされている場合、以下を実行する。

```bash
# anyenv 本体・全 env（nodenv / pyenv / rbenv など）・各 env のプラグインを一括アップデート
anyenv update
```

`anyenv update` コマンドが使えない場合（anyenv-update プラグイン未インストール）は、
スキルでは対応できないため、ターミナルで手動対応するよう案内する：

```
anyenv-update プラグインがインストールされていないため、自動アップデートできません。
ターミナルで以下を実行してください：

  mkdir -p $(anyenv root)/plugins
  git clone https://github.com/znz/anyenv-update.git $(anyenv root)/plugins/anyenv-update
  anyenv update
```

### Step 4: 結果サマリーの表示

全処理が完了したら以下の形式でサマリーを表示する。

```
## アップデート完了

### Homebrew
- アップグレード: N パッケージ（パッケージ名を列挙）
- クリーンアップ: 完了

### anyenv
- アップデート済み env: nodenv / pyenv / rbenv（インストールされているものを列挙）

### 注意事項
（エラーや要確認事項があれば記載）
```

## エラーハンドリング

エラーが発生してもパニックにならず、影響範囲を限定して残りの処理を続行する。

- **個別パッケージのエラー**: エラーになったパッケージ名を記録して、他のパッケージのアップデートを続ける。
  完了後にサマリーで「要確認パッケージ」として報告する。
- **sudo が必要な Cask**: displaylink など一部の cask はアンインストール時に sudo を要求する。
  インタラクティブなターミナル外（Claude Code の Bash 等）では自動実行できないため、
  エラー発生時は「ターミナルから手動で `brew upgrade --cask <cask名>` を実行してください」と案内する。
- **パーミッションエラー**: `/opt/homebrew` への書き込み権限がない場合、
  Homebrew の権限修復コマンド（`sudo chown -R $(whoami) $(brew --prefix)`）を案内する。
- **ネットワークエラー**: タイムアウトやアクセス失敗が出た場合、ネットワーク接続を確認するよう促す。
- **anyenv-update 未インストール**: Step 3 の案内テキストを表示する。
- **anyenv の一部エントリが "not git repo" でスキップ**: goenv の go-build など、git 管理されていない
  プラグインは `anyenv update` が自動でスキップする。これは正常な動作なので問題ない。

## 補足情報

必要に応じてユーザーに提供できる情報：

- **特定パッケージの固定**: `brew pin <package>` でアップグレード対象から除外できる。
  意図せず壊れたくないパッケージ（例: PHP バージョン、DB クライアント）に有効。
- **時間がかかる場合**: `brew upgrade` は大型パッケージ（FFmpeg, LLVM など）を含むと
  数十分かかることがある。バックグラウンドで実行することを提案してもよい。
- **mas（Mac App Store）**: `mas` がインストールされていれば `mas upgrade` で
  App Store アプリも一括アップデートできることを案内する。
