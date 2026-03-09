---
name: mp-weixin-skills
description: 微信公众号文章管理工具。用于管理微信公众号文章的发布和更新。使用场景：需要将文章发布到微信公众号草稿箱时；需要更新已有草稿内容时；需要上传图片素材到微信素材库时。核心功能：通过 AI 将文档转换为微信公众号 HTML，然后使用 Python 脚本调用微信 API 完成素材上传和草稿管理。
license: MIT
---

# 微信公众号文章管理 Skill

## 概述

这是一个专门用于管理微信公众号文章发布的 Skill。当您需要将文章发布到微信公众号时，此 Skill 会：

1. **首先要求 AI 将文章转换为微信公众号格式的 HTML**
2. **然后使用 Python 脚本上传素材和创建草稿**

**核心原则：**
- **AI 负责**：文档转换（Markdown/Word/PDF → 微信公众号 HTML）
- **Skill 负责**：微信 API 操作（上传素材、草稿管理）

## 快速开始

### 使用前准备

1. **配置微信公众号 API 凭证**

在 `skills` 目录下或项目根目录创建 `.env` 文件：

```bash
# 微信公众号配置（必需）
WECHAT_APP_ID=your_app_id_here
WECHAT_APP_SECRET=your_app_secret_here

# 输出配置（可选）
OUTPUT_DIR=./output
TEMP_DIR=./temp

# 样式配置（可选）
TEMPLATE_NAME=default
THEME_COLOR=#07c160
```

2. **安装依赖**

```bash
pip install -e .
```

### 基本使用

**场景 1: 发布新文章**

```
请将这篇文章发布到微信公众号草稿箱
```

AI 会自动：
1. 将文档转换为微信公众号格式的 HTML
2. 生成封面图片
3. 上传到微信草稿箱

**场景 2: 仅转换格式（不上传）**

```bash
python3 scripts/cli.py publish article.md --no-api
```

生成的 HTML 文件保存在 `output/` 目录

**场景 3: 更新已有草稿**

```bash
python3 scripts/cli.py update <media_id>
```

**场景 4: 上传图片素材**

```bash
# 上传单张图片
python3 scripts/cli.py upload-image image.jpg

# 批量上传
python3 scripts/cli.py upload-images ./images
```

## 工作流程

### 完整发布流程

```
┌─────────────────────────────────────────────────────────┐
│                    第一步：AI 文档转换                    │
├─────────────────────────────────────────────────────────┤
│  1. 读取文章内容（Markdown/Word/PDF）                       │
│  2. 按样式规范转换为 HTML                                  │
│  3. 应用内联样式（标题、段落、代码块等）                    │
│  4. 生成符合微信阅读体验的完整 HTML                       │
│                                                             │
│  输出：带有内联样式的 HTML 字符串                          │
└─────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────┐
│                第二步：微信草稿管理（Python 脚本）           │
├─────────────────────────────────────────────────────────┤
│  1. 接收 AI 生成的 HTML                                   │
│  2. 扫描并提取文章中的图片引用                              │
│  3. 下载远程图片到临时目录（如适用）                        │
│  4. 批量上传所有图片到微信素材库                            │
│  5. 替换 HTML 中的图片链接为微信 CDN URL                  │
│  6. 生成封面图片（模板生成或使用 AI 生成的图片）         │
│  7. 上传封面到微信素材库                                     │
│  8. 调用微信公众号 API 创建草稿                           │
│  9. 返回草稿 media_id 用于后续更新                          │
└─────────────────────────────────────────────────────────┘
```

### 图片处理流程（自动）

当文章包含图片时，脚本会自动执行以下步骤：

```
┌─────────────────────────────────────────────────────────┐
│                    图片提取与上传                         │
├─────────────────────────────────────────────────────────┤
│  扫描文章 → 识别图片类型 → 处理图片 → 上传素材库 → 替换链接  │
│                                                             │
│  图片类型处理：                                              │
│  • 本地图片 → 直接上传                                      │
│  • 相对路径 → 解析为完整路径后上传                          │
│  • 远程图片 → 下载到 temp/ 后上传                          │
│  • 已存在微信 → 跳过（可扩展）                              │
└─────────────────────────────────────────────────────────┘
```

**图片处理特性：**
- ✅ 自动扫描 Markdown/HTML 中的图片引用
- ✅ 支持本地图片和远程 URL
- ✅ 自动下载远程图片到临时目录
- ✅ 批量上传到微信素材库
- ✅ 自动替换 HTML 中的链接为微信 CDN URL
- ✅ 显示上传进度和结果统计

### 为什么这样设计？

| 优势 | 说明 |
|------|------|
| **职责分离** | AI 擅长内容理解和样式应用，脚本专注 API 操作 |
| **质量更高** | AI 能理解语义，生成更符合公众号风格的内容 |
| **维护简单** | 不需要维护复杂的文档解析逻辑，脚本只做 API 调用 |
| **灵活扩展** | 可以轻松更换 AI 提供商或转换方式 |

## CLI 命令

### 发布文章

```bash
# 使用 API 上传到草稿箱
python3 scripts/cli.py publish article.md

# 仅生成 HTML 文件
python3 scripts/cli.py publish article.md --no-api

# 使用指定模板
python3 scripts/cli.py publish article.md --template fancy
```

### 更新草稿

```bash
# 更新已有草稿
python3 scripts/cli.py update <media_id>

# 指定新的源文件
python3 scripts/cli.py update <media_id> --source new-article.md

# 重新生成封面
python3 scripts/cli.py update <media_id> --regenerate-cover
```

### 上传图片

```bash
# 上传单张图片
python3 scripts/cli.py upload-image cover.jpg

# 上传为缩略图
python3 scripts/cli.py upload-image cover.jpg --type thumb

# 批量上传文件夹中的图片
python3 scripts/cli.py upload-images ./images

# 指定文件模式
python3 scripts/cli.py upload-images ./photos --pattern "*.png"

# 上传为缩略图
python3 scripts/cli.py upload-images ./covers --type thumb
```

## 样式规范

### 自动应用的样式

| 元素 | 样式特点 |
|------|----------|
| **一级标题** | 主题色渐变背景、白色文字、圆角阴影 |
| **二级标题** | 左侧主题色装饰条（4px）、12px 左内边距 |
| **段落** | 行高 1.75、字号 15px、两端对齐 |
| **代码块** | 深色背景（#2d2d2d）、支持横向滚动、字号 13px |
| **内联代码** | 浅灰背景（#f0f0f0）、粉色文字（#d63384） |
| **引用块** | 左侧主题色边框、浅灰背景 |
| **表格** | 表头主题色背景、白色文字、边框合并 |

### 主题色推荐

| 色值 | 适用场景 |
|------|----------|
| `#07c160` | 科技、效率（默认） |
| `#ff6b6b` | 生活、情感 |
| `#4a90e2` | 商业、职场 |
| `#f5a623` | 教育、培训 |
| `#9013fe` | 创意、设计 |

## 详细文档

此 SKILL 遵循 Progressive Disclosure 原则，详细文档按需加载：

| 文档 | 内容 | 何时阅读 |
|------|------|----------|
| [平台特征参考](references/platform-guide.md) | 用户画像、内容调性、阅读行为 | 需要了解公众号平台特征时 |
| [转换规则参考](references/conversion-rules.md) | 标题优化、开头格式、正文结构、视觉元素 | AI 转换文档时 |
| [样式规范参考](references/style-specs.md) | 完整样式配置、移动端优化 | 需要自定义样式时 |
| [封面生成参考](references/cover-guide.md) | 封面规格、生成方式、设计原则 | 需要生成封面时 |
| [图片上传参考](references/image-upload.md) | 图片格式、批量上传、优化建议 | 需要上传图片时 |
| [工作流参考](references/workflows.md) | 完整工作流、场景示例、自动化脚本 | 需要了解完整流程时 |

## 图片素材上传

当文章包含本地图片时：

1. **AI 会自动**：扫描图片引用，批量上传到素材库
2. **手动上传**：使用 `upload-images` 命令
3. **图片规范**：
   - 格式：JPG, PNG
   - 大小：thumb ≤ 2MB，image ≤ 5MB
   - 推荐尺寸：宽度 ≤ 900px

详细说明请查看 [图片上传参考](references/image-upload.md)

## 封面图生成

**自动封面规格：**
- 尺寸：1080×460 (2.35:1)
- 格式：JPEG
- 质量：95%
- 字体：华文黑体（支持中文）

**封面生成方式：**

| 方式 | 说明 | 适用场景 |
|------|------|----------|
| **搜索加工**（默认） | 从 Unsplash/Pexels 搜索高质量图片，添加渐变遮罩和标题文字 | 适用于所有文章 |
| **AI 生成** | 使用 Claude/Midjourney/DALL·E 生成 | 重要文章、品牌建设 |
| **模板生成** | 自动使用文章标题生成，渐变背景 | 网络不可用时的备选 |

详细说明请查看 [封面生成参考](references/cover-guide.md)

## 移动端友好设计

### 代码块（移动端优化）

**关键特性：**
- 深色背景（#2d2d2d）保护眼睛
- 字号 13px 适合手机阅读
- **横向滚动**（overflow-x: auto）
- **不强制换行**（white-space: pre）
- **iOS 平滑滚动**（-webkit-overflow-scrolling: touch）

**设计原则：**
1. 不破坏代码结构
2. 支持横向滚动查看长代码
3. 触控滑动体验流畅

### 图片优化

**移动端建议：**
- 单张图片 ≤ 500KB
- 宽度 ≤ 900px
- 使用渐进式 JPEG
- 考虑图片懒加载

## 常见问题

### Q: 转换后的 HTML 在哪？

A: 使用 `--no-api` 参数时，HTML 保存在 `output/` 目录

### Q: 如何获取 media_id？

A: 发布成功后会返回 media_id，也可以在微信公众号后台查看

### Q: 图片上传失败怎么办？

A: 检查图片大小（image ≤ 5MB，thumb ≤ 2MB），使用 TinyPNG 压缩后重试

### Q: 代码块在手机上显示不全？

A: 这是正常的，代码块支持横向滚动，不会强制换行破坏代码结构

## 项目结构

```
mp-weixin-skills/
├── SKILL.md              # 主文件（304 行，<500 行 ✅）
├── skills.json           # Skill 元数据
├── .env.example          # 环境配置示例
│
├── scripts/              # 可执行脚本（核心功能）
│   ├── cli.py           # 命令行接口（主入口）
│   ├── config.py        # 配置管理
│   ├── exceptions.py    # 自定义异常
│   │
│   ├── wechat/          # 微信 API 操作（核心）⭐
│   │   ├── __init__.py
│   │   └── api_client.py
│   │
│   ├── covers/          # 封面生成（核心）⭐
│   │   ├── __init__.py
│   │   ├── base.py
│   │   └── template_maker.py
│   │
│   ├── converters/      # HTML 处理（可选）
│   │   ├── __init__.py
│   │   ├── html_builder.py
│   │   └── style_manager.py
│   │
│   ├── parsers/         # 文档解析（可选，AI 主要处理）
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── markdown.py
│   │   ├── pdf.py
│   │   └── word.py
│   │
│   └── utils/           # 工具函数
│       ├── __init__.py
│       └── logger.py
│
├── references/           # 详细文档（按需加载）📚
│   ├── platform-guide.md      # 平台特征
│   ├── conversion-rules.md    # 转换规则（AI 转换时）
│   ├── style-specs.md         # 样式规范
│   ├── cover-guide.md         # 封面指南
│   ├── image-upload.md        # 图片上传
│   └── workflows.md           # 工作流程
│
├── examples/             # 示例文章
├── tests/               # 测试文件（可选）
├── output/              # 输出目录（生成）
└── temp/                # 临时文件（生成）
```

**核心功能说明：**
- ⭐ **wechat/** - 微信公众号 API 操作（上传素材、创建/更新草稿）
- ⭐ **covers/** - 自动封面生成（1080×460）
- 📚 **references/** - Progressive Disclosure 文档，按需加载

## 许可证

MIT License
