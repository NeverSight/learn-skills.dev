---
name: godot-i18n
description: "Localization patterns for Godot 4.x: TranslationServer, CSV/PO/JSON translation formats, runtime language switching, RTL text support, font fallback chains, and pluralization. Use when implementing internationalization in Godot games."
license: MIT
compatibility:
  - godot-4.0
  - godot-4.1
  - godot-4.2
  - godot-4.3
  - godot-4.4
  - godot-4.5
  - godot-4.6
  - godot-4.7
metadata:
  author: vl4dt
  version: 0.1.0
  tags:
    - godot
    - i18n
    - localization
    - translation
    - rtl
  created: 2026-06-21
---

# Localization in Godot

Patterns for internationalizing Godot games.

## TranslationServer Basics

Godot's built-in translation system uses `.translation` files (CSV-based):

```gdscript
# Mark strings for translation with _() shorthand
func _ready():
    $Label.text = tr("Hello, Player!")
    $Button.text = tr("Start Game")

# tr() calls TranslationServer.translate() internally
# Strings are looked up in loaded .translation resources
```

### Creating Translation Files

Use the editor: **Project → Tools → Translation** to create `.csv` files, then export as `.translation`.

Or create CSV manually:

```csv
msgid "Hello, Player!"
msgstr "¡Hola, Jugador!"

msgid "Start Game"
msgstr "Comenzar Juego"

msgid "Score: {0}"
msgstr "Puntuación: {0}"
```

### Registering Translations

In **Project Settings → Locale → Configured Locales**, add supported languages (e.g., `es`, `fr`, `ja`).

## Runtime Language Switching

```gdscript
class_name LanguageManager extends Node

signal language_changed(locale: String)

var available_locales: Array[String] = ["en", "es", "fr", "ja"]
var current_locale: String = "en"

func set_language(locale: String) -> void:
    if not available_locales.has(locale):
        push_error("LanguageManager: Unsupported locale '%s'" % locale)
        return
    TranslationServer.set_locale(locale)
    current_locale = locale
    language_changed.emit(locale)
    _notify_ui_update()

func _notify_ui_update() -> void:
    # Re-tr() all UI labels that need updating
    # Connect to language_changed signal in UI nodes
    pass

# Save/restore preference
func _ready() -> void:
    var saved = ConfigFile.new()
    if saved.load("user://settings.cfg") == OK:
        var locale = saved.get_value("general", "language", "en")
        set_language(locale)

func _save_preference() -> void:
    var config = ConfigFile.new()
    config.load("user://settings.cfg")
    config.set_value("general", "language", current_locale)
    config.save("user://settings.cfg")
```

### Language Selector UI

```gdscript
# LanguageSelector.gd — attached to OptionButton
extends OptionButton

func _ready():
    for locale in LanguageManager.available_locales:
        var display_name = TranslationServer.get_locale_name(locale)
        add_item(display_name, locale)
    selected = LanguageManager.available_locales.find(LanguageManager.current_locale)
    item_selected.connect(LanguageManager.set_language)
```

## Pluralization

Godot supports plural forms via `trn()`:

```gdscript
# trn(singular, plural, count)
func show_item_count(count: int):
    $Label.text = trn("You have {0} item.", "You have {0} items.", count) % count

# For complex plurals (Slavic languages with 3+ forms), use custom logic
func get_plural_string(msgid_singular: String, msgid_plural: String, n: int) -> String:
    # Godot handles plural forms via .po format plural rules
    return trn(msgid_singular, msgid_plural, n)
```

## RTL Text Support

For Arabic, Hebrew, and other right-to-left languages:

```gdscript
# In Label or RichTextLabel:
$Label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
$Label.text_direction = TextServer.DIRECTION_RTL
$Label.alignment = HORIZONTAL_ALIGNMENT_RIGHT

# For mixed LTR/RTL content, use RichTextLabel with bbcode
$RichTextLabel.text = "[rtl]مرحبا[/rtl] [ltr]Hello[/ltr]"
```

### RTL-Aware UI Layout

```gdscript
# Container layouts flip automatically with RTL
# Use Control.layout_mode for proper RTL support:
$PanelContainer.set_anchors_preset(Control.PRESET_FULL_RECT)

# For manual positioning, mirror anchors:
func mirror_for_rtl(control: Control) -> void:
    if TranslationServer.get_locale() in ["ar", "he", "fa"]:
        var left = control.anchor_left
        control.anchor_left = control.anchor_right
        control.anchor_right = left
```

## Font Fallback Chains

Handle characters not available in the primary font:

```gdscript
# Theme approach (recommended):
# 1. Create Theme resource
# 2. Set "FontFile" for Label/LineEdit
# 3. Add fallback fonts via DynamicFont

# Code approach:
var dynamic_font = DynamicFont.new()
dynamic_font.font_path = "res://fonts/primary.ttf"
dynamic_font.fallback_fonts.append(DynamicFontLoading.new())
$Label.add_theme_font_override("font", dynamic_font)

# For CJK + Latin support, chain fonts:
# Primary: Noto Sans (Latin) → Fallback: Noto Sans CJK
```

## Translation Best Practices

### Use Context Keys

```gdscript
# When the same word has different meanings:
tr("Attack [weapon]")   # As a verb
tr("Attack [noun]")     # As a noun/stat name

# In .po files, msgctxt provides context
# msgctxt "weapon" / msgid "Attack" / msgstr "Atacar"
# msgctxt "noun" / msgid "Attack" / msgstr "Ataque"
```

### Avoid String Concatenation for Translatable Text

```gdscript
# Bad — translators can't reorder
tr("You found ") + item_name + tr(" in the cave!")

# Good — translators control word order
tr("You found {0} in the cave!") % item_name

# Better — named placeholders for clarity
tr("You found {item} in {location}!") % {"item": item_name, "location": location_name}
```

### Externalize All UI Strings

```gdscript
# Hardcoded strings make translation impossible
$Label.text = "Score: 100"  # BAD

# Use tr() for everything visible to players
$Label.text = tr("Score: {0}") % score  # GOOD
```

## Godot 4.7 i18n Notes

- **TextServer** API improved for complex script handling
- **RichTextLabel** supports better RTL paragraph alignment
- Translation import pipeline handles `.po` files natively (no conversion needed)

## MCP Bridge Tools (Optional — Live Editor Integration)

When the MCP bridge is running (Phase 2), these tools can inspect and modify your project live:

- **`project_info`** — Check configured locales and translation file paths
- **`script_read`** / **`script_edit`** — Read and modify localization scripts

> **Note:** MCP tools require the Godot editor to be running with the MCP plugin enabled. Skills work independently without the bridge.

## References

- [TranslationServer Deep Dive](references/translation-server.md)
- [RTL Layout Patterns](references/rtl-layout.md)
- [Font Fallback Strategies](references/font-fallbacks.md)
