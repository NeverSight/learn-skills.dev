---
name: docx
description: "当用户需要创建、读取、编辑或转换 Word 文档（.docx）时必须使用本技能。触发场景包括：提到 Word/docx、报告/备忘录/正式函件输出、目录和页眉页脚、批注或修订模式、替换文档内容、插入或替换图片、从 docx 提取结构化内容等。若目标交付物是 .docx，本技能应优先触发。不要用于 PDF、电子表格、Google Docs API 或无关编程任务。"
license: Proprietary. LICENSE.txt has complete terms
---

# DOCX 创建、编辑与分析

## 概览

`.docx` 本质上是 ZIP 包内的一组 XML。  
可分三类任务：

- 新建文档：用 `docx-js`
- 编辑现有文档：`unpack -> edit XML -> pack`
- 读取/检查：`pandoc`、`unpack`、渲染图片核验

## 快速参考

| 任务 | 推荐方式 |
|------|----------|
| 读取/分析正文 | `pandoc` 或解包看 XML |
| 新建 DOCX | `docx-js` + `scripts/office/validate.py` |
| 修改现有 DOCX | `scripts/office/unpack.py` -> XML 编辑 -> `scripts/office/pack.py` |

### `.doc` 转 `.docx`

```bash
python scripts/office/soffice.py --headless --convert-to docx document.doc
```

### 读取内容

```bash
# 含修订痕迹的文本导出
pandoc --track-changes=all document.docx -o output.md

# 读取原始 XML
python scripts/office/unpack.py document.docx unpacked/
```

### 渲染成图片做视觉检查

```bash
python scripts/office/soffice.py --headless --convert-to pdf document.docx
pdftoppm -jpeg -r 150 document.pdf page
```

### 一键接受全部修订

```bash
python scripts/accept_changes.py input.docx output.docx
```

---

## 新建文档（docx-js）

先安装：`npm install -g docx`

### 基础骨架

```javascript
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, ImageRun,
        Header, Footer, AlignmentType, PageOrientation, LevelFormat, ExternalHyperlink,
        InternalHyperlink, Bookmark, FootnoteReferenceRun, PositionalTab,
        PositionalTabAlignment, PositionalTabRelativeTo, PositionalTabLeader,
        TabStopType, TabStopPosition, Column, SectionType,
        TableOfContents, HeadingLevel, BorderStyle, WidthType, ShadingType,
        VerticalAlign, PageNumber, PageBreak } = require('docx');

const doc = new Document({ sections: [{ children: [/* content */] }] });
Packer.toBuffer(doc).then(buffer => fs.writeFileSync("doc.docx", buffer));
```

### 生成后必须校验

```bash
python scripts/office/validate.py doc.docx
```

校验失败时：解包修 XML 再回包，不要直接忽略。

### 页面尺寸（关键）

`docx-js` 默认 A4。若是美式文档，要显式设 US Letter：

```javascript
sections: [{
  properties: {
    page: {
      size: { width: 12240, height: 15840 }, // 8.5 x 11 inch (DXA)
      margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } // 1 inch
    }
  },
  children: []
}]
```

横向模式要点：传入短边 `width`、长边 `height`，再设 `orientation: PageOrientation.LANDSCAPE`，库会自动交换。

### 样式与标题

- 默认字体建议 Arial（跨平台稳定）
- 覆盖内置标题样式时，`id` 必须精确：`Heading1`、`Heading2`
- 目录依赖 `outlineLevel`（H1=0, H2=1）

### 列表（禁止手写 Unicode 项目符号）

- 错误：在文本里直接写 `•`
- 正确：用 `numbering + LevelFormat.BULLET`

### 表格（最易踩坑）

- 必须同时设置：表级 `columnWidths` + 单元格 `width`
- 表格宽度必须等于 `columnWidths` 总和
- 始终用 `WidthType.DXA`，不要用百分比（Google Docs 兼容性差）
- `shading` 使用 `ShadingType.CLEAR`，不要 `SOLID`
- 给单元格加 `margins` 作为内边距，提升可读性

### 图片

`ImageRun` 必须写 `type`（png/jpg/svg 等）且补齐 `altText`。

### 分页 / 超链接 / 脚注 / 制表位 / 多栏 / 目录 / 页眉页脚

这些场景按 `docx` 官方 API 正规建模，不要用“文本模拟布局”的捷径。  
尤其注意：

- `PageBreak` 必须放在 `Paragraph` 内
- 内链先建 `Bookmark` 再 `InternalHyperlink`
- 目录使用 `TableOfContents`，标题必须来自 `HeadingLevel`
- 双栏页脚优先用 tab stops，不要用 table 伪造

### docx-js 硬规则（请默认遵守）

- 必须显式设置页面尺寸
- 禁止在段内用 `\n` 代替段落
- 禁止手写 Unicode bullets
- 表格只用 DXA 宽度体系
- 不要用表格充当分割线

---

## 编辑现有文档（三步必须全走）

### Step 1: 解包

```bash
python scripts/office/unpack.py document.docx unpacked/
```

该脚本会做 pretty-print、run 合并和智能引号实体处理。需要时可 `--merge-runs false`。

### Step 2: 改 XML

编辑 `unpacked/word/` 下文件。  
默认作者名使用 `Claude`（除非用户要求其他名字）。

- 直接用编辑工具做字符串替换，不要无谓再写一次 Python 脚本
- 新增文本涉及引号/撇号时，用智能引号实体：

```xml
<w:t>Here&#x2019;s a quote: &#x201C;Hello&#x201D;</w:t>
```

| Entity | 字符 |
|--------|------|
| `&#x2018;` | ‘ |
| `&#x2019;` | ’ |
| `&#x201C;` | “ |
| `&#x201D;` | ” |

批注可用脚本生成样板：

```bash
python scripts/comment.py unpacked/ 0 "Comment text with &amp; and &#x2019;"
python scripts/comment.py unpacked/ 1 "Reply text" --parent 0
python scripts/comment.py unpacked/ 0 "Text" --author "Custom Author"
```

### Step 3: 回包

```bash
python scripts/office/pack.py unpacked/ output.docx --original document.docx
```

默认包含校验与自动修复。`--validate false` 可跳过，但不建议常态使用。

自动修复覆盖：

- `durableId` 越界
- `<w:t>` 缺少 `xml:space="preserve"`（有前后空白时）

不会自动修复：

- XML 结构损坏
- 元素顺序/嵌套非法
- 关系丢失等语义错误

---

## XML 参考（常用高风险点）

### Schema 顺序与空白

- `<w:pPr>` 内元素顺序要合法：`pStyle -> numPr -> spacing -> ind -> jc -> rPr`
- 文本有前后空白时必须 `xml:space="preserve"`
- RSID 使用 8 位十六进制

### 修订模式（Tracked Changes）

- 插入用 `<w:ins>`，删除用 `<w:del>`
- `<w:del>` 内文本必须是 `<w:delText>`，不是 `<w:t>`
- 只标记最小变更片段，避免整段重写
- 删除整段时，需在 `<w:pPr><w:rPr>` 补 `<w:del/>`，否则接受修订后会残留空段落
- 拒绝他人插入：在其 `<w:ins>` 内嵌你的 `<w:del>`
- 恢复他人删除：保留对方 `<w:del>`，再新增你的 `<w:ins>`

### 批注（Comments）

- `commentRangeStart/End` 是 `<w:p>` 的子节点，不可塞进 `<w:r>`
- 回复链路用 `--parent` 建立层级
- 在 `document.xml` 同步插入 `commentReference`

### 图片嵌入

必须四步齐全：

1. `word/media/` 放入图片
2. `word/_rels/document.xml.rels` 增加 relationship
3. `[Content_Types].xml` 增加扩展名映射
4. `document.xml` 中用 `r:embed` 引用对应 `rId`

---

## 依赖

- `pandoc`：文本抽取
- `docx`：`npm install -g docx`
- LibreOffice：转换与兼容渲染（通过 `scripts/office/soffice.py` 适配沙箱）
- Poppler：`pdftoppm` 出图核验

