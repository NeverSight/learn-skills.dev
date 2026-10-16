---
name: code-review-and-quality
description: 执行多维度代码审查。用于合并任何变更之前；用于审查自己、其他 agent 或人类编写的代码；用于在代码进入主分支前从多个维度评估代码质量。
---

# 代码审查和质量

## 概览

带质量门禁的多维度代码审查。每个变更在合并前都必须经过审查，没有例外。审查覆盖五个轴：正确性、可读性、架构、安全性和性能。

**批准标准：** 当一个变更明确改善了整体代码健康度时，就批准它，即使它并不完美。完美代码不存在，目标是持续改进。不要因为它和你自己的写法不完全一致就阻止它。如果它改善了代码库并遵循项目约定，就批准它。

## 何时使用

- 合并任何 PR 或变更之前
- 完成功能实现之后
- 当另一个 agent 或模型产出了你需要评估的代码时
- 重构现有代码时
- 修复任何 bug 之后（同时审查修复和回归测试）

## 五轴审查

每次审查都从这些维度评估代码：

### 1. 正确性

代码是否做了它声称要做的事？

- 是否符合 spec 或任务要求？
- 是否处理了边界情况（null、empty、边界值）？
- 是否处理了错误路径（不只是 happy path）？
- 是否通过所有测试？测试是否真的在测试正确的事情？
- 是否存在 off-by-one 错误、竞态条件或状态不一致？

### 2. 可读性和简单性

另一个工程师（或 agent）能否在作者不解释的情况下理解这段代码？

- 命名是否具有描述性，并与项目约定一致？（没有缺少上下文的 `temp`、`data`、`result`）
- 控制流是否直接清晰（避免嵌套三元表达式、深层 callback）？
- 代码组织是否符合逻辑（相关代码放在一起，模块边界清晰）？
- 是否有应该简化的“聪明”技巧？
- **能否用更少的行数完成？**（100 行足够却写了 1000 行就是失败）
- **抽象是否配得上它带来的复杂度？**（不要在第三个用例之前泛化）
- 注释是否有助于澄清非显而易见的意图？（但不要注释显而易见的代码。）
- 是否存在死代码痕迹：no-op 变量（`_unused`）、向后兼容 shim，或 `// removed` 注释？
- **是不是把一个新增的条件分支硬接到了不相干的流程上？** 这是设计异味，不是小问题（nit），把这段逻辑放进它自己的 helper、state 或 policy 里，别去纠缠已有路径。
- **是否出现了对同一形状反复做条件判断？** 这说明缺少一个模型或 dispatcher。“临时”分支通常是永久债务。

### 3. 架构

这个变更是否适合系统设计？

- 它遵循现有模式，还是引入了新模式？如果是新模式，是否有充分理由？
- 是否保持了清晰的模块边界？
- 是否存在应该共享的代码重复？
- 依赖流向是否正确（没有循环依赖）？
- 抽象层级是否合适（不过度工程化，也不过度耦合）？
- **这次重构是降低了复杂度，还是只是把它挪了个地方？** 数一数读者要跟上这个变更必须同时装进脑中的概念数量。如果所谓“更干净”的版本让这个数量没有变少，它就不干净：优先选择能让整块分支、模式或层消失的重构，而不是把同样的逻辑重新集中到别处。宁可删掉一个抽象，也不要打磨它。
- **功能专属逻辑是否泄漏进了共享或通用模块？** 让逻辑留在它所属的层，复用已有的规范 helper 而不是造一个近似重复品，也不要纵容架构漂移。
- **类型边界是否显式？** 质疑那些随手写下的 `any`/`unknown`/可选类型/类型断言，以及掩盖不清晰不变量的静默 fallback。把边界写明，往往能让周围的控制流更简单。

### 4. 安全性

详细的安全指南见 `security-and-hardening`。这个变更是否引入了漏洞？

- 用户输入是否经过校验和清洗？
- 密钥是否被排除在代码、日志和版本控制之外？
- 需要认证/授权的地方是否做了检查？
- SQL 查询是否参数化（没有字符串拼接）？
- 输出是否做了编码以防 XSS？
- 依赖是否来自可信来源且无已知漏洞？
- 来自外部来源的数据（API、日志、用户内容、配置文件）是否被视为不可信？
- 外部数据流是否在系统边界处先校验，再用于逻辑或渲染？

### 5. 性能

详细的 profiling 和优化指南见 `performance-optimization`。这个变更是否引入了性能问题？

- 有没有 N+1 查询模式？
- 有没有无界循环或不受约束的数据拉取？
- 有没有本该异步的同步操作？
- UI 组件中有没有不必要的重渲染？
- 列表 endpoint 是不是漏了分页？
- 热路径里有没有创建大对象？

## 结构化补救

指出结构性问题时，要给出改法，而不只是问题本身。只说“这太复杂了”的审查会让作者无所适从。要提出有名字的重构方案：

- **用带类型的模型或显式 dispatcher 替换一长串条件判断。**
- **把重复的分支合并成一条更清晰的流程。**
- **把编排与业务逻辑分离**，让两者各自单独可读。
- **把功能专属逻辑移出共享模块**，放进真正拥有这个概念的包（package）。
- **复用规范 helper**，而不是自己写一个近似重复的定制版。
- **把类型边界写明**，让下游的分支随之消失。
- **删掉只是透传的 wrapper**，它增加了间接层却没让 API 更清晰。
- **提取 helper，或把大文件拆成**职责聚焦的模块。

优先选择能减少活动部件的补救方案，而不是把同样的复杂度换个地方摊开的方案。

## 变更规模

小而聚焦的变更更容易审查、更快合并、部署更安全。以下为目标规模：

```
~100 lines changed   → Good. Reviewable in one sitting.
~300 lines changed   → Acceptable if it's a single logical change.
~1000 lines changed  → Too large. Split it.
```

**盯文件总大小，而不只是 diff 大小。** 一个小 diff 仍可能把某个文件推过健康边界：单个文件约 1000 *总*行数是常见的审视信号（区别于上面约 1000 *变更*行的阈值），但也不是硬性上限。当一个变更显著增大了本已很大的文件时，先问要不要提取 helper、子组件或模块，再往上堆代码。先分解，再添加。

**什么算“一个变更”：** 一个自包含的修改，只解决一件事，附带相关测试，提交后系统保持可用。是功能的一个组成部分，不是整个功能。

**变更太大时的拆分策略：**

| 策略 | 做法 | 适用时机 |
|----------|-----|------|
| **堆叠（Stack）** | 先提交一个小变更，下一个基于它继续 | 存在顺序依赖 |
| **按文件分组** | 为需要不同 reviewer 的文件组各开一个变更 | 横切关注点 |
| **水平切分** | 先写共享代码/stub，再写消费方 | 分层架构 |
| **垂直切分** | 把功能拆成更小的全栈切片 | 功能开发 |

**大变更何时可以接受：** 完整的文件删除，以及 reviewer 只需确认意图、无需逐行核对的自动化重构。

**重构和功能开发要分开。** 一个既改现有代码又加新行为的变更其实是两个变更，分开提交。小的清理（如变量重命名）可由 reviewer 酌情允许带入。

## 变更描述

每个变更都需要一段能在版本控制历史中独立读懂的描述。

**第一行：** 短、祈使语气、可独立理解。用 “Delete the FizzBuzz RPC”，不要用 “Deleting the FizzBuzz RPC.”。信息量要足够让搜索历史的人不必读 diff 就能明白这个变更。

**正文：** 改了什么、为什么改。包含代码本身看不到的上下文、决策和推理。相关的地方链接 bug 编号、benchmark 结果或设计文档。做法有缺陷时也要坦承。

**反模式：** “Fix bug”、“Fix build”、“Add patch”、“Moving code from A to B”、“Phase 1”、“Add convenience functions”。

## 审查流程

### 第 1 步：理解上下文

看代码之前，先理解意图：

```
- What is this change trying to accomplish?
- What spec or task does it implement?
- What is the expected behavior change?
```

### 第 2 步：先审查测试

测试揭示意图和覆盖面：

```
- Do tests exist for the change?
- Do they test behavior (not implementation details)?
- Are edge cases covered?
- Do tests have descriptive names?
- Would the tests catch a regression if the code changed?
```

### 第 3 步：审查实现

带着五个轴逐一走查代码：

```
For each file changed:
1. Correctness: Does this code do what the test says it should?
2. Readability: Can I understand this without help?
3. Architecture: Does this fit the system?
4. Security: Any vulnerabilities?
5. Performance: Any bottlenecks?
```

### 第 4 步：给发现分级

每条评论都要标注严重程度，让作者分清哪些必改、哪些可选：

| 前缀 | 含义 | 作者如何处理 |
|--------|---------|---------------|
| *(no prefix)* | 必改 | 合并前必须解决 |
| **Critical:** | 阻塞合并 | 安全漏洞、数据丢失、功能损坏 |
| **Nit:** | 次要、可选 | 作者可以忽略：格式、风格偏好 |
| **Optional:** / **Consider:** | 建议 | 值得考虑，但非必须 |
| **FYI** | 仅供参考 | 无需行动：留作日后参考的上下文 |

这能防止作者把所有反馈都当成必须处理的，在可选建议上浪费时间。

**把真正重要的放在最前面。** 按影响力给发现排序：先正确性和安全，再结构性回退和错过的简化机会，再是其他所有。不要把真问题埋在一堆外观类 nit 下面：几条高置信度的评论胜过一长串清单。如果你发现了一个结构性问题和十个 nit，那个结构性问题*就是*这次审查的核心。

### 第 5 步：核查验证情况

检查作者的验证叙事：

```
- What tests were run?
- Did the build pass?
- Was the change tested manually?
- Are there screenshots for UI changes?
- Is there a before/after comparison?
```

## 多模型审查模式

用不同的模型承担不同的审查视角：

```
Model A writes the code
    │
    ▼
Model B reviews for correctness and architecture
    │
    ▼
Model A addresses the feedback
    │
    ▼
Human makes the final call
```

这能抓住单个模型可能漏掉的问题，因为不同模型的盲区不一样。

**审查 agent 的示例 prompt：**
```
Review this code change for correctness, security, and adherence to
our project conventions. The spec says [X]. The change should [Y].
Flag any issues as Critical, Required, Optional, or Nit.
```

## 死代码卫生

任何重构或实现变更之后，检查是否有孤立代码：

1. 找出现在已不可达或不再使用的代码
2. 明确列出来
3. **删除前先问：** “这些元素现在已经不再使用，要删除吗：[list]？”

不要把死代码留在原地，它会迷惑后来的阅读者和 agent。但也不要悄悄删掉自己拿不准的东西。拿不准就问。

```
DEAD CODE IDENTIFIED:
- formatLegacyDate() in src/utils/date.ts — replaced by formatDate()
- OldTaskCard component in src/components/ — replaced by TaskCard
- LEGACY_API_URL constant in src/config.ts — no remaining references
→ Safe to remove these?
```

## 审查速度

审查慢了会阻塞整个团队。切换到审查所付出的上下文切换成本，低于让别人等待的成本。

- **在一个工作日内响应**：这是上限，不是目标
- **理想节奏：** 收到审查请求后尽快响应，除非正处于深度专注编码中。一个典型变更应在一天内完成多轮审查
- **优先保证每轮回复快**，而不是快速给出最终批准。快速反馈即使需要多轮，也能减少挫败感
- **大型变更：** 请作者拆分，而不是硬审一坨巨大的 changeset

## 处理分歧

解决审查争议时，遵循这个层级：

1. **技术事实和数据**优先于观点和偏好
2. **风格指南**是风格问题的最高权威
3. **软件设计**必须依据工程原则评估，而不是个人偏好
4. **代码库一致性**在不损害整体健康度的前提下可以接受

**不要接受“我之后再做清理”。** 经验证明，推迟的清理几乎不会发生。除非真是紧急情况，否则要求提交前完成清理。如果周边问题确实无法在本次变更中解决，要求提一个 bug 并指派给自己。

## 审查中的诚实

审查代码时，无论代码出自你、另一个 agent 还是人类之手：

- **不要走过场盖章。** 没有审查证据的 “LGTM” 对谁都没好处。
- **不要淡化真问题。** 明明是会打穿生产的 bug，却说是“一个小顾虑”，这是不诚实。
- **尽量量化问题。** “这个 N+1 查询会让列表里每项多出约 50ms” 比 “这可能有点慢” 好得多。
- **对确有问题的方案要顶回去。** 谄媚是审查中的失败模式。实现有问题就直说，并给出替代方案。
- **优雅地接受否决。** 如果作者掌握完整上下文并坚持己见，尊重他的判断。评论针对代码而不是人：把对个人的批评改写为对代码本身的意见。

## 依赖纪律

代码审查的一部分就是依赖审查：

**添加任何依赖之前：**
1. 现有技术栈能解决这个吗？（通常能。）
2. 这个依赖有多大？（检查对 bundle 的影响。）
3. 它还在积极维护吗？（查看最近提交、未解决 issues。）
4. 它有已知漏洞吗？（`npm audit`）
5. 许可证是什么？（必须与项目兼容。）

**规则：** 优先使用标准库和现有工具，而不是新依赖。每个依赖都是一项负债。

**升级现有依赖**和其他代码变更一样是代码变更，而风险最高的恰恰是那种以 “bump deps” 一笔带过、批量合并的升级。审查它们要拿出同样的纪律：

1. **读 changelog，不要只看版本号。** semver 只是维护者未必兑现的承诺：“patch” 也可能带着行为变化。大版本升级要读迁移说明，找出哪里会断。
2. **一个变更只升一个依赖。** 逐个（或按小的相关分组）升级并合并。批量 bump 弄坏构建时，你已经不知道是哪个包干的；单包变更让原因显而易见、回滚干净利落。
3. **让测试说话。** 升级的验证依据是升级前后都全绿的测试套件，而不是“装上了”。如果依赖行为周围的覆盖很薄，这个缺口才是真正的发现：先补测试。
4. **留意传递依赖图。** 大多数装进来的包并不是谁直接选的。审查 lockfile 的 diff，而不只是 `package.json`：一个直接依赖的 bump 可能牵出几十个间接变化。
5. **保持 lockfile 诚实。** 提交它、审查它的 diff、绝不手改。真正钉住发布内容的是 lockfile。

对 `npm audit` 结果和供应链风险（typosquatting、被攻陷的维护者）的分级处置，遵循 `security-and-hardening` skill：本节覆盖的是升级*工作流*，那一节给出的是安全结论。

## 审查 Checklist

```markdown
## Review: [PR/Change title]

### Context
- [ ] I understand what this change does and why

### Correctness
- [ ] Change matches spec/task requirements
- [ ] Edge cases handled
- [ ] Error paths handled
- [ ] Tests cover the change adequately

### Readability
- [ ] Names are clear and consistent
- [ ] Logic is straightforward
- [ ] No unnecessary complexity

### Architecture
- [ ] Follows existing patterns
- [ ] No unnecessary coupling or dependencies
- [ ] Appropriate abstraction level
- [ ] Refactors reduce complexity rather than relocate it
- [ ] No feature logic in shared modules; file stays within a healthy size

### Security
- [ ] No secrets in code
- [ ] Input validated at boundaries
- [ ] No injection vulnerabilities
- [ ] Auth checks in place
- [ ] External data sources treated as untrusted

### Performance
- [ ] No N+1 patterns
- [ ] No unbounded operations
- [ ] Pagination on list endpoints

### Verification
- [ ] Tests pass
- [ ] Build succeeds
- [ ] Manual verification done (if applicable)

### Verdict
- [ ] **Approve** — Ready to merge
- [ ] **Request changes** — Issues must be addressed
```
## 另见

- 详细的安全审查指南，见 `../../references/security-checklist.md`
- 性能审查检查项，见 `../../references/performance-checklist.md`

## 常见自我合理化

| 自我合理化 | 现实 |
|---|---|
| “能跑就够了” | 能跑但不可读、不安全或架构错误的代码，会积累复利式的技术债。 |
| “我写的，所以我确定没问题” | 作者对自己的假设是盲的。每个变更都需要另一双眼睛。 |
| “之后会清理的” | “之后”永远不会来。审查就是质量门禁，用它。要求合并前完成清理，而不是合并后。 |
| “AI 生成的代码应该没问题” | AI 代码需要更多审视而不是更少。它就算错了也表现得自信而可信。 |
| “测试过了，所以是好的” | 测试必要但不充分。它们抓不到架构问题、安全隐患或可读性问题。 |
| “重构让它更干净了” | 挪动复杂度不等于减少复杂度。如果读者仍需同时掌握同样多的概念，结构并没有改善：去找那个能让分支消失的版本。 |
| “只是给这个文件加了一小段” | 小 diff 仍会把文件推过健康大小、把分支硬接到不相干的流程上。评判的是最终结构，不是 diff 大小。 |
| “只是升个版本号” | 升级是你没写出来的行为变化。读 changelog：semver 不保证不破坏。 |
| “全部放一个 PR 里升级省时间” | 会弄坏构建的批量 bump 藏起了肇事包。一个变更一个依赖，原因和回滚才都干净。 |

## 危险信号

- 未经任何审查就合并 PR
- 只检查测试是否通过的审查（忽略其他轴）
- 没有实际审查证据的 “LGTM”
- 涉及安全的变更没有做面向安全的审查
- “大到没法好好审”的大 PR（拆了它）
- bug 修复 PR 没有附带回归测试
- 审查评论不带严重程度标签：分不清哪些必改、哪些可选
- 接受“我之后会修”：那不会发生
- 只是搬动了代码、却没有减少读者必须掌握的概念数量的重构
- 让本已很大的文件继续膨胀、而不是先做分解的变更
- 把新条件分支散落到不相干的代码路径里（缺失抽象的信号）
- 重复造轮子的定制 helper，与已有规范 helper 近似重复，或功能逻辑放进了共享模块
- 批量 “bump dependencies” PR：没读 changelog，也没按包隔离
- 手改的、未提交的、或未经 diff 审查就合并的 lockfile 变更

## 验证

审查完成后：

- [ ] 所有 Critical 问题已解决
- [ ] 所有必改（无前缀）项已解决，或有明确理由的显式延期
- [ ] 测试通过
- [ ] 构建成功
- [ ] 验证叙事已记录（改了什么、如何验证的）
- [ ] 依赖升级已对照 changelog 审查、按包隔离，并由升级前后全绿的测试套件验证，lockfile diff 也已审查

**推定阻塞项（presumptive blockers）：** 对下列每一项，提出来并给出更简单的设计；仅当变更确实在恶化结构时，才升级为必改（Required）：只是挪动复杂度而非减少它的重构；把文件推过大小边界却没有做分解的变更；往共享模块里添加功能逻辑；与已有规范 helper 近似重复；掩盖不清晰不变量的静默 fallback。
