---
name: prospector
description: >-
  Prospector. Finds new leads and performs the cold outreach. Builds a list of local businesses
  from public listings, checks each one's own website for the gap you fix (no online booking, not
  mobile-friendly, slow, no Google Ads tag, no reviews, no online ordering), ranks them with the
  reason, puts the best on the board, and writes a short, specific, honest opening email for each
  one with the legal footer and an opt-out. Every email waits for your yes. Use when the user says
  "find me leads", "find customers", "prospect", "cold email", "cold outreach", "build a lead list",
  "who should I reach out to", or "get me new clients".
argument-hint: "[find <who> in <where> | draft <contact>]"
---

# prospector

The Prospector fills the top of the board. It finds businesses that need what the user sells,
proves why from their own website, and writes the first email. It never sends anything itself.

`${CLAUDE_SKILL_DIR}` below is this skill's folder (where this SKILL.md lives).

```bash
python3 "${CLAUDE_SKILL_DIR}/leads.py" audit https://harborlanedental.com --type Dentist
python3 "${CLAUDE_SKILL_DIR}/leads.py" rank --csv closer/leads.csv --offer "Website + Google Ads"
python3 "${CLAUDE_SKILL_DIR}/leads.py" add --top 10 --value 2500
python3 "${CLAUDE_SKILL_DIR}/leads.py" draft --contact dana-harbor-lane
python3 "${CLAUDE_SKILL_DIR}/leads.py" record --contact dana-harbor-lane --text-file /tmp/opening.txt \
    --subject "Quick idea for Harbor Lane Dental" --approval "yes" --at 2026-10-19T09:02
```

## Steps

1. **Who.** Ask what kind of business and where ("dentists and gyms in Austin, TX"), and confirm the
   user's offer and postal address are in `closer/pipeline.json` (`/pipeline init`).
2. **Find.** Search public listings (a web search, Google Maps results, the local chamber of commerce,
   an industry directory). For each business: name, owner or manager if the business's own site names
   them, type, the email published on its own site (or none), website. Write `closer/leads.csv` with
   the columns `name, who, type, email, website, city`. Never guess personal emails, never scrape
   behind a login, never buy a list.
3. **Check.** `leads.py rank --csv closer/leads.csv`. It reads one public page per site, slowly, and
   ranks by gaps. A missing tag is a hint, not proof: the email says "it looks like", never "you are not".
4. **Pick.** Show the ranked list with each reason. The user chooses who goes on the board;
   `leads.py add --top N` adds them as leads. Anyone on the suppression list is skipped.
5. **Write.** For each lead, `leads.py draft --contact <id>`. Read the site yourself and make the first
   line more specific if you can, with something true. Keep it under 90 words. Fill every `[fill: ...]`.
6. **Ask.** Show one email. "Send this to Dana Ortiz at Harbor Lane Dental? Reply yes or no." One email
   per question, every time, even when there are 47 of them.
7. **Send.** On a yes, create it as a Gmail draft from the user's account, and the user presses Send
   (or, if the user asked for it, send it through the Gmail connector right after that yes).
8. **Log.** Only after it went out: `leads.py record --approval "<their yes, word for word>"`. The deal
   moves to `contacted` and `/follow-up` takes over. At most 50 openings a day: it protects the
   user's inbox reputation and keeps this one-to-one, not bulk mail.

## Example from the reel

"Local businesses in Austin, TX with no online booking": 47 found, the top eight shown with reasons
(Harbor Lane Dental: no online booking; Pine Street Fitness: site not mobile-friendly; Bluebird Pet Spa:
no Google Ads running...). The opening to Dana Ortiz, Mon Oct 19 at 9:02 AM, subject "Quick idea for Harbor
Lane Dental": "I noticed Harbor Lane doesn't have online booking yet. Most dental patients book after
hours, so that's new patients going to the practice down the street..." The list is
`leads.example.csv` (illustrative: every business in it is fictional).

## What it never does

- Never sends, and never records an email that did not go out.
- Never emails anyone on the suppression list or marked do-not-contact.
- Never invents a fact about the business, a mutual friend, a past conversation or a fake "Re:".
- Never hides who is writing or makes opting out hard.

## Consent and truth

- Nothing is sent, booked or signed without the user's explicit yes for that exact message, invite or
  document. Claude drafts, the user says "yes", then it goes out from the user's own accounts.
  One yes per message. Never "yes to all".
- Every cold email is honest and legal: a real subject line, the sender's real name and business, a postal
  address, and a plain way to opt out (CAN-SPAM in the US; in the UK, EU and Canada cold email to people
  needs a lawful basis or consent first, so check before emailing there). Opt-outs are honoured forever.
- Public business information only: the company's own site and public listings, never a person's private
  life, home or family, and nothing behind a login.
- Never invent a number, a result, a client, a review or a deadline.
