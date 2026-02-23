---
name: rust-cli
description: |
  General guidance for building Rust CLI programs (clap/anyhow/tracing/serde_json), with
  agent-friendly patterns: JSON output mode, stdout/stderr separation, predictable exit codes,
  integration testing, and a cargo-release based release workflow.
---

# rust-cli - Build Maintainable Rust CLIs

Use this skill when you need to design or implement a Rust CLI with production-grade ergonomics and automation.

For language-agnostic OSS publication/release hygiene (LICENSE/SECURITY.md, release notes, CI policy, repo bootstrap conventions), consult the `oss-publish` skill.

## Defaults (Agent-Friendly)

- CLI parsing: `clap` derive.
- Error handling: `anyhow` (or `thiserror` for library-style errors).
- Logging/diagnostics: `tracing` + `tracing-subscriber` (write logs to stderr).
- Structured output: `serde` + `serde_json`.

## Companion Skill: agentic-cli-design

If this CLI will be operated by AI agents and/or automation, also consult the `agentic-cli-design` skill.
Borrow these concepts: machine-readable output, non-interactive operation, idempotent commands, safe-by-default behavior, observability, and introspection.

## Cross-platform testing pitfalls

### Home directory override (Windows limitation)

On Windows, `directories::BaseDirs` calls Windows API (`SHGetKnownFolderPath`) directly; setting `HOME` or `USERPROFILE` environment variables does not override the returned path. This differs from Unix/Linux/macOS, where `directories` typically reads `$HOME`.

| Platform | Behavior | Override via env? |
|----------|----------|-------------------|
| Unix/Linux/macOS | Reads `$HOME` environment variable | ✅ Yes |
| Windows | Calls Win32 API (`SHGetKnownFolderPath`) | ❌ No |

**Test design patterns:**

```rust
// Pattern 1: Unix-only test (recommended for HOME override)
#[test]
#[cfg(not(target_os = "windows"))]
fn test_home_override() {
    let temp = TempDir::new().unwrap();
    env::set_var("HOME", temp.path());
    // Test code that uses directories::BaseDirs
}

// Pattern 2: Platform-specific logic
#[test]
fn test_cross_platform_home() {
    #[cfg(unix)]
    {
        env::set_var("HOME", "/tmp/test");
        // Unix-specific test
    }
    
    #[cfg(windows)]
    {
        // Windows: use explicit paths or dependency injection
        let test_dir = PathBuf::from("C:\\temp\\test");
        // Windows-specific test
    }
}

// Pattern 3: Dependency injection (best for portability)
fn install_skill_to_path(base_dir: &Path, skill_name: &str) {
    // Accept path directly, avoid BaseDirs in implementation
}

#[test]
fn test_install_with_explicit_path() {
    let temp = TempDir::new().unwrap();
    install_skill_to_path(temp.path(), "my-skill");
    // Portable across all platforms
}
```

**Other common cases with similar issues:**

| Function | Platform behavior | Override via env? |
|----------|-------------------|-------------------|
| `std::env::temp_dir()` | Calls OS API | ❌ No |
| `std::env::current_exe()` | Calls OS API | ❌ No |
| `directories::ProjectDirs` (config/cache) | Windows: API, Unix: XDG vars | Partial (Unix only) |

**Recommendation:** Design functions to accept explicit paths where testability matters; use `BaseDirs` / `ProjectDirs` only in top-level CLI entrypoint or well-isolated modules.

### Flaky tests: time-based cutoffs (SystemTime + second precision)

If you store timestamps as Unix seconds (`i64`) and compute a cleanup cutoff using `SystemTime::now()`, tests can become flaky across platforms.
This often passes on Linux/macOS and fails on Windows due to timing/resolution differences.

Typical failure mode (SQLite example):

- `record()` inserts `created_at = now_secs()` (e.g. `1707408142`).
- a moment later, `cleanup_old_entries(0)` computes `cutoff = now_secs()` (e.g. `1707408143`).
- SQL uses `WHERE created_at < cutoff` which matches the freshly inserted row (`1707408142 < 1707408143`).

Recommended fixes (pick one that matches intended semantics):

- **Tests:** avoid boundary conditions; use a large margin (e.g. `cleanup_old_entries(1)` instead of `0`), and optionally insert a small sleep between operations to avoid same-second edges.
- **Implementation:** define `days <= 0` semantics explicitly (often a no-op), or inject a clock so tests can be deterministic. If you keep second-precision storage, be careful with `<` vs `<=` and how you define "older than N days".

Example test adjustment (stable across platforms):

```rust
#[test]
fn test_cleanup_old_entries() {
    let (ledger, _temp) = create_test_ledger();

    ledger
        .record("test-1", "hash-1", "tweet-1", "success")
        .unwrap();

    // Ensure the cutoff is not computed in the exact same instant.
    std::thread::sleep(std::time::Duration::from_millis(10));

    // Use a safe margin: a fresh entry should not be deleted.
    let deleted = ledger.cleanup_old_entries(1).unwrap();
    assert_eq!(deleted, 0);

    let entry = ledger.lookup("test-1").unwrap();
    assert!(entry.is_some());
}
```

### Other common cross-platform differences

| Feature | Unix/macOS | Windows | Testing approach |
|---------|------------|---------|-----------------|
| Path separator | `/` | `\` | Always use `std::path::Path` |
| Line endings | `\n` | `\r\n` | Explicitly specify in tests or use `.replace()` |
| Executable extension | none | `.exe` | Use `env!("CARGO_BIN_EXE_<name>")` |
| Case sensitivity | Yes | No | Test with varied cases on Windows |
| Temp directory | `/tmp` or `/var/tmp` | `%TEMP%` | Use `std::env::temp_dir()` or `tempfile` crate |


## Rust-specific workflow (minimal)

1) Implement a JSON output mode (e.g. `--json`) with stdout reserved for the result.
2) Send logs/diagnostics to stderr (e.g. via `tracing`).
3) Use predictable exit codes and integration tests that execute the compiled binary.
4) For repo-wide release/quality gate conventions, see `oss-publish`.

## Release workflow (cargo-release)

Use `cargo-release` to bump versions, create git tags, and (optionally) publish to crates.io.

Install:

```bash
cargo install cargo-release
```

### Bump version + tag (no publish)

This is a safe default when you want to control publishing manually:

```bash
# Patch: 0.1.0 -> 0.1.1
cargo release patch --execute --no-confirm --no-publish

# Minor: 0.1.0 -> 0.2.0
cargo release minor --execute --no-confirm --no-publish

# Major: 0.1.0 -> 1.0.0
cargo release major --execute --no-confirm --no-publish
```

Notes:

- `--no-confirm` makes the command non-interactive (agent/CI friendly). Use without it for a safety prompt.
- `--no-publish` keeps crates.io publishing as an explicit step.

After bumping/tagging, publish explicitly:

```bash
cargo publish
```

### Publish preflight checks

Before publishing (especially in automation), prefer these checks:

```bash
cargo fmt
cargo clippy -- -D warnings
cargo test

# Ensures the package can be built as it will be uploaded
cargo publish --dry-run
```

### Optional: publish from a tag

If you need to publish an already-created tag:

```bash
git checkout <tag>
cargo publish
```

Recommendation: keep the release workflow simple.
In most repos, publishing from a clean working tree on the release commit (the one that was tagged) is sufficient.

## Templates

- Crate selection: `rust-cli/references/crates.md`
- Copy/paste scaffolding (Cargo.toml, main.rs, tests, prek config): `rust-cli/references/templates.md`
