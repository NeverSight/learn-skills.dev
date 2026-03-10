---
name: wechat-article-writer
description: 公众号/自媒体全流程。根据用户表述自动匹配：撰写文章、封面图、正文插图、风格提取。支持多种写作风格。当用户提到写公众号、技术博客、公众号封面、正文插图、步骤图、演示图、流程示意、分析写作风格、克隆文风、模仿爆款、提取风格时使用。详见 reference 目录。
---

# 公众号/自媒体创作

## 一、任务识别

根据用户需求选择执行路径：


| 任务类型    | 触发词                           | 执行                                                          |
| ------- | ----------------------------- | ----------------------------------------------------------- |
| 仅封面/结尾图 | 封面图、公众号封面、B站封面、小红书配图          | 读取 [cover_guide.md](reference/cover_guide.md)               |
| 仅正文插图   | 插图、步骤图、演示图、流程示意、前后对比          | 读取 [illustration_guide.md](reference/illustration_guide.md) |
| 撰写文章    | 写公众号、写文章、自媒体写作、爆款文章、内容创作      | 执行 Step 2–6                                                 |
| 风格提取    | 分析写作风格、克隆文风、模仿某篇、提取风格、范文转风格指南 | 执行「四、风格提取流程」                                                |


## 二、写作风格

撰写文章时，按用户指定选择风格文件；未指定则用默认风格。


| 序号  | 风格       | 触发词（互不重复）          | 参考文件                                                                           | 篇幅          |
| --- | -------- | ------------------ | ------------------------------------------------------------------------------ | ----------- |
| 1   | 默认       | （未指定时）             | [writing_style.md](reference/writing_style.md)                                 | 2000–4000 字 |
| 2   | 高流量/爆款   | 高流量、爆款、像 Skills 那篇 | [viral_style.md](reference/viral_style.md)                                     | 2500–4000 字 |
| 3   | 清单体/方法论  | 清单体、方法论、干货、步骤      | [checklist_methodology_style.md](reference/checklist_methodology_style.md)     | 2000–4000 字 |
| 4   | 资源盘点     | 盘点、替代方案、合集         | [resource_roundup_style.md](reference/resource_roundup_style.md)               | 3000–6000 字 |
| 5   | 个人实测推荐   | 个人实测、亲身推荐          | [personal_tool_review_style.md](reference/personal_tool_review_style.md)       | 4000–7000 字 |
| 6   | 认知颠覆     | 认知颠覆、反常识、观点文       | [contrarian_opinion_style.md](reference/contrarian_opinion_style.md)           | 2000–3500 字 |
| 7   | 身份共鸣/逆袭  | 身份共鸣、逆袭、你也行、转行经历   | [identity_transformation_style.md](reference/identity_transformation_style.md) | 2500–4000 字 |
| 8   | 故事化/情感共鸣 | 故事化、情感共鸣、人物故事      | [story_emotional_style.md](reference/story_emotional_style.md)                 | 2500–4500 字 |
| 9   | 深度随笔     | 深度思考、随笔、像日记那篇、个人感悟 | [personal_essay_style.md](reference/personal_essay_style.md)                   | 4000–7000 字 |


## 三、撰写流程（Step 2–6）

### Step 2：搜索资料

- 并行搜索多来源（官方文档、X/Twitter、Reddit、技术论坛等）
- 优先当月/当季最新资料
- 深度总结后再进入撰写

### Step 3：撰写文章

1. **读取风格文件**：按「二、写作风格」选择对应 reference 文件，严格遵循其写作规范与结尾语
2. **通用要求**：故事化开头、带情感色彩、准备 2–3 个备选标题

### Step 4：生成标题

生成 5 个爆款风格标题：痛点明确、数字吸引、结果导向、情绪调动、悬念设置。

### Step 5：排版优化

输出排版与配图建议：段落结构、配图位置（封面/正文/结尾）、代码块留白、金句单独成段。

### Step 6：生成配图（可选）

用户要求或排版建议中标注配图时：

- **封面/结尾图** → 读取 `reference/cover_guide.md`
- **正文插图** → 读取 `reference/illustration_guide.md`

输出 `.drawio` 文件及使用说明，配色与文章统一。

## 四、风格提取流程

当用户提供样本文章（全文粘贴或本地路径），希望分析风格、克隆文风、将范文转为风格指南时执行。

**先读取** [extraction_dimensions.md](reference/extraction_dimensions.md)，按统一维度提取。

### Step 1：任务确认

- 样本数量（1 篇或多篇）
- 使用目标（模仿写作 / 团队风格规范 / Prompt 固化）
- 是否保留作者口头禅、品牌词

### Step 2：结构拆解

提取：开头钩子模式、行文骨架、段落节奏、结尾动作。

### Step 3：语言与修辞拆解

提取：语气人称、句式与标点、高频词/过渡词/口头禅、修辞手法。

### Step 4：产出风格规则包

输出必须包含：风格画像（100–200 字）、可执行规则（15–30 条，必须/优先/避免）、风格复刻 Prompt、反向自检清单、边界声明。

### Step 5：验证与回放（可选）

若用户需要：同主题试写大纲、100–200 字试写段落、相似点/差异点说明。

**输出顺序**：样本概况 → 风格画像 → 风格规则包 → Prompt 模板 → 自检清单 → 边界声明

## 五、示例


| 用户请求                         | 执行                                          |
| ---------------------------- | ------------------------------------------- |
| 生成这篇文章的封面，16:9               | 读取 cover_guide.md 并生成                       |
| 生成 Cursor 启用四步骤的步骤图          | 读取 illustration_guide.md 并生成                |
| 帮我写一篇关于 Cursor Skills 的公众号文章 | Step 2–6 完整流程                               |
| 用高流量风格写一篇关于 Vibe Coding 的文章  | 读取 viral_style.md，按爆款风格撰写                   |
| 用资源盘点风格写免费传大文件替代方案           | 读取 resource_roundup_style.md，按盘点风格撰写        |
| 用深度随笔风格写 AI 时代记日记            | 读取 personal_essay_style.md，按随笔风格撰写          |
| 用个人实测风格写软件推荐                 | 读取 personal_tool_review_style.md，按实测推荐风格撰写  |
| 用清单体写提升效率的 5 个习惯             | 读取 checklist_methodology_style.md，按方法论风格撰写  |
| 用故事化风格写职场转型经历                | 读取 story_emotional_style.md，按情感共鸣风格撰写       |
| 用认知颠覆风格写「努力是最被高估的品质」         | 读取 contrarian_opinion_style.md，按反常识观点撰写     |
| 用身份共鸣风格写 30 岁转行做自媒体          | 读取 identity_transformation_style.md，按逆袭叙事撰写 |
| 分析这篇公众号文章的写作风格、提取可复用规则       | 执行「四、风格提取流程」                                |