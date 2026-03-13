---
name: create-pr-text
description: GitHub issue から PR のタイトルと説明文を作成する。
allowed-tools: Bash, Read, Glob, Grep, Write, Task
---

GitHub issue から PR のタイトルと説明文を作成する。`$ARGUMENTS` に issue 番号（`123`、`#123`）または URL が渡される。`$ARGUMENTS` が空の場合はユーザーに issue 番号を質問する。

**実際の PR は絶対に作成しない。** `gh pr create` は実行禁止。テキストの生成のみ行う。

1. `tmp/config.json` の `pull_request_template_path` を確認する。なければプロジェクト内の PR テンプレート（`pull_request_template.md`, `.github/pull_request_template.md` 等）を探し、見つかったパスを `tmp/config.json` に保存する。テンプレートがあればそのフォーマットに従う
2. `tmp/issues/<issue番号>/plan.md` や `tmp/issues/<issue番号>/checklist.md` が既にある場合はその内容を活用する
3. `gh issue view` で issue を取得する
4. `git log main..HEAD --stat` でコミット単位の変更概要を確認し、必要に応じて `git show <hash>` で個別のコミット内容を把握する
5. 結果を Write ツールで `tmp/issues/<issue番号>/pr.md` に書き込む（フォーマットは [sample.md](./examples/sample.md) を参照）
