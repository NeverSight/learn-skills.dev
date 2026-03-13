---
name: deepl-cli
description: |
  Translate text using the DeepL API via the deepl-cli command-line tool. Use when the user asks to:
  translate text, translate to another language, use DeepL, translate with formality control, or
  pipe text through a translation. Supports all DeepL language pairs, source language auto-detection,
  context-aware translation, and formality levels (formal/informal).
license: MIT
metadata:
  author: daliusd
  version: "0.1.0"
---

# deepl-cli

CLI tool for translating text using the DeepL API. Pipe-friendly, supports context and formality options.

## Prerequisites

- Node.js >= 18
- A DeepL API key ([free tier: 500,000 characters/month](https://www.deepl.com/pro#developer))

## Installation

```bash
npm install -g @daliusd/deepl-cli
```

## Configuration

Create `~/.config/deepl-cli/config.json`:

```bash
mkdir -p ~/.config/deepl-cli
```

**Option A -- Static API key:**

```json
{
  "api_key": "your-deepl-api-key"
}
```

**Option B -- Command-based key** (for password managers like `pass`, 1Password CLI, etc.):

```json
{
  "api_key_command": "pass show deepl-api-key"
}
```

If both are present, `api_key_command` takes precedence.

## Commands

All translation is done via a single command:

```
deepl-cli [options] [text]
```

### Basic Translation

```bash
deepl-cli -t de "Hello, world!"
```

### Specify Source Language

```bash
deepl-cli -t de -s en "Hello"
```

By default the source language is auto-detected. Use `-s` only when auto-detection is insufficient.

### Context-Aware Translation

Context influences the translation but is not itself translated or billed:

```bash
deepl-cli -t de -c "This is a greeting in a formal business email" "Hello"
```

### Formality Control

```bash
# Formal
deepl-cli -t de -f more "How are you?"

# Informal
deepl-cli -t de -f less "How are you?"
```

Valid formality values: `less`, `more`, `default`, `prefer_less`, `prefer_more`.

### Piped Input

```bash
echo "Hello, world!" | deepl-cli -t de
```

Translated text goes to stdout with no extra formatting, making it pipeline-friendly:

```bash
echo "Hello" | deepl-cli -t de | pbcopy
```

### Verbose Mode

Metadata is written to stderr so stdout remains clean:

```bash
deepl-cli -t de -v "Hello, world!"
# stdout: Hallo, Welt!
# stderr: Detected source language: en
# stderr: Billed characters: 13
```

## Options Reference

| Option | Short | Description |
|--------|-------|-------------|
| `--target <lang>` | `-t` | Target language code (**required**, e.g. `de`, `en-US`, `fr`) |
| `--source <lang>` | `-s` | Source language code (default: auto-detect) |
| `--context <text>` | `-c` | Additional context for translation (not translated, not billed) |
| `--formality <level>` | `-f` | Formality: `less`, `more`, `default`, `prefer_less`, `prefer_more` |
| `--verbose` | `-v` | Show metadata (detected source language, billed characters) |
| `--help` | `-h` | Show help |
| `--version` | | Show version |

## Common Language Codes

Language codes are case-insensitive and follow ISO 639-1.

**Source languages** (or omit for auto-detection):

| Code | Language |
|------|----------|
| `en` | English |
| `de` | German |
| `fr` | French |
| `es` | Spanish |
| `it` | Italian |
| `ja` | Japanese |
| `zh` | Chinese |
| `pl` | Polish |
| `nl` | Dutch |
| `pt` | Portuguese |
| `ru` | Russian |

**Target languages** (some include regional variants):

| Code | Language |
|------|----------|
| `en-US` | English (American) |
| `en-GB` | English (British) |
| `de` | German |
| `fr` | French |
| `es` | Spanish |
| `it` | Italian |
| `ja` | Japanese |
| `zh-Hans` | Chinese (Simplified) |
| `zh-Hant` | Chinese (Traditional) |
| `pl` | Polish |
| `nl` | Dutch |
| `pt-BR` | Portuguese (Brazilian) |
| `pt-PT` | Portuguese (European) |
| `ru` | Russian |

See the [DeepL API documentation](https://www.deepl.com/docs-api/translating-text/) for the full list.

## Tips

- **No arguments** or `--help` shows usage information.
- **Multiple words** as positional arguments are joined with a space: `deepl-cli -t de Hello world` translates "Hello world".
- **Verbose mode** writes metadata to stderr, so piping stdout is always safe.
- **`api_key_command`** is recommended over `api_key` to avoid storing secrets in plain text.
