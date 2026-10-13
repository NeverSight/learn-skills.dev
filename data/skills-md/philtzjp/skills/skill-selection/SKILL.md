---
name: skill-selection
description: どのスキルを導入するか決める。全員が入れる既定のスキル、作業に応じて追加するスキル、npx skills によるホームへの導入と削除、統合済みの旧スキルを入れない判断、リポジトリ固有のスキルを置くかどうかの判断を定義する。スキルを初めて導入するとき、philtzjp/skills に新しいスキルが追加されたとき、作業に必要なスキルが入っていないとき、不要になったスキルを外すときに使う。
---

# skill-selection

## 方針

philtzjp/skills のスキルは、各メンバーのホームに `npx skills` で導入します。作業対象リポジトリにはコピーしません。

ホームに入れたスキルは、そのメンバーのすべてのリポジトリの作業に効きます。導入も削除も、ユーザーの許可を得てから行ってください。

## 既定のスキル

全員が入れるスキルは次の 3 つです。

- github
- japanese
- turborepo

```sh
DISABLE_TELEMETRY=1 npx skills add philtzjp/skills -g -a claude-code -a codex -a cursor -s github -s japanese -s turborepo -y
```

実体は `~/.agents/skills/<スキル名>/` に置かれ、`~/.claude/skills/<スキル名>` からシンボリックリンクが張られます。Codex と Cursor は前者を、Claude Code は後者を読みます。

## 作業に応じて追加するスキル

実際にその作業をするときに追加します。「いつか使うかもしれない」段階では入れないでください。読み込まれるスキルが増えるほど、関係のない規約が作業に混ざります。

| スキル | 追加する場面 |
| --- | --- |
| hono | HTTP API を設計・実装する |
| db | データベースの選定、スキーマ、接続、マイグレーション、データ移行を扱う |
| e2etest | E2E テストを作成・実行する |
| analytics | アクセス解析や同意管理を実装する |
| errorpage | エラー応答やエラーページを設計する |
| cursor-hook-authoring | Cursor Cloud Agent の Git hook 連鎖を扱う |
| knowledge-elicitation | 対話でユーザーの暗黙知を引き出す |
| m4l-project | Max for Live デバイスを扱う |

一覧は増えることがあります。最新の一覧は次で確認してください。

```sh
DISABLE_TELEMETRY=1 npx skills add philtzjp/skills --list
```

追加するときは、スキル名だけを指定します。

```sh
DISABLE_TELEMETRY=1 npx skills add philtzjp/skills -g -a claude-code -a codex -a cursor -s <スキル名> -y
```

refresh-skills、skill-selection、skill-escalation は導入しません。スキルの追加、削除、更新、移行は `npx skills` を直接使って行います。手順は https://raw.githubusercontent.com/philtzjp/startingpoint/main/START.md にあります。

## 入れないスキル

次は統合済みの旧スキルで、中身は統合先への案内だけです。導入しないでください。

| 旧スキル | 代わりに入れるスキル |
| --- | --- |
| commit-and-git、issue-branch-pr-flow | github |
| japanese-writing | japanese |
| typescript-monorepo | turborepo |
| api-design | hono |
| data-migration | db |
| e2e-testing | e2etest |
| google-analytics | analytics |

## 外す

使わなくなったスキルは、ユーザーの許可を得てから外します。

```sh
DISABLE_TELEMETRY=1 npx skills remove -g -y <スキル名>
```

既定の 3 つは外さないでください。

## リポジトリ固有のスキルを置くか

そのリポジトリでしか意味を持たない規約は、ホームではなくリポジトリに置いてかまいません。

- まず、AGENTS.md に数行書けば足りないかを考える。足りるなら AGENTS.md に書く。
- スキルにするなら、`.agents/skills/<スキル名>/SKILL.md` に正本を置き、`.claude/skills/<スキル名>` から相対シンボリックリンクを張り、AGENTS.md のスキル表に行を足す。突き合わせの手順は refresh-skills に書いてある。
- philtzjp/skills と同じ名前にしない。
- 他のリポジトリでも役立つと分かったら、skill-escalation に従って philtzjp/skills への追加を提案する。

AGENTS.md には、導入していないスキルを前提にした規約を書かないでください。
