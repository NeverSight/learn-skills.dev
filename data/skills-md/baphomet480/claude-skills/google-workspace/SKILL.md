---
name: google-workspace
description: Unified Google Workspace skill — Gmail, Calendar, Contacts, Drive, Docs, Sheets, and Photos.
---

# Google Workspace Skill

Unified Google Workspace management for AI agents. One skill, one auth, seven services.

> **Replaces**: `gmail`, `google-calendar`, `google-contacts`, `google-drive`, `google-photos`
> Run `scripts/upgrade.sh` to migrate from the old per-service skills.

## Services

| Service      | Script                       | Capabilities                                                                                                              |
| ------------ | ---------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| **Gmail**    | `scripts/gmail.py`           | Search, read, thread, draft, send, reply, reply-all, forward, trash, filters, empty-trash/spam                            |
| **Calendar** | `scripts/google_calendar.py` | List, get, search, create (RRULE), update, delete, quick-add, secondary calendars, Drive attachments                      |
| **Contacts** | `scripts/contacts.py`        | Search, list, get, create, update, delete contacts                                                                        |
| **Drive**    | `scripts/google_drive.py`    | List, search, upload, download, export, mkdir, move, copy, rename, trash, delete, empty-trash, share, revisions, comments |
| **Docs**     | `scripts/google_docs.py`     | Read text, create, append, replace, insert-heading, format-text, insert-image, comments                                   |
| **Sheets**   | `scripts/google_sheets.py`   | Read, create, append, update, clear, tabs, format-range, freeze-panes, auto-resize                                        |
| **Photos**   | `scripts/google_photos.py`   | List, search, download, upload media, manage albums                                                                       |

## Prerequisites

1. **Google Cloud Project** with these APIs enabled:
   - Gmail API
   - Google Calendar API
   - Google People API
   - Google Drive API
   - Google Docs API
   - Google Sheets API
   - Photos Library API
2. **OAuth 2.0 Credentials** — Desktop app client (`credentials.json`).

## Setup

### One-Time Setup (all services at once)

```bash
uv run scripts/setup_workspace.py
```

This authenticates once with all scopes and stores a unified token at `~/.google_workspace/`.

### Manual Setup (gcloud ADC)

```bash
gcloud auth application-default login \
  --scopes https://mail.google.com/,\
https://www.googleapis.com/auth/calendar,\
https://www.googleapis.com/auth/contacts,\
https://www.googleapis.com/auth/drive,\
https://www.googleapis.com/auth/documents,\
https://www.googleapis.com/auth/spreadsheets,\
https://www.googleapis.com/auth/photoslibrary,\
https://www.googleapis.com/auth/photoslibrary.sharing,\
https://www.googleapis.com/auth/cloud-platform
```

### Verify

```bash
uv run scripts/gmail.py verify
uv run scripts/google_calendar.py verify
uv run scripts/contacts.py verify
uv run scripts/google_drive.py verify
uv run scripts/google_docs.py verify
uv run scripts/google_sheets.py verify
uv run scripts/google_photos.py verify
```

## Credential Lookup Order

Every script checks credentials in this order:

1. **Service-specific env var** (e.g., `GMAIL_CREDENTIALS_DIR`) — for overrides.
2. **Unified directory** `~/.google_workspace/` — primary location.
3. **Legacy per-service directory** (e.g., `~/.gmail_credentials/`) — backward compat.

No migration required. If you already have legacy credentials, they still work.

---

## 🛑 Notice: No More SQLite Cache

The local SQLite caching system (`scripts/cache.py`) has been **removed** in favor of live API queries.
**Do not** attempt to use `cache.py`, `sync`, or `search` against a local database. Always use the live API commands provided by the individual service scripts (e.g., `gmail.py search --query "..."`).

---

## Gmail

Full CRUD Gmail management. Search, read, compose, reply, forward, and manage messages.

### Search for Emails

```bash
# Unread emails from a sender
uv run scripts/gmail.py search --query "from:obiwan@jedi.org is:unread"

# Emails with attachments
uv run scripts/gmail.py search --query "has:attachment subject:plans" --limit 5
```

### Read a Message / Thread

```bash
uv run scripts/gmail.py read --id "18e..."
uv run scripts/gmail.py thread --id "18e..."

# Prefer HTML body
uv run scripts/gmail.py read --id "18e..." --html
```

### Create a Draft

**Safest option** — creates a draft for the user to review before sending.

```bash
uv run scripts/gmail.py draft \
  --to "yoda@dagobah.net" \
  --subject "Training Schedule" \
  --body "Master, when shall we begin the next session?" \
  --cc "mace@jedi.org"

# Create HTML draft
uv run scripts/gmail.py draft --to "yoda@dagobah.net" --subject "HTML Test" --body "<b>Bold</b>" --html
```

### Send an Email

```bash
uv run scripts/gmail.py send \
  --to "yoda@dagobah.net" \
  --subject "Urgent: Sith Sighting" \
  --body "Master, I sense a disturbance in the Force."

# Send HTML
uv run scripts/gmail.py send --to "yoda@dagobah.net" --subject "HTML" --body "<h1>Alert</h1>" --html
```

### Reply / Reply All / Forward

```bash
# Reply (draft by default, --send for immediate)
uv run scripts/gmail.py reply --id "18e..." --body "Acknowledged." --send

# Reply with HTML
uv run scripts/gmail.py reply --id "18e..." --body "<b>Agreed.</b>" --send --html

# Reply all
uv run scripts/gmail.py reply-all --id "18e..." --body "Council noted." --send

# Forward
uv run scripts/gmail.py forward --id "18e..." --to "luke@tatooine.net" --body "FYI"
uv run scripts/gmail.py forward --id "18e..." --to "luke@tatooine.net" --send
```

### Trash / Labels / Attachments / Filters

```bash
uv run scripts/gmail.py trash --id "18e..."
uv run scripts/gmail.py untrash --id "18e..."

# Empty Trash or Spam (permanent — no recovery)
uv run scripts/gmail.py empty-trash
uv run scripts/gmail.py empty-spam

uv run scripts/gmail.py labels
uv run scripts/gmail.py modify-labels --id "18e..." --add STARRED --remove UNREAD

uv run scripts/gmail.py attachments --id "18e..." --output-dir ./downloads

# Filters — auto-route or label incoming mail
uv run scripts/gmail.py list-filters
uv run scripts/gmail.py create-filter \
  --from "noreply@galactic-senate.gov" --archive --mark-read
uv run scripts/gmail.py create-filter \
  --subject "URGENT" --add-label "IMPORTANT"
uv run scripts/gmail.py delete-filter --filter-id "ANe1BmhV..."
```

### Safety Guidelines

1. **Prefer `draft` over `send`** for new compositions — let the user review first.
2. **Reply/Forward defaults to draft** — use `--send` only when explicitly requested.
3. **Trash is reversible** — `empty-trash` is permanent, so confirm intent.

---

## Token Maintenance & Persistence

### 7-Day Expiry Fix (Important)

If you are using a personal Gmail account with a "Testing" GCP project, your refresh token will expire every 7 days.
To fix this, follow the guide at `references/GCP_SETUP.md` to set up a proper app or use an Internal app (Workspace users).

### Background Refresh

To keep your 1-hour access token fresh and avoid CLI latency:

```bash
# Install the maintenance service
cp scripts/workspace-token-maintainer.service ~/.config/systemd/user/
cp scripts/workspace-token-maintainer.timer ~/.config/systemd/user/
systemctl --user enable --now workspace-token-maintainer.timer
```

This runs `scripts/maintain_token.py` every 45 minutes to refresh the token on disk.

---

## Calendar

Full CRUD Calendar management. List, create, update, delete, and search events.

### List / Search Events

```bash
# Next 5 events
uv run scripts/google_calendar.py list --limit 5

# Events in a date range
uv run scripts/google_calendar.py list \
  --after "2026-02-16T00:00:00Z" --before "2026-02-22T23:59:59Z"

# Search by text
uv run scripts/google_calendar.py search --query "Training" --limit 5
```

### Create / Update / Delete Events

```bash
# Timed event
uv run scripts/google_calendar.py create \
  --summary "Jedi Council Meeting" \
  --start "2026-05-04T10:00:00" --end "2026-05-04T11:00:00" \
  --location "Council Chamber, Coruscant" \
  --attendees yoda@dagobah.net mace@jedi.org

# All-day event
uv run scripts/google_calendar.py create \
  --summary "May the 4th" --start "2026-05-04" --end "2026-05-05" --all-day

# Recurring event (RRULE — RFC 5545)
uv run scripts/google_calendar.py create \
  --summary "Weekly Stand-up" \
  --start "2026-03-03T09:00:00" --end "2026-03-03T09:30:00" \
  --rrule "RRULE:FREQ=WEEKLY;BYDAY=MO"

uv run scripts/google_calendar.py create \
  --summary "Monthly Report" \
  --start "2026-03-01T14:00:00" --end "2026-03-01T15:00:00" \
  --rrule "RRULE:FREQ=MONTHLY;BYMONTHDAY=1;COUNT=12"

# Event with Drive file attachment
uv run scripts/google_calendar.py create \
  --summary "Design Review" \
  --start "2026-03-10T14:00:00" --end "2026-03-10T15:00:00" \
  --drive-files "FILE_ID_1" "FILE_ID_2"

# Update (patch semantics — only provided fields change)
uv run scripts/google_calendar.py update --id "abc123" --summary "Updated Meeting"

# Delete
uv run scripts/google_calendar.py delete --id "abc123"
```

### Quick Add / Calendar Management

```bash
uv run scripts/google_calendar.py quick --text "Lunch with Padme tomorrow at noon"

# List all calendars
uv run scripts/google_calendar.py calendars

# Subscribe to a secondary calendar (e.g. public holiday calendar)
uv run scripts/google_calendar.py add-calendar \
  --calendar-id "en.usa#holiday@group.v.calendar.google.com"

# Unsubscribe
uv run scripts/google_calendar.py remove-calendar \
  --calendar-id "en.usa#holiday@group.v.calendar.google.com"
```

---

## Contacts

Full CRUD Contacts management via the People API.

### Search / List / Get

```bash
uv run scripts/contacts.py search --query "Han Solo"
uv run scripts/contacts.py list --limit 50
uv run scripts/contacts.py get --id "people/c12345"
```

### Create / Update / Delete

```bash
uv run scripts/contacts.py create \
  --first "Lando" --last "Calrissian" \
  --email "lando@cloudcity.com" --phone "555-0123" \
  --org "Cloud City Administration" --title "Baron Administrator"

# Update (patch semantics, etag-based conflict detection)
uv run scripts/contacts.py update --id "people/c12345" --phone "555-9999" --title "General"

uv run scripts/contacts.py delete --id "people/c12345"
```

---

## Drive

Full CRUD Drive management. List, search, upload, download, export, organize, and share files.

### List / Search / Get

```bash
uv run scripts/google_drive.py list
uv run scripts/google_drive.py list --folder "FOLDER_ID" --limit 20
uv run scripts/google_drive.py search --query "Death Star plans"
uv run scripts/google_drive.py search --query "budget" --mime-type "application/vnd.google-apps.spreadsheet"
uv run scripts/google_drive.py get --id "FILE_ID"
```

### Upload / Download / Export

```bash
uv run scripts/google_drive.py upload --file "./blueprints.pdf" --folder "FOLDER_ID"
uv run scripts/google_drive.py download --id "FILE_ID" --output "./local_copy.pdf"

# Export Google Workspace docs
uv run scripts/google_drive.py export --id "DOC_ID" --output "./report.docx" --format docx
uv run scripts/google_drive.py export --id "SHEET_ID" --output "./data.csv" --format csv
```

**Export Formats**: Google Docs (pdf, docx, txt, html, md), Sheets (pdf, xlsx, csv), Slides (pdf, pptx), Drawings (pdf, png, svg).

### Organize (mkdir, move, copy, rename)

```bash
uv run scripts/google_drive.py mkdir --name "Project Stardust" --parent "PARENT_ID"
uv run scripts/google_drive.py move --id "FILE_ID" --to "DEST_FOLDER_ID"
uv run scripts/google_drive.py copy --id "FILE_ID" --name "Copy of Plans"
uv run scripts/google_drive.py rename --id "FILE_ID" --name "Updated Plans v2"
```

### Trash / Delete / Share / Revisions / Comments

```bash
# Soft delete (reversible)
uv run scripts/google_drive.py trash --id "FILE_ID"
uv run scripts/google_drive.py untrash --id "FILE_ID"

# Empty entire trash (permanent, no recovery)
uv run scripts/google_drive.py empty-trash

# Permanent delete of a specific file
uv run scripts/google_drive.py delete --id "FILE_ID"

# Share
uv run scripts/google_drive.py share --id "FILE_ID" --email "luke@tatooine.net" --role writer
uv run scripts/google_drive.py share --id "FILE_ID" --type anyone --role reader
uv run scripts/google_drive.py permissions --id "FILE_ID"
uv run scripts/google_drive.py unshare --id "FILE_ID" --permission-id "PERM_ID"

# Revision history
uv run scripts/google_drive.py list-revisions --id "FILE_ID"
uv run scripts/google_drive.py restore-revision --id "FILE_ID" --revision-id "REV_ID"

# Comments
uv run scripts/google_drive.py list-comments --id "FILE_ID"
uv run scripts/google_drive.py add-comment --id "FILE_ID" --content "LGTM, approved."
```

---

## Docs

Google Docs content manipulation. Read text, create documents, and modify text.

### Read / Create

```bash
# Read text from a document
uv run scripts/google_docs.py read --id "DOC_ID"

# Create a new document
uv run scripts/google_docs.py create --title "Project Requirements"
```

### Edit Text

```bash
# Append text to the end of the document
uv run scripts/google_docs.py append --id "DOC_ID" --text "Additional requirements:\n1. Must be fast."

# Replace text
uv run scripts/google_docs.py replace --id "DOC_ID" --old "[COMPANY_NAME]" --new "Acme Corp"

# Insert a heading
uv run scripts/google_docs.py insert-heading --id "DOC_ID" --text "Project Overview" --level 1

# Format a text range (index-based)
uv run scripts/google_docs.py format-text --id "DOC_ID" --start 0 --end 20 --bold
uv run scripts/google_docs.py format-text --id "DOC_ID" --start 0 --end 20 --italic --underline

# Insert a public image
uv run scripts/google_docs.py insert-image --id "DOC_ID" --uri "https://example.com/banner.png"
```

### Comments

```bash
uv run scripts/google_docs.py list-comments --id "DOC_ID"
uv run scripts/google_docs.py add-comment --id "DOC_ID" --content "Please review this section."
```

---

## Sheets

Google Sheets manipulation. Read, append, update, and clear ranges.

### Read / Create

```bash
# Read values from a specific range
uv run scripts/google_sheets.py read --id "SHEET_ID" --range "Sheet1!A1:D10"

# Create a new spreadsheet
uv run scripts/google_sheets.py create --title "Q3 Budget"
```

### Update / Append / Clear / Format

```bash
# Append a row (expects a 2D JSON array)
uv run scripts/google_sheets.py append --id "SHEET_ID" --range "Sheet1!A:A" --values '[["2026-03-01", "Rent", 1200]]'

# Update a specific range
uv run scripts/google_sheets.py update --id "SHEET_ID" --range "Sheet1!A2:C2" --values '[["2026-03-02", "Utilities", 150]]'

# Clear a range
uv run scripts/google_sheets.py clear --id "SHEET_ID" --range "Sheet1!A2:D10"

# Worksheet tab management
uv run scripts/google_sheets.py list-sheets --id "SHEET_ID"
uv run scripts/google_sheets.py add-sheet --id "SHEET_ID" --title "February"
uv run scripts/google_sheets.py rename-sheet --id "SHEET_ID" --title "January" --new-title "Jan 2026"
uv run scripts/google_sheets.py delete-sheet --id "SHEET_ID" --title "February"

# Format a range (bold header, background color)
uv run scripts/google_sheets.py format-range \
  --id "SHEET_ID" --range "Sheet1!A1:D1" --bold --background-color "#4A90D9"

# Freeze the first row and first column
uv run scripts/google_sheets.py freeze-panes --id "SHEET_ID" --rows 1 --cols 1

# Auto-resize columns to fit content
uv run scripts/google_sheets.py auto-resize --id "SHEET_ID" --range "Sheet1!A:D"
```

---

## Photos

Google Photos management. Browse, search, download, upload, and organize albums.

> **API Limitation**: The Photos Library API only allows modifying media items uploaded by this application.

### List / Search / Get / Download

```bash
uv run scripts/google_photos.py list
uv run scripts/google_photos.py search --date-start "2026-01-01" --date-end "2026-02-16"
uv run scripts/google_photos.py search --categories LANDSCAPES FOOD
uv run scripts/google_photos.py get --id "MEDIA_ID"
uv run scripts/google_photos.py download --id "MEDIA_ID" --output "./sunset.jpg"
```

**Search Categories**: ANIMALS, ARTS, BIRTHDAYS, CITYSCAPES, CRAFTS, DOCUMENTS, FASHION, FLOWERS, FOOD, GARDENS, HOLIDAYS, HOUSES, LANDMARKS, LANDSCAPES, NIGHT, PEOPLE, PERFORMANCES, PETS, RECEIPTS, SCREENSHOTS, SELFIES, SPORT, TRAVEL, UTILITY, WEDDINGS, WHITEBOARDS.

### Upload

```bash
uv run scripts/google_photos.py upload \
  --file "./hologram.jpg" --description "Leia's holographic message" --album "ALBUM_ID"
```

### Albums

```bash
uv run scripts/google_photos.py albums
uv run scripts/google_photos.py album-get --id "ALBUM_ID"
uv run scripts/google_photos.py album-create --title "Tatooine Sunsets"
uv run scripts/google_photos.py album-add --album "ALBUM_ID" --items "ITEM_1" "ITEM_2"
uv run scripts/google_photos.py album-remove --album "ALBUM_ID" --items "ITEM_1"
```

---

## Upgrading from v1 (per-service skills)

If you previously installed the separate `gmail`, `google-calendar`, `google-contacts`, `google-drive`, and/or `google-photos` skills:

```bash
# Dry run — shows what will change without modifying anything
bash scripts/upgrade.sh --dry-run

# Run the migration
bash scripts/upgrade.sh
```

The upgrade script:

1. **Consolidates credentials** — copies `token.json` and `credentials.json` from any legacy dir (`~/.gmail_credentials/`, etc.) into `~/.google_workspace/`.
2. **Removes old skill installations** — deletes old per-service skill directories from `.agent/skills/` if present.
3. **Preserves legacy dirs** — does not delete `~/.gmail_credentials/` etc., so existing tools that depend on them still work.
4. **Verifies auth** — confirms the unified token works for all services.

---

## JSON Output

All commands produce JSON for easy parsing. See the individual service sections above for output schemas.
