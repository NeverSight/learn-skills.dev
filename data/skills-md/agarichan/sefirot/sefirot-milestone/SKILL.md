---
name: sefirot-milestone
description: Milestoneを設計する (sefirot)
---

あなたはプロジェクトの Milestone 設計者です。

## やること

ユーザーから与えられたドキュメントを読み、プロジェクトの Milestone 一覧を設計する。
各 Milestone のゴール（何が動く状態になるか）を定義する。
Task の細分化は Milestone 着手時に計画セッションが行うため、ここでは Milestone レベルの設計のみ行う。

### 前提: 設計ドキュメント

引数: $ARGUMENTS

引数でドキュメントのパスが指定されていればそれを使う。

引数がない場合は `sefirot list --no-milestones` を実行して、milestones.json が未作成のタスクディレクトリを探す:

- **1つだけ見つかった場合**: そのディレクトリ内の設計ドキュメント（.md ファイル）を使う。
- **複数見つかった場合**: 一覧を提示して AskUserQuestion でユーザーに選択してもらう。
- **見つからない場合**: 以下を案内して終了する:
  > milestones.json が未作成のタスクがありません。`/sefirot-plan` で設計ドキュメントを作成してください。

指定されたドキュメントが `docs/tasks/` 配下にない場合は、タスクディレクトリを作成してコピーする:

1. ドキュメントの内容からタスク名を判断する
2. `docs/tasks/{YYYYMMDD}_{HHMM}_{タスク名}/` ディレクトリを作成する
3. ドキュメントを `design.md` としてコピーする
4. 以降はコピー先の `design.md` を対象として扱う

### 手順

1. 対象の設計ドキュメントを読む
2. `CLAUDE.md` を読む
3. `docs/` 配下のドキュメントがあれば読む（アーキテクチャ、設計規約等）
4. 既存コードがあれば Glob/Grep で現状を把握する
5. Milestone を設計する
6. 設計ドキュメントと同じディレクトリに `milestones.json` を出力する（例: `docs/tasks/20260310_1430_ユーザー認証設計/milestones.json`）。既存ファイルがあれば上書きする
7. milestones.json をコミットする

## 出力フォーマット

唯一の成果物は `milestones.json`。設計ドキュメントと同じディレクトリに配置する。

```json
{
  "source": "design.md",
  "milestones": [
    {
      "milestone": 1,
      "goal": "何が動く状態になるか（1文、具体的に）",
      "verification": "プロジェクトの検証コマンド",
      "done": false,
      "tasks": []
    },
    {
      "milestone": 2,
      "goal": "...",
      "verification": "プロジェクトの検証コマンド",
      "done": false,
      "tasks": []
    }
  ]
}
```

| フィールド | 型 | 説明 |
|-----------|------|------|
| source | string | 元の設計ドキュメントのファイル名（同ディレクトリ内） |
| milestones[].milestone | number | Milestone 番号（1 始まり、昇順） |
| milestones[].goal | string | この Milestone が完了したとき何が動く状態か（1文、具体的に） |
| milestones[].verification | string | Milestone 完了時の通過条件コマンド（CLAUDE.md で定義されたプロジェクトの検証コマンドを使う） |
| milestones[].done | boolean | 常に false（ループが更新する） |
| milestones[].tasks | array | 常に空配列（Milestone 着手時に計画セッションが生成する） |

## Milestone の設計方針

### 機能スライスで Milestone を分ける

**各 Milestone は「1つの機能が UI からバックエンドまで縦に通って動く」単位で切る。**
レイヤーごとの横割り（domain 全部 -> infrastructure 全部 -> UI 全部）にしない。

Milestone 間は逐次実行。Milestone 内の Task は並列実行される。
Milestone の境界は「次の Milestone が前の Milestone の成果物を import する」ところ。

### 構成パターン

1. **基盤 Milestone**: プロジェクト構成、ツールチェーン、認証など横断的な基盤。品質チェックツールのセットアップも含め、verification コマンドが通る状態にすること。DB を使うプロジェクトでは、ローカル DB のセットアップもこの Milestone に含め、以降の Milestone で DB が使える状態にする。**環境変数の初期化もこの Milestone に含める**
2. **最初の機能 Milestone**: 最もシンプルな機能を1つ選び、全レイヤーを縦に通す。ここで全レイヤーの実装パターンが確立される
3. **追加機能 Milestone**: 確立したパターンに乗せて、1 Milestone = 1機能ずつ追加していく

### 大方針: 実際に動かすことを最優先する

**各 Milestone のゴールは「実際に動作確認できる状態」でなければならない。**

コードが存在するだけでは不十分。実際にその機能を手で触って確認できること。

- DB 永続化なら -> ローカル DB で実際にデータが保存・表示される
- 外部 API 連携なら -> 実 API キーを使って本物の API で動作する状態をゴールとする
- 認証機能なら -> 開発環境で認証フローが動作する

「コードは書いたが動かしたことがない」状態で Milestone を完了にしてはならない。

### goal の書き方

- 悪い例: "DDD レイヤー構造で構成され、Gateway interface が定義される"（横割りで何も動かない）
- 悪い例: "OAuth のコードが実装され、開発環境ではダミーユーザーでバイパスできる"（コードはあるが動かしていない）
- 良い例: "/rules ページで表現ルール（NG表現→推奨表現）の一覧表示・新規登録・編集・削除ができ、DB に永続化される"（1機能が動く）
- 良い例: "Claude API による5観点チェックが実行され、実際の AI レスポンスによる結果一覧が表示される"（実 API 動作を明示）

goal は具体的に「何が動くか」「何ができるか」を書く。計画セッションがこの goal を見て Task を分解する。

### verification

- CLAUDE.md に記載されたプロジェクトの検証コマンドを使う
- 外部 API を叩かない（ループが毎回機械的に実行するため）

### Milestone の粒度

- 1 Milestone = 1つの独立した機能が動く状態になる粒度を目安にする
- 複数の機能を1 Milestone にまとめすぎない
- Milestone 番号は 1 から連番
- tasks は全て空配列（計画セッションが Milestone 着手時に W1-W5 の Task を生成する）

### 依存関係のない機能は同一 Milestone にまとめる

**互いに依存関係がなく、並列に実装可能な機能は、同一 Milestone にまとめること。**

Milestone 間は逐次実行されるため、独立した機能を別 Milestone に分割すると直列実行になり、並列化の恩恵がゼロになる。Milestone 内の Task は並列実行されるため、独立した機能は同一 Milestone に入れて Planner に並列タスクとして設計させるのが効率的。

- 悪い例: fibonacci と fizzbuzz を Milestone 1 と Milestone 2 に分割（依存関係がないのに逐次実行）
- 良い例: fibonacci と fizzbuzz を同一 Milestone に入れ、Planner が並列タスクとして設計する

**ただし、以下の場合は別 Milestone にすべき:**
- 一方が他方の成果物を import する（依存関係がある）
- 一方の完了を確認してから次に着手したい（リスク管理上の理由がある）

### 不確定要素が高い機能を先に

**仕様が曖昧、未決事項がある、技術的に不透明、要件の解釈に幅がある等、実装時に想定外の問題が起きやすい機能は、できるだけ前の Milestone に配置する。**

不確定要素を後回しにすると、ループ終盤で問題が発覚し手戻りが大きくなる。先に着手させることで、問題の早期発見・早期解決ができ、後続の Milestone に影響を与えにくい。
