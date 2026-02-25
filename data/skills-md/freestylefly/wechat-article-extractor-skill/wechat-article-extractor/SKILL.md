---
name: wechat-article-extractor
description: Extract metadata and content from WeChat Official Account articles. Use when user needs to parse WeChat article URLs (mp.weixin.qq.com), extract article info (title, author, content, publish time, cover image), or convert WeChat articles to structured data. Supports various article types including posts, videos, images, voice messages, and reposts.
---

# WeChat Article Extractor

Extract metadata and content from WeChat Official Account (微信公众号) articles.

## Capabilities

- Parse WeChat article URLs (`mp.weixin.qq.com`)
- Extract article metadata: title, author, description, publish time
- Extract account info: name, avatar, alias, description
- Get article content (HTML)
- Get cover image URL
- Support multiple article types: post, video, image, voice, text, repost
- Handle various error cases: deleted content, expired links, access limits

## Usage

### Basic Extraction from URL

```javascript
const { extract } = require('./scripts/extract.js');

const result = await extract('https://mp.weixin.qq.com/s?__biz=...');
// Returns: { done: true, code: 0, data: {...} }
```

### Extraction from HTML

```javascript
const html = await fetch(url).then(r => r.text());
const result = await extract(html, { url: sourceUrl });
```

### Options

```javascript
const result = await extract(url, {
  shouldReturnContent: true,      // Return HTML content (default: true)
  shouldReturnRawMeta: false,     // Return raw metadata (default: false)
  shouldFollowTransferLink: true, // Follow migrated account links (default: true)
  shouldExtractMpLinks: false,    // Extract embedded mp.weixin links (default: false)
  shouldExtractTags: false,       // Extract article tags (default: false)
  shouldExtractRepostMeta: false  // Extract repost source info (default: false)
});
```

## Response Format

### Success Response

```javascript
{
  done: true,
  code: 0,
  data: {
    // Account info
    account_name: "公众号名称",
    account_alias: "微信号",
    account_avatar: "头像URL",
    account_description: "功能介绍",
    account_id: "原始ID",
    account_biz: "biz参数",
    account_biz_number: 1234567890,
    account_qr_code: "二维码URL",

    // Article info
    msg_title: "文章标题",
    msg_desc: "文章摘要",
    msg_content: "HTML内容",
    msg_cover: "封面图URL",
    msg_author: "作者",
    msg_type: "post", // post|video|image|voice|text|repost
    msg_has_copyright: true,
    msg_publish_time: Date,
    msg_publish_time_str: "2024/01/15 10:30:00",

    // Link params
    msg_link: "文章链接",
    msg_source_url: "阅读原文链接",
    msg_sn: "sn参数",
    msg_mid: 1234567890,
    msg_idx: 1
  }
}
```

### Error Response

```javascript
{
  done: false,
  code: 1001,
  msg: "无法获取文章信息"
}
```

## Error Codes

| Code | Message | Description |
|------|---------|-------------|
| 1000 | 文章获取失败 | General failure |
| 1001 | 无法获取文章信息 | Missing title or publish time |
| 1002 | 请求失败 | HTTP request failed |
| 1003 | 响应为空 | Empty response |
| 1004 | 访问过于频繁 | Rate limited |
| 1005 | 脚本解析失败 | Script parsing error |
| 1006 | 公众号已迁移 | Account migrated |
| 2001 | 请提供文章内容或链接 | Missing input |
| 2002 | 链接已过期 | Link expired |
| 2003 | 内容涉嫌侵权 | Content removed (copyright) |
| 2004 | 无法获取迁移后的链接 | Migration link failed |
| 2005 | 内容已被发布者删除 | Content deleted by author |
| 2006 | 内容因违规无法查看 | Content blocked |
| 2007 | 内容发送失败 | Failed to send |
| 2008 | 系统出错 | System error |
| 2009 | 不支持的链接 | Unsupported URL |
| 2010 | 内容获取失败 | Content fetch failed |
| 2011 | 涉嫌过度营销 | Marketing/spam content |
| 2012 | 账号已被屏蔽 | Account blocked |
| 2013 | 账号已自主注销 | Account deleted |
| 2014 | 内容被投诉 | Content reported |
| 2015 | 账号处于迁移流程中 | Account migrating |
| 2016 | 冒名侵权 | Impersonation |

## Dependencies

Required npm packages:
- `cheerio` - HTML parsing
- `dayjs` - Date formatting
- `request-promise` - HTTP requests
- `qs` - Query string parsing
- `lodash.unescape` - HTML entities

## Notes

- Handles various WeChat page structures and anti-scraping measures
- Automatically detects article type from page content
- Supports extracting from Sogou WeChat search results (`weixin.sogou.com`)
- Some fields may be null depending on article type and page structure
