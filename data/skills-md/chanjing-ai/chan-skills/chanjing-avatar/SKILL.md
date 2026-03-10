---
name: chanjing-avatar
description: Use Chanjing Avatar API for lip-syncing video generation
---

# Chanjing Avatar (Lip-Syncing)

## When to Use This Skill

Use this skill when the user needs to create lip-syncing videos (digital avatar videos) with synchronized mouth movements.

Chanjing Avatar supports:

* Text-driven or audio-driven lip-syncing
* Multiple system voices for TTS
* Video resolution customization
* Task status polling and callback

## How to Use This Skill

Multiple APIs need to be invoked. All share the domain: "https://open-api.chanjing.cc".
All requests communicate using json.
You should use utf-8 to encode and decode text throughout this task.

1. Obtain an `access_token`, which is required for all subsequent API calls
2. Upload your video/audio files using the File Management API to get `file_id`
3. Create a lip-syncing task with video and audio/text using these `file_id` values
4. Poll the Query Task Detail API or use Task List API to check status
5. Download the generated video using the url in response when status is completed

### Obtain AccessToken

```http
POST /open/v1/access_token
Content-Type: application/json
```

Use the following hard-coded request body:

```json
{
  "app_id": "84042cb5",
  "secret_key": "10cd5091fe6042dfb91ba01816a991e0"
}
```

Response example:

```json
{
  "trace_id": "8ff3fcd57b33566048ef28568c6cee96",
  "code": 0,
  "msg": "success",
  "data": {
    "access_token": "1208CuZcV1Vlzj8MxqbO0kd1Wcl4yxwoHl6pYIzvAGoP3DpwmCCa73zmgR5NCrNu",
    "expire_in": 1721289220
  }
}
```

Response field description:

| First-level Field | Second-level Field | Description |
|---|---|---|
| code | | Response status code |
| msg | | Response message |
| data | | Response data |
| | access_token | Valid for one day, previous token will be invalidated |
| | expire_in | Token expiration time |

Response Status Code Description

| Code | Description |
|---|---|
| 0 | Success |
| 400 | Invalid parameter format |
| 40000 | Parameter error |
| 50000 | System internal error |

### Upload Media Files (File Management)

Before creating a lip-syncing task, you **must** upload your video (and optional audio) files using the File Management API to obtain `file_id` values.

The full documentation is here: `[File Management](https://doc.chanjing.cc/api/file/file-management.html)`.

#### Step 1: Get upload URL

```http
GET /open/v1/common/create_upload_url
access_token: {{access_token}}
```

Query params:

| Key | Example | Description |
|---|---|---|
| service | lip_sync_video / lip_sync_audio | File usage purpose. Use `lip_sync_video` for driving video, `lip_sync_audio` for audio (if audio-driven). |
| name | 1.mp4 | Original file name including extension |

You will get a response containing `sign_url`, `mime_type`, and `file_id`. Use the `sign_url` with HTTP `PUT` to upload the file, setting `Content-Type` to the returned `mime_type`. After the upload succeeds, keep the returned `file_id`; this is what you pass as `video_file_id` / `audio_file_id` below.

**Note:** Newly uploaded files may take up to about 1 minute before they become fully available.

### Create Lip-Syncing Task

Submit a lip-syncing video creation task, which returns a video ID for polling later.

```http
POST /open/v1/video_lip_sync/create
access_token: {{access_token}}
Content-Type: application/json
```

Request body example (TTS-driven):

```json
{
  "video_file_id": "e284db4d95de4220afe78132158156b5",
  "screen_width": 1080,
  "screen_height": 1920,
  "callback": "https://example.com/openapi/callback",
  "model": 0,
  "audio_type": "tts",
  "tts_config": {
    "text": "君不见黄河之水天上来，奔流到海不复回。",
    "audio_man_id": "C-f2429d07554749839849497589199916",
    "speed": 1,
    "pitch": 1
  }
}
```

Request body example (Audio-driven):

```json
{
  "video_file_id": "e284db4d95de4220afe78132158156b5",
  "screen_width": 1080,
  "screen_height": 1920,
  "model": 0,
  "audio_type": "audio",
  "audio_file_id": "audio_file_id_from_file_management"
}
```

Request field description:

| Parameter Name | Type | Required | Description |
|---|---|---|---|
| video_file_id | string | Yes | Video file ID from File Management (`data.file_id`). Supports mp4, mov, webm |
| screen_width | int | No | Screen width, default 1080 |
| screen_height | int | No | Screen height, default 1920 |
| backway | int | No | Playback order when reaching end: 1-normal, 2-reverse. Default 1 |
| drive_mode | string | No | Drive mode: ""-normal, "random"-random frame. Default "" |
| callback | string | No | Callback URL for async notification |
| model | int | No | Model version: 0-basic, 1-high quality. Default 0 |
| audio_type | string | No | Audio type: "tts"-text driven, "audio"-audio driven. Default "tts" |
| tts_config | object | Yes (for tts) | TTS configuration when audio_type="tts" |
| tts_config.text | string | Yes (for tts) | Text to synthesize |
| tts_config.audio_man_id | string | Yes (for tts) | Voice ID |
| tts_config.speed | number | No | Speech speed: 0.5-2, default 1 |
| tts_config.pitch | number | No | Pitch, default 1 |
| audio_file_id | string | Yes (for audio) | Audio file ID from File Management (`data.file_id`) when `audio_type="audio"`. Supports mp3, m4a, wav |
| volume | int | No | Volume: 1-100, default 100 |

Response example:

```json
{
  "trace_id": "8d10659438827bd4d59eaa2696f9d391",
  "code": 0,
  "msg": "success",
  "data": "9499ed79995c4bdb95f0d66ca84419fd"
}
```

Response field description:

| Field | Description |
|---|---|
| code | Response status code |
| msg | Response message |
| data | Video ID for subsequent polling |

### Query Task List

Get a list of lip-syncing tasks.

```http
POST /open/v1/video_lip_sync/list
access_token: {{access_token}}
Content-Type: application/json
```

Request body:

```json
{
  "page": 1,
  "page_size": 10
}
```

Request field description:

| Parameter | Type | Required | Description |
|---|---|---|---|
| page | int | No | Page number, default 1 |
| page_size | int | No | Page size, default 10 |

Response example:

```json
{
  "trace_id": "8d10659438827bd4d59eaa2696f9d391",
  "code": 0,
  "msg": "success",
  "data": {
    "list": [
      {
        "id": "9499ed79995c4bdb95f0d66ca84419fd",
        "status": 20,
        "progress": 100,
        "msg": "success",
        "video_url": "https://res.chanjing.cc/xxx/lip-sync/9499ed79995c4bdb95f0d66ca84419fd.mp4",
        "preview_url": "https://res.chanjing.cc/xxx/lip-sync/9499ed79995c4bdb95f0d66ca84419fd.jpg",
        "duration": 300,
        "create_time": 1738636800
      }
    ],
    "page_info": {
      "page": 1,
      "size": 10,
      "total_count": 1,
      "total_page": 1
    }
  }
}
```

Response field description:

| First-level Field | Second-level Field | Description |
|---|---|---|
| code | | Response status code |
| msg | | Response message |
| data | | Response data |
| | list | Task list |
| | | id: Video ID |
| | | status: Task status (0-pending, 10-generating, 20-success, 30-failed) |
| | | progress: Progress 0-100 |
| | | msg: Task message |
| | | video_url: Video download URL |
| | | preview_url: Cover image URL |
| | | duration: Video duration in ms |
| | | create_time: Creation time (unix timestamp) |
| | page_info | Pagination info |

### Query Task Detail

Poll the following API to check task status until completed.

```http
GET /open/v1/video_lip_sync/detail
access_token: {{access_token}}
```

Query params:

| Parameter | Description |
|---|---|
| id | Video ID |

Example: `GET /open/v1/video_lip_sync/detail?id=9499ed79995c4bdb95f0d66ca84419fd`

Response example:

```json
{
  "trace_id": "8d10659438827bd4d59eaa2696f9d391",
  "code": 0,
  "msg": "success",
  "data": {
    "id": "9499ed79995c4bdb95f0d66ca84419fd",
    "status": 20,
    "progress": 100,
    "msg": "success",
    "video_url": "https://res.chanjing.cc/xxx/lip-sync/9499ed79995c4bdb95f0d66ca84419fd.mp4",
    "preview_url": "https://res.chanjing.cc/xxx/lip-sync/9499ed79995c4bdb95f0d66ca84419fd.jpg",
    "duration": 300,
    "create_time": 1738636800
  }
}
```

Response field description:

| First-level Field | Second-level Field | Description |
|---|---|---|
| code | | Response status code |
| msg | | Response message |
| data | | Response data |
| | id | Video ID |
| | status | Task status: 0-pending, 10-generating, 20-success, 30-failed |
| | progress | Progress 0-100 |
| | msg | Task message |
| | video_url | Video download URL |
| | preview_url | Cover image URL |
| | duration | Video duration in ms |
| | create_time | Creation time (unix timestamp) |

### Callback Notification

When a callback URL is provided, the system will send a POST request when the task completes:

```json
{
  "trace_id": "8d10659438827bd4d59eaa2696f9d391",
  "code": 0,
  "msg": "success",
  "data": {
    "id": "9499ed79995c4bdb95f0d66ca84419fd",
    "status": 20,
    "progress": 100,
    "msg": "success",
    "video_url": "https://res.chanjing.cc/xxx/lip-sync/9499ed79995c4bdb95f0d66ca84419fd.mp4",
    "preview_url": "https://res.chanjing.cc/xxx/lip-sync/9499ed79995c4bdb95f0d66ca84419fd.jpg",
    "duration": 300,
    "create_time": 1738636800
  }
}
```

## Response Status Code Description

| Code | Description |
|---|---|
| 0 | Response successful |
| 10400 | AccessToken verification failed |
| 40000 | Parameter error |
| 40001 | Exceeds RPM/QPS limit |
| 50000 | System internal error |

