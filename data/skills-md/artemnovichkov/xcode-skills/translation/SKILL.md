---
name: translation
description: "Translate strings in Xcode String Catalogs (.xcstrings files). Prefer to use the `xcode-integration:translation-coordinator` skill for task-coordination. Use this skill when translating individual strings or working with String Catalogs. Should only be activated when translating a single string or a small batch of known string keys. The `translation-coordinator` skill should be used for anything else."
displayName: "Translate Strings"
sfSymbolName: translate
---
# String Catalog Translator

Translate a given set of strings in Xcode String Catalogs using specialized MCP tools. These strings are user-facing software strings for apps on Apple platforms — typically short UI text such as button titles, labels, and messages. Translate them as you would for a native app on those platforms. Access String Catalogs **only** through these tools—never write .xcstrings files directly.

Abort if no list of keys was provided, or if no target locale identifier was provided — something went wrong. Do not guess a locale from examples; the target locale must come from your initial instructions.

## Role Boundaries

A specific list of string keys and a target locale identifier have been provided via your initial instructions.
- Do not fetch additional string keys beyond what you were given
- Do not translate into any locale other than the one explicitly provided
- Do not use `LocalizationPlanner` (your coordinator already ran it)
- Do not spawn sub-agents of your own



## Quick Reference

| Tool | Purpose |
|------|---------|
| `StringCatalogRead` | Get string keys by translation state (new, needs_review, translated, machine_translated) |
| `StringCatalogContext` | Get source value and context: comments, similar strings, code locations, plural cases |
| `StringCatalogEdit` | Insert the translation |

## Workflow

Skip the `LocalizationPlanner` tool when told to do so.

For each string, **one at a time**, follow these steps in order.

**Step 1: Get source value and context**
Call `StringCatalogContext` with the target locale. The `sourceValues` field in the response contains the text that must be translated. The rest of the response provides context:
- Developer comments explaining intent
- Existing translations in other languages
- Similar strings with their translations (for terminology consistency)
- Code locations where the string is used
- UI appearance hints (button vs. label affects verb/noun choice)
- Required plural cases for the target locale

**Step 2: Read the source code** at the provided file paths to understand how the string is used. This reveals the developer's intention and helps you choose the right translation (e.g., a verb for buttons, descriptive for labels). For instance, the key "Save" could be a verb (button action → "Speichern") or a noun (a save file → "Spielstand") — only the source code reveals which. Reading the source code is REQUIRED for finding a good translation. If usage data is unavailable, use all the context clues you have so far — developer comments, similar strings, appearance hints, and existing translations in other languages.

Some UI words are both noun and verb (e.g. "Bookmark", "Archive", "Save"), and the noun is the more common reading, so might be the one you fall back to by default. When the comment, code, or appearance information shows the string is a button or other action control, you **MUST** translate it as a verb, not a noun (or the appropriate part-of-speech according to the target language's style guide). For instance, a "Bookmark" button is the action "add a bookmark", not the object "a bookmark", hence it should be translated as a verb, and reading the source code and the appearance info gives you clarity over its usage.
Give both labels of a toggle (e.g. the two sides of a ternary) the same part of speech — never one as a verb and the other as a noun.
Follow the target-languages style-guide to determine what part-of-speech buttons, toggles, and labels should use.

**Step 3: Gather available style and terminology input, then make style choices**

Read and consider guidance from the following:
- Explicit guidance in your instructions
- Existing translations for the target locale
- The locale-specific style guide

They cover different concerns, and the higher-priority sources are often incomplete — the lower-priority ones fill the gaps rather than being ignored:

1. **Explicit guidance in your instructions.** Any terminology or style direction in the instructions you were given (how to translate a specific term, the app name, tone guidance, DNT list, etc.) is authoritative — follow it above all else.
2. **Existing translations for the target locale.** Match their terminology, phrasing, register, tone, etc. so the app's translations stay consistent. These reflect choices already made for this project and take precedence over the style guide.
3. **The locale-specific style guide.** Always read `references/styleguide_{locale}.md` (resolve it relative to the skill's base directory) when one exists for the target locale (e.g. `styleguide_pt-BR.md`, `styleguide_zh-Hans.md`—if the file doesn't exist, there isn't a style guide for that locale). Use it to inform your choices when specific guidance doesn't exist in your instructions or existing translations.

When these sources conflict, higher-priority items win: explicit instructions override existing translations, which override the style guide. Where none of them settles a question, default to informal/colloquial style.

**Step 4: Formulate translation**
Consider:
- **Terminology**: Match terms used in similar strings. If "Save" is translated as "Speichern" elsewhere, use it consistently. No matter the similar strings, make sure the part of speech of your target string is preserved: a noun sibling ("Bookmarks") is not a precedent for an action button that shares its stem ("Bookmark") — reuse the term, keep the part of speech the usage calls for.
- **Tone and formality**: Decide on the style of your translation based on your choices in step 3
- **App names**: Once you decide on how to translate an app name, make sure to to stick to this decision everywhere the app name is referenced.
- **Format specifiers**: Understand what each specifier represents by reading the source code (e.g., `%lld` might be a count of items, files, or users).

**Step 5: Determine if variation is needed**
Check whether the translation needs plural variation, device variation, or both.

- **Plural**: If the string contains a numeric format specifier (`%lld`, `%d`, `%u`, etc.) paired with a countable noun, read [references/plural-variations.md](./references/plural-variations.md) (resolve it relative to the skill's base directory). The context tool provides `relevantPluralCases` for your target locale—use all of them.
    - If the context tool also returned `sourcePluralCasesToAdd`, the source itself isn't plural-varied yet. Vary the source first in a separate `StringCatalogEdit` call before translating the target — [references/plural-variations.md](./references/plural-variations.md) walks through this two-step flow.
    - If the count arrives pre-formatted in a non-numerical specifier (`%@`), plural variation cannot apply at all. [references/plural-variations.md](./references/plural-variations.md) covers how to restructure instead, and requires you to report the key back as needing a numerical placeholder.
- **Device**: If the string references a device-specific interaction (tap vs. click) or mentions a device by name, read [references/device-variations.md](./references/device-variations.md) (resolve it relative to the skill's base directory)
- **Both**: A string can need both — for example, "Tap to launch %lld spaceships" differs by device AND has a countable noun. Combine device and plural keys (e.g., `device.iphone.plural.one`), but keep `device.other` as a flat fallback string that covers both variations

**Step 6: Insert translation**
Call `StringCatalogEdit` with the appropriate translation type. Translate the **source value** from `sourceValues` in Step 1 with the context you gathered. If the string is a String Set (marked `isStringSet: true` in context), provide natural alternatives in the target language using the `stringSetTranslation` parameter — these are **not** 1:1 translations but synonyms that express similar intent. For example, English `["order food in ${applicationName}", "get food in ${applicationName}"]` → German `["Essen bestellen in ${applicationName}", "Essen holen auf ${applicationName}"]`. Continue to the next string.

**Repeat these 6 steps until all requested strings are translated.**

Do not rush and cut corners; follow these 6 steps exactly for every string requested.

**When you are finished**, list any string you had to work around rather than translate properly. A workaround nobody hears about is a workaround nobody fixes.


# Tool Reference
## StringCatalogContext

Returns context and the source language value for a given string. The `sourceValues` field contains the text that must be translated. Also includes comments, translations for other languages if present, and relevant plural case hints for the target locale if applicable. Curly apostrophes and quotes are escaped (e.g., \\u2019 for curly apostrophe, \\u201C for curly quote).

### Inputs

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `tabIdentifier` | String | Yes | Workspace tab identifier |
| `filePath` | String | Yes | Path to String Catalog |
| `stringKey` | String | Yes | String key to get context for |
| `targetLocaleIdentifier` | String | Yes | Locale for translation (e.g., `de`, `pt-PT`) |

### Outputs

| Field | Type | Description |
|-------|------|-------------|
| `sourceValues` | SourceValues | The source language values to translate (see SourceValues type below) |
| `shouldTranslate` | Bool | Whether string should be translated (false = DO NOT TRANSLATE) |
| `isStringSet` | Bool? | Whether this is a String Set (only present when true) |
| `comment` | String? | Developer comment from String Catalog |
| `relevantPluralCases` | [String]? | Plural cases for target locale (e.g., `["plural.one", "plural.other"]`). Absent when the string doesn't require pluralization. |
| `sourcePluralCasesToAdd` | [String]? | Plural cases for the source locale. Present when the source string has a numerical format specifier but is not yet plural-varied. Absent when the source string doesn't require pluralization. |
| `translations` | [LocalizationInfo] | All existing translations across non-source locales |
| `usageLocations` | [UsageLocation]? | Source code locations where string is used |
| `appearances` | [AppearanceInfo]? | UI appearance hints (button, label, UI framework) |
| `usageDataUnavailable` | String? | Message when usage data can't be retrieved (e.g., "Build the project...") |
| `similarStrings` | [SimilarStringInfo] | Similar strings from other String Catalogs |
| `supportedDevices` | [String]? | Devices this app builds for (e.g., `["device.iphone", "device.mac"]`). Only present when the app targets multiple device families. |

### Output Types

#### LocalizationInfo

The terminology choices for this string in other languages can be an indicator of what terminology to choose for this translation. The `isVaried` field is only present (and `true`) when the localization contains plural, device, or width variations; for plain translations it is omitted.

```json
{
  "localeIdentifier": "de",
  "value": "Willkommen!"
}
```

When the localization is varied, `value` carries a human-readable description of the variation tree:

```json
{
  "localeIdentifier": "he",
  "value": "plural.one: ...\nplural.other: ...",
  "isVaried": true
}
```

#### UsageLocation

Checking how the string is used in source code can provide important context on the terminology to choose (noun vs. verb, etc.)

```json
{
  "fileURL": "file:///path/to/File.swift",
  "lineNumber": 42,
  "columnNumber": 15
}
```

#### AppearanceInfo

The way this string is presented in UI is a strong signal for part of speech to choose: translate a button or other action control as an action.

```json
{
  "usageHint": "This string is used in a SwiftUI button"
}
```

#### SimilarStringInfo

Ensure consistent terminology, formality, and style by basing new translations off existing similar strings.

```json
{
  "key": "save_button",
  "sourceDescription": "Save",
  "targetDescription": "Speichern"
}
```

#### SourceValues

The source language values that must be translated. Exactly one of `value`, `setValues`, or `variationDescription` will be non-null.

| Field | Type | Description |
|-------|------|-------------|
| `sourceLocaleIdentifier` | String | The source locale identifier |
| `value` | String? | Source text for simple strings |
| `setValues` | [String]? | Source values for string sets |
| `variationDescription` | String? | Variation tree for varied strings |

---

## StringCatalogEdit

Inserts or updates a translation in a String Catalog. Can handle simple strings, varied strings, and String Sets. If the string needs variation (e.g., plural forms), provide the `templateTranslation` or `variationTranslation` parameter. For String Sets (voice assistant commands), use `stringSetTranslation`. Prefer typographically correct quotes for the target language (e.g., „...“ for German, «...» for French). All curly quotes must be escaped (e.g., \\u201E...\\u201C for German „...“).

**Critical:** Translations must be in the correct target locale. Refer to your initial instructions to determine which locale applies. Do not infer a locale from examples in this document.

### Inputs

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `tabIdentifier` | String | Yes | Workspace tab identifier |
| `filePath` | String | Yes | Path to String Catalog |
| `stringKey` | String | Yes | String key to translate |
| `targetLocaleIdentifier` | String | Yes | Target locale (e.g., `de`, `pt-PT`) |

**Plus exactly one of the following (mutually exclusive):**

| Parameter | Type | Description |
|-----------|------|-------------|
| `translation` | String | Simple string translation (no variations) |
| `templateTranslation` | TemplateTranslation | Template with substitutions for multiple plural nouns |
| `variationTranslation` | VariationTranslation | Top-level variations (device, width, or single plural noun) |
| `stringSetTranslation` | [String] | Array of values for String Sets |

### Translation Types

#### Simple Translation

For strings without variations:

```json
{
  "stringKey": "welcome_message",
  "targetLocaleIdentifier": "de",
  "translation": "Willkommen in unserer App!"
}
```

#### Template Translation

For strings with multiple format specifiers + countable nouns:

```json
{
  "stringKey": "usage_message",
  "targetLocaleIdentifier": "de",
  "templateTranslation": {
    "template": "iCloud+ wird von %#@arg1@ und %#@arg2@ verwendet.",
    "substitutions": [
      {
        "name": "arg1",
        "argNum": 1,
        "formatSpecifier": "lu",
        "variants": {
          "plural.one": "%arg Gerät",
          "plural.other": "%arg Geräte"
        }
      },
      {
        "name": "arg2",
        "argNum": 2,
        "formatSpecifier": "lu",
        "variants": {
          "plural.one": "%arg Mitglied",
          "plural.other": "%arg Mitglieder"
        }
      }
    ]
  }
}
```

#### Variation Translation

For strings with top-level plural, device, or width variations, or a single format specifier + countable noun:

**Single plural noun:**

```json
{
  "stringKey": "item_count",
  "targetLocaleIdentifier": "pl",
  "variationTranslation": {
    "topLevelVariation": {
      "plural.one": "Masz %lld przedmiot",
      "plural.few": "Masz %lld przedmioty",
      "plural.many": "Masz %lld przedmiotów",
      "plural.other": "Masz %lld przedmiotu"
    }
  }
}
```

**Device-only variations (no plurals):**

```json
{
  "stringKey": "action_hint",
  "targetLocaleIdentifier": "es",
  "variationTranslation": {
    "topLevelVariation": {
      "device.iphone": "Toca aquí",
      "device.mac": "Haz clic aquí",
      "device.other": "Pulsa aquí"
    }
  }
}
```

**Device variations with single plural noun:**

```json
{
  "stringKey": "launch_button",
  "targetLocaleIdentifier": "fr",
  "variationTranslation": {
    "topLevelVariation": {
      "device.iphone.plural.one": "Touchez pour lancer %lld vaisseau spatial",
      "device.iphone.plural.other": "Touchez pour lancer %lld vaisseaux spatiaux",
      "device.mac.plural.one": "Cliquez pour lancer %lld vaisseau spatial",
      "device.mac.plural.other": "Cliquez pour lancer %lld vaisseaux spatiaux",
      "device.other": "Touchez pour lancer %lld vaisseaux spatiaux"
    }
  }
}
```

**Device variations with substitutions (multiple plural nouns):**

```json
{
  "stringKey": "device_usage",
  "targetLocaleIdentifier": "de",
  "variationTranslation": {
    "topLevelVariation": {
      "device.iphone": "iCloud+ wird von %#@arg1_iphone@ und %#@users@ verwendet",
      "device.mac": "iCloud+ wird von %#@arg1_mac@ und %#@users@ verwendet",
      "device.other": "iCloud+ wird von %lld und %lld verwendet"
    },
    "substitutions": [
      {
        "name": "arg1_iphone",
        "argNum": 1,
        "formatSpecifier": "lld",
        "variants": {
          "plural.one": "%arg anderes iPhone",
          "plural.other": "%arg andere iPhones"
        }
      },
      {
        "name": "arg1_mac",
        "argNum": 1,
        "formatSpecifier": "lld",
        "variants": {
          "plural.one": "%arg anderer Mac",
          "plural.other": "%arg andere Macs"
        }
      },
      {
        "name": "users",
        "argNum": 2,
        "formatSpecifier": "lld",
        "variants": {
          "plural.one": "%arg Benutzer",
          "plural.other": "%arg Benutzer"
        }
      }
    ]
  }
}
```

**Critical**: See [plural-variations.md](./references/plural-variations.md) for detailed rules.

**Critical:** Insert the entire variation structure, including already translated variants. This overwrites what was there before.

#### String Set Translation

For String Sets (voice assistant commands):

```json
{
  "stringKey": "COMMAND_ORDER",
  "targetLocaleIdentifier": "de",
  "stringSetTranslation": ["Essen bestellen", "Essen holen", "Essen kaufen"]
}
```

Note: provide synonyms/alternatives, not direct 1:1 translations.

### Type Definitions

**TemplateTranslation:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `template` | String | Yes | Template with `%#@name@` substitution references |
| `substitutions` | [Substitution] | Yes | Array of substitution definitions |

**VariationTranslation:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `topLevelVariation` | {String: String} | Yes | Maps variation paths to templates (e.g., `"plural.one"`, `"device.iphone"`) |
| `substitutions` | [Substitution]? | No | Optional substitutions referenced by templates |

**Substitution:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | String | Yes | Placeholder name (used as `%#@name@` in template) |
| `argNum` | Int | Yes | 1-indexed argument position |
| `formatSpecifier` | String | Yes | Format type without % (e.g., `lld`, `@`, `u`) |
| `variants` | {String: String} | Yes | Maps variation paths to values (use `%arg` as number placeholder) |

### Outputs

| Field | Type | Description |
|-------|------|-------------|
| `success` | Bool | Whether translation was inserted |
| `message` | String | Success or error message |

---


## StringCatalogRead

This tool should only be used to verify your work.

Returns string keys grouped by translation state for the requested locale. Includes counts of all string keys grouped by translation state. Supports pagination. Curly apostrophes and quotes are escaped (e.g., \\u2019 for curly apostrophe, \\u201C for curly quote).

### Inputs

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `tabIdentifier` | String | Yes | — | Workspace tab identifier |
| `filePath` | String | Yes | — | Path to String Catalog (relative or absolute) |
| `targetLocaleIdentifier` | String | Yes | — | Locale to check translations for (e.g., `de`, `pt-PT`) |
| `requestedState` | String? | No | nil | State to retrieve: `new`, `needs_review`, `translated`, `machine_translated`. If omitted, only counts for all states are returned. |
| `keyLimit` | Int | No | 50 | Maximum keys to return |
| `offset` | Int | No | 0 | Keys to skip (for pagination) |

### Outputs

**Always returned:**

| Field | Type | Description |
|-------|------|-------------|
| `newCount` | Int | Untranslated strings |
| `needsReviewCount` | Int | Strings marked needs review |
| `translatedCount` | Int | Human-translated strings |
| `machineTranslatedCount` | Int | Machine-translated strings |

**When `requestedState` is provided:**

| Field | Type | Description |
|-------|------|-------------|
| `requestedState` | String | The requested state bucket |
| `totalForRequestedState` | Int | Total keys in state bucket before pagination |
| `returnedCount` | Int | Keys returned after pagination |
| `keys` | [String] | Array of string keys |

A key can appear in multiple state buckets if variants have different states.

---

# Critical Rules

1. **Use only String Catalog tools** to access .xcstrings files. Never write to them directly.
2. **Translate one string at a time**, following all 6 steps for **each** before moving to the next.
3. **Preserve format specifiers exactly** as they appear in source (`%1$lld`, `%@`, etc.).
4. **Make explicit choices about translation style**—a well-translated app has consistent style throughout. Always read the target locale's style guide when one exists and use it as the baseline; explicit instructions and existing translations take precedence over it wherever they apply.
5. **Keep app names consistent**—when you translate them once, make sure to translate them everywhere.
6. **Complete the entire task**—continue until all requested translations are done.
7. **Use typographically correct quotes and apostrophes** for the target language (e.g., „...“ for German, «...» for French). All curly quotes must be escaped (e.g., \\u201E...\\u201C for German „...“), as well as apostrophes (e.g. \\u2019 for curly apostrophe). NEVER XML-escape the ampersand: write a literal `&`, NOT `&amp;`. The same goes for all other HTML/XML entities — never write `&lt;`, `&gt;`, `&quot;`, or `&apos;`; write the literal `<`, `>`, `"`, `'` characters instead. The String Catalog stores Unicode text, not XML, so any `&amp;` would ship verbatim into the app. Other non-ascii characters do not need extra escaping either. DO NOT blindly escape everything.
8. Do NOT skip steps to save time, even when there are hundreds of strings. Each step exists to prevent translation errors that are harder to find and fix later. This process takes time, and that's ok. Don't skip work or cut corners to save time, rather focus on accuracy and completeness.
9. **Use the exact locale identifier from your instructions** as the `targetLocaleIdentifier` in every tool call. Do NOT normalize, canonicalize, or expand it (e.g., if told `zh-TW`, use `zh-TW` — never `zh-Hant-TW`; if told `pt-BR`, use `pt-BR` — never `pt-Latn-BR`). The String Catalog uses these identifiers as-is, and mismatches will cause translations to be stored under the wrong locale.


### Example

For each string key:

1. Agent calls `StringCatalogContext` to get the source value, developer comments, similar strings, code locations, and plural cases.
2. Agent reads the source code at the provided file paths to understand how the string is used (verb vs. noun, button vs. label).
3. Agent reads the locale style guide (when one exists for the target locale), reviews existing translations for terminology and tone, and notes any explicit guidance in its instructions — then applies them with explicit instructions taking precedence over existing translations, and existing translations over the style guide.
4. Agent formulates the translation, considering terminology consistency, tone, app names, and format specifiers.
5. Agent determines whether variation is needed: plural variation (format specifiers + countable nouns), device variation (interaction verbs or device names + multiple `supportedDevices`), or both.
6. Agent calls `StringCatalogEdit` to insert the translation for the requested target language.
