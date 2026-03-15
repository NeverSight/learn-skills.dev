---
name: modelslab-audio-generation
description: Generate speech, music, and sound effects using ModelsLab's v7 Voice API. Supports text-to-speech, speech-to-text, speech-to-speech, music generation, sound effects, dubbing, song extension, and song inpainting via ElevenLabs and Inworld models.
---

# ModelsLab Audio Generation

Generate high-quality audio including speech, music, voice conversion, sound effects, and dubbing using AI.

## When to Use This Skill

- Convert text to natural-sounding speech (TTS)
- Transcribe speech to text
- Transform voice characteristics (speech-to-speech)
- Generate music from text prompts
- Create sound effects
- Dub audio into different languages
- Extend or inpaint songs
- Build voice assistants or audiobooks

## Available APIs (v7)

### Voice Endpoints
- **Text to Speech**: `POST https://modelslab.com/api/v7/voice/text-to-speech`
- **Speech to Text**: `POST https://modelslab.com/api/v7/voice/speech-to-text`
- **Speech to Speech**: `POST https://modelslab.com/api/v7/voice/speech-to-speech`
- **Music Generation**: `POST https://modelslab.com/api/v7/voice/music-gen`
- **Sound Generation**: `POST https://modelslab.com/api/v7/voice/sound-generation`
- **Create Dubbing**: `POST https://modelslab.com/api/v7/voice/create-dubbing`
- **Song Extender**: `POST https://modelslab.com/api/v7/voice/song-extender`
- **Song Inpaint**: `POST https://modelslab.com/api/v7/voice/song-inpaint`
- **Fetch Result**: `POST https://modelslab.com/api/v7/voice/fetch/{id}`

> **Note**: v6 endpoints (`/api/v6/voice/text_to_speech`, etc.) still work but v7 is the current version. Parameter names have changed in v7 (e.g., `text` is now `prompt`, `audio` is now `init_audio`).

## Discovering Audio Models

```bash
# Search audio/voice models
modelslab models search --feature audio_gen

# Search by provider
modelslab models search --search "eleven"

# Get model details
modelslab models detail --id eleven_multilingual_v2
```

## Audio Model IDs

| model_id | Name | Use With |
|----------|------|----------|
| `eleven_multilingual_v2` | ElevenLabs Multilingual v2 | text-to-speech |
| `eleven_english_sts_v2` | ElevenLabs Voice Changer | speech-to-speech |
| `scribe_v1` | ElevenLabs Scribe | speech-to-text |
| `eleven_sound_effect` | ElevenLabs Sound Effects | sound-generation |
| `music_v1` | ElevenLabs Music | music-gen |
| `inworld-tts-1` | Inworld TTS | text-to-speech |

## Text to Speech

```python
import requests
import time

def text_to_speech(text, api_key, voice_id="21m00Tcm4TlvDq8ikWAM", model_id="eleven_multilingual_v2"):
    """Convert text to speech.

    Args:
        text: The text to convert to speech
        api_key: Your ModelsLab API key
        voice_id: ElevenLabs voice ID (see Available Voices below)
        model_id: TTS model to use
    """
    response = requests.post(
        "https://modelslab.com/api/v7/voice/text-to-speech",
        json={
            "key": api_key,
            "prompt": text,             # v7 uses "prompt" not "text"
            "voice_id": voice_id,
            "model_id": model_id
        }
    )

    data = response.json()

    if data["status"] == "success":
        return data["output"][0]
    elif data["status"] == "processing":
        return poll_audio_result(data["id"], api_key)
    else:
        raise Exception(f"Error: {data.get('message', 'Unknown error')}")

# Usage
audio_url = text_to_speech(
    "Hello! Welcome to ModelsLab. This is a test of our text-to-speech API.",
    "your_api_key"
)
print(f"Audio URL: {audio_url}")
```

## Speech to Text (Transcription)

```python
def speech_to_text(audio_url, api_key, model_id="scribe_v1"):
    """Transcribe speech from audio to text.

    Args:
        audio_url: URL of audio file (must be publicly accessible)
        model_id: STT model to use
    """
    response = requests.post(
        "https://modelslab.com/api/v7/voice/speech-to-text",
        json={
            "key": api_key,
            "init_audio": audio_url,    # v7 uses "init_audio" not "audio"
            "model_id": model_id
        }
    )

    data = response.json()

    if data["status"] == "success":
        return data["output"][0]
    elif data["status"] == "processing":
        return poll_audio_result(data["id"], api_key)
    else:
        raise Exception(data.get("message"))

# Transcribe audio
result = speech_to_text(
    "https://example.com/speech.mp3",
    "your_api_key"
)
print(f"Transcription: {result}")
```

## Speech to Speech (Voice Conversion)

```python
def speech_to_speech(audio_url, voice_id, api_key, model_id="eleven_english_sts_v2"):
    """Convert voice characteristics in audio.

    Args:
        audio_url: URL of the source audio
        voice_id: Target ElevenLabs voice ID
        model_id: Voice conversion model
    """
    response = requests.post(
        "https://modelslab.com/api/v7/voice/speech-to-speech",
        json={
            "key": api_key,
            "init_audio": audio_url,
            "voice_id": voice_id,
            "model_id": model_id
        }
    )

    data = response.json()
    if data["status"] == "success":
        return data["output"][0]
    elif data["status"] == "processing":
        return poll_audio_result(data["id"], api_key)
```

## Sound Effects Generation

```python
def generate_sound_effect(description, api_key, model_id="eleven_sound_effect"):
    """Generate a sound effect from a text description.

    Args:
        description: What sound to generate
        model_id: Sound effects model
    """
    response = requests.post(
        "https://modelslab.com/api/v7/voice/sound-generation",
        json={
            "key": api_key,
            "prompt": description,
            "model_id": model_id
        }
    )

    data = response.json()
    if data["status"] == "success":
        return data["output"][0]
    elif data["status"] == "processing":
        return poll_audio_result(data["id"], api_key)

# Generate door slam sound
sfx_url = generate_sound_effect(
    "Heavy wooden door slamming shut",
    "your_api_key"
)
```

## Music Generation

```python
def generate_music(prompt, api_key, model_id="music_v1"):
    """Generate music from a text description.

    Args:
        prompt: Description of music style/mood
        model_id: Music generation model
    """
    response = requests.post(
        "https://modelslab.com/api/v7/voice/music-gen",
        json={
            "key": api_key,
            "prompt": prompt,
            "model_id": model_id
        }
    )

    data = response.json()
    if data["status"] == "success":
        return data["output"][0]
    elif data["status"] == "processing":
        return poll_audio_result(data["id"], api_key)

# Generate background music
music_url = generate_music(
    "Upbeat electronic music with a driving beat, perfect for a tech startup video",
    "your_api_key"
)
print(f"Music: {music_url}")
```

## Polling for Async Results

```python
def poll_audio_result(request_id, api_key, timeout=300):
    """Poll for async audio generation results."""
    start_time = time.time()

    while time.time() - start_time < timeout:
        fetch = requests.post(
            f"https://modelslab.com/api/v7/voice/fetch/{request_id}",
            json={"key": api_key}
        )
        result = fetch.json()

        if result["status"] == "success":
            return result["output"][0]
        elif result["status"] == "failed":
            raise Exception(result.get("message", "Generation failed"))

        time.sleep(5)

    raise Exception("Timeout waiting for audio generation")
```

## Available ElevenLabs Voice IDs

| Voice ID | Name | Style |
|----------|------|-------|
| `21m00Tcm4TlvDq8ikWAM` | Rachel | Neutral, calm |
| `AZnzlk1XvdvUeBnXmlld` | Domi | Confident |
| `EXAVITQu4vr4xnSDxMaL` | Bella | Soft, warm |
| `ErXwobaYiN019PkySvjV` | Antoni | Well-rounded |
| `MF3mGyEYCl7XYWbV9V6O` | Elli | Young, clear |
| `TxGEqnHWrfWFTfGW9XjX` | Josh | Deep, warm |
| `VR6AewLTigWG4xSOukaG` | Arnold | Strong |
| `pNInz6obpgDQGcFmaJgB` | Adam | Deep, narrative |
| `yoZ06aMxZJJ28mfd3POQ` | Sam | Dynamic |

## Key Parameters

### Text to Speech
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `prompt` | string | Yes | Text to convert to speech |
| `voice_id` | string | Yes | ElevenLabs voice identifier |
| `model_id` | string | Yes | TTS model (e.g., `eleven_multilingual_v2`) |
| `temperature` | float | No | Voice variation |
| `webhook` | string | No | Async notification URL |

### Speech to Text
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `init_audio` | string | Yes | URL of audio to transcribe |
| `model_id` | string | Yes | STT model (e.g., `scribe_v1`) |

### Sound Generation
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `prompt` | string | Yes | Sound effect description |
| `model_id` | string | Yes | SFX model (e.g., `eleven_sound_effect`) |

## v6 to v7 Parameter Changes

| v6 Parameter | v7 Parameter | Notes |
|-------------|-------------|-------|
| `text` | `prompt` | TTS text input |
| `audio` | `init_audio` | STT/STS audio input |
| `target_audio` | `init_audio` | Voice-to-voice source |
| (not required) | `model_id` | Now required on all endpoints |

## Best Practices

### 1. Use Correct Voice IDs
TTS requires valid ElevenLabs voice IDs (not generic names like "alloy").

### 2. Ensure Audio Accessibility
Audio URLs for speech-to-text must be publicly accessible without redirects or authentication.

### 3. Use Webhooks for Long Operations
```python
payload = {
    "key": api_key,
    "prompt": "...",
    "model_id": "eleven_multilingual_v2",
    "webhook": "https://yourserver.com/webhook/audio",
    "track_id": "audio_001"
}
```

## Error Handling

```python
try:
    audio = text_to_speech(text, api_key)
    print(f"Audio generated: {audio}")
except Exception as e:
    print(f"Audio generation failed: {e}")
```

## Resources

- **Audio API Docs**: https://docs.modelslab.com/voice-cloning/overview
- **Model Browser**: https://modelslab.com/models
- **Model Selection Guide**: https://docs.modelslab.com/guides/model-selection
- **Get API Key**: https://modelslab.com/dashboard

## Related Skills

- `modelslab-model-discovery` - Find and filter models
- `modelslab-video-generation` - Add audio to videos
- `modelslab-chat-generation` - Chat with LLM models
- `modelslab-webhooks` - Handle async audio generation
