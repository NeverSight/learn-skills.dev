---
name: refresh-skills
description: スキルを最新にする、作業対象リポジトリに残ったスキルのコピーを移行する、スキルの正本とシンボリックリンクとスキル表を突き合わせる。npx skills によるホームのスキルの確認と更新、philtzjp/skills のコピーの削除提案、ローカル改変の扱い、リポジトリ固有のスキルと philtzjp/skills 本体の整合性検査を定義する。作業を始めるとき、上流からスキルを取り込み直すとき、.agents/skills や .claude/skills に philtzjp/skills と同名のスキルを見つけたとき、スキルを追加・削除・リネームしたときに使う。
---

# refresh-skills

## 方針

philtzjp/skills のスキルは、各メンバーのホームに `npx skills` で導入します。作業対象リポジトリにはコピーしません。コピーした時点から古くなり、上流の更新が届かなくなるためです。

作業の入口は https://raw.githubusercontent.com/philtzjp/startingpoint/main/START.md です。導入するスキルの選び方は skill-selection に従ってください。

以前は各リポジトリの `.agents/skills/` にスキルをコピーし、上流と同期していました。この手順はもう使いません。

## ホームのスキルを最新にする

作業を始めるたびに、導入済みのスキルを確認します。

```sh
DISABLE_TELEMETRY=1 npx skills list -g
```

Source が philtzjp/skills のスキルを、名前を指定して更新します。

```sh
DISABLE_TELEMETRY=1 npx skills update <スキル名> <スキル名> -g -y
```

- 名前を指定し、ユーザーが他の Source から入れたスキルには触れない。
- 必要なスキルが入っていない、または Source が philtzjp/skills 以外なら、ユーザーの許可を得てから導入し直す。手順は skill-selection に書いてある。
- 導入や更新ができなければ、推測で進めずにユーザーに報告する。

## 作業対象リポジトリに残ったコピーを移行する

作業対象リポジトリの `.agents/skills/` と `.claude/skills/` を確認し、philtzjp/skills と同名のスキルがあれば、次の手順で移行を提案します。移行は github スキルの手順で PR にします。ユーザーの確認なしに削除しないでください。

上流にあるスキルの一覧は次で取得できます。

```sh
DISABLE_TELEMETRY=1 npx skills add philtzjp/skills --list
```

### 1. コピーを分類する

- **上流と同じ内容のコピー**：削除してよい。
- **上流で統合済みの旧スキル**：削除してよい。統合先は次のとおり。

  | 旧スキル | 統合先 |
  | --- | --- |
  | commit-and-git、issue-branch-pr-flow | github |
  | japanese-writing | japanese |
  | typescript-monorepo | turborepo |
  | api-design | hono |
  | data-migration | db |
  | e2e-testing | e2etest |
  | google-analytics | analytics |

- **上流と内容が違うコピー**：ローカルで改変されている可能性がある。削除する前に差分をユーザーに見せる。

  ```sh
  curl -fsSL https://raw.githubusercontent.com/philtzjp/skills/main/.agents/skills/<スキル名>/SKILL.md | diff - .agents/skills/<スキル名>/SKILL.md
  ```

  上流が古い版のまま改変されただけか、そのリポジトリ固有の事情による改変かをユーザーと判断する。他のリポジトリにも役立つ改変なら、skill-escalation に従って philtzjp/skills に提案する。そのリポジトリだけの事情なら、リポジトリ固有のスキルとして残すか、AGENTS.md に規約として書く。

- **philtzjp/skills にないスキル**：リポジトリ固有のスキル。残す。

### 2. 移行する

1. 削除するスキル、または統合先のスキルが、ホームに導入されているか確認する。入っていなければ、ユーザーの許可を得て導入する。
2. 削除するスキルの `.agents/skills/<スキル名>/` と `.claude/skills/<スキル名>` を削除する。
3. AGENTS.md や CLAUDE.md のスキル表から、削除したスキルの行を消す。リポジトリ固有のスキルが残らなければ、スキル表ごと消す。
4. AGENTS.md や CLAUDE.md の中で、削除したスキルを前提にした記述（「philtzjp/skills から取り込む」「refresh-skills で同期する」など）を消す。
5. AGENTS.md に、philtzjp/startingpoint の START.md を読む案内を入れる。

   ```markdown
   ## 開発ルール

   作業を始める前に、https://raw.githubusercontent.com/philtzjp/startingpoint/main/START.md を curl で取得して全文を読み、書かれている手順に従ってください。
   ```

6. philtzjp/startingpoint 由来の `scripts/refresh-skills.sh` や `.cursor/environment.json` のように、コピーの同期を前提にした仕組みがあれば、`npx skills` に置き換えるようユーザーに提案する。

   - `scripts/refresh-skills.sh`：上流との差分確認（`--upstream`）とコピーの同期をやめ、`npx skills update` でホームのスキルを更新する内容にする。リポジトリ固有のスキルが残るなら、シンボリックリンクとスキル表の突き合わせだけを残す。残らなければ、スクリプトごと削除する。
   - `.cursor/environment.json` の `start`：Cursor Cloud Agent は起動のたびにホームが空になるので、`./scripts/refresh-skills.sh` の代わりに、起動時にスキルを導入する。

     ```json
     {
       "start": "DISABLE_TELEMETRY=1 npx skills add philtzjp/skills -g -a cursor -s github -s japanese -s turborepo -y"
     }
     ```

   - 他にも、CI、lefthook、セットアップ用のスクリプトなどでスキルのコピーや同期をしている箇所があれば、同じく `npx skills` に置き換える。

## スキルの正本とシンボリックリンクを突き合わせる

リポジトリ固有のスキルがあるリポジトリと、philtzjp/skills 本体では、次の 4 つが一致している必要があります。

- `.agents/skills/<スキル名>/SKILL.md`（正本）
- `.claude/skills/<スキル名>`（`../../.agents/skills/<スキル名>` への相対シンボリックリンク）
- AGENTS.md のスキル表の行
- SKILL.md の frontmatter の `name`

確認すること。

- 正本は `.agents/skills/` に置く。`.claude/skills/` の下に実ファイルを置かない。
- シンボリックリンクは相対パスにする。絶対パスにしない。
- リンク切れがない。対応するリンクが欠けていない。
- スキル表とディレクトリの集合が一致している。
- スキル名は kebab-case。frontmatter の `name` がディレクトリ名と一致している。
- スキル本体に機密情報、トークン、認証情報を書いていない。

直し方。

- リンクが欠けている：`ln -s ../../.agents/skills/<スキル名> .claude/skills/<スキル名>`
- リンクが実ファイル、または別の場所を指している：削除して作り直す。
- リンク先がない：リンクを削除する。
- スキル表とディレクトリがずれている：表の行を足すか消す。
- `name` がディレクトリ名と違う：frontmatter を直す。

直したら、もう一度突き合わせて一致を確認してください。

## スキルを追加・削除・リネームする

リポジトリ固有のスキル、または philtzjp/skills 本体のスキルを変えるときの手順です。

- **追加**：`.agents/skills/<スキル名>/SKILL.md` を作り、frontmatter に `name` と `description`（どんな場面で使うかを具体的に書く）を入れる。シンボリックリンクを作り、スキル表に行を足す。
- **削除**：ディレクトリ、シンボリックリンク、スキル表の行を消す。他のスキルや AGENTS.md からの参照も探して直す。
- **リネーム**：ディレクトリ名と frontmatter の `name` を変え、シンボリックリンクを作り直し、スキル表と参照を直す。

どれも最後に突き合わせを行い、github スキルに従ってコミットしてください。

philtzjp/skills 本体では、スキルを削除したりリネームしたりしないでください。古い版のコピーを持つリポジトリや、ホームに導入済みの環境で、スキルが見つからなくなります。役目を終えたスキルは、統合先を案内する内容に置き換えて残します。
