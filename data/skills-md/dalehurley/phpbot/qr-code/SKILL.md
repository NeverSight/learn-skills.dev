---
name: qr-code
description: "Generate QR codes as PNG images from text, URLs, or any data. Use this skill when the user asks to create a QR code, generate a QR code, make a scannable code, or encode data as a QR image."
tags: [qr-code, qr, barcode, image, generator, utility]
version: 0.1.0
---

# Skill: qr-code

## When to Use

Use this skill when the user asks to:

- Generate or create a QR code
- Make a scannable QR code image
- Encode a URL or text as a QR code
- Create a QR code for sharing a link
- Save a QR code as PNG

## Input Parameters

| Parameter  | Required | Description                                  | Example             |
| ---------- | -------- | -------------------------------------------- | ------------------- |
| `content`  | Yes      | Text, URL, or data to encode                 | https://example.com |
| `output`   | No       | Output PNG file path (default: ./qrcode.png) | /tmp/my-qr.png      |
| `size`     | No       | Box size in pixels (default: 10)             | 15                  |
| `color`    | No       | QR code color (default: black)               | navy                |
| `bg_color` | No       | Background color (default: white)            | white               |

## Procedure

1. Get the content to encode from the user's request
2. Run the bundled script:
   ```bash
   python3 skills/qr-code/scripts/generate.py "https://example.com"
   ```
   Or with options:
   ```bash
   python3 skills/qr-code/scripts/generate.py "Hello World" --output /tmp/qr.png --size 15 --color navy
   ```
3. The script auto-installs `qrcode` and `Pillow` if needed
4. Report the saved file path to the user

## Bundled Scripts

| Script                | Type   | Description                 |
| --------------------- | ------ | --------------------------- |
| `scripts/generate.py` | Python | Generate QR code PNG images |

### Script Usage

```bash
# Simple QR code
python3 scripts/generate.py "https://example.com"

# Custom output path
python3 scripts/generate.py "Hello World" --output /tmp/my-qr.png

# Custom size and colors
python3 scripts/generate.py "https://example.com" --size 15 --color darkblue --bg white

# WiFi QR code
python3 scripts/generate.py "WIFI:T:WPA;S:MyNetwork;P:MyPassword;;"
```

## Example

```
generate a QR code for https://example.com
create a QR code that says "Hello World"
make a QR code for my wifi network
generate a QR code and save it to my desktop
```
