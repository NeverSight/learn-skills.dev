---
name: po-glossary
description: Build and sharpen the product Glossaire in Notion. Use when a product term needs settling, or when editing the Glossaire or its domains.
---

# Product glossary

Actively build and sharpen the product language while the PO designs: challenge terms, invent edge-case scenarios, and write each term to the Glossaire the moment it is resolved.

The PO databases live under the **PO hub** page named in `~/.po-skills/config.md`; when the file is missing, stop and tell the user to run `/setup-po-skills`.

Write in French: every message to the user and everything written to Notion.

## Before the first question

Read the `Domaines` database: it is the glossary map, one row per domain with what it covers and how it relates to the others. Infer the topic's domain from the PRD's `Domaine` when one exists, or else from the PO's opening pitch; when two fit, take both. Then read every Glossaire entry in that domain and in the domains listed under its `Domaines liés`.

When the grill later settles a different `Domaine`, read that domain's terms and its neighbours' the same way.

Done when you hold the terms of the topic's domain and its neighbours.

## During the session

### Challenge against the Glossaire

When the PO uses a term that clashes with an entry, say so immediately: « Le Glossaire définit "Mandataire" comme X, mais tu sembles parler de Y. Lequel ? » A word listed under an entry's `À éviter` gets the same treatment.

### Sharpen fuzzy language

When a term is vague or overloaded, propose one precise term: « Quand tu dis "compte", tu parles du Compte pro ou de l'Utilisateur ? Ce sont deux choses différentes. »

### Discuss concrete scenarios

Stress-test relationships between concepts with specific scenarios that probe the edges, until the PO is precise about where one concept ends and the next begins.

### Write to the Glossaire inline

When a term is resolved, write it right there:

1. Re-fetch the entry if it exists. Another PO may have edited it since you read it; if it changed, show the PO the difference and settle it before writing.
2. Create or update the entry in the format below.
3. Link it to the PRD draft through the draft's `Termes` relation.

### New domains

When a term belongs to no existing domain, propose a new one to the PO. Once confirmed, add a `Domaines` row with its description and relations, then update `Relations` and `Domaines liés` on the domains it touches.

## Entry format

- **Terme**: the one word to use, singular. When several words name the same concept, pick the best one and move the others to `À éviter`.
- **Définition**: one or two sentences saying what the thing *is*. A constraint on it (thresholds, deadlines, who may do what) belongs in the PRD or the Sources.
- **À éviter**: retired synonyms, comma-separated.
- **Termes liés**, **Domaine**: set both.

Add a term only when it is specific to the product: a concept the business defines, not an everyday word used in its everyday sense.

```
Terme       : Mandataire
Définition  : Personne autorisée par le Titulaire à agir sur son compte, sans en être responsable légalement.
À éviter    : délégué, utilisateur secondaire, invité
Termes liés : Titulaire, Compte pro
Domaine     : Comptes
```
