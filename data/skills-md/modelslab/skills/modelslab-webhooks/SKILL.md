---
name: modelslab-webhooks
description: Handle async operations efficiently using ModelsLab webhooks. Get real-time notifications when API requests complete instead of polling.
---

# ModelsLab Webhooks

Receive real-time notifications when your API requests complete processing using webhooks instead of polling.

## When to Use This Skill

- Handle long-running operations (video, 3D, training)
- Build scalable applications
- Avoid continuous polling
- Reduce API calls
- Get instant completion notifications
- Process requests in the background

## Webhook-Supported Endpoints

Webhooks are supported by these API categories:

### Image Generation
- `text2img`, `img2img`, `inpaint`, `controlnet`

### Video
- `text2video`, `img2video`, `text2video_ultra`, `img2video_ultra`

### Audio
- `text_to_speech`, `voice_to_voice`, `music_gen`, `song_generator`

### 3D
- `text_to_3d`, `image_to_3d`

### Image Editing
- All editing endpoints

### Training
- `fine_tune`, `lora_fine_tune`

### Workflows
- `run` (workflow execution)

## How Webhooks Work

1. **Submit Request**: Include `webhook` URL in API request
2. **Get Request ID**: API returns immediately with request ID
3. **Processing**: ModelsLab processes your request
4. **Webhook Call**: When complete, ModelsLab sends POST request to your webhook URL
5. **Handle Result**: Your server receives and processes the result

## Basic Webhook Setup

### 1. Create Webhook Endpoint

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook/modelslab', methods=['POST'])
def handle_modelslab_webhook():
    """Handle webhook callbacks from ModelsLab."""
    try:
        # Get the webhook data
        data = request.json

        # Extract important fields
        status = data.get('status')
        output = data.get('output', [])
        track_id = data.get('track_id')  # Your custom identifier
        request_id = data.get('id')

        if status == 'success':
            # Process successful result
            result_url = output[0] if output else None
            print(f"Generation complete! Track ID: {track_id}")
            print(f"Result: {result_url}")

            # Store in database, notify user, etc.
            save_result(track_id, result_url)

        elif status == 'failed':
            # Handle failure
            error = data.get('message', 'Unknown error')
            print(f"Generation failed: {error}")
            handle_failure(track_id, error)

        return jsonify({"received": True}), 200

    except Exception as e:
        print(f"Webhook error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=8080)
```

### 2. Make Your Endpoint Publicly Accessible

```bash
# Use ngrok for local testing
ngrok http 8080

# Your webhook URL will be:
# https://abc123.ngrok.io/webhook/modelslab
```

## Using Webhooks with APIs

### Image Generation with Webhook

```python
import requests

def generate_image_with_webhook(prompt, api_key, webhook_url, track_id):
    """Generate image and receive result via webhook."""
    response = requests.post(
        "https://modelslab.com/api/v6/images/text2img",
        json={
            "key": api_key,
            "model_id": "midjourney",
            "prompt": prompt,
            "negative_prompt": "low quality",
            "width": 768,
            "height": 768,
            "webhook": webhook_url,  # Your webhook endpoint
            "track_id": track_id     # Your custom identifier
        }
    )

    data = response.json()

    if data["status"] == "error":
        raise Exception(f"Error: {data['message']}")

    # Return request ID for tracking
    return {
        "request_id": data["id"],
        "track_id": track_id,
        "status": data["status"]
    }

# Usage
result = generate_image_with_webhook(
    "A futuristic cityscape at sunset",
    "your_api_key",
    "https://yourserver.com/webhook/modelslab",
    "image_001"
)
print(f"Request submitted: {result['request_id']}")
# Result will be sent to your webhook when ready
```

### Video Generation with Webhook

```python
def generate_video_with_webhook(prompt, api_key, webhook_url, track_id):
    """Generate video and receive result via webhook."""
    response = requests.post(
        "https://modelslab.com/api/v6/video/text2video",
        json={
            "key": api_key,
            "model_id": "cogvideox",
            "prompt": prompt,
            "num_frames": 25,
            "webhook": webhook_url,
            "track_id": track_id
        }
    )

    data = response.json()
    return {
        "request_id": data["id"],
        "track_id": track_id
    }

# Submit video generation
video_request = generate_video_with_webhook(
    "A spaceship flying through an asteroid field",
    "your_api_key",
    "https://yourserver.com/webhook/video",
    "video_123"
)
```

### Audio Generation with Webhook

```python
def generate_audio_with_webhook(text, api_key, webhook_url, track_id):
    """Generate audio and receive result via webhook."""
    response = requests.post(
        "https://modelslab.com/api/v6/audio/text_to_speech",
        json={
            "key": api_key,
            "text": text,
            "voice_id": "alloy",
            "language": "en",
            "webhook": webhook_url,
            "track_id": track_id
        }
    )

    data = response.json()
    return data["id"]
```

## Track ID System

The `track_id` parameter lets you identify which webhook callback corresponds to which request:

```python
import uuid

def generate_unique_track_id(user_id, request_type):
    """Generate a unique tracking ID."""
    unique_id = str(uuid.uuid4())[:8]
    return f"{user_id}_{request_type}_{unique_id}"

# Usage
track_id = generate_unique_track_id("user123", "image")
# Returns: "user123_image_a1b2c3d4"

# Use in API request
generate_image_with_webhook(
    prompt,
    api_key,
    webhook_url,
    track_id=track_id
)
```

## Advanced Webhook Handler

```python
from flask import Flask, request, jsonify
import logging
from datetime import datetime

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

class WebhookHandler:
    """Handle ModelsLab webhook callbacks."""

    def __init__(self):
        self.handlers = {
            'image': self.handle_image_result,
            'video': self.handle_video_result,
            'audio': self.handle_audio_result,
            '3d': self.handle_3d_result
        }

    def process_webhook(self, data):
        """Process incoming webhook data."""
        track_id = data.get('track_id', '')
        status = data.get('status')
        request_id = data.get('id')

        logging.info(f"Webhook received: {track_id} - {status}")

        # Extract request type from track_id
        request_type = self.get_request_type(track_id)

        if status == 'success':
            output = data.get('output', [])
            result_url = output[0] if output else None

            # Route to appropriate handler
            if request_type in self.handlers:
                self.handlers[request_type](track_id, result_url, data)
            else:
                self.handle_generic_result(track_id, result_url, data)

        elif status == 'failed':
            error = data.get('message', 'Unknown error')
            self.handle_failure(track_id, error)

        return True

    def get_request_type(self, track_id):
        """Extract request type from track_id."""
        # Assuming track_id format: "user_type_id"
        parts = track_id.split('_')
        return parts[1] if len(parts) > 1 else 'unknown'

    def handle_image_result(self, track_id, result_url, data):
        """Handle image generation result."""
        logging.info(f"Image ready: {track_id}")
        # Store in database
        # Notify user
        # Post-process image
        pass

    def handle_video_result(self, track_id, result_url, data):
        """Handle video generation result."""
        logging.info(f"Video ready: {track_id}")
        # Store video
        # Trigger post-processing
        pass

    def handle_audio_result(self, track_id, result_url, data):
        """Handle audio generation result."""
        logging.info(f"Audio ready: {track_id}")
        pass

    def handle_3d_result(self, track_id, result_url, data):
        """Handle 3D generation result."""
        logging.info(f"3D model ready: {track_id}")
        pass

    def handle_generic_result(self, track_id, result_url, data):
        """Handle generic result."""
        logging.info(f"Result ready: {track_id} - {result_url}")

    def handle_failure(self, track_id, error):
        """Handle failed generation."""
        logging.error(f"Generation failed: {track_id} - {error}")
        # Notify user
        # Log error
        # Retry if appropriate

webhook_handler = WebhookHandler()

@app.route('/webhook/modelslab', methods=['POST'])
def webhook_endpoint():
    """Webhook endpoint for all ModelsLab callbacks."""
    try:
        data = request.json
        webhook_handler.process_webhook(data)
        return jsonify({"received": True}), 200
    except Exception as e:
        logging.error(f"Webhook error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=8080)
```

## Best Practices

### 1. Always Return 200 OK
```python
@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.json
        # Process data
        process_webhook(data)
    except Exception as e:
        logging.error(f"Error: {e}")
        # Still return 200 to acknowledge receipt
    return jsonify({"received": True}), 200
```

### 2. Process Asynchronously
```python
from threading import Thread

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    # Process in background thread
    Thread(target=process_webhook, args=(data,)).start()
    return jsonify({"received": True}), 200
```

### 3. Validate Webhook Data
```python
def validate_webhook(data):
    """Validate webhook payload."""
    required_fields = ['status', 'id', 'track_id']
    return all(field in data for field in required_fields)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if not validate_webhook(data):
        return jsonify({"error": "Invalid payload"}), 400
    # Process...
```

### 4. Implement Retry Logic
```python
# ModelsLab will retry failed webhooks automatically
# But handle idempotency in your endpoint

seen_requests = set()

def process_webhook(data):
    request_id = data.get('id')

    # Check if already processed
    if request_id in seen_requests:
        logging.info(f"Duplicate webhook: {request_id}")
        return

    # Mark as seen
    seen_requests.add(request_id)

    # Process...
```

### 5. Use HTTPS
```python
# Always use HTTPS for webhook URLs
webhook_url = "https://yourserver.com/webhook"  # ✓
webhook_url = "http://yourserver.com/webhook"   # ✗
```

## Webhook Payload Structure

```json
{
  "status": "success",
  "id": "request_id_here",
  "track_id": "your_custom_track_id",
  "output": [
    "https://modelslab.com/path/to/result.jpg"
  ],
  "meta": {
    "prompt": "The original prompt",
    "model_id": "midjourney",
    "seed": 12345
  }
}
```

## Common Use Cases

### Batch Processing

```python
def batch_generate_images(prompts, api_key, webhook_url):
    """Generate multiple images in batch."""
    request_ids = []

    for i, prompt in enumerate(prompts):
        result = generate_image_with_webhook(
            prompt,
            api_key,
            webhook_url,
            track_id=f"batch_{i}"
        )
        request_ids.append(result['request_id'])
        print(f"Submitted {i+1}/{len(prompts)}")

    return request_ids

# Generate 100 images
batch_generate_images(
    ["prompt 1", "prompt 2", ...],  # 100 prompts
    api_key,
    "https://yourserver.com/webhook/batch"
)
```

### User Notification System

```python
from flask import Flask, request, jsonify
import smtplib

@app.route('/webhook/notify', methods=['POST'])
def webhook_with_notification():
    """Webhook that notifies users when complete."""
    data = request.json
    track_id = data.get('track_id')

    # Extract user email from track_id or database
    user_email = get_user_email(track_id)

    if data['status'] == 'success':
        result_url = data['output'][0]
        send_email(
            user_email,
            "Your content is ready!",
            f"Download here: {result_url}"
        )

    return jsonify({"received": True}), 200
```

## Testing Webhooks Locally

```bash
# 1. Install ngrok
brew install ngrok

# 2. Start your webhook server
python webhook_server.py

# 3. Expose with ngrok
ngrok http 8080

# 4. Use the ngrok URL in your API requests
# https://abc123.ngrok.io/webhook/modelslab
```

## Error Handling

```python
@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.json

        if not data:
            logging.error("Empty webhook payload")
            return jsonify({"error": "Empty payload"}), 400

        if data['status'] == 'failed':
            handle_failed_generation(data)
        else:
            handle_successful_generation(data)

        return jsonify({"received": True}), 200

    except Exception as e:
        logging.error(f"Webhook processing error: {e}")
        # Log but still return 200
        return jsonify({"received": True, "error": str(e)}), 200
```

## Resources

- **Webhooks Documentation**: https://docs.modelslab.com/webhooks
- **Supported Endpoints**: Check individual API docs
- **Get API Key**: https://modelslab.com/dashboard

## Related Skills

- All ModelsLab generation skills support webhooks
- `modelslab-sdk-usage` - SDKs have built-in webhook support
