---
name: pandoc
description: 当用户需要对某个文档进行格式转换时（例如将 Markdown 转换为 DOCX、PDF、HTML 等）使用该技能。
---

# Pandoc 文档转换技能

该技能提供使用 Pandoc 进行文档格式转换的工作流程和最佳实践

## 何时使用此技能
当用户提出以下需求时，使用此技能：

- 需要将文档从一种格式转换为另一种格式（例如 Markdown 转换为 DOCX、PDF、HTML 等）
- 需要处理包含特殊内容（如 Mermaid 图表）的 Markdown 文件

## 工作流程

1. **环境检查**：
   - 运行 Bash 命令 `pandoc --version` 检查系统中是否已经安装了 Pandoc。
   - 如果系统未安装 Pandoc，请先按照 [Pandoc 安装指南](https://pandoc.org/installing.html) 进行安装。

2. **验证安装**：
   - 若进行了安装，请再次执行 `pandoc --version` 验证是否安装成功。

3. **执行转换**：
   - 根据用户的要求，构建 `pandoc` 命令并执行转换。
   - **注意**：在执行转换前，请务必查看下方“最佳实践”以应对特殊内容（如 Mermaid 图表）。

## 最佳实践

### 处理 Markdown 中的 Mermaid 图表

如果源文件是 Markdown (`.md`) 格式，在转换之前：
1. **必须先检查** 源文件中是否包含 Mermaid 图表（即 ````mermaid ` 代码块）。
2. 如果包含 Mermaid 图表，执行转换时**必须**使用 Lua 过滤器将其渲染为图片，否则图表会丢失或显示异常。
3. 请直接使用技能 `scripts/` 目录中已经准备好的 `mermaid-to-image.lua` 文件，**不要重新编写该脚本**。

**转换命令示例**（假设当前命令在项目根目录执行）：
```bash
pandoc "源文档.md" --lua-filter="D:/Sources/cruldra-skills/skills/pandoc/scripts/mermaid-to-image.lua" -o "输出文档.docx"
```
*(提示：在使用时请将过滤器路径替换为当前环境中 `mermaid-to-image.lua` 的实际绝对路径。)*