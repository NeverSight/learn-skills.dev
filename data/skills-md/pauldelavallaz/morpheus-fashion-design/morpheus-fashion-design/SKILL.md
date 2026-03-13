---
name: morpheus-fashion-design
description: Generate professional fashion/product advertising images using ComfyDeploy's Morpheus Fashion Design workflow. Use when the user asks to create fashion ads, product campaigns, commercial photography with models, or branded content. Supports model face consistency, product integration, and professional camera/lighting simulation.
---

# Morpheus Fashion Design

Generate professional fashion/product advertising images using ComfyDeploy's Morpheus Fashion Design workflow.

## ⚠️ CRITICAL RULE: NEVER USE AUTO VALUES

**Configuration packs MUST NEVER be left on `auto` or `AUTO`.**

`auto` = empty values = neutral, boring images with no creative direction.

The pack options listed below are **suggestions/ideas**, but you can send **custom values** that better fit the brief. The goal is to select the **best possible configuration** to represent the image needed for the brief.

### Pack Selection Guidelines

For EVERY generation, thoughtfully select values based on the creative brief:

| Pack | How to Choose |
|------|---------------|
| `style_pack` | Match brand personality: luxury→`premium_restraint`, sports→`cinematic_realism`, street→`street_authentic` |
| `camera_pack` | What camera would a real photographer use? Sports→`sony_a1`, editorial→`hasselblad_x2d`, street→`leica_m6` |
| `lens_pack` | Portrait compression? Anamorphic? Wide? Match the shot type and mood |
| `lighting_pack` | What's described in the brief? Golden hour? Studio? Natural window? Choose accordingly |
| `pose_discipline_pack` | What's the model doing? Sport action→`sport_in_motion`, commercial→`commercial_front_facing` |
| `film_texture_pack` | Warm editorial→`kodak_portra_400`, cinematic→`kodak_vision3_500t`, clean digital→`digital_clean_no_emulation` |
| `environment_pack` | Match brief location: beach→`beach_minimal`, urban→`urban_glass_steel`, nature→provide location_ref image |
| `color_science_pack` | Warm tones? Cool? Cinematic contrast? Select based on mood |
| `time_weather_pack` | When does the scene happen? Golden hour? Midday? Overcast? |

### Example: Oakley Snowboarding Campaign
```python
style_pack = "cinematic_realism"  # NOT auto - sports action needs energy
camera_pack = "sony_a1"            # Fast sports camera
lens_pack = "wide_distortion_controlled"  # Capture the action
lighting_pack = "golden_hour_backlit"     # Alpine dramatic lighting
pose_discipline_pack = "sport_in_motion"  # Rider in action
time_weather_pack = "golden_hour_clear"   # Mountain conditions
```

### Custom Values
If none of the preset options fit, you can write your own value as a descriptive string:
```python
lighting_pack = "harsh alpine midday sun reflecting off fresh powder"
environment_pack = "snowpark with metal rails and pristine packed snow"
```

## Overview

Morpheus Fashion Design is a comprehensive AI workflow for creating high-quality commercial photography with:
- Product integration
- Model face consistency
- Professional lighting and camera settings
- Brand-aligned creative direction

## API Details

**Endpoint:** `https://api.comfydeploy.com/api/run/deployment/queue`
**Deployment ID:** `1e16994d-da67-4f30-9ade-250f964b2abc` (production)

## Required Inputs

### Images (must be URLs)
1. **product** - Product image URL (the item being advertised)
2. **model** - Model face reference (frontal face photo)
3. **logo** - Brand logo (optional, use placeholder if not needed)

## 🎭 Model Catalog

A curated catalog of 114 AI-generated model references is available for use when no specific model is provided.

### Repository
**GitHub:** `https://github.com/PauldeLavallaz/model_management`

### ⚠️ PRIORITY: User-provided model ALWAYS wins
If the user attaches/provides a model image → use that image directly. The catalog is ONLY for when no model is specified.

### Setup (First Time Installation)
```bash
# Clone the catalog to your workspace
git clone https://github.com/PauldeLavallaz/model_management.git models-catalog
```

### Update Catalog
```bash
cd models-catalog && git pull
```

### Local Path (if already cloned)
`~/clawd/models-catalog/catalog/images/`

### Catalog Structure
```
models-catalog/
└── catalog/
    ├── catalog.json      # Full metadata for all models
    └── images/           # Model reference photos (model_01.jpg - model_114.jpg)
```

### Using the Catalog

**Priority order for model selection:**
1. **User provides model image** → Use that image directly
2. **User describes desired model** → Search catalog and select best match
3. **No specification** → Select appropriate model based on campaign brief

### Searching the Catalog
```bash
# List all models with basic info
cat models-catalog/catalog/catalog.json | jq '[.talents[] | {id, name, gender, ethnicity, tags: .tags[0:2]}]'

# Find models by ethnicity
cat models-catalog/catalog/catalog.json | jq '[.talents[] | select(.ethnicity == "hispanic") | {id, name, description}]'

# Find models by tag
cat models-catalog/catalog/catalog.json | jq '[.talents[] | select(.tags[] == "commercial") | {id, name, ethnicity}]'

# Find models by gender
cat models-catalog/catalog/catalog.json | jq '[.talents[] | select(.gender == "male") | {id, name, ethnicity}]'
```

### Model Attributes
Each model entry includes:
- `id`: Unique identifier (model_01, model_02, etc.)
- `name`: Model name
- `gender`: female, male, non-binary
- `ethnicity`: african, asian, caucasian, hispanic, mixed, etc.
- `age_group`: young_adult, adult, mature
- `tags`: editorial, commercial, beauty, lifestyle, avant-garde, etc.
- `description`: Detailed description of look and best uses
- `image_path`: Path to reference image

### Example: Selecting a Model
```bash
# For an Argentine campo/gaucho campaign, find hispanic females with commercial tags:
cat models-catalog/catalog/catalog.json | jq '[.talents[] | select(.ethnicity == "hispanic" and .gender == "female" and (.tags[] == "commercial" or .tags[] == "lifestyle")) | {id, name, description}]'

# Then use the selected model:
--model "models-catalog/catalog/images/model_08.jpg"
```

### Creative Brief
1. **brief** - Detailed campaign description including:
   - Scene/location description
   - Model pose and action
   - Product placement and interaction
   - Lighting and mood
   - Camera technique
   - Visual style

2. **target** - Target audience description including:
   - Demographics
   - Psychographics
   - Interests and lifestyle

### Configuration Packs

| Pack | Options |
|------|---------|
| `style_pack` | auto, premium_restraint, editorial_precision, cinematic_realism, cinematic_memory, campaign_hero, product_truth, clean_commercial, street_authentic, archive_fashion, experimental_authorial |
| `shot_pack` | auto, full_body_wide, medium_shot, close_up, low_angle_hero, three_quarter, waist_up, etc. |
| `camera_pack` | auto, arri_alexa35, canon_r5, hasselblad_x2d, leica_m6, sony_a1, etc. |
| `lens_pack` | auto, cooke_anamorphic_i_50, leica_noctilux_50, zeiss_otus_55, etc. |
| `lighting_pack` | auto, golden_hour_backlit, natural_window, studio_three_point, etc. |
| `pose_discipline_pack` | auto, commercial_front_facing, street_style_candid_walk, sport_in_motion, etc. |
| `film_texture_pack` | auto, kodak_portra_400, fujifilm_velvia_50, digital_clean_no_emulation, etc. |
| `color_science_pack` | auto, neutral_premium_clean, warm_golden_editorial, cinematic_low_contrast, etc. |
| `environment_pack` | AUTO, beach_minimal, urban_glass_steel, street_crosswalk, etc. |
| `time_weather_pack` | auto, golden_hour_clear, bright_midday_sun, overcast_winter_daylight, etc. |
| `branding_pack` | logo_none, logo_discreet_lower, logo_top_corner, logo_center_watermark, logo_integrated |
| `intent` | auto, awareness, consideration, conversion, retention |
| `aspect_ratio` | 9:16, 16:9, 1:1, 4:5, 5:4, 3:4, 4:3 |

## Workflow Process

1. **Receive request** with brand/product info
2. **Design brief** aligned with brand identity and campaign goals
3. **Define target audience** with demographics and psychographics
4. **Prepare images**:
   - Download product image(s)
   - Download/find model reference (frontal face)
   - Upload to ComfyDeploy storage to get URLs
5. **Select packs** based on creative direction
6. **Submit job** and poll for completion
7. **Deliver results**

## Usage

```bash
uv run ~/.clawdbot/skills/morpheus-fashion-design/scripts/generate.py \
  --product "path/to/product.jpg" \
  --model "path/to/model-face.jpg" \
  --brief "Campaign brief text..." \
  --target "Target audience description..." \
  --aspect-ratio "4:5" \
  --style-pack "street_authentic" \
  --output "output-filename.png"
```

## Example Brief (Franuí Carnaval)

```
La campaña Franuí Carnaval captura el espíritu festivo y la alegría del carnaval brasileño 
en Copacabana. Una mujer afrobrasileña baila en medio de la multitud, sosteniendo el 
producto Franuí Milk hacia la cámara en un gesto espontáneo y celebratorio. La escena 
está llena de confeti, movimiento y energía. La fotografía adopta un estilo documental 
con motion blur intencional, ángulo bajo que empodera al sujeto, y el producto como 
elemento hero en primer plano. La luz es natural de día tropical, cálida y vibrante.
```

## Example Target (Franuí Carnaval)

```
Jóvenes adultos 18-35, principalmente mujeres pero inclusivo, que celebran la vida, 
la música y los momentos compartidos. Consumidores de experiencias premium que buscan 
productos que se integren naturalmente a sus momentos de disfrute. Activos en redes 
sociales, valoran la autenticidad y la conexión cultural. Mercado: Brasil y LATAM.
```

## Important Notes

### Studio Override
The workflow has an automatic `studio_override` that activates when no location reference is provided. This will use a white cyclorama background regardless of the brief description.

**To get environmental backgrounds:**
1. Provide a `location_ref` image, OR
2. Set `environment_pack` to a specific environment (e.g., `beach_minimal`, `street_crosswalk`)

### Priority Hierarchy
The system follows this priority:
1. Talent (identity preservation) > 
2. Garments (product fidelity) > 
3. Fit > Pose > Style > Location > Branding

## API Key

**DO NOT pass the API key via parameter.** Leave it empty.

The API key is already configured in ComfyDeploy. Passing `--api-key` will cause authentication errors.

## Troubleshooting

### Imagen negra o vacía
Si la imagen generada sale completamente negra o vacía, es el **filtro de moderación de Google/Gemini**. Causas comunes:
- Se pidió una persona famosa o celebridad
- Contenido considerado sensible por el modelo
- La combinación de prompt + imágenes fue rechazada por políticas de contenido

**Solución:** Modificar el prompt para evitar referencias a personas reales/famosas, o cambiar elementos que puedan activar el filtro.
