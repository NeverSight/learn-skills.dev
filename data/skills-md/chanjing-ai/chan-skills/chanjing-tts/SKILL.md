---
name: chanjing-tts
description: Use Chanjing TTS API to convert text to speech
---

# Chanjing TTS

## When to Use This Skill

Use this skill when the user needs to generate audio from text.

Chanjing TTS supports:

* both Chinese and English
* multiple system voices
* adjustment of speech speed
* sentence-level timestamp in result

## How to Use This Skill

Multiple APIs need to be invoked. All share the domain: "https://open-api.chanjing.cc".
All requests communicate using json.
You should use utf-8 to encode and decode text throughout this task.

1. Obtain an `access_token`, which is required for all subsequent API calls
2. List all voice IDs and select one to use
3. Call the Create Speech API, record `task_id`
4. Poll the Query Speech Status API until success, then download generated audio file using the url in response

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
| | access\_token | Valid for one day, previous token will be invalidated |
| | expire\_in | Token expiration time |

Response Status Code Description

| Code | Description |
|---|---|
| 0 | Success |
| 400 | Invalid parameter format |
| 40000 | Parameter error |
| 50000 | System internal error |

### Select a Voice ID

Obtain all available voice IDs via API, and select one that fits the task at hand.
The dialect/accent can be deduced from the voice name.

```http
GET /open/v1/list_common_audio
access_token: {{access_token}}
```

Use the following request body:

```json
{
  "page": 1,
  "size": 100
}

Response example:

```json
{
  "trace_id": "25eb6794ffdaaf3672c25ed9efbe49c6",
  "code": 0,
  "msg": "success",
  "data": {
    "list": [
      {
        "id": "f9248f3b1b42447fb9282829321cfcf2",
        "grade": 0,
        "name": "带货小芸",
        "gender": "female",
        "lang": "multilingual",
        "desc": "",
        "speed": 1,
        "pitch": 1,
        "audition": "https://res.chanjing.cc/chanjing/res/upload/ms/2025-06-05/7945e0474b8cb526e884ee7e28e4af8d.wav"
      },
      {
        "id": "f5e69c1bbe414bec860da3294e177625",
        "grade": 0,
        "name": "方言口音老奶奶",
        "gender": "female",
        "lang": "multilingual",
        "desc": "",
        "speed": 1,
        "pitch": 1,
        "audition": "https://res.chanjing.cc/chanjing/res/upload/ms/2025-04-30/1b248ad05953028db5a6bcba9a951164.wav"
      },
      ...
    ],
    "page_info": {
      "page": 1,
      "size": 100,
      "total_count": 98,
      "total_page": 1
    }
  }
}
```

Response field description:

| First-level Field | Second-level Field | Third-level Field | Description |
|---|---|---|---|
| code | | | Response status code |
| message | | | Response message |
| data | | | Response data |
| | list | List data | Public voice - list data |
| | | id | Voice ID |
| | | name | Voice name, if it includes a place name, the generated speech is in dialect |
| | | gender | Gender |
| | | lang | Language |
| | | desc | Description |
| | | speed | Speech speed |
| | | pitch | Pitch |
| | | audition | Audition link |
| | | grade | Grade |

Response status code description:

| Code | Description |
|---|---|
| 0 | Response successful |
| 10400 | AccessToken verification failed |
| 40000 | Parameter error |
| 50000 | System internal error |
| 51000 | System internal error |

### Create Speech API

Submit a speech creating task, which returns a task ID for polling later.

```http
POST /open/v1/create_audio_task
access_token: {{access_token}}
Content-Type: application/json
```

Request body example:

```json
{
  "audio_man": "89843d52ccd04e2d854decd28d6143ce ",
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
| audio\_man | string | | Yes | 89843d52ccd04e2d854decd28d6143ce  | Voice ID |
| speed | number | | Yes | 1 | Speech speed: 0.5 (slow) - 2 (fast) |
| pitch | number | | Yes | 1 | Just set to 1 |
| text | object | text | Yes | Hello, I am your AI assistant. | Rich text, length must be less than 4000 characters |
| aigc\_watermark | bool |  | No | false | Whether to add visible watermark to audio, default to false |

Response example:

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

Response field description: 

| Field | Description |
|---|---|
| code | Response status code |
| msg | Response message |
| task\_id | Task ID, to be used in subsequent polling step |

Response status code description:

| code | Description |
| --- | --- |
| 0 | Response successful |
| 400 | Invalid parameter format |
| 10400 | AccessToken verification failed |
| 40000 | Parameter error |
| 40001 | Exceeds QPS limit |
| 40002 | Production duration reached limit |
| 50000 | System internal error |

#### Poll Query Speech Status API

Poll the following API until speech is generated.

```http
POST /open/v1/audio_task_state
access_token: {{access_token}}
Content-Type: application/json
```

Request example:

```json
{
  "task_id": "88f635dd9b8e4a898abb9d4679e0edc8"
}
```

Request field description:

| Parameter Name | Type | Required | Example | Description |
|---|---|---|---|---|
| task\_id | string | Yes | 88f789dd9b8e4a121abb9d4679e0edc8 | Speech synthesis task ID |

Response example:

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
| | type | | |
| | status | | 1: generating; 9: completed |
| | text | | Speech text |
| | full | url | url to download the generated audio file |
| | | path | |
| | | duration | Audio duration |
| | slice | | |
| | errMsg | | Error message |
| | errReason | | Error reason |
| | subtitles (array type) | key | Subtitle ID |
| | | start\_time | Subtitle start time |
| | | end\_time | Subtitle end time |
| | | subtitle | Subtitle text |

Response status code description:

| code | Description |
|---|---|
| 0 | Response successful |
| 10400 | AccessToken verification failed |
| 40000 | Parameter error |
| 50000 | System internal error |
