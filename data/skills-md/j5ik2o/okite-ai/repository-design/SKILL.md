---
name: repository-design
description: >
  DDDにおけるリポジトリの設計ルールとアンチパターンを提供する。集約単位の命名規則、
  CQS（Command Query Separation）に基づくメソッド設計、入出力の型制約をチェックする。
  コードレビュー、新規実装、リファクタリング時にリポジトリ設計の問題を検出する場合に使用。
  対象言語: 言語非依存（Java, Kotlin, Scala, TypeScript, Go, Rust, Python等すべて）。
  トリガー：「リポジトリの設計をレビュー」「Repository名がおかしい」「findByIdの戻り値」
  「リポジトリがDTOを返している」「テーブル名でリポジトリを作ってしまった」
  「集約単位のリポジトリ」「リポジトリのアンチパターン」「リポジトリのCQS」
  といったリポジトリ設計関連リクエストで起動。
---

# Repository Design

リポジトリは集約のI/Oに特化した責務である。

## 設計原則

### 命名規則

リポジトリ名は `集約名 + Repository` でなければならない。

```text
# NG: テーブル名ベース
OrdersTableRepository
UserAccountsRepository  (テーブル名 user_accounts に由来)

# NG: DTOベース
OrderDtoRepository
UserResponseRepository

# OK: 集約名ベース
OrderRepository
UserRepository
```

**検出基準**: リポジトリ名に `Table`, `Dto`, `Entity`, `Record`, `Row` 等のインフラ用語が含まれている。

### CQS（Command Query Separation）

リポジトリのメソッドはCQSに従う。各メソッドはコマンド（状態変更、戻り値なし）またはクエリ（状態変更なし、値を返す）のいずれかである。

**Query（問い合わせ）**: 集約を返す。副作用なし。

**Command（命令）**: 集約を受け取り、voidを返す。状態を変更する。

### 単件・複数件I/O

**単件I/O**:

```kotlin
// Query: 単件取得
fun findById(id: OrderId): Order?

// Command: 単件保存
fun store(order: Order)
```

**複数件I/O**:

```kotlin
// Query: 複数件取得
fun findByIds(ids: List<OrderId>): List<Order>

// Command: 複数件保存
fun storeMulti(orders: List<Order>): Int
```

### 同期・非同期パターン

リポジトリは同期型・非同期型いずれでも設計できる。エラーは例外方式またはResult/Either方式を選択する。
エラー方式の詳細な設計指針は `error-handling` スキルを参照。

**同期型（例外方式）**:

```kotlin
// Query: 例外でエラーを通知
fun findById(id: OrderId): Order?

// Command
fun store(order: Order)
```

**同期型（Result/Either方式）**:

```kotlin
// Query: Result型でエラーを返す
fun findById(id: OrderId): Result<Order?, RepositoryError>

// Command
fun store(order: Order): Result<Unit, RepositoryError>
```

**非同期型（Future）**:

```scala
// Query: Futureのエラー機構を使用
def findById(id: OrderId): Future[Option[Order]]

// Command
def store(order: Order): Future[Unit]
```

**非同期型（async/await + Result）**:

```rust
// Query
async fn find_by_id(&self, id: &OrderId) -> Result<Option<Order>, RepositoryError>;

// Command
async fn store(&self, order: &Order) -> Result<(), RepositoryError>;
```

## アンチパターン

### findByIdの戻り値が集約でない

```kotlin
// NG: DTOを返す
fun findById(id: OrderId): OrderDto

// NG: テーブル行を返す
fun findById(id: OrderId): OrderRecord

// NG: エンティティの一部を返す
fun findById(id: OrderId): OrderSummary

// OK: 集約を返す
fun findById(id: OrderId): Order?
```

### ドメインロジックを含むメソッド名

リポジトリは集約のI/O（保存・取得・削除）のみを担う。ドメイン固有の操作をメソッド名に含めてはならない。

```kotlin
// NG: ドメインロジックがリポジトリに漏れている
fun leave(userId: UserId)          // 「退会」はドメインの振る舞い
fun activate(orderId: OrderId)     // 「有効化」はドメインの振る舞い
fun cancel(orderId: OrderId)       // 「キャンセル」はドメインの振る舞い
fun approve(requestId: RequestId)  // 「承認」はドメインの振る舞い
fun rename(userId: UserId)         // 「名前の変更」はドメインの振る舞い

// NG: DB操作を想起するメソッド名(リポジトリはDB以外の実装もありえるため)
fun insert(order: Order)             // INSERT文を連想
fun update(order: Order)             // UPDATE文を連想
fun select(id: OrderId): Order?      // SELECT文を連想
fun upsert(order: Order)             // UPSERT文を連想

// OK: コレクションとしてのI/O操作
fun store(user: User)
fun put(order: Order)
fun add(order: Order)
fun delete(order: Order)
fun findById(id: OrderId): Order?
fun storeMulti(orders: List<Order>): Int
fun putAll(orders: List<Order>)
fun addAll(orders: List<Order>)
fun findByIds(ids: List<OrderId>): List<Order>
```

**許可されるメソッド名**: 
- 単体系
  - `store`
  - `findById`
  - `delete`
  - `put`
  - `remove`
  - `add`
- 複数形
  - `storeMulti`
  - `findByIds`
  - `deleteMulti`
  - `putMulti`
  - `addMulti`

等のI/O操作。

**禁止されるメソッド名**:
- ドメイン用語: `leave`, `activate`, `cancel`, `approve` 等
- DB操作用語: `insert`, `update`, `select`, `upsert` 等

**正しい設計**: ドメインロジックは集約のメソッドで実行し、リポジトリはその結果を保存するだけ。

```kotlin
// 集約でドメインロジックを実行
val user = userRepository.findById(userId)
val leftUser = user.leave()  // 集約のメソッド

// リポジトリは保存するだけ
userRepository.store(leftUser)
```

### リポジトリから別のリポジトリを呼び出す

リポジトリの実装内で別のリポジトリを呼び出してはならない。集約間の調整はユースケース層（アプリケーションサービス）の責務である。

**理由**:
- **集約境界の違反**: リポジトリは1つの集約に対して1つ。別のリポジトリへの依存は集約境界が正しく設計されていない兆候
- **責務の混在**: リポジトリの責務は「集約の永続化と復元」であり、他の集約の取得はその責務に含まれない
- **隠れた結合**: 集約間の依存がインフラ層に埋もれ、発見・変更が困難になる
- **テスト困難性**: リポジトリのテストに別のリポジトリのモックが必要になる

```kotlin
// NG: リポジトリが別のリポジトリに依存
class OrderRepositoryImpl(
    private val productRepository: ProductRepository
) : OrderRepository {
    override fun store(order: Order) {
        val product = productRepository.findById(order.productId)
        // ...
    }
}

// OK: ユースケース層で調整
class PlaceOrderUseCase(
    private val orderRepository: OrderRepository,
    private val productRepository: ProductRepository,
) {
    fun execute(command: PlaceOrderCommand) {
        val product = productRepository.findById(command.productId)
        val order = Order.create(product.id, command.quantity)
        orderRepository.store(order)
    }
}
```

**検出基準**: リポジトリのコンストラクタまたはメソッド内で別のリポジトリを参照している。

### storeの引数・戻り値の違反

```kotlin
// NG: DTOを受け取る
fun store(dto: OrderDto)

// NG: 保存後のDBレコードを返す（CQS違反）
fun store(order: Order): OrderRecord

// NG: IDを返す（CQS違反）
fun store(order: Order): OrderId

// OK: 集約を受け取り、voidを返す
fun store(order: Order)
```

## チェック手順

1. リポジトリのインターフェース/トレイトを特定する
2. 命名が `集約名 + Repository` であるか確認する
3. 各メソッドがCQSに従っているか確認する
   - Query: 集約を返す、副作用なし
   - Command: 集約を受け取る、voidを返す
4. 入出力の型が集約であるか確認する
5. 違反があれば具体的な修正案を提示する

## 関連スキル（併読推奨）
このスキルを使用する際は、以下のスキルも併せて参照すること：
- `repository-placement`: リポジトリインターフェースの配置場所（ユースケース層 vs ドメイン層）
- `aggregate-design`: リポジトリが永続化する集約の設計ルール
- `error-handling`: リポジトリの同期・非同期パターンにおけるエラー処理方式
