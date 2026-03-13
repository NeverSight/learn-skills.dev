---
name: flutter-triage
description: Use this skill to gather relevant PRs and issues for a specified team in Flutter.
---

# Flutter Triage

This skill guides the agent in locating relevant PRs and issues for a specified
team in Flutter and outputting them in a nicely formatted markdown file.

## Prerequisites
Before using this skill, ensure the following:
1.  The `requests` python library is installed (`pip install requests`).
2.  The `GITHUB_TOKEN` environment variable is set with a valid GitHub Personal Access Token with `repo` scope.

## Workflow

### 1. Ask for Team Name
Start by asking the user which team they would like to triage for (e.g., "Framework", "Engine", "Design Languages").

### 2. Fetch and Parse the Triage README
Once the user provides a team name:
1.  Load the triage README from the main Flutter repository, located at:
    `https://raw.githubusercontent.com/flutter/flutter/master/docs/triage/README.md`.
2.  Use the `scripts/parse_triage_readme.py` script with the provided team name to find the team's section and extract the URLs for their triage lists.
3.  If no lists are found, inform the user. Otherwise, proceed to the next step.

### 3. Generate and output lists of PRs and issues via GitHub API

For each list name and URL extracted in the previous step:
1.  **Convert to API URL:** Transform the web URL into a GitHub API URL.
    - **`https://github.com/`** becomes **`https://api.github.com/repos/`**.
    - The query parameters (`?q=...`) from the web URL should be used with the `search/issues` endpoint of the GitHub API.
    - **Example:** `https://github.com/flutter/flutter/issues?q=...` becomes `https://api.github.com/search/issues?q=repo:flutter/flutter...`
2.  **Fetch Data with Pagination:**
    - Create a temporary directory to store the paginated results for the current list.
    - Use `curl -i` with the `Accept: application/vnd.github.v3+json` header to fetch the first page of JSON data. Save the output (including headers) to a file.
    - Inspect the `Link` header in the output file. If there is a `rel="next"` link, extract the URL for the next page.
    - Continue fetching pages until there are no more "next" links. Save each page's JSON response to a separate file in the temporary directory, named `page_1.json`, `page_2.json`, etc.
3.  **Combine and Parse:**
    - Use the `scripts/combine_json.py <input_directory> <output_file>` script to combine the `items` from all pages into a single JSON file. The `<input_directory>` should be the temporary directory you created in the previous step.
    - Use the `scripts/parse_api_response.py <input_json_file> <output_json_file>` script to parse the combined JSON file and fetch additional context (issue body and comments). This script will output a new JSON file with all the data.

### 4. Combine all parsed JSON files
After all the lists have been processed, use the `scripts/combine_all.py` script to combine all the parsed JSON files into a single file named `combined_triage.json` in the temporary directory.

### 5. Summarize and Format Output

After running `combine_all.py`, the agent will have a single JSON file with all the data. The agent will then use the `scripts/generate_report.py` script to generate the final markdown report.

The final output should be a single markdown file in the `flutter-triage/output/` directory, named after the team and the date (e.g., `framework-20260310.md`). This file will contain a section for each triage list found in the README, with the generated summary and action items for each issue/PR. Include the date in the top heading of the file.
