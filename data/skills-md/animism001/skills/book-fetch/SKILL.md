---
name: book-fetch
description: Download ebooks (epub/pdf) from Anna's Archive and upload them to MEGA automatically. Use when the user asks to download a book, find an ebook, search for a title on Anna's Archive/libgen, or add a book to their MEGA library.
---

# book-fetch

Search Anna's Archive, download epub/pdf, upload to `mega:/Books/`.

## Setup (one-time)

Anna's Archive is DNS-blocked on the VPS. The `/etc/hosts` override is already in place:
```
186.2.165.77 annas-archive.li
```
MEGA is configured via rclone (`rclone ls mega:/` to verify).

## Usage

```bash
cd ~/clawd
.venv-books/bin/python3 skills/book-fetch/scripts/book_fetch.py "TITLE AUTHOR"
```

Options:
- `--format pdf` — prefer PDF over epub
- `--dry-run` — search only, no download
- `--pick -1` — interactive result picker
- `--pick N` — pick result index N (default: 0)

## Download Pipeline

1. Search `annas-archive.li` → parse `data-content` attributes for title/author/md5
2. Fetch `annas-archive.li/md5/<md5>` → find `libgen.li/ads.php` link
3. Fetch `libgen.li/ads.php` → extract `get.php?md5=...&key=...` direct link
4. Download file with progress bar
5. Upload via `rclone copy ... mega:/Books/`

**Fallback:** If no libgen.li mirror exists (newer books), tries Anna's Archive fast/slow download links.

## Notes

- New books (2023+) may lack libgen mirrors; fast_download requires AA membership; slow_download is rate-limited
- venv: `~/clawd/.venv-books/` (requests, beautifulsoup4, lxml)
- Files cached at `/tmp/books/` after download
- GitHub: <https://github.com/zerone0x/book-fetch>
