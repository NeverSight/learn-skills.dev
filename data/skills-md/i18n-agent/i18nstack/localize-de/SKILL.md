---
name: localize-de
description: Use when translating or localizing UI strings, marketing copy, documentation, or any source text into German (de). Enforces Sie/du consistency, der/die/das gender + 4-case agreement, V2 word order (verb-final in subordinate clauses), German quotation marks „...", compound-word formation, and replaces anglicisms with native German verbs.
---

# German Translation Rules (de / Deutsch)

Distilled from the production translation prompts. Follow these rules verbatim — they are model-agnostic and produce consistent native-quality German output.

## Mindset

> Du bist ein äußerst anspruchsvoller deutscher Muttersprachler, der unnatürliche Formulierungen hasst.

You are a demanding German native speaker who rejects literal English calques and awkward phrasing. Preserve the original meaning, but restructure for natural German. Occasional well-established English terms (API, Cloud, Token) are acceptable.

## Variant Selection (run FIRST)

The rules in this skill are for **Standard German (de / de-DE — Germany)** and apply unchanged to most B2B/software contexts in DE/AT/CH. Austrian and Swiss German diverge mainly in spelling, vocabulary, currency, and formatting — not in core grammar.

**Default behaviour:** assume `de-DE` unless the source text or user mentions Austria, Switzerland, AT, CH, ÖS, or shows region-specific cues (CHF currency, `Jänner`, `ss` instead of `ß`).

**If the user explicitly mentions Austria or Switzerland**, call `AskUserQuestion` before translating:

- Question: `Which German variant should I target?`
- Header: `DE variant`
- Options:
  1. **Standard German (de-DE)** — Germany. Uses `ß`, EUR, `Januar/Februar`. (Recommended default)
  2. **Austrian German (de-AT)** — same `ß` and EUR as DE, but month names and some vocabulary differ.
  3. **Swiss German (de-CH)** — never uses `ß` (always `ss`); currency CHF (format `CHF 99.95` with period decimal); some vocabulary diverges.

**If the user picks de-AT**, apply these deltas on top of the standard rules:

- **Months:** `Jänner` (not `Januar`) — required in formal/official Austrian text. `Feber` is older and rarely used; `Februar` is fine.
- **Greetings:** `Grüß Gott` (formal/business), `Servus` (informal). `Guten Tag` and `Hallo` are acceptable but feel less native.
- **Vocabulary deltas** (Austrian standard, fine in software UI):
  - `heuer` (this year), instead of `dieses Jahr` in marketing copy
  - `Jus` (juice, but also "law" in legal — context-dependent), DE uses `Saft`
  - `Sackerl` (bag), `Sackerl` or `Tasche` for shopping bags; DE uses `Tüte`
  - `Stiege` (stairs), DE prefers `Treppe`
- **Informal/food vocab** (use ONLY if matching a casual register): `Erdäpfel` (potatoes), `Marille` (apricot), `Paradeiser` (tomatoes), `Topfen` (quark), `Obers` (cream). For neutral software UI, the standard DE terms (`Kartoffeln`, `Aprikose`, `Tomaten`, `Quark`, `Sahne`) are safer.
- **Spelling:** uses `ß` like Germany (NOT `ss` like Switzerland).
- Currency: EUR, formatted `99,99 €` (same as DE).
- Numbers: `1.234,56` (period thousands, comma decimal — same as DE).
- Punctuation, quotation, comma rules: unchanged from DE.

**If the user picks de-CH**, apply these deltas:

- **Never use `ß`** — replace every `ß` with `ss`. Examples: `Straße` → `Strasse`, `groß` → `gross`, `weiß` → `weiss`, `heißt` → `heisst`, `Fußball` → `Fussball`, `süß` → `süss`. (This applies even in formal/official text — `ß` does not exist in Swiss orthography.)
- **Swiss number format:** `1'000.50` (apostrophe as thousands separator, **period** as decimal). Different from DE/AT which use `1.000,50`. Apply this for ALL numbers in CH context, not only currency.
- **Currency:** `CHF 99.95` (preferred for software) or `Fr. 99.95`. Period decimal, no comma. If both EUR and CHF appear, format EUR with German rules (`99,95 €`) and CHF with Swiss rules (`CHF 99.95`).
- **Quotation marks:** Swiss German commonly uses « ... » (guillemets, no inside spaces — unlike France) alongside the German „..." style. Either is acceptable; be consistent within a file.
- **Vocabulary deltas** (use Swiss form in CH context):
  - `Velo` (bicycle), not `Fahrrad`
  - `parkieren` (to park), not `parken`
  - `Natel` (mobile phone, older Swiss-German term), accepted but `Handy` / `Mobiltelefon` are also common
  - `Trottoir` (sidewalk), not `Bürgersteig`
  - `Estrich` (attic), not `Dachboden`
  - `grillieren` (to grill), not `grillen`
  - `Spital` (hospital), not `Krankenhaus` in informal CH
- **Date format:** `15.01.2024` (DD.MM.YYYY — same as DE) or ISO `2024-01-15` is increasingly common in Swiss software. Time: same `14:30` 24-hour.
- Everything else — three genders, four cases, V2 / verb-final, Sie/du, compound formation, separable verbs, comma rules — applies unchanged from standard de-DE.

If the user picks de-DE (or didn't mention AT/CH), skip the deltas and use the full skill below as-is.

## Pre-Translation Setup

Lock in before translating:

1. **Formality (Sie vs du)** — Default to **Sie** (formal, capitalized: Sie/Ihr/Ihnen) for B2B and most software. Use **du** only if explicitly consumer-casual. NEVER mix.
2. **Three genders** — der (masc), die (fem), das (neut). Adjectives + articles must agree with gender, number, AND case.
3. **Four cases** — Nominative, Accusative, Dative, Genitive. Selection depends on the verb/preposition.
4. **V2 word order** in main clauses, **verb-final** in subordinate clauses (dass, weil, wenn, obwohl, nachdem).
5. **Placeholders** — Preserve `{variables}` and ICU plural syntax exactly.

## Register Auto-Detection (run after Pre-Translation Setup, before translating)

If the user has NOT explicitly specified Sie or du, infer from source text register. Match output to source — formal source → Sie; informal source → du.

### Formal source signals → output Sie / Ihr / Ihnen (capitalized)
- Hedging / polite modals: "please", "kindly", "we recommend", "could you", "would you mind"
- Passive / impersonal constructions: "users are advised", "it is recommended", "applicants must"
- No contractions: "do not", "cannot", "we will", "it is"
- Domain vocabulary: legal, financial, healthcare, regulatory, enterprise B2B, government, insurance, automotive
- Third-person / distance: "the user must", "customers should", "members can access"
- Long sentences, subordinate clauses, formal connectors
- Brand voice: bank, insurance, government, B2B SaaS, healthcare, legal tech, premium retail
- No exclamations or emojis

### Informal source signals → output du / dein / dir (lowercase)
- Contractions: "don't", "you'll", "it's", "we're", "I'd"
- Casual greetings: "hey", "hi there", "yo", "what's up", "hi 👋"
- Second-person directness, exclamations, emoji (🎉 😎 🚀 ✨)
- Slang: "cool", "awesome", "no worries", "kinda"
- Consumer-app voice: gaming, social, lifestyle, dating, fitness, kids, casual e-commerce, food delivery
- Sentence fragments and conversational filler

### Mixed / ambiguous source → default to Sie
Sie reads slightly stiff but never offensive; du can read as disrespectful in the wrong context. When in doubt, stay formal — most German B2B and many consumer brands still use Sie.

### Explicit user override
If the user says "use du" / "use Sie" / "formal" / "casual", their instruction overrides auto-detection.

### Worked examples

| Source | Detected | German output |
|----------------|----------|---------------|
| "Please review the terms of service before proceeding." | formal | Bitte lesen Sie die Nutzungsbedingungen, bevor Sie fortfahren. |
| "Hey! Tap here to get started — it's super quick 🚀" | informal | Hey! Tippe hier, um loszulegen — geht super schnell 🚀 |
| "Submit your application by the deadline." | formal | Reichen Sie Ihre Bewerbung vor Ablauf der Frist ein. |
| "Don't forget to save your work!" | informal | Vergiss nicht, deine Arbeit zu speichern! |

After detection: keep the chosen form consistent. NEVER mix pronouns, possessives, OR imperatives.

## Critical Accuracy Rules

### 1. Gender of common IT nouns (memorize)

| Masculine (der) | Feminine (die) | Neuter (das) |
|-----------------|----------------|--------------|
| der Server | die Datei | das System |
| der Browser | die Plattform | das Problem |
| der Link | die E-Mail | das Konto |
| der Service | die App | das Netzwerk |
| der Ordner | die Seite | das Passwort |
| der Benutzer | die URL | das Feld |

Common errors: `die Problem` → `das Problem`. `der System` → `das System`. `das Plattform` → `die Plattform`. `die Service` → `der Service`. `der E-Mail` → `die E-Mail`.

### 2. Article declension by case

| Case | Masc. | Fem. | Neut. | Plural |
|------|-------|------|-------|--------|
| Nom. | der | die | das | die |
| Acc. | den | die | das | die |
| Dat. | dem | der | dem | den |
| Gen. | des | der | des | der |

### 3. Case after prepositions

| Case | Prepositions |
|------|--------------|
| Accusative | durch, für, gegen, ohne, um |
| Dative | aus, bei, mit, nach, seit, von, zu |
| Genitive (formal) | wegen, trotz, während, statt, aufgrund, anstatt |
| **Two-way** (in, an, auf, über, unter, vor, hinter, neben, zwischen) | **Motion → Acc**; **Location → Dat** |

Examples:
- `für der Benutzer` → `für den Benutzer` (acc)
- `mit das System` → `mit dem System` (dat)
- `in den Ordner` (motion: putting INTO) vs `im Ordner` (location: inside)
- `wegen dem Wetter` → `wegen des Wetters` (formal genitive)

### 4. Article contractions (mandatory)

| Combine | → |
|---------|---|
| an + dem | am |
| bei + dem | beim |
| in + dem | im |
| von + dem | vom |
| zu + dem | zum |
| zu + der | zur |

Use them. `in dem System` → `im System`.

### 5. Adjective declension — strong/weak/mixed

| Context | Rule |
|---------|------|
| **Strong** (no article) | Adjective carries full case ending: `guter Wein`, `gute Milch`, `gutes Bier` |
| **Weak** (after der/die/das) | -e or -en: `der gute Wein`, `den guten Wein` |
| **Mixed** (after ein/kein/possessive) | `ein guter Wein`, `einen guten Wein` |

Common errors: `den neue Benutzer` → `den neuen Benutzer` (weak: -en). `die internationales Dienste` → `die internationalen Dienste` (plural: -en).

### 6. V2 word order in main clauses

The conjugated verb is the **second element** in a German main clause.

| Wrong | Correct |
|-------|---------|
| Der Benutzer die Datei speichert | Der Benutzer **speichert** die Datei |
| Heute der Benutzer speichert | Heute **speichert** der Benutzer |

### 7. Verb-final in subordinate clauses

After **dass, weil, wenn, obwohl, nachdem, ob, damit**: conjugated verb goes to the END.

| Wrong | Correct |
|-------|---------|
| ...weil der Benutzer speichert die Datei | ...weil der Benutzer die Datei **speichert** |
| ...dass das System hat geladen | ...dass das System **geladen hat** |

### 8. Separable verbs

In main clauses, the prefix moves to the END of the clause. In subordinate clauses, the verb reunites.

| Context | Form |
|---------|------|
| Main | `Ich lade die Datei **herunter**.` |
| Subordinate | `...weil ich die Datei **herunterlade**.` |

### 9. Compound words — one word, no hyphen

German loves compounds. Gender follows the LAST noun.

| Wrong | Correct |
|-------|---------|
| Daten Bank | **Datenbank** (die) |
| Benutzer-Oberfläche | **Benutzeroberfläche** (die) |
| Arbeits Platz | **Arbeitsplatz** (linking -s-) |

### 10. FOR vs PER — never confuse

| English | Wrong | Correct |
|---------|-------|---------|
| for 5 languages (total) | pro Sprache | **für 5 Sprachen** |
| per language (rate) | für Sprache | **pro Sprache / je Sprache** |

### 11. Domain terminology — use IT terms

| Source | Wrong | Correct |
|--------|-------|---------|
| architecture | Architektur (Baukunst) | **Architektur (Softwarearchitektur)** |
| pipeline (CI/CD) | Rohrleitung | **Pipeline** |
| source of truth | Quelle der Wahrheit | **maßgebliche Datenquelle / Single Source of Truth** |
| build (software) | Bau / Konstruktion | **erstellen / entwickeln** |
| deploy | entfalten | **bereitstellen / ausrollen** |
| support (feature) | supportieren | **unterstützen / kompatibel mit** |

## UI Conventions

### Buttons — infinitive form

| Wrong | Correct |
|-------|---------|
| Speichert | **Speichern** |
| Bricht ab | **Abbrechen** |
| Löscht | **Löschen** |

### Status messages

| State | Form | Example |
|-------|------|---------|
| Ongoing | Passive: `Wird X...` (impersonal, never "Ich...") | `Wird gespeichert...`, `Lädt...` |
| Completed | Past participle | `Gespeichert`, `Erfolgreich gespeichert`, `Heruntergeladen` |
| Failed | `Fehler beim X` or `X fehlgeschlagen` | `Fehler beim Speichern`, `Speichern fehlgeschlagen` |

Wrong: `Ich speichere...` (first-person UI), `Speichern hat versagt` (calque) → use the patterns above.

### Completion / success

| Wrong | Correct |
|-------|---------|
| Upload Erfolg | **Upload abgeschlossen / Erfolgreich hochgeladen** |
| Vorgang komplett | **Vorgang abgeschlossen** |
| Zahlung erfolgreich | **Zahlung abgeschlossen / Zahlung bestätigt** |

### Empty state — Kein(e) X (gender-aware)

| Wrong | Correct |
|-------|---------|
| Nicht Ergebnisse | **Keine Ergebnisse** / **Es wurden keine Ergebnisse gefunden** |
| Kein Datei ausgewählt | **Keine Datei ausgewählt** (Datei is feminine) |
| Leer | **Keine Einträge vorhanden** |

### Drag and drop

| English | German |
|---------|--------|
| drag | ziehen |
| drop | ablegen |
| **release** (let go) | **loslassen** — NOT erlauben (= permit) |
| **browse** (file picker) | **auswählen** — NOT durchsuchen for file selection |

Wrong: `Dateien hierhin draggen` → `Dateien hierhin ziehen`. Wrong: `Drop hier` → `Hier ablegen`.

### Validation messages

- Clear structure with connector: `3-50 Zeichen. Erlaubt: Buchstaben, Zahlen, Bindestriche`
- Field required: `Dieses Feld ist erforderlich` (NOT `Feld fehlt` — "missing" calque)
- Invalid: `Ungültiges Format`
- Imperative for instructions (Sie-form): `Geben Sie einen gültigen Wert ein`

### Error messages — what + next step

| Wrong (bare) | Correct (actionable) |
|--------------|----------------------|
| Datei nicht gefunden. | **Datei nicht gefunden. Bitte überprüfen Sie den Pfad.** |

### Other UI patterns

| Wrong | Correct |
|-------|---------|
| Alternativ (bare) | **Alternative Erkennung** (complete noun phrase) |
| Automatisch (bare) | **Automatischer Modus** |
| Erweitert (bare) | **Erweiterte Einstellungen** |
| 25+ Sprachen | **mehr als 25 Sprachen** |
| +{count} mehr | **und {count} weitere** |
| Mehr hinzufügen | **Weitere hinzufügen** (countable items) |

## Sie / du Consistency

NEVER mix. ALL pronouns, possessives, AND imperatives must match.

| Don't mix | Use |
|-----------|-----|
| Sie können deine Einstellungen | Sie können **Ihre** Einstellungen |
| Laden Sie hoch + Durchsuche | Laden Sie hoch + **Durchsuchen Sie** |

Sie-form: `Sie`, `Ihr/Ihre`, `Ihnen` — all capitalized.
du-form: `du`, `dein/deine`, `dir` — lowercase.

Button infinitives (`Speichern`) work with either level, which is why they're preferred.

## Punctuation

| Item | German | Wrong |
|------|--------|-------|
| Decimal | `,` (e.g. `3,14`) | `3.14` |
| Thousands | `.` (e.g. `1.000`) | `1,000` |
| Quotation marks | `„..."` (low-9 open + high-6 close) or `»...«` | `"..."` (English) |
| Currency | `99,99 €` (comma, space, symbol after) | `€99.99` |
| Date | `15.01.2024` (DD.MM.YYYY) | `01/15/2024` |
| Time | `14:30 Uhr` (24-hour) | `2:30 PM` |

## Comma Rules

| Before | Comma? |
|--------|--------|
| und / oder | **No comma** |
| aber / sondern / denn | **Comma required** |
| dass / weil / wenn / obwohl / nachdem (subordinate) | **Comma always** |

| Wrong | Correct |
|-------|---------|
| Speichern, und schließen | Speichern und schließen |
| einfach aber effektiv | einfach**,** aber effektiv |
| sehe dass die Datei | sehe**,** dass die Datei |

## Calques to Avoid

| Wrong (literal) | Natural German |
|-----------------|-----------------|
| macht Sinn | **ergibt Sinn** |
| am Ende des Tages | **letztendlich** |
| nicht wirklich | **eigentlich nicht** |
| per Sprache | **pro Sprache** |
| Vorteil nehmen von | **nutzen / profitieren von** |
| basierend auf (in headers) | **auf Basis von / auf Grundlage von** |
| und viel mehr | **und vieles mehr / und noch viel mehr** |
| auf einer täglichen Basis | **täglich / jeden Tag** |
| in Bezug auf (overused) | **hinsichtlich / bezüglich / was ... betrifft** |
| Break a leg | **Hals- und Beinbruch!** |
| Piece of cake | **Ein Kinderspiel** |
| Icing on the cake | **Das Tüpfelchen auf dem i** |
| It's raining cats and dogs | **Es regnet in Strömen / Es schüttet wie aus Eimern** |

## Marketing "Zero X" patterns

German uses **Ohne / Kein(e)**, not **Null / Zero**.

| Wrong | Correct |
|-------|---------|
| Null Ausfallzeit / Zero Downtime | **Ohne Ausfallzeiten / Keine Ausfallzeiten** |
| Null Fehler | **Fehlerfrei** |
| Zero Engagement | **Ohne Verpflichtung** |

## Anglicism Avoidance (prefer native verbs)

| Anglicism | Native German |
|-----------|----------------|
| downloaden | **herunterladen** |
| uploaden | **hochladen** |
| updaten | **aktualisieren** |
| canceln | **abbrechen** |
| deleten | **löschen** |
| einloggen | **anmelden** |
| ausloggen | **abmelden** |
| supportieren (anglicism) | **unterstützen** |

## False Friends (German words ≠ English look-alikes)

| German word | Actual meaning | NOT the English |
|-------------|---------------|------------------|
| aktuell | current | NOT "actual" — use `tatsächlich` |
| bekommen | to receive | NOT "become" — use `werden` |
| **Gift** | **poison** | NOT "gift" — use `Geschenk` |
| eventuell | possibly | NOT "eventually" — use `schließlich` |
| sensibel | sensitive | NOT "sensible" — use `vernünftig` |
| realisieren | to implement | NOT "realize" — use `erkennen` |
| kontrollieren | to check/inspect | NOT "control" — use `steuern / regeln` |

## Structural Calques to Restructure

- **Avoid English noun stacking** — use compounds, genitive, or adjective forms.
  - Wrong: `Projekt Ordner` / `Benutzer Einstellungen`
  - Correct: `Projektordner` (compound), `Ordner des Projekts` (genitive), `projektspezifisch` (adjective)
- **Active voice over English-style passives.**
  - English "es wird gemacht" → German prefers `man macht` or `wir machen`.

## Compound Adjectives

| English | Wrong | Correct |
|---------|-------|---------|
| X-aware | X-bewusst | **mit X-Unterstützung / X-fähig** |
| X-powered/driven/based | X-angetrieben / X-getrieben | **auf X-Basis / mit X / basierend auf X** |

## Compound Descriptive Nouns

Decompose, then rebuild naturally.

- "mom creators" → `Mütter als Content-Creatorinnen` (NOT `Mama-Ersteller`)
- "niche creators" → `Nischen-Creator` or `Creator in Nischenbereichen`
- When 3+ components make the compound awkward, prefer prepositional phrases.

## Spatial Metaphor Prepositions

| English (figurative) | Use | Don't use |
|---------------------|-----|-----------|
| under [category] | unter / bei | (works in German) |
| on top of (in addition to) | zusätzlich zu / neben | oben auf |
| behind the scenes | hinter den Kulissen | (literal) |
| within [timeframe] | innerhalb / in | im Inneren von |

## Temporal Expression — "[YEAR] me" idiom

English "2014 me" / "90s me" / "teenage me" = "myself at that time", NOT "me from X years ago".

| Wrong | Correct |
|-------|---------|
| vor 2014 Jahren (for "2014 me") | **ich im Jahr 2014 / mein 2014er Ich** |
| vor 90er Jahren (for "90s me") | **ich in den 90ern / mein Ich aus den 90ern** |
| teenage-jähriges Ich | **ich als Teenager / mein Teenager-Ich** |

## UI Element Reference in Prose

| Wrong | Correct |
|-------|---------|
| das Namensfeld (for a specific UI label "Name") | `das Feld „Name"` or `das Feld »Name«` |
| der Kontentab (for a specific tab) | `der Tab „Konto"` |
| die Suchleiste | (generic, no quotes needed) |

## Cost / Estimate Ordering

- Pattern A (preferred): `{credits} Credits für {count} Sprachen`
- Pattern B: `{count} Sprachen: insgesamt {credits} Credits`
- Wrong (no connector): `{count} Sprachen {credits} Credits`

## Proper Nouns — short forms in UI

| Wrong | Correct |
|-------|---------|
| Vereinigte Staaten von Amerika | **USA / die USA** |
| Großbritannien und Nordirland | **Großbritannien / UK** |
| Amerikanisches Englisch | **US-Englisch / amerikanisches Englisch** |

## Brand Names

Foreign brands: implied gender (often neuter for platforms) or default masculine for tech brands. Genitive with -s: `Googles API`, `OneSkeys Einstellungen`.

## Cultural Conventions

- Week starts **Monday** (not Sunday).
- Currency symbol comes **after** with a space: `99,99 €`.
- Phone format groups digits naturally; date is DD.MM.YYYY.

## Letter and Email Conventions

- Formal salutations: `Sehr geehrte Damen und Herren,` (if recipient unknown), `Sehr geehrter Herr Müller,` (male, known), `Sehr geehrte Frau Müller,` (female, known).
- Informal salutations: `Hallo Anna,` `Hi Max,` `Liebe Anna,` (warmer informal).
- Formal closings: `Mit freundlichen Grüßen,` `Mit besten Grüßen,` `Hochachtungsvoll,` (very formal).
- Informal closings: `Viele Grüße,` `Liebe Grüße,` `LG,` `Beste Grüße,` `Bis bald,`.
- After salutation: lowercase continuation (`Sehr geehrte Frau Müller,\n\nvielen Dank für Ihre Anfrage...`).

## Negation: nicht vs kein

- `nicht` negates verbs, adjectives, adverbs, and specific noun phrases: `Ich verstehe das nicht.` / `Das ist nicht möglich.` / `Klicken Sie hier nicht.`
- `kein` negates nouns with an indefinite or no article: `Kein Problem.` / `Keine Ergebnisse.` / `Ich habe keine Zeit.`
- `kein` declines like `ein`: kein/keine/keinen/keiner/keinem/keines, by gender/case.
- Wrong: `Ich habe nicht Zeit` → Correct: `Ich habe keine Zeit`.
- Wrong: `Ich habe kein verstanden` → Correct: `Ich habe nicht verstanden`.
- UI empty state pattern: `Keine X gefunden` not `Nicht X gefunden`.

## Imperative vs Sie-form for Instructions

- Instructions in user manuals / help docs: use Sie-imperative — `Klicken Sie hier`, `Geben Sie Ihren Namen ein`.
- Step-by-step recipes / quick lists: infinitive — `1. Anmelden 2. Datei auswählen 3. Hochladen`.
- Inline help bubbles, tooltips: infinitive is shorter and neutral — `Datei auswählen` works in both Sie and du contexts.
- Error message imperatives: `Bitte überprüfen Sie den Pfad.` (Sie) / `Bitte überprüfe den Pfad.` (du).

## GDPR / Consent Standard Phrasing

- Cookie banner: `Wir verwenden Cookies, um Ihnen das beste Erlebnis zu bieten.` (formal) / `Wir verwenden Cookies, damit du die beste Erfahrung hast.` (informal).
- Accept / Reject buttons: `Alle akzeptieren` / `Alle ablehnen` / `Auswahl bestätigen` / `Einstellungen anpassen`.
- Privacy notice: `Datenschutzerklärung` (privacy policy), `Impressum` (legal notice — required for German websites), `Nutzungsbedingungen` (terms of use), `AGB` = `Allgemeine Geschäftsbedingungen`.
- Common phrasing: `Mit dem Absenden stimmen Sie unseren Datenschutzbestimmungen zu.`

## Phone, Address, Postal Code

- Phone: `+49 30 12345678` international or `030 12345678` national. Mobile prefix `+49 1xx` or `01xx`.
- Postal code: 5 digits, BEFORE the city: `10117 Berlin`, `80331 München`.
- Address format on letters:
  ```
  Anna Müller
  Beispielstraße 12
  10117 Berlin
  ```

## Self-Check Checklist (run before finalizing)

### Accuracy
- [ ] Gender correct (das Problem, die Plattform, der Service, die E-Mail, das System)
- [ ] Case correct after each preposition (für + Acc, mit + Dat, in two-way)
- [ ] Adjective endings agree (strong/weak/mixed × gender × case × number)
- [ ] Article contractions applied (im, am, beim, zum, zur, vom)
- [ ] Compound words written as one word (Datenbank, Benutzeroberfläche)
- [ ] V2 in main clauses; verb-final in subordinate (dass/weil/wenn/obwohl)
- [ ] Separable verb prefixes correct (lade...herunter / ...herunterlade)
- [ ] Sie/du consistent throughout (pronouns, possessives, imperatives)
- [ ] Genitive after wegen/trotz/während/statt/aufgrund
- [ ] German quotation marks `„..."` (not `"..."`)
- [ ] Numbers: `3,14` and `1.000`; currency `99,99 €`
- [ ] No comma before `und`/`oder`; always before `dass`/`weil`/`wenn`/`obwohl`
- [ ] FOR vs PER: `für` (total) vs `pro / je` (rate)
- [ ] All `{variables}` and ICU intact
- [ ] Date DD.MM.YYYY; time 14:30 Uhr
- [ ] Domain terminology uses IT meaning (Softwarearchitektur, CI/CD-Pipeline, maßgebliche Datenquelle)

### Naturalness
- [ ] UI labels are complete noun phrases (Alternative Erkennung, NOT Alternativ)
- [ ] Buttons in infinitive form
- [ ] Status ongoing: `Wird X...` — NEVER `Ich X...`
- [ ] Completion in past participle (Gespeichert, Heruntergeladen)
- [ ] Failure: `Fehler beim X` or `X fehlgeschlagen` — NOT `hat versagt`
- [ ] Empty state: `Keine X` / `Es wurden keine X gefunden`
- [ ] Drag-drop: ziehen / ablegen / loslassen — NOT draggen/erlauben
- [ ] `ergibt Sinn` (NOT `macht Sinn`)
- [ ] Anglicism avoided (herunterladen, aktualisieren, abbrechen, unterstützen)
- [ ] No false friends (aktuell ≠ actual, bekommen ≠ become, Gift = poison!)
- [ ] Compound adjectives: `auf X-Basis` / `mit X` — NOT `X-angetrieben`
- [ ] Marketing zero: `Ohne X` / `Kein(e) X` — NOT `Null/Zero X`
- [ ] No English noun stacking (Projektordner, not "Projekt Ordner")
- [ ] Active voice / impersonal "man" over passive when natural
- [ ] Cost expression has connector: `für N Sprachen` or `: insgesamt N Credits`
- [ ] Proper nouns: short forms (USA, Großbritannien)
- [ ] UI labels in prose use „..." around the label

## Worked Example

**Source:** "Welcome! Please select your file to upload — we support 25+ formats and translate it for 5 languages in {seconds}s. Don't worry, you can cancel at any time."

**Wrong (literal):**
Willkommen! Bitte selecten Sie Ihr file zum uploaden — wir supporten 25+ Formate und übersetzen es pro 5 Sprachen in {seconds}. Mach dir keine Sorgen, du kannst jederzeit canceln.

**Issues:** `selecten/uploaden/canceln/supporten` (anglicisms), `25+` (not natural), `pro 5 Sprachen` (FOR/PER inverted), `{seconds}` (no unit word — German would say `{seconds} Sekunden`), mixed Sie/du, `Mach dir...` (calque).

**Correct (Sie-form):**
Willkommen! Bitte wählen Sie Ihre Datei zum Hochladen aus. Wir unterstützen mehr als 25 Formate und übersetzen die Datei in {seconds} Sekunden für 5 Sprachen. Sie können den Vorgang jederzeit abbrechen.
