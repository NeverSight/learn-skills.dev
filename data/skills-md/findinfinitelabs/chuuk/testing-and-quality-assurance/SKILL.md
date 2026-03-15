---
name: testing-and-quality-assurance
description: Testing patterns for Python Flask APIs, ML translation models, and database operations. Use when writing tests, setting up test fixtures, or validating translation accuracy for the Chuuk Dictionary application.
---

# Testing & Quality Assurance

## Overview

Test infrastructure uses **pytest**. The `tests/` directory has a mix of utility scripts and actual `test_*.py` files. `tests/conftest.py` and `pytest.ini` are the canonical test configuration.

## Running Tests

```bash
# From project root with .venv active
.venv/bin/python -m pytest                    # run all tests
.venv/bin/python -m pytest -m unit            # unit tests only
.venv/bin/python -m pytest -m "not slow"      # skip slow ML tests
.venv/bin/python -m pytest tests/test_basic.py -v
```

## pytest.ini Markers

```ini
[pytest]
testpaths = tests
addopts = -v --tb=short -q
markers =
    unit: Pure unit tests — no I/O or network
    integration: Tests that require a real database or network
    translation: Tests that exercise the Helsinki-NLP pipeline
    slow: Tests expected to take > 5 seconds
```

## conftest.py Fixtures

`tests/conftest.py` provides:

| Fixture | Scope | Purpose |
|---|---|---|
| `mock_db` | session | `MagicMock` of `DictionaryDB` — no real DB required |
| `flask_app` | session | Flask test app with DB and translator mocked |
| `client` | function | Flask test client |
| `auth_headers` | function | Pre-authenticated session |

## Critical Patch Targets

The app uses **module-level globals** — patch them correctly:

```python
# CORRECT — variable is dict_db, not app.db
from unittest.mock import patch, MagicMock

def test_search(client):
    mock = MagicMock()
    mock.search_entries.return_value = [{'chuukese_word': 'ran', 'english_translation': 'water'}]
    with patch('app.dict_db', mock):
        resp = client.get('/api/dictionary/search?q=ran')
    assert resp.status_code == 200

# CORRECT — collection attribute is dictionary_collection
mock_db.dictionary_collection.find.return_value = iter([...])

# CORRECT — method is bulk_insert_entries, not bulk_insert
mock_db.bulk_insert_entries.return_value = {'inserted': 5}

# CORRECT — translator is a module global, not a function
with patch('app.helsinki_translator') as mock_translator:
    mock_translator.translate.return_value = 'water'
    ...
```

## API Test Pattern

```python
import pytest

@pytest.mark.unit
def test_dictionary_search_empty_query(client, auth_headers):
    resp = client.get('/api/dictionary/search?q=')
    assert resp.status_code in (200, 400)

@pytest.mark.integration
def test_bible_coverage(client, auth_headers):
    resp = client.get('/api/database/bible-coverage')
    data = resp.get_json()
    assert 'books' in data
```

## Translation Accuracy Testing

```python
from sacrebleu.metrics import BLEU

bleu = BLEU()
result = bleu.corpus_score(hypotheses, [references])
assert result.score > 15.0, f"BLEU too low: {result.score}"
```

## Test File Inventory

Files in `tests/` prefixed `test_` are runnable with pytest:
- `test_basic.py` — publication manager, JW.org lookup
- `test_collections.py` — database collection ops
- `test_helsinki_trainer.py` — HelsinkiNLP training helpers
- `test_translation.py` — translation pipeline
- `test_scripture_parsing.py` — scripture parsing logic
- `test_word_families.py` — word family grouping

Files **without** the `test_` prefix are exploratory scripts and are not collected by pytest.

## Source Files

- `tests/conftest.py` — shared fixtures
- `pytest.ini` — test runner configuration
- `tests/test_basic.py` — canonical example tests
