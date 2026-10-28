---
name: wx-favorites-report
description: End-to-end pipeline to extract, decrypt, and visualize WeChat Mac favorites from encrypted SQLite DB into an interactive HTML report.
triggers:
  - 微信收藏可视化
  - visualize wechat favorites
  - extract wechat favorites
  - generate wechat favorites report
  - decrypt wechat database
  - wechat favorites html report
  - parse wechat favorites db
  - wechat favorites visualization
---

# wx-favorites-report

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

End-to-end pipeline that hooks into the WeChat Mac client via Frida, extracts PBKDF2-derived encryption keys, decrypts the `favorite.db` SQLCipher database, parses XML-encoded favorites, and renders a single-file interactive HTML report with charts, word cloud, and filterable card browser.

---

## Prerequisites

- macOS (Apple Silicon or Intel)
- WeChat Mac 4.x installed and logged in
- Python 3.9+
- Frida 17.x

```bash
pip3 install frida frida-tools pycryptodome
```

---

## Project Layout

```
~/.claude/skills/wechat-favorites-viz/
├── SKILL.md
└── scripts/
    ├── parse_favorites.py      # SQLite/CSV/JSON → unified JSON
    ├── generate_report.py      # JSON → single-file HTML
    └── demo_data.py            # synthetic data for testing
```

---

## Full Pipeline (Step-by-Step)

### Step 1 — Strip Hardened Runtime from WeChat

The App Store build blocks Frida injection. Copy and re-sign without entitlements:

```bash
killall WeChat 2>/dev/null; sleep 2
cp -R /Applications/WeChat.app ~/Desktop/WeChat.app
codesign --force --deep --sign - ~/Desktop/WeChat.app
```

> **Never run with `sudo`** — doing so changes the data directory to `/var/root/…` and breaks DB path resolution.

### Step 2 — Hook PBKDF2 with Frida

Save as `hook_wechat.js`:

```javascript
// hook_wechat.js — capture all CCKeyDerivationPBKDF calls
var CCKeyDerivationPBKDF = Module.findExportByName(
  "libcommonCrypto.dylib",
  "CCKeyDerivationPBKDF"
);

Interceptor.attach(CCKeyDerivationPBKDF, {
  onEnter: function (args) {
    // args[3] = password ptr, args[4] = password len
    // args[5] = salt ptr,     args[6] = salt len
    // args[9] = iterations
    // args[10]= derived key ptr, args[11]= derived key len
    this.saltPtr = args[5];
    this.saltLen = args[6].toInt32();
    this.dkPtr   = args[10];
    this.dkLen   = args[11].toInt32();
  },
  onLeave: function (_retval) {
    try {
      var salt = Memory.readByteArray(this.saltPtr, this.saltLen);
      var dk   = Memory.readByteArray(this.dkPtr,   this.dkLen);
      var entry = {
        salt: Array.from(new Uint8Array(salt))
              .map(b => b.toString(16).padStart(2, "0")).join(""),
        key:  Array.from(new Uint8Array(dk))
              .map(b => b.toString(16).padStart(2, "0")).join(""),
        ts:   Date.now()
      };
      var line = JSON.stringify(entry) + "\n";
      // Write to log via send()
      send(line);
    } catch (e) {}
  }
});
```

Run the hook:

```bash
frida ~/Desktop/WeChat.app/Contents/MacOS/WeChat \
  -l hook_wechat.js \
  --runtime=v8 \
  2>/dev/null | tee /tmp/wechat_frida_keys.log &

# WeChat will launch — log in, then open the 收藏 (Favorites) tab.
# Wait ~60 seconds for all DB keys to be derived, then Ctrl+C.
```

> **Key insight:** `favorite.db` is only opened when the user navigates to the Favorites tab. If you hook before opening Favorites, the key won't appear.

### Step 3 — Match Key to `favorite.db`

```python
# match_key.py
import json, sqlite3, pathlib

LOG = pathlib.Path("/tmp/wechat_frida_keys.log")
DB  = pathlib.Path.home() / (
    "Library/Containers/com.tencent.xinWeChat/Data/Documents/"
    "xwechat_files"
)

def find_db(wxid=None):
    """Locate favorite.db under the first (or named) wxid folder."""
    root = DB
    candidates = sorted(root.glob("*/db_storage/favorite/favorite.db"))
    if not candidates:
        raise FileNotFoundError("favorite.db not found")
    if wxid:
        return next(p for p in candidates if wxid in str(p))
    return candidates[0]

def read_salt(db_path: pathlib.Path) -> bytes:
    """First 16 bytes after the 16-byte SQLCipher header = salt."""
    with open(db_path, "rb") as f:
        f.read(16)               # skip "SQLite format 3\x00"
        return f.read(16)        # salt

def match(db_path: pathlib.Path) -> str | None:
    salt_hex = read_salt(db_path).hex()
    for line in LOG.read_text().splitlines():
        try:
            entry = json.loads(line)
            if entry["salt"] == salt_hex:
                return entry["key"]
        except Exception:
            continue
    return None

if __name__ == "__main__":
    db = find_db()
    key = match(db)
    if key:
        print(f"enc_key (hex): {key}")
        print(f"db path      : {db}")
    else:
        print("Key not found — did you open the Favorites tab while Frida was running?")
```

### Step 4 — Decrypt the Database

```python
# decrypt_db.py
"""
SQLCipher 4 parameters:
  cipher       : AES-256-CBC
  hmac         : HMAC-SHA512
  kdf_iter     : 256000
  page_size    : 4096
  reserve      : 80  (64 HMAC + 16 IV)
"""
import hashlib, hmac, struct, pathlib
from Crypto.Cipher import AES

PAGE_SIZE = 4096
RESERVE   = 80
IV_SIZE   = 16
HMAC_SIZE = 64
KDF_ITER  = 256000

def decrypt_db(enc_path: pathlib.Path, key_hex: str, out_path: pathlib.Path):
    raw_key = bytes.fromhex(key_hex)
    data    = enc_path.read_bytes()

    # SQLCipher stores salt in first 16 bytes of file
    salt = data[:16]

    # Derive page key and HMAC key
    page_key  = hashlib.pbkdf2_hmac("sha512", raw_key, salt, KDF_ITER, dklen=32)
    hmac_key  = hashlib.pbkdf2_hmac("sha512", page_key, salt, 1, dklen=32)

    out_pages = bytearray()

    # Page 1: skip 16-byte salt header
    pages = [data[16:PAGE_SIZE]] + [
        data[i:i+PAGE_SIZE] for i in range(PAGE_SIZE, len(data), PAGE_SIZE)
    ]

    for page_num, page in enumerate(pages, start=1):
        content  = page[:PAGE_SIZE - RESERVE]
        reserved = page[PAGE_SIZE - RESERVE:]
        iv       = reserved[HMAC_SIZE:HMAC_SIZE + IV_SIZE]

        cipher    = AES.new(page_key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(content)

        if page_num == 1:
            # Restore SQLite header
            out_pages += b"SQLite format 3\x00" + plaintext[16:]
        else:
            out_pages += plaintext

        # Zero-pad to full page size
        out_pages += bytes(RESERVE)

    out_path.write_bytes(bytes(out_pages))
    print(f"Decrypted → {out_path}")

if __name__ == "__main__":
    import sys
    enc_path = pathlib.Path(sys.argv[1])
    key_hex  = sys.argv[2]
    out_path = pathlib.Path(sys.argv[3])
    decrypt_db(enc_path, key_hex, out_path)
```

```bash
python3 decrypt_db.py \
    ~/Library/Containers/.../favorite.db \
    <32-byte-key-hex> \
    /tmp/favorite_decrypted.db
```

### Step 5 — Parse Favorites

WeChat 4.x uses a **single table** `fav_db_item` with XML content (not the 3.x `FavItems`/`FavDataItem` split):

```python
# parse_favorites.py (core logic excerpt)
import sqlite3, json, re, pathlib
from datetime import datetime
from xml.etree import ElementTree as ET

TYPE_MAP = {
    1: "text", 2: "image", 3: "voice", 4: "video",
    5: "playlist", 6: "location", 7: "attachment",
    8: "article", 43: "video_channel", 49: "link",
}

def parse_xml_content(xml_str: str, fav_type: int) -> dict:
    """Extract title, desc, source, url from XML blob."""
    result = {"title": "", "desc": "", "source": "", "url": ""}
    if not xml_str:
        return result
    try:
        root = ET.fromstring(xml_str)
    except ET.ParseError:
        return result

    def txt(tag):
        el = root.find(f".//{tag}")
        return el.text.strip() if el is not None and el.text else ""

    if fav_type == 8:           # article — WeChat 4.x uses <pagetitle>
        result["title"]  = txt("pagetitle") or txt("title")
        result["url"]    = txt("url")
        result["source"] = txt("sourcename") or txt("fromnickname")
        result["desc"]   = txt("desc")
    elif fav_type == 49:        # link
        result["title"]  = txt("title")
        result["url"]    = txt("url")
        result["source"] = txt("sourcename")
        result["desc"]   = txt("desc")
    elif fav_type in (3, 4, 43):  # voice/video
        for item in root.findall(".//dataitem"):
            t = item.findtext("datatitle", "").strip()
            if t:
                result["title"] = t
                break
        result["source"] = txt("fromnickname")
    else:                       # text, image, etc.
        result["title"]  = txt("title") or txt("pagetitle")
        result["desc"]   = txt("desc") or txt("content")
        result["source"] = txt("fromnickname")

    return result

def parse(db_path: pathlib.Path) -> list[dict]:
    con = sqlite3.connect(db_path)
    con.row_factory = sqlite3.Row
    rows = con.execute(
        "SELECT localId, favLocalId, type, createTime, updateTime, "
        "       xmlBuf, tagNames "
        "FROM   fav_db_item "
        "ORDER  BY createTime"
    ).fetchall()

    items = []
    for row in rows:
        parsed = parse_xml_content(row["xmlBuf"] or "", row["type"])
        items.append({
            "id":         row["localId"],
            "type":       TYPE_MAP.get(row["type"], f"unknown_{row['type']}"),
            "created_at": datetime.utcfromtimestamp(row["createTime"]).isoformat(),
            "updated_at": datetime.utcfromtimestamp(row["updateTime"]).isoformat(),
            "title":      parsed["title"],
            "desc":       parsed["desc"],
            "source":     parsed["source"],
            "url":        parsed["url"],
            "tags":       [t.strip() for t in (row["tagNames"] or "").split(",") if t.strip()],
        })
    con.close()
    return items

if __name__ == "__main__":
    import sys
    db   = pathlib.Path(sys.argv[1])
    out  = pathlib.Path(sys.argv[2])
    data = parse(db)
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    print(f"Parsed {len(data)} items → {out}")
```

```bash
python3 parse_favorites.py /tmp/favorite_decrypted.db /tmp/data.json
```

### Step 6 — Generate HTML Report

```bash
python3 generate_report.py --input /tmp/data.json --output /tmp/report.html
```

Serve locally (required — `file://` breaks ECharts event delegation):

```bash
cd /tmp && python3 -m http.server 8765
open http://localhost:8765/report.html
```

---

## Key Configuration Reference

| Parameter | Value | Notes |
|-----------|-------|-------|
| SQLCipher version | 4 | WeChat 4.x |
| Cipher | AES-256-CBC | — |
| HMAC | HMAC-SHA512 | — |
| KDF iterations | 256 000 | PBKDF2 |
| Page size | 4 096 bytes | — |
| Reserve per page | 80 bytes | 64 HMAC + 16 IV |
| Salt location | bytes 0–15 of file | — |
| Table name (4.x) | `fav_db_item` | 3.x used `FavItems` |
| Article title field | `<pagetitle>` | Not `<title>` |

---

## Common Issues & Fixes

### "Key not found in log"

1. Confirm you opened the **收藏** tab while Frida was attached.
2. Check log for any entries: `wc -l /tmp/wechat_frida_keys.log`
3. Salt mismatch — re-read salt: `xxd ~/…/favorite.db | head -2` (bytes 16–31 after the ASCII header).

### "database disk image is malformed"

Decryption parameters are wrong. Double-check `KDF_ITER=256000` and `PAGE_SIZE=4096`. If WeChat updated, parameters may have changed — try `kdf_iter=64000` (SQLCipher 3 default) as a fallback.

### "codesign: No identity found"

Use `-` (ad-hoc signing), not a certificate name:
```bash
codesign --force --deep --sign - ~/Desktop/WeChat.app
```

### Report images broken

Thumbnail URLs are WeChat CDN links — they require an active network session. Add `onerror` handler using `&quot;` to avoid quote conflicts in inline HTML:

```python
img_tag = f'<img src="{url}" onerror="this.style.display=&quot;none&quot;">'
```

### onclick not firing on `file://`

Use event delegation on a parent element instead of inline `onclick`:

```javascript
document.getElementById("card-list").addEventListener("click", function(e) {
  var card = e.target.closest(".fav-card");
  if (card) showDetail(card.dataset.id);
});
```

### WeChat updated — hook stopped working

Re-copy and re-sign the app bundle, then re-run the full pipeline. The PBKDF2 hook targets a system library (`libcommonCrypto.dylib`) so it is resilient to WeChat binary changes, but the re-signing step must be repeated.

---

## Report Features

| Section | Chart type |
|---------|-----------|
| Summary cards | Static KPI tiles |
| Monthly trend | ECharts line + area |
| Type distribution | ECharts doughnut |
| Top 15 sources | ECharts horizontal bar |
| Activity heatmap | ECharts heatmap (weekday × hour) |
| Word cloud | echarts-wordcloud |
| Tag cloud | CSS flex tags |
| Favorites browser | Card grid with type/tag filter + full-text search + pagination |
| Detail modal | Full content, URL, source, tags |

---

## Known Limitations

- Image/video/file binary blobs are stored in WeChat's encrypted CDN — not previewable offline.
- Key extraction requires macOS + Frida; no Windows/Linux support.
- After each WeChat update, the Desktop copy must be re-signed.
- The `tagNames` column stores comma-separated tag strings; empty tags are filtered client-side.
