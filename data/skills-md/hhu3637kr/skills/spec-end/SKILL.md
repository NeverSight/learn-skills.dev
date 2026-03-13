---
name: spec-end
description: >
  整个 Spec 完成后的收尾工作。由角色 spec-ender 调用。
  触发条件：(1) 角色 spec-ender 需要在阶段五发起团队讨论、沉淀经验、询问用户归档并提交 git，
  (2) TeamLead 通知 spec-ender 开始工作（所有其他阶段已完成），
  (3) 一个完整的开发周期（计划→实现→测试）结束后需要收尾。
---

# Spec End

## 核心原则

1. **多角色视角**：通过 SendMessage 向团队成员收集各自视角的经验素材，不只是 spec-ender 的独角戏
2. **分流沉淀**：调用 exp-reflect 按权重分流（重大经验 → exp-write，轻量 → Auto Memory）
3. **用户确认归档**：归档前必须使用 AskUserQuestion 询问用户
4. **git 提交**：归档确认后调用 git-workflow-sop 完成提交

## 工作流程

### 步骤 1：接收任务

从 TeamLead 的 SendMessage 中获取：
- 当前 Spec 的目录路径
- 确认所有阶段（计划/实现/测试）已完成

### 步骤 2：扫描 Spec 目录

读取当前 spec 目录下的所有文档：
- `plan.md`：设计方案
- `exploration-report.md`：探索阶段发现
- `summary.md`：实现细节
- `test-plan.md`：测试策略
- `test-report.md`：测试过程和结果
- `debug-xxx.md` / `debug-xxx-fix.md`：问题和修复（如有）

### 步骤 3：向团队成员发起讨论

向各角色询问本次开发的经验素材：

```python
SendMessage(
    recipient="spec-writer",
    content="请分享本次撰写 plan.md 时遇到的困难、踩过的坑、值得记录的发现？"
)
SendMessage(
    recipient="spec-tester",
    content="请分享本次测试过程中的发现、边界情况、改进建议？"
)
SendMessage(
    recipient="spec-executor",
    content="请分享本次实现过程中遇到的技术挑战、解决方案、值得复用的模式？"
)
SendMessage(
    recipient="spec-debugger",
    content="请分享本次调试的根因分析、修复思路、预防建议？（如有 debug 文档）"
)
```

等待各角色回复，汇总讨论结果。

### 步骤 4：调用 exp-reflect 分流沉淀

以讨论结果 + spec 目录文档为素材，调用 `/exp-reflect`：

```bash
/exp-reflect
```

exp-reflect 会根据经验的重要性分流：
- 重大经验（解决了重要问题、有高复用价值）→ `exp-write` 写入正式经验文件
- 轻量知识（小技巧、上下文记忆）→ Auto Memory

### 步骤 5：询问用户是否归档

```python
AskUserQuestion(
    questions=[{
        "question": "所有阶段已完成，经验沉淀也已完成。是否可以将本 Spec 归档到 06-已归档，并提交 git？",
        "header": "确认归档",
        "multiSelect": False,
        "options": [
            {
                "label": "确认归档并提交 git",
                "description": "将 Spec 目录移动到 06-已归档，并调用 git-workflow-sop 提交"
            },
            {
                "label": "暂不归档",
                "description": "先保留在当前目录，稍后手动归档"
            }
        ]
    }]
)
```

### 步骤 6：归档（用户确认后）

用户选择"确认归档并提交 git"：

1. 将 Spec 目录移动到 `spec/06-已归档/`
2. 调用 `/git-workflow-sop` 提交本次开发的所有变更

用户选择"暂不归档"：
- 跳过归档步骤，直接执行步骤 7

### 步骤 7：通知 TeamLead 完成

```python
SendMessage(
    recipient="TeamLead",
    content="收尾工作完成，Teams 可以进入待机状态。"
)
```

## 与其他角色的协作

```
[所有其他阶段完成]
TeamLead → spec-ender 开始
spec-ender → SendMessage 向各角色发起讨论
各角色 → 回复经验素材
spec-ender → 汇总 + 调用 exp-reflect → 沉淀经验
spec-ender → AskUserQuestion → 用户确认归档
[如归档] spec-ender → 移动目录 → git-workflow-sop 提交
spec-ender → 通知 TeamLead 完成
TeamLead → 通知用户整个流程完成，Teams 进入待机
```

## 后续动作

完成收尾后确认：
1. 已向所有相关角色发起讨论并收到回复
2. 已调用 exp-reflect 完成分流沉淀
3. 已询问用户是否归档
4. 如归档：已移动目录 + 已调用 git-workflow-sop 提交
5. 已通知 TeamLead

### 常见陷阱
- 跳过多角色讨论，只用自己的视角沉淀经验（会遗漏各角色的独特发现）
- 未询问用户直接归档
- 沉淀完成后忘记通知 TeamLead
