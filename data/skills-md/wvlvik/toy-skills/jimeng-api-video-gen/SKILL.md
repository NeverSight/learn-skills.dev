---
name: jimeng-api-video-gen
description: (project - Skill) Generate AI videos using Volcengine Jimeng Video 3.0 Pro API. Use when users request video generation from text prompts or images, including text-to-video, image-to-video, or any AI-powered video creation. Triggers include "generate video", "create video", "AI video", "Jimeng video", "text to video", "image to video", or any request involving AI-powered video generation from descriptions.
---

# Jimeng API Video Generation

Generate high-quality AI videos using Volcengine's Jimeng Video 3.0 Pro API with text prompts or input images.

## Configure Environment Variables

[Get Access Key/Secret Key](https://www.volcengine.com/docs/85621/1995636?lang=zh#3C9mCW9O)

```bash
# ~/.zshrc or ~/.zshenv
export VOLC_ACCESSKEY="your_access_key_id"
export VOLC_SECRETKEY="your_secret_access_key"
```

## Output Behavior (Important)

**After video generation succeeds, you MUST display the video directly to the user!**

When generation completes, output in the following format:

\`\`\`markdown
**Generated Video:**

[Download Video](VIDEO_URL)

**Generation Info:**
- Prompt: [User's original prompt]
- Duration: [Video length in seconds]
- Mode: [Generation mode used]
- FPS: [Frames per second]
- Save Path: [Local file path, if applicable]
\`\`\`

### Example Output

\`\`\`markdown
**Generated Video:**

[Download Video](https://example.com/video.mp4)

**Generation Info:**
- Prompt: A golden retriever running through a field of sunflowers, warm afternoon sunlight
- Duration: 5 seconds
- Mode: t2v_720p
- FPS: 24
- Save Path: /generated_videos/dog_sunflowers.mp4
```

## API Configuration

| Parameter | Value | Description |
|-----------|-------|-------------|
| Endpoint | \`https://visual.volcengineapi.com\` | API base URL |
| Submit Action | \`CVSync2AsyncSubmitTask\` | Submit async generation task |
| Query Action | \`CVSync2AsyncGetResult\` | Query task result |
| Version | \`2022-08-31\` | API version |
| Service | \`cv\` | Service name for signing |
| Region | \`cn-north-1\` | Region for signing |

## Generation Modes

### Pro Version (1080P HD)

| Mode | req_key | Description |
|------|---------|-------------|
| `ti2v_pro` | `jimeng_ti2v_v30_pro` | Text-to-video + Image-to-video (first frame) Pro |

### 1080P Version

| Mode | req_key | Description |
|------|---------|-------------|
| `t2v_1080p` | `jimeng_t2v_v30_1080p` | Text-to-video 1080P |
| `i2v_first_1080p` | `jimeng_i2v_first_v30_1080` | Image-to-video (first frame) 1080P |
| `i2v_first_tail_1080p` | `jimeng_i2v_first_tail_v30_1080` | Image-to-video (first & last frame) 1080P |

### 720P Version

| Mode | req_key | Description |
|------|---------|-------------|
| `t2v_720p` | `jimeng_t2v_v30` | Text-to-video 720P |
| `i2v_first_720p` | `jimeng_i2v_first_v30` | Image-to-video (first frame) 720P |
| `i2v_first_tail_720p` | `jimeng_i2v_first_tail_v30` | Image-to-video (first & last frame) 720P |
| `i2v_recamera_720p` | `jimeng_i2v_recamera_v30` | Image-to-video (camera movement) 720P |

## Command-Line Options

\`\`\`
scripts/generate_video.py PROMPT [OPTIONS]

Arguments:
  PROMPT              Text prompt for video generation (required)

Options:
  --mode MODE         Generation mode (default: t2v_720p)
                      Pro: ti2v_pro
                      1080P: t2v_1080p, i2v_first_1080p, i2v_first_tail_1080p
                      720P: t2v_720p, i2v_first_720p, i2v_first_tail_720p, i2v_recamera_720p
  --duration SECS     Video duration: 4, 5, 6, 8, 10 (default: 5)
  --fps FPS           Frames per second: 24, 25, 30 (default: 24)
  --image URL         Input image URL for image-to-video (first frame)
  --tail-image URL    Tail image URL for first & last frame mode
  --seed INT          Random seed for reproducibility
  --output PATH       Download video to file
  --json              Output raw JSON response

Environment Variables:
  VOLC_ACCESSKEY           Access Key ID (required)
  VOLC_SECRETKEY           Secret Access Key (required)
  JIMENG_VIDEO_API_URL     API endpoint (default: https://visual.volcengineapi.com)
  JIMENG_VIDEO_API_TIMEOUT Request timeout seconds (default: 300)
  JIMENG_VIDEO_POLL_INTERVAL Polling interval seconds (default: 5)
  JIMENG_VIDEO_MAX_POLL_ATTEMPTS Max polling attempts (default: 120)
\`\`\`

## Video Specifications

### Duration Options

| Duration | Use Case |
|----------|----------|
| 4s | Quick clips, social media |
| 5s | Default, general purpose |
| 6s | Short scenes |
| 8s | Medium-length content |
| 10s | Longer narratives |

### FPS Options

| FPS | Use Case |
|-----|----------|
| 24 | Cinematic look (default) |
| 25 | PAL video standard |
| 30 | Smooth motion, NTSC standard |

## Authentication

This skill uses Volcengine IAM v4 signature authentication (HMAC-SHA256). The signing process:

1. Build canonical request with headers: \`content-type;host;x-content-sha256;x-date\`
2. Calculate SHA256 hash of canonical request
3. Derive signing key: secret_key → date → region → service → "request"
4. Sign the string-to-sign with derived key
5. Add \`Authorization\` header to request

Reference: [HTTP请求示例](https://www.volcengine.com/docs/6444/1390583)

## Error Codes

| Code | Message | Description |
|------|---------|-------------|
| 10000 | Success | Request successful |
| 50411 | Pre Img Risk Not Pass | Input image failed content check |
| 50511 | Post Video Risk Not Pass | Output video failed content check |
| 50412 | Text Risk Not Pass | Input text failed content check |
| 50429 | Request Has Reached API Limit | Rate limit exceeded, retry later |
| 50500 | Internal Error | Server error |
| timeout | Request timeout | Increase JIMENG_VIDEO_API_TIMEOUT |

## Input/Output Limits

**Input Images (for image-to-video):**
- Format: JPEG, PNG only
- Max size: 15MB per image
- Max resolution: 4096×4096

**Output:**
- Format: MP4
- URL validity: 24 hours
- Generation time: 2-10 minutes depending on duration and mode

## Reference Documentation

- [Jimeng Video 3.0 Pro API Documentation](https://www.volcengine.com/docs/85621/1777001)
- [Jimeng Video 3.0 720P API](https://www.volcengine.com/docs/85621/1792710)
- [Jimeng Video 3.0 1080P API](https://www.volcengine.com/docs/85621/1792711)
- [HTTP Request Example](https://www.volcengine.com/docs/6444/1390583)
- [Volcengine Console](https://console.volcengine.com)
- [API Key Management](https://console.volcengine.com/iam/key_manage/)
