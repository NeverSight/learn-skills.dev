---
name: new-prevent-encoding-mojibake
description: Guidelines and instructions for preventing Thai/multi-byte character encoding corruption (Mojibake) during file writes, code modifications, or command-line outputs in Windows.
---

# Preventing Character Encoding Mismatch (Mojibake)

This skill provides guidelines and procedures for avoiding character encoding issues (specifically Mojibake where UTF-8 Thai text is read/written as Windows-1252/ISO-8859-1).

## Problem Description

Mojibake (e.g. Thai text becoming `à¸„à¸¸à¸“à¸•à¹‰à¸­à¸‡à¸ à¸²à¸£`) occurs when text encoded in **UTF-8** is read or written using a single-byte encoding like **Windows-1252 (CP1252 / ISO-8859-1 / Latin-1)**.
On Windows systems, if file writing tools or terminal redirects do not explicitly specify the encoding, the OS defaults to ANSI/CP1252, corrupting multi-byte characters like Thai script.

---

## Guidelines for Agents

### 1. File Writing & Overwriting

Whenever writing or editing files containing Thai (or any non-ASCII) text:

- **Explicitly Specify UTF-8:** Always use UTF-8 encoding in all file system APIs.
- **Avoid Terminal Redirects on Windows:** Do not use `>` or `>>` redirects in Command Prompt or PowerShell (e.g. `echo "แก้ไข" > file.ts`) because they encode output using system-default code pages (like CP874 or CP1252).
- **Use Node.js/Python Script with Explicit UTF-8:** If you must generate or modify code with a script, use explicit encoding configuration:
  - **Python:** `open(file_path, "w", encoding="utf-8")`
  - **Node.js:** `fs.writeFileSync(file_path, content, 'utf8')` or `{ encoding: 'utf8' }`

### 2. Detection of Mojibake

Scan files for common signature strings of UTF-8 interpreted as CP1252:

- `à¸` (representing the start of most Thai characters from U+0E00 to U+0E3F)
- `à¹` (representing the start of Thai characters from U+0E40 to U+0E7F)

### 3. How to Recover / Decode Mojibake

If a file becomes corrupted, use a Python script to decode the CP1252-misinterpreted characters back to UTF-8 bytes:

```python
# -*- coding: utf-8 -*-
import os

cp1252_override = {
    0x20ac: 0x80, 0x201a: 0x82, 0x0192: 0x83, 0x201e: 0x84,
    0x2026: 0x85, 0x2020: 0x86, 0x2021: 0x87, 0x02c6: 0x88,
    0x2030: 0x89, 0x0160: 0x8a, 0x2039: 0x8b, 0x0152: 0x8c,
    0x017d: 0x8e, 0x2018: 0x91, 0x2019: 0x92, 0x201c: 0x93,
    0x201d: 0x94, 0x2022: 0x95, 0x2013: 0x96, 0x2014: 0x97,
    0x02dc: 0x98, 0x2122: 0x99, 0x0161: 0x9a, 0x203a: 0x9b,
    0x0153: 0x9c, 0x017e: 0x9e, 0x0178: 0x9f,
}

def clean_mojibake(s):
    byte_list = []
    for c in s:
        code = ord(c)
        if code in cp1252_override:
            byte_list.append(cp1252_override[code])
        elif code < 256:
            byte_list.append(code)
        else:
            try:
                byte_list.extend(c.encode('cp1252'))
            except Exception:
                byte_list.extend(c.encode('utf-8'))
    try:
        return bytes(byte_list).decode('utf-8')
    except Exception:
        return bytes(byte_list).decode('utf-8', errors='replace')
```

---

## Guidelines for Users

To ensure local editors do not save UTF-8 files under different encodings:

1. **VS Code Settings:** Make sure your global or workspace `settings.json` has:
   ```json
   "files.encoding": "utf8"
   ```
2. **Reopen with Encoding:** If you see weird characters on screen, click the encoding selector in the status bar (bottom right of VS Code), select **"Reopen with Encoding"**, and choose **"UTF-8"**.
