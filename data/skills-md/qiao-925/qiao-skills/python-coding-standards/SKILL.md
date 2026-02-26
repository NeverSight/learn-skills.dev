---
name: python-coding-standards
description: Python 编码规范，包括类型提示、日志规范、命名约定、代码结构等。适用于所有 Python 代码文件。
---

# Python 编码规范

> Python 代码实现阶段的统一基线，覆盖类型、日志、命名与结构要求。

---

## ⚠️ 核心强制要求

### 1. 类型提示

**所有函数、方法、类声明必须补全类型提示。**

- 缺值返回使用 `-> None`
- 公共 API 必须提供完整 docstring（参数、返回值、异常）

### 2. 日志规范

**业务代码统一通过 `src.logger.setup_logger` 获取 logger，禁止使用 `print`。**

- 测试示例代码除外
- 错误路径必须使用 `logger.error` 或 `logger.exception`

---

## AI Agent 行为要求

### 创建新文件时

- 必须添加类型提示
- 必须使用 logger（禁止 print）

### 修改现有文件时

- 新增代码必须符合类型提示要求
- 新增日志必须使用 logger

### 代码审查时

- 检查类型提示完整性
- 检查是否使用了 print

---

## 验收标准

- [ ] 所有函数、方法、类有类型提示
- [ ] 公共 API 有完整 docstring
- [ ] 关键模块的日志覆盖正常运行与异常分支

---

## 参考资料

- `references/type-hints.md` - 类型提示详细规范
- `references/logging.md` - 日志规范详细说明
- `references/naming-conventions.md` - 命名约定详细说明
- `references/code-structure.md` - 代码结构详细说明
