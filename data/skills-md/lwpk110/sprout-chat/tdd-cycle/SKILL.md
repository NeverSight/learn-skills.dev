---
name: tdd-cycle
description: 执行测试驱动开发的红-绿-重构循环，包含原子提交规范。用于 Python/FastAPI 项目开发。
---

# TDD 循环技能

## 概述
本技能为小芽家教后端开发强制执行严格的 TDD 纪律。所有功能开发必须遵循红-绿-重构循环。

## 核心原则
> **"无测试，不编码"** - 每次功能变更必须从失败的测试开始。

## 第一阶段：红灯（编写失败测试）

### 必要步骤
1. 编写测试文件
2. 运行 `pytest tests/test_<功能>.py` → **必须失败**
3. 提交：`[任务ID] test: <描述> (Red)`

### 示例
```bash
pytest tests/test_engine.py::test_create_session  # 预期：失败
git add tests/test_engine.py
git commit -m "[LWP-3] test: 添加会话创建测试 (Red)"
```

## 第二阶段：绿灯（最小实现）

### 必要步骤
1. 在 `backend/app/services/` 实现功能
2. 运行 `pytest tests/test_<功能>.py` → **必须通过**
3. 提交：`[任务ID] feat: <描述> (Green)`

## 第三阶段：重构（可选）

### 必要步骤
1. 重构代码
2. 运行 `pytest tests/test_<功能>.py` → **仍须通过**
3. 提交：`[任务ID] refactor: <描述> (Refactor)`

## 验证清单
- [ ] 所有测试通过 (`pytest`)
- [ ] 测试覆盖率 ≥ 80%
- [ ] 无 lint 错误
- [ ] 任务状态已更新

## 相关技能
- `git-commit` - 提交信息规范
- `github-sync` - GitHub 和 Taskmaster 同步
