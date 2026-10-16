---
name: doubt-driven-development
description: 在每个非平凡决策成立前，用全新上下文进行对抗式审查。当你想在继续推进前交叉质询每一个假设、对计划做压力测试以暴露隐藏的失败模式、正确性比速度更重要、在处理不熟悉的代码、风险很高（生产 auth、安全敏感逻辑、高风险迁移、不可逆操作），或任何自信输出现在验证比之后调试更便宜时使用。
---

# 怀疑驱动开发

## 概览

自信的答案不等于正确的答案。长会话会积累上下文，悄悄把假设变成“事实”，而没人察觉。怀疑驱动开发是一种纪律：在任何非平凡输出成立前，物化一个带全新上下文的审查者，其偏向是**证伪**，而不是批准。

这不是 `/review`。`/review` 是对已完成产物的裁决。这是一种进行中的姿态：在修正方向仍然便宜时，让非平凡决策接受交叉质询。

## 何时使用

当至少满足以下任一条件时，决策就是**非平凡**的：

- 引入或修改分支逻辑
- 跨越模块或服务边界
- 断言类型系统或编译器无法验证的性质（线程安全、幂等性、顺序、不变量）
- 正确性依赖未来读者看不到的上下文
- 影响半径不可逆（生产部署、数据迁移、公共 API 变更）

在以下场景应用此 skill：

- 准备在不确定性下做架构决策
- 准备提交非平凡代码
- 准备声称一个非显而易见的事实（“this is safe”、“this scales”、“this matches the spec”）
- 正在处理你没有完全理解的代码

**何时不使用：**

- 机械操作（重命名、格式化、移动文件）
- 遵循清晰、无歧义的用户指令
- 阅读或总结现有代码
- 正确性显而易见的一行改动
- 纯工具操作（运行测试、列文件）
- 用户明确要求速度优先于验证

如果你怀疑每一次按键，就什么也发布不了。该 skill 只适用于上面定义的非平凡决策。

## 加载约束

这个 skill 设计给**主会话编排者**使用，因为第 3 步（DOUBT，详见下文）可以 spawn 一个全新上下文审查者。

- **不要把此 skill 加入 persona 的 `skills:` frontmatter。** 遵循第 3 步的 persona 会 spawn 另一个 persona，这正是 `../../references/orchestration-patterns.md` 明确禁止的编排反模式（“personas do not invoke other personas”）。
- **如果你发现自己在 subagent 上下文中应用此 skill**（Claude Code 会阻止嵌套 subagent spawn）：首选路径是告知用户，doubt-driven 无法嵌套运行，并让主会话处理。只有作为最后手段，才使用降级的自我质询 fallback：把 ARTIFACT + CONTRACT 改写成一个带硬心理分隔的全新自我 prompt，与之前推理隔离，并执行第 1-5 步。这**不是全新上下文审查**（你携带着自己的上下文），所以要把结果标记为降级，并在用户可达时优先升级。

## 流程

应用该 skill 时复制此 checklist：

```
Doubt cycle:
- [ ] Step 1: CLAIM — wrote the claim + why-it-matters
- [ ] Step 2: EXTRACT — isolated artifact + contract, stripped reasoning
- [ ] Step 3: DOUBT — invoked fresh-context reviewer with adversarial prompt
- [ ] Step 4: RECONCILE — classified every finding against the artifact text
- [ ] Step 5: STOP — met stop condition (trivial findings, 3 cycles, or user override)
```

### Step 1: CLAIM — 呈现将要成立的内容

用两三行命名该决策：

```
CLAIM: "The new caching layer is thread-safe under the
        read-heavy workload described in the spec."
WHY THIS MATTERS: a race here corrupts user data and is
                  hard to detect in QA.
```

如果你无法把 claim 写得这么紧凑，那你拥有的是感觉，而不是决策。在审视它之前先把它呈现出来。

### Step 2: EXTRACT — 最小可审查单元

全新上下文审查者需要的是**产物**和**契约**，不是你的心路历程。

- 代码：diff 或函数，而不是整个文件
- 决策：3-5 句提案，以及它必须满足的约束
- 断言：claim 加上据称支持它的证据（与第 1 步 CLAIM 块保持区分，后者是编排者正在接受审视的假设）

剥离你的推理。如果你交付结论，得到的会是对结论的背书。这个单元必须小到审查者一遍就能装进脑子；如果它是 500 行 PR，先拆解。

### Step 3: DOUBT — 调用全新上下文审查者

审查者的 prompt **必须是对抗式的**。框架决定答案。

```
Adversarial review. Find what is wrong with this artifact.
Assume the author is overconfident. Look for:
- Unstated assumptions
- Edge cases not handled
- Hidden coupling or shared state
- Ways the contract could be violated
- Existing conventions this might break
- Failure modes under unexpected input

Do NOT validate. Do NOT summarize. Find issues, or state
explicitly that you cannot find any after thorough examination.

ARTIFACT: <paste artifact>
CONTRACT: <paste contract>
```

**只传 ARTIFACT + CONTRACT。不要传 CLAIM。** 把你的结论交给审查者，会让它偏向同意。审查者必须独立判断产物是否满足契约。

在 Claude Code 中，`agents/` 中基于角色的审查者天然以隔离上下文启动，可在这里使用。可查看 `agents/` 的 roster 和各领域匹配关系。

**上面的对抗式 prompt 优先于 persona 的默认响应形态。** 像 `code-reviewer` 这样的 persona 会被写成输出带优点和缺点的平衡裁决；doubt-driven 需要只输出问题。把对抗式 prompt 原样粘贴到调用中，让它覆盖 persona 默认行为。如果某个 persona 的响应形态无法被干净覆盖，fallback 到带该对抗式 prompt 的 generic subagent。

#### 跨模型升级

单模型审查者会与原作者共享盲点；更冷、架构不同的模型能捕捉这些盲点。Doubt-driven 本来就是对非平凡决策的 opt-in，因此在该范围内，提供跨模型选择是该 skill 的价值之一，不是可选摩擦。

**交互式会话：始终提供。不要静默跳过。**

**第 1 步：询问用户**

在上面第 3 步的单模型审查完成后、RECONCILE 之前，暂停并询问：

> *"Single-model review complete. Want a cross-model second opinion? Options: Gemini CLI, Codex CLI, manual external review (you paste it elsewhere), or skip."*

这个问题在每个交互式 doubt cycle 中都是强制的，即使产物看起来风险很低。由用户而不是 agent 决定成本是否值得。Agent 的职责是呈现选择。

**第 2 步：如果用户选择 CLI，先验证再调用**

1. 检查工具是否在 PATH 中（`which gemini`、`which codex`）。
2. 在传入完整 prompt 前测试它能工作（`gemini --version` 或等效命令）。过期或损坏的 binary 可能通过 `which`，但在真实输入上失败。
3. 与用户确认精确调用方式，包括必需 flags、auth 和 env vars（例如 API keys）。实现各不相同，绝不要假设。
4. 只传 ARTIFACT + CONTRACT + 对抗式 prompt。不要传会话上下文，不要传 CLAIM。
5. 注意 shell escaping。如果 artifact 包含引号、`$(...)` 或反引号，优先使用 stdin（`echo … | gemini`）或 heredoc，而不是内联 `-p "…"`。有疑问时，在运行前请用户确认调用。
6. 将输出带入第 4 步（RECONCILE）。

**绝不要把 artifact 插入 shell-quoted argument。** 代码、Markdown 和审查 prompt 经常包含反引号、`$(...)` 和引号字符，它们会截断 prompt 或执行嵌入的 shell。把完整 prompt 写入文件，并通过 stdin 管道传入。

示例形态（根据已安装工具验证 flags，不同实现和版本语法不同）：

```bash
# Write the adversarial prompt + ARTIFACT + CONTRACT to a temp file first.
# Then pipe via stdin so shell metacharacters in the artifact stay inert.

# Codex (read-only sandbox keeps the CLI from writing to your workspace):
codex exec --sandbox read-only -C <repo-path> - < /tmp/doubt-prompt.md

# Gemini ('--approval-mode plan' is read-only; '-p ""' triggers non-interactive
# mode and the prompt is read from stdin):
gemini --approval-mode plan -p "" < /tmp/doubt-prompt.md
```

只读 sandbox 是承重细节：doubt artifact 本身可能包含有意或无意的指令（prompt injection），否则跨模型 CLI 可能会对你的 workspace 执行它们。

**第 3 步：如果 CLI 不可用或失败**

明确呈现失败。提供选项：用户手动运行、尝试不同工具，或跳过。不要静默 fallback 到单模型；用户应该知道跨模型没有发生。

**第 4 步：如果用户跳过**

在输出中确认跳过（*"Proceeding with single-model findings only"*），然后继续 RECONCILE。跳过可以；静默跳过不行。

**非交互式上下文**（CI、`/loop`、autonomous-loop、scheduled runs）：

- 跨模型会被**跳过**，且输出中必须**声明**跳过：*"Cross-model skipped: non-interactive context."*
- **绝不要在没有用户明确授权的情况下调用外部 CLI**，这是一个承重安全属性。

跨模型会增加成本、延迟和工具脆弱性。Agent 在每个 cycle 呈现选择；由用户决定该产物是否值得。

### Step 4: RECONCILE — 合并发现

审查者的输出是数据，不是裁决。**你仍然是编排者。** 在分类每个发现前，重新对照 artifact 文本阅读；橡皮图章式接受审查者，与忽略它是同一种失败模式。

对每个发现，按以下**优先级顺序**分类（第一个匹配类别胜出）：

1. **Contract misread**：审查者之所以标记某事，是因为你提供的 CONTRACT 不清楚或不完整。先修复 contract，在下一轮重新分类。
2. **Valid + actionable**：真实问题，需要修改 artifact。修改后重新循环。
3. **Valid trade-off**：问题真实，但修复成本高于接受成本。明确记录 trade-off，让用户看到。
4. **Noise**：审查者标记了某个在其缺少的上下文下实际正确的内容。记录它，继续，并询问：如果把那段上下文加入 contract，是否能避免这个 false flag？

全新审查者可能因缺少上下文而出错。不要因为它“新鲜”就服从。

### Step 5: STOP — 有边界的循环，而不是递归

在以下条件停止：

- 下一轮只返回琐碎或已考虑过的发现，**或**
- 已完成 3 个 cycle（升级给用户，不要独自磨第四轮），**或**
- 用户明确说“ship it”

如果 3 个 cycle 后审查者仍提出实质问题，artifact 可能还没准备好。把这一点呈现给用户；三轮仍未解决本身就是关于 artifact 的信息，不是继续循环的理由。

如果因为 artifact 很大而“显然 3 轮不够”：说明 artifact 太大。回到第 2 步拆解。不要提高上限。

## 常见自我合理化

| 自我合理化 | 现实 |
|---|---|
| “我很有把握，跳过 doubt step” | 在新问题上，自信与正确性相关性很差。感觉最确定的时候，盲点最容易藏起来。 |
| “Spawn 一个审查者太贵” | 在生产中调试错误提交更贵。检查有边界，bug 没有。 |
| “审查者只会吹毛求疵” | 只有未设范围时才会这样。把 prompt 约束为“会使其在契约下失败的问题”。 |
| “我最后用 `/review` 做 doubt 就行” | `/review` 是最终闸门。Doubt-driven 在方向修正仍便宜时捕捉错误方向。到 PR 阶段就太晚了。 |
| “如果我怀疑每一步就永远发布不了” | 该 skill 适用于非平凡决策，不是每一次按键。重读“When NOT to Use”。 |
| “两个意见总比一个好” | 当第二个意见上下文更少且产生噪声时并非如此。要调和，不要服从。 |
| “审查者不同意，所以我错了” | 审查者缺少你的上下文。分歧是信息，不是裁决。重读 artifact、分类，然后决定。 |
| “Cross-model 总是更好” | Cross-model 能捕捉单模型与自身共享的盲点，但会增加成本和工具脆弱性。在每个交互式 doubt cycle 都提供它，由用户决定 artifact 是否值得。Agent 的职责是呈现选择，而不是把它当闸门。 |
| “用户同意过一次，所以我可以持续调用 CLI” | 每次调用都需要单独授权。Artifact、prompt 和 flags 在调用之间会变化；每次运行前都要重新确认精确命令。 |

## 危险信号

- 为一行重命名或格式化 spawn 全新上下文审查者
- 没有重新阅读 artifact 文本，就把审查者输出当权威
- 循环超过 3 个 cycle 而不升级给用户
- 用“is this good?” 而不是“find issues”来提示审查者
- 在高风险决策上因时间压力跳过 doubt
- 在未修改 artifact 的情况下重新 spawn 全新上下文（你会得到相同发现；这是拖延）
- **Doubt theater（可检查信号）**：连续 2 个或更多 cycle 中，审查者提出了实质发现，但 0 个发现被分类为 actionable。你是在验证，不是在怀疑。停下来并升级。
- 提交后才怀疑，那是 `/review`，不是 doubt-driven development
- 没有与用户确认工具存在、已配置且接受该语法，就硬编码外部 CLI 调用
- **在交互式 doubt cycle 中静默跳过 cross-model。** 即使不推荐，也必须让 offer 可见。跳过可以；静默跳过不行。
- 外部 CLI 报错或缺失时静默 fallback；要呈现失败并让用户重定向
- 从审查者输入中剥离 contract
- 把 CLAIM 传给审查者（会偏向同意）

## 与其他 Skills 的交互

- **`code-review-and-quality` / `/review`**：互补。`/review` 是事后的 PR 裁决；doubt-driven 是进行中的逐决策姿态。两者都用。
- **`source-driven-development`**：SDD 对照官方文档验证*框架事实*。Doubt-driven 验证*你对 artifact 的推理*。SDD 检查 API 是否存在；doubt-driven 检查你是否在契约下正确使用它。
- **`test-driven-development`**：TDD 的 RED 步骤是具体化的怀疑；一个失败测试就是证伪尝试。当 TDD 适用时，该失败测试*就是*行为 claim 的 doubt step。
- **`debugging-and-error-recovery`**：当审查者提出真实失败模式时，进入 debugging skill 来定位并修复。
- **仓库编排规则**（`../../references/orchestration-patterns.md`）：此 skill 从主会话编排。Persona 调用另一个 persona 是反模式 B，见上面的加载约束。

## 验证

应用怀疑驱动开发后：

- [ ] 每个非平凡决策（按上面的定义）在成立前都已明确命名为 CLAIM
- [ ] 每个非平凡 artifact 至少有一次全新上下文审查（TDD 的 RED 步骤产生的失败测试可满足行为 claim 的这一要求，见与其他 Skills 的交互）
- [ ] 审查者收到的是 ARTIFACT + CONTRACT，而不是 CLAIM，也不是你的推理
- [ ] 审查者的 prompt 是对抗式的（“find issues”），不是验证式的（“is it good”）
- [ ] 发现已根据 artifact 文本分类（不是橡皮图章式接受），分类优先级为：contract misread / actionable / trade-off / noise
- [ ] 已满足停止条件（琐碎发现、3 个 cycle，或用户 override）
- [ ] 在交互模式中，已向用户**明确提供** cross-model（无论 artifact 风险如何），并在输出中确认其回应
- [ ] 在非交互模式中，已跳过 cross-model 并声明跳过
- [ ] 任何外部 CLI 调用前，都已完成 PATH 检查、binary 可用性测试、与用户确认语法，并获得明确运行授权
