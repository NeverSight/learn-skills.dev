---
name: make-site-multilingual
description: >-
  Get a site ready for Rosey translation, with the CloudCannon connector (RCC)
  as an optional visual-editing layer. Use when the user wants to add
  multilingual support, internationalize a site, set up Rosey, replace an
  existing i18n system (astro-i18n, next-intl, path-based routing, etc.), or
  upgrade from RCC v1 to v2.
---

# Get a Site Ready for Rosey (+ the RCC)

Step-by-step workflow for making a single-language site translatable with **Rosey**, and — optionally — wiring up the **Rosey CloudCannon Connector (RCC)** so editors can translate inline in CloudCannon's Visual Editor.

## When to use

- A single-language site needs to become translatable — the main workflow, [setup.md](setup.md)
- The site already has an i18n system (astro-i18n, next-intl, dictionaries + `t()`) that should be replaced with Rosey — [migrating-from-i18n.md](migrating-from-i18n.md)
- The site runs RCC v1 and should move to v2 — [rcc-v1-to-v2-upgrade.md](rcc-v1-to-v2-upgrade.md)
- A Rosey-ready site needs the CloudCannon inline-translation layer added — [setup.md § Phase 5](setup.md#phase-5-add-the-rcc--cloudcannon-layer-optional)

## When not to use

- **Filling in translations** on a site that is already Rosey-ready — that's [`translate-site`](../translate-site/SKILL.md)
- **General CloudCannon configuration** unrelated to locales — that's [`cloudcannon-configuration`](../cloudcannon-configuration/SKILL.md)
- **Setting up editable regions themselves** — that's [`cloudcannon-visual-editing`](../cloudcannon-visual-editing/SKILL.md). This skill covers only where `data-rosey` and regions interact.

## Contents

| File                                                       | Covers                                                                      |
| ---------------------------------------------------------- | --------------------------------------------------------------------------- |
| **SKILL.md** (this file)                                   | When this skill applies, the two layers, starting point, SSG detection      |
| [setup.md](setup.md)                                       | **The main workflow** — nine phases, audit through locale picker, checklist |
| [tagging.md](tagging.md)                                   | **Phase 3 in full** — every `data-rosey` / `-ns` / `-root` authoring rule   |
| [gotchas.md](gotchas.md)                                   | Preventative one-line rules, framework-agnostic and SSG-specific            |
| [troubleshooting.md](troubleshooting.md)                   | Symptom → cause → fix for things that build cleanly and translate wrongly   |
| [migrating-from-i18n.md](migrating-from-i18n.md)           | Replacing an existing i18n system, before the main workflow                 |
| [rcc-v1-to-v2-upgrade.md](rcc-v1-to-v2-upgrade.md)         | Moving a site from RCC v1 to v2 — an alternative to the main workflow       |
| [astro/overview.md](astro/overview.md)                     | Astro implementations, plus the Astro i18n migration supplement             |
| [hugo/overview.md](hugo/overview.md)                       | Hugo: choosing one of three setups, root derivation, setup C (Rosey only)   |
| [hugo/native-multilingual.md](hugo/native-multilingual.md) | Hugo setup A: Hugo languages and `i18n` tables, no Rosey                    |
| [hugo/hybrid.md](hugo/hybrid.md)                           | Hugo setup B: Hugo languages for content, Rosey for UI strings              |
| [eleventy/overview.md](eleventy/overview.md)               | Eleventy implementations, incl. taxonomy scoping and link localization      |
| [scripts/fix-rosey-pages.mjs](scripts/fix-rosey-pages.mjs) | Postbuild fix for canonical and `og:url` on Rosey-generated pages           |

## The two layers

Keep these separate in your head. They are installed together but do different jobs, and only the first is required.

1. **Rosey-ready (required).** Rosey is an open-source, framework-agnostic tool that operates on your **built HTML**. You tag translatable elements with `data-rosey`, and a postbuild pipeline generates a key/value file per locale (`rosey/locales/{code}.json`) and builds translated copies of the site at `/{locale}/` URLs. This works on any SSG with no CMS. Once a site is Rosey-ready, translations can be filled in by **AI** (see the [`translate-site`](../translate-site/SKILL.md) skill), by hand, or by any external service.

2. **The RCC visual-editing layer (optional).** The RCC is a client-side script that bridges those locale files to CloudCannon's Visual Editor, giving editors a floating locale switcher and inline ProseMirror editors on every `data-rosey` element, with stale-translation detection. It **requires CloudCannon** as the CMS. If the site isn't on CloudCannon, skip every RCC/CloudCannon step and translate the locale files another way.

The bulk of this skill (tagging, the pipeline, locale files) is the required Rosey layer. Steps that belong only to the optional RCC layer are marked **(RCC layer)**.

## Which starting point are you in?

| Situation                                                                                          | Where to go                                                                                         |
| -------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| Single-language site, no translation system yet                                                    | Start at [setup.md](setup.md) — the main workflow                                                   |
| Site already uses an i18n system (astro-i18n, next-intl, path-based routing, dictionaries + `t()`) | Do [migrating-from-i18n.md](migrating-from-i18n.md) first, then [setup.md](setup.md)                |
| Site already uses **RCC v1** (form-based YAML editing, `generateRoseyId`, `data-rosey-tagger`)     | Follow [rcc-v1-to-v2-upgrade.md](rcc-v1-to-v2-upgrade.md) instead — a distinct, self-contained path |

## SSG detection and framework-specific guidance

After auditing the site (Phase 1), identify the SSG and read the matching `<ssg>/overview.md` for framework-specific implementation details:

| SSG             | File to read                                 |
| --------------- | -------------------------------------------- |
| Astro           | [astro/overview.md](astro/overview.md)       |
| Hugo            | [hugo/overview.md](hugo/overview.md)         |
| Eleventy (11ty) | [eleventy/overview.md](eleventy/overview.md) |

**Hugo: read `hugo/overview.md` before Phase 2.** It asks which of three setups the site needs, and one of them (Hugo's own multilingual system) replaces the Rosey workflow entirely.

These files contain root derivation patterns, content-block namespacing examples, the array-item component rule, split-by-directory details, locale picker examples, and framework-specific gotchas. The phase docs reference them where needed.
