---
name: optimizing-tauri-binary-size
description: Guides users through Tauri binary size optimization techniques to produce small, efficient desktop application bundles using Cargo profile settings and build configurations.
---

# Tauri Binary Size Optimization

This skill provides guidance on optimizing Tauri application binary sizes for production releases.

## Why Tauri Produces Small Binaries

Tauri is designed from the ground up to produce minimal binaries:

1. **Native Webview**: Uses the operating system's native webview instead of bundling Chromium (unlike Electron)
2. **Rust Backend**: Compiles to efficient native code with no runtime overhead
3. **Tree Shaking**: Only includes code that is actually used
4. **No V8 Engine**: Leverages existing system components rather than bundling a JavaScript engine

### Size Comparison

| Framework | Minimum Binary Size |
|-----------|---------------------|
| Tauri     | ~3-6 MB             |
| Electron  | ~120-180 MB         |
| NW.js     | ~80-100 MB          |

The dramatic size difference comes from Tauri's architectural decision to use native system webviews rather than bundling a full browser engine.

## Cargo.toml Optimization Settings

Configure release profile settings in `src-tauri/Cargo.toml` to minimize binary size.

### Recommended Stable Toolchain Configuration

```toml
[profile.release]
codegen-units = 1    # Compile crates one at a time for better LLVM optimization
lto = true           # Enable link-time optimization across all crates
opt-level = "s"      # Optimize for binary size (alternative: "z" for even smaller)
panic = "abort"      # Remove panic unwinding code
strip = true         # Strip debug symbols from final binary
```

### Configuration Options Explained

| Option | Values | Description |
|--------|--------|-------------|
| `codegen-units` | `1` | Reduces parallelism but allows LLVM to perform better whole-program optimization |
| `lto` | `true`, `"thin"`, `"fat"` | Link-time optimization; `true` or `"fat"` produces smallest binaries |
| `opt-level` | `"s"`, `"z"`, `"3"` | `"s"` balances size/speed, `"z"` prioritizes size, `"3"` prioritizes speed |
| `panic` | `"abort"` | Removes panic handler code, reducing binary size |
| `strip` | `true`, `"symbols"`, `"debuginfo"` | Removes symbols and debug information from binary |

### Nightly Toolchain Options

For projects using the nightly Rust toolchain, additional optimizations are available:

```toml
[profile.release]
codegen-units = 1
lto = true
opt-level = "s"
panic = "abort"
strip = true
trim-paths = "all"    # Remove file path information from binary

[profile.release.build-override]
opt-level = "s"       # Also optimize build scripts
```

You can also set rustflags for additional control:

```toml
[profile.release]
rustflags = ["-Cdebuginfo=0", "-Zthreads=8"]
```

## Tauri Build Configuration

### Remove Unused Commands (Tauri 2.4+)

Tauri 2.4 introduced the ability to automatically remove code for commands not permitted in your Access Control List (ACL). Add this to `tauri.conf.json`:

```json
{
  "build": {
    "removeUnusedCommands": true
  }
}
```

This feature:
- Analyzes your ACL configuration
- Removes Tauri command handlers that are not allowed
- Reduces binary size without changing functionality
- Works automatically during release builds

### Minimal Feature Set

Only enable Tauri features you actually need in `src-tauri/Cargo.toml`:

```toml
[dependencies]
tauri = { version = "2", features = ["macos-private-api"] }
# Avoid enabling unnecessary features like:
# - "devtools" in production
# - "protocol-asset" if not serving local assets
# - "tray-icon" if not using system tray
```

## Frontend Optimization

While this skill focuses on Rust/Tauri optimization, frontend bundle size also affects the final application:

1. **Use a bundler**: Vite, webpack, or similar with tree shaking
2. **Code splitting**: Load features on demand
3. **Minimize dependencies**: Audit and remove unused npm packages
4. **Compress assets**: Optimize images and other static assets

## Build Commands

### Standard Release Build

```bash
cd src-tauri
cargo tauri build --release
```

### Using Nightly Toolchain

```bash
cd src-tauri
cargo +nightly tauri build --release
```

### Check Binary Size

After building, check your binary size:

```bash
# macOS
ls -lh src-tauri/target/release/bundle/macos/*.app/Contents/MacOS/*

# Linux
ls -lh src-tauri/target/release/bundle/appimage/*.AppImage

# Windows
dir src-tauri\target\release\bundle\msi\*.msi
```

## Complete Example Configuration

Here is a complete `src-tauri/Cargo.toml` optimized for minimal binary size:

```toml
[package]
name = "my-tauri-app"
version = "0.1.0"
edition = "2021"

[dependencies]
tauri = { version = "2", features = [] }
serde = { version = "1", features = ["derive"] }
serde_json = "1"

[build-dependencies]
tauri-build = { version = "2", features = [] }

[profile.release]
codegen-units = 1
lto = true
opt-level = "s"
panic = "abort"
strip = true

[profile.release.package."*"]
opt-level = "s"
```

And corresponding `tauri.conf.json`:

```json
{
  "productName": "my-tauri-app",
  "version": "0.1.0",
  "identifier": "com.example.my-tauri-app",
  "build": {
    "removeUnusedCommands": true,
    "beforeBuildCommand": "npm run build",
    "frontendDist": "../dist"
  },
  "bundle": {
    "active": true,
    "targets": "all",
    "icon": ["icons/icon.png"]
  }
}
```

## Optimization Trade-offs

| Setting | Size Impact | Build Time | Runtime Performance |
|---------|-------------|------------|---------------------|
| `codegen-units = 1` | Smaller | Slower | Better |
| `lto = true` | Smaller | Much slower | Better |
| `opt-level = "s"` | Smaller | Similar | Slightly slower |
| `opt-level = "z"` | Smallest | Similar | Slower |
| `panic = "abort"` | Smaller | Faster | No unwinding |
| `strip = true` | Smaller | Similar | No impact |

## Troubleshooting

### Binary Still Large

1. Check for debug builds: Ensure you are using `--release` flag
2. Audit dependencies: Run `cargo tree` to see dependency graph
3. Check for duplicate dependencies: Different versions of same crate
4. Verify strip is working: Use `file` command to check for debug symbols

### Build Failures with LTO

If `lto = true` causes build failures:
- Try `lto = "thin"` as a fallback
- Ensure sufficient memory (LTO is memory-intensive)
- Update Rust toolchain to latest version

### Nightly Features Not Working

Ensure nightly is installed and active:

```bash
rustup install nightly
rustup default nightly
# Or use +nightly flag with cargo commands
```

## References

- [Tauri Size Documentation](https://v2.tauri.app/concept/size)
- [Cargo Profile Settings](https://doc.rust-lang.org/cargo/reference/profiles.html)
- [Rust Performance Book](https://nnethercote.github.io/perf-book/)
