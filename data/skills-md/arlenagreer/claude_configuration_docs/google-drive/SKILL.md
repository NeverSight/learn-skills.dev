---
name: google-drive
description: Manage Google Drive files and folders with full CRUD operations via Ruby scripts. Use for file storage operations, folder organization, sharing permissions, searching across Drive, and uploading/downloading files of any type. Works seamlessly with google-sheets and google-docs skills for complete Google Workspace integration.
category: productivity
version: 1.0.0
key_capabilities: list, search, upload, download, share, organize folders, manage permissions
when_to_use: File operations, folder management, permission sharing, Drive-wide search, any file type upload/download
---

# Google Drive Management Skill

## Overview

Provide comprehensive Google Drive file and folder management capabilities through Ruby-based scripts with shared authentication. Enable full CRUD operations (Create, Read, Update, Delete) on Google Drive files and folders.

## When to Use This Skill

Use this skill for ANY Google Drive operations:

- **File Management**: Upload, download, read, update, delete files
- **Folder Management**: Create, list, organize folders
- **Search**: Find files and folders by name, type, or content
- **Sharing**: Manage file and folder permissions
- **Content Reading**: Read text file contents directly
- **Metadata**: View and update file properties

## Authentication

This skill shares authentication with the calendar and contacts skills via `~/.claude/.google/token.json`. All skills use the same OAuth token with scopes:
- `https://www.googleapis.com/auth/calendar` (Calendar access)
- `https://www.googleapis.com/auth/contacts` (Contacts read/write)
- `https://www.googleapis.com/auth/drive` (Google Drive full access)

When any skill refreshes the token, all skills benefit from the updated authentication.

### First-Time Setup

If Google Drive scope not already configured:

1. Ensure `~/.claude/.google/client_secret.json` exists with OAuth credentials
2. Run any Google Drive operation - the script will prompt for authorization
3. The token will be stored and shared with calendar and contacts skills

### Re-authorization for New Scope

Since the Drive scope is new, you'll need to re-authorize once:

```bash
# Delete the existing token to force re-authorization
rm ~/.claude/.google/token.json

# Run any Drive operation to trigger OAuth flow
~/.claude/skills/google-drive/scripts/drive_manager.rb --list
```

Follow the authorization URL and enter the code when prompted.

## Core Script: drive_manager.rb

Location: `scripts/drive_manager.rb`

Comprehensive Ruby script providing all Google Drive operations through the Drive API v3.

### List Files and Folders

Browse your Google Drive:

```bash
# List all files (default: 100 items)
drive_manager.rb --list

# List with custom page size
drive_manager.rb --list --page-size 50

# List only folders
drive_manager.rb --list --type folder

# List only specific file types
drive_manager.rb --list --type "application/pdf"

# Get next page using token from previous response
drive_manager.rb --list --page-token "NEXT_PAGE_TOKEN"
```

Returns JSON array of files with metadata (id, name, mimeType, createdTime, modifiedTime, size, webViewLink).

### Search Files

Find files by name or query:

```bash
# Search by name (partial match)
drive_manager.rb --search "project report"

# Search by exact name
drive_manager.rb --search "Budget 2024.xlsx" --exact

# Search in specific folder
drive_manager.rb --search "invoice" --folder "FOLDER_ID"

# Advanced query (full Drive API query syntax)
drive_manager.rb --query "mimeType='application/pdf' and modifiedTime > '2024-01-01'"
```

### Get File Details

Retrieve complete information about a specific file:

```bash
# Get by file ID
drive_manager.rb --get "FILE_ID"

# Get with download URL
drive_manager.rb --get "FILE_ID" --include-download-url
```

Returns full file metadata including sharing permissions and download links.

### Read File Content

Read text-based file contents directly:

```bash
# Read text file content
drive_manager.rb --read "FILE_ID"

# Read with specific export format (for Google Docs)
drive_manager.rb --read "FILE_ID" --export-format "text/plain"
```

**Supported File Types**:
- Plain text files (.txt)
- Google Docs (exports as text/plain, text/html, or application/pdf)
- Google Sheets (exports as CSV, XLSX, or PDF)
- CSV files
- JSON files
- Markdown files (.md)

### Upload Files

Upload files to Google Drive:

```bash
# Upload file to root
drive_manager.rb --upload "/path/to/file.pdf"

# Upload to specific folder
drive_manager.rb --upload "/path/to/file.pdf" --folder "FOLDER_ID"

# Upload with custom name
drive_manager.rb --upload "/path/to/file.pdf" --name "Custom Name.pdf"

# Upload with description
drive_manager.rb --upload "/path/to/file.pdf" --description "Q4 Financial Report"
```

### Download Files

Download files from Google Drive:

```bash
# Download to current directory
drive_manager.rb --download "FILE_ID"

# Download to specific location
drive_manager.rb --download "FILE_ID" --output "/path/to/save/file.pdf"

# Download Google Docs as PDF
drive_manager.rb --download "FILE_ID" --export-format "application/pdf"

# Download Google Sheets as Excel
drive_manager.rb --download "FILE_ID" --export-format "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
```

### Create Folders

Organize files with folders:

```bash
# Create folder in root
drive_manager.rb --create-folder "Project Files"

# Create folder in specific parent
drive_manager.rb --create-folder "Invoices" --folder "PARENT_FOLDER_ID"

# Create nested folder structure
drive_manager.rb --create-folder "2024/Q4/Reports" --create-path
```

### Update Files

Modify file metadata:

```bash
# Rename file
drive_manager.rb --update "FILE_ID" --name "New Name.pdf"

# Update description
drive_manager.rb --update "FILE_ID" --description "Updated description"

# Move file to different folder
drive_manager.rb --update "FILE_ID" --move-to "NEW_FOLDER_ID"

# Update multiple properties
drive_manager.rb --update "FILE_ID" \
  --name "Report.pdf" \
  --description "Final version" \
  --move-to "FOLDER_ID"
```

### Share Files

Manage file and folder permissions:

```bash
# Share with specific user (reader)
drive_manager.rb --share "FILE_ID" --email "user@example.com" --role reader

# Share with specific user (writer)
drive_manager.rb --share "FILE_ID" --email "user@example.com" --role writer

# Share with anyone with link (reader)
drive_manager.rb --share "FILE_ID" --role reader --anyone

# Make file public
drive_manager.rb --share "FILE_ID" --role reader --anyone

# Share entire folder
drive_manager.rb --share "FOLDER_ID" --email "team@example.com" --role writer
```

**Permission Roles**:
- `reader` - Can view and download
- `commenter` - Can view and comment
- `writer` - Can edit and organize
- `owner` - Full control (transfer ownership)

### Delete Files

Remove files and folders:

```bash
# Move to trash (recoverable)
drive_manager.rb --delete "FILE_ID"

# Permanent delete (non-recoverable)
drive_manager.rb --delete "FILE_ID" --permanent
```

**Warning**: Permanent deletion cannot be undone.

### Copy Files

Duplicate files:

```bash
# Copy file in same location
drive_manager.rb --copy "FILE_ID"

# Copy with new name
drive_manager.rb --copy "FILE_ID" --name "Copy of Document"

# Copy to different folder
drive_manager.rb --copy "FILE_ID" --folder "TARGET_FOLDER_ID"
```

## File Type Reference

See `references/file_types.md` for comprehensive MIME type documentation.

### Common MIME Types

**Documents**:
- Google Docs: `application/vnd.google-apps.document`
- Microsoft Word: `application/vnd.openxmlformats-officedocument.wordprocessingml.document`
- PDF: `application/pdf`
- Plain text: `text/plain`

**Spreadsheets**:
- Google Sheets: `application/vnd.google-apps.spreadsheet`
- Microsoft Excel: `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`
- CSV: `text/csv`

**Folders**:
- Folder: `application/vnd.google-apps.folder`

## Workflow Patterns

### Finding and Reading a File

```bash
# 1. Search for file
SEARCH_RESULT=$(drive_manager.rb --search "report")

# 2. Extract file ID from results
FILE_ID=$(echo $SEARCH_RESULT | jq -r '.files[0].id')

# 3. Read file content
drive_manager.rb --read "$FILE_ID"
```

### Uploading and Sharing

```bash
# 1. Upload file
UPLOAD_RESULT=$(drive_manager.rb --upload "/path/to/file.pdf" --name "Shared Report.pdf")

# 2. Extract file ID
FILE_ID=$(echo $UPLOAD_RESULT | jq -r '.file.id')

# 3. Share with team
drive_manager.rb --share "$FILE_ID" --email "team@example.com" --role writer

# 4. Get shareable link
drive_manager.rb --get "$FILE_ID" --include-download-url
```

### Organizing Files into Folders

```bash
# 1. Create folder structure
FOLDER_RESULT=$(drive_manager.rb --create-folder "2024/Projects" --create-path)
FOLDER_ID=$(echo $FOLDER_RESULT | jq -r '.folder.id')

# 2. Move existing files
drive_manager.rb --update "FILE_ID_1" --move-to "$FOLDER_ID"
drive_manager.rb --update "FILE_ID_2" --move-to "$FOLDER_ID"

# 3. Upload new files directly to folder
drive_manager.rb --upload "/path/to/new-file.pdf" --folder "$FOLDER_ID"
```

### Bulk Operations

```bash
# Find all PDFs
drive_manager.rb --query "mimeType='application/pdf'" > pdfs.json

# Process each PDF
cat pdfs.json | jq -r '.files[].id' | while read file_id; do
  # Download each
  drive_manager.rb --download "$file_id" --output "/backup/$file_id.pdf"
done
```

## Integration with Other Skills

### Calendar Skill Integration

Share calendar-related documents:

```bash
# Upload meeting notes
drive_manager.rb --upload "meeting-notes.pdf" --name "Team Standup Notes"

# Share with meeting attendees
drive_manager.rb --share "$FILE_ID" --email "attendee@example.com" --role reader
```

### Contacts Skill Integration

Store contact-related documents:

```bash
# Create contacts folder
FOLDER_ID=$(drive_manager.rb --create-folder "Contact Documents" | jq -r '.folder.id')

# Upload contract for specific contact
drive_manager.rb --upload "contract.pdf" \
  --folder "$FOLDER_ID" \
  --name "John Doe - Service Agreement"
```

### Email Skill Integration

Attach Drive files to emails or save email attachments:

```bash
# Get shareable link for email
LINK=$(drive_manager.rb --get "$FILE_ID" --include-download-url | jq -r '.file.webViewLink')

# Include link in email message
~/.claude/skills/email/send_email.sh "recipient@example.com" \
  "Check out this document: $LINK"
```

## Error Handling

The script returns JSON with status and error details:

```json
{
  "status": "error",
  "code": "AUTH_ERROR|API_ERROR|FILE_NOT_FOUND|INVALID_ARGS",
  "message": "Detailed error message"
}
```

**Exit Codes**:
- `0` - Success
- `1` - Operation failed
- `2` - Authentication error
- `3` - API error
- `4` - Invalid arguments
- `5` - File not found

## Common Use Cases

### Document Management

```bash
# Upload and organize quarterly reports
drive_manager.rb --create-folder "2024/Q4" --create-path
drive_manager.rb --upload "Q4-report.pdf" --folder "$FOLDER_ID"
drive_manager.rb --share "$FILE_ID" --email "executive@company.com" --role reader
```

### Backup Strategy

```bash
# Download all important files for backup
drive_manager.rb --query "starred=true" > starred.json
cat starred.json | jq -r '.files[].id' | while read id; do
  drive_manager.rb --download "$id" --output "/backup/"
done
```

### Collaborative Workspace

```bash
# Create shared project folder
FOLDER_ID=$(drive_manager.rb --create-folder "Team Project" | jq -r '.folder.id')

# Share with team
drive_manager.rb --share "$FOLDER_ID" --email "team@company.com" --role writer

# Upload project files
drive_manager.rb --upload "specs.pdf" --folder "$FOLDER_ID"
drive_manager.rb --upload "design.fig" --folder "$FOLDER_ID"
```

### Content Retrieval

```bash
# Read configuration file from Drive
CONFIG=$(drive_manager.rb --search "config.json" | jq -r '.files[0].id')
drive_manager.rb --read "$CONFIG" > local-config.json
```

## Best Practices

1. **Search Before Upload**: Avoid duplicates by searching first
2. **Use Folders**: Organize files hierarchically for better management
3. **Descriptive Names**: Use clear, searchable file names
4. **Minimal Permissions**: Share with least privilege necessary
5. **Regular Cleanup**: Periodically review and delete unused files
6. **Backup Important Files**: Download critical files to local storage
7. **Check File IDs**: Always verify file IDs before destructive operations

## Troubleshooting

### Authentication Issues

```bash
# Re-authorize if token invalid
rm ~/.claude/.google/token.json
drive_manager.rb --list
```

### Scope Errors

If you see Drive scope-related errors, ensure the token has the Drive scope:

```bash
# Check current scopes
cat ~/.claude/.google/token.json | jq -r '.default.scope'

# Should include: https://www.googleapis.com/auth/drive
```

### File Not Found

```bash
# Verify file exists and you have access
drive_manager.rb --get "FILE_ID"

# Search for file by name
drive_manager.rb --search "filename"
```

### API Quota Limits

Google Drive API has rate limits. If you hit quota:
- Wait a few minutes before retrying
- Reduce batch operation sizes
- Implement exponential backoff for bulk operations

## Advanced Features

### Query Syntax

The `--query` flag supports full Drive API query syntax:

```bash
# Files modified in last 7 days
drive_manager.rb --query "modifiedTime > '2024-10-24'"

# Files larger than 10MB
drive_manager.rb --query "size > 10485760"

# Files shared with me
drive_manager.rb --query "sharedWithMe=true"

# Combine conditions
drive_manager.rb --query "mimeType='application/pdf' and starred=true and trashed=false"
```

### Export Formats

Google Workspace files can be exported in various formats:

**Google Docs**:
- `text/plain` - Plain text
- `text/html` - HTML
- `application/pdf` - PDF
- `application/vnd.openxmlformats-officedocument.wordprocessingml.document` - DOCX

**Google Sheets**:
- `text/csv` - CSV
- `application/pdf` - PDF
- `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet` - XLSX

**Google Slides**:
- `application/pdf` - PDF
- `application/vnd.openxmlformats-officedocument.presentationml.presentation` - PPTX

## Script Version

Current version: 1.0.0

Run `drive_manager.rb --version` to check installed version.

## Dependencies

- Ruby 3.3.7 (same as contacts and calendar skills)
- `google-apis-drive_v3` gem
- `googleauth` gem
- Shared OAuth credentials with calendar and contacts skills
