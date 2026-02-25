---
name: save-artifact
description: Save and organize target artifacts (documents, presentations, markdown, images, SVGs) to ~/projects/artifacts-viewer. Use when user wants to save or organize docs, PDFs, PPTs, markdown files, images (PNG, JPG, SVG), or any visual/document artifacts to a central viewer location. Also use to initialize git repo for artifacts-viewer and push to GitHub.
---

# save-artifact

Save target artifacts to ~/projects/artifacts-viewer for easy viewing and organization.

## Quick Usage

1. **Ensure target directory exists**: `~/projects/artifacts-viewer` (auto-created if missing)
2. **Save artifact**: Copy or move the file to artifacts-viewer with appropriate naming
3. **Git operations**: Initialize git repo and push to GitHub when needed

## Supported File Types

- Documents: `.pdf`, `.doc`, `.docx`
- Presentations: `.ppt`, `.pptx`
- Markdown: `.md`, `.mdx`
- Images: `.png`, `.jpg`, `.jpeg`, `.gif`, `.svg`
- Other: `.txt`, `.json`

## Workflow

### Save Artifact

```bash
# Ensure directory exists
mkdir -p ~/projects/artifacts-viewer/artifacts/<category-subdir>

# Copy artifact to viewer subdirectory (use descriptive name)
cp <source-file> ~/projects/artifacts-viewer/artifacts/<category-subdir>/<descriptive-name>

# REQUIRED: Regenerate manifest so web viewer picks up new files immediately
python3 ~/projects/artifacts-viewer/artifacts/scan_manifest.py
```

### Git Operations

```bash
cd ~/projects/artifacts-viewer
git init
git add .
git commit -m "Add artifacts"
git remote add origin https://github.com/<username>/artifacts-viewer.git
git push -u origin main
```

## Script Usage

Use `scripts/save_artifact.py` for automated saving:

```bash
python3 scripts/save_artifact.py <source_path> [--name <custom_name>] [--category <category>]
```

Categories: docs, slides, markdown, images, diagrams, other

## Notes

- Always use descriptive, unique names for artifacts
- Consider organizing by category subdirectories if needed
- Commit and push to GitHub for version control and sharing
