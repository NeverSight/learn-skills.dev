---
name: tmux-session-manager
description: 'Use when executing commands, running builds, starting services, or monitoring logs in a visible tmux pane'
---

# 共享终端协作

在用户可见的 tmux 面板中执行命令，实现协作式终端操作。

## 确定目标面板

目标面板由用户指定，或通过发现获取：

```bash
tmux list-sessions -F "#S"
# PANE Title
tmux list-panes -a -F "#S:#I.#P #T"
# PANE Title CMD PWD
tmux list-panes -t main -F "#S:#I.#P #T #{pane_current_command} @ #{pane_current_path}"
```

下文示例使用 `$PANE` 代表目标面板（如 `main:1.1`）。

## 关键规则

| 规则        | 说明                                  |
|-----------|-------------------------------------|
| 禁止交互式 TUI | 不运行 `vim`, `nano`, `top` 等需要持续交互的程序 |
| 引号转义      | `send-keys` 中注意引号转义，防止命令格式错误        |
| 读写分离      | 发送命令后**必须**读取输出确认结果，不假设成功           |

## 核心操作

### 执行命令

```bash
# 可选：先清屏
tmux send-keys -t $PANE "clear" C-m
# 发送命令
tmux send-keys -t $PANE "你的命令" C-m
# 必须：读取输出确认
tmux capture-pane -pt $PANE -S -100
```

### 读取输出

```bash
tmux capture-pane -pt $PANE -S -100  # 根据预期输出调整行数
```

### 终止进程

```bash
tmux send-keys -t $PANE C-c
```

## 常用按键

| 按键 | 作用 |
|------|------|
| `C-c` | 中断进程 |
| `C-d` | EOF/退出 |
| `C-z` | 挂起进程 |
| `C-l` | 清屏 |

## 提示

- 长时间任务确认启动即可，无需等待完成
- 输出过长时增加 `-S` 行数（如 `-S -200`）
- 判断命令完成：多次 capture 检查 shell prompt 是否出现
