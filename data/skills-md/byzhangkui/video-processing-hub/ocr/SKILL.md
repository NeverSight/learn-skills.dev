---
name: ocr
description: 对截图运行 OCR 提取文字。当用户要求提取文字、识别文字、OCR 时使用。
allowed-tools: Bash(source .venv/bin/activate *)
---

对 `output/captures/` 中的截图运行 OCR，提取文字内容。

执行以下命令：

```bash
source .venv/bin/activate && python pipeline.py ocr --input-dir output/captures --output output/extracted_text.txt
```

完成后读取 `output/extracted_text.txt`，将内容展示给用户。
