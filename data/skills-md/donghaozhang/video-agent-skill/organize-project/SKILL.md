---
name: organize-project
description: Organize files and folders into QCut's standard project structure. Use when setting up a new project, cleaning up files, or when the user asks to organize their workspace.
---

# QCut Project Organization Skill

Organize files and folders according to QCut's standard project structure.

## Standard QCut Project Structure

```
Documents/QCut/Projects/{project-name}/
├── project.qcut              # Project metadata file
├── media/                    # All media files
│   ├── imported/             # User-imported media (videos, images, audio)
│   ├── generated/            # AI-generated content (from skills)
│   └── temp/                 # Temporary processing files
├── skills/                   # Project-specific skills
│   ├── ai-content-pipeline/  # AI content generation skill
│   │   ├── Skill.md
│   │   ├── REFERENCE.md
│   │   └── EXAMPLES.md
│   └── ffmpeg-skill/         # FFmpeg processing skill
│       ├── Skill.md
│       └── REFERENCE.md
├── output/                   # Exported videos and renders
├── cache/                    # FFmpeg and processing cache
└── docs/                     # Project documentation (optional)
```

## Organization Rules

### Media Files
- **Videos** (.mp4, .mov, .webm, .avi): → `media/imported/` or `media/generated/`
- **Images** (.jpg, .png, .webp, .gif): → `media/imported/` or `media/generated/`
- **Audio** (.mp3, .wav, .aac, .m4a): → `media/imported/` or `media/generated/`
- AI-generated content goes to `media/generated/`
- User-imported content goes to `media/imported/`

### Hybrid Symlink Import System
QCut uses a **hybrid symlink/copy system** for imported media:
- **Symlinks preferred**: Creates symbolic links to original files (saves disk space)
- **Copy fallback**: Falls back to copying when symlinks unavailable (Windows without admin, network drives)
- **Metadata tracking**: Each import tracks `importMethod`, `originalPath`, and `fileSize`

Files in `media/imported/` may be:
- **Symlinks** pointing to the original file location
- **Copies** of the original file (when symlink creation fails)

### Skills
- Each skill is a folder with `Skill.md` as the entry point
- Additional reference files: `REFERENCE.md`, `EXAMPLES.md`, `CONCEPTS.md`
- Skills can have a `scripts/` subfolder for helper scripts

### Output
- Final rendered videos go to `output/`
- Use descriptive names: `{project-name}_{date}_{resolution}.mp4`

### Temporary Files
- Processing intermediates go to `media/temp/`
- Cache files go to `cache/`
- Clean up temp files after export

## Virtual Folder System

QCut uses a **virtual folder system** for organizing media in the UI:
- Virtual folders are metadata-only (files stay in original locations)
- Items can belong to multiple folders (like tags)
- Special "Skills" folder shows project skills
- Max folder depth: 3 levels

### Virtual Folder Naming Conventions
- Use clear, descriptive names (max 50 characters)
- Examples: "Raw Footage", "B-Roll", "Music", "Sound Effects"
- Color-code folders for quick identification

## When Organizing

1. **Identify file types** - Categorize by extension and source
2. **Check existing structure** - Don't duplicate folders
3. **Move files safely** - Use copy then delete, not direct move
4. **Update references** - Ensure project files still point to correct paths
5. **Clean up empty folders** - Remove unused directories

## Commands to Help

```bash
# List all media files recursively
find . -type f \( -name "*.mp4" -o -name "*.mov" -o -name "*.jpg" -o -name "*.png" -o -name "*.mp3" \)

# Create standard structure
mkdir -p media/{imported,generated,temp} output cache skills docs

# Move videos to imported
mv *.mp4 *.mov *.webm media/imported/ 2>/dev/null

# Find large files (over 100MB)
find . -type f -size +100M

# Clean temp files
rm -rf media/temp/* cache/*

# === Symlink Commands ===

# List all symlinks in imported folder
find media/imported -type l

# Check if a file is a symlink
ls -la media/imported/

# Find broken symlinks
find media/imported -xtype l

# Show symlink target
readlink media/imported/video-id.mp4

# Create symlink manually (Unix/macOS)
ln -s /path/to/original.mp4 media/imported/video-id.mp4

# Create symlink manually (Windows - requires admin or dev mode)
mklink media\imported\video-id.mp4 C:\path\to\original.mp4
```

## Example Organization Task

When asked to organize:

1. First, scan the current directory structure
2. Identify files that need to be moved
3. Create missing directories
4. Move files to appropriate locations
5. Report what was organized

**Always confirm before moving files that might break project references.**
