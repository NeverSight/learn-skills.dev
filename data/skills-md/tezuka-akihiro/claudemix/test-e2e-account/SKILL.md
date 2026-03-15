---
name: test-e2e-account
description: Execute E2E tests for the account service with proper server setup, test execution, and cleanup. Use when user requests account E2E testing, test execution, or running Playwright tests for account features.
allowed-tools: Bash, Read, KillShell, TaskOutput
---

# Account Service E2E Test Executor

AccountサービスのE2Eテストを環境構築からクリーンアップまで一気通貫で管理・実行するスキルです。

## When to Use

- ユーザーが「accountのE2Eテストを実行して」と指示した時
- 機能実装後の最終確認を行う時
- コミット前にデグレがないか確認する時
- 「/test-e2e-account」と指示された時

## 実行フロー概要

1. **環境準備** (`prompts/01-execute.md` Step 1-2)
   - 既存サーバーの停止と新規起動。
   - 安定稼働までの待機。
2. **テスト実行** (`prompts/01-execute.md` Step 3)
   - Playwright によるテストスイートの実行。
3. **結果報告と解析** (`prompts/01-execute.md` Step 4)
   - 成功/失敗のサマリー提示。
   - 失敗時は `docs/troubleshooting.md` に基づく分析。
4. **クリーンアップ**
   - サーバープロセスの終了。

---

## 運用上の注意

- サーバーの起動には時間がかかります。必ず十分な待機時間を設けてください。
- 失敗した場合は、闇雲に再実行せずトラブルシューティングガイドを参照して原因を切り分けてください。
- サーバーを立ち上げっぱなしにすると、他の作業でポート競合が発生するため、必ずクリーンアップを行ってください。
