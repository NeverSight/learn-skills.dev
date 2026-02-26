---
name: letterly-exporter
description: Automates the process of exporting data from Letterly and saving it to your Obsidian vault.
---

# letterly-exporter

This skill automates the process of exporting data from [Letterly](https://web.letterly.app) and saving it to your Obsidian vault.

## Prerequisites

1. **Python 3.8+**
2. **Playwright**: A browser automation library.

## Installation

```bash
pip install -r requirements.txt
playwright install chromium
```

## Usage

Run the script:

```bash
python3 export_letterly.py
```

## How it Works

1. **Browser:** The script uses **Playwright's bundled Chromium**. This is a standalone browser binary (about ~100MB) that won't touch your existing browsers (Arc, Brave, Zen).
2. **Persistent Session:** Your login session is stored in the `chrome_context/` folder, so you only log in once.
3. **Automation:**
    * Navigates to `https://web.letterly.app`.
    * Clicks "Settings".
    * Clicks "Export Data".
    * Downloads the CSV file.
    * Moves the file to `My Outputs/Transcriptions/` in your vault.
