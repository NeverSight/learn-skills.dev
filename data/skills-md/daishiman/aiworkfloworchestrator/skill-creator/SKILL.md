---
name: skill-creator
description: |
  スキルを作成・更新・プロンプト改善するためのメタスキル。
  **collaborative**モードでユーザーと対話しながら共創し、
  抽象的なアイデアから具体的な実装まで柔軟に対応する。
  **orchestrate**モードでタスクの実行エンジン（Claude Code / Codex / 連携）を選択。

  Anchors:
  • Continuous Delivery (Jez Humble) / 適用: 自動化パイプライン / 目的: 決定論的実行
  • The Lean Startup (Eric Ries) / 適用: Build-Measure-Learn / 目的: 反復改善
  • Domain-Driven Design (Eric Evans) / 適用: 戦略的設計・ユビキタス言語・Bounded Context / 目的: ドメイン構造の明確化
  • Clean Architecture (Robert C. Martin) / 適用: 依存関係ルール・層分離設計 / 目的: 変更に強い高精度スキル
  • Design Thinking (IDEO) / 適用: ユーザー中心設計 / 目的: 共感と共創

  Trigger:
  新規スキルの作成、既存スキルの更新、プロンプト改善を行う場合に使用。
  スキル作成, スキル更新, プロンプト改善, skill creation, skill update, improve prompt,
  Codexに任せて, assign codex, Codexで実行, GPTに依頼, 実行モード選択, どのAIを使う,
  IPC Bridge統一, API統一パターン, safeInvoke/safeOn, Preload API標準化,
  IPC handler registration, Preload API integration, contextBridge, Electron IPC pattern
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Task
  - AskUserQuestion
---

# Skill Creator

スキルを作成・更新・プロンプト改善するためのメタスキル。

## 設計原則

| 原則                    | 説明                                       |
| ----------------------- | ------------------------------------------ |
| **Problem First**       | 機能の前に本質的な問題を特定する           |
| **Collaborative First** | ユーザーとの対話を通じて要件を明確化       |
| Domain-Driven Design    | ドメイン構造を明確化し高精度な設計を導く   |
| Clean Architecture      | 層分離と依存関係ルールで変更に強い構造     |
| Script First            | 決定論的処理はスクリプトで実行（100%精度） |
| Progressive Disclosure  | 必要な時に必要なリソースのみ読み込み       |

## クイックスタート

| モード            | 用途                             | 開始方法                                        |
| ----------------- | -------------------------------- | ----------------------------------------------- |
| **collaborative** | ユーザー対話型スキル共創（推奨） | AskUserQuestionでインタビュー開始               |
| **orchestrate**   | 実行エンジン選択                 | AskUserQuestionでヒアリング開始                 |
| create            | 要件が明確な場合の新規作成       | `scripts/detect_mode.js --request "..."`        |
| update            | 既存スキル更新                   | `scripts/detect_mode.js --skill-path <path>`    |
| improve-prompt    | プロンプト改善                   | `scripts/analyze_prompt.js --skill-path <path>` |

---

## ワークフロー概要

### Collaborative モード（推奨）

```
Phase 0-0: 問題発見 → problem-definition.json
      ↓
Phase 0.5: ドメインモデリング → domain-model.json
      ↓
Phase 0-1〜0-8: インタビュー → interview-result.json
      ↓
[分岐] multiSkillPlan がある場合:
  Phase 0.9: マルチスキル設計 (design-multi-skill) → multi-skill-graph.json
  → 各サブスキルに対して以下を繰り返し:
      ↓
リソース選択: select-resources.md → resource-selection.json
      ↓
Phase 1: 要求分析 → Phase 2: 設計
      ↓
[条件] skillDependencies がある場合:
  Phase 2.5: 依存関係解決 (resolve-skill-dependencies) → skill-dependency-graph.json
      ↓
Phase 3: 構造計画 → Phase 4: 生成
      ↓
[条件] externalCliAgents がある場合:
  Phase 4.5: 外部CLIエージェント委譲 (delegate-to-external-cli) → external-cli-result.json
      ↓
Phase 5: レビュー (quick-validate) → Phase 6: 検証 (validate-all)
```

📖 [agents/discover-problem.md](.claude/skills/skill-creator/agents/discover-problem.md) — 根本原因分析
📖 [agents/model-domain.md](.claude/skills/skill-creator/agents/model-domain.md) — DDD/Clean Architecture
📖 [agents/interview-user.md](.claude/skills/skill-creator/agents/interview-user.md)
📖 [agents/select-resources.md](.claude/skills/skill-creator/agents/select-resources.md)

### Orchestrate モード

実行エンジン選択: `claude` | `codex` | `gemini` | `claude-to-codex`

📖 [references/execution-mode-guide.md](.claude/skills/skill-creator/references/execution-mode-guide.md)

---

## リソース一覧

| カテゴリ    | 詳細参照                     |
| ----------- | ---------------------------- |
| agents/     | [resource-map.md#agents]     |
| references/ | [resource-map.md#references] |
| scripts/    | [resource-map.md#scripts]    |
| assets/     | [resource-map.md#assets]     |
| schemas/    | [resource-map.md#schemas]    |

📖 [references/resource-map.md](.claude/skills/skill-creator/references/resource-map.md)

---

## 主要エントリポイント

| 用途                     | リソース                             |
| ------------------------ | ------------------------------------ |
| 問題発見                 | agents/discover-problem.md           |
| ドメインモデリング       | agents/model-domain.md               |
| インタビュー             | agents/interview-user.md             |
| リソース選択             | agents/select-resources.md           |
| 要求分析                 | agents/analyze-request.md            |
| スクリプト生成           | agents/design-script.md              |
| オーケストレーション     | agents/design-orchestration.md       |
| クロススキル依存関係解決 | agents/resolve-skill-dependencies.md |
| 外部CLIエージェント委譲  | agents/delegate-to-external-cli.md   |
| マルチスキル同時設計     | agents/design-multi-skill.md         |
| フィードバック記録       | scripts/log_usage.js                 |

---

## 機能別ガイド

| 機能                         | 参照先                                       |
| ---------------------------- | -------------------------------------------- |
| **問題発見フレームワーク**   | references/problem-discovery-framework.md    |
| **ドメインモデリング**       | references/domain-modeling-guide.md          |
| **Clean Architecture**       | references/clean-architecture-for-skills.md  |
| **スクリプト/LLM分担**       | references/script-llm-patterns.md            |
| **クロススキル参照パターン** | references/cross-skill-reference-patterns.md |
| **外部CLIエージェント統合**  | references/external-cli-agents-guide.md      |
| スクリプト生成               | references/script-types-catalog.md           |
| ワークフローパターン         | references/workflow-patterns.md              |
| オーケストレーション         | references/orchestration-guide.md            |
| 実行モード選択               | references/execution-mode-guide.md           |
| ドキュメント生成             | references/api-docs-standards.md             |
| 自己改善サイクル             | references/self-improvement-cycle.md         |
| ライブラリ管理               | references/library-management.md             |

### 追加リファレンス

| カテゴリ | 参照先 |
| --- | --- |
| 基礎設計 | `references/abstraction-levels.md`, `references/core-principles.md`, `references/creation-process.md`, `references/update-process.md`, `references/skill-structure.md`, `references/naming-conventions.md`, `references/quality-standards.md` |
| ヒアリング・設計補助 | `references/interview-guide.md`, `references/goal-to-api-mapping.md`, `references/variable-template-guide.md`, `references/event-trigger-guide.md` |
| 実装・統合 | `references/api-integration-patterns.md`, `references/integration-patterns.md`, `references/integration-patterns-rest.md`, `references/integration-patterns-graphql.md`, `references/integration-patterns-webhook.md`, `references/integration-patterns-ipc.md`, `references/runtime-guide.md`, `references/script-commands.md`, `references/official-docs-registry.md` |
| 実行・運用 | `references/parallel-execution-guide.md`, `references/scheduler-guide.md`, `references/skill-chain-patterns.md`, `references/codex-best-practices.md` |

---

## フィードバック（必須）

実行後は必ず記録：

```bash
node scripts/log_usage.js --result success --phase "Phase 4"
node scripts/log_usage.js --result failure --phase "Phase 3" --error "ValidationError"
```

---

## ベストプラクティス

| すべきこと                          | 避けるべきこと                |
| ----------------------------------- | ----------------------------- |
| 問題を先に特定する（Problem First） | 機能から設計を始める          |
| Core Domainに集中する               | 全体を均等に設計する          |
| Outcomeでゴール定義                 | Outputでゴール定義する        |
| Script優先（決定論的処理）          | 全リソースを一度に読み込む    |
| LLMは判断・創造のみ                 | Script可能な処理をLLMに任せる |
| Progressive Disclosure              | 具体例をテンプレートに書く    |
| クロススキル参照は相対パスで        | 絶対パスやハードコードで参照  |

> **自己参照ノート**: skill-creator自体がクロススキル参照パターンの実例。
> `resolve-skill-dependencies.md` で設計した参照構造は、skill-creatorが他スキルの
> SKILL.mdを読み込んで公開インターフェースを特定する際のパターンそのもの。

---

## 変更履歴

| Version     | Date           | Changes                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| ----------- | -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **10.37.43** | **2026-03-15** | **TASK-SKILL-LIFECYCLE-05 の Phase 12 実績同期ドリフト防止パターンを追加**: `references/patterns.md` に「design タスクでも system spec 更新が発生したら Step 2 を先送りしない」成功/失敗パターンを追記。`phase-12-documentation.md` / `documentation-changelog.md` / `spec-update-summary.md` の同値同期と planned wording 除去を標準手順化し、`LOGS.md` へ同日の更新記録を追加 |
| **10.37.42** | **2026-03-14** | **TASK-IMP-AI-RUNTIME-AUTHMODE-UNIFICATION-001 の Phase 4/6責務分離監査を template 入口へ同期**: `assets/phase12-system-spec-retrospective-template.md` / `assets/phase12-spec-sync-subagent-template.md` に追加した「Phase 4（契約テスト）/ Phase 6（回帰テスト）境界監査」の運用を `references/resource-map.md` へ反映し、template 説明だけ読めば責務分離チェック要件まで辿れるようにした。`LOGS.md` へ同日の実施ログを追加し、再利用手順を trace 可能にした |
| **10.37.41** | **2026-03-13** | **TASK-UI-09-ONBOARDING-WIZARD の統合入口 template を追加**: `assets/phase12-system-spec-retrospective-template.md` に onboarding overlay / Settings rerun / follow-up backlog resweep の反映先マトリクスを追加し、`assets/phase12-spec-sync-subagent-template.md` には canonical docs 7点、既存 follow-up 指示書の current contract 再同期、`workflow-onboarding-wizard-alignment.md` 更新を完了条件として追記。`references/resource-map.md` も同 profile 説明へ同期 |
| **10.37.40** | **2026-03-13** | **TASK-UI-09-ONBOARDING-WIZARD の follow-up drift 再発防止を template 化**: `references/patterns.md` の onboarding Phase 12 パターンへ、既存 `docs/30-workflows/unassigned-task/` 本文の `2.2` / `3.1` / `3.5` / 検証手順を current contract へ再同期する手順を追加。`completed=false reset` のような旧契約を残さず、必要時は `audit-unassigned-tasks --diff-from HEAD --target-file` で個別合否を取る運用を変更履歴へ追記 |
| **10.37.39** | **2026-03-13** | **TASK-SKILL-LIFECYCLE-04 の Phase 12 再確認知見を template 化**: `references/patterns.md` に「既存 IPC 再利用でも public preload / shared export 追加は Step 2 必須」と「未タスク 0 件でも `docs/30-workflows/unassigned-task/` への追加作成なしを明記する」を追加。`assets/phase12-system-spec-retrospective-template.md` / `assets/phase12-spec-sync-subagent-template.md` / `references/resource-map.md` に同判定と完了チェックを追記し、Task04 型の docs-heavy 再監査を短手順化 |
| **10.37.38** | **2026-03-12** | **UT-IMP-WORKSPACE-PARENT-REFERENCE-SWEEP-GUARD-001 の docs-only parent workflow パターンをテンプレート化**: `references/patterns.md` に「pointer / index / spec / script / mirror を 1 sweep で閉じ、screenshot 要求時は representative evidence board を current workflow へ集約する」を追加。`assets/phase12-system-spec-retrospective-template.md` / `assets/phase12-spec-sync-subagent-template.md` / `references/resource-map.md` に `SubAgent-P1..P5`、validator、review board、skill-creator feedback 同期を追記し、親 workflow 再監査の初動を短手順化 |
| **10.37.38** | **2026-03-13** | **TASK-IMP-AIWORKFLOW-REQUIREMENTS-LINE-BUDGET-REFORM-001 の Phase 12 root evidence パターンを追加**: `references/patterns.md` に「shallow PASS 表を root evidence へ昇格し、split 親から sibling backlog まで監査する」を追加。implementation guide 必須要素、未タスク10見出し、current/baseline 分離、`verify-unassigned-links` の sibling aware 実行を 1 パターンへ統合し、docs-heavy task の再監査を短手順化 |
| **10.37.37** | **2026-03-12** | **TASK-IMP-LIGHT-THEME-CONTRAST-REGRESSION-GUARD-001 の Phase 12 再利用パターンを追加**: `references/patterns.md` に「loopback screenshot capture は localhost 不達時に current build static server を自動起動する」を追加し、skill feedback template へ `skill-creator` を含む 3 skill 同値転記ルールを追記。`references/resource-map.md` の Phase 12 template 説明にも loopback static serve fallback と global `unassigned-task/` 二層報告を追加し、再監査の手戻りを減らす |
| **10.37.36** | **2026-03-12** | **TASK-FIX-LIGHT-THEME-SHARED-COLOR-MIGRATION-001 の `spec_created` 再利用パターンを追加**: `references/patterns.md` に「light theme shared color migration は token scope / component scope / verification-only lane を分離する」を追加し、`assets/phase12-system-spec-retrospective-template.md` / `assets/phase12-spec-sync-subagent-template.md` / `references/resource-map.md` に current inventory correction、verification-only wrappers、`ui-ux-settings` / `ui-ux-search-panel` / `ui-ux-portal-patterns` / `rag-desktop-state` / `api-ipc-*` / `security-*` 抽出、Phase 1-3 gate を反映。spec-only UI task の初動を短手順化 |
| **10.37.35** | **2026-03-11** | **TASK-UI-04C の preview/search cross-cutting spec 同期をテンプレート化**: `references/patterns.md` に「workspace preview/search は `ui-ux-search-panel` / `ui-ux-design-system` / `error-handling` / `architecture-implementation-patterns` まで同一ターン同期する」成功/失敗パターンを追加。`assets/phase12-system-spec-retrospective-template.md` / `assets/phase12-spec-sync-subagent-template.md` / `references/resource-map.md` に同 cross-cutting matrix と完了チェックを追記し、PreviewPanel / QuickFileSearch 系タスクの反映先漏れを防ぐ |
| **10.37.34** | **2026-03-11** | **TASK-UI-04C の Phase 12 本文 stale 防止パターンを追補**: `references/patterns.md` の「更新予定のみ残置を排除し、実更新ログへ昇格する」パターンを補強し、completed workflow では `phase-12-documentation.md` に対しても `仕様策定のみ` / `実行予定` / `保留として記録` を grep し、完了条件と `Task 100% 実行確認` を `[x]` へ同期するルールを追加 |
| **10.37.33** | **2026-03-11** | **TASK-UI-04B-WORKSPACE-CHAT の Phase 12再監査知見を template strictness として反映**: `references/patterns.md` に「implementation-guide と coverage matrix の validator 文字列を固定する」パターンを追加。`assets/phase12-system-spec-retrospective-template.md` / `assets/phase12-spec-sync-subagent-template.md` / `assets/phase12-task-spec-recheck-template.md` に `Part 1 の「たとえば」明示` と `phase-11-manual-test.md` の `## 画面カバレッジマトリクス` 固定を機械確認するコマンド・完了チェックを追記し、Phase 12 再監査の warning 再発を抑止 |
| **10.37.32** | **2026-03-11** | **TASK-FIX-LIGHT-THEME-TOKEN-FOUNDATION-001 の global light remediation をテンプレート化**: `references/patterns.md` に「Light Mode 全画面 white/black 基準 + compatibility bridge 固定」を追加し、`assets/phase12-system-spec-retrospective-template.md` / `assets/phase12-spec-sync-subagent-template.md` に renderer-wide hardcoded neutral class 監査、`vitest --shard=<n>/16` による desktop CI 再現、Light Mode 専用 SubAgent-L1..L4、screenshot 再取得後の coverage validator 記録を追記。global theme drift を token 修正だけで終えない Phase 12 運用を標準化 |
| **10.37.31** | **2026-03-11** | **TASK-FIX-LIGHT-THEME-TOKEN-FOUNDATION-001 の completed workflow backlog 配置ルールを反映**: `assets/phase12-spec-sync-subagent-template.md` に「active workflow 由来は `docs/30-workflows/unassigned-task/`、completed workflow 由来は `docs/30-workflows/completed-tasks/<workflow>/unassigned-task/`」の判定と `audit --unassigned-dir ... --target-file ...` を追加。`references/patterns.md` / retrospective template と同粒度で、親 workflow 移管後も PR / spec sync が破綻しないテンプレートへ更新 |
| **10.37.30** | **2026-03-11** | **TASK-FIX-APIKEY-CHAT-TOOL-INTEGRATION-001 のテンプレート最適化を反映**: `assets/phase12-system-spec-retrospective-template.md` に APIキー連動 + チャット経路整合マトリクス（interfaces/llm/api-ipc/security/ui/task/lessons の7責務）を追加。`assets/phase12-spec-sync-subagent-template.md` に同タスク専用 SubAgent プロファイル（A〜F）を追加し、`references/patterns.md` に成功/失敗パターン「APIキー連動3点セット同期（source + llm同期 + cache clear）」を追記。同種課題の初動を workflow 依存なしで短手順化 |
| **10.37.29** | **2026-03-11** | **TASK-UI-07 Phase 12 再監査の dual-root 運用をパターン化**: `references/patterns.md` に「dual skill-root repository の canonical root + mirror sync」を追加し、`.claude/skills/...` を正本、`.agents/skills/...` を mirror として扱う運用を標準化。Phase 12 の spec-update-summary / changelog / feedback に canonical root と mirror sync を併記するルールを固定 |
| **10.37.28** | **2026-03-11** | **TASK-UI-07 を踏まえた Phase 12 UIテンプレート最適化**: `assets/phase12-system-spec-retrospective-template.md` と `assets/phase12-spec-sync-subagent-template.md` の検証コマンドを `.claude` 正本へ統一し、UI current workflow では `ui-ux-components.md` にも `実装内容と苦戦箇所サマリー` を残すルールを追加。`assets/phase12-domain-spec-sync-block-template.md` に UI一覧仕様向けサマリーブロックを追加し、一覧specだけで再利用できる粒度へ改善 |
| **10.37.29** | **2026-03-11** | **TASK-SKILL-LIFECYCLE-01 の feature spec 形成ルールを追加**: `references/patterns.md` に「`ui-ux-feature-components.md` も 3ブロック構成で閉じる」パターンを追加。`assets/phase12-domain-spec-sync-block-template.md` に feature summary spec でも `実装内容（要点）` / `苦戦箇所（再利用形式）` / `同種課題の5分解決カード` をそろえる完了条件を追記し、system spec 単体で再利用可能な file formation を標準化 |
| **10.37.28** | **2026-03-11** | **TASK-SKILL-LIFECYCLE-01 の Phase 12 backlog 分離報告を template 化**: `references/patterns.md` に「`current=0` でも legacy backlog 参照を省略しない」成功/失敗パターンを追加。`assets/phase12-task-spec-recheck-template.md` に `phase12-task-spec-compliance-check.md` を root evidence とし、`baselineViolations>0` 時は既存 remediation task 参照を `unassigned-task-detection.md` へ残す完了条件を追加 |
| **10.37.27** | **2026-03-10** | **TASK-UI-06-HISTORY-SEARCH-VIEW の UI domain spec 形成パターンを反映**: `assets/phase12-domain-spec-sync-block-template.md` に UIドメイン仕様向け拡張ブロックを追加し、`画面の主目的` / `契約上の要点` / `視覚検証` を必須行として明文化。`references/patterns.md` に「UI domain spec は主目的 + 状態契約 + 画面証跡を先に固定する」パターンを追加し、`ui-history-search-view.md` 型の専用 system spec を再利用可能なテンプレートへ昇格 |
| **10.37.26** | **2026-03-10** | **TASK-UI-06-HISTORY-SEARCH-VIEW の canonical root ルールを反映**: `references/cross-skill-reference-patterns.md` に `.claude/skills/` を canonical root、`.agents/skills/` を mirror とする規則を追加。dual-root repo では workflow / outputs が mirror 側 `references/` を正本として書かないこと、`rg -n "\\.agents/skills/.+references"` による簡易監査を行うことを cross-skill 設計ルールへ昇格 |
| **10.37.25** | **2026-03-10** | **TASK-UI-03 の system spec 反映先最適化をテンプレート化**: `references/patterns.md` に「UI current workflow の system spec 反映先を最適化する」パターンを追加。`assets/phase12-system-spec-retrospective-template.md` と `assets/phase12-spec-sync-subagent-template.md` に `ui-ux-components` / `ui-ux-feature-components` / `arch-ui-components` / `ui-ux-design-system` / `task-workflow` / `lessons-learned` の責務マトリクスを追加し、1仕様書=1関心の file formation を標準化 |
| **10.37.24** | **2026-03-10** | **TASK-UI-03 再監査で Phase 12 template drift を是正**: `references/patterns.md` に「backlog 継続前の現物確認」と「component scope / token scope の切り分け」パターンを追加。`references/patterns.md` / `assets/phase12-system-spec-retrospective-template.md` / `assets/phase12-spec-sync-subagent-template.md` の task-spec script path を canonical `.agents/skills/task-specification-creator/scripts/` へ統一し、UI再監査で見つかった token 基盤課題の未タスク formalization を標準化 |
| **10.37.23** | **2026-03-10** | **TASK-FIX-SAFEINVOKE-TIMEOUT-001 の Phase 12再監査知見を skill-creator へ反映**: `references/patterns.md` に「画面検証で露出した副次不具合を即時未タスク化し、`3.5 実装課題と解決策` へ苦戦箇所を継承する」パターンを追加。`assets/phase12-system-spec-retrospective-template.md` / `assets/phase12-spec-sync-subagent-template.md` に screenshot 由来未タスクの formalization、`verify-unassigned-links missing=0` まで閉じる完了条件を追記 |
| **10.37.22** | **2026-03-10** | **TASK-UI-04A Workspace UI 再監査知見を skill-creator へ反映**: `references/patterns.md` に「workspace UI 再監査では current build static serve と 4観点の目視/挙動検証をセットにする」を追加。`assets/phase12-system-spec-retrospective-template.md` / `assets/phase12-spec-sync-subagent-template.md` に current worktree `out/renderer` の static serve、right preview panel reverse resize、watcher callback ref 分離、light theme 補助テキスト contrast 確認を追記し、worktree preview source drift と UI品質取りこぼしを同一テンプレートで防ぐ運用を標準化 |
| **10.37.21** | **2026-03-10** | **TASK-10A-G 再監査で判明した `generate-index` schema 互換問題を skill-creator へ反映**: `references/patterns.md` に「`generate-index` schema 互換監査 + 壊れた index の即時未タスク化」を追加。`assets/phase12-system-spec-retrospective-template.md` / `assets/phase12-spec-sync-subagent-template.md` に `undefined` 混入の検知、手動復旧、未タスク化の完了条件を追記し、自動再生成の誤出力を current task と汎用改善へ責務分離する運用を標準化 |
| **10.37.20** | **2026-03-10** | **TASK-FIX-AUTHGUARD-TIMEOUT-SETTINGS-BYPASS-001 の Phase 12再監査知見を反映**: `references/patterns.md` に「明示 screenshot 要求では plan / metadata / reset guard まで閉じる」を追加。`assets/phase12-system-spec-retrospective-template.md` に worktree preflight `pnpm install --frozen-lockfile`、`screenshot-plan.json` / `phase11-capture-metadata.json` 実在確認、公開ビュー bypass 時の state reset 除外 + nav 到達性チェックを追記し、legacy baseline と今回差分の未タスク判定分離を標準化 |
| **10.37.19** | **2026-03-09** | **TASK-FIX-APP-DEBUG-LOCALSTORAGE-CLEAR-001 の再利用パターンを skill-creator へ反映**: `references/patterns.md` に「persist/auth bug は bug path metadata と screenshot harness を分離する」を追加。`assets/phase12-system-spec-retrospective-template.md` / `assets/phase12-spec-sync-subagent-template.md` に `skipAuth=true` を唯一経路にしないチェックを追記し、Phase 12 の screen evidence と bug-path evidence の責務分離を標準化 |
| **10.37.19** | **2026-03-09** | **TASK-10A-G の Phase 12追補をパターン化**: `references/patterns.md` に「3層テストハードニング戦略」「並列エージェント分割によるPhase実行効率化」「supporting artifact の実測値を summary 文書と同値に固定する」「open backlog はタスク状態に応じた canonical path へ同期して閉じる」を追加。`phase12-task-spec-compliance-check.md` による evidence 集約と `audit --target-file` の completed workflow 対応を標準化 |
| **10.37.18** | **2026-03-09** | **TASK-FIX-AGENT-EXECUTE-SKILL-CONCURRENCY-GUARD-001 の再監査知見を skill-creator へ反映**: `references/patterns.md` に「current workflow 再監査で CLI drift / 未タスク9セクション / skill同期を同時に閉じる」成功パターンと、「BrowserRouter 配下の screenshot harness は descendant route で作る」パターンを追加。workflow 側の `documentation-changelog` / `skill-feedback-report` へ更新した skill 名を残す運用を標準化 |
| **10.37.17** | **2026-03-08** | **TASK-FIX-SUPABASE-FALLBACK-PROFILE-AVATAR-001 の Phase 12教訓をパターン化**: `references/patterns.md` に「fallback error の transport message / UI localized message 分離 + 画面起点の未タスク formalization」を追加。domain spec への責務線追記、`discovered-issues` から未タスク指示書/関連仕様への同一ターン同期、専用 harness route と `currentViolations=0` までの閉じ方を標準化 |
| **10.37.16** | **2026-03-08** | **08-TASK の再発防止パターンを反映**: `references/patterns.md` に「SettingsView 回帰での証跡先行固定（08-TASK）」と失敗パターン「screenshot取得失敗を後追い修正で放置」を追加。Phase 11証跡1:1同期・Phase 12実績記述固定・3仕様同時同期（task-workflow/testing-patterns/lessons）を標準化 |
| **10.37.15** | **2026-03-08** | **TASK-10A-F Phase 12 branch 再確認パターンを追加**: `references/patterns.md` に成功パターン「comparison baseline 正規化つき branch 再監査（TASK-10A-F）」と失敗パターン「current workflow PASS だけで comparison baseline を放置」を追加。あわせてクイックナビの Phase 12 行へ同観点を反映し、`currentViolations=0` と `baselineViolations>0` の二層報告を dual validator gate の前提として固定 |
| **10.37.14** | **2026-03-08** | **Phase 12 branch横断再確認の dual validator gate を標準化**: `references/patterns.md` に「`verify-all-specs` PASS と Phase 12 完了は同義ではない」パターンを追加。完了ゲートを `verify-all-specs` + `validate-phase-output --phase 12` + `validate-phase12-implementation-guide` の3点セットへ固定し、FAIL時は未タスクを `docs/30-workflows/unassigned-task/` へ分離して `audit --target-file` まで同一ターンで実施する運用を明文化 |
| **10.37.13** | **2026-03-07** | **TASK-10A-F の Phase 12再監査知見をパターン化**: `references/patterns.md` に成功パターン「Phase11文書名固定 + TC証跡1:1 + changelog完了記述の三点同期（TASK-10A-F）」と失敗パターン「Phase11文書名ドリフトとTC証跡未同期を放置（TASK-10A-F）」を追加。`validate-phase12-implementation-guide` / `validate-phase11-screenshot-coverage` / `audit --target-file` を再発防止の最小検証セットとして標準化 |
| **10.37.12** | **2026-03-06** | **TASK-10A-E-C の Phase 12再監査知見をパターン化**: `references/patterns.md` に「`documentation-changelog.md` の計画記述残置を排除して実更新ログへ昇格する」パターンと、「未タスク指示書を9見出しテンプレート準拠で作成し `audit --target-file` で個別検証する」パターンを追加。Phase 12 での完了誤判定と未タスクフォーマット逸脱の再発防止を標準化 |
| Version      | Date           | Changes                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| ------------ | -------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **10.37.12** | **2026-03-07** | **TASK-10A-F Store駆動スキルライフサイクルUI統合の仕様同期**: `arch-state-management.md` に Case B方式の状態管理設計を追加。`lessons-learned.md` に Store mock統一パターン等5件の苦戦箇所を追加。`architecture-implementation-patterns.md` に S19（直接IPC→Store移行パターン）を新設。LOGS.md 2ファイル + SKILL.md 2ファイル同時更新（P1/P25/P29対策）                                                                                                                                                                                       |
| **10.37.12** | **2026-03-06** | **TASK-10A-E-C の Phase 12再監査知見をパターン化**: `references/patterns.md` に「`documentation-changelog.md` の計画記述残置を排除して実更新ログへ昇格する」パターンと、「未タスク指示書を9見出しテンプレート準拠で作成し `audit --target-file` で個別検証する」パターンを追加。Phase 12 での完了誤判定と未タスクフォーマット逸脱の再発防止を標準化                                                                                                                                                                                          |
| **10.37.11** | **2026-03-06** | **domain spec 同期ブロックを新設し Phase 12 テンプレートへ接続**: `assets/phase12-domain-spec-sync-block-template.md` を新規追加し、`interfaces` / `api-ipc` / `security` / `ui-ux-feature` などの仕様書へ `実装内容（要点）` / `苦戦箇所（再利用形式）` / `同種課題の5分解決カード` を同粒度で配置する標準ブロックを定義。`phase12-system-spec-retrospective-template.md` / `phase12-spec-sync-subagent-template.md` / `references/resource-map.md` / `references/patterns.md` を更新し、domain spec 側の記述漏れを完了チェックへ組み込んだ |
| **10.37.10** | **2026-03-06** | **TASK-FIX-AUTH-MODE-CONTRACT-ALIGNMENT-001 再監査知見を skill-creator へ反映**: `assets/phase12-system-spec-retrospective-template.md` の重複手順（6.2）を修正し、IPC transport 契約更新時の `references/ipc-contract-checklist.md` / `indexes/quick-reference.md` 同期要件を追加。`assets/phase12-spec-sync-subagent-template.md` へ同 cross-cutting doc / 専用 harness 記録の完了条件を追記し、`references/patterns.md` に auth-mode 由来の成功パターン「shared transport DTO + cross-cutting doc + 専用 harness 同期」を追加             |
| **10.37.9**  | **2026-03-06** | **TASK-043B の Phase 12 運用知見をテンプレートへ同期**: `assets/phase12-system-spec-retrospective-template.md` と `assets/phase12-spec-sync-subagent-template.md` に `phase12-task-spec-compliance-check.md` による root evidence 集約、`currentViolations=0` と `baseline backlog` の二層管理、`audit --target-file` の `scope.currentFiles=1` 確認を追加。`references/patterns.md` に成功パターン「current=0 と baseline backlog の二層管理（TASK-043B）」を追加し、`references/resource-map.md` の説明も同内容へ最適化                    |
| **10.37.11** | **2026-03-07** | **TASK-UI-03 フィードバックレポートテンプレート + フィードバックループ改善**: `references/patterns.md` にスキルフィードバックレポートの4セクション標準テンプレート（ワークフロー改善点/技術的教訓/スキル改善提案/新規Pitfall候補）を追加。`references/feedback-loop.md` に Phase 12 → lessons-learned → Phase 2 テンプレート改善の5ステップフィードバック反映プロセスを追加し、TASK-UI-03 での適用例（Phase 10 MINOR 4件 → Phase 4 a11y テスト推奨）を記録                                                                                   |
| **10.37.10** | **2026-03-06** | **UI Phase 12 を基本6+domain add-on 同期へ拡張**: `assets/phase12-system-spec-retrospective-template.md` と `assets/phase12-spec-sync-subagent-template.md` に `ui-ux-navigation.md` のような domain UI spec を追加 SubAgent で扱う運用を追記。`references/resource-map.md` と `references/patterns.md` に「UI基本6仕様書だけ更新して domain UI spec を未同期」失敗パターンを追加し、UI仕様同期漏れの再発を防止                                                                                                                              |
| **10.37.9**  | **2026-03-06** | **TASK-UI-02 再々監査の workflow 本文 stale 是正パターンを追加**: `references/patterns.md` に「workflow 本文 `phase-1..11` の completed 同期（TASK-UI-02）」を追加。`assets/phase12-system-spec-retrospective-template.md` と `assets/phase12-spec-sync-subagent-template.md` に completed 扱いの Phase 本文へ `pending` が残っていないことを確認する `rg` コマンドと完了チェックを追記し、Phase 12 の三層同期（成果物 / 台帳 / 本文仕様書）を標準化                                                                                         |
| **10.37.8**  | **2026-03-06** | **TASK-UI-02 の Phase 12 再整合パターンを追加**: `references/patterns.md` に「workflow index / artifacts 二重同期」を追加。`assets/phase12-system-spec-retrospective-template.md` と `assets/phase12-spec-sync-subagent-template.md` に `outputs/artifacts.json` 同期、`generate-index.js --workflow ... --regenerate`、`index.md` 状態確認を追記し、workflow 表示ドリフトを再発防止                                                                                                                                                         |
| **10.37.8**  | **2026-03-06** | **SKILL.md の直接参照導線を最適化**: `references/overview.md` / `core-principles.md` / `creation-process.md` / `update-process.md` / `skill-structure.md` / `naming-conventions.md` / `quality-standards.md` など未リンクだった reference 群を、基礎設計・ヒアリング・実装・統合・運用の5カテゴリへ再編して `SKILL.md` から直接辿れる構造へ更新。`resource-map.md` 依存だけでは残っていた `quick_validate` warning 26件を解消し、Progressive Disclosure と validator の整合を取った                                                          |

| **10.37.7** | **2026-03-06** | **Phase 12テンプレートを台帳二重突合前提へ最適化**: `assets/phase12-system-spec-retrospective-template.md` と `assets/phase12-spec-sync-subagent-template.md` に `phase-12-documentation.md` の `ステータス=completed` + Task 12-1〜12-5 `[x]` 確認コマンド/完了チェックを追加。`references/resource-map.md` の重複テンプレート行を統合し、参照導線を1資産1行へ整理してファイル形成を最適化 |
| **10.37.6** | **2026-03-05** | **TASK-FIX-SKILL-EXECUTOR-AUTHKEY-DI-001 の Phase 12台帳ドリフト防止を追加**: `references/patterns.md` に「成果物実体と `phase-12-documentation.md` 状態の二重突合」成功パターンを追加。Task 12-1〜12-5 実体確認 + `verify-all-specs`/`validate-phase-output` 再実行 + 仕様書ステータス同期を1セットで完了判定する運用を標準化 |
| **10.37.7** | **2026-03-06** | **Phase 12テンプレートのファイル形成を最適化（TASK-INVESTIGATE追補）**: `assets/phase12-system-spec-retrospective-template.md` の重複手順（6.2の手順5重複）と重複検証コマンド（`validate-phase11-screenshot-coverage` 重複）を解消。`assets/phase12-system-spec-retrospective-template.md` / `assets/phase12-spec-sync-subagent-template.md` に「テンプレート重複行なし」完了チェックを追加し、再利用時の記述ドリフトを防止 |
| **10.37.6** | **2026-03-06** | **TASK-INVESTIGATE の再監査知見を skill-creator へ反映**: `references/patterns.md` に「ユーザー要求時の `NON_VISUAL`→`SCREENSHOT` 昇格運用（TASK-INVESTIGATE）」を追加。`assets/phase12-system-spec-retrospective-template.md` / `assets/phase12-spec-sync-subagent-template.md` の完了チェックへ同ルールを追記し、Phase 12 再確認時の画面証跡不足を予防する運用を標準化 |
| **10.37.4** | **2026-03-05** | **Phase 12再監査の対象テスト実行ガードを追加（TASK-UI-01-C）**: `references/patterns.md` に「`pnpm run test:run --` で全体テストへ展開される失敗パターン」と「`pnpm exec vitest run <対象ファイル>` を正とする成功パターン」を追加。再監査ログへ `N files / M tests` の実測固定を残す運用を標準化し、再確認時の時間ロスを抑止 |
| **10.37.5** | **2026-03-05** | **TASK-FIX-AUTH-KEY-HANDLER-REGISTRATION-001 の運用ガードをテンプレートへ反映**: `references/patterns.md` に「長時間fixtureテスト一括実行でSIGTERMを再発させる」失敗パターンを追加し、`assets/phase12-system-spec-retrospective-template.md` / `assets/phase12-spec-sync-subagent-template.md` に `apps/desktop test:run` 失敗時の `vitest run` 分割フォールバック記録を必須化。`resource-map.md` へ同要件を同期し、Phase 12 完了判定を「runtime配線対称性 + 分割回帰証跡」まで拡張 |
| **10.37.4** | **2026-03-05** | **TASK-FIX-AUTH-KEY-HANDLER-REGISTRATION-001 の再発防止パターンを追加**: `references/patterns.md` の Phase 12 ドメインへ「auth-key既存チャネルの register/unregister 対称性崩れ」パターンを追加。`No handler registered` 再発条件、`handler + register + unregister + lifecycleテスト` の4点完了条件、`task-workflow`/`lessons` 同時同期ルールを標準化 |
| **10.37.3** | **2026-03-05** | **Phase 12テンプレートを最適化（`target-file` 境界の明確化）**: `assets/phase12-system-spec-retrospective-template.md` と `assets/phase12-spec-sync-subagent-template.md` の監査手順を更新し、`--target-file` は `docs/30-workflows/unassigned-task/` 配下のみ許可する運用へ統一。`references/resource-map.md` も同条件へ同期し、`current/baseline` 分離判定の説明をテンプレート本体に固定 |
| **10.37.2** | **2026-03-05** | **TASK-UI-01-A Phase 12再監査パターンを追加**: `references/patterns.md` に成功パターン「`--target-file` は `docs/30-workflows/unassigned-task/` 配下限定 + `current/baseline` 分離判定」を追加。成果物監査を `--diff-from HEAD` へ切り替える運用と、baseline負債を別未タスクへ切り出す手順を標準化し、Phase 12 未タスク監査の誤用を抑止 |
| **10.37.1** | **2026-03-05** | **UT-TASK-10A-B-001 再利用最適化テンプレートを追加**: `assets/phase12-system-spec-retrospective-template.md` / `assets/phase12-spec-sync-subagent-template.md` を更新し、配置先3分類（未実施=`unassigned-task` / 完了済みUT=`completed-tasks` / legacy=`completed-tasks/unassigned-task`）と `target-file` 適用境界（unassigned系のみ）を明文化。`references/resource-map.md` と `references/patterns.md` も同期し、完了済みUT監査誤用の再発防止を標準化 |
| **10.37.0** | **2026-03-05** | **UT-TASK-10A-B-001 最終再監査パターンを追加**: `references/patterns.md` に成功パターン「完了済みUT指示書を `completed-tasks` 直下へ移管し、未実施UTを `unassigned-task` へ分離」と失敗パターン「完了済み指示書への `--target-file` 監査誤適用」を追加。Phase 12再監査での配置ドリフトと scoped監査誤用を同時防止する運用を標準化 |
| **10.36.9** | **2026-03-04** | **Phase 11証跡の workflow 配置ドリフト対策をテンプレートへ追加**: `assets/phase12-system-spec-retrospective-template.md` と `assets/phase12-spec-sync-subagent-template.md` に「視覚TC=`screenshots/*.png` / 非視覚TC=`NON_VISUAL:`」の証跡記法チェックを追加し、対象workflow配下 `outputs/phase-11/screenshots` 前提を完了条件へ固定。`references/patterns.md` に失敗パターン「別workflow証跡参照のまま coverage validator 実行」と成功パターン「対象workflow配下への証跡正規配置 + NON*VISUAL 記法固定」を追記 |
| **10.36.8** | **2026-03-04** | **workflow02 の screenshot Port 競合ガードを Phase 12 パターンへ追加**: `references/patterns.md` のクイックナビ（📋 Phase 12）へ成功キーワード「UI再撮影前ポート競合preflight（5174）+ 分岐記録固定」と失敗キーワード「Port 5174 競合ログ混在を未記録のまま完了判定」を追記。成功/失敗パターン本文も追加し、`lsof` 事前検査 + 分岐記録 + 未タスク化の導線を標準化 |
| **10.36.7** | **2026-03-04** | **Phase 12テンプレートへ未タスク配置先判定ガードを追補**: `assets/phase12-system-spec-retrospective-template.md` と `assets/phase12-spec-sync-subagent-template.md` に「未完了は `docs/30-workflows/unassigned-task/`、完了移管済みは `docs/30-workflows/completed-tasks/unassigned-task/`」の判定手順・検証コマンド・完了チェックを追加。`references/resource-map.md` のテンプレート説明も同基準へ同期し、配置先混同による再監査差し戻しを防止 |
| **10.36.6** | **2026-03-04** | **Phase 12テンプレートへ preview preflight 既定手順を同期**: `assets/phase12-system-spec-retrospective-template.md` と `assets/phase12-spec-sync-subagent-template.md` の検証コマンド/完了チェックへ `preview` build + `127.0.0.1:4173` 疎通確認、失敗時未タスク化分岐を追加。`references/resource-map.md` のテンプレート説明と `references/patterns.md`（SkillCenter成功/失敗パターン）を同時更新し、テンプレートと運用パターンのドリフトを解消 |
| **10.36.5** | **2026-03-04** | **SkillCenter 再撮影ブロッカーの Phase 12 パターンを追加**: `references/patterns.md` の Phase 12 クイックナビへ成功キーワード「UI再撮影前preview preflight + 失敗時未タスク化固定」と失敗キーワード「preview成否確認なしで再撮影開始（ERR_CONNECTION_REFUSED）」を追加。成功/失敗パターン本文も追補し、`UT-IMP-SKILL-CENTER-PREVIEW-BUILD-GUARD-001` へ接続する再発防止導線を標準化 |
| **10.36.4** | **2026-03-04** | **Phase 12再監査の3workflow+未タスク個別監査パターンを追加**: `references/patterns.md` に成功パターン「3workflow再監査 + 未タスク個別監査の二段固定（TASK-FIX-SKILL-IMPORT 3連続是正）」を追加。`verify-all-specs`/`validate-phase-output` の束ね実行、`verify-unassigned-links` + `audit --diff-from HEAD` の全体判定、`audit --target-file` の `scope.currentFiles` 判定固定を標準化 |
| **10.36.3** | **2026-03-04** | **Phase 12 テンプレートに仕様書別SubAgent実行ログを追加**: `assets/phase12-system-spec-retrospective-template.md` と `assets/phase12-spec-sync-subagent-template.md` に「実装内容/苦戦箇所/検証証跡」を仕様書単位で残す実行ログ欄を追加。`references/phase-completion-checklist.md` に同ログの完了条件を追記し、`references/resource-map.md` のテンプレート説明を同期更新 |
| **10.36.2** | **2026-03-04** | **Phase完了チェックを再発防止強化**: `references/phase-completion-checklist.md` の Phase 6 完了条件に「未タスク監査の current/baseline 分離記録」と「画面証跡の状態名+検証目的記録」を追加。検証コマンドへ `audit-unassigned-tasks --json --diff-from HEAD` と baseline監視コマンドを追記し、Phase 12再確認時の誤判定を防止 |
| **10.36.1** | **2026-03-03** | **TASK-10A-C 仕様転記ガードを追補**: `assets/phase12-system-spec-retrospective-template.md` に「標準5仕様書転記チェック（interfaces/api-ipc/security/task/lessons）」を追加し、各仕様書へ「実装内容 + 苦戦箇所 + 簡潔手順」を必須化。`references/patterns.md` の TASK-10A-C 成功パターンへ同最終チェックを追加し、`references/resource-map.md` のテンプレート説明を同期更新 |
| **10.36.0** | **2026-03-02** | **TASK-10A-C 再監査運用をテンプレート化**: `references/patterns.md` に成功パターン「UI再撮影 + TCカバレッジ検証の同時固定（TASK-10A-C）」と失敗パターン「UI再撮影後にTCカバレッジ検証を省略」を追加。`assets/phase12-system-spec-retrospective-template.md` の検証コマンドに `screenshot:<feature>` と `validate-phase11-screenshot-coverage` を追加し、UI完了チェックへ `coverage PASS` を必須化。`references/resource-map.md` も UI再撮影 + TCカバレッジ対応へ同期更新 |
| **10.35.0** | **2026-03-02** | **TASK-10A-B再監査パターン + テンプレート重複整理**: `references/patterns.md` のクイックナビ（📋 Phase 12）重複行を統合し、成功/失敗キーワードへ「Phase 11実画面証跡の当日再取得」「Phase 11必須節検証（統合テスト連携/完了条件）」「未タスク件数再計算（7→5是正）」を追加。成功パターン「Phase 11 実画面証跡 + 必須節検証固定（TASK-10A-B）」を新設。`assets/phase12-system-spec-retrospective-template.md` の `SubAgent分担` 重複行を解消し、Phase 11必須節確認コマンドとUI再撮影鮮度チェックをテンプレート標準へ追加 |
| **10.34.0** | **2026-03-02** | **Phase 12テンプレート最適化（2workflow同時監査 + 画面証跡）**: `assets/phase12-system-spec-retrospective-template.md` に 2workflow同時監査プロファイル（spec_created + completed）と UI画面証跡チェックを追加。`assets/phase12-spec-sync-subagent-template.md` に再確認向けSubAgent分担（workflow-a/workflow-b/unassigned/spec/lessons）を追加し、`references/resource-map.md` のテンプレート説明を同期更新 |
| **10.33.0** | **2026-03-02** | **Phase 12再確認パターン強化（2workflow同時監査）**: `references/patterns.md` に成功パターン「2workflow同時監査 + Task 1/3/4/5実体突合（TASK-UI-05A/TASK-UI-05）」と失敗パターン「spec_created/完了workflow混在時の証跡分散」を追加。クイックナビ（📋 Phase 12）へ同キーワードを反映し、`currentViolations=0` 判定固定の再利用導線を更新 |
| **10.34.0** | **2026-03-02** | **TASK-UI-05B 仕様書別SubAgent最適化**: `assets/phase12-system-spec-retrospective-template.md` と `assets/phase12-spec-sync-subagent-template.md` の UIプロファイルを「1仕様書=1SubAgent」の6責務（ui-ux-components / ui-ux-feature-components / arch-ui-components / arch-state-management / task-workflow / lessons）へ更新。`references/patterns.md` に成功パターン「UI6仕様書を1仕様書1SubAgentで同期固定」を追加し、失敗パターン「UI6仕様書を束ねて責務境界が曖昧」を追記 |
| **10.33.0** | **2026-03-02** | **TASK-UI-05B 再確認パターン追加**: `references/patterns.md` の Phase 12 に成功パターン「依存成果物参照補完 + 画面再撮影固定（TASK-UI-05B）」を追加。クイックナビへ同キーワードを反映し、失敗パターン「verify-all-specs warningドリフト放置」「UI再確認で既存スクショ存在確認のみ」を追記。Phase 12 再確認時の `current/baseline` 分離記録を標準運用に固定 |
| **10.32.0** | **2026-03-01** | **TASK-UI-05 向けテンプレート最適化（UIプロファイル対応）**: `assets/phase12-system-spec-retrospective-template.md` と `assets/phase12-spec-sync-subagent-template.md` を更新し、UI機能実装の6仕様書プロファイル（`ui-ux-components` / `ui-ux-feature-components` / `arch-ui-components` / `arch-state-management` / `task-workflow` / `lessons-learned`）を追加。`references/resource-map.md` を同期し、`references/patterns.md` へ成功/失敗パターン（UI6仕様書テンプレート適用・5仕様書誤適用）を追記 |
| **10.31.0** | **2026-03-01** | **TASK-UI-05 Phase 12 再利用パターン追加**: `references/patterns.md` に成功パターン「UI機能実装の未タスク6件分解 + 二段監査固定（TASK-UI-05）」と失敗パターン「task-workflow のみ更新で lessons-learned 同期漏れ（TASK-UI-05）」を追加。クイックナビの Phase 12 成功/失敗キーワードを同期し、未タスク運用（target監査 + diff監査）と台帳/教訓同時更新を標準化 |
| **10.30.0** | **2026-02-28** | **Phase 12テンプレートをSubAgent責務分離向けに最適化**: `assets/phase12-system-spec-retrospective-template.md` に「仕様書適用判定ログ（更新/N/A/理由/代替証跡）」と「実行可否ゲート（三点突合）」を追加。`references/patterns.md` へ成功パターン「仕様書単位SubAgent + N/A判定ログ固定」と失敗パターン「非対象仕様（N/A）の記録漏れ」を反映し、仕様書ごとの説明責任を標準化 |
| **10.29.0** | **2026-02-28** | **Phase 12 実行可否判定パターンを追加**: `references/patterns.md` に成功パターン「実行可否判定の三点突合（チェックリスト/成果物/artifacts）」を追加。成果物実体のみで完了判定しない運用を標準化し、再監査時の未同期差し戻しを防止 |
| **10.28.0** | **2026-02-28** | **TASK-FIX-AUTH-CALLBACK-SERVER-WORKER-EXIT-001 パターン追加**: `references/patterns.md` の Phase 12 へ成功パターン「待機API/停止API責務分離の仕様固定」を追加し、失敗パターン「timeout待機APIへの停止副作用混在」を追記。クイックナビへ同名キーワードを登録し、`phase12-system-spec-retrospective-template` 準拠で SubAgent 分担・検証証跡固定の運用を標準化 |
| **10.27.0** | **2026-02-27** | **TASK-9H 再発防止パターン追加**: `references/patterns.md` の Phase 12 ドメインへ「phase-12仕様書ステータス同期（未実施→完了）」成功パターンと「phase-12仕様書ステータス未更新」失敗パターンを追加。`phase-12-documentation.md` と `spec-update-summary.md` の二重台帳同期手順を明文化 |
| **10.26.0** | **2026-02-27** | **Phase 12 テンプレート準拠最適化（文書構造整理）**: `references/patterns.md` のクイックナビ重複行（Phase 12 / IPC）を統合し、探索性を改善。`phase12-system-spec-retrospective-template.md` 運用に合わせて `spec-update-summary.md` 生成を標準化し、SubAgent分担・苦戦箇所・検証証跡を1ファイルで再利用可能にする手順を追補 |
| **10.25.0** | **2026-02-27** | **Phase 12 親タスク参照同期パターン追加**: `references/patterns.md` に「完了移管後の親タスク証跡参照同期（UT-IMP-QUICK-VALIDATE-EMPTY-FIELD-GUARD-001）」を追加。`completed-tasks/` 配下の親子参照ドリフトを `rg` で検出し、運用ドキュメントのみ更新・監査生ログは保持する運用を標準化。`verify-unassigned-links` + `audit --diff-from HEAD` の再確認手順を明記 |
| **10.26.0** | **2026-02-27** | **Phase 12 システム仕様同期テンプレートを仕様書別SubAgent運用へ最適化**: `assets/phase12-system-spec-retrospective-template.md` を更新し、SubAgent分担を `interfaces/api-ipc/security/task-workflow/lessons` の5責務へ拡張。`spec-update-summary.md` の固定化、`audit-unassigned-tasks --diff-from HEAD` の必須検証、成果物チェックの `unassigned-task-report.md` 対応を追加。あわせて `references/resource-map.md` の説明を同期し、`references/patterns.md` に成功パターン「仕様書別SubAgent同期 + spec-update-summary 固定化（TASK-9F追補）」を追加 |
| **10.25.0** | **2026-02-27** | **Phase 12 未タスク運用ガードを追加**: `references/patterns.md` に成功パターン「未タスクの配置・命名・9セクション同時是正（TASK-9F）」を追加。`docs/30-workflows/unassigned-task/` 正本配置、テンプレート準拠、`task-workflow.md`/`unassigned-task-report.md` 同期、`audit-unassigned-tasks --diff-from HEAD` による `currentViolations` 判定を標準手順化 |
| **10.27.0** | **2026-02-28** | **Phase 12テンプレート最適化（TASK-9I再利用強化）**: `assets/phase12-system-spec-retrospective-template.md` に再確認タスク向けSubAgent分担（A:task-workflow/B:lessons/C:unassigned/D:検証）を追加。未タスク品質ゲートを `10見出し（## メタ情報 + ## 1..9）` と `audit --target-file` の `currentViolations=0` に統一し、成果物チェックの標準を `unassigned-task-detection.md` 優先へ正規化 |
| **10.26.0** | **2026-02-28** | **TASK-9I Phase 12再確認パターン追加**: `references/patterns.md` の Phase 12 ドメインに成功パターン「target監査 + 10見出し同時検証（TASK-9I再確認）」と失敗パターン「未タスクの存在確認止まり（10見出し未検証）」を追加。`audit-unassigned-tasks --target-file` の `current` 判定と、UT指示書10見出し/`メタ情報` 検証を同時実施する運用を標準化 |
| **10.26.1** | **2026-02-28** | **Phase 12 SubAgent同期テンプレート最適化（TASK-9J反映）**: `assets/phase12-spec-sync-subagent-template.md` を 5仕様書分担（interfaces/api-ipc/security/task-workflow/lessons）へ拡張し、`handler/register/preload` 三点突合を必須工程として追加。`references/patterns.md` に成功パターン「5仕様書同期 + IPC三点突合テンプレート」と失敗パターン「api-ipc仕様を同期対象から除外」を追記し、`references/resource-map.md` のテンプレート説明を同期更新 |
| **10.26.0** | **2026-02-28** | **TASK-9J再監査パターン追補**: `references/patterns.md` に成功パターン「IPC追加時の登録配線突合（handler/register/preload）」と失敗パターン「IPCハンドラ実装のみで登録配線を未確認」を追加。Phase 12 クイックナビへ同パターンを反映し、IPC追加時の起動経路漏れ再発を防止 |
| **10.25.1** | **2026-02-27** | **Phase 12/IPC クイックナビ重複整理**: `references/patterns.md` のクイックナビゲーションで重複していた `📋 Phase 12` と `🔌 IPC・アーキテクチャ` 行を統合。成功/失敗パターンの一覧を単一行へ正規化し、`仕様書別SubAgent同期テンプレート` / `IPC契約ブリッジ` など最新パターンを欠落なく保持 |
| **10.25.0** | **2026-02-27** | **UT-FIX-SKILL-IPC-RESPONSE-CONSISTENCY-001 再監査パターン追補**: `references/patterns.md` に成功パターン「IPCドキュメント契約同期（Main/Preload準拠）」と失敗パターン「IPC契約ドキュメントを概要のみで確定」を追加。Phase 12 Step 2で `ipc-documentation.md` の引数/戻り値/エラー契約を実装シグネチャへ同期し、契約テストで回帰確認する運用を標準化 |
| **10.24.0** | **2026-02-26** | **Phase 12 system-spec retrospective template最適化**: `assets/phase12-system-spec-retrospective-template.md` を汎用ドメイン仕様向けに更新（`ui-ux-design-system.md` 固定参照を `<domain-spec>.md` 化、SubAgent分担を `A:台帳 / B:ドメイン仕様 / C:教訓 / D:検証` に整理、`quick_validate.js` を repo 相対コマンドへ正規化、成果物名を `unassigned-task-detection.md` に同期）。`references/resource-map.md` の用途説明も同時更新 |
| **10.24.0** | **2026-02-26** | **Phase 12 未タスクフォーマット再発防止を追加**: `references/patterns.md` の Phase 12 成功/失敗パターンへ「未タスクメタ情報1セクション運用 / 未タスク指示書メタ情報の二重定義」を追加。`task-specification-creator` の `unassigned-task-guidelines.md` とクロスリファレンスし、`rg -n "^## メタ情報"` による機械監査手順を標準化 |
| **10.23.0** | **2026-02-25** | **Phase 12 仕様書別SubAgent同期テンプレートを追加**: `assets/phase12-spec-sync-subagent-template.md` を新規作成し、`references/resource-map.md` に登録。`references/patterns.md` に成功パターン「仕様書別SubAgent同期テンプレート」と失敗パターン「仕様書更新の単独進行による同期漏れ」を追加し、クイックナビへ反映 |
| **10.22.0** | **2026-02-25** | **Phase 12再確認パターンを追加**: `references/patterns.md` の Phase 12 ドメインに成功パターン2件（scoped監査の`current`判定固定、`validate-phase-output`位置引数固定）と失敗パターン2件（`--target-file`誤解、`validate-phase-output --phase`誤用）を追加。監査ログ読解ミスによる過剰修正を防止する運用を標準化 |
| **10.21.0** | **2026-02-25** | **UT-FIX-SKILL-EXECUTE-INTERFACE-001 パターン反映**: `references/patterns.md` の IPC ドメインに成功パターン「IPC契約ブリッジ（正式契約 + 後方互換）」と失敗パターン「正式契約切替時の後方互換欠落」を追加。クイックナビ（IPC成功/失敗）にも反映し、契約移行時の互換維持設計を標準化 |
| **10.20.0** | **2026-02-25** | **Phase 12 action-bridgeテンプレート新設**: `assets/phase12-action-bridge-template.md` を追加し、監査結果を優先度/Wave/SubAgent/outputsへ即変換する標準フォーマットを提供。`references/resource-map.md` の assets に登録し、`references/patterns.md` の「監査結果→次アクションブリッジ」へテンプレート適用手順を追記 |
| **10.19.0** | **2026-02-25** | **TASK-013再監査の実行導線パターン追加**: `references/patterns.md` の Phase 12 に成功パターン「監査結果→次アクションブリッジ（task-00導線化）」と失敗パターン「監査結果の棚卸し止まり（次アクション未定義）」を追加。再監査結果を優先度/Wave/SubAgent分担へ直結する運用を標準化 |
| **10.18.0** | **2026-02-25** | **UT-FIX-SKILL-IPC-RESPONSE-CONSISTENCY-001 再監査パターン追記**: `references/patterns.md` の Phase 12 に成功パターン「実装ガイド2パート要件ギャップの即時是正」と失敗パターン「Part 1/Part 2必須要件の欠落」を追加。クイックナビゲーションへ反映し、Task 1要件不足の再発防止を明文化 |
| **10.17.0** | **2026-02-24** | **UT-IPC-DATA-FLOW-TYPE-GAPS-001 パターン追加**: references/patterns.md の Phase 12 に成功パターン「spec-update-summary + artifacts二重台帳同期」を追加。クイックナビ更新と失敗パターン「spec-update-summary未作成/artifacts台帳非同期」を追記し、成果物不足と台帳ズレの再発防止を明文化 |
| **10.16.0** | **2026-02-24** | **UT-FIX-SKILL-VALIDATION-CONSISTENCY-001 パターン追加**: references/patterns.md にIPC成功パターン2件（P42準拠バリデーション一括移行・引数形式差異のYAGNI共通化判断）+ Phase 12失敗パターン1件（サブエージェント出力非永続化）追加。クイックナビゲーション更新 |
| **10.15.0** | **2026-02-24** | **UT-SKILL-IMPORT-CHANNEL-CONFLICT-001 パターン追加**: references/patterns.md に成功パターン3件（IPCチャネル名競合予防・仕様書修正タスクPhaseテンプレート・grepベース仕様書TDD）+ 失敗パターン1件（Phase4修正箇所数の事前検証不足）追加。クイックナビゲーション更新 |
| **10.14.0** | **2026-02-23** | **TASK-UI-00-ATOMS パターン反映**: references/patterns.md にUI/フロントエンドドメイン成功パターン3件（Props駆動設計・Record型バリアント・テーマ横断テスト）+ 失敗パターン2件（HTMLAttributes型衝突・Props命名ドリフト）を追加 |
| **10.13.1** | **2026-02-23** | **TASK-IMP-MODULE-RESOLUTION-CI-GUARD-001 パターン追加**: patterns.md に成功パターン2件（CIガード自動検証、正規表現TS設定パーサー）+ 失敗パターン1件（AST解析過剰設計）を追加。クイックナビゲーション更新 |
| **10.13.0** | **2026-02-22** | **TASK-IMP-MODULE-RESOLUTION-CI-GUARD-001 パターン反映**: references/patterns.md の Phase 12 ドメインに成功パターン「全体監査と対象差分の分離報告」と失敗パターン「全体ベースライン違反の今回起因誤判定」を追加。既存違反と今回差分の切り分け手順（baseline/scope-of-change）を明文化 |
| **10.12.0** | **2026-02-22** | **UT-FIX-SKILL-IMPORT-ID-MISMATCH-001 パターン反映**: references/patterns.md に成功パターン「Renderer層 id→name 契約変換」と失敗パターン「Renderer層での識別子混同（id/name）」を追加。クイックナビゲーションの IPC・アーキテクチャ行を更新 |
| **10.11.2** | **2026-02-21** | **UT-FIX-SKILL-IMPORT-INTERFACE-001 再監査パターン反映**: references/patterns.md に Phase 12 成功パターン「成果物ログとStep判定の同期（先送り禁止）」を追加。クイックナビに同パターンを反映し、失敗パターン「Step2該当なし誤判定 / Phase 13先送り記載」を追記 |
| **10.11.1** | **2026-02-20** | **UT-FIX-SKILL-REMOVE-INTERFACE-001 教訓反映**: references/patterns.md に Phase 12 成功パターン「未実施タスク配置ドリフト是正（completed-tasks/unassigned-task → unassigned-task）」を追加。クイックナビゲーションに同パターンを反映し、失敗パターン「未実施タスクの completed-tasks 配置混入」を明文化 |
| **10.11.0** | **2026-02-20** | **TASK-FIX-TS-SHARED-MODULE-RESOLUTION-001 Phase 12再監査パターン反映**: references/patterns.md に成功パターン「Phase 12 実行仕様書ステータス同期」を追加。成果物生成済みでも `phase-12-documentation.md` 本体のステータス/チェックリスト未同期が残る失敗を再発防止対象として明文化 |
| **10.10.0** | **2026-02-19** | **TASK-FIX-10-1 仕様最適化パターン追加**: references/patterns.md に Phase 12 成功パターン「仕様更新三点セット（quality/task-workflow/lessons-learned）」を追加。クイックナビゲーションのPhase 12ドメインを更新し、再利用性の高い仕様反映手順を明文化 |
| **10.9.1** | **2026-02-19** | **TASK-FIX-10-1-VITEST-ERROR-HANDLING 教訓反映**: references/patterns.md のテストドメインを更新。成功パターン「Vitest未処理Promise拒否の可視化運用」と失敗パターン「dangerouslyIgnoreUnhandledErrors 常時有効化」を追加し、クイックナビゲーションへ反映 |
| **10.9.0** | **2026-02-19** | **TASK-9A-B再監査パターン追加**: references/patterns.md に「[Phase12] 実装-仕様ドリフト再監査（数値・パス・文言）」を追加。テスト件数の実測値基準化、旧パス（`skill-file-api.ts`）横断修正、未タスクraw件数と確定件数の分離記録を標準化 |
| **10.9.0** | **2026-02-19** | **TASK-9A-C Phase 12再監査パターン追補**: references/patterns.md に成功パターン「仕様書作成タスクの `spec_created` 状態判定」を追加。失敗パターン「仕様書作成タスクの completed 誤判定」を追加し、Phase 12クイックナビゲーションに反映 |
| **10.8.0** | **2026-02-14** | **UT-FIX-IPC-RESPONSE-UNWRAP-001 教訓反映**: references/patterns.md に「Phase 12 仕様書参照パスの実在チェック」パターンを追加（`test -f` による更新対象仕様書の事前検証、非実在参照の即時是正、index再生成のセット運用） |
| **10.7.0** | **2026-02-14** | **TASK-FIX-14-1 Phase 12再監査パターン追加**: references/patterns.mdに成功パターン「実装差分ベース文書化（ファイル名誤記防止）」を追加。失敗パターン「実装ガイドへの誤ファイル名混入（TASK-FIX-14-1）」を追加。クイックナビゲーションのPhase 12行を更新 |
| **10.6.1** | **2026-02-14** | **UT-FIX-IPC-HANDLER-DOUBLE-REG-001 パターン追補**: references/patterns.md のクイックナビに「IPCハンドラライフサイクル管理（unregister→register）」を追加。新規パターン「[IPC] IPCハンドラライフサイクル管理パターン（UT-FIX-IPC-HANDLER-DOUBLE-REG-001）」を追記し、IPC_CHANNELS全走査前提確認・IPC外リスナー解除（themeWatcher）・順序固定（unregister→createWindow→register）・`ipcMain.handle()`/`ipcMain.on()`挙動差を明文化 |
| **10.6.0** | **2026-02-14** | **LLM System Promptテンプレート追加**: assets/system-prompt-template.md新規作成（LLM外部呼び出し用System Promptフォーマット: あなたの役割/目的/背景/成功基準/用語定義/手順/出力フォーマット/制約条件の8セクション構造、Handlebars変数対応、セクション設計ガイドライン、使用例付き）。references/output-patterns.mdに§5.3「LLM System Promptパターン」セクション追加・assets/との連携ツリー更新。references/resource-map.mdにsystem-prompt-template.mdエントリ追加。agents/select-resources.mdに§4.1.4.1「LLM System Prompt生成→追加アセット」選択条件追加 |
| **10.5.0** | **2026-02-13** | **ラウンド3リファクタリング（修正）**: script-types-catalog.md全24テンプレート参照修正（存在しないassets/*.js/_.py/_.sh→実在のassets/type-\_.md+base-*.{js,py,sh}形式）、interview-user.mdにPhaseラベル追加（Phase 0-1〜0-8）、resource-map.mdのinterview-user.mdエントリにPhase情報追加、phase-completion-checklist.mdのPhase 5/6に「担当スクリプト」セクション追加、SKILL.md v10.4.0 changelogファイル数修正（17→16）、scripts/ DRY違反修正（19スクリプト: getArg/resolvePath/EXIT\_*定数をutils.jsからimportに統一 — generate*agent/generate_script/generate_skill_md/generate_dynamic_code/detect_runtime/collect_feedback/validate_all/validate_plan/validate_workflow/apply_updates/apply_self_improvement/analyze_prompt/update_skill_list/assign_codex/check_prerequisites/init_skill + execute_chain/execute_parallel/validate_orchestrationのbare exit code統一）、generate_script.jsテンプレート本体のEXIT\*\*→EXIT_CODES.*統一、validate_all.jsのnormalizeLink()ローカル重複定義をutils.jsからのimportに統一、delegate-to-codex.md §5.5残留integrate-results参照修正 |
| **10.4.0** | **2026-02-13** | **ラウンド2リファクタリング（27件修正）**: phase-completion-checklist.md完全書き換え（task-specification-creator用→skill-creator用Phase 0-0〜6対応）、creation-process.mdにCollaborativeモード追加、SKILL.md重複バージョン統合（v9.4.0/v9.3.0/v9.1.0各2行→1行）、全エージェントへのPhaseラベル追加（16ファイル: discover-problem/model-domain/extract-purpose/define-boundary/design-workflow/design-scheduler/design-conditional-flow/design-event-trigger/design-orchestration/design-custom-script/plan-structure/generate-code/generate-api-docs/generate-setup-guide/select-resources/analyze-feedback）、データフロー修正（resolve-skill-dependencies.md受領先Phase 2→3、後続処理Phase 2→3、delegate-to-codex.md受領先integrate-results→呼び出し元ワークフロー、design-multi-skill.md受領先Phase 2→各サブスキルPhase 1+インラインスキーマにfailureRecovery/status追加） |
| **10.3.0** | **2026-02-13** | **ラウンド1リファクタリング（20件修正）**: design-multi-skill.md 後続処理フロー修正（Phase 2,3欠落・resolve位置修正）、delegate-to-external-cli.mdインライン例修正（output型・error型・executedAt・status enum）、interview-user.md入出力インターフェース拡充・チェックリスト補完・ビジネスルール例外明示・Phase番号体系拡張、analyze-request.mdにPhase 1ラベル・上流入力・受領先追加、resolve-skill-dependencies.md/delegate-to-external-cli.mdにPhase番号追加、select-resources.md Phase 2.5記述修正・type-aggregator.md追加、extract-purpose.mdスキーマ参照統一、interview-result.json MoSCoW記述修正、multi-skill-graph.json failedSkills required追加 |
| **10.2.0** | **2026-02-13** | **interviewDepth機能追加**: インタビュー開始時にquick/standard/detailedの3段階深度選択を追加。quickモードで3-4問の最小限質問＋自動推定、detailedモードで10-15問の網羅的ヒアリング。interview-user.mdにPhase実行マトリクス・デフォルト値テーブル・深度別スキップ条件追加。interview-result.jsonスキーマにinterviewDepthフィールド追加 |
| **10.1.0** | **2026-02-13** | **4レビューエージェントの全指摘事項を修正。スキーマ新規作成(external-cli-result.json, multi-skill-graph.json)、ワークフロー図更新、相対パス修正、失敗リカバリ追加** |
| **10.0.1** | **2026-02-13** | **v10.0.0レビュー修正18件**: E1-E3(緊急3件: select-resources.mdステップ追加、シェルインジェクション修正、multi-skill-graph.jsonスキーマ作成)、H1-H5(高5件: 責務境界明確化、静的/ランタイム分離、enum不一致修正、スキップ条件追加、Script First原則適用)、M1-M6(中6件: 正規化マッピング、creationOrder優先順位、ユーザー承認ステップ、examples拡充、Mesh DAG明確化、relativePath削除)、L1-L3(低3件: 自己参照ノート、MCP検討、パターン記録) |
| **10.0.0** | **2026-02-13** | **クロススキル依存関係・外部CLIエージェント・マルチスキル対応**: interview-result.jsonスキーマ拡張（skillDependencies/externalCliAgents/multiSkillPlan）、interview-user.mdにPhase 0-3.5（クロススキル参照）・Phase 0-5.5（外部CLI）追加、新規エージェント3件（resolve-skill-dependencies/delegate-to-external-cli/design-multi-skill）、新規リファレンス2件（cross-skill-reference-patterns/external-cli-agents-guide）、新規スキーマ1件（skill-dependency-graph.json）、select-resources.mdに選択マトリクス4.1.7-4.1.8追加、execution-mode-guideにGemini CLI追加、resource-map.md更新 |
| **9.4.0** | **2026-02-13** | **UT-9B-H-003セキュリティ教訓反映 + TASK-FIX-11-1教訓反映**: patterns.mdにTDDセキュリティテスト分類体系・YAGNI共通化判断記録の成功パターン2件、正規表現Prettier干渉の失敗パターン1件追加。Phase 12の未タスク2段階判定（raw→精査）を成功パターンとして追加し、失敗パターン「未タスクraw検出の誤読」を追加。lessons-learned.md・architecture-implementation-patterns.md更新。クイックナビゲーションにセキュリティドメイン追加 |
| **9.3.0** | **2026-02-12** | **TASK-9B-Iパターン追加 + Phase 12未タスク参照整合の再発防止 + UT-9B-H-003 Phase 12再監査反映**: patterns.mdにSDK統合ドメイン新設（成功パターン1件: TypeScriptモジュール解決による型安全統合、失敗パターン2件: カスタムdeclare moduleとSDK実型共存、未タスク配置ディレクトリ混同）。「未タスク参照リンクの実在チェック」パターン追加。phase-completion-checklist.md のPhase 12完了条件に `verify-unassigned-links.js` 実行を追加。Phase 12成果物名を `documentation-changelog.md` に統一。完了済み未タスク指示書の移管と参照パス同期を追加 |
| **9.2.0** | **2026-02-12** | **TASK-9B-Hスキル改善: patterns.mdにIPC機能開発ワークフロー6段階パターン追加（チャンネル定数→ハンドラー→Preload→統合→型定義→登録）。クイックナビゲーション更新** |
| **9.1.0** | **2026-02-12** | **TASK-9B-H-SKILL-CREATOR-IPC完了記録 + UT-STORE-HOOKS-TEST-REFACTOR-001パターン追加**: SkillCreatorService IPC通信基盤の構築完了（6チャンネル定義、ハンドラー実装、Preload API統合、85テスト全PASS、3層セキュリティモデル適用）。patterns.mdにStore Hook renderHookテストパターン追加、テストカテゴリ分類(CAT-01〜CAT-05)、Phase 12苦戦箇所テンプレート改善 |
| **9.0.0** | **2026-02-11** | **TASK-FIX-7-1パターン追加: patterns.mdにSetter Injection（遅延初期化DI）、型変換パターン（Skill→SkillMetadata）、DIテストモック大規模修正パターン追加。06-known-pitfalls.md#P32-P33追加。aiworkflow-requirements/lessons-learned.md新規作成** |
| **8.10.0** | **2026-02-10** | **TASK-FIX-15-1パターン追加: patterns.mdに統合テストでの依存サービスモック漏れ防止パターン（P25）と入力バリデーション統一パターン（whitespace対策、P26）を追加** |
| **8.9.0** | **2026-02-09** | **TASK-FIX-17-1パターン追加: patterns.mdにmockReturnValue vs mockReturnValueOnceテスト間リーク防止パターン追加。06-known-pitfalls.md#P23追加。aiworkflow-requirements/patterns.mdにも同パターン追加** |
| **8.8.0** | **2026-02-06** | **TASK-AUTH-CALLBACK-001パターン追加: patterns.mdにSupabase OAuth flowType設定、PKCE内部管理委任、ローカルHTTPサーバーコールバック受信の3成功パターン追加。失敗パターン5件（カスタムstate競合、Site URL未設定、Implicit Flow混同、code_verifier不足）追加。06-known-pitfalls.mdにP15-P18追加** |
| **8.7.0** | **2026-02-06** | **TASK-FIX-5-1最適化: patterns.mdの3パターンにクロスリファレンス追加（architecture-implementation-patterns.md, 06-known-pitfalls.md連携）** |
| **8.6.1** | **2026-02-06** | **TASK-FIX-5-1パターン追加: patterns.mdにIPC Bridge API統一時のテストモック設計、セッション間仕様書編集永続化検証、Phase 1依存仕様書マトリクスの3パターン追加** |
| **8.6.0** | **2026-02-06** | **TASK-AUTH-SESSION-REFRESH-001パターン追加: patterns.mdにSupabase SDK競合防止、setTimeout vs setInterval選択、vi.useFakeTimers+flushPromisesテスト、Callback DIテスタブル設計の4パターン追加。06-known-pitfalls.mdにP12(SDK競合)・P13(タイマーテスト無限ループ)追加** |
| **8.5.0** | **2026-02-05** | **TASK-FIX-GOOGLE-LOGIN-001パターン追加: patterns.mdにOAuthコールバックエラーパラメータ抽出、Zustandリスナー二重登録防止、IPC経由エラー情報伝達設計の3パターン追加** |
| **8.4.0** | **2026-02-05** | **TASK-FIX-4-1-IPC-CONSOLIDATIONパターン追加**: patterns.mdにIPCチャンネル統合パターン追加（ハードコード文字列発見、重複定義整理、ホワイトリスト更新漏れ検証）、aiworkflow-requirements連携更新 |
| **8.3.0** | **2026-02-04** | **AUTH-UI-001パターン追加: patterns.mdに既実装済み修正の発見、テスト環境問題切り分け、React Portal z-index解決、Supabase認証状態変更後即時UI更新の4パターン追加** |
| **8.2.0** | **2026-02-02** | **E2Eテストパターン追加: patterns.mdにARIA属性ベースセレクタ、ヘルパー関数分離、安定性対策3層パターン追加（TASK-8C-B由来）** |
| 8.1.0 | 2026-01-30 | 構造リファクタリング: schemas追加（problem-definition.json, domain-model.json）、integration-patterns.md分割（1,171→70行+4サブファイル）、.tmpクリーンアップ、resource-map.md更新 |
| 8.0.0 | 2026-01-30 | Problem First + DDD/Clean Architecture統合: 問題発見Phase(0-0)・ドメインモデリングPhase(0.5)追加、discover-problem.md・model-domain.md新規エージェント、problem-discovery-framework.md・domain-modeling-guide.md・clean-architecture-for-skills.md新規リファレンス、Anchors更新（Clean Architecture追加・DDD拡張） |
| 7.2.0 | 2026-01-30 | 統合パターン集・Phase完了チェックリスト追加: integration-patterns.md, phase-completion-checklist.md新規作成、resource-map.md更新（成果物明確化セクション追加、統合契約パターンリンク） |
| 7.1.2 | 2026-01-28 | ハードコード数値を削除: 動的に変わるリソース数等の具体的数値を排除 |
| 7.1.1 | 2026-01-28 | script-llm-patterns.mdリファクタリング: 責務分離明確化、関連リソース整理 |
| 7.1.0 | 2026-01-28 | スクリプト/LLMパターンガイド追加: script-llm-patterns.md |
| 7.0.1 | 2026-01-24 | 整合性修正: custom-script-design.json追加、壊れた参照修正 |
| 7.0.0 | 2026-01-24 | リファクタリング: SKILL.md 481→130行（73%削減）、詳細をreferencesに委譲 |
| 6.2.0 | 2026-01-24 | API推薦機能追加: recommend-integrations.md, goal-to-api-mapping.md |
| 6.1.0 | 2026-01-24 | 自動リソース選択機能追加: select-resources.md |
| 6.0.0 | 2026-01-24 | オーケストレーション・ドキュメント生成機能追加 |
| 5.7.0 | 2026-01-21 | Part 5をresource-map.mdに分離 |
| 5.6.0 | 2026-01-21 | Self-Contained Skills: PNPM依存関係管理 |
| 5.0.0 | 2026-01-15 | Collaborative First追加、抽象度レベル対応 |
