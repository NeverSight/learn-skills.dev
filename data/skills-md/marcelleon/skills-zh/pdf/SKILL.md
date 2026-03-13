---
name: pdf
description: 只要任务涉及 PDF 输入或输出，就应优先使用本技能。包括：读取/抽取文本与表格、合并拆分、旋转页面、加水印、创建新 PDF、填写表单、加解密、提取图片、扫描件 OCR 等。用户提到 `.pdf` 文件名或要求交付 PDF 时都应触发。
license: Proprietary. LICENSE.txt has complete terms
---

# PDF 处理指南

## 概览

本技能覆盖常见 PDF 工作流（Python + 命令行）。  
若要填写 PDF 表单，请额外阅读 [forms.md](forms.md)；更深入的扩展能力可看 [reference.md](reference.md)。

## 快速开始

```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("document.pdf")
print(f"Pages: {len(reader.pages)}")

text = ""
for page in reader.pages:
    text += page.extract_text()
```

---

## Python 库

### pypdf（基础结构处理）

#### 合并
```python
from pypdf import PdfWriter, PdfReader

writer = PdfWriter()
for pdf_file in ["doc1.pdf", "doc2.pdf", "doc3.pdf"]:
    reader = PdfReader(pdf_file)
    for page in reader.pages:
        writer.add_page(page)

with open("merged.pdf", "wb") as output:
    writer.write(output)
```

#### 拆分
```python
reader = PdfReader("input.pdf")
for i, page in enumerate(reader.pages):
    writer = PdfWriter()
    writer.add_page(page)
    with open(f"page_{i+1}.pdf", "wb") as output:
        writer.write(output)
```

#### 元数据
```python
reader = PdfReader("document.pdf")
meta = reader.metadata
print(meta.title, meta.author, meta.subject, meta.creator)
```

#### 旋转页面
```python
reader = PdfReader("input.pdf")
writer = PdfWriter()

page = reader.pages[0]
page.rotate(90)
writer.add_page(page)

with open("rotated.pdf", "wb") as output:
    writer.write(output)
```

### pdfplumber（文本/表格抽取）

#### 文本抽取
```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    for page in pdf.pages:
        print(page.extract_text())
```

#### 表格抽取
```python
with pdfplumber.open("document.pdf") as pdf:
    for i, page in enumerate(pdf.pages):
        tables = page.extract_tables()
        for j, table in enumerate(tables):
            print(f"Table {j+1} on page {i+1}:")
            for row in table:
                print(row)
```

#### 进阶：多表拼接
```python
import pandas as pd
import pdfplumber

all_tables = []
with pdfplumber.open("document.pdf") as pdf:
    for page in pdf.pages:
        for table in page.extract_tables():
            if table:
                all_tables.append(pd.DataFrame(table[1:], columns=table[0]))

if all_tables:
    pd.concat(all_tables, ignore_index=True).to_excel("extracted_tables.xlsx", index=False)
```

### reportlab（新建 PDF）

#### 基础单页
```python
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

c = canvas.Canvas("hello.pdf", pagesize=letter)
width, height = letter

c.drawString(100, height - 100, "Hello World!")
c.drawString(100, height - 120, "This is a PDF created with reportlab")
c.line(100, height - 140, 400, height - 140)
c.save()
```

#### 多页文档
```python
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet

doc = SimpleDocTemplate("report.pdf", pagesize=letter)
styles = getSampleStyleSheet()
story = []

story.append(Paragraph("Report Title", styles["Title"]))
story.append(Spacer(1, 12))
story.append(Paragraph("This is the body of the report. " * 20, styles["Normal"]))
story.append(PageBreak())
story.append(Paragraph("Page 2", styles["Heading1"]))
story.append(Paragraph("Content for page 2", styles["Normal"]))

doc.build(story)
```

#### 下标/上标（关键）

不要直接用 Unicode 下标/上标字符（在默认字体里容易显示为黑方块）。  
用 `Paragraph` 的标记语法：

```python
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet

styles = getSampleStyleSheet()
chemical = Paragraph("H<sub>2</sub>O", styles["Normal"])
squared = Paragraph("x<super>2</super> + y<super>2</super>", styles["Normal"])
```

---

## 命令行工具

### `pdftotext`
```bash
pdftotext input.pdf output.txt
pdftotext -layout input.pdf output.txt
pdftotext -f 1 -l 5 input.pdf output.txt
```

### `qpdf`
```bash
qpdf --empty --pages file1.pdf file2.pdf -- merged.pdf
qpdf input.pdf --pages . 1-5 -- pages1-5.pdf
qpdf input.pdf output.pdf --rotate=+90:1
qpdf --password=mypassword --decrypt encrypted.pdf decrypted.pdf
```

### `pdftk`（若环境可用）
```bash
pdftk file1.pdf file2.pdf cat output merged.pdf
pdftk input.pdf burst
pdftk input.pdf rotate 1east output rotated.pdf
```

---

## 常见任务模板

### 扫描版 OCR
```python
import pytesseract
from pdf2image import convert_from_path

images = convert_from_path("scanned.pdf")
text = ""
for i, image in enumerate(images):
    text += f"Page {i+1}:\n"
    text += pytesseract.image_to_string(image)
    text += "\n\n"

print(text)
```

### 加水印
```python
from pypdf import PdfReader, PdfWriter

watermark = PdfReader("watermark.pdf").pages[0]
reader = PdfReader("document.pdf")
writer = PdfWriter()

for page in reader.pages:
    page.merge_page(watermark)
    writer.add_page(page)

with open("watermarked.pdf", "wb") as output:
    writer.write(output)
```

### 抽取图片
```bash
pdfimages -j input.pdf output_prefix
```

### 加密
```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("input.pdf")
writer = PdfWriter()
for page in reader.pages:
    writer.add_page(page)

writer.encrypt("userpassword", "ownerpassword")
with open("encrypted.pdf", "wb") as output:
    writer.write(output)
```

---

## 快速索引

| 任务 | 推荐 |
|------|------|
| 合并/拆分/旋转 | `pypdf` |
| 文本/表格提取 | `pdfplumber` |
| 新建 PDF | `reportlab` |
| 命令行流水线 | `qpdf`/`pdftotext` |
| OCR | `pytesseract` + `pdf2image` |
| 表单填写 | 先读 [forms.md](forms.md) |

## 下一步

- 进阶技巧看 [reference.md](reference.md)
- 表单填写严格按 [forms.md](forms.md)

