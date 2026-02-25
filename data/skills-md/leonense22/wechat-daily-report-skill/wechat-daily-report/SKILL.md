---
name: wechat-daily-report
description: 微信群聊天记录日报图片生成工具。分析微信群聊天记录，结合 AI 生成内容，**最终输出为手机端分辨率的日报长图（PNG）**。
---

# 微信群聊日报生成 Skill

## 工作流程

```
1. 运行 analyze_chat.py 分析聊天记录
   ↓
2. AI 根据聊天文本生成内容 (ai_content.json)
   ↓
3. 运行 generate_report.py 生成日报图片 (.png)
```

> ⚠️ **最终输出是 PNG 图片**，不是 HTML。确保 --output 参数使用 `.png` 后缀。

## 使用步骤

### 1. 分析聊天记录

```bash
python scripts/analyze_chat.py <聊天记录.json> --output-stats stats.json --output-text simplified_chat.txt
```

**输出**:
- `stats.json` - 统计数据（话唠榜、熬夜冠军、词云等）
- `simplified_chat.txt` - 全量聊天文本，供 AI 分析

### 2. AI 生成内容

根据 `simplified_chat.txt` 和 `stats.json`，按 `references/ai_prompt.md` 中的格式生成 AI 内容，保存为 `ai_content.json`。

AI 需要生成的内容包括：
- `topics`: 讨论热点（3-5 个）
- `resources`: 教程/资源分享
- `important_messages`: 重要消息
- `dialogues`: 有趣对话
- `qas`: 问答
- `talker_profiles`: 话唠成员的特点标签（常用词已由脚本统计）

### 3. 生成日报图片

```bash
python scripts/generate_report.py --stats stats.json --ai-content ai_content.json --output report.png --clean-temp
```

> ✅ 输出后缀必须是 `.png`，使用 iPhone 14 Pro Max 分辨率 (430x932 @3x)
> 
> 使用 `--clean-temp` 参数可在生成完成后自动删除临时文件（stats.json、ai_content.json、simplified_chat.txt、临时 HTML）
> 
> 图片生成需要安装 playwright：`pip install playwright && playwright install chromium`

## 聊天记录 JSON 格式

```json
{
  "meta": {
    "name": "群名称",
    "platform": "wechat",
    "type": "group"
  },
  "members": [
    {"platformId": "xxx", "accountName": "昵称", "groupNickname": "群昵称"}
  ],
  "messages": [
    {
      "sender": "platformId",
      "accountName": "昵称",
      "groupNickname": "群昵称",
      "timestamp": 1234567890,
      "type": 0,
      "content": "消息内容"
    }
  ]
}
```

> 💡 显示名称优先级：`groupNickname` > `accountName`

**消息类型 (type)**:
- `0`: 纯文本（脚本和 AI 分析此类型）
- `1`: 图片
- `2`: 语音转文字（脚本和 AI 分析此类型，内容格式：`[语音转文字] xxx`）
- `5`: 动画表情
- `99`: 系统消息

## 脚本分析内容（保证准确性）

| 数据 | 说明 |
|------|------|
| 总消息数 | 所有消息计数 |
| 活跃用户数 | 去重用户数 |
| 时间范围 | 首尾消息时间 |
| 话唠榜 TOP3 | 按发言数排序 + 常用词 |
| 熬夜冠军 | 23:00-06:00 最晚活跃者 |
| 词云数据 | jieba 分词 + 词频统计 |

## AI 生成内容（需要理解上下文）

| 内容 | 输入数据 |
|------|----------|
| 讨论热点 | 精简文本 + 词云 TOP50 |
| 成员画像 | 精简文本中的发言 |
| 有趣对话 | 高互动片段 |
| 问答识别 | 问号消息 ± 上下文 |
| 教程/资源 | 精简全文识别 |

## 依赖

```bash
pip install jieba jinja2 playwright
playwright install chromium
```
