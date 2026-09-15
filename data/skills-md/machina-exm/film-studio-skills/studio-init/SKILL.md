---
name: studio-init
description: Scaffold an AI film studio before production starts.
---

# Studio Init

Create the project tree that acts as the film studio.

## Start with one question

Ask only:

> What is the project name?

Wait for the answer before doing anything else.
Use the name as the root folder when there is no existing project repository.
When a project repository already exists, use its root and keep the project name in the generated documentation.

## Create the studio

Create this exact structure under the project root:

```text
assets/
  characters/
  locations/
  props/
prompts/
generations/
selects/
edit/
color/
sound/
master/
docs/
```

Do not rename, merge, or omit these folders.
Preserve existing files and folders if the studio is being added to an active project.

## Seed the documents

Create `/docs/breakdown.md` with this empty template:

```markdown
# Breakdown

## Scenes

| Scene ID | Summary | Location | Time of day | Characters | Props | Shot-card file | Status |
|---|---|---|---|---|---|---|---|
```

Create `/docs/bible.md` with this empty template:

```markdown
# Visual Bible

## Asset boards

## Style boards

## Ban list
```

Create `/docs/registry.md` with this empty registry:

```markdown
# Asset Registry

| Tag | Type | Version | Seed file | Scenes | Status |
|---|---|---|---|---|---|
```

Create `/docs/generation-log.md` with this empty log:

```markdown
# Generation Log

| Shot ID | Prompt version | What changed | Result | Verdict |
|---|---|---|---|---|
```

Do not overwrite populated documents.
If a required document already exists, verify its headings and table columns and add only missing empty sections.

## Write the studio laws

Create `/docs/README` and include the project name, the folder map, and these three laws verbatim in meaning:

1. Only `/selects/` is visible to the edit.
2. Nobody but the prompt engineer enters `/generations/`.
3. Reference files are never renamed; a new version is a new file.

Explain that `/generations/` holds raw attempts and `/selects/` holds approved takes.
Do not add exceptions to the three laws.

## Verify the scaffold

Check that every required folder exists.
Check that all four seeded documents exist under `/docs/`.
Check that the registry and generation log use the required columns in the required order.
Check that `/docs/README` contains all three laws.

## Report the result

State the project root and list every created or preserved path.
Repeat the three studio laws in the output.
If anything could not be created, name the exact path and reason instead of claiming completion.
