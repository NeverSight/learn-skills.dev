---
name: image-uploader
description: Uploads images to image hosting services (supports sm.ms, Imgur, and GitHub + jsDelivr CDN). Use this skill when the user wants to upload a local image file to the web and get a public URL.
license: Apache-2.0
metadata:
  author: crossoverJie
  version: "1.2"
---

# Image Uploader Skill

This skill allows uploading local image files to public image hosting services. It supports **sm.ms**, **Imgur**, and **GitHub** (with jsDelivr CDN acceleration).

## Prerequisites

1.  **Dependencies**: The skill requires Python 3 and the `requests` library.
    ```bash
    pip install -r skills/image-uploader/requirements.txt
    ```
2.  **Configuration**: An API token or client ID is required depending on the provider.

    **sm.ms** (default):
    *   **Config File**: `skills/image-uploader/config.json`
        ```json
        { "smms_token": "YOUR_TOKEN" }
        ```
    *   **Environment Variable**: `SMMS_TOKEN`
    *   **CLI Argument**: `--token`

    **Imgur**:
    *   **Config File**: `skills/image-uploader/config.json`
        ```json
        { "imgur_client_id": "YOUR_CLIENT_ID" }
        ```
    *   **Environment Variable**: `IMGUR_CLIENT_ID`
    *   **CLI Argument**: `--token`

    **GitHub**:
    *   **Config File**: `skills/image-uploader/config.json`
        ```json
        {
            "github_token": "YOUR_GITHUB_TOKEN",
            "github_owner": "YOUR_GITHUB_USERNAME",
            "github_repo": "YOUR_IMAGE_REPO_NAME",
            "github_path": "images",
            "github_branch": "main",
            "github_cdn": "jsdelivr"
        }
        ```
    *   **Environment Variables**: `IMAGE_UPLOADER_GITHUB_TOKEN`, `IMAGE_UPLOADER_GITHUB_OWNER`, `IMAGE_UPLOADER_GITHUB_REPO`, `IMAGE_UPLOADER_GITHUB_CDN`
    *   **CLI Argument**: `--token` (for token only)
    *   **CDN Options**:
        *   `"jsdelivr"` — `cdn.jsdelivr.net` (default, international)
        *   `"china"` — `jsd.cdn.zzko.cn` (China mirror)

    **Default Provider**: Set `default_provider` in `config.json` to `"smms"`, `"imgur"`, or `"github"`, or use the `IMAGE_UPLOADER_PROVIDER` environment variable.

## Usage

To upload an image, run the Python script:

```bash
python3 skills/image-uploader/image_uploader.py <path_to_image>
```

### Examples

**Upload to sm.ms (default, using config/env token):**
```bash
python3 skills/image-uploader/image_uploader.py /Users/me/Pictures/screenshot.png
```

**Upload to Imgur:**
```bash
python3 skills/image-uploader/image_uploader.py /Users/me/Pictures/screenshot.png --provider imgur
```

**Upload to GitHub (jsDelivr CDN):**
```bash
python3 skills/image-uploader/image_uploader.py /Users/me/Pictures/screenshot.png --provider github
```

**Upload with explicit token:**
```bash
python3 skills/image-uploader/image_uploader.py image.png --token "YOUR_API_TOKEN"
```

**Upload to Imgur using env var:**
```bash
IMGUR_CLIENT_ID="your_id" python3 skills/image-uploader/image_uploader.py image.png --provider imgur
```

**Upload to GitHub using env vars:**
```bash
IMAGE_UPLOADER_GITHUB_TOKEN="your_token" IMAGE_UPLOADER_GITHUB_OWNER="user" IMAGE_UPLOADER_GITHUB_REPO="images" python3 skills/image-uploader/image_uploader.py image.png --provider github
```

## Output

The script outputs the result to stdout.

**Success (sm.ms):**
```text
✅ Upload Successful!
URL: https://s2.loli.net/2023/01/01/abcdefg.jpg
Delete Link: https://sm.ms/delete/xyz123
Filename: screenshot.png
```

**Success (Imgur):**
```text
✅ Upload Successful!
URL: https://i.imgur.com/abcdefg.png
Delete Hash: AbCdEfGhIjK
```

**Success (GitHub):**
```text
✅ Upload Successful!
CDN URL: https://cdn.jsdelivr.net/gh/user/repo@main/images/a1b2c3d4_screenshot.png
Raw URL: https://raw.githubusercontent.com/user/repo/main/images/a1b2c3d4_screenshot.png
```

**Already Exists (sm.ms):**
```text
⚠️  Image already exists.
URL: https://s2.loli.net/2023/01/01/abcdefg.jpg
```

**Failure:**
```text
❌ Upload Failed
Message: Unauthorized.
```
