---
name: data-conversion
description: Convert audio, video, images, documents, and PDF text with the right CLI tool. Use when the user wants format conversion, media extraction, PDF-to-text, or guidance on installing ffmpeg, ImageMagick, pandoc, or pdftotext.
---

# Data Conversion

Use this skill when the user needs to convert one format into another and the
best path is a standard CLI tool rather than custom code.

## Pick the primary tool

- Audio or video conversion: use `ffmpeg`
- Image format conversion: use ImageMagick `convert`
- Text or document conversion: use `pandoc`
- PDF to plain text extraction: use `pdftotext`

If the request spans multiple categories, choose the tool that matches the
output the user actually wants. For example, `mp4 -> mp3` is still `ffmpeg`.

## Keep the entry point short

Use this file for routing and dependency handling only. Load the matching
reference file when you need concrete commands, supported formats, or caveats:

- `references/ffmpeg.md`
- `references/imagemagick.md`
- `references/pandoc.md`
- `references/pdftotext.md`

## Missing command workflow

1. Check whether the required command exists before assuming it is usable.
2. If the command is missing, ask whether installation is acceptable before
   proposing environment changes.
3. If the user agrees to install, prefer package-manager installation guidance
   or execution when allowed. You may also provide manual installation links or
   commands for the user to run.
4. If the user declines installation and `python3` exists, attempt a Python
   fallback only when it is a reasonable substitute for the requested
   conversion.
5. If neither the native CLI nor a practical Python fallback is available,
   explain the limitation and refuse the approach instead of guessing.

## Installation handling rules

Supported installation paths:

- Use a package manager when appropriate for the environment.
- Provide installation commands for the user to run themselves.
- Refuse installation-based approaches if the user does not want local changes
  or the environment makes them inappropriate.

When you provide package-manager guidance, prefer the least surprising package
name for the platform and note any common variants if that helps. If a command
normally needs elevated privileges, say so clearly rather than implying it will
work unprivileged.

## Python fallback guardrails

Use Python only as a fallback when the required CLI is unavailable and the user
has declined installation.

- For images, Python libraries such as Pillow can sometimes replace `convert`.
- For text or lightweight document transforms, Python parsing libraries may be
  viable when the requested format is simple.
- For audio/video conversion, Python is usually only a wrapper around native
  codecs. Do not imply that pure Python can replace a missing `ffmpeg` for
  general media transcoding.
- For PDF extraction, Python libraries may work for basic extraction but can be
  less reliable than `pdftotext` on layout-heavy files.

If the fallback would require non-trivial third-party Python packages that are
also absent, treat that as another installation request instead of a silent
workaround.
