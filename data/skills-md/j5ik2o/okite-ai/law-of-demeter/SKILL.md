---
name: law-of-demeter
description: >-
  デメテルの法則（最小知識の原則）に基づくコードレビューと設計支援。オブジェクトの連鎖呼び出し
  （Train Wreck）を検出し、直接の友人とのみ会話する設計へ変換する。結合度の低減と
  変更容易性の向上を促進する。コードレビュー、新規実装、リファクタリング時に
  オブジェクト間の結合が深い場合に使用。
  対象言語: Java, Kotlin, Scala, TypeScript, Python, Ruby, Go, Rust。
  トリガー：「デメテルの法則」「連鎖呼び出しを減らしたい」「Train Wreckを直して」
  「結合度を下げたい」「ドット連鎖が多い」「最小知識の原則」「Law of Demeter」
  といったオブジェクト間結合関連リクエストで起動。
---

# Law of Demeter

直接の友人とだけ話せ。見知らぬ者に話しかけるな。

## 核心原則

**メソッドは「直接の友人」のメソッドだけを呼び出し、「友人の友人」には手を出さない。**

Karl Liebherr（1987年、ノースイースタン大学）が提唱。正式名称は「最小知識の原則（Principle of Least Knowledge）」。

| アプローチ | 特徴 | 問題 |
|-----------|------|------|
| 連鎖呼び出し | `a.getB().getC().doX()` | 内部構造に依存、変更に脆い |
| 委譲 | `a.doX()` | 結合度が低い、変更に強い |

## 4つのルール

メソッド `M` が呼び出してよいのは、以下の4種類のメソッドのみ：

| # | 許可される呼び出し先 | 説明 |
|---|---------------------|------|
| 1 | 自身（`this` / `self`）のメソッド | 自分のクラスに定義されたメソッド |
| 2 | `M` の引数として渡されたオブジェクトのメソッド | パラメータ経由の直接の友人 |
| 3 | `M` 内で生成したオブジェクトのメソッド | 自分が作ったオブジェクトは友人 |
| 4 | 自身のインスタンス変数（フィールド）のメソッド | 保持しているオブジェクトは友人 |

**禁止**: 上記メソッド呼び出しの**戻り値**のメソッドを呼び出すこと（＝友人の友人）

## 判断フロー

```
メソッド内で obj.method() を呼んでいる
    ↓
obj はどこから来たか？
    ├─ this/self のフィールド → ✅ 許可（ルール4）
    ├─ メソッドの引数 → ✅ 許可（ルール2）
    ├─ メソッド内で new/生成した → ✅ 許可（ルール3）
    ├─ this/self 自身 → ✅ 許可（ルール1）
    └─ 別のメソッド呼び出しの戻り値 → ❌ 違反（友人の友人）
```

## アンチパターン検出

### Train Wreck（列車事故）

連鎖的なドット呼び出しでオブジェクトの内部構造をたどるパターン：

```
❌ order.getCustomer().getAddress().getCity()
❌ user.getProfile().getSettings().getTheme().getName()
❌ app.getConfig().getDatabase().getConnection().execute(query)
❌ invoice.getLineItems().get(0).getProduct().getCategory()
```

### 検出基準

| パターン | 問題 |
|---------|------|
| ドットが2つ以上の連鎖 | 構造依存（ただし流暢APIは例外） |
| getter連鎖 + 末尾の操作 | 取得したオブジェクトの操作 = 友人の友人 |
| getter連鎖 + if文 | 遠いオブジェクトの状態で分岐 |

## 変換パターン

### 1. 委譲メソッドの導入

```java
// ❌ 違反: 友人(order)の友人(customer)の友人(address)に話しかけている
City city = order.getCustomer().getAddress().getCity();

// ✅ 修正: 各レベルに委譲メソッドを追加
City city = order.getShippingCity();

// Order
public City getShippingCity() {
    return customer.getShippingCity();
}

// Customer
public City getShippingCity() {
    return address.getCity();
}
```

### 2. 目的に応じたメソッド名

```java
// ❌ 違反: 内部構造を露出した名前
Email email = order.getCustomer().getEmail();

// ✅ 修正: 目的を表すメソッドを提供
Email email = order.getNotificationEmail();
```

### 3. パラメータとして渡す

```java
// ❌ 違反: 遠いオブジェクトを取得して使用
void processOrder(Order order) {
    PaymentGateway gateway = order.getCustomer().getPaymentGateway();
    gateway.charge(order.getTotal());
}

// ✅ 修正: 必要なオブジェクトを引数で受け取る
void processOrder(Order order, PaymentGateway gateway) {
    gateway.charge(order.getTotal());
}
```

### 4. 振る舞いをオブジェクトに移動

```java
// ❌ 違反: 外部で判定
if (order.getCustomer().getAddress().getCountry().equals("JP")) {
    applyJapaneseTax(order);
}

// ✅ 修正: 判定ロジックをオブジェクトに持たせる
Order orderUpdated = order.applyApplicableTax();

// Order
public Order applyApplicableTax() {
    return customer.applyTaxFor(this);
}
```

## 例外：違反ではないケース

### 1. 流暢API / ビルダーパターン

```java
// ✅ 許可: 流暢APIは同一オブジェクトを返す
User user = User.builder()
    .name("Alice")
    .email("alice@example.com")
    .build();
```

**理由**: 各メソッドが `this` を返すため、友人の友人ではなく同じ友人と会話し続けている。

### 2. データ構造（DTO / Value Object）

```java
// ✅ 許可: DTOは振る舞いを持たない単なるデータ構造
City city = addressDto.getCity();
int zip = addressDto.getZipCode();
```

**理由**: DTOは内部構造の隠蔽を目的としない。ただし、ドメインオブジェクトでは違反。

### 3. ストリーム / コレクション操作

```java
// ✅ 許可: ストリームAPIの連鎖
List<String> names = users.stream()
    .filter(u -> u.isActive())
    .map(u -> u.getName())
    .collect(Collectors.toList());
```

**理由**: ストリームAPIは流暢APIの一種であり、内部構造の探索ではない。

### 4. 標準ライブラリの連鎖

```python
# ✅ 許可: 標準ライブラリの連鎖
result = text.strip().lower().replace(" ", "_")
```

**理由**: 同一型（String）のメソッド連鎖であり、内部構造への依存ではない。

## 過剰適用の警告

### 「ラッパーメソッドの爆発」に注意

```java
// 過剰: すべてのフィールドに委譲メソッドを作成
class Order {
    Name getCustomerName() { return customer.getName(); }
    Email getCustomerEmail() { return customer.getEmail(); }
    Phone getCustomerPhone() { return customer.getPhone(); }
    City getCustomerCity() { return customer.getAddress().getCity(); }
    // ... 延々と続く
}
```

**対処**: 本当に必要な操作だけを委譲する。全フィールドの委譲は設計の問題を示す。

### 判断基準

| 状況 | 対応 |
|------|------|
| 委譲メソッドが3個以内 | 適切 |
| 委譲メソッドが4個以上 | 設計を見直す（責務の分割を検討） |
| 同じ委譲先への委譲が大量 | そのオブジェクトを直接使うべきか検討 |

## 関連原則

| 原則 | 関係 |
|------|------|
| Tell, Don't Ask | 補完関係。TDAは「命じよ」、LoD は「友人にだけ」 |
| カプセル化 | LoD はカプセル化を構造的に強制する手段 |
| 疎結合 | LoD の遵守は結合度を機械的に低下させる |
| 単一責任原則 | 委譲メソッドの爆発は SRP 違反のサイン |
| breach-encapsulation-naming | getter を明示的に制限する命名規約 |

## レビュー観点

コードレビュー時の確認ポイント：

1. **ドット連鎖**: `a.b().c()` 形式の連鎖が2段以上ないか
2. **getter連鎖**: 取得→取得→操作のパターンはないか
3. **遠いオブジェクトへの依存**: メソッドが知るべきでないオブジェクトを参照していないか
4. **例外の確認**: 流暢API / DTO / ストリームなら許容

## 詳細ガイドライン

言語別の実装パターン、リファクタリング手順の詳細は [references/patterns.md](references/patterns.md) を参照。

## 関連スキル（併読推奨）
このスキルを使用する際は、以下のスキルも併せて参照すること：
- `tell-dont-ask`: 振る舞い面の補完原則（状態を問い合わせず命じる）
- `first-class-collection`: コレクションへのデメテルの法則適用パターン
- `breach-encapsulation-naming`: 連鎖呼び出しが避けられない場合の命名規約
