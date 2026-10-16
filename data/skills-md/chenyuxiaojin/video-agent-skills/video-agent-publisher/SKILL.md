---
name: video-agent-publisher
description: >
  视频团队的发布员。生成各平台（抖音/B站/YouTube）的发布元数据，
  包括标题、描述、标签、BGM推荐，以及引用出处列表。
  触发条件："准备发布素材"、"生成封面和标题"、"生成发布信息"
---

# video-agent-publisher

认知成长视频团队的运营。生成各平台（抖音/B站/YouTube）的发布元数据，包括标题、描述、标签，以及引用出处列表。

## 触发条件

- 「准备发布素材」
- 「生成封面和标题」
- 「生成发布信息」
- 由制片人（producer）调度时自动触发

## 输入 → 输出

- 输入：`script.md` + `materials/sources.json`
- 输出：`publish/metadata.json` + `publish/sources.md`

## 平台规则

- 抖音：标题 ≤ 30 字，描述 ≤ 300 字，标签 5-10 个
- B 站：标题 ≤ 40 字，描述 ≤ 250 字，标签 ≤ 12 个
- YouTube：标题 ≤ 100 字符，描述 ≤ 5000 字符，标签 ≤ 500 字符总长
- 所有平台标题都需要包含钩子元素

## 处理流程

### 步骤 1：读取输入文件

读取 script.md 和 sources.json，提取主题、论点、关键词。

### 步骤 2：生成发布元数据

```bash
python scripts/generate_metadata.py <script.md> <outline.md> [output_dir]
```

生成 metadata.json，包含：
- 多个标题候选（不同风格）
- 视频描述
- 标签/Hashtags
- BGM 推荐

### 步骤 3：整理引用出处

```bash
python scripts/compile_sources_list.py <script.md> [output.md]
```

从逐字稿中提取所有【出处：...】标注，生成格式化的引用列表。

## 标题生成策略

| 策略 | 模板 | 适用场景 |
|------|------|----------|
| 疑问式 | 为什么 [主题] 如此重要？ | 引发好奇心 |
| 数字式 | 关于 [主题]，你必须知道的 N 件事 | 信息密度高 |
| 反常识 | 你以为的 [主题]，可能完全是错的 | 颠覆认知 |
| 故事式 | 从 [案例] 说起：重新理解 [主题] | 叙事型内容 |

## BGM 推荐规则

| 内容类型 | 推荐风格 | 关键词 |
|----------|----------|--------|
| 认知/科普 | 轻松思考 | calm, thinking, ambient |
| 故事/叙事 | 温暖叙事 | warm, narrative, gentle |
| 励志/成长 | 积极向上 | uplifting, inspiring, motivational |
| 反思/深度 | 沉静内省 | reflective, minimal, piano |

推荐来源：Pixabay Music（免费商用）

## metadata.json 格式

```json
{
  "topic": "主题",
  "titles": ["标题1", "标题2", "标题3", "标题4"],
  "description": "视频描述",
  "hashtags": ["#标签1", "#标签2"],
  "keywords": ["关键词1", "关键词2"],
  "recommended_bgm": [
    {"name": "名称", "mood": "风格", "source": "pixabay"}
  ]
}
```

## 依赖

- Python 3：标准库（json, re, pathlib）

## 脚本文件

- `scripts/generate_metadata.py` - 发布元数据生成
- `scripts/compile_sources_list.py` - 引用出处整理
