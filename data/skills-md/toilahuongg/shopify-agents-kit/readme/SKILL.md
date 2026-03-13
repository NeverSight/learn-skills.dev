---
name: readme
description: Update the project README.md with comprehensive documentation based on the current codebase state. Use when the README needs updating or is outdated.
disable-model-invocation: true
---

# Update README

Update the project README.md with comprehensive documentation.

1. **Analyze Project Structure and State**
   - List the files in the root directory to identify the project type (Node.js, Python, etc.).
   - Read key configuration files if they exist (e.g., `package.json`, `tsconfig.json`, `shopify.app.toml`, `fly.toml`, `requirements.txt`, `Gemfile`, `cargo.toml`).
   - List the contents of valid source directories (e.g., `app/`, `src/`, `lib/`, `components/`) to understand the architecture.

2. **Read Existing Documentation**
   - Read the current `README.md` to preserve any manual sections or specific instructions the user has added.
   - If available, read `.agent/brain/task.md` or `implementation_plan.md` to understand recent changes and current features (optional, do not fail if missing).

3. **Generate/Update README.md**
   - Rewrite `README.md` to include the following sections (adapt as necessary for the project type):
     - **Project Title & Description**: A clear summary of what the project does.
     - **Features**: A list of key features inferred from the codebase and installed packages/skills.
     - **Tech Stack**: Languages, frameworks, and key libraries used.
     - **Prerequisites**: Tools needed to run the project (Node, Python, Docker, etc.).
     - **Getting Started / Installation**: Step-by-step instructions to install dependencies and run the project (e.g., `npm install`, `npm run dev`).
     - **Project Structure**: A high-level overview of the main directories.
     - **Workflows & Skills**: Mention available workflows (like this one) or skills if relevant.
     - **License**: If a license file exists, mention it.

4. **Review and Verification**
   - Ensure the new `README.md` is formatted correctly in Markdown.
   - Check that all links (if any) are valid.
