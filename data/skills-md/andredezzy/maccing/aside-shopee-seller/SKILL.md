---
name: aside-shopee-seller
description: "Use when you need the Shopee Brasil Seller Centre (seller.shopee.com.br, Central do Vendedor) through the Aside browser: product listings, listing copy, images and video, orders, shipping, store profile, blocked listings, finances, marketing or chat."
autoInject:
  keywords: ["shopee", "seller centre", "central do vendedor", "shopee seller", "vendedor shopee", "anúncio shopee"]
  url:
    - "seller.shopee.com.br/**"
---

# Shopee Seller Centre (Brasil)

Drive the Seller Centre in Aside, in the user's logged-in session. There is no API global for it: read with `snapshot()` and act on refs.

> **Depends on:** the `aside` skill, and through it Aside's official `aside-browser` skill. ALWAYS load `aside` first and follow its Iron Laws (update and load `aside-browser`, prefer an Aside built-in skill for the site) before this skill's steps. Its files: `../aside/SKILL.md` and `../aside/references/` (profiles, one-shot `aside repl`, REPL behaviour). Inside the Aside app, a builtin skill is also named `aside`; that one covers the app's settings, not this.

## Canonical URLs

- Home: `https://seller.shopee.com.br/`
- Product list: `https://seller.shopee.com.br/portal/product/list/all`
- A listing's edit form: `https://seller.shopee.com.br/portal/product/<itemid>`
- Seller education centre (rules, fees, how-tos): `https://seller.shopee.com.br/edu`
- A public product page: `https://shopee.com.br/product/<shopid>/<itemid>/`

For any other area, follow the left nav from a snapshot. Never guess a URL.

## Area references

| Area | Read |
|---|---|
| Product listings: create, edit, replicate, images, video, price, stock, shipping, save | `references/listings.md` |
| Listing copy: writing or reviewing a title, description or specifications | `references/listing-copy.md` |
| Product diagnostics: a listing blocked or getting no traffic, the optimiser's quality tasks | `references/diagnostics.md` |
| Shop profile: name, logo, description, phone, and its password gate | `references/shop-profile.md` |
| A store logged in on another Aside profile | `../aside/references/profiles.md` |
| Driving from a terminal: one call per session, getting an image or video in | `../aside/references/terminal.md` |
| Anything else (orders, finances, marketing, chat, other settings) | No reference yet. Snapshot the page, read it, and apply the rules below. |

## Rules for every area

### 1. Confirm the account first

A user may run more than one store, each logged in on its own Aside profile. Before any action, name the store to the user, and stop if it is not the one they meant.

- **Find the profile.** List each profile's tabs and look for a `seller.shopee.com.br` tab (`../aside/references/profiles.md`). If the user keeps a record per store, it holds the store's username and may name its profile. Ask where it is when you don't know.
- **Header username.** A `generic` near the top of an interactive snapshot, before the left nav. Shopee may have generated it, so it need not name the store: compare it with the username the user or the store's record gives.
- **Shop name.** In a listing form, the live preview panel prints the shop name right after the title. This is the check to make before any save.

The shop profile page asks for the login password: only the user types it (`references/shop-profile.md`). A login email shown by Gmail or a password manager is a weak hint, never the check.

### 2. Outward-facing actions need the user's explicit ask

These change what buyers see or what Shopee holds, and many take effect with no confirmation dialog:

- saving, publishing, updating, deactivating or deleting a listing;
- deleting an image, flipping a shipping switch, changing price or stock;
- anything on an order: shipping, cancelling, refunds, returns;
- sending a chat message, replying to a review, joining a campaign or promotion;
- changing store, shipping, payment or bank settings.

Do one only when the user asked for that action on that item. Just before it, show the user the values you will submit, read back from the page, and ask when the user has not already confirmed them (the Aside agent: `ask_user_question`). When you are only reading, leave by navigating away; `references/listings.md` says what the cancel button asks.

### 3. Nothing here is current. Read it live

Shopee changes labels, required fields, fees, categories, deadlines and menus often. The references name controls by purpose ("the price input", "the shipping channel switch"). Snapshot for today's label. Where a fact lives:

| Fact | Where to read it |
|---|---|
| Which fields a form requires | A `*` before the label in the snapshot. The final word is the validation banner the form shows on a failed save, with a link to the first error. |
| Commission, fees, policy | The education centre. Search it, and cite the article you read. |
| Shipping rates | Shown beside the channel on the page. It is a default, not the buyer's price. |
| Deadlines, campaigns | The page that offers them. |

Quote a fee, deadline or rule only from a page you read in this task.

## How the Seller Centre behaves in Aside

The parent's `../aside/references/repl.md` covers stale refs, reading after a navigation, a lagging `page.url()` and the unsupported APIs. On top of that:

- **Attach the existing tab.** Prefer `listBrowserTabs()` → `attachBrowserTab(<targetId>)` on a `seller.shopee.com.br` tab. `page.goto(url)` works inside it. Open a tab only when none exists. A tab holding the user's open form is theirs: for a read, open, read and close a tab of your own.
- **Long pages render sections empty.** A section can show as a bare `region`, and one scrolled away can go empty again, even though `aside guide repl` says no scroll is needed. The section tab bar can vanish too. To act on a section, call `scrollIntoViewIfNeeded()` on something inside it, or scroll with the mouse wheel (`await page.mouse.wheel(0, 800)`) until its field shows, then snapshot. To read a listing form's values, use `shpRead()` from `references/listings.md`: it reads the DOM, not the snapshot.
- **Hidden fields.** Some sections hide fields behind a show-more button. Expand it before you conclude that a field does not exist.
- **Overlays.** A promo panel and a password manager overlay can sit over the page. Neither always shows as a `dialog`. `Escape` clears both. If a click misses, check the snapshot for one.
- **Formatted inputs.** Money, stock and measurement inputs reformat themselves. `fill()` throws on them, and keyboard typing after a click can land in another field. See `references/listings.md` for the method that works. Always read the value back.
- **Custom switches.** Shopee's `.eds-switch` is not an ARIA switch, so the snapshot does not list it. Read its state from the class: `--open` means on, `--close` means off.
- **Uploads.** `setInputFiles` accepts only files inside the REPL session folder. From a terminal, bring each file in within the call that uploads it (`../aside/references/terminal.md`). Upload one file at a time, and wait for each to finish (`references/listings.md`).
