---
name: localize-fr
description: "Use when translating or localizing UI strings, marketing copy, documentation, or any source text into French (fr). Enforces vous/tu consistency, le/la gender + number agreement, French typography (non-breaking spaces before : ; ? !), guillemets « », anglicism avoidance per Toubon Law, and prepositional-chain simplification."
---

# French Translation Rules (fr / français)

Distilled from the production translation prompts. Follow these rules verbatim — they are model-agnostic and produce consistent native-quality French output.

## Mindset

> Tu es un écrivain français natif extrêmement exigeant qui déteste les calques de l'anglais et les formulations maladroites.

You are a demanding French native speaker who rejects literal English calques and Académie-frowned anglicisms. Preserve meaning, but restructure into natural French. Anglicisms are acceptable ONLY when no good French equivalent exists (API, token, cloud) or for brand names.

## Variant Selection (run FIRST)

The rules in this skill are for **Metropolitan French (fr / fr-FR — France, Belgium, Switzerland-romand by default)**. Canadian French (fr-CA / Québec) diverges enough that applying these rules to QC content produces visibly wrong output.

**If the user has not specified the variant**, before translating call `AskUserQuestion` with:

- Question: `Which French variant should I target?`
- Header: `FR variant`
- Options:
  1. **Metropolitan French (fr-FR)** — France/Europe; NBSP before `: ; ? !`; `vous` default; `DD/MM/YYYY`. (Recommended for most software)
  2. **Canadian French (fr-CA / Québec)** — `tu` more common; **no space** before punctuation; ISO `YYYY-MM-DD`; Loi 101 anglicism rules.

**If the user picks fr-FR (or already specified Metropolitan French)**, use the full skill below as-is and ignore the Quebec deltas section.

**If the user picks fr-CA**, apply ALL the deltas in the "Quebec French (fr-CA) Deltas" section near the end of this skill in addition to the Metropolitan rules. The deltas override the Metropolitan rules wherever they conflict (punctuation spacing, dates, terminology, formality default). Everything not contradicted by a delta (gender, plural, agreement, contractions, elisions, subjunctive, prepositional-chain simplification, BANGS adjective order) carries over.

## Pre-Translation Setup

Lock in before translating:

1. **Formality (vous vs tu)** — Default to **vous** (formal) for B2B and most software. Use **tu** only if explicitly consumer-casual. NEVER mix within a file.
2. **Two genders** — le (masc), la (fem). Articles, adjectives, participles all agree in gender + number.
3. **Typography** — Non-breaking space BEFORE `:` `;` `?` `!` and inside guillemets `« »`.
4. **SVO + adjective position** — Most adjectives FOLLOW the noun; BANGS (Beauty, Age, Number, Goodness, Size) precede.
5. **Placeholders** — Preserve `{variables}` and ICU plural syntax exactly.

## Register Auto-Detection (run after Variant Selection + Pre-Translation Setup, before translating)

If the user has NOT specified vous or tu, infer from source text register. Match output to source — formal source → vous; informal source → tu.

### Formal source signals → output vous / votre / vos
- Hedging / polite modals: "please", "kindly", "we recommend", "could you", "would you mind"
- Passive / impersonal: "users are advised", "it is recommended", "applicants must"
- No contractions: "do not", "cannot", "we will"
- Domain vocabulary: legal, financial, healthcare, regulatory, enterprise B2B, government, insurance, luxury
- Third-person / distance: "the user must", "customers should"
- Long sentences, formal connectors ("furthermore", "moreover")
- Brand voice: bank, insurance, government, B2B SaaS, healthcare, legal, luxury retail
- No exclamations or emojis

### Informal source signals → output tu / ton / ta / tes
- Contractions: "don't", "you'll", "it's", "we're"
- Casual greetings: "hey", "hi there", "yo", "hi 👋"
- Second-person directness, exclamations, emoji (🎉 😎 🚀 ✨)
- Slang: "cool", "awesome", "no worries", "kinda"
- Consumer-app voice: gaming, social, lifestyle, dating, fitness, kids, casual e-commerce
- Sentence fragments and conversational filler

### Mixed / ambiguous source → default to vous (fr-FR) or tu (fr-CA consumer)
- fr-FR: default to **vous** when ambiguous. Most French B2B and many consumer brands still use vous.
- fr-CA: default to **tu** for consumer/casual contexts; **vous** for B2B/government/banking.

### Explicit user override
If the user says "use tu" / "use vous" / "formal" / "casual", their instruction wins.

### Worked examples (fr-FR)

| Source | Detected | French output |
|----------------|----------|---------------|
| "Please review the terms of service before proceeding." | formal | Veuillez lire les conditions d'utilisation avant de continuer. |
| "Hey! Tap here to get started — it's super quick 🚀" | informal | Salut ! Appuie ici pour commencer — c'est super rapide 🚀 |
| "Submit your application by the deadline." | formal | Soumettez votre candidature avant la date limite. |
| "Don't forget to save your work!" | informal | N'oublie pas d'enregistrer ton travail ! |

After detection: keep the chosen form consistent. NEVER mix pronouns, possessives, OR imperatives.

## Critical Accuracy Rules

### 1. Gender of common IT nouns (memorize)

| Masculine (le) | Feminine (la) |
|----------------|----------------|
| **le** problème | **la** solution |
| **le** système | **la** erreur (one of the trickiest) |
| **le** fichier | **la** plateforme |
| **le** compte | **la** page |
| **le** dossier | **la** connexion |
| **le** navigateur | **la** sauvegarde |
| **le** PDF | **la** base de données |

**Acronyms inherit gender from the expanded form:**

| Acronym | Expansion | Gender |
|---------|-----------|--------|
| IA | Intelligence Artificielle | **feminine** → l'IA |
| API | Application Programming Interface | **feminine** → l'API |
| PDF | Portable Document Format | **masculine** → le PDF |
| URL | (locator) | feminine in most usage |

Common errors: `une problème` → `un problème`. `le solution` → `la solution`. `un erreur` → `une erreur`. `le IA` → `l'IA` (fem).

### 2. Plural forms

| Pattern | Example |
|---------|---------|
| Regular | `livre → livres` |
| -eau, -au, -eu | `bureau → bureaux` |
| -al | `journal → journaux` |
| -s, -x, -z | no change: `souris, voix, nez` |

Adjectives + participles must agree: `les nouveaux paramètres`, `les solutions personnalisées`.

### 3. Article contractions (mandatory)

| Combine | → |
|---------|---|
| à + le | au |
| à + les | aux |
| de + le | du |
| de + les | des |

`à le système` → `au système`. `de les utilisateurs` → `des utilisateurs`.

### 4. Elision before vowels

`le`, `la`, `de`, `que`, `ne`, `me`, `te`, `se`, `je` drop the vowel before a vowel/h-mute:

| Wrong | Correct |
|-------|---------|
| le utilisateur | **l'utilisateur** |
| de autre | **d'autre** |
| que il | **qu'il** |

### 5. Subject–verb agreement + participle agreement

- Subject and verb agree in person and number.
- Past participle with **être** agrees with the subject. With **avoir**, it agrees with the preceding direct object.

| Wrong | Correct |
|-------|---------|
| Les fichiers a été supprimé | **Les fichiers ont été supprimés** |
| Elle a se connecté | **Elle s'est connectée** (reflexive → être; agrees with subject) |

### 6. Subjunctive mood (required after specific triggers)

After **il faut que**, **il est possible que**, **bien que**, doubt/desire/emotion expressions:

| Wrong | Correct |
|-------|---------|
| Il faut que vous pouvez | **Il faut que vous puissiez** |
| Il est possible que c'est | **Il est possible que ce soit** |

### 7. FOR vs PER — never confuse

| English | Wrong | Correct |
|---------|-------|---------|
| for 5 languages (total) | par langue | **pour 5 langues** |
| per language (rate) | pour langue | **par langue** |

### 8. Domain terminology — use IT meaning

| Source | Wrong | Correct |
|--------|-------|---------|
| architecture | architecture (bâtiment) | **architecture (logicielle)** |
| pipeline (CI/CD) | canalisation | **pipeline** |
| source of truth | source de vérité | **source de référence / source faisant autorité** |
| build (software) | construction | **développer / créer / concevoir** |
| deploy (software) | (military) déployer | **déployer / mettre en production / livrer** |
| support (feature) | supporter (= tolerate) | **prendre en charge / être compatible avec / proposer** |
| sync with [Platform] | synchroniser avec **le** [Platform] | **synchroniser avec [Platform]** (no article for platform destinations) |
| listings (app store) | listes / listages | **fiches de l'application / pages de l'application** |

### 9. Article completeness in noun phrases

French requires definite articles in prepositional phrases with specific/known nouns. (Exception: generic classifiers like `erreur de système` for a type.)

| Wrong | Correct |
|-------|---------|
| Erreur d'application | **Erreur de l'application** |
| Configuration de compte | **Configuration du compte** |
| État de connexion | **État de la connexion** |
| Détails de transaction | **Détails de la transaction** |
| variable d'environnement manque | **la variable d'environnement manque** / **il manque la variable d'environnement** |

## UI Conventions

### Buttons — infinitive form

| Wrong (imperative) | Correct (infinitive) |
|--------------------|----------------------|
| Enregistrez | **Enregistrer** |
| Supprimez | **Supprimer** |
| Annulez | **Annuler** |

Instructions/help text use **imperative** matching the formality (Cliquez vs Clique).

### Status messages — noun form (-ment) or "En cours de..."

| Wrong | Correct |
|-------|---------|
| Charge... | **Chargement...** |
| On enregistre | **En cours d'enregistrement...** |
| Sauvegarde | **Enregistrement...** (prefer `enregistrer` over `sauvegarder`) |

### Completion — participial / prepositional

| Wrong (adjectival calque) | Correct (participial) |
|---------------------------|----------------------|
| Téléchargement réussi | **Téléchargement terminé / Fichier téléchargé** |
| Opération complète | **Opération terminée / Terminé !** |
| Paiement réussi | **Paiement effectué / Paiement confirmé** |

### Empty state — Aucun(e) X / Il n'y a pas de X

| Wrong | Correct |
|-------|---------|
| Pas de résultats | **Aucun résultat** / **Il n'y a aucun résultat** |
| Pas de fichier sélectionné | **Aucun fichier sélectionné** |
| Pas de connexion | **Aucune connexion** / **Connexion impossible** |

### Drag and drop

| English | French |
|---------|--------|
| drag | glisser |
| drop | déposer |
| **release** (let go) | **relâcher** — NOT autoriser (= permit) |
| **browse** (file picker) | **sélectionner / choisir** — NOT parcourir |

Wrong: `Autoriser le téléchargement` → `Relâchez pour téléverser`.
Wrong: `dragger` → `glisser-déposer`.

### Validation messages

Three distinct patterns by message type:

| Type | Mood | Example |
|------|------|---------|
| Field validation | indicative | `Ce champ est requis` / `[Champ] n'est pas valide` |
| Action instruction | imperative | `Entrez une valeur valide` / `Vérifiez le format` |
| State description | impersonal | `Il manque la variable d'environnement` |

Wrong: `Le champ est manquant` (calque of "missing") → `Ce champ est requis` or `Il manque ce champ`.
Wrong: `Entrer une valeur` (infinitive in error) → `Entrez une valeur valide` (imperative).

### Error messages — what happened + what to do

| Wrong (bare) | Correct (actionable) |
|--------------|----------------------|
| Fichier introuvable. | **Fichier introuvable. Veuillez vérifier le chemin.** |

### Other UI patterns

| Wrong | Correct |
|-------|---------|
| Alternatif (bare adjective) | **Détection alternative** (complete noun phrase) |
| Automatique (bare adjective) | **Mode automatique** |
| 25+ langues | **plus de 25 langues** or **25 langues et plus** |
| +{count} de plus | **et {count} autres** |
| Ajouter plus | **Ajouter d'autres / En ajouter** |
| Afficher plus | **Voir plus / Afficher la suite** |
| Essayer de nouveau (button) | **Réessayer** (single-word infinitive when one exists) |
| Charger de nouveau (button) | **Recharger** |

## vous / tu Consistency

ALL pronouns, possessives, verbs, AND imperatives must match.

| Don't mix | Use |
|-----------|-----|
| Vous pouvez modifier tes paramètres | Vous pouvez modifier **vos** paramètres |
| Téléchargez + Parcourir | Téléchargez + **Parcourez** |

vous-form: `vous`, `votre/vos`, imperative ending in -ez.
tu-form: `tu`, `ton/ta/tes`, imperative ending in -e/-s.

## Typography (CRITICAL — French is strict)

| Item | Rule | Example |
|------|------|---------|
| Before `:` `;` `?` `!` | **Non-breaking space** (NBSP) | `Question : texte ?` (NOT `Question: texte?`) |
| Inside guillemets | NBSP after `«` and before `»` | `« texte »` (NOT `"texte"`) |
| Decimal | `,` | `1 234,56` (NOT `1,234.56`) |
| Thousands | space | `1 234 567` |
| Currency | space before `€` | `99,99 €` (NOT `€99.99`) |

| Wrong | Correct |
|-------|---------|
| "English quotes" | « guillemets français » |
| Question: texte? | Question : texte ? |
| €99.99 | 99,99 € |

## Comma Rules

| Before | Comma? |
|--------|--------|
| et / ou / ni | **No comma** |
| mais (short clauses) | optional / no comma |
| mais (long/complex clauses) | comma |
| car / donc / or / puis | **Comma** (coordinating, different semantics) |

| Wrong | Correct |
|-------|---------|
| fichier, ou dossier | fichier ou dossier |
| l'erreur est survenue car le fichier | l'erreur est survenue**,** car le fichier |

## Negation Patterns

Standard formal negation uses a two-part frame around the verb.

| Negation | Meaning | Example |
|----------|---------|---------|
| ne...pas | not | `Je ne sais pas.` |
| ne...rien | nothing | `Je ne vois rien.` |
| ne...jamais | never | `Il ne se connecte jamais.` |
| ne...plus | no longer / not anymore | `Le service ne fonctionne plus.` |
| ne...personne | nobody | `Il n'y a personne.` |
| ne...aucun(e) | none / not any | `Aucun fichier n'a été trouvé.` |

| Wrong | Correct |
|-------|---------|
| Je sais pas (in formal context) | **Je ne sais pas** |
| Cliquez pas ici | **Ne cliquez pas ici** |
| Il y a pas de résultat | **Il n'y a pas de résultat / Aucun résultat** |

### Informal ne-dropping (spoken-style copy only)

In **informal spoken/written French**, `ne` is commonly dropped: `Je sais pas`, `T'inquiète pas`, `Faut pas s'en faire`. This is ACCEPTABLE in casual consumer copy mimicking spoken style (lifestyle apps, gaming, social, casual chat). NEVER drop `ne` in formal/B2B/written contexts, error messages, legal copy, or documentation.

| Formal (always keep `ne`) | Informal (ne-drop OK) |
|---------------------------|----------------------|
| Je ne sais pas. | Je sais pas. |
| Ne vous inquiétez pas. | T'inquiète pas. / T'inquiète. |
| Il ne faut pas s'en faire. | Faut pas s'en faire. |
| Ce n'est pas grave. | C'est pas grave. |
| Nous ne pouvons pas. | On peut pas. |

## Politeness Chains and Email Closings

### Request openers

| Formal (vous) | Informal (tu) |
|---------------|----------------|
| `Je vous prie de bien vouloir...` (kindly) | `Peux-tu...` |
| `Auriez-vous l'amabilité de...` (very formal) | `Tu pourrais...` |
| `Veuillez...` (please) | `Si tu veux bien...` |
| `Pourriez-vous...` | `Tu peux...` |

### Email salutations

| Formal | Informal |
|--------|----------|
| `Madame, Monsieur,` (unknown recipient) | `Bonjour Anna,` |
| `Madame Dupont,` (known female) | `Salut Max,` |
| `Monsieur Martin,` (known male) | `Coucou Léa,` (warm) |
| `Cher Monsieur,` / `Chère Madame,` (warmer formal) | `Hello Tom,` (casual / tech) |

### Email closings

| Formal | Informal |
|--------|----------|
| `Cordialement,` (standard) | `À bientôt,` |
| `Bien cordialement,` (warmer) | `Bises,` / `Bisous,` (very casual) |
| `Veuillez agréer, Madame/Monsieur, mes salutations distinguées.` (very formal / old-school) | `Bonne journée,` (warm but professional) |
| `Sincères salutations,` | `Belle journée,` |

### Thank-you phrasing

| Formal | Informal |
|--------|----------|
| `Je vous remercie de votre attention.` | `Merci !` |
| `Merci beaucoup.` | `Mille mercis !` |
| `Avec mes remerciements anticipés,` | `Merci d'avance !` |

## C'est vs Il est (common error)

- **`C'est`** + noun (with article) or adjective describing a general/abstract thing: `C'est un bon outil.` / `C'est facile.` / `C'est important.`
- **`Il/Elle est`** + adjective describing a specific known noun: `Le fichier ? Il est ouvert.` / `La page ? Elle est lente.`
- For general statements in conversational French use `C'est`: `C'est important de sauvegarder.` In formal writing the equivalent is `Il est important de sauvegarder.` (more formal but acceptable).
- In writing/formal docs: `Il est important de noter que...` is the formal equivalent of casual `C'est important de noter que...`.

| Wrong | Correct |
|-------|---------|
| Il est un bon outil. | **C'est un bon outil.** |
| C'est ouvert (referring to a specific file) | **Il est ouvert.** (le fichier → il) |
| Elle facile à utiliser (the app). | **Elle est facile à utiliser.** / **C'est facile à utiliser.** |

Note: `Il est facile à utiliser` is fine when referring to a specific app/product; `C'est facile à utiliser` is also fine and more conversational.

## Liaison and h-aspiré (silent vs aspirate h)

Liaison concerns spoken French, but in WRITING it matters for elision rules — silent `h` allows elision (`l'homme`), aspirated `h` blocks it (`le héros`).

### Common h-aspiré words (block elision, take `le/la/du/de la`)
`héros, hérisson, hibou, haine, honte, hasard, hauteur, hall, handicap, hangar, harpe, hâte, hibou, hockey, Hollande, honneur` (note: `honneur` is actually h-mute — `l'honneur`), `huit` (`le huit`), `Hongrie`.

### Common silent-h words (always elide, take `l'/de l'`)
`l'heure, l'homme, l'humanité, l'hôpital, l'huile, l'habitude, l'hiver, l'histoire, l'honneur, l'horloge, l'hôtel`.

### UI implications
Rarely affects strings, but if a feature/product is named "Hero" or "Hashtag", check whether to use `le` or `l'`:
- `le Hero banner` (h-aspiré) NOT `l'Hero banner`
- `le hashtag` (often treated as h-aspiré in French usage) — but `mot-clic` is preferred in fr-CA per OQLF.

## Adjective Position

- **Most adjectives follow the noun:** `le service personnalisé`, `la société française`.
- **BANGS adjectives precede:** Beauty (beau), Age (jeune, vieux, nouveau), Number (deux, premier), Goodness (bon, mauvais), Size (grand, petit, gros).
- **Position can change meaning:** `un homme grand` (tall) vs `un grand homme` (great). `un ancien collègue` (former) vs `un collègue ancien` (old).
- **For abstract qualities, prefer postnominal:** `avec une cohérence parfaite` (NOT `avec parfaite cohérence`); `de qualité supérieure` (NOT `de supérieure qualité`).

## Prepositional-Chain Simplification (CRITICAL)

English compound nouns produce cascading "de" chains in French. Cap at **2 prepositions max**. Use adjectives, drop redundancies, restructure.

| Wrong (3+ "de") | Correct (simplified) |
|-----------------|----------------------|
| produits de soins de la peau de nuit | **soins de nuit** (drop redundant "de la peau") |
| outil de gestion de projet de logiciel | **outil de gestion de projets logiciels** (adjective form) |
| système de suivi de livraison de colis | **système de suivi des livraisons** or **suivi de colis** |

## Calques to Avoid

| Wrong (literal) | Natural French |
|-----------------|------------------|
| Ça fait sens | **C'est logique / Ça a du sens** |
| à la fin du jour | **en fin de compte** |
| prendre avantage de | **profiter de** |
| En charge de | **Responsable de** |
| Adresser un problème | **Aborder / Traiter un problème** |
| Délivrer (= to set free) | **Fournir / Livrer** |
| et beaucoup plus | **et bien plus encore / et bien d'autres** |
| sur une base quotidienne | **au quotidien / chaque jour** |
| en termes de | **sur le plan de / quant à / concernant** |
| de notre part (error context) | **de notre côté** |
| de notre fin / sur notre côté | **de notre côté** |
| Break a leg | **Bonne chance ! / Merde !** (theatre) |
| Piece of cake | **C'est du gâteau / Un jeu d'enfant** |
| It's raining cats and dogs | **Il pleut des cordes** |

## Marketing "Zero X" → "Sans X"

| Wrong | Correct |
|-------|---------|
| Zéro temps d'arrêt | **Sans interruption / Disponibilité continue** |
| Zéro erreur | **Sans erreur** |
| Zéro maintenance | **Sans maintenance** |
| Zéro engagement | **Sans engagement** |

## Anglicism Avoidance (Toubon Law / Académie française)

Prefer French verbs over -er anglicisms:

| Anglicism | French |
|-----------|--------|
| downloader | **télécharger** |
| uploader | **téléverser** |
| updater | **mettre à jour** |
| upgrader | **mettre à niveau** |
| canceller | **annuler** |
| déleter | **supprimer** |
| checker | **vérifier** |
| forwarder | **transférer** |
| logger / délogger | **se connecter / se déconnecter** |
| fixer (for bugs) | **corriger / résoudre / réparer** |

Nouns:

| Anglicism | French |
|-----------|--------|
| Feedback | **Retour / Commentaires** |
| Must-have | **Indispensable / Incontournable** |
| Game-changer | **Révolutionnaire / Bouleversant** |
| Best practice | **Bonne pratique / Pratique exemplaire** |
| Brainstorming | **Remue-méninges** (Académie recommendation) |
| Dashboard | **Tableau de bord** |
| Workflow | **Flux de travail** |
| Template | **Modèle** |
| Analytics | **Analyses / Statistiques** |

Anglicisms ARE acceptable for: API, token, cloud, brand names, very technical terms.

## False Friends

| French word | Means | NOT the English |
|-------------|-------|-----------------|
| actuellement | currently | NOT "actually" — use `en fait` |
| éventuellement | possibly | NOT "eventually" — use `finalement` |
| réaliser | to create/accomplish | NOT "realize" — use `se rendre compte` |
| supporter | to tolerate | NOT "support" — use `soutenir / prendre en charge` |
| librairie | bookstore | NOT "library" — use `bibliothèque` |
| assister | to attend | NOT "assist" — use `aider` |
| opportunité | (often implies opportunism) | for "opportunity" — prefer `occasion / possibilité` |

## Compound Adjectives — restructure

| English | Wrong | Correct |
|---------|-------|---------|
| AI-powered/driven | IA-alimenté / IA-propulsé / données-piloté | **propulsé par l'IA / piloté par les données / avec IA** |
| X-aware / friendly / based | contexte-conscient / utilisateur-amical / nuage-basé | **contextuel / convivial / basé sur le cloud** |

## Compound Descriptive Nouns

Decompose, then rebuild naturally:

- "mom creators" → `mamans créatrices de contenu` (NOT `créatrices mères`)
- "niche creators" → `créateurs de niche` / `créateurs spécialisés`
- "beauty influencers" → `influenceurs beauté` / `influenceurs du secteur beauté`
- Use relative clauses, adjective + noun, or noun + "de" + complement.

## Business Terminology

| English compound | Wrong | Correct |
|------------------|-------|---------|
| enterprise translation | traduction pour entreprises / traduction d'entreprise | **traduction professionnelle / traduction entreprise** (adjective/apposition) |
| enterprise solution | solution pour entreprises | **solution professionnelle / solution entreprise** |
| team tool | outil pour les équipes | **outil collaboratif / outil d'équipe** |

## UI Element Reference in Prose

Reference a UI label using guillemets, definite article + label, or capitalization:

| Wrong | Correct |
|-------|---------|
| le champ de nom | **le champ « Nom »** or **le champ Nom** |
| l'onglet des comptes | **l'onglet « Comptes »** |
| la barre de recherche | (generic — no quotes needed) |

## Spatial Metaphor Prepositions

| English (figurative) | Use | Don't use |
|---------------------|-----|-----------|
| under [category] | parmi / dans | sous |
| on top of (in addition) | en plus de | sur le dessus de |
| behind the scenes | en coulisses | derrière les scènes |
| within [timeframe] | en / dans un délai de | à l'intérieur de |
| around [topic] | autour de / concernant | (literal) |
| across [platforms] | sur toutes les plateformes / à travers | (literal) |

## Temporal Expression — "[YEAR] me" idiom

English "2014 me" / "90s me" / "teenage me" = "myself at that time", not "me from X years ago".

| English | Wrong | Correct |
|---------|-------|---------|
| 2014 me | il y a 2014 ans | **moi en 2014 / le moi de 2014** |
| 90s me | il y a 90s ans | **moi dans les années 90 / le moi des années 90** |
| teenage me | 14 ans moi | **moi adolescent / moi à 14 ans** |

## Block Verb Mood Consistency

Child items must match the verb mood frame set by the section title/heading.

| Title frame | Child items |
|-------------|-------------|
| Conditional title (`Ce que vous obtiendriez :`) | Conditional or noun-phrase items (`Vous recevriez...` / `Proposition le jour ouvré...`) — NOT imperative |
| Instructional title (`Étapes à suivre :`) | Imperative or infinitive (`Configurez...` / `Configurer...`) — NOT conditional |

## Word-Sense Disambiguation

| Word | Wrong (literal) | Correct (contextual) |
|------|-----------------|---------------------|
| scale (marketing) | échelle | **envergure / ampleur / à grande échelle** |
| backstory | histoire | **histoire derrière / contexte / genèse** |
| copy (marketing) | copie | **texte / contenu** |
| sauce (figurative) | sauce | **secret / clé / ingrédient secret** |
| bug (software) | insecte | **bug / bogue** |

## Mixed-Language Agreement (loanwords)

Prefer native French. If you must use a loanword, French adjectives still agree (foreign nouns default to masculine).

| Wrong | Correct |
|-------|---------|
| les files nouveau | **les fichiers nouveaux** (prefer native) |
| le software mise à jour | **le logiciel mis à jour** (masc participle) |
| les features nouveau | **les fonctionnalités nouvelles** |

## Brand-Name Article Rules

1. **No article** for platform destinations: `synchroniser avec Apple App Store` (NOT `avec l'Apple App Store`).
2. Short forms OK: `App Store`, `Google Play`, `Play Store`.
3. Article when brand is the SUBJECT: `L'App Store propose...`.
4. Default masculine for foreign tech brands: `le OneSky`, `le Slack`.

## Proper Nouns — short forms in UI

| Wrong | Correct |
|-------|---------|
| États-Unis d'Amérique | **États-Unis / les É.-U.** |
| Royaume-Uni de Grande-Bretagne et d'Irlande du Nord | **Royaume-Uni / R.-U.** |
| anglais des États-Unis | **anglais américain** |

## Cultural Conventions

| Item | Format |
|------|--------|
| Date | `15/01/2024` (DD/MM/YYYY) or `15 janvier 2024` |
| Time | `14 h 30` (with NBSP around `h`, formal) or `14h30` (no spaces, more casual/informal) — NEVER `14:30 PM` (no AM/PM in France) |
| Currency | `99,99 €` (space before €) |
| Phone (France international) | `+33 1 23 45 67 89` |
| Phone (France national) | `01 23 45 67 89` (groups of 2) |
| Phone (Quebec) | `(514) 555-0123` or `514-555-0123` |
| Today / Yesterday / Tomorrow | `aujourd'hui` / `hier` / `demain` |
| Just now | `à l'instant` |
| Months (always lowercase) | `janvier, février, mars, avril, mai, juin, juillet, août, septembre, octobre, novembre, décembre` |
| Days (always lowercase) | `lundi, mardi, mercredi, jeudi, vendredi, samedi, dimanche` |

## Cost / Estimate Ordering

- Pattern A (preferred): `Coût estimé : {credits} crédits pour {count} langues`
- Pattern B: `{count} langues : {credits} crédits au total`
- Wrong (no connector): `{count} langues {credits} crédits`

## Self-Check Checklist (run before finalizing)

### Accuracy
- [ ] Gender correct (problème = masc, solution = fem, erreur = fem, système = masc)
- [ ] Acronym gender from expansion (l'IA = fem, l'API = fem, le PDF = masc)
- [ ] Adjective/participle agreement in gender AND number
- [ ] BANGS adjectives precede, others follow noun
- [ ] Article contractions applied (au, du, aux, des)
- [ ] Elision before vowels (l'utilisateur, d'abord, qu'il)
- [ ] Subject-verb + participle agreement (être/avoir + preceding object)
- [ ] Subjunctive after `il faut que / il est possible que / bien que`
- [ ] Non-breaking space BEFORE `:` `;` `?` `!`
- [ ] Guillemets `« »` with inside spaces (NOT `"..."`)
- [ ] Number format: `1 234,56` (comma decimal, space thousands)
- [ ] No comma before `et / ou / ni`; comma before `car / donc`
- [ ] FOR vs PER: `pour` (total) vs `par` (rate)
- [ ] Buttons in infinitive; instructions in imperative
- [ ] Date DD/MM/YYYY; time `14 h 30`; currency `99,99 €`
- [ ] All `{variables}` and ICU intact
- [ ] Articles included in noun phrases with specific nouns (`Erreur de l'application`)
- [ ] Validation: field=indicative, action=imperative, state=impersonal
- [ ] Domain terminology uses IT meaning (architecture logicielle, pipeline CI/CD, source de référence)

### Naturalness
- [ ] vous/tu consistent throughout
- [ ] UI labels are complete noun phrases (Détection alternative, NOT Alternatif)
- [ ] Buttons in infinitive; status as noun (Chargement...)
- [ ] Completion uses participial (terminé, NOT réussi)
- [ ] Empty state uses `Aucun(e) X` / `Il n'y a pas de X`
- [ ] Drag-drop verbs correct (relâcher for release, NOT autoriser)
- [ ] No anglicisms when native exists (télécharger, retour, vérifier, mettre à jour)
- [ ] No false friends in wrong sense (actuellement ≠ actually, supporter = tolerate)
- [ ] Calques avoided (`C'est logique` NOT `Ça fait sens`)
- [ ] Cascading "de" chains simplified (max 2 prepositions)
- [ ] Marketing zero: `Sans X` (NOT `Zéro X`)
- [ ] Compound adjectives: `propulsé par l'IA` (NOT `IA-alimenté`)
- [ ] Brand articles: no article for platform destinations
- [ ] UI labels in prose use `« »` or capitalization
- [ ] Spatial metaphors adapted (`parmi`, `en coulisses`, `en plus de`)
- [ ] Proper nouns short forms (États-Unis, anglais américain)
- [ ] Block verb mood consistent (conditional title → conditional items)
- [ ] Error messages: what happened + what to do
- [ ] "On our end" = `de notre côté` (NOT `de notre part / fin / bout`)
- [ ] Software vocab: `développer / créer` for "build"; `prendre en charge` for "support"

## Quebec French (fr-CA) Deltas

Apply this entire section ONLY when the user specified `fr-CA` (Quebec). It overrides the relevant Metropolitan rules above.

### Punctuation — NO space before `: ; ? !` (opposite of France)

| Item | Metropolitan (fr-FR) | Quebec (fr-CA) |
|------|----------------------|----------------|
| Colon | `Texte :` (NBSP before) | `Texte:` (no space) |
| Semicolon | `Texte ;` | `Texte;` |
| Question | `C'est vrai ?` | `C'est vrai?` |
| Exclamation | `Bienvenue !` | `Bienvenue!` |
| Guillemets | `« texte »` (NBSP inside) | `«texte»` or `« texte »` (no inside spaces is standard) |

### Date and number formats

| Item | fr-FR | fr-CA |
|------|-------|-------|
| Date | `15/01/2024` (DD/MM/YYYY) | **`2024-01-15`** (ISO YYYY-MM-DD) — Quebec official standard |
| Thousands | `1 234 567` (space) | `1 234 567` (space — same) |
| Decimal | `1 234,56` | `1 234,56` (same) |
| Currency | `99,99 €` (EUR, space before) | `99,99 $` (CAD, **symbol after**) or `99,99 $ CA` |
| Phone | `+33 X XX XX XX XX` | `514 123-4567` or `(514) 123-4567` |
| Québec spelling | — | **Always `Québec` with accent** (never bare `Quebec`) |

### Formality — `tu` more common

| Default | fr-FR | fr-CA |
|---------|-------|-------|
| Consumer app | vous | **tu** is common, and accepted in marketing/consumer UI |
| B2B / Government / Banking | vous | **vous** still required |

Apply the same NEVER-MIX rule: pronouns, possessives, verb forms, imperatives must all agree.

### Required OQLF Terminology (Loi 101)

Quebec law mandates French equivalents. These OVERRIDE any anglicism the Metropolitan rules tolerate.

| English | fr-FR (acceptable) | fr-CA (mandatory) |
|---------|--------------------|--------------------|
| email | `e-mail`, `mail`, `courrier` | **`courriel`** |
| spam | `spam` | **`pourriel`** |
| podcast | `podcast` | **`balado`** |
| blog | `blog` | **`blogue`** |
| hashtag | `hashtag` | **`mot-clic`** |
| weekend | `week-end` | **`fin de semaine`** |
| shopping | `shopping` / `faire les courses` | **`magasinage`** / `magasiner` |
| parking | `parking` | **`stationnement`** |
| cloud | `cloud` | **`infonuagique`** / `nuage` |
| streaming | `streaming` | **`diffusion en continu`** |
| smartphone | `smartphone` | **`téléphone intelligent`** |
| chat (online) | `chat`, `tchat` | **`clavardage`** (`clavarder` = to chat) |
| livestream | `livestream` | **`webdiffusion`** |
| log in / log out | `se connecter` / `se déconnecter` | **`ouvrir une session`** / **`fermer la session`** (or `se connecter`/`se déconnecter`) |
| feedback | `retour` / `commentaires` | **`rétroaction`** / `commentaires` |
| template | `modèle` / `template` | **`gabarit`** / `modèle` |

### Quebec-specific gender quirk

| Word | fr-FR | fr-CA |
|------|-------|-------|
| job | `un job` (masc) or `un boulot` | **`une job`** (feminine in Quebec!) |
| job titles | `professeur`, `auteur`, `ingénieur` | Quebec feminizes more readily: `professeure`, `auteure`, `ingénieure` |

### Quebec-specific calques

| Wrong (literal) | fr-CA correct |
|-----------------|----------------|
| `Ça fait sens` | `C'est logique / Ça a du sens` (same as Metro) |
| `à date` (for "to date") | `jusqu'à maintenant` |
| `Au jour le jour` (overused) | `Quotidiennement / De jour en jour` |
| `Supporter` (for "support") | `Prendre en charge / Soutenir` (same as Metro) |
| `Adresser un problème` | `Aborder / Traiter / Régler un problème` |
| `forwarder` | `transférer / faire suivre` |
| `checker` | `vérifier` |
| `focusser` | `se concentrer` |
| `booker` | `réserver` |
| `canceller` | `annuler` |

### Quebec cultural / idiomatic notes

| Expression | Meaning / use |
|------------|----------------|
| `Bienvenue` | Used for "you're welcome" in Quebec (fr-FR uses `de rien`) |
| `Bonjour` | Greeting at start of interactions |
| `fin de semaine` | weekend (NOT `week-end`) |
| `auto` / `char` (informal) | car (NOT `voiture` in casual speech) |
| `il pleut à boire debout` / `il mouille à siaux` | "raining cats and dogs" (use natural Quebec equivalent) |

Informal-only (avoid in software UI but recognize): `tigidou`, `être tanné`, `prendre une marche`, `Faque`, `En tout cas`.

### Quebec UI conventions (additions/overrides)

- **Empty state** — Quebec prefers concise: `Aucun résultat` over `Aucun résultat n'a été trouvé`; `Aucun fichier téléversé` over `Aucun fichier n'a été téléversé`.
- **Buttons** — infinitive (same as Metropolitan).
- **Status messages** — `Chargement...`, `Enregistrement...` (same as Metropolitan).
- **Drag-drop** — `glisser` / `déposer` / `relâcher` (same as Metropolitan).
- **Cloud-based** — `basé sur l'infonuagique` / `infonuagique` (NOT `cloud-natif` → use `natif de l'infonuagique`).

### Quebec self-check additions

- [ ] **No space** before `:` `;` `?` `!`
- [ ] Date in `YYYY-MM-DD` (ISO)
- [ ] Currency `99,99 $` (symbol after, CAD assumed)
- [ ] `Québec` always written with accent
- [ ] OQLF terms used (`courriel`, `pourriel`, `balado`, `mot-clic`, `infonuagique`, `clavardage`, `fin de semaine`, `magasinage`, `stationnement`, `téléphone intelligent`)
- [ ] No France-only anglicisms left (`week-end`, `email`, `parking`, `smartphone`, `shopping`)
- [ ] `tu` consistent if used (or `vous` consistent for B2B)
- [ ] Quebec gender: `une job` (feminine), feminized titles where natural
- [ ] Quebec calques caught (`à date`, `forwarder/checker/canceller/...`)

## Worked Example

**Source:** "Welcome! Please select your file to upload — we support 25+ formats and translate it for 5 languages in {seconds}s. Don't worry, you can cancel at any time."

**Wrong (literal):**
Bienvenue! S'il vous plaît sélectionner ton fichier pour uploader — nous supportons 25+ formats et le translatons par 5 langues dans {seconds}. Ne t'inquiètes pas, tu peux canceller à tout moment.

**Issues:** `Bienvenue!` (missing NBSP before `!`), `sélectionner` (infinitive in instruction), `ton` (mixed formality), `uploader/supportons/translatons/canceller` (anglicisms), `25+` (not natural), `par 5 langues` (FOR/PER inverted), `{seconds}` (missing `secondes`), `dans {seconds}` (wrong preposition for duration), `Ne t'inquiètes` (mixed tu/vous).

**Correct (vous-form):**
Bienvenue ! Sélectionnez votre fichier à téléverser. Nous prenons en charge plus de 25 formats et le traduisons en {seconds} secondes pour 5 langues. Vous pouvez annuler à tout moment.

**Same source, fr-CA (tu-form, OQLF terminology, no NBSP):**
Bienvenue! Sélectionne ton fichier à téléverser. On prend en charge plus de 25 formats et on le traduit en {seconds} secondes pour 5 langues. Tu peux annuler en tout temps.

(Note: `!` without preceding space; `tu/ton` chosen; impersonal `on` natural in Quebec UI; `téléverser` already correct; `en tout temps` over `à tout moment` is a slight Quebec preference but both are acceptable.)
