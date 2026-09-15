---
name: setup
description: Configure AI film tools when setting up a studio project.
---

# Set Up the AI Film Studio

Connect the user's existing image and video tools to the project.
Store the shared configuration in both project instruction files so every agent reads the same settings.

## Start safely

Work from the project root.
Read the project's `CLAUDE.md` and `AGENTS.md` if they exist.
Preserve every unrelated section and instruction.
Do not create the studio file tree during this setup; `studio-init` handles that next.

If the user already supplied an answer, confirm it from context instead of asking again.
Otherwise, ask one question at a time and wait for the answer before continuing.
Never present a wall of questions.
Never suggest or name a model or service; the user names their own stack.

## Interview the user

Ask these questions in order:

1. Which image model or models do you use?
2. How do you access the first image model: app, API key, CLI, or another method?
3. Repeat the access question separately for each additional image model.
4. Which video model do you use?
5. How do you access the video model: app, API key, CLI, or another method?
6. What clip length do you normally generate within the 10–15 second range?
7. Which folder should hold the studio project and its generated output?

When access uses an API key, ask only for the environment variable name that holds it.
Never ask for, display, copy, or write the secret value.
If the user provides a secret value, do not place it in a file.
Ask them to save it in their usual environment or secret store, then record only its variable name.

For CLI access, record the command name or invocation pattern without credentials.
For app or other access, record a short operational description.
Keep the user's model names exactly as given.

## Build the shared section

Create one section with this shape:

```markdown
## AI film studio

### Image models
- `<model name>` — access: `<app, API via ENV_VAR, CLI, or other>`

### Video model
- `<model name>` — access: `<app, API via ENV_VAR, CLI, or other>`

### Working defaults
- Clip length habit: `<number or range in seconds>`
- Output folder: `<project-relative or absolute path>`
```

Add one bullet per image model.
Use the user's exact access details, but omit credentials and other secret values.
Use a path that identifies the studio project root, not a temporary download folder.
Do not add model recommendations, pricing, account details, or invented configuration.

## Update both instruction files

Write the completed section into `CLAUDE.md`.
If `## AI film studio` already exists, replace only that section through the line before the next level-two heading.
If it does not exist, append the section with clean blank-line separation.

Mirror the exact same section into `AGENTS.md`.
If `AGENTS.md` exists, replace or append only the studio section and preserve the rest.
If `AGENTS.md` is missing, create it as a copy of the updated `CLAUDE.md`.
If `CLAUDE.md` is missing but `AGENTS.md` exists, copy `AGENTS.md` to `CLAUDE.md`, then update both.
If both files are missing, create `CLAUDE.md` with the section and copy it to `AGENTS.md`.

Verify that the two `## AI film studio` sections match exactly.
Verify that neither section contains an API key, token, password, or secret value.
Report which files were created or updated.

## Hand off the workflow

End by printing this chain with one line per skill:

`setup → studio-init → film-breakdown → reference-board → asset-passport → stress-test → shot-prompt`

- `setup` — connect the user's tools and share the configuration.
- `studio-init` — scaffold the studio tree, templates, and file laws.
- `film-breakdown` — turn the script or idea into scenes and shot cards.
- `reference-board` — define approved references, captions, and bans.
- `asset-passport` — create verbatim descriptors and reference-sheet prompts.
- `stress-test` — test every draft asset and lock only repeatable ones.
- `shot-prompt` — turn a shot card and locked passports into the fixed prompt.

Then print the four golden rules:

1. Lock assets before generating for the film.
2. Keep one approved reference passport per asset.
3. Make surgical one-line edits and keep everything else verbatim.
4. Version and log everything.

Tell the user to run `studio-init` next.
