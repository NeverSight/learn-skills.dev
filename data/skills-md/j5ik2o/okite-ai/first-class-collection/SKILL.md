---
name: first-class-collection
description: >-
  ファーストクラスコレクションパターンの設計・実装を支援。コレクションをラップする専用クラスの
  設計、ドメインロジックの集約、不変性の確保をガイド。コードレビュー、新規実装、リファクタリング
  時にコレクション操作ロジックが散在している場合に使用。
  対象言語: Java, Kotlin, Scala, TypeScript, Python, Ruby, Go, Rust。
  トリガー：「コレクションをラップしたい」「リストのロジックを集約」「ファーストクラスコレクション」
  「コレクション操作が散在」「List<Order>をOrdersクラスに」といったコレクション設計関連リクエストで起動。
---

# First Class Collection

コレクションをラップする専用クラスを作成し、ドメインロジックを集約する。

## 核心原則

**コレクションをラップするクラスは、コレクション以外のフィールドを持たない。**
（ThoughtWorks Anthology, Object Calisthenics Rule 4）

| アプローチ | 特徴 | 問題 |
|-----------|------|------|
| 生のコレクション | `List<Order> orders` | ロジック散在、ドメイン概念の欠如 |
| ファーストクラス | `Orders orders` | 責任集約、ドメイン表現、不変性保証 |

## 判断フロー

```
コレクション型のフィールド/変数
    ↓
ビジネスロジック（集計/フィルタ/バリデーション）が必要か？
    ├─ YES → ファーストクラスコレクション化を検討
    │         ├─ 同じ操作が複数箇所にあるか？ → 必須
    │         └─ 1箇所のみ → 将来性を考慮して判断
    └─ NO → 生のコレクションで可
```

## アンチパターン検出

以下のパターンを見つけたら変換を検討：

```
❌ orders.stream().filter(o -> o.getStatus() == PENDING).toList()  // 複数箇所で同じフィルタ
❌ int total = items.stream().mapToInt(Item::getPrice).sum()       // 呼び出し側で集計
❌ if (users.isEmpty()) throw new EmptyUsersException()            // バリデーション散在
❌ for (Order o : orders) { if (o.isOverdue()) ... }               // 外部でループ処理
❌ orders.add(order)                                                // 直接変更可能
```

## 変換パターン

以下の説明にはJavaのコレクションを利用しているが、提供される種々の型は可変コレクションであるため、内部のコレクションをそのまま返すことができないので、複製を作るなど工夫が必要になる。しかし、Scalaのように不変コレクションがある場合は、わざわざそのような考慮は不要であるため、不変コレクションがある場合は優先して利用すること。

### 1. 基本構造

```java
// ❌ 生のコレクション
List<Order> orders;

// ✅ ファーストクラスコレクション
public final class Orders {
    private final List<Order> values;

    public Orders(List<Order> values) {
        this.values = List.copyOf(values);  // 不変性保証
    }

    // ドメインロジックをここに集約
}
```

### 2. 集計ロジックの集約

```java
// ❌ 呼び出し側で集計
Money total = Money.ZERO;
for (Order order : orders) {
    total = total.add(order.getAmount());
}

// ✅ コレクションに集約
public Money totalAmount() {
    return values.stream()
        .map(Order::amount)
        .reduce(Money.ZERO, Money::add);
}
```

### 3. フィルタリングの内部化

```java
// ❌ 外部でフィルタリング
List<Order> pending = orders.stream()
    .filter(o -> o.getStatus() == PENDING)
    .toList();

// ✅ ドメイン用語でメソッド化
public Orders pending() {
    return new Orders(
        values.stream()
            .filter(Order::isPending)
            .toList()
    );
}
```

### 4. バリデーションの集約

```java
// ❌ 外部でバリデーション
if (orders.isEmpty()) {
    throw new IllegalArgumentException("注文がありません");
}

// ✅ 生成時にバリデーション
public Orders(List<Order> values) {
    if (values.isEmpty()) {
        throw new EmptyOrdersException();
    }
    this.values = List.copyOf(values);
}
```

### 5. 不変な追加操作

```java
// ❌ 破壊的変更
orders.add(newOrder);

// ✅ 新しいインスタンスを返す
public Orders add(Order order) {
    List<Order> newList = new ArrayList<>(values);
    newList.add(order);
    return new Orders(newList);
}
```

## 言語別イディオム

### TypeScript

```typescript
class Orders {
    private constructor(private readonly values: readonly Order[]) {}

    static of(orders: Order[]): Orders {
        return new Orders([...orders]);
    }

    totalAmount(): Money {
        return this.values.reduce(
            (sum, order) => sum.add(order.amount),
            Money.ZERO
        );
    }
}
```

### Rust

```rust
pub struct Orders(Vec<Order>);

impl Orders {
    pub fn new(orders: Vec<Order>) -> Self {
        Self(orders)
    }

    pub fn total_amount(&self) -> Money {
        self.0.iter().map(|o| o.amount()).sum()
    }

    pub fn pending(&self) -> Self {
        Self(self.0.iter().filter(|o| o.is_pending()).cloned().collect())
    }
}
```

### Python

```python
@dataclass(frozen=True)
class Orders:
    _values: tuple[Order, ...]

    @classmethod
    def of(cls, orders: list[Order]) -> "Orders":
        return cls(tuple(orders))

    def total_amount(self) -> Money:
        return sum((o.amount for o in self._values), Money.ZERO)
```

### Go

```go
type Orders struct {
    values []Order
}

func NewOrders(orders []Order) Orders {
    copied := make([]Order, len(orders))
    copy(copied, orders)
    return Orders{values: copied}
}

func (o Orders) TotalAmount() Money {
    total := ZeroMoney()
    for _, order := range o.values {
        total = total.Add(order.Amount())
    }
    return total
}

func (o Orders) Pending() Orders {
    var pending []Order
    for _, order := range o.values {
        if order.IsPending() {
            pending = append(pending, order)
        }
    }
    return NewOrders(pending)
}
```

## 設計指針

### ファーストクラスコレクション化すべきもの

- ドメインで名前がつくコレクション（「注文一覧」「在庫リスト」等）
- 集計・フィルタリング・検証ロジックを持つ
- 複数箇所から同じ操作をされる
- ビジネスルールに関わる制約がある

### 生のコレクションで良いもの

- 純粋なデータ転送（DTO内のリスト）
- フレームワーク/ライブラリの制約
- 一時的な中間データ
- ロジックが不要な単純なグループ化

## レビュー観点

1. **ロジック散在**: 同じコレクション操作が複数箇所にないか
2. **ドメイン概念**: コレクションにビジネス上の名前があるか
3. **不変性**: 外部から直接変更されていないか
4. **責任**: Tell, Don't Askに従っているか

## 関連原則

| 原則 | 関係 |
|------|------|
| Tell, Don't Ask | コレクションに問い合わせず命じる |
| 単一責任原則 | コレクション操作を一箇所に集約 |
| DRY | 重複するコレクション操作を排除 |
| カプセル化 | 内部リストを隠蔽 |

## 詳細ガイドライン

言語別の詳細パターン、イテレータ実装、テスト方法は [references/patterns.md](references/patterns.md) を参照。

## 関連スキル（併読推奨）
このスキルを使用する際は、以下のスキルも併せて参照すること：
- `tell-dont-ask`: コレクションに命じるパターンの基盤原則
- `law-of-demeter`: コレクション内部への直接アクセスを防ぐ原則
- `intent-based-dedup`: 同じ構造のコレクションでも意図が異なれば共通化しない判断
