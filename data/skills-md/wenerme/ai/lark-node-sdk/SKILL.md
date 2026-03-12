---
name: lark-node-sdk
description: 'Use when developing with Lark/Feishu Open Platform using @larksuiteoapi/node-sdk, including API calls, event handling, or message card building'
---

# Lark/Feishu Node SDK

Development guide for `@larksuiteoapi/node-sdk`.

## References

| Resource | Link |
|----------|------|
| Official Node SDK | [larksuite/node-sdk](https://github.com/larksuite/node-sdk) |
| Official MCP Reference | [larksuite/lark-openapi-mcp](https://github.com/larksuite/lark-openapi-mcp) |
| Open Platform Docs | [open.feishu.cn](https://open.feishu.cn/document/) |
| Message Card Builder | [Card Builder](https://open.feishu.cn/document/ukTMukTMukTM/uYzM3QjL2MzN04iNzcDN/message-card-builder) |

## Client Setup

```typescript
import * as lark from '@larksuiteoapi/node-sdk';

const client = new lark.Client({
  appId: 'app id',
  appSecret: 'app secret',
  // domain: lark.Domain.Feishu,  // Default. Use lark.Domain.Lark for international
});

// ISV (store app)
const client = new lark.Client({
  appId: 'app id',
  appSecret: 'app secret',
  appType: lark.AppType.ISV,
});
```

| Param | Description | Required | Default |
|-------|-------------|----------|---------|
| appId | App ID | Yes | - |
| appSecret | App Secret | Yes | - |
| domain | Feishu / Lark / custom URL | No | Domain.Feishu |
| appType | SelfBuild / ISV | No | SelfBuild |
| disableTokenCache | Disable token caching | No | false |

## API Calls

Semantic chaining: `client.<domain>.<resource>.<method>`

### Send Messages

```typescript
// Text message
const res = await client.im.message.create({
  params: { receive_id_type: 'chat_id' },  // chat_id | open_id | user_id | union_id | email
  data: {
    receive_id: 'oc_xxx',
    content: JSON.stringify({ text: 'hello world' }),
    msg_type: 'text',
  },
});

// Interactive card
const res = await client.im.message.create({
  params: { receive_id_type: 'chat_id' },
  data: {
    receive_id: 'oc_xxx',
    content: JSON.stringify({
      config: { wide_screen_mode: true },
      header: {
        template: 'blue',
        title: { content: '标题', tag: 'plain_text' },
      },
      elements: [{ tag: 'markdown', content: '**内容**' }],
    }),
    msg_type: 'interactive',
  },
});

// Built-in card helper
const res = await client.im.message.create({
  params: { receive_id_type: 'chat_id' },
  data: {
    receive_id: 'oc_xxx',
    content: lark.messageCard.defaultCard({ title: '标题', content: '内容' }),
    msg_type: 'interactive',
  },
});

// Card template ID
const res = await client.im.message.createByCard({
  params: { receive_id_type: 'chat_id' },
  data: {
    receive_id: 'oc_xxx',
    template_id: 'AAqCxxxxxx',
    template_variable: { title: '标题', content: '内容' },
  },
});
```

### Pagination (Async Iterator)

```typescript
for await (const items of await client.contact.user.listWithIterator({
  params: { department_id: '0', page_size: 20 },
})) {
  console.log(items);
}
```

### File Upload / Download

```typescript
// Upload
const res = await client.im.file.create({
  data: {
    file_type: 'mp4',
    file_name: 'test.mp4',
    file: fs.readFileSync('path/to/file.mp4'),
  },
});

// Download
const resp = await client.im.file.get({ path: { file_key: 'file_key' } });
await resp.writeFile('download.mp4');
// Or: resp.getReadableStream().pipe(fs.createWriteStream('download.mp4'));
```

## Event Handling

### WebSocket (Recommended)

No public IP or tunnel needed — works in local dev.

```typescript
const wsClient = new lark.WSClient({
  appId: 'xxx',
  appSecret: 'xxx',
  loggerLevel: lark.LoggerLevel.info,
});

wsClient.start({
  eventDispatcher: new lark.EventDispatcher({}).register({
    'im.message.receive_v1': async (data) => {
      const { message: { chat_id, content } } = data;
      await client.im.message.create({
        params: { receive_id_type: 'chat_id' },
        data: {
          receive_id: chat_id,
          content: JSON.stringify({ text: `Reply: ${JSON.parse(content).text}` }),
          msg_type: 'text',
        },
      });
    },
  }),
});
```

### Webhook

```typescript
const eventDispatcher = new lark.EventDispatcher({
  encryptKey: 'encrypt key',
}).register({
  'im.message.receive_v1': async (data) => {
    // Handle message
  },
});

// Express
app.use('/webhook/event', lark.adaptExpress(eventDispatcher, { autoChallenge: true }));

// Koa
app.use(lark.adaptKoa('/webhook/event', eventDispatcher, { autoChallenge: true }));
```

## Card Action Handler

```typescript
const cardDispatcher = new lark.CardActionHandler(
  { encryptKey: 'encrypt key', verificationToken: 'verification token' },
  async (data) => {
    // Return new card to update the original
    return {
      header: { title: { tag: 'plain_text', content: 'Done' } },
      elements: [{ tag: 'markdown', content: 'Operation complete' }],
    };
  },
);

app.use('/webhook/card', lark.adaptExpress(cardDispatcher));
```

## Common API Domains

| Domain | Description | Example |
|--------|-------------|---------|
| `im` | Messages & Groups | `client.im.message.create()` |
| `contact` | Contacts | `client.contact.user.list()` |
| `calendar` | Calendar | `client.calendar.event.create()` |
| `drive` | Docs | `client.drive.file.list()` |
| `sheets` | Spreadsheets | `client.sheets.spreadsheet.create()` |
| `bitable` | Base (Multitable) | `client.bitable.app.create()` |
| `approval` | Approval | `client.approval.instance.create()` |
| `attendance` | Attendance | `client.attendance.record.list()` |

## Request Options

```typescript
// ISV: pass tenant_key
await client.im.message.create({ ... }, lark.withTenantKey('tenant key'));

// Custom headers
await client.im.message.create({ ... }, { headers: { 'X-Custom': 'value' } });

// Combine options
await client.im.message.create({ ... }, lark.withAll([
  lark.withTenantToken('tenant token'),
  lark.withTenantKey('tenant key'),
]));
```
