---
name: i18n-pseudo
description: |
  Use when testing an internationalization implementation BEFORE real
  translations exist — pseudo-translate locale files to expose hardcoded
  strings, text overflow/truncation, encoding bugs, RTL layout breakage, and
  font rendering issues. 7 strategies, 5 presets, 32 file formats. Wraps the
  i18n-pseudo CLI.
allowed-tools:
  - Bash
  - Read
---

# i18n-pseudo: pseudo-translation for i18n QA

Transforms real locale files into pseudo-translated versions (e.g.
`[Šéttíñgš]`) so untranslated/hardcoded strings and layout bugs are visible at
a glance. Placeholders (`{name}`, `{{count}}`, `%s`, `${var}`, HTML tags) are
never mangled.

## Setup check

```bash
command -v i18n-pseudo || npm install -g @i18n-agent/i18n-pseudo
```

## Usage

```bash
i18n-pseudo <files...> [-o <output-dir>] [--preset <preset>] [strategy flags]
```

| Flag | Meaning |
|------|---------|
| `-o, --output <PATH>` | Output directory |
| `-f, --format <FORMAT>` | Override format auto-detection |
| `--in-place` | Modify files in place (creates `.bak` backups) |
| `--no-backup` | Skip `.bak` creation with `--in-place` |
| `--preset <PRESET>` | `default`, `layout`, `charset`, `rtl`, `full` |

Strategy flags (combine freely; `--no-<strategy>` overrides a preset):
`--accents`, `--cjk`, `--special-chars`, `--expansion <1.0-3.0>`,
`--brackets`, `--rtl`, `--unicode-stress`

## Presets

| Preset | Strategies | Use for |
|--------|-----------|---------|
| `default` | accents + brackets | Quick visual scan for untranslated strings |
| `layout` | expansion 1.5 + brackets | UI overflow/truncation testing |
| `charset` | accents + CJK + special chars + unicode stress | Encoding & font rendering |
| `rtl` | RTL markers + brackets + expansion 1.3 | Right-to-left layout testing |
| `full` | all 7 (expansion 1.3) | Comprehensive stress test |

## Examples

```bash
i18n-pseudo en.json -o pseudo/                       # default preset
i18n-pseudo en.json --preset layout -o pseudo/       # overflow testing
i18n-pseudo en.json --accents --expansion 1.5 -o pseudo/
i18n-pseudo en.json --preset layout --no-brackets -o pseudo/
```

## Agent guidance

- Pseudo-translate BEFORE real translation work: it's the cheapest way to
  prove every string goes through the i18n layer.
- For German/Finnish-bound UIs use `--preset layout` (long words); for
  Arabic/Hebrew use `--preset rtl`; for CJK targets use `--preset charset`.
- Load the pseudo file as a fake locale in the app and screenshot key screens;
  any un-bracketed English text = hardcoded string.
- Keys are NOT always preserved: the JSON parsers (auto, `-f json`, `-f i18next`) split keys on `.`, so
  natural-language keys (i18next `keySeparator: false`, e.g. `"Sign in now."`) come back as nested objects
  (seen 2026-10-22). Workaround: re-key to `{"k0": value, …}`, pseudo that, map the
  values back onto the original keys.
