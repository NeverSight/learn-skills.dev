---
name: nuxt-docs
description: Fetches Nuxt 4 framework documentation from GitHub. Use when needing info about Nuxt composables (useFetch, useAsyncData), directory structure, configuration, routing, data fetching, deployment, or any Nuxt framework concepts.
allowed-tools: Bash, Read
---

# Nuxt 4 Documentation Skill

Fetches up-to-date Nuxt framework docs from the official GitHub repository.

## Categories

| Category | Topics |
|----------|--------|
| `getting-started` | installation, config, routing, data-fetching, deployment |
| `api/composables` | useFetch, useAsyncData, useState, useRoute, etc. |
| `api/components` | NuxtPage, NuxtLayout, NuxtLink, ClientOnly, etc. |
| `api/utils` | $fetch, defineNuxtConfig, definePageMeta, etc. |
| `directory-structure` | app/, server/, composables/, pages/, etc. |
| `guide` | concepts, best practices, recipes |

## Usage

### Fetch a specific topic

```bash
python3 .claude/skills/nuxt-docs/fetch.py data-fetching
python3 .claude/skills/nuxt-docs/fetch.py useFetch
python3 .claude/skills/nuxt-docs/fetch.py routing
```

### List available topics

```bash
python3 .claude/skills/nuxt-docs/fetch.py --list
```

### Check cache status

```bash
python3 .claude/skills/nuxt-docs/fetch.py --status
```

## When to Use

- "How do I use useFetch?"
- "What's the Nuxt 4 directory structure?"
- "How do I configure nuxt.config.ts?"
- "How does server-side rendering work?"
- "How do I deploy a Nuxt app?"
