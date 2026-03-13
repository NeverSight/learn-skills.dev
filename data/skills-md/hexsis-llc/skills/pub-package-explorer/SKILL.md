---
name: pub-package-explorer
description: Find and read source code for Dart or Flutter packages from project dependencies or pub.dev. Use when asked to inspect package implementation details, trace dependency code, locate package files by resolving `.dart_tool/package_config.json`, or inspect a package that is not currently installed by unpacking it with `dart pub unpack`.
---

# Pub Package Explorer

Use this workflow to read package source code for Dart or Flutter, including packages not currently installed in the project.

## Choose the Source Strategy

1. Prefer `.dart_tool/package_config.json` when the package is already in the project dependency graph.
2. Use `dart pub unpack` when the package is missing from `package_config.json` or when source needs inspection before adding the dependency.
3. Prefer the installed package path when both are available to match the project-resolved version.

## Resolve a Package Source Path

1. Confirm the project contains `.dart_tool/package_config.json`.
2. Read the package entry from `packages[]` by `name`.
3. Extract:
- `rootUri` (package root, usually in pub cache)
- `packageUri` (usually `lib/`)
4. Build source path as `rootUri + packageUri`.
5. Convert `file://` URI to a filesystem path before reading files.

Use this command pattern:

```bash
PACKAGE="analyzer"
CONFIG=".dart_tool/package_config.json"

SOURCE_URI="$(jq -r --arg pkg "$PACKAGE" '
  .packages[]
  | select(.name == $pkg)
  | (.rootUri + (if (.rootUri | endswith("/")) then "" else "/" end) + .packageUri)
' "$CONFIG")"
```

Convert the URI to a local path:

```bash
SOURCE_PATH="$(printf '%s\n' "$SOURCE_URI" | sed 's#^file://##')"
```

Then inspect source files under that directory (`rg`, `ls`, `cat`).

## Unpack a Package That Is Not Installed

Use this path when the package is not in `.dart_tool/package_config.json` or when pre-install inspection is needed.

```bash
PACKAGE="analyzer"              # or "analyzer:7.4.0"
OUTPUT_DIR="/tmp/pub-unpack"

mkdir -p "$OUTPUT_DIR"
dart pub unpack "$PACKAGE" --output "$OUTPUT_DIR"
```

Find the extracted directory and inspect it:

```bash
PACKAGE_NAME="${PACKAGE%%:*}"
UNPACKED_DIR="$(find "$OUTPUT_DIR" -maxdepth 1 -type d -name "${PACKAGE_NAME}-*" | sort | tail -n 1)"

ls "$UNPACKED_DIR"
ls "$UNPACKED_DIR/lib"
rg --files "$UNPACKED_DIR/lib"
```

Notes:

- `dart pub unpack` downloads and extracts a package even when it is not in the current project's dependencies.
- Use `--force` if the output directory already contains an unpacked copy that must be overwritten.
- `--output` controls where the extracted `<package>-<version>` folder is created.

## Useful Variants

- Return only the package root:

```bash
jq -r --arg pkg "$PACKAGE" '
  .packages[]
  | select(.name == $pkg)
  | .rootUri
' .dart_tool/package_config.json
```

- Return both root and package URI:

```bash
jq -r --arg pkg "$PACKAGE" '
  .packages[]
  | select(.name == $pkg)
  | "\(.rootUri)\t\(.packageUri)"
' .dart_tool/package_config.json
```

## Verification and Error Handling

- If no package matches in `package_config.json`, switch to `dart pub unpack` instead of stopping.
- If `.dart_tool/package_config.json` is missing, run dependency resolution first (`dart pub get` or `flutter pub get`) and retry.
- Prefer reading from `rootUri + packageUri` because package APIs are exposed from that subpath, not always from the package root.
- If `dart pub unpack` fails, report the exact failure (for example network access, invalid descriptor, or permissions for output path).
