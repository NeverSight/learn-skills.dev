---
name: dev
description: GitHub issue から計画・実装・チェックリスト・PR テキストまで一気通貫で行う。
allowed-tools: Bash, Read, Glob, Grep, Write, Edit, Task, Skill
disable-model-invocation: true
---

GitHub issue ( $ARGUMENTS ) に対して、計画から PR テキスト作成まで一気通貫で実行する。`$ARGUMENTS` は issue 番号（`123`、`#123`）または URL。`$ARGUMENTS` が空の場合はユーザーに issue 番号を質問する。

以下の順に各スキルを Skill ツールで呼び出す。

1. `/plan $ARGUMENTS` — 実装計画を作成し、ユーザーに方針を選択してもらう
2. `/implement $ARGUMENTS` — 計画に基づいてコードを実装する
3. `/create-checklist $ARGUMENTS` — 動作確認チェックリストを作成する
4. `/create-pr-text $ARGUMENTS` — PR のタイトルと説明文を作成する

## 注意事項

- ユーザーに確認を取らず、全ステップを連続で実行する。途中で止まらないこと
- plan の方針選択のみユーザーに質問する。それ以外は中断せず最後まで進める
