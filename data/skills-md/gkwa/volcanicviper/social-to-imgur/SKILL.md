---
name: social-to-imgur
description: Download the thumbnail/cover image from a social media post (Instagram, Facebook, or any yt-dlp-supported platform) and upload it to Imgur, returning a permanent URL. Use when the user shares a social media URL and wants a permanent image link.
---

## Requirements

- `uvx` (comes with `uv`) — used to run `yt-dlp` without installing it
- Imgur Client ID stored in the macOS keychain under service name `imgur-api`

## Getting a new Imgur Client ID

Register a new application at https://api.imgur.com/oauth2/addclient

Choose "OAuth 2 authorization without a callback URL" as the authorization type.

The Client ID is shown immediately after registration — no secret is needed for anonymous uploads.

## Installing the Client ID in the keychain

Store the Client ID in the macOS keychain using the service name `imgur-api`:

```
security add-generic-password -s imgur-api -a "$USER" -w "your_client_id_here"
```

To verify it was stored correctly:

```
security find-generic-password -s imgur-api -w
```

To update an existing entry:

```
security add-generic-password -U -s imgur-api -a "$USER" -w "your_client_id_here"
```

## Social to Imgur Workflow

When the user shares a social media URL (Instagram, Facebook, or any yt-dlp-supported platform) and wants a permanent image URL, follow these steps.

### Step 1: Get the thumbnail URL

```
uvx yt-dlp --get-thumbnail "<post_url>"
```

Save the output — it is the expiring CDN URL for the cover image.

### Step 2: Download the image

Generate a random temp filename:

```
mktemp /tmp/social_XXXXXX.jpg
```

Use the path it returns for all subsequent steps.

```
curl -sL "<thumbnail_url>" -o "<tempfile>"
```

Verify it is a JPEG:

```
file "<tempfile>"
```

If the file is not a JPEG, stop and tell the user what file type was returned.

### Step 3: Upload to Imgur

Fetch the Client ID from the macOS keychain:

```
security find-generic-password -s imgur-api -w
```

If the command fails, stop and tell the user to add the Client ID to the keychain:

```
security add-generic-password -s imgur-api -a "$USER" -w "your_client_id_here"
```

Upload:

```
curl -s -X POST -H "Authorization: Client-ID <client_id>" -F "image=@<tempfile>" https://api.imgur.com/3/image
```

### Step 4: Extract and return the URL

Parse the JSON response and extract the `link` field.

Print the permanent Imgur URL to the user.

If the upload fails, show the full API response so the user can debug.
