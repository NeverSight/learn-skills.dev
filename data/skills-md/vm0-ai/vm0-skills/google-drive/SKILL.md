---
name: google-drive
description: Google Drive API for file management. Use when user mentions "Google
  Drive", "drive.google.com", shares a Drive link, "upload file", or asks about cloud
  storage.
vm0_secrets:
  - GOOGLE_DRIVE_TOKEN
---

# Google Drive API

Use the Google Drive API via direct `curl` calls to **manage files, folders, uploads, downloads, sharing, and permissions**.

> Official docs: `https://developers.google.com/drive/api/v3/reference`

---

## When to Use

Use this skill when you need to:

- **List and search** files and folders
- **Upload files** to Google Drive
- **Download files** from Google Drive
- **Create folders** and organize files
- **Move and copy** files between locations
- **Share files** and manage permissions
- **Get file metadata** (name, size, type, modified date)
- **Delete files** (move to trash or permanent deletion)
- **Export Google Docs** to different formats (PDF, DOCX, etc.)

---

## Prerequisites

Go to [vm0.ai](https://vm0.ai) **Settings → Connectors** and connect **Google Drive**. vm0 will automatically inject the required `GOOGLE_DRIVE_TOKEN` environment variable.

---

> **Important:** When using `$VAR` in a command that pipes to another command, wrap the command containing `$VAR` in `bash -c '...'`. Due to a Claude Code bug, environment variables are silently cleared when pipes are used directly.

> **Placeholders:** Values in `{curly-braces}` like `{file-id}` are placeholders. Replace them with actual values when executing.

---

## How to Use

Base URL: `https://www.googleapis.com/drive/v3`

---

## Files

### List Files

List files in your Google Drive:

```bash
bash -c 'curl -s "https://www.googleapis.com/drive/v3/files?pageSize=10&fields=files(id,name,mimeType,modifiedTime,size)" --header "Authorization: Bearer $GOOGLE_DRIVE_TOKEN"' | jq '.files[] | {id, name, mimeType, size}'
```

### List Files with Query

Search using query syntax:

```bash
bash -c 'curl -s "https://www.googleapis.com/drive/v3/files?q=name+contains+'"'"'report'"'"'&pageSize=10&fields=files(id,name,mimeType)" --header "Authorization: Bearer $GOOGLE_DRIVE_TOKEN"' | jq '.files'
```

Common query operators:
- `name = 'filename'` - Exact name match
- `name contains 'text'` - Partial name match
- `mimeType = 'application/pdf'` - Filter by MIME type
- `modifiedTime > '2024-01-01T00:00:00'` - Modified after date
- `trashed = false` - Not in trash
- `'folder-id' in parents` - Files in specific folder
- `fullText contains 'keyword'` - Search file content

Combine with `and` or `or`:

```bash
bash -c 'curl -s "https://www.googleapis.com/drive/v3/files?q=mimeType+%3D+'"'"'application/pdf'"'"'+and+trashed+%3D+false&fields=files(id,name)" --header "Authorization: Bearer $GOOGLE_DRIVE_TOKEN"' | jq '.files'
```

### Get File Metadata

Get detailed information about a file:

```bash
bash -c 'curl -s "https://www.googleapis.com/drive/v3/files/{file-id}?fields=id,name,mimeType,size,createdTime,modifiedTime,owners,parents,webViewLink,webContentLink" --header "Authorization: Bearer $GOOGLE_DRIVE_TOKEN"' | jq .
```

### Download File

Download a file's content:

```bash
bash -c 'curl -s "https://www.googleapis.com/drive/v3/files/{file-id}?alt=media" --header "Authorization: Bearer $GOOGLE_DRIVE_TOKEN"' > downloaded_file.bin
```

### Export Google Docs

Export Google Docs, Sheets, Slides to different formats:

```bash
bash -c 'curl -s "https://www.googleapis.com/drive/v3/files/{file-id}/export?mimeType=application/pdf" --header "Authorization: Bearer $GOOGLE_DRIVE_TOKEN"' > document.pdf
```

```bash
bash -c 'curl -s "https://www.googleapis.com/drive/v3/files/{file-id}/export?mimeType=application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" --header "Authorization: Bearer $GOOGLE_DRIVE_TOKEN"' > spreadsheet.xlsx
```

```bash
bash -c 'curl -s "https://www.googleapis.com/drive/v3/files/{file-id}/export?mimeType=application/vnd.openxmlformats-officedocument.wordprocessingml.document" --header "Authorization: Bearer $GOOGLE_DRIVE_TOKEN"' > document.docx
```

Common export MIME types:
- **PDF**: `application/pdf`
- **DOCX**: `application/vnd.openxmlformats-officedocument.wordprocessingml.document`
- **XLSX**: `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`
- **Plain Text**: `text/plain`
- **HTML**: `text/html`

### Upload File (Simple)

Upload a file (up to 5MB):

```bash
bash -c 'curl -s -X POST "https://www.googleapis.com/upload/drive/v3/files?uploadType=media" --header "Authorization: Bearer $GOOGLE_DRIVE_TOKEN" --header "Content-Type: application/octet-stream" --data-binary @/path/to/file.txt' | jq '{id, name, mimeType}'
```

> **Note:** Simple upload creates the file with an auto-generated name ("Untitled"). Use **Update File Metadata** immediately after to set the filename.

### Update File Metadata

Update file name or other metadata:

Write to `/tmp/drive_request.json`:

```json
{
  "name": "NewFileName.txt"
}
```

Then run:

```bash
bash -c 'curl -s -X PATCH "https://www.googleapis.com/drive/v3/files/{file-id}?fields=id,name,modifiedTime" --header "Authorization: Bearer $GOOGLE_DRIVE_TOKEN" --header "Content-Type: application/json" -d @/tmp/drive_request.json' | jq '{id, name, modifiedTime}'
```

### Copy File

Create a copy of a file:

Write to `/tmp/drive_request.json`:

```json
{
  "name": "Copy of Document"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://www.googleapis.com/drive/v3/files/{file-id}/copy" --header "Authorization: Bearer $GOOGLE_DRIVE_TOKEN" --header "Content-Type: application/json" -d @/tmp/drive_request.json' | jq '{id, name}'
```

### Move File to Trash

Move a file to trash (can be restored):

Write to `/tmp/drive_request.json`:

```json
{
  "trashed": true
}
```

Then run:

```bash
bash -c 'curl -s -X PATCH "https://www.googleapis.com/drive/v3/files/{file-id}?fields=id,name,trashed" --header "Authorization: Bearer $GOOGLE_DRIVE_TOKEN" --header "Content-Type: application/json" -d @/tmp/drive_request.json' | jq '{id, name, trashed}'
```

### Delete File Permanently

Permanently delete a file (cannot be restored):

```bash
bash -c 'curl -s -X DELETE "https://www.googleapis.com/drive/v3/files/{file-id}" --header "Authorization: Bearer $GOOGLE_DRIVE_TOKEN"'
```

---

## Folders

### List Folders Only

List only folders:

```bash
bash -c 'curl -s "https://www.googleapis.com/drive/v3/files?q=mimeType+%3D+'"'"'application/vnd.google-apps.folder'"'"'+and+trashed+%3D+false&fields=files(id,name,modifiedTime)" --header "Authorization: Bearer $GOOGLE_DRIVE_TOKEN"' | jq '.files'
```

### Create Folder

Create a new folder:

Write to `/tmp/drive_request.json`:

```json
{
  "name": "My New Folder",
  "mimeType": "application/vnd.google-apps.folder"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://www.googleapis.com/drive/v3/files" --header "Authorization: Bearer $GOOGLE_DRIVE_TOKEN" --header "Content-Type: application/json" -d @/tmp/drive_request.json' | jq '{id, name, mimeType}'
```

### Create Folder in Parent Folder

Create a folder inside another folder:

Write to `/tmp/drive_request.json`:

```json
{
  "name": "Subfolder",
  "mimeType": "application/vnd.google-apps.folder",
  "parents": ["{parent-folder-id}"]
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://www.googleapis.com/drive/v3/files?fields=id,name,parents" --header "Authorization: Bearer $GOOGLE_DRIVE_TOKEN" --header "Content-Type: application/json" -d @/tmp/drive_request.json' | jq '{id, name, parents}'
```

### List Files in Folder

List all files in a specific folder:

```bash
bash -c 'curl -s "https://www.googleapis.com/drive/v3/files?q='"'"'{folder-id}'"'"'+in+parents&fields=files(id,name,mimeType,size)" --header "Authorization: Bearer $GOOGLE_DRIVE_TOKEN"' | jq '.files'
```

---

## Sharing and Permissions

### List Permissions

List all permissions for a file:

```bash
bash -c 'curl -s "https://www.googleapis.com/drive/v3/files/{file-id}/permissions?fields=permissions(id,type,role,emailAddress)" --header "Authorization: Bearer $GOOGLE_DRIVE_TOKEN"' | jq '.permissions'
```

### Share with Specific User

Grant access to a specific user:

Write to `/tmp/drive_request.json`:

```json
{
  "type": "user",
  "role": "reader",
  "emailAddress": "user@example.com"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://www.googleapis.com/drive/v3/files/{file-id}/permissions" --header "Authorization: Bearer $GOOGLE_DRIVE_TOKEN" --header "Content-Type: application/json" -d @/tmp/drive_request.json' | jq '{id, type, role, emailAddress}'
```

### Share with Anyone (Public Link)

Make a file accessible to anyone with the link:

Write to `/tmp/drive_request.json`:

```json
{
  "type": "anyone",
  "role": "reader"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://www.googleapis.com/drive/v3/files/{file-id}/permissions" --header "Authorization: Bearer $GOOGLE_DRIVE_TOKEN" --header "Content-Type: application/json" -d @/tmp/drive_request.json' | jq .
```

### Update Permission

Change permission level:

Write to `/tmp/drive_request.json`:

```json
{
  "role": "writer"
}
```

Then run:

```bash
bash -c 'curl -s -X PATCH "https://www.googleapis.com/drive/v3/files/{file-id}/permissions/{permission-id}" --header "Authorization: Bearer $GOOGLE_DRIVE_TOKEN" --header "Content-Type: application/json" -d @/tmp/drive_request.json' | jq .
```

### Remove Permission

Revoke access:

```bash
bash -c 'curl -s -X DELETE "https://www.googleapis.com/drive/v3/files/{file-id}/permissions/{permission-id}" --header "Authorization: Bearer $GOOGLE_DRIVE_TOKEN"'
```

Permission roles:
- **reader**: Can view and download
- **commenter**: Can view, download, and comment
- **writer**: Can view, download, comment, and edit
- **owner**: Full control (only for type=user)

Permission types:
- **user**: Specific email address
- **group**: Google Group email
- **domain**: Everyone in organization
- **anyone**: Public access

---

## Common MIME Types

| Type | MIME Type |
|------|-----------|
| Folder | `application/vnd.google-apps.folder` |
| Google Doc | `application/vnd.google-apps.document` |
| Google Sheet | `application/vnd.google-apps.spreadsheet` |
| Google Slides | `application/vnd.google-apps.presentation` |
| PDF | `application/pdf` |
| Text | `text/plain` |
| CSV | `text/csv` |
| JPEG | `image/jpeg` |
| PNG | `image/png` |
| ZIP | `application/zip` |

---

## Guidelines

1. **Rate limits**: Default quota is 1,000 requests per 100 seconds per user
2. **File IDs**: File IDs are permanent and don't change when files are renamed or moved
3. **Pagination**: Use `pageToken` from response to get next page of results
4. **Fields parameter**: Specify `fields` to reduce response size and improve performance
5. **Upload size limits**: Simple upload limited to 5MB; use resumable upload for larger files
6. **Query escaping**: Escape single quotes in queries as `\'` and backslashes as `\\`

---

## API Reference

- REST Reference: https://developers.google.com/drive/api/v3/reference
- Search Query Guide: https://developers.google.com/drive/api/guides/search-files
- Upload Guide: https://developers.google.com/drive/api/guides/manage-uploads
- Download Guide: https://developers.google.com/drive/api/guides/manage-downloads
- OAuth Playground: https://developers.google.com/oauthplayground/
- OAuth Scopes: https://developers.google.com/identity/protocols/oauth2/scopes#drive
