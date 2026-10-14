---
name: typescript-monorepo
description: パッケージの追加、turbo.json、pnpm-workspace.yaml、tsconfig の編集、apps や packages の構成変更を行うときに参照する。このスキルは turborepo スキルに統合した。内容は turborepo スキルを使う。
---

# typescript-monorepo

このスキルは turborepo スキルに統合しました。ここには規約を書いていません。

## すること

1. turborepo スキルを読み、その規約に従う。
2. turborepo スキルが見つからなければ、次のどちらかで読む。
   - `DISABLE_TELEMETRY=1 pnpm dlx skills add philtzjp/skills -a claude-code -a codex -a cursor -s github -s japanese -s turborepo -y` をリポジトリの直下で実行して入れる。導入はユーザーの許可を得てから行う。
   - https://raw.githubusercontent.com/philtzjp/skills/main/.agents/skills/turborepo/SKILL.md を取得する。
3. 作業中のリポジトリに、このスキルの古い規約本文がコピーされて残っていたら、turborepo スキルを優先する。そのうえで、古いコピーの削除をユーザーに提案する。

## 経緯

philtzjp/skills の typescript-monorepo を改良した turborepo スキルを正本にしました。refresh-skills で同期している各リポジトリが壊れないように、このスキルは削除もリネームもせず、案内として残しています。
