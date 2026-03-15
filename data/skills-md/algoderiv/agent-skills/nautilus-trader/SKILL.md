---
name: nautilus-trader
description: NautilusTrader developer guide for contributing, building from source, testing, and extending the platform. Use this skill for NautilusTrader development setup, Rust/Python integration, testing practices, and contribution guidelines.
---

# Nt_Dev Skill

Nautilustrader developer guide for contributing, building from source, testing, and extending the platform. use this skill for nautilustrader development setup, rust/python integration, testing practices, and contribution guidelines., generated from official documentation.

## When to Use This Skill

This skill should be triggered when:
- Working with nt_dev
- Asking about nt_dev features or APIs
- Implementing nt_dev solutions
- Debugging nt_dev code
- Learning nt_dev best practices

## Quick Reference

### Common Patterns

*Quick reference patterns will be added as you use the skill.*

### Example Code Patterns

**Example 1** (bash):
```bash
uv sync --active --all-groups --all-extras
```

**Example 2** (bash):
```bash
make install
```

**Example 3** (typescript):
```typescript
crates/<crate_name>/└── benches/    ├── foo_criterion.rs   # Criterion 组    └── foo_iai.rs         # iai 微基准
```

**Example 4** (json):
```json
[[bench]]name = "foo_criterion"             # benches/ 下文件名（不含扩展名）path = "benches/foo_criterion.rs"harness = false                    # 关闭默认的 libtest harness
```

**Example 5** (bash):
```bash
make pytest# oruv run --active --no-sync pytest --new-first --failed-first# or simplypytest
```

## Reference Files

This skill includes comprehensive documentation in `references/`:

- **building.md** - Building documentation
- **getting_started.md** - Getting Started documentation
- **other.md** - Other documentation
- **rust.md** - Rust documentation
- **testing.md** - Testing documentation

Use `view` to read specific reference files when detailed information is needed.

## Working with This Skill

### For Beginners
Start with the getting_started or tutorials reference files for foundational concepts.

### For Specific Features
Use the appropriate category reference file (api, guides, etc.) for detailed information.

### For Code Examples
The quick reference section above contains common patterns extracted from the official docs.

## Resources

### references/
Organized documentation extracted from official sources. These files contain:
- Detailed explanations
- Code examples with language annotations
- Links to original documentation
- Table of contents for quick navigation

### scripts/
Add helper scripts here for common automation tasks.

### assets/
Add templates, boilerplate, or example projects here.

## Notes

- This skill was automatically generated from official documentation
- Reference files preserve the structure and examples from source docs
- Code examples include language detection for better syntax highlighting
- Quick reference patterns are extracted from common usage examples in the docs

## Updating

To refresh this skill with updated documentation:
1. Re-run the scraper with the same configuration
2. The skill will be rebuilt with the latest information
