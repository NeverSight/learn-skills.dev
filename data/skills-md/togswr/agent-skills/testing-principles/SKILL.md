---
name: testing-principles
description: |
  テスト設計・レビュー・改善を、観測可能な振る舞いと決定性を軸に実行する。
  テスト戦略の再設計、フレーキー修正、テストダブル方針の整理、回帰防止強化が必要な依頼で使用する。
version: 2.0.0
---

# Testing Principles

観測可能な振る舞いを守りながら、回帰検知能力と保守性を高めるためのテスト支援スキル。

## 目的

- テストの品質判断を「動くか」ではなく「壊れ方が正しいか」で行う。
- 実装詳細への結合を減らし、リファクタリング耐性を上げる。
- 決定的なテストを増やし、フレーキーの再発を防ぐ。

## 適用条件

- テスト戦略を Unit / Integration / E2E のどこに置くべきか迷っている。
- 過度なモックや brittle test が増え、レビューで指摘が繰り返される。
- フレーキーが CI を不安定にしており、再発防止まで含めて整理したい。
- バグ修正時の回帰防止テストを、最小コストで追加したい。
- 外部 API やイベント連携をどこまで契約としてテストすべきか判断したい。
- フロントエンドテスト（UI/React/DOM/RTL/Playwright/Cypress）方針を決めたい。

## 標準ワークフロー

1. Scope
- 対象機能、失敗コスト、外部契約の有無を定義する。
- 期待する検知対象を「回帰」「仕様逸脱」「環境依存」に分解する。

2. Strategy
- リスクと変更頻度からテストサイズを決める。
- カバレッジ数値ではなく、未検知リスクで優先度を付ける。
- フロントエンド文脈を検出した場合は、設計前に必ず [Frontend Testing Principles (Kent C. Dodds)](references/07-frontend-testing-principles-kent-c-dodds.md) を参照する。

3. Design
- AAA を基準にテストを組み立て、1 テスト 1 Act を守る。
- Test Double は境界優先で選び、内部相互作用のモックを避ける。

4. Verify
- 再現テストを先に追加してから修正する。
- 決定性チェック（時刻、乱数、I/O、並列性）を必ず通す。

5. Improve
- フレーキーは「隔離 -> 根因修正 -> 再発防止」で処理する。
- 失敗を分類して、テスト設計か本番設計のどちらを直すべきか判定する。

## 成果物

- テスト戦略メモ（対象、サイズ、境界、非対象）
- 追加/修正テスト一覧（狙い、検知対象、依存制御）
- フレーキー対応記録（原因、恒久対策、監視ポイント）
- レビュー結果（重大順の指摘、修正提案、残リスク）

## 参照

- [Core Principles](references/01-core-principles.md)
- [Strategy And Test Sizing](references/02-strategy-and-test-sizing.md)
- [Test Doubles And Boundaries](references/03-test-doubles-and-boundaries.md)
- [Determinism And Flaky Control](references/04-determinism-and-flaky-control.md)
- [Anti-patterns And Remediation](references/05-anti-patterns-and-remediation.md)
- [Source Map](references/06-source-map.md)
- [Frontend Testing Principles (Kent C. Dodds)](references/07-frontend-testing-principles-kent-c-dodds.md)
- [Review Checklist Template](templates/review-checklist.md)

## 検証

- `bash skill-creator/scripts/validate-skill.sh testing-principles`
- `bunx markdown-link-check testing-principles/SKILL.md`
- `find testing-principles -name "*.md" -exec bunx markdown-link-check {} \\;`
