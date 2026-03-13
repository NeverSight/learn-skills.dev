---
name: sefirot-loop
description: sefirotループを実行し、質問があればユーザーに確認する
---

## sefirot とは

Sefirot は Claude Code 上のマルチエージェントオーケストレーションフレームワーク。3つのエージェント（Planner / Builder / Verifier）が Milestone 単位で設計→実装→検証のループを自動で回す。

- **Planner**: 設計ドキュメントからタスクを分割し、Wave（並列実行単位）を割り当てる
- **Builder**: 各タスクを独立した git worktree 内で並列実装する（最大8並列）
- **Verifier**: Builder のブランチをマージし、テスト・リント・型チェックで検証する。失敗時は fix task を生成して再ループ

すべての状態は `milestones.json`（タスクディレクトリ内）と設計ドキュメント（Markdown）で管理される。エージェント間の直接通信はなく、これらのファイルを介して連携する。

エージェントが判断に迷った場合は `milestones.json` の `questions` 配列に質問を書き込み、ループが一時停止する。このスキルがその質問をユーザーに仲介し、回答を設計ドキュメントに反映してループを再開する。

## 前提チェック

まず `sefirot` CLI がインストールされているか確認してください:

```bash
command -v sefirot
```

インストールされていない場合は、以下のメッセージを返して終了してください:

> `sefirot` CLI がインストールされていません。以下のコマンドでインストールしてください:
>
> ```bash
> uv tool install git+https://github.com/agarichan/sefirot.git
> ```

## 概要

sefirot のビルドループをバックグラウンドで実行し、エージェントからの質問があればユーザーに確認して回答を反映した上で再実行する。

## 手順

### ステップ0: 対象タスクの確認

`sefirot list --active` を実行して未完了タスクの一覧を確認する:

- **見つからない場合**: 以下を案内して終了する:
  > 未完了のタスクがありません。`/plan` で設計ドキュメントを作成し、`/milestone` で milestones.json を生成してください。
- **1つだけ見つかった場合**: そのまま使う。
- **複数見つかった場合**: `sefirot list --active` の結果を提示して AskUserQuestion でユーザーにどのタスクを実行するか確認する。

### ステップ1: バックグラウンドでループ実行

Bash ツールの `run_in_background: true` を使ってバックグラウンドで起動する:

```bash
sefirot loop --from-skill --task-dir <ステップ0で特定したタスクディレクトリ>
```

起動後、ユーザーに以下を伝える:

> sefirot loop をバックグラウンドで開始しました。
> 完了時に通知します。実行中も自由に質問できます。

### ステップ2: ユーザーとの対話（ループ実行中）

バックグラウンドタスクの完了通知が届くまで、ユーザーの入力を待つ。
ユーザーから質問や依頼があった場合は通常通り応答する。

典型的なリクエスト:
- **「進捗は？」「状況教えて」** → TaskOutput でバックグラウンドプロセスの出力を読み、進捗を報告する。各エージェントの詳細ログは `.sefirot/sessions/<タスク名>/` 配下にあるので、必要に応じてそちらも確認する
- **その他の質問** → 通常通り応答する

### ステップ3: 完了時の処理

バックグラウンドタスクが完了したら、TaskOutput で出力を取得する。
出力の末尾に `[SEFIROT:ACTION]` 行が含まれているので、そのアクション指示に従う:

- **`[SEFIROT:ACTION] COMPLETE`**: 正常完了。ステップ5 に進む。
- **`[SEFIROT:ACTION] QUESTIONS_PENDING`**: 質問が保留中。ステップ4 に進む。
- **`[SEFIROT:ACTION] ERROR`**: エラー。`[SEFIROT:MESSAGE]` 行のメッセージをユーザーに報告し、終了する。
- **`[SEFIROT:ACTION]` が見つからない場合**: 予期しないクラッシュ。出力の末尾をユーザーに報告し、終了する。

### ステップ4: 質問の処理

エージェントからの質問が `milestones.json` の `$.questions` 配列に格納されている。
milestones.json は `docs/tasks/<タスクディレクトリ>/milestones.json` に配置されている。

1. milestones.json を読み、`questions` 配列を取得する
2. 各質問について:
   - 質問内容をユーザーに提示する。フォーマット:

     ```
     [質問 N/{total}] from {agent} (task: {task_id})
     {question}
     ```

   - AskUserQuestion ツールを使ってユーザーの回答を得る
   - 回答を関連する設計ドキュメントに反映する:
     a. `milestones.json` から該当タスクの所属する Milestone を特定する
     b. その Milestone の `plan_doc` フィールドから設計ドキュメントのパスを取得する。`plan_doc` がない場合（Planner からの質問等）は、`milestones.json` の `source` フィールド（design.md）を使う
     c. 設計ドキュメント内の該当タスクのセクション（または末尾）に「追加指示」として回答を追記する:
        ```markdown
        #### 追加指示（ユーザー回答）
        - Q: {元の質問}
        - A: {ユーザーの回答}
        ```
3. 全ての質問を処理したら、`milestones.json` の `questions` 配列を空にする（`"questions": []`）
4. 変更をコミットする:
   ```bash
   git add -A && git commit -m "chore: resolve agent questions"
   ```
5. ステップ1 に戻り、再度バックグラウンドでループを実行する

### ステップ5: 完了報告

ループが正常完了したら、結果を報告する:

1. `milestones.json` を読み、現在の状態を把握する
2. 以下の情報を報告する:
   - 完了した Milestone とそのゴール
   - 完了したタスクの一覧
   - 次の未完了 Milestone があればその情報
   - 検証結果のサマリー

## 注意事項

- **ループは必ずバックグラウンドで実行する。** フォアグラウンドで実行しない
- ループ実行中もユーザーの入力を受け付け、進捗確認などに応答する
- 質問が発生した場合のみユーザーの判断を求める
- 質問への回答は設計ドキュメントに永続化されるため、再実行時にエージェントが参照できる
- 1回のループで複数の質問が発生する場合がある。全て処理してから再実行すること
