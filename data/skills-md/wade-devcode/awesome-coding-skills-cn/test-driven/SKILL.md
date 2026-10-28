---
name: test-driven
description: 实现功能或修 bug 前使用。先写会失败的测试,再写实现。
category: discipline
tags: [测试, tdd]
---

# 测试驱动

## 何时用

- 实现一个新功能或新接口，还没有一行实现代码时。
- 修复 bug，想用测试把"错误行为"钉死，防止日后回归。
- 重构已有代码，需要一张安全网确认行为没有改变。
- 不确定某个边界条件下系统应该做什么，想用测试把期望行为写清楚再动手。

## 核心规则

### 1. 先写测试

**规则：** 在写任何实现代码之前，先写一个表达期望行为的测试。

**为什么：** AI 最常见的路线是"先把功能写出来，最后补测试"——但补出来的测试天然向实现靠拢，只覆盖 happy path，不会质疑假设。等实现已经存在，测试变成了橡皮图章：它测的是"代码现在怎么跑"，而不是"代码应该怎么跑"。先写测试才能强迫自己想清楚"调用方视角的合约"。

**怎么做：**
- 从调用方视角出发：给什么输入，期望得到什么输出或副作用？
- 测试文件比实现文件先存在，`import` 指向尚不存在的模块也没关系，先写好断言。
- 一次只写一个测试用例，专注于当前最重要的行为。

---

### 2. 看它失败

**规则：** 写完测试后立即运行，确认测试因"功能未实现"而失败，而非因测试本身写错而失败。

**为什么：** AI 写完测试后经常直接跳到实现，跳过"看红"这一步。但如果测试从一开始就是绿的（比如断言条件写反了、`assert True` 之类），那整个 TDD 循环就是假的——你永远不知道这个测试有没有能力抓住真正的错误。一个从未失败过的测试，保护价值接近零。

**怎么做：**
- 运行测试，读错误信息，确认失败原因是 `ModuleNotFoundError`、`AttributeError` 或断言不等式，而非语法错误或导入错误（后者说明测试本身有 bug）。
- 如果测试意外通过了，停下来审查：是断言写错了，还是功能早已存在？搞清楚再继续。
- 把失败信息记下来，待会儿用于确认"绿"时对应的正是这个失败点。

---

### 3. 最小实现

**规则：** 只写刚好让当前测试通过的代码，不多写。

**为什么：** AI 一旦开始实现就容易"发散"：顺手加错误处理、抽接口、加日志、考虑将来的扩展——测试还没绿，代码已经膨胀了一倍。最小实现原则把"让这一个测试通过"和"完善代码"拆成两个独立步骤，避免在不确定行为是否正确的时候就堆代码。

**怎么做：**
- 允许暂时写"硬编码返回值"——目的是让测试绿，再靠下一个测试逼迫你写真正的逻辑。
- 克制"顺手做"的冲动：看到相关代码有坏味道，记到 TODO，当前步骤只做让测试通过的最小改动。
- 实现完成后立即运行测试，不要先重构再运行。

---

### 4. 看它通过

**规则：** 运行测试，确认当前测试由红变绿，且原有测试仍然全绿。

**为什么：** AI 改完代码后会说"应该好了"而不真的跑。或者只运行新测试，没跑全量套件——导致刚写的实现破坏了其他已有功能，而这个问题要等 CI 才暴露。本地绿才算绿，口头绿不算绿。

**怎么做：**
- 运行**全量**测试套件，不只跑新写的测试文件。
- 若出现意外的新失败，先查清楚是新代码引入的回归还是测试本身的问题，再继续。
- 全绿之后才可以进入重构阶段（"整理代码"）。

---

### 5. 测行为，不测实现

**规则：** 测试只断言对外可观察的行为（返回值、副作用、抛出的异常），不断言内部实现细节（私有方法是否被调用、内部变量的值、调用次数等）。

**为什么：** AI 写测试时有一个典型错误：用 `mock.assert_called_once_with(...)` 检查内部函数调用顺序，或者 `spy` 私有方法——这样的测试与实现高度耦合。一旦重构内部逻辑（即便行为没有任何改变），测试就会莫名其妙地挂掉，让人觉得"测试在妨碍重构"而最终把它删掉。测试应该是安全网，不应该是紧身衣。

**怎么做：**
- 断言函数的返回值，而不是函数内部调用了哪个子函数。
- 断言系统的状态变化（数据库里有没有记录、文件是否存在），而不是某个私有方法被调用了几次。
- Mock 只用于隔离真正的外部依赖（网络、数据库、时钟），不用于验证内部调用链。

---

## 正例 / 反例

### 完整红→绿循环示例（Python + pytest）

**场景：** 实现一个 `parse_amount` 函数，接受形如 `"¥1,234.56"` 的字符串，返回浮点数 `1234.56`；若格式非法则抛出 `ValueError`。

---

**第一步：先写测试（此时 `parse_amount` 函数根本不存在）**

```python
# tests/test_parse_amount.py
import pytest
from myapp.currency import parse_amount   # 模块尚不存在，先写断言

def test_parse_valid_amount():
    assert parse_amount("¥1,234.56") == 1234.56

def test_parse_without_symbol():
    assert parse_amount("1,234.56") == 1234.56

def test_parse_invalid_raises():
    with pytest.raises(ValueError):
        parse_amount("not_a_number")
```

---

**第二步：运行——确认因"模块不存在"而失败（红）**

```
$ pytest tests/test_parse_amount.py -v

FAILED tests/test_parse_amount.py::test_parse_valid_amount
  ModuleNotFoundError: No module named 'myapp.currency'
```

失败原因是"模块不存在"，而非测试写错。符合预期，继续。

---

**第三步：最小实现——只写让测试通过的代码**

```python
# myapp/currency.py
def parse_amount(value: str) -> float:
    cleaned = value.lstrip("¥").replace(",", "")
    try:
        return float(cleaned)
    except ValueError:
        raise ValueError(f"无法解析金额：{value!r}")
```

---

**第四步：运行——确认全部变绿（绿）**

```
$ pytest tests/test_parse_amount.py -v

PASSED tests/test_parse_amount.py::test_parse_valid_amount
PASSED tests/test_parse_amount.py::test_parse_without_symbol
PASSED tests/test_parse_amount.py::test_parse_invalid_raises

3 passed in 0.04s
```

三个测试全绿，可以进入重构阶段（如有必要）。

---

### 测行为 vs 测实现细节：正反例

```python
# 反例 — 测内部实现细节：断言私有方法被调用
from unittest.mock import patch

def test_parse_calls_strip_internally():
    with patch("myapp.currency._strip_symbol") as mock_strip:
        parse_amount("¥100.00")
        mock_strip.assert_called_once_with("¥100.00")  # ❌ 与内部实现强耦合
                                                        #    重命名 _strip_symbol 就挂
```

```python
# 正例 — 只测对外可观察的返回值
def test_parse_valid_amount():
    assert parse_amount("¥100.00") == 100.0             # ✅ 只关心输入→输出
                                                        #    内部怎么实现随便改
```

---

## 自查清单

- [ ] 写实现代码之前，测试文件已经存在，断言已经写好。
- [ ] 测试已运行过一次并确认是红的，且失败原因是"功能缺失"而非"测试写错"。
- [ ] 实现代码只写了让当前测试通过的最小量，没有顺手加无关逻辑。
- [ ] 实现完成后运行了全量测试套件，新测试绿且没有引入新的失败。
- [ ] 测试断言的是返回值或可观察状态，没有 mock 或 spy 内部私有方法。
- [ ] 每个测试用例只验证一个行为，测试名能清楚说明"什么条件下期望什么结果"。
- [ ] 边界条件（空值、非法输入、极值）有对应的测试用例，不只测 happy path。
