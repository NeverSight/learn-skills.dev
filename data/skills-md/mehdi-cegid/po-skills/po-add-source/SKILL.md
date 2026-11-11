---
name: po-add-source
description: Add business-rules docs (Sources) or git repos (Projets) to the PO hub in Notion, mapping their domains and overlaps. Use when a PO wants to register a doc or a repo, or accepts a « Hors registre » source from po-research.
---

Add documents to the `Sources` database and git repos to the `Projets` database: the two registries `po-research` answers from. Each new **entry**, a document or a project, goes through **discovery**: it is placed against the existing registries and domains before it is written, and a short grill settles what discovery couldn't.

The PO databases live under the **PO hub** page named in `~/.po-skills/config.md`; when the file is missing, stop and tell the user to run `/setup-po-skills`.

Write in French: every message to the user and everything written to Notion.

When invoked during a `po-grill` session, run the same discovery, and put your questions into the grill's next round instead of opening a separate session.

## Process

### 1. Collect the URLs

Take the URLs from the user's message or from the caller, with whatever the user already said about each. With no URL, ask for them.

### 2. Read each new entry

A git repo URL, on any git host, is a **project**; anything else is a **document**. Reduce each project link to its repo URL before comparing or storing it: drop browser suffixes such as `/tree/<branche>` or `/blob/…` and a trailing `.git`; on Azure Repos, keep `https://dev.azure.com/<org>/<projet>/_git/<dépôt>`.

- **Already registered** (same `URL` in `Sources`, same `Dépôt` in `Projets`) → skip it and list it as « déjà présente ».
- **Document that opens** → read it in full and note what it covers: its topics, the rules it states (with their numbers and conditions), and who it is for.
- **Project** → invoke `po-repos` with its `Dépôt` and the repo's name as `Nom`; with no `Branche de référence` yet, it mirrors the remote's default branch until the user confirms one. Read its README, top-level layout, and `GLOSSARY.md` or `GLOSSARY-MAP.md` when present, and note what it does and which parts of the product it implements.
- **Won't open** → record the reason (no access, 404, login required, git sign-in missing). Keep it in the batch: a registered entry research can't open gets reported at every grill until someone fixes the access. What it covers must then come from the user.

Done when every URL is classified.

### 3. Discover

Read the `Domaines` database, then every `Sources` and `Projets` row in the domains the new entries might touch and in `Transverse`.

For **every entry**:

- **Domains**: every domain it touches. When none fits, draft a **new domain**: name, description, and its relations to existing domains.

For **documents** only, open each existing document whose `Description` shares a topic with a new one, and compare their content; compare the new documents with each other the same way. Look for:

- **Overlap**: an existing document covering the same topic. Note what they share.
- **Contradiction**: an overlapping document stating a different rule. Quote both, with their sections.
- **Summary**: one document restating another, like a FAQ restating a policy. The restating one is usually `Informatif`.
- **Replacement**: a new document that is a newer version of an existing one.

A project's discovery stops at its domains: duplicates were caught in step 2.

Done when every new entry has its domains drafted, and every document sharing a topic, existing or new, is opened (or recorded as inaccessible) and compared.

### 4. Grill the findings

Settle the findings with the user in **rounds**: number each question, give your recommended answer, and word it so « oui » accepts it. Wait for the answers, then ask what they unblocked. Grill only on the findings and the missing fields:

- the `Domaine`s of each new entry, and any new domain
- each new document's `Autorité`, with your reason
- each project's `Description` and `Branche de référence` (the branch matching production)
- each overlap and summary to record as `Sources liées`
- each contradiction: which document is right, and who must fix the other. The answer sets their `Autorité`; the wrong doc stays in the registry, and `po-research` keeps flagging the conflict until its `Propriétaire` fixes it
- each replacement: whether to remove the old row
- what's still missing: `Description` for entries that wouldn't open; for documents, `Propriétaire` and `Dernière revue` (propose the doc's last-edited date when visible)

Done when every finding is confirmed or rejected, and every new entry has a `Domaine` (every document an `Autorité`, every project a `Branche de référence`), or the user chose to leave them blank.

### 5. Write

1. New domains first: a `Domaines` row each with its description and relations, then update `Relations` and `Domaines liés` on the domains they touch.
2. One `Sources` row per new document, one `Projets` row per new project (with its `Glossaire projet` path when it has one). `Description` says concretely what the entry covers, in one or two sentences: `po-research` picks documents and projects by reading it.
3. `Sources liées` for every confirmed overlap and summary between documents.
4. `Autorité` changes on existing rows, and removal of replaced rows, as the user decided.
5. When a project's confirmed `Branche de référence` differs from the one mirrored, invoke `po-repos` again for the registered project: it clones the mirror again on that branch.
6. When the caller passed a PRD draft, add the new rows to its `Sources` or `Projets` relation.

### 6. Report

Report the entries added, those « déjà présentes », those that wouldn't open with their reason, the new domains, the links recorded, and each contradiction left to fix with the `Propriétaire` to contact.
