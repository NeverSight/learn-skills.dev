---
name: bunny-net
description: Use Bunny.net for CDN, image hosting, video hosting, edge storage, image optimization, AI image generation, edge scripting, container hosting, DNS, and security (WAF/DDoS). Trigger when user mentions bunny, cdn, image hosting, video hosting, media storage, edge storage, image optimization, video streaming, pull zone, storage zone, WebP conversion, AVIF, lazy loading, DRM, video encoding, edge functions, serverless edge, container hosting, WAF, DDoS protection, bot detection, or content delivery.
---

# Bunny.net Skill

Bunny.net is a comprehensive CDN and media platform offering content delivery, storage, video streaming, image optimization, AI image generation, edge computing, DNS, and security services.

## Account Configuration

**API Key**: Set as environment variable `BUNNY_API_KEY`

**Storage Key**: Set as environment variable `BUNNY_STORAGE_KEY` (per storage zone)

**Base URLs**:
| Service | Base URL |
|---------|----------|
| API | `https://api.bunny.net` |
| Storage (Frankfurt) | `https://storage.bunnycdn.com` |
| Storage (UK) | `https://uk.storage.bunnycdn.com` |
| Storage (NY) | `https://ny.storage.bunnycdn.com` |
| Storage (LA) | `https://la.storage.bunnycdn.com` |
| Storage (Singapore) | `https://sg.storage.bunnycdn.com` |

## Authentication

### Management API
```bash
curl -H "AccessKey: $BUNNY_API_KEY" \
  https://api.bunny.net/storagezone
```

### Storage API
Uses **storage zone password** as API key (different from main API key):
```bash
curl -H "AccessKey: $BUNNY_STORAGE_KEY" \
  https://storage.bunnycdn.com/<zone-name>/<path>
```

---

## 1. Edge Storage (File Hosting)

Store and serve files globally via CDN.

### Storage Zones

| Zone | ID | Password | CDN URL |
|------|-----|----------|---------|
| your-storage-zone | YOUR_ZONE_ID | YOUR_STORAGE_PASSWORD | https://your-zone.b-cdn.net |

### Upload File
```bash
curl -X PUT "https://storage.bunnycdn.com/your-storage-zone/images/photo.jpg" \
  -H "AccessKey: $BUNNY_STORAGE_KEY" \
  -H "Content-Type: image/jpeg" \
  --data-binary @photo.jpg
```

### Download File
```bash
curl "https://storage.bunnycdn.com/your-storage-zone/images/photo.jpg" \
  -H "AccessKey: $BUNNY_STORAGE_KEY" \
  -o photo.jpg
```

### List Files
```bash
curl "https://storage.bunnycdn.com/your-storage-zone/images/" \
  -H "AccessKey: $BUNNY_STORAGE_KEY"
```

### Delete File
```bash
curl -X DELETE "https://storage.bunnycdn.com/your-storage-zone/images/photo.jpg" \
  -H "AccessKey: $BUNNY_STORAGE_KEY"
```

### Python Upload Example
```python
import os
import requests
from pathlib import Path

def upload_to_bunny(local_path: str, remote_path: str):
    """Upload file to Bunny.net storage"""
    STORAGE_KEY = os.environ.get("BUNNY_STORAGE_KEY")
    ZONE = os.environ.get("BUNNY_STORAGE_ZONE", "your-storage-zone")
    CDN_URL = os.environ.get("BUNNY_CDN_URL", "https://your-zone.b-cdn.net")

    url = f"https://storage.bunnycdn.com/{ZONE}/{remote_path}"

    with open(local_path, "rb") as f:
        response = requests.put(
            url,
            headers={"AccessKey": STORAGE_KEY},
            data=f
        )

    if response.status_code == 201:
        cdn_url = f"{CDN_URL}/{remote_path}"
        return cdn_url
    else:
        raise Exception(f"Upload failed: {response.status_code}")
```

---

## 2. CDN (Pull Zones)

Content delivery network with global edge locations.

### CDN Configuration
- **Pull Zone ID**: YOUR_PULLZONE_ID
- **CDN URL**: https://your-zone.b-cdn.net
- **Connected Storage**: your-storage-zone (ID: YOUR_ZONE_ID)
- **Geo Zones**: US, EU, Asia, South America, Africa (all enabled)
- **Cache TTL**: 30 days

### Create Pull Zone
```bash
curl -X POST "https://api.bunny.net/pullzone" \
  -H "AccessKey: $BUNNY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"Name":"my-cdn","StorageZoneId":YOUR_ZONE_ID,"OriginType":2}'
```

### Purge Cache
```bash
# Purge single URL
curl -X POST "https://api.bunny.net/purge?url=https://your-zone.b-cdn.net/image.jpg" \
  -H "AccessKey: $BUNNY_API_KEY"
```

### Pull Zone Features
- **Edge Rules**: Custom request/response handling
- **Token Authentication**: Secure URLs with time-limited tokens
- **WebSockets**: Real-time connections supported
- **Origin Shield**: Reduce origin load
- **Custom Hostnames**: Use your own domain
- **SSL/TLS**: Free SSL certificates

---

## 3. Bunny Optimizer (Image Transformation)

Real-time image optimization and transformation via URL parameters.

### Base URL
`https://your-zone.b-cdn.net/<path>?<transformations>`

### Transformation Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `width` | Resize width | `?width=800` |
| `height` | Resize height | `?height=600` |
| `aspect_ratio` | Force aspect | `?aspect_ratio=16:9` |
| `crop` | Crop region | `?crop=x,y,width,height` |
| `focus_crop` | Focus point crop | `?focus_crop=x,y,scale,aspect` |
| `quality` | JPEG quality (1-100) | `?quality=85` |
| `format` | Output format | `?format=webp` |
| `blur` | Blur effect | `?blur=10` |
| `sharpen` | Sharpen image | `?sharpen=true` |
| `brightness` | Adjust brightness | `?brightness=4` |
| `contrast` | Adjust contrast | `?contrast=4` |
| `saturation` | Color saturation | `?saturation=20` |
| `gamma` | Gamma correction | `?gamma=25` |
| `tint` | Color tint | `?tint=ffeeee` |
| `flop` | Horizontal flip | `?flop=true` |

### Example Transformations
```
# Resize to 800px width, WebP format
https://your-zone.b-cdn.net/photo.jpg?width=800&format=webp

# Thumbnail with aspect ratio
https://your-zone.b-cdn.net/photo.jpg?width=400&aspect_ratio=1:1

# Optimized with quality and blur
https://your-zone.b-cdn.net/photo.jpg?quality=75&blur=5
```

---

## 4. Bunny AI (Image Generation)

Generate images via URL using AI models.

### URL Structure
```
https://your-zone.b-cdn.net/.ai/img/<engine>/<blueprint>/<seed>/<prompt>.jpg
```

### Available Engines

| Engine | Code | Resolution | Cost |
|--------|------|-----------|------|
| DALLE-2 256px | `dalle-256` | 256x256 | $0.016 |
| DALLE-2 512px | `dalle-512` | 512x512 | $0.018 |
| DALLE-2 1024px | `dalle-1024` | 1024x1024 | $0.020 |
| Stable Diffusion v1.5 | `sd15-512` | 512x512 | $0.001 |
| Stable Diffusion v2.1 | `sd21-512` | 512x512 | $0.001 |
| Stable Diffusion v2.1 | `sd21-768` | 768x768 | $0.030 |

### Examples
```
# Generate avatar with DALLE
https://your-zone.b-cdn.net/.ai/img/dalle-512/default/12345/cute-pixel-bunny.jpg

# Stable Diffusion landscape
https://your-zone.b-cdn.net/.ai/img/sd21-768/default/67890/tropical-island-sunset.jpg
```

### Prompt Tips
- Hyphens become spaces: `bunny-eating-carrots` -> "bunny eating carrots"
- File extension is stripped
- Results cached for 3 months

### DALLE Best For
- Concept art, pixel art
- Illustrations, abstract
- 3D renders

### Stable Diffusion Best For
- Photo-realistic images
- Landscapes, architecture
- Traditional/digital art

---

## 5. Bunny Stream (Video Hosting)

Professional video hosting with transcoding, DRM, and analytics.

### Key Features
- **Adaptive Streaming**: Auto quality adjustment
- **Multiple Codecs**: H.264, H.265, VP9, AV1
- **DRM Support**: Widevine, FairPlay, MediaCage
- **Captions**: Multi-language subtitles
- **Analytics**: Heatmaps, view counts, engagement

### Video Library API

```bash
# Create video library
curl -X POST "https://api.bunny.net/videolibrary" \
  -H "AccessKey: $BUNNY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"Name":"my-videos"}'
```

### Upload Video
```bash
# 1. Create video entry
curl -X POST "https://video.bunnycdn.com/library/{libraryId}/videos" \
  -H "AccessKey: {library-api-key}" \
  -H "Content-Type: application/json" \
  -d '{"title":"My Video"}'

# 2. Upload video file
curl -X PUT "https://video.bunnycdn.com/library/{libraryId}/videos/{videoId}" \
  -H "AccessKey: {library-api-key}" \
  --data-binary @video.mp4
```

### Get Embed Code
```bash
curl "https://video.bunnycdn.com/library/{libraryId}/videos/{videoId}" \
  -H "AccessKey: {library-api-key}"
```

### Video Player Embed
```html
<iframe src="https://iframe.mediadelivery.net/embed/{libraryId}/{videoId}"
  loading="lazy"
  style="border:none;width:100%;aspect-ratio:16/9"
  allow="accelerometer;gyroscope;autoplay;encrypted-media;picture-in-picture"
  allowfullscreen>
</iframe>
```

---

## 6. Edge Scripting (Serverless)

Run JavaScript at the edge for custom logic.

### Use Cases
- URL redirects
- Header modification
- A/B testing
- Geo-based routing
- Authentication
- HTML/JSON transformation

### Create Edge Script
```bash
curl -X POST "https://api.bunny.net/edgescript" \
  -H "AccessKey: $BUNNY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"Name":"my-script","Type":1}'
```

### Example Script
```javascript
// Redirect based on country
export default {
  async fetch(request, env) {
    const country = request.headers.get('cf-ipcountry');
    if (country === 'NO') {
      return Response.redirect('https://no.example.com' + request.url.pathname);
    }
    return fetch(request);
  }
}
```

---

## 7. Magic Containers (Edge Container Hosting)

Run Docker containers at edge locations.

### Features
- Auto-scaling
- Health checks
- Environment variables
- Regional provisioning
- Rolling updates
- GitHub Actions integration

### Use Cases
- Gaming backends
- AI inference
- Image processing
- API services

---

## 8. Bunny Shield (Security)

Comprehensive security suite.

### Features

| Feature | Description |
|---------|-------------|
| **WAF** | Web Application Firewall with custom rules |
| **DDoS** | Layer 3/4/7 DDoS protection |
| **Bot Detection** | AI-powered bot filtering |
| **Rate Limiting** | Per-IP and custom rate limits |
| **Access Lists** | IP allowlist/blocklist |
| **Upload Scanning** | Malware detection |

### Create Shield Zone
```bash
curl -X POST "https://api.bunny.net/shield/zones" \
  -H "AccessKey: $BUNNY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"PullZoneId":YOUR_PULLZONE_ID}'
```

---

## 9. Bunny DNS

Managed DNS with global anycast.

### Features
- IPv4 + IPv6 support
- DDoS protection
- DNSSEC support
- Fast propagation

### Create DNS Zone
```bash
curl -X POST "https://api.bunny.net/dnszone" \
  -H "AccessKey: $BUNNY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"Domain":"example.com"}'
```

---

## Quick Reference: API Endpoints

### Storage Zones
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/storagezone` | List all zones |
| POST | `/storagezone` | Create zone |
| GET | `/storagezone/{id}` | Get zone details |
| DELETE | `/storagezone/{id}` | Delete zone |

### Pull Zones
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/pullzone` | List all zones |
| POST | `/pullzone` | Create zone |
| GET | `/pullzone/{id}` | Get zone details |
| POST | `/pullzone/{id}` | Update zone |
| DELETE | `/pullzone/{id}` | Delete zone |

### Purge
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/purge?url=<url>` | Purge single URL |

### Video Libraries
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/videolibrary` | List libraries |
| POST | `/videolibrary` | Create library |
| GET | `/videolibrary/{id}` | Get library |

---

## Python Service Template

```python
"""
Bunny.net Media Service
"""
import os
import requests
from pathlib import Path
from typing import Optional
import mimetypes

class BunnyService:
    """Bunny.net CDN and Storage Service"""

    def __init__(self, api_key=None, storage_key=None, storage_zone=None, cdn_url=None):
        self.api_key = api_key or os.environ.get("BUNNY_API_KEY")
        self.storage_key = storage_key or os.environ.get("BUNNY_STORAGE_KEY")
        self.storage_zone = storage_zone or os.environ.get("BUNNY_STORAGE_ZONE", "your-storage-zone")
        self.cdn_url = cdn_url or os.environ.get("BUNNY_CDN_URL", "https://your-zone.b-cdn.net")
        self.storage_url = "https://storage.bunnycdn.com"

    def upload(self, local_path: str, remote_path: str) -> str:
        """Upload file and return CDN URL"""
        url = f"{self.storage_url}/{self.storage_zone}/{remote_path}"
        content_type = mimetypes.guess_type(local_path)[0] or "application/octet-stream"

        with open(local_path, "rb") as f:
            response = requests.put(
                url,
                headers={
                    "AccessKey": self.storage_key,
                    "Content-Type": content_type
                },
                data=f
            )

        response.raise_for_status()
        return f"{self.cdn_url}/{remote_path}"

    def delete(self, remote_path: str) -> bool:
        """Delete file from storage"""
        url = f"{self.storage_url}/{self.storage_zone}/{remote_path}"
        response = requests.delete(url, headers={"AccessKey": self.storage_key})
        return response.status_code == 200

    def list_files(self, path: str = "") -> list:
        """List files in directory"""
        url = f"{self.storage_url}/{self.storage_zone}/{path}/"
        response = requests.get(url, headers={"AccessKey": self.storage_key})
        return response.json()

    def purge_cache(self, path: str):
        """Purge CDN cache for path"""
        url = f"https://api.bunny.net/purge?url={self.cdn_url}/{path}"
        response = requests.post(url, headers={"AccessKey": self.api_key})
        return response.status_code == 200

    def get_optimized_url(self, path: str, width: int = None, format: str = None, quality: int = None) -> str:
        """Get optimized image URL with transformations"""
        url = f"{self.cdn_url}/{path}"
        params = []
        if width:
            params.append(f"width={width}")
        if format:
            params.append(f"format={format}")
        if quality:
            params.append(f"quality={quality}")
        if params:
            url += "?" + "&".join(params)
        return url


# Usage
bunny = BunnyService()

# Upload image
cdn_url = bunny.upload("photo.jpg", "images/photo.jpg")
print(f"Uploaded: {cdn_url}")

# Get optimized versions
webp_url = bunny.get_optimized_url("images/photo.jpg", width=800, format="webp", quality=85)
thumb_url = bunny.get_optimized_url("images/photo.jpg", width=200, format="webp")
```

---

## Documentation Links

- **API Reference**: https://docs.bunny.net/reference
- **Stream Docs**: https://docs.bunny.net/docs/stream-overview
- **Optimizer**: https://docs.bunny.net/docs/stream-image-processing
- **Edge Scripting**: https://docs.bunny.net/docs/edge-scripting-overview
- **Shield (Security)**: https://docs.bunny.net/docs/bunny-shield-overview
