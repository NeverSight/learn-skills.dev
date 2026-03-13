---
name: feishu
description: 与飞书集成的技能。当需要与飞书交互或自动化时使用此技能。适合自动化场景。
---

# 飞书集成技能

## 何时使用此技能

当用户：

- 明确提到"飞书"
- 需要将本地 Markdown 文件上传到飞书云文档
- 需要自动化发送消息到飞书群聊
- 需要获取群聊列表、文件列表等信息
- 需要批量上传文档或执行自动化工作流

## 关键：始终使用 run.py 包装器

绝对不要直接调用脚本。始终使用 `python scripts/run.py [script]` :

```bash
# ✅ CORRECT - Always use run.py:
python scripts/run.py lark_cli.py [command] [options]

# ❌ WRONG - Never call directly:
python scripts/lark_cli.py [command] [options]  # Fails without venv!
```

`run.py` 包装器会自动：

1. 创建 `.venv` 虚拟环境（如果不存在）
2. 安装所有依赖
3. 激活环境
4. 正确执行脚本

## 环境配置

如果 `.env` 文件不存在，告诉用户：

1. 访问 [飞书开放平台](https://open.feishu.cn/)获取应用凭证
2. 参考`.env.example`配置`.env`文件
3. 在飞书开放平台为应用开通对应权限

配置完成后，告诉我"配置完成"，我将继续执行操作。"

## 命令速查表

| 命令              | 说明          | 必需参数                 |
| ----------------- | ------------- | ------------------------ |
| `send-text`       | 发送文本消息  | `--chat-id`, `--message` |
| `list-chat`       | 获取群聊列表  | 无                       |
| `root-folder`     | 获取根文件夹  | 无                       |
| `list-file`       | 获取文件清单  | 无                       |
| `upload-markdown` | 上传 Markdown | `--file-path`            |


## 功能列表

### 发送文本消息

```bash
python scripts/run.py lark_cli.py send-text --chat-id "聊天ID" --message "消息内容"
```

### 获取群聊列表

```bash
python scripts/run.py lark_cli.py list-chat
```

返回机器人所在的所有群聊信息（名称和 chat_id）。

### 云文档操作

**获取根文件夹元数据：**

```bash
python scripts/run.py lark_cli.py root-folder
```

**获取文件夹中的文件清单：**

```bash
python scripts/run.py lark_cli.py list-file
```

**上传 Markdown 文档到飞书：**

```bash
python scripts/run.py lark_cli.py upload-markdown --file-path "/path/to/document.md" --file-name "文件名称"
```
