---
name: modelslab-interior-design
description: Transform and redesign interior spaces using ModelsLab's Interior API. Generate interior designs, decorate rooms, create floor plans, and restore exteriors with AI.
---

# ModelsLab Interior Design

AI-powered interior design, room decoration, floor planning, and exterior restoration.

## When to Use This Skill

- Redesign interior spaces
- Decorate rooms with AI assistance
- Generate floor plans from images
- Transform room styles and aesthetics
- Restore or enhance building exteriors
- Create design mockups and variations
- Visualize renovation ideas

## Available Endpoints

### Interior Design
`POST https://modelslab.com/api/v6/interior/interior`

### Room Decorator
`POST https://modelslab.com/api/v6/interior/room_decorator`

### Floor Planning
`POST https://modelslab.com/api/v6/interior/floor_planning`

### Exterior Restorer
`POST https://modelslab.com/api/v6/interior/exterior_restorer`

### Scenario Changer
`POST https://modelslab.com/api/v6/interior/scenario_changer`

### Object Removal
`POST https://modelslab.com/api/v6/interior/object_removal`

### Interior Mixer
`POST https://modelslab.com/api/v6/interior/interior_mixer`

## Interior Redesign

```python
import requests

def redesign_interior(room_image, design_prompt, api_key):
    """Redesign an interior space based on a prompt.

    Args:
        room_image: URL of the room photo
        design_prompt: Description of desired design
        api_key: Your ModelsLab API key

    Returns:
        URL of the redesigned interior
    """
    response = requests.post(
        "https://modelslab.com/api/v6/interior/interior",
        json={
            "key": api_key,
            "init_image": room_image,
            "prompt": design_prompt,
            "negative_prompt": "low quality, distorted, unrealistic",
            "num_inference_steps": 31,  # 21, 31, or 41
            "guidance_scale": 7.5,
            "strength": 0.7
        }
    )

    data = response.json()

    if data["status"] == "success":
        return data["output"][0]
    else:
        raise Exception(f"Error: {data.get('message', 'Unknown error')}")

# Usage
redesigned = redesign_interior(
    "https://example.com/living-room.jpg",
    "Modern minimalist living room with Scandinavian furniture, white walls, natural light",
    "your_api_key"
)
print(f"Redesigned room: {redesigned}")
```

## Room Decorator

```python
def decorate_room(room_image, decor_prompt, api_key, specific_object=None):
    """Decorate a room with AI-generated furniture and decor.

    Args:
        room_image: URL of the empty or basic room
        decor_prompt: Description of desired decoration
        specific_object: Specific furniture/decor item that must appear
    """
    payload = {
        "key": api_key,
        "init_image": room_image,
        "prompt": decor_prompt,
        "negative_prompt": "cluttered, low quality, distorted",
        "num_inference_steps": 31,
        "guidance_scale": 7.5,
        "strength": 0.8
    }

    if specific_object:
        payload["specific_object"] = specific_object

    response = requests.post(
        "https://modelslab.com/api/v6/interior/room_decorator",
        json=payload
    )

    data = response.json()

    if data["status"] == "success":
        return data["output"][0]
    else:
        raise Exception(data.get("message"))

# Decorate empty room
decorated = decorate_room(
    "https://example.com/empty-room.jpg",
    "Cozy bedroom with warm lighting, plants, wooden furniture",
    "your_api_key",
    specific_object="king size bed"
)
print(f"Decorated room: {decorated}")
```

## Floor Planning

```python
def generate_floor_plan(room_image, api_key):
    """Generate a floor plan from a room image.

    Args:
        room_image: URL of room photo
        api_key: Your API key

    Returns:
        URL of the generated floor plan
    """
    response = requests.post(
        "https://modelslab.com/api/v6/interior/floor_planning",
        json={
            "key": api_key,
            "init_image": room_image
        }
    )

    data = response.json()

    if data["status"] == "success":
        return data["output"][0]
    else:
        raise Exception(data.get("message"))

# Generate floor plan
floor_plan = generate_floor_plan(
    "https://example.com/room-photo.jpg",
    "your_api_key"
)
print(f"Floor plan: {floor_plan}")
```

## Exterior Restoration

```python
def restore_exterior(building_image, restoration_prompt, api_key):
    """Restore or enhance building exterior.

    Args:
        building_image: URL of building exterior photo
        restoration_prompt: Description of desired restoration
    """
    response = requests.post(
        "https://modelslab.com/api/v6/interior/exterior_restorer",
        json={
            "key": api_key,
            "init_image": building_image,
            "prompt": restoration_prompt,
            "negative_prompt": "damaged, old, worn",
            "num_inference_steps": 31,
            "guidance_scale": 7.5
        }
    )

    data = response.json()

    if data["status"] == "success":
        return data["output"][0]
    else:
        raise Exception(data.get("message"))

# Restore old building
restored = restore_exterior(
    "https://example.com/old-building.jpg",
    "Restored Victorian house with fresh paint, new windows, landscaped garden",
    "your_api_key"
)
```

## Scenario Changer

```python
def change_room_scenario(room_image, new_scenario, api_key):
    """Change the environment scenario of a room.

    Args:
        room_image: URL of room photo
        new_scenario: Description of new scenario/ambiance
    """
    response = requests.post(
        "https://modelslab.com/api/v6/interior/scenario_changer",
        json={
            "key": api_key,
            "init_image": room_image,
            "prompt": new_scenario,
            "num_inference_steps": 31,
            "guidance_scale": 7.5
        }
    )

    data = response.json()

    if data["status"] == "success":
        return data["output"][0]
    else:
        raise Exception(data.get("message"))

# Change from day to evening
evening_room = change_room_scenario(
    "https://example.com/daytime-room.jpg",
    "Evening ambiance with warm lamp lighting, cozy atmosphere",
    "your_api_key"
)
```

## Object Removal

```python
def remove_interior_object(room_image, object_to_remove, api_key):
    """Remove an object from an interior image.

    Args:
        room_image: URL of room photo
        object_to_remove: Description of object to remove
    """
    response = requests.post(
        "https://modelslab.com/api/v6/interior/object_removal",
        json={
            "key": api_key,
            "init_image": room_image,
            "object_name": object_to_remove
        }
    )

    data = response.json()

    if data["status"] == "success":
        return data["output"][0]
    else:
        raise Exception(data.get("message"))

# Remove furniture
cleaned = remove_interior_object(
    "https://example.com/cluttered-room.jpg",
    "old sofa",
    "your_api_key"
)
```

## Interior Mixer

```python
def mix_interior_objects(room_image, object_image, placement_prompt, api_key):
    """Add objects from one image into another room.

    Args:
        room_image: URL of the target room
        object_image: URL of image containing object to add
        placement_prompt: Description of how to place the object
    """
    response = requests.post(
        "https://modelslab.com/api/v6/interior/interior_mixer",
        json={
            "key": api_key,
            "init_image": room_image,
            "object_image": object_image,
            "prompt": placement_prompt,
            "width": 512,
            "height": 512,
            "num_inference_steps": 8,
            "guidance_scale": 7.5
        }
    )

    data = response.json()

    if data["status"] == "success":
        return data["output"][0]
    else:
        raise Exception(data.get("message"))

# Add furniture from another image
mixed = mix_interior_objects(
    "https://example.com/empty-room.jpg",
    "https://example.com/furniture.jpg",
    "Place the chair in the corner near the window",
    "your_api_key"
)
```

## Key Parameters

| Parameter | Description | Values |
|-----------|-------------|--------|
| `init_image` | Room/building image | Image URL |
| `prompt` | Design description | Detailed text |
| `negative_prompt` | What to avoid | "cluttered, low quality" |
| `strength` | Transformation strength | 0.0-1.0 (0.7 typical) |
| `num_inference_steps` | Quality level | 21, 31, or 41 |
| `guidance_scale` | Prompt adherence | 1-20 (7.5 typical) |
| `specific_object` | Required item | Object name |
| `object_name` | Object to remove | Description |

## Best Practices

### 1. Write Detailed Design Prompts
```
✗ Bad: "modern room"
✓ Good: "Modern minimalist living room with Scandinavian furniture, white walls, oak floor, large windows, indoor plants"

Include: Style, furniture, colors, lighting, materials, atmosphere
```

### 2. Use Appropriate Strength Values
```python
# Subtle changes
strength = 0.5

# Moderate redesign
strength = 0.7

# Complete transformation
strength = 0.9
```

### 3. Quality vs Speed
```python
# Fast (21 steps)
num_inference_steps = 21

# Balanced (31 steps) - Recommended
num_inference_steps = 31

# Best quality (41 steps)
num_inference_steps = 41
```

### 4. Use High-Quality Input Images
- Well-lit room photos
- Clear view of the space
- Minimal distortion
- High resolution preferred

## Common Use Cases

### Virtual Staging

```python
def stage_empty_room(room_image, style, api_key):
    """Stage an empty room for real estate listing."""
    return decorate_room(
        room_image,
        f"{style} furnished room with modern furniture, well-lit, professional",
        api_key
    )

# Stage for listing
staged = stage_empty_room(
    "https://example.com/empty-apartment.jpg",
    "Modern luxury",
    api_key
)
```

### Design Variations

```python
def create_design_variations(room_image, styles, api_key):
    """Generate multiple design style variations."""
    variations = []

    for style in styles:
        variant = redesign_interior(
            room_image,
            f"{style} interior design style",
            api_key
        )
        variations.append(variant)
        print(f"{style}: {variant}")

    return variations

# Generate variations
designs = create_design_variations(
    "https://example.com/room.jpg",
    ["Modern Scandinavian", "Industrial Loft", "Classic Traditional", "Bohemian"],
    api_key
)
```

### Renovation Planning

```python
def plan_renovation(current_room, desired_style, api_key):
    """Plan room renovation with before/after."""
    before = current_room

    after = redesign_interior(
        before,
        f"Renovated {desired_style} room with updated fixtures and furniture",
        api_key
    )

    return {"before": before, "after": after}

# Plan kitchen renovation
plan = plan_renovation(
    "https://example.com/old-kitchen.jpg",
    "modern farmhouse kitchen",
    api_key
)
```

### Complete Room Makeover

```python
def complete_room_makeover(room_image, api_key):
    """Full room transformation workflow."""

    # Step 1: Remove unwanted items
    cleaned = remove_interior_object(
        room_image,
        "old furniture and clutter",
        api_key
    )

    # Step 2: Redesign space
    redesigned = redesign_interior(
        cleaned,
        "Modern minimalist interior with natural materials",
        api_key
    )

    # Step 3: Add specific decor
    final = decorate_room(
        redesigned,
        "Add cozy lighting and indoor plants",
        api_key,
        specific_object="pendant lamp"
    )

    return final
```

### Before/After Scenarios

```python
# Day to night transformation
day_room = "https://example.com/daytime.jpg"

night = change_room_scenario(
    day_room,
    "Evening ambiance with warm lighting, twilight outside windows",
    api_key
)

# Summer to winter
winter = change_room_scenario(
    day_room,
    "Winter scene with snow outside, cozy fireplace, warm interior",
    api_key
)
```

## Error Handling

```python
try:
    design = redesign_interior(room_image, prompt, api_key)
    print(f"Design created: {design}")
except Exception as e:
    print(f"Design generation failed: {e}")
    # Log error, try different prompt, notify user
```

## Performance Tips

1. **Use Appropriate Inference Steps**: 31 steps balances quality and speed
2. **Optimize Prompts**: Clear, detailed prompts work best
3. **Batch Similar Requests**: Generate multiple variations together
4. **Cache Results**: Store generated designs
5. **Monitor Quality**: Adjust strength and guidance_scale as needed

## Enterprise API

For dedicated resources:

```python
# Enterprise endpoints
url = "https://modelslab.com/api/v1/enterprise/interior/interior"
url = "https://modelslab.com/api/v1/enterprise/interior/room_decorator"
```

## Resources

- **Interior API Docs**: https://docs.modelslab.com/interior-api/overview
- **Interior Design**: https://docs.modelslab.com/interior-api/interior
- **Room Decorator**: https://docs.modelslab.com/interior-api/room-decorator
- **Floor Planning**: https://docs.modelslab.com/interior-api/floor-planning
- **Get API Key**: https://modelslab.com/dashboard

## Related Skills

- `modelslab-image-generation` - Generate room reference images
- `modelslab-image-editing` - Additional editing tools
- `modelslab-sdk-usage` - Use official SDKs
