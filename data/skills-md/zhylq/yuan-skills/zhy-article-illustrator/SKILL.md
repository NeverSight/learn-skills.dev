---
name: zhy-article-illustrator
version: 1.2.0
description: >
  Use when illustrating a Markdown article with high-finish editorial visuals,
  visual-bible planning, structured prompts, optional Qiniu upload, and inserted
  image references for article publishing workflows.
inputs:
  - name: article_path
    type: string
    required: true
    description: 文章 Markdown 文件路径（如 articles/my-topic/article.md）
  - name: slug
    type: string
    required: false
    description: 输出目录标识（kebab-case）。若不提供，从文章标题自动推导
    default: ""
  - name: density
    type: string
    required: false
    description: "配图密度：minimal（1-2 张）| balanced（每主要章节一张）| rich（尽量多配）"
    default: balanced
  - name: upload
    type: boolean
    required: false
    description: 是否上传到七牛云图床并替换为 CDN URL
    default: false
  - name: aspect_ratio
    type: string
    required: false
    description: "图片宽高比，如 16:9、4:3、1:1"
    default: "16:9"
  - name: prompt_profile
    type: string
    required: false
    description: 提示词配置档案。默认 `nano-banana`，强调高完成度编辑视觉与强风格统一
    default: nano-banana
  - name: text_language
    type: string
    required: false
    description: 图片内默认文字语言。推荐 `zh-CN`
    default: zh-CN
  - name: english_terms_whitelist
    type: array
    required: false
    description: 允许在图片中保留英文展示的术语白名单，如产品名、协议名、缩写
    default: []
  - name: image_provider
    type: string
    required: false
    description: 生图通道，默认 `xiaomi`。支持 Gemini 官方直连、Gemini 原生代理，或 Xiaomi Gemini 兼容接口
    default: xiaomi
  - name: image_model
    type: string
    required: false
    description: 生图模型名称。默认使用接口调用时的 `gemini-3.1-flash-image-preview`
    default: gemini-3.1-flash-image-preview
  - name: image_base_url
    type: string
    required: false
    description: 生图 API 基础地址。可传入 Xiaomi Gemini 兼容接口、官方 Gemini 地址或自建代理地址；未提供时由运行环境决定默认值
outputs:
  - name: illustrated_article_path
    type: string
    description: 插入图片引用后的文章副本路径（article.illustrated.md）
  - name: illustrations_dir
    type: string
    description: 生成图片所在的目录路径
  - name: outline_path
    type: string
    description: 配图规划文件路径（outline.md）
  - name: visual_bible_path
    type: string
    description: 文章级视觉基线文件路径（visual-bible.md）
  - name: image_count
    type: integer
    description: 成功生成的图片数量
  - name: failed_count
    type: integer
    description: 生成失败的图片数量
  - name: uploaded_urls
    type: array
    description: 上传成功的 CDN URL 列表（仅 upload=true 时有值）
---

# zhy-article-illustrator

## Purpose

为任意 Markdown 文章自动规划并生成配图。技能默认采用“高完成度编辑视觉”作为
全局质量基线：不是简单插画，不是装饰图标拼贴，也不是低信息密度草图。系统会先
为文章生成统一的 visual bible，再为每张图生成结构化提示词，使同一篇文章的配图
共享统一风格语言，同时根据章节内容调整构图、信息重点和版式。

默认优先兼容 Gemini Nano Banana 工作流，并默认走 Xiaomi Gemini 兼容接口；同时支持 Gemini 原生代理 / 中转站模式与官方 Gemini 接口。

## When to Use

- 用户请求“为文章配图”、“illustrate article”、“add images to article”
- `zhy-wechat-writing` 技能的 Step 6 调用（`with_illustrations=true`）
- 用户希望生成更适合公众号场景的高完成度专题视觉
- 用户希望将本地图片上传到七牛云获取 CDN URL

## Prerequisites

- 文章 Markdown 文件已存在
- 已配置至少一种可用生图通道：
  - Gemini 官方直连：`GEMINI_API_KEY` 或 `GOOGLE_API_KEY`
  - Gemini 原生代理 / 中转站：`IMAGE_PROVIDER=gemini`、`IMAGE_API_KEY`、可选 `IMAGE_BASE_URL`
  - Xiaomi Gemini 兼容接口：`IMAGE_PROVIDER=xiaomi` 或 `XIAOMI_API_KEY`，可选 `XIAOMI_BASE_URL`
  - 若启用上传：七牛云配置已就绪（技能根目录 `.env` 中的 `QINIU_ACCESS_KEY` / `QINIU_SECRET_KEY` / `QINIU_BUCKET` / `QINIU_DOMAIN`）

## Workflow

### Step 1: 分析文章

**目标**：理解文章结构，确定配图数量、位置与表达方式

**操作**：
1. 读取 `article_path` 的完整内容
2. 解析文章结构：标题、各章节标题（`##` / `###`）、段落数、代码块位置
3. 识别核心信息点：
   - 关键概念 / 术语解释 -> 适合信息图
   - 对比 / 差异描述 -> 适合对比图
   - 步骤 / 流程描述 -> 适合流程图
   - 架构 / 框架描述 -> 适合架构图
   - 数据 / 统计 -> 适合数据可视化
   - 场景 / 叙事描述 -> 适合专题插画或编辑场景图
4. 根据 `density` 确定配图策略：
   - `minimal`：仅为最核心的 1-2 个信息点配图
   - `balanced`：每个 `##` 级主要章节配一张图
   - `rich`：每 300 字左右或每个重要段落配一张图
5. 确定 `slug`：
   - 若用户提供 `slug`：直接使用
   - 否则从文章 H1 标题推导 `kebab-case`
6. 创建输出目录：`{article_dir}/illustrations/{slug}/`

**输出**：文章结构分析结果、配图位置列表

### Step 2: 生成 visual bible 与配图规划

**目标**：为整篇文章建立统一视觉基线，并生成每张图的规划信息

**操作**：
1. 先生成文章级 `visual_bible`，保存到 `{article_dir}/illustrations/{slug}/visual-bible.md`
2. `visual_bible` 必须覆盖：
   - `quality_baseline`：统一采用高完成度编辑视觉 / 专题配图标准
   - `visual_theme`：本篇文章的整体风格方向
   - `color_system`：主色、辅色、强调色、背景倾向
   - `graphic_language`：图形语言、线条/材质/光感、信息层级方式
   - `layout_discipline`：页面留白、模块密度、标题区与内容区节奏
   - `text_policy`：默认简体中文；仅 `english_terms_whitelist` 中的术语保留英文
   - `negative_rules`：禁止简单画图、低幼卡通、无意义装饰、英文乱码、随意混搭风格
3. 再对每个配图位置生成 outline 条目，至少包含：
   - `position`：插入位置（在哪个章节/段落之后）
   - `purpose`：这张图要传达什么信息
   - `image_type`：对比图 / 流程图 / 架构图 / 数据图 / 场景图 / 编辑专题视觉
   - `core_message`：本图唯一核心表达
   - `content_blocks`：画面中必须出现的内容块
   - `text_blocks`：图中需要出现的标题、标签、注释（默认中文）
   - `english_terms_used`：本图允许出现的英文术语子集
   - `layout_hint`：布局方向与信息分区
   - `filename`：输出文件名（格式：`NN-简短描述.png`）
   - `alt_text`：Markdown 图片的 alt 文本
4. 保存到 `{article_dir}/illustrations/{slug}/outline.md`
5. 同时为每张图生成独立提示词文件，保存到 `{article_dir}/illustrations/{slug}/prompts/`

**outline.md 格式**：
```yaml
---
article: <article_path>
slug: <slug>
density: <density>
aspect_ratio: <ratio>
prompt_profile: <profile>
text_language: <language>
image_provider: <provider>
image_model: <model>
image_count: <N>
generated_at: <ISO timestamp>
---
```

**输出**：`visual_bible_path`、`outline_path`

### Step 3: 生成图片

**目标**：根据 `visual_bible` + outline 生成高质量图片文件

**操作**：
1. 为每张图构建结构化提示词，提示词必须同时继承：
   - 全局质量基线：高完成度编辑视觉，而非简单画图
   - 文章级 `visual_bible`
   - 单图内容规划
2. 提示词必须包含以下层次：
   - `任务定位`：这是可直接用于公众号文章的成品级专题视觉
   - `风格锚点`：复用本篇文章统一视觉语言
   - `画面主体`：核心对象、信息模块、前中后景关系
   - `版式结构`：标题区、内容区、对比区、流程区、数据区的组织方式
   - `信息层级`：主标题、次要标签、补充说明的优先级
   - `文字规则`：默认所有可见文字使用简体中文；仅白名单术语保留英文
   - `质量要求`：丰富细节、清晰层级、强版式感、避免模板感
   - `禁止项`：低幼、空泛、装饰性过强、无意义图标堆砌、英文乱码
3. 对 Nano Banana / Gemini 类模型，优先优化以下特性：
   - 画面信息完整、指令明确、元素具体
   - 文本展示尽量短而准，避免大段说明文字
   - 同一篇文章的每张图共享统一色系、统一图形语言、统一完成度
   - 图片更像编辑专题视觉，而不是普通插图
4. 将所有提示词保存到 `{article_dir}/illustrations/{slug}/prompts/` 目录
5. 调用本技能内置脚本生成图片：
   - 脚本路径：`scripts/image-gen.ts`
   - 参数：`--prompt "<提示词内容>" --output "<输出路径>" --ar <宽高比>`
   - 可选：`--provider gemini|google|xiaomi|openai`
   - 可选：`--model <模型名>`
   - 可选：`--base-url <Gemini 原生代理基础地址>`
   - 可选：`--api-key <临时 key>`
   - 可选：`--image-size <清晰度/尺寸标识>`（如 Xiaomi 的 `1K`）
   - 可选：`--ref <参考图路径>`（Gemini 多模态场景）
   - **并行生成**：建议最多 4 个并发
6. 若需要一键完成规划 + 生图 + 插回文章，可直接调用：
   ```bash
   node scripts/illustrate-article.ts --article <article.md>
   ```
   - 若使用 Xiaomi Gemini 兼容接口，可补充：`--image-provider xiaomi --image-model gemini-3-pro-image-preview --image-size 1K`
7. 失败处理：
   - 单张失败 -> 重试一次，可微调提示词中的布局、文字密度或禁止项
   - 仍失败 -> 记录到失败列表，继续下一张
   - 不中断整体流程

**输出**：图片文件列表、失败列表

### Step 4: 上传图床（可选）

**触发条件**：`upload=true`

**目标**：将生成的图片上传到七牛云，获取 CDN URL

**操作**：
1. 检查七牛云配置：读取技能根目录 `.env`
2. 调用上传脚本：
   ```bash
   bun run scripts/qiniu-upload.ts --file <本地路径> --key <远程路径>
   ```
3. 远程 key 格式：`illustrations/{slug}/{filename}`
4. 逐张上传，记录每张的 CDN URL
5. 上传失败时保留本地路径，不中断流程

**输出**：`uploaded_urls` 列表（CDN URL 或 `null`）

### Step 5: 插入文章副本

**目标**：创建带有图片引用的文章副本

**操作**：
1. 复制 `article_path` 为 `article.illustrated.md`（同目录）
2. 在 outline 指定的每个位置插入图片引用：
   - 若已上传（有 CDN URL）：`![alt_text](CDN_URL)`
   - 若未上传：`![alt_text](illustrations/{slug}/{filename})`
3. 对生成失败的图片，插入占位注释：
   ```markdown
   <!-- IMAGE PLACEHOLDER: {filename} — {purpose} -->
   ```
4. 输出完成摘要：
   - `illustrated_article_path`
   - 成功 / 失败 / 上传统计
   - 失败图片列表及原因

**输出**：`illustrated_article_path`

## Data Flow

```text
article.md
    |
    v
Step 1: 分析文章结构 -> 配图位置列表
    |
    v
Step 2: 生成 visual-bible.md + outline.md
    |
    v
Step 3: 生成结构化 prompts -> illustrations/{slug}/*.png
    |
    v
Step 4: (--upload) 上传七牛云 -> CDN URLs
    |
    v
Step 5: 插入副本 -> article.illustrated.md
```

## Error Handling

| 失败场景 | 处理方式 |
|----------|----------|
| 文章文件不存在 | 立即报错退出 |
| Gemini / 代理配置缺失 | 提示用户配置 `IMAGE_PROVIDER`、`IMAGE_API_KEY`、可选 `IMAGE_BASE_URL`，或回退到官方 `GEMINI_API_KEY` |
| Xiaomi 接口配置缺失 | 提示用户配置 `IMAGE_PROVIDER=xiaomi` 或 `XIAOMI_API_KEY`，并按需设置 `XIAOMI_BASE_URL` / `XIAOMI_IMAGE_SIZE` |
| 单张图片生成失败 | 重试一次；仍失败记录跳过，继续下一张 |
| 文字过多导致效果差 | 精简标题/标签/注释长度后重试 |
| 七牛云配置缺失 | 提示用户配置技能根目录 `.env`，跳过上传步骤 |
| 七牛云上传失败 | 保留本地路径，记录错误，继续下一张 |
| slug 目录已存在 | 直接使用（覆盖同名文件） |

## Example Usage

**默认 Nano Banana 风格配图**：
```yaml
article_path: articles/playwright-introduction/article.md
density: balanced
prompt_profile: nano-banana
text_language: zh-CN
image_provider: xiaomi
image_model: gemini-3.1-flash-image-preview
image_base_url: https://your-compatible-endpoint.example/v1beta
image_size: 1K
upload: false
```

**通过 Gemini 原生代理生图**：
```yaml
article_path: articles/playwright-introduction/article.md
density: balanced
image_provider: gemini
image_model: gemini-3.1-flash-image-preview
image_base_url: https://your-relay.example.com/v1beta
upload: false
```

**通过 Xiaomi Gemini 兼容接口生图**：
```yaml
article_path: articles/playwright-introduction/article.md
density: balanced
image_provider: xiaomi
image_model: gemini-3.1-flash-image-preview
image_base_url: https://your-compatible-endpoint.example/v1beta
image_size: 1K
upload: false
```

**指定英文白名单术语**：
```yaml
article_path: articles/playwright-introduction/article.md
english_terms_whitelist:
  - Playwright
  - Chromium
  - Firefox
  - WebKit
```

## Notes

- 全局质量基线固定为高完成度编辑视觉，不生成简单装饰图
- 不同文章可以有不同视觉风格，但同一篇文章内必须共享统一风格体系
- 默认所有可见文字使用简体中文；仅白名单术语保留英文
- 始终创建副本（`article.illustrated.md`），不修改原文
- 图片引用强制使用相对路径和 `/` 分隔符（本地模式）
- 提示词保存到 `prompts/` 目录，便于追溯和手动调整后重新生成
- 可使用 `bun run scripts/plan-illustrations.ts --article <article.md>` 自动生成 `visual-bible.md`、`outline.md` 和 `prompts/`
- 可使用 `node scripts/illustrate-article.ts --article <article.md>` 一键完成规划、出图和 `article.illustrated.md` 生成
- Xiaomi/Gemini 兼容接口可通过 `image_provider=xiaomi` 与自定义 `image_base_url` 配置；开源仓库不预设任何私有中转地址
