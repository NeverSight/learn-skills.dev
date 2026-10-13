---
name: github
description: Issue 起票からブランチ、実装、PR、マージまでの標準フローと、Git / GitHub 操作の規約。コミットメッセージの type(scope) 形式、scope の決め方、--author の扱い、author と committer のアドレスの確認、Co-Authored-By と git add . の禁止、merge ラベルによる philtz-organizer-bot の squash マージ、ahead/behind の確認、Issue コメントと Release の書き方。コミット、プッシュ、ブランチ作成や切り替え、マージ、リベース、Issue や PR やコメントや Release の作成を行うときに使う。
---

# github

## 最新の規約を優先する

エージェントのメモリや過去の会話に古い手順が残っていると、同じ誤りを何度も繰り返す。

- スキルは作業を始めるたびに入れ直す。前回読んだ内容やメモリで済ませない。
- メモリや過去の会話の手順がスキルと食い違ったら、スキルに従う。食い違っていたメモリは、どこがどう違うかをユーザーに伝え、更新か削除を提案する。許可なしにメモリを書き換えない。
- スキルの内容をメモリに保存しない。
- 会話が長くなってコンテキストが要約されたら、Git の操作を続ける前にスキルを読み直す。

## フロー

パッチバグフィクス以外の実装作業は、この順で進める。

1. Issue を起票する。
2. Issue 番号を含む専用ブランチを作る。
3. 実装する。
4. PR を作る。
5. ahead / behind とマージ可否を確認する。
6. `merge` ラベルを付け、philtz-organizer-bot に squash でマージさせる。

判断に迷う作業はパッチバグフィクスではなく通常フローとして扱う。通常フロー対象の実装を、Issue なし、専用ブランチなし、PR なしで進めない。デフォルトブランチ上で始めない。

会社、チーム、担当領域をまたぐ変更では、影響範囲、検証内容、残リスクを Issue と PR に明記する。

## フローを省略できる場合

次をすべて満たすときだけ、パッチバグフィクスとして Issue の起票を省略できる。ブランチと PR は省略できない。デフォルトブランチには直接 push できないため。

- 既存挙動の明確な不具合を直す最小差分である。
- 仕様追加、設計変更、データモデル変更、API 契約変更、依存関係変更、権限・課金・認証の変更を含まない。
- 変更範囲が局所的で、他チームの作業や統合予定リポジトリに影響しない。
- Issue 化して合意形成する価値より、即時修正する価値が明らかに高い。
- ユーザーがパッチ対応を明示している、または同等の Issue や PR の文脈が既にある。

## 開始前

```sh
git status --short --branch
git fetch --prune
```

- git hook を有効にする。リポジトリに `.vite-hooks/` があれば `git config core.hooksPath .vite-hooks` を、`lefthook.yaml` しかなければ `lefthook install` を実行する。どちらも clone ごとの設定なので、新しい作業環境では毎回実行する。
- デフォルトブランチ、現在ブランチ、リモート追跡ブランチの状態を確認する。
- 未コミット変更があれば、内容と所有者を確認する。今回の作業に無関係な変更をステージ、コミット、修正しない。
- 現在ブランチがデフォルトブランチでなければ、今回の作業用か確認する。
- gh など Issue や PR の操作に必要なツールや権限がなければ、不足を報告し、ローカル実装だけ先行してよいか確認する。

## Issue

- 既存 Issue があるか先に確認する。なければ実装前に作る。
- タイトルと本文は、philtzjp/.github の `conventions.yml` に従う。リポジトリに `.github/conventions.yml` があれば、そちらに従う。本文は署名の行から始め、見出しを背景、作業範囲、受け入れ条件の順に書く。必要なら最後に備考を足す。
- 背景は最初の行から箇条書きにする。影響範囲や検証方針は、作業範囲か備考に書く。
- philtz-organizer-bot が Issue の書式を検査し、違反があれば内容をコメントにまとめるので、直す。
- 受け入れ条件は task list（`- [ ]`）で書き、達成状況を追跡できるようにする。
- 複数会社や複数領域に影響するなら、担当境界とレビュー観点を書く。
- 実装単位が大きすぎない粒度に分割する。
- Issue が曖昧なまま大きな変更に着手しない。

## ブランチ

- Issue 番号を含む専用ブランチを作る。
- 名前は `<type>/<issue-number>-<short-kebab-summary>`。
- type は feat、fix、refactor、docs、test、chore、ci、build のいずれか。
- 作成前にベースブランチが最新であることを確認する。
- 複数 Issue の実装を1ブランチに混ぜない。
- ユーザーの確認なしにブランチを切り替えない。

## 実装

- Issue の受け入れ条件に沿って、最小の論理単位で実装する。
- スコープが広がったら Issue と PR の説明を更新する。必要なら別 Issue に分割する。
- 変更に応じてテスト、Lint、型チェック、E2E、ドキュメント更新を行う。
- レビューしづらい巨大差分を、理由なく1 PR にまとめない。

## コミットメッセージ

`type: 説明` の形式。日本語の短い文にする。モノレポでは `type(scope): 説明` にし、説明を短く保つためにカッコ表記は使わない。

type は次のいずれか。

- feat 新機能 / fix バグ修正 / perf 性能改善 / refactor 機能変更なしの改善
- docs ドキュメント / style スタイル修正 / test テスト / chore その他
- ci CI/CD 設定 / build ビルド設定 / merge PR のマージ（philtz-organizer-bot が作る squash のコミット専用。人とエージェントは使わない）

scope の決め方。

- ファイル変更のあったトップレベルディレクトリ名（リポジトリ直下のディレクトリ名）を使う。
- Turborepo などのモノレポで apps/ や packages/ 配下を変更するなら、配下のパッケージ名やアプリ名（leaf 名）を使う。apps/dashboard なら dashboard、packages/log なら log。
- リポジトリ全体に関わる変更は repo。
- 隠しディレクトリは先頭のドットを含めて書く。agents ではなく .agents。
- スラッシュで階層を表現しない。
- apps や packages などモノレポの親ディレクトリ自体を scope にしない。
- workspace、design のような実体のない総称や、存在しないフォルダ名を使わない。

```
NG: feat(workspace): / feat(design): / feat(agents): / feat(apps): / feat(apps/dashboard): / feat(packages/log):
OK: feat(repo): / feat(.agents): / feat(.claude): / feat(dashboard): / feat(log):
```

説明の書き方。

- 動作で終える。〜する、〜追加、〜修正、〜削除、〜実装など。
- 動作を伴わない名詞で終えない。`feat(api): ユーザー認証` ではなく `feat(api): ユーザー認証を追加`。
- emoji を含めない。
- 論理的なスコープ（パッケージ、機能）ごとにコミットを分割する。無関係な変更を1つのコミットに混ぜない。

## コミットの実行

- ファイルごとに `git diff` を実行し、各変更の作者を確認する。
- `git add .` と `git add -A` を使わない。
- committer を上書きしない。常にユーザーの git config を使う。
- `Co-Authored-By` を、コミットメッセージと PR 本文のどちらにも含めない。

すべての変更がエージェントによるもので、ユーザーが編集した行がない場合だけ、`--author` で自身のエージェント種別を明示する。

```sh
git commit --author="Claude <noreply@anthropic.com>" -m "<message>"
git commit --author="Codex <noreply@openai.com>" -m "<message>"
git commit --author="Cursor Agent <cursoragent@cursor.com>" -m "<message>"
```

実際に動作しているエージェント種別と一致する行を使う。他エージェントの例を流用しない。一部でもユーザーによる変更があれば、通常の `git commit` を使う。

- commit-msg hook が未承認の `Co-authored-by:` を自動付与する環境では、それを除去する hook を入れて対処する。`git commit --no-verify` で hook を迂回しない。
- 履歴修正で force push が必要なら、guard の許可を一時的に有効にして push し、作業後に戻す。
- PR の途中のコミットは squash されて main に残らない。途中のコミットのメッセージを直すためだけに、履歴を書き換えて force push しない。

## author と committer

GitHub は、コミットに記録されたメールアドレスで、どのアカウントの変更かを判断する。名前は判断に使わない。登録していないアドレスでコミットすると、アイコンが灰色になり、誰の変更か追えなくなる。author と committer のアドレスは別々に判断されるので、片方だけ灰色になることもある。

最初にコミットする前に、設定を確認する。

```sh
git config --show-origin user.name
git config --show-origin user.email
env | grep -E '^GIT_(AUTHOR|COMMITTER)_'
```

- user.email が未設定か、`root@...`、`...@localhost`、`....local` のような自動生成のアドレスなら、コミットしない。ユーザーに状況を伝え、設定を相談する。
- リポジトリ単位の設定や環境変数がグローバル設定を上書きしていないか、`--show-origin` の出力で確かめる。CI、Docker、devcontainer、クラウドのエージェント環境では、設定が入っていないことが多い。
- ユーザーの許可なしに git config を書き換えない。
- どのアドレスを使うか迷っていたら、GitHub が発行する noreply アドレスを提案する。必ずアカウントに紐づき、個人のアドレスを公開せずに済む。`gh api user --jq '"\(.id)+\(.login)@users.noreply.github.com"'` で取得できる。

rebase、cherry-pick、`commit --amend` では、author はそのまま残り、committer は実行した環境の設定に置き換わる。実行したあとは両方を確認する。

```sh
git log --format='%h author=%an <%ae> committer=%cn <%ce>' -10
```

push したあとは、GitHub 上でアカウントに紐づいたかを確認する。null の側が灰色のアイコンになっている。

```sh
gh api repos/<owner>/<repo>/commits/<sha> --jq '{author: .author.login, committer: .committer.login}'
```

灰色になっていたら、原因と直し方をユーザーに説明する。使ったアドレスを GitHub の Settings → Emails に追加して確認を済ませれば、過去のコミットにもさかのぼって紐づく。履歴を書き換えて直そうとしない。

## Git 操作の安全確認

あらゆる Git 操作（コミット、プッシュ、ブランチ作成、マージ、リベース）の前に `git fetch --prune` を実行する。そのうえで確認する。

- 現在のブランチがデフォルトブランチにマージ済みでないか。済みなら警告してブランチの切り替えを提案する。
- リモート追跡ブランチがまだ存在するか。削除されていれば警告する。
- ローカルブランチがリモートより遅れていないか。遅れていれば `git pull --rebase` を提案する。
- リモートと乖離していないか。乖離していれば警告し、リベースかマージを提案する。

ユーザーの承認なしに `git pull` や `git rebase` を実行しない。確認なしにローカルブランチを削除しない。

## PR

```sh
gh pr create --body "<本文>"
gh pr create --body-file <file>
```

- 本文を必ず明示する。`--fill` やエディタ生成で `Co-Authored-By` が混入し得る場合は使わない。
- タイトルと本文は、philtzjp/.github の `conventions.yml` に従う。リポジトリに `.github/conventions.yml` があれば、そちらに従う。
- タイトルは `type(scope): 説明` にする。説明はそのまま main のコミットの件名になる。
- 本文は署名の行から始め、見出しを背景、作業範囲、受け入れ条件、影響範囲・残リスクの順に書く。必要なら最後に備考を足す。
- 対象 Issue を自然言語で参照する。本文の背景に `#<issue-number>` を書く。
- `Closes #N` などの自動クローズのキーワードを使わない。Issue はマージ後に手で閉じる。
- philtz-organizer-bot が PR を開いたとき、編集したとき、push したときに書式を検査し、`organizer-bot/conventions` のステータスを付ける。違反があれば内容をコメントにまとめるので、直す。
- 作成前にローカルブランチを upstream へ push する。
- Draft で早めに作り、実装完了後に Ready for review へ切り替える。
- レビュー、CI、必要な検証を迂回してマージしない。

## マージ前チェック

```sh
git fetch --prune
git status --short --branch
```

- ローカルブランチが upstream に対して ahead / behind / diverged していないこと。
- PR ブランチがベースブランチに対して behind していないこと。
- PR が mergeable で、コンフリクトがなく、必須の CI、レビュー、チェックが通っていること。
- `organizer-bot/conventions` のステータスが成功していること。

対処。

- ahead なら push して再確認する。
- behind か diverged なら、ユーザーに報告し、rebase / merge / pull の方針を確認してから同期する。
- PR ブランチがベースブランチに対して behind なら、ベースブランチを取り込んで検証を再実行する。
- コンフリクト、失敗した CI、未解決レビュー、未確認の ahead / behind があるならマージしない。

## マージ

人とエージェントはマージしない。デフォルトブランチには誰も直接 push できず、画面のマージボタンも使えない。マージは philtz-organizer-bot だけが行う。

直前にもう一度 `git fetch --prune` と ahead / behind の確認を行い、PR に `merge` ラベルを付ける。

```sh
gh pr edit <番号> --add-label merge
```

philtz-organizer-bot は、次をすべて満たすときだけ squash でマージする。

- PR が開いていて、Draft でない。
- タイトルと本文が規約に合っている。
- ブランチがデフォルトブランチに追いついている。
- 必須の検査が通り、ruleset が求める承認がある。ラベルを付けたのが org の owner なら、承認は確かめない。

main に残るのは 1 PR につき 1 つのコミットで、件名は `merge(scope): 説明` になる。説明は PR のタイトルから取り、scope は変更したファイルから bot が決める。本文は付かない。author は PR を出した人、committer は philtz-organizer-bot で、`(#N)` と `Co-authored-by` は付かない。

- `gh pr merge` を使わない。
- merge プレフィクスでマージであることは明示されるので、PR のタイトルの説明に「マージ」と書かない。`feat(api): foo をマージ` ではなく `feat(api): foo を追加`。
- 条件を満たさなければ、bot が理由をコメントしてラベルを外す。直してからラベルを付け直す。
- ラベルを付けて 1 分たってもマージもコメントもされなければ、ラベルを外して付け直す。

## マージ後

- 対象 Issue は自動では閉じないので、`gh issue close <番号>` で閉じる。
- リモートの作業ブランチはマージで自動的に消える。ローカルのブランチは、ユーザーの意図を確認してから消す。
- マージ、レビュー、検証を保留する場合や解決が pending の場合は、Issue をクローズせず、保留（pending review）として状況と再開条件をコメントに残す。重複起票を防ぐため。
- 未解決の同一事象について Issue を重複起票しない。
- 同一事象で複数の Issue が起票・クローズされていたら、最古の Issue を親（正本）として sub-issue 関係を付け、後発を duplicate としてクローズし、変更内容を各 Issue にコメントする。

## Issue コメント

進み具合、完了、対応できないこと、設計のメモを Issue に残すときの書き方。GitHub はコメントにテンプレートを当てないので、次の形で書く。

```markdown
✳︎ <会社名> <モデル名> <バージョン>

## 背景

このコメントの論点を書く。実装の状況、調べた結果、前提の変化など。

## 作業範囲

- 行ったこと、調べた範囲、これからの対応

## 受け入れ条件

- [x] 受け入れ条件 1。満たし方と、確かめたコマンドと結果
- [ ] 受け入れ条件 2。満たせない理由と制約

## 備考

補足、関連する Issue や PR。なければ見出しごと消す。
```

- 署名の行は Issue や PR の本文と同じ。モデル名がバージョンを含むとき（GPT-5.5 など）は `<バージョン>` を省く。
- 主観ではなく、確かめられる事実、根拠、制約で書く。
- scope は Issue のタイトルが表すので、コメントには書かない。
- 受け入れ条件は Issue の項目ごとに、満たしたか、満たせないかを書く。
- 対応できないことを記録するときと、レビューやマージを保留するときは、Issue を閉じない。保留なら理由と再開の条件を書く。
- 重複として閉じたときは、正本にした最古の Issue と、duplicate にしたことを備考に書く。

## Release

GitHub Release のリリースノートの書き方。GitHub は Release にテンプレートを当てないので、次の形で書く。

- 署名を付けない。署名を付けるのは、Issue と PR の本文とコメントだけ。
- tag は `v<セマンティックバージョン>`、リリース名は `<リポジトリ名> v<バージョン>` にする。
- 主観ではなく、変わった事実と制約で書く。
- 配布物を添付するときは、ダウンロードのリンクを実際の tag の URL にする。

```markdown
<リポジトリ名> v<バージョン> は、<前のバージョン> からの変更を 1〜2 文でまとめる。

## 変更内容

### <機能追加などの分類>

- <変更>

## 制約

- <制約>

## インストール

1. <手順>

## 更新手順

1. <手順>

## 備考

補足、既知の問題、pre-release にした理由など。なければ見出しごと消す。
```

当てはまらない見出しは消してよい。
