---
name: skill-escalation
description: スキルの改良を正本リポジトリに提案する。スキルどおりに進まない、Web 検索などでスキルと違う情報や新しい情報が得られた、スキルの条件を厳守すると最良の結果が得られない、と判断したときの進め方を定義する。ホームに導入したスキルを直接編集しないこと、提案先の振り分け、Issue のタイトルと本文テンプレートを含む。スキルの内容に疑問を持ったとき、スキルの改良を提案するときに使う。
---

# skill-escalation

## 使う場面

- スキルに従って作業したが、期待どおりに進まなかった。
- Web 検索などで、スキルと違う情報や、より新しい情報が得られた。
- スキルの条件を厳守すると、技術選定や実装の自由度が狭まり、最良の結果が得られないと判断した。

## 目の前の作業の進め方

スキルと違うやり方をとるなら、理由をユーザーに説明し、合意を得てから進めてください。黙ってスキルを無視しないでください。

ホームに導入したスキル（`~/.agents/skills/<スキル名>/SKILL.md`）は直接編集しないでください。

- `npx skills update` で上書きされ、改変が消える。
- そのメンバーの他のリポジトリの作業にも、改変が効いてしまう。
- 他のメンバーには届かない。

改良は、正本のリポジトリに提案して反映します。

## 提案するかどうか

- 他のメンバーや他の作業にも役立つなら提案する。
- その場限りの回避策や、特定の作業だけの例外なら提案しない。そのリポジトリ固有の事情なら、リポジトリの AGENTS.md に書くことをユーザーに提案する。
- 同じ内容の Issue や PR が既にあれば、新しく起票せず、そこにコメントする。

## 提案先

| 変えたいもの | 提案先 |
| --- | --- |
| スキルの内容 | philtzjp/skills |
| スキルの導入手順、エージェントが作業前に読む手順（START.md） | philtzjp/startingpoint |

変更内容がはっきりしていてユーザーの許可があれば、Issue に加えて PR を作ってもかまいません。PR は github スキルの手順で作ります。

統合済みの旧スキル（commit-and-git、issue-branch-pr-flow など）に向けた提案はしないでください。統合先のスキルに向けて提案します。

## Issue の起票

```sh
gh issue create --repo philtzjp/skills --title "<タイトル>" --body-file <ファイル>
```

タイトルは `type(scope): 短い日本語` の形式にします。

- type は feat、fix、perf、refactor のいずれか。
- scope は変更対象のスキル名。例：github、refresh-skills、hono。
- 説明は動作で終える。〜する、〜修正、〜追加、〜削除、〜実装、〜廃止など。体言止めにしない。
- emoji を含めない。1 行で完結させる。

本文の先頭には、philtzjp/skills の AGENTS.md の署名規約に従って `✳︎ <会社名> <モデル名> <バージョン>` の署名行を入れ、1 行空けて本文を続けます。本文には「背景」「作業範囲」「完了条件」「備考」の節を設けます。

## タイトル例

- `feat(github): scope のドット込みディレクトリ表記ルールを明文化する`
- `fix(refresh-skills): symlink 検査スクリプトの誤検知を修正する`
- `refactor(github): マージ前チェック手順を再編する`
- `perf(hono): OpenAPI 検証コマンドの実行時間を短縮する`

## 本文テンプレート

`gh issue create --body-file <file>` に渡すファイル（または `--body` の文字列）の中身は以下を使用する。`<...>` を具体内容に置き換える。

```markdown
✳︎ <会社名> <モデル名> <バージョン>

## 背景

なぜこの作業が必要か、動機・関連 Issue/PR を 1〜3 文で書く。

## 作業範囲

- やること 1
- やること 2

## 完了条件

- [ ] 受け入れ条件 1
- [ ] 受け入れ条件 2

## 備考

補足・参考リンク・注意点（任意）。
```

## GitHub Issue Template ファイル（参考）

GitHub Web UI 経由で人間が起票する場合は、リポジトリルートに `.github/ISSUE_TEMPLATE/skill-escalation.md` を配置する。frontmatter 付き全文は以下:

```markdown
---
name: skill-escalation
about: より良いスキルにするための変更提案をスキルの正本リポジトリに対して起票する
title: "type(scope): 短い日本語"
labels: ""
assignees: ""
---

<!--
タイトル形式: type(scope): 短い日本語

  type は次のいずれか:
    feat / fix / perf / refactor

  scope は変更範囲（スキル名）:

  短い日本語の説明:
    - 体言止めは使用しない（〜する / 〜修正 / 〜追加 / 〜削除 / 〜実装 / 〜廃止 等、動作の意味を持たせる）
    - emoji は使用不可
    - 1 行で完結させる
    - 例: chore(ci): Github Workflow の不整合を修正
    - 例: feat(numsec): plugin と gui を monorepo に移行
    - 例: refactor(xtask): Standalone Target を物理削除
-->

✳︎ ${会社名} ${モデル名} ${バージョン名}

## 背景

なぜこの作業が必要か、動機・関連 Issue/PR を 1〜3 文で書く。

## 作業範囲

- やること 1
- やること 2

## 完了条件

- [ ] 受け入れ条件 1
- [ ] 受け入れ条件 2

## 備考

補足・参考リンク・注意点（任意）。
```

## 改変記録の例（cursor-hook-authoring / commit-and-git）

スキルを各リポジトリにコピーしていたころの記録です。今はホームのスキルを直接編集せず、正本に提案します。

Cursor Cloud Agent が lefthook より後に `commit-msg.cursor.co-author` を実行し `Co-authored-by:` を付与する事象に対し、asna リポジトリで strip 連鎖 Hook を実装した。ローカル改変内容:

- `commit-and-git`: `--no-verify` 回避策を削除し、strip 連鎖への委譲と `GIT_GUARD_ALLOW_FORCE_PUSH` を明記
- `cursor-hook-authoring`（新規）: 実行順、`commit-msg.cursor.co-author-strip` 命名、install スクリプト、lefthook 多層防御、テスト手順

有用と判断した場合は本リポジトリ（`philtzjp/skills`）へ Issue を起票する（本件: Issue #27）。

## 関連スキル

- `github`: コミットメッセージ・PR 操作の規約と、パッチ以外の実装作業の Issue / PR フロー
- `cursor-hook-authoring`: Cursor Cloud の commit-msg hook 連鎖と Co-authored-by 除去
- `AGENTS.md` / `CLAUDE.md` のベース署名規約: Issue / PR 本文・コメントの署名形式
- `refresh-skills`: スキルの更新と、リポジトリに残ったコピーの移行
- `skill-selection`: 導入するスキルの選び方
