---
description: "Coordinates translation of an Xcode project or its String Catalogs (.xcstrings) into other languages. This is the main skill to activate when asked to work on translating strings, adding languages or working with .xcstrings files. Handles the full workflow: preparing the project for a new language, fetching untranslated strings, delegating translation work, and verifying results."
displayName: "Coordinate Translation"
sfSymbolName: globe
user-invocable: false
name: translation-coordinator
---
# Localization Coordinator

Orchestrate the translation of an Xcode project by preparing it, fetching untranslated strings, and delegating translation work to sub-agents. Access String Catalogs **only** through the tools below—never write .xcstrings files directly.
Never translate strings directly. Instead, fetch the context that sub-agents need to succeed as translators.

## Quick Reference

| Tool | Purpose |
|------|---------|
| `LocalizationPlanner` | Prepare project for new language (creates String Catalogs, adds locale) or other localization changes |
| `StringCatalogRead` | Get string keys by translation state (new, needs_review, translated, machine_translated) |

## Workflow

### 1. Prepare the Project (Optional)

Call `LocalizationPlanner` first when adding a new language to a project. Skip if the user instructs you to, or if the user only requested translation of a few specific strings.

If the tool's `nextStep` output says to build the project, build the project—only building extracts strings from code into newly created String Catalogs.

### 2. Select Relevant String Catalogs

Identify all String Catalogs relevant to the user's request. If the user's request is very broad, all catalogs may be relevant.

### 3. Get Strings to Translate

If the prompt already contains per-locale key lists, skip this step, as you have already been given the keys and languages to translate.
Otherwise, call `StringCatalogRead` with the file path, target locale, and `requestedState: "new"` to get untranslated strings. You can also request `"needs_review"` or `"machine_translated"` states to improve existing translations.

If `totalForRequestedState` exceeds the number of returned keys, paginate by increasing `offset` until you have collected all keys. Collect all keys before moving to step 4.

The keys are unique identifiers to strings in this String Catalog. Use them exactly as returned by this tool in any operations or operations in sub-agents that you conduct.

### 4. Delegate Translations

Split the fetched strings into batches and delegate each batch to a sub-agent.

1. Split the strings you fetched from `StringCatalogRead` into batches of up to 15 strings each. Smaller batches produce better translations because sub-agents can dedicate more attention to context and terminology per string.
2. Create sub-agents for each batch. You **MUST** tell each sub-agent to use the `xcode-integration:translation` skill to translate their batch. Tell them to skip the `LocalizationPlanner` tool—you ran it for them.
3. **Limit concurrency to 5 sub-agents at a time.** Launch at most 5 sub-agents in parallel, then wait for all of them to complete before launching the next group of up to 5. This prevents overloading the system with too many concurrent translation tasks.
4. Use the keys exactly as returned by the StringCatalogRead tool, and tell each agent to use them verbatim (including any escaping).
5. **Instruct each sub-agent to invoke the `xcode-integration:translation` Skill, and provide the target locale, the tab identifier, the String Catalog path, and the key list to them.** See the examples below for the exact format.
6. Forward the user's request, terminology and style choices to sub-agents (they don't have access to the user's original prompt, you have to forward it to them). State that any guidance you include takes precedence over the style guide, and that the sub-agent must still read the style guide as the baseline for anything your guidance and existing translations don't cover.


If you have any string keys that represent an app name (e.g. `CFBundleDisplayName`, `CFBundleName`), make sure to put them at the top of the first batch to translate. This way subsequent translations can reuse chosen terminology.

### 5. Verify Results

Once all sub-agents have completed their tasks, use the `StringCatalogRead` tool to verify the strings you requested to translate are translated.

Collect anything the sub-agents flagged as needing a code change. Pass these to the user with the key and the catalog, so the call site can be fixed.


# Tool Reference

## LocalizationPlanner

Prepares an Xcode project for localization. **Call this each time you are tasked with adding a language** to the project, or to translate an entire project or feature. It is ok to skip this tool if requested explicitly.

### What It Does

1. Adds target language to all localizable containers (projects, packages)
2. Prepares the project for translation by creating String Catalogs as necessary

### Inputs

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `tabIdentifier` | String | Yes | Workspace tab identifier |
| `targetLocaleIdentifier` | String | Yes | Locale identifier (e.g., `de`, `pt-PT`) |

### Outputs

| Field | Type | Description |
|-------|------|-------------|
| `nextStep` | String | What to do next (e.g. "ready for translation") |
| `stepsFailed` | String? | Failed steps requiring manual intervention |
| `changesMade` | String? | List of changes successfully made |
| `suggestions` | String? | Non-blocking suggestions the user may want to follow (e.g., migrate `.strings` to String Catalogs) |
| `stringCatalogPaths` | [String] | Absolute paths to all String Catalogs in workspace |

Follow the instructions in the `nextStep` field.

---

## StringCatalogRead

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

1. **Always delegate translation work to sub-agents**. Never write a translation yourself.
2. **Use only String Catalog tools** to access .xcstrings files. Never read or write them directly.
3. **Complete the entire task**—continue until all requested strings are translated.
4. **Use typographically correct quotes and apostrophes** for the target language (e.g., „...“ for German, «...» for French). All curly quotes must be escaped (e.g., \\u201E...\\u201C for German „...“), as well as apostrophes (e.g. \\u2019 for curly apostrophe). NEVER XML-escape the ampersand: write a literal `&`, NOT `&amp;`. The same goes for all other HTML/XML entities — never write `&lt;`, `&gt;`, `&quot;`, or `&apos;`; write the literal `<`, `>`, `"`, `'` characters instead. The String Catalog stores Unicode text, not XML, so any `&amp;` would ship verbatim into the app. Other non-ascii characters do not need extra escaping either. 
5. Do NOT skip strings to save time, even when there are hundreds of strings. Don't skip work or cut corners to save time—rather, focus on accuracy and completeness.
6. Forward keys into sub-agents **exactly** as you have received them from the StringCatalogRead tool. Escaped strings with \\uXXXX sequences might lose one level of escaping during transit. Keep them double-escaped them so the sub-agent receives the original form.
7. **Locale identifiers:** If the user provides an explicit locale code, pass it through verbatim to tool calls and to sub-agents — do not normalize, canonicalize, or swap separators (e.g., if told `pt_BR`, use `pt_BR`; if told `zh-TW`, use `zh-TW`). If the user only names a language/region in prose (e.g., "Brazilian Portuguese", "Traditional Chinese"), derive a BCP 47 identifier with hyphens (`pt-BR`, `zh-Hant`) rather than underscores. The explicit-code rule always wins over the BCP 47 default.

### Examples

#### Entire Project

1. User requests translating the project into Japanese
2. Agent calls `LocalizationPlanner` tool. Once completed, the project is ready for localization.
3. Agent reviews the returned String Catalog paths and selects only those relevant to the user's request.
4. Agent uses `StringCatalogRead` on the relevant String Catalogs to understand what string keys need translating.
5. Agent divides work among subagents, prompting each subagents with the following:

============
Translate the strings for the following keys into Japanese (ja). Skip running the `LocalizationPlanner` tool. Do NOT spawn further sub-agents. Translate only the keys listed below. Use the `xcode-integration:translation` Skill.

IMPORTANT: Use the keys EXACTLY as written below, including all escaping. You must preserve this escaping exactly when passing the key to StringCatalogContext and StringCatalogEdit.

- Tab identifier: <tabIdentifier>
- String Catalog: path/to/string/catalog.xcstrings
- Keys:

```
key1
```

```
key2
```

```
key3
```
============

6. Once all sub-agents have completed, agent uses `StringCatalogRead` to verify that each requested string has received a translation.

#### Specific Strings

1. User requests translation of specific strings in a specific String Catalog into Japanese.
2. Agent skips `LocalizationPlanner` and `StringCatalogRead` since the user already specified which strings to translate.
3. Agent divides work among sub-agents, prompting each with the following: 

============
Translate the strings for the following keys into Japanese (ja). Skip running the `LocalizationPlanner` tool. Do NOT spawn further sub-agents. Translate only the keys listed below. Use the `xcode-integration:translation` Skill.

IMPORTANT: Use the keys EXACTLY as written below, including all escaping. You must preserve this escaping exactly when passing the key to StringCatalogContext and StringCatalogEdit.

- Tab identifier: <tabIdentifier>
- String Catalog: path/to/string/catalog.xcstrings
- Keys:

```
key1
```

```
key2
```

```
key3
```
============

4. Once all sub-agents have completed, agent uses `StringCatalogRead` to verify that each requested string has received a translation.
