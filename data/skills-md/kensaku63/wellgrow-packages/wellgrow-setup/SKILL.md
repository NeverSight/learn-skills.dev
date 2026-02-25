---
name: wellgrow-setup
description: >
  WellGrow のセットアップを案内する。
  "wellgrowをセットアップ", "wellgrow MCPを入れたい", "setup wellgrow",
  "install wellgrow", "connect wellgrow", "wellgrowを接続",
  "wellgrow CLIを入れたい", "wellgrow CLIをセットアップ",
  などの発話で使用する。
---

# WellGrow セットアップ

WellGrow のセットアップを案内する。2つの方法がある。

- **方法 A（推奨）**: WellGrow CLI をインストールし、オンボーディングで MCP も含めて一括セットアップする
- **方法 B**: CLI は使わず、WellGrow MCP だけを手動で設定する

## 前提条件

- Node.js 20 以上（未導入なら https://nodejs.org を案内）

## 手順

### Step 1: 方法の選択

ユーザーに以下を聞く：

> WellGrow CLI をインストールしますか？
> CLI をインストールすると、ターミナルで AI チャットが使えるほか、オンボーディングで MCP の設定も一緒にできます（推奨）。
> CLI なしで MCP だけ設定することもできます。

- **はい** → 方法 A へ
- **いいえ** → 方法 B へ

---

## 方法 A: CLI インストール（推奨）

### Step A-1: CLI のインストール

ユーザーにターミナルで以下を実行してもらう：

```bash
npm install -g @wellgrow/cli
```

### Step A-2: オンボーディングの実行

インストール後、ターミナルで以下を実行してもらう：

```bash
wellgrow
```

初回起動時にオンボーディングウィザードが自動的に開始される。ウィザードでは以下が順番に案内される：

1. 名前の入力
2. Anthropic API キーの設定
3. WellGrow MCP の設定（メール・パスワード・OpenAI API キーを含む）
4. 推奨ツール・スキルのインストール

ユーザーにはオンボーディングの指示に従って進めてもらえばよい。MCP も含めてすべて設定できる。

### Step A-3: 完了確認

オンボーディングが完了すると、CLI がそのまま使えるようになる。

```bash
wellgrow --version
```

このスキルの役割はここまで。あとはオンボーディングエージェントが引き継ぐ。

---

## 方法 B: MCP のみ（CLI なし）

CLI をインストールしない場合、WellGrow MCP を手動で設定する。

### Step B-1: 情報の確認

ユーザーにどのツールで使うか聞く。
WellGrow MCP はリモートサーバーのため、API キーや認証情報の事前設定は不要。初回接続時にブラウザで OAuth ログインする。

### Step B-2: MCP サーバーの登録

#### ChatGPT アプリ

1. 設定 → アプリ → 「アプリを作成する（高度な設定）」を開く
2. 名前に `wellgrow` を入力
3. MCP サーバー URL に `https://wellgrow.ai/api/mcp` を入力
4. 保存して、OAuth ログインを完了する

#### Claude アプリ

1. 設定 → コネクタ → 「カスタムコネクタを追加」を開く
2. 名前に `wellgrow` を入力
3. リモート MCP サーバー URL に `https://wellgrow.ai/api/mcp` を入力
4. 保存して、OAuth ログインを完了する

#### Claude Code

```bash
claude mcp add --transport http \
  --scope user \
  wellgrow https://wellgrow.ai/api/mcp
```

`--scope user` で全プロジェクトから利用可能。

#### Cursor

`~/.cursor/mcp.json` に追加：

```json
{
  "mcpServers": {
    "wellgrow": {
      "type": "http",
      "url": "https://wellgrow.ai/api/mcp"
    }
  }
}
```

### Step B-3: MCP の動作確認

MCP の `list_questions` ツールを呼び出して接続を確認する。
質問一覧が返ってくれば成功。

---

## トラブルシューティング

### CLI 関連

| エラー | 対処 |
|--------|------|
| `wellgrow: command not found` | `npm install -g @wellgrow/cli` を再実行。Node.js のグローバル bin が PATH に含まれているか確認 |
| `ANTHROPIC_API_KEY` 未設定エラー | シェルの環境変数に `export ANTHROPIC_API_KEY=...` を追加し、シェルを再起動 |

### MCP 関連

| エラー | 対処 |
|--------|------|
| OAuth ログイン画面が開かない | ブラウザがデフォルトブラウザとして設定されているか確認 |
| 認証後もツールが使えない | MCP サーバーの設定を確認し、`url` が `https://wellgrow.ai/api/mcp` になっているか確認 |
| 接続タイムアウト | ネットワーク接続を確認 |

## アップデート

```bash
npm update -g @wellgrow/cli    # CLI
```
