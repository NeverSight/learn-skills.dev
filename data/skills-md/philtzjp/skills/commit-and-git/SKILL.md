---
name: commit-and-git
description: コミット、プッシュ、ブランチ作成や切り替え、マージ、リベース、gh pr merge など Git / GitHub の操作を行うときに参照する。このスキルは github スキルに統合した。内容は github スキルを使う。
---

# commit-and-git

このスキルは github スキルに統合しました。ここには規約を書いていません。

## すること

1. github スキルを読み、その規約に従う。
2. github スキルが見つからなければ、次のどちらかで読む。
   - `DISABLE_TELEMETRY=1 pnpm dlx skills add philtzjp/skills -a claude-code -a codex -a cursor -s github -s japanese -s turborepo -y` をリポジトリの直下で実行して入れる。導入はユーザーの許可を得てから行う。
   - https://raw.githubusercontent.com/philtzjp/skills/main/.agents/skills/github/SKILL.md を取得する。
3. 作業中のリポジトリに、このスキルの古い規約本文がコピーされて残っていたら、github スキルを優先する。そのうえで、古いコピーの削除をユーザーに提案する。

## 経緯

philtzjp/skills の commit-and-git を改良した github スキルを正本にしました。refresh-skills で同期している各リポジトリが壊れないように、このスキルは削除もリネームもせず、案内として残しています。
