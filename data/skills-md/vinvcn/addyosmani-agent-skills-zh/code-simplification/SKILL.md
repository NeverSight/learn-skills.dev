---
name: code-simplification
description: 为清晰度简化代码。用于在不改变行为的前提下重构代码以提升清晰度；用于代码能运行但比应有状态更难阅读、维护或扩展时；用于审查已累积不必要复杂度的代码时。
---

# 代码简化

> 灵感来自 [Claude Code Simplifier plugin](https://github.com/anthropics/claude-plugins-official/blob/main/plugins/code-simplifier/agents/code-simplifier.md)。这里改编为一个模型无关、流程驱动的 skill，供任何 AI coding agent 使用。

## 概览

通过降低复杂度来简化代码，同时精确保留行为。目标不是减少行数，而是让代码更容易阅读、理解、修改和调试。每次简化都必须通过一个简单测试：“新团队成员理解它会不会比理解原版本更快？”

## 何时使用

- 功能已经可用且测试通过，但实现感觉比必要状态更重
- 代码审查中发现可读性或复杂度问题
- 遇到深层嵌套逻辑、长函数或不清晰命名
- 重构在时间压力下写出的代码
- 合并分散在多个文件中的相关逻辑
- 合并引入重复或不一致的变更之后

**不应使用的情况：**

- 代码已经干净可读，不要为了简化而简化
- 你还不理解代码在做什么，先理解再简化
- 代码是性能关键路径，而“更简单”的版本会明显变慢
- 你即将完全重写该模块，简化即将丢弃的代码是在浪费精力

## 五项原则

### 1. 精确保留行为

不要改变代码做什么，只改变它如何表达。所有输入、输出、副作用、错误行为和边界情况都必须保持一致。如果你不确定某个简化是否保留行为，就不要做。

```
ASK BEFORE EVERY CHANGE:
→ Does this produce the same output for every input?
→ Does this maintain the same error behavior?
→ Does this preserve the same side effects and ordering?
→ Do all existing tests still pass without modification?
```

### 2. 遵循项目约定

简化意味着让代码更符合代码库，而不是强加外部偏好。简化之前：

```
1. Read CLAUDE.md / project conventions
2. Study how neighboring code handles similar patterns
3. Match the project's style for:
   - Import ordering and module system
   - Function declaration style
   - Naming conventions
   - Error handling patterns
   - Type annotation depth
```

破坏项目一致性的简化不是简化，而是 churn。

### 3. 清晰优先于聪明

如果紧凑写法需要停下来费力解析，那么显式代码就优于紧凑代码。

```typescript
// UNCLEAR: Dense ternary chain
const label = isNew ? 'New' : isUpdated ? 'Updated' : isArchived ? 'Archived' : 'Active';

// CLEAR: Readable mapping
function getStatusLabel(item: Item): string {
  if (item.isNew) return 'New';
  if (item.isUpdated) return 'Updated';
  if (item.isArchived) return 'Archived';
  return 'Active';
}
```

```typescript
// UNCLEAR: Chained reduces with inline logic
const result = items.reduce((acc, item) => ({
  ...acc,
  [item.id]: { ...acc[item.id], count: (acc[item.id]?.count ?? 0) + 1 }
}), {});

// CLEAR: Named intermediate step
const countById = new Map<string, number>();
for (const item of items) {
  countById.set(item.id, (countById.get(item.id) ?? 0) + 1);
}
```

### 4. 保持平衡

简化也有失败模式：过度简化。注意这些陷阱：

- **过度内联** — 移除了给概念命名的 helper，会让调用点更难读
- **合并无关逻辑** — 把两个简单函数合并成一个复杂函数并不更简单
- **移除“没必要”的抽象** — 有些抽象是为了可扩展性或可测试性，而不是为了复杂度
- **为行数优化** — 更少行数不是目标，更容易理解才是目标

### 5. 限定在变更范围内

默认只简化最近修改过的代码。除非明确要求扩大范围，否则避免顺手重构无关代码。无边界的简化会制造 diff 噪音，并带来意外回归风险。

## 简化流程

### 步骤 1: 动手前先理解（Chesterton's Fence）

在修改或移除任何东西之前，先理解它为什么存在。这就是 Chesterton's Fence：如果你看到路上有一道栅栏，却不知道它为什么在那里，就不要拆掉它。先理解原因，再判断这个原因是否仍然成立。

```
BEFORE SIMPLIFYING, ANSWER:
- What is this code's responsibility?
- What calls it? What does it call?
- What are the edge cases and error paths?
- Are there tests that define the expected behavior?
- Why might it have been written this way? (Performance? Platform constraint? Historical reason?)
- Check git blame: what was the original context for this code?
```

如果回答不了这些问题，就还没准备好简化。先读更多上下文。

### 步骤 2: 识别简化机会

扫描这些模式。每一项都是具体信号，而不是模糊的 smell：

**结构复杂度：**

| 模式 | 信号 | 简化方式 |
|---------|--------|----------------|
| 深层嵌套（3+ 层） | 控制流难以跟随 | 将条件提取为 guard clauses 或 helper functions |
| 长函数（50+ 行） | 多个职责 | 拆分为命名清晰、职责聚焦的函数 |
| 嵌套三元表达式 | 需要 mental stack 才能解析 | 替换为 if/else 链、switch 或 lookup objects |
| Boolean parameter flags | `doThing(true, false, true)` | 替换为 options objects 或独立函数 |
| 重复条件判断 | 多处出现相同 `if` 检查 | 提取为命名良好的 predicate function |

**命名和可读性：**

| 模式 | 信号 | 简化方式 |
|---------|--------|----------------|
| 泛化命名 | `data`, `result`, `temp`, `val`, `item` | 重命名以描述内容：`userProfile`, `validationErrors` |
| 缩写命名 | `usr`, `cfg`, `btn`, `evt` | 除非缩写是通用的（`id`, `url`, `api`），否则使用完整单词 |
| 误导性命名 | 名为 `get` 的函数同时会修改状态 | 重命名以反映真实行为 |
| 解释 "what" 的注释 | `// increment counter` 写在 `count++` 上方 | 删除注释，代码本身已经足够清楚 |
| 解释 "why" 的注释 | `// Retry because the API is flaky under load` | 保留它们，它们承载了代码无法表达的意图 |

**冗余：**

| 模式 | 信号 | 简化方式 |
|---------|--------|----------------|
| 重复逻辑 | 相同的 5+ 行出现在多处 | 提取为共享函数 |
| 死代码 | 不可达分支、未使用变量、注释掉的代码块 | 移除（确认它确实已死之后） |
| 不必要抽象 | 不增加价值的 wrapper | 内联 wrapper，直接调用底层函数 |
| 过度工程化模式 | Factory-for-a-factory、strategy-with-one-strategy | 替换为简单直接的方案 |
| 冗余类型断言 | 转换为已经能推断出的类型 | 移除断言 |

### 步骤 3: 增量应用变更

一次只做一个简化。每次变更后都运行测试。**将重构变更与功能或 bug fix 变更分开提交。** 一个既重构又添加功能的 PR，其实是两个 PR，应拆分。

```
FOR EACH SIMPLIFICATION:
1. Make the change
2. Run the test suite
3. If tests pass → commit (or continue to next simplification)
4. If tests fail → revert and reconsider
```

避免把多个简化打包成一个未经测试的变更。如果出现破坏，你需要知道是哪次简化导致的。

**The Rule of 500:** 如果一次重构会触及超过 500 行，就投入自动化（codemods、sed scripts、AST transforms），不要手工修改。这个规模的手工编辑容易出错，也很难审查。

### 步骤 4: 验证结果

完成所有简化后，退一步评估整体：

```
COMPARE BEFORE AND AFTER:
- Is the simplified version genuinely easier to understand?
- Did you introduce any new patterns inconsistent with the codebase?
- Is the diff clean and reviewable?
- Would a teammate approve this change?
```

如果“简化”后的版本更难理解或审查，就 revert。不是每次简化尝试都会成功。

## 特定语言指导

### TypeScript / JavaScript

```typescript
// SIMPLIFY: Unnecessary async wrapper
// Before
async function getUser(id: string): Promise<User> {
  return await userService.findById(id);
}
// After
function getUser(id: string): Promise<User> {
  return userService.findById(id);
}

// SIMPLIFY: Verbose conditional assignment
// Before
let displayName: string;
if (user.nickname) {
  displayName = user.nickname;
} else {
  displayName = user.fullName;
}
// After
const displayName = user.nickname || user.fullName;

// SIMPLIFY: Manual array building
// Before
const activeUsers: User[] = [];
for (const user of users) {
  if (user.isActive) {
    activeUsers.push(user);
  }
}
// After
const activeUsers = users.filter((user) => user.isActive);

// SIMPLIFY: Redundant boolean return
// Before
function isValid(input: string): boolean {
  if (input.length > 0 && input.length < 100) {
    return true;
  }
  return false;
}
// After
function isValid(input: string): boolean {
  return input.length > 0 && input.length < 100;
}
```

### Python

```python
# SIMPLIFY: Verbose dictionary building
# Before
result = {}
for item in items:
    result[item.id] = item.name
# After
result = {item.id: item.name for item in items}

# SIMPLIFY: Nested conditionals with early return
# Before
def process(data):
    if data is not None:
        if data.is_valid():
            if data.has_permission():
                return do_work(data)
            else:
                raise PermissionError("No permission")
        else:
            raise ValueError("Invalid data")
    else:
        raise TypeError("Data is None")
# After
def process(data):
    if data is None:
        raise TypeError("Data is None")
    if not data.is_valid():
        raise ValueError("Invalid data")
    if not data.has_permission():
        raise PermissionError("No permission")
    return do_work(data)
```

### React / JSX

```tsx
// SIMPLIFY: Verbose conditional rendering
// Before
function UserBadge({ user }: Props) {
  if (user.isAdmin) {
    return <Badge variant="admin">Admin</Badge>;
  } else {
    return <Badge variant="default">User</Badge>;
  }
}
// After
function UserBadge({ user }: Props) {
  const variant = user.isAdmin ? 'admin' : 'default';
  const label = user.isAdmin ? 'Admin' : 'User';
  return <Badge variant={variant}>{label}</Badge>;
}

// SIMPLIFY: Prop drilling through intermediate components
// Before — consider whether context or composition solves this better.
// This is a judgment call — flag it, don't auto-refactor.
```

## 常见合理化借口

| 合理化借口 | 现实 |
|---|---|
| “它能工作，没必要动” | 难读的可运行代码在出问题时也会很难修。现在简化，会节省未来每次修改的时间。 |
| “行数越少就越简单” | 一行嵌套三元表达式不比五行 if/else 更简单。简单性关乎理解速度，而不是行数。 |
| “我顺手快速简化一下这段无关代码” | 无范围的简化会制造嘈杂 diff，并给你本不打算修改的代码带来回归风险。保持聚焦。 |
| “类型让它自解释了” | 类型记录结构，不记录意图。命名良好的函数比类型签名更能解释 *why*。 |
| “这个抽象以后可能有用” | 不要保留投机性抽象。如果现在用不上，它就是没有价值的复杂度。移除它，需要时再加回来。 |
| “原作者一定有原因” | 也许。检查 git blame，应用 Chesterton's Fence。但累积复杂度往往没有原因，只是压力下迭代的残留。 |
| “我会一边加功能一边重构” | 将重构和功能开发分开。混合变更更难审查、回滚，也更难在历史中理解。 |

## 危险信号

- 需要修改测试才能通过的简化（你很可能改变了行为）
- “简化”后的代码比原来更长、更难跟随
- 为了符合个人偏好而不是项目约定去重命名
- 因为“这样代码更干净”而移除错误处理
- 简化你尚未完全理解的代码
- 把许多简化打包进一个很大且难以审查的 commit
- 未被要求时重构当前任务范围外的代码

## 验证

完成一次简化后：

- [ ] 所有现有测试无需修改即可通过
- [ ] Build 成功且没有新增警告
- [ ] Linter/formatter 通过（没有风格回归）
- [ ] 每个简化都是可审查的增量变更
- [ ] Diff 干净，没有混入无关变更
- [ ] 简化后的代码遵循项目约定（已对照 CLAUDE.md 或等价文件检查）
- [ ] 没有移除或削弱错误处理
- [ ] 没有留下死代码（未使用 import、不可达分支）
- [ ] 队友或审查 agent 会认可该变更是净改进
