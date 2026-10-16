---
name: constraint-driven-development
description: 把一个项目的质量线确立为书面契约，并阻止 agent 悄悄降低它。通过访谈确定用户在意哪些维度，当用户心里没有数字时提供合理的默认阈值，把一切记录进 CONSTRAINTS.md，并盯住 diff 中质量线被削弱的迹象——新增的 @ts-ignore 或 eslint-disable 抑制注释、被跳过或删除的测试、被剥掉的断言、未实现的 stub、被调低的阈值。当没有任何质量线被写下来时使用；当用户说 "set up constraints" 或 "define our standards" 时；当用户希望把他们在意的维度——无障碍性、Web 性能、覆盖率——设置成被强制执行的约束时；当 agent 为了变绿不断静默检查或跳过测试时；当你需要一个覆盖率或性能阈值却不知道该选什么数字时；或者当 agent 写下的代码超出任何人会读的体量时。
---

# 约束驱动开发

## 概览

本技能包里的其他 skill 描述的是“好”长什么样。`code-review-and-quality` 给你五个轴。`test-driven-development` 给你一个循环。`security-and-hardening` 给你一份威胁清单。所有这些都活在文字里，agent 读了可能照做也可能不照做，而且没有一个能活过会话结束。

这个 skill 产出的是别的东西：**本项目**质量线的书面记录，带数字，能活过对话，并且可以被机械地检查。

背后的原因很重要。当你亲手写代码时，读代码就能告诉你它好不好。一个 agent 一个下午写下的代码超出你一周能读完的量，于是判断就从你的脑子里挪到了围绕循环运行的检查里。这些检查需要存在，需要用到你真正选过的数字，而且需要离工作足够近，让 agent 能修好自己的产出。

Spec-driven development 说清楚要构建什么。Test-driven development 证明它能工作。Constraint-driven development 定义“好到可以发布”意味着什么——在任何人在 pull request 里为此争吵之前。

## 何时使用

在以下情况应用这个 skill：

- 启动一个项目或一个重要功能，而没有任何质量线被写下来
- 用户要求 "set up constraints"、"add quality gates"、"define our standards" 或 "stop the agent shipping junk"
- Agent 在产出没人逐行阅读的体量
- CI 有检查，但没人说得清哪些会阻塞合并、哪些只是摆设
- 覆盖率、性能或无障碍性的数字在每个 PR 上被争论，而不是被一次性决定
- 你正准备运行 `/build auto` 或任何自主循环，而它和 main 之间唯一的屏障是一套 agent 自己写的测试

**何时不要使用：**

- 项目已经有 `CONSTRAINTS.md` 而用户并不想改它——去读它并遵循它
- 一次性脚本、spike、用完即弃的原型
- 用户现在就要 code review（`code-review-and-quality`）或要搭 CI pipeline（`ci-cd-and-automation`）
- product-market fit 之前的代码，预期寿命两周——下面的 floor 仍然值得，其余的不值得

## 加载约束

这场访谈需要一个活的用户。**不要在非交互上下文中运行它**（CI、`/loop`、自主运行）。如果你在其中之一里且约束缺失，套用下面的 Floor，注明你这样做了，并把剩下的标记出来交给人来处理。

## 流程

### Step 1: 先检测，再提问

能读到的东西绝不要问。在第一个问题之前，先收集：

| 看什么 | 去哪看 |
|------|---------------|
| 语言与技术栈 | `package.json`、`pyproject.toml`、`go.mod`、`Cargo.toml` |
| 测试 runner | dev 依赖、`test` script、已有的测试文件 |
| 已有的 linter | `eslint.config.*`、`biome.json`、`.ruff.toml` |
| 当前覆盖率 | `coverage/` 输出，或把套件跑一遍 |
| CI | `.github/workflows/`、`.gitlab-ci.yml` |
| Agent harness | `.claude/`、`.codex/`、`AGENTS.md` |

用两行汇报你发现的东西，然后只问剩下的。

### Step 2: 四个问题，每个都带默认值

遵循 `interview-me` 的一次一问纪律，只有一个变化：这里的每个问题都有默认值，所以 "I don't know" 也是一个完整的答案，并且仍能产出可用的配置。

```
Q1: Beyond the floor, which of these do you want enforced?
    (a) Test coverage on new code
    (b) Security scanning
    (c) Performance budgets
    (d) Accessibility
    (e) Architecture boundaries
GUESS: (a) and (b) — you have a test runner already and you're handling user input.
DEFAULT if unsure: (a) and (b).
Say what each pick costs: (c) and (d) need a running URL, (e) needs a rules file written.
```

```
Q2: When a check fails while the agent is mid-task, should it block or warn?
GUESS: Block. You're running agents unattended and a warning nobody reads is a warning.
DEFAULT if unsure: Block on the floor, warn on everything else for the first two weeks.
```

```
Q3: Do you have target numbers in mind, or should I measure where you are today and hold that line?
GUESS: Measure. Most teams don't have a number, and an invented one gets ignored.
DEFAULT if unsure: Measure and hold. See "Ratchets" below.
```

```
Q4: What's the slowest check you'll tolerate before the agent hands work back?
GUESS: About 90 seconds. Longer and you'll stop running it.
DEFAULT if unsure: 90 seconds at task end, unlimited in CI.
```

止步于四个。一个十二问的 intake 产出的是一份没人理解的配置和一个后悔开始的 user。

### Step 3: 写出 CONSTRAINTS.md

仓库根目录放一个文件。任何 harness 上的任何 agent 都能读它，而它的一次变更会出现在 review 里——它本该在的地方。

```markdown
# Constraints

Last reviewed: 2026-08-08 by @addy

## Floor (always enforced, no setup required)

- No new suppression comments: `@ts-ignore`, `eslint-disable`, `# noqa`, `# type: ignore`
- No unimplemented stubs: `throw new Error("Not implemented")`, empty `catch {}`
- No skipped or deleted tests without a reason in the commit message
- No secrets in source
- This file does not get weakened to make a change pass

## Enforced with numbers

| Dimension | Rule | Checked by | Runs at |
|-----------|------|-----------|---------|
| Types | Zero type errors | `tsc --noEmit` | every edit |
| Lint | Zero errors from our config | `biome check` | every edit |
| Secrets | No secrets in source | `gitleaks detect --redact` | every edit |
| Coverage | Changed lines ≥ 80% covered | `vitest run --coverage` + git diff | task end, CI |
| Security: code | No high findings | `semgrep scan --config p/default` | CI |
| Security: deps | Nothing at high or above | `osv-scanner scan source -r .` | CI |
| Accessibility | Zero critical or serious | `axe $PREVIEW_URL --tags wcag2a,wcag2aa,wcag21aa` | preview deploy |
| Performance | LCP ≤ 2500ms, CLS ≤ 0.1 | `lighthouse $PREVIEW_URL --output=json` | preview deploy |

Every row names the command that produces the verdict. A dimension with a
number and no command in this column is an aspiration, not a constraint.

## Measured, not yet enforced

| Metric | Today | Direction |
|--------|-------|-----------|
| Project coverage | 62.4% | must not fall |
| Bundle size (main) | 184 kB | must not grow |

## Exceptions

| ID | Rule | Path | Reason | Owner | Expires |
|----|------|------|--------|-------|---------|
| W1 | `no-explicit-any` | `src/legacy/**` | Rewrite tracked in ENG-441 | @addy | 2026-11-01 |
```

然后在 `AGENTS.md` 和 `CLAUDE.md` 各加一行：`Read CONSTRAINTS.md before writing code. Do not weaken it to make a change pass.`

### Step 4: 为每个维度安装它需要的东西

选择一个维度就意味着安装一些东西。别给用户留下一个数字却没有机制，也别在有事实标准工具时凭空发明你自己的 checker——这里列出的工具之所以入选，是因为它们的规则格式和阈值就是整个生态所对准的目标，所以团队已有的配置会继续有效。

| 维度 | 工具 | 安装 | 运行 | 拦截条件 |
|-----------|------|---------|-----|---------|
| 类型 (TS) | tsc | 已内置 | `tsc --noEmit` | 任何错误 |
| 类型 (Python) | mypy | `pip install mypy` | `mypy .` | 任何错误 |
| Lint | 你已有的配置 | 已内置 | `eslint .` / `biome check` / `ruff check` | 任何错误 |
| 覆盖率 (JS) | 你的 test runner | 已内置 | `vitest run --coverage`（或 `jest --coverage`） | 变更行的覆盖率 |
| 覆盖率 (Python) | pytest-cov | `pip install pytest-cov` | `pytest --cov --cov-report=lcov` | 同上 |
| Security: 代码 | Semgrep | `pipx install semgrep` | `semgrep scan --config p/default --config p/owasp-top-ten` | 任何 high finding |
| Security: secrets | gitleaks | `brew install gitleaks` | `gitleaks detect --redact --no-banner` | 任何 finding |
| Security: 依赖 | osv-scanner | `brew install osv-scanner` | `osv-scanner scan source -r .` | high 及以上 |
| 性能: 页面 | Lighthouse | `npm i -D lighthouse` | `lighthouse $URL --output=json --quiet` | LCP、CLS、performance score |
| 性能: bundle | size-limit | `npm i -D size-limit` | `size-limit --json` | 每个 entry 的字节预算 |
| 无障碍性 | axe-core | `npm i -D @axe-core/cli` | `axe $URL --tags wcag2a,wcag2aa,wcag21aa` | critical 或 serious 为零 |
| 架构 | dependency-cruiser | `npm i -D dependency-cruiser` | `depcruise --validate src` | 任何违规 |
| 断言质量 | Stryker | `npm i -D @stryker-mutator/core` | `stryker run --mutate <changed files>` | mutation score |

跳过下面五件事，它们会反咬你一口：

1. **gitleaks 的 `--redact` 不是可选的。** 没有它，被匹配到的 secret 会落入 agent 的 transcript——这正是泄露的 key 进入日志、summary 或 commit message 的路径。报告规则和位置，绝不报告值。
2. **Lighthouse 和 axe 需要一个 URL。** 它们只能对运行中的应用生效，所以它们属于 runtime 阶段，对准一个 preview deploy 或你先启动的本地 server。如果项目没有可访问的 URL——CLI、库、桌面应用——说清楚，然后砍掉这个维度，而不是发明一个跑不起来的检查。
3. **把贵的检查限定在 diff 上。** 对整个仓库跑 `stryker run --mutate` 要几个小时，然后就会被人关掉；只跑一次变更触及的文件不到一分钟。Semgrep 也一样，它接受一个路径列表。
4. **覆盖率不需要第二次 test run。** 读你的套件已经在写的 lcov，把它和 `git diff` 求交集。为了拿一个数字而把套件跑两遍，是让人最快开始憎恨这件事的办法。
5. **Semgrep 注册表里的规则可以免费运行；再分发之前先看 licence。** 如果这关系到你的法务团队，`opengrep` 是一个 drop-in fork，规则格式和 JSON output 相同。

把每一个都加进项目自己的 script，让它在没有 agent 的情况下也可复现：

```json
{
  "scripts": {
    "check:fast": "tsc --noEmit && eslint . && gitleaks detect --redact --no-banner",
    "check:task": "npm run check:fast && vitest run --coverage",
    "check:full": "npm run check:task && semgrep scan --config p/default && osv-scanner scan source -r ."
  }
}
```

这个映射比工具本身更重要。`check:fast` 是每次编辑之后运行的，`check:task` 是 agent 自以为完成时运行的，`check:full` 在 CI 里运行。

这些命令现在住在两个地方——`CONSTRAINTS.md` 的 `Checked by` 列，和这些 scripts。`CONSTRAINTS.md` 是权威来源：它把理由随每条命令一起承载，而且它会出现在 review 里。这些 scripts 是必须与它保持一致的便捷包装，不是第二个权威来源；一旦漂移，以文件为准。

### Step 5: 把它接到生命周期上

最大的单一错误就是在所有地方运行所有东西。一个会拖慢 agent 的检查会被关掉，而被人关掉的 gate 比没有 gate 更糟，因为质量线看起来仍然存在。

| 阶段 | 命令 | 运行什么 | 预算 |
|-------|---------|-----------|--------|
| BUILD | `/build` | 类型、lint、secrets、floor | 5 秒内，只查变更文件 |
| VERIFY | `/test` | 相关测试、变更行的覆盖率 | 90 秒内 |
| REVIEW | `/review` | 全部，外加下面的 guards | 以分钟计 |
| SHIP | `/ship` | 方向检查，不许回退 | CI |

两条让这件事保持在可忍受范围内的规则：

1. **限定到 diff。** 检查这次变更触及的行，而不是整个仓库。变更行的覆盖率是 agent 能推动的数字；项目覆盖率是它继承来的数字。
2. **成本决定位置。** 任何超过几秒钟的东西都要挪出编辑循环。对整个仓库做 mutation testing 要几个小时；对变更触及的文件做，不到一分钟——这就是“人们会运行的检查”和“人们不会运行的检查”之间的差别。

### Step 6: 守护质量线本身

总会有人指出：如果 agent 既写代码又写检查，那检查证明不了什么。这个说法对一半，而且值得围绕它做工程。

Agent 不会精心构造巧妙的漏洞。它们撞上一个红色检查，然后走通往绿色的最便宜的路。在 review 时盯住 diff 里的这五个动作：

1. **阈值动了。** 预算被调低，severity 被降级，某个检查被移出快速阶段。把 `CONSTRAINTS.md` 与它在 branch 起点处的状态做对比。
2. **测试变简单了。** 加了 `.skip`，删了测试文件，从留下的测试里抽走了断言。
3. **checker 被静默了。** 新增的 `@ts-ignore` 或 `eslint-disable`。有四种抑制要特别警惕，因为它们关掉的是你正依赖的检查：`istanbul ignore` 把代码从覆盖率里剔除而不是去测它，`Stryker disable` 藏起一个存活的 mutant，`nosemgrep` 和 `gitleaks:allow` 对 security findings 做的是同一件事。
4. **工作没完成。** 一个抛异常的 stub，一个把失败变成沉默的空 `catch`，一个站在实现该在的位置上的 `TODO`。
5. **出现了例外。** Exceptions 表里多了一行没人讨论过的记录。

这些都不需要 `git diff` 之外的任何工具。收紧质量线应当是无声的；放松它应当是响亮的。

与带编号的维度不同，floor 没有属于自己的事实标准工具，所以被要求执行它的 agent 倾向于从零写一个 checker，两个 agent 就写出两个不同的。这五项检查的一个参考实现随本 skill 一起提供，在 [references/floor-guard.md](references/floor-guard.md)（diff-scoped，exit `0`/`1`/`2`，patterns 可按生态调整）。改用它，而不是重新发明——理由和每个维度都指名一个事实标准工具相同：让机制在每次运行、每个技术栈之间保持一致。

**不是所有检查都同样循环自证。** 用一个问题给它们排序：agent 能不能靠写一段根本不能工作的代码让这个检查通过？

- **External（外部）** —— axe-core 编码了 WCAG，`osv-scanner` 读一个漏洞数据库，Lighthouse 度量一个真实的浏览器。Agent 争不过这些。
- **Project（项目）** —— 你的 lint 规则、你的层级边界。文件由人拥有。
- **Suite（套件）** —— 你自己的测试。最有用，也是唯一真正循环自证的那一个。

完全由第三种构成的质量线，价值低于其中含有一个外部意见的质量线。检查至少存在一个外部约束。

### Step 7: 没有数字时用 Ratchet（棘轮）

在一个 62% 的代码库上设 80% 覆盖率，你会得到一个永远红色的 build，然后是一个学会无视红色 build 的团队。

另一种做法不需要任何决策：记录你现在在哪里，然后拒绝变差。把它放进 "Measured, not yet enforced" 表，带上今天的数字和一个方向。每次检查都对照记录值，而不是对照愿景。当数字变好时，更新它；当它下滑时，那就是 finding。

这也回应了对 training 的一个合理质疑。模型因通过测试而获得奖励，而这是几秒内就能评估的。架构腐坏在几个月里才显形，永远到不了权重。一个 ratchet 就是那个缺失的惩罚，写在 build 看得见的地方。

## 合理默认值

当用户没有意见时，用这些。它们的选取标准是：多数代码库在第一天就能满足。

| 约束 | 默认值 | 为什么是这个数字 |
|------------|---------|-----------------|
| 变更行的覆盖率 | ≥ 80% | 高到足以逼出一个测试，低到足以放过一行配置 |
| 项目覆盖率 | 今天的值，不许下降 | 采纳它不需要争论 |
| Mutation score（如果用） | 起步 ≥ 60% | 对一个从没被 mutate 过的套件这是典型值；80% 是成熟态 |
| 依赖漏洞 | high 及以上不许有 | 低于那个的多半是噪音 |
| LCP | ≤ 2500 ms | Core Web Vitals 的 "good" 阈值 |
| CLS | ≤ 0.1 | 同上 |
| 无障碍性 | axe 的 critical 或 serious 违规为零 | Moderate 和 minor 常常可辩 |
| 例外寿命 | 90 天 | 长到够规划修复，短到还记得 |
| Ratchet 容差 | 0.5% | 当无关文件挪动数字时吸收漂移 |

把数字和理由一起说出口。一个没有依据的阈值会被下一个撞上它的人删掉。

## 升级路径

约束在三个“牙齿”强度上工作。从第一个开始。

1. **仅书面。** `CONSTRAINTS.md` 存在且 agent 会读它。零成本，能抓住诚实的错误，依赖 agent 自觉。
2. **脚本化。** 一个 `npm run check`（或 `make check`）运行快速检查，接到你的 agent 的 post-edit hook 和你的 CI 里。确定性，无新依赖。
3. **工具化。** 一个专职 runner，处理 diff scoping、预算、ratchet 和 guard 检查。当配置长到一个 shell script 装不下时用它。[references/floor-guard.md](references/floor-guard.md) 里的 floor-guard 参考是这一层中 guard-checks 那一半的起点。

多数项目应当止步于 2。当你要维护超过大约三十行跑检查的 shell 时，再上 3。

**第一次运行可以只有 floor。** Floor guard 只针对 diff、不需要任何安装，所以你在第一天就能执行 floor，再随每个工具的安装逐个加上带编号的维度——不必在第一行代码受保护之前把每个 checker 都搭起来。以机器方式安装的安全工具（gitleaks、osv-scanner）如果不想污染笔记本，也可以只跑在 CI；在 `Runs at` 列里声明每个维度运行在哪。

## 常见合理化借口

| 借口 | 现实 |
|--------|---------|
| "等代码稳定了我们再加约束" | 代码会围绕着它流动期间被允许的一切稳定下来 |
| "测试就是我们的约束" | 你自己写的测试只能证明你和自己意见一致；它们对变更代码的覆盖率、依赖风险或 bundle 增长什么都没说 |
| "我们达不到 80% 覆盖率" | 那就别设 80%。设今天的数字并守住它 |
| "这会让 agent 变慢" | 只有当你把慢检查放进快速循环时才会。那是放置错误，不是反对约束的论据 |
| "我会记得我们的标准是什么" | Agent 不会，而它正在写大部分代码 |
| "约束会挡住我们发布" | 一个带 owner 和日期的例外能放行你。删掉约束则永远放行所有人 |

## 危险信号

如果你注意到这些，停下来重新考虑：

- 访谈超过了四个问题，或产出了一份用户自己解释不了的配置
- 设了一个代码库今天就不达标的预算，且没有达标的计划
- 一个维度带着数字写进了 CONSTRAINTS.md，背后却没有工具
- 明明存在事实标准的 checker，你却手工造了一个，导致团队已有的配置被无视
- 每个约束都由项目自己的测试套件检查，没有外部意见
- `CONSTRAINTS.md` 和那个正失败的功能出现在同一个 commit 里
- 一个例外没有 owner，或到期日在一年以上
- Agent 提议放松阈值而不是修代码
- 慢检查落进了编辑循环，有人已经开始传 `--no-verify`
- 自从 `CONSTRAINTS.md` 写下后就没人打开过它

## 验证

当以下条件满足时，说明本 skill 被正确应用：

- [ ] `CONSTRAINTS.md` 存在，其中每个数字都有陈述的理由
- [ ] Floor 被强制执行，并且在当前代码库上无需任何改动即可通过
- [ ] 用户挑选的每个维度都有安装好的工具和今天就能运行的命令
- [ ] 每条约束都写明它运行在哪，且快速阶段保持在几秒之内
- [ ] 至少一条约束是外部的（不由本项目自己的测试裁决）
- [ ] 仅测量的指标记录了今天的值和一个方向
- [ ] 例外有 owner 和到期日
- [ ] `AGENTS.md` 或 `CLAUDE.md` 指向这个文件
- [ ] 在当前分支上试运行一次，没有用户不认可的失败

## 另见

- `interview-me` —— 本 skill 的 intake 借用的一次一问纪律
- `code-review-and-quality` —— 如何 review；本 skill 决定 review 执行什么
- `ci-cd-and-automation` —— 搭建这些约束运行其中的 pipeline
- `test-driven-development` —— 覆盖率和 mutation 约束所度量的那个套件
- `security-and-hardening` —— security 维度应当包含的内容
- `performance-optimization` —— 性能数字的来源
