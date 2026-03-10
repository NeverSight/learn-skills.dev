---
name: md-to-wechat
description: Convert markdown articles to WeChat Official Account (微信公众号) publishing format with beautiful inline-styled HTML. Use when the user wants to publish markdown content to WeChat, convert articles for WeChat public account, or mentions 微信公众号、公众号排版、公众号发布.
---

# Markdown 转微信公众号格式 & 一键发布

将 Markdown 文章转换为微信公众号编辑器可直接粘贴的富文本 HTML，排版美观大方，代码高亮、表格、目录等元素均正确渲染。支持通过 API 一键创建草稿/发布到微信公众号。

## 快速使用

### 依赖安装

```bash
# 格式转换依赖
pip install markdown pygments beautifulsoup4

# 一键发布依赖（可选，仅发布时需要）
pip install requests

# 更好的默认封面图（可选）
pip install Pillow
```

### 格式转换（单篇）

```bash
python ~/.cursor/skills/md-to-wechat/scripts/convert.py input.md
```

**参数说明：**

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `input.md` | 输入的 Markdown 文件路径 | 必填 |
| `-o output.html` | 输出 HTML 文件路径 | `{input}_wechat.html` |
| `--theme` | 主题风格：`blue` / `green` / `dark` / `warm` | `blue` |
| `--dir` | 批量转换：指定目录路径 | - |

### 批量转换（整个目录）

```bash
# 转换目录下所有 .md 文件
python ~/.cursor/skills/md-to-wechat/scripts/convert.py --dir ./articles

# 批量转换，指定主题
python ~/.cursor/skills/md-to-wechat/scripts/convert.py --dir ./articles --theme green
```

### 一键发布 - 配置（首次）

```bash
# 首次使用：配置 AppID 和 AppSecret
python ~/.cursor/skills/md-to-wechat/scripts/publish.py --setup
```

需要在微信公众平台获取：
1. 进入 **公众号后台 → 设置与开发 → 基本配置**
2. 获取 **AppID** 和 **AppSecret**
3. 将本机 IP 添加到 **IP 白名单**

### 一键发布（单篇）

```bash
# 创建草稿（推荐，可在公众号后台检查后手动发布）
python ~/.cursor/skills/md-to-wechat/scripts/publish.py input.md

# 创建草稿并直接发布
python ~/.cursor/skills/md-to-wechat/scripts/publish.py input.md --publish

# 指定标题、作者和封面图
python ~/.cursor/skills/md-to-wechat/scripts/publish.py input.md --title "文章标题" --author "作者" --thumb cover.jpg
```

### 批量发布（整个目录）

```bash
# 批量创建草稿
python ~/.cursor/skills/md-to-wechat/scripts/publish.py --dir ./articles

# 批量创建草稿并发布
python ~/.cursor/skills/md-to-wechat/scripts/publish.py --dir ./articles --publish

# 批量操作，自定义间隔（默认60s）
python ~/.cursor/skills/md-to-wechat/scripts/publish.py --dir ./articles --delay 30
```

**发布参数说明：**

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--setup` | 配置 AppID/AppSecret | - |
| `--publish` | 创建草稿后直接发布 | 否（仅创建草稿） |
| `--title` | 文章标题 | 自动从 h1 提取 |
| `--author` | 文章作者 | 空 |
| `--thumb` | 封面图片路径（建议 900x500+） | 自动生成默认封面 |
| `--theme` | 文章主题风格 | `blue` |
| `--dir` | 批量操作：指定目录路径 | - |
| `--delay` | 每篇文章操作间隔秒数（防限流） | `60` |

## 使用流程

### 方式一：预览 + 手动粘贴

1. 执行转换命令，生成 HTML 文件
2. 用浏览器打开生成的 HTML 文件
3. 点击页面顶部「复制内容到剪贴板」按钮
4. 在微信公众号后台编辑器中 `Ctrl+V` 粘贴即可

### 方式二：API 一键创建草稿（推荐）

1. 首次使用先运行 `--setup` 配置凭据
2. 执行发布命令，脚本自动创建草稿
3. 前往公众号后台检查草稿内容，确认后手动群发

### 方式三：API 一键发布

1. 首次使用先运行 `--setup` 配置凭据
2. 执行 `--publish` 命令，脚本自动创建草稿并发布
3. 注意：API 发布的文章**不会推送给粉丝**，如需推送请在后台手动群发

## 可用主题

- **blue** (优雅蓝)：蓝色系，专业简洁，适合技术/商务文章
- **green** (清新绿)：绿色系，自然清新，适合生活/科普文章
- **dark** (经典黑)：黑色系，沉稳大气，适合深度/学术文章
- **warm** (温暖橙)：橙色系，活泼温暖，适合营销/故事文章

## 支持的 Markdown 元素

- 标题 (h1-h4)，带装饰样式
- 段落，两端对齐
- **加粗**、*斜体*、~~删除线~~
- 有序/无序列表，含嵌套
- 代码块（带语法高亮和语言标签）
- 行内代码
- 表格（带斑马纹）
- 引用块
- 分割线
- 图片（居中自适应，自动上传到微信素材库）
- 脚注
- 任务列表

## 注意事项

- 微信编辑器不支持外部链接跳转，链接会显示为带下划线的文字
- 一键发布时，文章内的外部图片会自动上传到微信素材库
- 手动粘贴模式下，图片需要先上传到微信素材库
- 所有样式均为内联 CSS，确保在微信编辑器中完整保留
- 代码块在移动端会自动横向滚动
- 首次发布需要配置 AppID/AppSecret 并将 IP 加入白名单
- access_token 有效期 2 小时，脚本会自动缓存和刷新
- 通过 API 发布的文章不会出现在粉丝的订阅消息中，需手动群发
- 2025年7月起，个人主体/未认证账号将被回收发布接口权限
