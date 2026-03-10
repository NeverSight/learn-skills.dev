---
name: domain-model-first
description: >-
  ドメインモデル中心の開発手順ガイド。テストファーストでドメインモデルを設計・実装し、
  インメモリリポジトリ→ユースケース→インフラの順で開発を進める手法を解説。
  トリガー：「ドメインモデルから始めたい」「TDDでDDD」「インメモリリポジトリの作り方」
  「ユースケースのテスト方法」「DDD開発の進め方」等の開発プロセス関連リクエストで起動。
---

# ドメインモデル中心の開発手順

> このガイドは特定のプログラミング言語に依存せず、どの言語でも適用可能な原則を説明しています。コード例はTypeScriptで示していますが、概念は他の言語にも応用できます。

## テストファーストのドメインモデル設計・実装

### 目的

外部依存に左右されない純粋なドメインロジックを実装する。

### 具体的な手順

1. **ドメインモデルの振る舞いをテストとして定義**
    - モデルが持つべき機能と制約を明確にする
    - エッジケースも含めて考慮する
1. **テストを満たすドメインモデルの実装**
    - テストが示す仕様に従って実装
    - 値オブジェクト、エンティティ、集約の設計原則に従う
1. **リファクタリングによる設計の洗練**
    - コードの重複排除
    - 責務の明確化と分離
    - 命名の改善

### メリット

- 仕様の明確化と要件の理解促進
- 設計品質の向上（責務分離・凝集度向上）
- リファクタリングの安全性確保
- エッジケースの早期発見
- ドキュメントとしての価値

### テスト例

```typescript
// Taskのテスト例
describe("Task", () => {
  it("タスクが完了しているかどうかを確認できる", () => {
    const taskId = TaskId.of("task-1");
    const title = TaskTitle.of("テストタスク");

    const task = Task.of({
      id: taskId,
      title: title,
      completed: false,
      createdAt: new Date("2023-03-01T10:00:00")
    });

    expect(task.isCompleted()).toBe(false);

    const completedTask = task.markAsCompleted();
    expect(completedTask.isCompleted()).toBe(true);
  });

  it("期限日が未来の日付であることを検証できる", () => {
    const pastDate = new Date();
    pastDate.setDate(pastDate.getDate() - 1); // 昨日の日付

    const result = Task.validateDueDate(pastDate);

    expect(result.isFailure()).toBe(true);
    expect(result.error.message).toContain("期限は未来の日付である必要があります");
  });
});
```

## インメモリリポジトリの実装

### 目的

- データベースに依存せず、ドメインモデルとユースケースのテスト実行を可能にする

### 具体的な手順

1. **リポジトリインタフェースの定義**
    - ドメインモデルで必要な操作を定義
2. **インメモリ実装の作成**
    - メモリ上のコレクションを使用
    - 実際のデータベースの振る舞いをシミュレート

## ユースケース開発

### 目的

- アプリケーション層のロジックをドメインモデルとリポジトリを使って実装

### 具体的な手順

1. **ユースケースのテストを定義**
    - 実行条件と期待結果を明確に
    - 成功ケースと失敗ケースの両方をカバー
2. **テストを満たすユースケースを実装**
    - 適切なドメインモデルとリポジトリの利用
    - ビジネスルールの適用
3. **リファクタリング**
    - 責務の分離と明確化

### テスト例

```typescript
describe("CompleteTaskUseCase", () => {
  let taskRepository: TaskRepositoryInMemory;
  let completeTaskUseCase: CompleteTaskUseCase;

  beforeEach(() => {
    taskRepository = new TaskRepositoryInMemory();

    const task1 = Task.of({
      id: TaskId.of("task-1"),
      title: TaskTitle.of("未完了タスク"),
      completed: false,
      createdAt: new Date("2023-03-01T10:00:00"),
    });

    const task2 = Task.of({
      id: TaskId.of("task-2"),
      title: TaskTitle.of("既に完了しているタスク"),
      completed: true,
      createdAt: new Date("2023-03-01T13:00:00"),
    });

    taskRepository.save(task1);
    taskRepository.save(task2);

    completeTaskUseCase = new CompleteTaskUseCase(taskRepository);
  });

  it("タスクを完了できる", async () => {
    const result = await completeTaskUseCase.execute({
      taskId: "task-1",
    });

    expect(result.isSuccess()).toBe(true);

    const updatedTask = await taskRepository.findById(TaskId.of("task-1"));
    expect(updatedTask.isSuccess()).toBe(true);
    expect(updatedTask.value.isCompleted()).toBe(true);
  });

  it("存在しないタスクを処理できる", async () => {
    const result = await completeTaskUseCase.execute({
      taskId: "non-existent",
    });

    expect(result.isFailure()).toBe(true);
    expect(result.error.message).toContain("タスクが見つかりません");
  });
});
```

## インタフェースアダプタとインフラの実装

### 目的

- ドメインモデルとユースケースを実際のインフラと接続する

### 具体的な手順

1. **永続化リポジトリの実装**
    - 実際のデータベースへの接続
    - リポジトリインタフェースの実装

2. **コントローラの実装**
    - 入力の検証とユースケースへの橋渡し

3. **プレゼンテーション層の実装**
    - ユースケース結果の表示形式への変換

## 統合テストと結合テスト

### 目的

- システム全体の動作を検証する

### 具体的な手順

1. **統合テストの作成**
    - 実際のインフラを使用したテスト
    - エンドツーエンドの動作検証

2. **結合テストの実行**
    - コンポーネント間の連携を検証

## この開発手順に従わないリスク

ドメインモデルを中心とする設計・実装で、本ナレッジが示す順序（ドメインモデル→インメモリリポジトリ→ユースケース→インフラ）に従わない場合、以下のような重大なリスクが発生します：

1. **ドメインモデルの設計歪曲**
    - インフラや UI の制約によってドメインモデルの設計が不適切な影響を受ける
    - データベーススキーマから影響を受けたエンティティ設計になる
    - O/Rマッパフレームワークの制約に合わせてドメインモデルを妥協する

2. **技術的関心事の漏洩**
    - 永続化やトランザクション管理などの技術的関心事がドメインロジックに混入する
    - ドメインモデルがフレームワーク依存になり、純粋なビジネスロジックから逸脱する

3. **テスト困難性の増大**
    - 外部依存を多く含むモデルはテストが複雑になり、カバレッジが低下する
    - テスト実行速度の低下によりフィードバックサイクルが遅くなる

4. **変更容易性の低下**
    - 外部レイヤーとの依存関係が複雑になり、変更の影響範囲が広がる
    - ドメインモデルの変更がインフラの変更を強制する状況が発生する

5. **概念の一貫性喪失**
    - ドメインエキスパートの言語（ユビキタス言語）ではなく技術用語がモデルに混入する
    - ビジネスルールの表現が技術的制約によって不明瞭になる

## まとめ：この開発アプローチの利点

1. **ドメインモデルの設計が歪まない**
    - インフラ制約に引きずられない純粋なドメイン設計
    - ビジネスルールと技術的関心事の明確な分離

2. **バグの早期発見と修正が容易**
    - テストが仕様を明確にし、変更の影響を素早く検出
    - 単体レベルでのテストカバレッジが高まる

3. **要件変更に柔軟に対応**
    - 堅牢なテスト基盤があることで安全なリファクタリングが可能
    - ドメインロジックの変更がインフラに依存しない

4. **ドキュメントとしての価値**
    - テストがドメインルールや振る舞いを文書化
    - ユビキタス言語の一貫した使用が促進される

## 関連スキル（併読推奨）
このスキルを使用する際は、以下のスキルも併せて参照すること：
- `domain-building-blocks`: TDD対象となるビルディングブロック（値オブジェクト、エンティティ等）の設計
- `aggregate-design`: 集約の設計ルールと境界の決定
- `repository-design`: インメモリリポジトリを含むリポジトリの設計パターン
