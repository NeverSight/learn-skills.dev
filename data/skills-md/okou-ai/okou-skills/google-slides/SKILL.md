---
name: google-slides
description: Google Slides API for reading and editing presentations and speaker notes. Use when user mentions "Google Slides", "slides", "presentation", "speaker notes", or shares a docs.google.com/presentation link.
---

# Google Slides

Read and edit Google Slides presentations through the Google Drive connector.

> Official docs: `https://developers.google.com/workspace/slides/api/reference/rest`

---

## When to Use

Use this skill when you need to:

- Read presentation structure, slide content, or speaker notes
- Create presentations or slides
- Insert, replace, delete, or format presentation text
- Update speaker notes without changing slide content or design
- Generate slide thumbnails

---

## Prerequisites

Connect the **Google Drive** connector at [app.okou.ai/connectors](https://app.okou.ai/connectors).

> **Troubleshooting:** If requests fail, run `okou doctor check-connector --env-name GOOGLE_DRIVE_TOKEN` or `okou doctor check-connector --url https://slides.googleapis.com/v1/presentations/<presentation-id> --method GET`

The Slides API reuses `$GOOGLE_DRIVE_TOKEN`. Reading presentations is allowed by default. Creating or modifying presentations requires the `presentations.create` or `presentations.write` Google Drive connector permission.

---

## How to Use

Base URL: `https://slides.googleapis.com/v1`

The presentation ID is in the URL:

```text
https://docs.google.com/presentation/d/<presentation-id>/edit
```

### 1. Read a Presentation

Read the presentation structure, slides, page elements, and notes pages:

```bash
curl -s "https://slides.googleapis.com/v1/presentations/<presentation-id>" --header "Authorization: Bearer $GOOGLE_DRIVE_TOKEN" | jq '{presentationId, title, revisionId, slides}'
```

### 2. List Speaker Notes

Read every slide's speaker notes object ID and current text:

```bash
curl -s "https://slides.googleapis.com/v1/presentations/<presentation-id>" --header "Authorization: Bearer $GOOGLE_DRIVE_TOKEN" | jq '[.slides[] | .slideProperties.notesPage as $notes | {slideObjectId: .objectId, speakerNotesObjectId: $notes.notesProperties.speakerNotesObjectId, text: ([$notes.pageElements[]? | select(.objectId == $notes.notesProperties.speakerNotesObjectId) | .shape.text.textElements[]?.textRun.content] | join(""))}]'
```

Always read the presentation immediately before editing. Object IDs can change when a presentation is edited in the Google Slides UI.

### 3. Replace Existing Speaker Notes

Use the `speakerNotesObjectId` returned by the previous request. Write to `/tmp/google_slides_request.json`:

```json
{
  "requests": [
    {
      "deleteText": {
        "objectId": "<speaker-notes-object-id>",
        "textRange": {
          "type": "ALL"
        }
      }
    },
    {
      "insertText": {
        "objectId": "<speaker-notes-object-id>",
        "insertionIndex": 0,
        "text": "Updated speaker notes"
      }
    }
  ],
  "writeControl": {
    "requiredRevisionId": "<revision-id>"
  }
}
```

Then run:

```bash
curl -s -X POST "https://slides.googleapis.com/v1/presentations/<presentation-id>:batchUpdate" --header "Authorization: Bearer $GOOGLE_DRIVE_TOKEN" --header "Content-Type: application/json" -d @/tmp/google_slides_request.json | jq '{presentationId, writeControl}'
```

When updating multiple slides, include each slide's `deleteText` and `insertText` requests in the same `requests` array. A batch update is atomic: if one request is invalid, none of the changes are applied.

### 4. Add Speaker Notes to an Empty Notes Shape

If the speaker notes shape has no text, omit `deleteText`. Write to `/tmp/google_slides_request.json`:

```json
{
  "requests": [
    {
      "insertText": {
        "objectId": "<speaker-notes-object-id>",
        "insertionIndex": 0,
        "text": "New speaker notes"
      }
    }
  ],
  "writeControl": {
    "requiredRevisionId": "<revision-id>"
  }
}
```

Then run:

```bash
curl -s -X POST "https://slides.googleapis.com/v1/presentations/<presentation-id>:batchUpdate" --header "Authorization: Bearer $GOOGLE_DRIVE_TOKEN" --header "Content-Type: application/json" -d @/tmp/google_slides_request.json | jq '{presentationId, writeControl}'
```

The Slides API creates the speaker notes shape automatically when it receives a valid text operation using a `speakerNotesObjectId` that does not yet have a shape.

### 5. Create a Presentation

Write to `/tmp/google_slides_request.json`:

```json
{
  "title": "Quarterly Review"
}
```

Then run:

```bash
curl -s -X POST "https://slides.googleapis.com/v1/presentations" --header "Authorization: Bearer $GOOGLE_DRIVE_TOKEN" --header "Content-Type: application/json" -d @/tmp/google_slides_request.json | jq '{presentationId, title, url: ("https://docs.google.com/presentation/d/" + .presentationId + "/edit")}'
```

### 6. Replace Text Throughout a Presentation

Write to `/tmp/google_slides_request.json`:

```json
{
  "requests": [
    {
      "replaceAllText": {
        "containsText": {
          "text": "Old text",
          "matchCase": true
        },
        "replaceText": "New text"
      }
    }
  ],
  "writeControl": {
    "requiredRevisionId": "<revision-id>"
  }
}
```

Then run:

```bash
curl -s -X POST "https://slides.googleapis.com/v1/presentations/<presentation-id>:batchUpdate" --header "Authorization: Bearer $GOOGLE_DRIVE_TOKEN" --header "Content-Type: application/json" -d @/tmp/google_slides_request.json | jq '.replies[0].replaceAllText'
```

### 7. Create a Slide

Write to `/tmp/google_slides_request.json`:

```json
{
  "requests": [
    {
      "createSlide": {
        "insertionIndex": 1,
        "slideLayoutReference": {
          "predefinedLayout": "TITLE_AND_BODY"
        }
      }
    }
  ],
  "writeControl": {
    "requiredRevisionId": "<revision-id>"
  }
}
```

Then run:

```bash
curl -s -X POST "https://slides.googleapis.com/v1/presentations/<presentation-id>:batchUpdate" --header "Authorization: Bearer $GOOGLE_DRIVE_TOKEN" --header "Content-Type: application/json" -d @/tmp/google_slides_request.json | jq '.replies[0].createSlide.objectId'
```

### 8. Get a Slide Thumbnail

```bash
curl -s "https://slides.googleapis.com/v1/presentations/<presentation-id>/pages/<page-object-id>/thumbnail" --header "Authorization: Bearer $GOOGLE_DRIVE_TOKEN" | jq '{contentUrl, width, height}'
```

---

## Guidelines

1. Read the latest presentation and revision ID immediately before writing.
2. Use `writeControl.requiredRevisionId` to avoid overwriting concurrent edits.
3. Batch related changes so dependent requests succeed or fail together.
4. Only the text inside the speaker notes shape is editable; other notes-page properties are read-only.
5. Preserve slide content and design when the request only concerns speaker notes.
6. Request `presentations.write` only when a mutation is required.
