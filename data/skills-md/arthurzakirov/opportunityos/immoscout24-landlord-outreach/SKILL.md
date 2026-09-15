---
name: immoscout24-landlord-outreach
description: Compose, verify, and send concise ImmoScout24 landlord contact messages when the user is already logged in on ImmoScout24 and wants to contact one or more rental listings. Use for German rental listing outreach, landlord/broker message templates, profile-based apartment introductions, and troubleshooting ImmoScout24 contact form automation. Do not use for full portal applications with PDF uploads; use a separate apartment application workflow for that.
---

# ImmoScout24 Landlord Outreach

## Purpose

Use this skill for the lightweight outreach stage on ImmoScout24: one listing, one contact form, one concise message.

The goal is not to write a full cover letter. The goal is to make the landlord or broker quickly see that the applicant is solvent, low-risk, complete, and easy to invite.

## Private Context

Load personal facts from the user's private context, not from this reusable skill.

Prefer these files when available:

```text
$PERSONAL_REPOS_DIR/AgentDesk-private-context/shared/personal-profile.yaml
$PERSONAL_REPOS_DIR/AgentDesk-private-context/apartment-search/search-profile.yaml
$PERSONAL_REPOS_DIR/AgentDesk-private-context/apartment-search/document-manifest.yaml
```

If `$PERSONAL_REPOS_DIR` is unset, infer `$HOME/Repos/personal`.

Use only facts that are explicitly present or confirmed by the user. Do not invent salary, contract type, pets, smoking status, move-in date, household size, or document availability.

## Message Strategy

Keep the message short. The ImmoScout24 profile and Bewerbungsmappe carry the detail; the message should only increase conversion.

Include these facts when known:

- Correct personal salutation for the provider: `Sehr geehrte Frau X,` or `Sehr geehrter Herr X,`
- Interest in this 1-room/apartment listing and request for a viewing
- Age
- Marital status if simple and favorable, such as single
- Non-smoker status
- No pets
- One-person household / moving in alone
- Stable employment and employer
- Annual gross salary when the user has approved mentioning it
- Move-in date or flexibility
- ImmoScout24 profile / Bewerbungsmappe availability
- Viewing availability

Do not over-explain why the location is perfect. Landlords usually care more about solvency, completeness, and low hassle than commute motivation.

## German Message Template

Use this template and replace only confirmed fields:

```text
Sehr geehrte Frau [Nachname],

ich interessiere mich sehr fuer Ihre [Wohnungstyp] und wuerde mich ueber eine Besichtigung freuen.

Kurz zu mir: Ich bin [Alter] Jahre alt, [Status], Nichtraucher, ohne Haustiere und arbeite [Vertragsart] als [Jobtitel] bei [Arbeitgeber] in [Arbeitsort] mit einem Jahresbruttogehalt von [Gehalt] EUR. Ich wuerde allein einziehen und koennte [Einzugsdatum/Flexibilitaet] einziehen. Meine Bewerbungsmappe inkl. SCHUFA, Selbstauskunft, Ausweiskopie und Gehaltsnachweisen ist in meinem ImmoScout-Profil hinterlegt.

Ich bin fuer Besichtigungstermine zeitlich flexibel und freue mich ueber Ihre Rueckmeldung.

Mit freundlichen Gruessen
[Name]
```

For male providers, use `Sehr geehrter Herr [Nachname],`.

If the browser automation reliably supports umlauts, use normal German spelling. If text entry is fragile, ASCII German (`fuer`, `wuerde`, `Muenchen`, `Rueckmeldung`, `Gruessen`) is acceptable and safer than corrupt pasted text.

If no provider name is visible, use:

```text
Sehr geehrte Damen und Herren,
```

If document availability is unknown, replace the document sentence with:

```text
Meine Unterlagen kann ich bei Bedarf gerne kurzfristig bereitstellen.
```

## Listing Verification Before Contact

Before sending, inspect the listing page and reject or pause if any hard exclusion appears:

- `Tauschwohnung`
- `Wohnungstausch`
- `WG`
- `WG-Zimmer`
- `nur fuer Studenten`
- `nur fuer Studierende`
- `Azubi`
- `Zwischenmiete`
- `Mindestmietdauer 24 Monate`
- `Kuendigungsverzicht 24 Monate`
- warm rent above the user's hard maximum

Record these visible facts mentally before opening the form:

- Listing ID / Scout-ID
- Title
- Warm rent
- Location
- Provider name
- Whether the provider is private, broker, or company
- Any required documents listed in the expose

## ImmoScout24 Click Path

Use this flow when the user is already logged in:

1. Open the listing expose URL.
2. Find the provider block near the lower part of the page.
3. Read the provider name. Prefer a personal salutation.
4. Click the `Nachricht` button in the provider block. There may be two identical `Nachricht` buttons; the second one near the provider card often opens the contact modal.
5. Confirm the modal title is `Kontaktanfrage`.
6. Confirm `Anbieter:in` shows the expected provider.
7. Inspect the `Nachricht schreiben` textarea.
8. If an old message is prefilled, clear it before typing the new one.
9. Confirm `Anbieter:in darf dein Profil sehen` is checked when the user wants the profile/Bewerbungsmappe visible.
10. Leave optional marketing checkboxes such as `Erhalte Angebote von Umzugsfirmen` unchecked unless the user explicitly wants them.
11. Enter the message.
12. Verify the message contains the correct recipient name and does not contain a previous recipient's name.
13. Confirm with the user before final submission unless the user has already explicitly approved sending this exact message to this exact provider.
14. Click `Abschicken`.
15. Verify the confirmation text, usually `Nachricht gesendet` and `Deine Nachricht ist auf dem Weg zu ...`.

## Browser Automation Rules

Use browser-internal controls. Avoid host OS automation unless the user is manually taking over.

Working approach observed on ImmoScout24:

- Browser-internal click into the textarea works.
- Browser-internal select-all and backspace can clear stale text.
- Browser-internal single-character keypresses can type into the textarea reliably.
- A normal form submit button click works after message verification.

Fragile or unsafe approaches:

- Host OS keystrokes, AppleScript, `System Events`, AutoHotkey, or global paste can target the agent chat instead of the ImmoScout24 textarea.
- Clipboard-based paste may fail when the browser automation environment lacks a virtual clipboard.
- `fill()` or high-level `type()` may internally rely on clipboard and fail with errors like `virtual clipboard is not installed`.
- Direct page evaluation may be read-only or expose textarea objects whose `value` cannot be set.
- Do not click `Abschicken` while the textarea still contains a previous listing's message.

When high-level input fails, fall back to:

1. Browser-internal click in the textarea.
2. Browser-internal `ControlOrMeta+A`.
3. Browser-internal `Backspace`.
4. Test a single browser-internal printable key, such as `A`, and verify it appears in the textarea.
5. Clear the test character.
6. Type the final message with browser-internal keypresses.
7. Verify recipient name, salary, and absence of old recipient names.
8. Submit.

## Stale Message Hazard

ImmoScout24 may preserve the previous contact text across listings. This can cause an application to the next provider to begin with the last provider's salutation and address details.

Always check for:

```text
previous provider name
previous salutation
old listing address
old listing-specific rent or location text
```

Use names relevant to the current session. The principle is: search for any old recipient or old listing-specific text before sending.

## Submission Safety

Sending a message to a landlord, broker, or property manager transmits personal data. Treat it as a real external communication.

Do not submit unless one of these is true:

- The user explicitly confirmed sending this message to this provider on ImmoScout24.
- The user gave a narrow batch instruction that names the listings/providers and approved the common message pattern.

Before submission, state the exact provider and listing ID when possible.

After submission, report:

- Provider contacted
- Listing ID
- Confirmation text
- Whether profile sharing was enabled
- Whether optional marketing checkboxes were left unchecked
