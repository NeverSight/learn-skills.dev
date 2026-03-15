---
name: translate
description: "Translate text between languages. Use this skill when the user asks to translate text, convert text to another language, say something in another language, or get a translation. Supports 100+ languages with no API key required."
tags: [translate, translation, language, i18n, multilingual, utility]
version: 0.1.0
---

# Skill: translate

## When to Use

Use this skill when the user asks to:

- Translate text to/from another language
- Say something in a different language
- Convert text between languages
- Get a translation of a phrase or document
- Detect the language of text

## Input Parameters

| Parameter | Required | Description                                | Example             |
| --------- | -------- | ------------------------------------------ | ------------------- |
| `text`    | Yes      | The text to translate                      | Hello, how are you? |
| `to`      | Yes      | Target language code or name               | es, french, zh      |
| `from`    | No       | Source language (auto-detected if omitted) | en                  |

## Common Language Codes

| Code | Language   | Code | Language |
| ---- | ---------- | ---- | -------- |
| `en` | English    | `fr` | French   |
| `es` | Spanish    | `de` | German   |
| `pt` | Portuguese | `it` | Italian  |
| `zh` | Chinese    | `ja` | Japanese |
| `ko` | Korean     | `ar` | Arabic   |
| `ru` | Russian    | `hi` | Hindi    |
| `nl` | Dutch      | `sv` | Swedish  |

## Procedure

1. Extract the text and target language from the user's request
2. Run the bundled script:
   ```bash
   python3 skills/translate/scripts/translate.py "Hello, how are you?" --to es
   ```
   With source language:
   ```bash
   python3 skills/translate/scripts/translate.py "Bonjour" --from fr --to en
   ```
3. The script auto-installs `deep-translator` if needed
4. Report the translation to the user

## Bundled Scripts

| Script                 | Type   | Description                      |
| ---------------------- | ------ | -------------------------------- |
| `scripts/translate.py` | Python | Translate text between languages |

### Script Usage

```bash
# Translate to Spanish (auto-detect source)
python3 scripts/translate.py "Hello, how are you?" --to es

# Translate from French to English
python3 scripts/translate.py "Bonjour le monde" --from fr --to en

# Translate to Japanese
python3 scripts/translate.py "Good morning" --to ja
```

## Example

```
translate "hello world" to spanish
how do you say "thank you" in japanese
translate this to french: "the meeting is at 3pm"
what does "bonjour" mean in english
```
