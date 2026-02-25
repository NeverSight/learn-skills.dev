---
name: ccskills
description: Claude Codeのカスタマイズを支援。「Claude Codeをカスタマイズしたい」「こういう挙動にしたい」「自動で〇〇したい」などのリクエストに対応し、適切な設定ファイルを作成・配置する。
argument-hint: [カスタマイズ内容 | update <section> | sync]
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebFetch
---

# Claude Code カスタマイズ支援スキル

ユーザーのカスタマイズリクエストに対し、適切な機能を選択し、正しい場所にファイルを配置します。

## 呼び出し方

```
/ccskills                          # カスタマイズ支援（対話）
/ccskills ファイル保存時に自動lint    # 引数付きで呼び出し
/ccskills update <section>         # リファレンスの特定セクションを更新
/ccskills sync                     # GitHubから最新版を同期
```

---

## サブコマンド

### `/ccskills update <section>`

reference.mdの指定セクションを公式ドキュメントから更新する。

**セクション名と出典URL**:

| section | 出典URL |
|---------|---------|
| memory | https://code.claude.com/docs/ja/memory |
| skills | https://code.claude.com/docs/ja/skills |
| subagents | https://code.claude.com/docs/ja/sub-agents |
| settings | https://code.claude.com/docs/ja/settings |
| hooks | https://code.claude.com/docs/ja/hooks |
| mcp | https://code.claude.com/docs/ja/mcp |
| plugins | https://code.claude.com/docs/ja/plugins |
| best-practices | https://code.claude.com/docs/ja/best-practices |

**手順**:
1. WebFetchで出典URLから最新情報を取得
2. reference.mdの該当セクションを更新
3. 「最終更新」日付を現在日に更新
4. 変更内容のサマリーを報告

### `/ccskills sync`

GitHubリポジトリ https://github.com/myuon/ccskills から.claudeディレクトリを同期する。

**手順**:
```bash
# 1. リモート追加（初回のみ、既にあればスキップ）
git remote add ccskills-upstream https://github.com/myuon/ccskills.git 2>/dev/null || true

# 2. フェッチ
git fetch ccskills-upstream

# 3. .claude ディレクトリを上書き
git checkout ccskills-upstream/main -- .claude

# 4. 結果確認
git status --short .claude
```

**注意**: ローカルの変更は上書きされる

---

## 意思決定ガイド

### どの機能を使うか？

| やりたいこと | 使う機能 | 配置場所 |
|-------------|----------|---------|
| 常にこのルールを適用 | CLAUDE.md / Rules | `.claude/CLAUDE.md`, `.claude/rules/*.md` |
| ワークフローを定型化 | Skills | `.claude/skills/<name>/SKILL.md` |
| ツールを許可/拒否 | Settings (permissions) | `.claude/settings.json` |
| 自動実行（lint, 検証, ブロック） | Hooks | `.claude/settings.json` |
| 独立コンテキストで調査/実行 | Subagents | `.claude/agents/<name>.md` |
| 外部ツール連携 | MCP | `claude mcp add` コマンド |
| まとめて配布 | Plugins | `.claude-plugin/plugin.json` |

### ファイル配置場所（詳細）

| 機能 | プロジェクト用 | 個人用（全プロジェクト） |
|------|---------------|------------------------|
| Memory | `.claude/CLAUDE.md` または `./CLAUDE.md` | `~/.claude/CLAUDE.md` |
| Rules | `.claude/rules/*.md` | - |
| Skills | `.claude/skills/<name>/SKILL.md` | `~/.claude/skills/<name>/SKILL.md` |
| Agents | `.claude/agents/<name>.md` | `~/.claude/agents/<name>.md` |
| Settings | `.claude/settings.json` | `~/.claude/settings.json` |
| Hooks | `.claude/settings.json` | `~/.claude/settings.json` |
| MCP | `.mcp.json` | `claude mcp add --scope user` |

## 対応フロー

1. ユーザーのリクエストを分析
2. 上記の意思決定ガイドで最適な機能を選択
3. 適切な場所にファイルを作成
4. 設定内容と使い方を説明

## 詳細リファレンス

- 各機能の詳細: [reference.md](reference.md)
- 具体的な実装例: [examples.md](examples.md)

## カスタマイズ作成時の原則

1. **最小限から始める** - 必要なものだけ追加
2. **具体的に書く** - 曖昧な指示は効果が薄い
3. **テストする** - 作成後に動作確認
4. **共有を考慮** - `.local` ファイルと通常ファイルの使い分け
