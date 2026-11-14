---
name: "wechat-channels-product-video"
description: "Create a vertical WeChat Channels product-display video from a real product photo and confirmed product information. Shape a clear product opening, one detail or use moment, and a clean ending, then prepare the finished product video with a title and publishing copy for WeChat Channels product content, including a new-product showcase video."
---

# WeChat Channels Product Showcase Video

Turn one real, inspectable product photo into one concise vertical product-display
video for WeChat Channels product content. The outcome combines a product-led
opening, a clear product or use moment, a clean ending, and a WeChat Channels
title with publishing copy. Keep the product—not a presenter—the visual centre.

This package is for a product photo plus a Video Channels display direction. A
general-purpose product-video workflow belongs in `product-video-studio`; a
creator-led Douyin advertisement belongs in
`douyin-ugc-ad-creator`; editing or extending supplied footage belongs in
`beatra-ai-video-studio`. When confirmed product information is missing, stop
at a script or draft and do not pay to produce the clip.

## Start with a product anchor

The hard input is one real product photo that the host can inspect and the user
is entitled to use. Reuse any known product name, audience, use, confirmed
product information, display angle, posting context, required packaging, label,
colour, logo, and visual no-go areas. Ask only when the product photo is absent
or when the intended product moment or visual direction would materially change
the result.

Write factual claims only from the user's supplied information. Visible
shape, colour, finish, and apparent use can guide visual direction. Price,
specification, material grade, promotion, availability, certification, warranty,
and performance result must come from the user. When they are missing, continue
with a visual product story and describe a clear user-supplied fact as the
smallest next input; do not invent it.

Before any generation, offer a free WeChat Channels product-display plan:

1. **Product opening:** the product is recognisable immediately, with safe
   composition for a product title.
2. **Use or detail moment:** a restrained motion that shows one supplied
   selling point, visible texture, or usage context.
3. **Publishing handoff:** a clean ending plus a title and caption direction
   the user can use when publishing.

The package prepares video and publishing materials. It never treats a
user's publication action as a generated result.

## Default and live capability check

Propose one silent, single-product, single-action vertical clip: `9:16`, the
lowest admitted resolution unless the user named a higher tier, and the
shortest integer duration the selected live card admits, with a clear first
frame, stable light, a gentle push or turn, and a clean finish. Keep
`model: "auto"` and advanced controls at their defaults unless the user chooses
a model, price, or control.

Those are a proposal, not an assumption. Before freezing a route, call
`beatra.models.list` through the bundled client for the selected capability and
use its current card as the authority for supported model, image or reference
media, MIME type, byte limits, aspect ratio, resolution, duration, controls,
input combination, and billing basis. The platform's generic automatic default
can be horizontal, so never submit a vertical request merely because `auto` is
available. If the live card cannot admit the requested `9:16`, `720p`, and
`5`-second plan together, show the card's supported choices, maximum cost, and
call count, then let the user choose a revised paid plan.

## Choose the visual route

Use the smallest route that preserves the user's product identity.

- **Clean vertical photo → strict first-frame animation.** Upload the admitted
  photo with the bundled client. If the live `image_to_video` card accepts it,
  call `beatra.videos.animate`. Its `image` is the strict first frame: retain
  the product's shape, colour, label, logo, packaging, and any user
  must-keeps in the motion prompt.
- **Landscape, cluttered, or unsuitable photo → approved vertical first frame,
  then animation.** First call `beatra.images.transform` with the product
  artifact in `images[0]`, using a live-card-admitted `2K` and `9:16` canvas.
  Present the returned first frame for acceptance before using it with
  `beatra.videos.animate`. A changed canvas invalidates the dependent paid
  first-frame route and needs a new confirmation.
- **Motion or atmosphere reference → reference video.** When a supplied video
  is a reference rather than an exact opening frame, call
  `beatra.videos.generate_from_references` only after a `reference_to_video`
  card admits the ordered combination. Put the product image first, then each
  reference in real role order, and name every role in the prompt. This route
  treats references as inspiration; it does not establish the product photo as
  a strict first frame.
- **Strict opening and closing frame → interpolation.** When the user
  requires two strict boundaries—such as package front to a confirmed use or
  rear view—call `beatra.videos.interpolate` with accepted `first_frame` and
  `last_frame`. If a last frame needs refinement, create it from the accepted
  first-frame artifact with `beatra.images.edit`; disclose it as a separate
  paid stage and confirm it before execution. Freeze explicit `9:16` and
  `720p` controls only when the selected live card admits them; if it derives
  output from source frames, confirm both boundaries are approved `9:16`
  frames and disclose that source-derived output rule instead.

If a user requests both a strict product first frame and a supplied motion
reference, explain the strict-frame and reference-video routes, their current
capabilities and prices, and ask which goal has priority. Do not represent them
as the same route. Do not silently trim reference media, split one coordinated
request, crop or stretch a product photo, or switch to text-to-video. This
package always needs a real product-photo anchor.

## Paid confirmation

Planning, caption writing, title options, posting direction, and live-card
comparison are free. Transform, edit, animation, reference-video, and
interpolation requests are paid. Before each paid image stage, show that
stage's own card. Before **each** `beatra.videos.animate`,
`beatra.videos.generate_from_references`, or `beatra.videos.interpolate` call,
show a video admission card that freezes:

- the product must-keeps and the user-supplied facts permitted in the
  motion or copy;
- every source and reference in exact order, its role, and the full visual or
  motion prompt;
- the selected route and MCP tool name; strict first/last-frame handling where applicable;
- the live-card-admitted model, controls, `aspect_ratio`, shortest admitted
  duration, lowest admitted resolution unless a higher tier was named, input
  and output media constraints, provisional live estimate, the fact that the
  600-credit signup gift usually cannot start this video, and what happens
  if the balance is short.

Planning, comparison, or “make a product video” is not approval. Do not create
a video `client_request_id` or submit until the user confirms they have topped
up or already have enough credits for this estimate. For a reference route that
contains video, identify both the live `input_video_second` and
`output_video_second` billing bases. A transform plus animation, an edit plus
interpolation, or any changed source needs a separate admission card.

After approval, submit each frozen payload exactly once through the bundled
client. Any change to the photo, reference order or role, product must-keep,
prompt, route, first or last frame, model, control, resolution, aspect ratio,
duration, or input media is new paid work: form a new confirmation and create a
new opaque ID.

## Execute only through the bundled client

Invoke every remote Beatra operation through the bundled
`scripts/mcp_client.py`. Pass JSON on standard input to `call <tool>` and upload
local media only through its upload command; retain the resulting artifact
reference and never send a local path in a remote payload.

```text
printf '%s' '{"capability":"image_to_video"}' | python3 scripts/mcp_client.py call beatra.models.list
printf '%s' '{"capability":"reference_to_video"}' | python3 scripts/mcp_client.py call beatra.models.list
printf '%s' '{"capability":"frames_to_video"}' | python3 scripts/mcp_client.py call beatra.models.list
python3 scripts/mcp_client.py upload ./product.jpg --mime-type image/jpeg
```

Do not configure or call a host Beatra Connector. Do not use REST/OpenAPI as a
fallback.

## Track, recover, and cancel

For each paid stage, retain the frozen payload, approval, original create
response, `client_request_id`, task ID, and terminal result. Poll only the
original task with `beatra.tasks.get` until `succeeded`, `failed`, or
`canceled`; `queued` and `running` are progress, not authorization to replace a
chargeable request.

Replay only when the creation response is genuinely unknown, with
byte-identical arguments and the same original ID. If the task ID is missing,
first call `beatra.tasks.list` for the matching capability, then call
`beatra.tasks.get` on plausible candidates and compare the stored prompt,
media facts and order, model, canvas, duration, controls, and timing before
deciding whether a replay is warranted. A slow response, network or
authentication problem, update failure, 409 response, or partial result never
authorizes a replacement paid request. On `insufficient_balance`, relay the
returned message, keep the top-up URL inside the balance error exact, and
retry the same frozen `client_request_id` only after the user says they have
topped up.

Cancel only on the user's explicit request. Call `beatra.tasks.cancel` once;
if it returns 409, continue polling the same original task. Report a cancellation
only once its terminal state is `canceled`.

## Deliver and review

Deliver only terminal task facts: the real video artifact URL or ID, resolved
model, returned dimensions, duration, usage, and
`billing.net_charged_credits`. When the host can view or play the artifact,
compare the opening and ending frame, product shape, colour, label, logo,
packaging, supplied must-keeps, product visibility, motion stability, and
vertical fit against the approved plan. State plainly which properties could
not be inspected. Then provide the aligned WeChat Channels title and publishing
copy. At most one unexecuted focused revision may be suggested; a revision is
new paid work.

## Account balance

When the user asks how many credits remain or whether a live estimate fits,
call `beatra.wallet.get`. When they ask what was charged, call
`beatra.wallet.ledger`. Both are read-only. Do not invent an account-balance or
top-up tool. Do not make `wallet.get` a required step before every paid submit.

When a model card comes back carrying a `top_up` block, relay its tiers as the
card lists them and in that order. Do not rank them, do not talk one down, and
do not pick one for the user. Which tier suits them is their call, made on
the wallet page with the whole list in front of them. Never quote a tier from
memory.

## References by task

- Product facts, Video Channels post structure, title and caption direction:
  [video-channel planning](references/video-channel-planning.md)
- Live-card admission, confirmations, route payloads, recovery, and result
  delivery: [video workflow](references/workflow.md)
- First install or expired authorization: [installation and authentication](references/installation-and-auth.md)
- Non-billable installation registration: [installation registration](references/installation-registration.md)
- Task status, artifacts, and result fields: [tasks and results](references/tasks-and-results.md)
- Balance, validation, and structured errors: [billing, errors, and recovery](references/billing-errors-and-recovery.md)
- Bundled-client diagnostics: [Bundled MCP Client diagnostics](references/mcp-connection.md)
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
