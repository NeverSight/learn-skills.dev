---
name: sandbox-runtime
description: implementation worker用の独立sandboxを作成・検証し、macOS / WSL/Linux / remote provider差を吸収する時に使用する。
---

# Sandbox Runtime

Layer: **Practice**

このSkillは主にConstitutionの **Mutable Ownership Safety** と **Organizational Continuity** をruntime boundaryへmaterializeするcurrent Practiceである。

特定sandbox/provider自体を要求するのではなく、taskに必要なfilesystem/process/network/credential/service-state separationのguaranteeを要求する。

実装用mutable workspaceとverification環境を同一視しない。ADR-0020のVerification Executorは、sourceをauthoringしない限りimplementation worker用worktree/sandbox topologyを要求せず、検証対象artifact identityとenvironment ownershipを別contractで扱う。

## Current practice guarantees

- 1 implementation worker = 1 isolated workspace/runtime。
- mutable runtime stateはworker間で共有しない。
- 同一内部portは使用してよい。host公開port / preview routeはruntime側で一意化する。
- host Docker socket、root-equivalent host capability、master credentialをworkerへ渡さない。
- immutable/cacheable stateのみ共有する。
- provider差はadapterへ閉じ込め、project semanticsを変えない。
- Worktrunkはworkspace/worktree lifecycle adapterであり、sandbox/runtime isolation boundaryとして扱わない。
- `security-audit` がtarget-controlled codeを実行する場合も本Skillのnetwork / environment / writable state / resource isolationを満たす。必要controlをenforceできない環境ではhost executionへfallbackせず `needs_validation` とする。

## Isolate

最低限:

- repository checkout
- process boundary
- network / port mapping
- writable filesystem
- DB / Redis / queue
- application local state
- test artifacts
- mutable build output

## macOS

- Apple Silicon `arm64`を第一級targetとして扱う。
- binary / dependency / container imageのarm64対応を確認する。
- x86_64 emulationを暗黙前提にしない。
- portable Web/backend taskは原則Linux sandboxで実行する。
- Apple-native toolingが必要なtaskだけmacOS-native workerを許可する。
- Docker Desktopを必須にしない。

## Windows + WSL2

- Linux-oriented repoはWSL Linux filesystemを優先する。
- `/mnt/c`等を高頻度build/watchの標準workspaceにしない。
- WSL自体をworker isolationとみなさない。
- permission / symlink / executable bit / line ending差を検証する。
- port forwardingはSupervisor/runtime側で抽象化する。
- WSL/Linuxでlocal worktreeを複数扱う場合は`worktree-workflow` Skillを適用し、worktree pathはLinux filesystemを優先する。

## Worktrunk integration

WSL/Linuxのlocal workspace materializationではWorktrunkをpreferred frontendとしてよい。

- shared project hookはproject-local `.config/wt.toml`へ置く。
- shared hostへ公開するdev serverは、実際のframework/runtimeが許すport overrideへ `{{ branch | hash_port }}` を接続してdeterministically割り当てる。`hash_port`自体をuniqueness proofとせず、startup時のbind conflictを検出する。
- long-running local processは適切なら `wt step tether -- <command>` でworktree lifecycleへ結び付ける。
- container/sandbox内部portは同一値のままでよく、`hash_port`は必要なhost-published portへ適用する。
- DB / Redis / queue / socket / container name等のmutable stateは別途runtime adapterで一意化する。必要ならWorktrunkのdeterministic template valueをidentifierへ利用してよい。
- `wt merge main` 等をGitHub delivery policyの代替integration pathとして使わない。

詳細な操作は `worktree-workflow` Skillに置き、このSkillではisolation semanticsをcanonicalに保つ。

## Verification-only native environments

Windows native / macOS native / GUI application / physical device / installed application / CI等でworktreeを作れない、または作ることが検証対象を歪める場合は、verification-only executorとして扱える。

優先materialization:

1. immutable package / installed artifact / image digest / deployment revision
2. clean dedicated checkout
3. disposable clone / snapshot
4. unavoidable場合のみexclusive leaseを取ったsingleton checkout

verification executorは最低限、candidate identity、environment identity、procedure、result、evidence artifact、source mutation有無を記録する。

singleton environmentはparallelizeを要求しない。exclusive lease / serialization / queue等でMutable Ownership Safetyを満たす。

unexpectedなtracked source/config mutationが生じた場合、そのままcurrent candidateのverification evidenceとして採用しない。expected behaviorとしてmutation自体を検証する場合を除き、clean candidateで再実行する。

verification中にfix実装へ移る場合は、新しいmutable Worker attemptとして切り替える。

## Portability

Apple Silicon localとx86_64 CI/remoteが混在する場合、architecture-sensitive dependency install/build/testを検証する。

## Reproducibility target

```text
clone
-> bootstrap
-> sandbox create
-> dependency install
-> migrate / seed
-> app/test start
-> validation
```


## Refinement criteria

別runtime/provider/native agent environmentへ置換する場合、変更surfaceに必要な次のguaranteeを比較する。

- writable mutable state isolation
- process/service namespace safety
- network policy
- credential boundary
- resource/lifecycle cleanup
- durable result extraction / recovery
- snapshotの永続性、suspend / resume、provider喪失時の復旧、remote artifactの耐久性（create / destroyの費用だけで比べない）

同等以上ならprovider implementationは自由に置換できる。単なるworktree分離をruntime isolationのproofとして扱わない。
