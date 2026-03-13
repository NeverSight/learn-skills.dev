---
name: hackmd-writer
description: 當使用者要求撰寫 HackMD 筆記、技術文件、投影片（Slide Mode），或詢問 HackMD 特有的 Markdown 語法（色塊、螢光筆、數學公式、Mermaid、Markmap、reveal.js 投影片等）時啟動此 Skill。
---

# HackMD Writer

撰寫與排版 HackMD 文件、技術筆記及 Reveal.js 投影片的完整指南。

## Workflow

依任務類型決定需要載入哪些 reference 檔案：

```
使用者要寫一般筆記 / 技術文件？
  → 載入 references/syntax-basics.md（基本語法）
  → 若用到圖表、數學、嵌入 → 另載入 references/advanced-features.md

使用者要製作投影片（Slide Mode）？
  → 載入 references/syntax-basics.md（基本語法）
  → 載入 references/advanced-features.md（圖表 / 公式）
  → 必載 references/slide-mode.md（投影片專屬設定）

使用者只問語法問題？
  → 先查下方《常用語法速查》，能回答就直接回答，不必載入 reference
```

## 常用語法速查

以下為最高頻使用的 HackMD 語法，熟悉後多數問題不需讀 reference：

| 功能 | 語法 |
| :-- | :-- |
| 標題 | `# H1` … `###### H6` |
| 粗體 / 斜體 | `**粗體**`、`*斜體*`、`***粗斜體***` |
| 刪除線 | `~~刪除~~` |
| 螢光筆 | `==重點==` |
| 上標 / 下標 | `19^th^`、`H~2~O` |
| 行內程式碼 | `` `code` `` |
| TOC | `[TOC]`（置於文件任意處） |
| 色塊（info） | `:::info` … `:::` |
| 行內數學 | `$x^2 + y^2$` |
| 區塊數學 | `$$` … `$$` |
| Mermaid 圖 | ` ```mermaid ` … ` ``` ` |
| YouTube 嵌入 | `{%youtube VIDEO_ID %}` |
| 投影片分頁 | `---`（水平）/`----`（垂直），上下各空一行 |

## 色塊快查

```
:::success   ← 綠色
:::info      ← 藍色
:::warning   ← 黃色
:::danger    ← 紅色
:::spoiler   ← 收合區塊（需加標題文字）
```

## 輸出品質 Checklist

產出 HackMD 內容前，確認以下事項：

- [ ] 色塊使用 `:::type` 語法，不用 `<div>` 代替
- [ ] 行內數學：`$...$`，左 `$` 後與右 `$` 前**不能有空格**
- [ ] 複雜圖表優先用 **Mermaid**；需精細組織圖才改用 Graphviz 或 Flow
- [ ] 文件需要目錄時，在頂部放 `[TOC]`（而非只靠右下角按鈕）
- [ ] 螢光筆 `==text==` 不能跨行；跨行需改用 HTML `<mark>`
- [ ] 投影片的 YAML frontmatter 中 `slideOptions.theme` 與 `slideOptions.transition` 已設定
- [ ] 嵌入外部資源使用 `{%youtube id%}` 或 `{%hackmd id%}`，不硬貼 iframe

## Reference 檔案

| 檔案 | 用途 | 何時載入 |
| :-- | :-- | :-- |
| `references/syntax-basics.md` | 基本文字、清單、表格、連結、圖片、TOC | 撰寫一般筆記 |
| `references/advanced-features.md` | 色塊、數學公式、UML / Mermaid / Markmap、外嵌 | 文件含圖表 / 公式 / 嵌入 |
| `references/slide-mode.md` | 投影片分頁、YAML 選項、動畫、主講者模式 | 製作 Slide Mode 簡報 |
