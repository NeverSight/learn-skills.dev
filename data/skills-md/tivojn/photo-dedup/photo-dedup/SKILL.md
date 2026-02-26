---
name: photo-dedup
description: "Find & select unique photos from duplicates using perceptual hashing. Interactive browser UI for reviewing duplicate groups. Use when user says: dedup photos, find duplicate photos, unique photos, remove duplicate images, photo dedup, /photo-dedup."
user_invocable: true
---

# Photo Dedup — Find & Select Unique Photos from Duplicates

Use this skill when the user wants to deduplicate photos, find unique images from a large set, remove similar/duplicate photos, or organize photos by uniqueness. Trigger phrases: "dedup photos", "find duplicate photos", "unique photos", "remove duplicate images", "photo dedup", "/photo-dedup".

## Overview

This skill processes a folder of photos (typically hundreds from events like school photography), identifies duplicates and near-duplicates using perceptual hashing, and organizes them into unique vs duplicate folders. It's designed for the workflow where ~500 photos come in but only ~100 are truly unique.

## How It Works

1. **Perceptual Hashing** — Each image is converted to a perceptual hash (pHash) that represents its visual content. Similar-looking images produce similar hashes, even if they differ in resolution, compression, or minor edits.

2. **Clustering** — Images are grouped by hash similarity. Each cluster represents one "scene" or "shot". The best image from each cluster (largest file size = highest quality) is selected as the unique representative.

3. **Output** — Unique photos are copied to a `unique/` folder. A report is generated showing how many duplicates were found and the cluster groupings.

## Usage

### Basic — Dedup a folder:
```
/photo-dedup ~/Photos/school-event/
```

### With custom threshold:
```
/photo-dedup ~/Photos/school-event/ --threshold 8
```
Threshold controls similarity sensitivity (default: 6, range 0-20). Lower = stricter matching, higher = more aggressive grouping.

### Preview mode (no file copying):
```
/photo-dedup ~/Photos/school-event/ --preview
```

## Workflow

When the user invokes this skill:

1. **Validate input** — Confirm the source folder exists and contains images
2. **Install dependencies if needed** — `pip3 install Pillow imagehash pillow-heif`
3. **Run the dedup scan**:
   ```bash
   python3 ~/.claude/skills/photo-dedup/scripts/dedup.py <source_folder> --preview [--threshold N]
   ```
4. **Report results** to the user (total, unique, duplicates)
5. **Launch the review server** (runs locally, opens browser automatically):
   ```bash
   python3 ~/.claude/skills/photo-dedup/scripts/review_server.py /tmp/dedup_report_<folder_name>.json --output ~/Desktop/selected_photos &
   ```
   The user can then:
   - See all duplicate groups side by side (Notion-style UI)
   - Click to select which photo to keep from each group
   - Use "Auto-select best" for one-click defaults
   - Hit "Save selected" — photos are copied instantly, no Terminal needed
6. **After user saves**, tell them where the selected photos are
7. **Kill the server** when done: `kill $(pgrep -f review_server)`

The review server is a lightweight local HTTP server — no install, no config, just Python.
Non-technical users only interact with the browser. One click to save.

## Output Structure

```
~/Desktop/selected_photos/     ← User's selected photos (copies, originals untouched)
/tmp/dedup_report_*.json       ← Clustering report
(original photos are NEVER modified or deleted)
```

## Important Notes

- **Non-destructive** — Original photos are NEVER moved or deleted. Unique photos are copied to a subfolder.
- **Supported formats** — JPG, JPEG, PNG, HEIC, WEBP, TIFF, BMP
- **Performance** — Handles 500+ photos in under a minute on modern hardware
- **Selection criteria** — When duplicates are found, the largest file (highest quality) is picked as the representative
