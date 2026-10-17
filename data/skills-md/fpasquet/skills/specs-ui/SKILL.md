---
name: specs-ui
description: >
  Crée et fait évoluer des spécifications UI maquettées en HTML + Tailwind CSS : écrans desktop et
  mobile annotés, parcours, règles fonctionnelles, points ouverts et journal des itérations, pour
  itérer sur une application ou un outil avant les développements. Si l'interface n'est pas encore
  validée, propose d'abord trois propositions qui diffèrent par la disposition (navigation,
  organisation des écrans) et par le thème (couleurs, typographie, formes), à choisir ou combiner.
  Peut aussi partir d'un site ou d'un code existant pour reprendre son style et spécifier de
  nouvelles fonctionnalités. Utiliser dès que la personne parle de maquettes, wireframes, specs UI,
  spécifications fonctionnelles avec écrans, prototype d'interface, parcours à maquetter, charte ou
  direction graphique pour une app, ou nouvelle fonctionnalité à maquetter sur un site existant,
  même sans prononcer le mot « specs ». Aussi pendant les développements, pour tenir les specs à jour
  avec l'implémentation (statut des écrans, écarts).
metadata:
  author: fpasquet
  version: "3.5.1"
---

# Specs UI maquettées en Tailwind

Ce skill produit un petit site de specs (une page par écran, publié comme un seul artifact multi-pages) qui sert de référence entre le métier et les développeurs : chaque écran y est maquetté en Tailwind (desktop et mobile), situé dans son parcours et annoté avec ses règles. On itère jusqu'à valider le fonctionnement et le rendu, puis les développements reprennent les mêmes tokens et les mêmes classes.

Documents, libellés, annotations et échanges sont en français. Le code (scripts, attributs, variables, identifiants techniques) est en anglais ; ses commentaires peuvent être en français.

Les specs sont **fonctionnelles et UI** : aucun nom de bibliothèque, de fonction, de champ d'API ni de notation technique dans les écrans, les annotations ou les règles (`redaction-specs.md`, « Specs fonctionnelles, sans code »).

`<skill>` désigne le dossier de ce skill : les scripts se lancent avec `node <skill>/scripts/…` depuis le projet de la personne.

## Économiser le contexte (à lire en premier)

Un projet de specs grossit vite : un lot d'une dizaine d'écrans en une seule page dépasse 300 Ko. C'est pourquoi les specs sont découpées en **pages par écran**, et pourquoi il ne faut jamais relire ce qui n'est pas utile. Règles :

1. **`specs/ui/CONTEXTE.md` est la mémoire du projet.** En reprise, le lire en premier et s'en contenter tant que possible. Il contient les décisions, l'identité, la disposition, les personas, les **faits du fil rouge en chaînes exactes** (identifiants, libellés, heures : à y ajouter dès qu'un écran en crée), l'inventaire avec les ancres, l'état des lots et leurs URL, les conventions propres au projet, les points ouverts et la prochaine étape. Le créer depuis `templates/contexte.md` dès l'étape 1, et le **mettre à jour à la fin de chaque étape**. Il doit rester sous 200 lignes.
2. **Ne jamais lire les pages construites (`specs/ui/site/`).** Les specs vivent dans `specs/ui/sources/` : un fichier par état d'écran. On lit et modifie seulement les fichiers utiles (`sources/<lot>/070-e15d.html`, `sources/shared/shells.html`), puis on reconstruit (étape 3).
3. **Relire ses captures en commençant par le moins cher.** Lire d'abord les alertes de `capture.mjs`, puis la planche réduite (`--sheet`, environ 1 000 tokens pour plusieurs écrans), et ouvrir un cadre seul seulement en cas de doute. Les captures de section (`--sections`) coûtent cher : à réserver aux mises en page de document.
4. **Limiter au travail en cours** : `--ids` pour ne capturer que les écrans modifiés, références du skill lues selon la table ci-dessous.
5. **Déléguer sobrement, au bon modèle** (voir « Répartir le travail entre modèles »). Un sous-agent reçoit le chemin de `CONTEXTE.md` et sa tâche, pas un résumé de tout le projet. Deux sous-agents en parallèle ne travaillent jamais sur les mêmes fichiers, et l'inventaire révisé (ID, titres, ancres) est écrit dans `CONTEXTE.md` avant de les lancer.
6. **Publier seulement ce qui a changé.** Tout le projet est un seul artifact multi-pages : `prepare-publish.mjs` liste les pages modifiées depuis la dernière publication, et seules celles-là sont envoyées. Regrouper les retouches avant de publier.

### Répartir le travail entre modèles

Écrire ou modifier du HTML d'écran, appliquer une décision, extraire du texte : c'est de l'exécution, qui ne demande pas le modèle le plus capable. Quand l'environnement permet de choisir le modèle d'un sous-agent (paramètre `model` de l'outil Agent dans Claude Code), répartir ainsi :

| Rôle | Modèle | Tâches |
|---|---|---|
| Conception et décision | modèle principal de la session | Cadrage, propositions (disposition + thème), inventaire, **fiches d'écran**, relecture des planches avec la grille de `qualite-ui.md`, dialogue et questions, `CONTEXTE.md`, publication |
| Rédaction | `sonnet` | Écrire les fichiers d'écran d'un lot à partir des fiches ; appliquer des retours ou des décisions dans les sources ; mutualiser un composant ; migrer un projet |
| Exécution mécanique | `haiku` | Lancer `build.mjs` et `capture.mjs` et rapporter les alertes ; corriger une pastille ou un lien signalé ; extraire en texte brut les points ouverts, journaux ou inventaires ; renommer en série |

**Pourquoi Sonnet pour rédiger** : écrire un écran demande de composer une mise en page soignée et de rester fidèle à la fiche, au fil rouge et à la grille de qualité. Haiku y perd en finition et oblige à des allers-retours qui coûtent plus que l'écart de prix. Haiku reste le bon choix pour ce qui ne demande aucun jugement de mise en page : lancer les scripts, extraire, renommer, corriger une pastille ou un lien signalé.

**Fiche d'écran** : ce que le modèle principal transmet au rédacteur, en 10 à 20 lignes par écran. Elle contient l'ID et les ancres de chaque état, l'objectif et l'usage dominant, le point focal, le contenu exact (faits du fil rouge), les composants et l'écran modèle à reprendre, les annotations à écrire (règle, condition, renvoi), les liens Depuis / Ensuite, et la portée mobile. Plus la fiche est précise, moins le rédacteur a besoin de contexte, et plus il peut être léger.

Le rédacteur ne décide pas : une ambiguïté ou un manque dans la fiche lui fait poser la question dans son compte rendu, pas improviser. Le modèle principal relit toujours les planches avant de publier ; un défaut de conception revient au rédacteur avec une consigne précise.

| Tâche | À lire |
|---|---|
| Reprise, itération, retouche | `CONTEXTE.md`, puis les fichiers sources concernés ; `redaction-specs.md` §6 si besoin |
| Nouveau lot de specs | `CONTEXTE.md`, `tailwind.md` §2 à §6, `qualite-ui.md` §9, un écran existant comme modèle, `shells.html` |
| Propositions d'interface | `propositions.md`, `qualite-ui.md` |
| Site existant | `site-existant.md` |
| Inventaire, évolution transverse | `redaction-specs.md` §1 à §4 |

## Fichiers produits

Les trois skills de la chaîne rangent leurs livrables dans un seul dossier `specs/` à la racine du projet. C'est aussi le dossier qui vit dans le dépôt de code de l'application pendant les développements :

```
specs/
├── ui/              ce skill : specs maquettées
├── prototype/       skill prototype-ui (facultatif)
└── requirements/    skill requirements-doc : cahier des charges (facultatif)
```

```
specs/ui/
├── CONTEXTE.md                 mémoire du projet (à jour à chaque étape)
├── tokens.css                  identité : bloc @theme Tailwind, injecté dans chaque document
├── propositions.html           propositions d'interface et décision (jamais supprimé ; copié dans le site)
├── captures/                   captures du site existant (étape 1B)
├── assets/                     (facultatif) images du produit : logos, illustrations, photos de démonstration
├── sources/
│   ├── site.json               titre, introduction, URL de l'artifact, liste ordonnée des lots, dossier des images
│   ├── shared/shells.html      coquilles <template id="tpl-shell-…"> communes à tous les lots
│   └── <lot>/                  lot.json, 000-header.html, NNN-<id>.html (un état d'écran par fichier), templates.html
└── site/                       construit par build.mjs, ne pas modifier à la main :
                                index.html (accueil), <lot>/index.html (en-tête, règles, écrans, points ouverts,
                                journal), <lot>/eN.html (une page par écran, tous ses états), propositions.html,
                                assets/ (les images citées par les pages)
```

**Images du produit.** Un logo, une mascotte, une illustration ou un insigne que l'interface affiche se montre dans la maquette, pas une forme de couleur qui le remplace : sans lui, l'écran ne se reconnaît pas. Les sources citent l'image par `assets/<chemin>` ; dans un projet qui a déjà ses images (application existante), `sources/site.json` → `"assets"` désigne leur dossier (chemin relatif à `specs/ui/`, par exemple `"../../apps/web/public/assets"`) plutôt que de les copier. `build.mjs` copie dans `site/assets/` les seules images citées, et `prepare-publish.mjs` les publie avec les pages (`tailwind.md` §7).

Les captures de vérification vont dans un dossier temporaire (le scratchpad de la session s'il existe), jamais dans le projet.

**Dans un dépôt git**, on commite les sources et `site/.published.json`, qui dit ce qui est publié, mais **pas le site construit** : le build est déterministe et prend quelques secondes, et l'équipe lit les specs dans l'artifact publié. Dans le `.gitignore` du projet : `specs/ui/site/*`, puis `!specs/ui/site/.published.json`. Sur un clone neuf, lancer `build.mjs` avant `prepare-publish.mjs`. Ne versionner le site que si l'équipe doit lire le HTML sans rien construire ni ouvrir l'artifact. Les captures et les dossiers de publication restent hors du dépôt.

## Ressources du skill

| Fichier | Rôle |
|---|---|
| `references/tailwind.md` | Tokens, cadres, blocs réutilisables, annotations, catalogue de composants |
| `references/qualite-ui.md` | Principes de qualité UI et grille de revue avant publication |
| `references/propositions.md` | Construire trois propositions (disposition + thème) |
| `references/site-existant.md` | Fonctionnalité ajoutée à un site ou une application existante |
| `references/redaction-specs.md` | Inventaire, anatomie d'un écran, états, itérations, évolutions transverses |
| `templates/specs.html` | Squelette d'un document de specs : habillage, script, deux écrans d'exemple |
| `templates/propositions.html` | Page de comparaison : trois dispositions, trois thèmes, combinables en direct |
| `templates/tokens.css`, `templates/contexte.md` | Fichier d'identité, mémoire du projet |
| `scripts/build.mjs` | Construit le site depuis les sources : pages, liens entre pages, tokens, coquilles, habillage, typographie ; liste les pages modifiées |
| `scripts/split.mjs` | Crée un lot (`--new <lot> --root specs/ui`) ou découpe un document existant en sources |
| `scripts/capture.mjs` | Contrôles d'un fichier ou de tout le site ; images : `--sheet`, `--frames`, `--thumbnails`, `--sections`, `--themes`, `--ids` |
| `scripts/check-contrast.mjs` | Contrôle WCAG AA des tokens |
| `scripts/prepare-publish.mjs` | Prépare la publication du site (page principale + pages modifiées) ou d'un document isolé ; `--check` dit si l'artifact est en retard sur le site local |
| `scripts/migrate-layout.mjs` | Range un projet à l'ancienne disposition (`specs-ui/`, `prototype-ui/`, `cdc/` côte à côte) dans `specs/` |
| `scripts/extract-identity.mjs` | Identité d'un site (URL) ou d'un code (dossier), captures |
| `scripts/upgrade.mjs` | Met un document ancien (sans sources) au niveau des templates, sans toucher aux maquettes |
| `scripts/typography.mjs` | Typographie française (appliquée automatiquement par `build.mjs`) |
| `scripts/export-design-system.mjs` | (Facultatif) Prépare un dossier Design System Claude Design : tokens, fondations, composants, README |
| `scripts/design-sync-package.mjs` | (Facultatif) Crée le paquet « tokens seuls » envoyé à Claude Design par `/design-sync` |
| `templates/design-system.html` | Catalogue de composants exporté vers le Design System |
| `templates/design-sync/` | Modèles du paquet : `build.mjs`, brouillon de conventions, notes de synchronisation |

Les templates contiennent un produit fictif (« Orbe », demandes clients) qui ne sert qu'à montrer le format : en remplacer tout le contenu.

**Où poser les questions.** Une question ne doit jamais exister seulement dans la conversation. Les choix fermés passent par l'outil de questions interactives s'il existe (AskUserQuestion), avec une option recommandée. Tout ce qui attend une réponse est aussi reporté dans le document publié (« À valider » des propositions, « Points ouverts » des specs) et dans `CONTEXTE.md`. Le message annonce ce qui est attendu.

## Étape 0 · Cadrer

1. **Reprise ?** Si `specs/ui/` existe, lire `CONTEXTE.md` et reprendre à l'étape utile. Un projet à l'ancienne disposition (`specs-ui/` à la racine, versions 2.x) se range d'abord avec `node <skill>/scripts/migrate-layout.mjs <projet>` (`--dry-run` pour voir), puis se reconstruit ; les artifacts gardent leur URL. Un projet sans `CONTEXTE.md` ni `sources/` (créé par une version 1.x, un document par lot) se migre d'abord :
   - `split.mjs` sur chaque document de specs, dans l'ordre des lots ;
   - ranger les anciens documents dans `specs/ui/archives/` ;
   - `build.mjs specs/ui`, puis contrôle avec `capture.mjs specs/ui/site <tmp>` ;
   - rédiger `CONTEXTE.md` en extrayant le texte des points ouverts et des journaux, plutôt qu'en lisant les pages ;
   - publier le site comme un nouvel artifact, et noter les anciens artifacts comme remplacés.
2. **Origine de l'identité**, déduite de la conversation : **à définir** → étape 1A ; **site ou code existant** → étape 1B ; **fournie** (charte, design system, tokens) → `tokens.css` directement, puis étape 2. Si la personne dispose d'un **Design System Claude Design** et souhaite partir de celui-ci (c'est facultatif, le proposer seulement s'il existe), le lire (outil Artifact : `list` avec le type « Design System », puis `read` du README et des tokens) et le traduire en `tokens.css` et en coquilles : l'étape 1A devient inutile.
3. **Besoin fonctionnel** : objectif, utilisateurs, règles, documents fournis. Un brief qui s'appuie sur une bibliothèque ou une documentation se lit avant de concevoir, puis se traduit en vocabulaire fonctionnel (`redaction-specs.md` §1). La bibliothèque n'apparaît jamais dans les specs.

S'il manque des informations, les demander **toutes dans un seul message**. Si le brief suffit, ne rien demander : écrire les hypothèses et produire. Sans nom de produit, en choisir un provisoire et le signaler.

## Étape 1A · Trois propositions : disposition + thème

Suivre `references/propositions.md`. Une proposition associe une **disposition** (navigation, organisation, manière de travailler) et un **thème** (palette, typographie, formes, densité). Les trois propositions diffèrent sur les deux plans, sur le **même écran représentatif**, avec le même contenu réel, desktop et mobile. Partir de `templates/propositions.html` : chaque disposition a son balisage, et des boutons appliquent n'importe quel thème à n'importe quelle disposition.

Vérifier : `check-contrast.mjs`, puis `capture.mjs --thumbnails` (test de la vignette : les trois dispositions se distinguent au premier coup d'œil), `--themes` sur deux ou trois combinaisons, et la grille de `qualite-ui.md`. Publier, puis demander un choix : une lettre, une combinaison ou des retouches. **Présenter au même point d'arrêt l'inventaire de l'étape 2** dans la section « À valider ».

Après un retour (« A et C se ressemblent »), refaire l'étape dans le même fichier et le même artifact, avec un encadré « Depuis la version précédente ». Une fois le choix fait :

- figer le thème dans `tokens.css` (source, date, contrastes revérifiés) et la disposition dans `sources/shared/shells.html` ;
- ajouter à `propositions.html` un encadré « Décision » et marquer « À valider » comme tranché. **Ne jamais supprimer `propositions.html`.**

Un choix composite se reformule précisément avant d'être appliqué. S'il reste ambigu sans moyen de demander, retenir l'interprétation la plus plausible, l'écrire comme hypothèse et la poser en première question.

## Étape 1B · Reprendre un site existant

Suivre `references/site-existant.md` : `extract-identity.mjs <url> --screenshots specs/ui/captures` (ou un dossier de code), croiser le rapport avec les captures, écrire `tokens.css` avec les valeurs exactes et leur origine, puis reproduire une page en **E0 · Existant** à côté de sa capture et faire valider la fidélité. Si l'emplacement de la fonctionnalité est incertain, proposer deux ou trois dispositions d'intégration.

## Étape 2 · Inventaire des écrans

Suivre `references/redaction-specs.md` §1. Avant toute maquette, présenter le tableau des écrans (ID, objectif, états), les parcours, les règles comprises, les hypothèses et deux ou trois questions au plus. L'écrire aussi dans le document publié et dans `CONTEXTE.md`, avec l'ancre de chaque écran. Attendre la validation. Un brief large se découpe en **lots** (un document par lot, numérotation globale) ; commencer par celui qui fixe la coquille. Le mobile est maquetté pour chaque écran, sauf portée réduite acceptée par la personne.

## Étape 3 · Écrire les specs (sources par écran)

**Créer un lot** :

```bash
node <skill>/scripts/split.mjs --new <lot> --root specs/ui     # → sources/<lot>/, inscrit dans sources/site.json
```

Dans un projet qui a déjà ses coquilles, le lot démarre d'un squelette vide (en-tête, règles, points ouverts, journal à remplir, annexe d'identité reprise d'un lot existant) : partir des écrans modèles cités dans `CONTEXTE.md`.
Puis, dans `sources/<lot>/` :

- renseigner `lot.json` : `label` (« Lot 2 · Projets et dépôts »), `title`, `fonts`, `screens` (titre court de chaque écran : `{ "e4": "Assistant de création" }`) ;
- renseigner l'en-tête (`000-header.html`) : contexte, règles, parcours ;
- écrire **un fichier par état d'écran** (`020-e4a.html`, `030-e4b.html`…) en remplaçant les écrans d'exemple. Les sections `eN…` d'un même écran forment une page ; les autres sections (règles, points ouverts, journal, annexe) vont sur l'index du lot.

Un lot peut n'avoir aucun écran : une revue des points ouverts ou une liste de décisions à prendre, faite seulement de sections (tableaux à annoter avec « Retours »), avec `"summary"` dans `lot.json` pour sa carte sur l'accueil.

Les coquilles se modifient une seule fois dans `shells.html`, pour tous les lots ; les composants communs à plusieurs lots (en-tête de projet…) vont dans `sources/shared/components.html`. Les fonds de calque et contenus réutilisés vont dans `templates.html`. Les liens s'écrivent simplement (`#e13b`, `sessions.html#e13b`, `propositions.html#retenu`) : le build les réécrit vers la bonne page.

**Construire** après chaque série de modifications :

```bash
node <skill>/scripts/build.mjs specs/ui
```

`build.mjs` produit `specs/ui/site/` : il injecte `tokens.css`, les coquilles utiles à chaque page, l'habillage et le script du template à jour, ajoute la navigation entre écrans, réécrit les liens et applique la typographie française. Les pages construites n'ont jamais besoin de mise à niveau. Il signale les liens non résolus et liste les pages modifiées.

Contenu : suivre `tailwind.md` (tokens uniquement, catalogue de composants, annotations) et `qualite-ui.md` (usage dominant, point focal, hiérarchie). Chaque écran comporte un ID, un titre, un badge, une note, « Depuis / Ensuite », une maquette desktop, une maquette mobile repensée et 3 à 6 annotations. Écrire l'en-tête et le premier écran, construire, vérifier, puis la suite.

## Étape 4 · Vérifier, puis publier

```bash
node <skill>/scripts/capture.mjs specs/ui/site <tmp>/captures                       # contrôles seuls, aucune image
node <skill>/scripts/capture.mjs specs/ui/site <tmp>/captures --sheet --ids e4,e5   # planches des écrans touchés
```

Le script signale la version du template, les icônes inconnues, les blocs non assemblés, le contenu coupé et les **pastilles posées sur du texte ou coupées par un bord** (avec le cadre, le numéro et le texte recouvert). Corriger ces alertes, relire les planches avec la grille de `qualite-ui.md` §9, ouvrir un cadre seul (`--frames --ids …`) seulement en cas de doute, puis corriger les trois défauts les plus visibles et recapturer les écrans touchés. Cette boucle prime sur toute consigne générale de vérification unique. Sans navigateur, le dire.

**Publier** (outil Artifact s'il existe ; les fichiers locaux font foi). Tout le projet est **un seul artifact multi-pages** :

```bash
node <skill>/scripts/prepare-publish.mjs specs/ui/site <tmp>/publish    # page principale + pages à envoyer
```

- Passer à l'outil Artifact la page principale préparée (`file_path`) et la table `files` affichée par le script : chemin publié → fichier de `specs/ui/site/`. Les pages secondaires sont des documents complets ; les liens relatifs entre pages fonctionnent tels quels.
- Première publication : toutes les pages (`--all`). Ensuite, seules les pages modifiées depuis la dernière publication ; les autres restent en ligne. Un artifact introuvable (supprimé, ou publié depuis un autre compte claude.ai) se remplace par un nouveau : publier avec `--all`, puis remplacer l'URL partout (`site.json`, `CONTEXTE.md`, configurations du prototype et du cahier des charges, README du projet) en notant l'ancienne comme remplacée. Avec `url`, l'outil peut exiger d'avoir vu la liste des fichiers : demander la liste (`scope: "files"`) plutôt que de relire les pages.
- Après une publication réussie : `prepare-publish.mjs specs/ui/site --confirm`. Noter l'URL dans `sources/site.json` (`artifact`) et dans `CONTEXTE.md`.
- Respecter les règles de l'outil Artifact pour la publication ; titre de deux à quatre mots.

Terminer par le chemin, le lien, un résumé court et les décisions attendues, et rappeler comment faire des retours : bouton « Retours » sur chaque page, puis coller l'export (voir « Retours de relecture » à l'étape 5). Mettre `CONTEXTE.md` à jour.

## Étape 5 · Itérer

Suivre `redaction-specs.md` §6. Pour chaque retour :

- modifier seulement les sources concernées (et celles qu'elles impactent) en gardant les identifiants stables, puis reconstruire ;
- incrémenter l'itération, ajouter une entrée au journal, mettre à jour les points ouverts ;
- vérifier, republier, mettre à jour `CONTEXTE.md`.

Selon le type de changement :

- **identité** : passe par `tokens.css`, puis reconstruire ;
- **coquille** : se fait dans `shells.html`, puis reconstruire (c'est une maintenance, pas une itération) ;
- **disposition d'un écran qui fait débat** : maquetter des variantes `E5-A` / `E5-B` côte à côte ;
- **évolution transverse** : analyse d'impact, décisions, inventaire révisé dans `CONTEXTE.md` et les propositions, puis production en commençant par le lot qui la porte.

### Retours de relecture

Chaque page du site porte un bouton **« Retours »** (habillage du document, absent des captures et de l'impression). La personne qui relit passe en mode « Annoter », clique sur l'endroit d'une maquette ou d'un texte (règle, annotation, point ouvert) et écrit une **correction à faire** ou une **question**. Chaque retour est repéré à l'endroit cliqué (R1, R2…), gardé dans son navigateur seulement, puis exporté en Markdown et collé dans la conversation : « Copier l'export », « Afficher l'export » (grande fenêtre de lecture, avec copie et sélection du texte quand le presse-papiers est refusé) et, hors artifact, « Télécharger » (une page publiée dans un artifact ne peut pas déclencher de téléchargement). L'export regroupe les retours par état d'écran et cite pour chacun le fichier source (`sources/<lot>/NNN-<id>.html`, inscrit par `build.mjs` dans chaque section), le cadre (`e4c-desktop`), la position dans le cadre et le texte visé.

Pour traiter un export :

1. **Ne lire que l'export**, puis les seuls fichiers sources qu'il cite. Repérer l'élément par le texte cité, le cadre et la position (en % de la largeur et de la hauteur du cadre) ; jamais de relecture des pages construites.
2. **Correction** claire et compatible avec les règles et décisions : l'appliquer dans la source. Correction ambiguë, qui contredit une règle, une décision de `CONTEXTE.md` ou un autre écran : la poser à la personne (outil de questions, choix fermés) plutôt que d'improviser.
3. **Question** : y répondre dans la conversation ; si elle appelle une décision, l'ajouter aux points ouverts du lot (et à `CONTEXTE.md`) avec une recommandation.
4. Une itération par série de retours : journal du lot qui cite les retours traités (« R1, R3 : … »), reconstruire, capturer les écrans touchés (`--ids`), republier les pages modifiées.
5. **Répondre par un tableau** `Retour | Suite donnée | Écran` (corrigé, question posée, point ouvert, non retenu et pourquoi). La personne marque ensuite les retours « traités » dans le panneau, ou les efface.

Les retours restent dans le navigateur de chaque personne : plusieurs relecteurs exportent chacun les leurs (le nom saisi les signe). Un retour sur un écran déjà livré (statut d'implémentation) suit la boucle de l'étape 7 : il change aussi le code, ou devient un écart.

## Option · Design System Claude Design

Fonctionnalité **facultative** : chaque personne décide de l'utiliser ou non. La proposer une fois, par une question fermée (« Exporter l'identité vers un Design System Claude Design ? » Oui / Non / Plus tard), juste après la décision de l'étape 1A ou à l'étape 6, et noter la réponse dans `CONTEXTE.md` (section « Préférences ») pour ne pas la reposer. Ne jamais l'exporter sans accord.

Si la réponse est oui, deux temps.

**1. Le catalogue** (`specs/ui/design-system/`) :

```bash
node <skill>/scripts/export-design-system.mjs specs/ui
```

Il contient le README (thème, vocabulaire des tokens, règles d'usage), `tokens.css`, les fondations (couleurs, typographie, formes), les composants du catalogue et ceux du projet (`sources/shared/`). Chaque fiche porte le marqueur de carte de Claude Design.

**2. Le paquet « tokens seuls »** (`specs/design-system-package/`, à côté de `specs/ui/`). Claude Design construit en React à partir d'un paquet : comme les specs n'ont pas de composants React, on lui envoie l'identité sous forme de tokens et de classes utilitaires. Les fiches du catalogue deviennent les cartes visibles du projet.

```bash
node <skill>/scripts/design-sync-package.mjs specs/ui
cd design-system-package && npm install && npm run build
```

- Compléter `.design-sync/conventions.md` à partir de `CONTEXTE.md`, en anglais, entre 2 000 et 4 000 caractères. C'est l'en-tête que lit le design agent : il doit nommer chaque token et dire quand l'employer, décrire les motifs récurrents (badges, coquille, en-têtes) et donner un exemple réaliste.
- La personne lance ensuite `/design-sync` depuis ce dossier, et accorde l'accès avec `/design-login` si on le lui demande. Ce skill n'envoie rien lui-même.
- Les étapes de reconstruction et les pièges connus sont dans `.design-sync/NOTES.md`.

Après une évolution de l'identité ou des composants partagés : relancer l'export, puis `npm run build` dans le paquet, puis `/design-sync`.

## Étape 6 · Passer aux développements

Vérifier qu'aucun point ouvert ne bloque, activer le statut d'implémentation (étape 7), proposer l'export Design System si la personne ne s'est pas encore prononcée (voir l'option ci-dessus), proposer l'inventaire des composants récurrents, et rappeler que `tokens.css` se colle tel quel après `@import "tailwindcss";`. Sur demande, découper en stories avec les annotations comme critères d'acceptation.

Pour faire tester les parcours ou les montrer avant de développer, le skill `prototype-ui` transforme ces specs en prototype cliquable (mêmes écrans, données simulées, scénarios de test). Pour lancer les développements, le skill `requirements-doc` en tire le cahier des charges de l'équipe (specs par lot avec critères d'acceptation, architecture, stack, infrastructure, lots et estimations).

## Étape 7 · Maintenir pendant les développements

Une fois les développements lancés, les specs restent **la référence** : elles décrivent ce que l'application fait, écran par écran, et suivent l'implémentation. Le dossier `specs/` vit dans le dépôt de l'application.

**Statut d'implémentation.** L'activer dans `sources/site.json` (`"implementation": true`), puis le tenir à jour dans le `lot.json` de chaque lot :

```json
"status": { "e1": "done", "e2": "doing", "e3": { "status": "gap", "note": "Codex pas encore pris en charge" } }
```

- Valeurs : `todo` (À développer, par défaut), `doing` (En cours), `done` (Livré), `gap` (Écart : l'application diffère des specs ; la note dit en quoi).
- Le build remplace le badge « Nouveau » de chaque état par le statut, met une pastille dans la navigation et affiche l'avancement sur l'index des lots et l'accueil. Le cahier des charges reprend les statuts à l'extraction.

**Un écart constaté pendant le développement** se tranche, puis se reporte dans le même changement que le code (même branche, même PR) :

1. **Le code a raison** (contrainte technique, meilleure idée validée) : modifier les sources de l'écran, incrémenter l'itération et noter au journal du lot « aligné sur l'implémentation », avec la raison. Garder les identifiants (écrans, états, numéros de règles) : le code et les tests les citent.
2. **Les specs ont raison** : le code se corrige ; en attendant, statut `gap` avec une note.
3. **Question ouverte** : point ouvert du lot et de `CONTEXTE.md`, statut `gap`.

Puis, dans l'ordre :

- reconstruire les specs ;
- reporter l'écart dans le prototype s'il câble l'écran (skill `prototype-ui`, « Suivre les specs ») ;
- réextraire le cahier des charges et ajuster les critères touchés (skill `requirements-doc`, « Maintenir ») ;
- publier les artifacts concernés (`prepare-publish.mjs … --check` dit lesquels sont en retard) ;
- commiter les sources et les `.published.json` ensemble (et les sites construits, s'ils sont versionnés).

**Numérotation stable.** Une règle fonctionnelle garde son numéro : une nouvelle règle va à la fin de la liste, une règle abandonnée reste avec la mention « Retirée ». Un écran ou un état retiré garde son identifiant réservé. Les identifiants RF du cahier des charges viennent de ces numéros.

## Ce que ce skill ne fait pas

- Il ne code pas l'application : les maquettes sont statiques, et les specs restent la référence.
- Il ne copie pas l'identité d'un produit tiers : un site extérieur sert d'inspiration de structure, jamais de modèle visuel.
