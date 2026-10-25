---
name: nextdoor-renew-listings
description: "Renew the Nextdoor For Sale & Free listings that are about to expire, using the Claude in Chrome browser tools in the user's signed-in Chrome. Renews only listings labeled Expiring, including items pending pickup, and never marks sold or deletes. Use when asked to renew Nextdoor listings, when a Nextdoor email says a listing expires soon, or when asked to keep the Nextdoor for sale listings from expiring."
---

## Renewing expiring Nextdoor listings

Nextdoor has no renew-all control, so each expiring listing is renewed on its own detail page.

The work runs in the user's signed-in Chrome through the `mcp__claude-in-chrome__*` tools, so no credentials are needed and none are ever entered.

Read the claude-in-chrome skill first, then load every browser tool in one ToolSearch call.

## Which listings are renewed

Renew only listings whose label reads Expiring in N days.

A listing labeled See 1 tip to sell faster is not expiring and is left alone.

An item pending pickup is renewed like any other, because a pickup can fall through and the item is not sold.

An item the vault note records as sold or given away is not renewed.

The unsold items are listed in /Users/mtm/Documents/Obsidian Vault/selling stuff management console.md, and each item has its own note tagged forsale.

Read those to confirm an expiring listing is still unsold, and never write to them, because Nextdoor already shows the posted date and a copy in a note would go stale.

## Procedure

Open a new tab with tabs_create_mcp rather than reusing one.

Navigate to https://nextdoor.com/for_sale_and_free/your_items

The listing text loads late, so wait about 3 seconds before reading the page.

Read the Selling tab with get_page_text and collect every title carrying the Expiring label.

If none carry it, report that nothing is expiring and stop.

For each expiring listing, scroll it into view and click its thumbnail, since clicking the title does nothing.

The detail page shows Mark sold and Renew side by side below the price.

Click Renew only, and never Mark sold.

There is no confirmation dialog and no charge.

Success shows as the posted date under the description changing to Just now.

Return to the listings URL for the next one, because the list reloads and positions shift after a renewal.

A renewed listing drops its Expiring label, which is a second way to confirm it.

Close the tab when finished.

## What not to use

The three-dot menu on a listing offers only Edit, Delete and Mark sold, with no renew entry.

The listing cards in the list view carry no Renew button, so do not hunt for one there.

Never click Delete or Mark sold from this skill.

## The reply

Say how many listings were renewed and name each one with its price.

Say so plainly if a listing was expiring but not renewed, with the reason.
