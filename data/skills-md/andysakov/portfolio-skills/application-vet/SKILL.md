---
name: application-vet
description: "Vet Temi's job applications against what his portfolio site can actually prove, at three points: before applying (is this role a fit, what are the gaps, and what lens would it get), before sending (does the letter or form answer cite only real numbers, link a live lens, and avoid the banned tells), and after sending (which applications were opened or read, and what to do about each). Use when he shares a job post and asks whether to apply, asks to check or vet a cover letter or application before it goes out, or asks which applications to follow up on, nudge or drop."
---

# Application vet

Temi's portfolio site (`AndySakov/obafemiteminife`) is the source of truth for what he can claim: numbers live in
`src/content/claims.json`, the problems he's solved in `src/content/work/`, tools and where he used them in
`src/content/toolbox.json`, and his roles in `src/content/profile.json`. This skill checks applications
against that, at three points. `npm run vet` does the mechanical part, and you do the judgment.

## Find the site repository first

Everything below runs in a checkout of the site, `AndySakov/obafemiteminife`, and every path (`src/content/...`,
`lenses/private/`, `scripts/...`) is relative to it. This skill lives in its own repository, so locate the site
before doing anything else:

1. If the current directory is the site (its `package.json` has `"name": "obafemiteminife"`), use it.
2. Otherwise try `$PORTFOLIO_REPO`, then `~/obafemiteminife`, `~/code/obafemiteminife` and
   `~/Projects/obafemiteminife`.
3. Otherwise clone it. In a cloud session, attach the repository first (`add_repo`), then clone it.
   Locally, run `git clone https://github.com/AndySakov/obafemiteminife ~/obafemiteminife`.

Then `git pull` so the claims and lenses are current. Run `npm ci` if `node_modules` is missing. Run every
`npm run lens` and `npm run vet` command from that directory.

## Where it sits in the application stack

```
jev-job-sweep    shortlists roles from a large catalogue
application-vet  fit: apply, maybe or skip, with the gaps          <- this skill
portfolio-lens   makes the link, using the lens this skill proposed
write-as-temi    drafts the letter or form answers
application-vet  check: the draft before it goes out               <- this skill
send-as-temi     sends it
application-vet  triage: what happened to every live lens          <- this skill
```

## 1. Fit, before applying

1. Get the post's full text. Fetch the URL or use what he pasted. Save it to a scratch file outside the
   repository. A job post names a company he's applying to, so it never gets committed.
2. Run the matcher, and read the evidence it matched against:
   ```bash
   npm run vet -- fit <post.txt>
   npm run vet -- evidence
   ```
   `fit` lists:
   - the tools in the post that are on his board, and where he used each one;
   - the toolbox needs and tags the post leans on, with a suggested framing and lead;
   - the lines a person has to judge: years asked, location, visa, clearance and degree.

   It matches words, so it misses tools that aren't on the board. Read the post yourself for those.
3. Go through the post's requirements one by one, and put each into one of three columns:
   - **Proven:** a claim id, a problem page slug, or a tool with the employer where he used it. Name it.
   - **Adjacent:** he's done the neighbouring thing (Kafka asked, and he's used SQS). Say what bridges it.
   - **Gap:** nothing on the site backs it. Don't invent a bridge.
4. Check the hard requirements against his profile.
   - **Years:** he has been paid for this since 2020, which is the `paidYears` value. A "7+ years" ask is a
     stretch, not a disqualifier, unless the post is strict about it.
   - **Location and time zone:** he's in Nairobi (UTC+3).
   - **Visa:** he's based in Nairobi, so a role based elsewhere needs sponsorship unless it's remote.
   - **Degree:** he holds a BIT (Hons) from Lincoln University College, Malaysia.

   Any one of these can end it. Location and visa usually do.
5. Give a verdict:
   - **Apply:** every must-have is proven or adjacent, and no hard requirement rules him out.
   - **Maybe:** one must-have is a gap, or a hard requirement is unclear. Say exactly what would settle it,
     for example a question for the recruiter.
   - **Skip:** a hard requirement rules him out, or the core of the role is a gap. One line on why is
     enough.
6. For Apply or Maybe, propose the lens:
   - framing, lead (three problem pages), emphasis tags and need;
   - start from `fit`'s suggestion, then correct it with your reading. Keep employers mixed in the lead.

   Hand that to `portfolio-lens` to create. Don't create it from this skill.

Report it as a short table (requirement, column, evidence), then the verdict and the proposed lens. Keep the
whole thing readable in a minute.

## 2. Check, before sending

1. Save the draft (letter, form answers, or message) to a scratch file, and run:
   ```bash
   npm run vet -- check <draft.txt> --lens <token>
   ```
   It exits non-zero on any issue:
   - **Numbers:** a number the site doesn't state anywhere, or years of experience above his paid years.
   - **Punctuation:** em or en dashes, or semicolons.
   - **Tooling:** any mention of the lens, the tailoring, tracking or an open, or a `?me` link (which would
     hide that reader's opens).
   - **The link:** the lens link is missing, belongs to another lens, or doesn't return 200 on the live site.
2. Then read it against the evidence yourself, for what a script can't see:
   - Every claim maps to something on the site, at the right employer. Inverter Network, JobStash and Betty
     stay separate, and nothing from one is credited to another. Credited work stays credited: the
     recommendation engine was his design and David Leonardi's build, and the research crawler's later layers
     are David's.
   - Roles, titles and dates match `profile.history`. No promotions, no stretched dates.
   - The letter's emphasis matches the lens's lead. If the letter leans on billing, the lens shouldn't lead
     with ranking.
   - No overclaims in the verbs: "built" when he built it, "led" only where he led.
3. Report the issues as a short list, each with the fix. If it's clean, say so in one line. Fixing the prose
   is `write-as-temi`'s job; this skill only says what's wrong.

## 3. Triage, after sending

```bash
npm run vet -- triage
```

It sorts every live lens into one of three groups, each with a next action and date:
- **Read something:** a person engaged. Follow up 7 days after sending, using the `write-as-temi` follow-up
  register.
- **Opened, nothing read:** they skimmed it. Wait, then one light follow-up is fair after 7 days.
- **Never opened:** after 7 days, nudge once through a different channel than the application (for example,
  the recruiter on LinkedIn). After 21 days, drop it.

The day thresholds are constants at the top of `scripts/vet.mjs`. Relay the groups as they are, and add
anything the receipts can't show that you know from the conversation (a reply already came in, an interview
is booked).

**Never reference an open or a read in a follow-up**, not even obliquely. The follow-up reads as ordinary
timing.

## Setup

- `fit`, `check` and `evidence` work offline, apart from `check`'s live-link test.
- `triage` needs `SITE_URL` (it defaults to the live site) and `ADMIN_TOKEN`. In 1Password the token is
  "Portfolio ADMIN_TOKEN", in the Automation vault.

## Rules

- **The site is the ceiling.** A claim the site can't back stays out of the application, however true it
  might be. If Temi says something new is true, it goes into `claims.json` first (his call, with `employer`
  and `when`), and only then into applications.
- **Nothing company-specific gets committed:** no job posts, drafts or lens files. The repository is public.
- **Vetting decides, it doesn't write.** Drafting is `write-as-temi`, and the link is `portfolio-lens`.
