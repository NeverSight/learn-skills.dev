---
name: aiworkflow-requirements
description: |
  AIWorkflowOrchestratorの正本仕様を `references/` から検索・参照・更新するスキル。
  resource-map / quick-reference / topic-map / keywords を起点に、必要最小限の文書だけを段階的に読む。
  用途: 要件確認、設計/API/IPC契約確認、UI/状態管理/セキュリティ判断、task-workflow・lessons-learned・未タスク同期。
  特に safeInvoke timeout、settings bypass、skill lifecycle、global nav、Skill Center / Workspace / Agent / Skill Creator の導線再編を扱う。

  Anchors:
  • Specification-Driven Development / 適用: 正本仕様同期 / 目的: 実装-仕様整合の維持
  • Progressive Disclosure / 適用: resource-map起点読込 / 目的: 必要最小限参照で漏れ防止

  Trigger:
  仕様確認, 仕様更新, task-workflow同期, lessons-learned同期, UI仕様反映, API/IPC契約確認, セキュリティ要件確認, safeInvoke, timeout, settings bypass, skill lifecycle, Skill Center, Workspace, Agent, Skill Creator, navContract, GlobalNavStrip, MobileNavBar, SkillManagementPanel, line budget reform, spec splitting, family split, generated index sharding
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
---

# AIWorkflow Requirements Manager

## 概要

AIWorkflowOrchestratorプロジェクトの全仕様を管理するスキル。
**このスキルが仕様の正本**であり、references/配下のドキュメントを直接編集・参照する。

## クイックスタート

### 仕様を探す

```bash
# キーワード検索（推奨）
node scripts/search-spec.js "認証" -C 5

# または resource-map.md でタスク種別から逆引き
```

### 仕様を読む

1. **まず [resource-map.md](indexes/resource-map.md) を確認** - タスク種別と current canonical set を特定
2. 該当ファイルを `Read` ツールで参照
3. 今回差分の完全ファイル一覧、旧 ordinal filename から current semantic filename への対応、エレガンス監査が必要な場合は [workflow-aiworkflow-requirements-line-budget-reform-artifact-inventory.md](references/workflow-aiworkflow-requirements-line-budget-reform-artifact-inventory.md), [legacy-ordinal-family-register.md](references/legacy-ordinal-family-register.md), [spec-elegance-consistency-audit.md](references/spec-elegance-consistency-audit.md) を参照
4. 詳細行番号や完全ファイル一覧が必要な場合は [topic-map.md](indexes/topic-map.md) と `node scripts/list-specs.js --topics` を参照

### 仕様を作成・更新

1. `assets/` 配下の該当テンプレートを使用
2. `references/spec-guidelines.md` と `references/spec-splitting-guidelines.md` を見て、classification-first で更新する
3. 編集後は `node scripts/generate-index.js` を実行

## ワークフロー

```
                    ┌→ search-spec ────┐
user-request → ┼                       ┼→ read-reference → apply-to-task
                    └→ browse-index ───┘
                              ↓
                    (仕様変更が必要な場合)
                              ↓
              ┌→ create-spec ──────────┐
              ┼                         ┼→ update-index → validate-structure
              └→ update-spec ──────────┘
```

## Task仕様ナビ

| Task               | 責務           | 起動タイミング     | 入力         | 出力             |
| ------------------ | -------------- | ------------------ | ------------ | ---------------- |
| search-spec        | 仕様検索       | 仕様確認が必要な時 | キーワード   | ファイルパス一覧 |
| browse-index       | 全体像把握     | 構造理解が必要な時 | なし         | トピック構造     |
| read-reference     | 仕様参照       | 詳細確認が必要な時 | ファイルパス | 仕様内容         |
| create-spec        | 新規作成       | 新機能追加時       | 要件         | 新規仕様ファイル |
| update-spec        | 既存更新       | 仕様変更時         | 変更内容     | 更新済みファイル |
| update-index       | インデックス化 | 見出し変更後       | references/  | indexes/         |
| validate-structure | 構造検証       | 週次/リリース前    | 全体         | 検証レポート     |

## リソース参照

### 仕様ファイル一覧

See [indexes/resource-map.md](indexes/resource-map.md)（読み込み条件付き）

詳細セクション・行番号: [indexes/topic-map.md](indexes/topic-map.md)

| カテゴリ         | 主要ファイル                                                                                      |
| ---------------- | ------------------------------------------------------------------------------------------------- |
| 概要・品質       | overview.md, quality-requirements.md                                                              |
| アーキテクチャ   | **architecture-overview.md**, architecture-patterns.md, arch-\*.md                                |
| インターフェース | interfaces-agent-sdk.md, llm-\*.md, rag-search-\*.md                                              |
| API設計          | api-endpoints.md, api-ipc-\*.md                                                                   |
| データベース     | database-schema.md, database-implementation.md                                                    |
| UI/UX            | ui-ux-components.md, ui-ux-design-principles.md, ui-history-\*.md                                 |
| セキュリティ     | security-principles.md, security-electron-ipc.md, csrf-state-parameter.md, security-\*.md         |
| 技術スタック     | technology-core.md, technology-frontend.md, technology-desktop.md                                 |
| Claude Code      | claude-code-overview.md, claude-code-skills-\*.md                                                 |
| デプロイ・運用   | deployment.md, deployment-electron.md, environment-variables.md                                   |
| ガイドライン     | spec-guidelines.md, development-guidelines.md, architecture-implementation-patterns.md, rag-\*.md |

**注記**: 18-skills.md（Skill層仕様書）は `skill-creator` スキルで管理。

### scripts/

| スクリプト                  | 用途               | 使用例                                       |
| --------------------------- | ------------------ | -------------------------------------------- |
| `search-spec.js`            | キーワード検索     | `node scripts/search-spec.js "認証" -C 5`    |
| `list-specs.js`             | ファイル一覧       | `node scripts/list-specs.js --topics`        |
| `generate-index.js`         | インデックス再生成 | `node scripts/generate-index.js`             |
| `validate-structure.js`     | 構造検証           | `node scripts/validate-structure.js`         |
| `select-template.js`        | テンプレート選定   | `node scripts/select-template.js "IPC仕様"`  |
| `split-reference.js`        | 大規模ファイル分割 | `node scripts/split-reference.js <file>`     |
| `remove-heading-numbers.js` | 見出し番号削除     | `node scripts/remove-heading-numbers.js`     |
| `log_usage.js`              | 使用状況記録       | `node scripts/log_usage.js --result success` |

### agents/

| エージェント       | 用途         | 対応Task           | 主な機能                         |
| ------------------ | ------------ | ------------------ | -------------------------------- |
| [create-spec.md](agents/create-spec.md) | 新規仕様作成 | create-spec        | テンプレート対応、重複チェック   |
| [update-spec.md](agents/update-spec.md) | 既存仕様更新 | update-spec        | テンプレート準拠、分割ガイド     |
| [validate-spec.md](agents/validate-spec.md) | 仕様検証     | validate-structure | resource-map登録確認、サイズ検証 |

### indexes/

| ファイル             | 内容                                       | 用途                  |
| -------------------- | ------------------------------------------ | --------------------- |
| `quick-reference.md` | キー情報の即時アクセス（推奨・最初に読む） | パターン/型/IPC早見表 |
| `resource-map.md`    | リソースマップ（読み込み条件付き）         | タスク種別→ファイル   |
| `topic-map.md`       | トピック別マップ（セクション・行番号詳細） | セクション直接参照    |
| `keywords.json`      | キーワード索引（自動生成）                 | スクリプト検索用      |

> **Progressive Disclosure**: まずresource-map.mdでタスクに必要なファイルを特定し、必要なファイルのみを読み込む。

### templates/

新規仕様書作成時のテンプレート。`node scripts/select-template.js` で自動選定可能。

| ファイル                    | 用途                 | 対象カテゴリ     |
| --------------------------- | -------------------- | ---------------- |
| `spec-template.md`          | 汎用仕様テンプレート | 概要・品質       |
| `interfaces-template.md`    | インターフェース仕様 | インターフェース |
| `architecture-template.md`  | アーキテクチャ仕様   | アーキテクチャ   |
| `api-template.md`           | API設計              | API設計          |
| `ipc-channel-template.md`   | Electron IPC         | IPC通信          |
| `react-hook-template.md`    | React Hook           | カスタムフック   |
| `react-context-template.md` | React Context        | 状態管理         |
| `service-template.md`       | サービス層           | ビジネスロジック |
| `database-template.md`      | データベース仕様     | データベース     |
| `ui-ux-template.md`         | UI/UX仕様            | UI/UX            |
| `security-template.md`      | セキュリティ仕様     | セキュリティ     |
| `testing-template.md`       | テスト仕様           | テスト戦略       |

> **注記**: 詳細はtemplates/配下を直接参照。追加テンプレートが必要な場合は `agents/create-spec.md` を参照。

### references/（ガイドライン）

| ファイル                       | 内容                           |
| ------------------------------ | ------------------------------ |
| `spec-guidelines.md`           | 命名規則・記述ガイドライン     |
| `spec-splitting-guidelines.md` | 大規模ファイル分割ガイドライン |
### 連携スキル

| スキル                       | 用途                                                   |
| ---------------------------- | ------------------------------------------------------ |
| `task-specification-creator` | タスク仕様書作成、Phase 12での仕様更新ワークフロー管理 |

**Phase 12 仕様更新時**: `.claude/skills/task-specification-creator/references/spec-update-workflow.md` を参照

### 運用ファイル

| ファイル     | 用途                         |
| ------------ | ---------------------------- |
| `EVALS.json` | スキルレベル・メトリクス管理 |
| `LOGS.md`    | 使用履歴・フィードバック記録 |

## ベストプラクティス

### すべきこと

- キーワード検索で情報を素早く特定
- 編集後は `node scripts/generate-index.js` を実行
- 500行超過時は classification-first で parent / child / history / archive / discovery を同一 wave で分割

### 避けるべきこと

- references/以外に仕様情報を分散
- インデックス更新を忘れる
- 詳細ルールをSKILL.mdに追加（→ spec-guidelines.md へ）

**詳細ルール**: See [references/spec-guidelines.md](references/spec-guidelines.md)
## 変更履歴
> 古い履歴（v8.31.0以前）は [logs-archive-index.md](references/logs-archive-index.md) を参照してください。

| Version     | Date           | Changes                                                                                                                                                                           |
| ----------- | -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **9.01.94** | **2026-03-15** | **TASK-SKILL-LIFECYCLE-05 Phase 12 実績同期是正を反映**: `references/workflow-skill-lifecycle-created-skill-usage-journey.md` の Artifact Inventory を実体ファイル名へ全面更新し、苦戦箇所へ「Phase 12 本文と成果物乖離」を追加。`references/lessons-learned-current.md` へ苦戦箇所6と5ステップ解決手順を追記し、`phase-12-documentation` / `documentation-changelog` / `spec-update-summary` の同値同期ルールを固定 |
| **9.01.93** | **2026-03-15** | **TASK-SKILL-LIFECYCLE-05 インデックス同期**: `indexes/resource-map.md` クイックルックアップに「CTA制御マトリクス」導線を追加、変更履歴 v1.17.0 を登録。`indexes/quick-reference.md` に `CTA制御マトリクスパターン` セクション（11行）と型定義テーブルへ `CTAVisibility`/`CTAState` 行を追加 |
| **9.01.92** | **2026-03-14** | **TASK-SKILL-LIFECYCLE-04 system spec same-wave 同期を追加**: `workflow-skill-lifecycle-evaluation-scoring-gate.md` を新規作成し、実装内容・苦戦箇所・`current canonical set`・`artifact inventory`・legacy path 互換を統合。`indexes/resource-map.md` / `indexes/quick-reference.md` / `references/task-workflow.md` / `references/lessons-learned-current.md` / `references/legacy-ordinal-family-register.md` / `LOGS.md` を同一 wave で同期し、mirror parity（`.claude` 正本→`.agents`）を完了条件に固定 |
| **9.01.91** | **2026-03-14** | **TASK-SKILL-LIFECYCLE-04 完了同期**: ScoringGate型・evaluatePrompt追加・ScoreDeltaBadge実装 |
| **9.01.90** | **2026-03-14** | **TASK-IMP-AI-RUNTIME-AUTHMODE-UNIFICATION-001 の canonical set / legacy register 同期を追加**: `workflow-ai-runtime-authmode-unification.md` に `current canonical set` / `artifact inventory` / parent docs / 旧 filename 互換管理を追記し、`legacy-ordinal-family-register.md` の current alias row（`qa-checklist` -> `quality-assurance-checklist`）を同期。あわせて `task-workflow-backlog.md` / `lessons-learned-current.md` / `indexes/resource-map.md` / `indexes/quick-reference.md` へ `UT-AI-RUNTIME-TEST-SEPARATION-CRITERIA-001` 導線を同一 wave で反映 |
| **9.01.89** | **2026-03-12** | **TASK-IMP-TASK-SPECIFICATION-CREATOR-LINE-BUDGET-REFORM-001 を同期**: `claude-code-skills-structure.md` / `claude-code-skills-resources.md` / `claude-code-skills-process.md` / `task-workflow.md` / `lessons-learned.md` に、`SKILL.md` 入口特化、family file 分割、rolling `LOGS.md` + archive、`.claude` 正本 / `.agents` mirror、validator 順序の再利用ルールを追加 |
| **9.01.88** | **2026-03-12** | **TASK-IMP-LIGHT-THEME-CONTRAST-REGRESSION-GUARD-001 の未タスク formalize を反映**: `UT-IMP-PHASE11-CURRENT-BUILD-PREFLIGHT-BUNDLE-001` を `docs/30-workflows/unassigned-task/` に formalize し、`task-workflow.md` / `lessons-learned.md` / `ui-ux-feature-components.md` / `workflow-light-theme-contrast-regression-guard.md` へ導線を追加。completed workflow の Phase 12 outputs も 1 件 formalize 前提へ更新 |
| **9.01.87** | **2026-03-12** | **TASK-IMP-LIGHT-THEME-CONTRAST-REGRESSION-GUARD-001 の Phase 12 再確認を同期**: `task-workflow.md` に global `unassigned-task/` 監査値（current 0 / baseline 134）と legacy normalization task を追記し、`lessons-learned.md` に workflow baseline 64 と directory baseline 134 の分離、Task 5 の 3 skill 同値転記ルールを追加。Phase 12 root evidence と system spec の再突合手順を固定 |
| **9.01.86** | **2026-03-12** | **TASK-IMP-LIGHT-THEME-CONTRAST-REGRESSION-GUARD-001 の統合正本を追加**: `references/workflow-light-theme-contrast-regression-guard.md` を新規作成し、今回実装した audit / harness / static serve fallback / selector readiness / workflow sync と苦戦箇所を 1 ファイルへ集約。`indexes/resource-map.md` / `indexes/quick-reference.md` も同時更新し、同種課題の参照初動を短縮 |
| **9.01.85** | **2026-03-12** | **TASK-IMP-LIGHT-THEME-CONTRAST-REGRESSION-GUARD-001 を反映**: `task-workflow.md` / `lessons-learned.md` / `ui-ux-feature-components.md` に、light theme guard の current build static serve、selector-based capture、`current=0 / baseline=64` の二層判定、Apple UI/UX helper text review を同期。remediation task と guard task の routing 分離を再利用ルールへ追加 |
| **9.01.84** | **2026-03-12** | **TASK-FIX-LIGHT-THEME-SHARED-COLOR-MIGRATION-001 の `spec_created` 追補を同期**: `workflow-light-theme-global-remediation.md` / `ui-ux-design-system.md` / `task-workflow.md` / `lessons-learned.md` に current workflow `docs/30-workflows/light-theme-shared-color-migration/`、actual target inventory、verification-only lane、必要 system spec 抽出セット、Phase 1-3 gate を追加し、spec-only UI task の再利用導線を強化 |
| **9.01.83** | **2026-03-11** | **TASK-UI-04C follow-up の未タスク formalize を同期**: `UT-IMP-WORKSPACE-PREVIEW-SEARCH-RESILIENCE-GUARD-001` を `task-workflow.md` / `ui-ux-feature-components.md` / `ui-ux-search-panel.md` / `architecture-implementation-patterns.md` / `error-handling.md` / `lessons-learned.md` へ追加し、04C の fuzzy no-match、renderer timeout+retry、parse/transport 分離を次回 preview/search UI 向け共通ガードへ接続。workflow `outputs/phase-12` の Step 1-C も 0件→1件へ再同期 |
| **9.01.82** | **2026-03-11** | **TASK-UI-04C の cross-cutting system spec を補完**: `ui-ux-search-panel.md` / `ui-ux-design-system.md` / `architecture-implementation-patterns.md` / `error-handling.md` に Workspace 04C の quick file search dialog、modal token、renderer local timeout+retry、recoverable parse fallback を追記し、Phase 12 の planned wording 是正結果も workflow 側へ同期 |
| **9.01.81** | **2026-03-11** | **TASK-UI-04C-WORKSPACE-PREVIEW を同期**: `ui-ux-feature-components.md` / `ui-ux-components.md` / `arch-state-management.md` / `api-ipc-system.md` / `security-electron-ipc.md` / `ui-ux-navigation.md` / `task-workflow.md` / `lessons-learned.md` に 04C の preview / quick search、renderer timeout+retry、structured fallback、screenshot 11件、52 tests PASS を反映 |
| **9.01.80** | **2026-03-11** | **TASK-UI-04B-WORKSPACE-CHAT を同期**: `ui-ux-feature-components.md` / `arch-state-management.md` / `interfaces-llm.md` / `interfaces-chat-history.md` / `security-electron-ipc.md` / `task-workflow.md` / `lessons-learned.md` に Workspace Chat Panel 実装、stream race 対策、Phase 11 screenshot 8件、Phase 12 implementation-guide 再監査結果を反映 |
| **9.01.79** | **2026-03-11** | **TASK-FIX-LIGHT-THEME-TOKEN-FOUNDATION-001 の global light remediation を system spec へ昇格**: `references/workflow-light-theme-global-remediation.md` を新規作成し、white background / black text 基準、renderer-wide compatibility bridge、desktop shard 11 再現、completed workflow 側 screenshot 再取得を 1 ファイルへ集約。`ui-ux-design-system.md` / `task-workflow.md` / `lessons-learned.md` / `indexes/resource-map.md` も同一ターンで同期し、同種課題の参照初動を短縮 |
| **9.01.78** | **2026-03-11** | **TASK-FIX-LIGHT-THEME-TOKEN-FOUNDATION-001 の完了移管後同期を反映**: `ui-ux-design-system.md` / `task-workflow.md` / `lessons-learned.md` に light token foundation の完了記録、Phase 11 screenshot 5件、follow-up 2件の正本導線 `docs/30-workflows/completed-tasks/light-theme-token-foundation/unassigned-task/` を追記し、completed workflow 移管後も system spec の参照先がぶれない運用を明文化 |
| **9.01.77** | **2026-03-11** | **UT-IMP-APIKEY-CHAT-TRIPLE-SYNC-GUARD-001 完了移管を反映**: `docs/30-workflows/completed-tasks/api-key-chat-tool-integration-alignment/` と `docs/30-workflows/completed-tasks/task-imp-apikey-chat-triple-sync-guard-001.md` への移管を system spec 側で同期し、関連改善タスクの状態と参照先を completed 配置へ統一 |
| **9.01.76** | **2026-03-11** | **UT-IMP-APIKEY-CHAT-TRIPLE-SYNC-GUARD-001 を追加**: `TASK-FIX-APIKEY-CHAT-TOOL-INTEGRATION-001` の苦戦箇所を、`docs/30-workflows/unassigned-task/task-imp-apikey-chat-triple-sync-guard-001.md` として formalize。`task-workflow.md` / `lessons-learned.md` / `api-ipc-system.md` / `workflow-apikey-chat-tool-integration-alignment.md` に残課題導線を同期し、修正済み契約を次回の回帰 guard へ接続 |
| **9.01.75** | **2026-03-11** | **TASK-FIX-APIKEY-CHAT-TOOL-INTEGRATION-001 の Phase 12再確認運用を反映**: `task-workflow.md` に再確認追補（4検証 + screenshot再取得 + `current=0 / baseline=133` 二層判定）を追加し、`lessons-learned.md` に再確認時の苦戦箇所を追記。再監査時は「今回差分合否」と「legacy baseline 監視」を分離する運用を明文化 |
| **9.01.74** | **2026-03-11** | **TASK-FIX-APIKEY-CHAT-TOOL-INTEGRATION-001 の再利用導線を最適化**: `references/workflow-apikey-chat-tool-integration-alignment.md` を新規作成し、実装内容・苦戦箇所・5分解決カード・仕様書別責務分離を1ファイルへ集約。`indexes/resource-map.md` に bugfix 逆引きと workflow 一覧導線を追加して、同種課題の参照初動を短縮 |
| **9.01.73** | **2026-03-11** | **TASK-UI-07 由来の dual skill-root follow-up を同期**: `UT-IMP-PHASE12-DUAL-SKILL-ROOT-MIRROR-SYNC-GUARD-001` を `references/task-workflow.md` / `references/lessons-learned.md` / `references/ui-ux-feature-components.md` へ登録し、`.claude` canonical root / `.agents` mirror sync / `diff -qr` 検証を Phase 12 の再利用ルールとして固定 |
| **9.01.72** | **2026-03-11** | **TASK-UI-07 の UI カタログ正本を最適化**: `references/ui-ux-components.md` に `TASK-UI-07 実装完了記録` と `実装内容と苦戦箇所サマリー` を追加し、実装内容・検証値・harness screenshot・内部契約境界・dual-root mirror sync を UI カタログ正本へ集約 |
| **9.01.71** | **2026-03-11** | **TASK-UI-08-NOTIFICATION-CENTER 再監査追補を反映**: `ui-ux-components.md` / `ui-ux-navigation.md` / `ui-ux-portal-patterns.md` / `lessons-learned.md` まで同期範囲を拡張し、Phase 11 coverage validator drift と delete reveal screenshot を system spec 正本へ記録 |
| **9.01.70** | **2026-03-11** | **TASK-UI-08-NOTIFICATION-CENTER を同期**: `api-endpoints.md` / `api-ipc-system.md` / `ui-ux-feature-components.md` / `arch-state-management.md` / `security-electron-ipc.md` / `task-workflow.md` に 058e の `お知らせ` UI、Portal、`notification:delete`、dedupe、Phase 11 screenshot 7件を同期し、topic-map / keywords 再生成を実施 |
| **9.01.72** | **2026-03-11** | **TASK-SKILL-LIFECYCLE-01 の feature spec 形成を再最適化**: `references/ui-ux-feature-components.md` の lifecycle 追補を `実装内容（要点）` / `苦戦箇所（再利用形式）` / `同種課題の5分解決カード` の3ブロックへ再編し、`task-workflow.md` / `lessons-learned.md` / `ui-ux-navigation.md` と同粒度で再利用可能な system spec へ整理 |
| **9.01.71** | **2026-03-11** | **TASK-SKILL-LIFECYCLE-01 Phase 12 準拠再確認を同期**: `references/task-workflow.md` に `phase12-task-spec-compliance-check.md` と `verify-all-specs=13/13` / `verify-unassigned-links=213/213` / `audit current=0 baseline=133` を追加し、`references/lessons-learned.md` へ 0件報告でも legacy backlog を隠さないルールを追記。`references/ui-ux-navigation.md` には surface ownership board / TC-11-05 要素証跡 / 苦戦箇所 / 5分解決カードを追加 |
| **9.01.70** | **2026-03-11** | **TASK-SKILL-LIFECYCLE-01 再監査同期**: `references/ui-ux-feature-components.md` に `SkillCenterView` の surface ownership board と TC-11-05 要素 capture を追加し、`references/task-workflow.md` / `references/lessons-learned.md` に representative screenshot は selector-based element capture を優先する再利用ルールを追記。`.claude` / `.agents` mirror 同期と search/validate 再確認の前提も整備 |
| **9.01.69** | **2026-03-10** | **TASK-UI-06-HISTORY-SEARCH-VIEW の system spec 形成を最適化**: `references/ui-history-search-view.md` に `実装内容（要点）` を追加し、変更範囲・契約要点・視覚検証・完了根拠を明文化。`references/ui-ux-feature-components.md` では TASK-UI-06 節を 5分解決カード付きのテンプレート準拠構成へ整理し、`references/lessons-learned.md` の解決手順を 5 ステップへ統一 |
| **9.01.68** | **2026-03-10** | **TASK-UI-06-HISTORY-SEARCH-VIEW Phase 12 再監査同期**: `references/ui-history-search-view.md` を新規作成し、timeline UI / state / IPC / screenshot / 苦戦箇所を統合。`ui-ux-feature-components.md` / `arch-state-management.md` / `api-ipc-system.md` / `task-workflow.md` / `lessons-learned.md` に 058c と未タスク `UT-IMP-SKILL-ROOT-CANONICAL-SYNC-GUARD-001` を同期 |
| **9.01.67** | **2026-03-10** | **TASK-UI-03 workflow を completed-tasks へ移管**: `docs/30-workflows/completed-tasks/task-ui-03-agent-view-enhancement/` を正本導線に切り替え、関連未タスク `UT-UI-03-LIGHT-SECONDARY-TEXT-CONTRAST-001` も親 workflow 配下 `unassigned-task/` へ移動。`ui-ux-feature-components.md` と Phase 12 検出レポートの path を同期 |
| **9.01.66** | **2026-03-10** | **UT-UI-03-LIGHT-SECONDARY-TEXT-CONTRAST-001 の未タスク仕様書を強化**: task-spec 準拠で `3.6 実装課題と解決策` を追加し、component/token 切り分け、dedicated harness 前提、`audit --diff-from HEAD --target-file` による品質判定を記録。あわせて `task-workflow.md` と `ui-ux-design-system.md` に教訓継承を反映 |
| **9.01.65** | **2026-03-10** | **TASK-UI-03 の system spec 記述先を最適化**: `ui-ux-components.md` に実装完了記録と苦戦サマリー、`ui-ux-feature-components.md` に 5分解決カード、`arch-ui-components.md` に adapter helper / dedicated harness / 専用型境界の苦戦箇所を追加し、実装内容と再利用知見の参照起点を明確化 |
| **9.01.64** | **2026-03-10** | **TASK-UI-03 Phase 12再監査の最終整合**: `task-workflow.md` に current workflow の完了追随（`UT-UI-03-TYPE-ASSERTION-001` 完了化、`UT-UI-03-LIGHT-SECONDARY-TEXT-CONTRAST-001` 新規登録）を反映。`lessons-learned.md` に backlog 継続前の現物確認ルールを追加し、`ui-ux-design-system.md` / `ui-ux-feature-components.md` へ token scope の改善タスク導線を同期 |
| **9.01.63** | **2026-03-10** | **TASK-UI-03 current workflow 同期**: `ui-ux-components.md` / `ui-ux-feature-components.md` / `arch-ui-components.md` の TASK-UI-03 節を current workflow 導線・実測 136 tests・`types.ts` / dedicated harness 実装へ更新し、`lessons-learned.md` に Phase 11 harness 化と light theme review scope 切り分けの教訓を追加 |
| **9.01.62** | **2026-03-10** | **TASK-FIX-SAFEINVOKE-TIMEOUT-001 Phase 12追補**: safeInvoke timeout の再監査で得た教訓を `lessons-learned.md` / `security-electron-ipc.md` へ追記し、`clearTimeout` cleanup 実装・rollout scope 再確認・Fake Timer 検証手順を正本へ同期 |
| **9.01.61** | **2026-03-10** | **TASK-FIX-SAFEINVOKE-TIMEOUT-001 Phase 1-12 実装完了**: Preload `invokeWithTimeout()` 契約、`IPC_TIMEOUT_MS = 5000`、allowlist fail-fast、`clearTimeout` cleanup、Phase 11 screenshot 4件、preload 19 files / 551 tests PASS を system spec 正本へ反映 |
| **9.01.60** | **2026-03-10** | **UT-IMP-WORKSPACE-PHASE11-CURRENT-BUILD-CAPTURE-GUARD-001 を同期**: `task-workflow.md` / `ui-ux-feature-components.md` / `lessons-learned.md` に、Workspace UI の current build source pinning と visual checklist 共通化を active 未タスクとして追加。workflow `unassigned-task-detection.md` の 0件判定も 1件へ是正し、04A の苦戦箇所から active backlog へ直接たどれるようにした |
| **9.01.59** | **2026-03-10** | **TASK-UI-04A-WORKSPACE-LAYOUT 再監査同期**: `ui-ux-feature-components.md` / `arch-state-management.md` / `ui-ux-navigation.md` / `security-electron-ipc.md` / `api-ipc-system.md` / `task-workflow.md` / `lessons-learned.md` に Workspace layout 04A の UI・state・IPC・教訓を同期。`generate-index.js` により topic-map/keywords も再生成 |
| **9.01.58** | **2026-03-10** | **TASK-FIX-SAFEINVOKE-TIMEOUT-001 スキル改善同期**: Trigger キーワードに `safeInvoke` / `timeout` / `Promise.race` / `ハング防止` / `Preloadセキュリティ` を追加。典型キーワードにも同キーワードを追記し、IPC タイムアウトパターンの仕様検索性を向上 |
| **9.01.57** | **2026-03-10** | **TASK-FIX-SAFEINVOKE-TIMEOUT-001 完了同期**: `security-electron-ipc.md` に Preload timeout + `clearTimeout` cleanup 契約と完了タスクを追加。`architecture-implementation-patterns.md` に S33 を追加し、`task-workflow.md` / `lessons-learned.md` / `ui-ux-feature-components.md` に screenshot 4件と未タスク `UT-IMP-AUTH-TIMEOUT-FALLBACK-LIGHT-CONTRAST-GUARD-001` を同期 |
| **9.01.56** | **2026-03-10** | **TASK-FIX-AUTHGUARD-TIMEOUT-SETTINGS-BYPASS-001 再監査追補を同期**: `architecture-auth-security.md` / `arch-state-management.md` / `ui-ux-navigation.md` / `ui-ux-feature-components.md` に `settings` reset 除外と screenshot 4件を追記。`task-workflow.md` / `lessons-learned.md` / LOGS.md 2件も実績ベースへ同期 |
| **9.01.55** | **2026-03-09** | **TASK-FIX-AUTHGUARD-TIMEOUT-SETTINGS-BYPASS-001 完了同期**: `architecture-auth-security.md` に認証状態遷移 "timed-out" 追加・Settings bypass セキュリティ記録。`arch-state-management.md` に AUTH_TIMEOUT_MS タイムアウト機構記録。`ui-ux-navigation.md` に Settings の AuthGuard 外アクセス記録。LOGS.md 2ファイル + SKILL.md 2ファイル同時更新（P1/P25対策） |
| **9.01.54** | **2026-03-09** | **TASK-FIX-AGENT-EXECUTE-SKILL-CONCURRENCY-GUARD-001 再監査の苦戦箇所を system spec へ固定**: `arch-state-management.md` に ChatPanel の現行 selector 実装と、CLI drift / Router 二重化 / workflow 本文 stale の短縮手順を追記。`lessons-learned.md` に未タスク9セクション逸脱・Router 二重化・4ステップ解決手順を追加し、未タスク `UT-FIX-CANCEL-SKILL-CONCURRENCY-GUARD-001` をテンプレート準拠へ再構成 |
| **9.01.54** | **2026-03-09** | **TASK-FIX-APP-DEBUG-LOCALSTORAGE-CLEAR-001 Phase 12 再同期**: Phase 11 screenshot 3件と metadata 検証、`UT-FIX-DEBUG-CLEAR-STORAGE-SHIM-CLEANUP-001` の formalization、`arch-state-management` / `development-guidelines` / `lessons-learned` / `task-workflow` / `phase-11-12-guide` の再利用ルール追記を反映 |
| **9.01.53** | **2026-03-09** | **TASK-FIX-AGENT-EXECUTE-SKILL-CONCURRENCY-GUARD-001 再監査追補**: workflow12 の Phase 11 screenshot 証跡と Phase 12 実装ガイドを実績ベースへ是正し、`task-workflow.md` の workflow12 判定を PASS へ更新。`validate-phase-output --phase` ドリフトを system spec / template 群で是正し、残未タスクを `UT-FIX-CANCEL-SKILL-CONCURRENCY-GUARD-001` の 1 件へ整理 |
| **9.01.52** | **2026-03-09** | **TASK-FIX-AGENT-EXECUTE-SKILL-CONCURRENCY-GUARD-001 完了同期**: `arch-state-management.md` に executeSkill 並行実行ガードパターン（二重防御: Store層 + UI層）を追記。LOGS.md 2ファイル + SKILL.md 2ファイル同時更新（P1/P25対策）。未タスク2件検出 |
| **9.01.51** | **2026-03-08** | **TASK-FIX-IPC-HANDLER-GRACEFUL-DEGRADATION-001 苦戦箇所追補**: lessons-learned に S-GD-1〜S-GD-4、security-electron-ipc に SEC-GD-1〜SEC-GD-3、api-ipc-system と architecture-implementation-patterns S31 に実装パターン詳細を追記 |
| **9.01.50** | **2026-03-08** | **TASK-FIX-IPC-HANDLER-GRACEFUL-DEGRADATION-001 仕様同期**: `api-ipc-system.md` に Graceful Degradation 実装状況と完了タスクを追加、`architecture-implementation-patterns.md` に S31 パターン追加、`security-electron-ipc.md` に戻り値契約追記、`task-workflow.md` に完了タスク追加。LOGS.md 2ファイル + SKILL.md 2ファイル同時更新（P1/P25対策） |
| **9.01.49** | **2026-03-08** | **TASK-FIX-SUPABASE-FALLBACK-PROFILE-AVATAR-001 の Phase 12実績と教訓を system spec へ固定**: `references/api-ipc-auth.md` に fallback 契約の実装要点 / 苦戦箇所 / 5分解決カードを追加。`references/architecture-auth-security.md` / `references/security-electron-ipc.md` に再発条件付きの苦戦箇所を追記し、`references/lessons-learned.md` に 3件の教訓と4ステップ手順を追加 |
| **9.01.48** | **2026-03-08** | **TASK-FIX-SUPABASE-FALLBACK-PROFILE-AVATAR-001 完了同期**: `api-ipc-auth.md` に Profile/Avatar fallback ハンドラ完了タスクと変更履歴 v1.7.0 を追加。`error-handling.md` に変更履歴 v1.10.0 を追加。LOGS.md 2ファイル + SKILL.md 2ファイル同時更新（P1/P25対策） |
| **9.01.47** | **2026-03-08** | **TASK-10A-F Phase 12タスク仕様再確認を反映**: `references/task-workflow.md` に current workflow の Phase 12準拠、canonical backlog 3件の指定ディレクトリ配置、repo-wide legacy baseline の別管理（`baselineViolations=110`）を追記。`references/lessons-learned.md` には comparison baseline 正規化と未タスク current/baseline 二層報告の苦戦箇所を追加し、system spec から再利用できるようにした |
| **9.01.46** | **2026-03-08** | **TASK-10A-F final sync を反映**: `store-driven-lifecycle-ui` の re-audit を current workflow だけで閉じず、comparison baseline の completed workflow も `phase-7-coverage-check.md` / `phase-11-manual-test.md` / `artifacts.json` まで正規化して validator PASS に揃える運用を追加。あわせて screenshot harness の待機条件は UI 実文言または `data-testid` を正本とするルールを `task-workflow.md` / `lessons-learned.md` / `LOGS.md` に同期 |
| **9.01.45** | **2026-03-08** | **TASK-10A-F current workflow 再監査の仕様同期を追補**: `store-driven-lifecycle-ui` の Phase 11/12 実体を current workflow 正本として再同期し、`task-workflow.md` / `lessons-learned.md` / `LOGS.md` との整合を再固定。あわせて `spec_created` workflow でも Phase 11/12 artifacts を completed として台帳同期する方針と、Progressive Disclosure に基づく必要仕様抽出マトリクスを反映 |
| **9.01.44** | **2026-03-08** | **TASK-10A-E-D/TASK-UI-03/TASK-10A-F 仕様同期**: 5教訓（worktreeエラー・コンポーネント分割テスト戦略・Store統合テスト設計・P31回帰テスト・lintパス不整合）・5パターン（コンポーネント分割テスト戦略・P31回帰テスト・Store統合テスト分離・worktree環境プロトコル・品質ゲート先行）・5完了タスク・5未タスクを6並列SubAgentで仕様書正本へ同期。LOGS.md 2ファイル + SKILL.md 2ファイル同時更新（P1/P25対策） |
| **9.01.43** | **2026-03-08** | **Phase 12 再確認結果を system spec へ同期**: `references/task-workflow.md` に workflow 07/10/11/12 の branch横断判定テーブル（`verify-all-specs` / `validate-phase-output --phase 12` / `validate-phase12-implementation-guide`）を追記し、`references/lessons-learned.md` に再確認の苦戦箇所（構造PASSでもPhase 12不足を見落とす / baselineノイズ誤読）と4ステップ解決手順を追加 |
| **9.01.42** | **2026-03-07** | **TASK-10A-F の Phase 12再確認を同期**: `references/task-workflow.md` に完了台帳と検証証跡（Phase 11 screenshot 11件）を追加し、`references/ui-ux-feature-components.md` に Store-Driven Lifecycle Integration を新規収録。`references/arch-state-management.md` へ TASK-10A-D/E-C/F の責務境界を追記し、direct IPC 排除の仕様を固定 |
| **9.01.42** | **2026-03-08** | **branch横断 Phase 12 再監査 + persist iterable hardening 仕様同期を完了**: `arch-state-management.md` に persist 復旧契約（DD-01〜DD-03）追記、`lessons-learned.md` にコード例と関連Pitfall参照追加、`task-workflow.md` に完了タスクと5分解決カード追記、`skill-creator/references/patterns.md` に persist 3段ガード + branch横断監査パターン追加。4仕様書を5並列SubAgentで同時更新 |
| **9.01.41** | **2026-03-07** | **TASK-10A-E-C の実装知見をシステム仕様へ資産化**: `architecture-implementation-patterns.md` に S18 useShallow派生selectorパターンを追加し、`.filter()` が毎回新参照を返す問題と解決策を体系化。`lessons-learned.md` に苦戦箇所3件（P31派生/worktree rollup/差分分析）と5分解決カードを追記。`06-known-pitfalls.md` に P48（useShallow未適用による無限ループ）を追加 |
| **9.01.40** | **2026-03-06** | **TASK-10A-E-C の Phase 12準拠再確認を同期**: `documentation-changelog.md` の「仕様策定のみ」残置を是正し、実更新ログへ統一。`references/arch-state-management.md` と `references/lessons-learned.md` に実装時の苦戦箇所（`useShallow` 派生、Phase 12同期漏れ、未タスクフォーマット逸脱）と5分解決カードを追記。未タスク2件をテンプレート準拠へ更新し `docs/30-workflows/unassigned-task/` 配下に正規配置した状態を反映 |
| **9.01.39** | **2026-03-06** | **TASK-10A-E-C の Phase 12再確認を同期**: `references/arch-state-management.md` に import lifecycle selector/action 契約（`useAvailableSkillsForImport` / `useFilteredAvailableSkills` / `useShallow`）を追記し、`references/task-workflow.md` に完了台帳と未タスク2件（UT-10A-E-C-001/002）を登録。Phase 11 は `TC-01..08` の実画面証跡を取得し `manual-test-result.md` を証跡列付きへ更新 |
| **9.01.38** | **2026-03-06** | **TASK-FIX-AUTH-MODE-CONTRACT-ALIGNMENT-001 の completed-tasks 移管を同期**: workflow本体を `docs/30-workflows/completed-tasks/03-TASK-FIX-AUTH-MODE-CONTRACT-ALIGNMENT-001/` へ移動し、関連未タスク2件を同workflow配下 `unassigned-task/` へ移管。`references/task-workflow.md` / `references/lessons-learned.md` / `references/interfaces-auth.md` / `references/api-ipc-system.md` / Phase 12成果物の参照パスを新配置へ更新 |
| **9.01.37** | **2026-03-06** | **auth-mode 由来の domain spec 同期ブロック残課題を仕様同期**: `docs/30-workflows/completed-tasks/03-TASK-FIX-AUTH-MODE-CONTRACT-ALIGNMENT-001/unassigned-task/task-imp-phase12-domain-spec-sync-block-validator-001.md` を追加し、`references/task-workflow.md` / `references/lessons-learned.md` / `references/interfaces-auth.md` / `references/api-ipc-system.md` に関連未タスクと苦戦箇所を反映。Phase 12 で更新対象 domain spec の3ブロック存在検証を次の改善導線として明文化 |
| **9.01.36** | **2026-03-06** | **TASK-FIX-AUTH-MODE-CONTRACT-ALIGNMENT-001 の system spec 記述粒度を最適化**: `references/interfaces-auth.md` / `references/api-ipc-system.md` / `references/task-workflow.md` に auth-mode の `実装内容` だけでなく `苦戦箇所` と `同種課題の5分解決カード` を追加し、domain spec 単体でも再利用可能な記録形式へ整理                                                                                                                                                              |
| **9.01.35** | **2026-03-06** | **TASK-FIX-AUTH-MODE-CONTRACT-ALIGNMENT-001 の Phase 12準拠再確認を反映**: `references/task-workflow.md` と `references/lessons-learned.md` に `phase12-task-spec-compliance-check.md`、cross-cutting doc 同期、`verify-unassigned-links` 105/105、`audit --diff-from HEAD` current=0 baseline=93 を追記。あわせて改善バックログ `UT-IMP-PHASE12-UNASSIGNED-LINK-DIAGNOSTICS-001` を `docs/30-workflows/unassigned-task/` に登録し、未タスク導線まで system spec に同期             |
| **9.01.34** | **2026-03-06** | **TASK-FIX-AUTH-MODE-CONTRACT-ALIGNMENT-001 再監査の横断導線補強を反映**: `references/ipc-contract-checklist.md` に shared transport DTO 正本化 / `IPCResponse<T>` / event payload / quick-reference 同期の確認項目を追加し、`indexes/quick-reference.md` に `auth-mode:get/set/status/validate/changed` と `AuthModeStatus` / `IPCResponse<T>` 早見表を追記。再監査で見落としやすい cross-cutting doc 更新を標準化                                                                 |
| **9.01.33** | **2026-03-06** | **TASK-043B 由来の skill import 契約横展開UTを同期**: `references/task-workflow.md` / `references/ui-ux-feature-components.md` / `references/lessons-learned.md` に `UT-IMP-SKILL-IMPORT-RESULT-CONTRACT-GUARD-001` を追加し、`importSkill` の post-condition 成功判定と error surface 一元化を他導線へ横展開する改善導線を正本へ登録                                                                                                                                               |
| **9.01.32** | **2026-03-06** | **TASK-043B の再利用導線を UI 機能仕様へ追補**: `references/ui-ux-feature-components.md` に同種課題の簡潔解決手順を追加し、`phase12-task-spec-compliance-check.md` による root evidence 集約と `current=0 / baseline backlog` 分離運用を UI 機能仕様側からも辿れるようにした                                                                                                                                                                                                        |
| **9.01.60** | **2026-03-10** | **TASK-UI-03 再監査で current workflow 完了台帳と UI review パターンを補完**: `references/task-workflow.md` に current workflow の再監査記録と検証証跡を追加し、`references/architecture-implementation-patterns.md` に dedicated harness + review scope 分離パターン（S34）を追記。併せて `.claude/task-specification-creator` と current workflow の script path ドリフト是正を system spec 側ログへ同期 |
| **9.01.31** | **2026-03-06** | **legacy 未タスク正規化課題の分離を同期**: `references/task-workflow.md` に `UT-IMP-UNASSIGNED-TASK-LEGACY-NORMALIZATION-001` を追加し、TASK-043B の未タスク判定を `current=0` と `baseline backlog` の二層管理へ更新。`references/lessons-learned.md` にも同ルールを反映し、未タスク監査の誤読を防ぐ運用を標準化                                                                                                                                                                   |
| **9.01.30** | **2026-03-06** | **TASK-043B の Phase 12準拠再確認を同期**: `references/task-workflow.md` / `references/ui-ux-feature-components.md` / `references/lessons-learned.md` に `phase12-task-spec-compliance-check.md`、未タスク配置監査 PASS、Phase 12根拠分散の苦戦箇所を追記。再利用時は「準拠根拠を1ファイルに集約する」運用を標準化                                                                                                                                                                  |
| **9.01.29** | **2026-03-06** | **TASK-043B 再監査の状態契約と参照導線を補強**: `references/arch-state-management.md` に non-throw action failure / post-condition success / dialog error surface 一元化 / `useAppStore.getState()` モック契約を追加。併せて `references/task-workflow.md` / `references/lessons-learned.md` に親仕様ブリッジ欠落と dialog test copy drift の教訓を追記                                                                                                                             |
| **9.01.38** | **2026-03-07** | **TASK-UI-03 スキルフィードバック改善を反映**: `references/spec-guidelines.md` に「完了タスクセクション標準化」ガイドラインを追加し、全仕様書の完了記録フォーマット（メタ情報テーブル + テスト結果サマリー + 成果物テーブル）を統一                                                                                                                                                                                                                                                 |
| **9.01.37** | **2026-03-07** | **TASK-UI-03-AGENT-VIEW-ENHANCEMENT Phase 12 完了を反映**: `task-workflow.md` に未タスク4件（UT-UI-03-A11Y-RADIOGROUP-001 / A11Y-DIALOG-001 / A11Y-LABEL-001 / TYPE-ASSERTION-001）を登録。`ui-ux-feature-components.md` に AgentView リデザイン完了記録を追加。LOGS.md 2ファイル + SKILL.md 2ファイル同時更新（P1/P25/P29対策）                                                                                                                                                    |
| **9.01.36** | **2026-03-06** | **UT-IMP-AIWORKFLOW-SKILL-ENTRYPOINT-COVERAGE-GUARD-001 を反映**: `references/task-workflow.md` と `references/lessons-learned.md` に、`aiworkflow-requirements` の warning 145件を「大規模 reference スキルの入口設計課題」として切り出した未タスクを追加。`SKILL.md` には `SKILL.md` / `quick-reference` / `resource-map` の三層入口を validator 整合とセットで管理する運用ルールを追記                                                                                           |
| **9.01.35** | **2026-03-06** | **UT-TASK-10A-B-008 の追補を skill-creator 導線改善まで同期**: `references/task-workflow.md` と `references/lessons-learned.md` に、repo 内 `skill-creator/SKILL.md` の直接参照導線再編と `quick_validate` warning 26→0 解消を反映。reference 追加時は `resource-map` と `SKILL.md` の両方を同時更新する標準ルールを追加                                                                                                                                                            |
| **9.01.34** | **2026-03-06** | **UT-TASK-10A-B-008 の Phase 12 Task 1 再確認を同期**: `references/task-workflow.md` と `references/lessons-learned.md` に、実装ガイドの内容不足是正と `validate-phase12-implementation-guide.js` 追加を反映。Phase 12 完了判定を「成果物存在 + 内容 validator PASS」まで引き上げた                                                                                                                                                                                                 |
| **9.01.33** | **2026-03-06** | **UT-TASK-10A-B-008 再監査追補を同期**: `references/task-workflow.md` / `references/ui-ux-feature-components.md` / `references/lessons-learned.md` に、明示的な screenshot 要求で発見した `useSkillAnalysis` の StrictMode ローディング固着修正と 8ケースの画面再検証を追記。`references/ui-ux-components.md` にも再監査追補を反映し、関連未タスク台帳の active/completed 分離ルールをベストプラクティスへ格上げ                                                                    |
| **9.01.30** | **2026-03-06** | **TASK-UI-02 派生未タスクの system spec 同期を反映**: `UT-IMP-PHASE12-UI-DOMAIN-SPEC-SYNC-GUARD-001` と `UT-IMP-PHASE12-WORKFLOW-BODY-STALE-GUARD-001` を `task-workflow.md` / `lessons-learned.md` / `ui-ux-feature-components.md` / `ui-ux-navigation.md` へ同一ターンで登録し、Global Navigation 改修の苦戦箇所から未タスク仕様書へ直接たどれる導線を固定                                                                                                                        |
| **9.01.29** | **2026-03-06** | **TASK-UI-02 再監査の正本導線を強化**: `SKILL.md` に再監査で優先参照すべき正本8件（navigation/components/feature-components/arch/task/lessons/directory）を直リンクで追加し、`generate-index.js` / `validate-structure.js` の実行例を canonical path へ統一。Global Navigation 再監査で発見したリンクドリフト・古い `AppDock` 前提表現の是正導線を明確化                                                                                                                            |

| **9.01.28** | **2026-03-06** | **TASK-FIX-SKILL-EXECUTOR-AUTHKEY-DI-001 の教訓同期を強化**: `references/task-workflow.md` に完了タスク専用セクション（SubAgent分担/実装反映/検証証跡/苦戦箇所）を追加し、`references/lessons-learned.md` に同タスクの実装内容 + 再発条件付き苦戦箇所を新設。Phase 12完了判定を「成果物実体 + 機械検証 + `phase-12-documentation.md` ステータス同期」の3点セットで固定 |
| **9.01.27** | **2026-03-05** | **TASK-FIX-SKILL-EXECUTOR-AUTHKEY-DI-001 の Phase 12準拠再確認を同期**: `phase-12-documentation.md` の `pending` 残置を `completed` へ是正し、Task 12-1〜12-5成果物実在 + `verify-all-specs` + `validate-phase-output` の3点突合を完了条件として固定。`task-workflow.md` / `lessons-learned.md` に苦戦箇所（台帳ドリフト）と再利用手順を追記 |
| **9.01.26** | **2026-03-05** | **TASK-FIX-SKILL-EXECUTOR-AUTHKEY-DI-001 再監査を同期**: 仕様書と実装のDIシグネチャ差分を再点検し、`interfaces-agent-sdk-executor.md` / `arch-electron-services.md` / `interfaces-agent-sdk-skill.md` / `lessons-learned.md` の `registerSkillHandlers(..., authKeyService)` と `new SkillExecutor(mainWindow, undefined, authKeyService)` を現行実装へ統一。追加でPhase 11画面回帰スクリーンショット3件を取得し、workflow証跡へ反映 |
| **9.01.25** | **2026-03-05** | **TASK-FIX-SKILL-EXECUTOR-AUTHKEY-DI-001 の仕様同期を反映**: `interfaces-agent-sdk-executor.md` に AuthKeyService DI配線契約（単一生成 + Skill/Auth同一注入）と完了タスクを追加し、`api-ipc-system.md` の auth-key 実装状況/関連タスク/完了タスクを更新。Step 2 判定は「新規I/F追加なし」で記録 |
| **9.01.21** | **2026-03-05** | **TASK-UI-01-C の Phase 12準拠再確認を同期**: `task-workflow.md` に `1.67.16` を追加し、`validate-phase-output --phase 12` / screenshot再撮影 / 未タスク差分監査（`current=0`, `baseline=92`）を固定。`lessons-learned.md` に `1.29.25` を追加し、`pnpm run test:run --` で全体テストへ展開される苦戦箇所と回避ルール（`pnpm exec vitest run` 明示指定）を追記 |
| **9.01.20** | **2026-03-05** | **TASK-UI-01-C 再監査追補を同期**: `task-workflow.md` に `1.67.15` を追加し、`artifacts.json` 完了状態と `index/phase` 文面ドリフト（pending残置）を是正する運用を固定。`lessons-learned.md` へ Phase 11 灰色スクリーンショット再発条件（初期化リロード競合）と preflight（`debug-clear-storage` / `dev-skip-auth`）を追記し、`SCREENSHOT + NON_VISUAL` 併用の証跡設計を標準化 |
| **9.01.24** | **2026-03-05** | **Phase 12完了条件を満たした成果物を completed-tasks へ移管**: `outputs/phase-12` 実体と `phase-12-documentation.md` completed を満たした `01-TASK-FIX-AUTH-KEY-HANDLER-REGISTRATION-001` を `docs/30-workflows/completed-tasks/` へ移動し、併せて `UT-IMP-DESKTOP-TESTRUN-SIGTERM-FALLBACK-GUARD-001` を `completed-tasks/unassigned-task/` へ移管。`task-workflow.md` の関連タスク/残課題を完了化し、参照パスを同期 |
| **9.01.23** | **2026-03-05** | **UT-IMP-DESKTOP-TESTRUN-SIGTERM-FALLBACK-GUARD-001 を同期**: `docs/30-workflows/unassigned-task/` に `apps/desktop test:run` の `SIGTERM` フォールバック未タスクを追加し、`task-workflow.md` 残課題/関連タスク、`lessons-learned.md` 関連未タスク、`api-ipc-system.md` 関連未タスクの3仕様書へ同一IDを反映 |
| **9.01.22** | **2026-03-05** | **TASK-FIX-AUTH-KEY-HANDLER-REGISTRATION-001 を運用最適化**: `task-workflow.md` / `api-ipc-system.md` / `lessons-learned.md` に `apps/desktop test:run` の `SIGTERM` 中断を苦戦箇所として追補し、長時間fixtureテストの分割実行ガードと「同種課題の5分解決カード（runtime配線 + テスト中断ガード）」を3仕様書で同期 |
| **9.01.21** | **2026-03-05** | **TASK-FIX-AUTH-KEY-HANDLER-REGISTRATION-001 の苦戦箇所同期を追補**: `lessons-learned.md` に当該タスク専用の苦戦箇所（runtime register漏れ / unregister非対称 / 教訓同期漏れ）と4ステップ手順を追加。`task-workflow.md` と `api-ipc-system.md` にも再発防止テーブルを追記し、実装内容と教訓を同一ターンで固定 |
| **9.01.20** | **2026-03-05** | **TASK-FIX-AUTH-KEY-HANDLER-REGISTRATION-001 再監査（画面証跡同期）を反映**: `task-workflow.md` の同タスク記録を「実装+テスト+画面回帰検証」へ更新し、Phase 11 のスクリーンショット3件（TC-11-UI-01〜03）と `validate-phase11-screenshot-coverage` PASS（3/3）を検証証跡へ追加。SubAgent-C責務を視覚監査ベースへ是正 |
| **9.01.19** | **2026-03-05** | **Phase 12 再監査の workflowパス正規化ガードを同期**: `task-workflow.md` に関連未タスク `UT-IMP-PHASE12-WORKFLOW-PATH-CANONICALIZATION-001` を追加し、`lessons-learned.md` に workflow 実体パス取り違えの苦戦箇所（preflight: `test -d` + `rg --files`）を追記。Phase 12 の検証順序（実体確認→verify/validate→links/audit）を再利用手順として固定 |
| **9.01.18** | **2026-03-05** | **TASK-UI-01-A-STORE-SLICE-BASELINE の Phase 12準拠再確認を同期**: `task-workflow.md` に再監査結果（Phase 12準拠PASS、実装差分未タスク0件）と関連未タスク `UT-IMP-PHASE12-UNASSIGNED-BASELINE-REDUCTION-001` を追補。`lessons-learned.md` に `audit --target-file` 適用境界と `current/baseline` 分離判定の苦戦箇所・再利用手順を追加 |
| **9.01.17** | **2026-03-05** | **TASK-UI-01-A-STORE-SLICE-BASELINE 再監査を同期**: `arch-state-management.md` に Store baseline 契約（型定義/16行 inventory/境界マトリクス/セレクタ規約）を追加し、`task-workflow.md` に完了台帳と Phase 11 TC証跡（TC-11-01〜03）を記録。`lessons-learned.md` に再発防止手順（TC-ID必須化、件数ドリフト防止、Step 2判定基準）を追記 |
| **9.01.16** | **2026-03-05** | **UT-TASK-10A-B-009 未タスク起票を同期**: `docs/30-workflows/unassigned-task/task-10a-b-completed-ut-placement-policy-guard.md` を追加し、`task-workflow.md` / `ui-ux-feature-components.md` / `lessons-learned.md` に同IDを反映。完了済みUT配置の3分類ルールと `target-file` 監査境界の誤用防止を再利用可能なガードとして標準化 |
| **9.01.15** | **2026-03-05** | **UT-TASK-10A-B-001 の再利用最適化を同期**: `task-workflow.md` / `ui-ux-feature-components.md` / `ui-ux-components.md` / `lessons-learned.md` にクイック解決カード（配置判定、`target-file` 適用境界、画面証跡5/5、`current/baseline` 分離）を追補し、同種UI課題を短手順で再現可能化 |
| **9.01.14** | **2026-03-05** | **UT-TASK-10A-B-001 最終再監査（未タスク配置是正）を同期**: 完了済み `task-10a-b-autofixable-filter-button.md` を `docs/30-workflows/completed-tasks/` 直下へ移管し、未実施 `UT-TASK-10A-B-002〜008` の7件を `docs/30-workflows/unassigned-task/` へ再配置。`task-workflow.md` / `ui-ux-feature-components.md` / `ui-ux-components.md` / `lessons-learned.md` を同時更新し、スクリーンショット5件を 11:00 JST に再取得したうえで `verify-unassigned-links`（102/102）と `audit --diff-from HEAD`（current=0, baseline=90）を反映 |
| **9.01.13** | **2026-03-05** | **UT-TASK-10A-B-001 再監査追補を同期**: Phase 11 light証跡ドリフト（theme mock固定値）を `task-workflow.md` / `ui-ux-feature-components.md` / `ui-ux-components.md` / `lessons-learned.md` に反映。`capture-ut-task-10a-b-001-screenshots.mjs` の `prefers-color-scheme` 連動修正、再撮影時刻（10:28 JST）、`validate-phase11-screenshot-coverage` 5/5 PASS を追記 |
| **9.01.12** | **2026-03-05** | **UT-TASK-10A-B-001 完了同期**: `task-workflow.md` / `ui-ux-feature-components.md` / `ui-ux-components.md` / `lessons-learned.md` に自動修正可能フィルタボタン実装の完了記録を反映。残課題テーブル `UT-TASK-10A-B-001` を完了化し、未タスク管理件数を `4件+3件` へ再計算。参照先を `docs/30-workflows/completed-tasks/ut-task-10a-b-001-autofixable-filter-button/` に統一 |
| **9.01.11** | **2026-03-04** | **Phase 11 画面カバレッジマトリクス警告の未タスク化を同期**: `docs/30-workflows/unassigned-task/task-imp-phase11-screenshot-coverage-matrix-guard-001.md` を追加し、`task-workflow.md` 残課題テーブルへ `UT-IMP-PHASE11-SCREENSHOT-COVERAGE-MATRIX-GUARD-001` を登録。`lessons-learned.md` と `ui-ux-feature-components.md` に同苦戦箇所（matrix未記載 warning）と4ステップ再利用手順を反映 |
| **9.01.10** | **2026-03-04** | **UT workflow の Phase 11証跡正規化ルールを仕様同期**: `task-workflow.md` に `UT-IMP-PHASE12-SCREENSHOT-COMMAND-REGISTRATION-GUARD-001` 追補2を追加し、対象workflow配下 `outputs/phase-11/screenshots` の必須化と `NON_VISUAL:` 記法を明文化。`lessons-learned.md` と `ui-ux-feature-components.md` にも同苦戦箇所（別workflow参照による coverage validator fail）を反映し、再利用手順を4ステップで標準化 |
| **9.01.9** | **2026-03-04** | **workflow02 再確認で検出した Port 5174 競合課題を仕様同期**: `task-workflow.md` に `UT-IMP-PHASE12-SCREENSHOT-PORT-CONFLICT-GUARD-001` を残課題登録し、追補検証証跡へ `lsof` 事前検査結果を記録。`ui-ux-feature-components.md` の workflow02 苦戦箇所へ同課題を追加し、`lessons-learned.md` に再発条件付き教訓（ポート検査→再撮影→coverage→台帳同期）を追記 |
| **9.01.8** | **2026-03-04** | **UT-IMP-PHASE12-SCREENSHOT-COMMAND-REGISTRATION-GUARD-001 の完了状態を再同期**: `ui-ux-feature-components.md` の workflow02 関連未タスク表で同IDを完了表記（取り消し線 + 完了注記）へ更新し、`docs/30-workflows/completed-tasks/unassigned-task/task-imp-phase12-screenshot-command-registration-guard-001.md` と `docs/30-workflows/issues/issue-968.md` のステータス/チェックリストを完了状態へ整合 |
| **9.01.7** | **2026-03-04** | **未タスク仕様書（coverage include pathガード）の反映を同期**: `UT-IMP-SKILL-CENTER-HOTFIX-COVERAGE-INCLUDE-GUARD-001` を `docs/30-workflows/unassigned-task/` に追加した内容を `task-workflow.md`（追加未タスク + 残課題 + 変更履歴）と `lessons-learned.md`（関連未タスク + 変更履歴）へ同期し、苦戦箇所から未タスク化までの再利用導線を固定 |
| **9.01.6** | **2026-03-04** | **SkillCenter削除導線ホットフィックスの再計測値確定 + テンプレート追補**: `task-workflow.md` / `ui-ux-feature-components.md` / `lessons-learned.md` の hotfix 証跡を `3 files / 30 tests`, coverage `86.89/84.61/88.88` へ更新。あわせて Phase 12テンプレート最適化の記録へ未タスク配置先判定（未完了=`unassigned-task` / 完了移管=`completed-tasks/unassigned-task`）を追補し、仕様転記漏れを防止 |
| **9.01.5** | **2026-03-04** | **TASK-FIX-SKILL-CENTER-METADATA-DEFENSIVE-GUARD-001 第2回再確認を同期**: `task-workflow.md` / `lessons-learned.md` の再監査証跡を最新値（`verify-unassigned-links` 88/88, `audit --diff-from HEAD` baseline=94）へ更新。Phase 11 画面証跡時刻を 16:50 JST へ統一し、`UT-IMP-SKILL-CENTER-PREVIEW-BUILD-GUARD-001` の参照先を `completed-tasks/unassigned-task/` へ正規化 |
| **9.01.4** | **2026-03-04** | **SkillCenter削除導線ホットフィックスの最終同期**: `task-workflow.md` / `ui-ux-feature-components.md` / `lessons-learned.md` に不具合原因（削除確認ダイアログ未描画）と修正内容（`confirm/cancel/Escape` 導線）を固定。`vitest` 再計測結果（10 files / 132 tests, 対象coverage 86.89/84.61/88.88）を追記し、Phase 12成果物の数値整合を更新 |
| **9.01.3** | **2026-03-04** | **Phase 12テンプレート最適化の仕様同期を追加**: `task-workflow.md` / `lessons-learned.md` に今回実装内容（`skill-creator` の Phase 12テンプレートへ preview preflight + 失敗時未タスク化分岐を同期）と苦戦箇所（パターン集とテンプレート本体の同期漏れ）を追記。再利用手順（テンプレート同期版5ステップ）を追加し、同種課題の初動を短縮 |
| **9.01.2** | **2026-03-04** | **TASK-FIX-SKILL-CENTER-METADATA-DEFENSIVE-GUARD-001 再監査追補（preview preflight）**: `task-workflow.md` / `lessons-learned.md` に UI再撮影時の preview preflight 不足（`ERR_CONNECTION_REFUSED` / module resolve fail）を苦戦箇所として追加。未タスク `UT-IMP-SKILL-CENTER-PREVIEW-BUILD-GUARD-001` を `docs/30-workflows/unassigned-task/` へ登録し、再発防止導線を同期 |
| **9.01.1** | **2026-03-04** | **TASK-FIX-SKILL-CENTER-METADATA-DEFENSIVE-GUARD-001 再監査の最終整合**: `task-workflow.md` の workflow 導線を現行 `docs/30-workflows/03-...` へ再統一し、Phase 11 証跡（TC-01〜TC-04）と検証結果（13/13, 28項目, 4/4, 88/88）を再固定。`artifacts.json`/`outputs/artifacts.json` 同期と Phase 1〜12 `completed` 更新の運用を変更履歴に反映 |
| **9.01.0** | **2026-03-04** | **TASK-FIX-SKILL-IMPORT 3連続是正を最終同期**: `01/02/03`（imported state復元 / import冪等ガード / SkillCenter欠損メタデータ防御）を `api-ipc-agent.md` / `interfaces-agent-sdk-skill.md` / `arch-state-management.md` / `ui-ux-feature-components.md` / `task-workflow.md` / `lessons-learned.md` に反映。Phase 12 Task 5 要件として `LOGS.md` 2ファイル + `SKILL.md` 2ファイル同時更新を実施し、3workflow監査（13/13, 28項目, TC 4/4, current=0）を記録 |
| **9.00.9** | **2026-03-04** | **TASK-10A-D 苦戦箇所を未タスク仕様書へ分離**: `docs/30-workflows/unassigned-task/` に `UT-IMP-TASK10A-D-SUBAGENT-EXECUTION-LOG-GUARD-001`（仕様書別SubAgent実行ログ必須化）と `UT-IMP-TASK10A-D-SCREENSHOT-PURPOSE-DISAMBIGUATION-GUARD-001`（画面証跡の状態名+検証目的分離）を追加。`task-workflow.md` 残課題テーブル、`ui-ux-feature-components.md` 関連未タスク、`lessons-learned.md` 教訓を同期更新 |
| **9.00.8** | **2026-03-04** | **TASK-10A-D を仕様書別SubAgent運用へ最適化**: `task-workflow.md` / `ui-ux-feature-components.md` / `lessons-learned.md` に仕様書別SubAgent実行ログを追加し、実装内容と苦戦箇所の同時記録を標準化。`task-workflow.md` に SubAgent運用版5ステップ、`ui-ux-feature-components.md` に反映ログ、`lessons-learned.md` に実装サマリー + 分担表を追補 |
| **9.00.7** | **2026-03-04** | **TASK-10A-D 再確認結果を仕様へ追補**: `task-workflow.md` / `ui-ux-feature-components.md` / `lessons-learned.md` に再検証結果（13/13, 28項目, TC 5/5, current=0/baseline=85）を追加。`manual-test-result.md` の TC-02/TC-05 に証跡意図注記を追加し、画面証跡解釈の曖昧さを解消。`phase-12-documentation.md` の状態を完了へ同期 |
| **9.00.6** | **2026-03-03** | **TASK-10A-D 再監査追補**: `task-workflow.md` の UT-UI-05A 関連未タスクリンク3件を `completed-tasks/skill-editor-view-closure/unassigned-task/` へ是正。`verify-unassigned-links` を `ALL_LINKS_EXIST`（89/89）へ回復し、Phase 11 画面証跡5件の追加後に `validate-phase11-screenshot-coverage` PASS（5/5）を確認 |
| **9.00.5** | **2026-03-03** | **TASK-10A-D スキルライフサイクルUI統合 完了同期**: `ui-ux-components.md` / `ui-ux-feature-components.md` / `arch-ui-components.md` に完了記録を追加。`arch-state-management.md` に agentSlice拡張（`currentAnalysis`/`isAnalyzing`/`isImproving` + 5アクション + 8セレクタ）を記録。`interfaces-agent-sdk-skill.md` に型契約追記。`task-workflow.md` に完了セクションと苦戦箇所3件（Suggestion型不整合、P40再発、P11パターン）を記録。LOGS.md 2ファイル・SKILL.md 2ファイル同時更新 |
| **9.00.4** | **2026-03-03** | **TASK-10A-C 未タスク仕様書を追加**: `docs/30-workflows/unassigned-task/` に `UT-IMP-TASK10A-C-FIVE-SPEC-SYNC-GUARD-001` と `UT-IMP-TASK10A-C-PHASE11-SCREENSHOT-COVERAGE-GUARD-001` を新規作成。`task-workflow.md` 残課題テーブルと TASK-10A-C セクションへ同期し、`lessons-learned.md` に関連未タスク導線を追加 |
| **9.00.3** | **2026-03-03** | **TASK-10A-C 最終再確認を履歴化**: `task-workflow.md` / `api-ipc-agent.md` / `interfaces-agent-sdk-skill.md` / `security-electron-ipc.md` / `lessons-learned.md` の5仕様書に実装内容・苦戦箇所・簡潔解決手順が反映済みであることを再確認。`screenshot:skill-create-wizard` 再実行と `validate-phase11-screenshot-coverage` PASS（8/8）を確認し、SubAgent分離運用の証跡を固定 |
| **9.00.2** | **2026-03-02** | **TASK-10A-C SubAgent責務分離を仕様固定**: `task-workflow.md` に仕様書別SubAgent分担（api-ipc/interfaces/security/task/lessons）を追加。`api-ipc-agent.md` / `interfaces-agent-sdk-skill.md` / `security-electron-ipc.md` に TASK-10A-C の苦戦箇所と簡潔解決手順を追補し、`spec-update-summary.md` をテンプレート準拠（分担表 + 苦戦箇所）へ最適化 |
| **9.00.1** | **2026-03-02** | **TASK-10A-C 教訓追補**: `lessons-learned.md` に TASK-10A-C 専用セクションを追加し、苦戦箇所3件（UI再撮影後のTC紐付け検証漏れ、`skill:create` 契約4仕様書同期漏れ、Phase 11/12 依存成果物参照漏れ）と同種課題向け5ステップ手順を反映。再利用性向上のため `task-workflow.md` / `ui-ux-feature-components.md` と同一方針へ統一 |
| **9.00.0** | **2026-03-02** | **TASK-10A-C 再監査反映**: `task-workflow.md` に SkillCreateWizard 完了記録と検証証跡を追加。`api-ipc-agent.md` / `interfaces-agent-sdk-skill.md` / `security-electron-ipc.md` に `skill:create` 契約（引数 `description + options`、P42準拠検証、sender検証、エラーサニタイズ）を同期し、Phase 11/12 依存成果物参照漏れを是正 |
| **8.99.0** | **2026-03-02** | **TASK-10A-B 再監査（画面証跡ベース）を反映**: `ui-ux-components.md` / `ui-ux-feature-components.md` / `arch-ui-components.md` に SkillAnalysisView 完了記録を追加。`task-workflow.md` のテスト証跡を `74 tests PASS` へ更新し、`verify-all-specs` warning=0 / `validate-phase-output` PASS / `verify-unassigned-links` missing=0 を確認 |
| **8.98.0** | **2026-03-02** | **TASK-10A-B SkillAnalysisView 実装完了を反映**: Phase 1-12全完了（72テスト全PASS、カバレッジ Line100%/Branch95.83%/Function100%）。LOGS.md 2ファイル・SKILL.md 2ファイルを同時更新し、topic-map.md を再生成。`docs/30-workflows/completed-tasks/skill-analysis-view/outputs/phase-12/spec-update-summary.md` を更新 |
| **8.97.0** | **2026-03-02** | **UT-IMP-PHASE12-TWO-WORKFLOW-EVIDENCE-BUNDLE-001 を反映**: `docs/30-workflows/unassigned-task/task-imp-phase12-two-workflow-evidence-bundle-001.md` を新規作成し、`task-workflow.md` 残課題へ登録。`lessons-learned.md` に関連未タスク導線を追記し、2workflow同時監査（spec_created/completed）での証跡集約・Task 1/3/4/5 実体突合・UI画面証跡・`currentViolations=0` 判定固定を再利用可能化 |
| **8.96.0** | **2026-03-02** | **Phase 12準拠再確認（TASK-UI-05A/TASK-UI-05）を反映**: `task-workflow.md` に2workflow同時監査の検証証跡（`verify-all-specs`/`validate-phase-output`/必須成果物突合）と苦戦箇所（証跡分散、baseline/current誤読）を追記。`lessons-learned.md` に再利用4ステップを追加し、未タスク監査の合否基準を `currentViolations=0` 固定で明文化 |
| **8.95.0** | **2026-03-02** | **TASK-UI-05A 再監査（実装実体同期 + 未タスク正本化）**: `task-workflow.md` / `ui-ux-components.md` / `ui-ux-feature-components.md` の TASK-UI-05A 状態を「実装ファイル実在・統合未完了」へ是正。`docs/30-workflows/unassigned-task/` に未タスク正本3件を作成し、Phase 11再取得スクリーンショット（2026-03-02）と Phase 12 `spec-update-summary.md` / `artifacts.json` 同期を反映 |
| **8.94.0** | **2026-03-01** | **TASK-UI-05A 包括的監査・getFileTree仕様追加**: `api-ipc-agent.md` に `skill:getFileTree` チャネル仕様（FileNode型定義含む）を追加。`ui-ux-feature-components.md` SkillEditorView セクションに getFileTree 未実装注記を追記。LOGS.md 2ファイル・SKILL.md 2ファイルを同期更新 |
| **8.93.0** | **2026-03-01** | **TASK-UI-05A spec_created + 参照整合を反映**: `task-workflow.md` / `ui-ux-components.md` / `ui-ux-feature-components.md` に `TASK-UI-05A-SKILL-EDITOR-VIEW`（仕様書作成完了・実装未着手）を追加。Phase 11 画面検証証跡（Dashboard/Editorスクリーンショット、manual-test-result、discovered-issues）を同期し、`UT-IMP-PHASE12-SUBAGENT-NA-LOG-GUARD-001` と `UT-IMP-IPC-HANDLER-COVERAGE-GRANULAR-001` の参照パスを実体へ是正 |
| **8.97.0** | **2026-03-02** | **TASK-UI-05B 仕様書別SubAgent分割の最適化**: UIプロファイルを 1仕様書=1SubAgent の6責務へ再編し、`ui-ux-components.md` / `ui-ux-feature-components.md` / `arch-ui-components.md` / `arch-state-management.md` / `task-workflow.md` / `lessons-learned.md` に実装内容と苦戦箇所を同期。`task-workflow.md` の検証証跡日付を 2026-03-02 へ統一し、テンプレート再利用性を向上 |
| **8.96.0** | **2026-03-02** | **TASK-UI-05B Phase 12 再確認追補**: `task-workflow.md` の TASK-UI-05B 検証証跡を最新値（`verify-all-specs` warning=0、初回 warning=7 を是正 / `audit` current=0 baseline=75）へ同期。`ui-ux-feature-components.md` と `lessons-learned.md` に再発条件付きの苦戦箇所（Phase 12参照不足warning、画面証跡再撮影、current/baseline誤読）と簡潔解決手順を追加し、再利用可能な運用知見を固定 |
| **8.95.0** | **2026-03-02** | **TASK-UI-05B 実装完了再同期**: `spec_created` 残存を `completed` へ統一し、`ui-ux-components.md` / `ui-ux-feature-components.md` / `task-workflow.md` / `arch-*` / `quality-requirements.md` / `api-ipc-agent.md` / `interfaces-agent-sdk-skill.md` を実装実体へ再同期。Phase 11 画面証跡（TC-04〜TC-07）を追加し、`phase-12-documentation.md` の必須章不足を補正して `verify-all-specs` / `validate-phase-output` を PASS へ復帰 |
| **8.94.0** | **2026-03-01** | **TASK-UI-05B アーキテクチャ層仕様書追補**: 多角的検証（垂直思考・システム思考・改善思考）で検出した4仕様書の未反映を是正。`arch-ui-components.md` に4ビュー/33コンポーネント・状態管理方針・ファイル配置を追加。`arch-state-management.md` に4ビューの状態管理設計（useState + agentSlice個別セレクタ）を追加。`architecture-overview.md` の UI/UXアーキテクチャ・ディレクトリ構造にTASK-UI-05Bを追記。`quality-requirements.md` にパフォーマンス基準4項目と完了タスク（spec_created）を追加。P26（仕様書更新遅延）・P31（Phase 12更新漏れ）パターンの再発防止 |
| **8.93.0** | **2026-03-01** | **TASK-UI-05B spec_created 同期を反映**: `task-workflow.md` / `ui-ux-components.md` / `ui-ux-feature-components.md` に `TASK-UI-05B-SKILL-ADVANCED-VIEWS` の仕様書作成完了（spec_created）を追加。`verify-unassigned-links` で検出した未タスクリンク2件（`UT-IMP-PHASE12-SUBAGENT-NA-LOG-GUARD-001`, `UT-IMP-IPC-HANDLER-COVERAGE-GRANULAR-001`）を実在パスへ是正し、画面検証スクリーンショット導線を登録 |
| **8.92.0** | **2026-03-01** | **TASK-UI-05 completed-tasks 移管を反映**: `docs/30-workflows/completed-tasks/TASK-UI-05-SKILL-CENTER-VIEW/` へワークフロー本体を移動し、関連未タスク7件（`task-ui-05-*.md`）を同ディレクトリ配下 `unassigned-task/` へ移管。`task-workflow.md` / `ui-ux-components.md` / `ui-ux-feature-components.md` の参照先を新パスへ同期 |
| **8.91.0** | **2026-03-01** | **UT-UI-05-007 未タスク登録を反映**: `docs/30-workflows/completed-tasks/TASK-UI-05-SKILL-CENTER-VIEW/unassigned-task/task-ui-05-phase12-ui-spec-sync-guard.md` を新規作成し、`task-workflow.md` の TASK-UI-05節/残課題テーブルへ登録。`ui-ux-components.md` と `ui-ux-feature-components.md` の SkillCenterView 関連未タスク表へ同IDを同期し、UI仕様同期ガードの運用課題を追跡可能化 |
| **8.90.0** | **2026-03-01** | **TASK-UI-05 UI仕様書追補を反映**: `ui-ux-components.md` の SkillCenterView 関連未タスクを `UT-UI-05-001`〜`006` へ拡張し、`ui-ux-feature-components.md` に実装時の苦戦箇所（型境界、DetailPanel責務集中、Phase 12同期）と4ステップ簡潔解決手順を追加。`task-workflow.md` / `lessons-learned.md` の教訓記録と整合するよう仕様導線を統一 |
| **8.89.0** | **2026-03-01** | **TASK-UI-05 教訓同期を追補**: `task-workflow.md` の TASK-UI-05 セクションへ再発条件付きの苦戦箇所（CategoryId/SkillCategory型境界、DetailPanel責務集中、Phase 12三点同期）と5ステップ簡潔手順を追加。`lessons-learned.md` に同内容を転記し、未タスク運用（UT-UI-05-001〜006）と検証証跡の再利用導線を固定 |
| **8.88.0** | **2026-03-01** | **TASK-UI-05 仕様同期完了**: `ui-ux-components.md` / `ui-ux-feature-components.md` / `arch-ui-components.md` / `arch-state-management.md` / `task-workflow.md` に SkillCenterView 実装内容を反映。未タスク `UT-UI-05-001`〜`006` を `docs/30-workflows/unassigned-task/` に登録し、残課題テーブル・参照リンクを同期 |
| **8.84.2** | **2026-02-28** | **TASK-FIX-AUTH-CALLBACK-SERVER-WORKER-EXIT-001 完了移管反映**: ワークフローディレクトリを `docs/30-workflows/completed-tasks/TASK-FIX-AUTH-CALLBACK-SERVER-WORKER-EXIT-001/` へ移動し、派生未タスク `UT-IMP-AUTH-CALLBACK-LIFECYCLE-CONTRACT-GUARD-001` を `docs/30-workflows/completed-tasks/unassigned-task/` へ移管。`task-workflow.md` の残課題行を完了表記へ更新し、関連参照パスを completed-tasks 正本へ同期 |
| **8.84.1** | **2026-02-28** | **UT-IMP-AUTH-CALLBACK-LIFECYCLE-CONTRACT-GUARD-001 未タスク登録**: `docs/30-workflows/completed-tasks/unassigned-task/task-imp-auth-callback-lifecycle-contract-guard-001.md` を新規作成し、`TASK-FIX-AUTH-CALLBACK-SERVER-WORKER-EXIT-001` の苦戦箇所（wait/stop責務混在・stop冪等性・監査スクリプト所在誤認）を Section 3.5 へ転記。`task-workflow.md` 残課題テーブルと `security-implementation.md` 参照リンクを同期更新 |
| **8.84.0** | **2026-02-28** | **TASK-FIX-AUTH-CALLBACK-SERVER-WORKER-EXIT-001 テンプレート最適化追補**: `security-implementation.md` に再発条件付きの苦戦箇所と4ステップ手順を追加し、`task-workflow.md` の同タスク節へ「苦戦箇所と解決策（再利用用）」+「簡潔解決5ステップ」を追記。`outputs/phase-12/spec-update-summary.md` を `phase12-system-spec-retrospective-template` 準拠構造へ再編して SubAgent 分担・検証証跡を1ファイル固定化 |
| **8.83.0** | **2026-02-28** | **TASK-FIX-AUTH-CALLBACK-SERVER-WORKER-EXIT-001 仕様同期**: `security-implementation.md` のローカルHTTPサーバー停止契約を実装準拠（timeout時は自動停止しない/停止は呼び出し側責務）へ更新。`task-workflow.md` に完了記録と検証証跡を追加し、`lessons-learned.md` に wait/stop 責務分離の再発防止手順を追記 |
| **8.82.0** | **2026-02-27** | **TASK-9H 教訓同期を追補**: `lessons-learned.md` に TASK-9H 専用セクション（苦戦箇所3件 + 同種課題向け4ステップ）を追加。`phase-12-documentation.md` の実行状態同期を反映し、成果物実体と仕様台帳の不一致を解消 |
| **8.81.0** | **2026-02-27** | **TASK-9H Phase 12再監査の仕様同期を完了**: `api-ipc-agent.md` / `security-electron-ipc.md` / `interfaces-agent-sdk-skill.md` / `architecture-overview.md` / `task-workflow.md` を最終同期。`skillDebugHandlers` 起動配線、成果物4件（spec-update-summary / documentation-changelog / unassigned-task-detection / skill-feedback-report）と検証証跡（13/13, error=0, ALL_LINKS_EXIST, current=0）を固定 |
| **8.87.0** | **2026-02-28** | **TASK-9I completed-tasks 移管反映**: `docs/30-workflows/TASK-9I-skill-docs/` を `docs/30-workflows/completed-tasks/TASK-9I-skill-docs/` へ移動し、関連未タスク `UT-9I-001/002` を同ディレクトリ配下 `unassigned-task/` へ移管。`task-workflow.md` / `interfaces-agent-sdk-skill.md` / `lessons-learned.md` の参照先を新パスへ同期 |
| **8.86.0** | **2026-02-28** | **UT-IMP-PHASE12-EVIDENCE-LINK-GUARD-001 反映**: `task-workflow.md` の TASK-9I 再確認セクションに苦戦箇所（未タスクリンクのワイルドカード false fail、`current/baseline` 判定軸、証跡値ドリフト）を追記し、残課題テーブルへ新規未タスクを登録。`lessons-learned.md` に再利用用5ステップ手順を追加 |
| **8.85.0** | **2026-02-28** | **TASK-9I Phase 12記録最適化**: `task-workflow.md` の再確認テーブルを最新証跡へ同期（`verify-unassigned-links` 96/96, `audit --diff-from HEAD` 追記）。`lessons-learned.md` に「同種課題の即時実行コマンドセット」を追加し、target監査と差分監査を含む再利用手順を標準化 |
| **8.84.0** | **2026-02-28** | **TASK-9I Phase 12再確認の最終同期**: `task-workflow.md` に Phase 12再確認証跡（`verify-all-specs` / `validate-phase-output` / `verify-unassigned-links` / `quick_validate` / `audit --target-file`）を追記し、`UT-9I-001` / `UT-9I-002` の配置・フォーマット検証結果（`current=0`, baseline分離）を固定化。`lessons-learned.md` に苦戦箇所3件と4ステップ簡潔解決手順を追加し、同種課題の再利用手順を標準化 |
| **8.83.0** | **2026-02-28** | **TASK-9I 再監査反映**: `api-ipc-agent.md` / `arch-electron-services.md` / `security-electron-ipc.md` / `architecture-overview.md` / `interfaces-agent-sdk-skill.md` / `task-workflow.md` の必須6仕様書を実装準拠へ同期。`UT-9I-001` / `UT-9I-002` の未タスク指示書を `docs/30-workflows/unassigned-task/` に作成し、残課題テーブルと関連未タスクリンクを同期 |
| **8.84.3** | **2026-02-28** | **TASK-9J 完了移管反映**: `docs/30-workflows/TASK-9J-skill-analytics/` を `docs/30-workflows/completed-tasks/TASK-9J-skill-analytics/` へ移動。`UT-IMP-TASK9J-PHASE12-IPC-SYNC-AUTO-VERIFY-001` も `completed-tasks/unassigned-task/` へ移管し、関連仕様書の参照を更新 |
| **8.84.2** | **2026-02-28** | **TASK-9J 未タスク同期 + 台帳整合**: `task-imp-task9j-phase12-ipc-sync-auto-verify-001.md` を新規作成し、`task-workflow.md` 残課題テーブルと `interfaces-agent-sdk-skill.md` 関連未タスクへ同期。残課題テーブルの重複行（同一IDの完了/未完了混在）を是正 |
| **8.84.1** | **2026-02-28** | **TASK-9J 仕様同期テンプレート最適化**: `task-workflow.md` の TASK-9J セクションをテンプレート準拠へ再整形（メタ情報/仕様書別SubAgent分担/再発条件付き苦戦箇所/検証証跡）。`lessons-learned.md` に5仕様書同期マトリクスを追加し、`interfaces-agent-sdk-skill.md` / `api-ipc-agent.md` / `security-electron-ipc.md` へ実装時の苦戦箇所を追補 |
| **8.84.0** | **2026-02-28** | **TASK-9J Phase 12再確認追補**: `task-workflow.md` と `lessons-learned.md` に苦戦箇所（IPC登録漏れ・責務重複・Preload API命名ドリフト）を再発条件付きで追記。`verify-all-specs` / `validate-phase-output` / `verify-unassigned-links` / `audit --diff-from HEAD` による再確認証跡を同期 |
| **8.83.0** | **2026-02-28** | **TASK-9J完了**: スキル使用統計・分析機能のバックエンド実装。新規5 IPCチャンネル（skill:analytics:record/statistics/summary/trend/export）、SkillAnalytics/AnalyticsStoreサービス、共有型定義8インターフェース追加。テスト97件全PASS、カバレッジ全基準クリア |
| **8.82.0** | **2026-02-27** | **TASK-9G Step 1-E追補**: Phase 12で検出した UT-9G-001〜005 を `docs/30-workflows/unassigned-task/` に正式登録し、`task-workflow.md` 残課題テーブルと `interfaces-agent-sdk-skill.md` 関連未タスクへ同期。`outputs/phase-12/unassigned-task-detection.md` の3ステップ完了化、`spec-update-summary` / `documentation-changelog` への反映を実施 |
| **8.81.0** | **2026-02-27** | **TASK-9G Phase 12再監査反映**: `api-ipc-agent.md` / `arch-electron-services.md` / `security-electron-ipc.md` / `architecture-overview.md` / `interfaces-agent-sdk-skill.md` / `task-workflow.md` の必須6仕様書を実装準拠へ同期。`docs/30-workflows/completed-tasks/TASK-9G-skill-schedule/outputs/phase-7〜13` の不足成果物補完、`artifacts.json` 実装パス補正、ゴーストディレクトリ `{outputs` 削除を実施 |
| **8.80.0** | **2026-02-27** | **UT-IMP-PHASE12-SPEC-VERSION-CONSISTENCY-GUARD-001 登録**: `task-workflow.md` v1.61.7 に未タスク（Phase 12 仕様更新の版数・手順整合ガード）を追加。`spec-update-summary` と正本仕様の版数/手順ドリフト再発防止を運用課題として固定し、関連行の参照先整合（SubAgent同期ガード行の `unassigned-task/` 正本化）を実施 |
| **8.79.0** | **2026-02-27** | **UT-IMP-QUICK-VALIDATE-EMPTY-FIELD-GUARD-001 テンプレート最適化**: `outputs/phase-12/spec-update-summary.md` をテンプレート準拠で追加。`task-workflow.md` v1.61.6 に仕様書別SubAgent分担を追記し、苦戦テーブルを再発条件付き形式へ最適化。`lessons-learned.md` v1.26.3 を再発条件カラム付きへ整形し、同種課題の再利用性を強化 |
| **8.78.0** | **2026-02-27** | **UT-IMP-QUICK-VALIDATE-EMPTY-FIELD-GUARD-001 Phase 12再監査反映**: `task-workflow.md` に苦戦箇所3件（チェックリスト同期漏れ、親タスク旧参照残存、検証スクリプト所在誤認）と5ステップ簡潔解決手順を追記。`lessons-learned.md` v1.26.2 を追加し、同種課題の再利用導線を強化 |
| **8.77.0** | **2026-02-27** | **UT-IMP-QUICK-VALIDATE-EMPTY-FIELD-GUARD-001完了**: `quick_validate.js` name/description 検証にP42準拠3段バリデーション（typeof → 空文字列 → trim()）を適用。テスト21件追加、85テスト全PASS。`task-workflow.md` 完了台帳、`claude-code-skills-process.md` 検証規則、`spec-update-workflow.md` の既知課題分類を同期更新 |
| **8.77.0** | **2026-02-27** | **TASK-9F完了反映**: `api-ipc-agent.md` にスキル共有IPCチャネルセクション追加（3チャンネル、型定義10型、バリデーションルール）。`security-electron-ipc.md` にskillShareAPIセキュリティパターン追加。`interfaces-agent-sdk-skill.md` にスキル共有型定義セクション追加。`task-workflow.md` に完了タスク記録追加 |
| **8.76.0** | **2026-02-26** | **TASK-9B 再監査の知見固定化**: `task-workflow.md` に TASK-9B 完了記録（実装要点/苦戦箇所/検証証跡）を追加。`lessons-learned.md` に TASK-9B 教訓（13chドリフト、P42 create未完了、current/baseline混同）と5ステップ簡潔解決手順を追加。`interfaces-agent-sdk-skill.md` / `security-skill-ipc.md` に仕様書別SubAgent分担と再監査時の苦戦箇所を追記 |
| **8.75.0** | **2026-02-26** | **TASK-9B再監査反映（SkillCreator IPC拡張同期）**: `api-ipc-agent.md` / `interfaces-agent-sdk-skill.md` / `architecture-overview.md` / `arch-electron-services.md` / `security-skill-ipc.md` を実装準拠へ更新。SkillCreator契約を 13チャンネル（12 invoke + 1 progress）へ統一し、`task-workflow.md` の TASK-9B-H 参照を `completed-tasks/skill-creator-ipc/` に正規化 |
| **8.74.9** | **2026-02-26** | **TASK-9A Phase 12完了移管**: `docs/30-workflows/TASK-9A-skill-editor/` を `docs/30-workflows/completed-tasks/TASK-9A-skill-editor/` へ移動。`TASK-9A-C-004` を完了化し、`task-9a-c-phase12-spec-sync-guard.md` を `completed-tasks/unassigned-task/` へ移管。関連仕様書（task-workflow / ui-ux-feature-components / interfaces-agent-sdk-skill / ui-ux-components）の参照を同期更新 |
| **8.74.8** | **2026-02-26** | **TASK-9A-C-004 未タスク登録同期**: `docs/30-workflows/unassigned-task/task-9a-c-phase12-spec-sync-guard.md` を新規作成し、`task-workflow.md` / `ui-ux-feature-components.md` / `interfaces-agent-sdk-skill.md` の関連未タスクテーブルへ同時反映。Phase 12再確認で顕在化した4課題（Part 1/2要件漏れ、監査判定誤読、メタ情報重複、3仕様書同期漏れ）を再発防止タスクとして記録 |
| **8.74.7** | **2026-02-26** | **TASK-9A Phase 12再確認追補**: `task-workflow.md` に TASK-9A の苦戦箇所3件と4ステップ再利用手順を追記。`lessons-learned.md` に同タスク専用セクション（Part 1/2要件不足、`audit-unassigned-tasks --target-file` 誤読、未タスクメタ情報重複）を追加し、再発防止手順を標準化 |
| **8.74.6** | **2026-02-26** | **TASK-9A 完了同期**: `ui-ux-feature-components.md` / `ui-ux-components.md` / `interfaces-agent-sdk-skill.md` / `architecture-implementation-patterns.md` / `testing-component-patterns.md` を `completed` 状態へ更新し、`task-workflow.md` に TASK-9A 完了記録を追加。`TASK-9A-C-002` を完了化して `completed-tasks/unassigned-task/` へ移管 |
| **8.74.5** | **2026-02-26** | **UT-IMP-SKILL-VALIDATION-GATE-ALIGNMENT-001 完了同期**: `task-workflow.md` の完了移管リンク2件を `completed-tasks` 正本へ補正し、`verify-unassigned-links.js` の参照整合を回復。`lessons-learned.md` に検証経路統一運用（`quick_validate.js` 優先 + baseline/current 分離判定）の教訓を追記 |
| **8.74.4** | **2026-02-25** | **UT-IMP-PHASE12-SPEC-SYNC-SUBAGENT-GUARD-001 未タスク登録**: `docs/30-workflows/unassigned-task/task-imp-phase12-spec-sync-subagent-guard-001.md` を作成し、今回実装での苦戦箇所（4仕様書同期漏れ、current/baseline誤読、検証コマンド誤用）を Section 3.5 に記録。`task-workflow.md` 残課題と `interfaces-agent-sdk-skill.md` 検出未タスクを同期更新 |
| **8.74.3** | **2026-02-25** | **UT-FIX-SKILL-EXECUTE-INTERFACE-001 仕様同期を最適化**: `task-workflow.md` / `interfaces-agent-sdk-skill.md` / `security-skill-ipc.md` / `lessons-learned.md` に仕様書別SubAgent分担を追記し、実装内容・苦戦箇所・再利用手順を仕様書ごとに同期。`security-skill-ipc.md` に同タスク専用セクション（実装反映/苦戦箇所/4ステップ）を追加 |
| **8.74.2** | **2026-02-25** | **UT-FIX-SKILL-EXECUTE-INTERFACE-001 再確認追補**: `task-workflow.md` に Phase 12再実行証跡（`verify-all-specs` 13/13、`validate-phase-output` 28項目、`verify-unassigned-links` 91/91、`audit --diff-from HEAD` current=0/baseline=75）を追加。`lessons-learned.md` に監査解釈ミス（`--target-file`）と `validate-phase-output` 引数誤用の教訓を追記 |
| **8.74.1** | **2026-02-25** | **UT-FIX-SKILL-EXECUTE-INTERFACE-001 反映 + Phase 12参照整合是正**: `interfaces-agent-sdk-skill.md` / `security-skill-ipc.md` / `task-workflow.md` / `lessons-learned.md` に `skill:execute` 契約整合（`skillName` 正式 + `skillId` 後方互換）を反映。`task-workflow.md` の未タスク参照ドリフトを補正し、`UT-IMP-AIWORKFLOW-SPEC-REFERENCE-SYNC-001` を完了表記へ同期 |
| **8.72.6** | **2026-02-25** | **Phase 12完了移管反映（UT-IMP-UNASSIGNED-AUDIT-SCOPE-CONTROL-001）**: 実行ワークフローを `docs/30-workflows/completed-tasks/ut-imp-unassigned-audit-scope-control-001/` へ移動し、関連未タスク `UT-IMP-PHASE12-VALIDATION-COMMAND-STANDARDIZATION-001` も `completed-tasks/unassigned-task/` へ移管。`task-workflow.md` の残課題行を完了化 |
| **8.72.5** | **2026-02-25** | **UT-IMP-PHASE12-VALIDATION-COMMAND-STANDARDIZATION-001 登録反映**: `task-workflow.md` 残課題へ Phase 12 検証コマンド標準化タスクを追加。`quick_validate.js` 統一・`verify-all-specs --workflow` 必須化・`*-final.log` 運用を未タスク仕様として管理開始 |
| **8.72.4** | **2026-02-25** | **UT-IMP-UNASSIGNED-AUDIT-SCOPE-CONTROL-001 最終整合**: 旧 `quick_validate` 表記を `quick_validate.js` に統一。`task-workflow.md` / `lessons-learned.md` に再検証の必須条件（`--workflow` 指定）と最新証跡同期ルールを反映 |
| **8.72.3** | **2026-02-25** | **UT-IMP-UNASSIGNED-AUDIT-SCOPE-CONTROL-001 Phase 12再確認反映**: `task-workflow.md` に再確認履歴（v1.60.1）を追加。`lessons-learned.md` に証跡同期/quick_validate経路混同の苦戦箇所と4ステップ解決手順を追記。`architecture-implementation-patterns.md` に Phase 12 準拠確認チェーンを追加 |
| **8.72.2** | **2026-02-25** | **UT-IMP-UNASSIGNED-AUDIT-SCOPE-CONTROL-001 再監査反映**: `lessons-learned.md` に scope分離運用の苦戦箇所と5ステップ解決手順を追加。`architecture-implementation-patterns.md` に未タスク監査スコープ分離パターンを追加。完了済み未タスク指示書を `completed-tasks/unassigned-task/` へ移管し、`task-workflow.md` 参照を同期更新 |
| **8.72.1** | **2026-02-25** | **UT-IMP-UNASSIGNED-AUDIT-SCOPE-CONTROL-001 完了反映**: `task-workflow.md` の残課題行を完了化し、参照先を `docs/30-workflows/completed-tasks/ut-imp-unassigned-audit-scope-control-001/index.md` へ更新。未タスク監査の current/baseline 分離運用（`--target-file` / `--diff-from`）を完了タスクとして同期 |
| **8.71.0** | **2026-02-25** | **Phase 12完了済み成果物の移管反映**: `ut-skill-ipc-preload-extension-001` ワークフローを `completed-tasks/` へ移動し、対応未タスク `task-imp-ipc-preload-extension-spec-alignment-001.md` も `completed-tasks/unassigned-task/` へ移管。`task-workflow.md` の成果物・未タスク参照を新パスへ更新 |
| **8.70.0** | **2026-02-25** | **UT-IMP-IPC-PRELOAD-SPEC-SYNC-CI-GUARD-001未タスク登録**: `task-workflow.md` 残課題テーブルへ task-9D〜9J 仕様契約ドリフト自動検証CIガード（旧参照パス/artifacts/Date方針）を追加。親タスク `UT-IMP-IPC-PRELOAD-EXTENSION-SPEC-ALIGNMENT-001` の苦戦箇所3件を未タスク指示書 Section 3.5 に反映 |
| **8.69.0** | **2026-02-25** | **UT-IMP-IPC-PRELOAD-EXTENSION-SPEC-ALIGNMENT-001完了反映 + 再発防止スキル登録**: `task-workflow.md` に task-9D〜9J 仕様差分是正タスクの完了記録を追加し、残課題を完了化。`lessons-learned.md` に苦戦箇所3件と5ステップ解決手順を追加。`claude-code-skills-overview.md` に `ipc-preload-spec-sync-guardian` を登録 |
| **8.74.0** | **2026-02-25** | **UT-IMP-AIWORKFLOW-SPEC-REFERENCE-SYNC-001 未タスク登録反映**: `task-workflow.md` 残課題に Phase 12 仕様更新リンク同期ガード強化タスクを追加。苦戦箇所（baseline/current混同、完了移管後リンク漏れ、通常/fallback片側修正）を未タスク指示書へ標準記録する運用を明文化 |
| **8.73.0** | **2026-02-25** | **UT-IPC-AUTH-HANDLE-DUPLICATE-001 テンプレート最適化**: `api-ipc-auth.md` にクイック解決ガイド（目的/前提/実行ステップ/検証/トラブルシューティング）を追加。`lessons-learned.md` に20分版即時実行テンプレートを追加。`architecture-implementation-patterns.md` S22に再利用テンプレート（目的/場所/検証/落とし穴対処）を追加 |
| **8.72.0** | **2026-02-25** | **UT-IPC-AUTH-HANDLE-DUPLICATE-001 パターン追補**: `architecture-implementation-patterns.md` に S22（AUTH IPC登録一元化）を追加。`lessons-learned.md` に再監査時の苦戦箇所（baseline/current混同、完了移管後リンク同期）と4ステップ解決手順を追記 |
| **8.71.0** | **2026-02-25** | **UT-IPC-AUTH-HANDLE-DUPLICATE-001 再監査補完**: `ipc-contract-checklist.md` に AUTH登録一元化（通常/fallback同時監査）を追加。`api-ipc-auth.md` の実装箇所記載を行番号依存から関数依存へ更新。`lessons-learned.md` の参照先を completed-tasks へ正規化 |
| **8.70.0** | **2026-02-25** | **UT-IPC-AUTH-HANDLE-DUPLICATE-001完了反映**: `api-ipc-auth.md` にAUTH登録一元化戦略と完了記録を追加。`security-electron-ipc.md` にAUTH登録一元化パターンを追加。`task-workflow.md` の残課題行を完了化し completed 参照へ更新。`lessons-learned.md` に苦戦箇所と3ステップ再発防止手順を追記 |
| **8.69.0** | **2026-02-25** | **UT-IPC-CHANNEL-NAMING-AUDIT-001 完了反映と未タスク分離**: `task-workflow.md` に `spec_created` 完了記録を追加し、旧 unassigned 参照を completed 参照へ更新。`UT-IPC-AUTH-HANDLE-DUPLICATE-001` を未タスク登録。`architecture-implementation-patterns.md` に監査運用パターン、`lessons-learned.md` に再発防止手順を追加 |
| **8.71.0** | **2026-02-25** | **UT-FIX-SKILL-IPC-RESPONSE-CONSISTENCY-001 派生未タスク登録**: `docs/30-workflows/unassigned-task/` に未タスク2件（`UT-IMP-SKILL-IPC-RESPONSE-CONTRACT-GUARD-001`, `UT-IMP-PHASE12-IMPLEMENTATION-GUIDE-QUALITY-GATE-001`）を追加。`task-workflow.md` 残課題テーブルと `interfaces-agent-sdk-skill.md` 関連未タスクテーブルを同期更新 |
| **8.70.0** | **2026-02-25** | **UT-FIX-SKILL-IPC-RESPONSE-CONSISTENCY-001 Phase 12要件再適合**: `task-workflow.md` に本タスクの苦戦箇所と4ステップ簡潔解決手順を追記。`implementation-guide.md` を task-spec の Part 1/Part 2 必須要件（中学生向け例え話 + 型/API/エッジケース明記）へ再構成し、Phase 12完了チェックリストを実完了状態に同期 |
| **8.69.0** | **2026-02-25** | **UT-FIX-SKILL-IPC-RESPONSE-CONSISTENCY-001 Phase 12再監査整合**: `task-workflow.md` の残課題を完了化し、完了タスクセクションへ成果物6件を追記。`interfaces-agent-sdk-skill.md` の関連未タスク表を完了化し、`skill:remove` 戻り値記述を `Promise<RemoveResult>` に同期。`spec-update-summary.md` 追加と未タスクリンク整合（`verify-unassigned-links`）を反映 |
| **8.68.2** | **2026-02-24** | **未タスク監査スコープ分離タスク登録**: `UT-IMP-UNASSIGNED-AUDIT-SCOPE-CONTROL-001` を `task-workflow.md` 残課題テーブルへ追加。未タスク監査の対象差分判定（current）と全体ベースライン監視（baseline）を分離する運用改善タスクとして管理開始 |
| **8.68.1** | **2026-02-24** | **SKILL frontmatter制約準拠化**: `SKILL.md` の YAML `description` を1024文字以内に要約し、`quick_validate.js` で `Skill is valid!` を確認。仕様管理用途（要件/設計/API・IPC契約/テスト/未タスク/教訓反映）のトリガーは維持 |
| **8.68.0** | **2026-02-24** | **UT-IPC-DATA-FLOW-TYPE-GAPS-001 Phase 12再監査是正**: `task-workflow.md` の成果物テーブルに `spec-update-summary.md` を追加。`lessons-learned.md` v1.22.0 に苦戦箇所3件（成果物不足 / artifacts二重管理非同期 / 未タスク指示書フォーマット不一致）と4ステップ簡潔解決手順を追記。Phase 12運用の再発防止ルールを明文化 |
| **8.67.0** | **2026-02-24** | **UT-IPC-DATA-FLOW-TYPE-GAPS-001完了反映**: IPCデータフロー型ギャップ6件を7仕様書上で解消（仕様書修正のみ）。Gap 1: Date→ISO 8601（14フィールド/4ファイル）、Gap 2: DebugSession.status idle追加、Gap 3-6: onExport/ExportResult/safeOn/object形式統一。累計173検証項目ALL PASS。LOGS.md 2ファイル・SKILL.md 2ファイル更新 |
| **8.66.0** | **2026-02-24** | **UT-FIX-SKILL-VALIDATION-CONSISTENCY-001 実装パターン追加**: `architecture-implementation-patterns.md` にP42準拠バリデーション一括移行パターン（S18）追加。移行チェックリスト・引数形式別適用パターン・後方互換性注記・describe.eachマトリクステスト戦略を含む |
| **v8.65.0** | **2026-02-24** | **UT-SKILL-IMPORT-CHANNEL-CONFLICT-001 パターン文書化**: architecture-implementation-patterns.md に IPCチャネル名競合予防パターン新設（命名規則3パターン・チャネル対応表・判断基準・実装チェックリスト・苦戦箇所3件）。lessons-learned.md に技術的教訓3件追加（チャネル命名体系化・grepベース仕様書TDD・Phase4見積もり精度） |
| **8.65.0** | **2026-02-24** | **Phase 12再監査反映（TASK-UI-00-ATOMS / UT-SKILL-IMPORT-CHANNEL-CONFLICT-001）**: `task-workflow.md` に完了タスク2件を追記。`lessons-learned.md` v1.20.0 に苦戦箇所3件（完了台帳未反映、旧参照パス残存、`{outputs` ゴーストディレクトリ）と簡潔解決手順4ステップを追加。`task-ui-00-atoms` の旧参照を `tasks/completed-task/` 正本へ統一 |
| **8.65.0** | **2026-02-24** | **UT-FIX-SKILL-VALIDATION-CONSISTENCY-001 再監査整合**: `lessons-learned.md` に苦戦箇所3件と簡潔解決手順（4ステップ）を追加。`task-workflow.md` / `security-skill-ipc.md` の `UT-FIX-SKILL-VALIDATION-P42-001` を補完タスク実施済みとして完了同期し、重複管理を解消 |
| **8.64.2** | **2026-02-24** | **UT-FIX-TS-VITEST-TSCONFIG-PATHS-001 Phase 12追補**: `technology-devops.md` に本タスクの完了記録を追加し、`check-module-sync` 説明を4設定整合へ補正。`lessons-learned.md` v1.20.0 を追加（再監査の苦戦箇所3件 + 5ステップ簡潔解決手順） |
| **8.64.1** | **2026-02-24** | **UT-FIX-TS-VITEST-TSCONFIG-PATHS-001 再監査是正**: `architecture-monorepo.md` を実装実態（vite-tsconfig-paths運用）へ更新、`quality-requirements.md` の未タスク記載を完了化、`task-workflow.md` の完了行参照を `completed-tasks/task-vitest-tsconfig-paths-sync-automation.md` へ整合 |
| **8.64.0** | **2026-02-24** | **UT-SKILL-IMPORT-CHANNEL-CONFLICT-001完了反映**: skill:import IPCチャネル名競合の予防的解消（仕様書修正のみ）。task-022/task-030のチャネル名修正（skill:import→skill:importFromSource）。LOGS.md完了記録追加 |
| **8.64.0** | **2026-02-24** | **UT-FIX-SKILL-VALIDATION-CONSISTENCY-001完了反映**: skillHandlers.ts 6ハンドラP42準拠バリデーション統一。security-skill-ipc.md IPCチャネル検証テーブル更新、security-api-electron.md完了タスク追加、interfaces-agent-sdk-skill.md/task-workflow.md完了化。LOGS.md 2ファイル・SKILL.md 2ファイル更新 |
| **8.64.0.1** | **2026-02-24** | **UT-FIX-TS-VITEST-TSCONFIG-PATHS-001完了反映**: vite-tsconfig-pathsプラグイン導入で27個の手動alias削除、6つの双方向チェック+checkMapContainment汎用関数。60テスト全PASS。architecture-monorepo.md完了ステータス更新。LOGS.md完了記録追加 |
| **8.63.0** | **2026-02-23** | **TASK-UI-00-ATOMS 実装知見・苦戦箇所の仕様書体系化**: `ui-ux-atoms-patterns.md` v1.0.0 新規作成（7 Atoms実装パターン・苦戦箇所6件・テスト戦略）。`architecture-implementation-patterns.md` にS12-S17 Atoms設計パターン追加。`testing-component-patterns.md` v1.7.0（Atomsテストパターンセクション13追加）。`ui-ux-design-system.md` v1.4.0（StatusIndicatorカラー定義追加）。`ui-ux-design-principles.md`（HIG準拠パターンテーブル追加）。`06-known-pitfalls.md` にP46/P47追加。`skill-creator/patterns.md` に成功3件+失敗2件追加。topic-map.md再生成 |
| **8.62.0** | **2026-02-23** | **TASK-UI-00-ATOMS Phase 12完了反映**: `ui-ux-components.md` v2.11.0（TASK-UI-00-ATOMS完了タスク追加 + Atoms実装状況テーブル追加）、`ui-ux-design-system.md` v1.3.0（デザイントークン使用パターン追加）。LOGS.md完了記録追加 |
| **8.61.0** | **2026-02-23** | **TASK-IMP-MODULE-RESOLUTION-CI-GUARD-001 教訓追加**: lessons-learned.md に苦戦箇所4件（正規表現パース、キー変換設計、typesVersionsスキップ、process.exitCodeテスタビリティ）を追記 |
| **8.61.0** | **2026-03-06** | **TASK-043B 完了反映**: `ui-ux-components.md` / `ui-ux-feature-components.md` / `arch-ui-components.md` / `task-workflow.md` / `lessons-learned.md` に SkillManagementPanel import list refinement を同期。2セクション UI、dialog 追加導線、store action 非 throw 契約への対処、Phase 11 証跡（TC 9/9 + mobile 補助）を記録 |
| **8.60.0** | **2026-02-22** | **TASK-IMP-MODULE-RESOLUTION-CI-GUARD-001 教訓追補**: `architecture-monorepo.md` に実装時の苦戦箇所と対処（MINOR未タスク化、Phase 12証跡同期、未タスク監査ベースライン分離）を追加。`lessons-learned.md` v1.18.3 に苦戦箇所3件と5ステップ簡潔解決手順を追記 |
| **8.59.0** | **2026-02-22** | **TASK-IMP-MODULE-RESOLUTION-CI-GUARD-001再監査是正**: `technology-devops.md` に主要CIジョブ構成テーブルを追加し、Step 1-B の実装状況反映を仕様実体化。`SKILL.md` / `LOGS.md` の競合痕跡文字列を除去し、`generate-index.js` 再実行で `topic-map.md` / `keywords.json` を再同期 |
| **8.58.0** | **2026-02-22** | **TASK-IMP-MODULE-RESOLUTION-CI-GUARD-001完了反映**: @repo/shared 3層整合CIガードスクリプト追加。check-module-syncジョブCI統合。43テスト全PASS。quality-requirements.md/architecture-monorepo.md/technology-devops.md更新。LOGS.md完了記録追加 |
| **8.57.0** | **2026-02-22** | **未タスク配置監査と教訓追記**: `interfaces-agent-sdk-skill.md` に UT-FIX-SKILL-IMPORT-ID-MISMATCH-001 の苦戦箇所と4ステップ簡潔解決手順を追加。`lessons-learned.md` v1.18.2 追記。`task-workflow.md` 等の未タスク参照を `unassigned-task/` に統一し、誤配置6件移動+重複1件整理を反映 |
| **8.56.0** | **2026-02-22** | **UT-FIX-SKILL-IMPORT-ID-MISMATCH-001完了反映**: interfaces-agent-sdk-skill.md v1.28.0（関連未タスクテーブル完了化 + 完了タスクセクション追加）、task-workflow.md v1.50.0（残課題完了化 + 完了タスクセクション追加）。Renderer層のみ変更（skill.id→skill.name） |
| **8.56.0** | **2026-02-22** | **仕様準拠再監査反映**: `testing-component-patterns.md` v1.6.0（テーマ横断テストヘルパーパターン追加: `renderWithTheme`/`renderWithAllThemes`）。`task-workflow.md` 残課題の未実在参照を実在化し `verify-unassigned-links` 79/79 を確認。`topic-map.md` / `keywords.json` 再生成 |
| **8.54.0** | **2026-02-22** | **TASK-UI-00-TOKENS Phase 1-12完了反映**: `ui-ux-design-system.md` v1.2.0（Apple HIG System Colors light/darkテーマ定義、TASK-UI-00-TOKENS完了記録追加）。LOGS.md完了記録追加 |
| **8.53.0** | **2026-02-21** | **UT-FIX-SKILL-REMOVE-INTERFACE-001 Phase 1-12実行知見反映**: architecture-implementation-patterns.md にP44解決パターン追加、lessons-learned.md に実装苦戦箇所3件記録（Phase依存順序・worktree制約・カバレッジ閾値）、interfaces-agent-sdk-skill.md にskill:remove契約更新 |
| **v1.40.2** | **2026-02-21** | **未実施タスク誤配置の再是正 + 教訓追記**: `task-workflow.md` の未実施2件（`UT-FIX-TS-VITEST-TSCONFIG-PATHS-001`, `TASK-IMP-MODULE-RESOLUTION-CI-GUARD-001`）参照を `docs/30-workflows/unassigned-task/` へ戻し、`lessons-learned.md` に「ワークツリー環境でのStep 1-A先送り誤判断」教訓を追加 |
| **v1.40.1** | **2026-02-21** | **task-workflow 未タスク参照リンク整合を是正**: `verify-unassigned-links` で検出した未実在リンク4件を実在パスに修正。`UT-FIX-TS-VITEST-TSCONFIG-PATHS-001` / `TASK-REFACTOR-SHARED-SOURCE-STRUCTURE-001` / `TASK-IMP-MODULE-RESOLUTION-CI-GUARD-001` を `completed-tasks/unassigned-task/` へ、`UT-FIX-SKILL-IMPORT-RETURN-TYPE-001` を `skill-import-agent-system/tasks/` へ補正 |
| **v1.44.0** | **2026-02-21** | **P44/P45契約ドリフト防止強化**: security-electron-ipc.md v1.7.0（契約ドリフト防止セクション追加: ipc-contract-checklist.md参照・3段バリデーション検証テーブル）。api-ipc-agent.md skill:import完了タスク記録。interfaces-agent-sdk-skill.md リクエスト契約詳細テーブル追加 |
| **v1.43.0** | **2026-02-21** | **UT-FIX-SKILL-IMPORT-INTERFACE-001完了反映**: `skill:import` IPC引数契約を `skillName: string` に統一。api-ipc-agent.md, interfaces-agent-sdk-skill.md, task-workflow.md, lessons-learned.md 更新済み。P44パターン完全解決。LOGS.md完了記録追加 |
| **v1.42.0** | **2026-02-21** | **UT-FIX-SKILL-IMPORT-INTERFACE-001 再監査追補**: `lessons-learned.md` に苦戦箇所3件（Phase 12ステータス未同期、旧参照パス残存、Vitest実行ディレクトリ差異）を追加。`interfaces-agent-sdk-skill.md` に実装課題を追記し、`security-electron-ipc.md` に Skill API の `skillName` + `trim()` 検証パターンを反映 |
| **v1.41.0** | **2026-02-21** | **UT-FIX-SKILL-IMPORT-INTERFACE-001 Phase 12反映**: `task-workflow.md` を完了反映（残課題→完了 + completed-task参照へ移行）。`arch-electron-services.md` / `security-skill-ipc.md` / `interfaces-agent-sdk-skill.md` / `api-ipc-agent.md` に `skill:import` 契約（`skillName: string` + P42検証）を反映 |
| **v1.42.0** | **2026-02-21** | **UT-FIX-SKILL-IMPORT-RETURN-TYPE-001 スキル改善**: `architecture-implementation-patterns.md` v1.26.0 に S13 IPC戻り値型2ステップ変換パターン追加（苦戦箇所5件記録）。`ipc-type-resolution-guide.md` v1.0.0 新規作成（P23/P32/P42/P44/P45統合ガイド）。`patterns.md` に成功パターン2件追加 |
| **v1.41.0** | **2026-02-21** | **UT-FIX-SKILL-IMPORT-RETURN-TYPE-001 Phase 12反映**: `skill:import` IPC戻り値型修正（ImportResult→ImportedSkill）を `interfaces-agent-sdk-skill.md` / `arch-electron-services.md` / `security-skill-ipc.md` / `task-workflow.md` / `ipc-contract-checklist.md` に反映。残課題→完了タスクへ移動 |
| **v1.40.0** | **2026-02-20** | **IPC契約チェックリスト新規作成 + クロスリファレンス強化**: `ipc-contract-checklist.md` を新規作成（P23/P32/P42/P44統合チェックリスト）。`lessons-learned.md` / `security-skill-ipc.md` にチェックリスト参照を追加。`skill-creator/patterns.md` のクイックナビゲーション重複行を統合 |
| **v1.39.0** | **2026-02-20** | **未タスク配置ドリフト是正 + 実装苦戦箇所追記**: `task-workflow.md` / `api-ipc-agent.md` の未実施タスク参照を `docs/30-workflows/unassigned-task/` に統一。`lessons-learned.md` に UT-FIX-SKILL-REMOVE-INTERFACE-001 の苦戦箇所（契約ドリフト/配置ドリフト/テスト実行コンテキスト差異）を追加 |
| **v1.38.1** | **2026-02-20** | **UT-FIX-SKILL-REMOVE-INTERFACE-001 Phase 12反映**: `task-workflow.md` の未タスク参照を実ファイルに修正し、UT-FIX-SKILL-REMOVEを完了化。`interfaces-agent-sdk-skill.md` / `api-ipc-agent.md` / `arch-electron-services.md` / `security-skill-ipc.md` に `skill:remove` の `skillName` 契約を反映 |
| **v1.38.0** | **2026-02-20** | **TASK-FIX-TS-SHARED-MODULE-RESOLUTION-001 Phase 12反映**: `@repo/shared` 三層モジュール解決整合化（228件→0件）。27 paths + 26 typesVersions + 3 alias 追加、224テスト全PASS。architecture-monorepo.md / development-guidelines.md / lessons-learned.md / quality-requirements.md / task-workflow.md / patterns.md を更新。未タスク `UT-FIX-TS-VITEST-TSCONFIG-PATHS-001` 登録 |
| **v1.37.0** | **2026-02-19** | **TASK-9A-C SkillEditor UI仕様書作成反映**: references 5ファイル更新（ui-ux-feature-components/interfaces-agent-sdk-skill/architecture-implementation-patterns/testing-component-patterns/lessons-learned）。SkillEditorコンポーネント仕様・型定義・実装パターン・テストパターン・苦戦箇所を追加 |
| **v1.36.0** | **2026-02-19** | **TASK-9A-C Phase 12準拠監査反映（追補）**: ui-ux-components.md v2.9.1 / ui-ux-feature-components.md v1.8.1 に監査エビデンスを追記。lessons-learned.md v1.15.0 に苦戦箇所4件（参照混在、phase表記ゆれ、spec_created判定、未タスク実体不足）を追加 |
| **v1.35.0** | **2026-02-19** | **TASK-FIX-10-1 教訓最適化反映**: `lessons-learned.md` に実装苦戦箇所（Step 2判定、未タスク検出範囲、alias運用継続性）と「同種課題の簡潔解決手順（5ステップ）」を追加。類似課題の再現性を強化 |
| **v1.34.0** | **2026-02-19** | **TASK-FIX-10-1-VITEST-ERROR-HANDLING再監査反映**: Vitest設定修正（dangerouslyIgnoreUnhandledErrors削除 + 18個の@repo/sharedサブパスエイリアス追加）に加え、`task-workflow.md` 完了記録/残課題更新（`task-imp-vitest-alias-sync-automation-001`追加）、`quality-requirements.md` に未処理Promise拒否検知ルールとalias管理ルールを追記 |
| **v1.33.0** | **2026-02-19** | **TASK-9A-C仕様再監査反映**: ui-ux-components.md / ui-ux-feature-components.md に SkillEditor（TASK-9A-C）の「仕様書作成済み・実装未着手」状態を追記。タスク参照整合（tasks/completed-task）と Phase 12成果物リンクを更新 |
| **v1.32.0** | **2026-02-14** | **TASK-FIX-14-1 実装パターン体系化**: logging-migration-guide.md新規作成、patterns.md・development-guidelines.md・lessons-learned.md更新 |
| **v1.31.0** | **2026-02-14** | **UT-FIX-IPC-RESPONSE-UNWRAP-001実装知見追記**: lessons-learned.md 実装苦戦箇所4件、architecture-implementation-patterns.md safeInvokeUnwrap パターン、patterns.md 成功/失敗パターン追加 |
| **v1.31.0** | **2026-02-14** | **TASK-FIX-14-1 苦戦箇所の仕様化**: lessons-learned.md v1.11.0 を追加（実変更ファイル名との乖離防止、Phase 12 Step 1-A/1-C/1-D先送り誤判定防止、未タスク登録3ステップ同時完了）。task-fix-14-2 への追跡リンクを明記 |
| **v1.30.2** | **2026-02-14** | **UT-FIX-IPC-HANDLER-DOUBLE-REG-001 Phase 12再監査追補**: lessons-learned.md に苦戦箇所2件を追記（IPC_CHANNELS全走査の前提確認、IPC外リスナー解除漏れ防止）。Phase 12準拠監査結果を反映し、未タスク検出は「新規0件（rawは既存TODO）」を確認 |
| **v1.31.0** | **2026-03-10** | **TASK-10A-G完了**: スキルライフサイクル統合テスト強化（G1:14件IPC契約 + G2:21件Store駆動 + G3:17件ChatPanel結線 = 52テスト全PASS）。arch-state-management.md関連タスクステータス更新、task-workflow.md完了タスク追加。LOGS.md 2ファイル + SKILL.md 2ファイル同時更新（P1/P25対策） |
| **v1.30.1** | **2026-02-14** | **UT-FIX-IPC-HANDLER-DOUBLE-REG-001 参照整合の是正**: task-workflow.md の完了タスク参照を `completed-tasks/` に正規化し、完了タスク仕様書の Issue 番号不整合（#814/#818 → #815）を修正。`generate-index.js` 再実行で topic-map/keywords を同期 |
| **v1.30.0** | **2026-02-14** | **UT-FIX-IPC-RESPONSE-UNWRAP-001完了反映**: interfaces-agent-sdk-skill.md v1.20.0更新（Preload IPCラッパー展開の完了記録、苦戦箇所追記）、task-workflow.md v1.37.0更新（完了反映 + MINOR由来未タスク2件追加）、lessons-learned.md v1.11.0更新（参照正本不一致・MINOR未タスク化漏れ・完了移管リンク不整合の教訓追加） |
| **v1.30.0** | **2026-02-14** | **UT-FIX-IPC-HANDLER-DOUBLE-REG-001完了**: IPC ハンドラ二重登録防止修正。security-electron-ipc.md v1.4.0更新（IPCハンドラライフサイクル管理セクション追加）、task-workflow.md更新（完了タスク追加）、lessons-learned.md更新（ipcMain.handle()二重登録教訓追加）。7テスト全PASS |
| **v1.30.0** | **2026-02-14** | **TASK-FIX-14-1 Phase 12反映**: task-workflow.md v1.37.0（完了タスク追加 + 未タスク TASK-FIX-14-2 登録）、interfaces-agent-sdk-history.md v6.39.0（残課題更新）、development-guidelines.md v1.7.0（Skill系Main Processログ規約追加） |
| **v1.29.0** | **2026-02-13** | **TASK-FIX-13-1未タスク仕様書作成（UT-TYPE-DATETIME-DOC-001追加、task-workflow.md更新）** |
| **v1.28.0** | **2026-02-13** | **TASK-FIX-13-1再検証教訓追記**: lessons-learned.md v1.8.0更新（ドキュメント偏重による実装検証省略、並列エージェント品質保証の教訓2件追加）。skill-creatorのpatterns.mdにdeprecatedプロパティ移行パターンを追加 |
| **v1.27.0** | **2026-02-13** | **TASK-FIX-13-1教訓追記**: interfaces-agent-sdk-skill.md v1.19.0（苦戦箇所・再発防止策を追加）、task-workflow.md v1.36.0（完了タスク節に苦戦箇所テーブル追加）、lessons-learned.md v1.7.0（教訓3件追加） |
| **v1.26.0** | **2026-02-13** | **TASK-FIX-13-1完了反映 + 未タスク登録**: interfaces-agent-sdk-skill.md v1.18.0更新（deprecated型プロパティ削除を反映、Skill型にlastModified明記）、task-workflow.md v1.35.0更新（完了タスク追加 + UT-PERF-001未タスク登録） |
| **v1.25.0** | **2026-02-13** | **TASK-FIX-11-1スキル改善（技術詳細）**: lessons-learned.md v1.7.0（Vitestモック管理3サブセクション追加: clearAllMocks限界・mockRejectedValueOnce・モジュールモックタイムアウト）。architecture-implementation-patterns.md v1.18.0（2パターン追加: リセット戦略・タイムアウトテスト） |
| **v1.25.0** | **2026-02-12** | **完了タスク移動を反映**: UT-FIX-AGENTVIEW-INFINITE-LOOP-001を`docs/30-workflows/completed-tasks/`へ移動し、task-workflow.md v1.32.0で関連未タスク4件の参照先を`completed-tasks/`へ同期 |
| **v1.24.0** | **2026-02-13** | **TASK-FIX-11-1-SDK-TEST-ENABLEMENT 教訓追記**: lessons-learned.md v1.6.0追加（Phase 12 Step 1-A/1-D誤判定、未タスクraw誤検知、Vitestモック再初期化）。interfaces-agent-sdk-executor.md v1.7.1に「実装上の課題と教訓」を追記 |
| **v1.24.0** | **2026-02-13** | **テスト環境教訓体系化**: lessons-learned.md v1.6.0更新（happy-dom/userEvent非互換、テスト実行ディレクトリ依存、jsdom切替副作用）。architecture-implementation-patterns.md v1.18.0更新（fireEvent vs userEvent使い分けパターン追加）。06-known-pitfalls.md P39/P40追加 |
| **v1.23.0** | **2026-02-13** | **TASK-FIX-11-1-SDK-TEST-ENABLEMENT Phase 12是正**: Step 1-A/1-D誤判定を修正。interfaces-agent-sdk-executor.md v1.7.0、testing-component-patterns.md v1.4.0、task-workflow.md v1.31.0 更新。LOGS.md 2ファイル・SKILL.md 2ファイル更新、topic-map再生成を実施 |
| v1.23.0 | 2026-02-13 | UT-9B-H-003セキュリティ教訓追加: lessons-learned.md v1.6.0（苦戦箇所5件）、architecture-implementation-patterns.md v1.21.0（IPC L3ドメイン検証パターン） |
| **v1.23.0** | **2026-02-12** | **未タスク参照整合を是正**: task-workflow.md v1.31.0更新。完了済みタスクの参照先を `completed-tasks/` に正規化し、未実施タスク（UT-STORE-HOOKS-REFACTOR-002/003, UT-FIX-APP-INITAUTH-CHECK-001）の `unassigned-task/` 配置を反映 |
| **v1.22.2** | **2026-02-12** | **UT-9B-H-003 Phase 12再監査**: lessons-learned.md v1.5.2に苦戦箇所を追記（返却仕様文言不整合、完了済み未タスク残置、artifacts整合）。task-workflow.md v1.30.2 / interfaces-agent-sdk-skill.mdで完了済み指示書の参照パスを completed-tasks 側へ更新。skill-feedback-report.md追加 |
| **v1.22.1** | **2026-02-12** | **UT-9B-H-003追補**: 仕様整合性修正。security-electron-ipc.md v1.3.1（エラー返却仕様を実装準拠化）、api-ipc-agent.md v1.7.0（セキュリティ強化仕様追記）、interfaces-agent-sdk-skill.md v1.16.1 / task-workflow.md v1.30.1（UT-9B-H-003を未タスク表から完了反映） |
| **v1.22.0** | **2026-02-12** | **UT-FIX-AGENTVIEW-INFINITE-LOOP-001完了**: arch-state-management.md v1.16.0更新（AgentViewのP31適用拡張、個別セレクタ15個追加記録）、task-workflow.md v1.30.0更新（完了タスク追加）、interfaces-agent-sdk-skill.md v1.17.0更新（完了記録追加） |
| **v1.22.0** | **2026-02-12** | **UT-9B-H-003完了**: SkillCreator IPCセキュリティ強化。security-electron-ipc.md v1.3.0更新、interfaces-agent-sdk-skill.md完了記録更新、task-workflow.md完了記録更新。validatePath/sanitizeErrorMessage/ALLOWED_SCHEMA_NAMES追加。116テスト全PASS |
| **v1.22.0** | **2026-02-12** | **UT-STORE-HOOKS-TEST-REFACTOR-001完了**: arch-state-management.md更新（完了タスクセクション追加）。agentSlice.selectors.test.tsのgetState()→renderHookパターン移行、114テスト全PASS |
| **v1.21.0** | **2026-02-12** | **TASK-9B-I-SDK-FORMAL-INTEGRATION完了**: Claude Agent SDK型安全正式統合。SkillExecutor.ts `as any` 除去、SDK実型（@anthropic-ai/claude-agent-sdk@0.2.30）に基づく型安全な callSDKQuery 実装。apiKey → env.ANTHROPIC_API_KEY、signal → abortController、conversation直接利用。テスト278件全PASS |
| **v1.20.0** | **2026-02-12** | **UT-STORE-HOOKS-COMPONENT-MIGRATION-001テンプレート準拠最適化**: lessons-learned.md ファイルパス修正、patterns.md P31セクション重複削減（Progressive Disclosure準拠） |
| **v1.19.0** | **2026-02-12** | **UT-STORE-HOOKS-COMPONENT-MIGRATION-001完了**: arch-state-management.md更新（P31対策セクションに個別セレクタ実装完了記録、関連タスクステータス更新）、task-workflow.md更新（完了タスク追加）、06-known-pitfalls.md P31解決策更新。30個の個別セレクタHook、3コンポーネント移行、71テスト全PASS |
| **v1.18.0** | **2026-02-12** | **スキル改善**: UT-STORE-HOOKS-REFACTOR-001教訓反映。patterns.mdに「Zustand個別セレクタベース再設計パターン」追加（設計方針・命名規則・移行ガイド・参照安定性チェックリスト）。P31対策の長期解決策をパターン化 |
| **v1.17.0** | **2026-02-12** | **スキル最適化（TASK-FIX-7-1事後）**: Triggerキーワード網羅性確認（不足なし）、変更履歴整理。task-specification-creatorのcoverage-standards.md・unassigned-task-guidelines.md・phase-templates.mdフォーマット最適化と連動 |
| **v1.16.0** | **2026-02-12** | **TASK-FIX-7-1スキル改善(2)**: Triggerキーワードに「DIパターン, Constructor Injection, Factory Pattern, BrowserWindow遅延生成, テストモック大規模修正」を追加。DI関連の検索性をさらに向上 |
| **v1.15.1** | **2026-02-12** | **TASK-9B-H-SKILL-CREATOR-IPC完了**: SkillCreatorService IPC登録。security-skill-ipc.md v1.5.0、interfaces-agent-sdk-skill.md v1.14.0、arch-ipc-persistence.md v1.2.0更新。85テスト全PASS |
| **v1.15.0** | **2026-02-11** | **UT-STORE-HOOKS-REFACTOR-001完了**: 個別セレクタ53個追加（AuthMode 12個, LLM 16個, Agent 25個）、181テスト全PASS、カバレッジLine 88.51%/Branch 89.79%/Function 92.53%達成。arch-state-management.md関連タスク更新、03-state-management.mdにP31参照リンク追加、未タスク2件検出（002: JSDoc追加, 003: 合成Hook移行）|
| **v1.15.0** | **2026-02-19** | **TASK-9A-B完了**: ファイル編集IPCハンドラー6チャンネル追加（skill:readFile/writeFile/createFile/deleteFile/listBackups/restoreBackup）。api-ipc-agent.md/security-electron-ipc.md/architecture-overview.md/interfaces-agent-sdk-skill.md/task-workflow.md更新 |
| **v1.14.0** | **2026-02-11** | **TASK-FIX-7-1スキル改善**: Triggerキーワードに「Setter Injection, 依存性注入, 遅延初期化, setSkillExecutor, SkillExecutor委譲」を追加。検索性向上 |
| **v1.13.0** | **2026-02-11** | **TASK-FIX-7-1システム仕様書更新**: arch-electron-services.md v1.11.0更新（SkillService API追加、SkillService統合セクション追加）、interfaces-agent-sdk-executor.md v1.4.0更新（SkillService統合セクション新設）、architecture-implementation-patterns.md v1.17.0更新（Setter Injectionパターン追加）。LOGS.md 2ファイル・SKILL.md 2ファイル更新 |
| **v1.12.0** | **2026-02-11** | **TASK-FIX-7-1-EXECUTE-SKILL-DELEGATION完了**: SkillService.executeSkill()をSkillExecutorに委譲するTDD実装。Phase 1-12全工程完了、統合テスト7件・ユニットテスト12件全PASS、未タスク0件。スキル更新（LOGS.md 2ファイル、SKILL.md 2ファイル） |
| **v1.11.0** | **2026-02-10** | **TASK-FIX-6-1知見によるスキル改善**: patterns.md成功パターン3件追加（Slice統合、Race Condition対策、Phase 12チェックリスト）、arch-state-management.md v1.10.0（skillSlice統合記録）、06-known-pitfalls.md P25-P28追加、topic-map.md再生成実施 |
| **v1.10.0** | **2026-02-10** | **TASK-FIX-6-1-STATE-CENTRALIZATION完了**: arch-state-management.md更新（skillSlice統合記録、agentSlice拡張）、テスト70件PASS、Branch Coverage 89.09%達成 |
| **8.55.0** | **2026-02-21** | **UT-FIX-SKILL-IMPORT-RETURN-TYPE-001 未タスク検出**: skillHandlers.ts全14ハンドラ調査→3件検出（IPC応答形式統一・P45引数名ドリフト・P42バリデーション統一）。task-workflow.md残課題3エントリ追加、interfaces-agent-sdk-skill.md関連テーブル追加 |
| **8.54.0** | **2026-02-10** | **SKILL.md最適化**: skill-creatorテンプレート準拠。変更履歴を最新20件に圧縮（古い19件をLOGS.mdに移動）。500行以内維持 |
| **8.53.0** | **2026-02-10** | **P31対策スキル改善**: topic-map.md再生成、quick-reference.mdにP31対策早見パターン追加、SKILL.md Triggerキーワード追加、keywords.json再生成 |
| **8.53.0** | **2026-03-09** | TASK-10A-F P50検証完了: S19パターン追加、教訓5件追加 |
| **8.52.0** | **2026-02-10** | **UT-FIX-STORE-HOOKS-INFINITE-LOOP-001完了**: 06-known-pitfalls.md P31追加（Zustand Store Hooks無限ループ）。useRefガード実装 |
| **8.51.0** | **2026-02-10** | **UT-FIX-5-4-AGENT-SDK-API-TYPE-MISMATCH完了**: AgentSDKAPI abort()型定義修正。`abort(): void` → `abort(): Promise<void>`に変更（2箇所: shared/types.ts, preload/types.ts）。P23パターン準拠。実装（safeInvoke）と型定義の整合性確保。24テストPASS、未タスク0件 |
| **8.50.0** | **2026-02-10** | **UT-FIX-5-3-PRELOAD-AGENT-ABORT完了**: Agent Abort IPCセキュリティ修正。preload/index.ts `ipcRenderer.send` → `safeInvoke(IPC_CHANNELS.AGENT_ABORT)` 変更、agent-handler.ts `ipcMain.on` → `ipcMain.handle` 変更、dispose()に`removeHandler`追加。04-electron-security.md IPC原則準拠。21テストPASS、未タスク0件 |
| **8.49.0** | **2026-02-09** | **TASK-AUTH-MODE-SELECTION-001完了**: interfaces-auth.md更新（AuthMode型・AuthModeService・SubscriptionAuthProvider追加）。認証方式選択機能（サブスクリプション/APIキー切り替え）実装。86テスト全PASS |
| **8.48.0** | **2026-02-09** | **patterns.md構造最適化**: skill-creatorテンプレート準拠。目次カテゴリナビゲーション追加、成功パターン5カテゴリ（Phase 12ドキュメント/IPC・Electron/OAuth・認証/テスト・品質/ストア・永続化）、失敗パターン4カテゴリ（Phase 12漏れ/OAuth・認証エラー/テスト・型安全/その他）に再構成。見出しレベル統一（###カテゴリ/####個別パターン）。パターン件数：成功16件/失敗17件 |
| **8.47.0** | **2026-02-09** | **TASK-FIX-12-1苦戦箇所記録**: patterns.md成功/失敗パターン追加（IPCチャンネル名定数化、Phase 12 Step 1更新漏れ、未タスク検出時関連ファイル調査不足、未タスク配置ディレクトリ誤り）。architecture-implementation-patterns.md v1.16.0 IPCチャンネル名定数化パターン追加済み。06-known-pitfalls.md P23/P24追加予定 |
| **8.46.0** | **2026-02-09** | **TASK-FIX-12-1-IPC-HARDCODE-FIX完了**: SkillExecutor.ts L918/L1214 のハードコード文字列 `"skill:stream"` を `SKILL_CHANNELS.SKILL_STREAM` 定数参照に変更。IPC セキュリティ原則準拠。未タスク TASK-FIX-12-2 検出 |
| **8.45.0** | **2026-02-08** | **TASK-FIX-16-1-SDK-AUTH-INFRASTRUCTURE完了**: security-principles.md更新（SDK認証キー管理セクション追加）、api-ipc-system.md更新（auth-key IPCチャンネル4種追加）、api-endpoints.md更新（SDK認証キーカテゴリ追加）、interfaces-agent-sdk-executor.md更新（AUTHENTICATION_ERROR追加、AuthKeyService統合）。119テスト全PASS |
| **8.44.0** | **2026-02-08** | **TASK-FIX-4-2パターン追加**: 06-known-pitfalls.mdにP19-P20追加（型アサーション検証バイパス・テストログ出力汚染）。interfaces-agent-sdk-executor.md型バリデーションパターン記載 |
| **8.43.0** | **2026-02-08** | **TASK-FIX-4-2-SKILL-STORE-PERSISTENCE完了**: interfaces-skill-execution.md更新（validateStoredSkillIds詳細ロジック追加）、security-principles.md更新（ストレージ整合性検証セクション追加）。87テスト全PASS |
| **8.42.0** | **2026-02-06** | **DEBT-SEC-001仕様構造最適化**: csrf-state-parameter.md新規作成（OAuth CSRF/State詳細を分離）、security-principles.md軽量化（参照リンク追加）、patterns.md拡充（OAuth成功/失敗パターン10件追加） |
| **8.41.1** | **2026-02-06** | **DEBT-SEC-001完了**: security-principles.md更新（CSRF対策セクション）、architecture-auth-security.md更新（PKCE実装詳細）、api-ipc-auth.md更新（認証IPC Channel仕様） |
| **8.41.0** | **2026-02-06** | **TASK-FIX-5-1最適化**: architecture-implementation-patterns.md更新（S1-S4パターン追加、既知パターンテーブル拡充）、06-known-pitfalls.md P11追加（Claude Code Hooks Edit失敗） |
| **8.41.0** | **2026-03-14** | **TASK-IMP-WORKSPACE-CHAT-EDIT-AI-RUNTIME-001完了**: llm-workspace-chat-edit.md更新（RuntimeResolver/AnthropicLLMAdapter/TerminalHandoffBuilder）、interfaces-llm.md更新（RuntimeResolution/HandoffGuidance型）、api-ipc-agent-core.md更新（chat-edit:send-with-context契約変更）、security-electron-ipc-core.md更新（M-01 contextBridge修正/workspacePath検証）、lessons-learned-current.md更新（P57-P61）。55テスト全PASS |
| **8.40.1** | **2026-02-06** | **TASK-FIX-5-1-SKILL-API-UNIFICATION完了**: security-electron-ipc.md更新（safeInvoke/safeOnパターン、API統合アーキテクチャ図追加）、interfaces-skill-execution.md更新（ImportedSkill型統一）。Preload API統一（window.skillAPI→window.electronAPI.skill）。210テスト全PASS |
| **8.40.0** | **2026-02-06** | **TASK-AUTH-SESSION-REFRESH-001完了**: architecture-auth-security.md v1.10.0更新（TokenRefreshScheduler仕様追加）、interfaces-auth.md更新（TokenRefreshCallbacks/TokenRefreshConfig追加）、api-ipc-auth.md更新（session:scheduleRefreshチャンネル追加）。26テスト全PASS |
| **8.39.0** | **2026-02-05** | **ENV-INFRA-001苦戦箇所記録**: patterns.md更新（ネイティブモジュールNODE_MODULE_VERSION不一致解決パターン追加） |
| **8.38.0** | **2026-02-05** | **TASK-FIX-4-1-IPC-CONSOLIDATION完了**: api-ipc-system.md更新（統合チャンネル一覧）、security-electron-ipc.md更新（IPCチャンネルホワイトリスト更新）、architecture-patterns.md更新（Preload Bridge Pattern詳細）。42テスト全PASS |
| **8.37.0** | **2026-02-04** | **AUTH-UI-001完了**: architecture-implementation-patterns.md更新（React Portal/Supabase認証状態即時更新パターン追加）、ui-ux-auth-flow.md v1.3.0更新（Googleログインボタン仕様追加） |
| **8.36.0** | **2026-02-04** | **スキル最適化**: spec-update-workflow.mdファイル名修正（kebab-case統一）、topic-map.md再生成（新規ファイル反映） |
| **8.35.1** | **2026-02-04** | **task-imp-search-ui-001完了**: ui-ux-search-panel.md v1.2.0更新（E2Eテスト17件追加、グローバルショートカット統合完了） |
### バージョン更新: 9.01.91
- 日付: 2026-03-12
- 内容: `TASK-IMP-AIWORKFLOW-REQUIREMENTS-LINE-BUDGET-REFORM-001` の最終同期を反映。manual docs 34件 reform、Phase 1-12 completed / currentPhase=13 / Phase 13 blocked、generated `topic-map.md` の 500行超 blocker 化、`TASK-IMP-AIWORKFLOW-REQUIREMENTS-GENERATED-INDEX-SHARDING-001` と `TASK-IMP-AIWORKFLOW-GENERATED-INDEX-METRIC-SYNC-GUARD-001` の follow-up formalize、Phase 11 branch-level dashboard screenshot sanity に加え、Phase 12 root evidence 化、active 未タスク10見出し化、`verify-unassigned-links` の split 親 + sibling 監査、`workflow-aiworkflow-requirements-line-budget-reform.md` / `quick-reference.md` / `resource-map.md` / `spec-splitting-guidelines.md` の再利用導線まで system spec に固定した。
### バージョン更新: 9.01.90
- 日付: 2026-03-12
- 内容: Phase12監査で `outputs/phase-12` 未作成 drift を検出し `TASK-IMP-AIWORKFLOW-REQ-PHASE12-ARTIFACTS-MISSING-001` として切り出した。documentation shell 追加と verification rerun 完了済み。`TASK-IMP-AIWORKFLOW-REQUIREMENTS-LINE-BUDGET-REFORM-001` をシステム仕様追跡対象として追加。
