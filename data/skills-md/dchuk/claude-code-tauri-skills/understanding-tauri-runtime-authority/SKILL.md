---
name: understanding-tauri-runtime-authority
description: Explains how the Tauri runtime authority enforces security policies during application execution, covering ACL-based access control, capability resolution at runtime, scope injection, and command validation for secure IPC.
---

# Tauri Runtime Authority

The runtime authority is a core Tauri component that enforces security policies during application execution. It validates permissions, resolves capabilities, and injects scopes before commands execute.

## What Is Runtime Authority?

Runtime authority is the enforcement layer that sits between the WebView frontend and Tauri commands. It acts as a gatekeeper for all IPC (Inter-Process Communication) requests.

### Core Function

When a webview invokes a Tauri command, the runtime authority:

1. Receives the invoke request from the webview
2. Validates the origin is permitted to call the requested command
3. Confirms the origin belongs to applicable capabilities
4. Injects defined scopes into the request
5. Passes the validated request to the Tauri command

If the origin is not allowed, the request is denied and the command never executes.

### Trust Boundary Model

Tauri implements a trust boundary separating Rust core code from WebView frontend code:

| Zone | Trust Level | Access |
|------|-------------|--------|
| Rust Core | Full trust | Unrestricted system access |
| WebView Frontend | Limited trust | Only exposed resources via IPC |

The runtime authority enforces this boundary at execution time.

## Security Architecture

### How Runtime Authority Fits

```
Frontend (WebView)
       |
       v
[IPC Invoke Request]
       |
       v
+------------------+
| Runtime Authority|  <-- Validates permissions, capabilities, scopes
+------------------+
       |
       v (if allowed)
[Tauri Command Execution]
       |
       v
[System Resources]
```

### Key Components

| Component | Role in Runtime |
|-----------|-----------------|
| Permissions | Define what commands exist and their access rules |
| Capabilities | Map permissions to specific windows/webviews |
| Scopes | Restrict command behavior with path/resource limits |
| Runtime Authority | Enforces all of the above at execution time |

## Capability Resolution at Runtime

When a command is invoked, the runtime authority resolves which capabilities apply.

### Resolution Process

1. **Identify Origin**: Determine which window/webview made the request
2. **Match Capabilities**: Find all capabilities that include this window
3. **Collect Permissions**: Aggregate all permissions from matched capabilities
4. **Check Command Access**: Verify the command is allowed
5. **Merge Scopes**: Combine all applicable scope restrictions
6. **Validate or Deny**: Either proceed with scope injection or reject

### Window Capability Merging

When a window is part of multiple capabilities, security boundaries merge:

```json
// capability-1.json
{
  "identifier": "basic-access",
  "windows": ["main"],
  "permissions": ["fs:allow-read-file"]
}

// capability-2.json
{
  "identifier": "write-access",
  "windows": ["main"],
  "permissions": ["fs:allow-write-file"]
}
```

Result: The "main" window gets both read and write permissions.

### Platform-Specific Resolution

Capabilities can target specific platforms. At runtime, only capabilities matching the current platform are considered:

```json
{
  "identifier": "desktop-features",
  "platforms": ["linux", "macOS", "windows"],
  "windows": ["main"],
  "permissions": ["shell:allow-execute"]
}
```

On iOS/Android, this capability is ignored at runtime.

## Access Control Enforcement

### Deny Precedence Rule

When evaluating access, deny rules always take precedence:

```json
{
  "permissions": [
    {
      "identifier": "fs:allow-read-file",
      "allow": [{ "path": "$HOME/**" }],
      "deny": [{ "path": "$HOME/.ssh/**" }]
    }
  ]
}
```

At runtime:
- Request to read `$HOME/documents/file.txt` - **Allowed**
- Request to read `$HOME/.ssh/id_rsa` - **Denied** (deny rule matches)

### Command-Level Validation

Before any command executes:

1. Runtime authority checks if the command permission exists
2. Verifies the calling window has that permission via its capabilities
3. Validates any scope restrictions are satisfied

```
Window "editor" calls fs.readFile("/home/user/doc.txt")
                        |
                        v
Runtime Authority checks:
  - Does "editor" have fs:allow-read-file? Yes
  - Is "/home/user/doc.txt" in allowed scope? Yes
  - Is it in any deny scope? No
                        |
                        v
Command executes with scopes injected
```

## Scope Injection

### How Scopes Work at Runtime

Scopes are not just validation rules; they are injected into command execution context. Commands can access their applicable scopes to enforce restrictions.

### Scope Variables

At runtime, scope variables resolve to actual paths:

| Variable | Runtime Resolution |
|----------|-------------------|
| `$APP` | Application install directory |
| `$APPDATA` | App data directory |
| `$APPCONFIG` | App config directory |
| `$HOME` | User home directory |
| `$TEMP` | Temporary directory |
| `$DOCUMENT` | Documents directory |
| `$DOWNLOAD` | Downloads directory |
| `$DESKTOP` | Desktop directory |

### Scope Combination Example

```json
{
  "identifier": "main-capability",
  "windows": ["main"],
  "permissions": [
    {
      "identifier": "fs:allow-read-file",
      "allow": [{ "path": "$APPDATA/*" }]
    },
    {
      "identifier": "fs:allow-write-file",
      "allow": [{ "path": "$APPDATA/config.json" }]
    }
  ]
}
```

At runtime for the "main" window:
- Read operations allowed in `$APPDATA/*`
- Write operations only allowed for `$APPDATA/config.json`

## Path Traversal Prevention

The runtime authority includes built-in path traversal protection:

```
Request: /usr/path/to/../../../etc/passwd
Result: DENIED (path traversal detected)
```

Parent directory accessors (`..`) in paths are blocked, ensuring scope restrictions cannot be bypassed.

## Configuration Examples

### Basic Runtime Security Setup

`src-tauri/capabilities/default.json`:

```json
{
  "$schema": "../gen/schemas/desktop-schema.json",
  "identifier": "default-capability",
  "description": "Default runtime permissions",
  "windows": ["main"],
  "permissions": [
    "core:default",
    "core:event:default",
    "core:window:default"
  ]
}
```

### Scoped Filesystem Access

`src-tauri/capabilities/files.json`:

```json
{
  "$schema": "../gen/schemas/desktop-schema.json",
  "identifier": "file-access",
  "description": "Controlled filesystem access",
  "windows": ["main"],
  "permissions": [
    "fs:default",
    {
      "identifier": "fs:allow-read-file",
      "allow": [
        { "path": "$APPDATA/**" },
        { "path": "$DOCUMENT/**" }
      ],
      "deny": [
        { "path": "$DOCUMENT/private/**" }
      ]
    },
    {
      "identifier": "fs:allow-write-file",
      "allow": [
        { "path": "$APPDATA/**" }
      ]
    }
  ]
}
```

### Multi-Window Security Boundaries

`src-tauri/capabilities/editor.json`:

```json
{
  "$schema": "../gen/schemas/desktop-schema.json",
  "identifier": "editor-capability",
  "description": "Full editor permissions",
  "windows": ["editor"],
  "permissions": [
    "core:default",
    "fs:default",
    "fs:allow-read-file",
    "fs:allow-write-file",
    "dialog:default"
  ]
}
```

`src-tauri/capabilities/preview.json`:

```json
{
  "$schema": "../gen/schemas/desktop-schema.json",
  "identifier": "preview-capability",
  "description": "Read-only preview permissions",
  "windows": ["preview"],
  "permissions": [
    "core:window:default",
    "core:event:default",
    {
      "identifier": "fs:allow-read-file",
      "allow": [{ "path": "$TEMP/preview/**" }]
    }
  ]
}
```

At runtime:
- "editor" window can read/write files and open dialogs
- "preview" window can only read from temp preview directory

### HTTP Request Scoping

```json
{
  "identifier": "api-access",
  "windows": ["main"],
  "permissions": [
    {
      "identifier": "http:default",
      "allow": [
        { "url": "https://api.myapp.com/*" },
        { "url": "https://cdn.myapp.com/*" }
      ],
      "deny": [
        { "url": "https://api.myapp.com/admin/*" }
      ]
    }
  ]
}
```

## Runtime Security Guarantees

### What Runtime Authority Protects

| Threat | Protection |
|--------|------------|
| Frontend compromise | Limits damage to granted permissions only |
| Unauthorized command access | Commands denied without explicit capability |
| Path traversal attacks | Built-in prevention at runtime |
| Scope bypass attempts | All scopes enforced before command execution |
| Cross-window access | Each window isolated to its capabilities |

### What Runtime Authority Does NOT Protect

| Threat | Why Not Protected |
|--------|-------------------|
| Malicious Rust code | Rust core has full trust |
| Overly permissive config | Developer responsibility |
| WebView vulnerabilities | OS WebView security boundary |
| Supply chain attacks | Dependency security |

## Debugging Runtime Authority

### Permission Denied Errors

When a command fails with permission denied:

1. **Check Window Label**: Verify the window making the request
2. **Check Capability**: Ensure a capability targets that window
3. **Check Permission**: Verify the permission is in the capability
4. **Check Scope**: Verify the resource is in allowed scope and not denied

### Common Runtime Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Command not allowed | Missing permission in capability | Add permission to capability |
| Scope not applied | No scope defined for permission | Add allow scope |
| Access denied despite allow | Deny rule takes precedence | Remove conflicting deny |
| Window has no permissions | Capability not targeting window | Check window label in capability |

### Verifying Runtime Configuration

Check generated schemas to see what permissions are available:

```
src-tauri/gen/schemas/desktop-schema.json
src-tauri/gen/schemas/mobile-schema.json
```

## Best Practices

### Principle of Least Privilege

Grant only the permissions each window actually needs:

```json
// Good: Specific permissions
{
  "windows": ["settings"],
  "permissions": [
    "core:window:allow-close",
    "fs:allow-read-file"
  ]
}

// Avoid: Overly broad permissions
{
  "windows": ["settings"],
  "permissions": ["fs:default", "shell:default"]
}
```

### Always Define Scopes

Never leave filesystem or network permissions unscoped:

```json
// Good: Scoped access
{
  "identifier": "fs:allow-read-file",
  "allow": [{ "path": "$APPDATA/**" }]
}

// Avoid: Unscoped access
{
  "permissions": ["fs:allow-read-file"]
}
```

### Deny Sensitive Paths

Explicitly deny access to sensitive locations:

```json
{
  "identifier": "fs:allow-read-file",
  "allow": [{ "path": "$HOME/**" }],
  "deny": [
    { "path": "$HOME/.ssh/**" },
    { "path": "$HOME/.gnupg/**" },
    { "path": "$HOME/.aws/**" }
  ]
}
```

### Separate Capabilities by Trust Level

Create distinct capabilities for different security contexts:

```
capabilities/
  main-trusted.json      # Full access for main window
  plugin-limited.json    # Restricted for plugin windows
  preview-readonly.json  # Read-only for preview
```

### Platform-Specific Security

Use platform targeting for OS-specific permissions:

```json
{
  "identifier": "desktop-shell",
  "platforms": ["linux", "macOS", "windows"],
  "windows": ["main"],
  "permissions": ["shell:allow-execute"]
}
```

This prevents desktop-only permissions from being evaluated on mobile.

## Summary

The runtime authority is Tauri's enforcement mechanism for the ACL-based security model:

1. **Every IPC request** passes through runtime authority validation
2. **Capabilities resolve** at runtime based on the calling window
3. **Scopes inject** into command execution context
4. **Deny rules** always take precedence over allow rules
5. **Path traversal** is blocked automatically
6. **Security boundaries merge** when windows have multiple capabilities

Configure capabilities and permissions correctly, and the runtime authority ensures they are enforced consistently throughout application execution.
