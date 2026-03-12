---
name: video-uploader
description: Upload videos to Chinese and international social media platforms using browser automation. Supports Douyin (抖音), Kuaishou (快手), Xiaohongshu (小红书), TikTok, and Tencent Video/WeChat Channels (视频号). Use when users need to automate video publishing to these platforms with complete field generation and anti-detection browser configuration.
---

# Video Uploader Skill

Automated video upload to major Chinese and international social media platforms using Playwright browser automation with comprehensive anti-detection measures and field generation capabilities.

## Supported Platforms

**Douyin (抖音)**: China's leading short video platform with full feature support including thumbnails, product links, scheduled publishing, and third-party sync to Toutiao/Xigua.

**Kuaishou (快手)**: Popular Chinese short video platform supporting titles, hashtags (max 3), and scheduled publishing with confirmation dialogs.

**Xiaohongshu (小红书)**: Chinese lifestyle and social commerce platform supporting both image and video posts with API-based upload requiring signature service.

**TikTok**: International short video platform using Firefox browser with support for titles, hashtags, scheduled publishing (5-minute increments), and privacy controls.

**Tencent Video / WeChat Channels (视频号)**: WeChat's integrated video platform with short title formatting, collections, original content declaration, and category selection.

## Prerequisites

**Python Environment**: Python 3.8+ with pip installed.

**Dependencies**: Install from `references/requirements.txt`:
```bash
sudo pip3 install playwright==1.52.0 loguru==0.7.3 requests==2.32.3 PyYAML==6.0.2
```

**Playwright Browsers**: Install after package installation:
```bash
playwright install chromium firefox
```

**Account Cookies**: Each platform requires cookie file for authentication (Playwright storage state JSON format). First-time use triggers browser login window.

## Core Scripts

### 1. Direct Upload Script

`scripts/upload_video.py` - Command-line interface for direct uploads.

**Basic Usage**:
```bash
python scripts/upload_video.py \
  --platform douyin \
  --title "Video Title" \
  --video /path/to/video.mp4 \
  --tags "tag1,tag2,tag3" \
  --account /path/to/cookie.json
```

**Required Arguments**:
- `--platform`: Target platform (douyin/kuaishou/tiktok/tencent/xhs)
- `--title`: Video title (platform-specific length limits)
- `--video`: Absolute path to MP4 video file
- `--tags`: Comma-separated hashtags without # prefix
- `--account`: Absolute path to cookie JSON file

**Optional Arguments**:
- `--publish-date`: Schedule time "YYYY-MM-DD HH:MM:SS" or 0 for immediate
- `--thumbnail`: Thumbnail image path (Douyin only)
- `--product-link`: Product URL (Douyin only)
- `--product-title`: Product short title (Douyin only)
- `--category`: Video category (Tencent only)

### 2. Configuration-Based Upload

`scripts/upload_from_config.py` - Upload from JSON/YAML configuration files.

**Single Upload**:
```bash
python scripts/upload_from_config.py config.json
```

**Batch Upload**:
```bash
python scripts/upload_from_config.py batch_config.json --batch
```

**Configuration Format** (JSON):
```json
{
  "platform": "douyin",
  "video": {
    "path": "/path/to/video.mp4",
    "title": "Video Title",
    "description": "Description text",
    "tags": ["tag1", "tag2", "tag3"]
  },
  "account": {
    "cookie_file": "/path/to/cookie.json"
  },
  "options": {
    "publish_date": "2024-12-31 18:00:00",
    "thumbnail": "/path/to/thumbnail.jpg"
  }
}
```

**Configuration Format** (YAML):
```yaml
platform: douyin
video:
  path: /path/to/video.mp4
  title: Video Title
  description: Description text
  tags:
    - tag1
    - tag2
    - tag3
account:
  cookie_file: /path/to/cookie.json
options:
  publish_date: "2024-12-31 18:00:00"
  thumbnail: /path/to/thumbnail.jpg
```

### 3. Field Generation Tool

`scripts/generate_upload_config.py` - Auto-generate upload configuration from video file.

**Generate Configuration**:
```bash
python scripts/generate_upload_config.py \
  --platform douyin \
  --video /path/to/video.mp4 \
  --output json
```

**Auto-Generation Features**:
- **Title**: Extracted from filename with intelligent formatting
- **Tags**: Extracted from title with stop-word filtering
- **Description**: Expanded from title
- **Short Title**: Auto-formatted for Tencent (6-16 chars, special rules)

**Output Formats**:
- `--output json`: JSON configuration file
- `--output yaml`: YAML configuration file
- `--output command`: Ready-to-use command line
- `--output-file`: Save to file instead of stdout

**Schedule Generation**:
```bash
python scripts/generate_upload_config.py \
  --platform douyin \
  --video /path/to/video.mp4 \
  --schedule-days 1 \
  --schedule-hour 18 \
  --output command
```

## Platform-Specific Fields

### Douyin (抖音)

**Required**: title (max 30 chars), video_path, tags, account_file

**Optional**: publish_date, thumbnail_path (vertical), product_link, product_title (max 10 chars), description, location, sync_third_party

**Auto-Generated**: title, tags, description, thumbnail (from video frames)

**Notes**: Two page versions (v1/v2) auto-detected, supports third-party sync to Toutiao/Xigua

### Kuaishou (快手)

**Required**: title, video_path, tags (max 3), account_file

**Optional**: publish_date, description

**Auto-Generated**: title, tags (limited to top 3), description

**Notes**: Maximum 3 hashtags, requires confirmation dialog

### TikTok

**Required**: title, video_path, tags, account_file

**Optional**: publish_date (5-min increments), description, privacy (public/friends/private), allow_comments, allow_duet, allow_stitch

**Auto-Generated**: title, tags, description

**Notes**: Uses Firefox (not Chromium), two UI versions (iframe/direct)

### Tencent Video / WeChat Channels (视频号)

**Required**: title, video_path, tags, account_file

**Optional**: publish_date, short_title (6-16 chars), category, is_original, collection_id, description

**Auto-Generated**: title, tags, short_title (auto-formatted), description, category

**Notes**: Short title formatting rules (allowed chars: 《》"":+?%°), requires system Chrome

### Xiaohongshu (小红书)

**Required**: title, video_path, tags, account_file

**Optional**: publish_date, description, cover_path, location, post_type (video/image), images

**Auto-Generated**: title, tags, description, cover_path

**Notes**: Requires separate Flask signature service, supports video and image posts

## Browser Anti-Detection Configuration

The skill includes comprehensive anti-detection measures in `scripts/utils/browser_config.py`:

**Chromium Arguments**:
- Disable automation controlled flag
- Disable blink features detection
- Custom user agent and viewport
- Geolocation spoofing (Beijing for Chinese platforms)
- Timezone configuration
- Plugin and language spoofing

**Firefox Arguments**:
- Language and locale configuration
- Custom user agent
- Timezone settings

**Runtime Scripts**:
- Override navigator.webdriver
- Override navigator.plugins
- Override navigator.languages
- Add chrome property
- Permission query overrides

**Platform-Specific Configs**: Each platform has optimized browser configuration returned by `get_platform_specific_config(platform)`.

## Authentication and Cookie Management

**First-Time Login**: When cookie file missing or expired, script opens browser window for manual login (QR code/credentials). After successful login, session cookies saved to specified file.

**Cookie Validation**: Before each upload, script validates cookie by accessing upload page. If validation fails, login process triggered.

**Cookie Storage**: Playwright storage state format (JSON) including session data, tokens, and authentication information.

**Cookie Reuse**: Valid cookie files reusable for multiple uploads until expiration (typically 7-30 days).

**Recommended Organization**:
```
/home/ubuntu/cookies/
├── douyin_account1.json
├── douyin_account2.json
├── kuaishou_account.json
├── tiktok_account.json
└── tencent_account.json
```

## OpenClaw Integration Workflow

**Step 1: Prepare Video File**
- Ensure video file exists at accessible path
- Verify format is MP4
- Check platform requirements (duration, size, resolution)

**Step 2: Generate Configuration**
```bash
python scripts/generate_upload_config.py \
  --platform douyin \
  --video /path/to/video.mp4 \
  --schedule-days 1 \
  --output-file config.json
```

**Step 3: Review and Customize**
- Edit generated config.json
- Add platform-specific options
- Adjust title, tags, description as needed

**Step 4: Execute Upload**
```bash
python scripts/upload_from_config.py config.json
```

**Step 5: Verify Upload**
- Monitor console output for success/error messages
- Check platform for published video
- Verify scheduled time if applicable

## Batch Upload Workflow

**Create Batch Configuration**:
```json
[
  {
    "platform": "douyin",
    "video": {
      "path": "/path/to/video1.mp4",
      "title": "Video 1 Title",
      "tags": ["tag1", "tag2"]
    },
    "account": {
      "cookie_file": "/path/to/douyin.json"
    }
  },
  {
    "platform": "tiktok",
    "video": {
      "path": "/path/to/video2.mp4",
      "title": "Video 2 Title",
      "tags": ["tag3", "tag4"]
    },
    "account": {
      "cookie_file": "/path/to/tiktok.json"
    }
  }
]
```

**Execute Batch Upload**:
```bash
python scripts/upload_from_config.py batch.json --batch
```

**Batch Summary**: Displays total uploads, success count, failure count, and error details.

## Troubleshooting

**Cookie Expired Error**: Delete old cookie file and run script to trigger fresh login.

**Upload Failed Error**: Check video format, size, network connection, and platform-specific requirements.

**Browser Not Found Error**: Install Playwright browsers: `playwright install chromium firefox`

**Page Structure Changed Error**: Platform UI may have changed. Check for script updates or manually inspect page structure.

**Headless Mode Issues**: Most platforms require non-headless mode. Browser window will be visible during upload.

**Anti-Detection Bypass**: If platform detects automation, review browser configuration in `scripts/utils/browser_config.py` and ensure stealth.min.js is loaded.

## Reference Files

**platform_fields.md**: Complete field specifications for all platforms including required/optional/auto-generated fields, examples, and limitations.

**platform_details.md**: Platform-specific information including URLs, authentication methods, features, and special notes.

**requirements.txt**: Python package dependencies.

## Templates

**upload_config_template.json**: JSON configuration template with all fields.

**upload_config_template.yaml**: YAML configuration template with all fields.

## Advanced Programmatic Usage

Import uploader modules directly for custom integration:

```python
import asyncio
from scripts.douyin_uploader.main import DouYinVideo, douyin_setup

async def upload():
    account_file = "/path/to/cookie.json"
    await douyin_setup(account_file, handle=True)
    
    video = DouYinVideo(
        title="My Video Title",
        file_path="/path/to/video.mp4",
        tags=["tag1", "tag2", "tag3"],
        publish_date=0,
        account_file=account_file
    )
    
    await video.main()

asyncio.run(upload())
```

## Limitations

**Xiaohongshu Integration**: Not fully integrated due to complex signature service requirement. Requires separate Flask server for signature generation.

**Browser Visibility**: Most platforms require non-headless mode. Browser window visible during upload.

**Manual Login**: First-time authentication requires manual user interaction (QR code/credentials). Cannot be fully automated due to platform security.

**Platform Changes**: Social media platforms frequently update UI and security. Script may require updates when platforms change upload interfaces.

**Sandbox Testing**: Cannot test actual uploads in headless sandbox environment. Browser configuration verified but actual upload testing requires graphical environment.
