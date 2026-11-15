---
name: agent-recovery
description: AI agent/session/sandbox interruptionからticket workを安全に復旧・再開する時に使用する。
---

# Agent Recovery

AI agentの復旧は「同じ会話を再開できること」に依存させない。

native session/thread/subagent resumeが利用できる場合は高速経路として使ってよいが、**別agent・別process・別sandboxでもdurable project stateから再構成できること**をcanonical recovery pathとする。

## 1. Recovery goals

最低限、次のfailureから復旧可能にする。

- model/session context loss
- agent process crash / cancellation
- terminal/IDE restart
- parent agent crash while children continue
- child/subagent crash
- sandbox/container/VM recreation
- local Supervisor restart
- transient network/provider failure
- CI interruption/retry
- host reboot

project/provider要件に応じて、machine/provider lossまでのRPO/RTOも定義する。

## 2. Durable state / transient state

### Durable recovery sources

復旧時に優先するcanonical evidence:

1. GitHub Issue
2. GitHub Projectのstatus / target release / priority / dependency state
3. target release branch
4. ticket branch / current remote commit graph / stack relation
5. Draft/Ready PRとassignee / reviewer / labels / review / CI state
6. stack predecessor Issue/PR / pinned predecessor SHA when applicable
7. committed design / ADR / Agent Skills / docs
8. immutable worker/subagent result commits/refs/artifacts
9. durable recovery checkpoint / handoff record

active ticketにはpublished headとPRを必須とし、Issue/branch/baseを確認して欠落PRを修復する。PR stateは作業中Draft／readiness後Readyへ整合し、Ready ticketはblockerがなければ自律landingする。

release branchは例外を持つ。`main`とzero-diffのrelease branchはGitHub上Draft PRを作成できないため、その状態だけはDraft release PR不要である。first meaningful integrated differenceがrelease branchに入った後は、Draft release PRが存在しない状態を正常とみなさない。

### Transient optimization state

次は利用できれば使うが唯一のSoTにしない。

- native conversation/thread ID
- agent/subagent ID
- Supervisor local DB / queue
- sandbox process state
- shell history
- IDE state
- unpushed local logs
- model-private context

transient state消失だけでticketを最初からやり直す設計にしてはいけない。

## 3. Recovery checkpoint

長時間taskではmeaningful boundaryでstructured checkpointを作る。

checkpointにはprivate chain-of-thoughtを保存しない。**再開に必要な外部化可能な事実・決定・次行動だけ**を保存する。

最低限候補:

```text
schema_version
issue_id
target_release
ticket_branch
pr_number
immediate_pr_base
predecessor_issue_or_pr
predecessor_sha
base_sha
checkpoint_sha_or_snapshot
fencing_identity_or_execution_generation
status
completed_steps
next_steps
pending_validation
active_children
integrated_child_results
external_side_effects
blockers
decision_refs
artifact_refs
updated_at
```

checkpointはmachine-specific absolute pathやsecretへ依存させない。

README / ADR /通常のIssue・PR本文等のreader-facing proseをrecovery journalとして使用しない。Issue / PRをcheckpoint carrierにする場合も、通常本文へ作業履歴を混在させず、recovery用途として明示されたstructured record / handoff surfaceへ分離する。reader-facing prose側は `writing-discipline` に従う。

## 4. Soft checkpoint / hard checkpoint

すべての小さな操作をremote Gitへcommitしてhistoryを汚さない。

### Soft checkpoint

同一sandbox/host再開向け。

候補:

- local immutable Git ref/commit
- filesystem/container snapshot
- Supervisor durable journal
- native session state

高頻度に作成できる。

### Hard checkpoint

sandbox/providerを失っても復旧する境界。

最低限:

- meaningful code stateがcanonical remoteで到達可能
- durable ticket branchではrecorded commit SHAとremote branch headの対応が追跡可能
- Issue/Project/PRから現在statusを判断可能
- active durable ticket branchにはPRが存在し、stateが実際のwork stateと一致
- release branchはzero-diffならDraft release PR不要、first meaningful integrated difference後はDraft release PRが存在
- stackならpredecessor identity / exact predecessor snapshotが分かる
- next step / pending verification / blockerがdurableに分かる

実装方式はproject/runtimeに合わせて選ぶ。ticket branchへのWIP commit、dedicated checkpoint ref、durable object store、PR/Issue上の更新可能なhandoff record等を使用できる。

branch/UI clutterとhistory noiseを増やしすぎない方式を優先する。

## 5. Checkpoint triggers

最低限、次の前後でcheckpointを検討する。

- non-trivial implementation milestone完了
- risky refactor/migration前
- child/subagent spawn前
- child result integration後
- stack predecessor update / downstream rebase前後
- long validation開始前/完了後
- external side effect前/後
- user/external input待ちへ移る時
- provider shutdown/TTL接近時
- graceful cancellation/shutdown signal受信時
- context limit接近時

時間ベースcheckpointも利用できるが、semantic boundaryを優先する。

## 6. Recovery algorithm

新しいagentは以前の会話を推測しない。

標準手順:

1. Issue / GitHub Project / PR / target release / dependencyを特定する。
2. current ticket/release branch、remote commit graph、stack predecessor/successor relationをfetchする。
3. ticket PRのhead/state、linked Issue、metadata/baseをread-only確認し、欠落やdriftを修復候補として記録する。
4. 未landingのReady PR、未close Issue、残存branch、dependent PRをread-only検出する。ownership取得前はmutationしない。
5. release branchのmain差分とDraft PRを確認（zero-diff例外あり）。release PRはbulk landing対象外で、explicit authorizationなしにmergeしない。
6. latest valid recovery checkpointを読む。
7. canonical design/policy/decision refsを再確認する。
8. observed fencing identityに対するcompare-and-set等でrecovery ownershipを**原子的に取得**し、新しいfencing identityを確定する。current implementationでgeneration方式を使う場合はnew `execution_generation` と一意なlease/fencing tokenを発行する。競合した場合はownershipを共有せず、stateを再読してやり直す。
9. active child/subagent stateをlogical Supervisorへ問い合わせ、current fencing identityとの関係をreconcileする。
10. current workspaceをcheckpointからrecreateする。
11. stack-ready workではrecorded predecessor SHAとcurrent intended predecessor stateを比較し、差があればstale baseとしてreconcileする。
12. completed/pending validationをcurrent snapshotに対して再評価する。
13. current fencing・refs・validation・side effectsを再確認後、3〜5のPR修復、ticket landing、Issue close、dependent PR調整、safe cleanupを順次実行。mutationごとにfencing再検証し、release mergeを含めない。
14. stale base / conflicting integrationを確認する。
15. remaining planを再構成する。
16. safeな最小verificationを実行してstateを信頼できることを確認する。
17. current fencing identityの所有権を維持したまま作業を継続する。

native resumeが成功しても、重要なIssue/Project/branch/PR/stack/checkpoint stateとの整合を確認してから続行する。

## 7. Parent / child recovery

child lifecycleはparent model processではなくSupervisorが所有する。

parentが死亡しても、safeならchildを即cancelしない。

recovered parent/coordinatorは:

- child一覧を再発見
- input snapshot / predecessor snapshot / applicableなcurrent fencing identityを確認
- running/completed/failed/orphanedを分類
- completed resultをimmutable resultとして回収
- stale child resultは自動統合しない
- durable branchを作ったchildではpublished remote head / PR identity/state / metadataをreconcile
- 必要ならretry/resume/re-spawn

を行う。

child自身も独立checkpointを持てるようにする。

## 8. Duplicate execution / split-brain防止

network partitionやtimeout後に旧agentと新agentが同時実行される可能性を前提にする。

Supervisorはticket/taskごとにleaseまたはfencing identityを持つ。

- current implementationがgeneration方式の場合、mutable taskの初期 `execution_generation` は `1` とする
- recovery/reassignment時はobserved fencing identityに対するcompare-and-set等でownershipと新しいfencing identityを原子的に取得する
- 複数recoveryへ同じfencing identityを発行しない
- worker resultへapplicableなfencing identityを付与する
- stale fencing identityからのbranch integration / external writeを拒否する
- **各external write直前にcurrent fencing tokenを再検証する**
- heartbeat消失だけで即座に同一side effectを再実行しない

同じticket branchへ複数fencing identityが同時pushすることを通常運用にしない。

## 9. External side effects / idempotency

Git外の操作は特に危険。

例:

- production/staging deploy
- DB migration
- package publish
- release/tag creation
- cloud resource mutation
- notification/email/comment creation
- billing/cost-producing operation

可能ならidempotency keyを使用する。

side effect前にintent、後にresult/remote identifierをdurable journalへ記録する。実行直前にcurrent fencing tokenを検証し、recovery時はownership取得後にremote actual stateを確認してからretryする。

`command returned no response = operation did not happen` と推測してはいけない。

irreversible/destructive operationはengineering-decisionsのuser escalation policyも適用する。

## 10. Validation recovery

validation途中で中断した場合、途中までのgreenをfull passとみなさない。

各validation resultには最低限:

- `validated_sha` またはcontent-addressed `validated_snapshot`
- validation profile/version
- completed checks
- failed checks
- not-run checks
- artifacts/report references

を記録する。

recovery後に既存resultを再利用できるのは、**validated snapshotがcurrent code snapshotと完全一致し、そのcheck自体のdeterminism/dependency条件も維持されている場合だけ**とする。checkpointまたはcode snapshotが変わった場合は、古いgreen resultをcurrent codeのpassとして扱わない。

特にstack predecessor変更によるrebase/updateでdownstream SHAが変わった場合、affected required validationを新しいSHAで再実行する。

release/integration gateでは、stale code state上の古い成功結果を流用しない。

## 11. Context compaction / handoff

context window接近はfailureではなく予測可能なhandoff eventとして扱う。

agentはcontext不足になる前に:

- current objective
- accepted decisions
- relevant refs/files
- Issue / target release / PR / stack predecessor
- completed work
- current diff/checkpoint
- pending work
- validation state
- blockers

をstructured checkpointへ外部化する。

長い会話要約やprivate reasoningを保存するのではなく、fresh agentが再実行可能なoperational stateへ圧縮する。

## 12. Recovery test

recovery policyはdocumentだけで終わらせない。

project/runtimeが許す範囲で定期的に:

1. ticket workをcheckpointする
2. agent/sandboxを意図的に停止する
3. fresh agent/sandboxからrecoveryする
4. Issue/Project/branch/PR/stack/children/validation/side-effect journalを再構成する
5. durable ticketではpublished remote head / PR identity/state / linked Issue / metadata / predecessor baseを検証し、missing PRをrepairできることを確認する
6. Ready ticket PRのautonomous landing、target release landing後のIssue close、safe branch cleanupがrecovery後も重複mutationなしでreconcileできることを確認する
7. release branchではzero-diff例外またはfirst-difference後Draft release PRの存在を検証し、release PRがexplicit authorizationなしにlandingされないことを確認する
8. duplicate mutationなしで続行できることを確認する

chaos/recovery drillをintegration infrastructureの一部として採用できる。

## 13. Recovery completion criteria

recovered taskを「再開成功」とみなす条件:

- canonical Issue/Project/PR/release/dependencyとの対応が確認済み
- active durable ticket branchはmeaningful stateがcanonical remoteへpublish済みで、remote head identityが確認済み
- active ticketにPRと現状に合うDraft/Ready state、Issue/base/metadataが存在
- Ready ticketはblockerがなければlanding済みで、Issue close・safe cleanupまで整合
- release PRはzero-diff例外・Draft/Ready・明示authorization boundaryを遵守
- stackならpredecessor identity / exact base snapshotが確認済み
- workspaceが追跡可能なsnapshot/commitから再構成済み
- current fencing identityを一意に所有している
- stale executionがintegration/external-write権限を持たない
- active childrenがreconciled済み
- external side effectsの不明状態がない、または明示的blocker化済み
- validation stateがcurrent code snapshotに対して正しく再評価済み
- remaining next stepがstructured stateとして明確

会話を完全復元できたことは必要条件ではない。
