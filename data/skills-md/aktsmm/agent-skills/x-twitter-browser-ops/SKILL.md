---
name: "x-twitter-browser-ops"
description: "X/Twitter browser operations. Use for X browsing, analysis, bookmark management, content and profile operations, or browser-driven troubleshooting. Require explicit confirmation for outbound posts, DMs, engagement, follows, blocks, mutes, and list edits."
argument-hint: "対象のX画面、実行したい操作、対象アカウントまたは投稿"
user-invocable: true
license: CC BY-NC-SA 4.0
metadata:
  author: yamapan (https://github.com/aktsmm)
---

# X/Twitter Browser Ops

Use this skill for all X/Twitter browser operations: browsing and analysis, follower/following collection, bookmark-folder management, content/profile management, and browser-driven troubleshooting.

## When to Use

- User asks for X/Twitter follower, following, mutual follower, or verified follower analysis.
- User asks to rank X/Twitter accounts by followers, export CSV/Markdown/HTML, or build a dashboard from collected X data.
- User asks to organize bookmarks, create/rename/delete bookmark folders, or move bookmarks between folders.
- User asks to operate X/Twitter in the browser.

## Do Not Use

- Do not use to evade X rate limits, bans, access controls, paywalls, or privacy settings.
- Do not save or expose login cookies, auth headers, HAR files, tokens, or browser profile data.

## Safety and Session Rules

1. Confirm the user is logged in before collecting private/session-dependent lists.
2. Treat the browser session as sensitive. Never persist cookies, CSRF tokens, Authorization headers, or HAR captures.
3. Prefer read-only page navigation and response observation over replaying internal API calls.
4. If screenshots or HTML outputs include notification badges, DMs, private handles, or unrelated personal data, mask or omit them.
5. For any outward-facing or relationship-changing action—post, reply, like, repost, DM, follow/unfollow, block, mute, or list edit—show the exact action and obtain explicit confirmation immediately before execution.
6. Bookmark folder creation, renaming, deletion, and assignment are permitted after the user explicitly approves the organization plan.
7. Before any write or relationship-changing action, verify the acting account identity from the account switcher or profile UI and confirm it matches the intended account for this task.

## Post Draft Validation

- Before treating a draft as ready to post or entering it in the browser, measure it with a `twitter-text` v3-compatible parser using the official configuration: https://raw.githubusercontent.com/twitter/twitter-text/master/config/v3.json
- Require `valid === true` and `weightedLength <= maxWeightedTweetLength` (currently 280).
- Let the parser apply URL transformation and emoji parsing. An HTTP(S) URL uses `transformedURLLength` (currently 23), while ZWJ emoji and variation selectors must not be counted by visible glyphs or `String.length`.
- If a compatible parser or configuration is unavailable, report the draft as length-unverified rather than claiming it is ready to post.

## Bookmark Management

1. Inspect existing folders plus representative unfoldered and folder-specific posts before proposing a minimal taxonomy.
2. Show the proposed folder names, merges, renames, and classification priority before mutating bookmarks.
3. Confirm each assignment from the UI before removing a post from its prior folder.
4. In virtualized infinite-scroll feeds, operate in bounded batches using a post's canonical `/status/` URL; re-resolve the post immediately before each mutation and never retain an element ref across scrolls or mutations.
5. Process one visible post at a time and re-scan canonical URLs after each folder-picker mutation; do not pre-capture a whole visible candidate batch because X can recycle the sibling articles immediately.
6. On a shared logged-in browser, create a dedicated work tab, pin its CDP target ID, and assert `/i/bookmarks` plus the active search query before every write batch; close only that work tab afterward.
7. Folder membership hydrates after the picker shell. Wait for checkmark/icon state before deciding assigned vs unassigned; an immediately missing checkmark is unknown, not safe to click.
8. X can render duplicate `[role=dialog]` shells. Treat a dialog as actionable only when its bounding rect has both positive width and height, and close it only while the route is `/i/bookmarks/add` to avoid an extra history-back navigation.
9. Treat missing folder-picker options, modals, or navigations as unverified—not as success. Keep the source assignment until the destination is visibly confirmed.
10. Scroll through several batches with no new canonical post URLs before declaring the feed complete; deduplicate and report counts by canonical post ID, and report skipped or unverified items separately.

## X Page Semantics

Use URL path, not translated UI tab labels, to avoid tab mix-ups:

- `/followers` = all followers.
- `/following` = accounts the target follows.
- `/followers_you_follow` = followers known to the logged-in user; for the target user's own account this is the useful mutual-follower view.
- `/verified_followers` = verified followers only; this is not the same as all mutual followers.

For mutual analysis, collect from `/followers_you_follow` when available, or use `relationship_perspectives.following === true` and `relationship_perspectives.followed_by === true` from follower responses.

X changes DOM structure and GraphQL response shapes without notice. Re-verify these paths and field names against the live page instead of relying on remembered selectors.

## Collection Workflow

1. Open the profile and confirm the target handle and visible counts.
2. Navigate to the correct path explicitly.
3. Attach browser response observers for GraphQL list responses; parse user objects from responses rather than relying only on visible text.
4. Scroll slowly in small batches. Suggested baseline: 4-5 scrolls per batch, 4-9 seconds between scrolls, and pause 30-60 seconds after large batches.
5. If HTTP 429, repeated 403, forced redirects, login prompts, or unusual challenge pages appear, stop collection and report partial results instead of pushing harder.
6. If stopping early, record a resume checkpoint: last collected `rest_id`, canonical URL of the last processed post, and total collected count.
7. Deduplicate by `rest_id` / user ID. Keep `screen_name`, `name`, `followers_count`, `url`, and relationship flags.

## Verified / Non-Verified Split

1. Collect mutual follower IDs from the mutual source.
2. Collect verified follower IDs from `/verified_followers`; filter those where the logged-in account also follows them when relationship flags are available.
3. Verified mutual = mutual IDs present in verified mutual collection.
4. Non-verified mutual = mutual IDs minus verified mutual IDs.
5. Do not assume a visible blue badge in the DOM is enough; prefer response fields such as `is_blue_verified` or verified list membership.

## Ranking and Output

- Sort descending by `legacy.followers_count` / `followers_count`.
- Output rank, display name, handle, follower count, and profile URL.
- For Top 100, verify there are at least 100 rows; if fewer, say how many were collected.
- For HTML dashboards, delegate visual artifact styling to `web-artifacts-builder` when appropriate.
- For PowerShell-generated HTML, embed JSON safely: use `ConvertTo-Json -Compress`, place it in `<script type="application/json">`, and escape JSON `<`, `>`, and `&` as `\u003c`, `\u003e`, and `\u0026`. Do not HTML-encode JSON as `&quot;` before `JSON.parse`.

## Verification Checklist

Before final delivery, check:

- Acting account verified before mutation.
- Target handle and source paths used.
- Collected counts for all mutual, verified mutual, and non-verified mutual.
- Duplicate user IDs removed.
- Partial-stop output includes the resume checkpoint.
- Top rows are sorted by follower count descending.
- CSV/Markdown/HTML files open and contain the expected row counts.
- For HTML: `JSON.parse` succeeds, stats are not `-`, card/table DOM rows render, and browser console/page errors are zero.
- Edge cases: zero results, fewer than 100 results, and missing follower counts are handled visibly rather than silently.
