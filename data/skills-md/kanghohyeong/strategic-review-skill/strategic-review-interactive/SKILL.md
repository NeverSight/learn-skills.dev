---
name: strategic-review-interactive
description: This skill supports the strategic review process through a web interface.
disable-model-invocation: true
---

# Strategic Review Interactive Skill

## Instructions

### Step 1: Retrieve Report

* Ask the user to enter the filename of the strategic report.
* If the report does not exist, return an error message to the user.
* Verify that the report is saved in markdown format. If not, return an error message to the user.

### Step 2: Check Status

* Check the status of the report included in the frontmatter of the markdown file.


### Step 3: Act Based on Report Status

* **init** : Write the report.
  - Follow the instructions in `interactions/init.md`.

* **submit** : Guide the user to review the report through the web interface.

* **approve** : Summarize and present the approved results to the user, and inform them that work is ready to begin.
  - Follow the instructions in `interactions/approve.md`.

* **reject** : Summarize and present the rejection reasons to the user.

* **revision** : Rewrite the report.
  - Follow the instructions in `interactions/revision.md`.

* **Other** : Inform the user of an unknown status and guide them to check the report status.
