---
name: build-personalized-travel-guide-open-source
description: Build a complete personalized eight-module travel-handbook webpage from user preferences and destination research, with itinerary, routes, sights, shopping, experiences, food, preparation, language, local notes, Google Maps links, responsive HTML and practical interactions.
---

# Build a complete travel handbook

Create a destination-specific eight-module handbook inside the bundled canonical product. Preserve the responsive layout, Mini Routes, Trip Mode, itinerary adjustment, checklist persistence, themes and exact-place interactions.

## Scope and references

This public edition builds the editorial handbook only. It never searches, ranks, compares or recommends flights or hotels. User-supplied booked transport or accommodation facts may be displayed; otherwise keep the canonical pending state and continue.

Keep that boundary internal. Do not announce exclusions or discuss product architecture with ordinary users. For a new or preference-light request, use the bundled HTML questionnaire described in `references/first-use-intake.md`; do not substitute a host-native questionnaire. A genuinely complete pasted brief starts immediately. A brief containing only destination, duration/dates and travelers receives the single default-confirmation turn defined below. Tell users only that booked transport/accommodation screenshots or text may be supplied and otherwise remain pending.

## User collaboration contract

This contract applies before any research or build action and is especially important on hosts that prefer native choice widgets:

- Treat the user's current questionnaire output or written brief as the only intake source. Do not append risk lists, approval choices or host-native multiple-choice prompts.
- A genuinely complete brief with preferences/constraints starts work immediately. When the brief contains only destination, duration/dates and travelers (for example, `东京 4 天 3 晚，情侣`), make exactly one lightweight confirmation turn: attach/open the bundled HTML questionnaire and ask whether the user wants to fill it or have all remaining choices follow mainstream defaults. If the user replies `不必要`, `不用填`, `按默认`, or equivalent, start immediately with defaults and ask nothing else.
- For a genuinely new or incomplete request, offer only the bundled HTML questionnaire. Do not invent an alternative questionnaire or answer choices in chat. The default-confirmation above is the sole permitted routine follow-up.
- Treat every run as independent. Do not mention or import prior destinations, old handbooks, host memory or unrelated conversation unless the user explicitly asks to reuse them.
- Keep internal limitations, legacy defects, build mechanics and optional improvement ideas silent unless the user asks. Report only a real blocker that prevents safe completion.
- Transport and accommodation are the sole routine addendum: briefly say that booked screenshots/details may be supplied and otherwise those cards remain pending; do not turn this into a recommendation or follow-up question.

Treat the directory containing this `SKILL.md` as the sole authority for the run. Resolve every script and reference from this same root. Never mix controllers, validators, templates or prompts from another installed skill with a similar name. If a persisted build was started from another skill root, stop with a concise root-conflict message instead of reconciling versions.

Read only the reference needed for the current stage: [content model](references/content-model.md), [itinerary selection](references/itinerary-selection-logic.md) when choosing places and building days, [research pipeline](references/research-and-profile-pipeline.md), [data shapes](references/research-data-shapes.md), [image policy](references/image-and-source-policy.md), [rendering](references/rendering-and-assets.md), [release checks](references/release-validation.md), [gateway failure recovery](references/gateway-failure-recovery.md), or [first-use intake](references/first-use-intake.md).

## Workflow

```text
python scripts/start_build.py <workbench> --destination <name> --country <country> --start-date YYYY-MM-DD --days N
python scripts/advance_build.py <workbench>
```

Use `.travel-build-state.json` as the controller. Research only the bounded batch printed by `research_status.py` (normally two independent packs), save and validate each before continuing. After one repeated pack failure, rerun with `--batch-size 1`; do not impose single-pack serialization on capable hosts. Fix named errors in the source pack; never patch final HTML. Missing optional preferences are not blockers. Keep unprovided transport and stay information pending.

### Non-stop completion guard

`final_response_allowed` is a hard execution gate, not a progress label. Whenever the controller prints `FINAL_RESPONSE_ALLOWED: false` and `USER_INPUT_REQUIRED: false`, do not send a final answer, do not ask the user to say “继续”, and do not stop after reporting that a workspace, research pack or partial page exists. In the same turn, immediately execute `NEXT_COMMAND` or the bounded work in `next_required_action`, then reevaluate the controller. Continue until either `HANDOFF ALLOWED` is printed or a genuine external blocker requires new user authority. Workload, elapsed time, token use, unfinished research, missing optional fields and a desire to provide a progress update are never blockers.

Commentary may briefly report progress while work continues, but it never substitutes for the next tool call. A response that ends while `continuation_required` is true is a failed run.

Use a short research loop on every host. Establish daily area outlines first; then shortlist candidates and perform only cheap identity, coordinate, image-URL, MIME and dimension feasibility checks. Freeze qualified places before writing the full itinerary or module bindings. Download and visually review only final selected images in one later asset stage. Keep only rejected candidates and source incidents in `.research-state/candidate-ledger.json`; normal candidates need no prose log. Generated task specs and named validator errors are the working contract. Do not preload every reference or read validator source merely to infer the JSON shape.

When a host is prone to inventing pack shapes, run `validate_research_pack.py --scaffold <pack-id> --output <target-file>` once and fill that structure. The scaffold contains null placeholders, not facts, and never counts as a completed pack.

Treat questionnaire interests as selection constraints, not decorative copy. Apply explicit preferences first; when the user delegates choices, use the audience tendency and bounded scoring in [itinerary selection](references/itinerary-selection-logic.md). Shortlist before deep research and run one coherence check over existing candidates; do not add a separate trend-search pass.

If a research request returns a platform-level 500 or sensitive-content rejection for ordinary travel material, do not repeat the same request or redelegate it unchanged. Preserve completed packs and follow [gateway failure recovery](references/gateway-failure-recovery.md).

## Research priorities and truthfulness

Spend effort in this order: real place identity and branch; geographic fit; official opening/ticket/reservation facts; recommendation value; exact-place imagery; optional Google rating.

Never invent a restaurant, attraction, address, coordinate, opening time, ticket, rating, review count, reservation rule, transfer time or exact price. Verify changing facts from credible current sources or use conservative wording and require departure-time reconfirmation.

## Google rating lookup and stop-loss

Google Maps ratings are a normal research target, but remain optional enhancement data rather than a completion requirement.

- At the start of place research, open one ordinary exact-place Google result as a capability probe. If the page opens, treat Google as available for the run. Then query every rating-bearing sight and restaurant and record its Google score plus review count whenever visible. The stop-loss is not permission to sample only some venues or leave the remaining inventory blank after one success.
- If one venue cannot be opened because of timeout, access or blocking failure, retry that same venue once with a shorter exact name or alternate canonical Google Maps/search entry. If it still cannot be opened, record one access failure and move to a different real venue. Stop the remaining Google lookup only after two different venues fail to open consecutively. Any successfully opened venue resets this consecutive-failure count; never discard ratings already collected.
- When Google is available, attempt both score and review count for every rating-bearing sight and restaurant. Use a reliably displayed score even if its review count is absent; omit only the missing count.
- A venue page that opens without a reliable score affects only that venue: omit its rating and continue. Do not treat a parsing miss as proof that Google is unavailable for other venues.
- Do not repeat broad rating research after normal coverage. A focused rating-repair pass is allowed when an earlier run incorrectly stopped after a single venue failure; patch only rating records, then recompile, render and rerun the dependent gates instead of rebuilding the handbook.
- Never block recommendations, planning, imagery, HTML rendering or handoff because a rating is absent.
- Never guess a score or review count. Supplied ratings require an exact source URL and retrieval date; omit only the review count when Google does not expose it.
- A handbook with no ratings at all is a valid complete output.

## Required handbook content

Keep the eight chapters:

1. Itinerary — one day and Mini Route per trip day, ordered stops, realistic transfers, authored period descriptions and route-specific photography advice. Author each stop's practical visit note and time/queue fallback in the same pass; collect its verified coordinates during the normal place lookup. Trip Mode consumes these existing fields and must never trigger a second research pass.
2. Sights — at least eight useful first-visit choices, split into scheduled and optional choices.
3. Shopping — reputable shops or markets followed by an image-led souvenir section.
4. Experiences — Standard mode targets three locally meaningful types with two choices each. If one complete type still lacks two truthful, coordinate-verified, image-qualified choices after its bounded source ladder, use constrained mode with two strong types and two choices each; record the failed type and sources in the candidate ledger instead of padding the chapter. Expand only on an explicit experience-heavy request.
5. Food — destination-authored menu primer, exactly four local snacks, at least six dedicated-trip restaurants across four cuisine/scene labels, and two to four dependable local-chain fallbacks.
6. Preparation — essential and confirm-ahead checklists with at least 24 useful items total.
7. Language — five keyword and five phrase groups with five entries each, plus practical English fallback when relevant. Label that edition once as `英语备用`; group headings are plain Chinese without `(English)`、`（英语）` or `中英对照`, while English and its concise Chinese meaning stay inside the cards.
8. Local notes — exactly five folds for weather, culture/etiquette, transport, safety and payment, with four practical topics each.

Every named venue card needs an exact-place image. Before final selection, check each candidate's exact identity, coordinates and image feasibility together. Collect at most two image candidates per slot initially and inspect at most three source families for a commercial venue. Prefer exact official pages and official social/property listings before open-media search; Commons is not the default source for a commercial venue. If the bounded ladder fails, replace the venue once. Never use a generic category image, repeatedly cycle through venues, or keep retrying one throttled host.

## Rendering and release

`index.html` may be installed only by `install_ui_system.py` and changed only by `render_destination.py`. The compiled `destination-profile.json` is the sole content source. Follow the render commands in [rendering-and-assets.md](references/rendering-and-assets.md), then run:

Cover headlines are editorial copy, not compressed trip metadata. Traveler count, duration and destination normally stay in the existing cover metadata; put them in the headline only when they form a natural concept. Prefer a concise mood, contrast or route idea over constructions like `双人六日 + 目的地 + 漫游`. This is a writing choice, not an extra research or generation pass.

```text
python scripts/audit_skill_consistency.py
python scripts/audit_product.py <workbench> --strict
python scripts/quick_forward_test.py <workbench>
python scripts/check_handoff.py <workbench>
```

Complete only after `check_handoff.py` prints `HANDOFF ALLOWED`. A missing optional rating must never prevent that result. Required structural, factual, media or interaction failures still require correction.

After asset machine preflight and official rendering, the controller may report `PREVIEW_READY: true` while visual review is pending. This permits an honest user preview, not a publication claim. Inspect one sufficiently large contact sheet, then open only flagged or ambiguous images individually. If every available visual surface fails at the host level, preserve the preview and pending flags; do not redownload images, repeat research or fabricate verification.

## Trip Mode runtime contract

Trip Mode has one phone-first vertical interface on every viewport; desktop centers the same narrow panel for recording and parity. It is generated from one injected per-day JSON payload, never destination-specific constants or DOM guesswork. Keep these behaviors together:

- compact day tabs, overview, and richer stop cards with practical notes, transfer context and visible time/queue stop-loss;
- one collapsed offline hand-drawn route per day, based only on verified stop coordinates, plus Google/Apple navigation with Google as the first-use default;
- exact-place Xiaohongshu and map actions on stop cards, with no generic bottom Xiaohongshu button;
- an expanded photography card with two or three route-specific shooting moments;
- reference-photo upload stored locally as Data URLs, large tappable previews, full-screen viewing, per-photo deletion and clear-all memory.

The runtime performs no network map rendering and no extra destination research. If coordinates are unavailable, fix the source place record rather than drawing false geography. Do not retain an older Trip Mode implementation, Bali shopping constants, Blob object-URL previews, desktop-only layout or a second map component beside this runtime.
