---
name: xhs-md-to-plain-text
description: 将 Markdown 转为适合小红书粘贴的纯文本（去掉 #/**/列表等标记），可选只抽取“正文内容”段。
---

# XHS Markdown → Plain Text

把 Markdown 里的标记（标题 #、加粗 **、列表符号、引用 >、链接语法等）去掉，输出为 `.txt`，方便直接粘贴到小红书。

## 使用方法

Step 0：设置 `SKILL_DIR`

```bash
SKILL_DIR="/path/to/xhs-md-to-plain-text"
```

Step 1：生成纯文本

- 生成完整文本（全文件去标记）

```bash
npx -y bun ${SKILL_DIR}/scripts/md2text.ts /path/to/article.md --out xhs-img
```

- 只抽取 `## 正文内容` 到 `## 标签` 之间（更适合直接发正文）

```bash
npx -y bun ${SKILL_DIR}/scripts/md2text.ts /path/to/article.md --body-only --out xhs-img/body.txt
```

## 参数

```bash
npx -y bun ${SKILL_DIR}/scripts/md2text.ts <markdown-file> [options]

Options:
  --out <path>       输出文件路径或输出目录（默认: xhs-img）
  --body-only        仅抽取“正文内容”段（## 正文内容 → ## 标签）
```
