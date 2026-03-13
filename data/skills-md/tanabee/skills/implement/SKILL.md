---
name: implement
description: GitHub issue と実装計画をもとにコードを実装する。
allowed-tools: Bash, Read, Glob, Grep, Write, Edit, Task
---

GitHub issue ( $ARGUMENTS ) の内容をもとに実装を行う。`$ARGUMENTS` に issue 番号（`123`、`#123`）または URL が渡される。`$ARGUMENTS` が空の場合はユーザーに issue 番号を質問する。

1. `tmp/issues/<issue番号>/plan.md` を確認する。なければユーザーに `plan` スキルの実行を提案する
2. `gh issue view` で issue を取得し、目的・要件を把握する
3. `plan.md` のタスクを上から順に実装する。各タスクの影響範囲に記載されたファイルを確認してから変更する
4. 各タスクの完了条件を満たしていることを確認し、タスク単位でコミットしてから次のタスクに進む
5. 全タスク完了後、既存のテストがあれば実行して通ることを確認する
6. 実装の解説を `tmp/issues/<issue番号>/report.md` に書き込む（フォーマットは [sample.md](./examples/sample.md) を参照）

## 注意事項

- 実装中に要件が不明確な場合はユーザーに確認を取る
- タスクの完了条件を満たせない場合は、その理由をユーザーに伝える
