---
name: correctness-assurance
description: 重要な不変条件・事前条件・事後条件を抽出し、型・静的解析・runtime assertion・テスト・property/differential testing・formal verification・reviewの中から最小十分な保証手段を設計する時に使用する。
metadata:
  requires-skills: system-quality
---

# Correctness Assurance

## 要求保存と改善の証拠

[system-quality](../system-quality/SKILL.md) の契約に従い、要求充足、候補間の改善、既知欠陥排除、最適性を別々に扱う。実装から期待値を逆算せず、比較候補へ同じ要求と環境条件を適用する。前提強化・入力除外・証明対象縮小は契約変更として元の根拠と照合する。証明は実ソースの意味論との対応が確立した範囲に限る。必要な保証を満たした後に重複を除くのであり、保証範囲を「最小」に縮小しない。

correctness assuranceは、単一の手法で「正しさ」を保証することではない。

**何を正しいと呼ぶのかを性質ごとに分解し、その性質に対して最小十分なassurance mechanismを割り当て、保証できた範囲・保証していない範囲・前提を明示する。**

形式検証を自動的に優先しない。型・静的解析・テスト・runtime check・reviewで十分な性質にproofを持ち込まない。一方で、有限個のテストでは本質的に届かない全称的な性質を「テストが多いから十分」と扱わない。

## 1. いつ使うか

次のいずれかがある場合に使用する。

- 配列添字、範囲、長さ、offset、cursor、partition等の境界条件がある
- sentinel / optional state / partial stateを最終的に解消する必要がある
- state machineで到達不能状態や遷移制約がある
- sort / merge / search / scheduler / parser / allocator等に構造的不変条件がある
- 「事前条件を満たすすべての入力」で成り立ってほしい性質がある
- property-based testや差分テストでも入力空間を有限標本としてしか扱えない
- 破れるとpanic / trap / out-of-bounds / corruption / wrong-stateになる
- 型で責任箇所を狭められるが、そのconstruction function自体の正しさが残る
- runtime semanticsとverification/model semanticsの差がriskになる
- AI生成・変更されるコードに、機械可読なcontractを置く価値がある

次だけを理由に起動しない。

- UIの見た目だけを確認したい
- external API / DB / network wiringだけを確認したい
- product semantics自体がまだ決まっていない
- 重要な性質を具体的なpredicateとして書けない
- formal verification toolを使ってみたいだけ

## 2. 最初に「正しさ」を分解する

実装を見る前に、必要な性質を曖昧な「正しい」から分離する。

最低限、該当するものを列挙する。

### Structure / construction

例:

- この値は特定constructorを通してのみ生成される
- invalid variantを呼び出し側へ渡せない
- schema / shape / enum stateが正しい

主に型・visibility・module boundaryで担保する。

### Range / bounds

例:

- `0 <= index < length`
- offsetがbuffer範囲内
- selected rangeが空間外へ出ない
- integer resultがruntime表現範囲内

型だけで表現できない場合、contract / static analysis / runtime assertion / proofを検討する。

### Totality / completion

例:

- completion後にsentinelが残らない
- `Option` / nullable stateがfinal phaseではすべて解消される
- partial mappingがcompleteになる

「特定関数を通った」と「その関数が本当にcompleteにした」を分ける。

### State transition

例:

- forbidden transitionが存在しない
- terminal stateから通常stateへ戻らない
- event sequenceに対してinvariantが保存される

型、state-machine test、model checking、formal verification等を候補にする。

### Ordering / uniqueness / preservation

例:

- sort後に順序が保たれる
- stable orderingが必要
- keyが重複しない
- length / membership / correspondenceが処理前後で保存される

### Arithmetic / numeric model

例:

- overflowしない
- saturation semanticsを守る
- floating-point orderingの差で結果順序を壊さない
- fixed-width integerと数学整数を混同しない

ここはverification modelとruntime modelの一致確認を必須にする。

### Semantic correctness

例:

- 最適解である
- 推薦結果が正しい
- business rule上正解である
- user intentを満たす

構造的安全性と分離する。「クラッシュしない」を「答えが正しい」に拡張しない。

## 3. Assurance mechanismをproperty単位で選ぶ

各propertyについて、最小十分な手段を選択する。

| Mechanism | 強い領域 | 単独では弱い領域 |
| --- | --- | --- |
| Type system | shape、construction boundary、invalid stateの排除 | collection全体の内容、不変条件、constructor内部の仕事 |
| Static analysis | language/toolがmodelできるdefect class | runtime integration、tool model外 |
| Runtime assertion | 実行したcaseのpre/post condition違反 | 未実行入力への全称保証 |
| Unit test | 局所behavior、境界値、machine semantics | 入力空間全体 |
| Property-based test | 広い入力探索、反例発見 | 全入力保証ではない |
| Differential test | 既存実装との互換性、移植 | oracle自体の誤り、未実行入力 |
| Integration/E2E | real boundaryとsystem behavior | 局所invariantの網羅 |
| Formal verification / model checking | model内の全入力・全状態に対するproperty | specification error、model外のruntime semantics |
| Review | specificationの十分性、意図、assumption妥当性 | 機械的網羅性 |

原則:

> **同じpropertyを複数手法で無意味に重複させるのではなく、異なるfailure classを補完する。**

ただし高risk propertyでは独立な二重化が有効な場合がある。たとえばproofしたpredicateと同義のruntime checkerを別実装で持ち、model/runtimeの食い違いを検出する。

## 4. Assurance mapを作る

実装前または変更前に、対象propertyごとに次を記録する。

```text
Property:
  completion後に未決定sentinelが残らない

Scope:
  事前条件を満たすすべてのmapping input

Mechanism:
  formal verification

Supporting mechanisms:
  runtime checker
  boundary unit tests

Assumptions:
  input length > 0
  first/last entries are assigned
  verification modelのinteger semanticsが対象propertyに十分

Not covered:
  assigned valueが有効な参照添字であること
  floating-point側の候補選択の正しさ
  global optimum
```

**「Aを証明した」からB・Cまで保証したように書かない。**

## 5. Contractを具体的にする

formal verificationを使うかどうかに関係なく、重要なpropertyは可能なら次へ分解する。

- precondition / requires
- postcondition / ensures
- invariant
- frame / preservation property
- termination condition
- model assumption

悪い例:

```text
mapping is valid
```

良い分解:

```text
forall i in [0, map.length):
  map[i] != SENTINEL

forall i in [0, map.length):
  0 <= map[i] < reference.length

result.length == input.length
```

sentinelが消えたことと、有効なindexだけが入っていることは別propertyとして扱う。

## 6. Preconditionをcall chainで閉じる

contractのpreconditionはruntime checkとは限らない。

```text
caller
  ↓ must establish P
function f requires P
  ↓ proves Q
caller uses Q
```

次を確認する。

- preconditionはどこで成立するのか
- 呼び出し側でもproof/static checkされるのか
- runtime validationが必要なのか
- external inputから来る場合、trusted boundaryはどこか
- call chain途中で保証が切れていないか

「functionがproof済み」でも、precondition違反のcallが可能ならその実行は保証外である。

## 7. 検証困難なら先にboundaryを疑う

重要なinvariantが検証しにくい場合、すぐにcontractを弱めない。

次が混在していないか確認する。

- I/O
- mutable shared state
- floating-point decision
- external service
- nondeterminism
- time
- random
- UI/event wiring
- index/range arithmetic
- pure transformation

可能なら、

```text
unverified / environment-dependent layer
        ↓ explicit boundary
small verifiable core
        ↓
unverified / environment-dependent layer
```

へ分離する。

典型例:

- floating-pointで「どれを選ぶか」を決める
- integer coreで「選ばれた位置を安全に扱う」
- external layerで結果をI/Oへ接続する

ただし、**proofの都合だけで不必要なallocation、copy、latency、複雑化を入れる場合は、その設計コストを明示する。**

## 8. Formal verificationを選ぶ基準

次が揃うほど適用価値が高い。

- propertyが明確なpredicateとして書ける
- 全入力・全状態に対する保証が本当に必要
- test enumerationでは本質的に保証できない
- pureまたは副作用が限定されたcoreへ分離できる
- index/range/state/ordering等の構造的property
- failure impactが高い
- solver/modelが必要なlanguage featureを正しく扱える
- proof maintenance costに見合う

適用価値が低い、または先に別手段を選ぶ例:

- specificationが曖昧
- UI appearance
- external integration correctness
- modelが対象featureを表現できない
- rapidly changing exploratory codeでproperty自体が未確定
- unit/property testで十分な局所logic
- proofを通すこと自体が目的化している

## 9. Verification modelとruntime semanticsを照合する

proofの前後で必ずmodel boundaryを確認する。

最低限:

- integerはmathematical integerかfixed-width machine integerか
- overflow / underflowはmodelされるか
- floating-pointはIEEE 754としてmodelされるか、未対応か
- division / modulo / shift semanticsはruntimeと同じか
- pointer / alias / mutation / memory modelは同じか
- concurrency / atomicity / orderingはmodelされるか
- exceptions / panic / trapはmodelされるか
- compiler target差、Wasm/JS/native差があるか
- library / host functionはaxiom扱いか、verified implementationか

例:

```text
proof model: unbounded mathematical Int
runtime: signed 32-bit Int
```

なら、結果範囲のcontractだけでは途中式のoverflow安全性を保証できない場合がある。

**proof greenとmachine-safeを同義にしない。**

## 10. Specification自体をadversarialにreviewする

solverは「書いた仕様」を検証する。必要だった仕様を自動で発見してはくれない。

reviewでは少なくとも次を行う。

### Counterexample challenge

contractを満たすが、実際には受け入れたくない値を探す。

例:

```text
property: value != -1
counterexample: -2
```

この反例が危険なら、必要propertyは `0 <= value < n` のように強化する。

### Vacuity challenge

preconditionが強すぎて、実質的に何も保証していない可能性を確認する。

### Missing-dimension challenge

- safetyだけでlivenessを忘れていないか
- totalityだけでrange validityを忘れていないか
- local correctnessだけでpreservationを忘れていないか
- resultだけでintermediate overflowを忘れていないか

### Oracle challenge

differential testではreference implementation自体を無条件に正しいと扱わない。

## 11. Loop / recursive invariantは必要な性質から逆算する

強いinvariantを大量に入れれば良いわけではない。

まずpostconditionに必要なpropertyを特定し、そのpropertyを各stepで保存できる最小限のinvariantを置く。

例:

```text
post:
  all entries are assigned

loop invariant:
  all entries before cursor are assigned
```

必要以上に値そのものを追うことでsolver costやmaintenance costが増える場合がある。

一方で、弱すぎるinvariantでproofを通すために本来必要なpropertyを削ってはいけない。

## 12. Tool resultの意味を正確に読む

formal toolのstatusを過大解釈しない。

- proved / valid: 指定model・assumption・contractのもとで成立
- invalid / counterexample: propertyが偽であるevidenceになり得る
- timeout / unknown: この設定では結論が出なかっただけ
- unsupported: model外。propertyが正しいとも間違いとも言っていない

timeoutを「バグがある証拠」と扱わない。
proof obligation数を「保証の強さ」のmetricとして使わない。

## 13. Runtime verificationを残す判断

proof済みでもruntime checkやtestを残す価値がある。

残す候補:

- machine integer境界
- floating-point behavior
- compiler/backend差
- Wasm/JS/native差
- serialization
- FFI
- generated code
- host API
- unsafe code
- proof modelで抽象化したboundary
- contractと同義のindependent runtime checker

contractがcompile artifactへ残らないtoolでは、必要ならruntime safety checkを別途設計する。

## 14. Evidence

assuranceの結果は最低限次で報告する。

**既知のmodel gapが存在する場合、`Known model gaps`項目に必ず記載する。** gapがないと確認できる場合のみ「なし」と明記する。

```text
Correctness properties
- P1: ...
- P2: ...

Verified / assured
- P1: formal proof, tool/version, result
- P2: type-level construction boundary

Runtime-tested
- integer boundary cases
- differential compatibility
- target backend behavior

Assumptions
- ...
- ...

Not verified
- ...
- ...

Known model gaps
- ...
- ...

Evidence
- command
- artifact
- commit/SHA
- toolchain/version
```

「tests green」「proof green」だけで終了しない。

## 15. Reproducibility

proof/toolingをCIやteamで使う場合は、通常のtest toolchainと同じく再現可能にする。

- compiler/tool version
- verifier / SMT solver / model checker version
- solver strategy/configuration
- timeout/resource limit
- architecture差
- package/lock/Nix/container等のenvironment definition

solver versionやstrategy差で結果が変わり得る場合は、current working environmentを固定する。

## 16. AI agent向けルール

AIにcontract・invariant・proof annotationを書かせることはできるが、生成されたcontractを意図の代わりにしない。

AI agentは:

1. 先にpropertyを自然言語とpredicateの両方で述べる
2. implementationから都合の良いpostconditionを逆算しない
3. counterexampleを最低1回探す
4. model/runtime差を確認する
5. proofを通すためだけにpreconditionを強めない
6. unsupported領域を隠さない
7. verified / Not verified / assumptionsを分離する
8. contract変更をbehavior変更と同じくreview対象にする

contractはAIにとってもmachine-readable specificationとして扱う。

## 17. Anti-patterns

禁止:

- 「formal verification済み」だけでprogram全体の正しさを主張する
- test件数の多さから全入力保証を推論する
- proof greenをruntime overflow安全性へ自動拡張する
- sentinel absenceをindex validityと同一視する
- timeoutをfailure/counterexampleとみなす
- type-safeだからcollection invariantも成立するとみなす
- abstract type constructorを通ったからconstructor内部も正しいとみなす
- proofを通すために必要なpropertyを弱める
- preconditionを呼び出し側で成立させずに利用する
- modelで扱えない部分を「証明済み範囲」に含める
- generated proof obligation数をquality KPIにする
- testをproofで置換する
- proofを理由にreviewを省略する

## 18. Completion gate

このSkillを適用したtaskは、少なくとも次を満たして終了する。

- correctness-critical propertyが列挙されている
- 各propertyのassurance mechanismが決まっている
- mechanism選択理由がpropertyの性質とriskに対応している
- 必要なpre/post/invariantが具体化されている
- preconditionの成立元が追跡できる
- verification modelとruntime modelの差を確認した
- formal verificationを使う場合、unsupported領域を明示した
- specificationへcounterexample challengeを行った
- verified / runtime-tested / assumptions / Not verifiedを分離した
- Known model gapsを明示している
- evidenceがcurrent code revisionへ紐づいている

## 19. Source case

このSkillの初期設計では、MoonBitで実プロダクトの整数部分をSMT solverで検証した次の記事を重要なcase studyとして使用した。

- Mates Engineering: [アルゴリズムの実装に MoonBit の Formal Verification を活用する](https://eng.mates.education/blog/b-moonbit-formal-verification/)

case studyから一般化した主な点:

- 型・テスト・proof・reviewは競合ではなく責務が異なる
- finite test suiteと全称propertyを区別する
- verifiableな整数の骨格を、浮動小数点等のmodel外領域から分離できる
- mathematical integer modelとmachine integerの差はproofのsoundness interpretationに直結する
- specificationの不足はsolverでは救えない
- proofはtestの置き換えではなく、testでは見落とし得るfailure classを検出する手段である。finite test suite が見落とすfailure classをproofは補完的に検出し、両者は相互補完の関係にある

MoonBit固有の制約を他toolへ一般化してはならない。実際のprojectでは採用するlanguage/verifier/modelのcurrent behaviorを個別に確認する。
