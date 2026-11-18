---
name: github-delivery
description: current release-driven Operating ModelをGitHub Issues / Pull Requestsへmaterializeし、release sprint / dependency / review / durable delivery stateを扱う時に使用する。
---

# GitHub Delivery

Layer: **Operating Model + Practice**

このSkillはcurrent release-driven profileのGitHub materializationを定義する。Issue / PR / branch / PR state lifecycleそのものはConstitutionではない。

重要なのは、durable implementation identity、reviewable evidence、canonical consistency、authority boundary、organizational continuityを維持すること。将来別platform/topologyがこれらを同等以上に満たす場合は置換できる。

## Source of Truth

- released source state: `main`
- active sprint/release integration state: `release-x-y-z`
- durable implementation work state: GitHub Issues
- dependency state: GitHub Issue dependency metadata
- release planning / health / portfolio state: Linear Projects / Initiatives
- ticket review/integration: Pull Requests
- transient execution state: Supervisor

`main` はリリース済み・統合済みの安定状態を表す。
通常のticket PRを直接 `main` へ向けない。

## Landing authority boundary

PR landing前にcurrent PRを再取得し、actual head/baseから **ticket-class / release-class** を分類する。

### Ticket-class

- `base != main`
- current ticket/release integration topologyに属する
- 通常はticket branch -> target `release-*`、またはdependent ticket -> immediate predecessor ticket branch

ticket-class PRはper-PR user merge authorizationを要求しない。acceptance criteria、current-SHA validation、blocking review/conversation、staleness等のapplicable readiness/quality gateを満たしreal blockerがなければ、Agent/Coordinatorはready-to-mergeで停止せずlandingまで進める。ただしrelease candidate freeze中は同じrelease trunkへの候補外ticketの自律landingを保留し、実装・reviewは継続できる（ADR-0032）。

standaloneではAgent / subagent / Coordinator / Supervisorがticket landingを実行できる。parallel-orchestration下でshared durable integration stateへのordered landingが必要な場合はCoordinator / Supervisorがlandingを実行し、worker/subagentはvalidated candidateをhandoffする。

### Release-class

- `base == main`
- `head == current release-*`

release-class PRだけはexplicit user authorizationを必要とする。Ready/mergeable、green validation、approval、ticket PRへのstanding autonomous landing authority、genericな `readyなPRをmerge` / `cleanup` / `最後まで進めて` 等からrelease authorizationを推定しない。

release PRはbulk/autonomous ticket landingとauto-mergeから常に除外する。userがcurrent interactionで対象release PRまたは明確なrelease actionをexplicitにauthorizeした場合だけmergeできる。authorization後もcurrent head/base/SHAを再取得し、materialにcandidateが変化していればauthorization applicabilityを再確認する。

`base == main` かつheadがcurrent release branchでないPRはinvalid integration pathとしてlandingを拒否する。

quality gateは「candidateがlanding可能な品質か」を判定する。ticket-classではその成功後に自律landingへ進み、release-classでは別途explicit authorization gateを要求する。ticket authorityをrelease authorityへ伝播させない。

## Pull Request merge method

current release-driven profileでは、GitHub PR landingは **merge commit (`merge`) のみ**（ADR-0018）。repository settingsは `allow_merge_commit=true` / `allow_squash_merge=false` / `allow_rebase_merge=false` へreconcileし、権限不足なら差分をblocker/limitationとして報告する。Agent / automationはmerge APIでmethodを暗黙選択せず `merge` を明示する。

squash merge / rebase mergeは使用しない。branch-local `git rebase` はstack maintenance / conflict解消のbranch mechanicsとして許可する。stack landingがmerge commit semanticsを保証できない場合はordered merge-commit landingへfallbackする。method固定からauthorizationを導出しない。
#### Orchestrated workflow landing boundary

`parallel-orchestration` の execution model 下では、Agent / subagent / worker は **target release integration branch (`release-x-y-z`) や `main` への shared durable integration state への ordered landing を直接実行しない**。landing は Coordinator / Supervisor が durable integration の責務として行う。

- ticket-class candidateはreadiness/quality gate通過後、追加authorizationなしでCoordinator / Supervisorへlanding handoffする。
- release-class candidateはexplicit user authorization scopeもhandoff artifactへ含め、Coordinator / Supervisorはcurrent refs/SHAとauthorization applicabilityを再検証してからlandingする。
- standaloneでrelease PRを扱うAgentは、explicit release authorizationがある場合に限り直接landingできる。

この境界を越えてworker/subagentがshared durable integration stateへlandingした場合、resultはstale candidateとして扱いreconciliationする。

## Main protection / release-only integration

GitHub上で保護機能を利用できるrepositoryでは、`main` をbranch protection / rulesetで保護する。

標準baseline:

- `main`変更にはPull Requestを必須とする
- required approving review countは **0** とし、個人開発で自己approvalを要求しない
- conversation resolutionを必須とし、未解決review conversationを残したままmergeしない
- required status checksは **既定で設定しない**。存在しないCI/check名を推測・固定してmergeを停止させない
- CIが存在する場合はquality evidenceとして確認するが、branch protectionの固定required checkとは分離する
- direct push / direct web edit / force push / deletionを通常運用で許可しない
- normal actor/adminが保護を日常的にbypassする運用を作らない
- `main`への正規delivery pathは current `release-x-y-z -> main` release PRだけとする
- ticket branch / arbitrary branchから`main`へ向いたPRはmerge対象にしない

GitHubの標準branch protection/rulesetではPR head branch patternを直接制約できないため、存在しないrequired status checkを捏造して補わない。source branch制約はproject policy / release automation / merge executorで検証し、`base == main` かつ `head == current release-*` でないPRのmergeを拒否する。既にrepository固有の信頼できるguardが存在する場合は利用できるが、そのcheck名を他projectへ固定継承しない。

readiness reportでは `ruleset enforced` と `merge-executor policy enforced` を区別する。外部guardがない場合、GitHub UIで任意headからのPR mergeを完全に禁止できるとは報告しない。Agentがmerge APIを呼ぶ直前には必ずbase/headを再取得してpreflightする。

初期化時にrepositoryのmain protection/rulesetを実際に確認する。設定変更権限がある場合は上記baselineへ作成・修復し、権限がない場合は差分をblockerとして報告する。

## Weekly planning / adaptive release batching

週次はplanning checkpointであり公開日ではない。1 release train = 1 target version = 1 release branchを維持し、週内の早期release・複数週への持ち越しを許容する（ADR-0032）。

versionは変更の意味・互換性・user指定に従う。major/minor/patchは公開意図から選び、週次境界だけでbumpしない。

canonical format:

`release-<major>-<minor>-<patch>`

release train開始時に`main`からbranchを切る。緊急patchもrelease PRを経由する。候補はscope・公開価値・滞留・変更リスク・release-only実測コストで判定し、PR数だけで決めない。freezeとcarry-overは [adaptive-release-batching.md](./references/adaptive-release-batching.md) に従う。

### Delivery forecast / capacity

1週間はplanning cadenceであり、選んだscopeが必ず1週間で完了するというestimateではない。

release / roadmap / milestoneの完了時期、release date、capacity、carry-over、agent数変更による短縮効果を判断する場合は `agent-delivery-estimation` Skillを使用する。

- IssueのSizeをcalendar durationとして扱わない
- AI自身の「数日・数ヶ月」という主観的estimateをrelease dateの根拠にしない
- dependency graph、Work Unit、observed throughput、human review capacity、CI/external wait、usage limitを使う
- material unknownがある場合は `complete / conditional / unavailable` を維持し、日付を捏造してfieldを埋めない
- sprintごとの実績を次のforecast calibrationへ戻す

## Issue

durable planning unitは原則GitHub Issueにする。

Issueのtitle/bodyは日本語を標準とする。

最低限、該当するものを明示する:

- 目的 / user-visible outcome
- acceptance criteria
- scope / non-scope
- dependency / blocked-by
- priority
- size
- area/component
- target version
- release date
- accountable assignee

短命なresearch/worker subtaskまでIssue化する必要はない。

Issue dependency graphはcanonical dependency SoTであり、Git branch topologyだけでdependencyを表現しない。

## Linear planning control plane

release planning / health / portfolio はLinearへ統一する。GitHub Projectsは標準運用では作成・要求・同期しない。

- GitHub Issues: implementation scope / acceptance criteria / dependency の durable SoT
- GitHub PR: review / integration / validation evidence
- Linear Project / Initiative: release goal / target date / health / portfolio
- Linear Issue: cross-repository blockerやexternal dependencyなどrelease-level coordinationに限定

GitHub IssueをLinear Issueへ全面mirrorしない。詳細は `linear-release-control` Skillに従う。

Dependency execution上は必要に応じて `blocked` / `stack-ready` / `integrated` を区別するが、GitHub ProjectsのStatus fieldを前提にしない。

## Sprint / release cycle

1. 週次planning windowを置き、release intent / scopeとtarget versionを決める。release dateは `agent-delivery-estimation` のevidence-backed forecastまたは外部deadlineと区別する。週次終了自体はpublication triggerにしない。
2. 新しいrelease trainの開始時に `release-x-y-z` branchを `main` から作成する。
3. sprint goalを定義する。
4. Ready ticketを選択する。
5. dependency / stack候補 / capacityを確認する。中長期capacity判断では `agent-delivery-estimation` のcurrent evidence / bottleneck / forecast statusを参照する。
6. ticketごとにnumber-only branchを作る。
7. 最初のmeaningful commitをremoteへpublishし、remote head SHA一致を確認した直後にPRを必ず作成し、metadataとstateを設定する。active/incompleteならDraft、readiness条件を満たしていればReady for reviewとする。
8. isolated workerをdependency/WIP制約内で並行起動する。
9. independent ticketまたはstacked ticketをreviewし、current landing candidateを検証する。
10. ticket/stackをReady + landing可能状態へ持っていく。
11. ticket-class PRをdependency順にmerge commitで自律landingし、target release trunkへの到達を確認する。
12. target release trunkへlandしたticketのlinked Issueを明示的にcloseし、dependent PRをreconcileしたうえでsafeならlanded ticket branchを削除する。
13. repository stateをsweepし、PRなしticket branch / Ready未landing ticket PR / land済みopen Issue / merged後残存ticket branchを修復する。
14. 週次またはproject-local triggerでrelease review（hold/candidate/blocked）。candidateならscope/SHAをfreeze、候補外landingを保留し、current SHAでrelease gateを実行する。候補変更時は再検証し、Linearをreconcileする。
15. explicit release-merge authorizationがなければrelease merge前で停止する。authorizationがある場合だけrelease PRを `merge` methodで `main` へmergeし、merge commit / resulting `main` SHAを確認する。
16. project-local release contractに従い、version tag / GitHub Release / package / deploy / store artifact等のpublication処理を実行する。release PR mergeだけでrelease completeとしない。
17. publication artifactをprovider/APIから再取得し、expected version・expected release SHA・draft/prerelease state・artifact availabilityを検証する。publicationが欠落・stale・別SHAならrelease blockerとして閉じるまで継続する。
18. publication/post-release verification完了後、safeならmerged release branchを削除する。
19. 候補外の未完了ticket/stackは次releaseへ明示的にretarget/rebaseし、dependencyとvalidationをreconcileする。release後はpublication済み `main` を基準に次のrelease trainを開始する。

## Release publication invariant

`release-x-y-z -> main` のrelease PR mergeはintegration完了であり、publication完了そのものではない。

projectごとに「何が存在すればreleasedか」をproject-local release contractとして定義する。対象例:

- semantic version tag
- GitHub Release
- package registry artifact
- deploy / environment promotion
- desktop/mobile installer・store artifact
- checksum / provenance / attestation

最低限のinvariant:

- expected versionとrelease merge commit / release source SHAの対応を固定する
- publication automationは再実行しても安全なidempotent operationにする
- existing tag/artifactがexpected SHAと異なる場合は上書きせずfail closedする
- merge成功を根拠にpublication成功を推定しない
- publish command / workflow successだけで完了せず、provider/APIからartifactを再取得して実在とidentityを確認する
- GitHub Releaseを採用するrepositoryではdraft / prerelease状態もrelease contractに含める
- publicationが人手・権限・store review等に依存する場合は、integration complete / publication pendingを別状態として報告する

post-merge verificationでpublication artifactが存在しない、expected release SHAを指さない、またはrequired artifactが利用不能ならreleaseは未完了として扱う。

## Ticket branch

原則、1 top-level Issueにつき1 durable ticket branchを作る。

canonical format:

`<issue-number>`

例:

- `123`
- `418`
- `1024`

branch名に `issue/` prefix、slug、title、type等を追加しない。

nested workerが返すephemeral immutable ref/commitはこの命名規則の対象外でよい。

## Branch creation and PR creation are one start procedure

**active durable ticket branchにはpublished remote headとPRを必ず持たせ、PR stateを実際の作業状態と一致させる。**

GitHubはremoteで解決できないheadやbaseと差分のないbranchにはPRを作れないため、canonical sequenceは次の通り:

1. durable branchを作成する
2. 最初のmeaningful commitを直ちに作る
3. そのcommitをcanonical remoteへpublishする
4. remote branch head SHAがpublishしたcommit SHAと一致することを確認する
5. PRを直ちに作る。active/incompleteならDraft、readiness条件を満たしていればReady for reviewとする
6. published commit + PRがない状態でactive implementationを継続しない

「後でpushする」「後でPRを作る」は禁止する。

このruleはhuman / Coordinator / implementation worker / subagentのすべてに適用する。
subagentがdurable branchを作る権限を持つ場合、そのsubagent自身がpublish + remote head検証 + PR作成/state設定まで完了する。remote publicationまたはPR mutation権限がないworkerはfirst meaningful commit後ただちにSupervisor/Coordinatorへcontrolを返し、Supervisor/Coordinatorがcommit publication・remote head SHA確認・PR作成/state設定を完了するまで追加implementationを進めない。

Ephemeral immutable worker ref/resultはdurable branchではないため対象外。

## PR metadata is required state

PRはdiffだけではなくdurable work stateである。ただし、durable stateとPR proseを同一視しない。

作成時にrepository evidenceからnative GitHub metadataを評価し、最低限次を設定する。

- linked Issue。number-only ticket branch `<issue-number>` ではPR本文に `Closes #<issue-number>`（cross-repositoryならqualified reference）または同等のnative linked-Issue relationを必須とし、PRから対応Issueを一意に再発見できるようにする。ただしnon-default release trunkへのlandingでは自動closeに依存せず、landing確認後にIssueを明示closeする
- accountable assignee
- reviewer request / CODEOWNERS-derived reviewer
- repositoryで定義済みの適切なlabels
- target release branch
- stacked PRならstack trunk / immediate predecessor / relevant successor context

PR bodyはreviewerがchangeを理解・評価するためのartifactとして書く。必要に応じて次を含める。

- purpose / intended outcome
- implementation summary
- acceptance criteriaまたはその参照
- non-obvious design decision / constraint
- review判断に必要なvalidation evidence
- merge後も意味を持つlimitation / migration / compatibility note

current head SHA、ahead/behind、bot status、branch同期履歴、tool invocation、trial-and-error等を、作業contextに存在するという理由だけでPR bodyへ転写しない。GitHub checks、branch state、review status等のmutable stateはnative surfaceをcanonicalにし、proseへ重複させるのはreader判断に必要な場合だけにする。

ownership、scope、stack position、review requirementが変わった場合はmetadataも更新する。

存在しないlabelを勝手に作る、関係のないreviewerを形式的に指定する、PR author自身を自己reviewerとして埋める、という運用はしない。meaningful reviewer不在をPR bodyへ自動記録せず、それがreview/merge semanticsの理解に必要な場合だけ説明する。

PR title/body/review discussionには `writing-discipline` を適用し、Select -> Compose -> Rereadを経てreader-oriented proseへ整える。

Issue/PR title/body/review discussionは日本語を標準とする。

## Independent ticket PR

hard predecessorを持たないticketはtarget release branchをdirect baseにする。

```text
main
└─ release-x-y-z
   └─ 123
```

PR:

`123 -> release-x-y-z`

## Dependency-aware stacked PR

同一repository・同一target release内でlinear hard dependencyを持つtop-level Issuesはstacked PRを使用してよい。

```text
main
└─ release-x-y-z
   └─ 123
      └─ 124
         └─ 125
```

PR:

- `123 -> release-x-y-z`
- `124 -> 123`
- `125 -> 124`

全ticketはtarget release `release-x-y-z` を共通stack trunkとして持つ。

Stack eligibility:

- same repository
- same target release
- real hard dependency
- stacked segmentがordered chainとして表現可能
- predecessorにreviewable immutable commit/snapshotが存在

Issue dependency graphがbranchする場合、無理に1本のlinear stackへ変換しない。
PR stackはIssue dependency graphのlinear pathをexecution/integration topologyへprojectionしたものにすぎない。

`1 top-level Issue = 1 durable ticket branch = 1 ticket PR` はstackでも維持する。
1 Issueを細切れのdurable PRへ分割するためだけにstackを使わない。

## Stack-ready execution

predecessorがrelease branchへ未mergeでも、reviewable immutable snapshotが存在すればdependent ticketを開始してよい。

開始時に少なくとも以下をpinする:

- predecessor Issue/PR identity
- predecessor commit SHA / immutable snapshot
- common target release
- immediate PR base

predecessor reviewで変更が入った場合、downstreamをdependency orderでrebase/updateし、影響したrequired validationを再実行する。

古いgreen resultを異なるSHAへ流用しない。

## Ready for review

Draftは未完了作業の一時状態である。次の条件をすべて満たしたopen PRは、userの明示指示を待たず速やかにReady for reviewへ移す。PR作成時点ですでに条件を満たす場合は最初からReadyとして作成し、形式的なDraft -> Ready往復を行わない:


- Issue acceptance criteriaを実装済み
- current SHAに対するstage-specific ticket-level integration quality gateを実行済み
- blocking known issueが解消済み、または明示的にscope外
- PR description / assignee / labels / reviewer metadataが現在の実装と一致
- required reviewerをrequest済み。meaningful reviewer不在はreview/merge semanticsへ影響する場合だけreaderに必要な形で説明し、mutable stateとして恒常的にserializeしない
- target release branchまたはimmediate stack predecessorとのstaleness/conflictを処理済み
- predecessor変更によるdownstream revalidationを処理済み

## Ticket landing / Done

IssueのDone条件:

- acceptance criteria satisfied
- current landing candidateに対するapplicable project validationを実行済みで、既知の失敗を残していない
- blocking review / conversation resolved
- release/stack staleness handled
- ticket changesがtarget release trunkへland済み
- linked Issue explicitly closed after successful trunk landing

independent ticketでは通常のticket PR mergeがそのままtarget release trunkへのlandingになる。readiness/quality gateを満たしreal blockerがなければ、追加のuser merge authorizationを待たずmerge commitでlandingする。

GitHub native stacked PR等のplatform featureは実装手段として使えるが、policy semanticsをpreview feature固有の挙動に依存させない。

native stacked PRもticket-classとして自律landingできる。stackはbottom（trunkに最も近いPR）からdependency順に扱い、実際にlandingするcontiguous setの各ticketがacceptance criteria / review / current-SHA validationを満たしていることを確認する。mid-stack PRだけをintermediate predecessor branchへ孤立してmergeしたものをDone boundaryとして扱わない。

native stack landingを使えずordinary nested PRへfallbackする場合、例えば `124 -> 123` の通常mergeはintermediate integrationにすぎない。#124のchangesがtarget `release-x-y-z` へ到達するまでIssue #124をclose/Doneにしない。

contiguous stack groupまたはstack全体を一括landingする場合、含まれるすべてのticketが個別にacceptance criteria / review / current-SHA validationを満たしていることを確認する。landing後に各GitHub Issueを明示的にreconcileする。Linearはticketを全面mirrorしないため、release-level stateだけを必要に応じてreconcileする。

`main`へのmergeをIssue単位のDone条件にはしない。Issue Done boundaryはtarget release trunkである。

GitHubのclosing keywordはdefault branch向けPRでのみ自動closeに使えるため、release trunkへのlanding成功確認後にCoordinatorまたはdelivery automationがIssueを明示的にcloseする。

### Post-landing reconciliation / branch cleanup

target release trunk landing後は次を同じticket operationとして実行する。

1. ticket changesがtarget release branchからreachableであることを確認する
2. linked GitHub Issueをcompletedとして明示closeする
3. downstream/open PRがlanded ticket branchをbase/headとして使用していないか確認する
4. dependencyがあればsurviving baseへretarget/rebaseし、affected validationを再実行する
5. dependencyがなくなったlanded ticket branchをremoteから削除する

Issue closeやbranch cleanupを「後で行う任意housekeeping」にしない。削除権限/APIが利用できない場合はcleanup debtをdurableに残してblocker/limitationとして報告するが、黙ってstale branchを正常状態にしない。

### Repository lifecycle reconciliation

recovery、onboarding、task completion時にremote branch / open+merged PR / Issue stateを突き合わせ、最低限次を修復する。

- meaningful unlanded changesを持つnon-release durable branchにPRがない -> intended Issue/base/stackをrepository evidenceから復元してPRを作成
- Draftだがreadiness gate済み -> Readyへ遷移
- Ready ticket PRにreal blockerがない -> autonomous landing
- target release trunkへland済みだがIssue open -> explicit close
- landed/merged ticket branchが残存 -> dependency確認後delete
- release PRがbulk/autonomous landing候補へ混入 -> 除外

intended baseを安全に復元できない等、本当に解けない場合だけblockerとして残す。

## Release integration

release branchはticketを集約する開発中のintegration lineであり、常時release-readyではない（ADR-0036）。

release branchはrelease train開始時に作成する。GitHubは`main`と差分がない状態ではPRを作れないため、release branchに最初のmeaningful integrated differenceが入った直後にDraft release PRを作成する。zero-diff release branchだけはDraft PR invariantの例外である。

Draft release PRにもassignee / reviewer / labels / release goal / included Issuesを設定し、release期間中維持する。release readiness条件を満たしたらDraftのまま残さずReady for reviewへ遷移する。validationのmutable stateはGitHub checks等のcanonical surfaceで追跡し、PR proseにはrelease判断に必要な意味だけを書く。

release候補を選択しscope/current SHAをfreezeした後、release branch上でfull applicable quality gateを実行する。freeze中の新規ticket landingは禁止し、修正でSHAが変わった場合はapplicable gateを再実行する（[candidate review](./references/adaptive-release-batching.md)）。

release PR:

`release-x-y-z -> main`

最低限:

- release goal
- included Issues/PRs
- breaking changes
- migration notes
- release判断に必要なverification scope / evidence。CIのあるrepositoryではnative checksを正本とし、本文にはreaderが再確認に必要な時だけpointerを置く。CIのないrepositoryでは、検証したSHAと、controlを再実行するcommandを書く
- durable known limitations
- version/release metadata

public repositoryでは`main` protectionにより、このrelease PR以外の経路で`main`を更新できない状態を維持する。

release gate成功はrelease PRをready-to-mergeにするquality evidenceであり、release merge authorizationではない。release PRはbulk/autonomous ticket landingとauto-mergeから除外する。genericなmerge/cleanup/finish指示ではreleaseをmergeしない。current interactionで対象release PR/actionへのexplicit authorizationがなければReadyまで整えて停止し、current head SHA / release gate / blockersを報告する。authorizationがある場合だけ、直前にactual head/base/current SHAを再取得して `base == main` かつ `head == intended current release-*` を確認し、`merge` methodでmergeする。

release PRがmergeされた時点で `main` がそのversionのreleased source stateになる。

release PR merge後もtag / deploy / package / store等のproject-defined actual availabilityを確認し、final Linear Project Update / `Released` checkpointを反映してからLinear ProjectをCompletedへ進める。

## Version / tag-triggered release consistency

versionはSemantic Versioning `MAJOR.MINOR.PATCH` をcanonical formとする。external ecosystem上の明確な理由がない限り省略形式を使わない。

tag pushをpublish/release triggerとして使用するprojectでは、tag versionとauthoritative package/project versionを必ず一致させる。

例:

- tag: `v1.4.2`
- authoritative version: `1.4.2`

release automationは不一致を自動修正して続行せずfailする。

conditional minimum sequence:

1. tag format validation
2. semantic version extraction
3. authoritative version comparison
4. current release SHAに対するfull applicable release gate
5. release build/package
6. successful validation後のみpublish/release

複数release unitを持つprojectではauthoritative version sourceまたはunitごとのversion policyを明示する。

adaptive release branch modelとtag releaseは競合しない。release branch/PRがsource delivery、tag/publishがartifact deliveryに使われる場合、両者が同じintended version/SHAを指すことを検証する。

## Multi-agent integration

- 1 top-level Issue = 1 ticket branch = 1 ticket PRを基本とする。
- independent ticket PR base = target `release-x-y-z`。
- stacked dependent ticket PR base = immediate predecessor ticket branch。
- all stack members share one target release trunk。
- implementation workerはticket branchを複数agentで直接共有しない。
- nested workerはresolved immutable identityへpinされたcommit/ref resultを返す。
- durable branchを作るworker/subagentにはremote publication + PR creation/state / metadata contractも適用する。
- Coordinator/Supervisorだけがorchestrated shared durable integration stateへ順序立てて統合する。
- ticket-class landingはreadiness/quality gate通過後に追加authorizationなしで進める。
- release-class landingだけexplicit user authorizationを要求する。
- merge/landing前にtarget release / predecessor / current validation SHA / actual head+base classificationを確認する。
- Doneへ移す前にactual target release trunk上のlandingを確認し、Issue close + safe branch cleanupまでreconcileする。
- `main` protection/rulesetを上記baselineで初期化・検証し、merge executorはrelease-only main source invariantを確認する。

## Language policy

- Issue title/body: 日本語
- PR title/body/review discussion: 日本語
- internal planning docs: 日本語
- commit message: 英語
- source code: 英語

commit format:

`<work-prefix>: <extremely concise title>`


## Refinement boundary

GitHub delivery topologyを変更する場合、最低限次を維持する。

- durable work identityとdependencyを別actorから再発見できる
- integration candidateとvalidation/review evidenceを対応付けられる
- current/released source stateのcanonical authorityが曖昧にならない
- consequential landingのauthority boundaryが維持される
- interrupted workをconversation historyなしでreconcileできる
- valid workがdelivery ceremonyだけで不必要に停止しない

branch名、PR creation/state timing、release branch cadence等はcurrent profileのdefaultであり、上位guaranteeを満たすalternativeを一律に禁止しない。
