---
name: apple-suite
description: Automates macOS apps via AppleScript and URL schemes — Notes, Reminders, Maps, Mail, Calendar, Terminal, Shortcuts, Contacts, Photos, App Store search, and Phone. Runs locally through osascript with no API keys and no network for the AppleScript operations. Each app's scriptability is honestly assessed; non-scriptable apps (VoiceMemos, Passwords, Find My, Activity Monitor, App Store listing) are documented with their real limitations rather than faked.
when_to_use: Any macOS workflow that touches Apple's built-in apps — capture a note, add a reminder, open directions, check mail, list calendar events, run a terminal command, search contacts, browse photos, or search the App Store. NOT a sync tool or a replacement for iCloud. Find My, VoiceMemos, Passwords, and Activity Monitor are not scriptable — documented honestly.
version: 1.0.0
license: MIT
metadata:
  agentskills:
    tags: [macos, apple, notes, reminders, maps, mail, calendar, terminal, contacts, photos, automation]
---

# Apple Suite

Drive macOS built-ins directly from an agent session — no API keys, no
network for the AppleScript operations, just the apps already on the machine.

## Commands

```bash
# Notes
python3 scripts/apple_suite.py notes list [--limit 20] [--json]
python3 scripts/apple_suite.py notes create --title "Title" --body "Body text"
python3 scripts/apple_suite.py notes search "keyword"

# Reminders
python3 scripts/apple_suite.py reminders list [--json]
python3 scripts/apple_suite.py reminders add --title "Task" [--due "2026-08-27 09:00"]
python3 scripts/apple_suite.py reminders complete --title "Task"

# Maps
python3 scripts/apple_suite.py maps search "coffee near me"
python3 scripts/apple_suite.py maps directions --from "Home" --to "Office"
python3 scripts/apple_suite.py maps open "123 Main St, City"

# Mail
python3 scripts/apple_suite.py mail unread
python3 scripts/apple_suite.py mail list [--limit 20]

# Calendar
python3 scripts/apple_suite.py calendar list
python3 scripts/apple_suite.py calendar today
python3 scripts/apple_suite.py calendar add --title "Meeting" --date "2026-08-27 14:00"

# Terminal
python3 scripts/apple_suite.py terminal run "echo hello"

# Shortcuts
python3 scripts/apple_suite.py shortcuts list
python3 scripts/apple_suite.py shortcuts run "Calculate Tip"

# Contacts
python3 scripts/apple_suite.py contacts count
python3 scripts/apple_suite.py contacts search "Jane"

# Photos
python3 scripts/apple_suite.py photos count
python3 scripts/apple_suite.py photos albums

# App Store
python3 scripts/apple_suite.py appstore search "terminal"

# Phone
python3 scripts/apple_suite.py phone open "+1234567890"
```

## What is scriptable

| App | List | Create | Complete | Search | Notes |
|---|---|---|---|---|---|
| Notes | yes | yes | — | yes | folders included in list |
| Reminders | yes | yes | yes | by title | due dates optional |
| Maps | — | — | — | yes | opens Maps.app with query or directions |
| Mail | yes | — | — | — | unread count, inbox list with sender/date |
| Calendar | yes | yes | — | — | calendars, today's events, add events |
| Terminal | — | — | — | — | run commands, capture output |
| Shortcuts | yes | — | — | — | run by name (may timeout on interactive shortcuts) |
| Contacts | yes | — | — | yes | count, search by name |
| Photos | yes | — | — | — | media item count, album names |
| App Store | — | — | — | yes | search via macappstore:// URL scheme |
| Phone | — | — | — | — | opens tel: URL |

## Not scriptable (documented honestly)

| App | Limitation |
|---|---|
| VoiceMemos | No AppleScript dictionary (-2741 on every access pattern). Recordings are in ~/Library/Application Support/com.apple.voicememos/ but the format is private. |
| Passwords | No AppleScript API. Only the Settings UI. |
| Find My | No AppleScript API. Use the Find My app or Siri. |
| Activity Monitor | No AppleScript API for process data. Use `ps`, `top`, or `vm_stat`. |
| App Store (listing) | No AppleScript API for installed apps or updates. Search works via URL scheme. |

## Permissions

macOS will prompt for Automation permission the first time each app is
driven. Grant it once and subsequent calls are silent. The skill never
requests broader access than the specific app it drives.

## Exit codes

0 = success, 1 = app-level error (not found, permission denied), 2 = usage
error or non-macOS host.
