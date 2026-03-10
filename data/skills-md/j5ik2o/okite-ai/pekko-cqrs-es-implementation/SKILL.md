---
name: pekko-cqrs-es-implementation
description: >-
  Apache Pekko + Scala 3によるCQRS/Event Sourcing実装ガイド。
  PersistenceEffectorを用いた集約アクター、ドメインモデルとアクターの分離、
  状態遷移の型安全な表現、イベント設計、Protocol Buffersシリアライズ、
  ZIOベースのユースケース層、リードモデルアップデータの実装パターンを提供する。
  対象言語: Scala 3限定。CQRS/Event Sourcingアーキテクチャが前提の場合のみ使用。
  トリガー条件: 「Scala」かつ「CQRS」または「Event Sourcing」または「Pekko」が
  リクエストに含まれる場合のみ起動。Scala以外の言語やCQRS/ES以外のアーキテクチャでは
  このスキルを使用してはならない。
  トリガー：「PekkoでCQRS/ESを実装したい」「Scalaで集約アクターを書きたい」
  「PersistenceEffectorの使い方」「Pekkoのイベントソーシング」
  「ScalaでCQRSのコマンド側を実装」「Pekkoで状態遷移を管理」
  といったPekko + Scala + CQRS/ES実装リクエストで起動。
  非トリガー：「CQRSのトレードオフ」「イベントソーシングとは」「JavaでCQRS」
  「GoでEvent Sourcing」「CQRSの概念を教えて」など、Scala/Pekko以外や概念的な質問では
  起動してはならない。
---

# Pekko CQRS/ES 実装ガイド

Apache Pekko + Scala 3でCQRS/Event Sourcingを実装する際の具体的なパターン集。

## 適用条件

**このスキルは以下のすべてを満たす場合にのみ使用する：**

1. プログラミング言語がScala（3.x推奨）であること
2. CQRS/Event Sourcingアーキテクチャを採用していること
3. Apache Pekko（またはAkka）をアクターフレームワークとして使用していること

上記を満たさない場合は、`cqrs-tradeoffs`、`cqrs-to-event-sourcing`、`cqrs-aggregate-modeling`など
言語非依存のスキルを使用すること。

## アーキテクチャ概要

### システム全体のデータフロー

```
クライアント
    │
    ▼
コマンドAPI（GraphQL Mutation）
    │
    ▼
ユースケース層（ZIO）
    │
    ▼
集約アクター（Pekko Typed）
    │
    ▼
ドメインモデル（純粋Scala）→ イベント生成
    │
    ▼
イベントストア（DynamoDB）
    │
    ▼
DynamoDB Streams
    │
    ▼
リードモデルアップデータ（AWS Lambda）
    │
    ▼
リードモデル（PostgreSQL）
    │
    ▼
クエリAPI（GraphQL Query）
```

### コマンド側とクエリ側の分離

| | コマンド側 | クエリ側 |
|---|---|---|
| 目的 | ビジネスルール実行 | 効率的なデータ取得 |
| データストア | DynamoDB（イベントストア） | PostgreSQL（リードモデル） |
| API | GraphQL Mutation | GraphQL Query |
| レイヤー | ドメイン → ユースケース → インターフェースアダプタ | インターフェースアダプタのみ |
| 整合性 | 強い整合性（集約内） | 結果整合性 |

**クエリ側にユースケース層はない。** GraphQL自体がユースケースに相当する。

## モジュール構成

```
modules/
├── command/
│   ├── domain/                          # ドメイン層（純粋Scala）
│   ├── use-case/                        # ユースケース層（ZIO）
│   ├── interface-adapter/               # アクター、GraphQL、シリアライザ
│   ├── interface-adapter-contract/      # コマンド/リプライのプロトコル定義
│   └── interface-adapter-event-serializer/  # Protocol Buffersシリアライザ
├── query/
│   ├── interface-adapter/               # DAO（Slick）、GraphQL
│   └── flyway-migration/               # DBマイグレーション
└── infrastructure/                      # 共有ユーティリティ

apps/
├── command-api/                         # コマンド側HTTPサーバー
├── query-api/                           # クエリ側HTTPサーバー
└── read-model-updater/                  # AWS Lambda
```

### 依存方向

```
domain ← use-case ← interface-adapter ← apps
  │                       ↑
  │               interface-adapter-contract
  │               interface-adapter-event-serializer
  └── Scalaのみに依存。フレームワーク非依存。
```

## コマンド側実装パターン

### 1. ドメインモデル

**原則: ドメインモデルは純粋なScalaコードで、Pekkoに一切依存しない。**

#### 集約（trait + private case class）

```scala
trait UserAccount extends Entity {
  override type IdType = UserAccountId
  def id: UserAccountId
  def name: UserAccountName
  def emailAddress: EmailAddress
  def createdAt: DateTime
  def updatedAt: DateTime

  def rename(newName: UserAccountName): Either[RenameError, (UserAccount, UserAccountEvent)]
  def delete: Either[DeleteError, (UserAccount, UserAccountEvent)]
}

object UserAccount {
  // ファクトリ: 新しい状態とイベントのペアを返す
  def apply(
    id: UserAccountId,
    name: UserAccountName,
    emailAddress: EmailAddress,
    createdAt: DateTime = DateTime.now(),
    updatedAt: DateTime = DateTime.now()
  ): (UserAccount, UserAccountEvent) =
    (
      UserAccountImpl(id, false, name, emailAddress, createdAt, updatedAt),
      UserAccountEvent.Created_V1(
        id = DomainEventId.generate(),
        entityId = id,
        name = name,
        emailAddress = emailAddress,
        occurredAt = DateTime.now()
      ))

  // 実装はprivateで隠蔽
  private final case class UserAccountImpl(
    id: UserAccountId,
    deleted: Boolean,
    name: UserAccountName,
    emailAddress: EmailAddress,
    createdAt: DateTime,
    updatedAt: DateTime
  ) extends UserAccount {

    override def rename(
      newName: UserAccountName): Either[RenameError, (UserAccount, UserAccountEvent)] =
      if (name == newName) {
        Left(RenameError.FamilyNameSame)
      } else {
        val updated = this.copy(name = newName, updatedAt = DateTime.now())
        val event = UserAccountEvent.Renamed_V1(
          id = DomainEventId.generate(),
          entityId = id,
          oldName = name,
          newName = newName,
          occurredAt = DateTime.now()
        )
        Right((updated, event))
      }

    override def delete: Either[DeleteError, (UserAccount, UserAccountEvent)] =
      if (deleted) {
        Left(DeleteError.AlreadyDeleted)
      } else {
        val updated = copy(deleted = true, updatedAt = DateTime.now())
        val event = UserAccountEvent.Deleted_V1(
          id = DomainEventId.generate(),
          entityId = id,
          occurredAt = DateTime.now()
        )
        Right((updated, event))
      }
  }
}
```

**重要なパターン:**
- 状態変更メソッドは `Either[Error, (NewState, Event)]` を返す
- ファクトリも `(State, Event)` のペアを返す
- 実装クラスは `private` で外部から直接構築できない
- ドメインモデル内でPekkoのimportは一切ない

#### イベント定義（enum + バージョニング）

```scala
enum UserAccountEvent extends DomainEvent {
  override type EntityIdType = UserAccountId

  case Created_V1(
    id: DomainEventId,
    entityId: UserAccountId,
    name: UserAccountName,
    emailAddress: EmailAddress,
    occurredAt: DateTime
  )

  case Renamed_V1(
    id: DomainEventId,
    entityId: UserAccountId,
    oldName: UserAccountName,
    newName: UserAccountName,
    occurredAt: DateTime
  )

  case Deleted_V1(
    id: DomainEventId,
    entityId: UserAccountId,
    occurredAt: DateTime
  )
}
```

**イベント設計ルール:**

| ルール | 説明 | 例 |
|--------|------|-----|
| 過去形で命名 | 「何が起きたか」を表す | `Created`, `Renamed`, `Deleted` |
| `_V1`サフィックス | スキーマ進化に対応 | `Renamed_V1`, `Renamed_V2` |
| 不変 | case classで自動的に保証 | |
| 自己完結 | 変更前後の値を含む | `oldName`, `newName` |
| 必須フィールド | `id`, `entityId`, `occurredAt` | すべてのイベントに共通 |

### 2. 集約の状態（enum）

```scala
enum UserAccountAggregateState {
  case NotCreated(id: UserAccountId)
  case Created(user: UserAccount)
  case Deleted(user: UserAccount)

  def applyEvent(event: UserAccountEvent): UserAccountAggregateState = (this, event) match {
    case (NotCreated(id), UserAccountEvent.Created_V1(_, entityId, name, emailAddress, _))
        if id == entityId =>
      Created(UserAccount(entityId, name, emailAddress)._1)

    case (Created(user), UserAccountEvent.Renamed_V1(_, entityId, _, newName, _))
        if user.id == entityId =>
      Created(user.rename(newName) match {
        case Right((u, _)) => u
        case Left(error) =>
          throw new IllegalStateException(s"Failed to rename user: $error")
      })

    case (Created(user), UserAccountEvent.Deleted_V1(_, entityId, _))
        if user.id == entityId =>
      Deleted(user.delete match {
        case Right((deletedUser, _)) => deletedUser
        case Left(error) =>
          throw new IllegalStateException(s"Failed to delete user: $error")
      })

    case _ =>
      throw new IllegalStateException(s"Cannot apply event $event to state $this")
  }
}
```

**状態遷移の型安全性:**
- `NotCreated` → `Created`（Created_V1イベントのみ）
- `Created` → `Created`（Renamed_V1）/ `Deleted`（Deleted_V1）
- `Deleted` → 遷移なし（どのイベントも受け付けない）

### 3. プロトコル定義（コマンド/リプライ）

```scala
object UserAccountProtocol {
  // コマンド: すべてidを持つ
  sealed trait Command { def id: UserAccountId }
  final case class Create(
    id: UserAccountId, name: UserAccountName,
    emailAddress: EmailAddress, replyTo: ActorRef[CreateReply]) extends Command
  final case class Rename(
    id: UserAccountId, newName: UserAccountName,
    replyTo: ActorRef[RenameReply]) extends Command
  final case class Delete(
    id: UserAccountId, replyTo: ActorRef[DeleteReply]) extends Command
  final case class Get(
    id: UserAccountId, replyTo: ActorRef[GetReply]) extends Command

  // リプライ: コマンドごとに専用の型
  sealed trait CreateReply
  final case class CreateSucceeded(id: UserAccountId) extends CreateReply

  sealed trait RenameReply
  final case class RenameSucceeded(id: UserAccountId) extends RenameReply
  final case class RenameFailed(id: UserAccountId, reason: RenameError) extends RenameReply

  sealed trait DeleteReply
  final case class DeleteSucceeded(id: UserAccountId) extends DeleteReply
  final case class DeleteFailed(id: UserAccountId, reason: DeleteError) extends DeleteReply

  sealed trait GetReply
  final case class GetSucceeded(value: UserAccount) extends GetReply
  final case class GetNotFoundFailed(id: UserAccountId) extends GetReply
}
```

**プロトコル設計ルール:**
- コマンドはすべて `sealed trait Command` を継承し、`id` を持つ
- リプライはコマンドごとに専用の `sealed trait` を定義する（`CreateReply`, `RenameReply`等）
- `replyTo: ActorRef[XxxReply]` で型安全な応答を保証
- 成功/失敗をcase classで表現し、パターンマッチで網羅性チェック

### 4. 集約アクター（PersistenceEffector）

```scala
object UserAccountAggregate {

  // 状態ごとにハンドラ関数を分離
  private def handleNotCreated(
    state: UserAccountAggregateState.NotCreated,
    effector: PersistenceEffector[UserAccountAggregateState, UserAccountEvent, Command]
  ): Behavior[Command] = Behaviors.receiveMessagePartial {
    case Create(id, name, emailAddress, replyTo) if state.id == id =>
      val (newState, event) = UserAccount(id, name, emailAddress)
      effector.persistEvent(event) { _ =>
        replyTo ! CreateSucceeded(id)
        handleCreated(UserAccountAggregateState.Created(newState), effector)
      }
    case Get(id, replyTo) if state.id == id =>
      replyTo ! GetNotFoundFailed(id)
      Behaviors.same
  }

  private def handleCreated(
    state: UserAccountAggregateState.Created,
    effector: PersistenceEffector[UserAccountAggregateState, UserAccountEvent, Command]
  ): Behavior[Command] = Behaviors.receiveMessagePartial {
    case Rename(id, newName, replyTo) if state.user.id == id =>
      // ドメインモデルに委譲
      state.user.rename(newName) match {
        case Left(reason) =>
          replyTo ! RenameFailed(id, reason)
          Behaviors.same
        case Right((newUser, event)) =>
          effector.persistEvent(event) { _ =>
            replyTo ! RenameSucceeded(id)
            handleCreated(state.copy(user = newUser), effector)
          }
      }
    // ... Delete, Get も同様
  }

  // エントリポイント
  def apply(id: UserAccountId): Behavior[Command] = {
    val config = PersistenceEffectorConfig
      .create[UserAccountAggregateState, UserAccountEvent, Command](
        persistenceId = s"${id.entityTypeName}-${id.asString}",
        initialState = UserAccountAggregateState.NotCreated(id),
        applyEvent = (state, event) => state.applyEvent(event)
      )
      .withPersistenceMode(PersistenceMode.Persisted)
      .withSnapshotCriteria(SnapshotCriteria.every(1000))
      .withRetentionCriteria(RetentionCriteria.snapshotEvery(2))

    Behaviors.setup[Command] { implicit ctx =>
      Behaviors
        .supervise(
          PersistenceEffector.fromConfig(config) {
            case (state: UserAccountAggregateState.NotCreated, effector) =>
              handleNotCreated(state, effector)
            case (state: UserAccountAggregateState.Created, effector) =>
              handleCreated(state, effector)
            case (state: UserAccountAggregateState.Deleted, effector) =>
              handleDeleted(state, effector)
          })
        .onFailure[IllegalArgumentException](SupervisorStrategy.restart)
    }
  }
}
```

**アクター実装ルール:**
- **ドメインロジックをアクターに書かない。** アクターは永続化とライフサイクル管理に徹する
- 状態ごとにハンドラ関数を分離し、受け付けるコマンドを限定する
- `effector.persistEvent(event) { _ => ... }` でイベント永続化後にリプライ
- ドメインモデルが `Left` を返したらリプライのみ（永続化しない）
- ドメインモデルが `Right` を返したらイベントを永続化してからリプライ

### 5. ユースケース層（ZIO）

```scala
private[users] final class UserAccountUseCaseImpl(
  userAccountAggregateRef: ActorRef[UserAccountProtocol.Command]
)(implicit
  timeout: Timeout,
  scheduler: Scheduler,
  ec: ExecutionContext
) extends UserAccountUseCase {

  override def createUserAccount(
    userAccountName: UserAccountName,
    emailAddress: EmailAddress
  ): IO[UserAccountUseCaseError, UserAccountId] =
    for {
      userAccountId <- ZIO.succeed(UserAccountId.generate())
      reply <- askActor[UserAccountProtocol.CreateReply] { replyTo =>
        UserAccountProtocol.Create(
          id = userAccountId,
          name = userAccountName,
          emailAddress = emailAddress,
          replyTo = replyTo
        )
      }.mapError(e => UserAccountUseCaseError.UnexpectedError(e.getMessage, Some(e)))
      result <- reply match {
        case UserAccountProtocol.CreateSucceeded(id) => ZIO.succeed(id)
      }
    } yield result

  private def askActor[R](
    createMessage: ActorRef[R] => UserAccountProtocol.Command
  ): Task[R] =
    PekkoInterop.fromFuture { userAccountAggregateRef.ask(createMessage) }
}
```

**ユースケース層のルール:**
- **ビジネスロジックを書く場所ではない。** 処理ステップの調整役に徹する
- ZIOのfor式でアクターとの通信を型安全に記述
- `askActor` ヘルパーでPekko Ask → ZIO Task変換を共通化
- エラーは `UserAccountUseCaseError` にマッピング

## シリアライズ

### Protocol Buffersによるイベントシリアライズ

```protobuf
// event.proto
syntax = "proto3";

message UserAccountCreatedV1 {
  string id = 1;
  string entity_id = 2;
  string name = 3;
  string email_address = 4;
  string occurred_at = 5;
}

message UserAccountRenamedV1 {
  string id = 1;
  string entity_id = 2;
  string old_name = 3;
  string new_name = 4;
  string occurred_at = 5;
}
```

**シリアライズ方針:**
- イベントとスナップショットの両方をProtocol Buffersで定義
- ScalaPBでScalaコードを自動生成
- カスタムシリアライザでドメインイベント ↔ Protobufメッセージを変換
- バージョニングはProtobufのフィールド番号で後方互換性を確保

### スナップショット戦略

| 設定 | 値 | 理由 |
|------|-----|------|
| 保存頻度 | 1000イベントごと | 起動時間とストレージのバランス |
| 保持数 | 最新2つ | リカバリ安全性の確保 |

## テスト戦略

### ドメインモデルテスト（Pekko非依存）

```scala
test("ユーザー名を変更できる") {
  val (user, _) = UserAccount(id, name, email)
  val result = user.rename(newName)
  result match {
    case Right((updated, event)) =>
      updated.name shouldBe newName
      event shouldBe a[UserAccountEvent.Renamed_V1]
    case Left(error) => fail(s"Unexpected error: $error")
  }
}
```

### アクターテスト（ActorTestKit）

```scala
// PersistenceEffectorのテスト
val probe = testKit.createTestProbe[CreateReply]()
aggregateRef ! Create(id, name, email, probe.ref)
probe.expectMessage(CreateSucceeded(id))
```

### テストの分離

| レベル | 対象 | ツール | Pekko依存 |
|--------|------|--------|-----------|
| ドメイン | ビジネスロジック | ScalaTest | なし |
| アクター | メッセージング、永続化 | ActorTestKit | あり |
| シリアライザ | イベント/スナップショットの変換 | ScalaTest | なし |
| 統合 | エンドツーエンド | LocalStack | あり |

## 関連スキルとの使い分け

| スキル | フォーカス | 使うタイミング |
|--------|----------|---------------|
| **本スキル** | Pekko + Scala 3での具体的実装 | CQRS/ESをScalaで実装するとき |
| cqrs-tradeoffs | CQRS採用判断のトレードオフ分析 | CQRS導入の是非を検討するとき |
| cqrs-to-event-sourcing | なぜESが必要になるかの論理的説明 | ESの必然性を理解したいとき |
| cqrs-aggregate-modeling | CQRS導入時の集約境界再定義 | 集約の粒度を見直すとき |
| aggregate-design | 集約設計ルール全般 | 集約の新規設計やレビューのとき |
| domain-building-blocks | VO/Entity/Aggregate等の設計 | ドメインモデル全体を設計するとき |

## 参考文献

- かとじゅん「Apache Pekko(もしくはAkka)で実現するCQRS/Event Sourcingシステム設計の完全開発ガイド」 - https://tech-book.precena.co.jp/entry/pekko-cqrs-es-guide
- リファレンス実装: https://github.com/j5ik2o/pekko-cqrs-es-example
- pekko-persistence-effector: https://github.com/j5ik2o/pekko-persistence-effector

## 関連スキル（併読推奨）
このスキルを使用する際は、以下のスキルも併せて参照すること：
- `cqrs-tradeoffs`: CQRS/ES採用判断のトレードオフ分析
- `cqrs-to-event-sourcing`: CQRSからイベントソーシングへの必然性
- `aggregate-design`: ドメインモデルとしての集約設計ルール
