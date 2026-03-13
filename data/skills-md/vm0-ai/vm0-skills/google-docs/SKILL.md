---
name: google-docs
description: Google Docs API for document editing. Use when user mentions "Google
  Doc", "docs.google.com", shares a Doc link, "create document", or asks about document
  creation.
vm0_secrets:
  - GOOGLE_DOCS_TOKEN
---

# Google Docs API

Use the Google Docs API via direct `curl` calls to **create, read, update, and format Google Docs documents**.

> Official docs: `https://developers.google.com/docs/api`

---

## When to Use

Use this skill when you need to:

- **Create new documents** from scratch
- **Read document content** and metadata
- **Insert or replace text** in documents
- **Format text** (bold, italic, font size, color)
- **Manage paragraphs** (alignment, spacing, bullets)
- **Insert tables, images, and page breaks**
- **Get document structure** and element information

---

## Prerequisites

Go to [vm0.ai](https://vm0.ai) **Settings → Connectors** and connect **Google Docs**. vm0 will automatically inject the required `GOOGLE_DOCS_TOKEN` environment variable.

---

> **Important:** When using `$VAR` in a command that pipes to another command, wrap the command containing `$VAR` in `bash -c '...'`. Due to a Claude Code bug, environment variables are silently cleared when pipes are used directly.

> **Placeholders:** Values in `{curly-braces}` like `{document-id}` are placeholders. Replace them with actual values when executing.

---

## How to Use

Base URL: `https://docs.googleapis.com/v1`

**Finding your Document ID:**
The document ID is in the URL: `https://docs.google.com/document/d/{DOCUMENT_ID}/edit`

---

### 1. Create New Document

Create a blank document with a title:

Write to `/tmp/gdocs_request.json`:

```json
{
  "title": "My New Document"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://docs.googleapis.com/v1/documents" --header "Authorization: Bearer $GOOGLE_DOCS_TOKEN" --header "Content-Type: application/json" -d @/tmp/gdocs_request.json' | jq '{documentId, title, documentUrl: ("https://docs.google.com/document/d/" + .documentId + "/edit")}'
```

---

### 2. Get Document Content

Read the entire document structure and content:

```bash
bash -c 'curl -s "https://docs.googleapis.com/v1/documents/{document-id}" --header "Authorization: Bearer $GOOGLE_DOCS_TOKEN"' | jq '{title: .title, body: .body.content}'
```

---

### 3. Get Document Metadata Only

Get just the title and basic properties:

```bash
bash -c 'curl -s "https://docs.googleapis.com/v1/documents/{document-id}" --header "Authorization: Bearer $GOOGLE_DOCS_TOKEN"' | jq '{documentId, title, revisionId, suggestionsViewMode}'
```

---

### 4. Insert Text at Beginning

Insert text at the start of the document (index 1):

Write to `/tmp/gdocs_request.json`:

```json
{
  "requests": [
    {
      "insertText": {
        "location": {
          "index": 1
        },
        "text": "Hello, this is my first paragraph.\n"
      }
    }
  ]
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://docs.googleapis.com/v1/documents/{document-id}:batchUpdate" --header "Authorization: Bearer $GOOGLE_DOCS_TOKEN" --header "Content-Type: application/json" -d @/tmp/gdocs_request.json' | jq '.error // .replies // "done"'
```

---

### 5. Insert Text at Specific Location

Insert text at a specific index (get indexes from document content):

Write to `/tmp/gdocs_request.json`:

```json
{
  "requests": [
    {
      "insertText": {
        "location": {
          "index": 25
        },
        "text": "This is inserted text.\n"
      }
    }
  ]
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://docs.googleapis.com/v1/documents/{document-id}:batchUpdate" --header "Authorization: Bearer $GOOGLE_DOCS_TOKEN" --header "Content-Type: application/json" -d @/tmp/gdocs_request.json' | jq '.error // .replies // "done"'
```

---

### 6. Delete Content Range

Delete text from a specific range:

Write to `/tmp/gdocs_request.json`:

```json
{
  "requests": [
    {
      "deleteContentRange": {
        "range": {
          "startIndex": 1,
          "endIndex": 50
        }
      }
    }
  ]
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://docs.googleapis.com/v1/documents/{document-id}:batchUpdate" --header "Authorization: Bearer $GOOGLE_DOCS_TOKEN" --header "Content-Type: application/json" -d @/tmp/gdocs_request.json' | jq '.error // .replies // "done"'
```

---

### 7. Find and Replace Text

Replace all occurrences of text throughout the document:

Write to `/tmp/gdocs_request.json`:

```json
{
  "requests": [
    {
      "replaceAllText": {
        "containsText": {
          "text": "old text",
          "matchCase": true
        },
        "replaceText": "new text"
      }
    }
  ]
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://docs.googleapis.com/v1/documents/{document-id}:batchUpdate" --header "Authorization: Bearer $GOOGLE_DOCS_TOKEN" --header "Content-Type: application/json" -d @/tmp/gdocs_request.json' | jq '.error // .replies[0].replaceAllText'
```

---

### 8. Format Text as Bold

Make text bold in a specific range:

Write to `/tmp/gdocs_request.json`:

```json
{
  "requests": [
    {
      "updateTextStyle": {
        "range": {
          "startIndex": 1,
          "endIndex": 20
        },
        "textStyle": {
          "bold": true
        },
        "fields": "bold"
      }
    }
  ]
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://docs.googleapis.com/v1/documents/{document-id}:batchUpdate" --header "Authorization: Bearer $GOOGLE_DOCS_TOKEN" --header "Content-Type: application/json" -d @/tmp/gdocs_request.json' | jq '.error // .replies // "done"'
```

---

### 9. Format Text with Multiple Styles

Apply multiple text styles (bold, italic, font size, color):

Write to `/tmp/gdocs_request.json`:

```json
{
  "requests": [
    {
      "updateTextStyle": {
        "range": {
          "startIndex": 1,
          "endIndex": 30
        },
        "textStyle": {
          "bold": true,
          "italic": true,
          "fontSize": {
            "magnitude": 14,
            "unit": "PT"
          },
          "foregroundColor": {
            "color": {
              "rgbColor": {
                "red": 0.2,
                "green": 0.4,
                "blue": 0.8
              }
            }
          }
        },
        "fields": "bold,italic,fontSize,foregroundColor"
      }
    }
  ]
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://docs.googleapis.com/v1/documents/{document-id}:batchUpdate" --header "Authorization: Bearer $GOOGLE_DOCS_TOKEN" --header "Content-Type: application/json" -d @/tmp/gdocs_request.json' | jq '.error // .replies // "done"'
```

---

### 10. Set Paragraph Alignment

Change paragraph alignment (LEFT, CENTER, RIGHT, JUSTIFIED):

Write to `/tmp/gdocs_request.json`:

```json
{
  "requests": [
    {
      "updateParagraphStyle": {
        "range": {
          "startIndex": 1,
          "endIndex": 50
        },
        "paragraphStyle": {
          "alignment": "CENTER"
        },
        "fields": "alignment"
      }
    }
  ]
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://docs.googleapis.com/v1/documents/{document-id}:batchUpdate" --header "Authorization: Bearer $GOOGLE_DOCS_TOKEN" --header "Content-Type: application/json" -d @/tmp/gdocs_request.json' | jq '.error // .replies // "done"'
```

---

### 11. Create Bulleted List

Convert paragraphs to a bulleted list:

Write to `/tmp/gdocs_request.json`:

```json
{
  "requests": [
    {
      "createParagraphBullets": {
        "range": {
          "startIndex": 1,
          "endIndex": 100
        },
        "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE"
      }
    }
  ]
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://docs.googleapis.com/v1/documents/{document-id}:batchUpdate" --header "Authorization: Bearer $GOOGLE_DOCS_TOKEN" --header "Content-Type: application/json" -d @/tmp/gdocs_request.json' | jq '.error // .replies // "done"'
```

**Available bullet presets:**
- `BULLET_DISC_CIRCLE_SQUARE`
- `BULLET_DIAMONDX_ARROW3D_SQUARE`
- `BULLET_CHECKBOX`
- `NUMBERED_DECIMAL_ALPHA_ROMAN`
- `NUMBERED_DECIMAL_NESTED`

---

### 12. Insert Table

Insert a table with specified rows and columns:

Write to `/tmp/gdocs_request.json`:

```json
{
  "requests": [
    {
      "insertTable": {
        "rows": 3,
        "columns": 4,
        "location": {
          "index": 1
        }
      }
    }
  ]
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://docs.googleapis.com/v1/documents/{document-id}:batchUpdate" --header "Authorization: Bearer $GOOGLE_DOCS_TOKEN" --header "Content-Type: application/json" -d @/tmp/gdocs_request.json' | jq '.error // .replies // "done"'
```

---

### 13. Insert Page Break

Insert a page break at a specific location:

Write to `/tmp/gdocs_request.json`:

```json
{
  "requests": [
    {
      "insertPageBreak": {
        "location": {
          "index": 50
        }
      }
    }
  ]
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://docs.googleapis.com/v1/documents/{document-id}:batchUpdate" --header "Authorization: Bearer $GOOGLE_DOCS_TOKEN" --header "Content-Type: application/json" -d @/tmp/gdocs_request.json' | jq '.error // .replies // "done"'
```

---

### 14. Insert Inline Image

Insert an image from a URL:

Write to `/tmp/gdocs_request.json`:

```json
{
  "requests": [
    {
      "insertInlineImage": {
        "uri": "https://example.com/image.png",
        "location": {
          "index": 1
        },
        "objectSize": {
          "height": {
            "magnitude": 200,
            "unit": "PT"
          },
          "width": {
            "magnitude": 300,
            "unit": "PT"
          }
        }
      }
    }
  ]
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://docs.googleapis.com/v1/documents/{document-id}:batchUpdate" --header "Authorization: Bearer $GOOGLE_DOCS_TOKEN" --header "Content-Type: application/json" -d @/tmp/gdocs_request.json' | jq '.error // .replies // "done"'
```

---

### 15. Batch Operations (Multiple Updates)

Combine multiple operations in a single request:

Write to `/tmp/gdocs_request.json`:

```json
{
  "requests": [
    {
      "insertText": {
        "location": {
          "index": 1
        },
        "text": "Title: Important Document\n\n"
      }
    },
    {
      "updateTextStyle": {
        "range": {
          "startIndex": 1,
          "endIndex": 26
        },
        "textStyle": {
          "bold": true,
          "fontSize": {
            "magnitude": 18,
            "unit": "PT"
          }
        },
        "fields": "bold,fontSize"
      }
    },
    {
      "insertText": {
        "location": {
          "index": 28
        },
        "text": "This is the body text of the document.\n"
      }
    }
  ]
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://docs.googleapis.com/v1/documents/{document-id}:batchUpdate" --header "Authorization: Bearer $GOOGLE_DOCS_TOKEN" --header "Content-Type: application/json" -d @/tmp/gdocs_request.json' | jq '.error // (.replies | length)'
```

---

### 16. Extract Plain Text

Get just the text content from a document:

```bash
bash -c 'curl -s "https://docs.googleapis.com/v1/documents/{document-id}" --header "Authorization: Bearer $GOOGLE_DOCS_TOKEN"' | jq -r '.body.content[]?.paragraph?.elements[]?.textRun?.content' | tr -d '\0'
```

---

### 17. Get Document Structure

View document structure with element types and indexes:

```bash
bash -c 'curl -s "https://docs.googleapis.com/v1/documents/{document-id}" --header "Authorization: Bearer $GOOGLE_DOCS_TOKEN"' | jq '.body.content[] | {startIndex, endIndex, paragraph: .paragraph.elements[0].textRun.content}'
```

---

## Common Scopes

| Scope | Permission |
|-------|------------|
| `documents.readonly` | Read-only access |
| `documents` | Full read/write access |
| `drive.readonly` | Read files in Drive |
| `drive.file` | Access files created by app |
| `drive` | Full Drive access |

Use full URL: `https://www.googleapis.com/auth/documents`

---

## Index Reference

Understanding indexes is critical for the Google Docs API:

- **Index 1**: Start of document body
- **Index N**: Each character, newline, and structural element increments the index
- **End index**: Use `"endIndex": startIndex + textLength` for ranges
- **Tip**: Get document content first to see current indexes

---

## Text Style Fields

When using `updateTextStyle`, specify which fields to update in the `fields` parameter:

| Field | Description |
|-------|-------------|
| `bold` | Bold text |
| `italic` | Italic text |
| `underline` | Underline text |
| `strikethrough` | Strikethrough text |
| `fontSize` | Font size (PT or PX) |
| `foregroundColor` | Text color (RGB) |
| `backgroundColor` | Background color (RGB) |
| `fontFamily` | Font name (e.g., "Arial") |
| `baselineOffset` | Superscript/subscript |
| `link` | Hyperlink URL |

Use comma-separated for multiple: `"fields": "bold,italic,fontSize"`

---

## Paragraph Style Fields

When using `updateParagraphStyle`:

| Field | Description |
|-------|-------------|
| `alignment` | LEFT, CENTER, RIGHT, JUSTIFIED |
| `lineSpacing` | Line spacing percentage (100 = single) |
| `direction` | LEFT_TO_RIGHT or RIGHT_TO_LEFT |
| `spaceAbove` | Space before paragraph |
| `spaceBelow` | Space after paragraph |
| `indentFirstLine` | First line indentation |
| `indentStart` | Left indentation |
| `indentEnd` | Right indentation |
| `namedStyleType` | HEADING_1, HEADING_2, NORMAL_TEXT, etc. |

---

## Guidelines

1. **Batch operations**: Combine multiple requests in a single batchUpdate call to improve performance
2. **Index calculation**: Always get current document content to determine correct indexes
3. **Request order**: Requests are processed in order; later requests see effects of earlier ones
4. **Fields parameter**: Always specify which fields to update to avoid overwriting other properties
5. **RGB colors**: Color values range from 0.0 to 1.0 (not 0-255)
6. **Share permissions**: Ensure the authenticated user has edit access to the document
7. **batchUpdate responses**: Some operations (updateParagraphStyle, insertTable, insertPageBreak, insertInlineImage) return empty or absent `.replies`; output of `"done"` means success with no reply data. An `.error` key indicates failure.

---

## API Reference

- REST Reference: https://developers.google.com/docs/api/reference/rest
- Guides: https://developers.google.com/docs/api/how-tos/overview
- OAuth Playground: https://developers.google.com/oauthplayground/
- Scopes: https://developers.google.com/identity/protocols/oauth2/scopes#docs
- Request Types: https://developers.google.com/docs/api/reference/rest/v1/documents/request
