---
name: feishu-card-json-v2
description: Construct, refine, review, validate, and package polished Feishu/Lark Card JSON 2.0 payloads. Use when creating cards for Feishu custom-bot webhooks, application bots, notifications, alerts, reports, dashboards, approvals, forms, callbacks, updates, streaming AI output, Markdown-rich content, tables, charts, images, audio, localization, or responsive layouts; also use when converting a content brief or legacy card into strict JSON 2.0 or diagnosing a rejected card payload.
---

# Feishu Card JSON 2.0

Create production-oriented Feishu Card JSON 2.0. Select the delivery surface first, build only supported interactions, keep the visual hierarchy compact, and validate the exact final payload.

## Select the delivery surface

Classify the request before choosing components:

| Surface | Output shape | Supported interaction |
|---|---|---|
| Custom bot webhook | `{"msg_type":"interactive","card":{...}}` | Static display and URL navigation only |
| Application bot / OpenAPI | Raw card object, or the enclosing API request requested by the user | URL navigation, callbacks, forms, updates |
| Callback response | `{"toast":...,"card":{"type":"raw","data":{...}}}` | Immediate toast and optional card replacement |
| CardKit/template | Template ID, version, and variables | Follow the specific CardKit API; do not pretend raw JSON supports template variables |

Never add `callback` behavior, form submission, input collection, or server-side interaction to a custom-bot webhook card. Custom bots are one-way senders. Use an application bot when the user needs callbacks or data collection.

Read [delivery-and-interaction.md](references/delivery-and-interaction.md) for webhook signing, callbacks, updates, streaming, and payload envelopes.

## Gather the minimum brief

Infer safe defaults when possible. Identify:

- one primary purpose and audience;
- delivery surface;
- title, summary, content sections, severity/status;
- primary and secondary actions;
- dynamic fields, dates, people IDs, image/file keys, and URLs;
- localization and minimum client-version needs;
- whether the user wants raw card JSON, a webhook envelope, callback response, or code that returns the payload.

Use placeholder strings such as `${TITLE}` only when real values are unavailable. Never invent webhook URLs, secrets, user IDs, image keys, file keys, message IDs, or business metrics.

## Build the card

1. Start with `"schema": "2.0"`.
2. Put global behavior in `config`, optional whole-card navigation in `card_link`, title information in `header`, and ordered components in `body.elements`.
3. Keep `config.update_multi` absent or `true`; JSON 2.0 does not support `false`.
4. Choose `config.width_mode` deliberately:
   - omit for the default 600 px maximum;
   - `compact` for short notices or narrow forms;
   - `fill` for tables, charts, and dashboards.
5. Use body padding around `12px`, vertical spacing around `8px` or `12px`, and explicit responsive behavior for `column_set`.
6. Assign stable, globally unique `element_id` values only when later component operations need them. Match `^[A-Za-z][A-Za-z0-9_]{0,19}$`.
7. Keep strict JSON: no comments, trailing commas, JavaScript expressions, or unescaped newlines.

Read [core-schema-and-style.md](references/core-schema-and-style.md) for root fields, layout, colors, Markdown, localization, and global limits.

## Choose components

Prefer the smallest component set that expresses the information:

- Use `markdown` for structured narrative, links, mentions, lists, code, and compact key-value content.
- Use `div` for plain text that needs precise text/icon styling.
- Use `column_set` for responsive key metrics, paired labels/values, and button rows.
- Use `table` for typed, multi-row data; use Markdown tables only for small simple tables.
- Use `chart` only when the data relationship benefits from visualization.
- Use `img` or `img_combination` when a real `img_key` exists.
- Use `person` or `person_list` for identity display; use Markdown `<at>` only when an actual mention notification is intended.
- Use `collapsible_panel` for secondary detail.
- Use `button` with `open_url` for webhook actions.
- Use `form`, inputs, selectors, pickers, `checker`, or callback behaviors only for application-delivered cards.
- Use `audio` only with an OPUS `file_key`, client fallback, and `config.enable_forward: false`.

Read [component-catalog.md](references/component-catalog.md) before using an unfamiliar, nested, interactive, chart, table, image, or audio component.

## Compose for visual quality

Apply these defaults unless the content suggests otherwise:

- Lead with outcome or status, then details, then actions.
- Use one header theme that reflects semantics: red/carmine for failure, orange/yellow for warning, green for success, blue/indigo for neutral information.
- Keep one primary filled button. Render other actions as default buttons or links.
- Limit header suffix tags to three.
- Use separators sparingly; whitespace and grouping should carry most of the hierarchy.
- Prefer 2–4 metric columns and configure `flex_mode` so narrow clients do not crush content.
- Truncate or summarize long material, then link to the full source.
- Define both light and dark values for custom colors.
- Preserve meaningful fallbacks for version-gated components.

Read [design-recipes.md](references/design-recipes.md) for notification, alert, report, form, approval, and AI-streaming patterns. Reuse the closest file in `assets/templates/` rather than starting from an empty object.

## Add interaction correctly

For URL navigation, use:

```json
"behaviors": [
  {
    "type": "open_url",
    "default_url": "https://example.com",
    "pc_url": "https://example.com",
    "ios_url": "https://example.com",
    "android_url": "https://example.com"
  }
]
```

Use `lark://msgcard/unsupported_action` to disable a specific client. Ensure at least one usable URL exists.

For application callbacks, use:

```json
"behaviors": [
  {
    "type": "callback",
    "value": {
      "action": "acknowledge",
      "record_id": "${RECORD_ID}"
    }
  }
]
```

Keep callback `value` small and non-sensitive. Treat it as untrusted input on the server. For forms, give every interactive child a globally unique `name` and include a button with `"form_action_type": "submit"`.

## Localize

Use component-level `i18n_*` fields in JSON 2.0, such as `i18n_content`, `i18n_img_key`, `i18n_file_key`, and `i18n_text_tag_list`. JSON 2.0 does not support root-level `i18n_elements`.

If `config.locales` is present, include only supported locale identifiers and ensure fallback content still exists. Use `local_datetime` in Markdown for viewer-local time when appropriate.

## Validate and deliver

Run:

```bash
python3 scripts/validate_card.py path/to/payload.json
```

Use `--mode custom-bot`, `--mode raw`, or `--mode callback-response` when automatic envelope detection is ambiguous.

To wrap a raw card for a custom-bot webhook without sending it:

```bash
python3 scripts/wrap_webhook.py card.json
```

Add `--secret-env FEISHU_BOT_SECRET` only when the secret is already available through that environment variable. Never print or embed the secret or webhook URL.

Before returning output, verify:

- the delivery envelope matches the requested surface;
- the payload parses as strict JSON;
- `schema` is exactly `"2.0"`;
- all text, URLs, IDs, and metrics come from the user or are explicit placeholders;
- no custom-bot card contains callback-only controls;
- `element_id` and form `name` values are unique;
- component count is at most 200 and container depth is at most five;
- the card remains legible on narrow screens and in dark mode;
- no secret appears in the card, example command, logs, or prose.

Return the complete payload first. Add only the integration note or caveat needed for the chosen surface. Do not send the webhook or mutate a live card unless the user explicitly asks.
