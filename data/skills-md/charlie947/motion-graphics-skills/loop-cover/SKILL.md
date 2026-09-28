---
name: loop-cover
description: Turn a newsletter or blog cover into a seamless looping GIF at 896 x 640, 180 frames at 20fps. Only the one element you name moves, the loop is rotated so frame 1 shows the finished picture, and the seam is measured, not eyeballed. Use when someone says "animated cover", "make my cover move", "looping GIF cover", "newsletter cover GIF", "animate my thumbnail" or wants a cover that moves in the inbox without looking busy.
---

# Looping cover GIF

A cover that moves gets noticed in a feed full of stills. It only works if the move is small, the loop never jumps and the first frame still makes sense on its own.

**Before you start:** read `brand.md` and `MOTION.md` if they exist. If not, run `brand-intake` first, or ask for hex codes, a font and a logo file. Never call a result on-brand without them.

## Step 1: Ask for three things, then wait

1. **The cover.** A finished still (PNG) or a cover built in HTML. 896 x 640, or a larger image with the same 7:5 shape.
2. **The one element that moves,** named plainly. "The lighthouse beam." "The orange line drawing itself." "The lines between the cells."
3. **How it moves.** A pulse, a draw-on, a slow drift or a glow. One move, not three.

## Step 2: Build it

**If the cover is HTML:** animate only the named element as a pure function of time, add `window.seek(seconds)`, and capture 180 frames at 20fps (9 seconds).

**If the cover is an image:** animate the still in code. Make a mask of the named element by colour (for example every pixel where blue is much stronger than red), soften its edge a few pixels, and change only those pixels, frame by frame. Nothing outside the mask moves.

For both, use one clean sine cycle or one draw-on, hold and fade across the 9 seconds, so the last frame flows into the first.

**Rotate the loop so frame 1 is the finished picture.** Inboxes and link previews show frame 1 as a still. Frame i draws the moment `((i + offset) mod 180) / 20` seconds, where `offset` puts the fully drawn state first.

Encode with no dithering, because dither adds flicker to every frame of a flat image:

```
ffmpeg -y -framerate 20 -i f%03d.png -filter_complex "split[x][y];[x]palettegen=max_colors=128:stats_mode=full[p];[y][p]paletteuse=dither=none" -loop 0 cover.gif
```

## Step 3: Measure it

```
ffmpeg -v error -y -i cover.gif -vf scale=216:154,format=gray -f rawvideo frames.raw
python3 -c "
n = 216 * 154
d = open('frames.raw', 'rb').read()
f = [d[i:i + n] for i in range(0, len(d), n)]
diff = lambda a, b: sum(abs(x - y) for x, y in zip(a, b)) / n
print('frames', len(f))
print('seam', round(diff(f[-1], f[0]), 2))
print('excursion', round(max(diff(x, f[0]) for x in f), 2))
"
```

Targets from covers I shipped: 180 frames, a seam of 0.0 to 0.3, an excursion of about 0.7 to 2.8, and a file between 0.6 and 2.3 MB. An excursion near zero means nothing visible moves.

## What I learned the hard way

- **"You changed the image entirely."** My first GIF swept a band across the whole frame. Animate only the thing that was named.
- **A video model adds a camera move.** Told "camera holds completely still", it still pushed in. Animating the still in code is the only way to lock the camera.
- **Never measure motion at the halfway frame.** A sine is back at zero there, so a working animation reports no motion. Measure the biggest change against frame 0.
- **In ffmpeg's `eq` filter, add `eval=frame`,** or the expression runs once and nothing moves.
- **Shrink it to 240px wide and look again.** That is the size in an inbox. If the moving element disappears, it is too small.
- **Upload the GIF itself.** Some upload tools convert to PNG and the animation is silently gone. Check the uploaded link still ends in `.gif`.
