---
name: design-system
description: >
  Crée, maintient ou migre le design system d'une application React avec Tailwind CSS v4 : tokens en source
  unique, thème shadcn/ui et daisyUI pointé sur les tokens, classes sémantiques (btn, btn-primary, card) du projet
  ou de daisyUI posées par les variantes CVA des composants (shadcn/ui sur Radix ou Base UI), sans data-slot, un
  dossier par composant, Storybook (pages Tokens et Classes, accessibilité bloquante) et lint des classes (ni valeur
  arbitraire ni couleur de la palette). Tire les tokens et les classes du code existant, range les composants
  ajoutés par la CLI de shadcn, et mesure l'écart aux conventions par un audit. Utiliser dès que la personne parle
  de design system, de tokens, de Storybook, de shadcn/ui, de daisyUI, de Radix, de Base UI, de classes sémantiques,
  de thème ou de mode sombre, d'uniformiser l'interface, de migrer des styles (Tailwind v3, CSS modules,
  bibliothèque de composants) ou d'ajouter un composant d'interface partagé, même sans dire « design system ».
metadata:
  author: fpasquet
  version: "1.2.0"
---

# Design system React : tokens, classes sémantiques, shadcn/ui, Storybook

Ce skill met en place et fait vivre le design system d'une application React (Next.js ou Vite) en trois couches :

1. des **tokens** en source unique (bloc `@theme` de Tailwind v4) ;
2. un **thème shadcn/ui** pointé sur ces tokens, et des **classes sémantiques** (`btn`, `btn-primary`, `card`) dans `@layer components`, le CSS de chaque composant à côté de lui ;
3. des **composants shadcn/ui sur Radix ou Base UI** (style `base-*` de `components.json`), dont les variantes CVA posent ces classes : `<Button variant="primary" size="sm">` rend `btn btn-primary btn-sm`.

**Avec daisyUI**, les classes sémantiques sont les siennes, réglées par un thème daisyUI pointé sur les mêmes tokens, et les composants React posent ses classes (`btn`, `btn-primary`, `card`). Le reste ne change pas. Le mode est repéré seul (`@plugin "daisyui"`), ou choisi par `scaffold.mjs --classes daisyui` : lire `references/daisyui.md` avant le premier changement.

Storybook documente le tout : pages Tokens et Classes, une histoire par état, et un contrôle d'accessibilité qui bloque. Le lint garde les classes propres.

Trois modes, choisis à l'étape 0 :

- **créer** à partir de l'existant ;
- **maintenir** : ajouter un composant, un token ou une classe, mettre à jour une version ;
- **migrer** un design system existant vers ces conventions.

Échanges, documentation et commentaires en français. Code, identifiants, noms de classes et d'histoires en anglais.

`<skill>` désigne le dossier de ce skill, et `<app>` le dossier de l'application (celui de `components.json` ou de `package.json`). Les scripts se lancent avec `node <skill>/scripts/… <app>` depuis la racine du dépôt. Ils repèrent seuls les emplacements à partir de `components.json`, de l'alias `@/` de `tsconfig.json` et des `@import` de la feuille d'entrée de Tailwind. Des options les remplacent au besoin (`--ui`, `--tokens`…).

## Économiser les tokens (à lire en premier)

Une application compte des centaines de composants. Les lire « pour voir » est la première source de gaspillage. Règles :

1. **`<docs>/DESIGN-SYSTEM.md` est la mémoire** (en général `src/design-system/DESIGN-SYSTEM.md`) : emplacements, mode, décisions, avancement de la migration, versions. À lire en premier en reprise, et à tenir à jour à la fin de chaque étape, sous 120 lignes.
2. **Auditer avant de lire** : `audit.mjs <app>` donne l'état en une page (compteurs par règle et premiers exemples). On lit ensuite une seule règle en entier (`--rule palette-class --limit 0`), puis seulement les lignes signalées. Jamais un dossier de composants en entier.
3. **Le document de conventions du projet est la référence** (`.claude/rules/design-system.md` ou `docs/design-system.md`, posé par `scaffold.mjs`). Les références de ce skill ne servent qu'à la mise en place et à la migration.
4. **Scripts plutôt que travail à la main** : `scaffold.mjs` pose le socle, et `rehome.mjs` range et prépare un composant de shadcn. Les deux donnent un compte rendu court : le lire au lieu de relire les fichiers produits.
5. **Travailler par lot** : un dossier ou un composant à la fois, contrôlé par `eslint <dossier>` et `audit.mjs --rule …`, avec un commit par lot.

| Rôle | Modèle | Tâches |
|---|---|---|
| Conception | modèle principal | Mode, tokens et leurs noms, thème, conventions, plan de migration, revue des réécritures, mémoire |
| Rédaction | `sonnet` | Réécrire un composant ou un dossier selon le document de conventions : classes, histoires, textes |
| Exécution mécanique | `haiku` | Lancer les scripts, le lint et les tests, et rapporter ; corrections signalées par le lint |

Deux rédacteurs ne touchent jamais les mêmes fichiers. **Seul le modèle principal modifie les tokens, `theme.css` et `components.css`.** Un rédacteur reçoit le document de conventions et la liste de ses fichiers, pas l'historique de la conversation.

| Tâche | À lire |
|---|---|
| Mise en place (étape 1) | `references/setup.md` |
| Tokens (étape 2) | `references/tokens.md` |
| Ajouter ou réécrire un composant (étape 3) | `references/components.md`, `templates/ui/button/` (modèle) |
| Histoires et pages de documentation (étape 4) | `references/storybook.md` |
| Migration | `references/migration.md` |
| Projet avec daisyUI (thème, cascade, composants) | `references/daisyui.md`, `templates/ui/button-daisyui/` (modèle) |
| Toute modification de l'interface | le document de conventions du projet |

## Étape 0 · Repérer et choisir le mode

1. Trouver l'application. Dans un dépôt à plusieurs applications, demander laquelle si la conversation ne le dit pas. Quand les composants vivent dans un paquet partagé (`packages/ui`), `<app>` est ce paquet : l'audit d'une application qui le consomme l'indique (ligne `package`). Voir `references/setup.md`.
2. Si `DESIGN-SYSTEM.md` existe, c'est une reprise : lire la mémoire et passer à l'étape utile.
3. Lancer l'audit :

   ```sh
   node <skill>/scripts/audit.mjs <app>
   ```

   L'en-tête dit ce qui est en place : feuille d'entrée, tokens, thème, classes, composants, Storybook, lint, shadcn, daisyUI. Le reste liste les écarts aux conventions.
4. Proposer le mode avec **AskUserQuestion**, en recommandant celui qui découle de l'audit :
   - **créer** : ni tokens ni classes sémantiques, des couleurs et des listes d'utilitaires répétées dans le JSX ;
   - **migrer** : un design system existe, mais suit d'autres conventions (Tailwind v3, shadcn d'origine avec ses utilitaires et ses `data-slot`, CSS Modules, styled-components, bibliothèque de composants) ;
   - **maintenir** : le socle suit déjà ces conventions.
5. Un projet qui a des specs du skill `specs-ui` a déjà ses tokens. Les specs vivent dans un dépôt de specs, à part : l'application en garde une **copie** avec sa provenance (`tokens.mjs`), qu'on ne modifie jamais à la main. Une couleur se change dans les specs, puis se recopie. Ancienne disposition, `specs/ui/tokens.css` dans le dépôt de l'application : il est importé tel quel, jusqu'au déplacement des specs.
6. Les classes : un projet qui utilise daisyUI garde ses classes (mode daisyUI, ligne `daisyui` de l'audit). Pour un nouveau design system, demander avec **AskUserQuestion** si les classes sont celles du projet (recommandé : maîtrise complète, à la daisyUI) ou celles de daisyUI (moins de CSS à écrire, mise en forme imposée par daisyUI).

## Étape 1 · Poser le socle (créer, migrer)

```sh
node <skill>/scripts/scaffold.mjs <app> --mode create   # ou --mode migrate ; --classes daisyui ; --dry-run pour voir avant
```

Le script écrit ce qui manque et garde tout fichier existant :

- tokens, si l'application n'en a pas (avec daisyUI, pré-remplis par son thème en place) ;
- `theme.css` (avec daisyUI, son thème pointé sur les tokens), `components.css` et `utilities.css` ;
- Storybook : configuration et pages Introduction, Tokens et Classes ;
- le projet vitest des histoires ;
- le fragment ESLint ;
- le document de conventions et la mémoire.

Il complète aussi la feuille d'entrée par les `@import` manquants, et par `@plugin "daisyui" { themes: false; }` en mode daisyUI. Enfin, il affiche les dépendances à installer (versions testées ensemble, `templates/versions.json`), les scripts à ajouter au `package.json` et ce qui reste à faire.

Ensuite :

- installer les dépendances, ajouter les scripts, brancher le fragment ESLint (`level: 'warn'` pendant une migration) ;
- relier le document de conventions depuis `AGENTS.md` ou `CLAUDE.md` s'il n'est pas dans `.claude/rules/` ;
- servir les polices dans Storybook et envelopper les histoires dans le fournisseur de messages du projet ;
- vérifier que `build-storybook` et `test:stories` passent, puis remplir la mémoire.

Détails, Next.js ou Vite, CI : `references/setup.md`.

## Étape 2 · Tokens

- **À partir de l'existant** : `audit.mjs <app> --rule hardcoded-color --limit 0 --json`, puis `--rule palette-class`. Regrouper les valeurs par usage (fond, surface, bordure, texte, texte secondaire, marque, états), et proposer les tokens du vocabulaire commun (`canvas`, `surface`, `line`, `ink`, `muted`, `primary`, `success`…) avec leur valeur actuelle. Faire valider avec **AskUserQuestion** les fusions de valeurs proches et les couleurs d'état.
- **À partir des specs** : `scaffold.mjs <app> --specs <projet>/ui` copie les tokens des specs dans `<styles>/tokens.css`, en tête un commentaire de provenance (dépôt, chemin, empreinte). Des specs qui déclarent daisyUI (`sources/site.json` → `daisyui`) font passer aux classes de daisyUI, à leur version. Un token que lisent les feuilles du socle et qui manque à la copie (`--color-overlay`) est signalé : il s'ajoute aux specs, jamais à la copie. Ensuite :

  ```sh
  node <skill>/scripts/tokens.mjs <app> --from <projet>/ui            # recopie après une évolution des specs
  node <skill>/scripts/tokens.mjs <app> --check [--from <projet>/ui]  # à jour ? modifiée à la main ? (--strict en CI)
  ```

  Le script liste les tokens ajoutés et retirés. Il refuse de remplacer un fichier qui n'est pas une copie des specs, ou une copie modifiée à la main, sans `--force` : comparer d'abord. `<app>` et `<projet>/ui` se lisent depuis le dossier courant, quel qu'il soit. Le chemin du clone du dépôt de specs est noté dans la mémoire par `scaffold.mjs --specs` ; sans design system, l'en-tête de la copie donne le dépôt et le chemin source. Une feuille d'entrée qui importait encore `specs/ui/tokens.css` (ancienne disposition) importe la copie après le premier passage.
- **Avec daisyUI** : les couleurs de son thème en place deviennent les tokens (pré-remplies par `scaffold.mjs`), puis les thèmes intégrés se coupent et le thème du projet se supprime : `theme.css` pointe daisyUI sur les tokens (`references/daisyui.md`).
- **Toujours** :
  - une ligne par token, en hexadécimal, avec un commentaire d'usage (la page Tokens les affiche) ;
  - des échelles restreintes : les noms de Tailwind (`p-4`, `text-sm`), famille remise à zéro puis seuls les pas retenus redéclarés, jamais une échelle nommée (`p-m`) ;
  - des tailles fixes : pas de token qui change selon l'écran, la variation s'écrit en `md:` ou dans la classe d'un composant ;
  - `cn` configuré avec les tokens des échelles (`extendTailwindMerge`, `references/setup.md`) ;
  - des contrastes AA vérifiés ;
  - le mode sombre dans le bloc `.dark` de `theme.css`, seulement si la personne le veut ;
  - les mises en page d'écran en entrées nommées du thème, jamais en valeurs arbitraires.

Puis remplacer les couleurs dans le code, lot par lot (étape 5). Détails, noms et pièges (`muted`) : `references/tokens.md`.

## Étape 3 · Composants

**Avant d'écrire un bloc**, chercher s'il existe dans `<ui>` et `<components>`, puis dans daisyUI s'il est en place, puis dans le catalogue de shadcn/ui : un contrôle de formulaire passe toujours par son composant, et un champ par `Field` (`references/components.md`, « Champs de formulaire »).

**Avec daisyUI**, un composant que daisyUI a (bouton, carte, onglets, fenêtre…) s'écrit sur ses classes, avec le comportement du HTML natif ou d'une primitive Radix ou Base UI (modèle `templates/ui/button-daisyui/`, tableau des composants de `references/daisyui.md`). Un réglage de ses classes passe par le thème, sinon par la sous-couche de base de daisyUI, jamais par `@layer components` ni `@utility`. Seul ce que daisyUI n'a pas vient de shadcn, comme ci-dessous ; `rehome.mjs` refuse alors une classe qui reprend un nom de daisyUI.

Pour un composant de shadcn :

```sh
npx shadcn@<version> add dialog                      # dans <app> ; version épinglée dans la mémoire
node <skill>/scripts/rehome.mjs <app> dialog          # --class btn pour un préfixe court ; --dry-run pour voir
```

Un composant d'un sous-dossier de registre se désigne par son chemin (`rehome.mjs <app> ai-elements/message`).

`rehome.mjs` range le composant dans son dossier :

- un fichier par sous-composant, et un `index.ts` ;
- les attributs `data-slot`, `data-variant` et `data-size` retirés ;
- les utilitaires remplacés par des classes sémantiques, avec un premier jet de `dialog.css` importé par `components.css`.

Il liste ensuite ce qui reste à relire :

- les noms de classes et de variantes à aligner sur les conventions, dont les parties nommées d'après leur balise (`-div`, `-2`) ;
- les TODO (valeurs ou variantes arbitraires) ;
- les classes conditionnelles restées dans le TSX ;
- les textes en dur ;
- le code ailleurs qui ciblait ses `data-slot`.

La relecture suit `references/components.md` :

- `default` → `primary`, `destructive` → `danger` ;
- la taille par défaut fusionnée dans la classe de base ;
- les couleurs vers les tokens ;
- les états par `aria-*` ;
- les textes par les messages du projet.

Puis on écrit l'histoire, on formate et on lance le lint.

Pour un composant maison, ou des listes de classes répétées (`audit.mjs --rule repeated-classes`) : un motif d'interface devient un composant, un style répété une classe, et un ajustement ponctuel reste un utilitaire.

## Étape 4 · Storybook

- Chaque composant sans état a son histoire à côté de lui. Le titre suit la section de son dossier (`UI/`, `Shared/`, `Layouts/`, `Features/`, `Pages/`), avec une histoire par état et les données du fil rouge du produit.
- Les pages `Design system/` suivent chaque nouveau token et chaque nouvelle classe, dans le même changement.
- Une violation d'accessibilité se corrige dans le composant, jamais en désactivant la règle.

Détails : `references/storybook.md`.

## Étape 5 · Migrer (mode migrer)

1. Faire l'inventaire avec `audit.mjs <app> --json`, et lister les sources à migrer (`references/migration.md`).
2. Découper en **lots** (lint en `warn`, histoires pas encore migrées en `a11y: { test: 'todo' }`, jusqu'au dernier) : socle et tokens, puis composants de `<ui>`, puis composants partagés, puis une fonctionnalité à la fois. Écrire le plan dans la mémoire. Depuis shadcn d'origine, le lot des tokens renomme aussi les fonds `bg-muted` en `bg-surface-alt` dans tout le code qui importe le thème. Depuis daisyUI, il coupe les thèmes intégrés et réécrit ses couleurs avec `retoken.mjs` (`bg-base-100` → `bg-surface`). Proposer aussi de retirer les composants que rien n'importe (`references/migration.md`).
3. Pour chaque lot, dans un commit qui compile, passe le lint du lot et garde les histoires vertes :
   - réécrire le lot ;
   - lancer `eslint <dossier>`, puis `audit.mjs <app> --rule …` ;
   - mettre à jour la mémoire.
4. Quand l'audit n'a plus d'erreur, passer le lint de `warn` à `error`. On peut ajouter `audit.mjs <app> --strict` en CI.

## Maintenir

Chaque ajout se fait dans un seul changement, qui contient le code, sa feuille, la documentation et la mémoire :

- **un token** : le fichier de tokens, ou les specs puis `tokens.mjs` quand les tokens en sont une copie, le bloc `.dark` s'il existe, une décision datée dans la mémoire ; la page Tokens suit seule ;
- **une classe** : la feuille du composant, ou un fichier de `classes/` importé par `components.css`, plus une section de la page Classes ;
- **un composant de shadcn** : étape 3 ;
- **une variante** : on ajoute à l'API de shadcn, on n'en retire rien ;
- **du code écrit avec les classes de shadcn ou les couleurs de daisyUI** (`bg-card`, `text-muted-foreground`, `bg-base-100`) : `retoken.mjs <app>` les réécrit avec les tokens, puis le lint remet l'ordre des classes ;
- **un composant de l'application devenu générique** (sans état, sans routeur ni traductions) : le copier à plat dans `<ui>`, puis `rehome.mjs`. Ce qui tient à l'application devient une prop (libellé, rendu des liens, `locale`) et l'application garde un adaptateur ; un déclencheur de champ transmet `id` et `aria-*` à l'élément que le libellé doit nommer. Ses tests suivent le composant ;
- **un fichier qui contient plusieurs composants** : `rehome.mjs <app> <chemin> --ui src --keep-classes` le découpe (un fichier par composant, l'`index.ts` garde l'API d'origine), sur place si le fichier est déjà dans son dossier ;
- **une mise à jour de shadcn** : relancer la CLI. Comme le dossier existe, `rehome.mjs` refuse et laisse le fichier à plat pour la comparaison : reporter les changements utiles à la main, puis le supprimer ;
- **une montée de version** (Storybook, Tailwind, lint, daisyUI) : sur une branche, en vérifiant le build de Storybook, les histoires, le lint et l'audit (pour daisyUI, sa sous-couche de base et les variables de son thème), puis noter les versions dans la mémoire.

## Contrôler avant de rendre la main

```sh
node <skill>/scripts/audit.mjs <app>     # aucune nouvelle erreur sur ce qui a été touché
```

Lancer aussi les commandes du projet : lint, vérification de types, `build-storybook` et `test:stories`.

Les conventions et les pages MDX viennent de gabarits : leurs exemples (classes, tokens, fichiers) doivent exister dans le projet. L'audit signale ceux qui n'existent pas (`doc-unknown-name`) et le texte laissé à compléter (`doc-placeholder`) ; une relecture reste nécessaire pour le reste (sections Storybook sans histoires, commandes qui ne s'appliquent pas).

Dire à la personne ce qui a été contrôlé et ce qui ne l'a pas été. Une suggestion de l'audit (classes répétées, classes non documentées) se propose à la personne et ne s'applique pas d'office.

## Ressources

| Fichier | Rôle |
|---|---|
| `scripts/audit.mjs` | État des lieux : emplacements, erreurs (couleurs en dur, palette, valeurs arbitraires, pas hors de l'échelle, `data-*`, feuilles non importées, sélecteurs en double, `bg-muted`, configuration de `cn`, copie des tokens des specs modifiée, thème et cascade de daisyUI), avertissements, suggestions ; `--json`, `--strict` |
| `scripts/scaffold.mjs` | Socle sans rien écraser : tokens, thème, classes, Storybook, vitest, ESLint, conventions, mémoire ; dépendances à installer ; `--classes daisyui` |
| `scripts/rehome.mjs` | Composant de shadcn rangé (un fichier par sous-composant, `index.ts`), classes sémantiques et premier jet du CSS ; avec `--keep-classes`, découpe aussi un fichier d'application qui contient plusieurs composants |
| `scripts/retoken.mjs` | Classes de shadcn et couleurs de daisyUI réécrites avec les tokens dans le code d'une application (`bg-card`, `bg-base-100` → `bg-surface`), d'après `theme.css` ; peut être relancé |
| `scripts/tokens.mjs` | Copie des tokens des specs (dépôt de specs) avec leur provenance ; `--check` : copie en retard ou modifiée à la main |
| `scripts/project.mjs` | Repérage des emplacements (application, ou paquet de composants d'un monorepo), partagé par les scripts |
| `references/setup.md` | Mise en place : Next.js ou Vite, Storybook, vitest, ESLint, polices, messages, CI |
| `references/tokens.md` | Vocabulaire des tokens, tokens tirés du code, mode sombre, thème shadcn, mises en page nommées |
| `references/components.md` | Relecture d'un composant rangé, composants maison, classes ou composant, animations, textes |
| `references/storybook.md` | Titres et sections, histoires par état, pages d'écran, pages de documentation, accessibilité |
| `references/migration.md` | Migrer depuis shadcn d'origine, Tailwind v3, CSS Modules, styled-components ou une bibliothèque de composants |
| `references/daisyui.md` | daisyUI : mise en place, thème pointé sur les tokens, cascade (où écrire une règle), composants, lint, montée de version |
| `templates/rule.md`, `templates/memory.md` | Document de conventions et mémoire posés dans le projet |
| `templates/styles/`, `templates/storybook/`, `templates/docs/`, `templates/eslint/` | Gabarits du socle |
| `templates/ui/button/` | Modèle de composant : `button.tsx` (CVA → classes), `button.css`, histoire, `index.ts` |
| `templates/ui/button-daisyui/` | Le même modèle sur les classes de daisyUI : réglages de base dans sa sous-couche |
| `templates/versions.json` | Versions testées ensemble (CLI de shadcn, Storybook, Tailwind, vitest, lint, daisyUI) |
