---
name: telegram-bot-ui
description: >-
  Design, audit, and improve the interface of Telegram bots: message texts,
  microcopy, titles, captions, button labels, inline and reply keyboards, action
  grouping, visual hierarchy, colored buttons (style: primary/success/danger),
  custom emoji on buttons (icon_custom_emoji_id), menu button, commands,
  navigation, back and pagination, confirmations, empty and error states,
  consistency between screens and states, streaming AI replies
  (sendMessageDraft, sendRichMessageDraft, tg-thinking), progress and typing
  feedback, personalization, links and deep links, localization, and message
  formatting (HTML, MarkdownV2, entities, Rich Messages, tables). Use for any
  request about a bot's UI, UX, menu, keyboards, buttons, navigation, wording,
  or how a message looks — "rewrite this bot's text", "improve this menu", "add
  colored buttons", "the bot feels frozen", "can't parse entities".
  Do NOT use for bot logic that never reaches the interface (webhooks, payment
  processing, auth, databases, group admin) or Microsoft .rtf files.
---

# Telegram Bot UI

Portable, SDK-agnostic skill for the full life cycle of a **Telegram bot's user
interface**: audit → screen/state map → text, buttons and navigation design →
implementation → migration → testing → documentation.

A Telegram bot has no CSS and no layout engine. Its entire interface is made of
five things: **message text, formatting, keyboards, the chat-level chrome
(commands, menu button, deep links), and the transitions between states.** This
skill treats all five as one design surface.

## Purpose

Help an agent make a bot's interface **clear, consistent, and safe to change**:
choose what a screen says and how it says it; label, group, order, color, and
lay out buttons; design navigation between screens and states; keep every
screen consistent with the rest of the bot; keep localization intact; and
render message bodies with the richest format that fits — across any language
and any Telegram SDK, **without breaking existing handlers or business logic**.

## When to use

- **Interface work:** "improve the bot's UX/UI", "redesign this menu", "the
  keyboard is overloaded", "users don't understand this screen", "add a back
  button", "group these actions", "make the main action stand out".
- **Buttons and keyboards:** inline keyboards, reply keyboards, button labels,
  button order and layout, `style` colors, `icon_custom_emoji_id` custom emoji,
  Web App / URL / copy-text / switch-inline buttons, `ForceReply`, keyboard
  removal, pagination and back navigation.
- **Text and microcopy:** rewriting bot messages, titles, captions, prompts,
  confirmations, error and empty states, tone and length, emoji use.
- **Chat chrome:** `/commands` list and scopes, menu button, `/start` and deep
  links, first-run experience.
- **Dynamic feedback:** streaming AI answers (`sendMessageDraft`,
  `sendRichMessageDraft`, `<tg-thinking>`), progress bars, "typing" statuses,
  button loaders, "the bot feels frozen while it works".
- **Personalization and links:** greeting users by name safely, locale hints,
  URL buttons vs inline links, link previews, deep links, mentions.
- **Consistency:** the same action named three different ways, back buttons that
  exist on some screens only, mismatched states after an edit.
- **Message rendering:** HTML / MarkdownV2 / `MessageEntity`, custom emoji in
  text, captions, tables and Rich Messages, link-preview / silent / protected
  options, long-message splitting, streaming drafts, editing, channel posts,
  localization and RTL, `can't parse entities`, broken or oversized messages.

## When NOT to use

Bot logic that does not surface in the interface: webhook infrastructure,
payment *processing*, authorization, databases and migrations, group
administration and moderation logic, scraping, analytics pipelines, Mini App
*internals* (its own HTML/CSS UI is ordinary web front-end work — this skill
covers only the Telegram-side surface: the button or menu that opens it).
Also not for Microsoft `.rtf` files.

## Terminology — do not confuse these

- **Inline keyboard ≠ reply keyboard.** `InlineKeyboardMarkup` is attached to a
  specific message and sends `callback_query` / opens URLs. `ReplyKeyboardMarkup`
  replaces the user's letter keyboard and **sends text as a normal message**.
  Different button classes, different UX.
- **`style` is not a color value.** It is one of exactly `primary`, `success`,
  `danger`. Telegram has no HEX/RGB/CSS button colors.
- **`icon_custom_emoji_id` is not a `file_id`,** not an emoji-pack name, not a
  link, and not a Unicode emoji. It is the ID of one specific custom emoji.
- **Telegram Rich Text is NOT Microsoft RTF.** Never call Rich Messages "RTF".
- **Rich Markdown ≠ MarkdownV2.** MarkdownV2 is a `parse_mode` for *regular*
  messages with strict escaping. Rich Markdown is the document syntax for
  *Rich Messages*.
- **Rich HTML ≠ arbitrary browser HTML.** Only Telegram's supported tag set.
- **Editing a keyboard ≠ resending a screen.** `editMessageReplyMarkup` and
  `editMessageText` update in place; sending a new message stacks screens.

## Source-of-truth policy

Trust in this order:
1. Current **official Telegram documentation** (Bot API, Bot Features,
   formatting pages, official blog).
2. Official **Bot API changelog**.
3. Docs of the **SDK actually installed** in the project.
4. **SDK source code**.
5. **SDK issue tracker**.
6. Third-party articles — supplementary context only.

**Re-verify official docs before acting** when: the task touches new APIs; today
is later than the "last verified" date in `references/official-sources.md`; the
project's Bot API version is unknown; SDK docs contradict the Bot API; you meet
an unfamiliar type/field; or the user asks for "the latest capabilities".
This skill is **not frozen** at Bot API 10.2 — if Telegram shipped a newer
version, use it. UI-relevant version gates: `references/ui-changelog.md`.

## Core workflow (audit before you redesign)

1. Read the project's instructions (`AGENTS.md` / `CLAUDE.md` / README / docs).
2. Detect language, framework, **Telegram SDK, and exact versions**.
3. Determine the **Bot API version** the SDK actually supports — this decides
   whether `style` and `icon_custom_emoji_id` are reachable at all.
4. Build a **screen/state map**: every message the user can see, every keyboard,
   every `callback_data`, every command, every transition
   (`references/navigation-and-flows.md`).
5. Classify each screen: entry / menu / form step / confirmation / result /
   error / empty / notification.
6. Identify the **real UX defects** (don't invent work): ambiguous labels,
   overloaded keyboards, dead ends with no way back, inconsistent naming,
   destructive actions one tap away, unlocalized strings, unreadable bodies.
7. Design the fix: text first, then structure, then layout, then color/emoji —
   **in that order**. Color is the last layer, never the fix for a bad label.
8. Check SDK support for every field you plan to use
   (`references/sdk-compatibility.md`).
9. Implement in the project's existing style and utilities (don't duplicate its
   keyboard builders).
10. **Preserve** `callback_data`, URLs, deep links, handler routing, and
    localization keys unless the user explicitly asked to change them.
11. Add a **fallback** path and keep old clients usable
    (`references/errors-and-fallbacks.md`).
12. Add **tests** with the project's existing test infrastructure
    (`references/testing-playbook.md`).
13. Run the project's lint / typecheck / tests / applicable smoke checks.
14. Report: screen map, what changed and why, what was deliberately left alone,
    limits, and verification evidence.

Do **not** write implementation code before steps 1–6 are complete.

## The five UI layers (design in this order)

| # | Layer | Question it answers | Reference |
|---|---|---|---|
| 1 | **Words** | Does the user understand what this is and what happens next? | `references/microcopy-and-labels.md` |
| 2 | **Structure** | Which actions exist, how are they grouped and ordered? | `references/inline-keyboards.md`, `references/reply-keyboards.md` |
| 3 | **Navigation** | How do I get here, back, and out? Which state am I in? | `references/navigation-and-flows.md` |
| 4 | **Body rendering** | Is the content readable — table, list, headings, plain? | `references/format-selection.md`, `references/tables.md` |
| 5 | **Emphasis** | What is *the* action here? What is dangerous? | `references/buttons-and-styles.md`, `references/custom-emoji.md` |

A screen that fails layer 1 cannot be rescued by layers 4–5. Never start with
color.

## Button essentials (full rules in `references/buttons-and-styles.md`)

**Exactly one action per inline button.** Per the Bot API,
`InlineKeyboardButton` requires *exactly one* of the fields other than `text`,
`icon_custom_emoji_id`, and `style` (`url`, `callback_data`, `web_app`,
`login_url`, `switch_inline_query*`, `copy_text`, `callback_game`, `pay`).
`KeyboardButton` allows *at most one* of its non-`text`/`icon`/`style` fields.

**`style` (Bot API 9.4)** — optional, exactly one of:

| `style` | Color | Meaning | Typical labels |
|---|---|---|---|
| `primary` | blue | *The* main forward action of the screen | Continue, Start, Open, Next, Choose |
| `success` | green | Commit / confirm / complete positively | Save, Confirm, Publish, Submit, Finish |
| `danger` | red | Destructive or irreversible | Delete, Reset, Unsubscribe, Leave, Cancel plan |
| *omitted* | app default | Everything else | Back, Settings, Help, secondary options |

If `style` is omitted, an app-specific style is used. **At most one `primary`
per screen. `danger` only for genuinely destructive actions, paired with a
confirmation step.** Secondary actions such as "Back" normally stay unstyled.

**`icon_custom_emoji_id` (Bot API 9.4)** — shows a custom emoji before the
button text. Usable only by bots that **purchased additional usernames on
Fragment**, or in messages sent **directly by the bot to private, group, and
supergroup chats when the bot's owner has Telegram Premium**. **Never invent an
ID** — obtain it (`references/custom-emoji.md`) or ask the user for it.

Both fields are **decoration on top of a working button**: the label must still
make sense with no color and no icon.

## Message body: richest fit that helps

| Need | Use |
|---|---|
| Rows/columns or label→value data | **Table** — `references/tables.md` |
| Structured doc: report, AI answer, comparison, checklist | **Rich Markdown** |
| Server-templated content, precise tag control | **Rich HTML** |
| Typed generation from data / CMS / AST | **`InputRichBlock` blocks** |
| A screen with a keyboard: short prompt + options | **Regular HTML**, short |
| Exact offset control, no `parse_mode` | **`MessageEntity`** |
| Genuinely no styling needed | **Plain text** |

Rule: **structured data becomes a real table, never a monospace grid** — but a
menu screen is a short prompt plus buttons, not an essay. Full matrix:
`references/format-selection.md`.

## Feedback while the bot is working

Waiting with no signal is the most common UX failure in bots. Choose by the
shape of the operation (full rules:
`references/dynamic-feedback-and-streaming.md`):

| Situation | Mechanism |
|---|---|
| Inline button tapped | `answerCallbackQuery` **first**, then do the work |
| 2–5 s operation | `sendChatAction` (`typing`, `upload_photo`, …) — 5 s max |
| AI text being generated (private chat) | `sendMessageDraft` — same `draft_id`, finalize with `sendMessage` |
| AI answer with structure | `sendRichMessageDraft` + `<tg-thinking>` → `sendRichMessage` |
| Real, nameable stages | `editMessageText`, throttled |
| Progress not measurable | Named stages — **never a fake percentage** |
| Interactive process | Mini App (`BottomButton.showProgress()`, `WebApp.ready()`) |

Never edit per token: update on ~800–1500 ms, ~30–80 new characters, a finished
sentence, or a real stage change — and honour `retry_after`. One `draft_id` /
`message_id` / `operation_id` per operation, finalized exactly once.

## Which reference to read (task-routed — don't read them all)

**UI / UX**
- Button labels, message wording, tone, emoji in text →
  `references/microcopy-and-labels.md`
- `style` colors, emphasis, button layout and grouping →
  `references/buttons-and-styles.md`
- Inline keyboards, `callback_data`, pagination, editing in place →
  `references/inline-keyboards.md`
- Reply keyboards, `ForceReply`, keyboard removal, placeholders →
  `references/reply-keyboards.md`
- Screens, states, back/home, commands, menu button, deep links →
  `references/navigation-and-flows.md`
- Custom emoji on buttons and in text, obtaining IDs, eligibility →
  `references/custom-emoji.md`
- Streaming answers, thinking blocks, progress bars, loaders, chat actions →
  `references/dynamic-feedback-and-streaming.md`
- Personalizing with user data, links, previews, deep links →
  `references/personalization-and-links.md`
- Cross-screen consistency + the pre-finish checklist →
  `references/consistency-and-review.md`
- UI-relevant Bot API history and version gates → `references/ui-changelog.md`
- Worked before/after scenarios → `references/examples-before-after.md`

**Content rendering**
- Tables → `references/tables.md`
- Rich Messages / blocks / capability matrix →
  `references/telegram-capabilities.md`
- HTML / MarkdownV2 / entities / captions / previews →
  `references/regular-formatting.md`
- Choosing a format → `references/format-selection.md`
- Media → `references/rich-media.md`
- Limits & splitting → `references/limits-and-splitting.md`
- Streaming drafts & editing → `references/streaming-and-editing.md`
- Channels, notifications, broadcasts →
  `references/channels-and-broadcasting.md`

**Engineering**
- Investigating an unknown project → `references/project-adaptation.md`
- Escaping / injection / user or AI content →
  `references/security-and-escaping.md`
- Localization, RTL, button-label length →
  `references/localization-and-rtl.md`
- Errors, fallbacks, old clients → `references/errors-and-fallbacks.md`
- SDK gaps / raw Bot API payloads → `references/sdk-compatibility.md`
- Testing → `references/testing-playbook.md`
- Sources & last-verified dates → `references/official-sources.md`

Local validators: `scripts/validate_skill.py`, `scripts/validate_references.py`,
`scripts/validate_keyboard.py` (keyboard JSON rules — offline, no token).
Trigger scenarios: `evals/activation-evals.md`.

## Non-negotiable rules

- **Preserve behaviour.** Keep existing `callback_data`, URLs, deep links,
  payloads, and handler routing. A visual redesign must not rewrite handlers.
  If a `callback_data` change is unavoidable, say so and update every
  handler/route in the same change.
- **Words before pixels.** Fix the label before adding a color or an emoji.
- **No decorative color.** Assign `style` by the *meaning* of the action. Do not
  color every button; an all-colored keyboard has no hierarchy.
- **`style` accepts only** `primary`, `success`, `danger`. No HEX/RGB/CSS.
- **Never invent a `custom_emoji_id`.** Fetch it or ask for it. Never guess.
- **Never rely on color or emoji alone.** The interface must stay usable in
  plain text, in a client that ignores the new fields, and for a user who cannot
  distinguish the colors.
- **Verify SDK support** for `style` / `icon_custom_emoji_id` before using them;
  if absent, offer an SDK upgrade *or* a raw Bot API payload path
  (`references/sdk-compatibility.md`) — never silently drop the field.
- **Keep localization intact.** New strings go through the existing i18n
  mechanism with the project's key conventions; never hardcode a translated
  label over a catalog. Layout must survive the longest translation.
- **Don't mix Unicode emoji and custom emoji** on the same control set without a
  deliberate, stated reason.
- **Every tap gets feedback**, and every long operation gets an honest progress
  signal — no invented percentages, no per-token edits, no stalled spinners.
  Finalize a streamed draft with a real message, including on failure.
- **Treat user data as optional and untrusted:** `last_name`, `username`,
  `language_code`, `photo_url` may be absent; names must be escaped or passed as
  entities; Mini App personalization uses validated `initData`.
- Investigate the project **before** changing it; don't duplicate its keyboard
  builders or scatter magic limits.
- **One escaping function per format** — never a single universal escaper; never
  pass arbitrary or AI-generated HTML straight to Telegram.
- Pull **current limits from official docs**; don't hardcode remembered numbers.
- Fallbacks must be explicit and logged — no silent degradation, no infinite
  retries, no logging bot tokens or full personal text.
- Don't claim a screen works until it has been **tested**.

## Definition of done

Screen/state map produced · real UX defects identified (not invented) · text
fixed before structure, structure before color · every inline button carries
exactly one action field · `style` assigned by meaning, ≤1 `primary` per screen,
`danger` only where destruction is real and confirmed · custom emoji IDs
verified, never invented · labels readable with no color and no emoji · every
tap acknowledged and every long operation given honest, throttled progress ·
streamed drafts finalized with a real message · personalization degrades safely
when optional user fields are missing · existing
`callback_data`/URLs/deep links/handlers preserved · localization keys intact
and layout tolerant of long translations · SDK support verified or a documented
fallback path used · body rendered with the richest fit (tables for structured
data) · safe escaping · fallback + tests added · project checks green · limits
sourced from official docs · "last verified" date recorded. Report per step 14
and run `references/consistency-and-review.md`.
