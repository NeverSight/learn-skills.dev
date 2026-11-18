---
name: writing-discipline
description: Use when creating or editing persistent or reader-facing prose such as documentation, ADRs, Issues, Pull Requests, commit messages, code comments, and review comments. Converts working context into reader-oriented text through explicit selection, composition, and rereading instead of serializing conversation or execution context.
---

# Writing Discipline

文章生成を、agentが保持しているconversation / task / investigation / execution contextのserializationとして扱わない。

agentは作業中に大量のtext contextを保持する。そこに存在する情報を、その順序や粒度のまま成果物へ転写すると、会話・調査・作業の足場が文章へ混入する。persistentまたは他者向けのtextは、raw contextを縮約するのではなく、readerへ伝える内容を選び直し、独立したartifactとして再構成する。

原則:

> **Think in context. Select for purpose. Compose for the reader. Reread without the context.**

persistent reader-facing proseの作成・更新を開始する前にこのSkillをloadして適用する。raw context由来のdraftを先に作り、後から不要箇所をcleanupする順序にしない。routingが遅れて既にcontext serializationを含むdraftがある場合は、部分削除ではなくSelectから再構成する。

## 1. Scope

このSkillは、少なくとも次のtextを新規作成・更新するときに適用する。

- README / development guide / architecture docs / reference docs
- ADR / design / specification
- GitHub Issue / Pull Request description
- commit message
- code comment / doc comment
- review comment
- release note / migration note
- repository-controlled agent instructions / Skills

private scratchpadや一時的な内部整理を、ここでいうreader-facing artifactとして扱わない。ただし、内部整理をそのままpersistent artifactへ昇格してはいけない。

## 2. Writing is not context serialization

文章へ含める理由を「current contextに存在するから」にしてはいけない。

特に次を、そのまま文章化しない。

- conversationの流れ
- userとのやり取りの順序
- agentが調査した順序
- trial-and-errorの履歴
- 作業中に見つけた中間状態
- branch / commit / CI / tool outputの現在値
- 他agentから受け取ったraw report
- internal planning labelやscratch structure
- 「今回」「先ほど」「現在」等、artifact外のcontextへ依存するreferent

これらがartifactの意味、readerの判断、reproducibility、auditabilityに本当に必要なら含めてよい。時間性や履歴性そのものを禁止するのではなく、**readerへ伝える必要性**を根拠にする。

判断基準:

> その情報は、agentが知っているから書くのか。それとも、このartifactのreaderが知る必要があるから書くのか。

前者なら原則として捨てる。

## 3. Required writing pipeline

raw contextから直接final proseを作らない。

### Phase A: Select

書く前に次を決める。

1. audienceは誰か
2. artifactの目的は何か
3. readerが判断・理解・行動するために必要なfact / decision / constraint / rationaleは何か
4. readerに不要なconversation / execution / investigation scaffoldingは何か
5. 理解順に並べると、どの構造が自然か

ここでは文章を書き始めるより先に、communicative contentを確定する。

raw contextの順序を維持する必要はない。調査順、実装順、会話順ではなく、readerが理解する順序を選ぶ。

### Phase B: Compose

Selectしたcommunicative contentだけからstandalone proseを組み立てる。

- artifact単体で意味が通るようにする
- 主語・対象・referentをartifact内で解決する
- 必要な因果や接続を明示する
- readerに不要な作業者視点を消す
- raw noteの箇条書きを、そのまま完成文章とみなさない
- 同じ事実を複数の表現で反復しない
- 要約・見出し・比喩は元の事実に戻して説明できる形にする。根拠のない因果や語の結び付きを創作しない
- internal taxonomyやagent都合のsection構造を、reader都合の構造へ変換する
- rationaleを書く場合はdecision理解に必要な範囲へ限定する
- chronological narrativeが不要なら、conceptual structureへ組み替える

### Phase C: Reread

draftを完成扱いする前に、元contextを知らないreaderとして全文を読み直す。

> **Do not validate the prose against memory of the task. Read it as a standalone artifact.**

確認する:

- 前のconversationや作業経緯を知らなくても意味が通るか
- 書き手には自明だがreaderには欠けている前提がないか
- 指示語や「今回」「現在」等がartifact外へ依存していないか
- 文と文、段落と段落の接続が自然か
- 調査順・思考順ではなく理解順になっているか
- 同内容の重複や言い換え反復がないか
- 箇条書きがcontext dumpになっていないか
- 不要なstatus / history / implementation diaryが混ざっていないか
- internal reasoning labelやtool terminologyが露出していないか
- 一文ごとは自然でも、抽象的な結論の主張・語の関係・根拠が成立しているか
- 不要な説明を削っても、readerに必要な理由・制約・前提が残るか

問題があれば、追記だけで直そうとせず、順序変更・統合・削除・書き直しを行う。

## 4. Artifact-specific guidance

### Documentation

利用者が理解・操作・保守するためのcanonical knowledgeを書く。

- authorの作業履歴ではなく、対象のbehavior / contract / procedureを書く
- version-sensitive informationは必要ならversion/sourceを明示する
- obsoleteなmigration historyをcurrent procedureへ混ぜない
- troubleshootingでは再現可能なsymptom / cause / diagnosis / remedyを中心にする

### ADR

decisionを理解・再評価するために必要なproblem structure、constraints、decision、consequencesを書く。

- meeting/chat transcriptにしない
- 調査ログにしない
- 「この作業でこうなった」ではなく、なぜこのdecisionが妥当かを書く
- chronologyがdecision理解に必要な場合だけhistoryを残す

### Issue

解くべきproblem、desired outcome、constraints、acceptance criteria、dependencyを書く。

- 発見までの会話を再現しない
- implementation diaryを先回りして書かない
- unresolved consequential decisionがある場合だけ明示する

### Pull Request

reviewerがchangeの意図・surface・重要なdesign decision・validationを評価するために必要な内容を書く。

- commit historyの散文要約にしない
- branch同期やtrial-and-errorの経緯を通常本文へ書かない
- current SHA / ahead-behind / bot status等を、reader判断に必要でない限り本文へ転写しない
- 「何を変えたか」だけでなく、non-obviousな「なぜ」を必要な範囲で書く

### Commit message

commitによるrepository stateの意味ある変化を書く。

- agentが何を試したかではなく、commitが何を変えるかを書く
- temporary failureやtool invocationを記録しない
- rationaleが重要ならbodyで簡潔に補う

### Code comment / doc comment

codeから自明でないintent / invariant / constraint / contractを書く。

- 変更履歴を書かない
- 「ここを修正した」「以前は〜だった」を通常commentとして残さない
- codeの逐語的説明を繰り返さない
- work contextではなく、future maintainerが必要とする意味を書く

### Review comment

recipientが問題を理解し、判断または修正できる形へ整える。

- 「見ていて気になった」等のreviewer実況を不要に含めない
- 問題箇所、影響、根拠、期待する状態を明確にする
- raw thought processや調査過程を貼り付けない

## 5. Temporal and execution information

temporal informationを禁止しない。

次のいずれかを満たす場合は残してよい。

- version compatibilityを正しく説明する
- migration / deprecation / rolloutを理解するために必要
- incident / audit / security recordとして必要
- reproducibilityに必要
- readerが現在の判断を誤るのを防ぐ
- artifact自体がstatus report / changelog / runbook recordである

それ以外のcurrent-state情報は、作業中に存在するという理由だけでpersistent proseへ昇格しない。

## 6. Natural prose requires editing

correctnessだけで文章品質を判定しない。

自然な文章には、少なくとも次の編集を行う。

- redundant sentenceの削除
- awkward transitionの書き直し
- readerに合わせた情報順序への再配置
- fragmented bulletsの統合
- long sentenceの分割
- repeated terminologyの整理
- unnecessary meta-languageの削除
- referentの明確化
- paragraph単位でのtopic coherence確認

rereadはproofreadingだけではない。**reader-oriented editing**である。

## 7. Completion criterion

次を満たすまでreader-facing textを完成扱いしない。

- audience / purposeが明確
- communicative contentがraw contextから選別されている
- conversation / execution scaffoldingが不要に残っていない
- artifact単体で理解できる
- artifact種別に適した情報だけが残っている
- reread後に構造・接続・冗長・context dependenceを編集済み
- temporal/history情報はreaderへの必要性で説明できる

文章量を増やすことを品質とみなさない。必要な情報を選び、自然に伝わる形へ整えることを品質とする。
