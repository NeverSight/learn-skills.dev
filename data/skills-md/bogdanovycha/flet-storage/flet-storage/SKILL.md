---
name: flet-storage
description: Provides instructions and examples for using the flet-storage package, a lightweight asynchronous wrapper around Flet's SharedPreferences for persistent data management in Flet applications.
---

# FletStorage Skill

This skill provides context, examples, and best practices for integrating and working with the `flet-storage` package in Python Flet applications.

## What is `flet-storage`?

`flet-storage` is an asynchronous Python library built on top of Flet's `SharedPreferences`. It simplifies data persistence by providing:
- **Automatic JSON Serialization:** Transparently handles Python data types like `dict`, `list`, `set`, `str`, `int`, `float`, `bool`, and `None`. Sets are automatically preserved during serialization and deserialization.
- **Namespaced Storage:** Automatically prefixes keys with an `app_name` to prevent data collisions between different Flet applications on the same device or web domain.
- **Asynchronous API:** Offers non-blocking data operations for modern async Flet apps.
- **Robust API methods:** Includes `get_or_default()`, `contains_key()`, and safe parallelized `clear()` operations.

## When to Use This Skill

Activate this skill when the user:
- Asks how to save user preferences, session tokens, or local cache in a Flet app.
- Mentions `flet-storage` or `SharedPreferences` in Flet.
- Encounters issues with JSON serialization when storing data in Flet, especially with Python `set`s.
- Needs to persist data between app sessions.
- Asks about storing configuration, UI state, or small datasets locally.

## How to Guide the User

### 1. Installation

If the user hasn't installed it, suggest installing the package via pip:
```bash
pip install flet-storage
```

### 2. Basic Setup and Usage Example

Provide this typical usage pattern when users ask how to initialize and use the library:
```python
import flet as ft
from flet_storage import FletStorage

async def main(page: ft.Page):
    # Initialize storage with an app namespace to avoid key collisions
    storage = FletStorage(app_name="my_awesome_app")
    
    # Writing data (automatically serializes dicts, lists, sets, etc.)
    await storage.set("user_settings", {"theme": "dark", "notifications": True})
    await storage.set("login_attempts", 3)
    
    # Working with Python sets (automatically preserved!)
    await storage.set("favorite_tags", {"python", "flet", "async"})
    tags = await storage.get("favorite_tags")  # Returns a set, not a list
    
    # Reading data
    settings = await storage.get("user_settings")  # Returns a standard Python dict
    attempts = await storage.get_or_default("login_attempts", 0)
    
    # Checking for keys
    if await storage.contains_key("user_settings"):
        print("Settings found!")
        
    # Deleting a specific key
    await storage.remove("login_attempts")
    
    # Clearing all data associated with THIS app_name namespace
    await storage.clear()
    
    page.add(ft.Text(f"Settings loaded: {settings}"))
    page.add(ft.Text(f"Tags loaded (type: {type(tags).__name__}): {tags}"))

ft.run(main)
```

### 3. Key Methods to Remember

- `await storage.set(key: str, value: Any)`: Serializes and saves a value. Supports `set` directly.
- `await storage.get(key: str)`: Retrieves and deserializes a value. Reconstructs `set` objects automatically. Raises `KeyError` if the key does not exist.
- `await storage.get_or_default(key: str, default: Any)`: Retrieves a value or returns the provided `default` if the key is missing.
- `await storage.contains_key(key: str)`: Returns `True` if the key exists, otherwise `False`.
- `await storage.remove(key: str)`: Deletes the specific key from storage.
- `await storage.get_keys()`: Retrieves a list of all keys belonging to the current application namespace.
- `await storage.clear()`: Clears all stored data that belongs to the initialized `app_name` namespace.

### 4. Storage Limitations

Important to know when designing your app:
- **Web (localStorage):** ~5-10MB typical limit
- **Desktop/Mobile:** More generous, but still intended for configuration and small datasets
- **Use case:** Perfect for user preferences, auth tokens, small lists, UI state, cached data
- **Not suitable for:** Large datasets (>1-5MB), media files, database-like operations

For large datasets or complex queries, recommend using SQLite (`sqlite3` module) or backend APIs instead.

### 5. Error Handling

Guide users on proper exception handling:
```python
# Handling missing keys
try:
    user_data = await storage.get("user")
except KeyError:
    print("User data not found, using defaults")
    user_data = {"name": "Guest"}

# Handling corrupted JSON data
try:
    settings = await storage.get("settings")
except ValueError as e:
    print(f"Corrupted data: {e}")
    await storage.remove("settings")  # Clean up bad data

# Safe pattern using get_or_default (recommended)
user_data = await storage.get_or_default("user", {"name": "Guest"})
```

### 6. Working with Sets (Advanced Example)
```python
async def manage_tags(storage: FletStorage):
    # Initialize with empty set if not exists
    tags = await storage.get_or_default("tags", set())
    
    # Add tags
    tags.add("python")
    tags.add("flet")
    await storage.set("tags", tags)
    
    # Remove tag
    tags.discard("python")
    await storage.set("tags", tags)
    
    # Check membership
    if "flet" in tags:
        print("Flet tag exists!")
    
    return tags
```

**Important:** Sets are stored internally as `{"__type__": "set", "values": [...]}`. If you store a dict with key `"__type__"` equal to `"set"`, it may be misinterpreted during deserialization.

### 7. Data Caching Pattern

Show users how to implement time-based cache expiration:
```python
import time

async def cache_data(storage: FletStorage, key: str, data: Any, ttl: int = 3600):
    """Cache data with time-to-live in seconds."""
    cache_entry = {
        "data": data,
        "expires_at": time.time() + ttl
    }
    await storage.set(f"cache_{key}", cache_entry)

async def get_cached_data(storage: FletStorage, key: str) -> Any | None:
    """Retrieve cached data if not expired."""
    try:
        cache_entry = await storage.get(f"cache_{key}")
        if time.time() < cache_entry["expires_at"]:
            return cache_entry["data"]
        else:
            await storage.remove(f"cache_{key}")
            return None
    except KeyError:
        return None
```

### 8. Cross-Platform Compatibility

`flet-storage` works across all Flet platforms:
- ✅ **Web:** Uses browser localStorage
- ✅ **Windows/macOS/Linux:** Uses platform-specific preferences storage
- ✅ **Android/iOS:** Uses native storage APIs

**Tested platforms:**
- Android (production apps)
- Web applications
- Linux (compiled binaries)
- Windows (development environment)

**Note:** iOS/macOS community testing welcome - underlying Flet implementation should work seamlessly.

### Best Practices and Caveats

1. **Always Use Namespaces:** Strongly recommend initializing `FletStorage` with a unique `app_name`. Web browsers and some desktop environments share local storage per domain/user, and omitting a namespace can lead to apps overwriting each other's data.

2. **Async Environment:** Remind the user that `flet-storage` functions are `async`. They must be `await`ed, and the Flet `main` function (or event handlers using it) must be asynchronous (`async def`).

3. **Security:** Stored data (where `flet-storage` saves information) is **not encrypted**. Warn the user against storing sensitive data like clear-text passwords or high-privilege API keys unless they manually encrypt it first.

4. **Use `get_or_default()` for Optional Data:** Instead of try-except blocks, prefer `get_or_default()` for cleaner code when dealing with optional configuration.

5. **Regular Cleanup:** For apps with temporary data (caches, session data), implement periodic cleanup to prevent storage bloat:
```python
   # Example: Clean up old cached data
   async def cleanup_old_cache(storage: FletStorage):
       keys = await storage.get_keys()
       for key in keys:
           if key.startswith("cache_"):
               await storage.remove(key)
```

6. **Structure Your Data:** Store related data together in dictionaries for better organization and fewer storage operations.

7. **Use Sets for Unique Collections:** Sets are automatically preserved and are perfect for storing unique items like tags, favorites, or categories.

### Common Pitfalls to Avoid

1. **Forgetting to await:**
```python
   # ❌ Wrong - missing await
   storage.set("key", "value")
   
   # ✅ Correct
   await storage.set("key", "value")
```

2. **Not using async function:**
```python
   # ❌ Wrong - sync function
   def save_data(storage):
       await storage.set("key", "value")  # SyntaxError!
   
   # ✅ Correct
   async def save_data(storage):
       await storage.set("key", "value")
```

3. **Storing too much data:**
```python
   # ❌ Bad - large dataset in storage
   await storage.set("all_users", huge_list_of_10000_users)
   
   # ✅ Better - use backend/database for large data
   await storage.set("cached_recent_users", recent_10_users)
```

4. **Not handling exceptions:**
```python
   # ❌ Risky - will crash if key missing
   user = await storage.get("user")
   
   # ✅ Safe - using get_or_default
   user = await storage.get_or_default("user", {"name": "Guest"})
   
   # ✅ Also safe - explicit error handling
   try:
       user = await storage.get("user")
   except KeyError:
       user = {"name": "Guest"}
```

### Data Migration Pattern

When updating app structure, show how to safely migrate data:
```python
async def migrate_storage(storage: FletStorage):
    """Migrate storage schema from v1 to v2."""
    version = await storage.get_or_default("schema_version", 1)
    
    if version == 1:
        # Migrate from v1 to v2
        old_settings = await storage.get_or_default("settings", {})
        new_settings = {
            "ui": {
                "theme": old_settings.get("theme", "light"),
                "language": old_settings.get("language", "en")
            },
            "notifications": old_settings.get("notifications", True),
            "version": 2
        }
        await storage.set("settings", new_settings)
        await storage.set("schema_version", 2)
        print("Migrated to schema v2")
```

## Additional Resources

- **PyPI:** https://pypi.org/project/flet-storage/
- **GitHub:** https://github.com/BogdanovychA/flet-storage
- **Issues:** https://github.com/BogdanovychA/flet-storage/issues
- **Documentation:** Full API reference and examples available in the GitHub README

## Requirements

- Python 3.10+
- Flet >= 0.81.0

## License

MIT License
