---
name: flutter-assets-compress
description: Generate Flutter 1x and 2x image assets from existing 3.0x sources using a pure Dart script, compress PNG/JPG/WebP outputs, and update an architecture-appropriate AppImages asset index. Use when the user asks to normalize Flutter image assets, derive lower-density assets from @3x files, or create tool/image_assets.dart without external CLI tools.
license: MIT
metadata:
  author: ducafecat
  version: "1.0.2"
  compatibility: Requires a Flutter or Dart project with assets/images/3.0x source images. Script execution requires Dart SDK and package dependencies image ^4.8.0 and path ^1.9.1.
---

# Flutter Assets Compress

## Purpose

Create a pure Dart image asset tool for Flutter projects that:

- scans `assets/images/3.0x/`
- generates `assets/images/2.0x/<name>` at two-thirds size
- generates `assets/images/<name>` at one-third size
- compresses supported image outputs
- writes the `AppImages` index to the path matching the project's state-management architecture

## Use this skill when

- The user wants to generate 1x and 2x assets from 3x Flutter images.
- The source images live under `assets/images/3.0x/`.
- The user wants a repeatable Dart script at `tool/image_assets.dart`.
- The user requires image processing without ImageMagick, pngquant, cwebp, or other external CLI tools.

## Do not use this skill when

- The project has no Flutter-style asset directory.
- The user wants manual design editing rather than deterministic resizing.
- The source images are not available.
- The user requires external compression tools.

## Required inputs

Identify or confirm:

1. Project root.
2. `assets/images/3.0x/` source directory.
3. Existing `pubspec.yaml`.
4. Existing `tool/image_assets.dart`, if present.
5. Whether the project uses Riverpod or GetX, based on `pubspec.yaml`, imports, and existing directory structure.
6. Existing `lib/core/assets/app_images.dart` or `lib/common/values/app_images.dart`, if present.

## Dependencies

Ensure these Dart dependencies are available:

```yaml
dependencies:
  image: ^4.8.0
  path: ^1.9.1
```

## Workflow

### 1. Inspect existing assets

Scan `assets/images/3.0x/` and process image files only.

Supported outputs:

- PNG: `encodePng(level: 6)`
- JPG/JPEG: `encodeJpg(quality: 85)`
- WebP, when supported by the Dart image package: quality `80`

Ignore non-image files.

### 2. Create or update the script

Create `tool/image_assets.dart` if it does not exist. If it already exists, read it first and merge only the required behavior.

The script must:

- use only Dart packages, not system commands
- create missing output directories
- overwrite duplicate output files
- skip unreadable images and print a warning
- produce a summary with total images and successful images
- write the asset index to the architecture-specific path selected below

### 3. Select the asset index path

Inspect `pubspec.yaml`, project imports, and the existing directory structure before generating the index:

- For a Riverpod project, write `lib/core/assets/app_images.dart`.
- For a GetX project, write `lib/common/values/app_images.dart`.
- If both frameworks are present, preserve the existing `app_images.dart` location. If neither location exists, use the architecture that owns the application's current state-management and routing setup.

Create missing parent directories for the selected path. Do not generate both files and do not move or modify an index belonging to the other architecture.

### 4. Generate the asset index

Write constants for generated 1x image paths:

```dart
abstract final class AppImages {
  AppImages._();

  static const defaultPng = 'assets/images/default.png';
  static const homePlaceholderPng = 'assets/images/home_placeholder.png';
}
```

Convert asset paths to lower camel case names and include the extension in the constant name when useful to avoid collisions.

### 5. Run the script

Run:

```sh
dart run tool/image_assets.dart
```

Report:

- changed directory structure
- total source images
- successful outputs
- skipped files
- generated `AppImages` example

## Safety rules

- Do not call external CLI image tools.
- Do not delete source images.
- Do not modify unrelated assets.
- Do not install packages without permission when network access is required.
- Preserve existing custom script behavior when merging.

## Definition of done

The task is complete when:

- `tool/image_assets.dart` exists and is runnable.
- 1x and 2x assets are generated from all readable 3x images.
- The architecture-specific asset index is updated: `lib/core/assets/app_images.dart` for Riverpod or `lib/common/values/app_images.dart` for GetX.
- Failures are reported without stopping the whole batch.
- The final report includes processing statistics.
