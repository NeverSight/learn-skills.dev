---
name: sqlalchemy-query-patterns
description: SQLAlchemy の効率的なクエリパターン集。N+1回避、サブクエリ、バルク操作、インデックス活用、EXPLAIN解析など、SQLite ベースのプロジェクトに適用できるクエリ最適化ガイド。Use when writing new queries, optimizing slow queries, or reviewing database access patterns.
metadata:
  short-description: SQLAlchemy効率クエリ（N+1回避、バルク操作、インデックス、EXPLAIN）。
allowed-tools:
  - Grep
  - Glob
  - Read
  - Write
  - Edit
  - Bash
---

# SQLAlchemy Efficient Query Patterns

SQLite ベースのプロジェクトに適用できる、効率的な SQLAlchemy クエリパターン集。

## When to Use

Use this skill when:
- 新しいクエリメソッドを作成する
- 既存クエリのパフォーマンスを改善する
- N+1 クエリ問題を検出・修正する
- バルク操作を実装する
- クエリの実行計画を確認する

## 対象プロジェクトの前提

SQLite + SQLAlchemy ORM + Repository パターンの構成を想定。具体のスキーマ/リポジトリ配置は導入先に従う。

以降のコード例では、EC（受注管理）を題材にした以下のようなモデル構成を例として使う:

```
Order ──┬── OrderItem (1:N)  - 注文明細（OrderItem は Product を N:1 参照）
        └── Payment (1:N)    - 支払い記録

Product ──┬── Review (1:N)   - レビュー
          └── Category (M:N) - 商品カテゴリ
```

## 1. N+1 クエリ回避

### 問題: N+1 クエリ

```python
# ❌ BAD: N+1 クエリ（注文ごとに明細を個別取得）
with session_factory() as session:
    orders = session.execute(select(Order)).scalars().all()
    for order in orders:
        items = order.items  # 注文ごとに追加クエリ発行！
```

### 解決策 1: selectinload（推奨）

```python
from sqlalchemy.orm import selectinload

# ✅ GOOD: IN句で一括取得（2クエリ）
def get_orders_with_items(self) -> list[Order]:
    """注文一覧を明細付きで取得（selectinload）。

    Returns:
        明細をeager loadした注文リスト。
    """
    with self.session_factory() as session:
        stmt = (
            select(Order)
            .options(selectinload(Order.items))
            .order_by(Order.id)
        )
        return list(session.execute(stmt).scalars().all())
```

### 解決策 2: joinedload（1対1 / 少数リレーション向け）

```python
from sqlalchemy.orm import joinedload

# ✅ GOOD: JOINで1クエリ（子が少ない場合に有効）
def get_order_with_products(self, order_id: int) -> Order | None:
    """注文と商品情報をJOINで一括取得。

    Args:
        order_id: 注文ID。

    Returns:
        商品情報付きの注文。見つからない場合はNone。
    """
    with self.session_factory() as session:
        stmt = (
            select(Order)
            .options(joinedload(Order.items).joinedload(OrderItem.product))
            .where(Order.id == order_id)
        )
        return session.execute(stmt).unique().scalar_one_or_none()
```

### 解決策 3: 複数リレーション同時ロード

```python
# ✅ GOOD: 明細・支払い・商品情報を一括ロード
def get_order_full(self, order_id: int) -> Order | None:
    """注文の全関連データを一括取得。

    Args:
        order_id: 注文ID。

    Returns:
        全リレーションをeager loadした注文。
    """
    with self.session_factory() as session:
        stmt = (
            select(Order)
            .options(
                selectinload(Order.items),
                selectinload(Order.items).selectinload(OrderItem.product),
                selectinload(Order.payments),
            )
            .where(Order.id == order_id)
        )
        return session.execute(stmt).unique().scalar_one_or_none()
```

### 使い分けガイド

| パターン | 用途 | SQL | 適用例 |
|---|---|---|---|
| `selectinload` | 1:N リレーション | `SELECT ... WHERE id IN (...)` | Order→OrderItems, Order→Payments |
| `joinedload` | 1:1 / N:1 リレーション | `LEFT JOIN` | OrderItem→Product |
| `subqueryload` | 大量データの1:N | サブクエリ | 大規模バッチ処理 |
| `raiseload` | アクセス禁止（検出用） | N/A | デバッグ時のN+1検出 |

## 2. 効率的な SELECT パターン

### 必要なカラムだけ取得

```python
# ❌ BAD: 全カラム取得（不要なデータもメモリに載る）
products = session.execute(select(Product)).scalars().all()

# ✅ GOOD: 必要なカラムだけ取得
stmt = select(Product.id, Product.sku, Product.name).where(Product.is_active == True)
rows = session.execute(stmt).all()  # Row オブジェクト（軽量）
```

### EXISTS で存在チェック

```python
from sqlalchemy import exists

# ❌ BAD: 全件取得してlen()で判定
orders = session.execute(select(Order).where(...)).scalars().all()
has_orders = len(orders) > 0

# ✅ GOOD: EXISTS サブクエリ（即座にbool返却）
def has_unpaid_orders(self) -> bool:
    """未払い注文の存在を高速チェック。

    Returns:
        未払い注文が1件以上あればTrue。
    """
    with self.session_factory() as session:
        stmt = select(
            exists().where(
                and_(
                    Order.is_active == True,
                    ~exists().where(Payment.order_id == Order.id),
                )
            )
        )
        return bool(session.execute(stmt).scalar())
```

### COUNT の効率化

```python
# ❌ BAD: Pythonでlen()
count = len(session.execute(select(Order)).scalars().all())

# ✅ GOOD: SQLレベルでCOUNT
def count_orders_by_product(self, product_id: int) -> int:
    """特定商品を含む注文数を取得。

    Args:
        product_id: 商品ID。

    Returns:
        該当商品を含む注文数。
    """
    with self.session_factory() as session:
        stmt = (
            select(func.count(func.distinct(OrderItem.order_id)))
            .where(OrderItem.product_id == product_id)
        )
        return session.execute(stmt).scalar() or 0
```

## 3. バルク操作

### バルク INSERT

```python
# ❌ BAD: 1件ずつ追加（N回のINSERT）
for item_data in item_list:
    session.add(OrderItem(**item_data))
    session.commit()

# ✅ GOOD: バルクINSERT（1回のINSERT）
def bulk_add_order_items(self, items: list[dict[str, Any]]) -> int:
    """注文明細を一括挿入。

    Args:
        items: 明細データのリスト。各dictは OrderItem モデルのカラムに対応。

    Returns:
        挿入された件数。
    """
    with self.session_factory() as session:
        session.execute(OrderItem.__table__.insert(), items)
        session.commit()
        return len(items)
```

### バルク UPDATE

```python
# ❌ BAD: 1件ずつUPDATE
for product_id, avg in updates.items():
    product = session.get(Product, product_id)
    product.rating_avg = avg
    session.commit()

# ✅ GOOD: バルクUPDATE（WHERE IN句）
def bulk_update_ratings(
    self,
    rating_updates: list[dict[str, Any]],
) -> int:
    """平均評価を一括更新。

    Args:
        rating_updates: [{"id": 1, "rating_avg": 4.2}, ...] 形式のリスト。

    Returns:
        更新された件数。
    """
    with self.session_factory() as session:
        session.bulk_update_mappings(Product, rating_updates)
        session.commit()
        return len(rating_updates)
```

### バルク UPSERT（INSERT OR REPLACE）

```python
from sqlalchemy.dialects.sqlite import insert as sqlite_insert

def upsert_order_items(self, items: list[dict[str, Any]]) -> int:
    """注文明細のUPSERT（存在すれば更新、なければ挿入）。

    SQLite の ON CONFLICT を使用。

    Args:
        items: 明細データのリスト。

    Returns:
        処理された件数。
    """
    with self.session_factory() as session:
        stmt = sqlite_insert(OrderItem).values(items)
        stmt = stmt.on_conflict_do_update(
            index_elements=["order_id", "sku"],
            set_={
                "quantity": stmt.excluded.quantity,
                "unit_price": stmt.excluded.unit_price,
            },
        )
        session.execute(stmt)
        session.commit()
        return len(items)
```

## 4. サブクエリとCTE

### 相関サブクエリ

```python
# 最新レビューのみ取得（商品ごとに最新の1件）
def get_latest_reviews(self) -> list[Row]:
    """各商品の最新レビューを取得。

    Returns:
        (product_id, rating, reviewer_id) のリスト。
    """
    with self.session_factory() as session:
        # サブクエリ: 商品ごとの最大レビューID
        latest_review = (
            select(func.max(Review.id).label("max_id"))
            .where(Review.product_id == Product.id)
            .correlate(Product)
            .scalar_subquery()
        )
        stmt = (
            select(Review.product_id, Review.rating, Review.reviewer_id)
            .where(Review.id == latest_review)
        )
        return list(session.execute(stmt).all())
```

### CTE（Common Table Expression）

```python
from sqlalchemy import cte

def get_orders_with_item_count(self, min_items: int = 5) -> list[Row]:
    """明細数が閾値以上の注文を取得。

    Args:
        min_items: 最小明細数。

    Returns:
        (order_id, order_number, item_count) のリスト。
    """
    with self.session_factory() as session:
        # CTE: 注文ごとの明細数を集計
        item_counts = (
            select(
                OrderItem.order_id,
                func.count(OrderItem.id).label("item_count"),
            )
            .group_by(OrderItem.order_id)
            .cte("item_counts")
        )
        # メインクエリ: CTEとJOIN
        stmt = (
            select(Order.id, Order.order_number, item_counts.c.item_count)
            .join(item_counts, Order.id == item_counts.c.order_id)
            .where(item_counts.c.item_count >= min_items)
            .order_by(item_counts.c.item_count.desc())
        )
        return list(session.execute(stmt).all())
```

## 5. 動的フィルタ構築

### 条件の動的組み立て

```python
from dataclasses import dataclass, field

@dataclass
class OrderSearchCriteria:
    """注文検索条件（型安全）。"""

    skus: list[str] = field(default_factory=list)
    min_amount: float | None = None
    max_amount: float | None = None
    has_payment: bool | None = None
    limit: int = 100
    offset: int = 0

def search_orders(self, criteria: OrderSearchCriteria) -> list[Order]:
    """条件に基づく注文検索（動的フィルタ）。

    Args:
        criteria: 検索条件。

    Returns:
        条件に合致する注文リスト。
    """
    with self.session_factory() as session:
        stmt = select(Order).where(Order.is_active == True)
        conditions: list = []

        if criteria.skus:
            # 指定SKUをすべて含む注文のサブクエリ
            item_subq = (
                select(OrderItem.order_id)
                .where(OrderItem.sku.in_(criteria.skus))
                .group_by(OrderItem.order_id)
                .having(func.count(func.distinct(OrderItem.sku)) == len(criteria.skus))
            )
            conditions.append(Order.id.in_(item_subq))

        if criteria.min_amount is not None:
            payment_subq = select(Payment.order_id).where(
                Payment.amount >= criteria.min_amount
            )
            conditions.append(Order.id.in_(payment_subq))

        if criteria.max_amount is not None:
            payment_subq = select(Payment.order_id).where(
                Payment.amount <= criteria.max_amount
            )
            conditions.append(Order.id.in_(payment_subq))

        if criteria.has_payment is True:
            payment_subq = select(Payment.order_id)
            conditions.append(Order.id.in_(payment_subq))
        elif criteria.has_payment is False:
            payment_subq = select(Payment.order_id)
            conditions.append(~Order.id.in_(payment_subq))

        if conditions:
            stmt = stmt.where(and_(*conditions))

        stmt = stmt.limit(criteria.limit).offset(criteria.offset)
        return list(session.execute(stmt).scalars().all())
```

## 6. SQLite 固有の最適化

### インデックス設計

```python
from sqlalchemy import Index

# モデル定義でのインデックス定義
class Product(Base):
    __tablename__ = "products"
    __table_args__ = (
        # 複合インデックス: SKUで重複検索 + アクティブフィルタ
        Index("ix_product_sku_active", "sku", "is_active"),
        # カバリングインデックス: 商品名検索時にidも返せる
        Index("ix_product_name", "name"),
    )

class OrderItem(Base):
    __tablename__ = "order_items"
    __table_args__ = (
        # 複合インデックス: 注文ごとのSKU検索に最適
        Index("ix_order_item_order_sku", "order_id", "sku"),
        # SKU検索用
        Index("ix_order_item_sku", "sku"),
    )
```

### SQLite WAL モード

```python
from sqlalchemy import event

# エンジン初期化モジュールで設定（読み取り並行性向上）
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_conn, connection_record):
    cursor = dbapi_conn.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.execute("PRAGMA synchronous=NORMAL")
    cursor.execute("PRAGMA cache_size=-64000")  # 64MB
    cursor.close()
```

### EXPLAIN で実行計画を確認

```python
# デバッグ用: クエリの実行計画を表示
def explain_query(self, stmt: Select) -> list[str]:
    """クエリの実行計画を取得（デバッグ用）。

    Args:
        stmt: 解析対象のSELECT文。

    Returns:
        EXPLAIN出力の各行。
    """
    with self.session_factory() as session:
        # SQLite の EXPLAIN QUERY PLAN
        compiled = stmt.compile(
            dialect=session.bind.dialect,
            compile_kwargs={"literal_binds": True},
        )
        result = session.execute(
            text(f"EXPLAIN QUERY PLAN {compiled}")
        )
        return [str(row) for row in result.all()]
```

## 7. ページネーション

### Keyset ページネーション（推奨）

```python
# ❌ BAD: OFFSET ページネーション（大量データで遅い）
stmt = select(Order).offset(10000).limit(100)

# ✅ GOOD: Keyset ページネーション（一定速度）
def get_orders_page(
    self,
    last_id: int | None = None,
    page_size: int = 100,
) -> list[Order]:
    """Keysetベースのページネーション。

    Args:
        last_id: 前ページ最後のID。Noneなら先頭から。
        page_size: 1ページの件数。

    Returns:
        注文リスト（page_size件）。
    """
    with self.session_factory() as session:
        stmt = select(Order).order_by(Order.id)
        if last_id is not None:
            stmt = stmt.where(Order.id > last_id)
        stmt = stmt.limit(page_size)
        return list(session.execute(stmt).scalars().all())
```

## 8. アンチパターン集

| アンチパターン | 問題 | 正しいアプローチ |
|---|---|---|
| `session.query(X).all()` + Python フィルタ | 全件メモリロード | `WHERE` 句で DB 側フィルタ |
| `len(query.all())` | 全件取得してカウント | `func.count()` |
| ループ内 `session.get()` | N+1 クエリ | `selectinload` / `IN` 句 |
| `OFFSET` 大量ページング | 深いページほど遅い | Keyset ページネーション |
| `SELECT *` 常用 | 不要データ転送 | 必要カラム明示 |
| コミット多発 | トランザクションオーバーヘッド | バッチでまとめてコミット |
| 文字列連結 SQL | SQLインジェクション | ORM / パラメータバインド |

## Quick Reference

**Eager Loading:**
```python
selectinload(Order.items)      # 1:N → IN句（推奨）
joinedload(OrderItem.product)  # N:1 → JOIN
subqueryload(Order.items)      # 1:N → サブクエリ
```

**バルク操作:**
```python
session.execute(Table.insert(), data_list)   # バルクINSERT
session.bulk_update_mappings(Model, updates)  # バルクUPDATE
sqlite_insert().on_conflict_do_update(...)    # UPSERT
```

**集計:**
```python
func.count(), func.sum(), func.avg()  # 集計関数
func.distinct()                        # 重複排除
exists().where(...)                    # 存在チェック
```

**フィルタ構築:**
```python
and_(*conditions)   # AND結合
or_(*conditions)    # OR結合
Order.id.in_(subq)  # サブクエリIN
~Order.id.in_(subq) # NOT IN
```
