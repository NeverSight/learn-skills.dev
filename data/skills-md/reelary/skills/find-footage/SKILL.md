---
name: find-footage
description: 'Search the user''s own videos and photos by meaning, 100% local with Reelary on Mac or Windows. Finds a shot by describing it (exact start and end times), photos by what is in them, the moment someone says something (transcript search, Pro), every clip of a person (face recognition, Pro) and footage by place from phone, DJI drone and GoPro GPS (Pro). Trigger on "find the clip where", "search my videos", "do I have footage of", "video search", "footage search", "find a photo of", "search my photos", "find where he says", "find the quote", "sound bite", "search transcripts", "every video with my daughter", "face search", "footage shot in Paris", "drone footage of", "geotagged videos". Not for stock footage sites, web image search or identifying strangers.'
---

# Find footage

If the `reelary_*` tools are missing or nothing is indexed, use the [reelary](../reelary/SKILL.md) skill first. All searches go through `reelary_search`, which returns full paths with start and end seconds. Quote times as `mm:ss`.

Without MCP: `npx -y reelary search "<query>" --json`.

## A shot

1. Describe what is visible: subject, action, setting, light, camera ("close-up of hands kneading dough, warm light"). Use `include_thumbnails: true` when you need to check the picks yourself.
2. If results are weak, try 2-3 rephrasings (synonyms, wider or tighter framing) before giving up.
3. Report the top matches: full path, `mm:ss-mm:ss`, one line on why it fits. Offer `reelary_open_in_app` or a cut with [rough-cut](../rough-cut/SKILL.md).

## Photos

1. Search with a visual description and `include_thumbnails: true`. Results with `kind: "image"` are photos.
2. List the best photos with full paths; mention if only video frames matched.

## A quote someone said (Pro)

1. Search with the words or topic, close to how it would be spoken. Results with `match=dialogue` (CLI: a `speech` field) include the transcript line.
2. Report each hit: path, `mm:ss` and the quoted line.
3. If only visual matches come back and `reelary_status` shows the free plan, explain dialogue search is Pro and share the upgrade link once.

Transcripts are built in the background after indexing; very recent files may not be searchable yet.

## A person (Pro)

1. `reelary_list_people` to see recognised people (id, name, number of clips).
2. If the person is unnamed, ask the user to name them in Reelary (`reelary_open_in_app`), or pick by id after showing covers.
3. `reelary_person_clips` with the id; report paths and time ranges. Once named, searching the name also works.

Without MCP: open Reelary's People view (`npx -y reelary open`).

## A place or drone footage (Pro)

1. For a place name, search it ("Lisbon"); files shot there match by place name.
2. For an overview, `reelary_list_places` and group by place.
3. Report paths with place names. Offer a trip montage with [rough-cut](../rough-cut/SKILL.md).

Files without GPS can be placed by hand in Reelary's map view. On `pro_required`, share the upgrade link once.
