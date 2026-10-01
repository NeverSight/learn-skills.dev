---
name: lower-thirds
description: Make animated lower thirds and other broadcast overlays (name straps, corner bugs, subscribe reminders, scripture or song titles) as transparent video files, drawn frame by frame in JavaScript on a canvas and rendered to WebM with alpha for OBS and browsers, or ProRes 4444 for Premiere Pro, DaVinci Resolve and Final Cut. Use when someone wants a lower third, a name title, a chyron, a stream overlay, a corner bug, or any graphic with a transparent background to lay over their own footage or livestream.
---

# Lower thirds

A lower third is the name-and-role graphic in the bottom part of the frame that says who is speaking, laid over footage the graphic never sees. The deliverable is a file with an alpha channel: everything you do not draw stays see-through.

You copy `templates/lower-third.html` into the working folder, write the design into it, check it with `scripts/render.mjs`, and render the files. Run the script from the working folder (`node <this skill>/scripts/render.mjs …`); outputs land there. Make it in one go: don't ask questions the brief already answers or a sensible default covers, and list the defaults you chose when you deliver.

## 1. Read the brief

- **The words, exactly as they should read**: names, roles, show name, handle, scripture reference, song title. Keep the user's spelling and punctuation (setting a line in capitals is styling; the words stay theirs); never invent a title or a surname. If they give no second line, use their own words for one (what the stream is about) or leave it out.
- **How many cards**: each person or item is one entry in `CARDS`, rendered to its own file with the same design. Add fields when a card needs more than `title` and `sub`.
- **Where it goes**: OBS or a stream → WebM only; a web page → WebM plus the Safari HEVC copy (`references/delivery.md`); Premiere Pro, DaVinci Resolve, Final Cut → ProRes 4444 `.mov`; both named → both; a phone editor or tool without alpha → an MP4 on a green ground for chroma key. Not said: WebM and `.mov`.
- **The look**: the show, the brand colours, the mood (news, podcast, gaming, documentary, church, corporate). The design comes from this, not from the template.
- **Defaults when not given**: 1920×1080 at 30 fps; about 8 seconds (under a second in, a still hold of 5–6 seconds, half a second out); lower left; silent.

## 2. Design it for this show

The template's `drawGraphic` is a working example of the structure, not the look: rewrite it for the brief. What holds for every design:

- **Legible over any footage.** The graphic cannot know what is behind it, so text sits on its own backing (a panel, a bar, a band, a heavy shadow). Thin light text straight on the picture disappears on a bright shot.
- **Inside title-safe.** Keep every pixel at least 5% in from each edge (`SAFE` in the template is 6%). The lower third lives in the bottom third; a corner bug in a corner; the middle of the frame stays empty for the speaker.
- **Small.** A name strap covers a few percent of the frame; the name is roughly 50–80 px tall at 1080p, the role about half that.
- **Still while it's being read.** The motion is in the build-in and build-out; the hold does not move, or moves so little it doesn't pull the eye (one slow sheen at most).
- **Starts and ends empty.** The first and last frames have nothing in them, so the clip never pops on or cuts off in the edit. Keep `LEAD` and `TAIL`.
- **The words are never cut.** Use `fit()` so a long name shrinks to its box instead of overflowing it, and size every wipe or clip to the widest thing it reveals. Check the longest entry in `CARDS`.
- **Fonts**: one Google Fonts `<link>` per family with the weights and italics you use, and every face you draw with listed in `FONTS` (`'700 Inter'`, `'italic 400 Libre Baskerville'`), so nothing renders in a fallback font. Many serifs (Cormorant, EB Garamond, Playfair Display) draw old-style numerals that drop below the line, and canvas can't switch them to lining ones: if the card has digits ("Psalm 1:3", "Episode 12"), pick a face with lining numerals (Lora, for one) and check the stills.

Several things on screen (a host strap, a guest strap, a corner bug for the whole segment) can be one page with their own timings, or one page per graphic when the editor needs to place them separately; say which you did.

## 3. Check it

```bash
node render.mjs page.html --check                                    # fonts, transparency, empty first/last frame, title-safe, timing
node render.mjs page.html shot --stills 3s                           # the hold, full frame, over a checkerboard, dark and light footage
node render.mjs page.html in.jpg --sheet 0.1 --in                    # the build-in, frame by frame, cropped to the graphic
node render.mjs page.html out.jpg --sheet 0.1 --out                  # the build-out (both read window.PHASES)
```

`--check` must pass, but it can't see text cut off by a wipe or text that's hard to read: your eyes do that. In the stills, every word reads over both the dark and the light ground and the spacing is even. In the sheets, nothing jumps, no text shows before or outside the part of its panel that is revealed, none gets cut mid-hold, and the build-out is as clean as the build-in. Check every entry in `CARDS` (`--card N` counts from 0: `--card 1` is the second). Fix and look again until it holds up.

## 4. Render and deliver

```bash
node render.mjs page.html maya-chen.webm                    # VP9 with alpha
node render.mjs page.html maya-chen.mov                     # ProRes 4444 with alpha (large)
node render.mjs page.html daniel-ortiz.webm --card 1        # the next card
node render.mjs page.html maya-chen-4k.webm --scale 2       # 3840x2160
node render.mjs page.html maya-chen-green.mp4 --ground '#00ff00'
```

The script refuses an MP4 without `--ground` (H.264 has no alpha) and confirms that WebM and `.mov` files really carry an alpha channel, by decoding a frame from the hold. Hand over the files, the page (they can change a name and re-render), and how to use them in their tool from `references/delivery.md`, in two or three lines (a web page also needs the Safari file described there). Say what you chose that they didn't ask for.

Needs: Node 18+, `npm i playwright-core` in the working folder or any folder above it, ffmpeg, and Chrome (or `npx playwright install chromium`).
