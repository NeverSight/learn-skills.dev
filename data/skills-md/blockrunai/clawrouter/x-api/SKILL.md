---
name: x-api
description: Look up X/Twitter user profiles via BlockRun's API. Trigger when the user asks to look up, find, or get info about X/Twitter users or handles.
metadata: { "openclaw": { "emoji": "𝕏", "requires": { "config": ["models.providers.blockrun"] } } }
---

# X/Twitter User Lookup

Look up X/Twitter user profiles — follower counts, bio, verified status — in one call. Payment is automatic via x402.

## How to Look Up Users

POST to `http://localhost:8402/v1/x/users/lookup`:

```json
{
  "usernames": ["elonmusk", "sama", "vitalikbuterin"]
}
```

Also accepts a comma-separated string:

```json
{
  "usernames": "elonmusk, sama, vitalikbuterin"
}
```

- `@` prefix is stripped automatically
- Duplicates removed, normalized to lowercase
- Max **100 users** per request

## Response

```json
{
  "users": [
    {
      "id": "44196397",
      "userName": "elonmusk",
      "name": "Elon Musk",
      "profilePicture": "https://pbs.twimg.com/...",
      "description": "Bio text here",
      "followers": 219000000,
      "following": 1234,
      "isBlueVerified": true,
      "verifiedType": "blue",
      "location": "Texas, USA",
      "joined": "2009-06-02T20:12:29.000Z"
    }
  ],
  "not_found": ["unknownuser123"],
  "total_requested": 3,
  "total_found": 2
}
```

## Pricing

| Batch size   | Cost                        |
| ------------ | --------------------------- |
| 1–10 users   | $0.01 (minimum)             |
| 11–100 users | $0.001 per user             |
| 100+ users   | $0.10 (capped at first 100) |

## Example Interactions

**User:** What are the follower counts for elonmusk and naval?

→ POST with `["elonmusk", "naval"]`, show follower counts from response.

**User:** Look up these crypto influencers: vitalikbuterin, sassal0x, jessepollak

→ POST with the array, display a table with name, followers, verified status, bio.

**User:** Find info about @pmarca

→ POST with `["pmarca"]` (strip @ automatically), display profile.

## Notes

- Payment is automatic via x402 — deducted from the user's BlockRun wallet
- If the call fails with a payment error, tell the user to fund their wallet at [blockrun.ai](https://blockrun.ai)
- Rate limit: **20 requests per hour**
- Users in `not_found` were not charged — only found users count toward the bill
- Data is real-time from X/Twitter via [AttentionVC](https://api.attentionvc.ai/docs)
