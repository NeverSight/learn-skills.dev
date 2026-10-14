---
name: gh-review-until-approved
description: GitHub pull request のレビューを継続監視し、各指摘を実際のコードと要件に照らして検証し、正しい指摘だけを修正・検証・git-commit スキルでコミット・push して、現在の PR head が正式に approve されるまで反復する。GitHub PR URL を伴う「レビューを監視して修正を続けて」「approve まで継続」「/goal でレビュー対応を自動化」などの依頼に使用する。誤り、曖昧、競合、危険、範囲外、または既に満たされた指摘は変更対象からスキップし、他の指摘と監視ループを継続する。
---

# GitHub Review Until Approved

GitHub PR のレビューサイクルを、指摘の妥当性確認を省略せず approve まで継続する。

## 実行契約

- PR URL、対象リポジトリ、PR head branch、push 先を最初に確定する。
- `gh` を使うすべてのコマンドを、ネットワークアクセス可能な権限で実行する。
- 利用可能なら `github:gh-address-comments` スキルを併用し、未解決スレッドを thread-aware に取得する。
- 各修正コミットで `git-commit` スキルを読み、そのステージング分離、Conventional Commits、秘密情報保護の手順に従う。
- `/goal` などで「修正、commit、push を approve まで反復する」と明示された依頼を、レビュー範囲内の各コミット計画と通常の push に対する事前承認として扱う。コミット計画は commentary で示すが、同じ承認を反復して求めない。
- 自動反復が明示されていない場合、最初の commit と push の前に承認を得る。
- 誤り、曖昧、競合、危険、範囲外、重複、または既に満たされた指摘を、理由と comment/thread ID を記録してスキップする。スキップを理由にループ全体を停止しない。
- GitHub への返信、スレッド解決、review 投稿、force-push、amend、ブランチ削除、merge を自動実行しない。これらは個別の明示承認を必要とする。
- 既存の未コミット変更を上書き、混入、退避しない。安全に分離できなければ停止する。

## 1. PR と作業コピーを確定する

1. `https://github.com/OWNER/REPO/pull/NUMBER` 形式の URL を解析する。
2. `gh auth status` を確認し、失敗時は認証を依頼して停止する。
3. `gh pr view URL --json number,url,state,isDraft,headRefName,headRefOid,headRepository,headRepositoryOwner,baseRefName,reviewDecision,mergeStateStatus` で対象を確定する。
4. `state` が `OPEN` でない場合、または draft の扱いが依頼から判断できない場合は停止する。
5. matching checkout を探し、`git remote -v`、`git status --short --branch`、`git branch --show-current` で同一性と汚れを確認する。
6. checkout がなければ通常の clone/checkout を行う。対象ブランチへの切替で既存変更に触れる場合は、専用 worktree または別 clone を使う。
7. fork PR を含め、push remote が `headRepository`、push branch が `headRefName` に一致することを確認する。書込み権限を推測しない。
8. PR head を取得し、ローカル基準点を `headRefOid` に合わせる。履歴を書き換えない。

URL とレビュー状態の取得には、このスキルの `scripts/fetch_pr_review_state.py URL` を使用する。`gh` のネットワーク権限は呼出側で付与する。

## 2. レビュー状態をスナップショットする

各反復で次を同じ時点の証拠として保存する。

- `headRefOid`、`reviewDecision`、PR state、更新日時
- review の state、author、submittedAt、対象 commit OID
- review thread の `isResolved`、`isOutdated`、path、line、全コメント
- top-level conversation comments
- head commit の check/status 一覧

flat なコメント一覧だけで未解決状態を判断しない。`isResolved: false` かつ `isOutdated: false` の thread を active thread とする。active thread に加え、現在の head に対する `CHANGES_REQUESTED` review 本文と、基準点より後に reviewer が投稿した明示的な変更要求を finding 候補にする。一般的な CI レポートや会話コメントを自動的に変更要求へ昇格させない。前回処理済みの comment ID と head OID を記録し、同じ指摘を二重処理しない。

push 後はレビューが完了する前の途中状態を修正対象にしない。review/check が進行中なら 30〜60 秒単位で再確認し、1分を超える無言の待機を避ける。新しい review submission または active thread が揃うまで監視を続ける。

## 3. 指摘の正しさを判定する

コードを変更する前に、すべての新しい active finding を次のいずれかに分類する。

1. `correct-actionable`: 現在の head に実在し、要求または既存契約に反し、具体的な修正で解消できる。
2. `informational`: 変更要求ではない。
3. `duplicate-or-stale`: 解決済み、outdated、または既に head で満たされている。
4. `incorrect`: 前提、実行経路、API、テスト期待値、または要求理解が誤っている。
5. `ambiguous-conflicting-unsafe`: 意図を一意に決められない、別指摘と競合する、回帰や範囲外変更を要求する。

判定では PR diff だけに依存せず、実際の checkout から次を確認する。

- リポジトリ内の `AGENTS.md` と関連ドキュメント
- 指摘された行の呼出元、設定伝播、データフロー、互換性契約
- 関連テストと、必要なら再現または最小の診断
- PR の目的、base/head 差分、過去の関連コメント

`incorrect`、`ambiguous-conflicting-unsafe`、`duplicate-or-stale`、`informational` は変更対象からスキップし、comment/thread ID、分類、根拠を処理済み記録へ残す。スキップした指摘に対する修正、commit、GitHub 返信、thread resolve は行わない。同じスナップショットに `correct-actionable` があれば、その処理を継続する。

スキップ対象しかない場合は、空の commit や不要な push を作らずレビュー監視へ戻る。reviewer が完了しても approve していなければ、理由を推測した修正を行わず、新しい review submission、head 更新、または finding を待つ。

## 4. 正しい指摘を修正して検証する

`correct-actionable` が一つ以上あれば、スキップ対象を変更から除外し、正しい指摘を同じ原因や領域ごとにまとめて修正する。

1. 各変更を comment/thread ID と対応付ける。
2. 指摘された一行だけでなく、同じ契約を持つ並行経路も検索する。
3. 回帰テストを追加または更新する。
4. リポジトリ固有の最小検証から開始し、変更リスクに応じて対象テスト、lint、typecheck、build を実行する。
5. listener、network、credential など環境要因の失敗と、実装修正が必要な失敗を区別する。
6. `git diff --check`、`git diff`、`git status --short` で差分と混入を確認する。

検証失敗が実装の問題なら、同じ反復内で修正して再検証する。無関係な CI 障害や新しい権限が必要なら、レビュー修正へ偽装せず blocker として報告する。

## 5. `git-commit` で commit して push する

1. `git-commit` スキルに従い、変更分析とコミット計画を作る。
2. レビュー修正に属するファイルだけを個別に stage する。`git add .` と `git add -A` を使わない。
3. review finding と検証根拠が追える Conventional Commit を作る。
4. commit hook が失敗した場合、`--no-verify` を使わず原因を直して新しい commit を作る。
5. `git status` と commit 内容を再確認する。
6. `git push REMOTE HEAD:HEAD_REF_NAME` のように PR head branch を明示して通常 push する。force-push しない。
7. push 後に GitHub の `headRefOid` がローカル commit OID と一致するまで確認する。

push が拒否された場合、remote の新しい commit を読み、勝手に rebase/merge/force-push しない。競合または第三者更新として停止する。

## 6. approve まで反復する

push した head OID と時刻を次の基準点として保存し、レビュー状態を継続監視する。

- 新しい active finding が届いたら Step 3 へ戻る。
- スキップ対象だけが届いたら処理済み記録を更新し、変更や push を作らず監視を続ける。
- reviewer/check がまだ処理中なら待機して再確認する。
- review infrastructure が失敗した場合、コード修正で直る根拠がなければ変更せず blocker を報告する。
- PR head が第三者により変化した場合、ローカル変更を重ねず新しい head を再評価する。

次をすべて満たした場合だけ完了とする。

- PR が `OPEN` である。
- `reviewDecision` が `APPROVED` である。
- 現在の `headRefOid` を対象 commit とする正式な `APPROVED` review が存在する。
- 現在の head に active な actionable review thread が残っていない。

古い commit への approval、肯定的な top-level comment、成功した CI check、thread の自動 outdated 化だけを approve とみなさない。完了時は PR URL、最終 head OID、作成した commit、実行した検証、最終レビュー根拠を報告する。

## 停止条件

次のいずれかでは「approve まで」のループを停止し、証拠と次に必要な入力を返す。

- GitHub 認証、push 権限、必要な repository secret が不足する。
- checkout や push branch の同一性を保証できない。
- unrelated dirty changes を安全に分離できない。
- PR が closed、merged、draft のまま、または head が予期せず更新された。
- reviewer/check service が失敗し、再レビューが開始または完了しない。

ユーザーの判断が必要な停止を「approve 済み」や「完了」として扱わない。
