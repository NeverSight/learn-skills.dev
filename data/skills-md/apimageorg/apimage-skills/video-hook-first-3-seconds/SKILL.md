---
name: video-hook-first-3-seconds
description: Design the opening 3 seconds of a short-form video, which decides whether the rest is watched at all. Use whenever the user is generating a TikTok, Reel, Short or ad video, mentions hooks or retention or scroll-stopping, or has video that gets impressions but no watch time.
---

# The First Three Seconds

On every short-form platform, the opening frames decide the outcome. Retention curves fall off a cliff in the first two to three seconds and the algorithm reads that fall-off as a verdict on the whole video.

Which means the hook isn't the intro to the video. **The hook is the video's audition**, and everything else only gets watched if it passes.

## What the first frame has to do

Three jobs, simultaneously, before anyone has decided to watch:

1. **Stop the scroll** — visual interruption, unexpected motion, or a face
2. **Establish stakes** — why this matters to *me*, right now
3. **Promise a payoff** — something is going to resolve, and I want to see it

A clip that opens on a slow establishing shot of a product on a white background does none of the three. It reads as an advert in about 400 milliseconds, and the thumb moves.

## Hook patterns that survive

| Pattern | Opening frame | Works because |
|---|---|---|
| **Mid-action start** | Already in motion, no setup | No dead frames. Motion holds the eye |
| **Result first** | The finished outcome, then "here's how" | Payoff promised immediately |
| **Problem in frame** | The visible mess, break or failure | Recognition. That's my problem |
| **Pattern interrupt** | Something visually wrong or unexpected | Curiosity is involuntary |
| **Direct address** | Face, eye contact, talking | Faces are pre-attentive. Hard to scroll past |
| **Extreme close-up** | Texture, detail, unclear at first | Ambiguity resolves at 2s, buying you the watch |
| **Countdown or list** | "Three things about..." | Structure implies a finite, worth-it commitment |

**Mid-action is the most reliable and the most under-used.** Most generated video opens on a static or slowly-moving establishing shot because that's what the prompt implied. Explicitly prompting for motion that's already underway at frame one removes the dead opening.

## Prompting for it

The default output of a text-to-video prompt tends to start calm and build. You have to ask for the opposite.

**Weak — starts static:**
```
A skincare bottle on a marble counter, camera slowly pushes in,
soft morning light
```

**Strong — starts mid-motion:**
```
Hands already mid-pour, cream falling from bottle to palm, motion
blur, close-up, camera locked. Action is underway at the first frame,
no lead-in
```

The phrases that do the work: *already mid-action*, *starts in motion*, *no lead-in*, *action underway at frame one*, *cut in on movement*. State them explicitly — the model will otherwise give you the establishing shot.

## The generation call

```
generate_video(
  mode="image-to-video",
  model="flux-3-video-draft",
  reference_images=["<product or scene still>"],
  prompt="Hands already mid-motion at frame one, no lead-in. Fast "
         "close-up, subject fills frame, natural motion blur. Camera "
         "locked, no drift. Energetic, handheld feel.",
  aspect_ratio="9:16",
  resolution="hd",
  duration=4,
  seed=1234
)
```

**Generate the hook as its own 4-second clip.** Not as the opening of a 15-second render. Reasons:

- Four seconds is the cheapest unit to iterate on
- You can test six hooks against one body for the price of two full clips
- Hooks are the highest-variance element, so they deserve the most iterations
- Assembling hook plus body is a cut, not a re-render

See `multi-scene-video-assembly` and `video-ab-testing-variants`.

## Test the hook in isolation

The hook is judged in isolation by the viewer, so judge it that way yourself.

Watch the first three seconds **muted, on a phone, at arm's length**, in a feed if you can simulate one. That's the real viewing condition. A hook that only works at full attention on a desktop monitor with sound isn't a hook.

Three checks:

1. **Muted test.** Most feed viewing starts silent. Does the opening make sense with no audio?
2. **Thumbnail test.** Freeze frame one. Would you stop on that image alone?
3. **Three-second cut.** Show only the first three seconds. Does someone ask what happens next?

If the answer to the third is no, the rest of the video doesn't matter yet.

## Common failures in generated video

- **The slow push-in opening.** The default, and the weakest. Prompt against it explicitly.
- **Text-on-screen doing all the work.** If the visual is inert and the hook is a caption, the visual is failing.
- **A logo in frame one.** Reads as an ad instantly. Brand later, once attention is earned.
- **Empty frames.** A composition with the subject small and lots of background has nothing to grab.
- **Motion that starts at second two.** The model rendered a lead-in you didn't ask it not to.
- **Beautiful but static.** Aesthetics don't stop scrolls. Motion and stakes do.

## Iterate on the hook, not the video

Once you have a body clip that works, treat the hook as the variable. Six hooks, one body, same seed on the body — that's six testable creatives for a fraction of six full renders.

The hook is where almost all the performance variance in short-form lives. Spend the iteration budget there.

## Don't

- **Don't open on an establishing shot.** Start mid-action.
- **Don't put the logo in the first second.**
- **Don't judge the hook with sound on at full attention.** Test it muted, on a phone.
- **Don't render the hook inside a long clip** while you're still iterating on it.
- **Don't rely on a caption to carry a static visual.**
- **Don't iterate the whole video** when the hook is the thing that isn't working.

## Setup

```bash
claude mcp add --transport http apimage https://mcp.apimage.org/mcp \
  --header "Authorization: Bearer sk_your_api_key" -s user
```

## Related skills

`tiktok-video-generation`, `multi-scene-video-assembly`, `video-ab-testing-variants`, `ugc-hook-library`
