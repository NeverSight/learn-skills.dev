---
name: web-article-translator
description: 翻译在线文章为中文并保存为 Markdown 格式。当用户需要翻译网页文章、博客文章时使用此技能，例如："翻译这篇文章 https://example.com/article"、"把这个 URL 的文章翻译成中文并保存"。
---

# Web Article Translator

## Overview

翻译在线文章为中文，并将结果保存为 Markdown 格式文件，保留原文的图片链接。

## Workflow

### 1. 获取网页内容

使用 工具获取文章内容：
- 设置 `return_format` 为 `markdown`
- 设置 `retain_images` 为 `true`
- Keep all image links unchanged
- Do NOT translate code blocks or variable names

### 2. 翻译内容

将获取的 Markdown 内容翻译为中文：
- **翻译原则**：保持原文风格，根据原文类型（新闻、技术文档、博客等）自动调整翻译风格
- **专业术语**：技术术语首次出现时保留英文原文在括号中，后续可直接使用中文
- **可读性**：确保翻译合理、流畅、易懂
- **格式保留**：保持原有的 Markdown 结构（标题、列表、代码块等）

### 3. 保存文件

将翻译后的内容保存为 Markdown 文件：
- 文件名格式：`translated-{标题}.md` 或 `translated-article-{日期时间}.md`
- 保存到当前工作目录
- Keep all image links unchanged

### 4. 输出确认

完成翻译后，告知用户：
- 文件保存路径
- 翻译字数统计
- 图片数量（如果有）

## Example Usage

用户请求：
> 翻译这篇文章 https://example.com/article

执行流程：
1. 使用 webReader 工具获取 URL 内容
2. 翻译 Markdown 内容为中文
3. 保存到 `translated-article.md`
4. 告知用户完成情况