---
name: proposal-writer
description: >-
  Proposal Writer. Turns the call into a priced proposal the same day. Uses the prospect's own words
  from the call notes and replies, lays out what you will do, gives two or three clearly priced
  options (a full build, a monthly plan) with first-year totals, says what it pays back in one true
  line, recommends one, and ends with a single next step. Drafts the email; it goes out on your yes.
  Use when the user says "write a proposal", "send pricing", "put together a quote", "they asked for
  prices", "send options", or after a good call.
argument-hint: "<deal>"
---

# proposal-writer

A proposal that arrives the same afternoon, in the customer's own words, with a clear price and one
recommended option, gets signed. One that arrives next week with five options does not.

`${CLAUDE_SKILL_DIR}` below is this skill's folder (where this SKILL.md lives).

```bash
python3 "${CLAUDE_SKILL_DIR}/proposal.py" draft --deal bluebird-ads \
    --options "${CLAUDE_SKILL_DIR}/options.example.json" --today 2026-10-29
python3 "${CLAUDE_SKILL_DIR}/proposal.py" record --deal bluebird-ads --approval "yes" --at 2026-10-29T16:00
```

## Steps

1. Read the deal's history (`/record-keeper timeline`) and the call notes in `closer/calls/`.
2. Write the options file: 1 to 3 options, each `{"name", "setup", "monthly", "includes", "recommended"}`.
   Prices come from the user, never from you. Recommend one at most.
3. `proposal.py draft`. It writes `closer/proposals/<company>.md` with their words, an options table with
   first-year totals, the payback line from `me.value_line`, a next step and a 14-day valid-until date.
4. Fill every `[Claude: ...]`: "What we'll do" in 3 to 5 plain lines with dates. Use their words for
   their problem. `record` refuses while any placeholder is left.
5. Show it. Ask: "Send this proposal to Priya? Reply yes or no."
6. On a yes: a Gmail draft with the proposal (pasted in, or attached as a PDF) from the user's account,
   which the user sends (or sent through the Gmail connector right after that yes).
   Then `proposal.py record --approval "<their yes>"`.
7. When they pick an option, `/contract-writer`.

## Example

Priya Shah at Bluebird Pet Spa replied, "Maybe! Can you send me prices?" The proposal opens with that line,
then two options from `options.example.json`: Full build, $2,500 setup, $2,500 in the first year; Monthly
plan (recommended), $399/month, $4,788 in the first year, no setup fee, cancel anytime. It closes with
"Reply with the option you want and I'll send the agreement the same day." (Illustrative: Bluebird Pet Spa
is fictional.)

## What it never does

- Never invents a price, a discount, a result or a client story.
- Never sends without the user's yes for that exact proposal.
- Never gives more than 3 options or hides a fee.

## Consent and truth

- Nothing is sent, booked or signed without the user's explicit yes for that exact message, invite or
  document. Claude drafts, the user says "yes", then it goes out from the user's own accounts.
  One yes per message. Never "yes to all".
- Proposals are templates, not legal or financial advice.
- Never invent a number, a result, a client, a review or a deadline. Fill in only what is true and ask when
  something is missing.
