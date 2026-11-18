---
name: parallel-orchestration
description: 複数AIエージェントへtaskを分解・委譲し、immutable snapshot/resultとdependency-aware stacked deliveryで安全に並行統合する時に使用する。
---

# Parallel Orchestration

Layer: **Operating Model + Skill**

非自明な実装をdependency graphへ分解し、Readyまたはstack-readyなnodeをresource/WIP制約内で安全に並行実行する。

Constitutional requirementは「1 worker = 1 particular sandbox」ではなく **Mutable Ownership Safety / Identity Integrity / Organizational Continuity** である。current modelはisolated mutable runtime + immutable snapshot/result + fencing identity（現在はgeneration-based fencing）でこれを実現する。

より強いagent/runtimeが同等以上のguaranteeを別mechanismで提供する場合は、ADR-0017のrefinement contractに従って置換できる。Worker / Supervisor のlogical roleと observational / mutable / durable attempt の分類は `organization/execution-roles.md` と ADR-0019 をcanonical sourceとする。Herdrをselected runtime Practiceとして使う場合は `herdr-runtime` Skillを適用するが、Herdr lifecycle stateをcanonical task/result stateにしない。

## Attempt-class routing

spawn前にroleだけでなくexecution attempt classを決める。

- **observational**: research / exploration / independent review / read-only diagnostics。source/runtimeのmutable ownershipを持たない限りbranch / Draft PR / sandbox / fencing / durable checkpointを要求しない。
- **mutable**: independent implementationやstateful execution。明示的mutable-ownership boundary、base/result identity、stale result rejectionを要求する。
- **durable**: Issue-level / long-running / background / remote execution。mutable要件に加えてdurable discoverability、checkpoint/recovery、fencingを要求する。

観測用subagentがsourceを変更し始めた場合はmutableへ、session/provider lossを越えて継続すべきworkになった場合はdurableへpromotionする。

## Current operating guarantees

- concurrent mutable implementation workerごとにisolated runtime、serialization、transaction等の明示的mutable-ownership boundaryを持つ。current defaultは1 worker = 1 isolated mutable runtime。
- shared working tree / Git index / integration branchを複数workerが直接更新しない。
- parent -> child はimmutable snapshot。
- child -> parent はimmutable commit/ref/diff + validation result。
- sandbox lifecycleはworker外のSupervisorが管理する。
- worktree単体をexecution isolationとみなさない。
- WSL/LinuxでSupervisorがlocal branchをworktreeへmaterializeする場合は`worktree-workflow` Skillに従ってWorktrunkを使用できるが、各workerのruntime isolationとimmutable result contractは別に維持する。
- durable planning unitはGitHub Issue、短命な内部subtaskはSupervisor taskとしてよい。
- Issue dependency graphがdurable dependency SoTであり、Git branch topologyだけでdependencyを管理しない。
- child lifecycleはparent model processではなくSupervisorが所有する。
- durable worker task/resultはstale attemptを排除できるfencing identityを持つ。current implementationでは `execution_generation` を使用し、初期generationは `1`、recovery/reassignment時にSupervisorが原子的に進める。
- result統合前にapplicableなcurrent fencing identityとの一致を検証し、stale identityを統合しない。
- validation resultはvalidated SHA/snapshotにpinし、stack rebase/update後の別SHAへ流用しない。
- long-running task / context limit / sandbox recreationでは `agent-recovery` Skillを適用する。
- `security-audit` のcandidate validationではhunterとverifierを同一agentにせず、fresh verifierへimmutable candidate/evidenceを渡す。final record verificationが必要なprofileでも同じseparationを維持する。
- spawn前に `policy-evaluation` Skillのexecution profileを判定し、mechanical / localized taskへ不要なfan-outを導入しない。

## Execution profile routing

orchestration strengthはtask sizeの印象ではなくexecution profileから決める。

- `mechanical`: solo executionをdefaultとし、deterministic tooling / focused validationを優先する。
- `localized`: bounded scopeをsoloで進め、必要なvalidationと、policy/user-visible riskがある場合のcold final reviewを追加する。
- `cross-boundary`: dependency graphへ分解し、安全なnodeのみparallelizeする。candidate artifact完了後はbuilderと分離したindependent cold reviewを必須とする。
- `judgment-heavy`: evidence / reference / acceptance rubricを先に固定し、candidate artifact完了後はbuilderと分離したindependent cold reviewを必須とする。

複数profileに該当する場合はsafeguardを合成する。特に `cross-boundary` かつ `judgment-heavy` のtaskはdependency decomposition / safe parallelismとevidence/rubric-first executionの両方を適用し、combined routingをorchestration前に記録する。

execution profileは `quality-gate` のverification risk taxonomyを置換しない。orchestration/review強度とtest levelを別々に決定する。

## Adaptive fan-out / fan-in

fan-outはagent数ではなくadmitted progressを最適化する。まず **smallest useful fan-out**（独立して価値を出せる最小数）で開始し、各fan-in boundaryで再評価する。

mode:

- **independent decomposition**: Ready / stack-readyな独立nodeを並行実行する。
- **competitive exploration**: uncertain problemへ複数のobservational candidateを独立に作らせる。多数決ではなくevidence / measurement / validationで比較する。
- **specialist separation**: builder / reviewer / benchmark / security等を責務分離する。
- **speculative execution**: reviewable immutable predecessor snapshotへexact pinできる場合だけ先行する。predecessor変更時はstaleとしてreconcileする。

competitive mutable implementationは、各attemptが独立mutable ownership boundary、同一base/input identity、immutable result contractを持つ場合だけ許可する。満たせなければobservational explorationまたは直列implementationへ縮退する。

追加spawnはReady work、uncertainty、WIP、provider/host resource、human review、CI/external wait、retry/stale率、回収costを見て判断する。idle capacityだけを理由にworkを分割しない。追加Workerのmarginal valueよりorchestration/integration bottleneckが大きい場合はfan-outを止める。

短命でparent内部に閉じる観測・探索helperは、project-localでexternal routeが指定されていなければnative subagentを使用できる。独立lifecycle / mutable ownership / background continuity / provider separation / budget isolation / human attach、またはrole-specific external routeが必要ならtop-level Workerへ昇格する。起動前にroleのrouteをresolveし、実際のharness/providerがそのrouteに一致するようpreflight/permissionで保証する。Herdrを使う具体mappingと参照実装は `herdr-runtime` と `templates/agent-routing/` に従う。

fan-in時はtask/attempt/base/fencing/result identityとapplicable evidenceを確認する。複数agentの同意だけをcorrectness evidenceにしない。

## Capacity / delivery-estimation coupling

scheduleやroadmapを理由にWIP / spawn数 / agent数を増減する場合は、`agent-delivery-estimation` Skillを参照する。

orchestration側から少なくとも次の観測可能情報を提供する。

- active agent count / WIP
- Ready / blocked / stack-ready node数
- task type / risk / Work Unit when calibrated
- retry / reassignment / generation change
- blocked duration
- human-review queue
- CI / integration wait
- usage-limit / provider resource constraint

agent数増加を線形speedupとみなさない。task mixやhuman/CI bottleneckが異なる期間のthroughput差をagent数の因果効果と断定しない。

estimate達成のためにisolation、snapshot/result、fencing identity、WIP/resource safetyを弱めてはならない。安全なorchestration invariantはforecastより優先する。

## Dependency readiness

nodeは次のどちらかを満たす場合にspawn可能:

1. unfinished prerequisiteがない
2. hard predecessorが未mergeでも、reviewable immutable predecessor snapshotがあり `stack-ready` と判定できる

`stack-ready` で開始する場合、worker inputへpredecessor Issue/PR identityとexact commit SHA / immutable snapshotを記録する。

predecessorが後から変更された場合はaffected downstream task/branchをstaleとして扱い、base reconciliationとrequired revalidationを行う。

## Flow

1. Issueのobjective / acceptance criteria / dependency / target releaseを読む。
2. `policy-evaluation` に従ってexecution profileを判定し、fan-out / reviewer強度を決める。
3. canonical Issue dependency graphからtask graphを作る。
4. linear hard dependency segmentでstacked PRが適切かを判断する。
5. 各nodeのinput snapshot / predecessor snapshot / output contract / recovery boundaryを決める。
6. Supervisorがdurable taskへcurrent fencing identity（current defaultでは `execution_generation`）と実行policyを割り当ててspawnする。
7. Readyまたはstack-readyなnodeをWIP/resource制約内でspawnする。
8. durable ticket branchをworker/subagentが作る場合、first meaningful commitをcanonical remoteへpublishし、remote head SHA一致を確認した直後にPRを作成する。active/incompleteならDraft、readiness条件を満たしていればReady for reviewとし、published commit + PRなしでactive implementationを継続しない。
9. meaningful boundaryでcheckpointする。
10. worker resultをinspectし、applicableなcurrent fencing identityとbase snapshotがcurrent expected stateに一致することを確認する。
11. Coordinator/Supervisorだけがshared durable integration stateへ順序立てて統合する。
12. integration checkpointごとにrequired validationを行う。
13. predecessor変更でupstack/downstream branchが更新された場合、affected validationを再実行する。
14. Reviewerをclean candidate snapshotから起動する。cross-boundary / judgment-heavy workではbuilderのprivate reasoningではなくobjective / rubric / artifact / validation evidenceを渡すindependent cold reviewを必須とする。
15. GitHub Issue / Project / PR metadataを実行状態と同期する。

## Spawn contract

observational workerはobjective / scope / authority / expected evidenceの最小contractでよい。mutable workerでは次を基準とし、durable workerではfencing / recovery fieldsを必須化する。

mutable workerの最低限input:

```text
issue_or_task_id
objective
acceptance_criteria
target_release
base_snapshot
predecessor_issue_or_pr
predecessor_snapshot
immediate_pr_base
branch_identity
expected_pr_identity_and_state
assignee_expectation
reviewer_expectation
label_expectation
fencing_identity_or_execution_generation
role
attempt_class
allowed_tools
filesystem_policy
network_policy
budget
expected_result
```

durable workerでは上記に加えて、`recovery_boundary`、durable checkpoint/evidence reference、durable discoverability metadataを必須とする。resume/recovery時は`checkpoint_sha_or_snapshot`も必須とする。

dependency / durable GitHub deliveryを使わない短命taskでは該当しないfieldはnull/omittedでよい。

### Requirement provenance

複雑・長期・多段委譲とChatGPT等による着手・再開・監督指示の作成では [canonical requirement continuity](references/requirement-continuity.md) を適用する。正本・版の参照、検証stageと受入条件の照合を省略しない。

`budget` にはresource / cost / timeoutに加えて、childがさらにspawnできる深さと数の上限を含める。上限のないrecursive spawn（fork bomb）やunbounded costを作らない。

`filesystem_policy` / `network_policy` はSupervisorが実際にenforceする境界を表す。policy enforcementが別のruntime/provider設定で行われる場合も、spawn contractにはそのpolicy IDまたは解決済みpolicyを記録し、worker inputと実際のsandbox制約が追跡可能でなければならない。

## Durable branch contract

worker/subagentへdurable branch作成権限を与える場合、その権限はremote publication + PR state lifecycleとセットで扱う。

canonical sequence:

1. branch作成
2. first meaningful commit
3. canonical remoteへcommitをpublish
4. remote branch head SHAがfirst meaningful commit SHAと一致することを確認
5. immediate PR creation with state matching actual work
6. Issue linkage / assignee / reviewer / labels / target release / stack contextを設定
7. implementation継続

GitHub上のPRはremoteでheadを解決でき、head/baseに差分がある必要があるため、branch作成・first commit・remote publication・remote head検証・PR creation/state設定を1つのoperational start procedureとして扱う。

workerがremote publishまたはPR mutation権限を持たない場合、first meaningful commit後ただちにSupervisor/Coordinatorへcontrolを返す。Supervisor/Coordinatorがcommitをpublishし、remote head SHA一致を確認し、PR作成/state設定を完了するまでそのdurable branchでの追加implementationを進めない。

Ephemeral immutable ref/resultはこのcontractの対象外。

## Result contract

observational resultはsource mutationを含まず、evidence provenanceと対象artifact identityを返す。mutable/durable workerは次を基準とする。

mutable workerの最低限output:

```text
agent_id
issue_or_task_id
target_release
base_snapshot
predecessor_snapshot
fencing_identity_or_execution_generation
attempt_class
result_commit_or_ref
pr_identity (PR設定完了後は必須。それ以前の権限不足handoffではnull/omitted)
pr_state (PR設定完了後は必須。それ以前の権限不足handoffではnull/omitted)
summary
validation_results
known_issues
```

durable workerでは上記に加えて、`checkpoint_sha_or_snapshot`、`status`、`completed_steps`、`next_steps`、`pending_validation`、`external_side_effects`、`artifact_refs`、`updated_at`を含むrecovery handoffを必須とする。GitHub/branch deliveryの場合はpublished remote head、PR identityと実際のstate（Draft / Ready）、Issue/branch metadataも必須とする。

applicableなcurrent fencing identity（current implementationでは `execution_generation`）と一致しないresultは自動統合しない。

recorded predecessor/base snapshotとcurrent expected baseが異なるresultはstale candidateとしてreconcileし、盲目的に統合しない。

## Landing handoff boundary

worker / subagent の **shared durable integration state への ordered landing**（`release-x-y-z` への ticket landing、`release-x-y-z -> main` release PR merge、`main` への直接反映等）は **Coordinator / Supervisor だけが実行する**。

- worker / subagent は target release trunk / `main` への merge / landing 操作を実行せず、PR creation/state・remote publication・branch head verify・validationまで完了したcandidateをimmutable handoffする。
- **ticket-class** candidateはreadiness/quality gateを満たせば追加のuser merge authorizationなしでCoordinator / Supervisorがdependency順にlandingする。
- **release-class** `release-* -> main` candidateはexplicit user authorizationが必要で、authorization scopeをhandoff artifactへ含める。
- Coordinator / Supervisorはlanding直前にactual head/base/current SHAを再取得し、ticket/release classificationとrequired gateを再検証する。

この境界を越えて worker / subagent が landing 操作を実行した場合:

- 直近 landing は stale candidate として扱う。
- 自動rollback は前提としない。integration state への影響と reconciliation 必要性を Supervisor が reassess し、必要なら new landing 候補で再実行する。

standaloneでticket PRを扱うAgentはreadiness/quality gate通過後に自律landingできる。standaloneでrelease PRを扱うAgentはexplicit release authorizationがある場合に限り直接landingできる。

## Review handoff

Reviewer inputはclean candidate snapshotへpinする。

Reviewerが見るのは、requested scopeの網羅、decision precedenceとの整合、correctness / architecture consistency、regression risk、required verification levelに対するtest adequacy、validation evidenceがcurrent SHAのものか、hidden coupling、sandbox / runtimeでの再現性、target release / stack predecessorとの整合、PR metadataとIssue linkageの整合、関係する場合はrecovery / checkpointとの整合である。

PR review contextには最低限:

- linked Issue / acceptance criteria
- target release
- immediate stack predecessor if any
- current head SHA
- validation evidence for that SHA
- known blockers
- expected reviewer/CODEOWNERS context

review後にhead SHAが変わった場合、古いapproval/validationがcurrent policy上有効かを再評価する。

## Parent failure

parent agentが停止してもsafeなchildを自動破棄しない。

recovered CoordinatorはSupervisorからchildを再発見し、running/completed/failed/orphanedをreconcileする。completed resultはimmutable snapshot/result relationship、predecessor/base identity、applicableなcurrent fencing identityを確認してから統合する。

Recovery時のticket/PR/release整合とdrift修復は [handoff continuity](references/requirement-continuity.md#recovery-lifecycle) と `github-delivery` に従う。

## Fallback

isolated sandbox同士なら同じfileを触ること自体は直列化の理由にならない。直列化やdependencyが必要なのは、same interfaceの非互換変更、same generated artifact、same external mutable resourceを扱う場合である。

true isolationが使えない場合、shared mutable workspaceで並列実装しない。read-only researchの並列化または安全な直列実装へ縮退する。

stacked PRを安全に維持できない場合もdependency SoTを壊さず、predecessor merge後に通常ticketとして開始する直列workflowへ縮退する。

## Organizational outcome checks

orchestrationのqualityはfan-out数や特定Supervisor APIではなく、次のoutcomeで確認する。

- concurrent workersが互いのmutable stateを無調停に破壊しない
- task / attempt / result identityをretry/recovery後も取り違えない
- completed resultのevidenceがcurrent artifactへbindされる
- parent/worker loss後もdurable stateからreconcileできる
- dependency/authorityを無視して速さだけを最大化しない
- orchestration overheadがtask価値を上回る場合はsolo executionへ縮退できる

current Supervisor / execution_generation / Worktrunk shapeはこれらを満たす現在のimplementationであり、永続的なAPI contractではない。
