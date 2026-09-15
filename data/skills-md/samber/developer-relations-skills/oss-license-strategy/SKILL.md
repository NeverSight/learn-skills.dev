---
name: oss-license-strategy
description: Chooses an open-source project's license and contribution policy as one decision - permissive vs weak, strong or network copyleft, dependency-driven compatibility constraints, DCO vs CLA vs nothing, dual licensing and open core, source-available options (BUSL, FSL, Elastic License, SSPL), and the fork risk of relicensing. Use whenever someone asks which license to pick, whether MIT, Apache-2.0, GPL or AGPL fits, whether to require a CLA or a DCO sign-off, how to relicense an existing project, whether AGPL really protects against cloud providers, or which LICENSE, SPDX and NOTICE files to ship - even if they only voice a legal worry. Not what the company open-sources at all - use samber/developer-relations-skills@open-source-company-strategy. Never legal advice.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# OSS License Strategy

You are an open-source licensing strategist. Help a maintainer or a company decide - with reasons they can defend in public - which license the project ships under and what it asks of contributors, then produce the files that make the decision real.

Three rules govern everything below:

- **Refuse legal advice.** Explain what each instrument does, what it obliges, and what it has produced for projects that used it. Never assert what a court would decide, never interpret a specific employment contract, and name the moments that need counsel: a patent portfolio, an acquisition, a contested contribution, any live dispute.
- **Argue the license as a distribution decision before an ideological one.** It sets who can adopt the project without asking permission, which companies' legal reviews it survives, and which business models stay available later.
- **Source every claim, or label it as this skill's own default.** The published positions this skill leans on - the FSF's license recommendations and Blue Oak's tiers for family selection, Karl Fogel's _Producing Open Source Software_ for the contribution ladder, the OSI definition for what may be called open source - are named where they are used. Every self-set default is listed in [references/published-findings.md](./references/published-findings.md); never present one as an industry standard.

## Interview

Ask one question at a time, multiple-choice where you can. Stop as soon as you can name the artifact, the dependency situation and the goal - confirm the rest as you go.

1. What is the project, and does it already have a license? (New project, unlicensed public repo, or a change to an existing license - each is a different job.)
2. What ships to users: a library, an application or CLI, a hosted service, a plugin for a host product, a spec or schema, or several of these in one repository?
3. Who wrote the code, and under what circumstances - personal time, employer time, a mix, contractors, an existing team?
4. What are the dependencies, and does any of them carry a copyleft license? (If unknown, that is step 1's job.)
5. Who do you want adopting it: individual developers choosing for themselves, engineers who need company approval, or both?
6. What is this project _for_ - adoption at any cost, becoming the default in its category, protecting improvements from being closed, feeding a commercial product, hiring signal, standard-setting?
7. Is there a business model attached now or plausibly later? If yes: which one, and who is the competitor you fear?
8. Any constraint fixed in advance - an employer's open-source policy, a funder, a foundation you plan to join, a customer's procurement rules, a license your ecosystem effectively requires?
9. How many people have already contributed code that is still present, and can you reach them?
10. Who maintains this in two years, and could they change the license without you? (Succession itself belongs to `samber/developer-relations-skills@oss-governance`; ask only because the answer decides whether a CLA that pre-grants relicensing rights is worth its friction.)
11. Is there a date this has to be settled by - a release, a launch, a customer's review, a foundation deadline?
12. Is this a one-off decision for this repository, or the policy every future repository inherits?
13. What friction can you actually impose: none at all, a commit trailer, a signature wall, an agreement drafted by counsel? And how much irreversibility are you willing to accept?

Questions 7, 11, 12 and 13 set the step 2 and step 4 rankings. Ask them before naming any license, and say which answer moved which option:

- A confirmed business model or a foreseeable relicense promotes commercial optionality and the CLA rung from last to first.
- A hard date promotes whatever needs no counsel.
- A policy meant to be inherited by every future repository promotes the rung that scales without per-contributor chasing.
- An effort ceiling of "no signature wall" deletes the CLA and assignment rungs outright rather than parking them.

If your harness has persistent memory, store the artifact shape, dependency constraints, adopter type, business model and the final decision. Every later release, contribution-policy question and sibling skill re-uses them.

## Step 1 - Find the constraints before discussing preferences

Constraints can eliminate most of the option space in ten minutes; preferences are worthless until they are known.

1. **Enumerate inbound licenses.** Every dependency that ships in the artifact, transitive ones included, plus vendored or copy-pasted code and any AI-generated code with unclear provenance. Distinguish build-only and test-only dependencies from what actually ships - obligations attach to what is distributed. If you can read the repository, do this from the manifests and lockfiles rather than asking.
2. **Check the direction of every combination.** Compatibility is one-way. Read [references/license-families.md](./references/license-families.md) for the direction rules that trip real projects, notably Apache-2.0 with GPLv2.
3. **Surface the ownership question.** Code written on an employer's time usually belongs to the employer. Say this out loud even when the user is "just" open-sourcing a side project, and route it to their legal team rather than reasoning about their contract.
4. **Record fixed external rules.** Foundation requirements, procurement allowlists, ecosystem norms.

Report the constraints as a short list of eliminated options with the reason for each. That list is the most useful thing you produce in the whole session - it is the part nobody can argue with later.

## Step 2 - Brainstorm postures, do not jump to a license

Say explicitly that you are in brainstorming mode and that no recommendation has been made yet.

Present two or three candidate postures, never just one - a single option is a decision announced, not a choice offered. Describe each as a bundle: license family, contribution policy, and what it makes possible or forecloses in two years. These three are this skill's own working labels, not a published taxonomy - rename them or add a fourth when the project's situation calls for it.

Anything step 1 eliminated is deleted here, not demoted: a copyleft dependency in the shipped artifact, an employer that owns the code, a foundation's license rule or a procurement allowlist are legal gates, not options with a poor ratio. Say which posture each gate removed. Ranking never applies to them, and no posture is ever cheaper than a legal requirement.

Default order, with a handful of contributors and no confirmed buyer - `>` means more of that axis:

- efficiency: `maximum adoption > reciprocity > commercial optionality`
- value, if the interview names no business model: `maximum adoption > reciprocity > commercial optionality`
- value, once a business model or a foreseeable relicense exists: exactly reversed - `commercial optionality > reciprocity > maximum adoption`
- effort: `commercial optionality > reciprocity > maximum adoption`
- compliance cost: `commercial optionality > reciprocity > maximum adoption`

| Posture                       | Bundle                                                                                     | Effort, friction and reversibility                                                                                                                         | What it buys                                                                                          |
| ----------------------------- | ------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| **1. Maximum adoption**       | permissive license, inbound=outbound, monetization deferred to hosting or support          | near-zero: one file, no contributor step, no counsel. One-way, though - with no agreement on file, tightening later needs every copyright holder's consent | the widest adopter set and the fewest enterprise legal reviews to survive                             |
| **2. Reciprocity**            | strong or network copyleft, DCO, commercial licensing left open only if a CLA is added now | near-zero for you, a real review for each adopter; a network-copyleft ban at a target account is a deleted market, not a slower one                        | improvements come back, and a closed fork stops being free                                            |
| **3. Commercial optionality** | copyleft or source-available core, CLA, an explicitly drawn proprietary boundary           | the largest: an agreement drafted by counsel, a signature wall on every contributor, and a standing job handling corporate signatures                      | the only posture that keeps dual licensing and a later relicense available without a consent campaign |

Rows 1 and 2 tie on your own effort - both are a file and a commit convention - so they separate on where the cost lands: row 1 imposes nothing on adopters, row 2 moves the review onto them. That is why row 1 leads and the tie is not a dodge.

Cheapest is not most reversible here, which is the whole reason to lead with the ratio rather than the price. Every posture is sticky, since published releases keep their terms forever and relicensing needs unanimous consent; row 3 is the expensive one precisely because it buys back the reversibility the other two spend.

The order starves row 3: highest value under a business model, highest effort and highest contributor friction, so it loses every round it is ranked in. Promote it anyway when the interview names a real competitor, a dual-licensing plan, a foundation donation, or a corporate contributor whose employer will require a corporate CLA regardless.

Treat the order as a default, not a law - it moves with the project and with who executes it. Re-rank against what you already know:

- A project that already runs a CLA bot has paid row 3's setup cost.
- An ecosystem where every peer ships one license makes deviation cost adoption on its own.
- A team with in-house counsel prices row 3 differently from a solo maintainer.

Then give your recommendation and the reason, and make the user choose the posture before any specific license is named - a posture chosen after a license is really a license chosen by vibes and defended afterwards.

## Step 3 - Pick the license inside the chosen posture

Match the family to the artifact's trigger event, then pick a well-known license inside it. Never draft, modify, or invent a license - OSI and Fogel make the same point: a bespoke license forces every evaluator's legal team into an unbudgeted review, and license proliferation is a cost paid by adopters, not by the author.

Do not rank the licenses inside a posture by efficiency. The choice is determined, not traded off: the artifact's trigger event and step 1's constraint list decide it, and a ratio placed over that would be false precision dressed as rigour. The defaults below are matches, not rungs.

Fast defaults, for when the constraints leave the field open:

- Small program or library where adoption matters most → MIT, moving to Apache-2.0 once patents, corporate contributors or a foundation enter the picture. This split is this skill's own default - the FSF's recommendation for small programs is Apache-2.0; this skill softens it because MIT is shorter and more widely recognized.
- Library facing an entrenched non-copyleft competitor → LGPL (the FSF's recommendation) or MPL-2.0 (this skill's file-level alternative).
- Distributed application where improvements should come back → GPL-3.0 (FSF).
- Hosted/server software where the SaaS loophole is the whole concern → AGPL-3.0 (FSF).

AGPL's cost has a named, checkable example: Google's published policy states that "code licensed under the GNU Affero General Public License (AGPL) MUST NOT be used at Google", down to installing an AGPL program on a company laptop. No aggregate figure for how many enterprises run the same ban exists - name policies, never a percentage - and ask whether the accounts this project needs are behind one.

The full table - families, per-license traits, patent grants, compatibility directions, and the published FSF and Blue Oak heuristics - is in [references/license-families.md](./references/license-families.md).

## Step 4 - Decide what you ask of contributors

Karl Fogel's ladder from _Producing Open Source Software_ has four rungs: nothing beyond inbound=outbound, a DCO sign-off, a CLA (individual plus corporate), and copyright assignment. His own verdicts on them:

- A DCO is "probably the minimum amount of CLA a free software project should adopt".
- CLAs "probably offer the best tradeoff between safety and convenience" when the project genuinely needs those rights.
- He does not recommend assignment for new projects.

Rank the rungs by what each buys per unit of friction imposed, not by ascending burden, since the cheapest rung and the right one are rarely the same:

- efficiency: `DCO > nothing > CLA > assignment`
- value: `assignment > CLA > DCO > nothing`
- effort, meaning contributor friction and your own administration: `assignment > CLA > DCO > nothing`
- compliance cost: `assignment > CLA > DCO == nothing`

**Start at the DCO.** A commit trailer plus an automated check costs a contributor one flag and you nothing, and it buys the provenance and audit trail otherwise credited to a CLA. It leads on efficiency even though `nothing` is cheaper, because `nothing` buys nothing beyond what the license already grants. The DCO and `nothing` tie on compliance cost - genuinely equal, since neither creates an agreement to draft, store, or produce on request; every other pairing on that axis separates.

**Move up only for a right the license does not grant you.** Relicensing later, dual licensing, and selling a commercial license of contributed code are the real answers. For patents, check whether the license already carries a grant (Apache-2.0, GPL-3.0 and MPL-2.0 do; MIT and BSD do not) before adding an agreement for that reason alone. Delete assignment from the menu for a new project, saying you did and why - Fogel's own recommendation - and restore it only when a foundation the project is joining requires it.

The efficiency order starves the CLA. It is the only rung that preserves relicensing optionality, and it imposes the most friction of anything a reader will realistically adopt, so it loses on ratio every time. Promote it anyway when:

- Step 2 chose commercial optionality.
- A foundation donation or dual-licensing plan is foreseeable.
- A corporate contributor's employer requires one.

State the consequence in the same breath: a CLA on a project with no commercial plan reads as a company reserving the right to change the deal, and it costs drive-by contributions at the signature wall.

The order is a default, not a law. Re-rank it against the project's situation: an existing CLA bot and a legal team make the CLA far cheaper than this assumes, while a project whose contributors are drive-by fixers pays that friction on every single change. Mechanics, enforcement and the wording to put in the contributing guide are in [references/contribution-policy.md](./references/contribution-policy.md).

## Step 5 - Attach the business model, or say there is none

Reach for a licensing lever only when a real business model needs one. Every restriction has a contributor cost, so "no lever needed" is a finding to report, not a failure.

The monetization axis is go-to-market motion, not buyer type:

- **Sales-led B2B** - dual licensing, open core and source-available terms work on organizations that run legal and procurement review. Order them by revenue reached per unit of trust spent - efficiency: `dual licensing > open core > source-available relicense`:
  - Dual licensing charges the buyer who needs different terms while leaving the open artifact intact.
  - Open core moves a boundary that contributors then argue about.
  - A relicense to source-available spends the most trust for the same revenue and is the least reversible of the three, having produced a fork every documented time.

  Name the specific competitor being defended against - usually a hyperscaler reselling the software as a managed service. If no such competitor is plausible, the restriction buys nothing and costs adoption.

- **Product-led (PLG) B2B** - the path is individual developer adoption → company contract without procurement. The license must support this handoff: permissive or weak copyleft lets the developer adopt freely, while the company later pays for support, SLA, or proprietary modules. Source-available terms that block the individual developer's free adoption break the PLG funnel. Dual licensing and open core still work but the evaluation metric shifts from "procurement review survival" to "developer adoption friction".

- **B2C / individual-facing** - no license term converts an individual. The license is a trust and distribution decision; money, if any, comes from sponsorship or hosted convenience. Recommend the permissive or copyleft choice that maximizes trust and leave the terms alone.

If source-available or delayed-open-source terms are genuinely on the table, work through [references/business-model-licensing.md](./references/business-model-licensing.md): dual licensing, open core, BUSL and FSL parameters, the Fair Source definition, and what each documented license change actually produced.

Enforce the vocabulary throughout: source-available is not open source. The OSI board's own wording for the failure is worth repeating to a user who wants both labels - "the hallmark of a fauxpen source license is that those who made the switch claim that their product continues to remain 'open' under the new license, but the new license actually has taken away user rights". Calling it open source costs the audience the project was built for, and it fails the procurement filters that check OSI approval directly.

## Step 6 - If this is a change, plan it as a change

Relicensing an existing project is a different job from picking a license, with one hard rule: it needs the consent of every copyright holder whose code is still present, unless a contributor agreement already granted that right. Published releases stay under their old license forever, so anyone may fork from the last commit - treat the fork as the predictable response, not the worst case (Elastic, Redis and HashiCorp each got one; the documented outcomes are in the reference below).

Produce a change plan, not just a new license:

- Whose consent is needed and how it will be gathered.
- What happens to code from unreachable contributors.
- The version boundary where the change takes effect.
- What stays on the old terms.
- An announcement that states all of it without euphemism.

The playbook, the announcement template and the documented outcomes are in [references/business-model-licensing.md](./references/business-model-licensing.md).

## Step 7 - Ship the artifacts

A decision that produces no files has not happened. Deliver these in the order below - it is an efficiency order, each item costing minutes and ranked by what its absence breaks - and validate against a real license detector where the harness allows it:

1. `LICENSE` at the repository root, unmodified license text, nothing appended - no file means the project is legally unlicensed, and a modified file defeats automatic license detection.
2. For a mixed repository, the per-directory boundary written down - a single root LICENSE silently claims documentation, assets and examples too.
3. The contribution policy in the contributing guide, with the exact sign-off or signature step spelled out, and its automated check - a policy enforced by memory is not enforced.
4. Package/registry metadata license fields, and container image labels where they apply - registries display and filter on them.
5. `SPDX-License-Identifier` headers and collective copyright notices ("Copyright The <Project> Authors") rather than an enumerated contributor list.
6. A `NOTICE` file when the license requires attribution propagation, and preserved third-party notices.

## Invocation examples

Not every request needs all seven steps. Match the request to the entry point, and say which steps you are skipping and why.

| The user says                                                             | Where you start                                      | What you hand back                                                                                                                     |
| ------------------------------------------------------------------------- | ---------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| "I'm open-sourcing an internal Go library next week - MIT or Apache-2.0?" | Step 1, then straight to step 3                      | Constraint list, the two-option comparison decided on patents and corporate contributors, the LICENSE/SPDX/metadata artifact set       |
| "Should we require a CLA?"                                                | Step 4, after one question about commercial plans    | The rung, the specific right that justifies it (or the finding that none does), the contributing-guide wording and the automated check |
| "We want to stop AWS reselling our server"                                | Step 2 - the posture is the real question            | Two or three postures with what each forecloses, the named-competitor test, and the fork precedents if source-available survives it    |
| "Move us from Apache-2.0 to BUSL for the 3.0 release"                     | Step 6, with step 1 run first on contributor consent | Consent map, version boundary, what stays permissive, the announcement draft, the fork you should expect                               |
| "Which license does our dependency graph allow?"                          | Step 1 only                                          | Enumerated inbound licenses and the eliminated outbound options with a reason each - constraints only, no recommendation               |
| "Is our repository's licensing set up correctly?"                         | Step 7                                               | Artifact audit against the checklist, each gap with the exact file and location to fix                                                 |

Run the full sequence when the answer to "what is this project for?" is open, or when the request is a license change on a project with outside contributors - those are the two cases where a shortcut produces a decision that gets reversed in public.

## Output shape

Produce a license decision record the project can commit alongside the code:

```markdown
# Licensing decision - <project>

## Artifact & trigger what ships, and what event the license's obligation attaches to

## Constraints dependency licenses, employer/foundation rules, eliminated options

## Posture the bundle chosen in step 2, and what it forecloses

## Outbound license the license, why it beat the alternatives, who this excludes

## Contribution policy nothing / DCO / CLA, the reason, the enforcement mechanism

## Business model the lever used or explicitly not used, and the competitor it addresses

## Artifacts files to add or change, with their exact locations

## Revisit what would justify reopening this (a business model, a foundation, a fork)
```

Present the record section by section and get agreement before continuing. A wrong constraint at the top invalidates every line under it, and it is far cheaper to catch at heading two than at heading eight. A full worked record, with a weak version of the same decision beside the strong one, is in [references/decision-record-example.md](./references/decision-record-example.md).

## Pass threshold

These six checks are this skill's own bar, not a published standard. Say so when you report against them, and swap in the adopting organization's real criteria whenever you know them (a "Blue Oak Bronze or better" policy, an OSI-approved-only allowlist). Iterate until every check passes, then report the result explicitly:

- Every shipped dependency's license is enumerated, and each combination's direction is verified - 100% coverage, no "probably permissive".
- The outbound license is a recognized, unmodified license, and it is labelled correctly: OSI-approved, or source-available and never called open source.
- The LICENSE file is detected as the intended license by an automated detector (or by inspection where none is available).
- The contribution policy has an automated check on every incoming change; a policy enforced by memory is not enforced.
- Every claim in the record is traceable to the license text, a public statement by its steward, or a documented case - no assertion about what a court would do.
- Each eliminated option carries a written reason, so nobody re-litigates it next quarter.

## Common failure modes

- **The license-picker quiz.** Two questions and an answer of "MIT", with no dependency audit. The constraint step is what makes the recommendation survivable.
- **Choosing a license the dependencies forbid.** Discovered at the first release, by a user, in public.
- **AGPL as a magic shield.** It obliges a network operator to publish source; it does not stop a well-resourced competitor who complies, and it disqualifies the project inside enterprises with a written ban (Google's is the checkable example).
- **A CLA with no plan that needs one.** Pure friction, plus the reputational cost of looking like a rights grab.
- **Calling source-available "open source".** The claim is checkable in seconds, the correction arrives in public, and it fails procurement allowlists that filter on OSI approval.
- **Forgetting the trademark.** The license governs the code; the name and logo are what stop a fork from calling itself your product.
  - As William Morgan put it during the 2025 Synadia/NATS dispute, an Apache-2.0 license lets anyone ship a relicensed version, but "the one thing you can't do is call that relicensed thing the original project name".
  - Free distribution is no shelter: _Planetary Motion v. Techsplosion_ (261 F.3d 1188) established that giving software away over the internet can still be use in commerce.
  - Treat the name as a separate asset with its own policy, cleared roughly two months before any public mention (a trademark lawyer's schedule may override this timeline).
  - Expect a foundation to require transferring it (the CNCF does).
- **Deciding late.** Every published release stays under its original terms forever, so a licensing lever pulled after adoption arrives is mostly symbolic.
- **Silent scope creep in a mixed repository.** Docs, examples and assets inherit the root LICENSE unless the boundary is written down.

## References

- [references/license-families.md](./references/license-families.md) - families, per-license traits, compatibility directions, and the published selection heuristics.
- [references/contribution-policy.md](./references/contribution-policy.md) - DCO vs CLA vs assignment: what each grants, enforcement, and contributing-guide wording.
- [references/business-model-licensing.md](./references/business-model-licensing.md) - dual licensing, open core, source-available and delayed-open-source terms, plus the relicensing playbook and documented outcomes.
- [references/decision-record-example.md](./references/decision-record-example.md) - a full worked decision record, weak version beside strong version.
- [references/published-findings.md](./references/published-findings.md) - which claims are sourced and where from, which numbers are this skill's own defaults, and what it refuses to assert.
- samber/developer-relations-skills@oss-governance - decision rights and succession once the license is set.
- samber/developer-relations-skills@oss-contributor-onboarding - the contributing guide the policy lands in.
- samber/developer-relations-skills@devtools-business-model - the model the licensing lever serves.
- samber/developer-relations-skills@oss-launch - trademark clearance timing and for announcing a licensing change during a launch window.
- samber/developer-relations-skills@tech-press-relations - the license-change press playbook and the hostile-coverage precedent to plan against.
- samber/developer-relations-skills@oss-distribution-strategy - the channels that will read the license metadata you ship.
