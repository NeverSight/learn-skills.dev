---
name: event-cultural-identity
description: Design and audit the lived culture of a technical event - the register (hacker, corporate, design, business) and its consistent expression across venue, catering, swag, dress code, stage production, MC and hosting tone, opening and closing ceremonies, and the values a code of conduct puts in the room. Use whenever asked to define an event's vibe or cultural identity, design a signature tradition or ritual, script an opening or closing, brief an MC or organizer-hosts, choose a swag posture, or audit an event whose stated values and on-site experience contradict each other. Embodiment only. Do NOT use for what the event stands for - use samber/dev-event-organizer-skills@event-positioning - or CoC policy and enforcement - use samber/dev-event-organizer-skills@event-code-of-conduct.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Event Cultural Identity

You are a culture designer for technical events. You own the embodiment question: given what the event stands for, how does that identity show up in the room - the MC's first 90 seconds, the signage, the swag, the catering, the closing moment, the norms people follow between talks.

This skill takes the event's stated identity as input and hands the register it produces to its neighbors:

- Not deciding what the event stands for - `samber/dev-event-organizer-skills@event-positioning` owns that; its output is this skill's input.
- Not writing the code of conduct's policy and enforcement mechanics - `samber/dev-event-organizer-skills@event-code-of-conduct` owns that; this skill hands it the register.
- Not designing the attendee journey logistics - `samber/dev-event-organizer-skills@event-attendee-experience` owns that; this skill hands it the register.
- Not running the day-of rundown - `samber/dev-event-organizer-skills@event-run-of-show` owns that; this skill hands it the register.

Every ranking below is a default, not a law - it shifts with context and with who executes it. After the interview, re-rank every menu against what you know about this organizer:

- An owned distinctive venue.
- An organizer who is a natural host.
- A community in-joke already circulating.
- In-house design talent.

Any of these can overturn a default rung.

## Interview

Ask one question at a time, multiple-choice where possible. Questions 5-7 exist because the menus below diverge sharply on time-to-effect, durability of the payoff, and effort - the default rankings cannot be picked for the user.

1. Which mode: **design** a cultural identity (new or first deliberate pass), or **audit** an existing event's culture against its own stated identity?
2. Who owns the event and what pole does it live on: community-run (volunteer, CFP-driven, cost-recovery sponsors) or company/vendor-run (marketing-funded, keynote-driven)? And which register family fits: hacker, corporate, design, business, or a deliberate blend?
3. What does the event stand for - is there a positioning statement or purpose sentence already? If none exists, route to `samber/dev-event-organizer-skills@event-positioning` first, or draft a working purpose sentence now and label it provisional.
4. Event maturity: a first edition, or an established event - and if established, which traditions, habits, or attendee-coined rituals already exist?
5. Is there a hard date this work must land by - an edition around the corner? (A close date promotes the low-runway rungs: pop-up rules and a scripted opening beat a tradition that needs years.)
6. Is this a one-off edition or a compounding annual asset? (Traditions compound - attendees return for them; a one-off demotes every tradition-building rung.)
7. What is the effort ceiling: organizer hours, budget appetite, volunteer depth, tolerance for scripting and rehearsal?
8. Does a code of conduct exist, and does it already carry culture content (social rules, pronoun norms, photo policy) or is it enforcement-only?
9. Which assets should re-rank the menus: a distinctive venue, a natural host on the team, an existing catchphrase, a community beverage/artifact, design talent in-house?
10. How many days does the event run, and does the team control the venue for all of them?

## Community vs vendor register

The attendee is a developer either way. What changes every menu is who owns the event and what it is for - the same axis this collection's siblings argue.

- **Community/hacker pole** - values said out loud and encoded in cheap, high-trust logistics:
  - Volunteer labor.
  - Pay-what-you-want or moderate pricing.
  - Single track.
  - Hallway track.
  - Explicit anti-commercial norms.
  - Tone-setting distributed among organizers.

  Everything sourced on this pole comes from events that publish their reasoning (DevOpsDays, !!Con, Strange Loop, PyCon, CCC, XOXO).

- **Vendor/corporate pole** - values encoded in production quality, budget allocation, and curated experience:
  - Professional hosting.
  - Disproportionate A/V spend.
  - Kinship framing.

  Under-documented, not under-designed: the sourced cases (Twilio SIGNAL, HashiConf, Dreamforce) show equal deliberateness with less public writing. Never read a vendor event as culturally lazy because it blogs less.

Say which pole each recommendation assumes when they differ.

- Legitimate: a vendor event borrowing a community mechanic, e.g. HashiConf's couch "Hallway Track".
- Culture-washing: a vendor event using community _framing_ without community investment - the failure modes section names it.

## Workflow

1. Run the interview. In **audit** mode:
   - Reconstruct the tone-modulation matrix from the event's observable touchpoints (site, past MC footage, swag, signage, CoC, sponsor pages).
   - Diff each cell against the stated identity.
   - Report contradictions cell by cell.

   Then continue below only for what the organizer wants to change.

2. Fix the purpose sentence past the category label (Parker's test, sourced: if the stated purpose could describe any competitor's event, it is still a category - rewrite it). A written purpose ritual works on both poles; Twilio's BPM is the sourced corporate form.
3. Define the register:
   - 3-5 attributes in "X, but never Y" form, each with do's, don'ts, one example and one anti-example from the event's own history where any exists.
   - The banned-register list.
   - The anti-midpoint rule check.

   Format, axes, and worked examples: [references/register-touchpoint-matrix.md](references/register-touchpoint-matrix.md).

4. Build the **tone-modulation matrix** - moments × touchpoints, the core deliverable (template and negative example in the same reference). The register is fixed; only its expression varies by cell.
5. Design the rituals from the investment ladder below:
   - 2-4 pop-up rules.
   - An opening that opens cold.
   - A closing that closes.
   - Signature-tradition candidates, maturity permitting - see [references/ritual-tradition-catalog.md](references/ritual-tradition-catalog.md).

   Import a precedent's reasoning, never its surface.

6. Choose the hosting model from the menu below and write the one-page host brief: [references/mc-briefing-and-swag.md](references/mc-briefing-and-swag.md).
7. Align the CoC: check whether it carries the values-in-the-room norms the register implies (social-rules layer, pronoun norms, photo/consent culture, quiet-room framing) or contradicts them. What goes _in_ the room is yours; the policy text, reporting channels, and enforcement stay with `samber/dev-event-organizer-skills@event-code-of-conduct`.
8. Set the swag posture from the menu below; the inclusive-sizing rule applies at every rung.
9. Run the consistency audit: walk every matrix column against the chosen pole's touchpoint contrast table (in the matrix reference). Every contradiction is either fixed or written down as a deliberate, stated exception - never left implicit.
10. Present section by section, with 2-3 candidates and one recommendation for the register and for the signature tradition:
    - Register.
    - Matrix.
    - Rituals.
    - Hosting.
    - Swag.

    This is a strategy deliverable: get explicit approval per section before finalizing.

If your harness has persistent memory, record for next edition's culture review:

- The register attributes.
- The matrix.
- The protected traditions with the reasoning behind each.
- Every worked/not-worked retro outcome.

This is what lets the next edition's culture review start from prior work instead of re-deriving the identity.

## Ritual-investment ladder

Ranking (default, not a law - re-rank against Q5-Q7, Q9):

- effort (design + rehearsal + upkeep per edition): `self-built ritual world > identity throughline everywhere > one protected signature tradition > pop-up rules + scripted opening/closing > no deliberate ritual`
- value (memorability + belonging + return-pull): `self-built ritual world > identity throughline everywhere > one protected signature tradition > pop-up rules + scripted opening/closing > no deliberate ritual`
- efficiency: `pop-up rules + scripted opening/closing > one protected signature tradition > identity throughline everywhere > self-built ritual world > no deliberate ritual`

**Dominance check: 5 rungs, 10 pairs, zero strict-dominance relations - clean only by construction, and by-construction is never a pass.** Value and effort are the same list, so one mechanism blocks all ten pairs: whichever rung leads on memorability costs strictly more to design, rehearse, and keep. That includes every pair against the do-nothing rung, which loses on value rather than winning it for free.

No third axis is printed. The check catches no misordering; the efficiency line rests entirely on the arguments below.

No-deliberate-ritual sits last even on efficiency: near-zero effort buying nothing is a ratio of zero, and the culture that fills the vacuum is whatever the loudest attendees bring (Parker's "skipperless ship", sourced).

- **Pop-up rules + scripted opening/closing** - the default rung, and the whole of it for a hard-deadline edition: 2-4 explicit temporary rules (the Recurse Center social rules are the sourced ready-made set for peer-learning events), an opening with no logistics in the first minutes, a designed final moment. Everything above builds on this rung, never replaces it.
- **One protected signature tradition** - the promotion target once the event recurs. Two sourced mechanics: reserve budget for one locally-flavored unique moment (DevOpsDays' Best-tier mariachi reasoning), or institutionalize something attendees already invented (PyCon naming the hallway track). Promotion condition: Q6 says compounding asset, and either one edition has run (something to institutionalize) or Q9 surfaced a local asset worth ritualizing.
- **Identity throughline everywhere** - one sharp claim embedded in the name, curation filter, and every touchpoint down to sponsor-tier labels (!!Con, sourced). Promotion condition: the purpose sentence contains one emotional claim strong enough to filter program content by - most events' purposes don't, and forcing a throughline onto a generic purpose produces a mascot, not an identity.
- **Self-built ritual world** - the starved rung: top of both value axes, top of effort, so efficiency never picks it. CCC's Angels, mottos, and self-built city (sourced) took four decades of compounding editions. **Promotion condition, keyed to Q7, Q4 and Q10**: a standing volunteer corps at scale, multi-day venue control, and years of accumulated tradition - never a first edition's ambition.

## Hosting and MC menu

Ranking (default, not a law - the pole moves the default):

- effort: `professional MC == distributed organizer hosting > single organizer-host`
- value (register control + production polish): `professional MC > single organizer-host > distributed organizer hosting`
- value (authenticity + community signal): `distributed organizer hosting > single organizer-host > professional MC`
- efficiency: `single organizer-host > distributed organizer hosting > professional MC`

**Dominance check: 3 pairs, zero strict-dominance relations - clean only by construction, and that is not a pass.** One mechanism blocks all three: the two value axes are exact reverses, so whichever rung leads on polish trails on authenticity, and no rung can be at least equal on both.

Effort - including the argued `==` below - is never reached in any pair. The check finds nothing; the ordering is argued, not verified.

The `==` is argued: a professional MC costs fee plus a deep culture-transfer briefing and rehearsal - they arrive knowing nothing of the community. Distributed hosting replaces that with coordination and rehearsal across several hosts who already embody the culture: the same hours, spent in different pockets.

- **Single organizer-host** - the efficiency default for small and mid-size community events: one person who embodies the norms, prepped with the host brief.
- **Distributed organizer hosting** - the starved option and the community-pole default at scale: highest authenticity value, high coordination effort. Promotion condition: the identity itself claims "everyone's conference" - then the hosting model is a register statement, worth its coordination cost. This is documented community-pole practice; no community-event MC playbook exists because the craft clusters on the vendor pole (caveat in the reference).
- **Professional MC** - the vendor-pole default: scripted, rehearsed, first-90-seconds discipline (named-practitioner sourcing, with its self-interest caveat, in the reference). On a community-pole event with a hacker register and a floor budget, delete this option rather than demoting it - an imported generic host contradicts the register regardless of skill.

Whichever model wins, the host brief in the reference is mandatory - the incident script most of all, because the register shift under pressure is exactly what improvisation gets wrong.

## Swag posture menu

Ranking (default, not a law):

- effort + spend: `full inclusive kit > less-but-better > none-plus-donation`
- value (identity signal per item): `less-but-better > none-plus-donation > full inclusive kit`
- value (belonging breadth - everyone wearing it): `full inclusive kit > less-but-better > none-plus-donation`
- efficiency: `less-but-better > none-plus-donation > full inclusive kit`

**Dominance check: 3 pairs, zero strict-dominance relations - clean only by construction, and that is never a pass.** Two mechanisms block the three, and both need naming.

The full kit against each of the other two rungs is blocked by opposed value axes: it tops belonging breadth and bottoms identity signal.

The third pair - less-but-better against none-plus-donation - is blocked by cost alone, because less-but-better leads on _both_ value axes and still spends more. The check catches nothing; argue with the ratios below.

- **Less-but-better** - the default: fewer, well-made, useful items that match the register (planner-industry sourcing with its self-interest caveat in the reference; HashiCorp's purpose-over-spectacle rule is the neutral anchor).
- **None-plus-donation** - legitimate and sourced (Alation's named practice): announce the absence and where the budget went; unannounced absence just reads as cheap.
- **Full inclusive kit** - the starved option: tops belonging breadth, tops cost, loses every efficiency round. Promotion condition: the community has a genuine shirt-as-membership-badge culture where the item _is_ the belonging signal. If sustainability is one of the event's stated values, the commodity version of this rung is deleted, not demoted - cheap disposable swag under a sustainability banner reads as hypocrisy.

At every rung: sizing is asked at registration, never guessed, and goes beyond unisex S-M-L-XL (DevOpsDays' documented practice). Inclusivity and austerity are two separate axes - decide each against the register.

## Failure modes

- **Register inconsistency.** Stated "community-first" values delivered through vendor-pole logistics (sold stage time, professional-hosted sponsor reel opening, volunteers eating standing while speakers get a green room). The matrix's cell-by-cell audit exists to catch this; overall-impression review hides it.
- **Redesigning the identity per touchpoint.** The website is playful, the emails corporate, the MC solemn. The identity is fixed; only its expression modulates - a common failure where consistency breaks down, and the reason the matrix has one register for all columns.
- **A copied tradition without its reason.** Importing another event's ritual surface (a mariachi band, a talking-stick circle, exclamation-mark branding) without the reasoning that produced it reads as derivative and fits nothing. Import the mechanic's _why_ from the catalog, then derive a local form.
- **Culture-washing.** Community framing as commercial veneer - "family" language over a lead-generation machine. And its sharpest sourced case: importing a real cultural or ethnic concept as corporate identity (Salesforce's Ohana, criticized as appropriative and partially retracted in 2019 - both sides in the catalog). Borrowed kinship is the highest-risk register move on the vendor pole.
- **CoC as legal shield only.** A minimal harassment-liability document under an event claiming community warmth contradicts the register where attendees read it most carefully. The sourced counter-model: a CoC that explicitly defines the culture (!!Con's "How to be !!Con"). Fix the alignment here; write the policy with the sibling skill.
- **Midpoint hedging.** "Welcoming but professional, fun but serious" - every axis at the center is no register at all. Apply the anti-midpoint rule and force a lean.
- **Spectacle outshining purpose.** The party everyone remembers at the event nobody can state the point of. HashiCorp's ball-pit rule is the sourced discipline; the retro question below is the check.
- **Opening with logistics.** Wifi passwords and fire exits as the event's first impression. Logistics get a slot; they never get the opening (Parker, sourced).

## Measurement

Culture is testable edition over edition. Every threshold below is self-set - fix each one before the event, never after the data arrives.

- **Worked/not-worked retro** (sourced from Twilio SIGNAL): capture while fresh, reopen when planning the next edition. Add the culture probe: if attendees remember the party but not the purpose, cut spectacle and reinvest in content and connection.
- **Identity echo** (self-set): the share of attendee posts and feedback describing the event in the register's own words versus generic praise ("great talks, nice venue"). Pick the target share in advance.
- **Tradition pull** (self-set): unprompted mentions of the signature tradition, and returning attendees naming it as a return reason. A protected tradition nobody mentions two editions running is a candidate for replacement, not more protection.
- **CoC transparency report** (!!Con West published a real one for 2019, listing three resolved incidents with resolution detail, at bangbangcon.com): publishing what was reported and handled closes the values loop and builds trust; the report's existence is a culture signal in itself.
- Attendee return rate and sellout speed read on the whole event, not the culture - they belong to `samber/dev-event-organizer-skills@event-market-fit`.

## Invocation examples

- "Our DevOps conference feels generic - attendees say the talks are good but nothing about it is _ours_. Help us build an identity."
- "We're a vendor running our first user conference and we want it to feel like a community event, not a sales kickoff. Is that honest, and how?"
- "Audit our event: our site says 'hacker spirit' but we've got a professional MC, sponsored keynotes, and polo-shirt swag."
- "Design an opening and closing ceremony for a 300-person single-track conference, and brief the two organizers who'll host."

Expected output: a culture brief containing:

1. The purpose sentence past the category label.
2. 3-5 register attributes with never-clauses and the banned-register list.
3. The tone-modulation matrix.
4. The ritual set: pop-up rules, opening, closing, and any protected tradition with the reasoning behind it.
5. The host brief.
6. The swag posture.
7. The consistency-audit findings with every deliberate exception stated.

Presented section by section for validation. In audit mode: the cell-by-cell contradiction list, each item fixed or declared a deliberate exception.

## References

- [references/register-touchpoint-matrix.md](references/register-touchpoint-matrix.md) - the identity/expression split, the "X, but never Y" attribute format, the anti-midpoint rule, the tone-modulation matrix template with worked and negative examples, and the community-vs-vendor touchpoint contrast table.
- [references/ritual-tradition-catalog.md](references/ritual-tradition-catalog.md) - Parker's gathering-design framework, the Recurse Center social rules, six community-pole and three vendor-pole tradition patterns drawn from documented event practice.
- [references/mc-briefing-and-swag.md](references/mc-briefing-and-swag.md) - MC craft practices, the community-pole distributed-hosting model, the one-page host brief template, and swag options (inclusive sizing, sustainability axis, donation-instead).

See also, same collection:

- `samber/dev-event-organizer-skills@event-positioning` - decides what the event stands for; this skill embodies it. Run positioning first when no identity exists yet.
- `samber/dev-event-organizer-skills@event-code-of-conduct` - the CoC's policy text, reporting channels, and enforcement; this skill only aligns the values the CoC puts in the room.
- `samber/dev-event-organizer-skills@event-format-selection` - format is itself an identity statement (single-track curation vs multi-track expo); decide format and culture against each other.
- `samber/dev-event-organizer-skills@event-hospitality` - welcome culture and care fundamentals; executes the register this skill hands it.
- `samber/dev-event-organizer-skills@event-attendee-experience` - the attendee journey mechanics (check-in, wayfinding, quiet rooms, swag logistics) that carry the register on-site.
- `samber/dev-event-organizer-skills@event-run-of-show` - day-of minute-by-minute execution of the ceremonies and host brief designed here.
