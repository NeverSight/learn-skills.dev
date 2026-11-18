---
name: policy-evaluation
description: Constitution / Operating Model / Practice / Skillがorganizational outcomeとinvariantを維持するかを、formal model・deterministic checks・cold eval・grader controls・context budgetで検証する時に使用する。
metadata:
  requires-skills: system-quality
---

# Policy Evaluation

## 成果物に対する評価

[system-quality](../system-quality/SKILL.md) の排除能力と改善能力を、回答形式とは別に評価する。文言・record検査はその形式だけを保証する。既知違反を含む実コードを実際のgateへ投入し、正当ケースも通ることを確認する。さらに禁止事項を満たすが改善可能な実プロジェクトで、要求保存と改善関係を実行証拠へ対応付ける。cold reviewは補助であり、最適性や強制の代替ではない。

検査器の既知ケース識別、違反クラスの完全性、要求充足、Optimalは別の主張である。suiteやoracleを候補に合わせて弱めず、信頼されたrevisionとの差を審査する。portableな実コードchallengeはsystem-qualityに同梱する。

Organization policyは文章が存在するだけでは完成しない。Constitutional property、current Operating Model、replaceable Practice、Skill judgmentを区別して評価する。

**policyが実行可能なcommand/configへ落ちる部分はdeterministicに検証し、判断を含む部分はfresh agentへcold contextで読ませ、意図したbehaviorを再現できることまで検証する。**

policy changeのquality signalを、作者自身の読み直しや「もっともらしい回答」だけへ依存させない。

## 0. Constitutional outcome gate

policy changeを評価するとき、最初に「指定手順を使ったか」ではなくresulting organizationを確認する。

最低限の観点:

- artifact / attempt / evidence identityが保たれたか
- authorityを持たないactorのdecisionが確定していないか
- stale/partial evidenceがcurrent proofになっていないか
- concurrent mutable ownershipが安全か
- actor/session loss後にdurable stateから継続できるか
- conflicting canonical authorityを作っていないか
- safety mechanismがvalid progressを不必要に止めていないか

tool/command-specific assertionは、そのPractice自体のcontractを評価する場合だけhard requirementにする。

formalizableなconcurrency/recovery/identity propertyは `formal/Organization.tla` のabstract modelも参照する。TLC successをimplementation conformanceの代替にはしない。

## 1. Deterministic space / latent space

変更対象のruleを最初に2つへ分ける。

### Deterministic space

同じrepository stateとinputなら、原則として同じ結果を要求できる領域。

例:

- file / config / link / commandの存在
- naming / schema / metadata constraint
- Git / GitHub stateの整合性
- exact SHA / dependency / branch relationship
- machine-readable policy profile
- document structure
- command snippetの実行可能性
- regression fixtureに対するpass/fail

ここは自然言語推論を毎回やり直さず、script / command / parser / machine-readable checkへ寄せる。

### Latent space

単一の文字列比較では正しさを表現できず、policyを読んだagentの判断・優先順位・状況理解が必要な領域。

例:

- user escalationが必要か
- taskをどう分解するか
- どのquality levelを要求するか
- project evidenceから何をcanonicalと読むか
- ambiguity / risk / trade-offの扱い
- reviewerがartifactをどう評価するか

ここはfresh agentへ必要最小限のpolicyとscenarioだけを渡すcold evalで確認する。

deterministicにできるものをlatent evalへ残さない。逆に、keyword matchingだけでjudgment correctnessを証明したと扱わない。

## 2. Policy change gate

significantなAgent policy / Skill / prompt / routing変更では、変更前に次を判定する。

1. 何のbehaviorを変えるか
2. そのbehaviorのdeterministic部分は何か
3. latent judgmentが残るか
4. 過去に実際に起きたfailure / regressionがあるか
5. fresh agentがcold contextから理解できる必要があるか

次のいずれかに該当する場合、repo-local evalを追加・更新する。

- wordingだけではbehavior preservationを証明できない
- model generation差で解釈が揺れ得る
- safety / delivery / recovery / qualityのcritical invariantを扱う
- 過去に同じruleが誤解・退行した
- 複数Skillの優先順位やroutingに依存する
- deterministic testだけでは「読んで正しく使えるか」を証明できない

小さな誤字修正や意味を変えないrefactorへ無意味なevalを増やさない。

## 3. Cold eval contract

latent evalは作者の会話・実装経緯・期待回答をagentへ漏らさない。

原則:

- fresh agent / fresh contextを使用
- 対象ruleの理解に必要な最小policyだけを渡す
- builderのchain-of-thought、試行錯誤、grader実装を渡さない
- scenarioはactual taskに近い具体例にする
- answer formatを可能な範囲でstructuredにする
- artifact / decision / commands等、外部化可能な結果だけを採点する

評価対象policyを全文promptの他sectionで補ってしまわない。

## 4. Graderは自分自身をcontrolする

graderがanswer keyの表面形だけを数える状態を許容しない。

最低限、次の3 controlを持つ。

### Negative control

典型的だがpolicy上誤っているnaive answer。

必ずFAILしなければならない。

### Regression control

過去に実際に通ってしまった、または実害があったbroken answer / behavior。

表面shapeが正しくてもFAILさせる。

### Positive control

current policyが意図するvalid answer。

必ずPASSしなければならない。

controlが期待通りに分離できないgraderのscoreはquality evidenceとして使用しない。

重要なmust-not / safety invariantは、総合点で相殺させずhard failureにする。

## 5. Eval fixture structure

project conventionがなければ次を候補とする。

```text
evals/
  <policy-area>/
    scenario.md
    grade.sh
    controls.sh
    fixtures/
      positive.*
      negative.*
      regression.*
```

provider-specific eval runnerをcanonical policyへ固定しない。

model invocationはmanual / external runner / CI serviceのいずれでもよいが、scenarioとdeterministic grader / controlsはrepository-controlled stateとして再現可能にする。

## 6. Execution profile

task complexityだけでなく、**必要なexecution behavior**を先に分類する。

標準profile:

### mechanical

- deterministic transformation中心
- 局所変更
- product / architecture judgmentなし
- failure impactが限定的

default:

- solo execution
- deterministic/focused validation
- 不要なfan-outやcriticを起動しない

### localized

- 1つのcomponent / module / document領域
- existing conventionからほぼ決定可能
- limited judgment

default:

- solo implementation
- applicable focused/integration validation
- user-visibleまたはpolicy-sensitiveならcold final read/reviewを追加

### cross-boundary

- API / DB / UI / runtime / multiple docs/Skills等のboundaryを横断
- dependencyやintegration riskあり

default:

- dependency decomposition
- safeなnodeだけparallelize
- integration gate
- completed artifactに対するbuilderと分離したindependent cold reviewを必須とする

### judgment-heavy

- architecture / product semantics / policy interpretation / visual quality / trade-offが中心
- deterministic correctnessだけで完了判定できない

default:

- evidence / reference / acceptance rubricを先に固定
- builderと分離したindependent cold reviewerを必須とする
- completed artifact / diff / immutable snapshotをcold review
- significant decisionをappropriate durable surfaceへ保存

複数profileに該当する場合は、より弱いlabelへ丸めずsafeguardを合成する。特に `cross-boundary` かつ `judgment-heavy` のtaskはdependency decomposition / safe parallelismとevidence/rubric-first executionの両方を適用し、combined routingをorchestration前に記録する。

execution profileはquality taxonomyの代替ではない。

`quality-gate` が「何を検証するか」を決め、execution profileは「どの程度のorchestration / reviewを使うか」を決める。

## 7. Cold artifact review

cross-boundary / judgment-heavy taskでは、completed candidate artifactに対するbuilderと分離したindependent cold reviewをrequired completion gateとし、builder自身の作業記憶だけをfinal quality signalにしない。

reviewerへ原則渡すもの:

- objective / acceptance criteria
- canonical reference / frozen rubric
- completed artifact / diff / immutable snapshot
- applicable validation evidence
- known limitations

原則渡さないもの:

- builderのprivate reasoning
- 採用されなかった案の長い実況
- 「ここは良いはず」等のself-justification

reviewerはartifactをfreshに読み、実際に存在する結果から評価する。

数値self-ratingをquality gateとして要求しない。

## 8. Context budget

progressive disclosureは構造だけでなく、always-loaded context量でも監視する。

このrepositoryでは `bun evals/policy-evaluation/context-budget.mts` をdeterministic regression checkとして実行する。checked-in `evals/policy-evaluation/context-budget-baseline.tsv` とroot instruction files / total always-on instructions / 各conditional `skills/*/SKILL.md` を比較し、各surfaceのbyte growthがbaselineの10%または512 bytesの大きい方を超えた場合はFAILする。outputはmachine-readable TSVとし、intentionalなbaseline更新はreview対象にする。

初期化・policy再構成・root agent fileの大幅変更時に最低限確認する:

- root `AGENTS.md` / `CLAUDE.md` 等のword/byte/token estimate
- always-on instruction全体の概算cost
- conditional Skillごとのsize
- rootでしか成立しないinvariantと、Skillへ遅延できるworkflowの区別
- 同じruleの重複
- large embedded examples / copied docs

固定token上限を全projectへ強制しない。

ただしalways-on contextが増えた場合は、追加分が本当に全taskで必要かをreviewし、conditional workflow / reference / Skillへ移せないか検討する。

context削減のためにcritical invariantを消さない。

## 9. Repeated reasoningのcodification

同じ非自明な判断・手順を繰り返した場合、成功例でもcodification candidateとして扱う。

目安:

- deterministicで安定した処理 -> script / command / config
- judgmentを含む再利用workflow -> Agent Skill
- project-wide invariant / long-lived choice -> policy / ADR
- verification behavior -> quality profile / test / eval
- one-off local choice -> codeだけに留める

failureだけでなく、繰り返し成功しているmanual flowも自動化候補にする。

## 10. Comparative latent evaluation

output style、interaction policy、judgment routing等のlatent behaviorを評価する場合、candidate単独のabsolute scoreだけで改善を主張しない。

baselineとcandidateを比較できる場合は、**同じtask distributionに対するpaired comparative eval**を優先する。

### Condition parity

比較するcondition間で最低限そろえる。

- cases / prompts
- model family / exact model identity when configurable
- effort / sampling等、behaviorへmaterialなgeneration settings
- trial count
- rubric / blocker definition
- tool availability / sandbox / network policy
- provider/runtimeの主要version

conditionごとに異なるtask setやrubricを使ったscoreを直接比較しない。

modelやruntimeを意図的に変えるexperimentでは、その差をindependent variableとして明示し、policy差と混同しない。

### Runner isolation

eval runnerはoperatorのpersonal configurationから可能な限り隔離する。

contamination candidate:

- user-level Agent Skills / plugins
- hooks
- memory / saved instructions
- output style / personality
- local global config
- unrelated MCP / connector
- environment variableによるhidden behavior switch

baselineへcandidate policyがuser-global設定経由で注入される状態を許容しない。

runnerが完全隔離できない場合、そのcontamination riskをresultへ明示する。

### Identity pinning

reproducible comparisonではmodel / CLI / runner identityを固定または記録する。

default modelへ暗黙依存しない。CLI updateやprovider default変更で同じcommandのbehaviorが変わり得るため、published resultには少なくとも次を残す。

- model identity
- runner / CLI version
- cases revision
- rubric revision
- trial count
- policy revision / SHA

### Blind judging

graderがcandidate identityを知る必要がないtaskでは、condition名をblindする。

推奨:

- `baseline` / `candidate` 等をgrader promptへ直接渡さない
- `A` / `B` 等のopaque labelへ置換する
- position biasを避けるためlabel orderをper groupで入れ替える
- resumeしても同じgroupは同じlabel mappingになるdeterministic permutationを使う

release gateやcondition-specific thresholdはblind judgeへ渡さず、scoring後のseparate deterministic stageで適用する。

### Paired judging

同一case / trialのconditionsは可能なら同じjudge callまたは同じevaluation batchで比較し、task difficulty差をcondition差として誤認しない。

candidateだけを別時点・別judge contextで採点してbaseline scoreと比較する場合は、そのcomparability limitationを明示する。

### Release gate

weighted totalだけでrelease判断しない。

最低限:

- blocker finding = hard failure
- correctness / safety等のcritical dimensionはnon-regression constraintを持つ
- overall quality improvementはcritical dimensionを悪化させて相殺しない
- public competitor / baseline comparison claimはcases / model / trials / rubric等が同条件の場合だけ行う

numeric self-ratingはquality evidenceにしない。

### Budget and resumability

paid model evalでは、意図しないrunaway costを避けるためcondition / run単位のbudgetまたはprovider側hard capを持たせる。

long-running evalは、completed `(case, trial, condition, runner)` をdurable resultとして識別し、provider failureやoperator interruption後にcompleted rowsを再実行せずresumeできる形を優先する。

retryはboundedにし、最終provider errorをsilent dropしない。

特定provider API / runnerをcanonical dependencyにはしない。これらはeval harnessのcontractであり、実装はproject/runtimeに合わせる。

## 11. Eval maintenance

次の場合は関連evalを再実行・更新する。

- 対象policy / Skill / prompt / routing変更
- prompt routing / progressive disclosure変更
- model generation変更でbehavior差が疑われる
- grader変更
- 新しいreal regression発見
- control fixtureの前提変更

新しいregressionを修正した場合、可能ならそのbroken behaviorをregression fixtureへ保存する。

fixtureをcurrent answerへ都合よく書き換えてhistoryを消さない。

## 12. Completion evidence

policy change完了時は、該当する範囲で次を示す。

- deterministic checks
- control結果
- latent eval結果と使用したmodel/runtime identity when known
- current policy revision / SHA
- evalで確認できないknown limitation
- `bun evals/policy-evaluation/context-budget.mts` の結果とcontext budgetへの影響
- execution profileの変更有無

latent evalを実行できない環境では、未実施を明示し、deterministic controlsだけでlatent behaviorまで証明したと報告しない。


## 13. Policy decay evaluation

policyは追加だけでなく削除も評価する。

non-constitutional ruleについて、model/tool capabilityやorganization designが変化した場合は次を比較する。

- ruleあり
- ruleなし
- simpler replacement / alternative practice

条件を揃えたcomparative evalでmeaningful outcome差がなく、上位invariantも維持される場合、そのruleをpreserveすること自体をquality goalにしない。

削除candidate:

- original regression/failure modeをcurrent capabilityがinstructionなしで安定回避する
- replacement mechanismが同等以上のguaranteeを提供する
- instructionが上位propertyを重複説明するだけ
- context/coordination costがbenefitを上回る

critical constitutional propertyを「新modelなら賢いはず」という期待だけで削除しない。削除対象はまずOperating Model / Practice / Skillの具体ruleとする。
