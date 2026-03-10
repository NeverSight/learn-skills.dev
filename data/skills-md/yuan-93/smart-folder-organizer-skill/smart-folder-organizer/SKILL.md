---
name: smart-folder-organizer
description: Automatically organizes cluttered folders by categorizing files, identifying duplicates, and renaming PDF documents like invoices and receipts based on their content. Use when a directory is disorganized or contains a mix of documents, installers, and media.
---

# Smart Folder Organizer

This skill provides a structured workflow for tidying up disorganized directories while ensuring data safety.

## Core Mandates

1. **Safety First**: NEVER delete any file. Move files intended for deletion to specific subfolders within `to_remove/` (e.g., `to_remove/duplicates/` or `to_remove/empty_folders/`).
2. **Strict Scoping**: Operate ONLY within the current directory and its subdirectories. Never move or access files in the parent directory (`..`).
3. **Preservation**: If a file's category is ambiguous, move it to a `Needs_Review/` folder rather than guessing incorrectly.
4. **Large Files**: For any file larger than 20MB, skip deep content analysis (such as reading PDF text) to prevent memory issues. Move these unanalyzed large files to a dedicated `Needs_Review/LargeFiles/` directory.
5. **Folder Handling**: Recursively process all files within the current directory and its subdirectories. When moving files, place them in the categorized folders at the root level of the target directory (do not replicate the category structure inside every subfolder). Any empty subdirectories discovered or left behind must be moved to `to_remove/empty_folders/`.

## Workflow

### 1. Smart Folder Detection

Before processing individual files, run `scripts/detect_smart_folders.py <target_dir>` to identify subdirectories that are already well-organized (e.g., git repositories, software projects, macOS app bundles).

- **Action**: Move each detected folder to `Others/` as a whole — do NOT descend into or reorganize its contents.
- **Logic**: The script checks for project markers (`.git/`, `package.json`, `Cargo.toml`, `Makefile`, etc.) and app bundles (`.app`), returning a JSON list of matches with reasons.
- **Skip**: All subsequent steps should ignore the `Others/` directory.

### 2. Duplicate Detection

Run the `find_duplicates.py` script to identify identical files.

- **Action**: Move identified duplicates to `to_remove/duplicates/`.
- **Logic**: Use file hashes (SHA256) via the `scripts/find_duplicates.py` script for deterministic results.

### 3. General Categorization

Organize files by extension and common patterns:

- **Photos**: Move to `Photos/`. (Screenshots to `Photos/Screenshots/`)
- **Videos**: Move to `Videos/`.
- **Installers**: Move to `Installers/` (`.dmg`, `.pkg`, `.exe`, `.msi`).
- **Archives**: Move to `Archives/` (`.zip`, `.rar`, etc.).

### 4. Deep PDF Analysis

For PDF files, read the first few pages to determine the document type and extract metadata for renaming.

- **CRITICAL**: Do NOT generate dynamic Python scripts to read PDFs. Instead, execute the `scripts/extract_pdf_metadata.py` script provided in this skill to extract text and analyze the document deterministically. The script uses `pypdf` with a sampling strategy (first 3 pages + last page) for fast and efficient classification.
- **IMPORTANT**: Use **Universal Semantic Reasoning** for document classification. Modern AI models can understand dozens of languages (English, Chinese, Spanish, etc.); prioritize the _intent_ of the document (e.g., "requesting payment") over specific English keywords like "Invoice". Refer to `references/classification.md` for semantic guidelines.
- **Multilingual Naming**: For non-English documents, extract naming details (like [Vendor] or [Provider]) in their original script (e.g., Chinese characters). The standard date format `yyyy-mm-dd` remains unchanged.
- **Invoices**: Rename to `yyyy-mm-dd-[Vendor]-[Inv#-][Amount].pdf` and move to `Documents/Invoices/`.
- **Bills**: Rename to `yyyy-mm-dd-[Provider]-[Service]-[Account#].pdf` and move to `Documents/Bills/`.
- **Receipts**: Rename to `yyyy-mm-dd-[Store]-[TotalAmount].pdf` and move to `Documents/Receipts/`.
- **Travel**: Rename to `yyyy-mm-dd-[Transport/Hotel]-[Confirmation#].pdf` and move to `Documents/Travel/`.

### 5. Final Cleanup

- Group writing documents (`.docx`, `.doc`, `.pages`, `.odt`) into `Documents/Writing/`.
- Group spreadsheet files (`.xlsx`, `.xls`, `.numbers`, `.ods`, `.csv`) into `Documents/Spreadsheets/`.
- Group presentation files (`.ppt`, `.pptx`, `.key`, `.odp`) into `Documents/Presentations/`.
- Group audio files (`.mp3`, `.wav`, `.flac`, `.m4a`) into `Audio/`.
- Group remaining documents into `Needs_Review/Documents/` by sub-type if applicable.
- If a PDF document was analyzed but the category is unknown, move it to `Needs_Review/Unknown/`.
- Move any other unhandled files to `Needs_Review/`.

## Resources

### scripts/find_duplicates.py

A Python script that deterministically finds identical files. It uses SHA-256 hashing to compare file contents rather than relying on filenames or sizes, returning a JSON list of duplicates.

### scripts/extract_pdf_metadata.py

A Python helper script that extracts text from a PDF using the `pypdf` library. Use this instead of rolling your own script. It uses a sampling strategy (first 3 pages and the last page) to provide efficient text extraction for document classification, returning the text in a JSON wrapper.

### scripts/detect_smart_folders.py

A Python script that scans immediate subdirectories of a target folder for project markers (`.git/`, `package.json`, `Cargo.toml`, `Makefile`, etc.) and app bundles (`.app`). Returns a JSON list of detected "smart" folders that should be moved to `Others/` without being broken apart.

### references/classification.md

Contains detailed keyword lists and naming conventions for PDFs and other document types.
