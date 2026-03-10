---
name: chanjing-tts-voice-clone
description: Use Chanjing TTS API to synthesize speech from text, using user-provided voice
---

# Chanjing TTS Voice Clone

## When to Use This Skill

Use this skill when the user needs to generate speech from text, with a user-provided reference voice. The reference audio needs to be provided as a publicly accessible url.

This TTS service supports:

* bilingual Chinese and English
* adjustment of speech rate
* sentence-level timestamp

## How to Use This Skill

Chanjing-TTS-Voice-Clone provides an asynchronous speech synthesis API.
Hostname for all APIs is: "https://open-api.chanjing.cc".
All requests communicate using json.
You should use utf-8 to encode and decode text throughout this task.

1. Obtain an access\_token, which is required for subsequent requests
2. Call the Create Voice API, which accepts a url to an audio file as reference voice
3. Poll the Query Voice API until the result is success; keep the voice ID
4. Call the Create Speech Generation Task API, using the voice ID, record the `task_id`
5. Poll the Query Speech Generation Task Status API until the result is success
6. When the task status is complete, use the corresponding url in API response to download the generated audio file

### Get Access Token API

Post a request to:

```http
POST /open/v1/access_token
Content-Type: application/json
```

Use the following hard-coded json body:

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
| | access\_token | Valid for one day, previous token will be invalidated |
| | expire\_in | Token expiration time |

Response status code description:

| code | Description |
|---|---|
| 0 | Success |
| 400 | Parameter format error |
| 40000 | Parameter error |
| 50000 | System internal error |

### Create Voice API

Post to the following endpoint to create a voice.

```http
POST /open/v1/create_customised_audio
access_token: {{access_token}}
Content-Type: application/json
```

Request body example:

```json
{
  "name": "example",
  "url": "https://example.com/abc.mp3"
}
```

Request field description:

| Field | Type | Required | Description |
|---|---|---|---|
| name | string | Yes | A name for this voice |
| url | string | Yes | url to the reference audio file, format must be one of mp3, wav or m4a. Supported mime: audio/x-wav, audio/mpeg, audio/m4a, video/mp4. Size must not exceed 100MB. Recommended audio length: 30s-5min |
| model\_type | string | Yes | Use "Cicada3.0-turbo" |
| language | string | No | Either "cn" or "en", default to "cn" |

Response example:

```json
{
  "trace_id": "2f0f50951d0bae0a3be3569097305424",
  "code": 0,
  "msg": "success",
  "data": "C-Audio-53e4e53ba1bc40de91ffaa74f20470fc"
}
```

Response field description:

| Field | Description |
|---|---|
| code | Status Code |
| msg | Message |
| data | Voice ID, to be used in following steps |

Response status code description:

| Code  | Description |
|---|---|
| 0 | Success |
| 400 | Parameter Format Error |
| 10400 | AccessToken Error |
| 40000 | Parameter Error |
| 40001 | QPS Exceeded |
| 50000 | Internal System Error |

### Poll Voice API

Send a GET request to the following endpoint to query whether the voice is ready to be used, voice ID is obtained in the previous step.
The polling process may take a few minutes, keep polling until the status indicates the voice is ready.

```http
GET /open/v1/customised_audio?id={{voice_id}}
access_token: {{access_token}}
```

Response example:

```json
{
  "trace_id": "7994cedae0f068d1e9e4f4abdf99215b",
  "code": 0,
  "msg": "success",
  "data": {
    "id": "C-Audio-53e4e53ba1bc40de91ffaa74f20470fc",
    "name": "声音克隆",
    "type": "cicada1.0",
    "progress": 0,
    "audio_path": "",
    "err_msg": "不支持的音频格式，请阅读接口文档",
    "status": 2
  }
}
```

Response field description:

| First-level Field | Second-level Field | Description |
|---|---|---|
| code | | Status Code |
| msg | | Response Message |
| data | | |
| | id | Voice ID |
| | progress | Progress: range 0-100 |
| | type | |
| | name | |
| | err\_msg | Error Message |
| | audio\_path | |
| | status | 0-queued; 1-in progress; 2-done; 3-expired; 4-failed; 99-deleted |

Response status code description:

| Code | Description |
|---|---|
| 0 | Success |
| 10400 | AccessToken Error |
| 40000 | Parameter Error |
| 40001 | QPS Exceeded |
| 50000 | Internal System Error |

### Create Speech Generation Task API

Post to the following endpoint to submit a speech generation task:

```http
POST /open/v1/create_audio_task
access_token: {{access_token}}
Content-Type: application/json
```

Request body example:

```json
{
  "audio_man": "C-Audio-53e4e53ba1bc40de91ffaa74f20470fc",
  "speed": 1,
  "pitch": 1,
  "text": {
    "text": "Hello, I am your AI assistant."
  }
}
```

Request field description:

| Parameter Name | Type | Nested Key | Required | Example | Description |
|---|---|---|---|---|---|
| audio\_man | string | | Yes | C-Audio-53e4e53ba1bc40de91ffaa74f20470fc | Voice ID, obtained from previous step |
| speed | number | | Yes | 1 | Speech rate, range: 0.5 (slow) to 2 (fast) |
| pitch | number | | Yes | 1 | Pitch (always set to 1) |
| text | object | text | Yes | Hello, I am your Cicada digital human | Rich text, text length limit less than 4,000 characters |
| aigc\_watermark | bool | | No | false | Whether to add visible watermark to audio, default is false |

Response field description:

| Field | Description |
|---|---|
| code | Response status code |
| msg | Response message |
| task\_id | Speech synthesis task ID |

Example Response

```json
{
  "trace_id": "dd09f123a25b43cf2119a2449daea6de",
  "code": 0,
  "msg": "success",
  "data": {
    "task_id": "88f635dd9b8e4a898abb9d4679e0edc8"
  }
}
```

Response status code description:

| code | Description |
|---|---|
| 0 | Success |
| 400 | Incoming parameter format error |
| 10400 | AccessToken verification failed |
| 40000 | Parameter error |
| 40001 | Exceeds QPS limit |
| 40002 | Production duration reached limit |
| 50000 | System internal error |

#### Query Speech Generation Task Status API

Post a request to the following endpoint:

```http
POST /open/v1/audio_task_state
access_token: {{access_token}}
Content-Type: application/json
```

Request body example:

```json
{
  "task_id": "88f635dd9b8e4a898abb9d4679e0edc8"
}
```

Request field description:

| Parameter Name | Type | Required | Example | Description |
|---|---|---|---|---|
| task\_id | string | Yes | 88f789dd9b8e4a121abb9d4679e0edc8 | Task ID obtained in previous step |

Response body example:

```json
{
  "trace_id": "ab18b14574bbcc31df864099d474080e",
  "code": 0,
  "msg": "success",
  "data": {
    "id": "9546a0fb1f0a4ae3b5c7489b77e4a94d",
    "type": "tts",
    "status": 9,
    "text": [
      "猫在跌落时能够在空中调整身体，通常能够四脚着地，这种”猫右自己“反射显示了它们惊人的身体协调能力和灵活性。核磁共振成像技术通过利用人体细胞中氢原子的磁性来生成详细的内部图像，为医学诊断提供了重要工具。"
    ],
    "full": {
      "url": "https://cy-cds-test-innovation.cds8.cn/chanjing/res/upload/tts/2025-04-08/093a59021d85a72d28a491f21820ece4.wav",
      "path": "093a59013d85a72d28a491f21820ece4.wav",
      "duration": 18.81
    },
    "slice": null,
    "errMsg": "",
    "errReason": "",
    "subtitles": [
      {
        "key": "20c53ff8cce9831a8d9c347263a400a54d72be15",
        "start_time": 0,
        "end_time": 2.77,
        "subtitle": "猫在跌落时能够在空中调整身体"
      },
      {
        "key": "e19f481b6cd2219225fa4ff67836448e054b2271",
        "start_time": 2.77,
        "end_time": 4.49,
        "subtitle": "通常能够四脚着地"
      },
      {
        "key": "140beae4046bd7a99fbe4706295c19aedfeeb843",
        "start_time": 4.49,
        "end_time": 5.73,
        "subtitle": "这种，猫右自己"
      },
      {
        "key": "e851881271876ab5a90f4be754fde2dc6b5498fd",
        "start_time": 5.73,
        "end_time": 7.97,
        "subtitle": "反射显示了它们惊人的身体"
      },
      {
        "key": "fbb0b4138bad189b9fc02669fe1f95116e9991b4",
        "start_time": 7.97,
        "end_time": 9.45,
        "subtitle": "协调能力和灵活性"
      },
      {
        "key": "f73404d135feaf84dd8fbea13af32eac847ac26d",
        "start_time": 9.45,
        "end_time": 12.49,
        "subtitle": "核磁共振成像技术通过利用人体"
      },
      {
        "key": "e18827931223962e477b14b2b8046947039ac222",
        "start_time": 12.49,
        "end_time": 14.77,
        "subtitle": "细胞中氢原子的磁性来生成"
      },
      {
        "key": "d137bf2b0c8b7a39e3f6753b7cf5d92bd877d2d9",
        "start_time": 14.77,
        "end_time": 15.97,
        "subtitle": "详细的内部图像"
      },
      {
        "key": "0773911ae0dbaa763a64352abdb6bdac3ff8f149",
        "start_time": 15.97,
        "end_time": 18.41,
        "subtitle": "为医学诊断提供了重要工具"
      }
    ]
  }
}
```

Response field description:

| First-level Field | Second-level Field | Third-level Field | Description |
|---|---|---|---|
| code | | | Response status code |
| msg | | | Response message |
| data | id | | Audio ID |
| | type | | Speech type |
| | status | | Status: 1 - in progress, 9 - done |
| | text | | Speech text |
| | full | url | url to download generated audio file |
| | | path | |
| | | duration | Audio duration |
| | slice | | |
| | errMsg | | Error message |
| | errReason | | Error reason |
| | subtitles(array type) | key | Subtitle ID |
| | | start\_time | Subtitle start time point |
| | | end\_time | Subtitle end time point |
| | | subtitle | Subtitle text |

Response field description:

| Code | Description |
|---|---|
| 0 | Response successful |
| 10400 | AccessToken verification failed |
| 40000 | Parameter error |
| 50000 | System internal error |
