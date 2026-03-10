---
name: cot-cli
description: Helps users use cot_cli to /list/add/remove plugins.
---

# Cot CLI

This skill helps you use the `cot` to manage plugins.

## When to Use This Skill

Use this skill when the user:

- list all plugins
- wants to install a plugin
- wants to remove a plugin
- wants to activate a plugin
- find where huggingface models are stored
- find where modelscope models are stored
- find cpu/os information
- unzip a file of .zip/.tar.gz/.tar.zst format

## What is the Cot CLI?

The Cot CLI (`cot`) is Cross OS Toolkit for developers.

**Key commands:**

- `cot ls` - List all plugins
- `cot install <package>` - Install a plugin from a file
- `cot rm <package>` - Remove a plugin
- `cot activate <package>` - Activate a plugin
- `cot info` - Show CPU and OS information
- `cot unzip <file>` - Unzip a file of .zip format
- `cot xf <file>` - Unzip a file of .tar.gz or .tar.zst format
- `cot hf` - Show where huggingface models are stored
- `cot md` - Show where modelscope models are stored
- `cot help` - Show help information

## Example Usage
**List all plugins:**

```bash
cot ls
```
**Install a plugin:**

```bash
cot install my_plugin.zip
```