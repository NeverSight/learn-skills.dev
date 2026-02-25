---
name: strategic-doctrine-deployment
description: A workflow for deploying strategic documents (e.g., funding plans, architectural overviews) into a version-controlled repository, generating a presentation, and syncing all artifacts to GitHub and Google Drive. Use when a user provides a doctrinal document and asks for it to be processed, deployed, or presented.
---

# Strategic Doctrine Deployment

This skill codifies the workflow for taking a high-level strategic document, integrating it into a version-controlled system, generating a tactical presentation, and ensuring all artifacts are synced across GitHub and Google Drive.

## Core Workflow

The process follows these five phases:

1.  **Integrate Doctrine:** The source document is copied into the `docs/` directory of the target repository.
2.  **Generate Presentation:** A slide deck and speaker script are generated from the document's content.
3.  **Commit & Push:** All new artifacts (document, presentation, script) are committed and pushed to the GitHub repository.
4.  **Sync to Cloud:** All artifacts are synced to the corresponding Google Drive folder.
5.  **Report to User:** A summary of the deployment, including links to the live assets, is delivered.

## 1. Integrate Doctrine

-   **Input:** A user-provided document (e.g., from a file attachment).
-   **Action:** Copy the document into the `/home/ubuntu/agi-rollout-pack/docs/` directory.
-   **Naming Convention:** Use an uppercase, snake-cased name that reflects the document's purpose (e.g., `EMERGENCY_FUNDING_VORTEX.md`).

```bash
# Example
cp /home/ubuntu/upload/pasted_content.txt /home/ubuntu/agi-rollout-pack/docs/STRATEGIC_PLAN.md
```

## 2. Generate Presentation

This is a multi-step process that leverages the `presentation-workflow` skill. If you have not already, read `/home/ubuntu/skills/presentation-workflow/SKILL.md`.

### 2.1. Create Presentation Outline & Script

-   Read the source document from the `docs/` directory.
-   Create a new Markdown file in `presentations/` named `{document_name}_slides.md`.
-   In this file, write a complete slide-by-slide outline and a full speaker script for each slide. See the template in `templates/presentation_script_template.md`.

### 2.2. Initialize the Slide Deck

-   Use the `slide_initialize` tool to create the presentation project directory.
-   The `project_dir` should be `presentations/{document_name}`.
-   Use the outline created in the previous step.

### 2.3. Edit the Slides

-   Use the `slide_edit` tool to create the HTML for each slide, following the content from your script.
-   Adhere to the established visual style: dark background, high-contrast text (Inter/JetBrains Mono), and red accents (`#FF3333`).

### 2.4. Present the Slides

-   Use the `slide_present` tool to generate the final presentation output.

## 3. Commit & Push to GitHub

-   Authenticate with the GitHub CLI using the stored PAT.
-   Stage all new files in the `docs/` and `presentations/` directories.
-   Create a commit with a descriptive message.
-   Push to the `master` branch of the `Andy160675/agi-rollout-pack` repository.

```bash
# Example Commit
cd /home/ubuntu/agi-rollout-pack && \
git add docs/STRATEGIC_PLAN.md presentations/strategic_plan* && \
git commit -m "Deploy strategic plan: STRATEGIC_PLAN.md" && \
echo "ghp_..." | gh auth login --with-token && \
git push origin master
```

## 4. Sync to Google Drive

-   Use `rclone` to copy the updated `docs/` and `presentations/` directories to the `agi-rollout-pack` folder on Google Drive.

```bash
# Example Sync
rclone copy /home/ubuntu/agi-rollout-pack/docs/ manus_google_drive:agi-rollout-pack/docs/
rclone copy /home/ubuntu/agi-rollout-pack/presentations/ manus_google_drive:agi-rollout-pack/presentations/
```

## 5. Report to User

-   Deliver a final summary message to the user.
-   Attach the generated presentation (`manus-slides://...`), the speaker script (`.md`), and the original source document (`.md`).
-   Include the Git commit hash and a summary of the deployed assets.
