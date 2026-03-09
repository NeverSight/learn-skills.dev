---
name: tell-dont-ask
description: >-
  「Tell, Don't Ask」原則に基づくコードレビューと設計支援。オブジェクトの状態を問い合わせて
  外部で判断するパターンを、オブジェクトに直接命じるパターンに変換する。カプセル化を強化し、
  責任をデータを持つオブジェクトに集約する設計を促進する。コードレビュー、新規実装、
  リファクタリング時にgetterの乱用やFeature Envyの改善が必要な場合に使用。
  対象言語: Java, Kotlin, Scala, TypeScript, Python, Ruby, Go, Rust。
  トリガー：「getterを減らしたい」「カプセル化を改善して」「Feature Envyを直して」
  「オブジェクトに責任を持たせたい」「デメテルの法則」といったOOP設計関連リクエストで起動。
---

# Tell, Don't Ask

オブジェクトに問い合わせるな、命じよ。

## 核心原則

**オブジェクトの内部状態に基づく意思決定をし、その結果で該当オブジェクトを更新してはならない。**
（『達人プログラマー 第2版』167ページ）

| アプローチ | 特徴 | 問題 |
|-----------|------|------|
| Ask | 状態を取得→外部で判断→操作 | ロジックが散在、カプセル化破壊 |
| Tell | オブジェクトに直接命じる | 責任集約、変更に強い |

## 判断フロー

```
オブジェクトのメソッド呼び出し
    ↓
getterで状態を取得しているか？
    ├─ YES → その後ifで判定している？
    │         ├─ YES → Askパターン（問題あり）
    │         └─ NO → 表示/出力目的なら許容
    └─ NO → Tellパターン（推奨）
```

## アンチパターン検出

以下のパターンを見つけたら変換を検討：

```
❌ if (obj.getX() > threshold) { obj.setY(...) }
❌ if (obj.getStatus() == ACTIVE) { doSomething(obj) }
❌ obj.getA().getB().doSomething()  // デメテルの法則違反
❌ for (item : list) { total += item.getPrice() }
❌ if (user.getRole() == ADMIN) { ... }
```

## 変換パターン

### 1. 状態判定の内部化

```java
// ❌ Ask: 状態を取得して外部で判断
if (user.getAge() >= 18) {
    allowAccess(user);
}

// ✅ Tell: 判定ロジックをオブジェクトに持たせる
if (user.isAdult()) {
    allowAccess(user);
}

// ✅✅ さらに良い: 処理自体を委譲
user.ifAdult(() -> allowAccess());
```

### 2. 条件分岐のポリモーフィズム化

```java
// ❌ Ask: 型で分岐
if (user.getType() == UserType.ADMIN) {
    sendAdminNotification(user);
} else {
    sendUserNotification(user);
}

// ✅ Tell: 各クラスに責任を持たせる
user.sendNotification();  // Admin/RegularUserで実装が異なる
```

### 3. コレクション操作の委譲

```java
// ❌ Ask: 外部で集計
int total = 0;
for (Item item : order.getItems()) {
    total += item.getPrice();
}

// ✅ Tell: オブジェクトに集計を任せる
int total = order.calculateTotal();
```

### 4. Nullオブジェクトパターン

```java
// ❌ Ask: null判定の分岐
Address addr = user.getAddress();
if (addr != null) {
    return addr.format();
} else {
    return "住所未登録";
}

// ✅ Tell: NullObjectでデフォルト動作を定義
return user.getAddress().format();  // NullAddressは"住所未登録"を返す
```

## 関連原則・スキル

| 原則 / スキル | 関係 |
|------|------|
| law-of-demeter | 連鎖呼び出しを避ける（`a.getB().getC()` → `a.doC()`） |
| Feature Envy | 他クラスのデータに執着 → 責任を移動 |
| 単一責任原則 | データと処理を同じ場所に |
| カプセル化 | 内部状態を隠蔽し振る舞いを公開 |
| breach-encapsulation-naming | getter命名でカプセル化破壊を明示 |

## 適用指針

### 推奨

- getter後にif文で判定しているコード
- 同じ判定ロジックが複数箇所に散在
- オブジェクトの状態を取得→更新するパターン
- 型やステータスによる条件分岐

### 過剰適用を避ける

- 表示/レポート目的のデータ取得
- DTO/Value Objectからの単純な値取得
- フレームワーク/ライブラリの制約がある場合
- クラスが肥大化する場合は責任分割を検討

## レビュー観点

コードレビュー時の確認ポイント：

1. **getter + if**: 状態取得後に条件分岐していないか
2. **連鎖呼び出し**: `a.getB().getC()` のようなチェーンはないか
3. **外部での集計**: ループでデータ収集していないか
4. **型/ステータス分岐**: ポリモーフィズムで置換できないか

## 詳細ガイドライン

言語別の実装パターン、リファクタリング手順の詳細は [references/patterns.md](references/patterns.md) を参照。

## 関連スキル（併読推奨）
このスキルを使用する際は、以下のスキルも併せて参照すること：
- `law-of-demeter`: 構造面の補完原則（直接の友人とのみ会話する）
- `first-class-collection`: コレクションへのTell, Don't Ask適用パターン
- `breach-encapsulation-naming`: カプセル化を破る必要がある場合の命名規約
