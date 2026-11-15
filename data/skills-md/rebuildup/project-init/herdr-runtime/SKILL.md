---
name: herdr-runtime
description: Herdrをoptional Supervisor/session Practiceとして使い、Worker execution attemptの安全なmappingに加えてagent-driven fan-out / observe / collectを行う時に使用する。
---

# Herdr Runtime

Layer: **Practice**

Herdrはproject-initのlogical Worker / Supervisor modelを実装するoptional runtime adapterである。

Herdr固有のworkspace / pane / agent stateをorganizational truthへ昇格させない。canonical semanticsは `organization/execution-roles.md`、ADR-0019、`parallel-orchestration`、`agent-recovery` に従う。

## When to use

Herdrは次の場合に有効:

- 複数の独立Claude Code / Codex / OpenCode等を同時に走らせる
- long-running/background Workerを人間が一覧監視したい
- top-level agent同士をCLIからprompt / wait / readしたい
- terminal sessionをdetachして継続したい
- provider/runtimeの異なるWorkerを一つのoperational surfaceで扱いたい

次の場合はHerdr Workerへ昇格させないdefaultを優先する:

- 1つのClaude/OpenCode内部で完結する短いnative research subagent
- independent lifecycleを必要としないreview/explore
- orchestration overheadがtask価値を上回るwork

## Preconditions

`herdr` が利用可能か確認する。

Herdr-managed pane内では `HERDR_ENV=1` が設定される。必要に応じて `HERDR_PANE_ID` / `HERDR_WORKSPACE_ID` をtransient runtime identityとして利用できるが、durable task identityの代替にしない。

agent-specific integrationを使用する場合はcurrent Herdr CLIで確認してから導入する。現行CLIでは例として:

```bash
herdr integration install claude
herdr integration install codex
herdr integration install opencode
herdr integration status
```

integrationはstate/session detectionを改善するPracticeであり、project evidenceのSoTではない。

## Responsibility split

| Layer | Responsibility |
| --- | --- |
| project-init | work unit / attempt class / authority / evidence / admission / recovery semantics |
| Worktrunk or selected Git workspace Practice | branch/worktree materialization |
| sandbox/runtime | filesystem/process/service/network/credential mutable ownership |
| Herdr | terminal, pane, top-level agent lifecycle, transient state/observability |
| native coding-agent subagents | one top-level Worker内部のtemporary delegation |

Herdrの `worktree create` 等をWorktrunkの自動代替として使わない。workspace mechanismを変更する場合はADR-0017のrefinement contractで比較する。

## Mapping

project-init logical capabilityからHerdrへmappingする場合のcurrent shape:

| Logical capability | Herdr Practice |
| --- | --- |
| create execution surface | `workspace create` / `tab create` / `pane split` |
| spawn Worker agent | `agent start` |
| discover/observe | `agent list` / `agent get` |
| send work | `agent prompt` |
| wait | `agent wait` |
| inspect result/UI | `agent read` |
| human takeover | `agent attach` |
| interactive interrupt | `agent send-keys ... ctrl+c` |
| terminal teardown | `pane close` / workspace lifecycle |

このmappingはcommand compatibility layerであり、organizational contractではない。

特にcancelは `ctrl+c` を送っただけで完了とみなさない。process/agent stateとdurable side effectをreconcileし、durable Workerならfencing ownershipを更新してからreplacement attemptをadmitする。

## Provider-scoped launch and bounded layout

For a configured provider route, `herdr agent start --kind` does not replace the dotfiles `agent <harness> <provider>` launcher. Resolve route first; run that launcher in a Herdr pane. No silent native/paid/provider fallback. Herdr detection is not evidence of model identity or acceptance.

Use `herdr api snapshot` to reuse an unambiguous project workspace and function tab; do not create a workspace per attempt or a tab per function. Default presentation: `Ctrl`, `Work`, `Device`; default four panes per tab, then queue unless a bounded overflow is configured. Never commandeer an existing terminal, steal focus, or destructively replace live layouts. See `organization/execution-functions.md` and `templates/agent-routing/`. Layout does not grant authority or replace mutable resource leases, recovery fencing or safe cleanup.

## Agent-driven Supervisor loop

Herdr-managedなCoordinator / Supervisor agentは、`HERDR_ENV=1` を確認したうえでHerdr CLI/APIからsibling top-level Workerを起動・委譲・回収してよい。fan-out判断は `parallel-orchestration` のadaptive policyに従い、Herdr paneを増やすこと自体を目的にしない。

current command surfaceでは概ね次を使用する。

```bash
herdr agent list
herdr agent start <worker-name> --kind <agent-kind> --pane <pane-id>
herdr agent prompt <worker-name> "<bounded-task>" --wait --timeout <ms>
herdr agent read <worker-name> --source recent-unwrapped --lines <n>
```

workspace / tab / pane creationを行う場合はcommandが返したJSON IDを取得し、IDやpane placementを推測しない。

Supervisor loop:

1. execution profile / dependency / attempt class / fan-out modeを決める。
2. mutable WorkerならHerdrより先にworkspace/runtime ownershipをmaterializeする。
3. execution surfaceとagentを作る。
4. bounded task contractをpromptする。
5. `agent wait` / `agent read` / lifecycle telemetryでobserveする。
6. `blocked`、timeout、`agent_prompt_stalled` 等をreconcileしてからretry/reassignする。
7. immutable result / evidenceを回収し、base / fencing / validation / authorityを確認する。
8. remaining workとbottleneckを再評価し、spawn / continue / stopを選ぶ。

official Herdr Agent Skillはcommand adapterとして利用できるが、project-initのattempt / ownership / evidence / admission semanticsを置換しない。導入する場合はproject-local Skill policyに従うか、`herdr --skill` 等のinstalled releaseに対応したsourceを利用し、global installationをproject correctnessの前提にしない。

remote machineを使う場合はtargetを明示する。machine/server failure後に別machineやlocalへsilent fallbackして同じmutable attemptを二重継続しない。

## Spawn flow

1. objective / acceptance criteria / authorityを読む。
2. ADR-0019に従い observational / mutable / durable attemptを分類する。
3. mutable attemptなら先にrequired workspace/runtime isolationをmaterializeする。
4. Herdr snapshotから既存project workspace/tab/paneを調査し、必要なsurfaceだけ作る（capacity超過はqueue/block）。
5. creation commandが返したJSONのIDを使い、IDを予測しない。
6. supported top-level agentを `agent start` するか、既存agentをdetect/renameする。
7. execution attempt metadataへHerdr workspace/pane/agent nameをtransient referenceとして関連付ける。
8. promptを送る。
9. `agent wait` / `agent read` でobserveする。
10. project-init result/evidence contractを満たすartifactを回収する。
11. applicable fencing / validation / admission check後にのみorganizational resultへ採用する。

workspace creation example:

```bash
created=$(herdr workspace create --cwd <workspace-path> --label <label> --no-focus)
pane_id=$(printf '%s\n' "$created" | jq -r '.result.root_pane.pane_id')
```

agent start example:

```bash
herdr agent start <worker-name> --kind claude --pane "$pane_id"
```

agent kind / optionsはcurrent installed Herdr / provider CLIを確認して決める。model flag等をproject policyへ固定しない。

## Prompt / wait / read

例:

```bash
herdr agent prompt <worker-name> "<task>" --wait --timeout 120000
herdr agent read <worker-name> --source recent-unwrapped --lines 120
```

重要:

- `blocked` はhuman/approval/inputが必要なsignalとして扱う。
- `working` は実行中signal。
- `done` / `idle` はinput可能状態であり、acceptance criteria達成を意味しない。
- `unknown` を成功扱いしない。
- timeout / `agent_prompt_stalled` は「prompt未送信」の証拠ではない。retry前にread/getしてreconcileする。
- waitにはbounded timeoutを指定し、永続hangをSupervisor logicへ持ち込まない。

## Native subagents

top-level Claude Code等の内部subagentは、Herdr上で別paneとして可視化することを要求しない。

```text
Herdr Worker: Claude Code
  ├─ native Explore subagent
  ├─ native Reviewer subagent
  └─ native temporary helper
```

でよい。

次の場合だけ別Herdr Workerを検討する:

- independent mutable workspaceを持つ
- parent process loss後も継続させたい
- provider/model/toolを分離したい
- independent cost/budget/lifecycleを持つ
- humanがtop-level lifecycleを直接監視/attachする価値がある

## Worktrunk integration

WSL/LinuxでWorktrunkを使用するprofileでは:

1. Worktrunk / selected workspace Practiceでexpected branch/worktreeをmaterializeする。
2. sandbox/runtime policyで必要なmutable resourcesを分離する。
3. そのworkspace pathをHerdr workspaceのcwdへ渡す。
4. Herdrはagent/session lifecycleだけを所有する。

Herdr workspace pathやpane IDをGit branch / Issue identityとして推測しない。

## Recovery

Herdr detach/reattachはsoft continuityとして利用できる。

ただしdurable WorkerはHerdr process persistenceだけに依存しない。

server/host/provider loss後は:

1. durable Issue/PR/Git/checkpointを読む。
2. current fencing ownershipを取得する。
3. Herdrに残るagent/sessionがあればreconcileする。
4. stale attempt resultをadmitしない。
5. 必要なら新Herdr workspace/agentを作り直す。

native session restoreが利用できても、それだけをcanonical recovery mechanismにしない。

## Cleanup

pane/workspaceを閉じる前に:

- inventory at spawn/settle (`workspace list`, `agent list`, `api snapshot`); avoid workspace sprawl
- close settled surfaces (`pane/tab/workspace close`); keep uncollected results, uncommitted work, unresolved blocks, and surfaces owned by others
- required immutable resultが回収済み
- validation/evidence identityが記録済み
- consequential side effectがreconcile済み
- durable checkpointが必要なら作成済み
- uncommitted unique workを失わない

ことを確認する。

## Official references

Current reference documentation:

- https://herdr.dev/docs/agent-automation/
- https://herdr.dev/docs/agents/
- https://herdr.dev/docs/session-state/
- https://herdr.dev/docs/cli-reference/
- https://herdr.dev/docs/agent-skill/

Herdr command shapeが変わった場合は本Skillを更新する。Constitution/Operating ModelをHerdr commandへ合わせて変更しない。

## Remove / re-evaluate

- native runtimeが同等以上のtop-level Worker lifecycleを提供する
- Herdr CLI/APIが大きく変更される
- agent state detectionがselected providerで信頼できない
- remote execution中心になりlocal terminal runtimeが不要になる
- adapter maintenance costがbenefitを上回る
