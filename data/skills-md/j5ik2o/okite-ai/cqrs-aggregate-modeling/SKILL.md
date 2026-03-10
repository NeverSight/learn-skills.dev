---
name: cqrs-aggregate-modeling
description: >
  CQRS/ESが集約の境界定義とモデリングに与える影響を解説する。CQRSを導入すると集約は
  コマンド実行に必要な最小限の状態のみ保持すればよくなり、読み取り責務はリードモデルに
  委譲できる。大きすぎる集約の軽量化、集約境界の再定義、イベントによる状態管理を支援する。
  集約設計、CQRS導入時のモデリング見直し、パフォーマンス問題の解決時に使用。
  対象言語: 言語非依存。
  トリガー：「CQRSで集約が変わる」「集約が大きすぎる」「集約にメッセージ1000件」
  「集約の更新が重い」「CQRS導入で集約を見直す」「集約を軽量化したい」
  「集約にクエリ用データが混ざっている」「集約の境界を再定義」
  といったCQRS/モデリング関連リクエストで起動。
---

# CQRSによる集約の境界再定義

CQRSを導入すると集約のモデリングが変わる。集約はコマンド実行に必要な最小限の状態のみ保持し、読み取り責務はリードモデルに委譲する。

## 問題: 肥大化した集約

### 典型例: Thread集約が1000件のメッセージを保持

```scala
// 従来型: 集約がすべてのデータを保持
case class Message(id: MessageId, text: MessageText, senderId: AccountId,
                   createdAt: Instant, updatedAt: Instant)
case class Messages(values: List[Message])

class Thread(id: ThreadId, members: Members, messages: Messages,
             createdAt: Instant)
```

### 更新時の問題

```
1. threadRepository.findById(threadId)
   → 1000件のメッセージを含むスレッド全体をDBから取得

2. thread.addMessage(...)
   → メッセージを1件追加

3. threadRepository.store(newThread)
   → 1001件全体をDBに更新
   → どのフィールドが更新されたか不明なため、全情報を更新する必要がある
```

**1件のメッセージ追加のために1001件を更新する。** これは集約が「コマンドに必要なデータ」と「クエリに必要なデータ」を区別せずに保持していることが原因。

### 差分更新の誘惑

差分更新を実装しようとすると、集約の内部実装が複雑化する。どのフィールドが変更されたかを追跡する仕組みが必要になり、ドメインロジックとインフラの関心が混在する。

## 解決: CQRSによる集約の再設計

### 核心原則

**CQRSを導入すると、集約はコマンド実行に必要な最小限の状態だけ持てばよい。**

読み取り責務（クエリ）を集約から完全に除去し、リードモデルに委譲する。その結果、集約はコマンドの検証に必要な情報のみ保持する。

### 問い: このコマンドの検証に何が必要か？

Thread集約の場合、「メッセージ追加」コマンドの検証に必要なのは：

- 送信者がスレッドのメンバーであること → **メンバーIDのリスト**が必要
- メッセージIDの重複がないこと → **メッセージIDのリスト**が必要

**メッセージの本文は不要。** 本文は表示（クエリ）のために必要であり、コマンドの検証には関係ない。

### 再設計後の集約

```scala
// CQRS/ES: 集約はコマンド検証に必要な最小限の状態のみ保持
class Thread(id: ThreadId, memberIds: MemberIds, messageIds: MessageIds,
             createdAt: Instant) {

  def addMessage(messageId: MessageId, messageText: MessageText,
                 senderId: AccountId): Either[ThreadError, Thread] =
    if (memberIds.contains(senderId)) {
      // イベントを追記するだけ。1001件の更新は発生しない
      persistEvent(MessageAdded(id, messageId, messageText, senderId, Instant.now))
      Right(copy(messageIds = messageIds.add(messageId)))  // IDのみ追加
    } else {
      Left(new AddMessageError)
    }
}
```

**メッセージ本文を持たないため、集約は大幅に軽量化される。**

### イベントの設計

```scala
sealed trait ThreadEvent

case class MemberAdded(threadId: ThreadId, accountId: AccountId,
                       occurredAt: Instant) extends ThreadEvent

case class MessageAdded(threadId: ThreadId, messageId: MessageId,
                       messageText: MessageText, senderId: AccountId,
                       occurredAt: Instant) extends ThreadEvent

case class MessageUpdated(threadId: ThreadId, messageId: MessageId,
                         messageText: MessageText, senderId: AccountId,
                         occurredAt: Instant) extends ThreadEvent
```

イベントにはメッセージ本文を含める（リードモデル構築に必要なため）。ただし、集約の状態復元時にはIDのみを反映する。

### リードモデル（Q側）

```scala
// イベントを消費してリードモデルを構築
consumeEventsByThreadIdFromDDBStreams.foreach {
  case ev: MemberAdded   => insertMember(ev)
  case ev: MessageAdded  => insertMessage(ev)
  case ev: MessageUpdated => updateMessage(ev)
}

// リードモデルはクエリに最適化されたDTO
case class MessageDto(id: Long, threadId: Long, text: String,
                     senderId: Long, createdAt: Instant, updatedAt: Instant)

// 部分取得が可能（ページネーション等）
val messages: Seq[MessageDto] =
  MessageDao.findAllByThreadIdWithOffsetLimit(threadId, 0, 100)
```

## Before / After 比較

| 観点 | 従来型（非CQRS） | CQRS/ES |
|------|------------------|---------|
| 集約の状態 | メッセージ全文を保持 | メッセージIDのみ保持 |
| メッセージ追加 | 全件更新 | イベント1件追記 |
| 読み取り | 集約から直接取得 | リードモデルから取得 |
| メモリ使用量 | メッセージ数に比例して増大 | ID数に比例（軽量） |
| ページネーション | 集約内で実装（複雑） | リードモデルのDAO（自然） |

## 集約の境界再定義の考え方

### 判断基準: コマンドの検証に必要か？

集約が保持すべきデータを決めるには、各コマンドの検証ロジックを分析する。

```
集約が現在保持しているデータ
    ↓
各フィールドについて:
    「このデータはコマンドの検証に使われるか？」
    ├─ YES → 集約に残す
    └─ NO → クエリ専用データ → リードモデルへ移動
```

### 具体例: Thread集約の分析

| データ | コマンド検証に必要か | 判断 |
|--------|---------------------|------|
| メンバーID一覧 | YES（送信者がメンバーか確認） | 集約に残す |
| メッセージID一覧 | YES（重複チェック） | 集約に残す |
| メッセージ本文 | NO（表示のみ） | リードモデルへ |
| 送信者名 | NO（表示のみ） | リードモデルへ |

### 強い整合性の再検討

CQRSを導入する際に問うべき：

> スレッドとメッセージの関係性に強い整合性は必要か？

- メッセージの追加・表示に「メッセージ本文の即時一貫性」は不要
- メンバーシップの確認にのみ強い一貫性が必要
- **振る舞いがイメージできれば集約の構造が明確になる**

## 大きすぎる集約の兆候と対処

### 兆候

| 兆候 | 原因 |
|------|------|
| 集約の読み込みが遅い | 不要なデータを大量に保持 |
| 更新時に全件SQLが発生 | 差分が追跡できない |
| 集約内にページネーションロジック | クエリ責務が混在 |
| DTOと集約の構造が酷似 | クエリ用データがそのまま集約に |

### 対処フロー

```
集約が大きすぎる
    ↓
1. 各フィールドを「コマンド検証用」と「クエリ用」に分類
    ↓
2. クエリ用データをリードモデルへ移動（CQRSの導入）
    ↓
3. 集約はIDリストや状態フラグなど最小限の状態のみ保持
    ↓
4. イベントで状態変更を記録し、リードモデルはイベントから構築
```

## 関連スキルとの関係

| スキル | 関係 |
|--------|------|
| `aggregate-design` | 集約の内部設計原則。本スキルはCQRSによる**境界の再定義** |
| `cqrs-to-event-sourcing` | なぜESが必要か。本スキルはES前提の**モデリング変革** |
| `cqrs-tradeoffs` | 一貫性・可用性のトレードオフ。本スキルは**モデリングへの影響** |

## レビューチェックリスト

### 集約の肥大化

- [ ] 集約がクエリ専用データ（表示名、計算結果等）を保持していないか
- [ ] 集約の読み込みにパフォーマンス問題がないか
- [ ] 更新時に不要な全件更新が発生していないか

### CQRS/ESによる再設計

- [ ] 各フィールドが「コマンド検証に必要か」で分類されているか
- [ ] クエリ専用データはリードモデルに委譲されているか
- [ ] 集約はIDリスト等の最小限の状態のみ保持しているか
- [ ] イベントにはリードモデル構築に必要な情報がすべて含まれているか

### 境界の妥当性

- [ ] 集約内のデータすべてに強い整合性が本当に必要か再検討したか
- [ ] 振る舞い（コマンド）に基づいて集約の境界を決めているか
- [ ] 結果整合性で十分なデータを集約から分離しているか

## 関連スキル（併読推奨）
このスキルを使用する際は、以下のスキルも併せて参照すること：
- `cqrs-to-event-sourcing`: イベントソーシングが集約モデリングを変える理由
- `aggregate-design`: CQRS適用前の基本的な集約設計ルール
- `cqrs-tradeoffs`: CQRS採用のトレードオフ分析
