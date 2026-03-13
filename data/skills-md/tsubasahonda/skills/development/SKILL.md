---
name: development
description: ユーザーの合格基準を満たすために必ず守る必要がある原則. この原則に従っていないコミットをユーザーは承認しない. 実装完了の Definition of Done (DoD) を運用する。実装後に RUNBOOK.md 準拠で build/test/migrate/seed/container 再ビルドを実行し、ユーザーが検証可能な状態まで仕上げる。実行不能項目がある場合は理由を明記する。開発タスク全般で使用する。
---

# 実装の原則

テストファーストを実践し、 Red-Green-Refactor のフローを遵守する

## 実装前の準備

必ず、 web と docker コンテナが起動していることを確認する.
起動していない場合、ユーザーに起動を依頼すること
開発中に問題が起きた場合にはログから情報を得ること

### Linear チケット起点で実装する

実装タスクが Linear チケットに紐づく場合は、以下を必須で実施する。

1. 対象チケットを確認する（タイトル/説明/受け入れ条件/priority）。
   - 例: ブラウザ `https://linear.app/{team_id}/issue/STA-xxx/...`
   - 例: `.agents/skills/linear-curl-issue-ops/scripts/linear_graphql.sh 'query ...'`
2. 実装前に「この変更で満たす受け入れ条件」を 1-3 行で明文化する。
3. 実装中にスコープ変更が出たら、先に Linear 側へ追記してからコード変更する。
4. 実装完了時に、チケットへ以下を追記する。
   - 変更概要（何を変えたか）
   - テスト結果（実行コマンドと成功/失敗）
   - 未実施項目と理由
5. チケットに紐づかない作業を行った場合は、理由をユーザーへ明示する。

### ログから情報を取得する

`chase` コマンドで実行ログを取得することができる

1. Verify the project is initialized:
   - Run `chase describe --output json`.
   - If initialization is missing, run `chase install .`.
2. Collect high-signal failures first:
   - Run `chase errors --output json`.
3. Inspect specific logs only when needed:
   - Run `chase logs web 120 --output json`.
   - Run `chase logs compose 120 --output json`.
4. Produce a shareable snapshot for handoff:
   - Run `chase debug-bundle --output json`.
   - Read `.debug/latest.md`.

## テスト品質基準

### テスト観点は「壊れたら何が起きるか」から書く

実装前に最低でも以下を列挙する:

- 混入しないこと（異なるソース/種別のデータが混ざらない）
- 上書きしないこと（既存状態を意図せず変更しない）
- 表示できること（書いたデータが一覧/詳細で見える）
- 障害を握り潰さないこと（error を skip/success に変換しない）
- 片系だけ成功/失敗しても状態が壊れないこと

### コメントだけのテストを禁止する

- 本番コードを呼んでいないテストは弱い
- assertion がないテストは無効
- `t.Skip` だけの新規テストは原則追加しない
- stub に計測フィールドを足したら、テスト側で必ず読んで assert する

### テストを 3 層で最低 1 本ずつ置く

1. **pure unit**: 分岐・定数・引数伝搬（例: 定数に期待値が含まれるか）
2. **behavior unit**: stub で副作用確認（例: 正しい引数で呼ばれたか、呼ばれなかったか）
3. **integration-ish**: DB query / handler response の最小疎通（DB不要の場合は nil 注入で panic テスト等で代替可）

### データ分離の確認を必須とする

- 新しい識別軸（source, type, version 等）を追加した場合、「識別子が1つで足りるか」を必ず疑う
- read/write 両方で分離が効いているかテストする
- 既存一覧/詳細 API に新データが正しく出る（または出ない）ことを確認する

## 回帰チェックリスト（PR 前に毎回確認）

- [ ] 新しい識別軸は read/write 両方に反映したか
- [ ] 既存一覧/詳細 API に新データが出るか（または意図的に除外されるか）
- [ ] 既存処理から除外すべきデータは本当に除外されるか
- [ ] error を skip/success に変換していないか
- [ ] metrics / status / UI detail が実データと一致するか
- [ ] 書けることと見えることが一致しているか（実装と観測系の整合）

# Definition of Done (DoD)

1. 変更は課題解決に必要な範囲へ限定する。
2. 実装後は `RUNBOOK.md` の手順に従って必要コマンドを実行する。
3. ユーザーがすぐ検証できる状態を作る（起動、疎通、確認コマンド提示まで含む）。
4. 実行不能なチェックは黙って省略せず、未実施理由と影響を明記する。

# ブランチ戦略

- ブランチは `feature/xxx` 形式で作成する.
- main ブランチでの開発は避け、mainブランチにいる場合は新しいブランチに　checkout してから作業を開始する

- 対象: screening / backtest / jobs / （必要なら market, portfolio, autotrade）

# 記録と報告ルール

1. 実行したコマンドと結果（成功/失敗）を簡潔に報告する。
2. 変更した依存関係を ascii アートで示す（例: `A -> B` で A が B に依存していることを表す）。
3. 実装したテスト項目を必ずリストで記載する。

- 例: `追加したユニットテスト`, `修正した既存テスト`, `実行した統合テスト`, `手動確認シナリオ`

3. 未実施項目がある場合は以下を必ず記載する。

- 未実施項目
- 未実施理由（環境制約・権限・依存不足など）
- 影響範囲
- ユーザーが代替実行するためのコマンド

4. 変更終了時はプロジェクトメモリを同期する。

- 最低でも `STATUS.md` の「最終更新日」「変更点」「次アクション」を更新する。
- 仕様/設計/運用手順に変更があれば `SPEC.md` / `ARCHITECTURE.md` / `RUNBOOK.md` も更新する。
- `PLAN.md` も必要に応じて更新する。
- Linear チケット作業の場合は、対応 Issue に実装結果コメント（変更概要/テスト/未実施）を追記する。

# レビュー観点テンプレート

実装レビュー時に「正常系」だけでなく「逆方向」も見る。新機能の追加時は、既存機能から見て以下を必ず確認する:

- **データ分離は十分か**: 何が見えてはいけないか、何が混ざってはいけないか
- **状態更新の副作用は閉じているか**: 何が更新されてはいけないか
- **失敗は失敗として観測できるか**: error の握り潰し、silent skip がないか
- **一覧/詳細/履歴まで一貫して見えるか**: 書いたデータが全経路で正しく表示されるか
- **その仕様を落とす回帰テストがあるか**: 壊れたときにテストが落ちる assertion が存在するか
