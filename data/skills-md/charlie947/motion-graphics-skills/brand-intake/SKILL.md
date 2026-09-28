---
name: brand-intake
description: The setup step every other skill in this pack reads. A short interview plus 3 to 5 reference frames becomes two files in your project, brand.md (who you are, what you sell, your assets) and MOTION.md (your colours, type, timing and motion rules), plus a rule in CLAUDE.md so Claude reads them before it animates anything. Use at the start of any motion project, or when someone says "set up my brand", "brand intake", "build my motion design system", "make it look like my brand", "onboard me", "write my MOTION.md" or drops a batch of brand frames into chat.
---

# Brand intake

Every other skill in this pack reads the two files this one writes. Without them, Claude picks its own colours, its own type and its own idea of motion. Run this once per brand.

## Start straight away

When someone asks for this, your first message is the Batch 1 questions. No summary of the skill, no preamble.

## Step 1: The interview, in two batches

**Batch 1.** Ask these four together, then wait:
1. What is the brand called, and what do you do, in one line?
2. Who is it for? One sentence on the person watching.
3. What do you sell or promote in your videos? The offer, the product or the newsletter, with its real link.
4. What should people feel in the first second? Pick up to three: calm, premium, playful, urgent, technical, warm, bold.

**Batch 2.** Then ask these three, and wait:
5. Your colours as hex codes, your font names, and your logo files (SVG or PNG, attached). No hex codes? Say "sample them from my site" and give the link.
6. 3 to 5 reference frames: screenshots of motion you already like, from Dribbble, Pinterest or your own work. Put them in a folder called `examples`.
7. One thing your motion must never do.

If an answer is blank, ask for it once more, then move on. Never fill a gap with a guess.

## Step 2: Write brand.md

Save it in the project root, under 300 words:

```
# Brand

## Name and what we do
## Audience
## What we promote (with the real link)
## The feeling
## Assets
Colours (hex, typed by me or sampled from a named source), fonts, logo file names
## Never
```

## Step 3: Write MOTION.md from the frames

Read every frame in `examples`, then write MOTION.md with this brief to yourself:

```
Write one file called MOTION.md that any AI can read before it animates anything for me. It must cover:

1. Every colour as a hex code, and what each one is for
2. The fonts and the type sizes
3. Timing: how things come in, how long they hold, and how they leave
4. How things move: the frame rate, the easing, and anything that makes it feel handmade
5. Texture and finish
6. Five things my motion must never do, named plainly
7. One example, described shot by shot, of it done right

Work only from what is in the frames. Where you cannot tell, write ASK ME rather than guessing.
```

Show the user the file before you save it. Colours in brand.md win over colours sampled from a frame.

## Step 4: Add the read-first rule to CLAUDE.md

Create CLAUDE.md if it does not exist, and add this block word for word:

```
Before designing, generating or animating anything, read MOTION.md in full.

Every colour, font, timing and motion value comes from that file.

The file sets the look, not the ambition. When I say go all out, go all out.

If something I ask for is not covered there, ask me rather than choosing for yourself.

When you have finished, check your own frames against MOTION.md, fix what fails, and only then show me.
```

## What I learned the hard way

- **Mixed frames give mixed looks.** My five frames held four different looks. The file named all four and asked which to use. Pick one master look, or name which look goes with which job.
- **The ambition line is not optional.** Without "the file sets the look, not the ambition", my first try with the file came out far too polite.
- **ASK ME is a feature.** With the file in place, the one-line prompt stopped and asked a question before building. That is the file working.
- **Sampled hex codes drift.** A colour read off a JPEG is a few points out. Use the hex codes you typed wherever they exist.

## Step 5: Prove it (optional, two minutes)

Run the same one-line prompt twice, once in an empty folder and once in this project: "Make a dynamic 15-second motion graphics video that shows what an incredible motion designer you are. Go all out." Put the two side by side. Both should go all out. Only one should look like yours.

## Hand off

Tell the user brand.md, MOTION.md and the CLAUDE.md rule are in place, then list what to try next: `launch-video`, `vox-explainer`, `animated-chart`, `milestone-reveal`. Until both files exist, no other skill may call its result on-brand.
