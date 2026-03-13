---
name: rewrite-rustdoc
description: Rewrite Rust documentation comments to ensure all documentation and comments are in English, following rustdoc guidelines. Use when the user wants to clean up Rust documentation, translate Chinese comments to English, fix missing documentation, or ensure rustdoc compliance in a Rust codebase.
metadata:
  original-prompt: rewrite-rustdoc.prompt.md
---

# Rewrite Rustdoc

Ensure all Rust documentation and comments are exclusively written in English, following rustdoc guidelines.

## Steps

0. Determine which files to process:
   - If the user provides a method to find files, use that method.
   - Otherwise, assume files are in the `src/` directory.
   - Proceed immediately to the next steps after acquiring file information.

1. Conduct a comprehensive review to ensure all documentation and comments are in English.
   - Any Chinese text in documentation or code comments must be identified and corrected.
   - Chinese characters in test case strings are permissible and do not require modification.
   - Chinese report files should not be modified — focus on Rust source code files only.

2. Search for Chinese characters in the source code:
   ```bash
   rg -n "[\u4e00-\u9fff]" src/
   ```
   Check for missing documentation:
   ```bash
   cd src/ && cargo clippy -- -W missing_docs
   ```
   Replace `src/` with the user-specified location if provided.

3. Refer to `./docs/rustdoc-guidelines.md` for documentation structure and style standards.

4. Ensure all corrections adhere strictly to the documentation guidelines.

5. Repeat the search and revision process iteratively until no further occurrences require modification.
   - Do not prompt for confirmation before proceeding to the next item.
   - Complete all necessary changes before reporting back.
