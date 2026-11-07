---
name: captions
description: Clean, readable burned-in style subtitles from the verbatim transcript - stutters and fillers removed, spoken slang written correctly, one short line at a time, names checked, every line read by Claude before import into DaVinci Resolve. Use for "subtitles", "captions", "legendas", or when the creator reports wrong words in the captions.
---

# Captions

Goal: people watching **on mute** can follow; the captions are just there, never in the way.

## Source
The verbatim transcript mapped onto the **current** timeline (follow the creator's trims), not Resolve's own auto-captions (a second, less accurate transcription). Drop words on B-roll (radio lyrics, background talk).

## Clean, not verbatim
Captions show what they *mean*, written correctly:
1. **Stutters:** "pro-product" → "product", "da-da," → "da,".
2. **Cut-off words:** "es--", "A--" → gone.
3. **Filler sounds:** drawn-out "uuum", "hããã", "ééé" → gone. Careful with real words that look like fillers ("um" = "a" in Portuguese, "é" = "is").
4. **Self-corrections:** "get a, an appointment" → "get an appointment".
5. **Spoken short forms → correct written forms**, if the creator asks. Brazilian Portuguese example: cê/cês → você/vocês, tá → está, tô → estou, tava → estava, tamo → estamos, vamo → vamos, pra/pro → para/para o, né → não é, "o que que" → "o que", "por que que" → "por que", "tu consegue" → "você consegue"; "tão" → "estão" only before a verb in -ndo ("tão bonito" stays). Keep **expressions and swear words** (fix grammar, not voice). Keep capital letters at sentence starts when you shorten.
6. **Names and spellings checked on the web** (transcripts garble product names), and the creator's own name exactly as they write it.
7. Don't reveal what the creator wants kept secret (a place, a company) even if they say it.

Keep two lists: global rules (word map + phrases) in config, per-video fixes in `caption_fixes.json`. Apply phrase fixes *after* the word map.

## Lines
- **One line, max 42 characters**; a sentence's last word may stretch it to ~50 rather than sit alone.
- New cue at a pause ≥ 0.6 s, at sentence ends (if the line is already substantial), or after 3.2 s.
- Min 0.9 s on screen, end 0.25 s after the last word, never overlapping the next.
- A lone small word after a pause ("que", "vai", "not") joins the next line. Single-word cues are fine only when they stand alone ("Calm down.", "Bye.").
- **First cue starts at 00:00:00,000** (Resolve's import shifts everything relative to the first cue).
- Write a **new file name per version** (`captions_v3.srt`).

## Read every cue
Print every line and actually read it before handing it over. Grep for leftover short forms, double punctuation (",,"), lowercase after a full stop, words lost by your own filters. Fix rules, regenerate, read again.

## Into Resolve
The creator imports with **File > Import > Subtitle** (the API places subtitles after the timeline end; a workaround crashed Resolve). Delete the old subtitle clips but keep the track so its style stays.

## Style
Record the creator's style once (font, size, position, shadow) from their timeline and save it in config as the house style, e.g. a light sans at size 68, centred ~11% up from the bottom, soft drop shadow. Overlays must stay out of that band (see `motion-overlays`).
