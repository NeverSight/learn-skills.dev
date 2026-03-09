---
name: wechat-ai-publisher
description: 自动采集 AI 热门内容，撰写公众号文章，生成配图并发布到微信公众号草稿箱。当用户说"发布AI热点"、"写公众号文章"、"采集AI内容"、"publish AI news"时触发。
homepage: https://github.com/bbwdadfg/wechat-ai-publisher
metadata: {"openclaw":{"emoji":"📰","requires":{"bins":["bash","curl","jq"]}}}
---

# 微信公众号 AI 热点自动发布工具

## 完整链路

```
1. 询问用户配置（主题、风格、配图数量）
       ↓
2. Exa/Tavily 搜索采集 AI 热点资料
       ↓
3. 撰写文章（Markdown 格式）
       ↓
4. 调用 nanobanana API 生成配图
       ↓
5. 上传图片到微信服务器（获取 mmbiz URL）
       ↓
6. 转换为 HTML 并发布到公众号草稿箱
       ↓
7. 提示用户去微信公众号后台检查文章
```

---

## 配置信息

### 微信公众号 API

- **AppID**: `WECHAT_APPID`（通过环境变量配置）
- **AppSecret**: `WECHAT_SECRET`（通过环境变量配置）

### 图片生成 API

- **模型**: `google/nano-banana-pro`（通过 Replicate）
- **脚本**: `~/.codex/skills/article-illustrator/scripts/generate_image.py`（也可能是 `~/.claude/skills/...` 或 `~/.gemini/skills/...`，以你的工具为准）

> 配置方法见 `README.md`（本仓库已移除所有硬编码密钥/Token/本地路径）。

---

## 图片配字语言规则

**重要**：根据文章语言决定图片中的文字语言！

| 文章语言 | 图片 Prompt 语言 | 示例 |
|----------|------------------|------|
| 中文文章 | 中文配字 | "流程图展示：搜索新闻 → 撰写文章 → 生成配图 → 发布，中文标注" |
| 英文文章 | 英文配字 | "Flowchart: Search → Write → Generate → Publish, English labels" |

**Prompt 编写规则**：
- 中文文章：在 prompt 末尾加 `，中文标注，简体中文文字`
- 英文文章：在 prompt 末尾加 `, English text labels`

---

## 执行流程详解

### Step 1: 询问用户配置

**设计思路**：不同主题、风格、配图数量会影响后续所有步骤，所以先收集用户偏好。

如果是交互式运行，可以询问用户；如果是定时任务/自动运行（比如 OpenClaw Cron），则**不要提问**，直接从触发消息里解析参数或使用默认值。

#### 默认配置（建议固定一套）

- 主题：AI工具
- 风格：github
- 配图：封面 + 3 张
- 作者：田威 AI（环境变量 `WECHAT_AUTHOR` 默认值）

支持的参数（建议写在触发语句中）：
- `主题`：例如 `AI工具` / `大模型` / `AI Agent`
- `风格`：例如 `purple` / `orangeheart` / `github`
- `配图`：例如 `仅封面` / `封面+2张` / `封面+3张`
- `作者`：例如 `田威 AI`（会映射到环境变量 `WECHAT_AUTHOR`）

#### 覆盖规则（让用户“诉说”即可）

1. 如果用户/定时任务消息里出现 `主题=...` / `风格=...` / `配图=...` / `作者=...`，则覆盖默认值。
2. 其余自然语言描述（例如“写得更科普一些”“多强调边界和风险”“更偏护理视角”）视为写作约束，AI 可以自由调整结构与措辞以提升可读性。
3. 冲突时以用户指令为准；不确定就保守处理（不编造数据、不夸大结论）。

交互式询问（可选）：

**问题 1 - 文章主题**：
- AI Agent
- 大模型
- AI 工具
- 行业动态
- 自定义

**问题 2 - CSS 风格**：
- 紫色经典 purple（推荐）
- 橙心暖色 orangeheart
- GitHub风格 github
- 其他...

**问题 3 - 配图数量**：
- 仅封面图
- 封面 + 2张配图
- 封面 + 3张配图（推荐）

---

### Step 2: 搜索采集 AI 热点（两阶段深度采集）

**问题**：简单搜索只返回标题和 200 字摘要，内容太浅，写不出有深度的文章。

**解决方案**：两阶段采集

```
阶段 1：广度搜索（发现）
  ↓ 筛选 3-5 篇高质量文章
阶段 2：深度抓取（提取）
  ↓ 获取完整原文内容
```

---

#### 阶段 1：广度搜索（发现相关文章）

**设计思路**：
- **为什么用 Tavily/Exa？** 专为 AI 优化，返回结构化数据
- **为什么搜 3 天？** 太短没素材，太长不新鲜
- **为什么要 10 条？** 足够筛选，但不会太多

**Tavily vs Exa 选择**：
| 场景 | 推荐 | 原因 |
|------|------|------|
| 新闻热点 | Tavily | `topic="news"` 专门优化新闻搜索 |
| 技术文档 | Exa | 对技术内容索引更全面 |
| 综合搜索 | 两者并用 | 互补，覆盖更广 |

```python
# Tavily 搜索（适合新闻热点）
mcp__tavily__tavily-search(
    query="AI artificial intelligence news {主题}",
    topic="news",
    days=3,
    max_results=10,
    search_depth="advanced"  # 使用高级搜索
)

# Exa 搜索（适合技术内容）
mcp__exa__web_search_exa(
    query="AI {主题} latest news tutorial",
    numResults=10
)
```

**筛选标准**（从 10 条中选 3-5 条）：
1. **相关性**：与主题直接相关，不是泛泛而谈
2. **深度**：有具体案例、数据、代码，不是纯新闻稿
3. **新鲜度**：优先最近 3 天的内容
4. **来源质量**：优先技术博客、官方文档、知名媒体

---

#### 阶段 2：深度抓取（获取完整原文）

**关键**：使用 `tavily-extract` 抓取完整文章内容！

```python
# 深度抓取选中的文章（返回完整原文，可达 2 万字）
mcp__tavily__tavily-extract(
    urls=[
        "https://example.com/article1",
        "https://example.com/article2",
        "https://example.com/article3"
    ],
    extract_depth="advanced"  # 高级提取，获取更多内容
)
```

**对比效果**：
| 方法 | 返回内容 | 适用场景 |
|------|----------|----------|
| `tavily-search` | 标题 + 200字摘要 | 发现文章 |
| `tavily-extract` | 完整原文（可达2万字） | 深度阅读 |
| `exa web_search` | 标题 + 摘要 + 部分正文 | 快速了解 |

**为什么要深度抓取？**
- 摘要只有观点，没有论据
- 完整原文有案例、数据、代码
- 深度内容才能写出有价值的文章

---

#### 素材整理模板

抓取完成后，整理成以下格式：

```markdown
## 素材 1：[文章标题]
- **来源**：[URL]
- **核心观点**：[1-2 句话总结]
- **关键数据/案例**：
  - [具体数据点 1]
  - [具体案例 1]
  - [代码片段（如有）]
- **可引用的金句**：[原文中的精彩表述]

## 素材 2：[文章标题]
...

## 素材 3：[文章标题]
...
```

**整理要点**：
1. 提取具体数据（数字、百分比、对比）
2. 提取真实案例（谁用了、怎么用、效果如何）
3. 提取代码片段（如果是技术文章）
4. 记录可引用的原文表述（增加可信度）

---

#### 完整采集流程示例

```python
# 1. 广度搜索
search_results = mcp__tavily__tavily-search(
    query="Claude Code Skills tutorial 2025",
    topic="general",
    max_results=10,
    search_depth="advanced"
)

# 2. 筛选高质量文章（人工或自动）
selected_urls = [
    "https://huggingface.co/blog/...",
    "https://www.siddharthbharath.com/claude-skills/",
    "https://www.youngleaders.tech/p/..."
]

# 3. 深度抓取
full_content = mcp__tavily__tavily-extract(
    urls=selected_urls,
    extract_depth="advanced"
)

# 4. 整理素材（见上方模板）
```

---

### Step 3: 撰写文章

**设计思路**：
- **为什么用 Markdown？** 结构清晰，易于转换为 HTML，支持代码块
- **为什么标记配图位置？** 让后续步骤知道在哪里插入图片，以及图片应该表达什么
- **为什么用科普/护理/科技风格？** 准确克制、步骤清晰、强调边界与可落地性

参考示例文章：[examples/nursing-tech-article.md](./examples/nursing-tech-article.md)

**文章结构设计**：
```
引子（钩子开头，抛出问题或观点）
  ↓
核心内容（3-5 个分点，每点配一张图）
  ↓
价值总结（明确结论）
  ↓
行动号召（引导读者下一步）
```

**输出格式**：Markdown，用注释标记配图位置和描述

```markdown
# 文章标题

开头段落（钩子，吸引读者继续阅读）...

## 第一部分

内容...

<!-- IMAGE_1: 图片描述（根据文章语言决定中英文） -->
<!-- 图片应该可视化这部分的核心概念 -->

## 第二部分

内容...

<!-- IMAGE_2: 图片描述 -->

## 第三部分

内容...

<!-- IMAGE_3: 图片描述 -->

## 总结

结尾（明确结论 + 行动号召）...
```

**配图位置选择原则**：
- **前 1/3**：可视化核心概念或问题
- **中间 1/3**：展示流程、对比或数据
- **后 1/3**：总结图或行动引导

---

### Step 4: 调用 nanobanana 生成配图

**设计思路**：
- **为什么用 nanobanana？** Google 的 Imagen 3 模型，生成质量高，支持中文
- **为什么封面用 16:9？** 公众号封面最佳比例，在列表中显示效果好
- **为什么配图用 4:3？** 文章内图片的标准比例，阅读体验好
- **为什么要中文配字？** 中文文章配中文图，视觉一致性更好

**必须使用 article-illustrator 的脚本**（通过环境变量配置 API Key）：

```bash
# 生成封面图（16:9，横版，适合列表展示）
python3 ~/.codex/skills/article-illustrator/scripts/generate_image.py \
  --prompt "封面图描述，中文标注" \
  --output "/tmp/wechat_cover.png" \
  --aspect-ratio "16:9"

# 生成配图（4:3，适合文章内嵌）
python3 ~/.codex/skills/article-illustrator/scripts/generate_image.py \
  --prompt "配图描述，中文标注" \
  --output "/tmp/wechat_img1.png" \
  --aspect-ratio "4:3"
```

**Prompt 编写技巧**：
```
[主题] + [具体内容] + [视觉风格] + [颜色调性] + [语言标注]
```

**Prompt 示例**（中文文章）：
- 封面："AI 自动化工作流程图，展示从命令到发布的完整链路，科技感蓝色调，简洁扁平设计，中文标注"
- 配图1："开发者配置 API 的界面示意图，显示 AppID 输入框，深色主题 UI，中文标注"
- 配图2："Python 代码编辑器截图风格，显示图片生成函数，VS Code 深色主题"
- 配图3："微信公众号后台草稿箱界面，显示文章列表，绿色微信品牌色，中文标注"

**常见问题**：
- 图片没有中文？→ 确保 prompt 末尾加"，中文标注，简体中文文字"
- 图片风格不一致？→ 所有图片使用相同的风格描述词

---

### Step 5: 上传图片到微信服务器

**设计思路**：
- **为什么还要上传到微信？** 公众号文章只能显示 `mmbiz.qpic.cn` 域名的图片，外部图片会被过滤
- **为什么有两个接口？** 封面图和文章内图片的处理方式不同
- **为什么 access_token 要每次获取？** 有效期只有 2 小时，不能缓存

**重要**：公众号文章只能显示微信域名的图片！

```python
import os
import requests

# 1. 获取 access_token（有效期 2 小时）
token_resp = requests.get(
    "https://api.weixin.qq.com/cgi-bin/token",
    params={
        "grant_type": "client_credential",
        "appid": os.environ["WECHAT_APPID"],
        "secret": os.environ["WECHAT_SECRET"]
    }
)
access_token = token_resp.json()["access_token"]

# 2. 上传封面图（永久素材接口，返回 media_id）
#    用于草稿的 thumb_media_id 字段
with open("/tmp/wechat_cover.png", "rb") as f:
    thumb_resp = requests.post(
        f"https://api.weixin.qq.com/cgi-bin/material/add_material"
        f"?access_token={access_token}&type=image",
        files={"media": ("cover.png", f, "image/png")}
    )
thumb_media_id = thumb_resp.json()["media_id"]

# 3. 上传文章内配图（图文消息内图片接口，返回 URL）
#    返回的 URL 可以直接嵌入 HTML
with open("/tmp/wechat_img1.png", "rb") as f:
    img_resp = requests.post(
        f"https://api.weixin.qq.com/cgi-bin/media/uploadimg"
        f"?access_token={access_token}",
        files={"media": ("img1.png", f, "image/png")}
    )
img1_url = img_resp.json()["url"]
# 返回: http://mmbiz.qpic.cn/sz_mmbiz_png/...
```

**两个接口的区别**：

| 接口 | 用途 | 返回值 | 使用场景 |
|------|------|--------|----------|
| `/material/add_material` | 永久素材 | media_id | 封面图（thumb_media_id） |
| `/media/uploadimg` | 图文消息内图片 | mmbiz URL | 文章内嵌图片 |

**为什么这样设计？**
- 封面图需要 media_id 是因为草稿 API 要求用 ID 引用
- 文章内图片需要 URL 是因为 HTML 里用 `<img src="">` 引用

---

### Step 6: 转换 HTML 并发布草稿

**设计思路**：
- **为什么要转 HTML？** 公众号不支持 Markdown，只接受 HTML
- **为什么用内联 CSS？** 公众号会过滤 `<style>` 标签，只有内联样式才生效
- **为什么 ensure_ascii=False？** 否则中文会变成 `\uXXXX` 编码，微信无法正确显示

```python
import json

# 1. 构建 HTML（使用微信返回的图片 URL）
#    所有样式必须内联，不能用 class
html_content = f'''
<section style="font-family: -apple-system, sans-serif; line-height: 1.8; color: #333; padding: 15px;">
  <p style="margin-bottom: 20px;">段落内容</p>

  <h2 style="border-bottom: 1px solid #eee; padding-bottom: 8px;">标题</h2>

  <p style="text-align: center; margin: 25px 0;">
    <img src="{img1_url}" style="max-width: 100%; border-radius: 6px;">
  </p>

  <blockquote style="background: #f6f8fa; border-left: 4px solid #ddd; padding: 12px 16px;">
    引用内容
  </blockquote>
</section>
'''

# 2. 构建草稿数据
draft_data = {
    "articles": [{
        "title": "文章标题（不超过21个中文字符）",
        "digest": "文章摘要（会显示在分享卡片上）",
        "content": html_content,
        "thumb_media_id": thumb_media_id,  # 封面图 ID
        "need_open_comment": 1,            # 开启评论
        "only_fans_can_comment": 0         # 所有人可评论
    }]
}

# 3. 发布草稿（关键：ensure_ascii=False）
response = requests.post(
    f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={access_token}",
    data=json.dumps(draft_data, ensure_ascii=False).encode('utf-8'),
    headers={"Content-Type": "application/json; charset=utf-8"}
)
result = response.json()
# 成功返回: {"media_id": "草稿ID"}
```

**HTML 样式要点**：
- 所有样式必须内联（`style="..."`）
- 图片加 `max-width: 100%` 防止溢出
- 使用系统字体栈保证跨平台一致性
- 行高 1.8-2.0 提升阅读体验

**常见错误**：
- 中文乱码？→ 检查 `ensure_ascii=False`
- 样式不生效？→ 检查是否用了内联样式
- 图片不显示？→ 检查是否用了微信返回的 URL

---

### Step 7: 提示用户检查

**设计思路**：
- **为什么要提示检查？** 自动发布的是草稿，需要人工确认后才能正式发布
- **为什么要输出 R2 链接？** 方便用户在其他平台复用图片
- **为什么要输出草稿 ID？** 方便后续通过 API 操作（如删除、修改）

发布完成后，输出：

```
✅ 发布完成！

📝 文章信息
- 标题：xxx
- 摘要：xxx
- 风格：xxx

📤 公众号
- 草稿 ID：xxx
- 请前往微信公众号后台检查文章：https://mp.weixin.qq.com

⚠️ 检查要点：
1. 图片是否正常显示
2. 排版是否正确
3. 标题和摘要是否合适
4. 确认无误后点击"发布"
```

---

## CSS 风格配置

| 风格 ID | 名称 | 标题色 | 正文色 | 引用背景 |
|---------|------|--------|--------|----------|
| `purple` | 紫色经典 | #8064a9 | #444444 | #f4f2f9 |
| `orangeheart` | 橙心暖色 | #ef7060 | #000000 | #fff5f5 |
| `github` | GitHub风格 | #333333 | #333333 | #f6f8fa |

详细配置见 [styles.json](./styles.json)

---

## 注意事项

1. **图片语言**：中文文章用中文配字，英文文章用英文配字
2. **图片域名**：公众号只能显示 mmbiz.qpic.cn 域名的图片
3. **中文编码**：JSON 必须用 `ensure_ascii=False`
4. **标题长度**：最多 64 字节（约 21 个中文字符）
5. **access_token**：有效期 2 小时，每次需重新获取
6. **定时任务**：自动运行时不要提问，直接按参数/默认值执行
