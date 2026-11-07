---
name: tella-launch-video
description: Make a launch, promo or feature announcement video in Tella through the Tella MCP. Asks what is launching and what material exists, picks a launch shape (founder to camera with product graphics, product walkthrough, music-only trailer, vertical feature drop), plans it, then cuts, lays out, shows the product, adds proof, music and an end card, and checks every frame. Use when asked for a launch video, product video, promo, trailer, teaser, feature announcement or a video for a landing page or launch post.
---

# Make a launch video in Tella

A launch video makes one promise and proves it in the real product.

This skill needs the Tella MCP. If tools such as `get_timeline` are missing, follow the connection steps in the `tella` skill first.

## Scope

Ask, then show a plan and wait for a go before the first write. After the go, build it all and report. Edit a copy (`duplicate_video`) when the recording is used elsewhere.

## 1. Ask and pick the shape

Ask in one message, guesses filled in: what is launching and for whom, the one task to show done in the product, the material (recording, screen recording, screenshots, site, logo, brand colours), the voice, where it plays, and the call to action exactly as it should read.

| Shape | When |
| --- | --- |
| Founder to camera with product graphics | The user talks to camera; trust in a person matters |
| Product walkthrough | A screen recording of the real flow exists |
| Music-only trailer | No voice; a feed, a hero section or a teaser |
| Vertical feature drop | One feature for a social feed, 9:16, 15 to 40 s |

A vertical feature drop follows this skill's plan, build and end card at 1080×1920. From an existing talking recording, borrow `tella-short` for the 9:16 copy, captions, pace and phone checks; this plan replaces its segment pick, and the end card replaces its end-on-speaker rule. With no speaker (music and type, or screenshots), skip `tella-short`'s speaker rules.

## 2. Plan

Plan with `tella-plan-video` on this shape: hook (~10%, the product working or the need, never a logo first), problem (~15%, shown), reveal (~10%), proof (~40%, three to six actions in the product), payoff (~15%, the result at full size), ask (~10%). A long, loose take gets a short script to re-record rather than a cut. List each product shot as a zoom into the recording, a parallax shot of a screenshot (`tella-ui-parallax`) or redrawn UI that acts (`tella-ui-redraw`).

## 3. Build

1. Cut the speech (`tella-auto-cut`) and check every seam; launches have no room for a stumble.
2. Lay it out (`tella-auto-layouts`). On a founder launch the speaker stays visible most of the time; product shots sit beside them or in a split, full screen only for the payoff.
3. Product shots as planned, the first one built and checked, the rest made from it.
4. Proof, only what the user gives: a quote word for word with the person's name and photo; a logo wall from the brands' own files; a real number (`tella-data-callouts`); a before and after (the old way piling up, then the calm new way).
5. Type for the hook and the claim (`tella-kinetic-type`), transitions (`tella-transitions`), and the brand's background (`list_backgrounds`).
6. Music under the voice (`set_background_music`); sound effects only on visible actions.
7. End card (`tella-title-cards`): the logo from the brand's file, the call to action exactly as given, held at least 2 s.

Never invent a feature, screen, customer, logo, quote or number; put a labelled placeholder ("Screen: Billing → Invoices") and ask for the real one.

## 4. Check and report

Run the checks in `tella-motion-design`, plus: the hook reads muted in the first 3 s, each product shot matches its source, the face is never covered. Report the link, length, shape, one line per beat, placeholders still open, and what to listen to.
