---
name: voicemail-script
description: "Use this skill when you need sales voicemails and LinkedIn voice notes that get remembered: \"write a voicemail script\", \"what should I say in a voice note\", \"voicemail for a cold call follow-up\". Writes 15-25 second scripts that tie to an email or message, give one reason to listen, and tell the prospect exactly what happens next. Includes versions for cold calls, post-email follow-ups, referrals, no-shows and LinkedIn voice notes."
license: MIT
metadata:
  title: Voicemail and voice note script
  category: multichannel
  tags: "SDR, Sales, Founders"
  author: prosyo
  version: "1.0.0"
  keywords: "sales voicemail script, cold call voicemail, linkedin voice note script, claude voicemail skill, voicemail that gets callbacks"
  inputs: "Situation, Related email or message, Prospect name and problem"
  outputs: "Voicemail scripts, Voice note scripts, Delivery tips"
---

Use this when a call goes to voicemail or when a LinkedIn voice note could stand out. Callbacks are rare; the real job of a voicemail is to make your next email or message recognised and opened.

## Inputs

- The situation: cold, follow-up to an email, referral, no-show, post-event.
- The email or message it pairs with.
- The prospect's name and the problem.

## The play

### 1. Keep the structure
1. Name and company (2 seconds).
2. One reason, tied to their situation (8-10 seconds).
3. What happens next: "I'll send you a short note today with the subject <x>" (5 seconds).
4. Number twice, slowly, only if a callback is realistic (5 seconds).

15-25 seconds total. Longer voicemails get deleted before the point.

### 2. Pair it with a written touch
Always send the email or message within an hour, and reference the voicemail in it ("Left you a quick voicemail about...").

### 3. Scripts by situation

**Cold, paired with an email**
> "Hi Maya, Sam from Acme. I work with finance leads whose month-end close drags because of approvals. I'm sending you a short note today, subject 'month-end close', with how Contoso got to 4 days. That's it, have a good day."

**Referral**
> "Hi Tom, Sam from Acme. Priya Shah suggested I reach out about your scheduling rollout. I'll email you a couple of times that might work. My number is 555 0134, again 555 0134."

**No-show**
> "Hi Ana, Sam here, we had 2 o'clock booked. No problem at all, I know days get away. I'll send a link to pick a new time that suits you."

**LinkedIn voice note (after a connection accepts)**
> "Hey Dev, thanks for connecting. Your post about ramping SDRs got me curious: do your new reps build their own lists, or does someone hand them accounts on day one? No pitch, genuinely curious how you run it."

### 4. Delivery
Stand up, smile, speak slower than feels natural, say the name correctly (check pronunciation if unsure), and record the voice note again if it sounds read.

## What good looks like

- Under 25 seconds, one reason, a clear next step.
- The paired email arrives the same day.
- The common mistake is the 60-second voicemail that pitches the product and lists features.

## Rules

- MUST keep voicemails under 30 seconds.
- MUST send the paired written touch.
- NEVER leave misleading voicemails that imply an existing relationship or an urgent account issue.

## Example prompts

- "Write voicemails for my 3-call cadence to IT directors."
- "Give me a LinkedIn voice note script for new connections who are VPs of Sales."
- "Write a voicemail for a prospect who missed our meeting."
