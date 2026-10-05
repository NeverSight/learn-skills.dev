---
name: translating-app-stores
description: Use when localizing App Store and Play Store product listings for store metadata, screenshots, keywords, market adaptation, and listing constraints.
---

# Translating App Stores

## Overview

Define a separate, verifiable listing contract for each store and market. Preserve product facts and asset identity while sending listing prose to translation and search terms to market research.

## Capabilities

- `surface:app-store`
- `surface:play-store`
- `aso`
- `store-metadata`

## Input Inspection

Build an inventory per target market and per App Store or Play Store listing:

- store, storefront/market, source and target locale, release/version, and current product availability
- title or app name, subtitle or short description, description, promotional/update fields, and keyword fields actually supported by that store
- screenshots, preview media, overlay copy, depicted UI strings, device class, ordering, and asset IDs
- approved product name, feature/fact sheet, claims and substantiation, legal text, offers, pricing, support, and privacy disclosures
- current localized build, exact UI terminology, regional feature/bank/service availability, approved glossary, and brand voice

Keep Apple and Google field maps separate. Do not infer that equivalent-looking fields share limits, indexing behavior, policies, or asset requirements.

## Translation Surface

Send store-supported user-facing prose—such as subtitle, description, promotional text, release notes, and screenshot overlays—to `translating-core` with field purpose, target market, approved facts, claims, and verified length constraint. Send UI labels through the product's software/mobile localization owners and reuse the exact approved strings shown in the shipping build.

This skill does not generate listing copy, language mechanics, or target-market keywords.

## Non-Translatable Elements

Preserve exactly unless an approved owner supplies a replacement:

- protected product and brand names, legal entity names, product IDs, bundle/package identifiers, URLs, support contacts, and asset IDs
- numbers, feature scope, compatibility, availability, pricing, rankings, awards, security statements, and other factual claims
- screenshot/UI relationships, device frames, badges, legal marks, and source asset provenance
- store field identity and structured submission keys

Never improve a listing by inventing superiority, coverage, outcomes, endorsements, or local availability. A translated screenshot overlay does not authorize showing untranslated or unavailable product UI.

## Store and Market Constraints

- Validate each field against the current target store and storefront rules before accepting it; measure length using the store's documented method rather than an assumed character count.
- Treat keyword research as market discovery, not translation. Research how users in that store and market search for the approved product need, then evaluate relevance, intent, competition, policy, and fit. Do not upload literal translations or unsupported volume estimates.
- Preserve conversion intent only within approved facts. Route semantic adaptation to core and linguistic treatment to the installed language specialist.
- Make screenshots match the localized release candidate: depicted features, navigation, labels, prices, dates, currencies, accounts, and availability must be real for that market.
- Keep overlay copy legible within every required asset size and safe area; preserve asset IDs and ordering unless the approved listing plan changes them.
- Maintain store-specific parity between metadata, screenshots, preview media, in-app experience, privacy/support information, and regional availability.

## Store-Review Rejections

When a store rejects submitted metadata or assets, preserve an immutable rejection packet: store/storefront, locale, submission and version IDs, review date, exact reviewer feedback, exact rejected field or asset, rejected content, attachments, and fields explicitly accepted or unaffected. Never delete or paraphrase away the evidence.

Classify the rejection by its actual cause—such as unsupported fact/claim, current policy, field/format constraint, metadata-to-build mismatch, asset defect, or unclear reviewer interpretation—and route it to the owner of that cause. Research current store rules only when the classification or correction hinges on a current policy, limit, or platform detail. Do not automatically reopen keyword, competitor, market, or whole-listing research.

Revise the smallest rejected field or asset and only its necessary dependencies. Preserve accepted content, route replacement meaning to `translating-core` and linguistic form to the installed language specialist, and obtain fact/claim or platform approval from its owner. Revalidate the corrected field against the rejection, approved facts, applicable current rule when needed, and the final submission diff; then return a resubmission-ready or appeal-ready evidence packet.

Do not upload assets or metadata, contact the store, resubmit, or appeal unless the user explicitly authorizes that external action. When authorized, perform only the scoped action represented by the approved packet and preserve the evidence trail.

## Targeted Research

Research only current facts needed for the listing:

- App Store or Play Store field support, length calculation, asset specifications, indexing behavior, and submission policy
- target-market search language, query intent, competitors, seasonality, and store-specific keyword evidence
- product availability, supported institutions/services, pricing, regulation, and disclosure requirements in the named market

Prefer official store documentation for platform rules and dated, market-specific evidence for keyword research. Record source and observation date. If current evidence is unavailable, mark the constraint or keyword decision unresolved; do not substitute memory or source-language keywords.

## Authority and Conflict Boundary

Follow explicit user requirements, approved product facts/configuration, and core semantic fidelity before growth preferences. Brand owns protected names; product and operations own features and regional availability; legal/compliance owns claims and disclosures; store operations owns submission mapping; growth/ASO owns evidence-backed recommendations but cannot alter facts.

This skill owns listing field classification, store/market constraints, protected facts/assets, and listing QA. `translating-core` owns meaning and target copy; installed language specialists own linguistic mechanics; product surface owners own in-app UI; `reviewing-translations` owns final review. If a limit conflicts with an approved name, term, or fact, report the field and conflict instead of abbreviating or rewriting it without approval.

## QA Handoff

Pass source and target listings, per-store field map, locale/market, current rule citations, approved facts/claims, keyword evidence, release-build identifier, screenshot manifest, UI string source, any rejection packet and classification, and these checks to `reviewing-translations`:

- product names, numbers, claims, availability, contacts, links, asset IDs, and required disclosures preserve approved truth
- title, subtitle/short description, description, promotional/update fields, and screenshots satisfy their verified store-specific constraints
- keyword choices have target-store market evidence and are not literal translations presented as research
- every screenshot matches the localized release build, contains approved UI strings, and avoids accidental mixed-language content
- overlay and metadata wording preserve meaning, brand voice, conversion intent, and accessibility/readability without adding a claim
- App Store and Play Store packages were validated independently for field, asset, policy, and submission parity
- a rejected resubmission preserves the exact review evidence, changes only the rejected field or necessary dependencies, resolves the classified cause, and retains accepted fields unchanged

Block submission for an invented or unsubstantiated claim, protected-name change, inaccurate regional availability, unverified platform constraint, unsupported keyword assertion, mismatched screenshot/UI, required-field failure, or accidental mixed-language customer content. Route the exact affected field or asset to its responsible installed skill.
