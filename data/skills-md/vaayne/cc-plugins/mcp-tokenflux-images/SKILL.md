---
name: mcp-tokenflux-images
description: Generate images using AI models via TokenFlux API. Use when creating AI-generated images, artwork, or visual content. Triggers on "generate image", "create picture", "AI art", "image generation", "TokenFlux".
---

# TokenFlux Image Generation

MCP service at `https://tokenflux.ai/v1/images/mcp` (http) with 4 tools.

## Requirements

- `mh` CLI must be installed. If not available, install with:
  ```bash
  curl -fsSL https://raw.githubusercontent.com/vaayne/mcphub/main/scripts/install.sh | sh
  ```
- `TOKENFLUX_API_KEY` environment variable must be set with your TokenFlux API key

## Usage

List tools: `mh list -u https://tokenflux.ai/v1/images/mcp --header "Authorization:Bearer ${TOKENFLUX_API_KEY}"`

Get tool details: `mh inspect -u https://tokenflux.ai/v1/images/mcp --header "Authorization:Bearer ${TOKENFLUX_API_KEY}" <tool-name>`

Invoke tool: `mh invoke -u https://tokenflux.ai/v1/images/mcp --header "Authorization:Bearer ${TOKENFLUX_API_KEY}" <tool-name> '{"param": "value"}'`

## Workflow

1. **List models first**: Use `listModels` to discover available image generation models
2. **Get model schema**: Use `getModel` with the chosen model_id to get the required input_schema
3. **Generate image**: Use `generateImage` with the correct input format from the schema
4. **Poll if needed**: If generation returns `status: 'processing'`, use `getGeneration` to poll until complete

## Notes

- Run `inspect` before invoking unfamiliar tools to get full parameter schema
- Timeout: 30s default, use `--timeout <seconds>` to adjust
- `generateImage` waits up to 30 seconds; if still processing, poll with `getGeneration`
- Always call `getModel` before `generateImage` to understand the correct input format

## Tools

- **listModels**: List all available VLM models with their IDs, names, descriptions, and pricing. Use this first to discover valid model_id values for generate_image. This tool takes no parameters.
- **getModel**: Get detailed information about a specific VLM model including its input_schema. The input_schema is a JSON Schema describing the required input object for generate_image. Always call this before generate_image to understand the correct input format.
- **generateImage**: Generate an image using a VLM model. IMPORTANT: Call get_model first to get the input_schema for your model. This tool waits up to 30 seconds for completion. If the image is ready, returns {id, status: 'succeeded', images: [...]}. If still processing after 30s, returns {id, status: 'processing'} - use get_generation to poll.
- **getGeneration**: Get the status and result of an image generation request. Use the id returned by generate_image to poll until status is 'succeeded' or 'failed'. Returns {id, model, status, images?, error?, cost?}.
