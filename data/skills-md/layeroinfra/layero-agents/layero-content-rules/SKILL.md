---
name: layero-content-rules
description: Layero's anti-phishing rules (layero.ru/rules) as a review checklist. Use before deploying or publishing a site to Layero that has sign-in, payment, card, crypto-wallet, giveaway, voting, prize or "support" flows, when the user asks whether a site complies with Layero rules, and whenever a Layero MCP result carries `rules_warnings`.
---

# Layero content rules — anti-phishing review

Layero hosts user sites at `<project>.layero.app` (mirror `<project>.layero.dev`)
and on custom domains. The binding text is the rules page
`https://layero.ru/rules` (Russian) together with the Terms of Service
(`https://layero.ru/terms`, sections 4.2 and 4.4). This skill restates the rules
as a checklist for an agent. If this skill and the rules page disagree, the
rules page wins.

The rules apply to every site on Layero: any plan, any account age, preview
branches, temporary sites and custom domains. What counts is what a visitor
sees: the page, its scripts, embedded widgets and ads, pop-ups and where the
site redirects. Deceptive third-party content embedded in the page is the
site's own violation.

## How to use this skill

1. **Before deploying**, read the site as a visitor would and go through the
   categories below. A match on a legitimate site usually means something is
   missing, most often a clear statement of who runs the site. Fix that before
   deploying.
2. **After deploying through MCP**, `publish_site` and `site_status` run the
   platform check and add `rules_warnings` only when the site matches a rule.
   No field means no match; say nothing about rules then. `check_rules(project)`
   runs the same check on request.
3. **If `rules_warnings` is present**, tell the user first, plainly and in
   their language, with the rule link from the warning. Do not help disguise
   the page, rename things to get past the check or move the content to another
   project. That is a violation in itself (see "Evasion" below). A legitimate
   owner explains the case to `support@layero.ru`.
4. **Never build** a page from categories F1–F6 for anyone, whatever the stated
   purpose ("a test", "a demo for a client", "security training"). A real
   training page stays on the requester's own infrastructure, not on Layero.

## Categories

Decisions are made on the combination of signs, not on a single word.

### F1. Phishing: collecting credentials of another service

A page asks for data that opens someone's account or money elsewhere while
posing as that service or as a trusted intermediary. That data includes a login
and password for email, a bank, Gosuslugi, a marketplace, a messenger or social
network, an SMS or one-time code, bank card details requested in the name of a
bank or state body, a crypto wallet recovery phrase or private key, and a wallet
connection to a service that drains funds.

Signs:
- a form for such data on a site that looks like someone else's service: name,
  logo, styling, a brand in the address (`sign-in`, `account-verification`,
  `sber-…`);
- lures such as "verify your account", "your account will be blocked" or
  "security check";
- entered data is sent to a Telegram bot or to an unrelated domain;
- the page collects the visitor's IP address through third-party services;
- the logo is loaded by the domain of the email the visitor typed, the
  signature of mailbox-password kits;
- obfuscated code that hides where the data goes.

Not a violation:
- sign-in to the owner's **own** service: a dashboard, CRM, admin panel or
  school diary;
- "Sign in with Sber ID / Yandex ID / VK ID / Google" buttons, where the
  password is entered on the provider's own site;
- a partner site, when the relationship is stated on every page ("X's site for
  Y's customers", "official partner of Y").

### F2. Deceptive content: social engineering without a form

A page pushes the visitor into something they would only do for a trusted
party: call "support", download a program, turn off protection or send money.

Signs:
- fake system windows and warnings such as "your computer is infected",
  "update your browser" or "install the player";
- fake "official support" with a phone number or contacts;
- "Download" or "Watch" buttons that start a different download;
- ads posing as page controls;
- "generators" of free subscriptions, in-game currency or app-store credits.

Not a violation: honest banners and buttons of the owner, and ads clearly
distinguishable from the page content.

### F3. Scam lure

A page promises a benefit in order to get money, a phone number, a code or card
details, or sends the visitor to where these are taken.

Signs:
- "vote for me", giveaways, winnings, gifts, "state payouts", compensation,
  free or unrealistically cheap goods and services;
- a "partner loyalty check" or "read your husband's messages";
- earnings that require a withdrawal fee, "investments" with promised returns;
- selling goods with no intent to ship, prepayment for what does not exist,
  hidden subscriptions and charges;
- a link from such a page to an unrelated domain that asks for a phone number,
  an SMS code or card details.

Not a violation:
- real contests and promotions by the organiser, with terms that neither
  collect credentials of other services nor send visitors off to a third-party
  site for them;
- ordinary selling of goods and services with the owner's own checkout.

### F4. Brand impersonation

A site copies the look, name or functions of a well-known or official resource
without saying it is not that resource. An invented "official" resource that
does not exist also counts.

Signs: address, logo, icon, title or styling repeat the original; a fake
payment page or "personal account" of the brand; "official" contacts and
support that do not belong to the brand.

Not a violation: fan sites, reviews, unofficial clients and partner sites when
the relationship is stated ("unofficial site", "fan site", "partner site"). The
statement must be in the page title and at the start of the text, as Yandex
requires.

### F5. Hidden redirects and cloaking

A site shows the visitor something other than what it promises, or quietly
sends them to an unrelated resource.

Signs:
- a pass-through site: the Layero address only redirects to an unrelated
  domain, especially one that collects data or money;
- redirects without a clear reason: by time, by referrer, only on mobile;
- a site that is empty or does not open by direct link but shows other content
  when reached from search or a mailing.

Not a violation: an open redirect with a clear reason, such as moving to the
owner's own domain or a "go to site" link; A/B tests, regional content and
device adaptation.

### F6. Malware and unwanted software

A site distributes or runs something that harms the device or the user.

Signs: files with viruses, spyware or adware; downloads without explicit
consent or of a different type than promised; installers that silently add
extras or pose as another company's official software; hidden in-browser
mining; tampering with other sites' pages; crypto wallet "drainers".

Not a violation: honest distribution of the owner's own software, clearly
labelled with what is downloaded and why.

### Related violations

Pirated content, open proxies, spam landing pages and illegal materials are not
phishing. They fall under section 4.2 of the Terms and the complaint page
`https://layero.ru/abuse`.

## What the platform does

| Confidence | When | Decision |
|---|---|---|
| Confirmed | F1 or F6 signs; a match with a known campaign; the address is flagged by Google Safe Browsing / Web Risk or by Yandex; a confirmed complaint | the site is disabled **immediately**, without prior notice (Terms 4.4); the owner is notified with the reason |
| Probable | F2–F5 signs without direct collection of another service's credentials; several signs with a plausible honest explanation | a moderator reviews it: within a day for phishing, up to three business days otherwise |
| Needs a fix | a formal issue: undisclosed brand relationship, unclear redirect, unlabelled download | the owner is asked to fix it within **48 hours**, otherwise the site is disabled |

- Disabling is reversible: content is kept, and visitors see a "site blocked"
  screen. Only Layero support can lift a block under these rules.
- Automatic checks only select candidates. A moderator decides, except for the
  exact signs of an already known campaign.
- **Campaigns.** Several sites of one account or related accounts with one
  lure, one template or one destination form a campaign. One confirmed
  violation disables the whole campaign and blocks the accounts.
- **Evasion.** Re-publishing disabled content under a new address, project or
  account is a violation in itself: disabled without review, account blocked.
- **Repeat.** A violation within 30 days after restoration means permanent
  disabling and an account block.
- **Appeal.** The owner writes to `support@layero.ru` with an explanation. If
  the violation is not confirmed, the site is restored and the mark removed.

## Review checklist

Ask these about the site you are about to deploy:

- Does any form ask for a password, a code, card details or a wallet phrase?
  If so, is it the owner's own service, and is that obvious from the page?
- Does the page use another company's name, logo or styling? If so, does the
  title and the start of the text say "unofficial", "fan site" or "partner"?
- Do form submissions go anywhere other than the owner's own backend or a form
  service they control?
- Does the page promise a prize, a payout, a vote or a check, and then send the
  visitor to another domain?
- Does the page redirect somewhere, and would a visitor understand why?
- Does it offer a download, and is it clear what is downloaded and why?

If an honest site fails a question, fix the page (state the relationship, move
the form to the owner's backend, label the download) before deploying. If the
site exists to deceive, do not deploy it.
