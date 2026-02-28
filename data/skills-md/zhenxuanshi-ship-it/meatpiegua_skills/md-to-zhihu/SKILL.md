---
name: md-to-zhihu
description: Convert markdown articles to Zhihu (知乎) publishing format and one-click publish articles. Use when the user wants to publish markdown content to Zhihu, convert articles for Zhihu, or mentions 知乎、知乎专栏、知乎发布、发布到知乎.
---

# Markdown 一键发布到知乎

将 Markdown 文章转换为知乎文章编辑器可接受的格式，支持多种排版风格预览，并可一键发布到知乎专栏。

## 快速使用

### 依赖安装

```bash
# 格式转换依赖
pip install markdown pygments beautifulsoup4

# 一键发布依赖（可选，仅发布时需要）
pip install playwright requests
playwright install chromium
```

### 格式转换（单篇）

```bash
python ~/.cursor/skills/md-to-zhihu/scripts/convert.py input.md
```

**参数说明：**

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `input.md` | 输入的 Markdown 文件路径 | 必填 |
| `-o output.html` | 输出 HTML 文件路径 | `{input}_zhihu.html` |
| `--theme` | 主题风格 | `zhihu` |
| `--content-only` | 仅输出纯净 HTML 内容（用于 API 发布） | 否 |
| `--dir` | 批量转换：指定目录路径 | - |

### 批量转换（整个目录）

```bash
# 转换目录下所有 .md 文件
python ~/.cursor/skills/md-to-zhihu/scripts/convert.py --dir ./articles

# 批量转换，指定主题
python ~/.cursor/skills/md-to-zhihu/scripts/convert.py --dir ./articles --theme tech
```

### 一键发布（单篇）

```bash
# 首次使用：登录知乎并保存 Cookie
python ~/.cursor/skills/md-to-zhihu/scripts/publish.py --login

# 发布文章
python ~/.cursor/skills/md-to-zhihu/scripts/publish.py input.md

# 保存为草稿
python ~/.cursor/skills/md-to-zhihu/scripts/publish.py input.md --draft

# 指定标题和话题
python ~/.cursor/skills/md-to-zhihu/scripts/publish.py input.md --title "文章标题" --topic "AI,编程"
```

### 批量发布（整个目录）

```bash
# 批量发布目录下所有 .md 文件
python ~/.cursor/skills/md-to-zhihu/scripts/publish.py --dir ./articles

# 批量保存为草稿
python ~/.cursor/skills/md-to-zhihu/scripts/publish.py --dir ./articles --draft

# 批量发布，设置话题和自定义间隔（默认60s）
python ~/.cursor/skills/md-to-zhihu/scripts/publish.py --dir ./articles --topic "AI,编程" --delay 30
```

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--dir` | 批量发布：指定目录路径，发布所有 .md | - |
| `--delay` | 每篇文章发布间隔秒数（防限流） | `60` |
| `--draft` | 仅保存为草稿 | 否 |
| `--topic` | 文章话题，逗号分隔 | - |

## 可用主题

- **zhihu** (知乎蓝)：知乎官方蓝色调，专业简洁，推荐默认使用
- **elegant** (优雅灰)：深灰色调，沉稳大气，适合深度长文
- **tech** (科技紫)：紫色/靛蓝色调，现代科技感，适合技术文章
- **warm** (温暖橙)：橙色暖色调，活泼亲和，适合故事/经验分享
- **nature** (自然绿)：绿色清新调，自然舒适，适合科普/生活文章

## 支持的 Markdown 元素

- 标题 (h1-h4)，h1 自动提取为文章标题
- 段落，两端对齐
- **加粗**、*斜体*、~~删除线~~
- 超链接（知乎支持跳转）
- 有序/无序列表，含嵌套
- 代码块（带语法高亮和语言标签）
- 行内代码
- 表格（带斑马纹）
- 引用块
- 分割线
- 图片（居中自适应，带图注）
- 脚注
- 任务列表

## 使用流程

### 方式一：预览 + 手动粘贴

1. 执行转换命令，生成 HTML 文件
2. 用浏览器打开生成的 HTML 文件
3. 点击页面顶部「复制内容到剪贴板」按钮
4. 在知乎文章编辑器中 `Ctrl+V` 粘贴

### 方式二：一键自动发布

1. 首次使用先运行 `--login` 登录
2. 执行发布命令，脚本自动完成发布
3. 发布成功后会输出文章链接

## 注意事项

- 首次发布需要通过浏览器登录知乎，Cookie 会保存供后续使用
- Cookie 过期后需要重新登录（`--login`）
- 图片需使用可公开访问的 URL，本地图片需先上传到图床
- 发布前建议先用预览模式检查排版效果
- 知乎对文章长度有限制，超长文章建议分篇发布
