---
name: data-migration-versioning
description: |
  Provides systematic data format migration and versioning for backward-compatible schema changes.
  Use when "add data versioning", "migrate data format", "backward compatible file format",
  "upgrade v1 to v2", "schema migration", "support old file format", or "migrate JSON structure".
  Covers version numbering strategies (semantic, dotted, integer, date-based), backward compatibility
  patterns (auto-convert, explicit migration, dual-format), auto-upgrade timing, field deprecation,
  testing checklists, and common pitfalls like partial data preservation. Works with JSON, YAML,
  database schemas, and configuration files in Python, JavaScript, Go, Rust.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
---

# Data Migration & Versioning

## Table of Contents

### Core Sections
- [When to Use This Skill](#when-to-use-this-skill) - Trigger phrases and situations
- [What This Skill Does](#what-this-skill-does) - Migration workflow and outcomes
- [Quick Start](#quick-start) - Immediate examples
  - [Example 1: JSON Format Migration](#example-1-json-format-migration) - v1.0 → v2.0 upgrade
  - [Example 2: Auto-Upgrade on Load](#example-2-auto-upgrade-on-load) - Transparent migration

### Migration Process
- [Version Numbering Strategies](#version-numbering-strategies) - Semantic, dotted, integer versioning
- [Backward Compatibility Patterns](#backward-compatibility-patterns) - Load old formats
- [Auto-Upgrade Timing](#auto-upgrade-timing) - When to migrate (load, save, update)
- [Field Deprecation Workflow](#field-deprecation-workflow) - Remove old fields safely
- [Testing Checklist](#testing-checklist) - Comprehensive migration validation

### Implementation
- [Migration Workflow](#migration-workflow) - 7-step process
- [Common Pitfalls](#common-pitfalls) - Anti-patterns to avoid
- [Language-Specific Patterns](#language-specific-patterns) - Python, JavaScript, Go, Rust

### Supporting Resources
- [Supporting Files](#supporting-files) - References, examples, templates, scripts
- [Examples](#examples) - Real-world migration patterns
- [Troubleshooting](#troubleshooting) - Common issues and solutions

## Purpose

Provides systematic guidance for migrating data formats (JSON, YAML, SQLite, config files) with version numbering and backward compatibility. Prevents data loss during migrations by enforcing testing checklists and detecting common anti-patterns like partial preservation. Essential when evolving file formats, adding features that require schema changes, or supporting multiple versions of data structures.

## When to Use This Skill

**Use when:**
- Adding version field to existing data format
- Migrating from v1.0 to v2.0 (or any version change)
- Adding new fields that change data structure
- Supporting multiple schema versions simultaneously
- Upgrading file formats (JSON, YAML, config files)
- Migrating database schemas with backward compatibility

**User trigger phrases:**
- "add data versioning"
- "migrate data format"
- "backward compatible file format"
- "upgrade v1 to v2"
- "schema migration"
- "support old file format"
- "migrate JSON structure"

**NOT for:**
- Breaking changes without backward compatibility
- Database migrations with ORM tools (use Alembic, Flyway, etc.)
- API versioning (different concern)

## What This Skill Does

Guides you through a systematic data migration process:

1. **Version Numbering** - Choose appropriate versioning scheme
2. **Backward Compatibility Design** - Load old formats transparently
3. **Auto-Upgrade Strategy** - Decide when to migrate data
4. **Migration Implementation** - Write conversion code
5. **Field Cleanup** - Remove deprecated fields
6. **Testing** - Validate all migration paths
7. **Documentation** - Record format changes

**Result:** ✅ Safe migration with zero data loss and backward compatibility

## Quick Start

### Example 1: JSON Format Migration

**Scenario:** Adding multi-material support to layout optimizer

**Before (v1.0):**
```json
{
  "version": "1.0",
  "material": "18mm Plywood",
  "result": { ... }
}
```

**After (v2.0):**
```json
{
  "version": "2.0",
  "materials": {
    "18mm Plywood": { "result": { ... } },
    "6mm MDF": { "result": { ... } }
  }
}
```

**Migration code:**
```python
def load_layout(path):
    data = json.loads(path.read_text())
    version = data.get("version", "1.0")

    if version == "1.0":
        # Auto-convert to v2.0 structure
        material = data.get("material", "Unknown")
        result = PackingResult.from_dict(data["result"])
        return {material: result}, config  # Return as dict

    elif version == "2.0":
        # Load v2.0 format
        results = {}
        for mat_name, mat_data in data["materials"].items():
            results[mat_name] = PackingResult.from_dict(mat_data["result"])
        return results, config
```

**Outcome:** Old v1.0 files load seamlessly, returned in v2.0 structure

### Example 2: Auto-Upgrade on Load

**User workflow:**
```
1. User has old v1.0 file: layout-old.json
2. Loads file via load_layout()
3. Adds new material
4. Saves via update_layout()
5. File automatically upgraded to v2.0
6. Both old and new materials preserved ✅
```

**Critical anti-pattern detected by this skill:**
```python
# ❌ BAD: Only saves original material during upgrade
materials_data = {
    original_material: {"result": results[original_material].to_dict()}
}
# RESULT: New materials LOST! 💥

# ✅ GOOD: Iterate through ALL materials
materials_data = {}
for mat_name, result in results.items():
    materials_data[mat_name] = {"result": result.to_dict()}
# RESULT: All materials preserved ✅
```

## Instructions

### Step 1: Choose Version Numbering Strategy

**Semantic Versioning (MAJOR.MINOR.PATCH):**
- Use for: Libraries, APIs, public data formats
- Example: `{"version": "2.1.0"}`

**Dotted Versioning (MAJOR.MINOR):**
- Use for: Application data files, configuration files
- Example: `{"version": "2.0"}`

**Integer Versioning (1, 2, 3):**
- Use for: Internal formats, simple migrations
- Example: `{"version": 2}`

**Date-Based Versioning (YYYY-MM-DD):**
- Use for: Configuration files, data exports, snapshots
- Example: `{"version": "2025-12-21"}`

See [references/detailed-patterns.md](./references/detailed-patterns.md#version-numbering-strategies-detailed) for complete guide.

### Step 2: Design Backward Compatibility Pattern

**Pattern 1: Auto-Convert on Load (Recommended)**
```python
def load_data(path):
    data = json.loads(path.read_text())
    version = data.get("version", "1.0")

    if version == "1.0":
        return convert_v1_to_v2(data)  # Auto-convert in memory
    elif version == "2.0":
        return load_v2(data)
    else:
        raise ValueError(f"Unsupported version: {version}")
```

**When to use:** Most applications (transparent, works with read-only files)

**Pattern 2: Explicit Migration Script**
- Use for: Large datasets, breaking changes, user needs notification

**Pattern 3: Dual-Format Support**
- Use for: Transitional periods, multiple clients with different versions

See [references/detailed-patterns.md](./references/detailed-patterns.md#backward-compatibility-patterns-detailed) for all patterns.

### Step 3: Choose Auto-Upgrade Timing

**Option 1: On Load (Recommended)**
- Advantage: Immediate compatibility, works with read-only files
- Disadvantage: File stays in old format until saved

**Option 2: On First Save**
- Advantage: File updated to new format on disk
- Disadvantage: File remains old format if never saved

**Option 3: On First Update (Hybrid)**
- Advantage: File loads in any format, upgrades only when modified
- Disadvantage: More complex logic

**Option 4: Manual Migration Tool**
- Advantage: User controls timing, can handle large batches
- Disadvantage: Requires user action

See [references/detailed-patterns.md](./references/detailed-patterns.md#auto-upgrade-timing-detailed) for implementation examples.

### Step 4: Implement Load Function

```python
def load_multi_version(path):
    data = json.loads(path.read_text())
    version = data.get("version", "1.0")

    if version == "1.0":
        return load_v1(data)  # Auto-convert
    elif version == "2.0":
        return load_v2(data)
    else:
        raise ValueError(f"Unsupported version: {version}")
```

### Step 5: Implement Save/Update Functions with Field Cleanup

```python
def update_layout(path, results):
    """Update existing file, auto-upgrade if v1.0."""
    data = json.loads(path.read_text())
    version = data.get("version", "1.0")

    if version == "1.0":
        # Upgrade to v2.0 - save ALL materials (not just original!)
        data["version"] = "2.0"
        data["materials"] = {
            mat_name: {"result": result.to_dict()}
            for mat_name, result in results.items()  # ALL materials
        }
        # Clean up old fields
        data.pop("material", None)
        data.pop("result", None)

    elif version == "2.0":
        # Update existing v2.0 structure
        for mat_name, result in results.items():
            data["materials"][mat_name] = {"result": result.to_dict()}

    path.write_text(json.dumps(data, indent=2))
```

### Step 6: Write Comprehensive Tests

**Essential test checklist:**
- [ ] Load v1.0 file - Verify old format loads without errors
- [ ] Load v2.0 file - Verify new format loads correctly
- [ ] Round-trip v2.0 (save → load) - Data preserved
- [ ] Upgrade v1.0 → v2.0 (load v1 → save → load) - Verify upgrade works
- [ ] **Data preservation** - ALL entities/materials preserved during upgrade ← CRITICAL
- [ ] Field cleanup - Old fields removed after upgrade
- [ ] Version detection - Correct version identified
- [ ] Error handling - Unsupported versions rejected with clear error

**Critical test pattern:**
```python
def test_v1_to_v2_upgrade_preserves_all_data():
    """Test v1.0 file auto-upgrades to v2.0 with all data preserved."""
    # Create v1.0 file
    v1_data = {
        "version": "1.0",
        "material": "18mm Plywood",
        "result": {"sheets_used": 2}
    }

    # Load v1.0 (auto-converts)
    results, config = load_layout(v1_path)
    assert len(results) == 1

    # Add new material
    results["6mm MDF"] = create_result(sheets_used=1)

    # Update (triggers v1→v2 upgrade)
    update_layout(v1_path, results)

    # Verify upgrade
    upgraded = json.loads(v1_path.read_text())
    assert upgraded["version"] == "2.0"
    assert len(upgraded["materials"]) == 2  # Both materials!
    assert "18mm Plywood" in upgraded["materials"]
    assert "6mm MDF" in upgraded["materials"]
    assert "material" not in upgraded  # Old field removed
```

See [references/detailed-patterns.md](./references/detailed-patterns.md#testing-strategies-detailed) for complete test suite template.

### Step 7: Update Documentation

```markdown
# File Format

## Version 2.0 (Current)
- Multi-material support
- Structure: `{"version": "2.0", "materials": {...}}`

## Version 1.0 (Deprecated, still supported)
- Single material only
- Structure: `{"version": "1.0", "material": "...", "result": {...}}`

## Migration
v1.0 files auto-convert on load. On first update, files upgrade to v2.0 format.
```

## Red Flags to Avoid

### ❌ Critical: Partial Data Preservation Bug

**Problem:** Only saving original entity during migration

```python
# ❌ BAD: Only saves the material from v1.0 file
materials_data = {
    original_material: {"result": results[original_material].to_dict()}
}
# RESULT: If user added new materials, they're LOST! 💥
```

**Fix:**
```python
# ✅ GOOD: Iterate through ALL materials
materials_data = {}
for mat_name, result in results.items():
    materials_data[mat_name] = {"result": result.to_dict()}
# RESULT: All materials preserved ✅
```

**Real-world impact:** This exact bug was found during Stream A testing. Would have caused DATA LOSS.

### ❌ Other Red Flags

- [ ] Missing version field in original format (use `data.get("version", "1.0")`)
- [ ] Breaking changes without backward compatibility
- [ ] Orphaned fields after migration (use `data.pop()` to clean up)
- [ ] Untested migration paths (always test v1→v2 upgrade)
- [ ] Unclear version errors (provide expected versions in error message)
- [ ] Not handling missing optional fields during migration
- [ ] Hardcoding version strings instead of using constants

## Integration Points

### With Project Patterns

**ServiceResult Pattern:**
```python
from domain.value_objects import ServiceResult

def migrate_file(path: str, target_version: str) -> ServiceResult[dict]:
    try:
        data = load_data(path)
        migrated = upgrade_to_version(data, target_version)
        save_data(path, migrated)
        return ServiceResult.success(migrated)
    except ValueError as e:
        return ServiceResult.failure(f"Migration failed: {e}")
```

**Fail-Fast Version Detection:**
```python
# ✅ CORRECT - Fail fast on unsupported version
def load_data(path):
    version = data.get("version", "1.0")
    if version not in ["1.0", "2.0"]:
        raise ValueError(f"Unsupported version: {version}")
    # Continue with version-specific loading

# ❌ WRONG - Silently default to v1.0
def load_data(path):
    version = data.get("version", "1.0")  # Always treats unknown as v1.0
```

## Supporting Files

### References
- **[detailed-patterns.md](./references/detailed-patterns.md)** - Comprehensive guide with all version numbering strategies, backward compatibility patterns, auto-upgrade timing options, field deprecation workflow, language-specific patterns (Python, JavaScript, Go, Rust), advanced migration scenarios, and detailed testing strategies

### Examples
- **[json-v1-to-v2.md](./examples/json-v1-to-v2.md)** - Real-world JSON migration (Stream A layout optimizer)
- **[yaml-migration.md](./examples/yaml-migration.md)** - YAML configuration migration example

### Templates
- **[migration-test-suite.py](./templates/migration-test-suite.py)** - Complete test template with all essential tests

## Expected Outcomes

**Successful Migration:**
```
✅ Old v1.0 files load seamlessly
✅ New v2.0 files load correctly
✅ Auto-upgrade preserves ALL data (no partial preservation bugs)
✅ Deprecated fields removed after upgrade
✅ Clear errors for unsupported versions
✅ All tests pass (especially data preservation test)
```

**Common Issues:**
- **Partial data preservation bug** - See [Red Flags](#red-flags-to-avoid)
- **Orphaned fields** - Old fields remain after upgrade (see Step 5)
- **Version detection fails** - Use `data.get("version", "1.0")` with explicit default
- **Old files won't load** - Ensure backward compatibility in load function

## Requirements

**No external dependencies** - Works with standard library JSON/YAML parsing

**Minimum requirements:**
- Read/Write access to data files
- JSON or YAML parser
- Unit testing framework (for validation)

**Optional:**
- Schema validation library (JSON Schema, Pydantic)
- Migration tracking system (database or log file)
