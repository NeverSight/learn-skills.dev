---
name: quality-gate
description: project固有のstack・framework・runtimeに合わせてquality gateと動作確認レベルを設計・実行・更新する時に使用する。
metadata:
  requires-skills: system-quality
---

# Quality Gate

## 全体品質との接続

[system-quality](../system-quality/SKILL.md) が扱う要求保存、アンチケース排除、改善比較をproject-local gateへ接続する。必要解析と自前コード・script・設定・Skillの適用範囲を照合し、無分類・未実行を成功にしない。違反混入は固有診断による拒否を確認し、crashやtimeoutは検出成功にしない。検査・抑制・対象除外・期待値の変更は信頼された比較元と照合する。候補自身がgateを変更・迂回できるなら独立強制は未成立である。

要求充足、既知違反の排除、実証された改善の取込みを区別する。必須の未成立条件や実証された劣位を残して完了にしない。検査合格は最適性の証明ではない。検査の実行段階は既存のstage契約に従い、早期検証とrelease検証を混同しない。

quality gateは固定bundleではない。

**何をcheckするか、どのtest levelまで要求するかを、projectの実stack、framework/runtimeのcurrent official guidance、変更surface、release riskからcompileする。**

このSkillは通常taskのvalidationだけでなく、初期化時にquality infrastructureそのものを設計・導入・修復する責務を持つ。

## 1. Initialization / recompile

初回 `/init`、major framework/runtime upgrade、test architecture変更、CI/CD変更時はquality profileを再設計する。

実repoから検出:

- languages / frameworks / SDKs / versions
- package/workspace structure
- app type: web / API / CLI / desktop / mobile / library / IaC
- architecture boundaries
- persistence / queue / cache / external services
- auth / network / filesystem boundaries
- existing test/lint/type/build scripts
- generated-code boundary
- browser / OS / CPU architecture targets
- release/deploy target
- GitHub PR topology: independent / stacked / release trunk

次に実versionに対応するcurrent official documentationを調査する。

優先順位:

1. framework/runtime/SDK official quality/testing guidance
2. official examples/templates/starters
3. official first-party Actions / CI examples
4. official language/toolchain guidance
5. coherent existing project configuration
6. established maintained ecosystem tooling
7. custom tooling

存在しない「公式推奨」を捏造しない。

## 2. Verification taxonomy

project固有profileへ最低限、必要なtest levelの意味を定義する。

名称はframework慣習に合わせて変更できるが、責務を混同しない。

### Unit test

**1つの小さいlogic/component/moduleのbehaviorを、外部boundaryを最小化して高速に検証する。**

主な対象:

- pure/domain logic
- parser / validator / scheduler / algorithm
- state transition
- isolated component behavior
- error handling branch

目的:

- logic regressionを局所的・高速に検出
- failure locationを狭くする

unit testだけでDB/API/runtime wiringの正しさを証明しない。

### Smoke / connectivity test（疎通テスト）

**systemまたは主要serviceが起動し、主要boundaryが最低限接続可能で、critical pathの入口が成立することを安価に検証する。**

主な対象:

- process/service startup
- health/readiness endpoint
- application -> DB connection
- application -> cache/queue connection
- frontend -> API basic request
- required migration/schema availability
- desktop/mobile app launch
- packaged artifact startup

疎通testはdeep behavior correctnessではなく「配線が成立しているか」を見る。

unit/integration testがgreenでも、設定・DI・port・env・migration・packagingが壊れていればsmoke testで落とす。

### Integration test（結合テスト）

**2つ以上のreal boundary/componentを組み合わせ、interface・data flow・transaction等が実際に成立することを検証する。**

主な対象:

- API + service + database
- repository + real/test DB
- queue producer + consumer
- auth middleware + endpoint
- filesystem/network adapter + domain
- frontend data layer + API contract
- migration + application read/write

mockだけでboundary contractを再現したtestをreal integration testと偽らない。

外部SaaSはsandbox/test double/contract testを選択できるが、何をrealに検証しているか明示する。

### Contract / schema test

projectに意味がある場合は独立levelとして使う。

対象:

- OpenAPI / GraphQL / protobuf
- DB schema compatibility
- event/message schema
- generated client/server compatibility
- public SDK/API contract

### E2E / system test

**user-visibleまたはsystem-level critical flowを、productionに近い境界構成でend-to-endに検証する。**

主な対象:

- sign-in -> operation -> persistence -> rendered result
- purchase/scheduling/upload等のcritical journey
- browser/native interaction
- cross-service workflow
- release-like environment smoke + critical scenarios

E2Eですべてのedge caseを網羅しない。slow/flakyなE2Eでunit/integrationの責務を代替しない。

### Manual / visual verification

UI/UX、native platform、hardware integration等でautomationが十分でない場合のみ明示的gateとして定義する。

manual verificationを暗黙の「見た感じOK」にしない。手順・期待結果・artifactを残す。

UI/native変更で人間レビューが必要な場合は [visual/native review handoff](references/visual-review-handoff.md) に従う。非視覚taskへ一律適用しない。

複数OSで動作する対象は [execution placement](../../organization/execution-placement.md) を適用し、実OS/deviceで検証する。WSL/Windows/macOSは互換ではない。

### Verification Executor / native environment

verificationはimplementation workerと同じworkspace topologyを必須にしない。ADR-0020に従い、検証対象をimmutable candidate identityへpinし、environment identityとevidence provenanceを記録する。

最低限のevidence shape:

```text
candidate_identity
environment_identity
procedure_or_command
observed_result
evidence_artifacts
source_mutation_observed
```

Windows-native、macOS-native、GUI application、physical device、installed build、CI runner等のsingleton environmentは、必要ならexclusive lease / serializationで安全に使用する。worktreeを作れないこと自体をverification skip理由にしない。

unexpectedなtracked source/config mutationが確認されたvalidationは、current candidateのclean evidenceとして扱わずreconcile/re-runする。

## 3. 動作確認ゲートを変更riskから決める

全ticketに全test levelを機械的に要求しない。

変更前に最低限判定する:

- 変更したlogic
- 変更したboundary
- runtime/configuration変更
- persistence/schema変更
- user-visible flow変更
- deployment/package変更
- security-sensitive path変更
- failure時のimpact

代表的なdefault:

| Change | Minimum verification candidate |
| --- | --- |
| pure/domain logic | unit |
| API/service behavior | unit + integration |
| DB query/schema/migration | integration + migration/schema check + smoke |
| runtime/env/DI/network wiring | smoke + relevant integration |
| frontend component local behavior | unit/component |
| user journey/navigation/auth | integration/contract + E2E |
| external API adapter | unit + contract/integration + failure-path test |
| build/package/container | build/package + smoke |
| frozen release candidate | full applicable integration + critical E2E/smoke + release-specific checks |
| security fix | regression test + vulnerable-path verification + applicable integration/E2E + affected `security-audit` coverage revalidation when applicable |

これはfixed universal matrixではない。framework official guidanceとproject architectureでcompileする。詳細: [stage placement](references/verification-stage-placement.md)（ADR-0036）。

## 4. Quality profileをproject-localにcompileする

通常taskで毎回再調査しなくて済むよう、**再現可能なcanonical quality profileをrepository-controlled stateとして必ず保存する。**

profileはproject conventionsに合う場所へ置く。標準候補は `quality/profile.yaml`、`quality/profile.json`、または同等のmachine-readable project-local configとし、既存のcanonical configがある場合はそれを再利用する。

profileには最低限:

- `schema_version`
- profile version / updated-at or source revision
- detected framework/runtime/SDK versions
- official guidance source referencesと確認時点
- test taxonomyとproject内の具体例
- change-type -> required verification mapping
- fast worker gate
- ticket integration gate
- stack reconciliation/revalidation policy
- release gate
- canonical validation entry points
- configured CI checks when present
- coverage policy when meaningful
- browser/device/OS/architecture matrix
- native/device/GUI verificationのcandidate materializationとenvironment ownership policy
- CI trigger semantics (`pull_request` / `push` / schedule / dispatch / comment/review event)
- runner policyとplatform matrixの起動条件
- expensive/native/platform-specific gateの適用条件
- concurrency / cancellation / timeout policy
- artifact/report pathsとretention policy
- repository visibility / included usage / billing modelを踏まえたCI resource policy
- expected CI usage/cost modelまたはbudget guardrail（意味があるprojectのみ）
- failure policy

を持たせる。

worker / integration / releaseの各gateには、agentとCIが同じsemanticsで呼べるstable deterministic entry pointを**必須**で定義する。

例:

```text
validate:fast
validate:integration
validate:release
```

実command名はproject conventionに合わせる。

例外として、platform制約等で1つのlocal commandへ完全統合できない場合は、profileにその適用条件・runner/platform・required evidenceを明示し、agent/CIが別々の暗黙gateを選ばないようにする。

## 4.1 Semantic validation evidence verification

commit / PRのcombined statusが `success` であることだけをquality gate成功の証拠にしない。

repository policy / quality profileは、release・ticket・runtime等の各candidateに対して **どのvalidationがapplicableか** をmachine-readableまたは一意に判定可能な形で持つ。validation identityはlocal deterministic commandでもCI job/checkでもよく、CIの存在や成功を全project共通の必須条件にはしない。

CI/checkが存在する場合は最低限、次を確認する:

- check context / job名がcandidate SHA上に実在する
- checkが検証対象のcurrent SHA / current PR headを対象としている
- known failureを無視していない
- skipped / neutral / cancelled / unrelated bot successをapplicable validationの代替にしない
- 同名checkでも別workflow / 別event semanticsなら誤同定しない
- Draftのためreviewをskipしたbot status等をrelease validation成功として数えない
- current SHAへ更新後、staleな以前のgreenを再利用しない

**validation implementation exists** と **branch protection enforcement** は別invariantとして扱う。

ADR-0016のdefault `main` protectionではfixed required status checksを設定しない。workflowやdeterministic gateが存在しても、それをrulesetのrequired statusへ自動登録しない。repositoryが明示的に安定したrequired status checkを採用する場合だけ、quality profileにそのidentityと適用範囲を記録する。

release-source制約は架空のrequired checkで補わず、merge executor / release automationが `base == main` のとき `head == current release-*` を検証する。

## 5. 調査だけで終わらず実装する

初期化完了とはrecommendation reportを書くことではない。

必要なら実際に追加・修復する:

- formatter / linter / static-analysis config
- compiler / type-check config
- unit/component test infrastructure
- smoke/connectivity test infrastructure
- integration/contract/E2E infrastructure
- framework/platform-specific validation
- documentation tests
- dependency/static analysis
- coverage configuration
- schema/migration validation
- browser/device/OS/architecture matrices
- production build/package checks
- code/dependency/security checks
- project-local specialized Agent Skills
- `.github/workflows/*`
- required CI check structure

既存の高品質な構成を理由なく置換しない。

## 6. Framework-native checksを優先する

一般toolを機械的に追加する前にframework/runtimeの標準checkを確認する。

同じ責務のtoolを重複導入しない。

frameworkが特定領域をE2E/real runtimeで検証することを推奨する等、test levelにofficial constraintがある場合はgateへ反映する。

## 7. Agent Skills / toolingもstack-awareにする

必要なspecialized workflowについてofficial / maintained Agent Skills、CLI、LSP、plugin、MCP等を調査する。

優先:

1. existing deterministic project command
2. framework/runtime official CLI
3. short project-local Skill wrapping deterministic tools
4. native agent capability
5. 明確な優位があるplugin/MCP

## 7.1 Delivery-estimation integration

`agent-delivery-estimation` がdelivery forecastを行う場合、quality gateは次の観測値を提供できる形にする。

- validation level / required gate
- CI started/completed duration
- queue / retry / failure
- E2E / manual verification wait
- release-only validation cost
- current-SHA revalidationによる追加round

これらはforecast inputであり、estimateを短縮するためにrequired gateを削除・skip・弱体化してはならない。
delivery forecastはquality requirementへ従い、逆にquality requirementをforecastへ合わせない。

## 8. GitHub Actions / CI resource efficiency

GitHub Actionsを使用するprojectではlocal gateとCI gateを同じsemanticsへ揃える。

**CI resource efficiencyもquality invariantとして扱う。品質を落としてActionsを節約するのではなく、同じverification signalを必要な境界で一度だけ実行する。**

初期化時とCI/CD変更時にcurrent official GitHub Actions guidance、billing/usage model、framework/runtime公式CI exampleを確認する。GitHub Actionsのrunner価格、included usage、rounding、public/privateの扱い等は変化し得るため、固定価格をpolicyへ埋め込まない。

### 8.1 実測してから最適化する

workflow run回数だけでcostやquota消費を判断しない。

最低限、次を使ってactual usageを評価する:

- repository visibility
- workflow / event / branch
- job count
- runner label / OS / architecture
- job started/completed timeまたはbillable duration
- success / failure / cancelled / skipped
- 同一commit/SHAに対する重複run
- artifact / cache usage when relevant
- billing/usage画面または利用可能なusage API

基本モデルは次で考える:

```text
expected CI usage ≈ trigger frequency × started jobs × billed duration × runner cost/weight
```

単なる `workflow runs = N` をusage量として報告しない。

### 8.2 trigger duplicationを避ける

同じvalidationを同じcommitに対して意味なく `push` と `pull_request` の両方で実行しない。

通常のdefault:

- ticket/feature branch: `pull_request` でintegration gate
- `main` / tag: post-merge確認。release trunk pushは軽量health、full release gateはfreeze後に実行
- manual deep verification: `workflow_dispatch`
- periodic verificationに実際の意味がある場合のみ `schedule`

`push.branches: ['**']` + `pull_request` のような構成を、同じfull CIを二重起動するdefaultにしない。

両eventが必要な場合は、それぞれ異なる責務を持つことをprofileへ明示する。

stacked PRでも同じ原則を適用し、immediate predecessorへのPR validationとbranch push validationを無意味に重複させない。

### 8.3 fast PR gateとexpensive platform gateを分離する

通常PRのfeedback loopでは、変更surfaceを十分検証できる最小のrepresentative gateを優先する。

Windows/macOS/native/device/browser matrix等のexpensive platform verificationは削除せず、必要条件へ移す。

代表的な起動条件:

- platform/native関連pathが変更された
- platform-specific behavior / packaging / process invocationが変更された
- frozen release candidate / tag
- explicit label / manual dispatchによるfull verification
- required compatibility matrixを定期的に再確認する必要がある

platform-specific defect riskが常に高いprojectではPRごとのmatrixを維持してよい。その場合もcostを認識した明示的decisionとしてprofileへ記録する。

### 8.4 expensive jobはrunner allocation前にgateする

高コストjobを起動してからstep内で「対象変更ではない」と判定して終了する設計を避ける。

可能なら次を使い、runnerを必要としない段階またはjob start前に不要実行を除外する:

- workflow `paths` / `paths-ignore`
- event / branch filter
- job-level `if`
- lightweight preflight jobからのoutputを使ったdependent expensive jobの条件分岐

ただしpreflight自体のminimum billing/latencyも考慮し、単純なpath filterで十分なら余計なjobを増やさない。

### 8.5 comment/review-driven automationを事前filterする

`issue_comment`、`pull_request_review_comment`、`pull_request_review` 等でAI assistantやautomationを起動する場合、すべてのcomment/review eventでrunnerを確保し、action step内部のtrigger phrase判定だけに依存してはいけない。

可能ならjob-level条件で最低限:

- explicit trigger phrase / command
- intended event type
- trusted actor / permission条件 when necessary
- bot-generated noiseの除外

を判定してからrunnerを起動する。

### 8.6 superseded CIをcancelする

新commitで価値を失うvalidationには `concurrency` と `cancel-in-progress: true` を原則設定する。

concurrency identityはworkflow + PR identityまたはref等、同一feedback streamを正しく表すものにする。

ただしdeploy、migration、release publish等のside effectを伴うjobは安易に途中cancelしない。idempotency/recovery policyと合わせて個別設計する。

### 8.7 timeoutを明示する

各jobへ実測に基づく `timeout-minutes` を設定する。

通常実行時間に合理的marginを加える。GitHubの大きなdefault timeoutをfailure recovery policyの代わりにしない。

hung process / deadlock / unavailable serviceで数十分〜数時間runnerを保持する状態を防ぐ。

### 8.8 artifact / cacheは目的別に管理する

PR verificationの一時artifactとrelease artifactを同じretention policyにしない。

- CI evidence / debug artifact: 必要な期間だけ短く保持
- release deliverable: release policyに従う
- artifactが不要ならuploadしない
- cacheは実測でbuild/test時間を改善する場合に使う

storage削減とActions minutes削減を混同しない。現在のbottleneckをusage dataから判断する。

### 8.9 CIを削るのではなく境界を再配置する

禁止:

- quota不足を理由にrequired verificationを無断削除する
- native/platform testを単に消してgreenにする
- required verificationをdisableしてusage問題を隠す
- self-hosted runnerへ移せば安全性検討不要とみなす

高コストverificationが必要なら、PR every-commitからrelease gate / change-sensitive gate / manual full gateへ移せないか評価する。

self-hosted runnerを使う場合はActions minutesだけでなく、untrusted code execution、credential exposure、host persistence、availability、maintenance costを含めて判断する。

### 8.10 budgetはlast guardrailにする

private repository等でmetered usageがある場合、必要に応じてaccount/org/repositoryのbudget/alertを設定する。

budgetはworkflow設計の代替ではない。

推奨運用:

1. included usageとactual monthly burnを確認
2. trigger duplication / unnecessary platform jobs / runaway jobsを先に修正
3. optimized baselineを1 billing cycle観測
4.通常利用 + 合理的headroomにbudgetを設定
5. usage spike時は「回数」ではなくrunner/job単位で再計測

### 8.11 反復テストの適応的な頻度制御

初期化・再整備時は既存runnerの差分実行とcacheを優先して調査する。必要であれば、**決定的な任意workerテスト**だけに履歴ベースの頻度減衰をopt-inで導入する（[実装例と適用条件](../../templates/quality/README.md)、ADR-0033）。

検証入力・環境・commandの同一性が不明、または変更・失敗・履歴欠損時は実行する。延期は成功ではない。required worker / integration / CI / release / security / native / deviceのgateは減衰によって省略しない。

quality profileに対象check、入力・環境の識別、最大間隔、強制実行入口、延期結果、測定・撤去条件を残す。状態はworkerごとに隔離し、他の環境へ流用しない。

## 9. Worker gate

workerは担当scopeの高速feedbackを得る。

canonical quality profileのworker entry pointと変更risk mappingからfocused test/checkを選択する。

Worker gateはIntegration gateの代替ではない。

## 10. Ticket integration gate

clean integration candidateで、canonical integration entry pointからticketに必要なverificationを実行する。

PR topologyは固定しない:

- independent ticket: `<issue-number> -> release-x-y-z`
- stacked dependent ticket: `<issue-number> -> <immediate-predecessor-ticket-branch>`

どちらでもticketは共通のtarget release trunkを持つ。

最低限:

- acceptance criteriaに対応するverification
- changed boundaryに必要なticket-applicable focused unit/contract/targeted integration
- formatter/lint/type/static/必要なtargeted build等のapplicable checks
- required CI checks
- current head SHAまたはcurrent head SHA / snapshotにprovenanceで結び付いたimmutable artifact identityとvalidation evidenceの一致
- immediate PR base / target release trunkとのstaleness確認

「all unit tests green」だけをintegration completionにしない。

## 11. Stack reconciliation gate

stack predecessorがreview/rebase/updateで変化した場合、affected downstream branchをdependency orderでreconcileする。

必須:

- previous `validated_sha` とcurrent head SHAを比較
- SHAが変わったdownstream ticketではaffected required verificationを再実行
- old green resultをcurrent headのpassとして流用しない
- configured CI/checksが存在する場合はcurrent headで再評価
- predecessor contract/API/schema変更時はdependent contract/integration testを優先して再評価

単なるbranch ref名ではなくresolved immutable SHAをvalidation identityにする。

## 12. Release gate

`release-x-y-z -> main` 前にcanonical release entry pointからticketより広いrelease-level verificationを行う。

必要に応じて:

- full integration suite
- clean production build/package
- release artifact smoke test
- critical user-journey E2E
- supported browser/device/OS matrix
- migration rehearsal
- packaging/signing/notarization
- deployment/IaC validation
- upgrade/backward-compatibility
- release-like environment smoke

## 13. PR readiness gate

- Issue acceptance criteriaを満たす
- required verification levelを満たす
- configured CI/checksが存在する場合はcurrent SHAで失敗を残していない
- blocking review解消
- known limitationを隠さない
- target release trunk / immediate predecessorとのstaleness確認
- stack update後のaffected revalidation完了
- PR metadata / linked Issueがcurrent delivery stateと一致

このreadiness gateを満たしたopen PRはDraftのまま残さず、速やかにReady for reviewへ遷移する。userからの明示的なReady化指示を待たない。PR作成時点ですでにこのgateを満たしている場合は最初からReadyとして作成し、形式的なDraft -> Ready往復を行わない。Draftはこのgate未達でimplementation/integrationがactiveな場合だけ使用する。

**Readyはticket Doneではない。** ticket-class PRは`github-delivery` / ADR-0027に従ってそのままautonomous landingへ進み、target release trunk到達後のlinked Issue closeとsafe branch cleanupまで完了して初めてticket lifecycleが完遂する。release-classだけはReady後にexplicit release authorization gateで停止する。

## 14. False green禁止

禁止:

- skipped test / `.only`
- blanket ignore/suppression
- ignored exit code / `|| true`
- no-fail option
- CI check disabling
- broad generated-code excuse
- mock-only testをreal integrationと報告
- manual check未実施を「動作確認済み」と報告
- coverage threshold低下や不当exclude
- predecessor変更後にold SHAのgreen resultを流用

## 15. Coverageは固定万能指標にしない

coverageは有用なtestable sourceでproject-specific policyとして利用する。

framework guidance、risk、code type、existing baselineを優先する。

coverageが適切でない領域では別のdeterministic signalへ置き換える。

## 16. Re-evaluation triggers

次の場合はquality profileを再compileする:

- framework/runtime upgrade
- official testing guidance変更
- architecture boundary変更
- new app/platform target
- CI workflow変更
- PR/stack/release integration model変更
- flaky/slow gateが開発速度を阻害
- Actions usage/costが想定baselineから大きく乖離
- included usage / runner billing model / repository visibility変更
- escaped regressionがgateの穴を示した
- release process変更

quality gate自体をversioned project configurationとして扱う。
