---
name: feishu-image
description: Send images and screenshots via Feishu (Lark) messaging platform. Use when the user asks to send screenshots, images, or any visual content through Feishu. This skill handles the complete workflow of uploading images to Feishu servers and delivering them to the specified recipient. Works both within OpenClaw (reads config automatically) and as a standalone tool (requires manual credential setup).
---

# Feishu Image Sender

Send images to Feishu (Lark) conversations. This skill works both inside OpenClaw and as a standalone CLI tool.

## When to use this skill

- User asks to "截图发给我" (send me a screenshot)
- User wants to share any image file through Feishu
- Need to send visual content (charts, diagrams, photos) via Feishu
- OpenClaw's built-in message tool fails to send images

## Configuration

### For OpenClaw Users

When running inside OpenClaw, this skill automatically reads credentials from OpenClaw's Feishu configuration. No manual setup required.

### For Standalone Usage

Set the following environment variables:

```bash
export FEISHU_APP_ID="cli_xxxxxxxxxxxxxxxx"
export FEISHU_APP_SECRET="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

Or create a `.env` file in your project root:

```
FEISHU_APP_ID=cli_xxxxxxxxxxxxxxxx
FEISHU_APP_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**Note**: If running outside OpenClaw without credentials configured, this skill will display a clear error message with setup instructions.

### Feishu App Setup

1. Go to [Feishu Developer Console](https://open.feishu.cn/app)
2. Create a new app (Enterprise self-built app)
3. Enable the following permissions:
   - `im:resource` - Upload images
   - `im:message` - Send messages
4. Get your App ID and App Secret from the app credentials page
5. Publish the app and make it available to your organization

## Usage

### As a Skill in OpenClaw

The skill will automatically use OpenClaw's Feishu configuration:

```javascript
// Example: User asks to "send me a screenshot"
// The skill will automatically:
// 1. Read OpenClaw config for Feishu credentials
// 2. Upload the screenshot to Feishu
// 3. Send it to the user
```

### As a CLI Tool

Send an image to a Feishu user:

```bash
node feishu-image.js --image /path/to/screenshot.png --to ou_xxxxxxxx
```

With an optional message:

```bash
node feishu-image.js --image chart.png --to ou_xxxxxxxx --text "Q4 Sales Report"
```

Send to a chat group:

```bash
node feishu-image.js --image announcement.png --to oc_xxxxxxxx --chat
```

### As a Node.js Library

```javascript
const { FeishuImage } = require('./scripts/feishu-image.js');

const sender = new FeishuImage({
  appId: 'cli_xxxxxxxxxxxxxxxx',
  appSecret: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
});

// Send image to a user
await sender.sendImage({
  imagePath: '/path/to/screenshot.png',
  receiveId: 'ou_xxxxxxxx',
  receiveType: 'user'
});

// Send image with text
await sender.sendImage({
  imagePath: '/path/to/chart.png',
  receiveId: 'ou_xxxxxxxx',
  receiveType: 'user',
  text: 'Here is the sales report'
});
```

## CLI Reference

### Options

| Option | Short | Description | Required |
|--------|-------|-------------|----------|
| `--image` | `-i` | Path to the image file | Yes |
| `--to` | `-t` | Recipient's Feishu open_id or chat_id | Yes |
| `--text` | | Optional text message to include | No |
| `--chat` | `-c` | Send to a chat group (default: user) | No |
| `--help` | `-h` | Show help message | No |

### Examples

```bash
# Basic usage
node feishu-image.js -i screenshot.png -t ou_123456

# With message
node feishu-image.js --image chart.png --to ou_123456 --text "Q4 Report"

# To group chat
node feishu-image.js -i announcement.png -t oc_789012 --chat
```

## Library API Reference

### `new FeishuImage(config)`

Creates a new Feishu Image sender instance.

**Parameters:**
- `config.appId` (string): Feishu app ID
- `config.appSecret` (string): Feishu app secret
- `config.baseUrl` (string, optional): API base URL, defaults to 'https://open.feishu.cn/open-apis'

**Example:**
```javascript
const sender = new FeishuImage({
  appId: process.env.FEISHU_APP_ID,
  appSecret: process.env.FEISHU_APP_SECRET
});
```

### `async sendImage(options)`

Uploads an image and sends it to a Feishu conversation.

**Parameters:**
- `options.imagePath` (string, required): Path to the local image file
- `options.receiveId` (string, required): Recipient's open_id (for users) or chat_id (for groups)
- `options.receiveType` (string, optional): 'user' or 'chat', defaults to 'user'
- `options.text` (string, optional): Optional text message to send with the image

**Returns:** Promise<string> - The ID of the sent message

**Throws:**
- `FeishuImageError` - Various error codes: MISSING_CREDENTIALS, AUTH_FAILED, FILE_NOT_FOUND, UPLOAD_FAILED, SEND_FAILED

**Example:**
```javascript
try {
  const messageId = await sender.sendImage({
    imagePath: '/path/to/screenshot.png',
    receiveId: 'ou_xxxxxxxx',
    receiveType: 'user',
    text: 'Here is the screenshot you requested'
  });
  console.log('Image sent successfully, message ID:', messageId);
} catch (error) {
  console.error('Failed to send image:', error.message);
}
```

## Error Handling

All errors are instances of `FeishuImageError` with specific error codes:

| Error Code | Description | Solution |
|------------|-------------|----------|
| `MISSING_CREDENTIALS` | FEISHU_APP_ID or FEISHU_APP_SECRET not set | Set environment variables or pass to constructor |
| `AUTH_FAILED` | Authentication with Feishu API failed | Check app_id and app_secret are correct |
| `FILE_NOT_FOUND` | Image file does not exist | Check the image path is correct |
| `UPLOAD_FAILED` | Image upload to Feishu failed | Check network connection and file size limits |
| `SEND_FAILED` | Message sending failed | Check recipient ID and permissions |

**Example error handling:**

```javascript
const { FeishuImage, FeishuImageError } = require('./scripts/feishu-image.js');

try {
  await sender.sendImage({ ... });
} catch (error) {
  if (error instanceof FeishuImageError) {
    switch (error.code) {
      case 'MISSING_CREDENTIALS':
        console.error('Please set FEISHU_APP_ID and FEISHU_APP_SECRET');
        break;
      case 'AUTH_FAILED':
        console.error('Invalid credentials. Check your app ID and secret.');
        break;
      case 'FILE_NOT_FOUND':
        console.error(`Image file not found: ${error.details.path}`);
        break;
      default:
        console.error(`Error: ${error.message}`);
    }
  } else {
    console.error('Unexpected error:', error);
  }
}
```

## Limitations

- Image size: Subject to Feishu API limits (check Feishu documentation for current limits)
- Supported formats: PNG, JPG, GIF (as supported by Feishu)
- Rate limiting: Subject to Feishu API rate limits

## See Also

- [Feishu Open Platform Documentation](https://open.feishu.cn/document/)
- [Feishu Image Upload API](https://open.feishu.cn/document/server-docs/im-v1/image/create)
- [Feishu Message Send API](https://open.feishu.cn/document/server-docs/im-v1/message/create)
- [Peekaboo - Screenshot Tool](https://github.com/your-org/peekaboo) (if applicable)