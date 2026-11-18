---
name: worktree-workflow
description: current release-driven profileでWorktrunkをWSL/Linux workspace lifecycle Practiceとして使い、Rust/Cargo worktreeのbuild-output isolation・cache reuse・cleanupを含め、同等以上のguaranteeを持つalternativeへのrefinementも判断する時に使用する。
---

# Worktree Workflow

Layer: **Practice**

Current release-driven profileではWorktrunkをGit worktreeの標準操作frontendとして使用する。WSL2/LinuxまたはLinux hostでWorktrunkが利用可能なら、日常のworktree作成・切替・一覧・review checkout・cleanupは原則 `wt` 経由で行う。

Worktrunk自体はConstitutionではない。採用理由はworkspace lifecycle / recoverability / process-port ergonomicsであり、native agent workspace等が同等以上のguaranteeを提供する場合はADR-0017のrefinement contractに従って置換できる。

単にagentがnative `git worktree` に慣れていることはdeviation evidenceにならない。native WindowsをこのSkillの必須targetにはしない。

このSkillは主に**authoring workspace lifecycle**を扱う。ADR-0020のverification-only executorへworktree作成を機械的に要求しない。Windows native等でproject/tooling constraintによりworktreeが使えない検証は`sandbox-runtime` / `quality-gate`のverification contractへrouteする。

## Current practice guarantees

- Worktrunkはworkspace lifecycle toolであり、execution isolation boundaryではない。
- branch/ref/GitHub Issue/PRがcanonical stateであり、worktree pathやWorktrunk local stateをSoTにしない。
- ticket branchはIssue番号のみ、release branchは`release-<major>-<minor>-<patch>`を維持する。
- `wt merge main`等でGitHub PR lifecycle / protected main / explicit release authorization boundaryを迂回しない。ticket PRのautonomous landingもGitHub delivery contract経由で行う。
- project-shared Worktrunk hookは`.config/wt.toml`へcommitする。
- worktree path等のmachine preferenceはuser configであり、project truthにしない。
- WSLでは高頻度build/watch用worktreeをLinux filesystemへ置き、`/mnt/c`を標準にしない。

## Prerequisites

最初に `wt --version` で利用可否を確認する。未導入ならrepositoryのreproducible toolchainに含められるかを確認し、安全にprovision可能なら導入する。導入不能・非対応・権限不足の場合だけnative `git worktree`へfallbackし、恒常的な制約ならproject documentationへ理由を残す。

Cargoで導入する例:

```bash
cargo install worktrunk
wt config shell install
```

shell integrationは`wt switch`でcurrent shell directoryを切り替えるために必要。

導入後:

```bash
wt --version
wt config show
```

で利用可能性とconfig locationを確認する。

## Standard operations

現在のrelease branchへ移動:

```bash
wt switch release-0-2-0
```

Issue #123用ticket branch/worktreeを作成:

```bash
wt switch --create 123 --base=release-0-2-0
```

`wt switch --create <name>` は `--base` を指定しないとdefault branch（通常 `main`）をbaseにするため、release branchやpredecessor branchから派生させたい場合は必ず `--base` を明示する。

- current HEADから派生: `wt switch --create <name> --base=@`
- 指定release branchから派生: `wt switch --create <name> --base=release-x-y-z`
- stacked ticketでimmediate predecessor branchから派生: `wt switch --create <dependent-issue> --base=<predecessor-issue>`

default branchからの派生はtarget release trunkへ直接stackできないticketを作るため、`github-delivery` policy違反になる。作成元はcurrent expected baseでなければならない。stacked ticketではimmediate predecessor snapshot/branchとの関係を`github-delivery` / `parallel-orchestration` policyに従って決める。

worktree一覧:

```bash
wt list
wt list --full
```

PR review用checkout:

```bash
wt switch pr:123
```

PR checkoutはreview workspaceを分離するための操作であり、review対象SHAとvalidation evidenceは別途pinする。

branchが不要になった後のcleanup:

```bash
wt remove <branch>
```

削除前にPR / release landing state、未commit変更、必要artifactを確認する。

## Project configuration

repository-specific hookが必要なら:

```bash
wt config create --project
```

で`.config/wt.toml`を作成し、実際のproject stackへ合わせて編集・commitする。

universalなdev commandを決め打ちしない。initializerはpackage scripts、framework docs/config、existing startup commandを調査して、port override方法を特定する。

Worktrunk専用のdev server例（Orca/plain gitでは展開されない）:

```toml
# .config/wt.toml
[post-start]
server = "wt step tether -- <project-specific command using {{ branch | hash_port }}>"

[list]
url = "http://localhost:{{ branch | hash_port }}"
```

例のplaceholderをそのままcommitしてはいけない。Vite / Next.js / backend CLI / env-based server等、実際のcommand semanticsへ変換する。

## Frontend independence

worktreeを作るfrontendはWorktrunk以外（Orca、plain git等）も使われる。frontendごとにsetupが違うと、同じbranchでも作り方によって状態がずれる。そのため、作成・削除時の処理はfrontendに書かず、repository-controlledな入口（例：`mise run worktree:setup` / `mise run worktree:teardown`）に置く。frontendはその入口を呼ぶだけにする。

```toml
# .config/wt.toml
[pre-start]
setup = "mise run worktree:setup"

[pre-remove]
teardown = "mise run worktree:teardown"
```

- portなどworktreeごとの値は、frontendのtemplate（`hash_port` 等）ではなく入口の中でbranch名から決める。
- 入口は何度実行しても同じ状態になるようにする。どのfrontendから、何回呼ばれても壊れないためである。
- `.worktreeinclude` はliteralなpathだけで書く。globはOrcaが無視する。
- 全frontendで使える入口がなければ、plain gitで作ったworktreeで手動実行できる形にする。

参照実装はproject-initの `scripts/worktree/`、`mise.toml`、`.config/wt.toml`、`orca.yaml` にある。projectへ写してから、project固有のsetupを入口に足す。Orcaを併用する手順は `orca-frontend` Skillを参照する。

## Rust / Cargo build output and cache

Rust/Cargo projectでは、`target/`肥大化をworktree lifecycle上の明示的なresource concernとして扱う。ただし容量削減のためにcorrectness-sensitiveなmutable build outputを共有してはいけない。詳細なdecisionはADR-0024に従う。

### Default boundary

concurrentにbuildされ得るworktree間では次を共有しない。

- `target-dir` / `CARGO_TARGET_DIR`
- Cargo `build.build-dir`
- incremental compilation state
- `target/`へのsymlinkや同一external build directory

Cargoのtarget directory lockingはparallel buildを直列化し得るうえ、divergent Git worktreeが同じbuild directoryを共有した場合のfingerprint/artifact correctness issueがcurrent Cargoで報告されている。したがって「全worktreeを1個のtargetへ向ける」を標準optimizationにしない。

Cargo 1.91+の`build.build-dir`をexternal locationへ移す場合も、workspace pathごとに一意なdirectoryを使い、そのdirectoryのcleanup ownershipを定義する。異なるmutable worktreeへ同じbuild directoryを割り当てない。

共有候補は次に限定する。

- Cargo registry / git dependency download cache
- read-only toolchain cache
- bounded compiler cache such as `sccache`

`sccache`を採用する場合は`build.rustc-wrapper`または`RUSTC_WRAPPER`で接続する。ただし2026-09-27時点のsccache v0.17.0では、Rust hash keyへ`SCCACHE_BASEDIRS` / `basedirs`を適用するissue #2652が未解決である。Rustのparallel checkout / Git worktreeで`basedirs`だけによりcross-worktree hitが成立すると仮定しない。`--remap-path-prefix`はcompiler outputへ埋め込まれるpathを安定化できるが、cache-key normalizationの代替ではない。cross-worktree Rust reuseを有効化する場合は、使用するsccache version / rustc-Cargo configuration / path flagsを記録し、複数worktree間のhit/missを実測する。未検証ならfuture-facing optimizationとして扱う。absolute machine pathはproject truthにせずuser/runtime configへ置き、local cache sizeはhost capacityに応じてboundedにする。local storageを使う場合、同じ`SCCACHE_DIR`へ複数の独立sccache serverを競合させず、同一hostでは単一serverを共有するかserverごとにstorageを分離する。repository-required toolとして採用する場合は既存mise policyに従ってversion/provisioningを再現可能にする。

### Worktree bootstrap

Rust `target/`をsymlinkしたり、単一directoryとして共有してはいけない。一方、Worktrunkの`wt step copy-ignored`がfilesystemのreflinkを使える場合は、`--require-include`を必須とし、repository-controlled `.worktreeinclude`で承認済みseed pathだけをallowlistした場合に限り、各worktreeに独立pathを保ったcopy-on-write seedとして利用してよい。Rust target seedでは`target/`を基本allowlistとし、`.env`、credential、token、socket、DB、その他mutable runtime stateを含めない。

WorktrunkはAPFS / btrfs / XFS / ReFS等ではreflinkを使用できる。reflink対応が実測で確認できたhostでは、compatibleなbase worktreeから`target/`をseedすることでinitial disk増加を抑えつつcold startを短縮できる。

ext4 / NTFS等ではfull copyになるため巨大な`target/`をコピーしない。Worktrunkのsummaryでreflink利用を確認できないhostではproject config等で:

```toml
[step.copy-ignored]
exclude = ["target/"]
```

を標準候補とする。`wt step copy-ignored`は`--require-include`なしで実行せず、`.worktreeinclude`はrepository-controlled allowlistとしてreviewする。`target/`を含めるのもreflink capabilityを確認したhost/projectだけにする。

CoW seedはmutable-directory sharingではないが、seed artifact自体をvalidation evidenceにしない。新worktreeでは通常どおりCargoのfingerprint/rebuildとrequired validationを実行する。

### Incremental compilation

incremental compilationは一律に無効化しない。

- long-lived interactive checkout: Cargo dev defaultのincremental buildを標準候補とする
- short-lived / disposable agent worktree: reuse期間が短くdisk amplificationが大きい場合、`CARGO_INCREMENTAL=0`を優先候補とする
- project-wide `[profile.dev] incremental = false` はclean build / representative rebuild / disk footprintを比較してから採用する

sccacheはincrementally compiled Rust crateをcacheできない。short-lived agent worktreeでcross-worktree sccache reuseを狙う場合は`CARGO_INCREMENTAL=0`を明示することを標準候補とする。long-lived interactive checkoutではedit/rebuild latencyとの比較で決め、「incrementalを保持すること」自体を目的化しない。

### Reclamation

`cargo clean`をroutine build/test stepへ入れない。disk pressureやstale artifact recoveryでは狭いcleanupを先に選ぶ。

```bash
cargo clean --dry-run -v
cargo clean --doc
cargo clean --release
cargo clean --profile <name>
cargo clean --target <triple>
cargo clean -p <package>
```

full `cargo clean` はcache corruption、toolchain/profile regime change、active worktreeの強いdisk pressure、externalized per-worktree build directoryのretirement等、rebuild costよりreclamation benefitが大きい場合に限定する。

通常のworktree-local `target/` はworktree directoryと一緒に削除されるため、`wt remove`直前にfull cleanを二重実行しない。external build directoryを採用したprojectだけは、worktree removal時にそのworktree固有directoryを安全にreclaimするhook/taskを用意する。

Cargo global cache auto-GCはregistry/git等のglobal cache用であり、current Cargoのtarget build artifact lifecycleの代替として扱わない。

### Reduce what gets built

target footprintが継続的に問題になるprojectでは、cleanupだけでなくartifact production自体を調べる。

- `cargo tree -e features` で実際に有効なfeatureとenable元を調べる
- `cargo tree -d` でduplicate dependency versionを調べる
- `cargo build --timings` で高cost compile unitを調べる
- virtual workspaceを含めappropriate Cargo resolverを確認する
- unused default featuresがproject evidenceで確認できたdirect dependencyだけ`default-features = false` + explicit featuresを検討する
- project MSRVがstring debug levelをsupportし、通常開発でfull debugger variable informationを必要としないなら、Cargo公式build-performance guidanceの次のshapeを優先候補として計測する

```toml
[profile.dev]
debug = "line-tables-only"

[profile.dev.package."*"]
debug = false

[profile.debugging]
inherits = "dev"
debug = true
```

通常devではworkspace memberをbacktraceに必要なline infoへ抑え、dependency debug infoを生成しない。full debugger sessionは`--profile debugging`へopt-inする。

dependency default featureやlibrary feature surfaceはpublic behaviorへ影響し得るため、disk optimizationだけを理由に一括変更しない。

recursive cleaner等のthird-party toolはhost convenienceとして使ってよいが、project correctnessの必須依存にしない。unmaintained toolをcurrent defaultへ固定しない。

## Port allocation

Worktrunk専用の `{{ branch | hash_port }}` はbranch名からportを決める。Orca/plain gitと併用する場合は使わず、共通setup入口でportを決める。

ただしhash-based allocationは絶対的なuniqueness guaranteeではない。dev server / runtimeはbind failureを明示的に検出し、必要ならproject-specificなport reservationまたはcollision-resolutionを追加する。既に別processが占有しているportを「自分のbranch用」と仮定して継続してはいけない。

適用境界:

- hostへ直接bindするprocess: dev commandのportへ適用
- container/sandbox: host-published portへ適用し、container内部portは通常固定でよい
- preview URL: 同じport templateから構築できる
- DB等の別service: 別namespaceを使う。Worktrunk専用なら `('db-' ~ branch) | hash_port`、複数frontendなら共通入口で決める

portが一意でもprocess/database/filesystem/credential isolationが成立したとは扱わない。

## Process lifecycle

long-running dev server/watch processをWorktrunk hookから起動する場合は、適切なら:

```bash
wt step tether -- <command>
```

を使用する。

tethered processはworktree lifecycleへ結び付け、worktree removal後のorphan processやstale port ownershipを減らす。

これはprocess cleanup mechanismであり、sandbox security boundaryではない。

## Mutable services and state

同一hostへ複数worktreeをmaterializeする場合、次を共有しない設計にする:

- writable DB/schema
- Redis namespace / queue
- container name
- Unix socket
- app-local mutable state
- generated runtime state
- credentials with broader authority than the worker requires

Worktrunkの`sanitize_db` / `hash_port`等はdeterministic identifierとして利用できるが、実際のservice isolationは`sandbox-runtime` policyに従う。

## Delivery boundary

Worktrunk commandはGitHub deliveryのergonomic frontendに限定する。

許可される典型操作:

```text
wt switch release-x-y-z
-> wt switch --create <issue-number> --base=release-x-y-z
-> implementation / commit / publish
-> immediate PR creation/state
-> review / validation
-> ticket-class: autonomous GitHub landing / release-class: explicitly authorized GitHub landing
-> wt remove <issue-number>
```

`wt merge`のlocal integration convenienceは、project-initのticket PR lifecycle / release PR / protected main / explicit release authorization boundaryを置き換えない。

## Fallback and recovery

### Authoring

Worktrunkが利用できないmutable authoring workerではnative `git worktree`へ縮退してよい。ただしbranch naming、mutable ownership、runtime state safety、PR state lifecycle等のapplicable semanticsは維持する。

worktree自体を作れないauthoring environmentでは、同じshared checkoutへ複数workerを並行配置しない。isolated clone / sandbox / serialized ownership等、同等以上のmutable ownership guaranteeを選ぶ。

### Verification-only

verification-only executionはworktree fallback chainの対象ではない。immutable candidate artifactをcleanにmaterializeできれば、package / installed build / clean checkout / disposable clone / serialized singleton checkout等を利用できる。

singleton checkoutを使う場合はdirty stateを暗黙に上書きせず、exclusive ownershipとbefore/after state auditを行う。validation中にsource authoringへ移行した場合はmutable worker policyへpromotionする。

fresh environmentではGit refs、Issue/PR metadata、committed `.config/wt.toml`、project docsからworkflowを再構成できなければならない。user-level Worktrunk configだけに必要情報を残さない。


## Refinement / deviation

Worktrunkから外れる場合は、少なくとも次を確認する。

- canonical task/source identityがlocal pathに依存しない
- concurrent workspaceのmutable-state safetyを悪化させない
- current expected baseからmaterializeできる
- review/recoveryがtool-local hidden stateだけに依存しない
- dev process / port / mutable service lifecycleについて必要なguaranteeを維持する

同等以上ならalternativeを許容する。Worktrunk command shapeそのものをorganizational correctnessとして扱わない。

## Remove / re-evaluate

- agent/runtimeがnativeに同等以上のworkspace lifecycleを提供する
- Worktrunk固有hookがproject stackと不整合になる
- host worktreeを使わないruntime modelへ移行する
- comparative evalでWorktrunk-specific instructionの追加価値が消える
