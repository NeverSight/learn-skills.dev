---
name: repository-placement
description: >-
  リポジトリインターフェースの配置場所に関するガイド。クリーンアーキテクチャにおいて
  リポジトリインターフェースをドメイン層ではなくユースケース層に配置すべき理由を解説。
  ドメインモデルとリポジトリの結合防止、構造による設計意図の強制を主眼とする。
  トリガー：「リポジトリをどこに置く」「リポジトリインターフェースの配置」「ドメイン層にリポジトリ」
  「クリーンアーキテクチャでリポジトリ」等のリポジトリ配置関連リクエストで起動。
---

# リポジトリインターフェースの配置

## 結論

**リポジトリインターフェースはユースケース層に置く。ドメイン層には置かない。**

## なぜドメイン層に置くと問題か

### 物理的な近さが結合を誘発する

同じ層にあると、ドメインモデルがリポジトリを使いやすくなる：

```java
// ❌ 集約の中でリポジトリを使ってしまう
class Order {
  Order withRelatedOrder(OrderId relatedId, OrderRepository repo) {
    Order related = repo.findById(relatedId);  // ← 同じ層にあるから気軽に使える
    return this.withAddedRelatedOrder(related);
  }
}
```

```java
// ❌ ドメインサービスがリポジトリだらけになる
class OrderDomainService {
  private OrderRepository orderRepo;
  private CustomerRepository customerRepo;
  private ProductRepository productRepo;
  private InventoryRepository inventoryRepo;
  // リポジトリの注入が増え続ける
}
```

### ドメインが「永続化」を知ってしまう

```java
// ドメイン層にこれがあるということは...
interface OrderRepository {
  void save(Order order);      // ← 「保存」という概念を知っている
  Order findById(OrderId id);  // ← 「取得」という概念を知っている
}
```

ドメインモデルは**純粋なビジネスルール**だけを持つべき。

## ユースケース層に置く利点

### 構造が設計意図を強制する

```
[ドメイン層]              ← リポジトリをimportできない = 結合しない
     ↑
[ユースケース層]          ← リポジトリインターフェース定義（出力ポート）
     ↑
[インターフェースアダプタ層] ← リポジトリ実装（入力/出力アダプタ）
```

物理的な距離がガードレールになる：

- ドメインモデルからimportしにくい（別パッケージ/モジュール）
- 「リポジトリはユースケース層のポート」という意図が構造で伝わる
- 集約がIDで参照するルールを守りやすい

### 集約のID参照ルールを自然に守れる

```java
// ✅ 集約は他の集約をIDで参照
class Order {
  private final CustomerId customerId;  // Customer実体ではなくID
  private final List<ProductId> productIds;
}

// ユースケース層でリポジトリを使って解決
class PlaceOrderUseCase {
  private OrderRepository orderRepo;
  private CustomerRepository customerRepo;

  void execute(PlaceOrderCommand cmd) {
    Customer customer = customerRepo.findById(cmd.customerId);
    // ユースケース層で必要なエンティティを取得
  }
}
```

## 検出パターン

### ドメイン層にリポジトリがある兆候

```
domain/
  order/
    Order.java
    OrderRepository.java  ← ❌ ここにある
```

### インターフェースアダプタ層にリポジトリインターフェースがある兆候

```
interface-adapters/
  repositories/
    OrderRepository.java  ← ❌ ここにある
```

### 正しい配置

```
domain/
  order/
    Order.java
    OrderId.java

usecases/  (または application/, interactor/)
  order/
    OrderRepository.java      ← インターフェース定義

interface-adapters/  (または adapters/, infra/)
  repositories/
    JpaOrderRepository.java   ← 実装
```

## DDDとの関係

**DDDの伝統的解釈**では、リポジトリはドメインの一部（集約のライフサイクル管理）とされる。

**しかし実践上は**、ドメイン層に置くと結合が生まれやすい。クリーンアーキテクチャの規約では、
リポジトリインターフェースはユースケース層の出力ポートとして扱う。

| アプローチ | メリット | デメリット |
|-----------|---------|-----------|
| ドメイン層に配置 | DDDの教科書通り | 結合が生まれやすい |
| ユースケース層に配置 | 規約に一致/依存方向が明確 | DDDの純粋主義と異なる |

**推奨**: ユースケース層に配置し、構造でガードする。

## レビューチェックリスト

1. **配置確認**: リポジトリインターフェースがユースケース層にあるか？
2. **結合確認**: ドメインモデル（エンティティ/集約）がリポジトリをimportしていないか？
3. **ID参照確認**: 集約が他の集約を実体ではなくIDで参照しているか？

## 参考

- Martin, Robert C. "Clean Architecture" (2017)
- Vernon, Vaughn. "Implementing Domain-Driven Design" (2013)

## 関連スキル（併読推奨）
このスキルを使用する際は、以下のスキルも併せて参照すること：
- `clean-architecture`: リポジトリ配置の基盤となる4層アーキテクチャ
- `aggregate-design`: リポジトリが対応する集約の設計ルール
- `repository-design`: リポジトリの命名・CQS・メソッド設計
