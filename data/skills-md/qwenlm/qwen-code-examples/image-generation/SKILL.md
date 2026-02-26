---
name: image-generation
description: Image generation skill based on Alibaba Cloud DashScope, supporting the creation of high-quality hand-drawn or standard images from user descriptions.
version: 1.0.0
license: MIT
---

# Image Generation Skill

This skill allows agents to automatically generate high-quality images (defaulting to hand-drawn style) based on user intent.

## Core Features

- **Smart Prompt Optimization**: Transforms simple user intent into detailed hand-drawn style prompts.
- **Fast Generation**: Uses non-streaming interfaces to significantly speed up image generation.
- **Auto-Save**: Automatically downloads generated images locally and saves metadata and API responses simultaneously.

## Prerequisites

Before using this skill, ensure that the `DASHSCOPE_API_KEY` environment variable is set:

```bash
export DASHSCOPE_API_KEY="Your API Key"
```

## User Guide

### 1. Refine the Prompt

You need to refine the user's original intent into a prompt suitable for image generation. For hand-drawn versions of architecture or flowcharts, it's recommended to include keywords like "hand-drawn", "sketch", "architectural drawing", etc.

### 2. Run the Script

Use the following command to call the generation script:

```bash
node skills/image-generate/scripts/generate_image.js "Your detailed prompt"
```

### 3. View Results

After the script completes, it will generate the following files in the current directory:

- `image_YYYY-MM-DDTHH-mm-ss.png`: The generated image file.
- `metadata_YYYY-MM-DDTHH-mm-ss.json`: Metadata including prompt, file size, and duration.
- `response_YYYY-MM-DDTHH-mm-ss.json`: Raw API response data (for debugging).

## Example

**User Intent**: "Help me draw an architecture diagram of an AI coding assistant."

**Recommended Prompt**: "A detailed hand-drawn architectural diagram of an AI coding assistant, showing the interaction between the user, the IDE, and the LLM, technical sketch style, clean lines, white background."

**Execution Command**:

```bash
node skills/image-generate/scripts/generate_image.js "A detailed hand-drawn architectural diagram of an AI coding assistant, showing the interaction between the user, the IDE, and the LLM, technical sketch style, clean lines, white background."
```
