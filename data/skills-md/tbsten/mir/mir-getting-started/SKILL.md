---
name: mir-getting-started
description: mir のインストールと基本的な使い方をユーザに案内する。「mir の使い方を教えて」「mir を始めたい」「snippet ツールの導入方法は？」など、mir を初めて使う場合や使い方を知りたい場合に使用する。
---

# getting-started

mir をインストールして基本的な使い方を教える skill。

## トリガー

ユーザが mir を初めて使う場合、使い方を知りたい場合に使用する。

## 手順

1. mir がインストールされているか確認する
   ```bash
   npx @tbsten/mir --version
   ```
2. インストールされていなければインストール方法を案内する
   ```bash
   npm i -g @tbsten/mir
   # または
   npx @tbsten/mir
   ```
3. ユーザがやりたいことを確認する。明示されていない場合は選択肢を提示:
   - **公開されている snippet を利用したい** → snippet の検索・インストール方法を案内
   - **独自の snippet を作成・公開したい** → snippet の作成・公開方法を案内
4. 選択に応じて案内する

### snippet を利用したい場合

```bash
# プロジェクトの初期化
mir init

# 利用可能な snippet を一覧表示
mir list

# snippet の詳細を確認
mir info <name>

# snippet をインストール
mir install <name>
```

### snippet を作成・公開したい場合

```bash
# プロジェクトの初期化
mir init

# snippet の雛形を作成
mir create <name>

# テンプレートファイルを .mir/snippets/<name>/ に配置
# .mir/snippets/<name>.yaml で変数を定義

# 変数定義を同期
mir sync <name>

# 動作確認
mir install <name> --out-dir=/tmp/test

# ローカル registry に公開
mir publish <name>

# リモート registry（official 等）に公開する場合:
# 1. まずログイン（GitHub OAuth）
mir login
# 2. リモート registry に公開
mir publish <name> --registry=official
```

## 注意事項

- `mir init` 実行前にプロジェクトのルートディレクトリにいることを確認する
- ユーザの習熟度に合わせて説明の詳細度を調整する
