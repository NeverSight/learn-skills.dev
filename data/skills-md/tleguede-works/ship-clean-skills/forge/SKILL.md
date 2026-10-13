---
name: forge
description: "Plateforme de conception, planification et spécification de nouveaux produits logiciels. Transforme une idée initiale en un plan d'implémentation exhaustif, sans ambiguïté, suffisamment précis pour être exécuté par une IA même peu performante. Couvre PRD, roadmap, benchmarks, design UI/UX, architecture, découpage en slices, plan d'implémentation par slice, plan de tests, analyse d'impact, et validation automatique des plans (mode Fast Track). Utiliser pour tout nouveau projet (greenfield) — de l'idée vague jusqu'au plan prêt à coder. Ne pas utiliser pour migrer un projet existant vers une autre stack, ni pour un travail sur du code legacy. — Design, planning and specification platform for new software products. Turns a rough idea into an exhaustive, unambiguous implementation plan precise enough for a low-capability model to execute: PRD, roadmap, benchmarks, UI/UX design, architecture, slice breakdown, per-slice implementation plans, test plan, impact analysis, and automated plan validation (Fast Track mode). Use this skill for any greenfield project, from a vague idea to a code-ready plan. Do not use it to migrate an existing project to a different stack, or to work on legacy code."
---

# Forge

Forge transforme une idée initiale — même floue — en un plan de produit et d'implémentation exhaustif, structuré en six niveaux de profondeur croissante, suffisamment précis pour qu'une IA même peu performante puisse implémenter chaque slice sans ambiguïté.

## Les six niveaux de documents

```
Niveau 0 — INTENT       : Pourquoi ce produit existe, pour qui, quel problème il résout (PRD).
Niveau 1 — SCOPE         : Quoi et quand. MVP, V1, V2..., roadmap, compromis de scope.
Niveau 2 — DESIGN        : À quoi ça ressemble. Standards, direction visuelle, écrans, flows, interactions.
Niveau 3 — ARCHITECTURE  : Comment c'est structuré. Slices, modules, fondations, modèles de données, API, dépendances.
Niveau 4 — PLAN          : Comment implémenter chaque slice. Contrats, algorithmes, composants, checklist de tâches, critères d'acceptation.
Niveau 5 — VALIDATION    : Comment vérifier que tout fonctionne. Tests unitaires, intégration, E2E, UI (Chrome MCP), régression.
```

## Vocabulaire — les trois unités de planification

- **Slice** : une fonctionnalité complète de bout en bout — UI, logique métier, accès aux données, intégration. **C'est l'unité de spécification et d'implémentation.** Inspirée de la « capacité » de [Corpus](https://github.com/anomalyco/corpus) — *une méthodologie open source tierce, pas un skill de cette collection* — mais définie à partir des besoins plutôt que du code. Une slice répond à un besoin utilisateur identifié dans le PRD.
- **Module** : un regroupement technique cohérent (ex. "authentification", "paiement"). Contient plusieurs slices. Sert à l'organisation de l'architecture, pas à la planification de l'implémentation. Son **rang** est déterminé par la fréquence d'usage, pas par l'organigramme du domaine.
- **Fondation** : une préoccupation transverse (design system, auth, gestion d'erreur, i18n, configuration, logging, CI/CD). Implémentée avant les slices métier. Reste atomique, ne se décompose pas en slices.

## Principe directeur

**Chaque décision non triviale est justifiée, chaque affirmation est vérifiable, chaque chemin est anticipé.**

Forge applique cinq principes fondamentaux :

1. **Toute règle métier, tout edge case, toute contrainte porte un identifiant stable** (B1, B2... pour les règles métier, E1, E2... pour les edge cases, V1, V2... pour les validations, C1, C2... pour les contraintes). Ces IDs ne sont jamais réutilisés, même si une règle est supprimée. Ils servent de colonne vertébrale à toute la traçabilité : PRD → Architecture → Plan → Tests.

2. **Les gates humains sont non négociables.** Chaque phase se termine par une validation explicite. Ne jamais entamer la phase suivante sans un "approuvé" clair. Ne jamais interpréter un silence ou une question comme une approbation. *(Exception bornée et documentée : le mode Fast Track, qui automatise les Phases 4-5 derrière un checkpoint unique — cf. `references/fast-track.md`.)*
   **Cette règle est appliquée par un garde-fou, pas seulement par la discipline.** Chaque artefact appartient à une phase (`PHASE_ARTIFACT_OWNERS`) : `state.js register` **refuse** d'enregistrer un artefact produit avant que sa phase soit atteinte, et `forge-guard` rattrape ce qui est déjà sur disque (`no_premature_artifacts`). Un `architecture.md` et quinze plans se sont une fois écrits pendant que le design portait `draft`, et les douze contrôles passaient : l'ordre des phases n'était qu'une consigne. S'il te dit `premature_artifact`, ce n'est pas un obstacle à contourner — c'est le signal que la base n'a pas été validée. Avance la phase, ou produis l'artefact après son gate.

3. **L'exhaustivité avant la vitesse.** Un plan superficiel qui semble cohérent mais cache des trous est pire qu'un plan plus lent à produire mais réellement complet. La question permanente : "qu'est-ce qui manque ? qu'est-ce qui a été oublié ?"

4. **Multi-perspective systématique.** Avant de verrouiller un document majeur (PRD, Architecture, Plan), au moins deux perspectives différentes doivent l'avoir analysé. Leur but n'est pas de dire "c'est bon" mais de trouver ce que la perspective principale a manqué.

5. **Les livrables vivent dans `.forge`, et rien ailleurs.** Un document produit dans un dossier temporaire est un document perdu. Ce n'est pas une recommandation, c'est une contrainte vérifiée mécaniquement par `forge-guard.js`.

## Comment exécuter les scripts

**Les commandes de ce document sont relatives au dossier DU SKILL, pas au projet.**

Les scripts ne sont pas dans le projet : ils sont installés avec le skill
(`~/.agents/skills/forge/scripts/`, `.opencode/skills/forge/scripts/`…). Un projet
n'a pas de dossier `scripts/`. Une commande dont le chemin de script est relatif
au projet n'est donc exécutable **depuis aucun projet** — à la première
invocation, elle échoue sur `Cannot find module '<projet>/scripts/state.js'`.

Définis une fois le chemin du skill, et utilise-le partout :

```bash
# Le dossier de base du skill est communiqué au chargement du skill.
export FORGE=/chemin/vers/skills/forge

node "$FORGE/scripts/state.js" start
```

Deux règles qui en découlent :

1. **Le répertoire courant est le projet**, pas le dossier du skill. Les scripts
   résolvent l'anchor depuis `process.cwd()` : lancés depuis le dossier du skill,
   ils ancrent le projet sur le dépôt des skills — c'est-à-dire sur le mauvais
   projet, sans le dire.
2. **Passe l'anchor explicitement** quand le répertoire courant n'est pas la racine
   du projet : `node "$FORGE/scripts/state.js" start /chemin/du/projet`.

---

## Étape 0 — Reprendre l'état réel (EN PREMIER, à chaque invocation)

**Cette étape précède tout le reste** — y compris la lecture de `state.json`, y compris la résolution de l'anchor.

```bash
node "$FORGE/scripts/state.js" start
```

Une commande. Elle affiche : la phase courante, les gates en attente, les slices par statut **avec présence réelle du plan et du nombre de cas de test**, les documents en dérive de hash, les divergences ouvertes, les constats non promus, et l'état de la mémoire du projet (`AGENTS.md` §Definition of Done, ADR ouvertes, volume de `LEARNINGS.md`).

**Pourquoi une commande et pas un fichier.** Un journal de session lu en entier à chaque session est trop long, et il finit par être reconstruit de mémoire. Conséquence mesurée sur un projet réel : 14 slices approuvées sans aucun test, et le suivi qui **disait faux sans aucun signal** — parce que l'avancement était connu « par la mémoire de conversation, pas par le fichier qui est censé être la source ».

Si `start` signale des slices **marquées faites sans cas de test**, ce n'est pas une nouveauté : c'est le premier signal fiable. Les traiter avant de continuer.

## Étape 0 bis — Résoudre le projet courant

Un `.forge` créé dans le mauvais dossier est un rattrapage manuel complet.

```bash
node "$FORGE/scripts/state.js" anchor
```

La commande affiche l'anchor retenu, sa source (`existing_state` | `project_marker` | `cwd`), s'il a été résolu par remontée, et la chaîne de répertoires parcourue.

**Si un projet Legacy, un corpus ou un projet de référence est accessible depuis la session, il ne doit JAMAIS devenir l'anchor.** Il se déclare en lecture seule et n'est jamais modifié :

```bash
node "$FORGE/scripts/state.js" init <racine> "<NomProduit>" --reference /chemin/vers/Legacy
```

La résolution suit trois règles, dans l'ordre :

1. Un `.forge/state.json` existant dans un répertoire ancêtre gagne — c'est la reprise d'un projet en cours, y compris depuis un sous-dossier.
2. À défaut, un marqueur de projet (`package.json`, `pyproject.toml`, `go.mod`, `.git`...) dans le répertoire courant, ou remontée courte **si le répertoire contient déjà des fichiers**. Un répertoire **vide** est un projet neuf : on ne remonte pas, sinon on ancre le nouveau projet sur un monorepo voisin.
3. À défaut, le répertoire de travail tel quel.

La commande **échoue explicitement** si l'anchor résolu est un projet de référence déclaré — y compris quand ce Legacy n'a pas de `.forge`, ce qui est le cas le plus dangereux et le plus fréquent. C'est le filet de sécurité contre le scénario le plus coûteux : analyser Legacy, puis écrire le `.forge` du nouveau projet **dans** Legacy.

## État et reprise

Si `anchor` renvoie `state_exists: true`, lis `state.json`. Il indique la dernière phase complétée, le statut de chaque slice/fondation, et les gates en attente. Annonce à l'utilisateur où en est le projet et reprends à la phase suivante — ne régénère jamais un document déjà `approved` sans demande explicite.

Si le fichier est au schéma v1, il est **refusé**, pas migré silencieusement :

```bash
node "$FORGE/scripts/state.js" migrate <anchor>
```

Voir `references/state-schema.md` pour le format exact.

## Où écris — la règle non négociable

| Quoi | Où |
|---|---|
| **Tout livrable Forge** | `<anchor>/.forge/`, sur le chemin canonique de `CANONICAL_LAYOUT` |
| État du projet | `.forge/state.json` — **métadonnées uniquement, jamais de contenu** |
| Journal d'audit | `.forge/audit/` |

Trois interdits, tous vérifiés par `forge-guard.js` :

1. **Jamais hors de `.forge/`.** Un livrable dans un dossier temporaire ou à la racine du projet est un livrable perdu.
2. **Jamais de contenu de document dans `state.json`.** Le PRD est `.forge/prd.md`. Un bloc de texte dans l'état est un bug — détecté par clé interdite et par longueur de valeur.
3. **Jamais de `status:` écrit à la main** dans le front matter d'un `.md`. Le seul écrivain est `state.js set-status`, qui met à jour l'état et le front matter dans la même opération.

## Les scripts du kit ne se modifient pas — et c'est vérifié

Les trois interdits ci-dessus protègent **les livrables du projet**. Le kit, lui,
n'était protégé par rien : `forge-guard.js` portait sur `.forge/`, `AGENTS.md`,
`.opencode/rules/` et les manifestes — **pas sur les scripts qui le font tourner**.
Et `$FORGE` est un `export` que pose l'agent, donc il peut pointer où il veut.

Deux chemins de contournement, donc, et aucun détecté. Constaté sur un projet
réel : une IA a modifié le script pour franchir des gates, et l'état du dépôt —
script corrompu, livrables obligatoires manquants — n'a été vu qu'à la relecture
humaine. **C'est le seul défaut qui désactive ses propres protections**, donc le
seul qui ne peut pas se voir tout seul.

```bash
node "$FORGE/scripts/forge-guard.js" kit-integrity <anchor>
node "$FORGE/scripts/forge-guard.js" kit-integrity <anchor> --write-manifest
```

`.forge/kit-manifest.json` enregistre une empreinte `sha256` par fichier du kit.
À chaque exécution, la porte compare. **Deux régimes, volontairement distincts :**

| Ce qui a changé | Régime | Pourquoi |
|---|---|---|
| Un **script** | **échec dur** | Les scripts appliquent le processus. Un script modifié, c'est un processus qui n'est plus appliqué |
| Un **document** de référence | **avertissement** | Il informe l'agent ; il n'applique rien. Fail et warn confondus, une mise à jour de documentation bloquerait un projet pour rien — et la porte serait contournée pour cette raison |

**Le manifeste s'écrit par un acte explicite, jamais automatiquement.** C'est la
seule opération qui puisse masquer une modification : une porte qui se
réécrirait elle-même ne protégerait plus rien. Si un script a été modifié
**voulablement** — mise à jour du kit — réécris le manifeste et **dis pourquoi
dans `DECISIONS.md`**. Sinon, restaure le script.

### Les scripts complémentaires ont une place

Quand le kit ne couvre pas un besoin réel, on écrit un script. Il va dans
`.forge/tools/`, et il est déclaré :

```json
{ "project": { "tools": { "seed-dwight.js": { "purpose": "…", "owner": "…" } } } }
```

`forge-guard.js tools` refuse trois choses, et chacune est un défaut distinct : un
outil **non déclaré** (personne ne saura qu'il existe dans trois mois), un outil
**déclaré sans but**, un outil **déclaré mais absent du disque** — un registre qui
ment sur ce qu'il contient est pire qu'un registre absent, parce qu'on s'y fie.

Écrire ailleurs — à la racine, dans `.forge/` hors `tools/` — est signalé comme un
script égaré. C'est l'emplacement par défaut de ce qui n'a pas trouvé sa place.

## Qui fait foi — l'état et les livrables ne divergent jamais

```
state.json   =  AUTORITÉ   pour le statut
front matter =  MIROIR    (champ status:), écrit par set-status
```

Si un écart apparaît — `state.json` dit `implemented`, le `.md` dit encore `draft` — il est détecté et corrigé mécaniquement :

```bash
node "$FORGE/scripts/forge-guard.js" sync .          # détecte, exit 1
node "$FORGE/scripts/forge-guard.js" sync . --fix    # réaligne le miroir sur l'autorité
```

`content_hash` porte sur le **corps** du document, jamais sur le front matter : changer un statut n'invalide donc pas un plan. Un hash qui ne match plus signale une **édition hors bande** — le document est alors `stale`.

## Qui possède quoi — la frontière avec project-rules-architect

Deux skills qui ne se connaissent pas produisent deux systèmes de mémoire concurrents, sans règle de priorité. C'est la cause structurelle de la plupart des pannes de suivi.

| Forge possède | `project-rules-architect` possède |
|---|---|
| `.forge/` — ce qu'on construit, où on en est | `AGENTS.md`, `.opencode/rules/*.md` — ce qu'il faut suivre |
| `state.json` — statuts, chemins, IDs, empreintes | `DECISIONS.md` — pourquoi · `LEARNINGS.md` — ce qui a cassé · `SESSION_LOG.md` — ce qui s'est passé |

**La règle** : un fait métier ou technique vit dans un fichier possédé par `project-rules-architect`. `state.json` n'en contient qu'un pointeur. Un `state.json` qui contient de la prose n'est pas un fichier d'état, c'est un document déguisé — et `forge-guard.js state` le rejette.

Un constat se **route**, il ne s'empile pas :

```bash
node "$FORGE/scripts/state.js" finding <anchor> --domain=testing.md --severity=majeur "<fait>" "<correction>"
```

**Le domaine est obligatoire.** Un constat sans domaine n'a aucune cible de promotion, donc il ne change rien : il devient un journal de plus, en concurrence avec les règles qu'il devait informer. C'est la cause mesurée des promotions à zéro.

Contrat complet : **`references/skill-boundaries.md`**.

## Les deux modes

| | **Guided** (défaut) | **Fast Track** |
|---|---|---|
| Gates | Un par phase | 1 à la sortie de la Phase 5, **+ 1 par jalon** en Phase 7 |
| Phases 4-5 | Manuelles, slice par slice | Automatisées, validées par sous-agents |
| Phase 7 | Manuelle | Portes exécutables par slice |
| Validateurs | Rotation de posture en session | `quality-analyst` + `red-team` + `plan-validator` en parallèle |
| Activation | Toujours possible | PRD + conventions + design + écrans + benchmarks approuvés |
| Échappatoire | — | « Reviens en mode normal », à tout moment |

**Le niveau d'autonomie est choisi à chaque activation** : `milestone` (défaut) ou `full`. Détail et justification dans `references/fast-track.md` § Les deux niveaux d'autonomie.

Fast Track ne supprime pas la validation, il supprime la **répétition**.

## Les phases

Exécute-les dans l'ordre. **Chaque phase se termine par un gate de validation humaine explicite — n'entame jamais la phase suivante sans un "approved" clair.** C'est la règle la plus importante de ce skill.

**Une phase ne peut pas être approuvée sans avoir produit ce qu'elle doit produire.** `complete-phase` et `set-phase … approved` refusent une phase dont les livrables manquent, et `forge-guard` le signale avant le gate via `current_phase_has_deliverables`. Le refus nomme le livrable absent et donne la commande pour l'enregistrer.

Ce contrat n'est pas une formalité. Les contrôles valident les livrables *déclarés* : zéro déclaration donne zéro vérification, et tout passe au vert. Constaté sur un test grandeur nature — une Phase 0 approuvée avec `deliverables: {}` et aucun `conventions.md`, puis toute la chaîne enchaînée sur cette base absente, sans qu'aucun contrôle ne bronche.

**Comment formuler un gate.** Pour un document de spécification : *"Est-ce qu'il manque des cas d'usage, ou des contraintes que tu vois déjà ?"* Pour une décomposition : *"Tu valides ce découpage en slices, ou il y a des regroupements/scissions à faire ?"* Pour un plan : *"Est-ce que l'ordre d'implémentation te semble logique, ou tu vois des dépendances qui manquent ?"* N'avance que sur un mot d'approbation explicite.

**Avant chaque gate**, lance les garde-fous. Ils sont déterministes, instantanés, et coûtent zéro token :

```bash
node "$FORGE/scripts/forge-guard.js" all <anchor>        # chemins, état, contrat de phase, synchronisation, placeholders, versions
node "$FORGE/scripts/consistency-check.js" all <anchor>   # écarts ENTRE artefacts
```

Un `fail` ici n'est pas une suggestion : corrige avant de présenter le document.

**Pourquoi deux commandes.** `forge-guard` lit un document à la fois : il vérifie qu'il existe, qu'il est au bon chemin, que son statut est cohérent. Il ne peut pas voir qu'un plan contredit l'architecture qu'il est censé implémenter. `consistency-check` ne fait que cela, et c'est le seul outil qui le fasse — parce que le motif le plus coûteux d'un projet n'est pas une spec incomplète, c'est **un artefact ultérieur qui révèle un défaut d'un artefact antérieur déjà approuvé**. Compté 13 fois sur un projet réel, avec cette phrase à côté : *« Aucun contrôle du gate ne l'attrape. »*

**Déclare de quoi un livrable dépend.** Un livrable approuvé se justifie par des exigences du PRD, et cette dépendance doit être **nommée** :

```bash
node "$FORGE/scripts/state.js" register <anchor> deliverable conventions .forge/conventions.md --requires=B11,C1,C2
```

`consistency-check premises` compare ces IDs à l'état réel du PRD et signale une exigence **retirée** dont un livrable approuvé dépend encore. Sans cette déclaration, un document reste approuvé sur une prémisse que le PRD a abandonnée : sur un test grandeur nature, `conventions.md` justifiait PostgreSQL par « la réponse à l'exigence multi-tenant strict » pendant que le PRD mettait le multi-tenant hors scope faute de second client. Aucun contrôle ne le voyait.

**Une exigence retirée garde son ID**, en tête de l'entrée `## 9. Hors scope` : `- **C102** — Multi-tenant strict — raison : …`. Retirer une exigence en lui ôtant son identifiant la rend introuvable, et la contradiction redevient indétectable — le contrôle refuse d'ailleurs un retrait sans ID, parce qu'un retrait non traçable est un retrait non déclaré.

**Un ID ne désigne qu'une seule exigence.** Si `C1` est « multi-tenant strict » en hors scope et « un seul serveur » en contraintes, toute référence à `C1` devient ambiguë — y compris celle de ce contrôle, qui accuserait alors le mauvais livrable. Le contrôle refuse la collision.

**Comment on évite la collision — et ce qu'il ne faut surtout pas faire.**

Le réflexe « je renumérote les exigences retirées dans une plage à part (B1xx, C1xx) » **casse la traçabilité** et doit être écarté : la règle qui précède dit qu'une exigence retirée *garde son ID*, précisément pour qu'un livrable approuvé puisse être relié à elle. Renommer `B18` en `B118` fait disparaître le lien — et le contrôle n'accusera plus le bon livrable, il accusera un ID que personne n'a jamais écrit.

La bonne pratique est en amont, et tient en une règle :

> **Numérote les exigences retirées en fin de plage, à partir du plus haut numéro déjà utilisé, et ne réattribue jamais un numéro libéré.**

Autrement dit, quand tu retires `B18`, `B19`, `B20`, `B21`, la prochaine exigence vivante est `B22`. Les numéros retirés restent au § 9 avec leur ID d'origine, et la plage 18–21 est déclarée brûlée. C'est exactement ce que le contrôle de collision vérifie, et il n'y a donc rien à négocier.

Cette discipline a un coût — les numéros montent plus vite — et c'est le bon échange : un trou dans la numérotation se voit, une collision d'ID ne se voit pas avant d'avoir produit un diagnostic faux.

`conventions.md` est le cas le plus fréquent : c'est un document vivant, et un amendement du PRD l'oblige. Réamende-le, repasse-le `stale` puis `approved`, et relance `consistency-check premises`.

### Qui fait quoi, phase par phase

**Cette table est normative.** Elle dit quel fichier d'agent lire pour écrire le
livrable de la phase. Sans elle, il faut deviner le nom — et deviner produit des
fichiers qui n'existent pas, dont l'absence n'échoue jamais.

Constaté deux fois de suite sur le projet de test : `agents/solution-architect.md`
pour la Phase 4 (le fichier s'appelle `systems-architect.md`) et
`agents/plan-writer.md` pour la Phase 5 (il n'existe pas). Dans les deux cas
l'appel a **semblé réussir** : un sous-agent a bien produit le livrable, en
travaillant depuis `SKILL.md` § 5 et en signalant l'absence du fichier. Un agent
qui contourne une consigne fausse n'en fait pas un defect visible — il fait
disparaître le défaut.

| Phase | Livrable | Agent à lire | Vérifié par |
|---|---|---|---|
| 1 | `.forge/prd.md` | `agents/product-analyst.md` | `forge-guard placeholders`, `client-liaison --check` |
| 2 | `.forge/roadmap.md` | `agents/scope-architect.md` | `consistency-check premises` |
| 3 | `.forge/design/` | `agents/ux-designer.md` | `design-check contrast`, `design-check tokens-used` |
| 4 | `.forge/architecture.md` | `agents/systems-architect.md` | `ddl-exec all`, `dependency-check` |
| 5 | `.forge/plans/` | **tu les écris toi-même**, en suivant `SKILL.md` § Phase 5 et `templates/implementation-plan.md.tmpl` | `coverage-check slice`, `forge-guard placeholders` |
| 6 | `.forge/test-plan.md` | `agents/quality-analyst.md` | `consistency-check plans` |

**La Phase 5 n'a pas d'agent rédacteur, et c'est délibéré.** Un plan d'implémentation
est la chose la plus facile à écrire dans le vide : un document qui décrit un code
qu'on n'a pas encore écrit passe très bien toutes les vérifications de forme. Il n'y
a donc personne à qui déléguer la rédaction — seulement `agents/plan-validator.md`,
qui **relit** un plan déjà écrit et ne réécrit rien.

`premise-challenger.md` intervient **en plus**, à deux moments de la Phase 1 : à
mi-interview sur l'idée de départ, et à la fin sur le PRD. Il ne réécrit rien : il
signale, et tu appliques.

`validate-repo` refuse un fichier d'agent présent sur le disque et jamais nommé ici,
comme il refuse un agent nommé ici et absent du disque. La table ne peut donc pas
se désynchroniser d'elle-même.

---

### Phase 0 — Bootstrap

But : établir le contexte du projet et générer la base des conventions avant toute réflexion produit.

1. **Résous l'anchor** (`state.js anchor`) — c'est l'Étape 0, déjà faite.
2. Si un projet existe déjà dans l'anchor, lis ses fichiers de configuration : `package.json`, `tsconfig.json`, `.opencode/`, `AGENTS.md`, règles, ADR. Extrais-en les conventions implicites (lint, format, structure de dossiers, stack, frameworks de test).
3. Si le projet n'existe pas encore, demande à l'utilisateur :
   - Stack technique envisagée (langage, framework, base de données...)
   - Contraintes techniques ou d'hébergement
   - Outils obligatoires ou exclus
4. **Crée `.forge/`** : `node "$FORGE/scripts/state.js" init <anchor> "<Nom>" --reference <projet de référence si applicable>`.
5. **Invoque `project-rules-architect` en mode « socle de contexte »** — voir § Les deux appels. Un seul livrable attendu : `AGENTS.md`, `SESSION_LOG.md`, `DECISIONS.md`, `LEARNINGS.md`, à la racine de l'anchor.
6. Génère `.forge/conventions.md` depuis `templates/conventions.md.tmpl`. Les sections non encore décidées (ex. state management, E2E framework) sont marquées `À DÉCIDER EN PHASE 4`.
7. Enregistre le livrable : `state.js register <anchor> deliverable conventions .forge/conventions.md`.
8. Génère `.forge/contract.md` depuis `templates/contract.md.tmpl`, **passe-le dans `client-liaison --check`**, corrige ce qu'il signale, et fais-le **signer** :
   ```bash
   node "$FORGE/scripts/state.js" register <anchor> deliverable contract .forge/contract.md
   node "$FORGE/scripts/state.js" set-status <anchor> deliverable contract approved
   ```
9. Résume à l'utilisateur ce qui a été détecté et demande confirmation.

**Ne commence jamais à parler du produit avant d'avoir établi ce contexte.** Les choix techniques contraignent les possibilités produit, et inversement.

### Après la signature, vous n'êtes plus interruptu que pour deux choses

C'est l'engagement du contrat, et il n'est pas symbolique : **tout ce qui engage un
achat est décidé avant la signature**, ou le contrat est refusé par `forge-guard
contract`. Donc ensuite :

| Motif | Comment |
|---|---|
| un **écart** au contrat | `state.js client --kind=ecart …` |
| une **décision** qui vous appartient | `state.js client --kind=decision …` |

Les quatre champs sont obligatoires — `what`, `price`, `by`, `if_no_answer` — et la
commande **refuse** un point qui n'en a pas. Une décision sans échéance ne reste pas en
attente : elle se décide, et c'est Forge qui décide. Passé la date, Forge applique la
clause « sans réponse » et vous le signale au bilan suivant.

> **Le socle de contexte ne contient aucune règle.** Entre l'appel 1 et l'appel 2, le projet a une mémoire et pas de jeu de règles : c'est l'état normal, pas un travail à moitié fait. Si l'appel 1 te renvoie un `AGENTS.md` ou un `.opencode/rules/`, le mode scaffold a été court-circuité — il s'arrête avant la sonde de stack.

---

## Les deux appels à `project-rules-architect`

Forge est l'appelant, deux fois, à deux moments fixés. **Jamais l'appelé.**

| Appel | Quand | Tu transmets | Tu récupères |
|---|---|---|---|
| **1 — socle de contexte** | Phase 0, étape 5 | le nom du produit, ce que l'utilisateur a déjà dit | les quatre fichiers de mémoire, en place |
| **2 — jeu de règles** | quand `architecture` est `approved` | la stack décidée, les conventions retenues, le périmètre MVP | `AGENTS.md` + les règles, câblées |

### Appel 1 — le socle de contexte

Invoque `project-rules-architect` et demande **explicitement le mode scaffold** :

> *« Pose la structure de contexte pour ce projet : `AGENTS.md`, `SESSION_LOG.md`,
> `DECISIONS.md`, `LEARNINGS.md`. Aucune règle, aucun `AGENTS.md`, aucune sonde de
> stack — la stack n'est pas décidée. »*

Ce qui doit revenir : **quatre fichiers à la racine de l'anchor**, avec leurs
titres, et rien d'autre. Un retour qui contient des règles est un mauvais retour.

### Appel 2 — le jeu de règles

Au moment où `architecture` passe `approved`, et **pas avant** :

> *« Voici la stack décidée et le périmètre de ce projet. Établis le jeu de règles
> et câble-le sur l'outil cible. »*

Transmets, depuis `.forge/architecture.md` et `.forge/conventions.md` : la stack
avec ses versions exactes, les conventions retenues, le périmètre, et les questions
ouvertes qui ne doivent **pas** devenir des règles.

**Transmets des extraits, pas les fichiers entiers.** Ces deux documents peuvent
faire plusieurs milliers de lignes, et la partie qui décide d'une règle est
toujours une fraction de l'ensemble. Un résumé structuré — la table de stack, les
choix de bibliothèques, les questions ouvertes — est à la fois plus petit et plus
fiable qu'un fichier complet lu en diagonale. Règle : **un fait transmis est une
ligne, pas un chapitre.**

**Pourquoi pas avant.** Les règles se génèrent *contre* la stack. Les produire
avant que la stack soit décidée, c'est deviner — et une règle devinée a
l'autorité d'une règle et la fiabilité d'une supposition, donc l'agent l'applique.

**Cet appel a une porte, pas seulement un moment.** Avant `architecture approved`
il est dû ; après, son absence est un défaut que `forge-guard` signale :

```bash
node "$FORGE/scripts/forge-guard.js" rules-present <anchor>
```

Elle échoue si le répertoire de règles est absent, vide, **ou présent mais pas
câblé** — parce que quatre fichiers Markdown que rien ne charge sont un jeu de
règles complet en apparence et totalement inerte. C'est le contrôle qui manquait :
l'appel 2 était écrit, daté, conditionné, et jamais déclenché. Sur cinq projets
du laboratoire au même avancement, un seul avait un jeu de règles, et rien ne le
disait.

Vérifie le résultat avant de continuer :

```bash
node "$PRA/scripts/rules-selftest.js" <anchor>
```

Dix contrôles sur le jeu livré : câblage, index, placeholders, renvois, seuils
contradictoires, couplage `.forge/`, contamination, prose invérifiable, portes,
budget. **Un échec ici est un défaut de livraison, pas une discussion.**

### Ce que Forge ne fait jamais avec ces fichiers

| ❌ Jamais | ✅ À la place |
|---|---|
| Écrire dans `AGENTS.md`, `SESSION_LOG.md`, `DECISIONS.md`, `LEARNINGS.md` | Rien. C'est la mémoire de l'agent, tenue par lui. |
| Créer son propre `AGENTS.md` ou `.opencode/rules/` | Le jeu de règles, produit par l'appel 2. |
| Copier une règle dans `conventions.md` | Un fait de stack, transmis à l'appel 2. |

Une mémoire écrite par deux writers perd des données **sans laisser de trace** :
l'un ajoute, l'autre écrase, et le fichier existe toujours et paraît plausible.
C'est la raison du contrat, pas une précaution de propreté.

État réel de la mémoire : `state.js start` le rapporte dans `project_memory`.

**`conventions.md` est un document vivant.** Il démarre avec ce qui est connu en Phase 0, s'enrichit en Phase 4 (architecture : choix de validation library, state management), et peut être amendé à tout moment. Les plans d'implémentation (Phase 5) y font référence ; toute modification ultérieure de `conventions.md` invalide les plans qui en dépendent — lance `state.js check-stale` après chaque amendement.

#### Le contrat d'amendement — **étendre, jamais renuméroter**

Un document que d'autres artefacts citent **par numéro** ne doit pas être renuméroté : il doit être **étendu**. Insérer en § 5.9 décale § 5.10, § 5.11, tout le reste — et chaque renvoi pointe alors vers une section **qui existe encore**, donc vers la mauvaise. C'est la pire forme de dérive : elle **résout**, un contrôle la juge saine, et rien ne la signale.

Constaté, INC-011 : l'amendement de deux causes racines critiques a inséré deux endpoints en § 5.9 et § 5.10. **Dix-sept renvois** dans huit plans sont devenus faux — `error-handling` (4), `restriction-lignes` (3), `journal-acces` (4), `export-provenance` (4) — et pas une seule ligne ne le disait. Le correctif sans risque était d'ajouter les deux endpoints **en fin de § 5**.

**N'edite pas un artefact approuvé. Amende-le :**

```bash
node "$FORGE/scripts/state.js" amend <anchor> <clé> \
  --reason "<pourquoi cet amendement existe>" \
  [--changes <fichier-listant-ce-qui-change>]
```

Ce que la commande fait, et pourquoi chaque point est là :

| | |
|---|---|
| **`--reason` obligatoire** | un amendement sans raison est une édition ordinaire. Le dire est ce qui le distingue. |
| **carte des titres** | elle est capturée à l'**approbation** — c'est la version que les autres artefacts citent. Sans elle, le premier amendement pourrait renuméroter librement. |
| **renumérotage → refus** | un numéro qui porte un autre sujet, ou qui disparaît, **refuse** la commande et nomme la dérive, dans l'ordre. L'avertissement se contourne ; le refus oblige à écrire. |
| **`--allow-renumber`** | n'est pas un interrupteur : il exige `--renumber-reason <texte>`, et cette raison reste **dans l'état**, à côté des numéros cassés. C'est la seule trace qui demeure quand personne ne se souvient pourquoi. |
| **statut → `stale`** | un artefact amendé n'est plus celui qui a été approuvé. `stale` et non `draft` : c'est le trajet déjà décrit pour un document vivant — il repasse `approved` au gate. |

Quand le refus tombe, il dit quoi faire :

```
Un document cité par numéro s'étend, il ne se renumérote pas.
Corrige sans risque : ajouter les sections NOUVELLES en fin de numérotation,
et ne toucher à aucun numéro existant.
```

**Un renvoi doit nommer sa cible.** `§ 5.15` seul ne dit pas de quel document il parle. Écris `` `architecture.md` § 5.15 `` : le contrôle sait alors exactement où regarder, sans interpréter quoi que ce soit. `consistency-check references` rend deux verdicts :

- **pointeur cassé** — cible nommée, section absente → **échec**. C'est une dérive de numérotation, la forme d'INC-011 ;
- **cible non déclarée** — renvoi nu → **compté**, jamais échec. Sur le projet de test : **276**. Les faire échouer produirait un contrôle qu'on éteint au bout d'une semaine — ce qui est arrivé quatre fois dans ce dossier. Sa voie de sortie est écrite dans sa sortie : nommer le fichier, et le compte tombe.

### Phase 1 — Discovery (PRD)

But : transformer une idée vague en un Product Requirements Document complet et cohérent.

**Ce n'est PAS une phase de rédaction.** C'est une phase d'interview et de maturation. Le PRD est le résultat, pas le processus.

**`premise-challenger` intervient deux fois dans cette phase** : à mi-interview sur l'idée de départ, et à la fin sur le PRD. Il ne réécrit rien : il signale, et tu appliques. Cf. `agents/premise-challenger.md`.

#### 1.1 Interview initiale

Pose des questions progressivement, une ou deux à la fois. Ne bombarde pas l'utilisateur. Catégories à couvrir (dans l'ordre) :

1. **Problème** : Quel problème ce produit résout-il ? Pour qui ? Pourquoi maintenant ?
2. **Utilisateurs** : Qui sont les utilisateurs ? Segments ? Niveaux de compétence ? Contexte d'usage ?
3. **Solution** : Comment le produit résout-il le problème ? Quelle est la proposition de valeur ?
4. **Fonctionnalités** : Quelles sont les fonctionnalités principales ? Les secondaires ?
5. **Contraintes** : Y a-t-il des contraintes légales, techniques, budgétaires, de temps ?
6. **Existant** : Y a-t-il des concurrents ? Des produits similaires ? Qu'est-ce qui différencie celui-ci ?
7. **Risques** : Quels sont les risques anticipés ? Les inconnues ?
8. **Succès** : Comment saura-t-on que le produit est un succès ?

#### 1.2 Challenge et approfondissement

Après l'interview initiale, challenger les réponses :

- **Détecter les contradictions** : "Tu dis que le produit doit être simple, mais la fonctionnalité X est complexe — comment concilier les deux ?"
- **Identifier les implicites** : "Tu n'as pas mentionné la gestion des erreurs — est-ce que le produit doit gérer les cas d'échec ?"
- **Tester les limites** : "Que se passe-t-il si l'utilisateur fait X dans l'état Y ?"
- **Questionner l'ambition** : "Cette fonctionnalité représente probablement 40% du travail pour 5% de l'usage — est-elle vraiment nécessaire ?"
- **Signaler les oublis** : "Je ne vois pas de mécanisme de récupération de mot de passe — est-ce que c'est volontaire ?"
- **Identifier les dépendances** : "Pour que la fonctionnalité A fonctionne, il faut d'abord que B, C et D existent — est-ce que cet ordre te convient ?"
- **Proposer des alternatives** : "Plutôt que d'implémenter un système de rôles complexe en V1, est-ce qu'un simple flag admin/utilisateur suffirait ?"

#### 1.3 Rédaction du PRD

Une fois les réponses matures, rédige le PRD dans **`.forge/prd.md`** depuis `templates/prd.md.tmpl`. Jamais dans `state.json`, jamais ailleurs.

Règles :
- Chaque règle métier reçoit un ID stable (B1, B2...).
- Chaque edge case reçoit un ID stable (E1, E2...).
- Chaque contrainte reçoit un ID stable (C1, C2...).
- Les IDs sont définitifs — ne jamais les réutiliser.
- Les user stories sont numérotées et priorisées.
- Le PRD ne contient pas de jargon technique d'implémentation (framework, base de données...) — c'est un document produit pur.
- Toute ambiguïté identifiée mais non résolue va dans la section "Points à clarifier".

Puis : `state.js register`, `forge-guard.js placeholders`, et seulement ensuite le gate.

#### 1.4 Multi-perspective review

Avant le gate final, applique la [rotation de perspective](#multi-perspective--rotation-de-perspective) — cette phase est obligatoire pour le PRD :
- **Posture qualité** : tous les types d'utilisateurs sont-ils identifiés (y compris admin, support) ? Les user stories couvrent-elles tous les cas d'usage ? Les contraintes non-fonctionnelles sont-elles couvertes ?
- **Posture risques** : y a-t-il des contradictions entre user stories ? Des règles métier implicites non explicitées ? Des hypothèses non vérifiées ?

Corrige le PRD avec les problèmes trouvés avant de le présenter.

#### 1.5 Recherche — ne pas réinventer

Avant de figer le PRD, applique `references/research-protocol.md` :

1. Identifie l'**archétype** (`references/archetypes.md`).
2. Cherche **au moins deux produits de référence**, et lis-les. Enregistre le résultat dans **`.forge/benchmarks.md`** — pas dans `state.json`.
3. Pour chaque problème métier du PRD, extrais l'**invariant** (la propriété qui ne peut pas être fausse), **pas le code**.
4. Lis les **pathologies récurrentes** de l'archétype (§ 9 de `archetypes.md`) et demande-toi, pour chacune : notre conception fait-elle mieux, et comment le sait-on ?
5. Les **écarts assumés** vont dans `benchmarks.md` § 5, avec leur coût de réversibilité.

Une recherche qui ne change **aucune décision** n'a rien produit. Si c'est le cas, le dire plutôt que de remplir le document.

#### 1.6 GATE

Présente le PRD complet. Checklist de gate (`references/review-checklists.md#prd`).

### Phase 2 — Scope (Roadmap)

But : définir ce qui entre dans chaque version et pourquoi.

#### 2.1 Analyse du scope

1. Reprends le PRD et liste toutes les fonctionnalités/user stories.
2. Pour chaque fonctionnalité, évalue : valeur utilisateur, complexité, dépendances, risques.
3. Identifie le **MVP** : le plus petit ensemble qui résout le problème principal et peut être utilisé par de vrais utilisateurs.
4. Défins la **V1** : le MVP plus les fonctionnalités qui font la différence sans exploser le scope.
5. Repousse en **V2+** tout ce qui est "nice to have" ou dépend de retours utilisateurs.

#### 2.2 Justification du découpage

Pour chaque version, explique :
- Pourquoi ces fonctionnalités sont incluses.
- Pourquoi celles-ci sont repoussées.
- Quels compromis ont été faits.
- Quels risques sont pris.

#### 2.3 Roadmap

Génère **`.forge/roadmap.md`** depuis `templates/roadmap.md.tmpl`. Jamais dans `state.json`.

Inclus pour chaque version :
- Fonctionnalités avec leurs IDs (B*)
- Critères de succès
- Dépendances entre versions
- Estimation d'effort (relative, pas en jours)
- Risques spécifiques à cette version

#### 2.4 Multi-perspective review

Avant le gate, applique la [rotation de perspective](#multi-perspective--rotation-de-perspective) :
- **Posture qualité** : les risques par version sont-ils exhaustifs ? Y a-t-il des dépendances inter-versions non explicitées ?
- **Posture risques** : le MVP résout-il vraiment le problème principal ? Qu'est-ce qui a été repoussé qui pourrait bloquer des utilisateurs réels ?

#### 2.5 GATE

Présente la roadmap. Checklist de gate (`references/review-checklists.md#roadmap`).

### Phase 3 — Design (UI/UX)

But : concevoir les interfaces avant d'implémenter les fonctionnalités, avec une direction visuelle explicite et une navigation priorisée par usage réel.

**L'ordre de cette phase est structurant. Ne le shortcuts pas.**

#### 3.1 Direction visuelle et standards — AVANT toute conception

Rien ne se dessine avant ces deux documents.

1. **Identifie l'archétype d'application** (`references/archetypes.md`) et écris la **boucle de travail** en une phrase. Enregistre-le dans `state.json` (`product.archetype`).
2. **Appelle le skill de design adapté au contexte** — obligatoire, cf. `references/design-quality.md` § 2 (mobile → `imagegen-frontend-mobile`, landing → `frontend-design`, web app dense → `impeccable`...). Si aucun n'est disponible, applique au minimum les interdits du § 3 et signale-le dans l'audit.
3. **Fixe les trois ancres** : références, ambiance (trois mots), anti-références. Sans elles, la Phase 3 n'est pas terminée.
4. Génère **`.forge/benchmarks.md`** depuis `templates/benchmarks.md.tmpl` : produits de référence, grille de conformité à l'archétype, écarts assumés. Ce document servira de référence au validateur en Fast Track.

#### 3.2 Navigation priorisée par la fréquence

**L'ordre des entrées de navigation est une déclaration de priorité**, et c'est l'erreur la plus fréquente en conception d'application mobile.

Applique `references/module-prioritization.md` :
1. Note chaque module : **fréquence** (1–5) × **centralité** (1–5), avec justification.
2. Ordonne : la boucle principale d'abord, les actions récurrentes ensuite, les entrées de cycle de vie puis la configuration.
3. **Borne à 5 items principaux** — le reste part en overflow (« Plus »).
4. **« Accueil » n'est pas premier par défaut** : il l'est parce qu'il ouvre la boucle ou qu'il est le plus utilisé.

L'ordre devient vérifiable :

```bash
node "$FORGE/scripts/state.js" set-nav <anchor> '{ "archetype": "...", "core_loop": "...", "items": [ ... ] }'
```

#### 3.3 Design system

1. Définis les **design tokens** avec des **valeurs concrètes** — jamais « à définir plus tard ».
2. Définis les **composants primitifs** : boutons, inputs, modales, cartes, tableaux, etc.
3. Définis les **patterns de navigation** : routing, breadcrumbs, sidebar, navbar, ordre des entrées (cf. 3.2).
4. Applique les **interdits** de `references/design-quality.md` § 3 : pas de blanc pur non choisi, pas d'ombre comme séparateur par défaut, pas de palette par défaut, pas d'échelle typographique uniforme.
5. Génère **`.forge/design/design-system.md`** depuis `templates/design-system.md.tmpl`.
6. **Déclare les classes de tes couleurs** dans le design system (§ 0.0 du
   gabarit). Puis : **Mesure les contrastes — ne les écris pas.** La checklist
   demande « contraste N:1 », et rien ne la vérifiait : les ratios étaient donc
   *rédigés*, pas *calculés*.

   La déclaration n'est pas une formalité. Un contrôle qui devine la classe d'une
   couleur d'après son nom ne fonctionne que dans la langue de ce nom : les
   signaux historiques sont des littéraux **anglais** (`--color-text-*`,
   `--color-ink-50`, `*-subtle`), alors que tout ce que ce skill produit est en
   français. Sur un vocabulaire français, **tout** tombait sur « composant non
   textuel » et se jugeait à 3:1 — donc **un texte à 3,80:1 passait**. C'est le
   défaut que le contrôle existe pour trouver, revenu dans le document qu'il
   venait de mesurer.

   ```html
   <!-- forge:token-classes
   text     --color-texte-principal --color-texte-secondaire
   on       --color-texte-inverse = --color-encre-700
   surface  --color-background --color-surface --color-surface-sunken
   nontext  --color-bordure-champ
   exempt   --color-encre-50 = teinte de survol, aucun texte n'y est posé
   -->
   ```

   `on:` dit sur quels fonds un texte est **réellement** posé — sans quoi un texte
   inversé, jamais posé que sur de l'encre, est mesuré contre le papier et échoue
   par construction. `exempt:` porte une **raison** : une teinte décorative n'est
   pas un composant d'interface. Un token de couleur absent des listes est
   signalé : la déclaration est un engagement, donc l'omettre est un choix.

   ```bash
   node "$FORGE/scripts/design-check.js" contrast <anchor>
   node "$FORGE/scripts/design-check.js" tokens <anchor>
   ```

   Deux choses que ce contrôle attrape, et que la relecture ne voit pas :
   un ratio **annoncé** qui ne correspond pas au mesuré — une assurance que rien
   ne soutient — et un texte lisible sur le fond mais trop clair sur **une autre
   surface**, une ligne alternée de tableau ou un panneau creusé. C'est souvent
   là que l'échec se trouve.

   Les seuils sont ceux de WCAG : 4,5:1 pour le texte contre **toute** surface
   (1.4.3), 3:1 pour un composant non textuel — dont l'anneau de focus (1.4.11).
   La classe de chaque token (texte, composant, remplissage, exempte) est
   **affichée** dans la sortie, déduite de sa déclaration, de son usage et de son
   nom : un contrôle qui ne montre pas pourquoi il a classé un token ne peut pas
   être contesté.

#### 3.4 Écrans et flows

Pour chaque fonctionnalité du PRD qui a une interface utilisateur :

1. Inventorie tous les écrans nécessaires, chacun rattaché à un rang de navigation.
2. **Un fichier par écran** dans `.forge/design/screens/<nom>.md`, généré depuis **`templates/screen.md.tmpl`**.
3. Le gabarit exige 9 états, une direction visuelle par écran, les interactions, le responsive à chaque breakpoint, l'accessibilité et la traçabilité. **Remplis-le intégralement** — un `{{PLACEHOLDER}}` résiduel est un état qui ne sera pas implémenté.
4. Définis les flows de navigation entre écrans (happy path, alternatives, erreurs, onboarding).

Puis :

```bash
node "$FORGE/scripts/forge-guard.js" placeholders <anchor>
node "$FORGE/scripts/design-check.js" contrast <anchor>
node "$FORGE/scripts/design-check.js" component-parity <anchor>
```

> Un écran qui cite un token doit citer une valeur qui **existe** et qui est
> **lisible**. Le second n'est pas visible en relisant l'écran : il se mesure.

> Un écran qui rend un composant doit connaître sa **surface**. Quand un
> composant gagne un slot ou un état, le propager à tous les écrans qui le
> rendent n'est pas une politesse : c'est la condition pour que le même
> composant n'ait pas deux rendus. `component-parity` attrape la forme que ça
> prend quand on l'oublie — une énumération devenue fausse (« ses 6 slots »
> quand il y en a 7). Un écran qui choisit de ne pas rendre un état l'écrit
> avec sa raison : `` `Tile` — exempt: `offline` (le tableau est en ligne) ``.

#### 3.5 Validation design

1. Vérifie que chaque règle métier (B*) du PRD a un écran ou un flow correspondant.
2. Vérifie que chaque état d'erreur (E*) a une représentation visuelle.
3. Vérifie la cohérence visuelle entre tous les écrans.
4. **S'il y a déjà du code** : vérifie les interfaces avec Chrome MCP (overflows, responsive, layout, navigation).

#### 3.6 Multi-perspective review

Avant le gate, applique la [rotation de perspective](#multi-perspective--rotation-de-perspective) :
- **Posture qualité** : chaque edge case a-t-il un état visuel ? L'accessibilité est-elle couverte ? Le responsive couvre-t-il tous les breakpoints ?
- **Posture risques** : y a-t-il des incohérences visuelles entre écrans ? Des états d'erreur non traités ?

#### 3.7 GATE

Présente les standards, la navigation priorisée, le design system et les écrans. L'utilisateur valide visuellement avant de passer à l'architecture. Checklist de gate (`references/review-checklists.md#design`).

### Phase 4 — Architecture (System Design)

But : décomposer le produit en slices, modules et fondations, avec leurs dépendances.

#### 4.1 Décomposition en slices

1. Reprends chaque fonctionnalité du PRD.
2. Regroupe les fonctionnalités en **modules** (regroupement technique cohérent). **L'ordre et le regroupement des modules suivent `references/module-prioritization.md`** — fréquence d'abord, organigramme du domaine jamais.
3. Découpe chaque module en **slices** (fonctionnalité de bout en bout implémentable indépendamment).
4. Identifie les **fondations transverses** (design system de la Phase 3, auth, error handling, i18n, configuration, logging, API client).

Règles de découpage :
- Une slice doit pouvoir être implémentée et testée indépendamment (ou avec des mocks pour ses dépendances).
- Une slice ne devrait pas dépasser ~10 fichiers nouveaux.
- Si une slice est trop grosse, c'est qu'elle contient plusieurs fonctionnalités distinctes.
- Si deux slices partagent 50%+ de leur code, envisager de les fusionner.

#### 4.2 Modèles de données

Pour chaque slice, définis :
- Les entités et leurs champs (type, contraintes, relations).
- Les schémas de validation.
- Les contrats d'API (endpoints, requêtes, réponses, erreurs).

**Règle** : tous les modèles sont définis champ par champ, pas résumés. Un champ oublié à cette phase est un bug à l'implémentation.

#### 4.3 Graphe de dépendances

1. **Déclare** le graphe, slice par slice :
   ```bash
   node "$FORGE/scripts/state.js" dep <anchor> <slice|fondation> <a,b,c>
   ```
   `state.js dep` refuse une dépendance vers une slice inexistante, l'auto-dépendance, et tout ce qui fermerait un cycle. Un graphe faux ne se distingue pas d'un graphe incomplet : une dépendance morte ne sera jamais satisfaite, et rien ne le signale ensuite.
2. Lance `node "$FORGE/scripts/dependency-check.js" check <anchor> --write` pour calculer `depended_on_by` et `impl_wave`.
3. Identifie les dépendances circulaires, l'ordre topologique, et quelles slices peuvent être développées en parallèle.

**Déclare ton plan de vagues s'il est plus fin que le minimum.** `dependency-check` calcule le minimum topologique. Un plan d'ordonnancement plus fin est légitime — deux personnes ne peuvent pas porter à la fois la politique RLS et la formule d'écart — mais il doit être écrit dans le front matter de l'architecture :

```yaml
impl_waves: 13
impl_waves_rationale: >-
  Plan d'ordonnancement, pas minimum topologique. Le graphe se réduit à 8 vagues ;
  on en retient 13 parce que F4 et F9 ne doivent pas être portées par la même personne.
```

Sans cette déclaration, `writeBack` écrase `impl_wave` sans rien dire, et deux documents de la Phase 4 se contredisent avec la CI verte. Déclaré sans raison, l'écart **échoue** : un plan non justifié ne se distingue pas d'une erreur de comptage. Déclaré avec sa raison, il reste visible comme avertissement.

#### 4.4 Génération du document d'architecture

Génère **`.forge/architecture.md`** depuis `templates/architecture.md.tmpl`.

#### 4.5 Le DDL s'exécute, ou n'est pas écrit

**Un DDL dans un document n'est ni compilé, ni typé, ni exécuté.** Il n'est que relu. On ne voit donc ses défauts qu'au moment de l'écrire, quand on est son auteur et qu'on relit ce qu'on vient d'écrire.

Trois défauts de ce genre ont survécu à trois gates dans un test grandeur nature, et **aucun ne se voyait à la relecture** :

- `ALTER TABLE … ADD CONSTRAINT … CHECK (… <> (SELECT … FROM …))` — un `CHECK` qui contient une sous-requête. **PostgreSQL le refuse à la création**, parce qu'un `CHECK` doit être évaluable sur la ligne seule. La contrainte n'existe pas.
- `IF NEW.status = OLD.status THEN RETURN NEW; END IF;` en tête d'un trigger — la garde ne s'atteint que sur une transition de statut. Un `UPDATE` qui écrit une autre colonne passe **au travers**. La porte est écrite, commentée, et inerte.
- Un `published_at` que le trigger exige mais que rien ne produit.

Lance, avant le gate :

```bash
node "$FORGE/scripts/ddl-exec.js" all <anchor>
```

Trois verdicts, de trois natures :

| Commande | Ce qu'elle vérifie | Moteur |
|---|---|---|
| `completeness` | Chaque table que le DDL modifie est créée, ou décrite en tableau de colonnes. Aucune n'est utilisée dans le vide. | aucun |
| `execute` | PostgreSQL **accepte** chaque instruction. Une contrainte qu'il refuse n'existe pas. | `pglite` |
| `guards` | Chaque garde que le document **déclare** refuse bien l'opération interdite. | `pglite` |

**Déclare tes gardes.** Un bloc `sql` dont la première ligne est `-- forge:ddl-refuse` contient une instruction qui **doit être rejetée**. Si elle passe, le contrôle le dit — et ce qu'il dit est vrai, parce que c'est PostgreSQL qui l'a exécutée, pas une lecture :

```sql
-- forge:ddl-refuse
-- Publier sans signature doit être refusé. Si cette instruction passe, la
-- porte n'est pas une porte.
UPDATE definition_version SET status = 'published' WHERE definition_version_id = 1;
```

Le nom de l'opération interdite n'est pas deviné par le contrôle : **le document la nomme**. C'est la différence entre un contrôle qui fonctionne et un contrôle qui devine — et tout contrôle qui doit déduire produit du bruit.

**Un garde non déclaré n'est pas testé** : ni par un script, ni par un relecteur, ni par lui-même. `guards` rend `pass` avec `guards_declared: 0` sur une architecture qui n'en déclare aucune, et **le dit** — parce qu'un contrôle qui se tait sur ce qu'il n'a pas trouvé laisse passer un vide.

Le moteur est optionnel. Sans `pglite`, `execute` et `guards` rendent `skipped` avec la ligne à installer ; ils ne rendent **jamais** `pass` sans avoir exécuté. `completeness` reste disponible : il ne demande rien à un moteur, seulement au document.

#### 4.6 Multi-perspective review

Avant le gate, applique la [rotation de perspective](#multi-perspective--rotation-de-perspective) — obligatoire pour l'architecture :
- **Posture qualité** : les modèles de données sont-ils complets champ par champ ? Chaque endpoint liste-t-il tous ses codes d'erreur ? Les slices couvrent-elles toutes les user stories du PRD ?
- **Posture risques** : y a-t-il des cycles de dépendances ? Des slices avec trop de dépendances entrantes ? Des décisions d'architecture non justifiées ?

Ajoute la **conformité aux standards** : `plan-validator` compare l'architecture à `.forge/benchmarks.md` et à l'archétype (`references/archetypes.md`).

#### 4.7 GATE

Checklist de gate (`references/review-checklists.md#architecture`).

### Phase 5 — Plan d'implémentation par slice

But : produire un plan d'implémentation tellement précis qu'une IA moins performante ne puisse pas se tromper.

Pour chaque slice, une à la fois. En mode **Guided**, un gate après chaque slice. En mode **Fast Track**, la boucle de validation automatique de `references/fast-track.md`.

#### 5.1 Contrats de données (code)

Génère le code réel dans la syntaxe de la stack cible :
- Schémas de validation (Zod, Pydantic, classes Dart, etc.).
- Types et interfaces.
- Contrats d'API (types request/response).

**Règle non négociable** : chaque champ de code doit correspondre à un champ défini dans l'architecture (Phase 4). Pas de champ inventé.

#### 5.2 Algorithmes critiques

Pour chaque règle métier (B*) à plus d'une branche conditionnelle ou plus d'une étape, rédige le pseudocode ou le code réel. Pas de paraphrase en prose.

#### 5.3 Plan composants

- Arbre de composants.
- Props, state, événements pour chaque composant.
- Gestion des états (loading, empty, error, success, edge cases).

#### 5.4 Gestion d'état (state management)

- Quelles données sont globales, lesquelles sont locales.
- Quel mécanisme de stockage pour chaque donnée.
- Flux de données entre composants.

#### 5.5 Pièges à éviter

Anticipe les erreurs d'interprétation les plus probables. Chaque piège est lié à un ID B*/E* précis et formulé comme un contraste explicite : *"Ne pas confondre X avec Y — le comportement correct est Z (cf. B12)."*

#### 5.6 Checklist de tâches

Checklist concrète et ordonnée en phases :
1. Couche de données (schémas, types, API client).
2. Logique métier (algorithmes, services, state management).
3. Interface utilisateur (composants, écrans, formulaires, navigation).
4. Intégration (permissions, feature flags, routage).
5. Tests unitaires.
6. Tests de composants.
7. Tests d'intégration / E2E.
8. Polish (accessibilité, responsive, animations, erreurs).

#### 5.7 Critères d'acceptation

Chaque critère est vérifiable individuellement et lié à un ID B*/E*/C*.

#### 5.8 Plan de tests

Pour cette slice, liste uniquement ce qui est spécifique :
- Les IDs B*/E*/C* couverts et le type de test pour chacun.
- Les scénarios E2E propres à cette slice.
- Les vérifications Chrome MCP pour les écrans de cette slice.

Le cadre commun (frameworks, patterns, règles de couverture) est défini dans le plan de tests global (`.forge/test-plan.md`, généré en Phase 6). Ne pas le dupliquer ici.

#### 5.9 Vérification de couverture

Avant le gate : `node "$FORGE/scripts/coverage-check.js" slice <anchor> <slice>` puis `node "$FORGE/scripts/forge-guard.js" placeholders <anchor>`.

`pass: false` = retourne compléter le plan. Les scripts vérifient :
- Chaque ID B*/E*/C* du PRD a une correspondance dans le plan.
- Chaque section obligatoire est présente et non vide.
- Aucun `{{PLACEHOLDER}}` résiduel.

#### 5.10 GATE

Checklist de gate (`references/review-checklists.md#implementation-plan`).

### Phase 6 — Validation (Test Plan global)

But : définir la stratégie de test globale et configurer l'environnement de test.

#### 6.1 Configuration des tests

1. Installer/initialiser le framework de test (Jest, Vitest, Pytest...).
2. Installer/initialiser les outils E2E (Playwright, Cypress...).
3. Configurer le MCP Chrome pour les vérifications UI.

#### 6.2 Tests de fondation

Pour chaque fondation, écrire les tests AVANT l'implémentation des slices :
- Design system : tests de rendu des composants primitifs.
- Auth : tests du flux d'authentification.
- Error handling : tests du comportement en cas d'erreur.
- i18n : tests de présence des traductions.
- API client : tests des intercepteurs, retry, timeout.

#### 6.3 Plan de régression

Définir la suite de tests de régression qui devra passer avant chaque merge.

#### 6.4 GATE

Checklist de gate (`references/review-checklists.md#validation`).

### Phase 7 — Implémentation

Pour chaque slice dont le plan est approuvé :

1. Vérifie que toutes les dépendances sont implémentées (ou mockées) : `node "$FORGE/scripts/state.js" check-stale <anchor> <slice>`.
2. Lis d'abord le plan d'implémentation de cette slice et les conventions (`.forge/conventions.md`). Si le plan est ambigu sur l'interaction avec une autre slice, consulte uniquement la section concernée de l'architecture — ne lis pas l'architecture entière.
3. Implémente selon la checklist de tâches, en respectant strictement les contrats de données, algorithmes et pièges documentés.
4. **Écris les tests en premier** (TDD) quand c'est pertinent, sinon juste après l'implémentation de chaque couche.
5. Vérifie chaque critère d'acceptation.
6. **Exécute le critère de sortie** — c'est une porte, pas une checklist :
   ```bash
   node "$FORGE/scripts/forge-exit.js" <anchor> <slice>
   ```
   Elle lance les vraies commandes du projet et vérifie que la slice a des **cas de test**, pas un fichier de test. « Le test existe » signifie « il y a au moins un cas » — c'est la distinction qui manquait quand 14 slices ont été approuvées sans aucun test.
7. Lance les vérifications Chrome MCP : overflows, responsive, navigation, états d'erreur.
8. **Route les constats révélés** avec un domaine — jamais de constat sans cible :
   ```bash
   node "$FORGE/scripts/state.js" finding <anchor> --domain=<règle visée> --severity=<s> "<fait>" "<correction>"
   ```
9. `node "$FORGE/scripts/consistency-check.js" all <anchor>` — cette slice ne doit pas apparaître en écart.
10. Mets à jour le statut : `state.js set-status <anchor> slice <slice> implemented`, puis `validated` après validation.
11. **GATE** après chaque slice.

**Règle** : ne jamais passer à la slice suivante tant que la slice courante n'est pas entièrement testée et validée.

**Sous Fast Track**, les étapes 1-9 ne s'interrompent pas : l'implémentation avance, et un **rapport de jalon** (3 à 5 slices) est produit à la demande. Le rapport distingue explicitement ce qui a été vérifié mécaniquement de ce qui ne l'a pas été.

**Si le domaine a des échéances** — loyers, abonnements, délais — un **scénario de cycle complet** fait partie du critère de sortie de la slice qui introduit le cycle de vie, pas de la dernière. Cf. `references/scenario-tests.md`.

### Phase 8 — Validation finale

1. Lance la suite de régression complète.
2. Vérifie que tous les critères d'acceptation du PRD sont satisfaits.
3. Applique la rotation de perspective (posture qualité + posture risques) une dernière fois sur l'ensemble.
4. Lance `node "$FORGE/scripts/forge-guard.js" all <anchor>`.
5. Mets à jour `state.json` : projet → `validated`.
6. Ferme le journal d'incidents (`.forge/audit/issues.md`) et génère le rapport d'audit du projet.

---

## Gestion des changements et analyse d'impact

> **Chaque changement peut avoir des conséquences.**

Quand l'utilisateur demande une modification (fonctionnalité, règle, interface, architecture...), **ne jamais appliquer le changement immédiatement sans analyse d'impact.**

### Protocole d'analyse d'impact

Avant d'appliquer le changement, suis le protocole `references/impact-protocol.md`. Résume à l'utilisateur :

1. **Fonctionnalités affectées** : quelles règles métier (B*) sont modifiées, créées, supprimées ?
2. **Interfaces affectées** : quels écrans doivent être modifiés ?
3. **Modules/slices affectés** : quelles slices doivent être retouchées ?
4. **Dépendances affectées** : quelles autres slices dépendent de ce qui change ?
5. **Tests à modifier** : quels tests existants seront cassés ?
6. **Documents à mettre à jour** : PRD, architecture, plans, roadmap ?
7. **Risques** : qu'est-ce qui pourrait casser silencieusement ?
8. **Effort** : estimation relative de l'impact (localisé / modéré / majeur / structurel).

L'utilisateur doit confirmer explicitement qu'il accepte les conséquences avant que le changement soit appliqué.

### Après application du changement

1. Mets à jour le document source (PRD, architecture, design...).
2. Propage les conséquences dans tous les documents impactés (plans, roadmap, tests).
3. Marque les documents impactés `stale` : `state.js set-status <anchor> <kind> <clé> stale`.
4. Lance `state.js check-stale` sur les slices concernées.
5. Vérifie la cohérence globale : `forge-guard.js all`.
6. Signale tout ce qui est devenu incohérent.

---

## Multi-perspective — deux modes de validation

Un document majeur n'est jamais verrouillé après un seul regard. Deux mécanismes existe, selon le mode.

### Mode Guided — rotation de posture (par défaut)

Dans la session principale, le document est relu deux fois sous deux postures explicites :

1. **Posture qualité** : edge cases manquants, règles sans test correspondant, contraintes non-fonctionnelles non couvertes.
2. **Posture risques** : contradictions internes, hypothèses non vérifiées, dépendances implicites, angles morts.

Puis corrige, puis présente : *"J'ai relu ce document sous l'angle qualité et risques. Voici ce que j'ai trouvé et corrigé : [liste]. Voici ce qui reste à trancher : [liste]."*

**Quand l'appliquer** : obligatoire avant les gates PRD (Phase 1), Architecture (Phase 4) et Validation finale (Phase 8) ; recommandé pour Roadmap, Design et les plans.

**Pourquoi en session plutôt qu'avec des sous-agents** : la rotation de posture est immédiate, ne coûte aucun appel LLM supplémentaire, et force le même niveau de rigueur sur un document que la session vient de produire. Sur une majorité de projets, l'orchestration d'agents par gate n'apporterait pas proportionnellement plus.

### Mode Fast Track — sous-agents spécialisés (automatique)

Quand la direction est déjà validée (PRD, conventions, design, écrans, benchmarks approuvés), valider 15 plans à la main est fatigant et induit des validations de courtesy. Fast Track délègue alors la validation à des **agents spécialisés aux angles morts complémentaires**, lancés en parallèle :

| Agent | Cherche ce qui est… | Question |
|---|---|---|
| `quality-analyst` | **absent** | « Cette spec est-elle complète ? » |
| `red-team` | **faux** | « Qu'est-ce qui ne marchera pas ? » |
| `plan-validator` | **non standard** | « Est-ce cohérent avec les standards de ce type d'app ? » |

Chaque agent a un **contrat d'entrée** (les seuls fichiers à lire) et un **contrat de sortie** (JSON strict). Ils ne voient jamais tout `.forge` — le contexte est le coût, et un validateur surchargé de contexte valide moins bien.

Les scripts déterministes passent **avant** les agents : un script détecte en une seconde ce qu'un agent met trois lectures à trouver.

**La porte d'entrée est exécutable, et elle refuse en nommant** :

```bash
node "$FORGE/scripts/forge-guard.js" fast-track <anchor> \
     [--scope plans|phases4-7] [--autonomy milestone|full]
```

Elle n'est pas dans `forge-guard all` — `benchmarks` est de phase 3 et `test_plan` de
phase 6, donc elle ferait échouer tout projet ordinaire. Mais elle ne se contourne pas
parce qu'on l'a oubliée : `state.js status` affiche si le mode est actif, et
`state.js fast-track --attempt` **s'arrête à la troisième tentative**.

Protocole complet, conditions d'entrée, limites et échappatoires : **`references/fast-track.md`**.

---

## Agents spécialisés

Chaque agent est un **contrat** : un rôle, une liste d'inputs, une procédure, un format de sortie, et une liste explicite de ce qu'il ne fait pas. Ce n'est pas une description de rôle — c'est ce qui rend la délégation possible.

| Agent | Phase | Modes | Rôle |
|---|---|---|---|
| `product-analyst` | 1, 2 | produce, review | Discovery, interviews, PRD, user stories |
| `scope-architect` | 2 | produce, review | Roadmap, MVP, découpage en versions, compromis |
| `ux-designer` | 3 | produce, review | Standards, direction visuelle, navigation priorisée, écrans, flows |
| `systems-architect` | 4 | produce, review | Architecture, slices, modules, données, API, dépendances |
| `quality-analyst` | 1–8 | produce, **validate** | Exhaustivité, edge cases, plans de test ; validateur Fast Track |
| `red-team` | 1–8 | **validate** | Contradictions, angles morts, hypothèses non vérifiées |
| `plan-validator` | 4, 5 | **validate** | Conformité aux standards de l'archétype d'application |
| `premise-challenger` | 1–4 | **challenge** | **Met en cause les hypothèses de l'utilisateur** — idée de départ, fonctionnalités demandées, MVP |
| `scenario-tester` | 6–8 | produce, review | Tests par scénario métier : cycles de vie, horloge, invariants |
| `forge-implementer` | 7, 8 | produce | Implémentation, TDD, validation |
| `client-liaison` | 0, 4, 5, 7, 8 | **check, stress** | **Ce que le client ne comprendra pas** — questions sans réponse, pas de verdict |

`premise-challenger` est le seul agent qui ne relit pas les documents de Forge : il relit **ce que vous voulez**, et il dit quand une idée est mauvaise, déjà résolue, disproportionnée ou mal placée. Il est déclenché à la fin des Phases 1, 2 et 3, et **systématiquement** quand vous ajoutez une fonctionnalité en cours de route. Un seul verdict `critical` bloque jusqu'à votre réponse.

### `client-liaison` — le seul agent qui parle au client

Les dix autres sont des ingénieurs : ils cherchent ce qui est **faux**, **incomplet** ou
**non testable**. `client-liaison` cherche ce qui est **incompréhensible**, et c'est un
métier distinct. Un document peut être parfaitement correct et illisible pour son
destinataire — et aucun des dix autres ne le verra jamais, parce qu'ils lisent tous la
langue de son auteur.

| Mode | Question | Sortie |
|---|---|---|
| `check` | Ce client peut-il signer sans poser de question ? | les questions auxquelles le document ne répond pas |
| `stress` | Que dirait un client informé, et que Forge n'a pas écrit ? | l'objection principale, et le prix du silence |

**Il ne rend jamais de verdict.** Un sous-agent qui approuve remplace le client par un
faux client, et le gate devient auto-certifié — la faute la plus coûteuse possible ici,
parce qu'elle ne se voit pas. Il rend des **questions** ; le client décide.

Il ne lit ni le code, ni les plans, ni l'architecture. Cette restriction n'est pas une
précaution : c'est son métier. Un document client écrit par quelqu'un qui a lu
l'architecture contient **toujours** de l'architecture. Sa valeur est entièrement dans le
fait qu'il ne l'a pas lue.

À utiliser sur le **contrat** (Phase 0), sur chaque **bilan d'écart**, et sur le point
d'étape qui précède l'implémentation.

**Sans sous-agents disponibles** : charge les instructions de l'agent pertinent pour la phase en cours et applique la rotation de posture. Fast Track n'est alors **pas disponible** — c'est le mode Guided qui prend le relais.

---

## Audit — améliorer Forge à partir de ses propres exécutions

Chaque exécution de Forge journalise dans `.forge/audit/` :

| Fichier | Nature | Usage |
|---|---|---|
| `run-log.jsonl` | Machine, append-only | Tous les événements : transitions, gates, validateurs, garde-fous, incidents |
| `issues.md` | Humain | Le journal d'incidents : symptôme, cause racine, contournement, action corrective |
| `metrics.json` | Machine | Compteurs agrégés |

**Un incident qui n'est pas écrit n'a pas eu lieu.** C'est la seule donnée qui permette d'améliorer le skill.

### Ce qui doit être journalisé

```bash
node "$FORGE/scripts/state.js" log <anchor> <type> "<message>" [k=v ...]
```

Types à déclencher impérativement :

| Situation | Type |
|---|---|
| Un sous-agent renvoie `REVISE` | `fast_track_validate` |
| Un sous-agent renvoie `BLOCK` | `fast_track_block` |
| L'utilisateur corrige une sortie (« non, ce n'est pas ça ») | `user_correction` |
| Un garde-fou échoue | `guard_failure` |
| Un script échoue | `script_failure` |
| Une divergence d'état est détectée | (automatique via `sync`) |
| Un livrable est trouvé hors de `.forge` | (automatique via `strays --relocate`) |
| Une phase doit être reprise | `phase_retry` |
| Un gate humain est rejeté | `gate_revise` |
| L'utilisateur quitte Fast Track | `fast_track_escape` |

**L'onglet `origine`** dans `issues.md` (`forge` / `projet` / `environnement`) est le champ le plus important : c'est lui qui distingue « Forge a mal guidé » de « le PRD était ambigu ».

### Analyse inter-projets

```bash
node "$FORGE/scripts/audit-report.js" <dossier-contenant-les-projets> --out reports/
```

Fusionne les journaux de plusieurs projets, regroupe les défaillances par **signature normalisée**, et distingue les problèmes **structurels** (présents dans plusieurs projets → dans le skill) des incidents ponctuels (dans un projet). Sort en `0` normally, en `2` si un problème structurel est détecté.

---

## Discipline de vérification

> Ces règles ne sont pas des préférences. Ce sont les conclusions de 43 corrections accumulées sur un projet réel, dont **les 43 étaient des erreurs de vérification, pas de connaissance** — l'agent savait, ce qui manquait était l'étape qui applique le savoir au fichier réel.
>
> Elles sont ici parce qu'elles n'ont jamais été promues. Un constat qui n'atteint pas une règle n'a rien changé.

1. **Une affirmation coûte l'exécution qui la vérifie.** « Il n'existe aucun code qui fait X » est une affirmation sur le système, et elle mérite la même rigueur que « le code fait X ». Lire le bloc entier, ou ne rien affirmer.

2. **Un code de sortie n'est pas un résultat.** Une commande peut sortir 0 en ayant été ignorée. Un drapeau déprécié retiré en silence, un `replace` sans occurrence : les deux ont produit un faux vert.

3. **Un contrôle qui vérifie la PRÉSENCE d'un changement ne peut pas vérifier son CONTENU.** Une porte qui prouve qu'un fichier a été modifié prouve qu'il a été modifié, pas qu'il dit vrai.

4. **Un contrôle qui ne sait voir que ce qui a changé ne peut jamais détecter ce qui a été oublié.** `git status` montre ce qui a changé ; un fichier non mis à jour lui est indiscernable d'un fichier à jour.

5. **Un test qui réimplémente la règle qu'il est censé tester ne teste pas la règle, il teste sa copie.** Et il passe.

6. **Un test qui passe pour la mauvaise raison est pire qu'un échec.** Il occupe la place du test qui aurait trouvé le vrai défaut.

7. **Un test qui ne touche pas la ligne fautive n'est pas une couverture.** « La règle est écrite » ne vaut pas « la règle est branchée ».

8. **Un attendu est un énoncé, pas une invention.** L'écrire comme une question posée sur les données du test, puis y répondre. Un attendu calculé par le même code que le code testé ne vérifie rien.

9. **Un invariant doit avoir une forme.** Une symétrie se *suppose* ; un invariant se démontre. Si la seule façon de l'écrire est « sauf si », c'est qu'il n'en a pas.

10. **Un fait, deux représentations.** Deux endroits calculent la même chose, aucun ne réconcilie. Le jour où ils divergent, personne ne sait lequel a raison. Extraire une fonction canonique — jamais deux sites.

11. **Une frontière sans deux tests n'est pas une frontière.** Un test qui n'emprunte que le chemin nominal ne vérifie rien du reste.

12. **Une règle qu'on ne peut pas documenter est une règle qu'on supprime.** Et une règle qu'on ne peut pas **exécuter** est une décoration.

13. **Un constat sans domaine est incomplet.** Il n'a pas de cible de promotion, donc il ne change rien.

14. **Un constat qui n'atteint jamais un fichier de règles n'a rien changé.** Il est lu *à la place* de la règle, pas *en plus*.

---

## Références

### Scripts — déterministes, zéro dépendance

Invocation : `node "$FORGE/scripts/<fichier>" [<anchor>] [args…]`. `$FORGE` est le
dossier du skill, voir « Comment exécuter les scripts » plus haut.

**Une seule exception, et elle est explicite** : `ddl-exec.js` charge un moteur
PostgreSQL (`@electric-sql/pglite`) pour **exécuter** le DDL. Ce moteur est une
*dépendance de développement du dépôt*, jamais du skill distribué. Sans lui, le
script ne simule rien : il rend `skipped`, dit ce qu'il n'a pas fait, et donne la
ligne à installer. Un contrôle qui prétend avoir exécuté sans avoir exécuté est
le pire des contrôles, parce qu'il donne un vert.

| Script | Rôle | Quand |
|---|---|---|
| `state.js start` | État réel : phase, gates, slices **avec nombre de cas de test**, constats non promus | **Étape 0, chaque session** |
| `state.js anchor` | Résout le projet courant, refuse un projet de référence | Étape 0 bis |
| `state.js finding` | Route un constat avec son **domaine** de promotion | Dès qu'un défaut est trouvé |
| `state.js set-status` | Écrit l'**autorité** et son **miroir** en une opération | Chaque changement de statut |
| `state.js sync` | Réconcile état ↔ front matter | Avant chaque gate |
| `state.js set-nav` | Enregistre l'ordre de navigation et sa justification | Phase 3 |
| `state.js check-stale` | Document dérivé, ou plan modifié après approbation | Avant d'implémenter |
| `state.js dep` | Déclare le graphe de dépendances d'une slice ou d'une fondation | Phase 4 |
| `state.js amend` | Enregistre un amendement et **refuse le renumérotage** ; écrit `amended_from`, la raison, la liste des changements | Chaque amendment |
| `state.js migrate` | v1 → v2 | Un projet existant |
| `forge-guard.js all` | Chemins, état, vocabulaire, synchronisation, **provenance `derived_from`**, **artefacts produits en avance**, **caractères parasites**, cases « À DÉCIDER », placeholders, versions, **mémoire du projet**, **intégrité du kit**, **outils déclarés**, **incidents non consignés** | **Avant chaque gate** |
| `forge-guard.js memory-present` | Les quatre fichiers de mémoire existent, et `AGENTS.md` nomme chacun des trois **avec un déclencheur** | Phase 0, puis à chaque gate |
| `forge-guard.js kit-integrity` | Les scripts du kit correspondent à leur empreinte enregistrée ; **un script modifié est un échec dur**, un document un avertissement | **Avant chaque gate** |
| `forge-guard.js kit-integrity --write-manifest` | Écrit `.forge/kit-manifest.json` — **acte explicite**, jamais automatique | Une fois, et après chaque mise à jour du kit |
| `forge-guard.js tools` | Tout script complémentaire est dans `.forge/tools/` **et déclaré** avec son but | Avant chaque gate |
| `forge-guard.js incidents` | Un écart détecté par une porte est consigné dans `.forge/audit/issues.md` | Avant chaque gate |
| `consistency-check.js all` | Écarts **entre** artefacts : PRD ↔ archi ↔ plans ↔ tests ↔ écrans, et **renvois de section résolus** | **Avant chaque gate** |
| `forge-exit.js` | Critère de sortie **exécuté** d'une slice | **Phase 7, par slice** |
| `coverage-check.js` | Couverture d'un plan de slice | Phase 5 |
| `design-check.js` | **Mesure** contrastes (WCAG 1.4.3 / 1.4.11), tokens sans valeur, et **parité de surface** entre composant et écrans | **Phase 3, au gate** |
| `ddl-exec.js` | **Exécute** le DDL de l'architecture : PostgreSQL le refuse, ou pas. Vérifie que le DDL crée les tables qu'il modifie, et que les gardes **déclarées** tiennent | **Phase 4, au gate** |
| `dependency-check.js` | Cycles, ordre topologique ; `--write` persiste le graphe | Phase 4 |
| `audit-report.js` | Analyse croisée de plusieurs projets | Après plusieurs projets |
| `selftest` | Tests du skill lui-même | Avant toute publication |

### Un contrôle n'est pas validé tant qu'on ne l'a pas vu échouer

**Tout contrôle ajouté ou modifié doit casser, dans le même lot, un défaut
qu'il prétend chercher** — et laisser passer un témoin propre. Les deux.

Ce n'est pas une précaution de forme. Constaté deux fois sur un même projet :
un scan `Get-Content -Raw` + regex `\u` en PowerShell a déclaré « 0 problème »
sur des fichiers corrompus ; le scan Node qui l'a remplacé, conçu sur l'hypothèse
« la corruption est CJK », a déclaré propre un fichier contenant `U+1EE1` dans
`_USERNAMEOục` — Latin Extended Additional. Le troisième parasite n'a été trouvé
qu'en passant par une **liste blanche**.

Trois règles qui en découlent :

1. **Liste blanche, pas liste de suspects.** Autorisé = ASCII + Latin-1 +
   Latin Extended-A + ponctuation + symboles + emoji + la typographie de la
   langue du dépôt (ordinaux `1ᵉʳ`, indices `CO₂`). **Tout le reste est
   signalé.** Le premier essai de cette liste signalait 28 fois des ordinaux
   français corrects : une liste blanche qui ne couvre pas la langue du dépôt
   devient un contrôle que l'on éteint.
2. **Une ligne marquée `unicode-scan:ignore` est ignorée**, pour citer un
   défaut dans un journal sans que la citation se déclenche. Sans cela, le
   rapport qui prouve le défaut ne peut pas être commité.
3. **`skip` ≠ `pass`.** Un contrôle qui ne s'exécute pas annonce ce qu'il n'a
   pas couvert. Un contrôle jamais vu échouer n'est pas validé, il est inconnu.

Et pour les contrôles dont l'entrée est un **fichier produit** : ils doivent
être vérifiés sur le projet réel avant d'être branchés sur `all`. Un contrôle
piloté reste accessible par commande, hors de `all`.

## Documents de référence

| Fichier | Contenu |
|---|---|
| `references/skill-boundaries.md` | **Qui possède quoi** entre Forge et `project-rules-architect` ; routage des constats |
| `references/state-schema.md` | Format de `.forge/state.json` (v2), règles d'écriture, qui fait foi |
| `references/migration-v1-v2.md` | Procédure de migration d'un `state.json` v1 surchargé |
| `references/module-prioritization.md` | Ordonnancement des modules et de la navigation par fréquence d'usage |
| `references/design-quality.md` | Interdits anti-générique, skills de design obligatoires, direction visuelle |
| `references/scenario-tests.md` | **Tests par scénario métier** — cycles de vie, horloge injectée, invariants |
| `references/test-strategies.md` | Les familles de tests, comment choisir, ce qui tourne sans appareil |
| `references/archetypes.md` | Standards par archétype + **pathologies récurrentes** mesurées |
| `references/research-protocol.md` | Ne pas réinventer : extraire des invariants, pas du code |
| `references/fast-track.md` | Validation automatique, deux niveaux d'autonomie, limites |
| `references/impact-protocol.md` | Protocole d'analyse d'impact des changements |
| `references/review-checklists.md` | Checklists de gate par type de document |

L'interview produit est documentée dans `agents/product-analyst.md`.

---

## Résumé du workflow

```
anchor → Interview (Phase 1) → PRD → Roadmap (Phase 2)
  → Standards + Direction + Navigation priorisée + Design (Phase 3)
  → Architecture (Phase 4) → Plans d'implémentation (Phase 5) → Tests (Phase 6)
  → Implémentation (Phase 7) → Validation (Phase 8)
```

Avec, tout au long :

```
Anchor résolu · Livrables dans .forge · État = autorité, front matter = miroir
Gates humains (ou Fast Track) · Analyse d'impact · Multi-perspective
Identifiants stables · Exhaustivité · Garde-fous déterministes · Audit
```
