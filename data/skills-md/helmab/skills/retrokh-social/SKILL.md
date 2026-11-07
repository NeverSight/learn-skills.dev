---
name: retrokh-social
description: Makes TikTok, YouTube and Facebook thumbnails, covers and posters in the look of 1960s–70s Cambodian golden-era print (record sleeves, song books, cinema bills), rendered as PNGs at exact platform sizes in Google Sans. Use it whenever the user wants a thumbnail, YouTube banner, Shorts cover, TikTok cover, Facebook cover, event banner or social poster that is Khmer, Cambodian, vintage or retro, or names RetroKh for social media, even if they don't say "skill" or give a size. Handles Khmer, English and bilingual text. For websites and app UI, use retrokh-design instead.
license: MIT
metadata:
  version: "1.0.0"
---

# RetroKh Social

Turn one brief into finished social images that look printed in Phnom Penh around 1965: flat spot inks, heavy Khmer lettering,
halftone dots and worn paper. Write one HTML artwork, and `scripts/render.py` outputs and checks every platform size from it.

Paths below are relative to this skill's folder.

## Workflow

1. **Read the brief and choose without asking**, then state your choices in one line. Ask only if the title or subject is missing.
   - **Formats:** `python3 scripts/render.py --list` shows them. Map the request: thumbnail → `youtube-thumbnail`; TikTok cover →
     `tiktok-cover`; Facebook cover → `facebook-page-cover`; "poster" → `facebook-post` plus `tiktok-poster`; "all platforms" →
     `youtube-thumbnail,tiktok-cover,facebook-post`.
   - **Style:** pick from the table below by subject. If the user wants options, render 2–3 styles.
   - **Language:** Khmer leads unless the user writes only in English and asks for English.
2. **Write the copy short.** The title is 1–5 words, because a thumbnail shows at about 168×94px on a phone. Cut every word the
   image already says. Never invent dates, venues, prices, names or quotes: write `[ … ]` placeholders and list them at the end.
3. **Copy the template and fill it.** `cp assets/template.html <name>.html`, then edit that copy:
   - Set `data-style` on `<html>`, and `data-layout="art-left"` if that suits the subject.
   - Put each title line in its own `<span>` inside `.rs-title`. Break Khmer at a word boundary, since two lines read far larger than one.
     Latin title lines need `lang="en"`.
   - Delete anything you don't need: a title and one line beat a full stack.
   - Choose the art (next section). Add artwork-only CSS in the template's `<style>` block.
4. **Render with the guides on:**
   `python3 scripts/render.py <name>.html --formats a,b,c --out <folder> --guides`
   It writes each PNG, a `.guides.png` with the safe area drawn on it, and for thumbnails a `-small.png` at real viewing size.
5. **Look at the results, then fix.** Fix every ERROR and re-render. Then open each image and the `-small.png`, because the script
   can't judge these: is the title readable when small, is the Khmer complete and correctly spelled, does anything collide, does the
   subject read in one second? Don't hand over an image you haven't looked at.
6. **Finish** with the image paths, your choices and the placeholders to fill. Delete the `.guides.png` files unless the user wants them.

## Styles

| `data-style` | Looks like | Best for | Art |
|---|---|---|---|
| `sunburst` | Red and yellow rays with copy on plates | Music, comedy, promos, anything loud | vinyl, portrait in a circle |
| `giant-type` | Huge oxblood type on mustard | Short titles, tutorials, announcements | chapei, lotus, cut-out |
| `night-press` | Dark teal, halftone sun, gold type | Travel, stories, nostalgia, events | sugar-palms |
| `torn-collage` | Torn red and blue paper | News, history, documentary | cassette, cut-out |
| `songbook` | One blue ink on foxed paper | Lyrics, karaoke, classics, education | microphone, portrait in a circle |
| `halftone-noir` | Coal black, gold type, red dots | Portraits, film, drama, beauty | cut-out, portrait in a circle |

`references/styles.md` has palettes and composition notes. Read it when you go beyond the template or the result feels generic.

## Art

- **Motifs:** `<rs-motif name="…"></rs-motif>` inside `.rs-art`, using `chapei`, `vinyl`, `cassette`, `microphone`, `lotus` or
  `sugar-palms`. The renderer inlines them and colours them from the style. Tilt with `--art-rot:-12deg` on `.rs-art`.
- **The user's photo:** faces win thumbnails, so use one if you have it. Put the file beside the HTML.
  - Cut-out with a transparent background: `<div class="rs-art" data-frame="cutout"><img class="rs-photo" src="me.png" alt=""></div>`
  - Ordinary photo: `<div class="rs-art" data-frame="circle"><img class="rs-photo" src="me.jpg" alt=""><div class="rs-dots"></div></div>`
- **People:** never imitate a real person with drawn or generated art, and don't copy faces or layouts from existing vintage
  posters. Use a photo the user owns, or a motif.
- **Stay in the era.** No gradients, glass, soft shadows, emoji or neon. Avoid the flag, royal arms, Angkor silhouettes as decoration,
  Thai or Lao motifs passed off as Khmer, and any war or 1975–79 imagery.

## Fonts

Google Sans is the only font, for Khmer and Latin alike, in weights 400, 500 and 700. The renderer reports an ERROR for any other
family or weight, so the look has to come from scale, colour and print texture rather than from a decorative typeface.

- **Titles and kickers:** 700. Khmer has no heavier display face here, so make the title far bigger than feels polite.
- **Latin labels:** 500 caps with `.18em` tracking. Show Khmer numerals in Khmer copy, such as ១២ rather than 12.
- **Khmer:** line-height at least 1.5, no letter-spacing, no caps or faux italics, and break only at word boundaries. Clipped
  subscripts change the word, so never set a fixed title height. `.rs-title` handles sizing.

## Rendering problems

- **Chrome not found:** set `CHROME_PATH`.
- **Font did not load:** the render needs network access to Google Fonts. Say so if you can't reach it, and don't ship the fallback.
- **File over the limit:** the renderer converts to JPEG when Pillow is installed. Otherwise lower the grain with `--wear:.4` on `html`.

Sizes and safe areas change without notice. `references/formats.md` says which values are firm and which to confirm in a test upload.
