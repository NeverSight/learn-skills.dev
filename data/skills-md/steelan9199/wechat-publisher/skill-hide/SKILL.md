---
name: skill-hide
description: 用于隐藏或恢复技能；支持单技能或批量操作；管理技能父文件夹路径；防止隐藏自身；支持多目录搜索和指定目录操作；支持一键隐藏/恢复所有技能. 当用户需要[隐藏或恢复技能]的时候, 使用该技能.
---

# 技能隐藏管理 (Skill Hide Manager)

## ⚠️ 强制规则（AI 必须遵守）

### 规则 1：歧义词必须询问

当用户输入包含以下**歧义词**时，**禁止直接执行任何操作**，必须先询问确认：

| 歧义词 | 必须询问 |
|--------|----------|
| "显示" | ✅ 必须询问 |
| "展示" | ✅ 必须询问 |

**正确流程：**
```
用户: "显示所有技能"
AI:  "'显示'有两种含义：
     [1] 恢复（取消隐藏）技能
     [2] 查看/列出技能列表
     请回复 1 或 2："
```

**错误行为（禁止）：**
- ❌ 直接列出技能
- ❌ 直接恢复技能
- ❌ 假设用户意图

### 规则 2：非歧义词直接执行

| 用户输入 | 意图 | 直接执行 |
|----------|------|----------|
| "隐藏 xxx" | 隐藏技能 | `hide_skill.py xxx` |
| "查看/列出 xxx" | 预览技能 | `--show-all` |
| "恢复 xxx" / "取消隐藏 xxx" | 恢复技能 | `unhide_skill.py xxx` |
| "哪些被隐藏了" | 查看已隐藏列表 | `list_hidden.py` |

## 术语说明

| 术语 | 含义 | 对应操作 |
|------|------|----------|
| **隐藏** | 将技能标记为隐藏状态 | `hide_skill.py` |
| **恢复** | 取消隐藏，让技能重新显示 | `unhide_skill.py` |
| **预览/查看/列出** | 仅查看技能列表，不修改 | `--show-all` |

## 前置准备

- 依赖: Python 标准库，无需额外依赖

## 配置管理

首次使用需配置技能父文件夹路径。

### 配置方法

> 路径格式说明：使用正斜杠 `/` 兼容 Windows CMD、PowerShell 和类 Unix shell（Git Bash、MSYS2、WSL）

```bash
# 添加单个路径
python skill-hide/scripts/config_manager.py --add "C:/path/to/skills"

# 添加多个路径
python skill-hide/scripts/config_manager.py --add "C:/path1" --add "D:/path2"

# 覆盖设置所有路径（逗号分隔）
python skill-hide/scripts/config_manager.py --set "C:/path1,D:/path2,E:/path3"

# 列出当前配置
python skill-hide/scripts/config_manager.py --list

# 清空所有配置
python skill-hide/scripts/config_manager.py --clear

# 不带参数运行，显示当前配置和参考路径
python skill-hide/scripts/config_manager.py
```

## 操作步骤

### 隐藏技能

```bash
# 隐藏单个
python skill-hide/scripts/hide_skill.py <skill-name>

# 隐藏多个
python skill-hide/scripts/hide_skill.py <skill1> <skill2>

# 隐藏所有（所有配置文件夹）
python skill-hide/scripts/hide_skill.py --all

# 隐藏指定文件夹下的所有技能
python skill-hide/scripts/hide_skill.py --all --folder <path>

# 指定文件夹
python skill-hide/scripts/hide_skill.py <skill-name> --folder <path>
```

### 恢复技能

```bash
# 恢复单个
python skill-hide/scripts/unhide_skill.py <skill-name>

# 恢复多个
python skill-hide/scripts/unhide_skill.py <skill1> <skill2>

# 恢复所有（所有配置文件夹）
python skill-hide/scripts/unhide_skill.py --all

# 恢复指定文件夹下的所有技能
python skill-hide/scripts/unhide_skill.py --all --folder <path>

# 指定文件夹
python skill-hide/scripts/unhide_skill.py <skill-name> --folder <path>
```

### 预览技能（仅查看，不修改）

```bash
# 查看所有配置文件夹的技能状态（多文件夹场景）
python skill-hide/scripts/hide_skill.py --show-all

# 查看指定文件夹的技能状态
python skill-hide/scripts/hide_skill.py --show-all --folder <path>

# 查看所有已隐藏的技能（跨所有配置文件夹）
python skill-hide/scripts/list_hidden.py

# 查看操作历史记录
python skill-hide/scripts/list_history.py

# 查看操作过的文件夹列表
python skill-hide/scripts/list_history.py --folders
```

## 资源索引

- `scripts/config_manager.py` - 读取/写入配置
- `scripts/hide_skill.py` - 隐藏技能 / 查看所有技能状态（支持多文件夹）
- `scripts/unhide_skill.py` - 恢复技能
- `scripts/list_hidden.py` - 列出所有已隐藏技能（跨文件夹）
- `scripts/list_history.py` - 查看操作历史记录

## 注意事项

1. **禁止隐藏自己**: skill-hide 不能隐藏自身
2. **路径规范化**: 自动统一使用正斜杠 `/`
3. **多目录支持**:
   - 配置文件中可保存多个技能父文件夹路径
   - 隐藏/恢复技能时会搜索所有配置的文件夹
   - `--show-all` 不指定 `--folder` 时会显示所有配置文件夹的状态
4. **同名技能**: 不同文件夹中可以有同名技能，隐藏/恢复时会操作所有匹配的技能
5. **配置文件**: `skill-hide/.skill-config.json`

## ⚠️ 重要：AI 使用指南

### 如何判断技能是否隐藏

**不要仅依赖工具输出**，必须通过文件系统验证：

```bash
# 正确：直接检查文件存在性
ls -la skill-folder/
# 显示状态: SKILL.md 存在
# 隐藏状态: SKILL.md.hide 存在, SKILL.md 不存在
```

**判断逻辑**：
| 文件存在情况 | 状态 |
|-------------|------|
| `SKILL.md` 存在 | ✅ 显示 |
| `SKILL.md.hide` 存在，且 `SKILL.md` 不存在 | ❌ 隐藏 |

### 已知问题

1. **Windows 控制台编码问题**: 脚本输出中文可能出现乱码（不影响实际功能）
2. **验证机制**: 所有隐藏/恢复操作后应验证文件状态，确保操作成功

## 快速参考表

| 用户输入 | 歧义？ | AI 行动 |
|----------|--------|---------|
| "隐藏 xxx" | ❌ | 直接执行隐藏 |
| "查看/列出 xxx" | ❌ | 直接执行预览 |
| "恢复/取消隐藏 xxx" | ❌ | 直接执行恢复 |
| **"显示 xxx"** | **✅** | **必须询问** |
| **"展示 xxx"** | **✅** | **必须询问** |
| "哪些被隐藏了" | ❌ | 直接执行 list_hidden.py |
