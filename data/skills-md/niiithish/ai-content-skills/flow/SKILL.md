---
name: flow
description: >
  Generate Google Flow images and videos with the local Labflow `flow` CLI. Use for
  Flow, Labflow, Nano Banana Pro, Nano Banana 2.1, Omni Flash, `flow image`, `flow images`,
  `flow generate`, `flow batch`, or `flow upsample`. Do not use for prompt-only requests
  targeting other engines.
---

# Flow

Run `flow` and deliver the requested media. Do not stop after writing a prompt unless the user explicitly asks for prompt text only. In a video project, `video-production` decides who runs what: the agent runs stills and 360p draft batches through `make.py` and reviews them; the user runs only the 1080p finals, from the command the agent gives.

## When a job is stuck or flow is broken

- There is no cancel command. Don't kill and relaunch in a loop.
- `NOT_FOUND` in the final summary: flow has already spent its one regeneration on another account, so rerunning unchanged won't help. Put a new `"seed"` on that job and rerun. Clips Flow's content filter fails after accepting them are no longer reported as lost: they come back as `UNSAFE_GENERATION` with Google's reason (see below).
- `BATCH_WORKER_FAILED`: rerun the same command.
- **No progress for about 10 minutes, or the same failure twice after following the hint: stop.** Tell the user at once, in a few lines they can hand to whoever fixes flow: the exact command, the last lines of output, the error code, and what looks wrong (a stuck profile lock, an expired login, a Google error). Don't keep waiting, work around it or offer a menu of options.

## Waiting on a run

- Run the `flow` (or `make.py`) command itself as the background task; the harness tells you when it exits. That is the only wait you need.
- Never poll with `pgrep -f`/`pkill -f` on a pattern: the waiting shell's own command line contains the pattern, so the loop never ends (video-3: two loops ran 2.5 hours, looking like a flow hang) and `pkill -f` kills the shell that started it. To wait on or stop a process, use its PID (`tail --pid=<PID> -f /dev/null`, `kill <PID>`).
- Before reporting done, check your background tasks and stop any of yours still running.
- For a quick look at what flow is doing (batch saved/total, jobs in flight, last error, free and premium credits as last seen), run `flow summary`. It reads local files only and never spends credits.
- Write each scene's stills or clips into a folder named for it (`-o scene-3/scene-3-v2.jpg`). The user's status bar groups jobs by folder, showing what is done and what is generating, so a folder per scene keeps that readable.
- `flow stop` stops every running flow command (not only yours) and closes Labflow's browser. Use it only when the user asks to stop everything; to stop your own run, `kill <PID>`. Accepted jobs resume on rerun.

## Let the CLI manage itself

Run the requested generation command directly. Labflow owns:
- session validation and repair, and recognised Google re-login
- credit checks and account selection
- project alignment (an account saved without a project takes the last one its Chromium profile opened) and browser reuse
- FIFO queueing and durable job resume

What not to do:
- A `PROJECT_MISSING` error naming an account means that account has no Flow project and Labflow can't create one. Tell the user to open a project in it and run `flow account add NAME --project UUID --force`; other accounts keep working.
- Do not preflight with `flow account ls`, `flow whoami`, `flow credits` or `flow doctor` unless the user explicitly asks for account diagnostics.
- Let flow pick the account, and don't set any env var to steer it. Stills cost no credits, so they use free and premium accounts alike. 360p drafts go to free accounts and fall back to premium only when no free account can take them (out of credits, refused). Native 720p goes to premium first, because only premium clips can be upscaled to 1080p. `--upsample` is premium-only. Do not run `flow account use`, `flow rotate` or `flow sync`, and never run `flow logout`, `flow account clear` or `flow account rm`: they remove saved logins. The one exception: when `flow accounts` shows the free accounts expired, run `flow account refresh` before a batch.
- Do not pass `--no-rotate` unless the user explicitly asks to lock one account. Normal generation leaves rotation on so depleted or unhealthy accounts are replaced automatically.
- Never expose or request session tokens, cookies, passwords, recovery data or vault credentials.

Only when the user names one account for a batch, add `--account NAME` to `flow batch` (or set `FLOW_ACCOUNT=NAME`; the flag wins). Every job then runs on that account alone, paid or free, with no rotation.

Treat queue and resume progress as informational, and let the command finish. Separate commands queue only for the submit itself: once Google accepts a job the next command starts, so a few `flow` commands from different agent sessions are fine. They submit one at a time through a single Labflow browser, so a short queue wait is normal. On `LOGIN_REQUIRED`, stop and tell the user a Google challenge needs manual completion. For any other failure, report the CLI's error code and hint instead of inventing a workaround or retry loop.

## Batches

For independent bulk jobs, use `flow batch` with one manifest entry per output. Do not launch many separate CLI processes.
- **Pacing:** the default is ten accepted jobs in flight (`--concurrency`, up to 20) and at most twelve new submissions per minute (`--rpm`, one every 5s), with per-account video-credit accounting. These are the defaults, so don't pass them. Within one batch, submits go one at a time; the clips then render in parallel.
- **Stills** render `--concurrency` at a time in the one browser, so `--rpm` is what caps a large still batch: at the default `--rpm 12`, 20 stills take under 2 minutes.
- **Sequencing:** keep review-dependent or sequential shots in separate batches.
- **Resume:** rerun the same batch after an interruption; completed outputs are skipped and accepted jobs resume. Rerunning approved 360p drafts at `720p` into the same output paths makes the 720p clips: a 360p file never counts as the finished 720p clip.
- **Uploads:** an account reuses its upload of the same reference image for 24 hours, so reusing reference files across commands is cheap. `flow batch` also sends the next jobs' references to the current account ahead of their turn ("sent ahead to accN" lines are expected, not an error). Do not wrap Flow commands in an external retry loop.

What the errors mean:
- Signed-out accounts are not empty accounts. `flow batch` and `flow images` renew stale saved sessions themselves and print `renewed N stale session(s)` or `N account(s) signed out (...)`. A QUOTA error with `details.signedOut` means those accounts' credits are unknown: run `flow account refresh --only accX` once, rerun the same command, and if one still fails tell the user to run `flow account open accX`. Never report that as "out of credits".
- A final `QUOTA` means the live account pool lacks enough credits. When every account is out (`details.allOut`, or `"outOfCredits": true` in a batch summary), stop and tell the user: Google refills free accounts daily, so ask them to run `flow account refresh` and then rerun the same command. Do not run the refresh yourself or retry in a loop.
- `TIMEOUT` means an accepted job may still be resumable.
- A clip Google drops, or leaves generating for 4 minutes, is regenerated once on another account in the same run (`lost by Google · regenerating on another account`). Let it run; don't stop or rerun the batch.
- If accepted media is lost on two accounts, `PROMPT_REJECTED` means rewrite or simplify the prompt.
- A refresh line saying an account needs login: tell the user to sign it in with `flow account open accX`; the other accounts keep working.
- `accX can't open Flow (Google's age check) · skipping it for a day`: flow already skips that account in later commands too. Tell the user once that the account needs its age check cleared (`flow account open accX`); don't remove it or work around it.
- `verification rejected on accX · trying another account` and `retrying accX in Ns` are flow handling Google's refusals itself. Let the batch run; never add your own wait or sleep before rerunning.
- `UNSAFE_GENERATION` means Google's safety filter blocked the prompt or a reference. The same prompt is rejected every time, and flow refuses to resend it, so rewrite the flagged wording (or swap the reference) and rerun.
  - Blocks found during rendering carry the reason in the error (`failed · UNSAFE_GENERATION (PUBLIC_ERROR_…)`) and the hint says what to change:
    - `IP_INPUT_IMAGE`/`IP_PROHIBITED` (Flow says "interests of third-party content providers… edit your prompt"): it's the start or reference image, not the prompt. Edit out whatever looks copyrighted or branded (or regenerate the still) and rerun; rewording alone won't help.
    - `IDENTIFIABLE_PERSON_SAFETY`: the prompt or reference reads as a real person.
    - `MINOR`/`CHILD_SAFETY`: a character reads as a child, so make the ages explicitly adult.
    - `AUDIO_FILTERED`: reword the dialogue.
    - `DANGER_FILTER`: tone down the action.
- `NETWORK` means Google answered slowly or not at all, not that the job failed. Rerun the same command once: accepted jobs are picked up without spending credits, and jobs that never went through are sent again. Stop and report only if the rerun fails with `NETWORK` too.
- A failed batch lists each job's `error` and `hint` under `failedJobs`; follow the hint.

Seeds:
- A job resumes by its prompt, ingredients and seed. After a lost job (`NOT_FOUND`), or to get a genuinely new take of the same prompt, set a new `"seed"` on it.
- Different seeds on the same prompt are the cheap way to get variants, but make one take unless the user asks for more.

```json
{"jobs": [
  {"id": "scene-1a-v1", "kind": "image", "prompt_file": "/ABS/scene-1a-v1.md", "aspect": "9:16",
   "ingredient": ["/ABS/sheet.png"], "output": "/ABS/scene-1a-v1.jpg", "seed": 12345},
  {"id": "clip-1a-v1", "kind": "video", "prompt_file": "/ABS/clip-1a-v1.md", "aspect": "9:16",
   "duration": 4, "resolution": "360p", "timeout": 900,
   "ingredient": ["/ABS/scene-1a-v1.jpg", "/ABS/sheet.png"], "output": "/ABS/clip-1a-v1.mp4"},
  {"id": "clip-1a-v1-final", "kind": "video", "prompt_file": "/ABS/clip-1a-v1.md", "aspect": "9:16",
   "duration": 4, "resolution": "720p", "upsample": "1080p", "timeout": 1500,
   "ingredient": ["/ABS/scene-1a-v1.jpg", "/ABS/sheet.png"], "output": "/ABS/final/clip-1a-v1.mp4"}
]}
```

Paths in a manifest may be absolute or relative to that manifest. An `upsample` job also saves `<name>-1080p.mp4` next to its output.

## Commands

```bash
# One image
flow image --prompt-file /ABS/scene.md --aspect 9:16 --ingredient /ABS/ref.png --name /ABS/scene.jpg

# A folder containing scene1.md, scene2.md, ...
flow images /ABS/scripts --out /ABS/images --aspect portrait

# Independent images/videos with different references and output paths
flow batch /ABS/jobs.json --continue-on-error
# ...all on one named account (only when the user asks for it)
flow batch /ABS/jobs.json --account acc8

# One video, optionally using existing stills as references
flow generate --prompt-file /ABS/clip.md --aspect portrait --duration 8 \
  --ingredient /ABS/scene1.jpg --ingredient /ABS/scene2.jpg \
  --name /ABS/clip.mp4

# One video that opens on an exact still (and optionally ends on another)
flow generate --prompt-file /ABS/clip.md --aspect portrait --duration 6 \
  --start-frame /ABS/first.jpg --end-frame /ABS/last.jpg --name /ABS/clip.mp4

# 1080p of an existing native 720p clip (Pro, free)
flow upsample MEDIA_ID --name /ABS/clip-1080p.mp4
```

Use absolute paths for prompt files, ingredients and outputs. Inspect every referenced still before writing a video prompt. Ingredients are identity and cut references, not start or end frames. For a clip that must open on an exact still, use `--start-frame` (plus `--end-frame` to land on another); in a manifest, `"start_frame"`/`"end_frame"` on a video job. Frames and ingredients can't be mixed in one clip, and `--end-frame` needs `--start-frame`. Tag them in a prompt as `@image1`, `@image2`, … in ingredient order when the shot needs an explicit reference. Up to 10 ingredients for an image and 7 for a video.

## Resolution and cost

- Videos use **Omni Flash 1.1** by default (cheaper): clips of 4, 6, 8 or 10 s. **Omni Flash 1.2** (`--model omni-1.2`) makes 3 to 15 s clips (at most 10 s with `--end-frame`) at a higher price, and only some accounts have it, so flow sends it only to those. With no `--model`, a length 1.1 lacks (3, 5, 7, 9, 11-15 s) goes to 1.2 and says so. Don't pass `--model` unless the user wants 1.2 or a length 1.1 can't make; `--model omni-1.2` fails with `MODEL_UNAVAILABLE` if no account has it, and `--model omni-1.1` never moves to 1.2.
- **Credits:**

  | Resolution | 4 s | 6 s | 8 s | 10 s |
  |---|---|---|---|---|
  | 360p draft | 4 | 5 | 6 | 7 |
  | 720p | 7 | 10 | 12 | 15 |

  Those are Omni 1.1 prices. Omni 1.2 (opt-in) costs more: 720p is 3 credits per second up to 10 s (4 s = 12, 8 s = 24, 10 s = 30) then 6 per second (15 s = 60); a 360p draft is 1 per second up to 10 s then 2 (4 s = 4, 8 s = 8, 15 s = 20).

  Stills cost nothing (there is a daily cap per account). `flow image` and `flow images` default to **Nano Banana 2.1** (`BELUGA`); pass `--model nano-banana-pro` only when the user asks for Pro.
- 1080p is a download upscale of a **native 720p** generation, free only on a paid account. A 360p draft cannot be upscaled, so a final reruns the same prompt at 720p with `--upsample 1080p`. That is a new generation and can differ from the draft; check it.
- Never request 1080p, 2K or 4K generation, and never invent endpoints.
- For story work, a single coherent multi-beat generation can replace several tiny clips. Project skills that lock one shot per clip (`video-production` and its style skills) take precedence.

## Prompt hygiene

- Never write "TikTok" or name any social app, phone interface or on-screen UI in a prompt: the model draws the app's buttons into the frame. Say "vertical short film" instead.
- Image prompts describe one composed frame, not a reference-sheet layout.

The CLI mints verification in a headed Chromium parked off the active screen, reuses it for nearby commands, and closes it automatically after a short idle period. Do not manage that browser between generations. `flow browser status` and `flow browser close` are only for diagnostics or explicit cleanup.
