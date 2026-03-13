---
name: flask-api-development
description: Build Flask REST APIs with authentication, file handling, database integration, and production deployment. Use when creating or modifying API endpoints, implementing authentication, or working with the Flask backend for the Chuuk Dictionary application.
---

# Flask API Development

## Overview

The Chuuk Dictionary backend is a **single-file monolith**: `app.py` (~4150 lines) that contains all routes, auth logic, translation pipelines, OCR helpers, and database access. There is no Blueprint split.

## Application Structure

```text
chuuk/
├── app.py                          # All Flask routes and logic (~4150 lines)
├── src/
│   ├── core/jworg_lookup.py        # JW.org word lookup
│   ├── database/
│   │   ├── db_factory.py           # Connection helpers (module-level functions)
│   │   └── dictionary_db.py        # DictionaryDB class
│   ├── ocr/ocr_processor.py
│   ├── translation/
│   │   ├── helsinki_translator_v2.py
│   │   └── hybrid_translator.py
│   └── utils/nwt_epub_parser.py
├── config/
│   ├── users.json                  # Authorised users
│   └── bible_books.json            # Bible book metadata (66 books)
└── requirements.txt
```

## Key Conventions

### Module-level globals (not injected)

```python
# app.py — initialised at startup (not inside routes)
dict_db = DictionaryDB()           # database handle — NOT app.db
training_status = {}               # background job state
training_status_lock = threading.Lock()  # guards training_status mutations

helsinki_translator = None         # loaded lazily via load_helsinki_translator()
```

CORS is **disabled** (`flask_cors` import is commented out). Add it back deliberately if needed.

### Magic-link authentication (no passwords)

```python
magic_links = {}        # {token: {'email': email, 'expires': datetime}}
active_sessions = {}    # {email: session_id}  — enforces single active session

@app.route('/api/auth/request-magic-link', methods=['POST'])
def request_magic_link():
    email = request.json.get('email', '').lower().strip()
    # ... validate email against users.json, generate token, send SMTP email ...

@app.route('/auth/magic/<token>')
def magic_link_login(token):
    # ... validate token, create session, redirect to frontend ...
```

### Route return pattern

```python
@app.route('/api/dictionary/search', methods=['GET'])
@login_required
def api_search():
    try:
        query = request.args.get('q', '')
        results = dict_db.search_entries(query)   # use dict_db, not app.db
        return jsonify({'results': results})
    except Exception as e:
        app.logger.error(f'Search error: {e}')
        return jsonify({'error': str(e)}), 500
```

### Background training jobs

Mutate `training_status` only inside `training_status_lock`:

```python
with training_status_lock:
    training_status['state'] = 'running'
```

### Bible data

```python
# Loaded from config/bible_books.json — do NOT hardcode inline
BIBLE_BOOKS = _load_bible_books()   # dict keyed by book name
```

## Environment Variables

| Variable | Purpose | Default |
|---|---|---|
| `FLASK_SECRET_KEY` | Session signing key | random (dev) / required (prod) |
| `FLASK_ENV` | Environment tag | — |
| `COSMOS_DB_CONNECTION_STRING` | Cosmos DB URI | — |
| `SMTP_HOST/PORT/USER/PASSWORD` | Magic-link email | stdout fallback |
| `GOOGLE_VISION_API_KEY` | Cloud Vision OCR | optional |

## Testing

See `tests/conftest.py`. Mock `dict_db` via `patch('app.dict_db', mock_db)`.

## Source Files

- Backend entry point: `app.py`
- Database layer: `src/database/dictionary_db.py`
- Auth logic: `app.py` (magic-link sections, ~line 83–170)
