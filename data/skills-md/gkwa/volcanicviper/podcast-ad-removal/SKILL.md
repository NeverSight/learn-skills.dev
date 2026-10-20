---
name: podcast-ad-removal
description: Download a podcast episode, transcribe it, find the sponsor and ad blocks by reading the transcript, cut them out, and copy the ad-free MP3 into the Syncthing podcasts folder, which syncs to the Pixel's Audiobooks folder for playback in the Voice app. Takes the podcast name, and the most recent episode unless the user names a particular one. Use when asked to remove ads from a podcast, clean today's episode of a show, pre-download a podcast without ads, or run the ad cleaning for a named show.
---

## Podcast Ad Removal

The input is a podcast name.

The episode is the most recent one unless the user names a particular episode by title, number, or date.

If the user names an episode and it cannot be found in the feed, stop and say so.

Never substitute the newest episode for a named one that cannot be found.

Carry outputs forward and do not prompt the user between steps unless a step fails.

## Where things live

The project is steamysquirrel at /Users/mtm/pdev/taylormonacelli/steamysquirrel

It holds `transcribe.py`, `remove_ads.py`, `words.py`, `episodes_db.py`, `steptime.py` and `paths.py`, and a uv environment with faster-whisper installed.

Everything recorded about an episode lives in the SQLite database /Users/mtm/.local/state/steamysquirrel/episodes.db, in an `episodes` table with the feed metadata and cuts and a `step_events` table with the timings, so no run writes metadata or timing files.

The `finish` command also copies the database into /Users/mtm/.local/share/steamysquirrel/backups, which honors `XDG_DATA_HOME` and keeps the newest 14 copies, and `episodes_db.py backup` makes one on demand.

Each run gets its own directory under the XDG cache at /Users/mtm/.cache/steamysquirrel/runs, named by show slug and episode date, such as /Users/mtm/.cache/steamysquirrel/runs/aidailybrief-2026-10-15

The directory moves to the `XDG_CACHE_HOME` directory when that variable is set, and everything in it can be recreated, which is why it is cache and not part of the project.

The date is the episode publication date, which is not always today.

Create it with `paths.py`, which prints the new path and exits 1 when the directory already exists, and never write into a directory that already holds another run.

```
uv run --no-active --project /Users/mtm/pdev/taylormonacelli/steamysquirrel python /Users/mtm/pdev/taylormonacelli/steamysquirrel/paths.py --slug <show slug> --date <episode date>
```

Use the printed path as `<run dir>` in every later step.

## Timing every step

Every step is timed, because transcription time varies a lot with machine load and the durations are worth keeping.

The recorder is /Users/mtm/pdev/taylormonacelli/steamysquirrel/steptime.py, and it appends the step events to the `step_events` table of the database.

Wrap a command in the run subcommand, which records wall seconds and CPU seconds and passes the exit code through.

```
uv run --no-active --project /Users/mtm/pdev/taylormonacelli/steamysquirrel python /Users/mtm/pdev/taylormonacelli/steamysquirrel/steptime.py run --run-dir <run dir> --step <step name> -- <command>
```

For a step that is your own reading and not a command, bracket it with the begin and end subcommands using the same `--run-dir` and `--step` flags.

Use these step names so runs compare: `feed`, `episode`, `download`, `metadata`, `transcribe`, `find ads`, `place edges`, `cut`, `name`, `sync`.

The `find ads` step covers reading the transcript and `place edges` covers the word-level windows.

The run directory needs the episode date, so the first lookup happens before the directory exists.

Do the iTunes search and a scratch download of the feed into $CLAUDE_JOB_DIR/tmp, read the date from it, create the run directory, and then record `feed` by downloading the feed again into the run directory under the run subcommand.

The `episode` step is then skipped, because the choice was already made during the lookup, and the report says so.

## Step 1: Find the feed

Look the show up with the iTunes search API.

```
curl --silent "https://itunes.apple.com/search?term=<url encoded name>&entity=podcast&limit=5"
```

Pick the result whose `collectionName` and `artistName` match the requested show.

Several unrelated shows often share a similar name, so check the artist and the genre before choosing.

A show can also have a second feed for Patreon early releases.

Never use a feed URL that carries an `auth=` token, which is a private Patreon feed.

If no result matches, stop and report the candidates.

Download the feed with curl and the location flag into the run directory as feed.xml.

## Step 2: Pick the episode

Parse the feed and sort the items by `pubDate`, newest first.

Feed order alone is not reliable, because reruns and bonus items are interleaved.

For the default case take the newest item.

For a named episode match on title, episode number, or publication date against every item.

The title can carry the number, as in `#69 Tamara`, and the `itunes:episode` tag can disagree with it, so match on the title first.

Show the user the chosen title, date, and duration in one line before continuing.

## Step 2b: Stop when the episode was already done

Check the chosen episode against the episodes database before creating the run directory, using the scratch feed from the lookup.

```
uv run --no-active --project /Users/mtm/pdev/taylormonacelli/steamysquirrel python /Users/mtm/pdev/taylormonacelli/steamysquirrel/episodes_db.py check <scratch feed> --slug <show slug>
```

Add `--title <substring>` when the user named an episode, so the check matches the one chosen in step 2.

The command prints nothing and exits 0 for a new episode, and it exits 3 with the earlier run directory and output path when the episode was already processed.

On exit 3 stop, report the earlier run directory and output path, do not create a run directory, and ask the user before redoing the episode.

The database is /Users/mtm/.local/state/steamysquirrel/episodes.db, or under the directory in `XDG_STATE_HOME` when that variable is set.

## Step 3: Download

Download the item enclosure with curl and the location flag, because the URL often goes through tracking redirects, and wrap it as the `download` step.

Confirm with `file` that the result is audio and not an error page, and probe the duration with ffprobe.

Compare the downloaded size with the enclosure `length` attribute when the feed provides one, and skip the comparison when the length is 0.

Stop when the file is smaller than the feed length or is not audio.

A file larger than the feed length is expected when the host stitches ads in at download time, which Omny and Audioboom feeds do.

In that case the ffprobe duration exceeds the feed duration by roughly the length of the ads, which is the content this skill removes.

Continue, and say in the final report that the size did not match and why.

## Step 3b: Write the episode metadata

The Voice app on the Pixel reads the title, artist and album from ID3 tags embedded in the MP3, and it falls back to the filename when there are none.

ffmpeg copies the source tags through the cut, so a feed that ships tagged files, such as Audioboom, keeps them, and a feed that ships untagged files, such as anchor.fm, produces a file that Voice shows under a random name.

Always write the tags from the feed item, which is the one source every feed has, and wrap it as the `metadata` step.

```
uv run --no-active --project /Users/mtm/pdev/taylormonacelli/steamysquirrel python /Users/mtm/pdev/taylormonacelli/steamysquirrel/steptime.py run --run-dir <run dir> --step metadata -- uv run --no-active --project /Users/mtm/pdev/taylormonacelli/steamysquirrel python /Users/mtm/pdev/taylormonacelli/steamysquirrel/episodes_db.py begin <run dir>/feed.xml --slug <show slug> --run-dir <run dir>
```

Voice shows the album tag as the episode name, so the stored album is a short date and the title, such as `10-19-26 The AI Wealth Problem`, which tells episodes of one show apart.

Add `--title <substring>` when the user named an episode, so the item matches the one chosen in step 2.

The `episodes` row for the run holds the show name, title, artist, album, date, a cleaned description, the feed duration, the guid, the link, the copyright, the artwork URL and a `filename` stem such as `aidailybrief-2026-10-18-a-potentially-historic-ai-breakthrough`.

Read one stored field when a later step needs it, such as `filename` or `artwork`.

```
uv run --no-active --project /Users/mtm/pdev/taylormonacelli/steamysquirrel python /Users/mtm/pdev/taylormonacelli/steamysquirrel/episodes_db.py get <run dir> <field>
```

The `filename` stem contains only lowercase letters, digits and hyphens, because Android rejects `? " : * < > | \` in names.

## Step 3c: Fetch the cover art

Voice shows the embedded cover picture beside each episode, and it shows a placeholder disc when there is none.

The `artwork` field of the stored row holds the artwork URL, which is the episode's own image or else the show's image, and `get <run dir> artwork` prints it.

Download it into the run directory as `cover`, with no extension, because ffmpeg reads the type from the content.

```
curl --silent --show-error --fail --location --output <run dir>/cover <artwork url>
```

Confirm with `file` that the result is an image.

Skip the step and say so in the report when `artwork` is empty.

## Step 4: Transcribe

Run the transcription in the background as the `transcribe` step, because it takes a while on this machine.

```
uv run --no-active --project /Users/mtm/pdev/taylormonacelli/steamysquirrel python /Users/mtm/pdev/taylormonacelli/steamysquirrel/steptime.py run --run-dir <run dir> --step transcribe -- uv run --no-active --project /Users/mtm/pdev/taylormonacelli/steamysquirrel python /Users/mtm/pdev/taylormonacelli/steamysquirrel/transcribe.py <run dir>/episode.mp3 <run dir>/transcript.json
```

Compare the recorded wall time with the episode duration and report the ratio, such as 2.2x faster than real time or 1.3x slower than real time.

The defaults are the small.en model with greedy decoding, which is about twice as fast as beam search for 98.8% text similarity.

Do not poll or sleep while waiting, and continue when the completion notice arrives.

Wall time stretches a lot when the machine is loaded, so expect roughly 24 CPU minutes for a 30 minute episode and report that if the user asks.

## Step 5: Find the ad blocks by reading

Detection is reading the timestamped transcript, because pattern matching alone was wrong on two of three shows tried.

Search the transcript for ad-like lines to find where to look.

```
uv run --no-active --project /Users/mtm/pdev/taylormonacelli/steamysquirrel python -I -c "import json,re; d=json.load(open('<run dir>/transcript.json')); p=re.compile(r'sponsor|brought to you|promo code|use code|\.com|\.ai|patreon|ad-free|free at|slash|offer|iheart|learn more|terms|wherever you get|free trial|visit', re.I); [print(round(s['start'],1), round(s['end'],1), s['text']) for s in d if p.search(s['text'])]"
```

The hits cluster, and each cluster is one pod, so print the segments around each cluster and read them to decide the start and end of each block.

Repeated lines are a strong signal, because the same read often appears in several pods of one episode.

Some ads carry no keyword, such as a podcast promo or a story told in the host's voice, so read the whole gap between the keyword hits and the content on both sides.

What an ad block looks like:

- Ads are back to back with no speech gap between them, so a gap is not an edge.
- The edge is a topic change, such as a read that begins mid-sentence in content that was about something else.
- A block can start immediately after a host line like "Next up, the main episode" or "words from our sponsors".
- Content often resumes mid-sentence after dynamically inserted ads.
- The same read can appear more than once in one pod.
- A pod can also sit before the show starts and after the sign-off.
- A sponsor thanks, Patreon plug, or house promo in the intro counts as an ad block.
- A network tag such as "This is an iHeart podcast" belongs to the pod around it.

What is not an ad:

- A joke in the content that uses ad words, such as "Brought to you by Shopify" after a cash register sound.
- The host discussing a company in the story.
- The host's own lead-in before a break, such as "Right after the break", and a teaser line after it.
- The host's sign-off, including a social handle and "back in two weeks", which is the show and not a read.

Keep the host's "Welcome back" line when it follows the ads.

Use the regex helper only as a hint.

```
uv run --no-active --project /Users/mtm/pdev/taylormonacelli/steamysquirrel python /Users/mtm/pdev/taylormonacelli/steamysquirrel/remove_ads.py <run dir>/transcript.json
```

Its ranges can swallow real content or run to the end of the file, so never cut with them unchecked.

## Step 6: Place the edges precisely

Transcript timestamps are per segment, and a long segment can hold both content and ad, or a few words and a long stretch of music.

Get word-level timing for every edge that falls inside a segment, and for any edge where an ad ends in the same second a content line begins.

Pass all the windows of about 15 to 30 seconds to one invocation, so the model loads once.

```
uv run --no-active --project /Users/mtm/pdev/taylormonacelli/steamysquirrel python /Users/mtm/pdev/taylormonacelli/steamysquirrel/words.py <run dir>/episode.mp3 68:92 1930:1972
```

The helper is /Users/mtm/pdev/taylormonacelli/steamysquirrel/words.py, and it prints a start, an end, and a word per line in episode seconds.

Run it as a script and not with `-I`, because it imports `transcribe` from its own directory.

Place the cut start just after the last content word, and the cut end before the first content word that follows.

When there is silence or music between the ad and the content, put the edge inside that gap with about a second of margin on each side, and do not cut right against a word.

A pre-roll starts at 0 and ends before the first content word.

A post-roll starts after the sign-off, and its END is `end`.

## Step 7: Cut

Pass each verified block as a `--range START:END` flag, where END can be `end` for a post-roll, and wrap it as the `cut` step.

```
uv run --no-active --project /Users/mtm/pdev/taylormonacelli/steamysquirrel python /Users/mtm/pdev/taylormonacelli/steamysquirrel/steptime.py run --run-dir <run dir> --step cut -- uv run --no-active --project /Users/mtm/pdev/taylormonacelli/steamysquirrel python /Users/mtm/pdev/taylormonacelli/steamysquirrel/remove_ads.py <run dir>/transcript.json --audio <run dir>/episode.mp3 --output <run dir>/episode.clean.mp3 --run-dir <run dir> --cover <run dir>/cover --range 35.2:76.3 --range 752.2:923.4
```

Then probe both durations with ffprobe and confirm the difference equals the total of the ranges.

The ffmpeg on this machine is a Docker shim, so Docker Desktop must be running.

Start it with `open -a Docker` when ffprobe or ffmpeg reports that it cannot connect to the Docker daemon.

Pass `--cover` only when step 3c produced a cover, and then confirm with `ffprobe -v error -show_entries stream=codec_type,codec_name` that the output has a video stream, which is the embedded picture.

Probe the tags on the output with `ffprobe -v error -show_entries format_tags -of default=noprint_wrappers=1` and confirm the title, artist and album are present.

## Step 7b: Name the deliverable

Give the cleaned file its descriptive name, so a player that ignores ID3 tags still shows something readable, as the `name` step.

Read the `filename` stem with `episodes_db.py get <run dir> filename`, and copy `episode.clean.mp3` to `<run dir>/<filename>.mp3`.

The cuts are recorded in the database by the `finish` command in step 8, so no file is written for them.

Use the descriptive MP3 name for every later step, and keep `episode.clean.mp3` as the working copy.

Voice caches an episode's tags and cover by filename, so a re-cut of an episode already on the phone needs a new filename, such as a `-v2` suffix, in /Users/mtm/podcasts.

## Step 8: Copy into the Syncthing folder

Copy the cleaned file into /Users/mtm/podcasts, as the `sync` step, and let Syncthing carry them to the phone.

Never push over adb, because Syncthing replaces it and needs no pairing code.

The Syncthing folder with id `podcasts` is send only on the Mac at /Users/mtm/podcasts, and receive only on the Pixel 9a at /sdcard/Audiobooks.

Name the file with the `filename` stem from step 7b, which starts with the show slug and episode date so episodes sort and never collide.

```
cp <run dir>/<filename>.mp3 /Users/mtm/podcasts/<filename>.mp3
```

Verify the copy by comparing the sizes of the two files on the Mac.

```
stat --format %s <run dir>/<filename>.mp3
```

```
stat --format %s /Users/mtm/podcasts/<filename>.mp3
```

The `stat` on the Mac is the GNU one, so the BSD `-f %z` form fails.

Mark the run finished in the database only after the sizes match, so a failed run is never counted as done, and pass every cut range so they are stored with the episode.

```
uv run --no-active --project /Users/mtm/pdev/taylormonacelli/steamysquirrel python /Users/mtm/pdev/taylormonacelli/steamysquirrel/episodes_db.py finish --run-dir <run dir> --output /Users/mtm/podcasts/<filename>.mp3 --range 35.2:76.3 --range 752.2:923.4
```

Syncthing notices the new files within about 10 seconds and sends them when the phone is reachable, so delivery is asynchronous and the step does not wait for it.

Check whether the phone is reachable now with the connections listing, and look for the Pixel 9a device id XEEMPOJ-KBKPGKD-QO6MHQ7-MSSHV24-JN6MCSU-O6VFGFR-JSD5FIO-QD36LQS with `connected` true.

```
syncthing cli --home "/Users/mtm/Library/Application Support/Syncthing" show connections
```

If it is not connected, the files stay in /Users/mtm/podcasts and arrive when the phone is on the home Wi-Fi with Syncthing-Fork running, so say that in the report and do not retry.

Do not tell the user the file is on the phone, because nothing here confirms arrival.

The phone folder is receive only and shows Local Additions for files the Mac does not have, such as episodes pushed earlier.

Never tap Revert Local Changes on the phone and never ask the user to, because it deletes those files.

Do not use adb or open apps on the phone for this step.

## Fallback host

Use a temporary host only when the user asks for a link, or when Syncthing cannot be used and the user chooses a host.

The default host is Litterbox with a 72 hour expiry, as the `upload` step.

```
uv run --no-active --project /Users/mtm/pdev/taylormonacelli/steamysquirrel python /Users/mtm/pdev/taylormonacelli/steamysquirrel/steptime.py run --run-dir <run dir> --step upload -- curl --silent --show-error --fail --max-time 600 --form reqtype=fileupload --form time=72h --form fileToUpload=@<run dir>/<filename>.mp3 https://litterbox.catbox.moe/resources/internals/api.php
```

The upload URL is printed by curl, so read it from the command output.

Litterbox replaces the filename with a random id, so the downloaded file is named after the id and Voice shows the ID3 title and artist from step 3b instead.

Tell the user the filename to give it when moving it into the Audiobooks folder, which is the `filename` stem from step 7b.

The fail flag matters, because without it a 500 error page is saved as the result and the exit code is still zero.

Litterbox has returned a 500 on every attempt for hours at a time, so retry once under the step name `upload retry`, and then stop and say the Syncthing copy is already the delivery path.

```
curl --silent --head --location https://litter.catbox.moe/<id>.mp3
```

Confirm `content-type: audio/mpeg`, a `content-length` equal to the local file size, and `accept-ranges: bytes`.

Never use an ad-supported file host such as tmpfiles.org, because its download page redirected the user's phone to a scam page that asked them to install a VPN profile.

Never switch to a different public host without asking, and never use a permanent one, because the file is someone else's copyrighted audio.

## Final report

Lead with where the file is, which is the path under /Users/mtm/podcasts that Syncthing syncs to the Audiobooks folder on the phone, or a bare link for a fallback host.

Say whether the phone was connected at the time of the copy, and that arrival on the phone is not confirmed.

Then report:

- The episode title and publication date
- Duration before and after, and the total removed
- Each cut range as clock times
- The output of `steptime.py report --run-dir <run dir>`, which lists every step with wall and CPU time, and the real-time ratio for transcription
- Whether the download size matched the feed, and why not when it did not
- The ID3 tags written and the cover that was embedded, if any
- That the cut points were not listened to, and which joins are worth checking, such as an edge placed inside silence or music

To listen in Voice, tell the user to open the Audiobooks folder in Voice, where the episode appears.

The Download folder cannot be picked as a library folder.

For a fallback link, tell the user to open it in Chrome, download it, move it into the Audiobooks folder with the Files app, and open that folder in Voice.
