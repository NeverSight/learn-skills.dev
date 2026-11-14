---
name: "ai-podcast-voiceover"
description: "Turn an article, notes, or a finished script into a listener-ready solo podcast episode with a consistent host voice. This AI podcast voice generator and AI podcast narration service adapts supplied material into a speakable podcast script, sets names and specialist terms for clear pronunciation, and creates MP3 podcast audio with natural pacing. Use this podcast voiceover AI and text-to-speech podcast service for article-to-podcast audio, news briefings, expert commentary, and knowledge shows, then carry the host direction into the next episode."
---

# AI Podcast Voiceover

Work as an episode producer for one recurring host: begin with the show
profile, turn supplied material or a named topic into a listener-friendly
script, freeze the host and model path, prove a new direction with a short
sample, then create and record the episode audio.

## Scope and routes

Use this workflow for supplied articles, notes, outlines, newsletters, or final
scripts, and for a topic alone, when they become a single-host podcast episode,
trailer, opener, closer, or ordered episode parts. Keep the recurring host
direction, pronunciation list, and delivery facts together when the show will
continue.

Route a manuscript or chapter-led course narration to
`ai-audiobook-narration`; a standalone short social, ad, or promo read to
`short-form-voiceover-audio`; supplied approved scripts across several
languages to `ai-multilingual-dubbing`; and a custom host voice or a mixed
voice project to `beatra-ai-voice-studio` and its focused cloning route. Keep
the supplied material, episode order, language, and show direction available
when changing routes.

This package delivers single-host episode audio. Route multi-host mixing, RSS
listing, and professional mastering out. When the user wants a music bed, keep
that work here — do not send it to another music package. When the requested
episode requires named speakers or a mixed or assembled final episode,
preserve that production requirement and choose the appropriate production or
editing route. Offer a solo host narration only when the user chooses that
smaller audio deliverable.

## Open the show

The hard inputs are the show and its audience: who is listening, and what this
episode should accomplish. Look first for `./<show>/show-profile.json` and
reuse that archive when it exists. Reuse the show direction only after its
frozen host is re-validated against the current voice list and model path. For
a new show, establish the intended listener, host, language, recurring opener
and closer, pronunciation list, and delivery convention in a user-owned
working directory. If a music bed is wanted, confirm the style and whether the
user accepts a paid generated track. Follow [the show profile](references/show-profile.md).

## Prepare the episode script

Accept an article, notes, an outline, a final script, or a topic alone and
adapt it into an episode that listeners can follow. Start from the show's
intended listener; if the supplied material could serve materially different
listener goals, ask for the intended takeaway before drafting. A topic alone
does not wait on that question: infer the listener and draft in the same turn.
Otherwise state the inferred episode focus in the draft for approval. When the user supplies
material, every fact, opinion, number, and claim in the spoken script comes
from that material or from an edit the user confirmed. An evergreen topic
alone is drafted from widely accepted general knowledge, and a time-sensitive
topic gets its opening, structure, transitions, and close without facts until
the user chooses sources or pastes material. The three-way rule is in
[episode script guidance](references/episode-script.md). If a supplied link or
file cannot be read, stop and ask for the text; never switch the topic or the
source. A topic-only request defaults to the bulletin tier, an estimated 3-5
minutes, and the user can choose a longer tier.

Show the episode focus and spoken draft section by section, including the
opening, closer, and pronunciation list, then wait for approval before audio
is proposed. If the user wants only a script, deliver the approved script and
stop. Use [episode script guidance](references/episode-script.md) for the
material boundary, listener focus, spoken adaptation, pronunciation, and
length handling.

## Freeze the host and model path

Use `beatra.voices.list` to compare available previews and freeze one opaque,
ready `voice_id`; submit that ID, never a display name. Without a live
result, do not name voices, models, prices, or previews; give the selection
criteria and say the pick comes from the live list. Call
`beatra.models.list` with `capability: "text_to_speech"` before deciding a
model, language, or price. An explicit model must be current, compatible with
the frozen voice, and support the target BCP-47 language. For `auto`, retain
only the live available models in
`models.list.auto.candidate_order ∩ voice.compatible_models`, preserving the
catalogue order. Use `auto` only when that set is nonempty and every member supports the
target language; a compatible live model outside `candidate_order` is an
explicit choice rather than an auto candidate.

Default to `model: "auto"`, MP3, speed 1.0, volume 1.0, pitch 0, no emotion,
and no explicit sample rate unless the profile or destination calls for a
supported change. Follow [voice, delivery, and recovery](references/voice-and-delivery.md)
for casting, live-card validation, the weighted-character counter, and
current price math.

## Golden path

Lock the show and its audience first. Write the episode for the ear. Prove the
direction with a short sample the user has heard. Then present the episode
synthesis confirmation card. When a music bed is wanted, present a separate
music-bed confirmation card after that — never fold `beatra.music.generate`
into the speech card. The direction is established only after the sample has
been heard.

## Before the connection is ready

When Allow is still pending at the end of a turn, finish and deliver
everything that needs no connection, in the format the user asked for:
the show profile, the full episode script, the pronunciation list, three
title options, the episode description and show notes, and estimated
chapters. Synthesis waits until after Allow. Say in one line
that Allow is the one-time sign-in that connects their Beatra account, not
an approval of the paid card, and that the paid step continues on their
next message after it. Do not fill the gap with another tool or service.

## Price and confirm

Script preparation, voice previews, current model discovery, and price
estimation are free. Every `beatra.speech.synthesize` request is paid. Every
`beatra.music.generate` request is a separate paid step with its own current
production card. Present a speech production card with the exact text, frozen
voice and settings, weighted-character total, live price calculation, expected
request count, one new opaque `client_request_id` for each logical request,
what the user keeps if they stop here, and how a short balance is handled.
When a music bed is confirmed, present a second card that freezes the music
prompt, style, model, and its own new opaque `client_request_id`. Do not
automatically retry either paid call. A changed argument needs a new
`client_request_id` and a fresh card.

On a first episode or after a voice, language, or control change, begin with a
small paid sample that combines the opener with the most demanding passage.
When an unchanged profile has re-validated, present the episode card directly.
The episode has its own approval; a sample approval never authorizes it. A
music-bed approval never authorizes speech, and a speech approval never
authorizes the music bed. A script above 50,000 characters uses approved topic
or section parts and the episode card lists every paid call.

## Create, deliver, and record

Lead the reply with the result and format the user asked for; the production
card, route choice, and cost notes follow it and never replace it.

On first use or after the package version changes, make a best-effort
non-billable installation registration. Its failure never blocks the episode
workflow.

Invoke every remote Beatra tool only through the bundled
`scripts/mcp_client.py`, with the tool name as the CLI argument and its
arguments as JSON on standard input. Do not configure or call a host Beatra
Connector, and do not use REST/OpenAPI as a fallback. Submit each approved
logical paid request once under its stable request ID, record its returned task
ID immediately, and poll that task with `beatra.tasks.get` until it is terminal.
When a music bed was confirmed on its own card, submit `beatra.music.generate`
once under that card's identifier after the episode speech is approved.

Deliver the returned episode audio with its real artifact ID, duration, MIME
type, sample rate when present, resolved model, usage, and returned billing
facts. With that audio, also deliver three title options, the episode
description, show notes, and chapters re-timed in proportion to the returned
duration; these text pieces add no charge. The closing only recaps what was
said. When a music bed was generated, deliver that clip the same way, as its
own artifact — do not claim a solo TTS file is a mixed final episode. When the host can listen, review the actual pacing, pronunciations, and
host fit; otherwise make the outstanding listening review explicit. If the host
has user-approved access to the show's working directory, append the delivered
episode record there; otherwise hand the same factual record and artifact URL
to the user for their own show ledger. For a lost task ID, reconcile through
`beatra.tasks.list` before considering an identical replay. Use the detailed
recovery route in [voice, delivery, and recovery](references/voice-and-delivery.md).

## References by task

- Drafting from material or a topic, approving sections, titles, notes, and
  chapters, or capturing pronunciations: [episode script guidance](references/episode-script.md)
- Starting a show, reusing a host, or recording an accepted episode and its
  one-line recap: [the show profile](references/show-profile.md)
- Choosing a voice and model, counting weighted characters, pricing a read,
  submitting audio, delivery, or recovery: [voice, delivery, and recovery](references/voice-and-delivery.md)
- First install or expired authorization: [installation and authentication](references/installation-and-auth.md)
- Non-billable package registration: [installation registration](references/installation-registration.md)
- Task polling, artifacts, and result fields: [tasks and results](references/tasks-and-results.md)
- Balance, validation, and structured errors: [billing, errors, and recovery](references/billing-errors-and-recovery.md)
- When the bundled client cannot connect: [Bundled MCP Client diagnostics](references/mcp-connection.md)
- Updates and security: [updates and security](references/updates-and-security.md)
- Removing the package or shared credentials: [uninstall and disconnect](references/uninstall-and-disconnect.md)

## Updates and security

This Skill runs only the files installed with it and leaves them unchanged while
it runs; it never downloads or executes other code. It talks to Beatra's official
services over HTTPS, and a file you choose to upload goes only to the one-time
upload address Beatra issues for it.

Once a day at most, the bundled client reads Beatra's public version list. When
the store or tool you installed from has a newer version, it prints one line with
the command that updates it there. Updating stays your choice, through that store
or tool. See [updates and security](references/updates-and-security.md).
