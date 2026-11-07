---
name: fortify-create-app
description: "Create new Fortify application(s) in Fortify on Demand (FoD) or Application Security Center (SSC)."
license: MIT
metadata:
  version: "1.0.3"
  tested-with:
    fcli: "3.23"
    fod: "26.2"
    ssc: "26.2"
---

Creating an app is a 3-step process. Work through steps in order — each step has a clear entry condition and output that feeds the next.

> **Stay within the documented workflow.** Do not proactively offer side-quests or capabilities that aren't part of the step you're in. If a step in this skill calls for it, do it; if not, don't surface it as an option. Eager suggestions waste the user's attention and lead them off the remediation path.

> Use the `fortify-ssc` or `fortify-fod` skill to create new releases or application versions for existing applications.

---

## Step 0: Determine Fortify platform

Fortify on Demand (FoD) vs Software Security Center (SSC). If the user did not specify, run both session checks to determine which platform is active:

```bash
fcli fod session ls --query "expired=='No'"
fcli ssc session ls --query "expired=='No'"
```

- If only a FoD session is active → platform is FoD.
- If only an SSC session is active → platform is SSC.
- If both are active → ask the user which platform they want to use.
- If neither is active → ask the user which platform they are using and prompt them to create an fcli session with FoD or SSC.

**fcli not found:** You interact with Fortify using `fcli`. It must already be on the PATH. If it is not installed, load `references/fcli-install.md`.

Step 0 → Step 1 gate
- [ ] Platform identified and session verified

## Step 1: Determine application and initial release/versionname

### Step 1a: Identify the application name
If the user provided an explicit name for both the application and release/version, move on to Step 1b. If not, load `reference/naming-conventions.md` to determine the application and release/version names.

### Step 1b: Verify application does not already exist
Use the one of following commands to check if the application already exists in the selected platform:

```bash
fcli fod app list --query "applicationName=='<name>'" -o json
fcli ssc app list --query "name=='<name>'" -o json
```

Step 1 → Step 2 gate
 Application and initial release/version names identified
 Application does not already exist

## Step 2: Create the application

Load the reference file for your platform and follow it to create the application and initial version/release. The reference file covers naming convention inspection, idempotency checks, standard vs. microservice app paths (FoD), required attribute handling, and the pre-creation checklist.

- **FoD**: load `references/fod-create-app.md`
- **SSC**: load `references/ssc-create-app.md`

Step 2 → Completion gate
 Application created successfully

## Cross-Skill Dependencies
- `fcli-common` — used for fcli installation checks and any shared fcli logic