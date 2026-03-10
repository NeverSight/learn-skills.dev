---
name: analyze-app
description: "Analyze macOS .app bundles to identify technology stacks (Electron, Flutter, Qt, SwiftUI, native, etc.) by delegating to a specialized subagent. Use when given a .app file path, asked about app technology, or investigating how an application was built."
argument-hint: [app-path]
---

# Analyze App — macOS Application Stack Analyzer

Determines the technology stack of any macOS `.app` by inspecting its bundle structure, frameworks, binary, and metadata.

## Workflow

**All analysis MUST be delegated to the `app-stack-analyzer` subagent via the Task tool.**

### Step 1: Parse Input

Extract the `.app` path from the user's input. Accept:
- Full path: `/Applications/Linear.app`
- App name only: `Linear` → resolve to `/Applications/Linear.app`
- Relative path: `./MyApp.app`

If the path doesn't end with `.app`, append `.app`.
If no directory prefix, prepend `/Applications/`.

### Step 2: Validate Path

Confirm the app exists:
```bash
test -d "<resolved_path>/Contents" && echo "Valid" || echo "Invalid"
```

If invalid, inform the user and suggest checking the path or listing `/Applications/`.

### Step 3: Delegate to Subagent

**CRITICAL: Always use the Task tool to delegate analysis.**

```
Task(
  subagent_type: "Bash",
  description: "Analyze <AppName> tech stack",
  prompt: "Analyze the macOS application at '<app_path>' to determine its technology stack.

Execute these commands and report findings:

1. Info.plist analysis:
   plutil -p '<app_path>/Contents/Info.plist'

2. Frameworks inspection:
   ls '<app_path>/Contents/Frameworks/' 2>/dev/null || echo 'No Frameworks directory'

3. Binary analysis:
   file '<app_path>/Contents/MacOS/'*

4. Code signing:
   codesign -dv '<app_path>' 2>&1

5. If Electron detected (Electron Framework.framework exists):
   strings '<app_path>/Contents/Frameworks/Electron Framework.framework/Electron Framework' 2>/dev/null | grep -E '^Chrome/[0-9]' | head -1

6. Resources scan:
   ls '<app_path>/Contents/Resources/' | head -30

Based on ALL collected evidence, provide a structured analysis report:

## App Analysis: <AppName>

### Basic Info
| Property | Value |
|----------|-------|
| Name | ... |
| Bundle ID | ... |
| Version | ... |
| Min macOS | ... |
| Architecture | ... |
| Signed By | ... |

### Technology Stack
| Layer | Technology | Confidence | Evidence |
|-------|-----------|------------|----------|
| Runtime | ... | High/Medium/Low | ... |
| UI Framework | ... | ... | ... |
| Language | ... | ... | ... |
| Build Tool | ... | ... | ... |

### Frameworks Detected
List each framework with its purpose.

### Notable Details
Any interesting architectural or technical findings.

Detection rules:
- Electron: ElectronAsarIntegrity in plist OR Electron Framework.framework in Frameworks
- Flutter: Flutter.framework or FlutterMacOS.framework OR flutter_assets in Resources
- Qt: QtCore.framework or any Qt*.framework
- SwiftUI: SwiftUI references or modern Swift frameworks
- Native (AppKit): No cross-platform framework detected, Apple-only frameworks
- Catalyst: UIOKit.framework presence"
)
```

### Step 4: Present Results

Relay the subagent's analysis report to the user. Add any additional context if relevant.

## Multiple Apps

If the user provides multiple app paths, launch **parallel** Task calls — one per app.

## Examples

**Single app:**
```
/analyze-app /Applications/Linear.app
```

**App name only:**
```
/analyze-app Figma
```

**Multiple apps:**
```
/analyze-app Linear Notion Discord
```

## Success Criteria
- [ ] App path resolved and validated
- [ ] Analysis delegated to subagent (never done inline)
- [ ] Structured report returned with confidence levels
- [ ] Technology stack correctly identified with evidence
