---
name: rust-style-guide
description: Apply the user's Rust style conventions when writing or editing Rust code, organizing modules, or editing Cargo manifests.
license: MIT
---

# Rust style guide

## Reuse and dependencies

Reuse suitable code from the project, standard library, or existing dependencies. Check for a suitable crate before building a general-purpose solution. Implement locally when available crates miss a concrete requirement or when a small implementation suffices and a dependency would add disproportionate maintenance, transitive dependencies, or build artifact size.

## Project layout

### Order `Cargo.toml` by purpose

Use this order for the sections present in the manifest so readers can find the package identity and capabilities before its build details.

1. `cargo-features`, if needed, followed by `[package]` and `[workspace]` when present. Keep metadata and workspace settings with their respective tables.
2. Explicit targets (`[lib]`, `[[bin]]`, `[[example]]`, `[[test]]`, `[[bench]]`), then `[features]`.
3. Dependencies. In each group, order regular, build, and dev dependencies. Keep workspace dependency declarations with workspace settings and target-specific dependency tables after the package-wide dependency tables.
4. Build and tooling policy, such as profiles, lints, and dependency overrides. Keep subtables next to their parent group.

Within each dependency table, sort entries by the key used in the manifest. Move comments with their entries and keep the order of array values when it carries meaning.

### Order items in a module by how they are read

Start with module docs and inner attributes, then submodule declarations, re-exports, and imports. Present the main types, traits, and entry points before supporting implementation details. Keep each type next to its inherent and trait implementations. Group related operations by domain or lifecycle, and place a private helper near its caller when that makes the flow easier to follow. Put the test module last.

Preserve order where it affects behavior, including `macro_rules!` scope, implicit enum discriminants, and derived ordering.

### Split large modules at responsibility boundaries

Extract a submodule when a coherent responsibility can be understood and changed through a narrow interface, or when independent subsystems make the parent hard to navigate. Keep each invariant with the code that maintains it. Let the parent present the entry points and coordinate the children. Use responsibility and coupling to decide where to split.

Use `foo.rs` by default, including when children live under `foo/`. Use `foo/mod.rs` only when `foo/` can be delivered as a coherent bundle containing the module entry point and its implementation files, tests, or assets. A child file alone does not establish a bundle. For example, `config.rs` can have `config/validation.rs`, while `wire/mod.rs` can sit alongside the codec, framing, and fixtures that ship together as `wire/`.

## Names and imports

Import items so their names can be used directly, such as `Path` after `use std::path::Path`. Keep conventional qualifications such as `std::env::var` and `serde::Serialize`. Outside those conventions, keep `crate_name::function` or `crate_name::macro!` only when the bare name would cause confusion.

When names collide, use a fully qualified name for a narrow use such as `Read(std::io::Error)` in one error variant. Use a descriptive import alias such as `use std::io::Error as IoError` when the type appears across the module.

## Domain types

Use newtypes such as `UserId(u64)` and `TeamId(u64)` when the compiler should catch accidental substitution between values with the same representation. Use enums for mutually exclusive states and store each state's data on its variant. For example, `Queued`, `Running { started_at }`, and `Finished { result }` can represent a job without allowing unrelated state fields to be populated together.

## Default construction

Use `field: Default::default()` in a default constructor's struct literal when the field type supplies the intended default and its representation is incidental. Spell out values that express a policy. The `tags` initializer delegates to its type, while `retries` expresses the retry policy. This field initializer convention applies even where Clippy's optional `default_trait_access` lint would flag it.

```rust
struct Config {
    tags: Vec<String>,
    retries: u8,
}

impl Default for Config {
    fn default() -> Self {
        Self {
            tags: Default::default(),
            retries: 3,
        }
    }
}
```

## Bindings and control flow

Name intermediates when the name communicates a distinct domain meaning, such as `eligible_accounts` before selecting a recipient. Use iterator chains for straightforward transformations. Use loops when early exits or state carried across iterations drive the logic and are easier to follow in a loop body.

When matching a shared reference and most variants carry `Copy` fields or have no payload, prefer `match *target`. Bind `Copy` fields by value and use `ref` for fields that need to stay borrowed. This moves the dereference to the scrutinee and keeps it out of the arms that use copied values.

```rust
enum Event {
    Retry(u8),
    Delay(u16),
    Message(String),
}

fn describe(target: &Event) -> String {
    match *target {
        Event::Retry(attempt) => format!("retry {}", u16::from(attempt) + 1),
        Event::Delay(seconds) => format!("wait {} ms", u32::from(seconds) * 1_000),
        Event::Message(ref text) => format!("message: {text}"),
    }
}
```

## Error context

Preserve the original cause and add operation context where it first becomes meaningful. When loading configuration, attach the path at the call site that knows which file is being loaded and retain the I/O error as the source. For example, in a project that uses `anyhow`, call `with_context` on the read result with `format!("read configuration from {}", path.display())`.

## Lint suppressions

Use `#[expect(lint_name)]` for intentional lint suppressions. An unfulfilled expectation warns when the lint would no longer fire, making stale suppressions visible. Use `#[allow(lint_name)]` only when `#[expect]` cannot work, such as when the project's minimum supported Rust version predates the attribute.

```rust
#[expect(
    unused_variables,
    clippy::too_many_arguments,
    reason = "the legacy callback requires eight parameters, including a reserved byte"
)]
pub fn encode_legacy_timestamp(
    year_offset: u8,
    month: u8,
    day: u8,
    hour: u8,
    minute: u8,
    second: u8,
    centisecond: u8,
    reserved: u8,
) -> [u8; 7] {
    [year_offset, month, day, hour, minute, second, centisecond]
}
```

Add further conventions only with the user's approval. Leave rules that duplicate Clippy recommendations to Clippy.
