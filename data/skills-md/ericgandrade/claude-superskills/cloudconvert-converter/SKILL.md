---
name: cloudconvert-converter
description: This skill should be used when the user needs to convert files between formats (documents, images, video, audio, PDFs, presentations), perform PDF operations (OCR, merge, split, rotate, encrypt, decrypt), or process files that pandoc and docling do not support. Trigger when the user says "convert this file", "transform to PDF", "extract text with OCR", "merge PDFs", "compress video", "convert pptx to pdf", "convert image to webp", or mentions CloudConvert explicitly. Use this skill whenever format conversion or PDF manipulation is needed, even if the user does not name the tool.
license: MIT
---

# cloudconvert-converter

## Purpose

Orchestrate file conversions and PDF operations using the CloudConvert MCP tools. Supports 200+ formats across documents, images, video, audio, presentations, spreadsheets, archives, and CAD files.

## When to Use

- Converting between formats that pandoc or docling do not support (video, audio, CAD, fonts, archives)
- Converting presentation files (pptx, ppt, odp) to PDF, images, or HTML
- PDF operations: OCR for text extraction, merge multiple PDFs, split by page range, rotate, encrypt/decrypt
- Batch format conversion pipelines
- Any file conversion where quality, format fidelity, or specialized options matter

**Do NOT use for:**
- Converting code between programming languages (JavaScript → TypeScript, etc.)
- Currency or unit conversions
- Questions about conversion tools without an actual file to process
- Simple markdown → HTML conversions already handled by the shell

## Free Tier Warning

CloudConvert free accounts include **10 conversion minutes per day**.
Before converting, assess whether the task fits the free limit.
For testing: `export CLOUDCONVERT_SANDBOX=true` (no credits consumed).
Check remaining credits: https://cloudconvert.com/dashboard

## Step 0: Discovery

Before starting any conversion, check the environment:

```bash
# Verify API key is set
echo ${CLOUDCONVERT_API_KEY:+"API key is set"}
```

If `CLOUDCONVERT_API_KEY` is not set:
1. Stop immediately — do not attempt conversion
2. Show the setup instruction:
   ```
   export CLOUDCONVERT_API_KEY="your-key"
   ```
3. Link to key creation: https://cloudconvert.com/dashboard/api/v2/keys
4. Remind about free tier limits and sandbox mode

If the target format is unclear, call `cloudconvert_list_formats` first — it never consumes credits.

## Progress Tracking

Display progress before each conversion phase:

```
[████░░░░░░░░░░░░░░░░] 25% — Phase 1/4: Validating File & Format Support
[████████░░░░░░░░░░░░] 50% — Phase 2/4: Uploading & Converting
[████████████░░░░░░░░] 75% — Phase 3/4: Downloading Result
[████████████████████] 100% — Phase 4/4: Confirming & Cleaning Up
```

For batch operations: `[N/M files converted — X%]`

## Workflow

### Standard File Conversion (most common case)

Use `cloudconvert_convert` for end-to-end conversions. It handles import → convert → export → download in one call.

```
1. Identify input source: local file path or remote URL
2. Identify output format (ask if ambiguous)
3. Call cloudconvert_convert with:
   - input_file: "/path/to/file.pptx"   (local)
   - input_url:  "https://..."           (remote)
   - output_format: "pdf"
   - output_path: same directory as input (default: cwd)
   - options: only if the user requested specific settings (quality, resolution, pages)
4. Report saved_path and size_human to the user
```

### Advanced Multi-Step Pipeline

Use `cloudconvert_create_job` when chaining multiple operations (compress then convert, watermark then export, etc.):

```
1. Build the tasks dict with named operations
2. Call cloudconvert_create_job
3. Upload local files with cloudconvert_upload_file if needed
4. Call cloudconvert_wait_job (timeout: 120s for documents, 300s for video)
5. Download each URL with cloudconvert_download_file
```

### PDF Operations

Use `cloudconvert_pdf_operations` for specialized PDF tasks:

| Operation | When to use | Key options |
|-----------|-------------|-------------|
| `ocr`     | PDF/image has text in image form | `{"language": "por"}` for Portuguese |
| `merge`   | Combine 2+ PDFs into one | `input_files: [...]` (≥2 items) |
| `split`   | Extract specific pages | `{"pages": "1-3,5,7-9"}` |
| `rotate`  | Fix page orientation | `{"rotate": 90}` (90, 180, 270) |
| `encrypt` | Add password protection | `{"user_password": "...", "owner_password": "..."}` |
| `decrypt` | Remove password | `{"password": "..."}` |

### Format Discovery

Before converting an uncommon format, verify support:

```
cloudconvert_list_formats(input_format="pptx")
→ shows all supported output formats for .pptx
```

This call is free (no credits). Use it to:
- Confirm a conversion is supported before submitting
- Suggest alternatives when the requested output is not available
- Choose between multiple valid output options

## Error Handling

### API Key Not Set / Invalid (error: invalid_api_key)
```
Stop conversion immediately.
Show:
  "CloudConvert API key missing or invalid.
   Fix: export CLOUDCONVERT_API_KEY='your-key'
   Get key: https://cloudconvert.com/dashboard/api/v2/keys"
Do NOT retry automatically.
```

### Free Tier Quota Exceeded (error: quota_exceeded)
```
Stop and inform the user:
  "Free tier limit reached (10 conversion minutes/day).
   Options:
   1. Use CLOUDCONVERT_SANDBOX=true for testing (no real conversion)
   2. Upgrade at https://cloudconvert.com/pricing
   3. Try again tomorrow when the daily limit resets"
Do NOT retry — each attempt consumes credits.
```

### Format Not Supported (error: unsupported_format)
```
Call cloudconvert_list_formats for the input format.
Suggest the closest supported output formats.
If applicable, suggest a two-step route:
  Example: docx → pdf → epub  (if docx → epub is unsupported)
```

### File Not Found (error: file_not_found)
```
Report the exact path that was not found.
Ask the user to confirm the path or provide the correct one.
Do not guess alternative paths.
```

### Job Timeout (error: timeout)
```
Call cloudconvert_get_job to check current status.
If still running: report "still processing" and provide the job_id.
If failed: show the task-level error message from the response.
Never silently drop the job — always report final state.
```

### File Too Large (error: file_too_large)
```
Inform the user of the size limit.
Suggest compression before converting if applicable.
Link to plan comparison: https://cloudconvert.com/pricing
```

### Network / Server Error (error: server_error)
```
Retry once after 5 seconds.
If it fails again: report the error and link to status page.
  https://status.cloudconvert.com
```

## Common Conversion Examples

**PPTX → PDF:**
```
cloudconvert_convert(input_file="/path/file.pptx", output_format="pdf")
```

**Image → WebP (with quality):**
```
cloudconvert_convert(input_file="/path/photo.jpg", output_format="webp", options={"quality": 85})
```

**PDF OCR (Portuguese):**
```
cloudconvert_pdf_operations(operation="ocr", input_files=["/path/scan.pdf"], options={"language": "por"})
```

**Merge PDFs:**
```
cloudconvert_pdf_operations(operation="merge", input_files=["/a.pdf", "/b.pdf", "/c.pdf"])
```

**Video compress + convert:**
```
cloudconvert_convert(input_file="/path/video.mov", output_format="mp4", options={"video_codec": "h264", "crf": 23})
```

**Check formats for .docx:**
```
cloudconvert_list_formats(input_format="docx")
```

## Comparison: When to Use CloudConvert vs Alternatives

| Tool | Best for |
|------|----------|
| `cloudconvert-converter` | Video, audio, CAD, fonts, archives; high-fidelity PDF/Office; OCR; merging |
| `docling-converter` | PDF/Office → structured Markdown or JSON; layout-aware extraction |
| `pandoc` | Markdown ↔ HTML ↔ LaTeX ↔ DOCX; lightweight document conversions |

When in doubt: if the file is a document and the goal is structured text extraction, use docling. If the goal is format conversion with quality control, use CloudConvert.

## Critical Rules

- NEVER start a conversion without verifying `CLOUDCONVERT_API_KEY` is set
- NEVER retry on quota_exceeded errors — each attempt uses credits
- NEVER silently fail — always report error type and recovery action
- ALWAYS call `cloudconvert_list_formats` before converting uncommon format pairs
- ALWAYS report the `saved_path` after a successful download
- ALWAYS mention sandbox mode when helping users test or develop
