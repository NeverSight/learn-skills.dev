---
name: wp-plugin-tag
description: Create, verify, list, or delete WordPress plugin version tags safely.
---

# WordPress Plugin Tag

Use this skill to manage WordPress plugin git tags based on the plugin header version.

## Inputs

- Action: create, verify, list, delete.
- Optional: push, annotated, force.

## Safety Rules

- Stop if the working tree is dirty.
- Confirm default branch before tagging.
- Never delete or force without explicit user approval.
- Never push tags unless the user explicitly asks.

## Workflow

1. **Locate plugin file**
   - Look for a PHP file in repo root with a `Plugin Name:` header.
   - If multiple files exist, ask the user to choose.

2. **Extract version**
   - Read `Version:` from the plugin header.
   - Validate semantic format (MAJOR.MINOR.PATCH); warn if it does not match.

3. **Select action**
   - **verify**: confirm `v<version>` exists locally or on remote.
   - **list**: show local and remote version tags.
   - **create**: create `v<version>` tag on the current commit.
   - **delete**: remove a tag locally and optionally from remote.

4. **Create tag (if requested)**
   - Confirm you are on the default branch and up to date.
   - Ask if the tag should be annotated.
   - If annotated, use the tag message template.
   - Create the tag and report success.

5. **Push tag (optional)**
   - Only if the user explicitly requests it.

6. **Delete tag (optional)**
   - Ask for explicit confirmation before local or remote deletion.

## Output

- Show the detected plugin version.
- Show the tag action taken and the final tag list.
