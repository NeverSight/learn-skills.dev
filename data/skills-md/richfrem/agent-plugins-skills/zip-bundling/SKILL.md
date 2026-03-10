---
name: zip-bundling
description: Create technical ZIP bundles of code, design, and documentation for external review or context sharing. Use when you need to package multiple project files into a portable `.zip` archive instead of a single Markdown file.
allowed-tools: Bash, Read, Write
---
# ZIP Context Bundling Skill 📦

## Overview
This skill centralizes the knowledge and workflows for creating compressed ZIP "Context Bundles." These bundles are essential for compiling large amounts of code and design files into their native formats, compressed into a single portable `.zip` file for human review or agent ingestion.

## 🎯 Primary Directive
**Curate, Consolidate, and Archive.** You do not just run the zip command; you architect context. You ensure that any bundle you create is:
1. **Complete:** Contains all required dependencies, documentation, and source code files.
2. **Documented:** The archiver automatically injects a `_manifest_notes.md` file inside the ZIP. You must populate the manifest's JSON "note" fields with rich explanations so this metadata is passed onto the reviewers.

## Core Workflow: Generating a ZIP Bundle

The ZIP context bundler operates through the exact same JSON manifest pattern as the Markdown bundler. 

### 1. Analyze the Intent
Before bundling, determine what the user is trying to accomplish:
- **Code Review**: Include implementation files and overarching logic.
- **Red Team / Security**: Include architecture diagrams and security protocols.
- **Handoffs**: Include `README`, `.env.example`, and structural scaffolding.

### 2. Formulate the Manifest Schema
You must generate a `file-manifest.json` containing the exact files to be bundled.
```json
{
  "title": "Bundle Title",
  "description": "Short explanation of the bundle's goal.",
  "files": [
    {
      "path": "docs/architecture.md",
      "note": "Primary design document. Look closely at the Auth flow chart."
    },
    {
      "path": "src/main.py",
      "note": "Core implementation logic"
    }
  ]
}
```

### 3. Generate the ZIP Archive
Once the `file-manifest.json` is safely written to disk, invoke the native bundler script explicitly requesting a `.zip` output destination:

```bash
python3 "./scripts/bundle_zip.py" --manifest "file-manifest.json" --bundle "output_bundle.zip"
```

The script will automatically parse your JSON notes and generate a `_manifest_notes.md` root document explaining the archive contents to whoever unzips it.

## Conditional Step Inclusion & Error Handling
If a file requested in the manifest does not exist or raises a permissions error:
1. Do **not** abort the entire archive generation.
2. Ensure the bundler script injects an explicit failure warning into the `_manifest_notes.md` root document:
   ```markdown
   > 🔴 **NOT INCLUDED**: `missing/file.py` could not be read.
   ```
3. Proceed archiving the remaining valid files.

## Best Practices & Anti-Patterns
1. **Always Provide Notes:** The `note` field in the manifest JSON is crucial for ZIP files because it becomes the only context passing through to the recipient's `_manifest_notes.md` index.
2. **Directory Handling:** If you pass a directory path like `"path": "src/"` in the manifest schema, the Python script will recursively expand it and include all valid, readable contents.

### Common Bundling Mistakes
- **Binary/Media Bloat**: Including image assets without explicitly verifying if the downstream recipient can parse them.
- **Silent Exclusion**: Filtering out an unreadable file without explicitly declaring it missing in the manifest notes.
