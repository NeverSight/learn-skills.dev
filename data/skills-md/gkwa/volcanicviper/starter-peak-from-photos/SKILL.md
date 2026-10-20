---
name: starter-peak-from-photos
description: "Estimate when a sourdough starter peaked from the time-lapse photos in /Users/mtm/dcim2, measured from the feed time in the Zephyr bake log. Reports the peak time, how long after the feed it came, how long the starter held there, and how long ago it was. Use when asked to detect, find or estimate the starter peak from the images, photos or time-lapse, or when asked how long ago the starter peaked and no peak entry is in the bake log yet."
---

## Starter peak from photos

This skill estimates when the starter peaked by watching how high it rose in the jar across the night.

Read the zephyr skill first for the key scheme, the bake log filenames, and the event_time tags.

## Inputs

`zephyr` is required and has no default.

It accepts only the Zephyr key form, such as `5` or `3-2`.

The feed time is never typed by default.

It is the `event_time` of the feed starter entry in the bake log, resolved through the zephyr skill.

If no feed entry has a time, stop and ask for it.

## Before starting

Docker must be running, because ffmpeg runs in a container and is never installed on the host.

```sh
docker info --format {{.ServerVersion}}
```

If that fails, run `open -a Docker`, then check again.

The photos are in /Users/mtm/dcim2/OpenCamera, named `IMG_YYYYMMDD_HHMMSS.jpg`, one about every 2 minutes.

The camera is fixed on the jar, and frames are 720x1280.

Use the session scratchpad for every temporary file, or `mktemp -d` when there is none.

Docker cannot mount /Users/mtm/Downloads, so render into the scratch directory and copy out afterwards.

## Collect the frames

List the photos from the feed time onward, writing to a file in the scratch directory.

```sh
uv run --no-active --script /Users/mtm/pdev/taylormonacelli/volcanicviper/skills/starter-peak-from-photos/list_frames.py --start FEED > SCRATCH/frames-list.txt
```

FEED is the feed time as `YYYY-MM-DDTHH:MM:SS`.

The script reads the time from each filename, never from file dates and never from a fixed number of days, so a feed of any age is found.

It accepts `--end` with the same format, to stop at a later time such as when the starter was used, and `--frame-dir` to read another folder.

It prints nothing when no photo falls in the window.

Generate the ffmpeg script and manifest with the wackywolffish tool, using the feed time as the start.

```sh
uv run --no-active --project /Users/mtm/pdev/taylormonacelli/wackywolffish /Users/mtm/pdev/taylormonacelli/wackywolffish/gen_ffmpeg_script.py SCRATCH/frames-list.txt --sort-by timestamp --start FEED --script-output SCRATCH/run_ffmpeg.sh
```

FEED is the feed time as `YYYY-MM-DDTHH:MM:SS`.

Run the script from the scratch directory, because it writes `ffmpeg_list.txt` and `timelapse.mp4` into the working directory.

```sh
env --chdir=SCRATCH bash SCRATCH/run_ffmpeg.sh
```

The manifest `ffmpeg_list.txt` is what the measuring script reads, and `timelapse.mp4` is what the contact sheets are cut from.

New photos keep arriving, so the frame count grows while the starter is still rising.

## Look first

Build a contact sheet of every 20th frame to see the whole night at once.

```sh
docker run --pull never --rm --entrypoint /usr/local/bin/ffmpeg --volume SCRATCH:/work lscr.io/linuxserver/ffmpeg:latest -loglevel error -y -i /work/timelapse.mp4 -vf "select='not(mod(n,20))',scale=240:-1,tile=7x3" -frames:v 1 /work/sheet.png
```

Read the image.

The early evening frames have different lighting and framing, and the later ones are steadier.

## Measure the surface

The script prints the row of the starter's top edge in every frame, where a smaller row is a higher surface.

```sh
uv run --no-active --script /Users/mtm/pdev/taylormonacelli/volcanicviper/skills/starter-peak-from-photos/surface_height.py SCRATCH/ffmpeg_list.txt --frame-dir /Users/mtm/dcim2/OpenCamera > SCRATCH/surface.txt
```

Read the output file rather than printing it, because it has one line per frame.

Read the series with these cautions:

- A row stuck at 790 or at a constant low value means the edge was not found, which happens in the lit early frames, so ignore those stretches.
- The camera's auto-exposure shifts brightness in steps, which moves the detected row by 10 to 25 rows without the starter moving, so a single jump is not a rise until the photos show it.
- Slow drifts of a few rows are noise.
- The peak is the sustained minimum row, not a single frame.

## Verify by eye

Never report a peak from the numbers alone.

Cut the jar at the candidate peak and at four or five other times, such as one and two hours either side, and look at them together.

```sh
docker run --pull never --rm --entrypoint /usr/local/bin/ffmpeg --volume SCRATCH:/work lscr.io/linuxserver/ffmpeg:latest -loglevel error -y -i /work/timelapse.mp4 -vf "select='eq(n,A)+eq(n,B)+eq(n,C)+eq(n,D)',crop=490:330:130:420,scale=450:-1,tile=4x1" -frames:v 1 /work/key.png
```

A and so on are zero-based frame numbers, which are the manifest line minus one.

The peak looks like the highest, most domed and most bubbly surface, and the frames after the plateau look flatter.

If the eye and the numbers disagree, go with the eye and say so.

## Duration and temperature

The duration to peak is the peak time minus the feed time, written as `XhYm`.

The time since the peak is the current time from `date` minus the peak time.

Do not compute a temperature average here.

If one is asked for, use the bulk-ferment-remaining tools with the feed time as the start and the peak time as `--end`.

## Output

Print one plain line.

```
Zephyr 5; peaked about 4:35 AM; 9h33m after the 7:02 PM feed; held until about 5:45 AM; 4h32m ago
```

Add one short line only when the confidence is low, naming the reason, such as a frame stretch that could not be measured or a jump that may be a camera bump.

Round the peak to the nearest 5 minutes, because the data cannot support more.

Never write the result into the bake log unless asked.

When asked, add a starter peaked entry with an `event_time` tag and fill the `peaked` and `duration_to_peak` fields of the Starter peak duration block, following the zephyr skill.

## Errors

If Docker will not start, the photo folder has no frames since the feed, or fewer than 20 frames fall in the window, stop and say which.

State what was tried and the exact command and its output when a tool failed.
