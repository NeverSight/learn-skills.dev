---
name: linkedin-profile-optimizer
description: "Use this skill when a seller, founder or SDR needs a LinkedIn profile that converts prospects instead of reading like a resume: \"optimise my LinkedIn profile\", \"rewrite my headline\", \"make my profile buyer-focused\", \"why don't prospects accept my requests\". Rewrites the headline, About section, featured items, banner message and experience entries around the buyer's problem and proof, and checks the profile from a prospect's point of view. Built for social selling and outbound."
license: MIT
metadata:
  title: LinkedIn profile optimizer
  category: linkedin
  tags: "SDR, Founders, Sales, Agencies"
  author: prosyo
  version: "1.0.0"
  keywords: "linkedin profile optimization for sales, linkedin headline for sales reps, buyer focused linkedin profile, claude linkedin profile skill, linkedin about section examples"
  inputs: "Current profile text, Who you sell to, Proof and results"
  outputs: "New headline options, About section, Featured and banner plan, Experience rewrites"
---

Use this before running LinkedIn outreach. Prospects look at your profile before accepting or replying; a resume-style profile tells them you want something from them, a buyer-focused one tells them why talking to you is useful.

## Inputs

- The current profile text: headline, About, experience, featured.
- Who you sell to and the problem you solve.
- Proof: results, customers you can name, content you have made.

## The play

### 1. Headline: who you help and with what
Formula: **I help <who> <achieve outcome or fix problem>** | proof or specialism. Under 220 characters, front-loaded because only the first part shows in search and invitations.

- Resume: "Account Executive at Acme"
- Buyer-focused: "Helping restaurant groups close payroll in a day, not a week | Account Executive at Acme"

### 2. About section: the buyer's story
Read [references/profile-templates.md](references/profile-templates.md) for the About structure and three examples. Short version:
1. A first line about the reader's problem (only the first lines show before "see more").
2. What you have seen working with people like them.
3. How you help, in plain words.
4. Proof: one or two results.
5. A low-pressure invitation to talk.

### 3. Featured and banner
- Banner: one line on what you help with, plus a visual cue of the product or result. Not a stock skyline.
- Featured: a customer story, a useful resource and your best post. No product brochure as the first item.

### 4. Experience
Current role written for buyers: what customers get from working with you, not your quota attainment. Earlier roles: one line each unless they add credibility with this buyer.

### 5. The prospect test
Read the top of the profile as a target buyer, on a phone, for five seconds. Do they know who you help and why it matters to them?

## What good looks like

- The headline names the buyer and the outcome.
- The first two lines of About are about the reader.
- Proof is specific and true.
- The common mistake is "President's Club 3x, 147% of quota", which impresses your manager and signals to buyers that they are a target.

## Rules

- MUST keep every claim true and approved for public use.
- MUST write the first lines of the headline and About for the buyer.
- NEVER invent clients, results or titles.

## Example prompts

- "Rewrite my LinkedIn profile. I'm an SDR selling cybersecurity to mid-market IT leaders."
- "Give me 5 headline options for a founder selling to restaurant groups."
- "Review my profile as if you were a VP Sales I'm prospecting."
