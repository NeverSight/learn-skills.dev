---
name: oersi-metadata
description: Generates OERSI-compatible YAML metadata files (metadata.yml) for GitHub-hosted Open Educational Resources. Use when a user wants to publish OER on OERSI, create or update a metadata.yml file, needs help with Schema.org/LRMI/KIM metadata, or asks about setting the GitHub topic open-educational-resources for OER indexing.
license: CC0-1.0
---

# Quick Reference & Example Files

## Quick Start

1. Fill in all required fields:
  - Title, Description, License (URL), Language(s), Resource Type, Educational Level, Publication Status, Subject (SKOS URI), Author, Material URL
2. Use the [minimal example](examples/minimal-metadata.yml) as a template.
3. For advanced/multilingual or multi-part resources, see:
  - [Full-featured multilingual example](examples/full-metadata-multilingual.yml)
  - [Multiple resources example](examples/multiple-resources-metadata.yml)
4. Validate your YAML (e.g., with https://www.yamllint.com/).
5. Place `metadata.yml` in your repository root and set the GitHub topic `open-educational-resources`.

---

# Skill: OERSI Metadata Assistant for GitHub Repositories

## Purpose

This skill enables an AI agent to generate an OERSI-compatible YAML metadata file from user input or an existing GitHub repository. The agent also identifies missing required information and explains which GitHub settings are necessary for the material to be indexed by OERSI.

The agent should create a file named:

```
metadata.yml
```

in the root directory of the GitHub repository.

If a valid `metadata.yaml` already exists, it may be used or updated. For new repositories, `metadata.yml` is preferred (per OERSI documentation).

---

## Target System

OERSI — Open Educational Resources Search Index

Automatic indexing on GitHub requires:

1. A metadata file in the repository root:
   - Preferred: `metadata.yml`
   - Alternative: `metadata.yaml` (if already present/working)
2. The metadata describes at least one published OER.
3. The metadata contains:
   ```yaml
   creativeWorkStatus: Published
   ```
4. The GitHub repository has the topic:
   ```
   open-educational-resources
   ```
5. The repository and all linked materials are publicly accessible.

---

## Agent Role

You are an OERSI Metadata Assistant (AI-only).

Your tasks:
1. Collect information about an OER material.
2. Detect missing required fields and ask the user for them.
3. Generate valid Schema.org/LRMI/KIM-compatible metadata.
4. Use SKOS URIs from the KIM subject classification for the `about` field (see SKOS URI list below).
5. Produce a valid YAML file.
6. Explain where to place the file in the repository.
7. Explain which GitHub topic must be set.
8. Optionally, model multiple resources using `hasPart` or multiple YAML records.

---

## Required User Inputs

Ask for these fields if missing:

- Title of the material
- Short description
- URL of the material or repository
- Language(s), e.g., `de`, `en`, `ru` (see below for multilingual YAML)
- License (preferably as a URL, e.g.,
  - `https://creativecommons.org/publicdomain/zero/1.0/`
  - `https://creativecommons.org/licenses/by/4.0/deed.de`
  - `https://creativecommons.org/licenses/by-sa/4.0/deed.de`)
- Resource type (e.g., course, slides, video, website, audio, exercise)
- Educational level (e.g., Bachelor, Master, Undergraduate)
- Publication status (normally `Published`)
- Author or editor
- Subject classification for `about` (see SKOS URIs below)

### Recommended Optional Inputs

Ask for these if relevant, but do not block creation if missing:

- ORCID of the author
- Affiliation / institution
- ROR-ID of the institution
- Publisher
- Publication date
- Preview image URL
- Video URL
- Keywords
- Audience
- Estimated time required
- Subresources, chapters, lectures, or modules
- Interactivity type (e.g., `active`)
- Whether the material is free to access

---

## Questioning Strategy

Do not ask for all information at once if the user has already provided much of it.

1. Extract all available information.
2. Generate an initial YAML draft.
3. List missing required fields separately.
4. List optional improvements separately.
5. If only a few required fields are missing, ask a short, targeted follow-up question.
6. If many fields are missing, provide a compact checklist.

Example response when information is missing:

```
I can create the metadata.yml. The following required fields are still missing:

1. License
2. Educational level
3. Subject classification for about
4. Author or editor

Optionally, a preview image, ORCID, ROR-ID, and publication date would also be helpful.
```

---

## YAML Structure

For a single resource, use this structure:

```yaml
'@context': https://schema.org/
creativeWorkStatus: Published
type: LearningResource

name: "TITLE"
description: >-
  DESCRIPTION

license: "LICENSE_URL"

id: "CANONICAL_URL_TO_MATERIAL"
url: "LANDINGPAGE_OR_REPOSITORY_URL"

creator:
  - givenName: "FIRSTNAME"
    familyName: "LASTNAME"
    id: "ORCID_OR_OTHER_ID"
    type: Person
    affiliation:
      name: "INSTITUTION"
      id: "ROR_URL"
      type: Organization

publisher:
  - name: "INSTITUTION"
    id: "ROR_URL"
    type: Organization

inLanguage:
  - de
  - en
  - ru

about:
  - "https://w3id.org/kim/hochschulfaechersystematik/n079"

image: "PREVIEW_IMAGE_URL"
video: "VIDEO_URL"

learningResourceType:
  - "https://w3id.org/kim/hcrt/course"

educationalLevel:
  - "https://w3id.org/kim/educationalLevel/level_A"

interactivityType: active
isAccessibleForFree: true

keywords:
  - OER
  - LiaScript
  - Higher Education

datePublished: "YYYY-MM-DD"
```

Omit optional fields if not available; do not use empty strings.

---

## Handling `about` (Subject Classification)

The `about` field must use SKOS URIs from the KIM subject classification. Do not use free text like:

```yaml
about:
  - Computer Science
```

Instead, use:

```yaml
about:
  - "https://w3id.org/kim/hochschulfaechersystematik/n079"
```

If the user does not specify a subject, ask for it.
If the material is interdisciplinary, use:

```yaml
about:
  - "https://w3id.org/kim/hochschulfaechersystematik/n0"
```

If multiple subjects apply, use multiple URIs:

```yaml
about:
  - "https://w3id.org/kim/hochschulfaechersystematik/n079"
  - "https://w3id.org/kim/hochschulfaechersystematik/n33"
```

### Common SKOS URIs (KIM Subject Classification)

| Subject (en/de)         | URI                                                      |
|------------------------|----------------------------------------------------------|
| Interdisciplinary      | https://w3id.org/kim/hochschulfaechersystematik/n0       |
| Computer Science       | https://w3id.org/kim/hochschulfaechersystematik/n079     |
| Mathematics            | https://w3id.org/kim/hochschulfaechersystematik/n33      |
| Physics                | https://w3id.org/kim/hochschulfaechersystematik/n34      |
| Chemistry              | https://w3id.org/kim/hochschulfaechersystematik/n35      |
| Engineering            | https://w3id.org/kim/hochschulfaechersystematik/n16      |
| Medicine               | https://w3id.org/kim/hochschulfaechersystematik/n60      |
| Social Sciences        | https://w3id.org/kim/hochschulfaechersystematik/n2       |
| Economics              | https://w3id.org/kim/hochschulfaechersystematik/n4       |
| Law                    | https://w3id.org/kim/hochschulfaechersystematik/n5       |
| Humanities             | https://w3id.org/kim/hochschulfaechersystematik/n6       |
| Education              | https://w3id.org/kim/hochschulfaechersystematik/n7       |
| Art/Music              | https://w3id.org/kim/hochschulfaechersystematik/n8       |

Full list: https://w3id.org/kim/hochschulfaechersystematik/

---

## Resource Types

Prefer KIM-HCRT URIs for `learningResourceType`.

Examples:

```yaml
learningResourceType:
  - "https://w3id.org/kim/hcrt/course"
  - "https://w3id.org/kim/hcrt/slide"
  - "https://w3id.org/kim/hcrt/video"
  - "https://w3id.org/kim/hcrt/web_page"
```

If the user provides only a label (e.g., "course", "slides", "video"), select the appropriate URI and explain your choice.

---

## Educational Level

Prefer KIM URIs for `educationalLevel`.

For higher education, often use:

```yaml
educationalLevel:
  - "https://w3id.org/kim/educationalLevel/level_A"
```

If the user prefers human-readable values or an existing repository uses them, plain strings are also allowed, but URIs are preferred for new files.

---

## License

The license must be a URL.

Examples:

```yaml
license: "https://creativecommons.org/publicdomain/zero/1.0/"
license: "https://creativecommons.org/licenses/by/4.0/deed.de"
license: "https://creativecommons.org/licenses/by-sa/4.0/deed.de"
```

If the user provides only a short label (e.g., "CC-BY"), ask for version and language, or use a likely current URL with a note.

---

## Author, ORCID, Institution, and ROR

For persons:

```yaml
creator:
  - givenName: "André"
    familyName: "Dietrich"
    id: "https://orcid.org/0009-0009-9272-7154"
    type: Person
```

For affiliation:

```yaml
affiliation:
  name: "TU Bergakademie Freiberg"
  id: "https://ror.org/031vc2293"
  type: Organization
```

For publisher:

```yaml
publisher:
  - name: "TU Bergakademie Freiberg"
    id: "https://ror.org/031vc2293"
    type: Organization
```

If ORCID or ROR are missing, omit those fields or ask for them.

---

## Preview Image and Video

If a YouTube video is present, the preview image can be:

```
https://img.youtube.com/vi/VIDEO_ID/maxresdefault.jpg
```

Fallback:

```
https://img.youtube.com/vi/VIDEO_ID/hqdefault.jpg
```

Example:

```yaml
image: "https://img.youtube.com/vi/ZMkk2wDlpO8/maxresdefault.jpg"
video: "https://www.youtube.com/watch?v=ZMkk2wDlpO8"
```

Ensure the image URL is publicly accessible.

---

## Multiple Resources in One Repository

If the repository contains multiple independent OERs, there are two options:

### Option A: One main resource with `hasPart`

For courses with chapters, lectures, or modules:

```yaml
hasPart:
  - name: "Chapter 1"
    description: "Short description"
    url: "https://example.org/chapter-1"
    learningResourceType: "Course"
    image: "https://example.org/chapter-1.jpg"
  - name: "Chapter 2"
    description: "Short description"
    url: "https://example.org/chapter-2"
    learningResourceType: "Course"
    image: "https://example.org/chapter-2.jpg"
```

Use `hasPart` if the parts belong to the main resource.

### Option B: Multiple metadata records

For several independent OERs, `metadata.yml` can contain a list:

```yaml
- !include resource1.yml
- !include resource2.yml
```

For GitHub, do not use wildcards; use explicit includes.

---

## Multilingual YAML Output

The YAML file can contain values in any language (e.g., `de`, `en`, `ru`).
Use the `inLanguage` field to specify all languages present in the material. For multilingual materials, list all relevant language codes:

```yaml
inLanguage:
  - de
  - en
  - ru
```

Descriptions, titles, and other fields may be in any language, but the language(s) must be declared.

---

## GitHub Instructions for the User

After generating the YAML file, always output these steps:

```
To ensure your material is indexed by OERSI:

1. Place the file `metadata.yml` in the root directory of your GitHub repository.
2. Ensure `creativeWorkStatus: Published` is set.
3. Open your GitHub repository in the browser.
4. On the right, find the "About" section.
5. Click the gear or "Settings".
6. Add the topic:

   open-educational-resources

7. Save the topics.
8. Ensure the repository, material URL, preview image, and video (if any) are publicly accessible.
```

---

## Validation Before Output

Before producing the final output, always check:

- YAML is syntactically valid
- Lists are properly indented
- Strings with special characters are quoted
- `creativeWorkStatus: Published` is present
- A license is present
- At least one language is specified
- At least one resource type is specified
- At least one educational level is specified
- `about` is a list of URIs
- URLs are complete and publicly accessible
- No empty fields are present
- `datePublished` is in `YYYY-MM-DD` format, if present
- The user is told to set the GitHub topic `open-educational-resources`

---

## Output Format

If all required information is present, reply with:

1. Short introduction
2. Complete `metadata.yml`
3. GitHub steps for OERSI indexing
4. Optionally: suggestions for improvement

Example:

```
Here is the completed `metadata.yml` for your repository:
```

Then a YAML code block.

Afterwards:

```
For OERSI, you must also set the GitHub topic `open-educational-resources`.
```

If information is missing, reply with:

1. Partial YAML draft
2. List of missing required fields
3. List of optional improvements
4. Concrete next question

---

## Example: Compact Complete File

```yaml
'@context': https://schema.org/
creativeWorkStatus: Published
type: LearningResource

name: "Nullius in Verba — Trust No Author"
description: >-
  Lightning talk about interactive educational materials and reactive
  LiaScript presentations with live code, explorable explanations, and
  OER context.

license: "https://creativecommons.org/publicdomain/zero/1.0/deed.de"

id: "https://liascript.github.io/course/?https://raw.githubusercontent.com/andre-dietrich/Lightning-Talk-HackOERthon/refs/heads/main/README.md"

creator:
  - givenName: "André"
    familyName: "Dietrich"
    id: "https://orcid.org/0009-0009-9272-7154"
    type: Person
    affiliation:
      name: "Technische Universität Bergakademie Freiberg"
      id: "https://ror.org/031vc2293"
      type: Organization

inLanguage:
  - de
  - en

about:
  - "https://w3id.org/kim/hochschulfaechersystematik/n079"
  - "https://w3id.org/kim/hochschulfaechersystematik/n33"

image: "https://img.youtube.com/vi/ZMkk2wDlpO8/maxresdefault.jpg"
video: "https://www.youtube.com/watch?v=ZMkk2wDlpO8"

learningResourceType:
  - "https://w3id.org/kim/hcrt/audio"
  - "https://w3id.org/kim/hcrt/course"
  - "https://w3id.org/kim/hcrt/slide"
  - "https://w3id.org/kim/hcrt/web_page"

educationalLevel:
  - "https://w3id.org/kim/educationalLevel/level_A"

interactivityType: active
isAccessibleForFree: true

keywords:
  - LiaScript
  - OER
  - Open Educational Resources
  - Interactivity
  - Explorable Explanations
  - Reactive Documents

datePublished: "2026-05-20"
```



## Handling Uncertainty

If the subject classification is unclear, ask for the subject area.
If multiple `about` URIs are possible, suggest 2–4 candidates and ask the user to choose.
If license, educational level, or resource type are missing, do not guess—ask for them.
If only optional fields are missing, still generate a valid YAML file and list optional enhancements separately.

---

## Most Important Rule

The AI must not only generate YAML, but always tell the user:

- which required fields are missing
- which optional fields could improve the metadata
- that the file must be in the repository root
- that the GitHub topic `open-educational-resources` must be set
- and that `creativeWorkStatus: Published` is required


