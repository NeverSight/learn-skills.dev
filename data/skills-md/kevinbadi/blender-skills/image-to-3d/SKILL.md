---
name: image-to-3d
description: Convert a photo into a 3D model using Meshy API and import it into Blender via MCP.
---

## Image to 3D Blender Skill

Converts a user-provided photo into a textured 3D model using the Meshy AI API, then imports it into the active Blender scene.

## When to Use

Trigger this skill when:
- User wants to turn a photo/image into a 3D model
- User says "make this 3D", "convert to 3D", "3D model from image"
- User provides an image and wants it in Blender as a 3D object

## Prerequisites

- **Meshy API Key**: Stored in environment variable `MESHY_API_KEY` or passed directly
- **Blender MCP**: Must be connected (blender-mcp addon running on port 9876)
- **Image**: Local file path (.jpg, .jpeg, .png) or publicly accessible URL

## Flow

### Step 1: Prepare the Image

If the user provides a local file path, base64 encode it:

```bash
BASE64_IMAGE=$(base64 -i "<image_path>")
DATA_URI="data:image/png;base64,${BASE64_IMAGE}"
```

### Step 2: Create Image-to-3D Task

```bash
curl -s https://api.meshy.ai/openapi/v1/image-to-3d \
  -X POST \
  -H "Authorization: Bearer ${MESHY_API_KEY}" \
  -H 'Content-Type: application/json' \
  -d '{
    "image_url": "<data_uri_or_public_url>",
    "ai_model": "meshy-6",
    "enable_pbr": true,
    "should_remesh": true,
    "should_texture": true,
    "topology": "quad",
    "target_polycount": 30000,
    "target_formats": ["glb"]
  }'
```

Response gives a task ID: `{"result": "<task_id>"}`

### Step 3: Poll for Completion

```bash
curl -s https://api.meshy.ai/openapi/v1/image-to-3d/<task_id> \
  -H "Authorization: Bearer ${MESHY_API_KEY}"
```

Poll every 10 seconds. Check `status` field:
- `PENDING` — queued
- `IN_PROGRESS` — generating (check `progress` field for %)
- `SUCCEEDED` — done, `model_urls.glb` has the download URL
- `FAILED` — check `task_error.message`

### Step 4: Download the GLB

```bash
curl -L -o "/Users/kevinbahrabadi/Blender Test/output/<filename>.glb" "<model_urls.glb>"
```

### Step 5: Import into Blender

Use the Blender MCP `execute_blender_code` tool:

```python
import bpy

# Clear scene (optional, based on user preference)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Import GLB
bpy.ops.import_scene.gltf(filepath="/Users/kevinbahrabadi/Blender Test/output/<filename>.glb")

# Center and frame the imported object
bpy.ops.object.select_all(action='SELECT')
bpy.ops.view3d.view_selected()
```

## Configuration Options

| Option | Default | Description |
|--------|---------|-------------|
| `ai_model` | `meshy-6` | Model to use. Options: `meshy-5`, `meshy-6`, `latest` |
| `model_type` | `standard` | `standard` for detail, `lowpoly` for clean game meshes |
| `topology` | `triangle` | `quad` or `triangle` mesh |
| `target_polycount` | `30000` | 100–300,000 polygons |
| `enable_pbr` | `true` | Generate metallic/roughness/normal maps |
| `symmetry_mode` | `auto` | `off`, `auto`, or `on` |
| `pose_mode` | `""` | `a-pose`, `t-pose`, or empty |
| `should_texture` | `true` | Generate textures (costs extra credits) |
| `remove_lighting` | `true` | Clean textures without baked lighting |

## Output

After completion, the user gets:
- 3D model imported into Blender scene
- Textured with PBR materials (if enabled)
- Ready for rendering, animation, or further editing

## Error Handling

- **402**: Insufficient Meshy credits — inform user
- **429**: Rate limited — wait and retry
- **FAILED status**: Report `task_error.message` to user
- **Blender MCP disconnected**: Ask user to reconnect addon
