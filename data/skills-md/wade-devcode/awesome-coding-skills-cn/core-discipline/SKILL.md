---
name: core-discipline
description: 写/改任何代码前必读。约束 AI 避免造假 API、过度工程、大范围乱改。
category: discipline
tags: [纪律, api, yagni]
---

# 核心纪律

## 何时用

- 接到任何新的编码或改码任务，动手前先过一遍本文。
- 发现自己想"顺手"重构无关代码、提取公共抽象时。
- 不确定某个库函数/字段是否真实存在时。
- 准备交付代码或提 PR 前做最终自查。

## 核心规则

### 1. 不造 API

**规则：** 只调用真实存在的库函数、类、字段——不确定就先查文档或读源码，禁止凭记忆编造。

**为什么：** AI 的训练数据存在截止日期，且会在不同库之间混淆接口。常见事故：把 `pandas` 的方法名张冠李戴到 `polars`，把 Node.js v16 已删除的 API 当作现行 API 调用，编造根本不存在的 `requests.get(...).json_body` 字段。这类代码在 review 时看起来合理，跑起来立刻抛 `AttributeError` / `TypeError`，且错误定位成本很高。

**怎么做：**
- 不确定方法签名 → 用 `help()`、IDE 补全、或直接读源码确认。
- 不确定返回结构 → 先 `print` / `console.log` 或写一个小测试确认再用。
- 若无法查证，在代码注释中明确标注 `# TODO: 请核实此 API 是否存在`，不要默默造假。

---

### 2. 外科手术式改动

**规则：** 只改与当前任务直接相关的代码行，不顺手触碰无关部分。

**为什么：** AI 极容易在"顺手"时引入意外回归：重排 import 导致循环依赖，格式化改动污染 git blame，重命名变量破坏下游引用。改动面越大，reviewer 越难判断哪些变化是必要的，哪些是噪音，review 成本指数级上升。

**怎么做：**
- diff 提交前逐行确认：每一处改动都必须有对应的任务理由。
- 不改格式（缩进、引号风格、trailing comma），除非任务本身就是格式化。
- 不重排、增删无关 import。
- 若发现真实 bug 但不在本次任务范围内，新建 issue 记录，不在当前 PR 里修。

---

### 3. 拒绝过度工程

**规则：** 只实现当前需求的最小方案，不预留"将来可能用到"的抽象或扩展点（YAGNI）。

**为什么：** AI 倾向于生成"通用"、"可扩展"的代码——Strategy 模式、插件系统、多层配置——即使需求只是"把这个数字加一"。这些提前抽象几乎从不被用到，却带来维护负担、理解成本，以及因过度复杂而埋下的 bug。

**怎么做：**
- 问自己：「当前的具体需求是什么？」写刚好满足它的代码。
- 不引入新的间接层（额外的 interface、factory、wrapper）除非现有需求直接要求。
- 配置项只在真的有多个合法取值时才加，不为"灵活性"提前加开关。
- 泛型/模板只在当前就有两种以上具体类型时才抽象。

---

### 4. 显式暴露假设

**规则：** 动手前列出关键假设；假设有歧义先问清楚，不闷头猜。

**为什么：** AI 在上下文不足时会悄悄做假设并写进代码：假设某字段不会为 null、假设列表非空、假设调用方已鉴权。这些假设在 happy path 下不报错，在边界场景下造成生产事故，且事后难以溯源（代码里看不到这个"决策"是在哪里做出的）。

**怎么做：**
- 开始前写出假设列表，例如：
  ```
  假设：
  - user.profile 在此处一定非 null（由上游鉴权中间件保证）
  - items 列表至少有 1 条（调用方已校验）
  ```
- 对于数据形状不确定的，用 `assert` / TypeScript 类型守卫 / Zod schema 在代码中显式检查。
- 若某个假设无法当场验证，暂停并向用户提问，不要继续。

---

### 5. 改前先读

**规则：** 修改任何文件前先完整读一遍，理解现有约定再动手。

**为什么：** AI 经常在没读完文件的情况下就开始写代码，结果：重复定义已有的工具函数、违反项目既有的错误处理约定、用与周围代码不同的命名风格引入风格割裂。这些问题单独看不严重，积累起来会让代码库越来越难维护。

**怎么做：**
- 用 Read 工具读取目标文件全文，重点关注：已有的同类函数、命名规范、错误处理模式、import 风格。
- 改多个文件时，每个文件都先读，不要假设"它和另一个文件一样"。
- 读完后在心里（或明文写出）总结「此文件的约定」，再开始改。

---

## 正例 / 反例

### 反例：编造不存在的库方法

```python
# 反例 — AI 凭记忆编造了 httpx 不存在的 .json_body 属性
import httpx

resp = httpx.get("https://api.example.com/data")
payload = resp.json_body          # ❌ AttributeError: 'Response' object has no attribute 'json_body'
user_id = payload["id"]
```

```python
# 正例 — 查过文档，使用真实存在的 .json() 方法
import httpx

resp = httpx.get("https://api.example.com/data")
payload = resp.json()             # ✅ httpx.Response.json() 是真实 API
user_id = payload["id"]
```

---

### 反例：过度工程——为一个简单需求引入不必要的抽象

```python
# 需求：给用户名加前缀 "user_"
# 反例 — AI 预留了"将来可能需要不同策略"的扩展点

from abc import ABC, abstractmethod

class PrefixStrategy(ABC):
    @abstractmethod
    def apply(self, name: str) -> str: ...

class UserPrefixStrategy(PrefixStrategy):
    def apply(self, name: str) -> str:
        return f"user_{name}"

class PrefixFactory:
    _registry: dict = {}

    @classmethod
    def register(cls, key: str, strategy: PrefixStrategy):
        cls._registry[key] = strategy

    @classmethod
    def get(cls, key: str) -> PrefixStrategy:
        return cls._registry[key]

PrefixFactory.register("user", UserPrefixStrategy())

def format_username(name: str, strategy_key: str = "user") -> str:
    return PrefixFactory.get(strategy_key).apply(name)   # ❌ 三层间接，零复用
```

```python
# 正例 — 最小实现，直接满足需求

def format_username(name: str) -> str:
    return f"user_{name}"                                 # ✅ 清晰、可测、够用
```

---

## 自查清单

- [ ] 我调用的每一个库函数/字段，都经过文档或源码确认真实存在。
- [ ] 本次 diff 里的每一处改动，都能对应到当前任务的某个具体要求。
- [ ] 没有引入任何"将来可能有用"的抽象、配置项或泛型参数。
- [ ] 所有关键假设（数据形状、调用前置条件、边界）已在代码注释或类型注解中显式标注。
- [ ] 修改的每个文件，我都读过全文并理解了其中的命名和错误处理约定。
- [ ] 没有顺手改格式、重排 import 或重构与任务无关的代码。
- [ ] 若存在无法当场验证的假设，已向用户提问而非自行猜测。
