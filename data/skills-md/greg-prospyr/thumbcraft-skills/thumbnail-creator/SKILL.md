---
name: thumbnail-creator
description: Generate AI-powered YouTube thumbnails, analyze videos for thumbnail ideas, manage styles/faces/brands, and create SEO-optimized titles and descriptions. Use when users want to create thumbnails, need thumbnail ideas for a video, want to clone a thumbnail style, or need YouTube SEO content.
triggers:
  - thumbnail
  - youtube thumbnail
  - create thumbnail
  - generate thumbnail
  - video thumbnail
  - thumbnail ideas
  - analyze video
  - thumbnail style
  - SEO titles
  - video description
  - click-worthy
---

# Thumbnail Creator

Generate professional YouTube thumbnails using AI. This skill connects to the Thumbnail Creator API to create thumbnails, analyze videos, manage creative assets, and generate SEO content.

## Setup

Before using this skill, ensure you have:
1. A Thumbnail Creator account at https://app.thumbcraft.io
2. An API key from Settings → Developers → API Keys

### MCP Configuration (Recommended)

Add to your Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "thumbnail-creator": {
      "url": "https://app.thumbcraft.io/api/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_API_KEY"
      }
    }
  }
}
```

### REST API

Base URL: `https://app.thumbcraft.io/api/v1`

All requests require the header:
```
Authorization: Bearer YOUR_API_KEY
```

## Available Tools

### Thumbnail Generation

#### `generate_thumbnail`
Create a thumbnail from a text description.

**Parameters:**
- `prompt` (required): Detailed description of the thumbnail
- `youtube_url` (optional): YouTube URL for context
- `style_id` (optional): Apply a saved style
- `face_ids` (optional): Array of face IDs to include
- `brand_id` (optional): Brand ID for colors/logo
- `aspect_ratio` (optional): "16:9" (default) or "9:16"

**Best practices for prompts:**
- Be specific about composition, colors, and emotions
- Mention text overlays explicitly if needed
- Describe the main subject's expression and pose
- Include background details

**Example:**
```
Generate a thumbnail with a surprised man looking at a giant golden trophy.
Bold yellow text says "I WON". Dark gradient background with sparkles.
Photorealistic style, dramatic lighting.
```

#### `analyze_video`
Analyze a YouTube video and get 5 thumbnail concepts with prompts.

**Parameters:**
- `youtube_url` (required): Full YouTube URL

**Returns:** Video summary and 5 thumbnail concepts with:
- Title and description
- Ready-to-use generation prompt
- Emotional hook explanation

### Asset Management

#### `list_faces`
Get uploaded face models for personalized thumbnails.

**Parameters:**
- `active_only` (optional): Only return trained faces

#### `create_face`
Create a new face from an image URL. Requires training before use.

**Parameters:**
- `name` (required): Display name
- `image_url` (required): Clear face photo URL

#### `list_styles`
Get saved thumbnail styles to apply to generations.

#### `list_brands`
Get brand assets (logos, colors) for consistent branding.

#### `list_thumbnails`
Get recent generated thumbnails.

**Parameters:**
- `limit` (optional): Number to return (default: 10)

### SEO Tools

#### `generate_seo_titles`
Generate 10 SEO-optimized video titles from a YouTube URL.

**Parameters:**
- `youtube_url` (required): YouTube video URL

**Returns:** 10 titles with style labels:
- Search-Driven (keyword-focused)
- Curiosity/Viral (click-driving)
- Authority/Expertise (trust-building)
- Emotional/Story (connection)
- Contrarian/Controversial (attention-grabbing)

#### `generate_seo_description`
Generate a complete video description.

**Parameters:**
- `youtube_url` (required): YouTube video URL

**Returns structured description with:**
- Hook (2 engaging sentences)
- About This Video (150-200 word summary)
- Key Takeaways (3-5 bullet points)
- Timestamps/Chapters (6-10 sections)
- Notable Quotes (1-2)
- SEO Hashtags (3-5)

#### `get_credits`
Check remaining credit balance.

## Workflows

### Generate Thumbnail from YouTube Video

1. Call `analyze_video` with the YouTube URL
2. Present the 5 concepts to the user
3. Let user pick a concept or provide feedback
4. Call `generate_thumbnail` with the chosen concept's prompt
5. Optionally apply a style or include faces

### Create Thumbnails with Consistent Style

1. Call `list_styles` to show available styles
2. Let user pick a style or describe a new one
3. Call `generate_thumbnail` with `style_id` parameter

### Full YouTube Optimization

1. Call `analyze_video` for thumbnail concepts
2. Generate thumbnail with `generate_thumbnail`
3. Call `generate_seo_titles` for title options
4. Call `generate_seo_description` for the description
5. Present complete package: thumbnail + title + description

## Tips for Best Results

### Thumbnail Prompts
- **Be specific**: "A woman with wide eyes and open mouth" > "surprised person"
- **Describe lighting**: "dramatic side lighting", "soft natural light"
- **Mention style**: "photorealistic", "3D rendered", "illustrated"
- **Include text carefully**: Specify exact text, font style, and placement
- **Consider contrast**: High contrast between subject and background

### Using Faces
- Faces must be trained before use (check `trainingStatus`)
- Use `face_ids` array to include multiple people
- The AI will match the face to the described expression

### Using Styles
- Styles capture visual aesthetics from reference images
- Great for maintaining channel consistency
- Combine with custom prompts for unique results

## Error Handling

Common errors:
- `401 Unauthorized`: Check API key
- `402 Payment Required`: Out of credits
- `429 Too Many Requests`: Rate limited, wait and retry
- `Invalid YouTube URL`: Ensure full URL format

## Credits

Operations that consume credits:
- `generate_thumbnail`: 1 credit
- All other operations: Free

Check balance with `get_credits` before generating.
