---
name: japanese-writing
description: 日本語で文章を書く、直す、レビューするとき、日本語のコミットメッセージ、PR 説明、ドキュメント、UI 文言を書くときに参照する。このスキルは japanese スキルに統合した。内容は japanese スキルを使う。
---

# japanese-writing

このスキルは japanese スキルに統合しました。ここには規約を書いていません。

## すること

1. japanese スキルを読み、その規約に従う。
2. japanese スキルが見つからなければ、次のどちらかで読む。
   - `DISABLE_TELEMETRY=1 pnpm dlx skills add philtzjp/skills -a claude-code -a codex -a cursor -s github -s japanese -s turborepo -y` をリポジトリの直下で実行して入れる。導入はユーザーの許可を得てから行う。
   - https://raw.githubusercontent.com/philtzjp/skills/main/.agents/skills/japanese/SKILL.md を取得する。
3. 作業中のリポジトリに、このスキルの古い規約本文がコピーされて残っていたら、japanese スキルを優先する。そのうえで、古いコピーの削除をユーザーに提案する。

## 経緯

philtzjp/skills の japanese-writing を改良した japanese スキルを正本にしました。refresh-skills で同期している各リポジトリが壊れないように、このスキルは削除もリネームもせず、案内として残しています。
