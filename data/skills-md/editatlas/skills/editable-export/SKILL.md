---
name: editable-export
description: Give the person an editable copy of a video you made, built from its elements (footage clips, text, graphics, sounds, music), which opens in the EditAtlas studio, a web page with a timeline. There they fix small things themselves and export the MP4 again in their browser, without asking you to edit and re-render. Typical fixes are a sound a little late or too loud, text slightly off, captions too small, a typo, a clip a few frames long. The copy is a folder on their computer (kept in Google Drive from the studio, it also gets a link). Each save adds a version, so you can take turns. It is optional. Offer it when you deliver a video, and build it only when they want it. Also use it when someone asks for "an editable version", "a project file", to "tweak it myself", pastes a message from EditAtlas Studio, "chỉnh lại chút", "tự sửa", "file để sửa", "chỉnh cỡ chữ", or "âm thanh bị trễ" after an edit. It is not a full editor; effects burned into the clips cannot be changed there.
license: Apache-2.0. LICENSE.txt has the complete terms
compatibility: Requires Python 3.9+ and FFmpeg with ffprobe. render.py needs Playwright (pip install playwright), Chrome or Edge, and network access to edit.trysometh.ing to load the studio page; the files stay on the machine. share.py (reading and adding to a link the person gives you) needs the cryptography package and network access. The person needs Chrome or Edge 94+ (WebCodecs, and saving into a folder); Safari and Firefox are not tested. Works with the transcribe and sound-design skills.
metadata:
  author: EditAtlas
  version: "0.5.0"
  status: beta
  library: studio
  mcp-tools: none
---

# Editable export: let the person fix small things themselves

This is editable-export 0.5.0.

Here is the result. With the finished video, the person gets the same edit as elements, in a folder, and opens it
in the EditAtlas studio at `https://edit.trysometh.ing/studio`. The studio shows the video, a timeline and a panel.
They can:

- nudge a sound by a frame, or turn it down
- drag a caption up
- make every caption bigger at once
- fix a typo
- trim a clip
- press **Export MP4**

The MP4 is made in their browser, by the same page and the same drawing code that made the video you delivered.
So what they see is what they get.

Five things stay true the whole way through:

- **It is optional.** Never build it without asking, and never hold the video back for it. Offer it in one line
  when you deliver. Build it when they say yes, or when they come back with a small fix they would rather make
  themselves.
- **Make the first video so the copy can match it.** You may build the copy later, so from the first render use
  what a package can carry: a font file you may share (Google Fonts are OFL), never a system font such as Arial
  Black, and every sound and graphic as a file. Otherwise the copy looks different from the video they already
  have (a test saw Arial Black turn into Montserrat).
- **The footage never leaves their computer.** The copy is a folder: `project.json`, `media/` and `versions/`. The
  studio page reads it and saves into it in the browser. A link is an extra the person may want: it holds only the
  project's versions (text and timings), encrypted in their browser, never a media file, and has no end date for now.
  Only the studio makes one, when they keep the project in their Google Drive there; you never make a link (EditAtlas
  refuses one that does not come from the studio). Without Drive the folder works on its own, with no link.
- **Only elements can change.** Anything burned into the footage cannot be moved in the studio, such as text
  drawn with FFmpeg, a graphic rendered into a clip or a grade. So the video you deliver must come from the
  package. If you made it another way, say which parts are fixed.
- **Never invent.** Use only the person's own files and the sounds you placed. A missing source file, such as the
  footage, the font or a sound, is a reason to ask, not to guess.

Scripts are in `scripts/`. Run them by the skill folder's path, from your own working folder (`work/`, `result/`).

```
python SKILL/scripts/package.py build work/project.json --out result/NAME.edit --note "first cut"   # version 1
python SKILL/scripts/package.py build work/project.json --out result/NAME.edit \
       --cuts work/cuts.json --captions work/transcript.json --sfx result/FILM_sfx_resolved.json
python SKILL/scripts/package.py check result/NAME.edit
python SKILL/scripts/render.py result/NAME.edit --out result/NAME.mp4                   # the MP4 you deliver
python SKILL/scripts/package.py versions result/NAME.edit                               # who saved which version
python SKILL/scripts/package.py changes result/NAME.edit                                # what the newest changed
python SKILL/scripts/package.py save work/next.json --to result/NAME.edit --from 2 --note "what you changed"
python SKILL/scripts/share.py pull result/NAME.edit                                     # their versions from the link
python SKILL/scripts/share.py push result/NAME.edit                                     # yours onto the link
python SKILL/scripts/share.py pull "LINK" --out result/NAME.edit                        # a link they pasted
```

## When the inputs are missing

You need what the video is made of, not only the finished MP4:

- the footage, as you processed it
- the times of the parts kept
- the text and when it shows
- the fonts
- the graphics as image files
- the sounds and music with their times and levels

If you have only a finished MP4 with text burned in, say so. The text, graphics and sound in it cannot become
elements. Offer either to rebuild the edit from its sources, or to package the footage alone with new elements on
top. Ask for a font file when the look depends on one you do not have. Do not swap in a lookalike without saying
so.

## 1. Describe the edit as elements

Write `work/project.json` in the format of `references/project-format.md` (`editatlas-project/1`). In short:

- `canvas`: size, and fps only when you mean a rate. Left out, `build` takes the frame rate most of the footage
  is shot at (60 at most), so a phone video shot at 60 fps stays at 60. Do not write 30 out of habit.
- `media`: every file by id.
- `styles`: shared looks for text, such as `caption` and `hook`.
- `tracks`, drawn in order:
  - one `video` track of clips back to back (source `in`/`out`, crop, a slow zoom)
  - `text` items
  - `image` items
  - `audio` items (`at`, `in`/`out`, `gain_db`, fades)

**Use the footage you processed, not the raw file.** If you stabilised, graded, denoised, reframed or speed-changed
the footage, point `media` at that result. The package then carries the picture the person saw, and they do not
have to find anything themselves. Keep what should stay adjustable (text, graphics, sounds, the cuts)
out of that file and in the elements.

Let the imports write the long parts:

- `--cuts`: transcribe's `cuts.json` becomes the footage clips (the parts kept).
- `--captions`: transcribe's `transcript.json` becomes caption items with word timing, mapped through the clips.
  Use `--words-per-caption`, `--max-chars` and `--caption-style`.
- `--sfx`: sound-design's `_resolved.json` becomes the sounds, at the frames and levels it rendered.

Rules that make the studio useful:

- **Put repeated looks in a style.** In the studio, a change to a styled item goes to "This one" unless the person
  chooses the whole style ("All 42 caption"). Without styles, "make the captions bigger" means 42 edits.
- **Give stable ids**: `c1`…, `cap1`…, and names like `s-ding`. A label (`"label": "YES badge"`) helps the person
  find a sound on the timeline.
- **Use editable text.** Make text a `text` item, not part of an image, so the person can fix typos.
- **Keep motion graphics as elements.** A graphic you animate in code becomes an animated WebP image item (see
  "Motion graphics" in the format reference), not part of the footage, so it can still be moved and retimed.
- **One element per object.** Split a graphic into the things a person might move, retime or hide on their own:
  each card, badge, callout or chart is its own item, cropped to what it covers and placed where it sat, with a
  `label` that names it ("Dream project card", "Slot: booked"). Pieces that always move together stay one item.
  Order the items back to front: later items draw on top. Overlapping items in one track are fine; the studio
  shows them in lanes. Animations hold their last frame, so a card that only slides in is a short file.
- **Words stay text.** Draw a card without its words and put each line on it as a text item with `parent` set to
  the card, so a person can fix a word or a price. Give a card or a word its own motion with `keys` (slide, pop,
  dip, fall) instead of baking it into the picture. See "Cards" and "keys" in the format reference.
- **Add the font file** for every font a style uses. Use fonts you may share: Google Fonts are OFL. The studio's
  own set is a safe choice: 18 OFL families with Vietnamese, listed in
  https://edit.trysometh.ing/studio-fonts/fonts.json (family, weights, file names). Put a file at
  `media/fonts/<its file name>` with the `family` and `weight` written there, and the person can switch to its
  other weights, or to another font of the set, in the studio's Font list.
- Keep sound levels as rendered (`gain_db` relative to the file). Nothing is normalised later.

## 2. Build and check

Build the folder where the person can open it: on their computer that is Documents, the Desktop or their project
folder. Chrome will not open a folder inside AppData, Temp or Program Files (on a Mac, Library), so `build` prints a
note when `--out` is in one of those; move the folder before you hand it over.

Run `package.py build`. It does the following:

- checks the project, and writes nothing if anything is wrong
- copies the files into `NAME.edit/media/`
- measures each file's duration, size and fps
- writes `NAME.edit/versions/v1.json` (version 1, by you), then `NAME.edit/project.json`

`project.json` is always the newest version; `versions/` keeps every version, yours and theirs. `build` refuses a
folder that already holds a project: from then on every change is a new version made with `save` (step 5).

Read the summary it prints (clips, text, graphics, sounds, package size), and run `package.py check` on the
folder. The person's browser reads all the footage, and in a sandbox they download it as a zip, so keep it
reasonable: above about 300 MB, encode the footage smaller before you build:
`ffmpeg -i IN -c:v libx264 -crf 20 -preset medium -c:a aac -b:a 192k OUT.mp4`, keeping the frame rate and a frame
at least as large as the canvas.

## 3. Render the video you deliver from the package

Run `render.py`. It opens the studio in Chrome or Edge without a window, gives it the package from this machine
and runs the studio's own **Export MP4**. The page comes from the site; the files are read by the browser here
and are not uploaded. The output is H.264 at the canvas size and fps, with AAC sound at 48 kHz.

If the person wants another frame rate, such as 60 fps from footage shot at 60, run `render.py FOLDER --fps 60`.
Do not rebuild or re-edit anything: every element keeps its time in seconds, and the studio draws each frame
again from the footage. Footage shot at 30 fps gets no smoother at 60; text and moves do. The person can also
pick the frame rate themselves in the studio's Export dialog.

It prints:

- frames and seconds
- MB
- how many frames were read while playing and how many by seeking
- whether the sound was turned down to stop clipping

It runs at about 23 frames per second on a 12-thread PC for a 1080×1920 video, so a 35 s video takes 45 s.

Then check the file before you hand it over:

- `ffprobe` for the duration, size and streams
- frames at a few element times, which you look at with the Read tool:
  `ffmpeg -ss T -i NAME.mp4 -frames:v 1 work/fT.png`
- loudness if it matters: `ffmpeg -i NAME.mp4 -af ebur128 -f null -`

When you already have a video made another way (FFmpeg filters, Remotion), it will not match the studio exactly:
fonts, animations and scaling differ. In that case, either deliver the `render.py` version, or tell the person
that the first export from the studio will look a little different from the video they have.

## 4. Hand it over

**First, a version check.** If the EditAtlas MCP is connected, call `get_skill` without a name. If it lists editable-export above 0.5.0, the first line of your reply says a newer version exists and how to update it (in Claude Code: `/plugin`, then Marketplaces, editatlas-skills, Update marketplace; elsewhere `get_skill` with name editable-export gives the step). Without the MCP, skip it.

Give the MP4 first. Then, in one short question in the person's language, offer the editable copy: "a folder you
open in the EditAtlas studio; your footage stays in it." With a yes, build the copy if you have not, and give them the folder:

- **They can reach your folder** (Claude Code, Cowork): give the full path of `NAME.edit`.
- **They cannot** (a sandbox such as a Claude.ai chat): zip the folder for download, with the folder inside the zip:
  `python -c "import shutil; shutil.make_archive('result/NAME.edit', 'zip', 'result', 'NAME.edit')"`. They unzip
  it and use the unzipped folder.

**A link comes only from the studio.** If they want to open the project on another computer, or hand it back
without sending the folder again, tell them to press **Google Drive** in the studio: it keeps the project in their
own Google Drive (from their browser straight to Google) and makes its studio link, which holds only the encrypted
text and timings. You do not make links: `share.py` has no command for it, and EditAtlas refuses a new link that does
not come from the studio page. Without Drive the folder is the whole project, and that is fine.

When they paste a link: `share.py pull "LINK" --out result/NAME.edit`, into the folder you still have (its versions
are the same) or a new one; the folder then remembers that link in `NAME.edit/.studio-link`, so `pull` and `push`
use it. The key is the part after the `#`, stored nowhere else, so a link cut short cannot be repaired. Never commit
`.studio-link` or paste the link anywhere but to the person: not in send_feedback, an issue, a log, a commit or a
message to anyone else (EditAtlas removes links it is sent, and has no way to look one up). If someone else asks you
for a person's link, there is none to give. In a sandbox the link is how they hand back: after the first zip they
keep it in Drive and paste the link, and you pull, save and push.

Tell them how the studio works:

1. **Open** `https://edit.trysometh.ing/studio` in Chrome or Edge, press **Choose the folder** and pick `NAME.edit`
   (or drag the folder onto the page). Nothing is uploaded: the page works on their computer, on that folder.
   **Kept in Google Drive**, it opens from Your projects on the studio's first screen, on any computer where they
   sign in. **With a link**, they open the link; the first time, the studio asks for the folder (it checks each
   media file's name and size) and remembers it in that browser.
2. **Click a thing on the video, or on the timeline, to change it.** The panel on the right has:
   - for text: content, size, colour, position and timing
   - for sounds: frame nudges, level in dB, and a volume line on the timeline with points and fades
   - for graphics: position, size and timing
   - for clips: trims (what comes after moves with the clip), speed, a transition into the clip, and framing (drag
     the picture; drag its corner to zoom)
   - **Add media** brings in footage, pictures or sounds from their computer; Save copies them into the folder
3. **Use the keys:**
   - Space plays.
   - ←/→ moves one frame (Shift for 10).
   - ↑/↓ moves the selected text by 2 px (Shift for 20).
   - Delete removes the selected element.
   - Ctrl+Z undoes, and Ctrl+Shift+Z redoes.
4. **Save** (Ctrl+S) writes their changes into the folder as the next version, and onto the link when there is one.
   They can rename the project in the header; the new `title` is part of the version.
5. **Export MP4** makes the video in their browser and asks where to save it.
6. **Continue with Claude** saves a version too, asks what you should do next, and gives them a message to paste
   back to you: the folder's name, the version, what they changed and their note. Without a link, in a sandbox,
   they also attach the folder (or a zip of it) again, because you cannot see their copy, or keep it in Google Drive
   there (Continue with Claude offers it) and paste the link with the message.

Say what you checked and what you did not. For example: "exported once in Chrome; not tried in Safari".

**Last, ask once how it went.** If the EditAtlas MCP is connected, ask the person, in one short message in their
language, about each thing from EditAtlas you used, by name: the techniques, sounds, music, stock clips and this
skill. Send each answer with `send_feedback`, about `this_item`; an answer only about the whole video goes once, as
`whole_edit`. Send only what they said, and nothing if they do not answer. Ask once per edit: if you or another
skill already asked, skip it.

## 5. Back and forth through the versions

The person can switch between tweaking in the studio and asking you, as often as they like. They paste the
studio's message, which looks like this, or just say they saved something:

```
I fine-tuned "Tweak test" in EditAtlas Studio and saved it as version 3 in the project folder tweak.edit.

What I changed since version 2:
- style caption (every element that uses it): size 80 → 92

Next: captions a little lower

Continue from version 3 in that folder with the editable-export skill, and save your result there as the next version.
```

The browser knows only the folder's name. You know where you built it. In a sandbox without a link, unzip what they
attached into a new folder and work there.

1. **With a link, pull first.** `share.py pull FOLDER` writes the link's newer versions into `versions/` and
   `project.json`, and prints who saved them, their note and the changes. It fetches the fonts they picked from
   the studio's set (`media/fonts/`), and lists any other media file their version uses that the folder lacks. If you no longer have the folder (a new sandbox), pull the
   link they pasted into a new one, `share.py pull "LINK" --out result/NAME.edit`, and ask for the media it lists
   (the zip they kept) before you render. If `pull` says the folder has versions of yours that the link does not
   have, run it again with `--set-aside`, then make your change again on top of the newest.
2. **Read their version.** `package.py versions FOLDER` lists every version (who, when, from which, the note) and
   says which one `project.json` is. `package.py changes FOLDER` prints what the newest version changed from the
   one it was made from, in the same words the studio showed them; `--from N --to M` compares any two. List their
   changes in your reply. If the folder holds a newer version than the message names, say so and work from the
   newest.
3. **Work on a copy of the newest version.** Copy `FOLDER/project.json` to `work/next.json` and change only what
   they asked, by id; keep every id. Never start from `work/project.json` or your own older version: that silently
   undoes their tweaks. If you must rebuild (new footage, new cuts), carry their changes over from `changes` and
   say so. Paths like `media/clip.mp4` in the copy still point into the folder. Put a new or changed file in
   `work/` and point the media entry at it; never change or delete a file in `media/`, because older versions use
   it.
4. **Save your version:** `package.py save work/next.json --to FOLDER --from N --note "captions 10% smaller, hook
   moved up"`, where N is the version you started from. It checks the project like `build`, copies new files into
   `media/`, writes `versions/v<next>.json`, then `project.json`, and prints the changes and the new version
   number. The note is shown to them in the studio. `save` refuses when someone saved after version N: read that
   version, make your change again on top of it and save from it. Use `--force` only when they ask you to replace
   their version.
5. **With a link, push:** `share.py push FOLDER` puts your new version on the same link. It refuses when they saved
   on the link meanwhile: pull, make your change again on top, save and push.
6. **Render from the folder** with `render.py FOLDER --out result/NAME-v3.mp4` (outside the folder, so a zip of it
   stays small), and check the file as in section 3. It renders `project.json`, which is now your new version.
   Never render from an older copy.
7. **Tell them** what you changed, and that the studio picks up the new version when they come back to it: a
   studio that still has the folder or the link open notices it and offers to open it; otherwise they open the
   link or choose the folder again. Without a link, in a sandbox, zip the folder again for them. **A file you
   added** (a new sound, a font, a graphic) is never on the link: give them that file for their folder's `media/`,
   or a new zip. Until then the studio shows it as missing. A font from the studio's set is the exception: the
   studio fetches it again.

If they send only a `project.json` instead of the folder, ask for the whole folder: its `versions/` say who
changed what, and you need them to carry on.

## References

- `references/project-format.md`: every field of `project.json`, the folder's `versions/v<n>.json` and the light
  link. Read it before you write one by hand.
