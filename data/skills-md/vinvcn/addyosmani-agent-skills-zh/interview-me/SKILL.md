---
name: interview-me
description: 挖掘用户真正想要的东西，而不是他们觉得自己“应该”要的东西。实现方式是一次一问的访谈，直到对底层意图达到约 95% 的置信度。当一个请求信息不全时（"build me X" 却没说 "for whom" 或 "why now"）、当用户明确发出邀请（"interview me"、"grill me"、"are we sure?"、"stress-test my thinking"）、或者当你在任何 plan、spec 或代码存在之前发现自己悄悄补全着含糊的需求时，使用它。
---

# 访谈我（Interview Me）

## 概览

人们开口要的东西和他们真正想要的东西，是两回事。他们要“一个 dashboard”，是因为那是人们会去要的东西，而不是因为 dashboard 能解决他们的问题。他们说“再快一点”，却没有一个要达到的数字。

发现这个落差最便宜的时刻，是在任何 plan、spec 或代码存在之前。一旦你开始构建，切换成本就是真实的，用户会把错误的东西合理化成“够用的”东西。错配就此被锁死。

这个 skill 在落差造成任何代价之前把它合上。Define 阶段的其他 skill 都假定你已经大致知道要什么：`idea-refine` 从一个想法生成变体，`spec-driven-development` 把需求写下来，`doubt-driven-development` 在你起草完一个计划之后对它做压力测试。Interview-me 是所有这些之前的那一步：你一次问一个问题、每个问题附上你的最佳猜测，直到能在用户开口之前预测到他会说什么。

## 何时使用

在以下情况应用这个 skill：

- 这个请求至少缺一项：**谁**是用户、**为什么**想要它、**成功**长什么样、那个有约束力的**限制条件**是什么
- 请求是惯例式的而非具体的（"build me X"、"make it faster"），而你不动脑筋就无法拆解这个惯例
- 你蠢蠢欲动，想用没有摆到台面上的假设直接开工
- 当两个都合理的价值取向相互冲突时（简单 vs. 灵活、成本 vs. 速度），用户还没说他在优化哪一个
- 用户明确发出邀请："interview me"、"grill me"、"before we start, are we sure?"、"stress-test my thinking"

**何时不要使用：**

- 请求明确且自包含（"rename this variable"、"fix this typo"）
- 用户已明确要求速度优先于验证
- 纯信息类请求（"how does X work?"、"what does this code do?"）
- 机械操作（重命名、格式化、移动文件）
- 你已经有 ≥95% 的置信度；重读下面的停止条件，再假定你没有

## 加载约束

这个 skill 需要一个在线、会回应的用户。**不要在非交互上下文中调用**，比如 CI pipeline、定时运行、`/loop` 或自主循环。如果你在其中之一里且请求信息不全，把这个事实标记为用户的 blocker，而不是靠猜。

## 流程

### Step 1: 提出假设，附上置信度数字

在问任何问题之前，用**一句话**写下你对用户想要什么的当前最佳解读，外加一个诚实的置信度数字（0–100%）：

```
HYPOTHESIS: You want a way to answer "how are we doing?" in standup, and "dashboard" was the convention that came to mind.
CONFIDENCE: ~30% — missing: who it's for, what "metrics" means in context, and what success looks like
```

这个数字逼你诚实。如果你写下一个高数字，却根本预测不了用户对你接下来三个问题的反应，那这个数字就是错的。从你能自圆其说的置信度开始。

当置信度低于约 70% 时，在同一行追加一句简短的理由——还有什么悬而未决或缺失。这准确地告诉用户访谈需要浮现什么，也防止这个数字变成一个含糊的信号。

### Step 2: 一次问一个问题，每个都附上猜测

格式：

```
Q: <one focused question>
GUESS: <your hypothesis for the answer, with the reasoning that produced it>
```

等用户回应之后再问下一个问题。

**为什么一次一个，而不是一批：**

- 如果把猜测埋进一个列表，用户就没法对你的猜测做出回应
- 成批发问鼓励扫读和浮于表面的回答
- 第三个问题往往取决于第一个问题的答案；一口气全问出来会锁死错误的框架
- 用户认真思考的精力有限；一次一个问题地花掉它

**为什么附上猜测：**

- 用户纠正一个错误猜测，比从零生成一个答案快得多
- 它逼你给出一个会 visibly 出错的假设，这让你保持诚实
- 它浮现的是*你的*假设，而这正是访谈要暴露的东西

这里的风险是一个礼貌的用户为了配合而附和你的猜测。缓解方式：表现出你愿意出错，并且偶尔往你预期用户会反驳的方向猜。

### Step 3: 留意“想要”vs.“应该想要”

最危险的答案，是那些用户说出一个“显得有深度的答案长什么样”而不是他们真正想要的东西的答案。留意：

- 套用最佳实践话术的答案（"I want it to be scalable"、"clean architecture"），没有具体内容
- 推给惯例的答案（"the way most apps do it"、"the standard approach"）
- 类似 "I should probably…"、"I think I'm supposed to…"、"good engineering practice says…" 的措辞
- 把流行词当目标——当 "modern"、"scalable"、"robust" 本身就是答案，而不是一个具体结果

当你听到这些，该问的问题是：

> *“如果你不需要向任何人证明这件事的合理性，你真正想要的是什么？”*

这一个问题，常常比前面五个问题做的功还多。

### Step 4: 用用户自己的话复述意图

当你的置信度够高时，把你现在认为用户想要的东西写回去。保持紧凑（5–8 行），尽量使用用户的语言，并组织结构让用户可以逐行确认或纠正：

```
Here's what I now think you want:

- Outcome:      <one line>
- User:         <one line — who benefits>
- Why now:      <one line — what changed>
- Success:      <one line — how we know it worked>
- Constraint:   <one line — the binding limit>
- Out of scope: <one line — what we're explicitly not doing>

Yes / no / refine?
```

包含 "Out of scope" 没有商量余地。一半的目标偏差，来自关于*不*构建什么的心照不宣式分歧。

### Step 5: 确认——要明确的 yes，不是“你觉得啥好就啥好”

门槛是一个明确的 "yes"。以下都**不**算 yes：

- "Whatever you think is best." → 用户在放权，意味着他自己也没有 95% 的置信度。把问题换成两个具体选项、以选择题的形式重新问。
- "Sounds good." → 含糊。追问："有什么你想再调整的吗？"沉默不是确认。
- "Sure, let's go." → 往往是礼貌地结束对话，不是背书。同样追问。
- 沉默之后接一句 "okay let's start." → 用户是放弃了这场访谈，不是达成了共识。停下来，问问是不是你漏了什么。

如果用户纠正你，把纠正折进去再复述一遍。循环，直到你拿到一个明确的 yes。

### 95% 置信度停止条件

当你能够对这个问题回答 yes 时，就结束了：

> *我能不能预测用户对我接下来要问的三个问题的反应？*

如果能，你就拥有了共享理解。停止访谈，产出复述。如果不能，你还没结束；问下一个问题。

这是一个可检验的测试，不是一种感觉。它还有一个下限：如果你问了好几轮仍然无法预测，那是关于这个请求的信息，而不是继续硬磨的理由。停下来告诉用户："我已经问了 X 个问题，还是预测不了你的反应。有某个根本性的东西缺失了。我们要不要退一步？"

## 输出

这个 skill 的输出是一个**经过确认的意图陈述**：Step 4 的复述，加上 Step 5 拿到的明确 yes。这就是交付物。Spec、计划和任务清单都是下游；它们消费这个 skill 产出的意图。

如果用户希望这个意图能持久（一个跨多个 session 的项目、交接给另一个协作者），主动提出保存到 `docs/intent/[topic].md`。只在用户确认后才保存。

## 示例

一个简短的前后对比。

**没有 `interview-me`：**

```
User:  build me a dashboard for our metrics
Agent: <starts proposing chart libraries and layouts>
```

这个 agent 已经默认假设了：给谁用、什么指标、"for our team" 是什么意思、成功长什么样。这些一个都没被说出来。每一个假设都是用户日后说“这不是我的意思”的地方。

**有 `interview-me`：**

```
User: build me a dashboard for our metrics

Agent:
HYPOTHESIS: You want a way to answer "how are we doing?" in standup, and "dashboard" came to mind because that's the conventional answer.
CONFIDENCE: ~30% — missing: who it's for, what "metrics" are, and what success looks like

Q:     When you say "how are we doing?", who's asking — you alone, the engineering team in standup, or up the chain (e.g., your manager, an exec, a board)?
GUESS: engineering team in standup, because "we" usually scopes that way and standups are where this question gets asked. If it's for execs the metrics and the framing change a lot.

User: It's actually for me. I keep losing track of which experiments are running and what their early signal looks like.

Agent:
Updated read: not a team dashboard at all. It's a personal experiment tracker. Confidence: ~60% — still missing: what "early signal" means and what done looks like.

Q:     Is the gap that you don't know which experiments exist, or that you can't see their results in one place?
GUESS: the second one. You have a list of experiments somewhere, but their results live in five different tools, and reconciling them by hand is what you're tired of.

User: First one actually. I literally don't have a list. They're spread across different docs.

Agent: <continues>
```

两个问题之后，agent 发现真正的请求不是 "a dashboard"，而是 "a list"。不同的交付物、不同的范围、不同的工作量。做 dashboard 会是错的。

## 与其他 skill 的关系

- **`idea-refine`**：下游。如果确认后的意图是 "I want X but I don't know how to scope it"，交接给 `idea-refine`，针对已经明确的意图生成变体。
- **`spec-driven-development`**：下游。如果确认后的意图是具体的（"I want X for Y users with Z success criteria"），交接给 `spec-driven-development` 把它写下来。
- **`planning-and-task-breakdown`**：在本 skill 下游两跳（spec 之后）。
- **`doubt-driven-development`**：时间轴的另一端。Interview-me 是决策前的意图挖掘；doubt-driven 是决策后的成品审查。两者都捕捉偏差，但在不同的时刻。
- **`source-driven-development`**：正交。Interview-me 澄清用户想要什么；SDD 验证框架事实。两者不构成竞争。

## 常见合理化借口

| 合理化借口 | 现实 |
|---|---|
| "请求够清楚了" | 如果你此刻没法用一句话写出用户想要的结果，那请求就不清楚。先做 Step 1 再下判断。 |
| "问太多问题浪费他们的时间" | 4–6 个有针对性的问题浪费的时间很小。构建错误的东西浪费的时间是巨大的，而且这个成本由用户本人承担。 |
| "边做边就明白了" | 代码存在之后的切换成本是现在的 10 倍。实现期的发现就是返工。 |
| "他们说了‘你觉得啥好就啥好’，所以我直接定就行" | "Whatever you think" 是放权，不是决策。用两个具体选项、以选择题的形式重新问。 |
| "我应该给他几个选项挑" | 当用户知道自己要什么、只是在权衡取舍之间做选择时，选项才有效。他还不知道自己要什么。列选项是在扩大搜索；提问是在收窄搜索。 |
| "附上我的猜测，就是在引导他们" | 引导正是重点。回应比从零生成快。风险是谄媚，不是引导；用“表现出愿意出错”来缓解。 |
| "聊得够多了，我懂了" | 验证一下：你能预测他对接下来三个问题的反应吗？如果不能，你还没懂。 |
| "用户说了 yes，结束了" | 如果这个 yes 出现在一次含糊的复述或一句开放的 "sounds good" 之后，这个 yes 是空的。具体地复述，再确认一次。 |

## 危险信号

- 一条消息里出现三个或更多问题：那是批发提问，不是访谈
- 一个问题没附上你的假设：那是做 survey，不是在下注
- 把 "whatever you think is best" 当成最终答案接受下来
- 在用户明确确认你的复述之前，就产出 spec、计划或任务清单
- 用 "what would be best practice?" 而不是 "what do you actually want?" 来框架问题
- 用户给出一个彰显品味/资历的答案（"scalable"、"clean"、"modern"），你不追问这是否是他真正想要的就接受了
- 三轮过后你的置信度没有可见的上升：你在问错问题，退一步重新框架
- 低于约 70% 的置信度数字没有附上理由：用户不知道缺口在哪，就帮不上忙
- 在用户确认之前就保存意图文档（这份文档本身就暗示了一个用户没给过的 yes）
- 在复述里省略 "Out of scope" 那一行（关于非目标的心照不宣式分歧，是一半目标偏差的来源）

## 验证

应用 interview-me 之后：

- [ ] 在第一轮就陈述了一个明确的假设和置信度数字
- [ ] 每个低于约 70% 的置信度数字都附了一行理由（还有什么悬而未决或缺失）
- [ ] 问题是一次一个问的，每个都附上 agent 的猜测
- [ ] 当用户给出彰显资历或套用惯例的答案时，至少进行了一次“如果你不需要证明它的合理性，你真正想要什么？”的探查
- [ ] 一次具体的复述（Outcome / User / Why now / Success / Constraint / Out of scope）被写回给了用户
- [ ] 用户用明确的 yes 确认了复述（不是 "whatever you think"，不是 "sounds good"，不是沉默）
- [ ] 在停止点上，agent 能预测它对接下来三个问题的反应
- [ ] 任何向下游 skill（`idea-refine`、`spec-driven-development`）的交接，都是以确认后的意图来表述的，而不是最初那个信息不全的请求
