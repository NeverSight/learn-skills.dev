---
name: scope-validator
description: Validate feature requests against Genfeed OSS core vs Cloud scope. Helps users and contributors understand whether a feature belongs in the open-source core (submit PR) or Cloud SaaS (subscribe).
version: 1.0.0
tags:
  - genfeed
  - scope
  - oss
  - cloud
  - contribution
---

# Scope Validator

Helps users and contributors understand whether a feature belongs in:

- **OSS Core** → Submit a PR or feature request to [genfeedai/core](https://github.com/genfeedai/core)
- **Cloud SaaS** → Subscribe at [genfeed.ai/cloud](https://genfeed.ai/cloud)

## When This Activates

- User asks "should this be in core or cloud?"
- User wants to contribute a new node or feature
- User requests social publishing features
- User asks about RSS/Twitter/feed integration
- Feature request triage
- PR review for scope compliance

## OSS Core Scope

### Included Nodes (26 total)

#### Input Nodes (5)

| Node | Type | Description |
|------|------|-------------|
| Image Input | `imageInput` | Upload or reference an image |
| Audio Input | `audioInput` | Upload an audio file (MP3, WAV) |
| Video Input | `videoInput` | Upload or reference a video file |
| Prompt | `prompt` | Text prompt for AI generation |
| Template | `template` | Preset prompt template |

#### AI Nodes (7)

| Node | Type | Description |
|------|------|-------------|
| Image Generator | `imageGen` | Generate images with nano-banana models |
| Video Generator | `videoGen` | Generate videos with veo-3.1 models |
| LLM | `llm` | Generate text with meta-llama |
| Lip Sync | `lipSync` | Generate talking-head video from image/video and audio |
| Voice Change | `voiceChange` | Replace or mix audio track in a video |
| Text to Speech | `textToSpeech` | Convert text to natural-sounding speech |
| Transcribe | `transcribe` | Convert video or audio to text transcript |

#### Processing Nodes (12)

| Node | Type | Description |
|------|------|-------------|
| Resize | `resize` | Resize media to different aspect ratios using Luma AI |
| Animation | `animation` | Apply easing curve to video |
| Video Stitch | `videoStitch` | Concatenate multiple videos |
| Video Trim | `videoTrim` | Trim video to a specific time range |
| Frame Extract | `videoFrameExtract` | Extract a specific frame from video as image |
| Luma Reframe Image | `lumaReframeImage` | AI-powered image outpainting |
| Luma Reframe Video | `lumaReframeVideo` | AI-powered video reframing |
| Topaz Image Upscale | `topazImageUpscale` | AI-powered image upscaling with face enhancement |
| Topaz Video Upscale | `topazVideoUpscale` | AI-powered video upscaling to 4K |
| Grid Split | `imageGridSplit` | Split image into grid cells |
| Annotation | `annotation` | Add shapes, arrows, and text to images |
| Subtitle | `subtitle` | Burn subtitles into video using FFmpeg |

#### Output Nodes (2)

| Node | Type | Description |
|------|------|-------------|
| Output | `output` | Final workflow output |
| Preview | `preview` | Preview media with playback controls |

### Cloud-Only Nodes (EXCLUDED from OSS)

| Node | Type | Reason |
|------|------|--------|
| Social Publish | `socialPublish` | Requires OAuth integrations for 7 platforms |
| RSS Input | `rssInput` | Content aggregation is Cloud feature |
| Tweet Input | `tweetInput` | Twitter API dependency, feed feature |
| Tweet Remix | `tweetRemix` | Depends on tweet input, social-focused |

### Cloud-Only Providers (EXCLUDED from OSS)

| Provider | Reason |
|----------|--------|
| FAL.ai | Cloud-only provider |
| HuggingFace | Cloud-only provider |

**OSS Provider:** Replicate only

## Validation Rules

### Rule 1: Node Type Check

```
IF node.type IN [socialPublish, rssInput, tweetInput, tweetRemix]
THEN FAIL: "Node type '{node.type}' is Cloud-only. Use OSS alternatives or upgrade to Cloud."
```

### Rule 2: Provider Check

```
IF node.provider IN [fal, huggingface]
THEN FAIL: "Provider '{node.provider}' is Cloud-only. OSS only supports Replicate."
```

### Rule 3: Template Check

```
IF template contains Cloud-only nodes
THEN FAIL: "Template uses Cloud-only nodes. Remove: {cloud_nodes}"
```

### Rule 4: Feature Request Check

```
IF request mentions [publish, social, twitter, rss, feed, youtube upload]
THEN WARN: "Social publishing and feed features are Cloud-only."
```

## Validation Examples

### Valid OSS Workflow

```json
{
  "nodes": [
    { "type": "prompt" },
    { "type": "imageGen" },
    { "type": "videoGen" },
    { "type": "subtitle" },
    { "type": "output" }
  ]
}
```

✅ All nodes are within OSS scope.

### Invalid OSS Workflow

```json
{
  "nodes": [
    { "type": "rssInput" },
    { "type": "tweetRemix" },
    { "type": "socialPublish" }
  ]
}
```

❌ Contains Cloud-only nodes: `rssInput`, `tweetRemix`, `socialPublish`

## Response Templates

### When Cloud Feature Requested

```
The feature you're requesting ({feature}) is available in Genfeed Cloud.

OSS Core includes:
- 26 nodes for media generation and processing
- Replicate provider for AI models
- Visual workflow editor with queue-based execution
- Gallery asset management

For social publishing and content aggregation features,
consider upgrading to Genfeed Cloud: https://genfeed.ai/cloud
```

### When Suggesting Alternatives

```
Instead of {cloud_feature}, consider these OSS alternatives:

1. {alternative_1}
2. {alternative_2}

These achieve similar results within the OSS scope.
```

## Common Requests & Responses

### "Can I publish to YouTube?"

**Response:** Social publishing is Cloud-only. In OSS, use the `output` node to export your video, then manually upload to YouTube.

### "Can I fetch RSS feeds?"

**Response:** RSS/feed aggregation is Cloud-only. In OSS, use the `prompt` node with manually entered content, or the `template` node with predefined prompts.

### "Can I use FAL.ai models?"

**Response:** FAL.ai is Cloud-only. OSS uses Replicate provider. Check if the model you need is available on Replicate.

### "Can I remix tweets?"

**Response:** Tweet remix is Cloud-only. In OSS, use the `llm` node with a custom prompt to rewrite text in different tones.

## Integration

When validating:

1. **Parse the request** - Identify node types, providers, and features mentioned
2. **Check against scope** - Compare with OSS node list
3. **Report violations** - List all Cloud-only features found
4. **Suggest alternatives** - Provide OSS workarounds when possible
5. **Link to Cloud** - Mention upgrade path for full feature access

## Quick Reference

```
OSS Node Types (26):
  Input:      imageInput, audioInput, videoInput, prompt, template
  AI:         imageGen, videoGen, llm, lipSync, voiceChange, textToSpeech, transcribe
  Processing: resize, animation, videoStitch, videoTrim, videoFrameExtract,
              lumaReframeImage, lumaReframeVideo, topazImageUpscale,
              topazVideoUpscale, imageGridSplit, annotation, subtitle
  Output:     output, preview

Cloud-Only (4):
  socialPublish, rssInput, tweetInput, tweetRemix

OSS Provider:
  replicate (only)

Cloud Providers:
  fal, huggingface
```
