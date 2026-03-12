---
name: fukugyo
description: 副業・フリーランスの業務管理を自動化するスキル。勤怠管理・契約書読み込み・請求書発行・入金確認・未払い時の督促〜少額訴訟まで一気通貫でサポートする。Claude Code専用。
---

# fukugyo — 副業管理スキル

## コマンド一覧

| コマンド | やること |
|---------|---------|
| `/fukugyo/fukugyo-setup` | 初回セットアップ（名前・口座・クライアント情報を登録） |
| `/fukugyo-timecard` | 今日の勤怠を記録する |
| `/fukugyo-timecard-month` | 今月の稼働をまとめる（請求書作成前に使う） |
| `/fukugyo-contract <ファイル>` | 契約書ファイルを読み込んでAIが解析する |
| `/fukugyo-contract-sync <クライアント名>` | 読み取った単価・支払条件を設定に反映する |
| `/fukugyo-invoice` | 先月分の請求書を発行する |
| `/fukugyo-payment` | 入金確認・督促メールを生成する |
| `/fukugyo-escalate <請求書ID>` | 未払い対応（内容証明・支払督促・少額訴訟） |

---

## 各コマンドの動作定義

### `/fukugyo-setup`
`python3 scripts/setup.py` を実行する。

### `/fukugyo-timecard`
`python3 scripts/timecard.py today` を実行する。
Slack MCP が利用可能な場合は、config.json の slack.channels に登録されたチャンネルから
当日の自分の投稿を取得し、FUKUGYO_SLACK_DATA 環境変数にセットしてから実行する。

### `/fukugyo-timecard-yesterday`
`python3 scripts/timecard.py yesterday` を実行する。

### `/fukugyo-timecard-month [YYYY-MM]`
`python3 scripts/timecard.py month [YYYY-MM]` を実行する。月の指定がなければ先月分。

### `/fukugyo-contract <ファイルパス>`
`python3 scripts/contract.py read <ファイルパス>` を実行する。
スクリプトが契約書テキストを表示したら、Claude Code がその内容を解析して
報酬・契約形態・リスク条項などを抽出し、
`python3 scripts/contract.py read <ファイルパス> --data '<JSON>'` で保存する。

### `/fukugyo-contract-list`
`python3 scripts/contract.py list` を実行する。

### `/fukugyo-contract-show <クライアント名>`
`python3 scripts/contract.py show <クライアント名>` を実行する。

### `/fukugyo-contract-sync <クライアント名>`
`python3 scripts/contract.py sync <クライアント名>` を実行する。

### `/fukugyo-invoice [YYYY-MM]`
`python3 scripts/invoice.py create [YYYY-MM]` を実行する。月の指定がなければ先月分。

### `/fukugyo-invoice-list`
`python3 scripts/invoice.py list` を実行する。

### `/fukugyo-payment`
`python3 scripts/payment.py check` を実行する。

### `/fukugyo-payment-paid <請求書ID>`
`python3 scripts/payment.py paid <請求書ID>` を実行する。

### `/fukugyo-escalate <請求書ID>`
`python3 scripts/escalate.py start <請求書ID>` を実行する。

### `/fukugyo-escalate-letter <請求書ID>`
`python3 scripts/escalate.py letter <請求書ID>` を実行する。

### `/fukugyo-escalate-tokusoku <請求書ID>`
`python3 scripts/escalate.py tokusoku <請求書ID>` を実行する。

### `/fukugyo-escalate-shogaku <請求書ID>`
`python3 scripts/escalate.py shogaku <請求書ID>` を実行する。

---

## データ保存先

すべてのデータはプロジェクトルートの `.fukugyo/` に保存される（GitHubには上がらない）：

```
.fukugyo/
├── config.json       # 設定（名前・口座・クライアント情報）
├── timecard.json     # 勤怠記録
├── invoices.json     # 請求書台帳
├── invoices/         # 請求書ファイル
├── contracts/        # 読み込んだ契約書の解析結果
└── escalate/         # 内容証明・申立書ファイル
```

## 各スキルの詳細

- `skills/timecard/SKILL.md`
- `skills/contract/SKILL.md`
- `skills/invoice/SKILL.md`
- `skills/payment/SKILL.md`
- `skills/escalate/SKILL.md`
