---
name: plan
description: GitHub issue からコードベースを調査し実装計画を作成する。
allowed-tools: Bash, Read, Glob, Grep, Write, Task
---

GitHub issue ( $ARGUMENTS ) から実装計画を作成する。`$ARGUMENTS` は issue 番号（`123`、`#123`）または URL。

1. `tmp/issues/<issue番号>/plan.md` が既にある場合はその内容を確認し、更新が必要か判断する
2. `gh issue view` で issue を取得する
3. issue の目的・要件・受け入れ条件を分析する
4. コードベースを調査し、実装方法の候補を 3 つ程度洗い出す
5. 各候補の概要・メリット・デメリットを提示し、ユーザーに選択してもらう（自由入力でのフィードバックも受け付ける）
6. 選択された方法をもとに、各タスクの影響範囲（対象ファイル・関数）、具体的な変更内容、完了条件を特定する
7. 結果を Write ツールで `tmp/issues/<issue番号>/plan.md` に書き込む（フォーマットは [sample.md](./examples/sample.md) を参照）

## 注意事項

- issue の内容が曖昧で計画に落とし込めない部分がある場合は、ユーザーに確認を取る
- コードベースが大きい場合、調査は issue に関連する部分に絞る
