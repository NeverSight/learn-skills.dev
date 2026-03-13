---
name: figshare-data-download
description: "Download Figshare files via browser-only workflow (no web_fetch/curl probing). Use when a user provides a Figshare DOI or ndownloader URL and needs a reliable fetch path that always opens the page in browser, triggers the real download, then copies the downloaded file into a target path."
---

# Figshare Data Download

Use this skill to fetch Figshare dataset files behind anti-bot checks.

## Workflow

1. Normalize inputs:
- `item_or_file_url`: DOI URL, item page URL, or `ndownloader` URL
- `output_path`: final local path
- `expected_name`: expected browser filename (optional)

2. Resolve the file download link in browser:
- Open the DOI/item page with browser tooling.
- Find and click the dataset "Download" / "Download file" element.
- If already given an `ndownloader` URL, open it directly in browser.

3. Complete any browser challenge/verification and trigger the real file download.

4. Copy the downloaded file from `~/Downloads` to `output_path`.

5. Verify output:
- Ensure file size is non-zero.
- Ensure extension/type matches expectation (`.xlsx`, `.csv`, etc.).

## Decision Rules

- Do **not** use `web_fetch` for this skill.
- Do **not** run curl probing as part of this skill workflow.
- Always use browser path first and keep it end-to-end.

## Output Contract

- Always produce one final file at `output_path`.
- Keep the downloaded source file in `~/Downloads` unchanged.
- Report:
  - final path
  - file size
  - that the transfer used browser-only workflow

## Script

- `scripts/figshare_data_download.py` (browser-only helper)
  - supports semi-automatic flow: `--open-browser` + wait/poll in `~/Downloads` + copy/verify
  - does not perform curl/web_fetch probing
