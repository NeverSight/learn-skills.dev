---
name: 4d-find-command
description: Find 4D commands by keyword. Use this skill when the user wants to search for, find, or discover 4D commands matching a term. Searches the gram.4dsyntax file from tool4d.app to list all matching command names. Filters out deprecated commands.
license: Apache 2.0
---

# 4D Command Finder

Search for 4D commands by keyword.

## Prerequisites

Requires tool4d to access the `gram.4dsyntax` file:
- Install [4D-Analyzer extension](https://marketplace.visualstudio.com/items?itemName=4D.4d-analyzer) in VS Code/Antigravity, OR
- Set `TOOL4D` environment variable to point to tool4d executable

## Usage

```bash
scripts/find_command.sh <search_term> [--verbose]
```

## Options

- `--verbose` or `-v`: Add category for each command

## Examples

```bash
# Simple search
scripts/find_command.sh json

# Verbose output with types
scripts/find_command.sh json --verbose
```

## Output

Simple mode (signature only):
```
JSON Parse(Text) -> Expression
JSON Stringify(Expression, Text?) -> Text
JSON Validate(Text, Object?) -> Object
```

Verbose mode (adds category):
```
JSON Parse(Text) -> Expression [JSON]
JSON Stringify(Expression, Text?) -> Text [JSON]
JSON Validate(Text, Object?) -> Object [JSON]
```

Parameters marked with `?` are optional.
