---
name: modly-image-to-3d
description: Desktop app that generates 3D models from images using local AI running entirely on your GPU
triggers:
  - generate 3D model from image
  - image to 3D mesh locally
  - run Modly AI model
  - install Modly extension
  - set up local 3D generation
  - Modly GPU image to 3D
  - open source image to mesh desktop app
  - Hunyuan3D local generation
---

# Modly Image-to-3D Skill

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

Modly is a local, open-source desktop application (Windows/Linux) that converts photos into 3D mesh models using AI models running entirely on your GPU — no cloud, no API keys required.

---

## Architecture Overview

```
modly/
├── src/                    # Electron + TypeScript frontend
│   ├── main/               # Electron main process
│   ├── renderer/           # React UI (renderer process)
│   └── preload/            # IPC bridge
├── api/                    # Python FastAPI backend
│   ├── generator.py        # Core generation logic
│   └── requirements.txt
├── resources/
│   └── icons/
├── launcher.bat            # Windows quick-start
├── launcher.sh             # Linux quick-start
└── package.json
```

The app runs as an Electron shell over a local Python FastAPI server. Extensions are GitHub repos with a `manifest.json` + `generator.py` that plug into the extension system.

---

## Installation

### Quick start (no build required)

```bash
# Windows
launcher.bat

# Linux
chmod +x launcher.sh
./launcher.sh
```

### Development setup

```bash
# 1. Clone
git clone https://github.com/lightningpixel/modly
cd modly

# 2. Install JS dependencies
npm install

# 3. Set up Python backend
cd api
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (Linux/macOS)
source .venv/bin/activate

pip install -r requirements.txt
cd ..

# 4. Run dev mode (starts Electron + Python backend)
npm run dev
```

### Production build

```bash
# Build installers for current platform
npm run build

# Output goes to dist/
```

---

## Key npm Scripts

```bash
npm run dev        # Start app in development mode (hot reload)
npm run build      # Package app for distribution
npm run lint       # Run ESLint
npm run typecheck  # TypeScript type checking
```

---

## Extension System

Extensions are GitHub repositories containing:
- `manifest.json` — metadata and model variants
- `generator.py` — generation logic implementing the Modly extension interface

### manifest.json structure

```json
{
  "name": "My 3D Extension",
  "id": "my-extension-id",
  "description": "Generates 3D models using XYZ model",
  "version": "1.0.0",
  "author": "Your Name",
  "repository": "https://github.com/yourname/my-modly-extension",
  "variants": [
    {
      "id": "model-small",
      "name": "Small (faster)",
      "description": "Lighter variant for faster generation",
      "size_gb": 4.2,
      "vram_gb": 6,
      "files": [
        {
          "url": "https://huggingface.co/yourorg/yourmodel/resolve/main/weights.safetensors",
          "filename": "weights.safetensors",
          "sha256": "abc123..."
        }
      ]
    }
  ]
}
```

### generator.py interface

```python
# api/extensions/<extension-id>/generator.py
# Required interface every extension must implement

import sys
import json
from pathlib import Path

def generate(
    image_path: str,
    output_path: str,
    variant_id: str,
    models_dir: str,
    **kwargs
) -> dict:
    """
    Required entry point for all Modly extensions.
    
    Args:
        image_path:  Path to input image file
        output_path: Path where output .glb/.obj should be saved
        variant_id:  Which model variant to use
        models_dir:  Directory where downloaded model weights live
    
    Returns:
        dict with keys:
            success (bool)
            output_file (str) — path to generated mesh
            error (str, optional)
    """
    try:
        # Load your model weights
        weights = Path(models_dir) / variant_id / "weights.safetensors"
        
        # Run your inference
        mesh = run_inference(str(weights), image_path)
        
        # Save output
        mesh.export(output_path)
        
        return {
            "success": True,
            "output_file": output_path
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
```

### Installing an extension (UI flow)

1. Open Modly → go to **Models** page
2. Click **Install from GitHub**
3. Paste the HTTPS URL, e.g. `https://github.com/lightningpixel/modly-hunyuan3d-mini-extension`
4. After install, click **Download** on the desired model variant
5. Select the installed model and upload an image to generate

### Official Extensions

| Extension | Model |
|-----------|-------|
| [modly-hunyuan3d-mini-extension](https://github.com/lightningpixel/modly-hunyuan3d-mini-extension) | Hunyuan3D 2 Mini |

---

## Python Backend API (FastAPI)

The backend runs locally. Key endpoints used by the Electron frontend:

```python
# Typical backend route patterns (api/main.py or similar)

# GET /extensions         — list installed extensions
# GET /extensions/{id}    — get extension details + variants
# POST /extensions/install — install extension from GitHub URL
# POST /generate          — trigger 3D generation
# GET /generate/status    — poll generation progress
# GET /models             — list downloaded model variants
# POST /models/download   — download a model variant
```

### Calling the backend from Electron (IPC pattern)

```typescript
// src/preload/index.ts — exposing backend calls to renderer
import { contextBridge, ipcRenderer } from 'electron'

contextBridge.exposeInMainWorld('modly', {
  generate: (imagePath: string, extensionId: string, variantId: string) =>
    ipcRenderer.invoke('generate', { imagePath, extensionId, variantId }),

  installExtension: (repoUrl: string) =>
    ipcRenderer.invoke('install-extension', { repoUrl }),

  listExtensions: () =>
    ipcRenderer.invoke('list-extensions'),
})
```

```typescript
// src/main/ipc-handlers.ts — main process handling
import { ipcMain } from 'electron'

ipcMain.handle('generate', async (_event, { imagePath, extensionId, variantId }) => {
  const response = await fetch('http://localhost:PORT/generate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ image_path: imagePath, extension_id: extensionId, variant_id: variantId }),
  })
  return response.json()
})
```

```typescript
// src/renderer/components/GenerateButton.tsx — UI usage
declare global {
  interface Window {
    modly: {
      generate: (imagePath: string, extensionId: string, variantId: string) => Promise<{ success: boolean; output_file?: string; error?: string }>
      installExtension: (repoUrl: string) => Promise<{ success: boolean }>
      listExtensions: () => Promise<Extension[]>
    }
  }
}

async function handleGenerate(imagePath: string) {
  const result = await window.modly.generate(
    imagePath,
    'modly-hunyuan3d-mini-extension',
    'hunyuan3d-mini-turbo'
  )

  if (result.success) {
    console.log('Mesh saved to:', result.output_file)
  } else {
    console.error('Generation failed:', result.error)
  }
}
```

---

## Writing a Custom Extension

### Minimal extension repository structure

```
my-modly-extension/
├── manifest.json
└── generator.py
```

### Example: wrapping a HuggingFace diffusion model

```python
# generator.py
import torch
from PIL import Image
from pathlib import Path

def generate(image_path, output_path, variant_id, models_dir, **kwargs):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    weights_dir = Path(models_dir) / variant_id

    try:
        # Load model (example pattern)
        from your_model_lib import ImageTo3DPipeline
        
        pipe = ImageTo3DPipeline.from_pretrained(
            str(weights_dir),
            torch_dtype=torch.float16
        ).to(device)

        image = Image.open(image_path).convert("RGB")
        
        with torch.no_grad():
            mesh = pipe(image).mesh

        mesh.export(output_path)

        return {"success": True, "output_file": output_path}

    except Exception as e:
        return {"success": False, "error": str(e)}
```

---

## Configuration & Environment

Modly runs fully locally — no environment variables or API keys needed. GPU/CUDA is auto-detected by PyTorch in extensions.

Relevant configuration lives in:

```
package.json          # Electron app metadata, build targets
api/requirements.txt  # Python dependencies for backend
```

If you need to configure the backend port or extension directory, check the Electron main process config (typically `src/main/index.ts`) for constants like `API_PORT` or `EXTENSIONS_DIR`.

---

## Common Patterns

### Check if CUDA is available in an extension

```python
import torch

def get_device():
    if torch.cuda.is_available():
        print(f"Using GPU: {torch.cuda.get_device_name(0)}")
        return "cuda"
    print("No GPU found, falling back to CPU (slow)")
    return "cpu"
```

### Progress reporting from generator.py

```python
import sys
import json

def report_progress(percent: int, message: str):
    """Write progress to stdout so Modly can display it."""
    print(json.dumps({"progress": percent, "message": message}), flush=True)

def generate(image_path, output_path, variant_id, models_dir, **kwargs):
    report_progress(0, "Loading model...")
    # ... load model ...
    report_progress(30, "Processing image...")
    # ... inference ...
    report_progress(90, "Exporting mesh...")
    # ... export ...
    report_progress(100, "Done")
    return {"success": True, "output_file": output_path}
```

### Adding a new page in the renderer (React)

```typescript
// src/renderer/pages/MyPage.tsx
import React, { useEffect, useState } from 'react'

interface Extension {
  id: string
  name: string
  description: string
}

export default function MyPage() {
  const [extensions, setExtensions] = useState<Extension[]>([])

  useEffect(() => {
    window.modly.listExtensions().then(setExtensions)
  }, [])

  return (
    <div>
      <h1>Installed Extensions</h1>
      {extensions.map(ext => (
        <div key={ext.id}>
          <h2>{ext.name}</h2>
          <p>{ext.description}</p>
        </div>
      ))}
    </div>
  )
}
```

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `npm run dev` — Python backend not starting | Ensure venv is set up: `cd api && python -m venv .venv && pip install -r requirements.txt` |
| CUDA out of memory | Use a smaller model variant or close other GPU processes |
| Extension install fails | Verify the GitHub URL is HTTPS and the repo contains `manifest.json` at root |
| Generation hangs | Check that your GPU drivers and CUDA toolkit match the PyTorch version in `requirements.txt` |
| App won't launch on Linux | Make `launcher.sh` executable: `chmod +x launcher.sh` |
| Model download stalls | Check disk space; large models (4–10 GB) need adequate free space |
| `torch` not found in extension | Ensure PyTorch is in `api/requirements.txt`, not just the extension's own deps |

### Verifying GPU is detected

```bash
cd api
source .venv/bin/activate   # or .venv\Scripts\activate on Windows
python -c "import torch; print(torch.cuda.is_available(), torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'no GPU')"
```

---

## Resources

- **Homepage**: https://modly3d.app
- **Releases**: https://github.com/lightningpixel/modly/releases/latest
- **Official extension**: https://github.com/lightningpixel/modly-hunyuan3d-mini-extension
- **Discord**: https://discord.gg/FjzjRgweVk
- **License**: MIT (attribution required — credit Modly + Lightning Pixel in forks)
