---
name: apple-docs
description: Search, browse and read Apple developer documentation from the terminal. Query APIs, frameworks, symbols, sample code, and documentation updates.
---

# apple-docs

CLI for querying Apple Developer Documentation. Searches docs, reads full API pages, lists frameworks, browses symbols, and tracks documentation updates — all from the terminal.

## Getting Started

`apple-docs --schema` — view the full typed command spec at once.

## Commands

```bash
# Search documentation
apple-docs search <query> [--type all|documentation|sample] [--limit 50]

# Read a full documentation page
apple-docs doc <url> [--related] [--references] [--similar] [--platform]

# List all Apple frameworks and technologies
apple-docs technologies [--category "App Frameworks"] [--language swift|occ] [--no-beta] [--limit 200]

# Search symbols within a framework
apple-docs symbols <framework> [--type class|struct|enum|protocol|method|property|func|...] [--pattern "*View"] [--language swift|occ] [--limit 50]

# Get latest documentation updates
apple-docs updates [--category all|wwdc|technology|release-notes] [--technology SwiftUI] [--year 2025] [--search "..."] [--limit 50]

# Browse sample code projects
apple-docs samples [--framework SwiftUI] [--search "camera"] [--beta include|exclude|only] [--limit 50]
```

## Workflow

### Finding an API

1. **Search** for a topic:
   ```bash
   apple-docs search "navigation stack"
   ```

2. **Read** the full documentation page from the URL in search results:
   ```bash
   apple-docs doc https://developer.apple.com/documentation/swiftui/navigationstack --related --platform
   ```

### Exploring a Framework

1. **List symbols** in a framework:
   ```bash
   apple-docs symbols swiftui --type protocol --pattern "*Style"
   ```

2. **Read** a specific symbol's page:
   ```bash
   apple-docs doc https://developer.apple.com/documentation/swiftui/buttonstyle
   ```

### Staying Current

```bash
# Latest documentation updates
apple-docs updates --category wwdc --year 2025

# What's new in a specific framework
apple-docs updates --technology SwiftUI

# New sample code
apple-docs samples --framework RealityKit --beta only
```

## Tips

- `doc --related` includes "See Also" and relationship sections — useful for discovering related APIs.
- `doc --platform` shows platform availability (iOS, macOS, visionOS, etc.) with version numbers.
- `symbols --pattern` supports wildcards: `"*Controller"`, `"UI*"`, `"*View*"`.
- `technologies --language occ` filters Objective-C only frameworks.
- All output is Markdown — pipe to `mq` or other tools as needed.

## Troubleshooting

If `apple-docs` is not found: `bun install -g github:ethan-huo/apple-docs`

No authentication required — all data comes from Apple's public documentation API.
