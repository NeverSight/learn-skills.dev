---
name: data-migration
description: データベースの一括変換、スキーマ移行、既存レコードの修正など、データマイグレーションを実装・実行するときに参照する。このスキルは db スキルに統合した。内容は db スキルを使う。
---

# data-migration

このスキルは db スキルに統合しました。ここには規約を書いていません。

## すること

1. db スキルを読み、その規約に従う。
2. db スキルが見つからなければ、次のどちらかで読む。
   - `DISABLE_TELEMETRY=1 pnpm dlx skills add philtzjp/skills -a claude-code -a codex -a cursor -s db -y` をリポジトリの直下で実行して入れる。導入はユーザーの許可を得てから行う。
   - https://raw.githubusercontent.com/philtzjp/skills/main/.agents/skills/db/SKILL.md を取得する。
3. 作業中のリポジトリに、このスキルの古い規約本文がコピーされて残っていたら、db スキルを優先する。そのうえで、古いコピーの削除をユーザーに提案する。

## 経緯

philtzjp/skills の data-migration を改良した db スキルを正本にしました。refresh-skills で同期している各リポジトリが壊れないように、このスキルは削除もリネームもせず、案内として残しています。
