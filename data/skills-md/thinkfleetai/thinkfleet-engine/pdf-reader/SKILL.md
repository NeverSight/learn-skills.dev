---
name: pdf-reader
description: PDF reading and extraction
metadata:
  thinkfleetbot_emoji: "📄"
  requires_bins:
    - python3
  requires_env: []
---

# PDF Reader

Tools for reading, extracting, and manipulating PDF files.

## Extract text from PDF

```bash
# Using pdftotext (poppler-utils) if available
pdftotext input.pdf output.txt

# Using python with PyPDF2
python3 -c "
import PyPDF2

with open('input.pdf', 'rb') as f:
    reader = PyPDF2.PdfReader(f)
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        print(f'--- Page {i+1} ---')
        print(text)
"
```

## Extract tables from PDF

```bash
python3 -c "
import sys
try:
    import tabula
    dfs = tabula.read_pdf('input.pdf', pages='all')
    for i, df in enumerate(dfs):
        print(f'--- Table {i+1} ---')
        print(df.to_csv(index=False))
except ImportError:
    print('Install tabula-py: pip install tabula-py')
    sys.exit(1)
"
```

## Get PDF metadata

```bash
python3 -c "
import PyPDF2, json

with open('input.pdf', 'rb') as f:
    reader = PyPDF2.PdfReader(f)
    meta = reader.metadata
    info = {
        'title': meta.title if meta else None,
        'author': meta.author if meta else None,
        'subject': meta.subject if meta else None,
        'creator': meta.creator if meta else None,
        'pages': len(reader.pages),
    }
    print(json.dumps(info, indent=2, default=str))
"
```

## Convert PDF to text

```bash
python3 -c "
import PyPDF2

with open('input.pdf', 'rb') as f:
    reader = PyPDF2.PdfReader(f)
    text = []
    for page in reader.pages:
        text.append(page.extract_text() or '')
    with open('output.txt', 'w') as out:
        out.write('\n\n'.join(text))
print('Converted to output.txt')
"
```

## Merge PDFs

```bash
python3 -c "
import PyPDF2, sys

merger = PyPDF2.PdfMerger()
files = sys.argv[1:]
for pdf in files:
    merger.append(pdf)
merger.write('merged.pdf')
merger.close()
print(f'Merged {len(files)} files into merged.pdf')
" file1.pdf file2.pdf file3.pdf
```

## Split PDF pages

```bash
python3 -c "
import PyPDF2

with open('input.pdf', 'rb') as f:
    reader = PyPDF2.PdfReader(f)
    for i, page in enumerate(reader.pages):
        writer = PyPDF2.PdfWriter()
        writer.add_page(page)
        out_path = f'page_{i+1:03d}.pdf'
        with open(out_path, 'wb') as out:
            writer.write(out)
        print(f'Wrote {out_path}')
print(f'Split into {len(reader.pages)} files')
"
```

## Extract images from PDF

```bash
python3 -c "
import PyPDF2, os

os.makedirs('extracted_images', exist_ok=True)
with open('input.pdf', 'rb') as f:
    reader = PyPDF2.PdfReader(f)
    img_count = 0
    for page_num, page in enumerate(reader.pages):
        for img_key in page.images:
            img_count += 1
            img = page.images[img_key]
            ext = os.path.splitext(img.name)[1] or '.png'
            out_path = f'extracted_images/page{page_num+1}_img{img_count}{ext}'
            with open(out_path, 'wb') as out:
                out.write(img.data)
            print(f'Extracted {out_path}')
print(f'Total images extracted: {img_count}')
"
```
