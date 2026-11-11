---
name: setup-po-skills
description: Connect this machine to the PO hub in Notion and mirror the team's repos, creating the hub and its databases (Domaines, Glossaire, Sources, Projets, PRD) if none exists yet. Run once per PO, and again to bring an outdated hub up to date.
disable-model-invocation: true
---

# Setup PO skills

Point this machine at the **PO hub**: the Notion page holding the `Domaines`, `Glossaire`, `Sources`, `Projets` and `PRD` databases that the PO skills read and write. Join an existing hub, or create one when the team has none yet. Then mirror the team's repos on this machine.

Write in French: every message to the user and everything written to Notion.

## Process

### 1. Check the Notion connection

Confirm a Notion MCP server is connected and can search the workspace. If it isn't, stop and tell the user to connect it. Done when a workspace search returns results.

### 2. Ask for the hub

Ask: « Est-ce qu'un autre PO a déjà configuré la page PO dans Notion ? Si oui, colle son lien ici. »

- **A link** → step 3.
- **No hub yet** → step 4.

### 3. Join an existing hub

Open the page and find the five databases among its children. If the page won't open, tell the user they need access to it and stop there: a PO without access must be given access, never a second hub.

Compare each database with [SCHEMAS.md](./SCHEMAS.md). For a missing database, a missing property, or a select option SCHEMAS.md lists that the property lacks (for example `Abandonné` on `PRD.Statut`), show the gap and ask whether to add what's missing; existing properties and options stay as they are.

Compare the page body with the **hub guide** in [HUB-PAGE.md](./HUB-PAGE.md), heading by heading, its `<url du repo po-skills>` placeholder filled as that file says. Show the user every gap in one message:

- **Missing**: a heading of the guide absent from the page, or the whole guide.
- **Outdated**: a section whose text differs from HUB-PAGE.md. The difference may be the team's own edit, so show both versions.

Write what the user accepts: each missing section at its place in the guide's order, above the databases, and each accepted outdated section replaced by HUB-PAGE.md's text. Leave the rest of the page as it is.

Done when all five databases are found and match SCHEMAS.md, and every section of the hub guide is on the page and matches HUB-PAGE.md, or the user declined the changes. Go to step 5.

### 4. Create a new hub

First guard against a hub the user can't see: search the workspace for databases named `Domaines`, `Glossaire`, `Sources`, `Projets`, `PRD`. If any turn up, show where they live and ask whether one of those pages is the team's hub; if it is, go to step 3 with it.

Otherwise, ask in one message:

- the page to use as the hub (an existing empty page, or where to create one)
- the initial domains, each with a one-line description and how it relates to the others (seed the `Transverse` row yourself; reuse a domain that already exists under the same `Nom`)

Create the five databases under the hub in the order SCHEMAS.md gives, with every property and select option it lists, then the domain rows. Then write the **hub guide** from [HUB-PAGE.md](./HUB-PAGE.md) into the page body, above the databases.

### 5. Record the hub

Write the hub to `~/.po-skills/config.md`, creating the folder if needed:

```md
# PO skills

Page PO : <nom de la page> — <url de la page>
```

Overwrite an existing file only after showing the user the hub it currently points to and getting their confirmation.

### 6. Import sources and projects

Ask whether the user has business-rules docs or repos to add. If so, invoke `po-add-source` with them.

### 7. Mirror the projects

For every `Projets` row not yet mirrored, invoke `po-repos` to clone its mirror (`po-add-source` already mirrored the projects it just added), then ask it to prune. Projects added later get their mirror the first time a skill needs them.

Done when every project is mirrored or reported inaccessible with its reason. An inaccessible project leaves setup running: only questions about how the product behaves today need it.

### 8. Done

Done when the config file names the hub, the five databases under it match SCHEMAS.md, the hub guide on the page matches HUB-PAGE.md (or the user declined the changes), and the projects are mirrored. Give the user the hub URL, the projects still inaccessible with what to fix (usually git sign-in to the repo's host), and the next step: `/po-grill`, with `/po-ask` for any question about which skill to run.
