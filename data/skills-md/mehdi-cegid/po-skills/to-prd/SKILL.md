---
name: to-prd
description: Turn the current po-grill session into a French PRD on its Notion draft. No interview, just synthesis.
disable-model-invocation: true
---

Write up the PRD from what this conversation has already settled. Synthesize; the grilling is over.

The PRD's first reader is an agent: the dev grill and `to-spec` read it before any developer does. Write it as documentation for that agent, following the writing rules below.

The PO databases live under the **PO hub** page named in `~/.po-skills/config.md`; when the file is missing, stop and tell the user to run `/setup-po-skills`.

Write in French: every message to the user and everything written to Notion.

## Process

### 1. Find the PRD

Use the PRD this session grilled: a new draft, or an existing PRD the PO resumed. Without one, ask the PO for the PRD's name and `Domaine` and create it in the `PRD` database with `Statut: Brouillon`.

### 2. Write the body

Describe behaviour as the user experiences it; how to build it is for the devs to decide in their own grill.

- **New draft** (empty body): write the template below, applying every writing rule.
- **Resumed PRD** (body already written): edit it in place. Rewrite only what this conversation's decisions change and keep the rest word for word: the devs may have read it already. Move each question the PO answered from `Questions pour le PO` to `Réponses du PO`. A body with a single `Questions ouvertes` section predates the split: sort its questions into `Questions pour le PO` and `Questions pour les devs`.

### 3. Review

Reread what you wrote or changed against the writing rules, one rule at a time, and rewrite what fails. Done when every rule holds for every sentence and user story you wrote or changed.

### 4. Set the properties

- `Termes`: every Glossaire entry the PRD uses.
- `Sources`: every registry source cited in the research notes (`po-research` adds these; check that none are missing).
- `Projets`: every project the research notes cited, and any the PO named.
- `Statut`: `Prêt pour dev` when `Questions pour le PO` lists no question (it reads « Aucune », or holds nothing), whatever the current status. Otherwise keep the current `Statut` and list the remaining questions to the PO.

### 5. Done

Done when every section of the template is filled or reads « Aucun » or « Aucune » to match the section's noun, the review passed, and the properties are set. Give the PO the PRD URL and its `Statut`.

## Writing rules

- **One word per concept.** Name each concept by its Glossaire `Terme`, the same word every time it appears, user stories included. The agent reading the PRD matches words to the Glossaire and the code; a varied word reads as a different concept.
- **Checkable stories.** Each user story ends on an outcome a tester could pass or fail: the number, the state, or the message the actor sees.
- **Limits say what happens.** When a story or rule restricts an actor, state what the actor sees or gets on hitting the limit.
- **Co-located edge cases.** Group the stories under `###` headings by actor or capability, and put each story's edge cases and limits directly beneath it.
- **Link, don't restate.** A term's definition lives in the Glossaire, a rule's text in its Source, a finding in its research note. The PRD carries the decision and the link.
- **Reasons for surprises.** When a decision would surprise a reader (a deliberate limit, a rejected alternative, an exclusion), give its reason in one line: the dev agent can't recover it anywhere else.
- **Every sentence earns its place.** Each one carries a decision, a fact, or a reason.

## Template

```md
## Problème

Le problème, du point de vue de l'utilisateur.

## Solution

La solution, du point de vue de l'utilisateur.

## Récits utilisateurs

Une liste LONGUE, couvrant tous les aspects de la fonctionnalité. Numérotation continue d'un groupe à l'autre, pour que chaque récit garde un numéro unique :

### <Acteur ou capacité>

1. En tant que <acteur>, je veux <fonctionnalité>, afin de <bénéfice>. Résultat attendu : <ce que l'acteur voit ou obtient>.
   - Cas limite : <situation> → <ce qui se passe>
2. …

### <Acteur ou capacité suivante>

3. …

## Hors périmètre

- <ce que ce PRD ne couvre pas> — <pourquoi, quand ce n'est pas évident>

## Termes

| Terme | Nature | Changement |
|---|---|---|
| [<Terme>](<lien Glossaire>) | nouveau / modifié / existant | Pour « modifié » : ce qui a changé |

## Hypothèses à vérifier

Comportements actuels du produit que ni le PO, ni les Sources, ni le code n'ont pu confirmer. Le grilling dev les vérifie dans le code.

- <hypothèse>

## Recherches

Pour chaque note : le constat, puis la décision prise à partir de ce constat.

- [<Recherche : question>](<lien>) — Constat : … → Décision : …

## Questions pour le PO

Ce que le PO, ou la personne indiquée, doit trancher avant le développement. Tant qu'il en reste, le PRD n'est pas `Prêt pour dev`.

- <question> — à qui la poser

## Questions pour les devs

Ce que les devs tranchent ou vérifient dans leur grilling, par exemple un écart règle/code que le PO considère comme un bug.

- <question>

## Réponses du PO

Les questions tranchées par le PO, avec ce qu'elles ont changé dans ce PRD.

- <question> → <réponse> — <récits ou sections modifiés>
```
