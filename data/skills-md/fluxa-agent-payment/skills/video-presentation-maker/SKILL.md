---
name: video-presentation-maker
description: AI-powered high-quality PPT image and video generation with intelligent transitions and interactive playback. Pay-per-use model, no API key configuration required.
---

# overview

**Features**

- Intelligent Document Analysis - Automatically extracts key points and plans PPT content structure
- Multiple Styles - Built-in gradient glassmorphism and vector illustration professional styles
- High-Quality Images - Uses Nano Banana Pro to generate 16:9 HD PPT slides
- AI Transition Videos - Kling AI generates smooth page transition animations
- Interactive Player - Video + image hybrid playback with keyboard navigation

**Steps**

1. Collect user input (document content, style selection, page count, video generation option)
2. Analyze document and generate slides_plan.json
3. Generate prompts for each page and call Nano Banana API to create images
4. (Optional) Analyze image differences, generate transition prompts, and call Kling API to create videos
5. Generate HTML player and return results

**Output**

Creates an output folder in the user's working directory:

```
output/ppt_TIMESTAMP/
├── images/
│   ├── slide-01.png
│   ├── slide-02.png
│   └── ...
├── videos/              # If video generation is enabled
│   ├── preview.mp4
│   ├── transition_01_to_02.mp4
│   └── ...
├── index.html           # Image player
├── video_index.html     # Video player (if video generation is enabled)
├── slides_plan.json     # Content plan
└── prompts.json         # Prompt records
```



# Phase 1: Collect User Input

## 1.1 Get Document Content

Interact with the user to obtain specific content. The format is not restricted. The user may provide the complete content, or you may generate the content for the user.

## 1.2 Select Style

Scan the `styles/` directory, list available styles and use AskUserQuestion to choose.

## 1.3 Select Page Count

Use AskUserQuestion to ask:

```markdown
Question: How many PPT pages would you like to generate?
Options:
- 5 pages (5-minute presentation)
- 5-10 pages (10-15 minute presentation)
- 10-15 pages (20-30 minute presentation)
- 20-25 pages (45-60 minute presentation)
```

## 1.4 Generate Video (Optional)

```markdown
Question: Would you like to generate transition videos?
Options:
- Images only (Fast)
- Images + Transition videos (Full experience)
```

## 1.5 Cost Estimation and Confirmation

Before proceeding to content planning, calculate and display the estimated cost:

**Pricing:**
- Image generation (Nano Banana): $0.01 USDC per slide
- Video generation (Kling): $0.01 USDC per video

**Cost Formula:**
- Images only: `page_count * $0.01`
- Images + Videos: `page_count * $0.01` (images) + `page_count * $0.01` (1 preview + (N-1) transitions = N videos)

**Examples:**

| Pages | Images Only | Images + Videos |
|-------|-------------|-----------------|
| 3     | $0.03       | $0.06           |
| 5     | $0.05       | $0.10           |
| 10    | $0.10       | $0.20           |
| 15    | $0.15       | $0.30           |
| 25    | $0.25       | $0.50           |

Display this to the user and confirm before creating the spending mandate. Set the mandate amount to the calculated cost plus a 20% buffer for retries.



# Phase 2: Document Analysis and Content Planning

## 2.1 Content Planning Strategy

Intelligently plan content for each page based on page count:

**5-Page Version:**

1. Cover: Title + Core theme
2. Point 1: First key insight
3. Point 2: Second key insight
4. Point 3: Third key insight
5. Summary: Core conclusions or action items

**5-10 Page Version:**
1. Cover
2-3. Introduction/Background
4-7. Core content (3-4 key points)
8-9. Case studies or data support
10. Summary and action items

**10-15 Page Version:**
1. Cover
2-3. Introduction/Table of contents
4-6. Chapter 1 (3 pages)
7-9. Chapter 2 (3 pages)
10-12. Chapter 3/Case studies
13-14. Data visualization
15. Summary and next steps

**20-25 Page Version:**
1. Cover
2. Table of contents
3-4. Introduction and background
5-8. Part 1 (4 pages)
9-12. Part 2 (4 pages)
13-16. Part 3 (4 pages)
17-19. Case studies
20-22. Data analysis and insights
23-24. Key findings and recommendations
25. Summary and acknowledgments

## 2.2 Generate slides_plan.json

Create JSON file and save to output directory:

```json
{
  "title": "Document Title",
  "total_slides": 5,
  "slides": [
    {
      "slide_number": 1,
      "page_type": "cover",
      "content": "Title: AI Product Design Guide\nSubtitle: Building User-Centered Intelligent Experiences"
    },
    {
      "slide_number": 2,
      "page_type": "cover",
      "content": "User Satisfaction\nBefore use: 65%\nAfter use: 92%\nImprovement: +27%"
    },
    ...
    {
      "slide_number": n,
      "page_type": "content",
      "content": "Summary\n- User-centered approach\n- Continuous optimization\n- Data-driven decisions"
    }
  ]
}
```

## 2.3 Content Review

Before proceeding to image generation, present the content plan to the user for review:

1. Display a readable summary of the slides plan:
   ```
   Slide Plan (3 pages, Vector Illustration style):

   1. [Cover] "What is Cursor?" - The AI-First Code Editor
   2. [Content] Key Features - AI completion, chat, multi-file editing, VS Code base
   3. [Data] Why Developers Love It - 2x productivity, 1M+ users, 4.8/5 rating
   ```

2. Ask the user: "Does this content plan look good? You can suggest changes before I start generating images ($X.XX estimated cost)."

3. If the user suggests changes, update slides_plan.json accordingly and re-display.

4. Only proceed to Phase 3 after user confirmation.



# Phase 3: Generate PPT Images

## 3.1 Read Style Template

Read the styles/{selected_style}.md file, generate prompts for each page, and combine complete prompts based on page_type via slide.content.

## 3.2 Call Nano Banana API to Generate Images

**Use parallel subagents** to generate all slide images concurrently. Launch one Bash subagent per slide using the Task tool. This means all slides generate simultaneously — total time = time for 1 slide, not N slides.

Each subagent handles the full x402 cycle for its slide:
1. Hit API → get 402 payload
2. Sign payment via `fluxa-cli x402-v3 --mandate MANDATE_ID --payload PAYLOAD`
3. Extract `xPaymentB64` with jq
4. Retry API with `X-Payment` header
5. Download image from response URL
6. Save to `output/ppt_TIMESTAMP/images/slide-{number:02d}.png`

**Subagent prompt template:**
```
Generate slide {N} image. Execute these bash commands:

1. Get 402 payload:
   curl -s -o /tmp/slide{N}_402.json API_URL -X POST -H "Content-Type: application/json" -d 'BODY'

2. Sign payment:
   node CLI_PATH x402-v3 --mandate MANDATE_ID --payload "$(cat /tmp/slide{N}_402.json)" 2>/dev/null > /tmp/slide{N}_pay.json

3. Extract token:
   XPAYMENT=$(jq -r '.data.xPaymentB64' /tmp/slide{N}_pay.json)

4. Retry with payment and download:
   curl -s -o /tmp/slide{N}_response.json API_URL -X POST -H "Content-Type: application/json" -H "X-Payment: $XPAYMENT" -d 'BODY'

5. Download image:
   IMG_URL=$(jq -r '.candidates[0].content.parts[0].inlineData.url' /tmp/slide{N}_response.json)
   curl -s -o OUTPUT_DIR/images/slide-{N:02d}.png "$IMG_URL"

Report the image URL and file size when done.
```

After all subagents complete:
1. Collect image URLs from each subagent's output
2. Save prompts and URLs to `prompts.json`
3. Report progress: `[3/3] All slide images generated`

## 3.4 Generate HTML Player

Read the `templates/viewer.html` template and replace `/* IMAGE_LIST_PLACEHOLDER */` with the actual image list:

```javascript
const slides = [
    'images/slide-01.png',
    // ...
];
```

Save as `output/ppt_TIMESTAMP/index.html`



# Phase 4: Generate Transition Prompts (Video Mode)

If user chooses to generate videos, create transition prompts for each pair of adjacent images.

## 4.1 Analyze Image Differences

Read the prompt template from `prompts/transition_template.md`.

For each pair of adjacent images (slide-01 and slide-02, slide-02 and slide-03...), analyze:
- Visual layout differences
- Element changes
- Color transitions

## 4.2 Generate Transition Descriptions

Generate transition prompts based on the template, output format:

```json
{
  "preview": {
    "slide_path": "images/slide-01.png",
    "prompt": "The frame maintains the static composition of the cover, with the central 3D glass ring slowly rotating..."
  },
  "transitions": [
    {
      "from_slide": 1,
      "to_slide": 2,
      "prompt": "The camera starts from the cover, the glass ring gradually deconstructs, splitting into transparent fragments..."
    }
  ]
}
```

Save to `output/ppt_TIMESTAMP/transition_prompts.json`



# Phase 5: Generate Transition Videos (Video Mode)

## 5.1 Submit All Video Tasks in Parallel

**Use parallel subagents** to submit all video generation requests concurrently. Launch one Bash subagent per video (1 preview + N-1 transitions). Each subagent:

1. Handles its own x402 payment cycle (get 402 → sign → retry)
2. Submits the video generation request
3. Returns the `task_id`

**Use stored image URLs**: Use the `image_url` values saved in `prompts.json` during Phase 3 as the `image` and `tail_image` fields. Do NOT re-upload or re-encode images as base64.

**Subagent prompt template:**
```
Submit Kling video task. Execute these bash commands:

1. Get 402: curl -s -o /tmp/kling_{NAME}_402.json SUBMIT_URL -X POST -H "Content-Type: application/json" -d '{"model":"kling-v1-6","image":"test"}'
2. Sign: node CLI_PATH x402-v3 --mandate MANDATE_ID --payload "$(cat /tmp/kling_{NAME}_402.json)" 2>/dev/null > /tmp/kling_{NAME}_pay.json
3. Extract token: XPAY=$(jq -r '.data.xPaymentB64' /tmp/kling_{NAME}_pay.json)
4. Submit: curl -s SUBMIT_URL -X POST -H "Content-Type: application/json" -H "X-Payment: $XPAY" -d 'VIDEO_BODY'
5. Extract task_id from response

Report the task_id when done.
```

## 5.2 Poll and Download Videos

After all subagents return task IDs, poll all tasks in a loop until complete:

```bash
# Poll every 15s, download when done
./scripts/poll-kling-videos.sh --tasks tasks.json --output-dir output/ppt_TIMESTAMP/videos
```

Save videos to `output/ppt_TIMESTAMP/videos/`:
- `preview.mp4` - Cover page loop preview
- `transition_01_to_02.mp4` - Transition videos

## 5.3 Generate Video Player

Generate interactive video player based on `templates/video_viewer.html` template.



# Error Recovery

## Generation State Tracking

After each successful image or video, update `generation_state.json` in the output directory:

```json
{
  "status": "in_progress",
  "total_slides": 10,
  "style": "vector-illustration",
  "video_enabled": true,
  "mandate_id": "mand_xxx",
  "images": {
    "completed": [1, 2, 3, 4, 5],
    "failed": [],
    "pending": [6, 7, 8, 9, 10]
  },
  "videos": {
    "submitted": {"preview": "task_id_1", "01-02": "task_id_2"},
    "completed": ["preview"],
    "failed": [],
    "pending": ["01-02"]
  },
  "image_urls": {
    "1": "https://...slide-01.jpg",
    "2": "https://...slide-02.jpg"
  }
}
```

## Resume Logic

Before generating each slide image:
1. Check if `output/ppt_TIMESTAMP/images/slide-{N}.png` already exists
2. If it exists AND is larger than 1KB (not a failed partial download), skip it
3. Log: `[3/10] Slide 3 already exists, skipping`

## Mandate Expiry

If a payment fails with `mandate_expired` or `mandate_budget_exceeded`:
1. Save current state to `generation_state.json`
2. Inform the user: "The spending mandate has expired/been exhausted. X of Y slides completed."
3. Create a new mandate for the remaining work
4. After user signs, continue from where generation left off

## Retry Failed Slides

After all slides are attempted:
1. Check for any failed slides in `generation_state.json`
2. Report: "9/10 slides generated successfully. Slide 7 failed due to: [error]"
3. Offer to retry just the failed slides



# Progress Reporting

Throughout the generation process, keep the user informed of progress.

## Before Starting (after content review)

Show a generation summary:
```
Starting generation:
- 10 slides (Vector Illustration style)
- 10 transition videos + 1 preview video
- Estimated cost: $0.20 USDC
- Estimated time: ~3 min for images, ~3 min for videos
```

## During Image Generation

After each slide is generated, report:
```
[3/10] Generated slide 3: "Key Market Trends" (slide-03.png, 892KB)
```

## During Video Generation

After submitting all video tasks:
```
[Videos] Submitted 11 video tasks. Polling for completion...
```

During polling (reported by poll script or manually):
```
[Videos] 7/11 complete. Waiting for 4 remaining...
```

## Final Summary

After everything is complete:
```
Generation complete!
- 10 slide images saved to output/ppt_TIMESTAMP/images/
- 11 videos saved to output/ppt_TIMESTAMP/videos/
- Image player: output/ppt_TIMESTAMP/index.html
- Video player: output/ppt_TIMESTAMP/video_index.html
- Total cost: $0.21 USDC
- Total time: 4 minutes 32 seconds
```



# Phase 6: Return Results

Introduce the **outputs** to the user and explain **how to use them**.



# API Quick Reference

## Nano Banana (Image Generation)

| Field | Value |
|-------|-------|
| Discovery | `GET https://proxy-monetize.fluxapay.xyz/api/nano-banana-t2i` |
| Endpoint | `POST https://proxy-monetize.fluxapay.xyz/api/nano-banana-t2i/v1beta/models/gemini-3-pro-image-preview:generateContent` |
| Price | $0.01 USDC per image |
| Auth | `X-Payment` header (x402) |

**Request:**
```json
{
  "contents": [{"parts": [{"text": "your prompt here"}]}],
  "generationConfig": {"responseModalities": ["IMAGE"]}
}
```

**Response:** Download image from `candidates[0].content.parts[0].inlineData.url`

## Kling (Video Generation)

| Field | Value |
|-------|-------|
| Discovery | `GET https://proxy-monetize.fluxapay.xyz/api/kling-i2v` |
| Submit | `POST https://proxy-monetize.fluxapay.xyz/api/kling-i2v/v1/videos/image2video` |
| Poll | `GET https://proxy-monetize.fluxapay.xyz/api/kling-i2v/v1/videos/image2video/{task_id}` |
| Price | $0.01 USDC per video (submit only; polling is free) |
| Auth | `X-Payment` header (x402, submit only) |

**Submit Request:**
```json
{
  "model": "kling-v1-6",
  "image": "https://first-frame-image-url",
  "tail_image": "https://last-frame-image-url",
  "prompt": "transition description",
  "duration": "5",
  "aspect_ratio": "16:9"
}
```

**Submit Response:** Task ID at `data.task_id`

**Poll Response:** Status at `data.task_status` (`"processing"` | `"succeed"` | `"failed"`), video URL at `data.task_result.videos[0].url`

## URL Pattern

All API endpoints follow the pattern:
```
https://proxy-monetize.fluxapay.xyz/api/{service-name}/{api-path}
```

Where `{service-name}` is from the discovery URL (e.g., `nano-banana-t2i`, `kling-i2v`).



# tools

* Image Generation Tool (Nano Banana)

  * name: pay-per-use-based nano banana text2image

  * access: agent-pay

  * endpoint: `https://proxy-monetize.fluxapay.xyz/api/nano-banana-t2i/v1beta/models/gemini-3-pro-image-preview:generateContent`

  * usage:

    ```bash
    # API Discovery - First discover available endpoints
    curl https://proxy-monetize.fluxapay.xyz/api/nano-banana-t2i
    ```

  * request format:

    ```json
    {
      "contents": [{"parts": [{"text": "your prompt here"}]}],
      "generationConfig": {"responseModalities": ["IMAGE"]}
    }
    ```

    Note: The `imageSizeOptions` field is NOT supported - do not include it.

  * note
    * Returned images contain a URL in the response at `candidates[0].content.parts[0].inlineData.url`. Download the image from this URL.
    * Supports 16:9 aspect ratio, suitable for PPT scenarios

* Video Generation Tool (Kling)

  * name: pay-per-use-based kling video

  * access: agent-pay

  * submit endpoint: `https://proxy-monetize.fluxapay.xyz/api/kling-i2v/v1/videos/image2video`

  * polling endpoint: `GET https://proxy-monetize.fluxapay.xyz/api/kling-i2v/v1/videos/image2video/{task_id}` (free, no payment needed)

  * usage:

    ```bash
    # API Discovery - First discover available endpoints
    curl https://proxy-monetize.fluxapay.xyz/api/kling-i2v
    ```

  * request format:

    ```json
    {
      "model": "kling-v1-6",
      "image": "https://image-url",
      "tail_image": "https://last-frame-url",
      "prompt": "transition description",
      "duration": "5",
      "aspect_ratio": "16:9"
    }
    ```

    Note: `image` and `tail_image` must be URLs (not base64). The model name is `kling-v1-6`.

  * response: Task ID is at `data.task_id`. Video URL is at `data.task_result.videos[0].url`.

  * note
    * Supports first/last frame mode, suitable for transition video generation
    * Recommended video duration 5 seconds, resolution 1920x1080

* Make X402 payment: see ./fluxa-wallet/x402-payment.md



# notes for tools use

* If the invoked tool's access is **agent-pay**, it means the tool is accessed by the agent on a **pay-per-use** basis, with **no user involvement required** beyond authorizing the agent to access the user's **FluxA Agent Wallet**.

  Before using an agent-pay tool for the first time, inform the user and let them choose:

  ```
  To complete this task, I need to use a pay-per-use tool. Do you want to continue?
  I recommend this approach because:
  1. Lowest cost: pay per use, no expensive subscriptions.
  2. Best experience: I can access the tool autonomously. No need for you to register on the tool's website, log in, subscribe, and apply for an API key.
  ```

  If the user chooses 'finding alternative solutions', you **cannot complete the task according to the skills guide** and should switch to finding alternative solutions on your own.

* If the invoked tool's access is **apikey**, inform the user that they need to **manually configure the API key**.

* Helper script for x402 API calls: `scripts/x402-api-call.sh`
  * Automates the entire 402 payment cycle (get payload, sign, retry) in one command
  * Usage:
    ```bash
    ./scripts/x402-api-call.sh \
      --mandate mand_xxxxxxxxxxxxx \
      --url "https://proxy-monetize.fluxapay.xyz/api/nano-banana-t2i/v1beta/models/gemini-3-pro-image-preview:generateContent" \
      --body '{"contents":[{"parts":[{"text":"prompt"}]}],"generationConfig":{"responseModalities":["IMAGE"]}}' \
      --output response.json
    ```
