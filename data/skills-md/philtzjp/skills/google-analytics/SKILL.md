---
name: google-analytics
description: Google Analytics の組み込み、同意管理（Consent Mode）、Cookie バナーまわりを実装・変更するときに参照する。このスキルは analytics スキルに統合した。内容は analytics スキルを使う。
---

# google-analytics

このスキルは analytics スキルに統合しました。ここには規約を書いていません。

## すること

1. analytics スキルを読み、その規約に従う。
2. analytics スキルが見つからなければ、次のどちらかで読む。
   - `DISABLE_TELEMETRY=1 pnpm dlx skills add philtzjp/skills -a claude-code -a codex -a cursor -s analytics -y` をリポジトリの直下で実行して入れる。導入はユーザーの許可を得てから行う。
   - https://raw.githubusercontent.com/philtzjp/skills/main/.agents/skills/analytics/SKILL.md を取得する。
3. 作業中のリポジトリに、このスキルの古い規約本文がコピーされて残っていたら、analytics スキルを優先する。そのうえで、古いコピーの削除をユーザーに提案する。

## 経緯

philtzjp/skills の google-analytics を改良した analytics スキルを正本にしました。refresh-skills で同期している各リポジトリが壊れないように、このスキルは削除もリネームもせず、案内として残しています。
