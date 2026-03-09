---
name: when-to-wrap-primitives
description: >-
  プリミティブ型をドメイン固有型でラップすべきか否かの判断を支援する。
  Primitive Obsession（プリミティブ型の過剰使用）と Value Object Obsession（過剰なラップ）の
  両極端を避け、投資対効果に基づく合理的な判断基準を提供する。
  Value Objectの定義が文脈（PofEAA/DDD/一般）で異なることによる用語混乱の防止も含む。
  コードレビュー、新規実装、設計議論時にプリミティブ型のラップ判断が必要な場合に使用。
  対象言語: 言語非依存（Rust, TypeScript, Java, Kotlin, Scala, Go, Python等すべて）。
  トリガー：「この値をラップすべきか」「プリミティブ型のままでいいか」
  「Value Objectにすべきか」「型を作りすぎでは」「Primitive Obsession」
  「ラップしすぎ」「型が多すぎる」「Stringのままでいいか」
  といったプリミティブ型ラップ判断関連リクエストで起動。
---

# プリミティブ型ラップ判断ガイド

プリミティブ型をラップすべきか否かは、**コスト対効果**で判断する。盲目的にラップするのも、
一切ラップしないのも、どちらも設計の失敗である。

## 前提: Value Objectの定義は1つではない

「Value Object」という用語は文脈によって意味が異なる。議論やレビューで混乱が生じる主因である。

| 定義 | 出典 | スコープ | 核心 |
|------|------|----------|------|
| 一般的定義 | Wikipedia等 | 最も広い | 同等性がIDではなく値に基づくオブジェクト |
| PofEAA定義 | Martin Fowler | 実装パターン | IDに基づかず値で等価判定される小型オブジェクト。別名参照問題を避けるため不変が推奨 |
| DDD定義 | Eric Evans | ドメインモデリング | PofEAA版の特性をすべて備えた上で、ドメインの概念を計測・定量化・説明し、不変条件と副作用のない振る舞いを持つドメインオブジェクト |

### DDD版はPofEAA版のextends

DDD版VOとPofEAA版VOは独立した概念ではなく、**特化（specialization）の関係**にある。

| 特性 | PofEAA VO | DDD VO |
|------|-----------|--------|
| 値による等価判定 | 必須 | 必須（継承） |
| 不変性 | 推奨 | 必須（強化） |
| ドメイン不変条件 | ー | 必須（追加） |
| ドメイン振る舞い | ー | 必須（追加） |

つまり：
- **DDD VO IS-A PofEAA VO** → すべてのDDD VOはPofEAA VOでもある
- **PofEAA VO IS-A DDD VO** → 成立しない（Ruby HashはPofEAA VOだがDDD VOではない）

DDD版は「値で等価判定される」「不変である」というPofEAA版の特性を**前提として含んだ上で**、
ドメイン固有の要件を追加したものである。2つの定義を並列に見ると、DDD版が
PofEAA版の特性も持っていることを見落としやすいので注意。

**チーム内では「PofEAAのVO」「DDDのVO」のように文脈を明示して使い分けるべき。**

### 本スキルの立場

本スキルでは、「プリミティブ型をドメイン固有型でラップすべきか」という実践的判断に焦点を当てる。
VOの定義論争には立ち入らず、**ラップすることで得られる具体的な利益がコストに見合うか**で判断する。

## 2つのアンチパターン

### Primitive Obsession（プリミティブ型への固執）

すべてをString/int/floatで表現し、ドメインの制約がコードに表れない。

```
fn transfer(from: String, to: String, amount: f64)
// fromとtoを取り違えてもコンパイルが通る
// amountが負でもコンパイルが通る
// 通貨の概念がない
```

**症状**:
- 同じプリミティブ型の引数が2つ以上並ぶ
- バリデーションロジックが呼び出し側に散在
- 「この文字列はメールアドレスのはず」という暗黙の前提
- 単位の取り違え（メートルとフィート、円とドル）

### Value Object Obsession（過剰なラップ）

すべてのプリミティブ型を機械的にクラスで包み、複雑性だけが増す。

```
class CustomerFirstName(value: String)
class CustomerLastName(value: String)
class ShippingFirstName(value: String)  // CustomerFirstNameと何が違う？
class ShippingLastName(value: String)   // 同上
```

**症状**:
- 不変条件やドメインロジックを持たない「ただのラッパー」が大量に存在
- 文脈ごとに別の型を作るが、中身のバリデーションは同一
- 型変換のボイラープレートがドメインロジックより多い
- 新規メンバーが型の森で迷子になる

## 判断フレームワーク

### 5つの判断基準

プリミティブ型をラップすべきかを以下の基準で評価する。
**1つでも強くYesならラップを検討。複数Yesなら強く推奨。すべてNoならラップ不要。**

#### 基準1: ドメイン不変条件があるか

その値に「常に満たすべき制約」があるか？

| 例 | 不変条件 | 判断 |
|----|----------|------|
| メールアドレス | RFC準拠のフォーマット | ラップする |
| 金額 | 非負、通貨との組み合わせ | ラップする |
| 年齢 | 0〜150の範囲 | ラップする |
| ログメッセージ | 特に制約なし | ラップ不要 |
| 一時的なループカウンタ | なし | ラップ不要 |

#### 基準2: 取り違えリスクがあるか

同じプリミティブ型の引数が複数並び、取り違えてもコンパイラが検出できないか？

```
// ❌ userIdとorderIdは両方String。取り違えても気づかない
fn find_order(user_id: String, order_id: String)

// ✅ 型が異なるのでコンパイラが検出する
fn find_order(user_id: UserId, order_id: OrderId)
```

**特にID型は取り違えの被害が大きい。異なる概念のIDは型で区別すべき。**

#### 基準3: ドメイン操作を集約できるか

その値に関連する操作（加算、比較、変換など）がドメインロジックとして存在するか？

| 例 | ドメイン操作 | 判断 |
|----|------------|------|
| Money | 加算（同一通貨のみ）、通貨変換、比較 | ラップする |
| DateRange | 重複判定、包含判定、期間計算 | ラップする |
| 単なる名前文字列 | 特になし | 慎重に検討 |

#### 基準4: 複数の値が不可分か

2つ以上の値が常にセットで意味を持つか？

```
// ❌ 金額と通貨が別々に渡される → 不整合の可能性
fn price(amount: f64, currency: String)

// ✅ 不可分な値を1つの型にまとめる
fn price(money: Money)
```

#### 基準5: 利用箇所が複数あるか

その型が複数のコンテキスト（モジュール、レイヤー、関数）で使われるか？

| 状況 | 判断 |
|------|------|
| 3つ以上のモジュールで使われる | ラップの価値が高い |
| 2つのモジュールで使われる | 他の基準と合わせて検討 |
| 1つの関数内でしか使わない | ラップ不要（YAGNI） |

### 判断フロー

```
プリミティブ型を使おうとしている
    │
    ├─ 不変条件がある？ ─── Yes ──→ ラップする
    │                                （domain-primitives-and-always-valid スキル参照）
    │
    ├─ 取り違えリスクがある？ ─── Yes ──→ ラップする（特にID型）
    │
    ├─ ドメイン操作がある？ ─── Yes ──→ ラップする
    │
    ├─ 複数値が不可分？ ─── Yes ──→ 複合型としてラップする
    │
    ├─ 利用箇所が多い？ ─── Yes ──→ 他の基準と合わせて検討
    │
    └─ すべて No ──→ プリミティブ型のままでよい
```

## ラップの度合い: 3段階

すべてを「フルスペックの型」にする必要はない。状況に応じて適切な粒度を選ぶ。

### レベル1: 型エイリアス（最軽量）

不変条件はないが、取り違え防止や可読性向上が目的の場合。

```typescript
// TypeScript
type UserId = string & { readonly __brand: unique symbol };
type OrderId = string & { readonly __brand: unique symbol };
```

```rust
// Rust（newtype）
pub struct UserId(String);
pub struct OrderId(String);
```

**適用場面**: 不変条件なし、取り違え防止が主目的

### レベル2: 構築時検証付き型

不変条件があり、無効な値のインスタンス化を防ぐ。

```rust
pub struct Email(String);

impl Email {
    pub fn new(value: &str) -> Result<Self, EmailError> {
        if !value.contains('@') || value.len() <= 3 {
            return Err(EmailError::InvalidFormat);
        }
        Ok(Self(value.to_string()))
    }
}
```

**適用場面**: 明確な不変条件がある

### レベル3: 振る舞いを持つドメイン型

不変条件 + ドメイン操作を集約する。

```rust
pub struct Money { amount: Decimal, currency: Currency }

impl Money {
    pub fn add(&self, other: &Money) -> Result<Money, MoneyError> {
        if self.currency != other.currency {
            return Err(MoneyError::CurrencyMismatch);
        }
        Money::new(self.amount + other.amount, self.currency)
    }
}
```

**適用場面**: 不変条件 + そこに属すべきドメイン操作がある

## 言語特性による選択肢

ラップの手段はクラス化だけではない。言語機能に応じて適切な手段を選ぶ。

| 言語 | 軽量な手段 | フルラップ |
|------|-----------|-----------|
| Rust | newtype（`struct Foo(T)`） | newtype + impl |
| TypeScript | Branded Types | class with private constructor |
| Kotlin | value class | data class |
| Scala | opaque type / value class | case class |
| Go | `type Foo string` | struct + コンストラクタ関数 |
| Java | ー（軽量手段がない） | record / final class |
| Python | NewType（typing） | dataclass(frozen=True) |

**原則**: 不変条件がなく取り違え防止だけが目的なら、その言語で最も軽量な手段を使う。

## レビューチェックリスト

### 「ラップすべきなのにしていない」の検出

- [ ] 同じプリミティブ型の引数が2つ以上並んでいないか
- [ ] バリデーションが呼び出し側に散在していないか
- [ ] 「この文字列は〇〇のはず」という暗黙の前提がないか
- [ ] 異なる概念のIDが同じ型（String等）で表現されていないか
- [ ] 不可分な値のペア（金額+通貨等）が別々の引数になっていないか

### 「ラップしすぎ」の検出

- [ ] 不変条件もドメイン操作もない「ただのラッパー」がないか
- [ ] 型変換のボイラープレートがドメインロジックより多くないか
- [ ] 文脈ごとに型を分けたが、中身のバリデーションが同一ではないか
- [ ] 1箇所でしか使わない型をわざわざ作っていないか
- [ ] 型の数がチームの認知負荷を超えていないか

## 関連スキルとの使い分け

| スキル | フォーカス | 使うタイミング |
|--------|----------|---------------|
| **本スキル** | ラップすべきか否かの判断 | 「この型を作るべきか？」という意思決定時 |
| domain-primitives-and-always-valid | ラップする場合の設計と実装 | ラップすると決めた後の具体的な設計時 |
| domain-building-blocks | VO/Entity/Aggregate等の設計全般 | ドメインモデル全体の構造を設計するとき |
| parse-dont-validate | 検証結果を型で保持する変換 | validate→parse変換をレビューするとき |

## 議論のための用語整理

チームで議論する際、**パターン（設計概念）と実装技法を混同しない**ことが重要である。

### パターン（何であるか）

| パターン | 出典 | 定義 | 関係 |
|----------|------|------|------|
| Value Object（PofEAA） | Fowler | 値で等価判定されるオブジェクト。不変が推奨 | 基底 |
| Value Object（DDD） | Evans | PofEAA VOを継承し、ドメイン不変条件と振る舞いを追加 | PofEAA VOのextends |
| Domain Primitive | Johnsson et al. | 構築時検証・不変性・自己完結性を備えたドメイン固有の最小単位の型 | Secure by Design由来 |

### 実装技法（どう作るか）

| 技法 | 特性 | 例 |
|------|------|-----|
| Branded Type / Newtype | 型レベルで区別するが、ランタイム検証なし | Rust: `struct UserId(String)` |
| Smart Constructor | 構築時に不変条件を検証。無効な値を作れない | `Email::new(s) -> Result<Email, Error>` |
| 振る舞い付きドメイン型 | 不変条件 + ドメイン操作をカプセル化 | `Money::add(&self, other) -> Result<Money, Error>` |

### パターンと実装技法の対応

| パターン | 典型的な実装技法 |
|----------|-----------------|
| PofEAA VO | いずれの技法でも実現可能（値の等価性を実装すればよい） |
| DDD VO | Smart Constructor または 振る舞い付きドメイン型 |
| Domain Primitive | Smart Constructor（最小単位なので振る舞いは少ないことが多い） |

**推奨**: 「Value Objectにすべき」のようにパターン名だけで語らず、
「この値にはドメイン不変条件があるからSmart Constructorで保護すべき」
「取り違えリスクがあるからNewtypeで型を区別すべき」のように、**理由と実装技法をセットで**述べる。

## 参考文献

- Dan Bergh Johnsson et al. "Secure by Design" - Domain Primitivesの原典
- Martin Fowler "Patterns of Enterprise Application Architecture" - PofEAA版Value Objectの定義
- Eric Evans "Domain-Driven Design" - DDD版Value Objectの定義
- J. B. Rainsberger "Demystifying the Dependency Inversion Principle" - Primitive Obsessionへの言及
- ThoughtWorks "Object Calisthenics" - 「Wrap All Primitives」ルールの出典（練習用であり本番ルールではない）

## 関連スキル（併読推奨）
このスキルを使用する際は、以下のスキルも併せて参照すること：
- `domain-primitives-and-always-valid`: ラップする判断後の具体的な設計パターン
- `parse-dont-validate`: ラップ時に適用するparseパターン
- `domain-building-blocks`: ラップされたプリミティブが属する値オブジェクトの設計
