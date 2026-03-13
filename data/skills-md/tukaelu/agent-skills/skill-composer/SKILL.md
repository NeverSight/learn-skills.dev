---
name: skill-composer
argument-hint: "[スキル名またはパス] [スキルの説明（新規作成時）]"
description: >
  スキルの新規作成・既存スキルのメンテナンスを日本語でサポートします。
  情報収集・スキル生成または更新・品質レビュー・自動修正を一貫して実行します。
  「スキルを作って」「〇〇するスキルを追加したい」「このスキルを修正したい」
  「スキルを改善したい」などの日本語リクエストや /skill-composer コマンドで起動します。
allowed-tools:
  - AskUserQuestion
  - Skill
  - Glob
  - Read
  - Write
  - Edit
  - TaskCreate
  - TaskUpdate
  - TaskList
model: sonnet
---

# Skill Composer

スキルの新規作成とメンテナンスをサポートするオーケストレーターです。
情報収集・`example-skills:skill-creator` によるスキル生成・ `skill-reviewer` によるレビューと自動修正を一貫して管理します。

---

## ワークフロー

### Step 1: スキル情報の取得

#### ベースディレクトリの特定

以下のヒューリスティックでスキルのベースディレクトリを決定する：

| 条件 | ベースディレクトリ | 種別 |
|---|---|---|
| `.claude/skills/` が存在する | `.claude/skills/` | リポジトリ内スキル |
| `skills/` が存在する | `skills/` | スキル開発リポジトリのスキル |
| どちらもない | ユーザーに確認 | 不明 |

#### 引数の解析と操作モードの決定

**`$ARGUMENTS` がある場合：**

- 最初の単語をスキル名として取得
- `<ベースディレクトリ>/<スキル名>/SKILL.md` が存在するか確認
  - 存在する → **メンテナンスモード**
  - 存在しない → **新規作成モード**
- 残りの引数はスキルの説明として使用する（新規作成時のみ）

**`$ARGUMENTS` が空の場合：**

AskUserQuestion で操作モードを選択させる：

```javascript
AskUserQuestion({
  questions: [
    {
      question: "スキルの操作を選択してください。",
      header: "操作モード",
      options: [
        { label: "新規作成", description: "新しいスキルをゼロから作成する" },
        { label: "メンテナンス", description: "既存のスキルを修正・改善する" }
      ],
      multiSelect: false
    }
  ]
})
```

**新規作成モードの場合（スキル名・説明が未取得のとき）：**

以下の内容をテキストでユーザーに質問する：

1. **スキル名**: 「作成するスキルの名前を教えてください（例: pdf-converter, code-review）。小文字・数字・ハイフンのみ、64文字以内。`anthropic`、`claude` は予約語のため使用不可。」
2. **スキルの説明**: 「スキルが何をするか・いつ使うかを説明してください（例: 〇〇ファイルを操作するとき、〇〇と言われたら起動、など）。」

**メンテナンスモードの場合（スキルが未指定のとき）：**

ベースディレクトリ内のスキルを最大4件取得して選択肢として提示する（5件以上ある場合は最終更新日時が新しいものを優先）。ユーザーは「Other」を選択してスキル名を直接入力することもできる。

```javascript
AskUserQuestion({
  questions: [
    {
      question: "メンテナンスするスキルを選択してください。",
      header: "対象スキル",
      options: [
        // ベースディレクトリ内のスキルを列挙（最大4件、件数が足りない場合は Other で補完）
        { label: "<skill-name-1>", description: "<description の先頭100文字>" },
        { label: "<skill-name-2>", description: "<description の先頭100文字>" },
        // 3件以上あれば追加
      ],
      multiSelect: false
    }
  ]
})
```

---

### Step 2: スキルの作成・更新

#### TaskCreate でタスク管理

操作モードに応じて1タスク目の内容を変える。作成後は各 taskId を記憶し、以降のステップで使用する：

```javascript
// 新規作成モード
const t1 = TaskCreate({ subject: "新しいスキルを作成する",        activeForm: "スキルを作成中" })
const t2 = TaskCreate({ subject: "スキルをレビューする",          activeForm: "スキルをレビュー中" })
const t3 = TaskCreate({ subject: "レビュー結果に基づいて修正する", activeForm: "スキルを修正中" })
// t1.taskId, t2.taskId, t3.taskId を記憶する
TaskUpdate({ taskId: t1.taskId, status: "in_progress" })

// メンテナンスモード
const t1 = TaskCreate({ subject: "既存スキルを更新する",          activeForm: "スキルを更新中" })
const t2 = TaskCreate({ subject: "スキルをレビューする",          activeForm: "スキルをレビュー中" })
const t3 = TaskCreate({ subject: "レビュー結果に基づいて修正する", activeForm: "スキルを修正中" })
// t1.taskId, t2.taskId, t3.taskId を記憶する
TaskUpdate({ taskId: t1.taskId, status: "in_progress" })
```

#### skill-creator の実行

Skill ツールで `example-skills:skill-creator` を呼び出す：

```javascript
// 新規作成モード
Skill({
  skill: "example-skills:skill-creator",
  args: "[スキル名] [スキルの説明]"
})

// メンテナンスモード（スキル名またはパスを渡す）
// スキル名のみの場合は <ベースディレクトリ>/<スキル名> に解決して渡す
Skill({
  skill: "example-skills:skill-creator",
  args: "[スキルのパス]"
})
```

**重要**: skill-creator が対話的に質問してくる場合は、Step 1 で取得した情報を元に回答する。

#### 完了の確認

スキルが正常に作成・更新されたことを確認する：
- SKILL.md ファイルが生成または更新されているか
- 必要なディレクトリ構造が作成されているか

**フォールバック**: `example-skills:skill-creator` が利用できない場合は、スキルのベストプラクティスに従って Claude が直接 SKILL.md を作成・更新する。

---

### Step 3: レビューと自動修正

#### TaskUpdate でタスク状態を更新

```javascript
TaskUpdate({ taskId: t1.taskId, status: "completed"   }) // 「新しいスキルを作成する」or「既存スキルを更新する」
TaskUpdate({ taskId: t2.taskId, status: "in_progress" }) // 「スキルをレビューする」
```

#### skill-reviewer の実行

スキルのパスを明示的に渡して呼び出す：

```javascript
Skill({
  skill: "skill-reviewer",
  args: "[スキルのパス]"
})
```

#### レビュー結果の処理

skill-reviewer の Step 5 に従って対話的に改善を進める。修正がすべて完了したら TaskUpdate で全タスクを `completed` にして完了サマリーを表示する。

**フォールバック**: `skill-reviewer` が利用できない場合は Step 3 をスキップして完了サマリーを表示する。

---

## 完了サマリー

操作モードに応じて以下の形式で表示する：

**新規作成モード:**
```
✓ スキルの作成が完了しました

スキル名: [スキル名]
説明: [スキルの説明]

作成されたファイル:
- [ファイルパスのリスト]

レビュー結果:
- Critical: 問題なし / N件を修正
- Warning: N件を修正 / N件を見送り
- Info: N件
```

**メンテナンスモード:**
```
✓ スキルの更新が完了しました

対象スキル: [スキルのパス]

更新されたファイル:
- [ファイルパスのリスト]

レビュー結果:
- Critical: 問題なし / N件を修正
- Warning: N件を修正 / N件を見送り
- Info: N件
```
