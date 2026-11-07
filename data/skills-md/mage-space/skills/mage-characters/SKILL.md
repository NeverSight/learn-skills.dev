---
name: mage-characters
description: |
  Save a person, mascot, or product as a reusable Mage character or reference
  and keep it consistent across images and video by mentioning its @handle.
  Creates characters from a portrait (optionally with a voice), creates
  references for outfits, poses, locations, objects, and voice clips, lists
  and deletes them, and generates the same character in new scenes with
  Mango 3 or Cherry 2 Pro. Use when: "save this person as a character",
  "keep the same face", "consistent character", "make my character",
  "digital twin", "reuse this outfit", "same person in every image", "give my
  character a voice", "put @handle in a video". Chain: create the character
  here, then any Mage skill can use its @handle. NOT for: one-off edits of a
  single photo (use mage-generate), product listing sets
  (mage-product-photoshoot or mage-marketplace-cards), or face swaps onto
  real people without their consent.
license: MIT
compatibility: Requires the Mage connector (https://mcp.mage.space/mcp) and a Mage account with Gems.
metadata:
  author: mage-space
  version: "0.0.0" # x-release-please-version
---

# Mage Characters

Save someone or something once, then keep it consistent everywhere. A Mage **character** is a portrait with an optional voice; a **reference** is an outfit, pose, location, object, or voice clip. Both are private to the account and are used by writing `@handle` in any prompt.

## Before you start

1. **Mage tools.** This skill uses `list_characters`, `create_character`, `delete_character`, `list_references`, `create_reference`, `delete_reference`, and the generation tools (`get_model`, `estimate_cost`, `generate`, `get_request`). If they are missing, ask the user to connect Mage (Claude: Customize → Connectors → Add custom connector, `https://mcp.mage.space/mcp`; Claude Code: `/mcp` to sign in if the Mage plugin is installed, otherwise `claude mcp add --transport http mage https://mcp.mage.space/mcp`; others: https://www.mage.space/mcp), then wait.
2. **Images are links.** `create_character` and `create_reference` take an https URL of a JPEG or PNG, a data URL, or an upload URL from `create_upload`. Files attached to the chat never reach Mage: ask for a direct link, or upload from disk when you can run commands.
3. **Consent.** Only save a real person's likeness with that person's consent. Never build a character to impersonate someone.

## UX rules

1. Be concise. Report "Saved @nova" with the name, not ids or JSON.
2. Reply in the user's language.
3. Ask only for what's missing: a name and one portrait. Derive the handle from the name unless the user picks one.
4. Saving is free; generating costs Gems. Quote generations as usual and wait for a yes before a batch or a video.
5. Check `list_characters` before creating, so you don't duplicate one that exists.

## Save a character

1. **Get a portrait.** One clear image of one subject: face visible, even light, plain background, head and shoulders, no sunglasses or heavy filters. See `references/portrait-guide.md`.
   - No photo? Generate one first: Guava 2 Pro (`guava`, `guava-2-pro`) for a photoreal person, Mango 3 (`mango`, `mango-v3`) for an illustrated character or mascot, `1:1` or `4:5`. Use the prompt pattern in `references/portrait-guide.md` and show the portrait before saving it.
2. **Pick a handle:** 1–15 lowercase letters, digits, `_` or `-`, starting with a letter. It cannot change later. If it is taken (`handle_taken`), suggest another.
3. **Optional voice.** A voice clip (MP3 or WAV, trimmed to 10 seconds) makes the character speak in their own voice in Cherry and Lemon videos. No clip? Generate 10 seconds of the voice with Seed Audio (`seed_audio`), a line of natural speech in the voice you want, and pass its `result.url` as `voice`.
4. **Create** with `create_character` (`name`, `image`, optional `handle`, `voice`, `description`).
5. **Deliver:** "Saved @nova. Mention @nova in any prompt to use her."

## Save a reference

For anything that isn't a whole character, call `create_reference` with a `kind`:

| Kind | Use it for | Input |
|---|---|---|
| `outfit` | Clothing to put on any character | `image` of the garment or outfit (flat lay or worn) |
| `pose` | A body position to copy | `image` showing the pose |
| `location` | A place to reuse as the setting | `image` of the place |
| `object` | A product, prop, vehicle, or logo | `image` of the object on a plain background |
| `audio` | A voice or sound to reuse in audio and video | `audio` clip (MP3 or WAV, trimmed to 15 seconds) |

## Use them

Write the handles in the prompt as natural language: "@nova sits in @corner-cafe wearing @red-coat, reading a book." Mage attaches each entity to the request.

- **Images:** Mango 3 by default: it holds identity best across a set. Guava 2 Pro for photoreal close-ups. GPT Image 2.5 Flare when the image also needs text.
- **Video:** Cherry 2 Pro. A character with a voice speaks with it (`use_character_voices` defaults to true; set false to mute it). Quote the words: `@nova says, "Welcome back."`
- **Budget:** characters, references, and the request's own images share the model's `max_images`, and voices share `mentions.max_audio_references`. `get_model` has both.

For a consistent set (a storyboard, a campaign, a comic), keep the same handles, style words, and aspect ratio in every prompt, and generate the set in one batch. See `references/consistency.md`.

## Manage

- `list_characters` and `list_references` (optionally one `kind`) show what's saved, newest first.
- `delete_character` / `delete_reference` with the `id` from a list. The handle stops working at once and may be taken again later. Confirm with the user before deleting.
- Public characters from other Mage users also work by handle but aren't listed. Publishing happens in the Mage app.

## Errors

| Code | What to do |
|---|---|
| `handle_taken` | Pick another handle, or leave it out to derive one. |
| `invalid_config` on generate | A handle didn't resolve, the model doesn't take that kind, or the budget is exceeded. The message names it. |
| `invalid_config` on create | The image or clip couldn't be fetched or isn't JPEG/PNG or MP3/WAV. Ask for a direct link. |

## References

- `references/portrait-guide.md`: what makes a portrait hold up across scenes, and prompts for generating one.
- `references/consistency.md`: keeping characters, outfits, and style consistent across a set.
