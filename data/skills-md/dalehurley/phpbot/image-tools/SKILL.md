---
name: image-tools
description: "Resize, compress, convert, crop, and inspect images. Use this skill when the user asks to resize an image, compress a photo, convert image format (PNG to JPG etc), crop an image, get image dimensions/info, or optimize images for web."
tags: [image, resize, compress, convert, crop, pillow, photo, utility]
version: 0.1.0
---

# Skill: image-tools

## When to Use

Use this skill when the user asks to:

- Resize an image (scale, set dimensions)
- Compress or optimize an image for web
- Convert between image formats (PNG, JPG, WebP, GIF, BMP, TIFF)
- Crop an image
- Get image info (dimensions, format, file size)
- Create a thumbnail
- Rotate or flip an image

## Supported Formats

| Format | Read | Write | Notes                           |
| ------ | ---- | ----- | ------------------------------- |
| JPEG   | Yes  | Yes   | Lossy, quality adjustable       |
| PNG    | Yes  | Yes   | Lossless, supports transparency |
| WebP   | Yes  | Yes   | Modern web format               |
| GIF    | Yes  | Yes   | Animation supported             |
| BMP    | Yes  | Yes   | Uncompressed                    |
| TIFF   | Yes  | Yes   | Professional/print              |

## Input Parameters

| Parameter  | Required     | Description                                               | Example     |
| ---------- | ------------ | --------------------------------------------------------- | ----------- |
| `action`   | Yes          | `resize`, `compress`, `convert`, `crop`, `info`, `rotate` | resize      |
| `input`    | Yes          | Input image file path                                     | photo.jpg   |
| `output`   | For most     | Output file path                                          | resized.jpg |
| `width`    | For resize   | Target width in pixels                                    | 800         |
| `height`   | For resize   | Target height in pixels                                   | 600         |
| `quality`  | For compress | JPEG/WebP quality 1-100 (default: 80)                     | 75          |
| `format`   | For convert  | Target format                                             | webp        |
| `crop_box` | For crop     | left,top,right,bottom in pixels                           | 0,0,500,400 |
| `angle`    | For rotate   | Rotation angle in degrees                                 | 90          |

## Procedure

1. Determine the action from the user's request
2. Run the bundled script:

   ```bash
   # Resize
   python3 skills/image-tools/scripts/process.py resize input.jpg --width 800 --output resized.jpg

   # Compress
   python3 skills/image-tools/scripts/process.py compress photo.jpg --quality 75 --output compressed.jpg

   # Convert format
   python3 skills/image-tools/scripts/process.py convert image.png --format webp --output image.webp

   # Crop
   python3 skills/image-tools/scripts/process.py crop photo.jpg --box 0,0,500,400 --output cropped.jpg

   # Get info
   python3 skills/image-tools/scripts/process.py info photo.jpg

   # Rotate
   python3 skills/image-tools/scripts/process.py rotate photo.jpg --angle 90 --output rotated.jpg
   ```

3. The script auto-installs `Pillow` if needed
4. Report the result to the user

## Bundled Scripts

| Script               | Type   | Description                                                 |
| -------------------- | ------ | ----------------------------------------------------------- |
| `scripts/process.py` | Python | Resize, compress, convert, crop, inspect, and rotate images |

## Example

```
resize photo.jpg to 800px wide
compress this image to 75% quality
convert screenshot.png to webp
crop the image to 500x400
what are the dimensions of this image
make a thumbnail of photo.jpg
rotate the image 90 degrees
```
