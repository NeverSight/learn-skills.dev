---
name: portfolio-lens
description: "Make a tailored portfolio link (a lens) on Temi's site for one job application, or check whether a lens link has been opened and what was read. Use whenever an application, cover letter, form answer or recruiter message should carry a portfolio link, when he asks for a lens or a portfolio link for a role, and when he asks whether a company opened or read his portfolio."
---

# Portfolio lens

Temi's site (`AndySakov/obafemiteminife`) has a general version at `/` and any number of
tailored versions at `/l/<token>/`. A tailored version is a **lens**: one JSON file that decides which framing
leads, which postmortems come first, what gets highlighted, and an optional short note.

**The repository is public, so real lenses never go in it.** A lens names the company an application went to.
`lens new` writes it to `lenses/private/`, which git ignores, and `lens push` stores it in the site's Workers KV,
where the page reads it on each visit. No commit or deploy is involved. Only the made-up demo lenses live in
`lenses/`, and the build fails if a real one lands there. `push`, `pull`, `rm`, `opens` and `list` need
`ADMIN_TOKEN` (the Worker secret) and `SITE_URL` (the live site) in the environment.

**A lens selects, orders, and weights existing content.** Numbers live in `src/content/claims.json` and the
postmortems. A lens note or headline must not introduce a number that isn't already on the site.

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
jev-job-sweep    shortlists the role
application-vet  fit: apply, maybe or skip, and the proposed lens
portfolio-lens   makes the link            <- this skill
write-as-temi    drafts the letter or form answers, with the link in the signature block
application-vet  check: the draft before it goes out
send-as-temi     sends it
application-vet  triage: what happened to every live lens, and what to do next
```

The link goes in the signature block, under GitHub. Use the URL `lens new` prints, without `https://`:

```
Teminife Obafemi
<site>/l/<token>
github.com/AndySakov
```

**Never mention the tailoring, the lens, or the open receipts in an application.** Same standing rule as
`write-as-temi`: never cite the tooling. The recipient sees the "Made for" line on
their own, and that's the charm of it.

Use the Teminife Obafemi identity. The site is under that name only, so a lens never goes on an Andy Werner
application.

## Making a lens

1. **Get the job post text.** Fetch the URL or use the pasted text. Note the company, the exact role title and
   the URL.
2. **Read the catalog** so you choose from what exists:
   ```bash
   npm run lens -- catalog
   ```
   It prints the framings, every postmortem (slug, title, dek, employer, tags), the notes, the section keys,
   the allowed emphasis tags, and the limits.
3. **Decide the lens.**
   - `framing`: the framing whose lede the hiring manager should read first.

     The framings mirror the clusters in Temi's Notion job tracker. Examples are real past applications.

     | The role is mostly about | framing | Past examples |
     |---|---|---|
     | payments, billing, ledgers, banking, lending, treasury | `payments` | Cursor Billing, Alpaca Ledger, Noricum, OpenFX |
     | protocol backends, wallets, DeFi execution, chain infra | `onchain` | Uneven Labs Relay, Kamino, Alchemy, Tangem |
     | agent runtimes, LLM platforms, inference, forward-deployed AI | `agents` | Glean Agentic Runtime, Eigen, Oyster, Antimetal |
     | exchanges, perps, market data, clearing, order books | `trading` | Blockchain.com, Propr, t+, Ethena |
     | APIs, platform, integrations, product backends, devtools | `platform` | Railway, Supabase, Camunda, Enode |
     | fraud, AML, risk, trust and safety | `risk` | Grid, Feedzai, GoMining, Wikimedia Safety |
     | data engineering, indexing, search, ranking | `data` | Dune, edisyl, Wikidata, MixRank |
     | Scala, Effect, ZIO, functional programming | `functional` | Superformula, Tiko, Journi |
     | a generalist backend role, or nothing dominates | `default` | TypeSafe, Sticker Mule |

     Preview every framing at `/framings/` on the live site before choosing.

     Each framing brings its own headline, a one-line blurb and three numbers, and opens the toolbox on a matching need.

   - `need` (optional): the toolbox need to open on, one of the `needs` ids in the catalog. Leave it out to
     let the framing choose. Set it when the job's core requirement is narrower than the framing, for
     example `queue` for a Kafka-heavy platform role.

   - `headline` (optional): one line, at most 56 characters, naming the job's core requirement in Temi's
     terms, for when no framing's headline fits. Wrap the last few words in `*...*` to light them amber, for
     example `"I keep order books *consistent under load.*"`, or for an onchain indexing role
     `"I build pipelines for chains *that rewrite their own history.*"`. No digits, no colon or question mark, no dashes.
     It must be something his work backs up, because the intro and the postmortems underneath it have to prove
     it. No numbers in a headline. Draft it with the `copywriting` skill (two or three candidates, keep the one that passes its
     three-question gate) and check it with `stop-slop`. Leave it out when the framing's headline already fits.

   - `lead`: the three postmortems (five at most) a reader for this role should see first, most relevant
     first. Keep employers honest. Two Inverter pieces and one JobStash piece reads better than three of one.
     Only lead with `finding-the-same-product-twice` (Betty, never released) for a Rust-centred role.
   - `hero` (optional): what follows the headline block and its three numbers. `mechanism` adds the live
     sequencing simulation right under them, for readers who will enjoy breaking it (payments, onchain,
     trading, distributed systems, and a technical reader). `toolbox` or `headline` keep the default, where
     the toolbox comes next, opened on the lens's `need`. The page is built for a busy, possibly
     non-technical reader, so only use `mechanism` when the reader is an engineer.
   - `sections`: leave it out for the default order (`toolbox`, `work`, `ledger`): Toolbox, Work (three
     cards and a link to /work/, which holds every write-up, the side projects and the writing), Experience,
     then Contact. On the page these sections are called Problems I've solved, Projects and Essays.
     Optional extras: `public` (Projects: client work for Delicious Homes, NAPTIN and Stomp, then OmniMarket, METIS, Watch, nestjs-neogma and a merged neogma PR; worth adding for
     Rust, trading, Effect, agent, AI-tooling, NestJS, Neo4j, Cloudflare Workers or end-to-end product roles), `notes` (Writing) and `inflight` (Live demo, for an engineering reader).
     Put `work` first when the role is senior. Add an extra only when it clearly helps this reader; the page
     is meant to be read in under a minute.
   - `emphasis`: three to six tags from the catalog that the post leans on. They put accent dots on matching
     work cards and experience rows.
   - `note` (optional): one sentence is best, two at most, at most 300 characters. It sits in the hero block, so keep it short. Draft it with the `copywriting` skill,
     then run `humanizer` and `stop-slop` over it. Peer register, no opener about their posting, no em dashes, no
     semicolons, no new numbers. It says why this role, concretely. If there's nothing specific to say, leave
     it out. A generic note is worse than none.
4. **Create it**, then fill in the fields you decided:
   ```bash
   npm run lens -- new --company "Stripe" --role "Senior Backend Engineer" --url "https://..." --framing payments
   ```
   This prints `{ file, url, token }`. The token is random and unguessable. Edit the printed file to add
   `lead`, `emphasis`, and optionally `headline`, `hero`, `need`, `sections` and `note`.
5. **Push it live.** This validates the lens, then stores it:
   ```bash
   npm run lens -- push <token>
   ```
   Never commit the file. Fetch the URL and confirm it returns 200 before handing it over. KV can take up to a
   minute to reach every region, so retry once if the first fetch is a 404. To change a live lens, edit its file
   and push again. In a fresh checkout, `npm run lens -- pull` copies every live lens into `lenses/private/`.
7. **Hand back** the URL, the framing and the lead you picked, in one or two lines. If Temi wants to look at
   it himself, give him the URL with `?me` on the end. That marks his browser as the owner, so his own visits
   never count as opens. Never put `?me` in anything that gets sent.

## Open receipts

A lens page reports an **open** after it has been visible for three seconds, and a **read** when a postmortem
or note is opened from it and stays visible for eight. Link-preview bots, headless browsers and Temi's own
browser are filtered out. Each receipt stores the time, the rough city and country, and the user agent.

```bash
npm run lens -- opens             # every lens
npm run lens -- opens <token>     # one lens
npm run lens -- opens --json      # raw events
```

If Telegram is configured as a Worker secret on Cloudflare, each open and read also pings him there.

How to use them:
- **Opened, and read a postmortem:** a person engaged. Worth a follow-up when the normal follow-up timing
  comes round, using the `write-as-temi` follow-up register.
- **Opened, no reads:** skimmed. Nothing to do.
- **Not opened:** the application hasn't been looked at yet, or the link never made it past the ATS.

**Never reference an open in a follow-up**, not even obliquely. "Saw you had a look" is the fastest way to
make the whole site feel like surveillance.

## Rules

- A new fact goes into `src/content/claims.json` (with `employer` and `when`), and only Temi adds facts.
  New tools go into `src/content/toolbox.json`, and only ones on his master CV.
- Never merge employers in one claim. Inverter Network, JobStash and Betty stay separate, same as on the CV.
- One lens per application. Don't reuse a lens across companies, because the note and the bar name the company.
- Don't take a lens down (`lens rm`) after it has been sent, because the link would break. Old lenses cost nothing.
- Never commit a real lens. The repository is public, and a lens names a company he's applied to.
