---
name: commafeed-api
description: >
  Use this skill whenever the user wants to interact with a CommaFeed RSS reader
  instance via its REST API. Triggers include: listing, subscribing, unsubscribing
  from RSS feeds; reading, starring, or tagging feed entries; managing categories;
  marking entries as read/unread; importing or exporting OPML; managing user settings
  or profile; viewing unread counts; refreshing feeds; fetching feed info by URL;
  administering users on a CommaFeed instance. Also use for requests like "show my
  feeds", "subscribe to RSS feed", "list unread articles", "star this entry",
  "export my feeds as OPML", "mark all as read", "get unread count", or "refresh
  my feeds". Always use this skill for any CommaFeed API interaction.
---

# CommaFeed REST API Skill

Interact with a self-hosted CommaFeed RSS reader instance via its REST API.

## Environment Variables (REQUIRED)

Before making any API calls, ensure these environment variables are set:

| Variable | Description | Example |
|---|---|---|
| `COMMAFEED_HOST` | CommaFeed instance URL (with protocol, no trailing slash) | `https://commafeed.example.com` |
| `COMMAFEED_USER` | CommaFeed username | `admin` |
| `COMMAFEED_PASS` | CommaFeed password | `secretpass` |

```bash
export COMMAFEED_HOST="https://commafeed.example.com"
export COMMAFEED_USER="admin"
export COMMAFEED_PASS="your-password"
```

If these are not set, **ask the user** to provide them before proceeding.

## Authentication

All requests use **HTTP Basic Auth**:

```bash
curl -s -u "$COMMAFEED_USER:$COMMAFEED_PASS" \
  "$COMMAFEED_HOST/rest/category/get" | jq .
```

Every request pattern below assumes:
- Base URL: `$COMMAFEED_HOST/rest`
- Auth: `-u "$COMMAFEED_USER:$COMMAFEED_PASS"`
- Content-Type: `application/json` (for POST requests with JSON body)

Helper alias for examples:

```bash
CF="curl -s -u $COMMAFEED_USER:$COMMAFEED_PASS"
```

---

## API Endpoints

### Categories

| Method | Path | Description |
|---|---|---|
| GET | `/rest/category/get` | Get root category tree (all categories + subscriptions) |
| POST | `/rest/category/add` | Add a new category |
| POST | `/rest/category/modify` | Rename or move a category |
| POST | `/rest/category/delete` | Delete a category |
| POST | `/rest/category/collapse` | Collapse/expand a category in the UI |
| GET | `/rest/category/entries` | Get entries for a category |
| GET | `/rest/category/entriesAsFeed` | Get category entries as RSS/Atom XML |
| POST | `/rest/category/mark` | Mark all entries in a category as read |
| GET | `/rest/category/unreadCount` | Get unread count per subscription |

#### Get category tree (all subscriptions)

Returns the full tree: root category with nested children and feed subscriptions.

```bash
curl -s -u "$COMMAFEED_USER:$COMMAFEED_PASS" \
  "$COMMAFEED_HOST/rest/category/get" | jq .
```

Response — `Category` object:
```json
{
  "id": "all",
  "name": "All",
  "children": [
    {
      "id": "10",
      "parentId": "all",
      "name": "Tech",
      "children": [],
      "feeds": [
        {
          "id": 42,
          "name": "Hacker News",
          "feedUrl": "https://news.ycombinator.com/rss",
          "feedLink": "https://news.ycombinator.com",
          "iconUrl": "/rest/feed/favicon/42",
          "unread": 15,
          "categoryId": "10",
          "position": 0,
          "newestItemTime": "2026-03-07T10:30:00Z",
          "errorCount": 0,
          "lastRefresh": "2026-03-07T10:00:00Z",
          "nextRefresh": "2026-03-07T10:15:00Z"
        }
      ],
      "expanded": true,
      "position": 0
    }
  ],
  "feeds": [],
  "expanded": true,
  "position": 0
}
```

#### Add a category

```bash
curl -s -X POST \
  -u "$COMMAFEED_USER:$COMMAFEED_PASS" \
  -H "Content-Type: application/json" \
  -d '{"name": "Technology", "parentId": "all"}' \
  "$COMMAFEED_HOST/rest/category/add" | jq .
```

Request body — `AddCategoryRequest`:
- `name` (string, required, max 128 chars) — category name
- `parentId` (string, optional) — parent category ID, omit for root level

Response: category ID (integer).

#### Modify a category

```bash
curl -s -X POST \
  -u "$COMMAFEED_USER:$COMMAFEED_PASS" \
  -H "Content-Type: application/json" \
  -d '{"id": 10, "name": "Tech News", "parentId": "all", "position": 0}' \
  "$COMMAFEED_HOST/rest/category/modify"
```

Request body — `CategoryModificationRequest`:
- `id` (integer, required) — category ID
- `name` (string) — new name
- `parentId` (string) — new parent category ID
- `position` (integer) — position in parent

#### Delete a category

```bash
curl -s -X POST \
  -u "$COMMAFEED_USER:$COMMAFEED_PASS" \
  -H "Content-Type: application/json" \
  -d '{"id": 10}' \
  "$COMMAFEED_HOST/rest/category/delete"
```

Request body — `IDRequest`:
- `id` (integer, required) — category ID

#### Get category entries

```bash
curl -s -u "$COMMAFEED_USER:$COMMAFEED_PASS" \
  "$COMMAFEED_HOST/rest/category/entries?id=all&readType=unread&limit=20&order=desc" | jq .
```

Query parameters:
- `id` (required) — category ID, `"all"` for all feeds, or `"starred"` for starred entries
- `readType` (required) — `all` or `unread`
- `limit` (integer, default 20, max 1000) — entries per page
- `offset` (integer, default 0) — pagination offset
- `order` (string, default `desc`) — `desc` or `asc`
- `newerThan` (long) — Unix timestamp in ms, only entries newer than this
- `keywords` (string) — search filter
- `tag` (string) — filter by tag
- `excludedSubscriptionIds` (string) — comma-separated subscription IDs to exclude

Response — `Entries` object:
```json
{
  "name": "All",
  "entries": [
    {
      "id": "feed/42:entry/abc123",
      "guid": "https://example.com/article-1",
      "title": "Article Title",
      "content": "<p>Article HTML content...</p>",
      "author": "John Doe",
      "date": "2026-03-07T09:00:00Z",
      "insertedDate": "2026-03-07T09:05:00Z",
      "url": "https://example.com/article-1",
      "feedId": "42",
      "feedName": "Example Feed",
      "feedUrl": "https://example.com/rss",
      "feedLink": "https://example.com",
      "iconUrl": "/rest/feed/favicon/42",
      "read": false,
      "starred": false,
      "markable": true,
      "tags": [],
      "categories": "tech, news",
      "rtl": false,
      "enclosureUrl": null,
      "enclosureType": null,
      "mediaThumbnailUrl": null
    }
  ],
  "timestamp": 1741339200000,
  "hasMore": true,
  "offset": 0,
  "limit": 20,
  "errorCount": 0,
  "ignoredReadStatus": false
}
```

#### Get unread counts

```bash
curl -s -u "$COMMAFEED_USER:$COMMAFEED_PASS" \
  "$COMMAFEED_HOST/rest/category/unreadCount" | jq .
```

Response — array of `UnreadCount`:
```json
[
  {"feedId": 42, "unreadCount": 15},
  {"feedId": 55, "unreadCount": 3}
]
```

#### Mark category as read

```bash
curl -s -X POST \
  -u "$COMMAFEED_USER:$COMMAFEED_PASS" \
  -H "Content-Type: application/json" \
  -d '{"id": "all", "olderThan": 1741339200000, "read": true}' \
  "$COMMAFEED_HOST/rest/category/mark"
```

Request body — `MarkRequest`:
- `id` (string, required) — category ID or `"all"`
- `read` (boolean) — true to mark read, false for unread
- `olderThan` (long) — timestamp, mark only entries older than this
- `insertedBefore` (long) — mark only entries inserted before this
- `keywords` (string) — filter by keywords

#### Collapse/expand category

```bash
curl -s -X POST \
  -u "$COMMAFEED_USER:$COMMAFEED_PASS" \
  -H "Content-Type: application/json" \
  -d '{"id": 10, "collapse": true}' \
  "$COMMAFEED_HOST/rest/category/collapse"
```

---

### Feed Subscriptions

| Method | Path | Description |
|---|---|---|
| POST | `/rest/feed/subscribe` | Subscribe to a feed |
| POST | `/rest/feed/unsubscribe` | Unsubscribe from a feed |
| POST | `/rest/feed/modify` | Modify subscription (rename, move, filter) |
| GET | `/rest/feed/get/{id}` | Get subscription details |
| POST | `/rest/feed/fetch` | Fetch feed info by URL (preview before subscribing) |
| GET | `/rest/feed/refreshAll` | Queue all feeds for refresh |
| GET | `/rest/feed/entries` | Get entries for a specific feed |
| GET | `/rest/feed/entriesAsFeed` | Get feed entries as RSS/Atom XML |
| POST | `/rest/feed/mark` | Mark feed entries as read |
| GET | `/rest/feed/favicon/{id}` | Get feed favicon |
| GET | `/rest/feed/export` | Export all subscriptions as OPML |
| POST | `/rest/feed/import` | Import subscriptions from OPML file |

#### Subscribe to a feed

```bash
curl -s -X POST \
  -u "$COMMAFEED_USER:$COMMAFEED_PASS" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/rss",
    "title": "Example Blog",
    "categoryId": 10
  }' \
  "$COMMAFEED_HOST/rest/feed/subscribe" | jq .
```

Request body — `SubscribeRequest`:
- `url` (string, required) — feed URL
- `title` (string, required) — display name
- `categoryId` (integer) — target category ID

Response: subscription ID (integer).

#### Unsubscribe from a feed

```bash
curl -s -X POST \
  -u "$COMMAFEED_USER:$COMMAFEED_PASS" \
  -H "Content-Type: application/json" \
  -d '{"id": 42}' \
  "$COMMAFEED_HOST/rest/feed/unsubscribe"
```

#### Modify a subscription

```bash
curl -s -X POST \
  -u "$COMMAFEED_USER:$COMMAFEED_PASS" \
  -H "Content-Type: application/json" \
  -d '{
    "id": 42,
    "name": "New Feed Name",
    "categoryId": 10,
    "position": 0,
    "filter": "title.contains(\"important\")",
    "pushNotificationsEnabled": false,
    "autoMarkAsReadAfterDays": 30
  }' \
  "$COMMAFEED_HOST/rest/feed/modify"
```

Request body — `FeedModificationRequest`:
- `id` (integer, required) — subscription ID
- `name` (string) — new display name
- `categoryId` (integer) — move to a different category
- `position` (integer) — position in category
- `filter` (string) — CEL expression to auto-mark entries as read
- `pushNotificationsEnabled` (boolean) — enable push notifications
- `autoMarkAsReadAfterDays` (integer) — auto-mark read after N days (null to disable)

#### Get subscription details

```bash
curl -s -u "$COMMAFEED_USER:$COMMAFEED_PASS" \
  "$COMMAFEED_HOST/rest/feed/get/42" | jq .
```

Response — `Subscription` object:
```json
{
  "id": 42,
  "name": "Hacker News",
  "message": null,
  "errorCount": 0,
  "lastRefresh": "2026-03-07T10:00:00Z",
  "nextRefresh": "2026-03-07T10:15:00Z",
  "feedUrl": "https://news.ycombinator.com/rss",
  "feedLink": "https://news.ycombinator.com",
  "iconUrl": "/rest/feed/favicon/42",
  "unread": 15,
  "categoryId": "10",
  "position": 0,
  "newestItemTime": "2026-03-07T10:30:00Z",
  "filter": null,
  "pushNotificationsEnabled": false,
  "autoMarkAsReadAfterDays": null
}
```

#### Fetch feed info (preview)

```bash
curl -s -X POST \
  -u "$COMMAFEED_USER:$COMMAFEED_PASS" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/rss"}' \
  "$COMMAFEED_HOST/rest/feed/fetch" | jq .
```

Request body — `FeedInfoRequest`:
- `url` (string, required, 1–4096 chars) — feed URL to probe

Response — `FeedInfo`: title, url, link for the discovered feed.

#### Refresh all feeds

```bash
curl -s -u "$COMMAFEED_USER:$COMMAFEED_PASS" \
  "$COMMAFEED_HOST/rest/feed/refreshAll"
```

> **Note:** Returns 429 Too Many Requests if called too frequently.

#### Get feed entries

```bash
curl -s -u "$COMMAFEED_USER:$COMMAFEED_PASS" \
  "$COMMAFEED_HOST/rest/feed/entries?id=42&readType=unread&limit=50&order=desc" | jq .
```

Query parameters (same pattern as category entries):
- `id` (required) — subscription ID
- `readType` (required) — `all` or `unread`
- `limit` (integer, default 20, max 1000)
- `offset` (integer, default 0)
- `order` — `desc` or `asc`
- `newerThan` (long) — Unix timestamp in ms
- `keywords` (string) — search filter

Response: `Entries` object (same structure as category entries).

#### Mark feed as read

```bash
curl -s -X POST \
  -u "$COMMAFEED_USER:$COMMAFEED_PASS" \
  -H "Content-Type: application/json" \
  -d '{"id": "42", "read": true}' \
  "$COMMAFEED_HOST/rest/feed/mark"
```

#### OPML Export

```bash
curl -s -u "$COMMAFEED_USER:$COMMAFEED_PASS" \
  "$COMMAFEED_HOST/rest/feed/export" -o subscriptions.opml
```

Response: OPML XML file.

#### OPML Import

```bash
curl -s -X POST \
  -u "$COMMAFEED_USER:$COMMAFEED_PASS" \
  -F "file=@subscriptions.opml" \
  "$COMMAFEED_HOST/rest/feed/import"
```

> **Note:** Uses `multipart/form-data`, not JSON.

---

### Entries (individual entry operations)

| Method | Path | Description |
|---|---|---|
| POST | `/rest/entry/mark` | Mark a single entry as read/unread |
| POST | `/rest/entry/markMultiple` | Mark multiple entries at once |
| POST | `/rest/entry/star` | Star/unstar an entry |
| POST | `/rest/entry/tag` | Set tags on an entry |
| GET | `/rest/entry/tags` | Get all user tags |

#### Mark entry as read/unread

```bash
curl -s -X POST \
  -u "$COMMAFEED_USER:$COMMAFEED_PASS" \
  -H "Content-Type: application/json" \
  -d '{"id": "feed/42:entry/abc123", "read": true}' \
  "$COMMAFEED_HOST/rest/entry/mark"
```

Request body — `MarkRequest`:
- `id` (string, required) — entry ID
- `read` (boolean) — true = read, false = unread

#### Mark multiple entries

```bash
curl -s -X POST \
  -u "$COMMAFEED_USER:$COMMAFEED_PASS" \
  -H "Content-Type: application/json" \
  -d '{
    "requests": [
      {"id": "feed/42:entry/abc123", "read": true},
      {"id": "feed/42:entry/def456", "read": true}
    ]
  }' \
  "$COMMAFEED_HOST/rest/entry/markMultiple"
```

#### Star/unstar an entry

```bash
curl -s -X POST \
  -u "$COMMAFEED_USER:$COMMAFEED_PASS" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "feed/42:entry/abc123",
    "feedId": 42,
    "starred": true
  }' \
  "$COMMAFEED_HOST/rest/entry/star"
```

Request body — `StarRequest`:
- `id` (string, required) — entry ID
- `feedId` (integer, required) — feed subscription ID
- `starred` (boolean, required) — true to star, false to unstar

#### Tag an entry

```bash
curl -s -X POST \
  -u "$COMMAFEED_USER:$COMMAFEED_PASS" \
  -H "Content-Type: application/json" \
  -d '{
    "entryId": 12345,
    "tags": ["important", "read-later"]
  }' \
  "$COMMAFEED_HOST/rest/entry/tag"
```

Request body — `TagRequest`:
- `entryId` (integer, required) — entry ID
- `tags` (array of strings, required) — tags to assign (replaces existing)

#### Get all user tags

```bash
curl -s -u "$COMMAFEED_USER:$COMMAFEED_PASS" \
  "$COMMAFEED_HOST/rest/entry/tags" | jq .
```

Response: array of tag strings.

---

### User Profile & Settings

| Method | Path | Description |
|---|---|---|
| GET | `/rest/user/profile` | Get user profile |
| POST | `/rest/user/profile` | Update user profile |
| POST | `/rest/user/profile/deleteAccount` | Delete own account |
| GET | `/rest/user/settings` | Get user settings |
| POST | `/rest/user/settings` | Save user settings |

#### Get profile

```bash
curl -s -u "$COMMAFEED_USER:$COMMAFEED_PASS" \
  "$COMMAFEED_HOST/rest/user/profile" | jq .
```

Response — `UserModel`:
```json
{
  "id": 1,
  "name": "admin",
  "email": "admin@example.com",
  "apiKey": "abc-123-def-456",
  "enabled": true,
  "admin": true
}
```

#### Update profile

```bash
curl -s -X POST \
  -u "$COMMAFEED_USER:$COMMAFEED_PASS" \
  -H "Content-Type: application/json" \
  -d '{
    "currentPassword": "old-pass",
    "newPassword": "new-pass",
    "newEmail": "new@example.com"
  }' \
  "$COMMAFEED_HOST/rest/user/profile"
```

Request body — `ProfileModificationRequest`:
- `currentPassword` (string, required) — current password for verification
- `newPassword` (string) — new password
- `newEmail` (string) — new email
- `newApiKey` (boolean) — true to regenerate API key

#### Get settings

```bash
curl -s -u "$COMMAFEED_USER:$COMMAFEED_PASS" \
  "$COMMAFEED_HOST/rest/user/settings" | jq .
```

Response — `Settings`:
```json
{
  "language": "en",
  "readingMode": "unread",
  "readingOrder": "desc",
  "showRead": true,
  "scrollMarks": true,
  "scrollSpeed": 400,
  "scrollMode": "if_needed",
  "customCss": "",
  "customJs": "",
  "entriesToKeepOnTopWhenScrolling": 1,
  "starIconDisplayMode": "always",
  "externalLinkIconDisplayMode": "always",
  "markAllAsReadConfirmation": true,
  "markAllAsReadNavigateToNextUnread": false,
  "customContextMenu": true,
  "mobileFooter": false,
  "unreadCountTitle": true,
  "unreadCountFavicon": true,
  "disablePullToRefresh": false,
  "primaryColor": null,
  "sharingSettings": {
    "email": false,
    "gmail": false,
    "facebook": false,
    "twitter": false,
    "tumblr": false,
    "pocket": false,
    "instapaper": false,
    "buffer": false
  }
}
```

Settings enums:
- `readingMode`: `all`, `unread`
- `readingOrder`: `asc`, `desc`
- `scrollMode`: `always`, `never`, `if_needed`
- `starIconDisplayMode` / `externalLinkIconDisplayMode`: `always`, `never`, `on_desktop`, `on_mobile`

#### Save settings

```bash
curl -s -X POST \
  -u "$COMMAFEED_USER:$COMMAFEED_PASS" \
  -H "Content-Type: application/json" \
  -d '{
    "language": "en",
    "readingMode": "unread",
    "readingOrder": "desc",
    "showRead": false,
    "scrollMarks": true
  }' \
  "$COMMAFEED_HOST/rest/user/settings"
```

---

### Server Info

| Method | Path | Description |
|---|---|---|
| GET | `/rest/server/get` | Get server information (no auth required) |
| GET | `/rest/server/proxy` | Proxy an image through the server |

#### Get server info

```bash
curl -s "$COMMAFEED_HOST/rest/server/get" | jq .
```

Response — `ServerInfo`:
```json
{
  "announcement": "",
  "version": "5.x.x",
  "gitCommit": "abc1234",
  "loginPageTitle": "CommaFeed",
  "allowRegistrations": false,
  "googleAnalyticsTrackingCode": null,
  "smtpEnabled": false,
  "demoAccountEnabled": false,
  "websocketEnabled": true,
  "websocketPingInterval": 15000,
  "treeMode": "unread"
}
```

#### Proxy image

```bash
curl -s -u "$COMMAFEED_USER:$COMMAFEED_PASS" \
  "$COMMAFEED_HOST/rest/server/proxy?u=https://example.com/image.png" \
  -o proxied-image.png
```

---

### Admin Endpoints

> Require `ADMIN` role.

| Method | Path | Description |
|---|---|---|
| GET | `/rest/admin/metrics` | Get server metrics |
| GET | `/rest/admin/user/getAll` | List all users |
| GET | `/rest/admin/user/get/{id}` | Get user by ID |
| POST | `/rest/admin/user/save` | Create or update a user |
| POST | `/rest/admin/user/delete` | Delete a user |

#### Get server metrics

```bash
curl -s -u "$COMMAFEED_USER:$COMMAFEED_PASS" \
  "$COMMAFEED_HOST/rest/admin/metrics" | jq .
```

#### List all users

```bash
curl -s -u "$COMMAFEED_USER:$COMMAFEED_PASS" \
  "$COMMAFEED_HOST/rest/admin/user/getAll" | jq .
```

Response: array of `UserModel`.

#### Get user by ID

```bash
curl -s -u "$COMMAFEED_USER:$COMMAFEED_PASS" \
  "$COMMAFEED_HOST/rest/admin/user/get/1" | jq .
```

#### Create / update user

```bash
curl -s -X POST \
  -u "$COMMAFEED_USER:$COMMAFEED_PASS" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "newuser",
    "password": "securepass123",
    "email": "user@example.com",
    "enabled": true,
    "admin": false
  }' \
  "$COMMAFEED_HOST/rest/admin/user/save"
```

Request body — `AdminSaveUserRequest`:
- `name` (string, required) — username
- `password` (string) — password (required for new users)
- `email` (string) — email address
- `enabled` (boolean, required) — account active
- `admin` (boolean, required) — admin role

#### Delete user

```bash
curl -s -X POST \
  -u "$COMMAFEED_USER:$COMMAFEED_PASS" \
  -H "Content-Type: application/json" \
  -d '{"id": 5}' \
  "$COMMAFEED_HOST/rest/admin/user/delete"
```

---

### Registration & Password Reset

| Method | Path | Description |
|---|---|---|
| POST | `/rest/user/register` | Register new account (if allowed) |
| POST | `/rest/user/initialSetup` | Create initial admin (first-run only) |
| POST | `/rest/user/passwordReset` | Request password reset email |
| POST | `/rest/user/passwordResetCallback` | Confirm password reset with token |

#### Register

```bash
curl -s -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "name": "newuser",
    "password": "mypassword",
    "email": "user@example.com"
  }' \
  "$COMMAFEED_HOST/rest/user/register"
```

Request: `name` (3–32 chars), `password`, `email` (all required).

---

## Common Patterns

### List all feeds with unread counts

```bash
curl -s -u "$COMMAFEED_USER:$COMMAFEED_PASS" \
  "$COMMAFEED_HOST/rest/category/get" | \
  jq '[.. | .feeds? // empty | .[] | {id, name, unread, feedUrl}]'
```

### Get all unread entries across all feeds

```bash
curl -s -u "$COMMAFEED_USER:$COMMAFEED_PASS" \
  "$COMMAFEED_HOST/rest/category/entries?id=all&readType=unread&limit=100" | \
  jq '.entries[] | {title, url, feedName, date}'
```

### Get starred entries

```bash
curl -s -u "$COMMAFEED_USER:$COMMAFEED_PASS" \
  "$COMMAFEED_HOST/rest/category/entries?id=starred&readType=all&limit=50" | \
  jq '.entries[] | {title, url, starred, date}'
```

### Search entries by keyword

```bash
curl -s -u "$COMMAFEED_USER:$COMMAFEED_PASS" \
  "$COMMAFEED_HOST/rest/category/entries?id=all&readType=all&keywords=kubernetes&limit=50" | \
  jq '.entries[] | {title, url, feedName}'
```

### Mark all entries as read

```bash
# Get current timestamp
TS=$(date +%s)000
curl -s -X POST \
  -u "$COMMAFEED_USER:$COMMAFEED_PASS" \
  -H "Content-Type: application/json" \
  -d "{\"id\": \"all\", \"read\": true, \"olderThan\": $TS}" \
  "$COMMAFEED_HOST/rest/category/mark"
```

### Subscribe to a feed and put it in a category

```bash
# 1. Fetch feed info to verify URL
curl -s -X POST \
  -u "$COMMAFEED_USER:$COMMAFEED_PASS" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://blog.example.com/feed"}' \
  "$COMMAFEED_HOST/rest/feed/fetch" | jq .

# 2. Subscribe
curl -s -X POST \
  -u "$COMMAFEED_USER:$COMMAFEED_PASS" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://blog.example.com/feed",
    "title": "Example Blog",
    "categoryId": 10
  }' \
  "$COMMAFEED_HOST/rest/feed/subscribe" | jq .
```

### Export OPML backup

```bash
curl -s -u "$COMMAFEED_USER:$COMMAFEED_PASS" \
  "$COMMAFEED_HOST/rest/feed/export" -o "commafeed-backup-$(date +%Y%m%d).opml"
```

### Paginate through all entries

```bash
OFFSET=0
LIMIT=100
while true; do
  RESPONSE=$(curl -s -u "$COMMAFEED_USER:$COMMAFEED_PASS" \
    "$COMMAFEED_HOST/rest/category/entries?id=all&readType=all&limit=$LIMIT&offset=$OFFSET")

  COUNT=$(echo "$RESPONSE" | jq '.entries | length')
  HAS_MORE=$(echo "$RESPONSE" | jq '.hasMore')

  echo "$RESPONSE" | jq '.entries[] | {title, date, feedName}'

  if [ "$HAS_MORE" = "false" ] || [ "$COUNT" -eq 0 ]; then
    break
  fi

  OFFSET=$((OFFSET + LIMIT))
done
```

### Get entries by tag

```bash
curl -s -u "$COMMAFEED_USER:$COMMAFEED_PASS" \
  "$COMMAFEED_HOST/rest/category/entries?id=all&readType=all&tag=important&limit=50" | \
  jq '.entries[] | {title, url, tags}'
```

---

## Node.js Example

```javascript
const COMMAFEED_HOST = process.env.COMMAFEED_HOST;
const COMMAFEED_USER = process.env.COMMAFEED_USER;
const COMMAFEED_PASS = process.env.COMMAFEED_PASS;

const AUTH = 'Basic ' + Buffer.from(`${COMMAFEED_USER}:${COMMAFEED_PASS}`).toString('base64');

async function cfApi(method, path, body = null) {
  const url = `${COMMAFEED_HOST}/rest${path}`;
  const options = {
    method,
    headers: {
      'Authorization': AUTH,
      'Content-Type': 'application/json',
    },
  };
  if (body) options.body = JSON.stringify(body);
  const res = await fetch(url, options);
  if (!res.ok) throw new Error(`CommaFeed API ${res.status}: ${await res.text()}`);
  const text = await res.text();
  return text ? JSON.parse(text) : null;
}

// Get all subscriptions
const tree = await cfApi('GET', '/category/get');
console.log(tree);

// Get unread entries
const entries = await cfApi('GET', '/category/entries?id=all&readType=unread&limit=20');
for (const e of entries.entries) {
  console.log(`[${e.feedName}] ${e.title} — ${e.url}`);
}

// Subscribe to a feed
const subId = await cfApi('POST', '/feed/subscribe', {
  url: 'https://example.com/rss',
  title: 'Example Feed',
});
console.log('Subscribed, ID:', subId);

// Star an entry
await cfApi('POST', '/entry/star', {
  id: entries.entries[0].id,
  feedId: parseInt(entries.entries[0].feedId),
  starred: true,
});
```

## Python Example

```python
import os
import requests

COMMAFEED_HOST = os.environ["COMMAFEED_HOST"]
COMMAFEED_USER = os.environ["COMMAFEED_USER"]
COMMAFEED_PASS = os.environ["COMMAFEED_PASS"]

AUTH = (COMMAFEED_USER, COMMAFEED_PASS)
HEADERS = {"Content-Type": "application/json"}

def cf_api(method, path, json=None):
    url = f"{COMMAFEED_HOST}/rest{path}"
    resp = requests.request(method, url, auth=AUTH, headers=HEADERS, json=json)
    resp.raise_for_status()
    return resp.json() if resp.text else None

# Get category tree
tree = cf_api("GET", "/category/get")
for cat in tree["children"]:
    print(f"Category: {cat['name']}")
    for feed in cat["feeds"]:
        print(f"  {feed['name']} — unread: {feed['unread']}")

# Get unread entries
entries = cf_api("GET", "/category/entries?id=all&readType=unread&limit=20")
for e in entries["entries"]:
    print(f"[{e['feedName']}] {e['title']}")

# Subscribe to a feed
sub_id = cf_api("POST", "/feed/subscribe", {
    "url": "https://example.com/rss",
    "title": "Example Feed",
})
print(f"Subscribed, ID: {sub_id}")

# Export OPML
resp = requests.get(f"{COMMAFEED_HOST}/rest/feed/export", auth=AUTH)
with open("backup.opml", "w") as f:
    f.write(resp.text)
```

---

## Error Handling

| Code | Meaning |
|---|---|
| 200 | Success |
| 400 | Bad request (missing/invalid fields) |
| 401 | Not authorized (wrong credentials) |
| 403 | Forbidden (insufficient role — need ADMIN) |
| 404 | Resource not found (wrong feed/entry/category ID) |
| 429 | Too many requests (refreshAll rate limit) |
| 500 | Server error |

---

## Implementation Notes

- Always read `COMMAFEED_HOST`, `COMMAFEED_USER`, `COMMAFEED_PASS` from environment variables — never hardcode
- Authentication is **HTTP Basic Auth**, not API key headers
- The `/rest/server/get` endpoint does **not** require authentication
- Entry IDs follow the format `feed/{feedId}:entry/{guid}` — preserve them as strings
- Timestamps are in milliseconds (Unix epoch) for `newerThan` / `olderThan` parameters
- OPML import uses `multipart/form-data`, all other POST endpoints use `application/json`
- The `readType` parameter is **required** for entry listing endpoints
- Maximum `limit` is 1000 entries per request — use `offset` + `hasMore` for pagination
- `id=all` means all feeds, `id=starred` means starred entries in category endpoints
- Tags replace the full tag list on an entry — send the complete desired set
- CEL filter expressions on subscriptions auto-mark non-matching entries as read
