---
name: aggregate-transaction-boundary
description: >
  集約とトランザクション境界の関係を明確化し、複数集約を単一トランザクションに含めるアンチパターンを
  検出・是正する。集約は強い整合性境界であり、ユースケースで複数集約を更新する場合は結果整合性を
  使うべきという原則を適用する。コードレビュー、ユースケース設計、リファクタリング時に
  トランザクション境界の問題を検出する場合に使用。
  対象言語: 言語非依存（Java, Kotlin, Scala, TypeScript, Go, Rust, Python等すべて）。
  トリガー：「複数集約を同じトランザクションで更新している」「ユースケースに@Transactionalがある」
  「集約間の整合性をどう取るか」「Sagaパターンを使うべきか」「トランザクション境界の設計」
  「1トランザクション1集約」「結果整合性の実装」「集約をまたぐトランザクション」
  といったトランザクション境界関連リクエストで起動。
---

# 集約とトランザクション境界

集約は強い整合性境界である。ユースケースで複数集約を更新する場合は結果整合性を使う。

## 核心原則

**1トランザクション = 1集約。これを逸脱してはならない。**

集約の定義そのものが「強い整合性の境界」である。複数集約を単一トランザクションに含めることは、集約の定義からの逸脱であり、モジュラリティとスケーラビリティを破壊する。

## 権威ある定義

### エリック・エヴァンス（DDD原典）

> 複数の集約にまたがるルールはどれも、常に最新の状態にあるということが期待できない。イベント処理やバッチ処理、その他の更新の仕組みを通じて、他の依存関係は一定の時間内に解消できる。

### ヴァーン・ヴァーノン（実践ドメイン駆動設計）

> ひとつの集約上でコマンドを実行するときに、他の集約のコマンドも実行するようなビジネスルールが求められるのなら、その場合は結果整合性を使うこと。

### Lightbend Academy

> トランザクションは複数の集約ルートを費やすべきではありません。

> トランザクションは複数のエンティティにまたがりますか？ この質問の答えがイエスならば、間違った集約ルートを持っていると言えるでしょう。

## アンチパターン：ユースケースをトランザクション境界にする

### 問題のあるコード

```kotlin
class CreateTaskUseCase(
    private val taskRepository: TaskRepository,
    private val taskReportRepository: TaskReportRepository,
) {
    @Transactional  // ← 複数集約を1トランザクションに閉じ込めている
    fun execute(taskName: String) {
        val task = Task(taskName)
        taskRepository.insert(task)
        val taskReport = TaskReport(task)
        taskReportRepository.insert(taskReport)
    }
}
```

**なぜ問題か**:

1. **集約の定義違反**: 集約は強い整合性境界。複数集約を1トランザクションにすると、実質的に1つの巨大な整合性境界を作っている
2. **スケーラビリティの阻害**: 集約Aと集約Bの更新が常にセットになり、後のスケーリングやサーバ分散が困難になる
3. **異種DB環境で不可能**: 集約ごとに異なるデータストアを使う場合、同一トランザクションは実装不可能
4. **マイクロサービスへの発展を阻害**: 集約を別サービスに分離できなくなる

### 修正後のコード

```kotlin
class CreateTaskUseCase(
    private val taskRepository: TaskRepository,
    private val taskReportRepository: TaskReportRepository,
) {
    fun execute(taskName: String) {
        // 集約ごとに独立したトランザクション
        val task = Task(taskName)
        taskRepository.insert(task)

        val taskReport = TaskReport(task)
        taskReportRepository.insert(taskReport)
    }
}
```

## そもそもモデリングの問題ではないか

複数集約を同一トランザクションで更新したくなる場合、まずモデリングを見直すべきである。

### 判断フロー

```
2つの集約を常に一緒に更新する必要がある
    ↓
Task : TaskReport の関係は？
    ├─ 1:1 → 同一集約に統合を検討
    │         例: Task(taskReport: TaskReport)
    │         → 1トランザクションで問題なし
    │
    ├─ 1:N（少量） → 要件調整で小規模化できないか検討
    │         → 可能なら同一集約に統合
    │
    ├─ 1:N（大量） → 別集約 + 結果整合性
    │         → ドメインイベントで連携
    │
    └─ TaskReportは純粋なクエリ要件か？
          ├─ YES → CQRS: リードモデルとして構築
          │         → 集約ではなくプロジェクションで対応
          └─ NO → ドメイン知識を持つ → 独立集約 + 結果整合性
```

### 同一集約への統合（1:1の場合）

```kotlin
// TaskReportが常にTaskと1:1なら同一集約に統合
class Task private constructor(
    val id: TaskId,
    val name: TaskName,
    val report: TaskReport  // 集約内に含める
) {
    companion object {
        fun create(name: TaskName): Task {
            val id = TaskId.generate()
            return Task(id, name, TaskReport.create(id))
        }
    }
}
```

## 結果整合性の実現方法

集約が独立している場合、結果整合性で連携する。

### ドメインイベント + 非同期処理

```kotlin
// 1. Task集約がドメインイベントを発行
class Task private constructor(
    val id: TaskId,
    val name: TaskName,
    private val events: List<DomainEvent>
) {
    companion object {
        fun create(name: TaskName): Task {
            val id = TaskId.generate()
            return Task(
                id, name,
                listOf(TaskCreated(id, name))  // イベント発行
            )
        }
    }

    fun domainEvents(): List<DomainEvent> = events.toList()
}

// 2. ユースケースでTask保存後、イベントを発行
class CreateTaskUseCase(
    private val taskRepository: TaskRepository,
    private val eventPublisher: DomainEventPublisher,
) {
    fun execute(taskName: String) {
        val task = Task.create(TaskName(taskName))
        taskRepository.store(task)
        eventPublisher.publishAll(task.domainEvents())
    }
}

// 3. イベントハンドラでTaskReport作成（別トランザクション）
class TaskCreatedEventHandler(
    private val taskReportRepository: TaskReportRepository,
) {
    fun handle(event: TaskCreated) {
        val taskReport = TaskReport.create(event.taskId)
        taskReportRepository.store(taskReport)
    }
}
```

### ダブルコミット問題とSaga

独立トランザクションでは、集約Bの更新失敗時に集約Aはコミット済みという状態が発生する。

**対処方法**:

| 方法 | 適用場面 |
|------|---------|
| **リトライ** | 一時的な障害の場合 |
| **Saga（補償トランザクション）** | 複雑な複数集約の協調が必要な場合 |
| **Outboxパターン** | イベント発行の確実性が必要な場合 |

Sagaは並行性問題を防止・軽減する設計テクニックであり、マイクロサービス環境での分散トランザクション管理に必須となる。

## なぜこの規律が必要か

### モジュラリティの確保

同一トランザクションに複数集約を含めると、暗黙的な結合が生まれる。

```
同一トランザクション:
  Task ←──強結合──→ TaskReport
  （分離不可能、独立スケーリング不可能）

結果整合性:
  Task ──イベント──→ TaskReport
  （独立デプロイ可能、独立スケーリング可能）
```

### スケーラビリティへの道

```
モノリス（結果整合性を採用）
  → 集約ごとに独立したDB/テーブルへの分離が容易
  → マイクロサービス化が容易
  → 集約ごとの独立スケーリングが可能

モノリス（同一トランザクション）
  → 集約間の暗黙的結合で分離困難
  → マイクロサービス化に大規模リファクタリング必要
  → スケーリングはシステム全体でしかできない
```

## `aggregate-design` スキルとの関係

| 観点 | 本スキル | aggregate-design スキル |
|------|---------|------------------------|
| 焦点 | トランザクション境界と結果整合性 | 集約の内部設計と構造 |
| 対象 | 集約間の連携パターン | 集約単体の設計原則 |
| 用途 | ユースケース設計・レビュー | 集約のモデリング・レビュー |

`aggregate-design` のルール8「1トランザクション = 1集約」とVernon Rule 4「結果整合性」を深掘りしたものが本スキルである。

## レビューチェックリスト

### トランザクション境界

- [ ] `@Transactional`（またはトランザクション制御）の範囲内で、複数のリポジトリを呼び出していないか
- [ ] 1つのユースケースで複数集約を更新する場合、結果整合性を採用しているか
- [ ] 「便利だから」という理由で複数集約を同一トランザクションに含めていないか

### モデリング

- [ ] 常に一緒に更新される2つの「集約」は、本来1つの集約ではないか
- [ ] 片方がクエリ要件のみなら、CQRSのリードモデルで対応できないか
- [ ] 1:Nの関係でNが大量になる場合、別集約 + 結果整合性に分離しているか

### 結果整合性の実装

- [ ] ドメインイベントによる集約間連携が実装されているか
- [ ] イベント発行の確実性が担保されているか（Outboxパターン等）
- [ ] 失敗時のリカバリ戦略（リトライ、Saga）が定義されているか
- [ ] ダブルコミット問題を認識し、対処方法が明確か

## 関連スキル（併読推奨）
このスキルを使用する際は、以下のスキルも併せて参照すること：
- `aggregate-design`: 集約の設計ルール（トランザクション境界の根拠）
- `cross-aggregate-constraints`: 集約間の制約と結果整合性の設計
- `cqrs-aggregate-modeling`: CQRS/ESによる集約軽量化とトランザクション問題の解消
