---
name: ae-things
description: "工作空间事项（things）：在明确的 AgentSpace 中用 ae-cli things 创建、查询、更新和推进事项。当对话出现分工指派（谁负责什么）、要交付的产出、推进节奏、待办、下一步、里程碑或阶段计划时主动使用——不需要用户显式说「创建事项」。"
---

# 工作空间事项

使用 `ae-cli things` 操作当前明确指定的 TE 空间事项。先读 [CLI reference](references/cli.md)，不猜 ID，不自动选择其他空间。

## 何时创建事项

**由你自己判断要不要建，不要等「帮我创建事项」这种显式指令。** 个人空间与共享空间一视同仁。

出现下列任一信号就直接创建，不必先问：

- 出现「谁做什么」的分工指派，例如「让 A 梳理 X，B 梳理 Y」。
- 出现要交付的产出加上推进意图，例如「输出一份最终方案」「按这个节奏推进」「安排一下」。
- 出现承诺、待办、下一步、里程碑或多阶段计划。
- 用户在复述已经定下来的事，并指向后续执行。

下列情况不要创建：

- 纯信息问答、概念解释、闲聊。
- 还在比较方案、假设性推演，或用户明确说「先不定」。
- 查重命中已有同义事项——指出已存在，不重复建。
- 用户说过不要建。

**不确定时，把拟建清单（标题、负责人、描述要点）在回复里列出来，一次性问用户确认。不允许什么都不做就把分工排版成清单交差。**

### 创建时的动作顺序

1. 确认已绑定明确的 AgentSpace；没有绑定就不创建。
2. `members` 取成员列表，把对话里提到的人名映射到成员 ID。唯一命中就直接作为 `--assignee-id`；命中 0 个或多个时该事项负责人留空（服务端默认当前用户），并在回复里点名待确认。
3. `list --query` 或 `options --query` 查重。
4. 逐个 `create`：标题写可交付物而不是原话复述，描述写清目标与验收要点，带 `--command-id` 保证重试幂等。
5. 需要时用 `conversation bind` 绑定主事项，或 `link-conversation` 建普通引用。
6. 在回复里报告已创建的事项编号、标题、负责人，以及哪些负责人待确认。

**粒度**：按「可独立交付、可独立负责」的单位建事项。没有子事项和分组，不要试图建层级。例如「A、B、C 各自梳理一块，然后合成一份总方案」对应 4 个事项，而不是 1 个，也不是每句话一个。

### 授权边界

自主执行：创建新事项；为自己刚建的事项补第一条记录。

用户已授权推进/完成的事项：直接追加或更新相应进展，并自动关联本次涉及的交付附件，按下节完成发布与回读。个人与共享空间一致，发布仍传 `--confirm-share`；授权事项交付即包含向该事项所在空间共享这些交付文件。

其他已有事项改写、负责人变更、归档/恢复、解绑及永久删除仍需明确授权；历史绑定本身不是授权。不自动发消息或创建定时任务。

### 交付附件闭环

追加/更新进展时，逐个核对本次实际交付文件：

1. 用 `asset available` 查本空间文件并翻完分页。已登记文件按 assetId 关联，未登记文件按返回的相对 path 关联。
2. 尚未进入空间的新文件用 `asset publish`：本轮未登记产物使用 `--conversation-id --run-id --source-path`；已有产物使用 `--artifact-id` 或 `--file-token`。每个文件保存独立 commandId，重试原样复用。
3. `linked:false` 表示已发布未关联，只用返回 assetId 补 `asset link`，不重复复制。只发布本次交付文件，不发布临时文件或整个会话目录。
4. `asset list --id` 回读，核实每个附件存在且 availability=available，再回读进展记录。只有两者均成功才报告“进展和附件已更新”；失败明确区分已发布、已关联、待恢复。

附件使用上述文件关联接口；本地路径文本链接不能代替附件，仅复制文件也不算交付完成。完整参数见 CLI reference。

## 当前会话绑定与执行快照

以本轮冻结的绑定声明确定本轮默认事项。涉及当前事项执行、审查、总结或更新前，按声明中的 `readCommand` 读取本次执行快照；普通聊天无需读取。运行中切换或解绑只立即改变会话归属，本轮（含等待、恢复、重试）仍用原快照；原先无事项则本轮继续无默认事项，下一次新 Run 才使用最新绑定。用户明确指定其他事项时仍按权限读取和操作，不将会话最新归属误认为本轮快照。

用户明确要求将当前对话绑定到某事项时，唯一定位目标后执行 `conversation bind`，再用 `conversation primary` 回读确认；同名事项不能唯一确定时询问用户。成功说明「已绑定，事项上下文从下一轮生效」。解绑也须回读确认。不得将 `link-conversation` 普通引用当成主事项绑定成功的替代；接口失败应如实说明，不绕过权限。

`context --id <thing-id> --run-id <run-id>` 返回执行受理时的业务文本和版本。需要最新事实或写入前版本时额外读取不带 `--run-id` 的实时上下文，并明确区分采集时间与快照版本。读取失败时披露缺失，不凭标题猜测，也不自动改读实时数据。具体契约见 [CLI reference](references/cli.md#执行快照与实时上下文)。

- 字段为标题、描述、标签、状态、负责人、协作者。状态 open/paused/done；归档与恢复是独立动作。新建描述必填，创建时省略负责人默认本人，显式 null 被拒绝。
- 用 members/options 查询成员和事项候选；创建、编辑和协作者管理遵循服务端权限。修改前读最新 version，409 后比较变化，不仅替换版本号。
- 记录使用 url/note/progress；省略类型时服务端将单个 HTTP(S) URL 保存为链接，其余为备注。更新进展用 entry append --type progress；修改记录用 entry update 和 expected-updated-at，支持单独修改标题、类型或正文；--clear-title 清空标题。
- 从会话消息整理事项用 from-message，提供已核实的 conversation-id/message-id 和确认正文；按上面的创建信号判断是否该整理，不要求用户显式点名该命令。推断出来的内容先在会话中呈现建议；不使用已删除的持久化修改草稿命令。
- 主事项使用 conversation primary/bind/unbind，普通引用用 link-conversation，conversations 查询关联。关联不改变会话隐私和权限。
- 阶段成果使用进展记录；交接使用备注写清已完成内容、证据和下一步。负责人和协作者是唯一人员协作关系，不额外认领。
- 文件使用 asset available/list/link/unlink/publish，遵循上面的授权边界与交付附件闭环；解除关联不删除文件。
- 永久删除先读最新版本，解释不可恢复及会话/文件保留边界，明确确认后使用 delete --confirm-delete --yes。运行冲突时等待，不自动终止运行。
- 已获明确授权的具体修改直接执行，不重复询问。

```bash
ae-cli things create --agent-space-id <space-id> --title '接口验收' --description '验证权限与数据一致性' --format json
ae-cli things entry append --agent-space-id <space-id> --id <thing-id> --type progress --content '已完成接口联调' --format json
```

审查使用 [ae-things-review](../ae-things-review/SKILL.md)，周期汇总使用 [ae-things-progress](../ae-things-progress/SKILL.md)。二者按完整采集事实归纳，保留未读文件、截断和非事务采集边界。

Use `things conversations` to list linked conversations and `things conversation get` to read one. Start new conversations from the workspace UI; Things CLI only manages thing links and primary-thing binding.
