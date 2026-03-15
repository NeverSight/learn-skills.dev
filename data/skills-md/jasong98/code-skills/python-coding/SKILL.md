---
name: python-coding
description: Python 代码编写规范和最佳实践。适用于代码生成、代码审查、代码重构场景。
---

## 核心原则

- **正确性优先**: 确保代码正确运行后再优化
- **显式优于炫技**: 可读性优先于技巧
- **保持一致性**: 与现有项目风格冲突时，优先匹配项目风格

## 快速参考

### 命名约定

| 类型 | 风格 | 示例 |
|------|------|------|
| 模块/函数/变量 | `snake_case` | `calculate_total` |
| 类名 | `CapWords` | `UserAccount` |
| 常量 | `UPPER_SNAKE_CASE` | `MAX_RETRY_COUNT` |
| 私有属性 | `_leading_underscore` | `_internal_id` |
| 布尔变量 | `is_`/`has_`/`can_` 前缀 | `is_active`, `has_permission` |

### 类型注解

```python
# 使用现代语法 (Python 3.10+)
def process(items: list[str]) -> dict[str, int]: ...
def get_user(id: int) -> User | None: ...

# 使用 Protocol 进行结构化类型
from typing import Protocol

class Drawable(Protocol):
    def draw(self) -> None: ...
```

详细指南: [style-guide.md#类型注解](references/style-guide.md)

### 函数设计

- **单一职责**: 每个函数做一件事
- **长度限制**: ≤60 行（理想 ≤20 行）
- **参数数量**: ≤5 个（超过则用 dataclass）
- **参数顺序**: 必填 → 可选 → *args → **kwargs

```python
# 参数过多时使用 dataclass
@dataclass
class EmailConfig:
    to: str
    subject: str
    body: str
    cc: list[str] = field(default_factory=list)

def send_email(config: EmailConfig) -> None: ...
```

### Import 规则

```python
# 分组顺序，每组内按字母排序
import os
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv

from myapp.models import User
from myapp.utils import logger
```

- 禁止 `from module import *`
- import 阶段不得执行 I/O 或重计算

### 错误处理

```python
# 使用具体异常类型
try:
    result = data["key"]
except KeyError:
    result = default_value
except requests.Timeout:
    logger.warning("Request timed out")
    raise

# 禁止裸 except
# Bad: except Exception: pass
```

## 文档注释规则

### 使用中文文档字符串（Google Style）

```python
def load_config(path: Path) -> dict[str, Any]:
    """加载并校验配置文件.

    该函数读取配置文件并返回解析结果, 不修改全局状态.

    Args:
        path: 配置文件路径.

    Returns:
        解析后的配置字典.

    Raises:
        ValueError: 当配置不合法时抛出.
    """
```

格式规则：
- 使用中文描述
- 使用英文关键字（Args/Returns/Raises）
- 使用英文半角标点（`. , :`）
- 描述语义/约束/副作用，不写实现细节

### 注释规则

- 使用中文文字书写
- 仅使用英文半角标点（`. , ;`）
- 中英文之间加空格：`使用 LRU 缓存`
- 解释为什么，不解释代码做了什么

```python
# 使用贪心策略, 因为回溯会导致指数级复杂度
result = greedy_search(data)
```

## 代码格式

- 使用 4 空格缩进（禁用 tab）
- 行宽 ≤120 字符
- 使用 `()` 换行，避免 `\`
- 顶层定义间 2 行空行，类内方法间 1 行空行

## 自检清单

- [ ] Import 分组正确（标准库/第三方/本地）
- [ ] 所有公共 API 有类型注解
- [ ] 所有公共 API 有 docstring
- [ ] 无类型重复（签名已有类型，docstring 不再重复）
- [ ] 注释标点为英文半角
- [ ] 无裸 `except Exception: pass`
- [ ] 函数 ≤60 行，参数 ≤5 个
- [ ] 无魔法数字（使用命名常量）
- [ ] 使用 context manager 管理资源
- [ ] 风格符合项目约定

## 详细资源

- [详细风格指南](references/style-guide.md) - 完整代码示例和深入说明
- [设计模式参考](references/design-patterns.md) - Factory, Strategy, Observer 等
- [重构模式参考](references/refactoring-patterns.md) - 常见代码异味及重构方法