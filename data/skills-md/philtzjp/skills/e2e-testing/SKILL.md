---
name: e2e-testing
description: 新しいユーザー向け主要フロー、重要な UI 変更、既存フローの成功条件を変更したときに参照する。このスキルは e2etest スキルに統合した。内容は e2etest スキルを使う。
---

# e2e-testing

このスキルは e2etest スキルに統合しました。ここには規約を書いていません。

## すること

1. e2etest スキルを読み、その規約に従う。
2. e2etest スキルが見つからなければ、次のどちらかで読む。
   - `DISABLE_TELEMETRY=1 pnpm dlx skills add philtzjp/skills -a claude-code -a codex -a cursor -s e2etest -y` をリポジトリの直下で実行して入れる。導入はユーザーの許可を得てから行う。
   - https://raw.githubusercontent.com/philtzjp/skills/main/.agents/skills/e2etest/SKILL.md を取得する。
3. 作業中のリポジトリに、このスキルの古い規約本文がコピーされて残っていたら、e2etest スキルを優先する。そのうえで、古いコピーの削除をユーザーに提案する。

## 経緯

philtzjp/skills の e2e-testing を改良した e2etest スキルを正本にしました。refresh-skills で同期している各リポジトリが壊れないように、このスキルは削除もリネームもせず、案内として残しています。
