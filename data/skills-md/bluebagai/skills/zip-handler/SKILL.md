---
name: zip-handler
description: Guide for working with zip files. Use when you need to create/compress a zip file from files or folders, extract/unpack/decompress a zip file, zip, compress, or archive files, make changes to files within a zip archive. Trigger words include; zip, unzip, compress, archive, extract, pack, unpack
---

## Overview

These are the steps for working with zip files using Python scripts. Do not stray from these instructions.

a. If the user wants a zip file:

1. Use the "pack" bash script (you can find it below) to zip up the files or folder.
2. Mint a download link for the zipped file.
3. Return the download link to the user

b. If someone wants to change something inside a zip file:

1. Use the "unpack" bash script (see below!) to unzip the file.
2. Open the files and make the changes you need via the text editor or bash tools
3. When you’re done, use the "pack" bash script again to zip everything back up.
4. Make a new download link to the zipped file.
5. Send the new link to the person.

- That’s it! Follow the steps one by one.

## Unpacking/Extracting Zip Files

### Basic Usage

```bash
python scripts/unpack.py <path_to_zip_file>
```

This will extract the zip file contents to a directory named after the zip file (without the .zip extension).

### Examples

```bash
# Extract archive.zip to ./archive/
python scripts/unpack.py archive.zip

# Extract to a specific output directory
python scripts/unpack.py archive.zip -o my_output_folder

# Extract with absolute path
python scripts/unpack.py /path/to/files/data.zip

# View help and all options
python scripts/unpack.py --help
```

### Options

- `zip_path` (required): Path to the zip file to extract
- `-o`, `--output`: Custom output directory (default: zip filename without extension)

## Packing/Creating Zip Files

### Basic Usage

```bash
python scripts/pack.py <path_to_folder_or_file>
```

This will create a compressed zip file named after the source (with .zip extension).

### Examples

```bash
# Zip a folder (creates my_folder.zip)
python scripts/pack.py my_folder

# Zip a single file (creates document.txt.zip)
python scripts/pack.py document.txt

# Create zip with custom name
python scripts/pack.py my_folder -o archive.zip

# Custom name without .zip extension (will be added automatically)
python scripts/pack.py my_folder -o archive

# Zip with absolute path
python scripts/pack.py /path/to/my_folder -o backup.zip

# View help and all options
python scripts/pack.py --help
```

### Options

- `source_path` (required): Path to the folder or file to zip
- `-o`, `--output`: Custom output zip file name (default: source name + .zip)
