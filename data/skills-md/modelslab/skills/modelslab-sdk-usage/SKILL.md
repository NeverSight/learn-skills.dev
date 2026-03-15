---
name: modelslab-sdk-usage
description: Use ModelsLab's official SDKs (Python, TypeScript, PHP, Go, Dart) for easier integration with type safety, better error handling, and cleaner code.
---

# ModelsLab SDK Usage

Official SDKs for Python, TypeScript/JavaScript, PHP, Go, and Dart with type safety and better developer experience.

## When to Use SDKs

- Want type safety and autocomplete
- Prefer object-oriented interfaces
- Need better error handling
- Building production applications
- Want cleaner, more maintainable code
- Working in typed languages

## Available SDKs

### Python
```bash
pip install modelslab-py
```

### TypeScript/JavaScript
```bash
npm install modelslab
# or
yarn add modelslab
```

### PHP
```bash
composer require modelslab/modelslab-php
```

### Go
```bash
go get github.com/modelslab/modelslab-go
```

### Dart/Flutter
```bash
dart pub add modelslab
# or add to pubspec.yaml
```

## Python SDK

### Installation & Setup

```python
from modelslab_py.core.client import Client
from modelslab_py.core.apis.realtime import Realtime
from modelslab_py.schemas.realtime import Text2ImageSchema

# Initialize client
client = Client(api_key="your_api_key")

# Create API instance
realtime_api = Realtime(client=client, enterprise=False)
```

### Image Generation

```python
from modelslab_py.core.apis.community import Community
from modelslab_py.schemas.community import Text2ImageSchema

# Community models
community_api = Community(client=client, enterprise=False)

schema = Text2ImageSchema(
    model_id="midjourney",
    prompt="A futuristic cityscape at sunset, cyberpunk style",
    negative_prompt="blurry, low quality",
    width=768,
    height=768,
    samples=1,
    num_inference_steps=30,
    guidance_scale=7.5,
    safety_checker="yes"
)

response = community_api.text_to_image(schema)
print(f"Image URL: {response['output'][0]}")
```

### Video Generation

```python
from modelslab_py.core.apis.video import Video
from modelslab_py.schemas.video import Text2Video

video_api = Video(client=client, enterprise=False)

schema = Text2Video(
    model_id="cogvideox",
    prompt="A spaceship flying through space",
    width=512,
    height=512,
    num_frames=25,
    num_inference_steps=20
)

response = video_api.text_to_video(schema)
print(f"Video: {response}")
```

### Audio Generation

```python
from modelslab_py.core.apis.audio import Audio
from modelslab_py.schemas.audio import Text2Speech

audio_api = Audio(client=client, enterprise=False)

schema = Text2Speech(
    text="Hello, welcome to ModelsLab!",
    voice_id="alloy",
    language="en"
)

response = audio_api.text_to_speech(schema)
print(f"Audio: {response['output'][0]}")
```

### Image Editing

```python
from modelslab_py.core.apis.image_editing import Image_editing
from modelslab_py.schemas.image_editing import (
    BackgroundRemoverSchema,
    SuperResolutionSchema
)

editing_api = Image_editing(client=client, enterprise=False)

# Remove background
bg_schema = BackgroundRemoverSchema(
    image="https://example.com/photo.jpg"
)
result = editing_api.background_remover(bg_schema)

# Upscale
upscale_schema = SuperResolutionSchema(
    image="https://example.com/image.jpg",
    scale=4
)
hd_image = editing_api.super_resolution(upscale_schema)
```

### 3D Generation

```python
from modelslab_py.core.apis.three_d import Three_D
from modelslab_py.schemas.threed import Text23D, Image23D

threed_api = Three_D(client=client, enterprise=False)

# Text to 3D
schema = Text23D(
    prompt="A medieval sword with ornate handle",
    num_inference_steps=50
)
response = threed_api.text_to_3d(schema)

# Image to 3D
img_schema = Image23D(
    image="https://example.com/product.jpg"
)
model = threed_api.image_to_3d(img_schema)
```

## TypeScript/JavaScript SDK

### Installation & Setup

```typescript
import { Client, Realtime, Community, Video } from "modelslab";

// Initialize client
const client = new Client("your_api_key");
```

### Image Generation

```typescript
import { Community } from "modelslab";

const community = new Community(client.key);

const result = await community.textToImage({
  key: client.key,
  model_id: "midjourney",
  prompt: "A futuristic cityscape",
  negative_prompt: "blurry, low quality",
  width: 768,
  height: 768,
  samples: 1,
  num_inference_steps: 30,
  guidance_scale: 7.5
});

console.log("Image:", result.output[0]);
```

### Video Generation

```typescript
import { Video } from "modelslab";

const video = new Video(client.key);

const result = await video.textToVideo({
  key: client.key,
  model_id: "cogvideox",
  prompt: "A spaceship flying through space",
  num_frames: 25,
  num_inference_steps: 20
});

console.log("Video:", result);
```

### Audio Generation

```typescript
import { Audio } from "modelslab";

const audio = new Audio(client.key);

const result = await audio.textToSpeech({
  key: client.key,
  text: "Hello, welcome to ModelsLab!",
  voice_id: "alloy",
  language: "en"
});

console.log("Audio:", result.output[0]);
```

### Deepfake

```typescript
import { DeepFake } from "modelslab";

const deepfake = new DeepFake(client.key);

const result = await deepfake.specificFaceSwap({
  key: client.key,
  init_image: "https://example.com/target.jpg",
  target_image: "https://example.com/face.jpg"
});

console.log("Face swap:", result.output[0]);
```

## PHP SDK

### Installation & Setup

```php
<?php
use ModelsLab\ModelsLab;
use ModelsLab\Schemas\Text2ImageSchema;

$modelslab = new ModelsLab('your-api-key');
```

### Image Generation

```php
<?php
use ModelsLab\Schemas\Text2ImageSchema;

$schema = new Text2ImageSchema([
    'model_id' => 'midjourney',
    'prompt' => 'A futuristic cityscape',
    'negative_prompt' => 'blurry, low quality',
    'width' => 768,
    'height' => 768,
    'num_inference_steps' => 30
]);

$response = $modelslab->community()->textToImage($schema);
echo "Image: " . $response['output'][0];
```

### Video Generation

```php
<?php
use ModelsLab\Schemas\Text2Video;

$video = new Text2Video([
    'prompt' => 'A spaceship flying through space',
    'model_id' => 'cogvideox',
    'num_frames' => 25
]);

$response = $modelslab->video()->textToVideo($video);
print_r($response);
```

### Audio Generation

```php
<?php
use ModelsLab\Schemas\Text2Speech;

$tts = new Text2Speech([
    'text' => 'Hello, welcome to ModelsLab!',
    'voice_id' => 'alloy',
    'language' => 'english'
]);

$response = $modelslab->audio()->textToSpeech($tts);
echo "Audio: " . $response['output'][0];
```

## Go SDK

### Installation & Setup

```go
package main

import (
    "context"
    "github.com/modelslab/modelslab-go/pkg/client"
    "github.com/modelslab/modelslab-go/pkg/apis/community"
    communitySchema "github.com/modelslab/modelslab-go/pkg/schemas/community"
)

func main() {
    c := client.New("your-api-key")
    communityAPI := community.New(c, false)
}
```

### Image Generation

```go
package main

import (
    "context"
    "encoding/json"
    "fmt"
    "github.com/modelslab/modelslab-go/pkg/apis/community"
    "github.com/modelslab/modelslab-go/pkg/client"
    communitySchema "github.com/modelslab/modelslab-go/pkg/schemas/community"
)

func main() {
    c := client.New("your-api-key")
    communityAPI := community.New(c, false)

    prompt := "A futuristic cityscape"
    negativePrompt := "blurry, low quality"
    width := 768
    height := 768

    req := communitySchema.Text2ImageRequest{
        ModelID: "midjourney",
        Prompt: &prompt,
        NegativePrompt: &negativePrompt,
        Width: &width,
        Height: &height,
    }

    resp, err := communityAPI.Text2Image(context.Background(), &req)
    if err != nil {
        panic(err)
    }

    prettyJSON, _ := json.MarshalIndent(resp, "", "  ")
    fmt.Println(string(prettyJSON))
}
```

### Video Generation

```go
package main

import (
    "context"
    "github.com/modelslab/modelslab-go/pkg/apis/video"
    "github.com/modelslab/modelslab-go/pkg/client"
    videoSchema "github.com/modelslab/modelslab-go/pkg/schemas/video"
)

func main() {
    c := client.New("your-api-key")
    videoAPI := video.New(c, false)

    req := videoSchema.Text2VideoRequest{
        Prompt: "A spaceship flying through space",
        ModelID: "cogvideox",
    }

    resp, err := videoAPI.TextToVideo(context.Background(), &req)
    if err != nil {
        panic(err)
    }
}
```

## Dart/Flutter SDK

### Installation & Setup

```dart
import 'package:modelslab/core/client.dart';
import 'package:modelslab/core/apis/community.dart';
import 'package:modelslab/schemas/community.dart';

var client = Client(key: "your_api_key");
var api = Community(client: client);
```

### Image Generation

```dart
import 'package:modelslab/core/apis/community.dart';
import 'package:modelslab/schemas/community.dart';

var schema = Text2ImageSchema(
  modelId: "midjourney",
  prompt: "A futuristic cityscape",
  negativePrompt: "blurry, low quality",
  width: 768,
  height: 768,
  numInferenceSteps: 30,
);

Future<Map<String, dynamic>> response = api.textToImage(schema);
```

### Video Generation

```dart
import 'package:modelslab/core/apis/video.dart';
import 'package:modelslab/schemas/video.dart';

var videoApi = Video(client: client);

var schema = Text2Video(
  prompt: "A spaceship flying through space",
  modelId: "cogvideox",
  numFrames: 25,
);

Future<Map<String, dynamic>> response = videoApi.textToVideo(schema);
```

## SDK Benefits

### 1. Type Safety
```typescript
// TypeScript autocomplete and type checking
const result = await community.textToImage({
  key: client.key,
  model_id: "midjourney",  // Autocompletes available models
  prompt: "...",           // Required field
  width: 768,              // Type checked (number)
});
```

### 2. Better Error Handling
```python
try:
    response = api.text_to_image(schema)
except ValidationError as e:
    print(f"Invalid parameters: {e}")
except APIError as e:
    print(f"API error: {e.status_code} - {e.message}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### 3. Cleaner Code
```python
# SDK - Clean and readable
schema = Text2ImageSchema(
    model_id="midjourney",
    prompt="A sunset",
    width=512,
    height=512
)
result = api.text_to_image(schema)

# vs Raw HTTP - More verbose
response = requests.post(
    "https://modelslab.com/api/v6/images/text2img",
    json={
        "key": api_key,
        "model_id": "midjourney",
        "prompt": "A sunset",
        "width": 512,
        "height": 512
    }
)
data = response.json()
```

### 4. Built-in Validation
```python
# SDK validates before API call
schema = Text2ImageSchema(
    width=513  # Not divisible by 8
)
# Raises ValidationError immediately

# vs Raw HTTP - Fails at API
response = requests.post(url, json={"width": 513})
# Only fails after round-trip
```

## Common Patterns

### Async/Await (Python)

```python
import asyncio
from modelslab_py.core.apis.video import Video

async def generate_multiple_videos(prompts, api_key):
    """Generate multiple videos concurrently."""
    client = Client(api_key=api_key)
    video_api = Video(client=client)

    tasks = []
    for prompt in prompts:
        schema = Text2Video(
            model_id="cogvideox",
            prompt=prompt,
            num_frames=25
        )
        tasks.append(video_api.text_to_video(schema))

    results = await asyncio.gather(*tasks)
    return results
```

### Error Handling (TypeScript)

```typescript
async function generateImageSafely(prompt: string) {
  try {
    const community = new Community(client.key);

    const result = await community.textToImage({
      key: client.key,
      model_id: "midjourney",
      prompt: prompt,
      width: 768,
      height: 768
    });

    return result.output[0];
  } catch (error) {
    if (error.response?.status === 429) {
      console.error("Rate limit exceeded");
      // Wait and retry
    } else if (error.response?.status === 400) {
      console.error("Invalid parameters:", error.message);
    } else {
      console.error("Unexpected error:", error);
    }
    throw error;
  }
}
```

## Best Practices

### 1. Initialize Client Once
```python
# Good - Reuse client
client = Client(api_key="...")
realtime_api = Realtime(client=client)
community_api = Community(client=client)

# Bad - Multiple clients
api1 = Realtime(client=Client(api_key="..."))
api2 = Community(client=Client(api_key="..."))
```

### 2. Use Type Hints (Python)
```python
from modelslab_py.schemas.community import Text2ImageSchema

def generate_image(schema: Text2ImageSchema) -> dict:
    """Generate image with type safety."""
    api = Community(client=client)
    return api.text_to_image(schema)
```

### 3. Environment Variables
```python
import os
from modelslab_py.core.client import Client

api_key = os.getenv("MODELSLAB_API_KEY")
client = Client(api_key=api_key)
```

```typescript
const apiKey = process.env.MODELSLAB_API_KEY;
const client = new Client(apiKey);
```

## Resources

- **Python SDK**: https://docs.modelslab.com/sdk/python
- **TypeScript SDK**: https://docs.modelslab.com/sdk/typescript
- **PHP SDK**: https://docs.modelslab.com/sdk/php
- **Go SDK**: https://docs.modelslab.com/sdk/golang
- **Dart SDK**: https://docs.modelslab.com/sdk/dart
- **GitHub Repos**: https://github.com/modelslab

## Related Skills

- All ModelsLab skills - SDKs available for all APIs
- `modelslab-webhooks` - Per-request webhook URLs for async results
