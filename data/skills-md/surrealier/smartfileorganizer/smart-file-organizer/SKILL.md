---
name: smart-file-organizer
description: >
  Analyze file contents in a directory tree and intelligently rename files based on what they contain,
  optionally reorganizing them into a logical folder structure. Use this skill whenever the user wants to
  clean up messy file names, organize downloaded files, sort documents by content, rename files that have
  meaningless names (like IMG_20240101.jpg or document(3).pdf), or tidy up any folder where file names
  don't reflect their actual content. Also triggers when users mention bulk renaming, file cleanup,
  content-based organization, folder restructuring, collecting files by topic or purpose (e.g., "이력 관련
  자료 모아줘", "gather dataset files", "일회성 자료 판단해줘"), or filtering and grouping files by category.
---

# Smart File Organizer

Analyze file contents in a target directory (including all subdirectories), rename files to reflect their content, and optionally reorganize them into a logical folder structure.

## Modes

- **rename-only** (default): Rename files in place based on content analysis.
- **full-organize**: Rename files AND reorganize them into a categorized folder structure (create, rename, merge folders).
- **collect**: Scan files across directories and **copy** those matching a user-defined purpose into a single output folder. Does not rename or move originals.

## Procedure

### Step 1: Gather Parameters

Ask the user for:

1. **Target directory** — absolute path to scan (required).
2. **Mode** — `rename-only`, `full-organize`, or `collect` (default: `rename-only`).
   - If `collect`: also ask for the **collection query** — what kind of files to gather (e.g., "이력 관련 자료", "dataset files", "일회성 자료").
3. **Allowed languages** — which languages to keep in file names (default: match original or English).
   ```
   Which languages should be used in file names?
     Allowed: (e.g., Korean, English)
     Others:  auto-translate to an allowed language (e.g., 日本語 → Korean)
   ```
   - When file content is in a non-allowed language, translate the generated name into the user's preferred allowed language.
   - Acronyms and proper nouns are exempt from translation (`IITP`, `YOLOv8`, etc.).
4. **File filter** — specific extensions to include/exclude (default: all files).
5. **Max depth** — how deep to recurse into subdirectories (default: unlimited).
6. **Rename strictness** — how aggressively to rename files (default: `recovery`).
   ```
   How strictly should files be renamed?
     [R] Recovery  — only fix broken/meaningless names, keep already-descriptive names as-is
     [U] Uniform   — rename ALL files to a standardized format based on content
   ```
   - `recovery`: skip files whose current name already reasonably describes the content (even if format doesn't perfectly match the naming convention).
   - `uniform`: treat every original name as unreliable and regenerate from scratch — current behavior.

If the user provides a directory without specifying other options, use defaults and proceed.

### Step 2: Scan and Inventory

1. List all files recursively in the target directory.
2. **Skip hidden files/directories** (starting with `.`) and common ignore patterns (`node_modules`, `.git`, `__pycache__`, etc.).
3. **Skip source code files** by default — renaming breaks import paths, include directives, and build systems. Excluded extensions: `.py`, `.cpp`, `.c`, `.h`, `.hpp`, `.js`, `.ts`, `.jsx`, `.tsx`, `.java`, `.go`, `.rs`, `.rb`, `.cs`, `.swift`, `.kt`, `.scala`, `.sh`, `.bat`, `.ps1`, and CI/CD config files (`Jenkinsfile*`, `Makefile`, `Dockerfile`, `*.cmake`). The user can override this with an explicit `--include-code` flag or request.
4. **Skip executable/installer files** — keep `.exe`, `.msi`, `.appimage`, `.dmg` files with their original names.
5. **Detect suspected dataset directories** — identify directories that may contain bulk datasets before processing. A directory is suspected if ANY of the following is true:
   - Contains **100+ files with the same extension**.
   - Files follow sequential or hash-based naming patterns (e.g., `img_0001.jpg`…`img_9999.jpg`, `a3f8c2.png`).
   - Name matches common dataset patterns (case-insensitive): `train`, `val`, `valid`, `validation`, `test`, `dataset`, `datasets`, `images`, `labels`, `annotations`, `samples`, `corpus`, `raw`, `processed`.
   - Contains annotation/manifest files alongside bulk data (e.g., `*.json`/`*.csv` annotation + 50+ image/text files).

   For each suspected directory, **prompt the user** before deciding:
   ```
   ⚠ The following directories are suspected to be datasets:
     📁 train/       — 1,523 .jpg files, sequential naming pattern
     📁 annotations/ — 1,523 .json files + manifest.csv

   For each directory, choose:
     [S] Skip  — treat as dataset, do not rename
     [I] Include — treat as normal folder, process files
   ```
   - User-confirmed dataset directories are excluded entirely and logged as "dataset directory (user confirmed)".
   - User-confirmed non-dataset directories proceed to normal processing.
6. Create an inventory with: current path, file size, extension, last modified date.
7. **Scan directory names** — identify directories with broken or meaningless names (garbled encoding, `New Folder`, `새 폴더`, `Untitled`, numeric-only names like `1`, `2`, `3`). These are included in the rename map alongside files. Directory renames apply in all modes (including `rename-only`), and are executed **after** all file renames to avoid path invalidation.
   - **File/directory name encoding recovery** — names containing garbled bytes (mojibake) should be decoded by trying `EUC-KR`, `CP949`, `Shift_JIS`, `GB2312`, and `Latin-1` against the raw bytes. If a readable name is recovered, use it as the basis for renaming.
8. Report the inventory summary to the user:
   - Total file count
   - Breakdown by extension
   - Total size

If there are more than 100 files, ask the user to confirm before proceeding or suggest narrowing the scope with filters.

**Batch processing** — to avoid context overflow and tool-call failures:

- Maximum batch size: **50 files** per batch.
- When total files exceed 50, split the inventory into batches of up to 50.
- Process each batch as an independent sub-agent (or sequential batch if sub-agents are unavailable):
  1. Each batch receives its own file list and performs Steps 3–4 independently.
  2. Merge all batch results into a single unified rename map before presenting to the user.
- Sub-agent batches may run in parallel (up to 4 concurrent batches).
- **Sub-agent auto-approve** — sub-agents must execute all file reading and analysis operations without requiring user confirmation. Only the final consolidated dry-run map (Step 4) requires user approval. When invoking sub-agents, pass the `--auto-approve` or equivalent flag so that tool calls within each batch proceed automatically.
- Each batch must return its partial rename map as JSON for merging.
- **Batch merge deduplication** — after merging all batch results, scan for proposed name collisions:
  1. Group entries by proposed name (case-insensitive).
  2. For each collision, differentiate by appending a distinguishing attribute (date, parent folder name, or numeric suffix).
  3. Log resolved collisions in the dry-run output so the user can review.
- **Completion guardrail** — after all batches return, verify that every file in the inventory is accounted for (renamed, skipped-with-reason, or moved to `_unknown/`). If any files are missing from batch results, re-queue them in a supplementary batch. The final rename map MUST cover 100% of inventoried files.

### Step 3: Analyze File Contents

> **Behavior depends on the rename strictness setting from Step 1.**

#### When `uniform` mode:

> **⚠ CRITICAL: ALL non-code files MUST be renamed to a normalized format based on their actual content. No exceptions.**
>
> - The original file name is **unreliable** — treat it as if it were random characters.
> - You MUST read/analyze the file content first, then generate a name **from scratch**.
> - Files with partially descriptive but non-standard names (e.g., `073_disaster_safety_XR.hwpx`, `report_v2_final.docx`) MUST still be renamed after reading their content.
> - The ONLY reason to keep an original name is if it already perfectly matches the naming convention format AND accurately describes the specific content.

**Rename criteria (uniform)** — a file MUST be renamed if ANY of the following is true:

- Contains meaningless prefixes, serial numbers, or codes (`073_`, `IMG_`, `DSC_`, `001_`, `(3)`).
- Name is vague, abbreviated, or doesn't capture the document's specific subject.
- Doesn't follow the `[YYMMDD_]<attr1>_<attr2>[_...<attrN>].<ext>` format from `references/naming-conventions.md`.
- Contains non-allowed language characters (per Step 1 language settings).
- Contains generic words (`document`, `file`, `untitled`, `report`) without specific context.

#### When `recovery` mode (default):

> Only rename files with clearly broken or meaningless names. If the current name already conveys the file's content reasonably well, **keep it as-is** — even if it doesn't perfectly follow the naming convention format.

**Pre-filter (before content reading)** — to avoid reading hundreds of files unnecessarily, apply a fast name-quality heuristic FIRST:

1. Extract the file's stem (name without extension).
2. **Skip content reading** (mark as "keep") if the stem contains ≥ 2 meaningful words (not codes/numbers) and no disqualifying patterns.
3. **Require content reading** only if ANY of the following is true:
   - Stem is entirely non-alphabetic (hashes, UUIDs, numeric sequences).
   - Matches auto-generated patterns: `IMG_\d+`, `DSC\d+`, `Screen Shot`, `document\(\d+\)`, `Untitled`, `New File`.
   - Stem has fewer than 2 alphabetic tokens after stripping numbers and punctuation.
   - Contains non-allowed language characters (per Step 1).

This pre-filter dramatically reduces content reading for large directories where most files already have decent names.

**Rename criteria (recovery)** — a file is renamed ONLY if ANY of the following is true:

- Name is entirely meaningless (e.g., `IMG_20240315_142356.jpg`, `document(3).pdf`, `a3f8c2.png`).
- Name consists mostly of codes, hashes, or sequential numbers with no descriptive words.
- Name is a single generic word (`untitled`, `file`, `new`, `temp`).
- Contains non-allowed language characters (per Step 1 language settings).

Files with partially descriptive names (e.g., `quarterly_report.pdf`, `meeting_notes_march.txt`) are **kept as-is** in recovery mode.

For each file, read its content and determine a descriptive name:

#### Text-based files

Extensions: `.txt`, `.md`, `.json`, `.csv`, `.html`, `.xml`, `.log`, `.yaml`, `.yml`, `.ini`, `.cfg`, `.conf`, `.toml`, etc.

- Read the **first 10%** of the file (by line count or byte size). Minimum: 5 lines. Maximum cap: 200 lines or **4 KB**, whichever comes first.
- Identify the main topic, purpose, or subject matter from the actual text content.
- The proposed name must reflect what the text is about, not the file format.

#### Encoding detection

If file content appears garbled or unreadable:

1. Try common encodings in order: `utf-8` → `cp949` (Korean) → `shift_jis` (Japanese) → `gb2312` (Chinese) → `euc-kr` → `latin-1`.
2. Use `file` command or `chardet`-style heuristics to detect encoding if available.
3. Once readable text is obtained, proceed with content analysis.
4. If no encoding produces readable text, mark the file as **unreadable**.

#### Documents

Extensions: `.pdf`, `.docx`, `.xlsx`, `.pptx`, `.hwp`, `.hwpx`

- Extract text from the **first 10% of pages** (minimum: 1 page, maximum: **8 KB** of extracted text).
- Read the extracted text and identify the document's subject, title, or purpose.
- **`.hwpx`** files are ZIP archives containing XML — unzip and parse `Contents/section*.xml` to extract body text.
- **`.hwp`** files — use `hwp5txt` or `pyhwp` if available; otherwise try `strings` command with Korean encoding.
- If text extraction fails, use metadata (title, author, subject) as fallback.
- Only fall back to the existing name as a last resort, and flag it for user review with `⚠ content unreadable — name based on metadata/original`.

#### Images

Extensions: `.jpg`, `.png`, `.gif`, `.webp`, `.svg`, `.jfif`

- Check EXIF data or embedded metadata if available.
- If the agent has vision capability, **analyze the image content directly** and name based on what is depicted.
- Otherwise, attempt **contextual inference** in this order:
  1. **Sibling files** — check other files in the same directory for topic/project clues.
  2. **Timestamps** — compare creation/modification time with nearby files to find temporal clusters.
  3. **File name fragments** — extract any meaningful parts from the original name (dates, sequence numbers, app names).
  4. **Parent directory name** — use the folder name as a category hint.
- If none of the above yields a confident name, move to `_unknown/`.

#### Binary / unknown files

- Use file metadata and extension only.
- Do not attempt to read binary content.

#### Unreadable files

Files that cannot be analyzed (corrupted, encrypted, unsupported format, all encoding attempts failed):

- Move to `<target-dir>/_unknown/` preserving the original file name.
- Log the reason for failure (e.g., "encoding detection failed", "binary with no metadata").
- Include these in the dry-run preview so the user can override the decision.

#### Language handling

Apply the allowed languages setting from Step 1:

- Detect the language of the file content.
- If the content language is not in the allowed list, translate the proposed name into the user's preferred allowed language.
- Keep acronyms and proper nouns untranslated.

#### Naming rules

Refer to `references/naming-conventions.md` for detailed patterns. Key rules:

- Use `_` separator between attributes, `-` within multi-word attributes.
- Keep names concise: 3–6 attributes maximum.
- Preserve the original file extension.
- Include a date prefix (`YYMMDD_`) when the file has a clear associated date.
- Avoid generic names like `document`, `file`, `untitled`.
- **Always generate a fresh name from content analysis** — never copy the original file name. Even if the original name contains relevant words, rebuild the name from scratch following the naming convention format.

### Step 4: Generate Rename Map (Dry Run)

Build a rename map as JSON. **When total files exceed 30, use summary-first presentation:**

```
📊 Rename Summary
  Rename:  142 files
  Keep:    358 files (name already descriptive)
  Unknown:   5 files → _unknown/

  By extension: .pdf (42) · .hwpx (31) · .jpg (28) · .docx (22) · .txt (19)

  [Show full list]  [Show by folder]  [Show renames only]
```

When the user requests details (or total files ≤ 30), show the full rename map:

```
Current Name                    → Proposed Name
────────────────────────────────────────────────
IMG_20240315_142356.jpg         → 240315_sunset_beach-photo.jpg
document(3).pdf                 → 240901_quarterly_sales-report_Q3.pdf
073_disaster_safety_XR.hwpx     → 250530_IITP_disaster-safety_XR-augmentation_proposal.hwpx
notes.txt                       → meeting-notes_product-roadmap.txt

⚠ Unreadable (→ _unknown/):
corrupted-data.bin              → _unknown/corrupted-data.bin (reason: binary, no metadata)
```

**Iterative approval loop** — repeat until the user explicitly approves:

1. Present the full rename map.
2. The user may:
   - **Approve all** — proceed to Step 5.
   - **Request changes** — e.g., "use Korean names", "make names shorter", "keep the date prefix on photos only", "don't move file X to _unknown".
   - **Edit specific entries** — modify individual proposed names.
   - **Exclude files** — skip certain files.
   - **Cancel** — abort the operation.
3. If the user requests changes, revise the affected entries and present the updated map again.
4. Go back to step 1 of this loop.

Do NOT proceed to execution until the user gives explicit approval.

**Pre-execution rollback map** — immediately after the user approves, save the planned rollback map BEFORE any file operations:

```bash
bash <skill-path>/scripts/rename-map.sh save <target-dir>
```

This creates `<target-dir>/.file-organizer-map.json` so that even if execution is interrupted mid-way, the user can still rollback completed operations.

### Step 5: Execute Renames

After the rollback map is saved:

1. Rename files one by one.
2. **Progress reporting** — for large batches (50+ files), report progress every 25 files:
   ```
   ✅ 25/142 renamed... (17%)
   ✅ 50/142 renamed... (35%)
   ```
3. Report any errors (e.g., name conflicts, permission issues).
4. On name conflict, append a numeric suffix: `report_Q3_2.pdf`.
5. **Reconcile the rollback map** — after all renames complete, verify the map against actual filesystem state and remove entries for operations that did not execute:
   ```bash
   bash <skill-path>/scripts/rename-map.sh reconcile <target-dir>
   ```
   This ensures the rollback map only contains operations that actually happened.
6. **Execution completeness check** — compare the reconciled map + skip list against the original inventory. If any files were neither renamed nor explicitly skipped, report them as errors and retry.

### Step 6: Reorganize (full-organize mode only)

If the user chose `full-organize`, after renaming:

1. Analyze existing folder structure and file content categories.
2. Propose a new folder structure — this may include:
   - **Creating new folders** for categories that don't exist yet.
   - **Renaming existing folders** to more descriptive names (e.g., `misc/` → `reports/`, `New Folder/` → `presentations/`).
   - **Merging folders** that contain similar content.
   - **Removing empty folders** after files are moved out.

   Example proposal:
   ```
   📁 Folder changes:
     [NEW]    documents/reports/
     [NEW]    images/screenshots/
     [RENAME] misc/ → data/csv/
     [RENAME] New Folder/ → presentations/
     [DELETE] old-stuff/ (empty after move)

   📁 Proposed structure:
   <target-dir>/
   ├── documents/
   │   ├── reports/
   │   └── notes/
   ├── images/
   │   ├── photos/
   │   └── screenshots/
   ├── data/
   │   ├── csv/
   │   └── json/
   └── other/
   ```

3. Folder naming follows the same conventions as file naming (see `references/naming-conventions.md`), using descriptive names.
4. Present the proposed folder changes AND file moves to the user for approval.
5. After approval, execute folder operations first (create/rename), then move files, then clean up empty directories.
6. All folder rename/move operations are recorded in the rollback map for undo.

### Step 6b: Collect (collect mode only)

If the user chose `collect`, **skip Steps 3–6** and follow this procedure instead:

1. Use the **collection query** from Step 1 to define the search criteria.
2. For each file in the inventory, determine relevance by:
   - File name and path keywords.
   - Content sampling (first 4 KB for text, 8 KB for documents) — same caps as Step 3.
   - Metadata (extension, parent folder name, dates).
3. Score each file's relevance and build a **collect list** with confidence levels:
   ```
   📋 Collect: "이력 관련 자료" → _collected/이력_관련/
     ✅ High (12 files):
       documents/이력서_홍길동.pdf
       career/portfolio_2025.pptx
       ...
     🔶 Medium (5 files):
       misc/자기소개서_draft.docx
       ...
     ❌ Excluded (283 files): not relevant
   ```
4. Present the collect list and ask user to approve, adjust threshold, or exclude specific files.
5. After approval, **copy** (not move) matched files to `<target-dir>/_collected/<query-slug>/`.
6. Preserve original directory structure as flat copies (prepend parent folder name on conflict).
7. Log the collection in `.file-organizer-changelog.md`.

### Step 7: Summary Report

Output a summary:

- Files renamed: count
- Files moved: count (if full-organize)
- Files collected: count and destination (if collect)
- Files skipped: count and reasons
- Rollback command: `bash <skill-path>/scripts/rename-map.sh rollback <target-dir>`

**Save change log** — write a Markdown file at `<target-dir>/.file-organizer-changelog.md` with:

```markdown
# File Organizer Change Log

- **Date**: YYYY-MM-DD HH:MM
- **Mode**: rename-only | full-organize | collect
- **Target**: <target-dir>

## Changes (N files)

| # | Before | After |
|---|--------|-------|
| 1 | `old-name.pdf` | `new-name.pdf` |
| ... | ... | ... |

## Skipped (M files)

| # | File | Reason |
|---|------|--------|
| 1 | `some-file.py` | Source code (excluded) |
| 2 | `train/` (1523 files) | Dataset directory (user confirmed) |
| ... | ... | ... |

## Moved to _unknown/ (K files)

| # | File | Reason |
|---|------|--------|
| 1 | `hash-image.webp` | Unreadable content |
| ... | ... | ... |
```

This file is overwritten on each run (previous logs are not preserved).

## Rollback

The rollback map (`.file-organizer-map.json`) records every rename/move operation for undo purposes. The user can manage it with these commands:

```bash
# Save current rename map (done automatically before execution)
bash <skill-path>/scripts/rename-map.sh save <target-dir>

# Show the current rollback map contents
bash <skill-path>/scripts/rename-map.sh show <target-dir>

# Undo all renames/moves recorded in the map
bash <skill-path>/scripts/rename-map.sh rollback <target-dir>

# Reconcile map after execution (remove entries for operations that didn't happen)
bash <skill-path>/scripts/rename-map.sh reconcile <target-dir>

# Clear the rollback map (after confirming changes are correct)
bash <skill-path>/scripts/rename-map.sh clear <target-dir>
```

The user can also ask the agent directly: "rollback the last file organization", "show me what was renamed", or "clear the rollback history".

## Safety Rules

- NEVER overwrite existing files — always check for conflicts first.
- NEVER execute `rm -rf` or any recursive delete command without explicit user approval — even inside sub-agents. Deletions of empty directories (`rmdir`) are allowed only after confirming the directory is empty.
- ALWAYS save the rollback map before making any changes.
- ALWAYS show the dry-run preview and get explicit user approval before executing.
- Skip files that are currently open or locked.
- Preserve file permissions and timestamps when renaming/moving.
