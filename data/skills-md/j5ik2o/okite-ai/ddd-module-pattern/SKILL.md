---
name: ddd-module-pattern
description: >-
  DDDのモジュールパターンに基づくドメイン層パッケージングガイド。技術駆動パッケージング
  （entities/, value-objects/, services/, repositories/等）を検出し、ドメイン用語ベースの
  パッケージングへの修正を促す。ドメイン層においてモジュール名がユビキタス言語の一部となるよう導く。
  トリガー：「ドメイン層のパッケージ構造」「DDDのモジュール設計」「技術駆動パッケージングを直したい」
  「entities/フォルダをやめたい」「ドメインパッケージのレビュー」等のドメインモジュール関連リクエストで起動。
---

# DDDモジュールパターン

> 「モジュールはドメインの概念を反映すべきであり、技術的な関心事ではない」
> — Eric Evans, Domain-Driven Design (2003)

## 核心原則

**ドメイン層のパッケージ名は、ユビキタス言語の一部である。**

## 問題: 技術駆動パッケージング

```
domain/
  entities/           ← ❌ 技術的分類
    Order.java
    Customer.java
  value-objects/      ← ❌ 技術的分類
    Money.java
    OrderId.java
  services/           ← ❌ 技術的分類
    OrderService.java
```

| 問題点 | 影響 |
|--------|------|
| ドメイン構造が見えない | パッケージを見ても業務の形が分からない |
| 凝集性の低下 | 関連する概念が異なるフォルダに散在 |
| 変更の波及 | 1つの機能変更で複数フォルダを横断 |

## 解決策: ドメイン駆動パッケージング

```
domain/
  order/              ← ✅ ドメイン概念
    Order.java
    OrderId.java
    OrderItem.java
  customer/           ← ✅ ドメイン概念
    Customer.java
    CustomerId.java
  pricing/            ← ✅ ドメイン概念
    PricingPolicy.java
    Money.java
```

| 利点 | 効果 |
|------|------|
| ドメインの可視化 | パッケージ一覧 = ドメインの主要概念 |
| 高凝集 | 関連する型が同一パッケージに集約 |
| 局所的変更 | 機能変更が1パッケージで完結 |

## 検出パターン

### 避けるべきパッケージ名（ドメイン層）

```
❌ entities/
❌ value-objects/ (valueobjects/, vo/)
❌ aggregates/
❌ services/
❌ interfaces/
❌ impl/
❌ dto/
❌ domain/types/
❌ domain/core/
```

### レビューチェックリスト

1. **パッケージ名テスト**: 業務担当者に通じるか？
   - ✅ `order`, `billing`, `inventory` → 業務用語
   - ❌ `entities`, `services`, `impl` → 技術用語

2. **凝集性テスト**: 同じ業務文脈に属するか？
   - ✅ `order/` に `Order`, `OrderItem`, `OrderId`
   - ❌ `entities/` に `Order`, `Customer`, `Product`

3. **変更影響テスト**: 1業務要件で何パッケージ触るか？
   - ✅ 1-2パッケージ
   - ❌ 3パッケージ以上

## リファクタリング手順

### Step 1: ドメイン概念の抽出

```
現状分析:
- Order, OrderId, OrderItem → 「注文」概念
- Customer, CustomerId → 「顧客」概念
- Money, PricingPolicy → 「価格設定」概念
```

### Step 2: パッケージ境界の決定

```
order/
customer/
pricing/
```

### Step 3: 移動と参照更新

型を新パッケージに移動し、import文を更新。

### Step 4: 依存方向の確認

```
✅ order → pricing (注文が価格計算を使う)
❌ pricing → order (循環の可能性)
```

## 言語別ガイダンス

詳細は [references/language-guides.md](references/language-guides.md) を参照。

## 例外と注意点

### 共有カーネル (Shared Kernel)

複数ドメインで使われる基本型は共有パッケージに置いてよい：

```
domain/
  shared/           ← 許容される例外
    Money.java
    DateRange.java
  order/
  customer/
```

ただし `shared/` の肥大化は設計見直しのサイン。

### インフラストラクチャ層は別ルール

**ドメイン層以外では技術駆動パッケージングも許容**：

```
infrastructure/
  persistence/      ← 技術的分類OK
    jpa/
    redis/
```

### 小規模ドメイン

10型未満なら1階層で十分。超えたらサブパッケージを検討。

## 参考文献

- Evans, Eric. "Domain-Driven Design" (2003), Chapter 5: Modules
- Vernon, Vaughn. "Implementing Domain-Driven Design" (2013), Chapter 9: Modules

## 関連スキル（併読推奨）
このスキルを使用する際は、以下のスキルも併せて参照すること：
- `package-design`: モジュール設計の基盤となるパッケージ設計原則
- `clean-architecture`: ドメインモジュールを配置する層構造
- `domain-building-blocks`: モジュール内に配置するビルディングブロックの設計
