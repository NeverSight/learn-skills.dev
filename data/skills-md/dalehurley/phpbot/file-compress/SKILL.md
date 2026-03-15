---
name: file-compress
description: "Create and extract ZIP and tar.gz archives. Use this skill when the user asks to zip files, unzip an archive, compress a folder, extract a tar.gz, create an archive, or list archive contents."
tags: [zip, tar, compress, extract, archive, utility]
version: 0.1.0
---

# Skill: file-compress

## When to Use

Use this skill when the user asks to:

- Zip or compress files/folders
- Unzip or extract an archive
- Create a ZIP or tar.gz archive
- List contents of an archive
- Compress files for sharing or backup

## Supported Formats

| Format      | Extensions        | Notes                                |
| ----------- | ----------------- | ------------------------------------ |
| ZIP         | `.zip`            | Most common, cross-platform          |
| Gzipped Tar | `.tar.gz`, `.tgz` | Unix standard, preserves permissions |

## Input Parameters

| Parameter      | Required    | Description                                | Example        |
| -------------- | ----------- | ------------------------------------------ | -------------- |
| `action`       | Yes         | `create`, `extract`, or `list`             | create         |
| `archive_path` | Yes         | Path to the archive file                   | ./backup.zip   |
| `files`        | For create  | Files/directories to include               | file1.txt dir/ |
| `target_dir`   | For extract | Directory to extract to (default: current) | ./output/      |
| `format`       | For create  | `zip` (default) or `tar.gz`                | zip            |

## Procedure

1. Determine the action from the user's request
2. Run the bundled script:

   ```bash
   # Create a ZIP archive
   python3 skills/file-compress/scripts/archive.py create backup.zip file1.txt file2.txt mydir/

   # Create a tar.gz archive
   python3 skills/file-compress/scripts/archive.py create backup.tar.gz --format tar.gz file1.txt mydir/

   # Extract an archive
   python3 skills/file-compress/scripts/archive.py extract backup.zip --target ./output/

   # List archive contents
   python3 skills/file-compress/scripts/archive.py list backup.zip
   ```

3. Report the result to the user

## Bundled Scripts

| Script               | Type   | Description                                   |
| -------------------- | ------ | --------------------------------------------- |
| `scripts/archive.py` | Python | Create, extract, and list ZIP/tar.gz archives |

### Script Usage

```bash
# Create ZIP from files and directories
python3 scripts/archive.py create output.zip file1.txt file2.txt mydir/

# Create tar.gz
python3 scripts/archive.py create output.tar.gz --format tar.gz src/ README.md

# Extract to current directory
python3 scripts/archive.py extract archive.zip

# Extract to specific directory
python3 scripts/archive.py extract archive.tar.gz --target /tmp/extracted/

# List contents
python3 scripts/archive.py list archive.zip
```

## Example

```
zip up the src/ folder
create a tar.gz of these files
extract backup.zip to my desktop
what's inside archive.tar.gz
compress the project folder into a zip
unzip downloaded-file.zip
```
