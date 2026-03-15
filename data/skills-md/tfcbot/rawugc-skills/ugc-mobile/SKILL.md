---
name: ugc-mobile
description: >-
  UGC video format templates for mobile app brands. Contains 15 TikTok-native,
  lofi video formats with shot-by-shot structure and AI video generation prompts.
  Focuses on the person and their physical relationship with their phone — reactions,
  rituals, and real moments — never screen content or app UI.
  Use when the user wants to create mobile app UGC content.
requires:
  env:
    - RAWUGC_API_KEY
compatibility: >-
  Use alongside the rawugc-api skill for API endpoint knowledge.
  Requires RAWUGC_API_KEY.
homepage: https://github.com/tfcbot/rawugc-skills
source: https://github.com/tfcbot/rawugc-skills
---

# Mobile App UGC Video Formats

15 lofi, TikTok-native video formats for mobile app brands. Raw, authentic, easy to produce. No hard CTAs — these feel like real people and their phones. The focus is always on the person, their reactions, and their physical rituals with the phone — never the screen content itself.

## How to Use These Formats

1. Identify the user's goal (app launch, feature highlight, onboarding showcase, social proof).
2. Select the format below that best matches.
3. Use the **Prompt Template** to compose the `prompt` field for `POST /videos/generate`. Replace `[BRACKETED]` placeholders with details from the user.
4. Default to `aspectRatio: "portrait"` (9:16) and `nFrames: "10"` unless the format specifies otherwise.
5. Keep the tone casual, genuine, unscripted. These should feel like someone naturally living with an app they love.

---

## Formats

### 1. Phone in Hand Reaction

**Vibe**: Holding phone, looking at screen (we don't see the screen), genuine reaction to what the app just did.

**Structure**:
- 0-3s: Person sitting on couch, phone in hand, tapping casually
- 3-6s: Expression shifts — eyebrows raise, mouth opens slightly, impressed
- 6-8s: Looks up at camera with a "wait, seriously?" expression, holds phone up (screen facing away)
- 8-10s: Nodding slowly, looking back at phone — convinced

**Prompt Template**:
> A person sitting on their couch, phone in hand, casually tapping. Their expression shifts — eyebrows raise, mouth opens slightly, genuinely impressed by what they see on [APP NAME]. They look up at the camera with a "wait, seriously?" expression, holding the phone up with the screen facing away from camera. Nodding slowly, looking back at the phone — completely convinced. Natural living room light, vertical video, authentic reaction energy. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "10"`

---

### 2. App Made Me Do This

**Vibe**: Showing a real result/action the app enabled — casual storytime.

**Structure**:
- 0-3s: Person talking to camera, casual energy — "okay so this app…"
- 3-6s: Showing the result on their phone screen or in real life
- 6-8s: Quick flash of the app interface that made it happen
- 8-10s: Genuine pride/excitement about what they accomplished

**Prompt Template**:
> A person talking casually to the camera about something [APP NAME] helped them accomplish. They show [RESULT — e.g. a completed project, organized data, tracked goal] on their phone screen, then flash the app interface briefly. Their expression is genuinely proud and excited — this app actually changed something for them. Selfie angle, natural light, casual setting, vertical video. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "10"`

---

### 3. The Morning Phone Grab

**Vibe**: First thing in the morning — reaching for phone on nightstand, opening the app that starts the day.

**Structure**:
- 0-3s: Nightstand with phone, alarm going off, hand reaches from under covers
- 3-6s: Picks up phone, squinting at brightness, adjusting
- 6-8s: A few taps, expression softens — the app they open first
- 8-10s: Sitting up in bed, phone in hand, ready to start the day

**Prompt Template**:
> A nightstand with a phone, hand reaching from under the covers to grab it. Squinting at the brightness, adjusting. A few taps and their expression softens — the calm of opening [APP NAME] first thing. Sitting up in bed, phone in hand, a peaceful start. Bedroom morning light, vertical video, quiet ritual energy. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "10"`

---

### 4. The Couch Scroll

**Vibe**: Casually scrolling on the couch, genuinely engaged with the app — the comfort zone.

**Structure**:
- 0-3s: Person lounged on couch, legs up, phone held at comfortable angle
- 3-6s: Scrolling with thumb, face showing genuine interest, occasionally pausing
- 6-8s: Small reactions — a smile, a head tilt, an exhaled laugh
- 8-10s: Shifts position to get more comfortable, still fully engaged

**Prompt Template**:
> A person lounged on their couch, legs up, phone held at a comfortable angle. Scrolling with their thumb through [APP NAME], face showing genuine interest, occasionally pausing. Small reactions — a smile, a head tilt, an exhaled laugh. They shift position to get more comfortable, still fully engaged. Living room, warm afternoon light, vertical video, cozy scroll energy. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "10"`

---

### 5. Told a Friend About It

**Vibe**: Talking to camera about recommending the app to someone — genuine word-of-mouth.

**Structure**:
- 0-3s: Face to camera, casual energy — "okay so I told my friend about this…"
- 3-6s: Gesturing while explaining what the app does, holding phone casually
- 6-8s: "And now they won't stop using it" — amused expression
- 8-10s: Holding phone up with a knowing look — "you're welcome"

**Prompt Template**:
> A person face-to-camera, casual energy — like they're telling a story about [APP NAME]. Gesturing while explaining, holding their phone casually in one hand. Amused expression — "and now they won't stop using it." Holding the phone up with a knowing look — the recommendation that stuck. Natural light, vertical video, word-of-mouth storytelling energy. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "10"`

---

### 6. The "I Forgot How I Lived Without This" Moment

**Vibe**: Talking to camera about life before vs after the app — casual, no screen shown.

**Structure**:
- 0-3s: Talking to camera, slight headshake — "I genuinely don't remember how I did this before"
- 3-6s: Holding phone, gesturing at it — explaining casually
- 6-8s: Emphatic expression — "it just handles it for me now"
- 8-10s: Setting phone down, leaning back — "can't go back"

**Prompt Template**:
> A person talking to camera, slight headshake — genuine disbelief. Holding their phone and gesturing at it, explaining casually how [APP NAME] changed their routine. Emphatic expression — "it just handles everything for me now." Setting the phone down and leaning back — can't go back to the old way. Natural light, sitting at desk, vertical video, honest testimonial energy. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "10"`

---

### 7. Phone Flat on Table

**Vibe**: Phone placed on table, person reacting to what it does while their hands are free — the app works in the background.

**Structure**:
- 0-3s: Person sets phone face-up on table, taps once, then pulls hands away
- 3-6s: Goes about their activity — cooking, reading, working — while phone sits there
- 6-8s: Glances at phone, quick satisfied nod — it's doing its thing
- 8-10s: Picks phone up briefly, smiles, sets it back down — effortless

**Prompt Template**:
> A person sets their phone face-up on the table, taps once, pulls their hands away. They go about their activity while [APP NAME] runs in the background. Glances at the phone with a satisfied nod — it's doing its thing. Picks it up briefly, smiles, sets it back down. Natural setting, warm light, vertical video, effortless background energy. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "10"`

---

### 8. Charging Nightstand

**Vibe**: End of day, phone going on charger, the app is the last thing used — bookending the day.

**Structure**:
- 0-3s: Nightstand, hand places phone on wireless charger
- 3-6s: Person looks at phone one last time — a content expression
- 6-8s: Reaches for lamp, clicks it off
- 8-10s: Settling into bed, the phone's subtle charging light visible in the dark

**Prompt Template**:
> A nightstand scene — a hand places the phone on a wireless charger pad. The person looks at the phone one last time with a content expression — done with [APP NAME] for the night. Reaches for the bedside lamp and clicks it off. Settling into bed, the phone's subtle charging light glowing in the dim room. Warm bedroom light transitioning to darkness, vertical video, end-of-day ritual energy. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "10"`

---

### 9. Waiting Room Scroll

**Vibe**: Using the app while waiting somewhere — making dead time productive or enjoyable.

**Structure**:
- 0-3s: Person sitting in a waiting area (dentist, salon, etc.), slightly bored expression
- 3-6s: Pulls phone out, starts using the app, expression brightens
- 6-8s: Completely absorbed, boredom gone, small smiles
- 8-10s: Looks up briefly as if called, puts phone away reluctantly

**Prompt Template**:
> A person sitting in a waiting room chair, slightly bored expression, looking around. They pull out their phone and start using [APP NAME] — expression brightens immediately. Completely absorbed, small smiles, boredom completely gone. They look up briefly as if their name was called, putting the phone away reluctantly. Bright waiting room, vertical video, productive dead-time energy. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "10"`

---

### 10. Coffee Shop Phone Moment

**Vibe**: Using the app at a coffee shop — the aesthetic of being out and connected.

**Structure**:
- 0-3s: Coffee shop table, latte in one hand, phone in the other
- 3-6s: Sipping coffee while using the app, relaxed expression
- 6-8s: Setting the coffee down, both hands on phone, leaning in with interest
- 8-10s: Leaning back, satisfied, coffee shop ambiance surrounding them

**Prompt Template**:
> A coffee shop table — a latte in one hand, phone in the other. Sipping coffee while using [APP NAME], relaxed expression. Setting the coffee down, both thumbs on the phone, leaning in with interest. Leaning back satisfied, coffee shop ambiance surrounding them. Warm cafe light, vertical video, curated moment energy. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "10"`

---

### 11. Convince Me in 15s

**Vibe**: Fast-paced screen recording hitting every key feature — rapid fire.

**Structure**:
- 0-3s: App opens, immediately jumping into Feature 1
- 3-6s: Quick tap to Feature 2, then Feature 3
- 6-10s: Feature 4 and 5, each getting ~2 seconds
- 10-15s: Back to home screen, the whole package visible at once

**Prompt Template**:
> A rapid-fire tour of [APP NAME]. The app opens and immediately dives into [FEATURE 1], then quick-taps to [FEATURE 2], [FEATURE 3], [FEATURE 4], and [FEATURE 5] — each getting just a couple seconds. The pace is fast but not frantic, each feature clearly visible. Ends on the home screen showing the full, clean interface. The energy is "here's everything, and it all just works." Screen recording style, vertical video, slightly sped up. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "15"`

---

### 12. The Double Tap

**Vibe**: Quick, decisive interaction — open app, do the thing, close it. Under 5 seconds of actual use.

**Structure**:
- 0-3s: Person pulls phone from pocket confidently
- 3-6s: Quick taps — purposeful, they know exactly what they're doing
- 6-8s: Done — slips phone back in pocket with a satisfied expression
- 8-10s: Carries on with their day, hands free — the task took seconds

**Prompt Template**:
> A person pulls their phone from their pocket confidently. Quick, purposeful taps — they know exactly what they're doing in [APP NAME]. Done in seconds — slips the phone back in their pocket with a satisfied nod. Carries on with what they were doing, hands free, task complete. Natural light, vertical video, quick-draw efficiency energy. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "10"`

---

### 13. Bedtime Last App

**Vibe**: In bed, phone propped on chest, the last app before sleep.

**Structure**:
- 0-3s: Person lying in bed, dim light, phone held above face
- 3-6s: Gentle scrolling or tapping, sleepy but engaged expression
- 6-8s: Eyes getting heavy, but still looking at phone with a small smile
- 8-10s: Phone drops to chest, eyes close — drifting off

**Prompt Template**:
> A person lying in bed, warm dim lamp light, phone held above their face. Gentle scrolling through [APP NAME], sleepy but engaged expression. Eyes getting heavy but still looking at the phone with a small smile. The phone slowly drops to their chest as their eyes close — drifting off. Bedroom, warm dim light, vertical video, late-night scroll energy. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "10"`

---

### 14. Phone Face-Down Focus

**Vibe**: Deliberately putting the phone face-down to focus, then picking it up as a reward — the app earned the break.

**Structure**:
- 0-3s: Person working at desk, phone beside them, screen visible
- 3-6s: Deliberately flipping the phone face-down — focus time
- 6-8s: After a beat of working, they flip it back over with a reward-energy
- 8-10s: Using the app briefly with a satisfied smile — earned it

**Prompt Template**:
> A person working at their desk, phone beside them. They deliberately flip the phone face-down — focus time. After working for a beat, they flip it back over with reward energy. Using [APP NAME] briefly with a satisfied smile — they earned this break. Desk setup, natural light, vertical video, work-reward balance energy. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "10"`

---

### 15. The AirPod Tap

**Vibe**: AirPod tap to interact with the app without looking at screen — audio-first experience.

**Structure**:
- 0-3s: Person walking/standing, AirPods in, one hand reaches up to tap the AirPod
- 3-6s: Listening, expression changes — reacting to audio content
- 6-8s: Nods along, mouths "yes" or smiles at what they're hearing
- 8-10s: Double taps AirPod again, keeps moving — hands-free, seamless

**Prompt Template**:
> A person standing, AirPods in, one hand reaches up to double-tap the AirPod. Listening intently, expression softening — absorbed in what they're hearing on [APP NAME]. Nodding along, a small smile. Double-taps the AirPod again, keeps going about their activity — hands-free, seamless. Natural light, vertical video, audio-first experience energy. [ADDITIONAL DETAILS].

**Settings**: `aspectRatio: "portrait"`, `nFrames: "10"`