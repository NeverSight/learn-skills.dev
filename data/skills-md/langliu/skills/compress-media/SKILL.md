---
name: compress-media
description: 使用 ImageMagick 压缩本地图片文件，使用 ffmpeg 压缩本地视频文件。当 Codex 需要缩小 JPEG、PNG、WebP、HEIC、TIFF、MP4、MOV、MKV 或其他本地媒体体积时使用；适用于批量压缩文件夹、分享前缩放图片、将照片或截图默认转换为同目录同名 WebP、将视频默认压缩为同路径 MP4/H.265，保留源文件时输出到 compressed 压缩目录并镜像源目录结构，并在压缩成功后检查输出尺寸、重试 0KB 输出、默认删除或替换原文件并汇报压缩前后体积变化。
---

# 压缩图片和视频

## 概览

使用 ImageMagick 内置的 `magick` 和 `magick mogrify` 命令安全压缩本地图片，使用 `ffmpeg` 安全压缩本地视频。不要使用额外封装脚本；根据用户指定的输入路径、输出路径、格式、质量、缩放和元数据要求，直接组合 ImageMagick 或 ffmpeg 命令。

## 快速流程

1. 检查目标路径，区分图片和视频文件。
2. 处理图片前用 `magick -version` 确认 ImageMagick 可用。
3. 处理视频前用 `ffmpeg -version` 确认 ffmpeg 可用。
4. 图片默认转换为 WebP，默认质量 `-quality 85`；只有用户明确要求保留原格式时才输出为原格式。
5. 视频默认转换为 MP4/H.265，默认使用 `-crf 20` 和 AAC 128k；只有用户明确要求兼容优先时才使用 MP4/H.264。
6. 默认把压缩结果放回原文件所在目录：图片使用同名 `.webp`，视频尽量保持同一路径；不要在默认模式输出到 `compressed`、`webp_q85` 或 `compressed_videos` 这类新目录。
7. 除非用户明确要求保留，否则压缩成功后删除或替换原文件；不要直接原地编码，先写出临时/新文件，确认成功后再删除或替换源文件。
8. 如果用户明确要求保留源文件，把压缩结果输出到目标根目录下的 `compressed` 压缩目录，并保持相对文件结构一致；不要删除源文件。
9. 每个输出完成后检查文件尺寸：只有 `[ -s "$out" ]` 为真才视为成功；如果输出不存在或为 0KB，删除半成品并重试一次。
10. 重试后仍失败时，保留源文件，记录失败文件路径，不删除源文件。
11. 条件允许时，汇报输出位置、处理数量、失败数量和压缩前后体积。

## 命令模式

### 图片

单张图片，保留格式：

```bash
magick input.jpg -auto-orient -strip -sampling-factor 4:2:0 -interlace Plane -quality 85 output.jpg
```

单张图片，仅当任意边超过 1600px 时缩小：

```bash
magick input.jpg -auto-orient -resize '1600x1600>' -strip -sampling-factor 4:2:0 -interlace Plane -quality 85 output.jpg
```

将单张图片转换为同目录同名 WebP，压缩成功后删除原图：

```bash
in="input.png"
out="${in%.*}.webp"
success=0
for attempt in 1 2; do
  rm -f "$out"
  if magick "$in" -auto-orient -strip -quality 85 "$out" && [ -s "$out" ]; then
    success=1
    break
  fi
done
[ "$success" -eq 1 ] && rm -f "$in"
```

批量将 JPEG/PNG 转为同目录同名 WebP，压缩成功后删除原图：

```bash
find . -maxdepth 1 -type f \( -iname '*.jpg' -o -iname '*.jpeg' -o -iname '*.png' \) -print0 | \
  while IFS= read -r -d '' file; do
    out="${file%.*}.webp"
    success=0
    for attempt in 1 2; do
      rm -f "$out"
      if magick "$file" -auto-orient -strip -quality 85 "$out" && [ -s "$out" ]; then
        success=1
        break
      fi
    done
    if [ "$success" -eq 1 ]; then
      rm -f "$file"
    else
      printf 'failed: %s\n' "$file"
    fi
  done
```

批量递归将图片转为同目录同名 WebP，压缩成功后删除原图：

```bash
find . -type f \( -iname '*.jpg' -o -iname '*.jpeg' -o -iname '*.png' -o -iname '*.heic' -o -iname '*.tif' -o -iname '*.tiff' \) -print0 | \
  while IFS= read -r -d '' file; do
    out="${file%.*}.webp"
    success=0
    for attempt in 1 2; do
      rm -f "$out"
      if magick "$file" -auto-orient -strip -quality 85 "$out" && [ -s "$out" ]; then
        success=1
        break
      fi
    done
    if [ "$success" -eq 1 ]; then
      rm -f "$file"
    else
      printf 'failed: %s\n' "$file"
    fi
  done
```

保留源文件时，批量递归将图片输出到 `compressed` 压缩目录，并保持源目录结构：

```bash
root="target-folder"
(
  cd "$root" || exit 1
  find . -type f \( -iname '*.jpg' -o -iname '*.jpeg' -o -iname '*.png' -o -iname '*.heic' -o -iname '*.tif' -o -iname '*.tiff' \) ! -path './compressed/*' -print0 | \
    while IFS= read -r -d '' file; do
      rel="${file#./}"
      out="compressed/${rel%.*}.webp"
      mkdir -p "$(dirname "$out")"
      if [ -e "$out" ]; then
        printf 'failed: output exists: %s\n' "$out"
        continue
      fi
      success=0
      for attempt in 1 2; do
        rm -f "$out"
        if magick "$file" -auto-orient -strip -quality 85 "$out" && [ -s "$out" ]; then
          success=1
          break
        fi
      done
      if [ "$success" -ne 1 ]; then
        printf 'failed: %s\n' "$file"
      fi
    done
)
```

PNG 近似无损优化：

```bash
magick input.png -strip -define png:compression-level=9 -define png:compression-filter=5 output.png
```

写出后比较文件体积：

```bash
ls -lh input.jpg output.jpg
```

### 视频

单个 MP4 视频，默认压缩为 H.265 并替换回原路径：

```bash
in="input.mp4"
tmp="${in%.*}.tmp.mp4"
success=0
for attempt in 1 2; do
  rm -f "$tmp"
  if ffmpeg -i "$in" -map '0:v:0' -map '0:a?' -c:v libx265 -crf 20 -preset medium -tag:v hvc1 -c:a aac -b:a 128k -movflags +faststart "$tmp" && [ -s "$tmp" ]; then
    success=1
    break
  fi
done
[ "$success" -eq 1 ] && mv "$tmp" "$in"
```

单个 MP4 视频，兼容优先压缩为 H.264 并替换回原路径：

```bash
in="input.mp4"
tmp="${in%.*}.tmp.mp4"
success=0
for attempt in 1 2; do
  rm -f "$tmp"
  if ffmpeg -i "$in" -map '0:v:0' -map '0:a?' -c:v libx264 -crf 23 -preset medium -c:a aac -b:a 128k -movflags +faststart "$tmp" && [ -s "$tmp" ]; then
    success=1
    break
  fi
done
[ "$success" -eq 1 ] && mv "$tmp" "$in"
```

单个 MP4 视频，仅当任意边超过 1080p 时缩小，并替换回原路径：

```bash
in="input.mp4"
tmp="${in%.*}.tmp.mp4"
success=0
for attempt in 1 2; do
  rm -f "$tmp"
  if ffmpeg -i "$in" -map '0:v:0' -map '0:a?' -vf "scale='min(1920,iw)':-2" -c:v libx265 -crf 20 -preset medium -tag:v hvc1 -c:a aac -b:a 128k -movflags +faststart "$tmp" && [ -s "$tmp" ]; then
    success=1
    break
  fi
done
[ "$success" -eq 1 ] && mv "$tmp" "$in"
```

批量压缩视频，输出保持在原文件所在目录；MP4 替换回原路径，其他格式输出为同目录同名 `.mp4`：

```bash
find . -type f \( -iname '*.mp4' -o -iname '*.mov' -o -iname '*.mkv' -o -iname '*.avi' -o -iname '*.m4v' -o -iname '*.wmv' -o -iname '*.flv' -o -iname '*.webm' \) -print0 | \
  while IFS= read -r -d '' file; do
    dir=$(dirname "$file")
    base=$(basename "${file%.*}")
    final="$dir/$base.mp4"
    tmp="$dir/.$base.tmp.mp4"
    if [ "$final" != "$file" ] && [ -e "$final" ]; then
      printf 'failed: output exists: %s\n' "$final"
      continue
    fi
    success=0
    for attempt in 1 2; do
      rm -f "$tmp"
      if ffmpeg -i "$file" -map '0:v:0' -map '0:a?' -c:v libx265 -crf 20 -preset medium -tag:v hvc1 -c:a aac -b:a 128k -movflags +faststart "$tmp" && [ -s "$tmp" ]; then
        success=1
        break
      fi
    done
    if [ "$success" -eq 1 ]; then
      if [ "$final" = "$file" ]; then
        mv "$tmp" "$file"
      else
        rm -f "$file"
        mv "$tmp" "$final"
      fi
    else
      printf 'failed: %s\n' "$file"
    fi
  done
```

保留源文件时，批量递归将视频输出到 `compressed` 压缩目录，并保持源目录结构：

```bash
root="target-folder"
(
  cd "$root" || exit 1
  find . -type f \( -iname '*.mp4' -o -iname '*.mov' -o -iname '*.mkv' -o -iname '*.avi' -o -iname '*.m4v' -o -iname '*.wmv' -o -iname '*.flv' -o -iname '*.webm' \) ! -path './compressed/*' -print0 | \
    while IFS= read -r -d '' file; do
      rel="${file#./}"
      out="compressed/${rel%.*}.mp4"
      out_dir=$(dirname "$out")
      base=$(basename "${out%.*}")
      tmp="$out_dir/.$base.tmp.mp4"
      mkdir -p "$out_dir"
      if [ -e "$out" ]; then
        printf 'failed: output exists: %s\n' "$out"
        continue
      fi
      success=0
      for attempt in 1 2; do
        rm -f "$tmp"
        if ffmpeg -i "$file" -map '0:v:0' -map '0:a?' -c:v libx265 -crf 20 -preset medium -tag:v hvc1 -c:a aac -b:a 128k -movflags +faststart "$tmp" && [ -s "$tmp" ]; then
          success=1
          break
        fi
      done
      if [ "$success" -eq 1 ]; then
        mv "$tmp" "$out"
      else
        printf 'failed: %s\n' "$file"
      fi
    done
)
```

## 安全规则

1. 默认压缩成功后删除原文件；只有用户明确要求“保留原图”“保留原视频”“保留原文件”或“保存源文件”时才保留源文件。
2. 不要直接原地编码覆盖源文件；先输出到同目录临时文件或同名新扩展名文件，确认输出存在且非空后再删除或替换源文件。
3. 如果输出文件不存在或为 0KB，删除半成品并重试一次；重试后仍失败时保留源文件并记录失败路径。
4. 保留源文件模式下，输出到目标根目录的 `compressed` 压缩目录，按源文件相对路径镜像目录结构；不要删除源文件，也不要把 `compressed` 目录再次纳入批量压缩输入。
5. 使用 `magick mogrify` 时只有在用户明确要求单独输出目录时才搭配 `-path output-dir`；默认使用逐文件 `magick input output && [ -s output ] && rm -f input`，输出为同目录同名 `.webp`。保留源文件并需要镜像目录结构时，也优先逐文件处理。
6. 使用 `ffmpeg` 时默认输出到同目录临时文件，确认非空后再 `mv` 替换 MP4 原路径；非 MP4 源文件输出为同目录同名 `.mp4`，成功后删除源视频。保留源文件时输出到 `compressed` 镜像目录，不删除源视频。
7. 如果用户要求直接替换原文件，也必须先生成新文件并确认成功，再删除源文件，不要盲目原地改写。
8. 视频压缩输出为 MP4/H.265 时添加 `-tag:v hvc1`，提高 macOS、iPhone 和 iPad 播放兼容性。
9. 路径包含空格时加引号；包含 `>` 的 ImageMagick 几何参数也要加引号，例如 `-resize '1600x1600>'`。
10. 如果输出文件比源文件更大，不要默认删除源文件；告知用户并默认把源文件视为更合适的结果，除非用户指定必须转换格式并删除源文件。

## 默认压缩建议

- 用户只说压缩图片、不要求改格式时，默认转为同目录同名 `WebP`，默认质量 `-quality 85`，压缩成功后删除原图。
- 用户只说压缩视频、不要求改格式时，默认转为同路径 `MP4/H.265`，默认参数 `-crf 20 -preset medium -tag:v hvc1 -c:a aac -b:a 128k`；MP4 使用临时文件替换原路径，非 MP4 输出为同目录同名 `.mp4`，压缩成功后删除原视频。
- 用户明确要求保留或保存源文件时，图片和视频都输出到目标根目录下的 `compressed` 压缩目录，按源文件相对路径保持同样的文件夹结构，源文件不删除。
- 面向网页交付或追求明显减小图片体积时，使用 `WebP`，质量参数建议 `-quality 80-86`。
- 面向照片分享且不需要透明通道时，优先使用 `WebP`；只有用户明确要求 JPEG 时，使用 JPEG，质量参数建议 `-quality 82-88`。
- 截图、UI 素材或需要透明通道时优先保留 PNG，除非用户接受有损压缩换取更小体积。
- 大尺寸图片用于上传或邮件发送时，可添加 `-resize '1600x1600>'` 或 `-resize '2048x2048>'`。
- 视频兼容优先时使用 `MP4/H.264`，默认参数 `-crf 23 -preset medium -c:a aac -b:a 128k`。
- 视频极限压缩且能接受很慢时，可考虑 AV1，但默认不要使用 AV1，除非用户明确要求。
- 默认移除图片元数据；视频默认不保留复杂元数据，除非用户明确要求保留。

## 命令形态

ImageMagick 命令通常遵循 `magick input-file [options] output-file`。多图片处理时，默认逐文件输出到同目录同名 `.webp`，确认输出非空后删除源图；用户明确要求保留源文件时，输出到 `compressed` 压缩目录并镜像源目录结构。

ffmpeg 命令通常遵循 `ffmpeg -i input-file [options] output-file`。多视频处理时，默认输出到源文件同目录下的临时文件，确认成功且非空后替换 MP4 原路径；非 MP4 源文件输出为同目录同名 `.mp4`。用户明确要求保留源文件时，输出到 `compressed` 压缩目录并镜像源目录结构；如目标已存在则跳过并记录失败，除非用户明确允许覆盖。

需要选择高级参数、排查 ImageMagick 语法，或解释命令结构时，阅读 `references/imagemagick-compression.md`。
