---
name: configuring-tauri-scopes
description: Guides users through configuring Tauri command scopes for security, including filesystem restrictions, URL patterns, dynamic scope management, and capability-based access control.
---

# Tauri Command Scopes

This skill covers configuring scopes in Tauri v2 applications to control fine-grained access to commands and resources.

## What Are Scopes?

Scopes are a granular authorization mechanism in Tauri that controls what specific operations a command can perform. They function as fine-grained permission boundaries beyond basic command access.

### Key Characteristics

- **Allow scopes**: Explicitly permit certain operations
- **Deny scopes**: Explicitly restrict certain operations
- **Deny takes precedence**: When both exist, deny rules always win
- **Command responsibility**: The command implementation must validate and enforce scope restrictions

### How Scopes Work

The scope is passed to the command during execution. The command implementation is responsible for validating against the scope and enforcing restrictions. This means developers must carefully implement scope validation to prevent bypasses.

## Scope Configuration Location

Scopes are configured in capability files located at:
- `src-tauri/capabilities/default.json` (primary)
- `src-tauri/capabilities/*.json` (additional capability files)

## Filesystem Scopes

The filesystem plugin uses glob-compatible path patterns to define accessible paths.

### Basic Filesystem Scope Configuration

```json
{
  "$schema": "../gen/schemas/desktop-schema.json",
  "identifier": "default",
  "description": "Default capability for the application",
  "windows": ["main"],
  "permissions": [
    {
      "identifier": "fs:scope",
      "allow": [{ "path": "$APPDATA" }, { "path": "$APPDATA/**" }]
    }
  ]
}
```

### Command-Specific Scopes

Restrict individual filesystem operations rather than global access:

```json
{
  "permissions": [
    {
      "identifier": "fs:allow-read-text-file",
      "allow": [{ "path": "$DOCUMENT/**" }]
    },
    {
      "identifier": "fs:allow-write-text-file",
      "allow": [{ "path": "$HOME/notes.txt" }]
    }
  ]
}
```

### Combined Allow and Deny Scopes

```json
{
  "permissions": [
    {
      "identifier": "fs:allow-rename",
      "allow": [{ "path": "$HOME/**" }],
      "deny": [{ "path": "$HOME/.config/**" }]
    }
  ]
}
```

### Available Path Variables

Tauri provides runtime-injected variables for common system directories:

| Variable | Description |
|----------|-------------|
| `$APPCONFIG` | Application config directory |
| `$APPDATA` | Application data directory |
| `$APPLOCALDATA` | Application local data directory |
| `$APPCACHE` | Application cache directory |
| `$APPLOG` | Application log directory |
| `$AUDIO` | User audio directory |
| `$CACHE` | System cache directory |
| `$CONFIG` | System config directory |
| `$DATA` | System data directory |
| `$DESKTOP` | User desktop directory |
| `$DOCUMENT` | User documents directory |
| `$DOWNLOAD` | User downloads directory |
| `$EXE` | Application executable directory |
| `$HOME` | User home directory |
| `$PICTURE` | User pictures directory |
| `$PUBLIC` | Public directory |
| `$RESOURCE` | Application resource directory |
| `$TEMP` | Temporary directory |
| `$VIDEO` | User video directory |

## Scope Patterns

Scopes support glob patterns for flexible path matching.

### Pattern Examples

```json
{
  "permissions": [
    {
      "identifier": "fs:scope",
      "allow": [
        { "path": "$APPDATA/databases/*" },
        { "path": "$DOCUMENT/**/*.txt" },
        { "path": "$HOME/project/src/**" }
      ],
      "deny": [
        { "path": "$HOME/.ssh/**" },
        { "path": "$HOME/.gnupg/**" }
      ]
    }
  ]
}
```

### Pattern Syntax

| Pattern | Meaning |
|---------|---------|
| `*` | Matches any characters except path separator |
| `**` | Matches any characters including path separator (recursive) |
| `?` | Matches a single character |
| `[abc]` | Matches any character in brackets |

### Path Traversal Prevention

Tauri prevents path traversal attacks. These paths are NOT allowed:
- `/usr/path/to/../file`
- `../path/to/file`

## HTTP Plugin Scopes

The HTTP plugin uses URL patterns to control network access.

### URL Scope Configuration

```json
{
  "permissions": [
    {
      "identifier": "http:default",
      "allow": [{ "url": "https://*.tauri.app" }],
      "deny": [{ "url": "https://private.tauri.app" }]
    }
  ]
}
```

### URL Pattern Examples

```json
{
  "permissions": [
    {
      "identifier": "http:default",
      "allow": [
        { "url": "https://api.example.com/*" },
        { "url": "https://*.cdn.example.com/**" }
      ]
    }
  ]
}
```

## Defining Custom Permissions with Scopes (TOML)

For plugins or custom commands, define permissions in TOML files.

### Basic Permission with Scope

```toml
# permissions/my-permission.toml
[[permission]]
identifier = "scope-appdata-recursive"
description = "Recursive access to APPDATA folder"

[[permission.scope.allow]]
path = "$APPDATA/**"
```

### Permission with Deny Scope

```toml
[[permission]]
identifier = "deny-sensitive-data"
description = "Denies access to sensitive directories"
platforms = ["linux", "macos"]

[[permission.scope.deny]]
path = "$HOME/.ssh/**"

[[permission.scope.deny]]
path = "$HOME/.gnupg/**"
```

### Permission Sets

Combine permissions into reusable sets:

```toml
[[set]]
identifier = "safe-appdata-access"
description = "Allows APPDATA access while denying sensitive folders"
permissions = ["scope-appdata-recursive", "deny-sensitive-data"]
```

## Dynamic Scopes (Runtime Management)

Tauri allows runtime scope modification using the `FsExt` trait from Rust.

### Basic Runtime Scope Expansion

```rust
use tauri_plugin_fs::FsExt;

pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_fs::init())
        .setup(|app| {
            let scope = app.fs_scope();
            // Allow a specific directory (non-recursive)
            scope.allow_directory("/path/to/directory", false)?;
            // Check what's currently allowed
            dbg!(scope.allowed());
            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

### Tauri Command for Scope Expansion

```rust
use tauri_plugin_fs::FsExt;

#[tauri::command]
fn expand_scope(
    app_handle: tauri::AppHandle,
    folder_path: std::path::PathBuf
) -> Result<(), String> {
    // Verify path before expanding scope
    if !folder_path.exists() {
        return Err("Path does not exist".to_string());
    }

    // true = allow inner directories recursively
    app_handle
        .fs_scope()
        .allow_directory(&folder_path, true)
        .map_err(|err| err.to_string())
}
```

### Allow Specific File

```rust
#[tauri::command]
fn allow_file(
    app_handle: tauri::AppHandle,
    file_path: std::path::PathBuf
) -> Result<(), String> {
    app_handle
        .fs_scope()
        .allow_file(&file_path)
        .map_err(|err| err.to_string())
}
```

### Security Warning

Dynamic scope expansion should be used carefully:
- Validate paths before expanding scope
- Prefer static configuration when possible
- Never expand scope based on unvalidated user input

## Remote URL Scopes (Capabilities)

Control which remote URLs can access your application's commands.

```json
{
  "identifier": "remote-api-access",
  "description": "Allow remote access from specific domains",
  "windows": ["main"],
  "remote": {
    "urls": ["https://*.mydomain.dev", "https://app.example.com"]
  },
  "permissions": ["core:default"]
}
```

## Complete Capability File Example

```json
{
  "$schema": "../gen/schemas/desktop-schema.json",
  "identifier": "default",
  "description": "Default capability for desktop application",
  "windows": ["main", "settings"],
  "platforms": ["linux", "macos", "windows"],
  "permissions": [
    "core:default",
    "core:window:allow-set-title",
    {
      "identifier": "fs:default"
    },
    {
      "identifier": "fs:allow-read-text-file",
      "allow": [
        { "path": "$DOCUMENT/**/*.md" },
        { "path": "$DOCUMENT/**/*.txt" }
      ]
    },
    {
      "identifier": "fs:allow-write-text-file",
      "allow": [{ "path": "$APPDATA/notes/**" }],
      "deny": [{ "path": "$APPDATA/notes/.secret/**" }]
    },
    {
      "identifier": "http:default",
      "allow": [{ "url": "https://api.example.com/*" }]
    }
  ]
}
```

## Security Best Practices

1. **Minimize scope**: Only allow paths and URLs that are absolutely necessary
2. **Use deny rules**: Explicitly block sensitive directories even within allowed paths
3. **Prefer command-specific scopes**: Use `fs:allow-read-text-file` over global `fs:scope`
4. **Validate dynamic scopes**: Always verify paths before runtime scope expansion
5. **Audit scope enforcement**: Command developers must implement proper scope validation
6. **Use path variables**: Prefer `$APPDATA` over hardcoded paths for portability

## Common Scope Patterns

### Read-Only Application Data

```json
{
  "permissions": [
    {
      "identifier": "fs:allow-read-text-file",
      "allow": [{ "path": "$APPDATA/**" }]
    },
    {
      "identifier": "fs:allow-exists",
      "allow": [{ "path": "$APPDATA/**" }]
    }
  ]
}
```

### User Document Access

```json
{
  "permissions": [
    {
      "identifier": "fs:scope",
      "allow": [{ "path": "$DOCUMENT/**" }],
      "deny": [
        { "path": "$DOCUMENT/.hidden/**" },
        { "path": "$DOCUMENT/**/*.key" }
      ]
    }
  ]
}
```

### API-Only HTTP Access

```json
{
  "permissions": [
    {
      "identifier": "http:default",
      "allow": [
        { "url": "https://api.myapp.com/v1/*" },
        { "url": "https://cdn.myapp.com/**" }
      ],
      "deny": [
        { "url": "https://api.myapp.com/v1/admin/*" }
      ]
    }
  ]
}
```

## Troubleshooting

### "Path not allowed on the configured scope"

This error indicates the requested path is outside the configured scope. Solutions:

1. Add the path to your capability's allow list
2. Check for typos in path variables
3. Verify glob patterns match the intended paths
4. Check if a deny rule is blocking the path

### Testing Scope Configuration

Run in development mode to test permissions:

```bash
pnpm tauri dev
# or
cargo tauri dev
```

Permission errors will appear in the console indicating which permissions need configuration.

## References

- [Command Scopes Documentation](https://v2.tauri.app/security/scope/)
- [Permissions Overview](https://v2.tauri.app/security/permissions/)
- [Capabilities Reference](https://v2.tauri.app/reference/acl/capability/)
- [Filesystem Plugin](https://v2.tauri.app/plugin/file-system/)
- [HTTP Plugin](https://v2.tauri.app/plugin/http-client/)
