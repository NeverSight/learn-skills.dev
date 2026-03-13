---
name: create-new-wiki-page
description: Create a new Azure DevOps wiki page. Use when the user wants to add a new wiki page, write project documentation in Azure DevOps wiki format, or update wiki page structure with mermaid diagrams in Traditional Chinese.
metadata:
  original-prompt: create-new-wiki-page.prompt.md
  wiki-language: 正體中文
---

# Create New Wiki Page

Create a new Azure DevOps wiki page with proper structure and formatting.

## Steps

1. Execute `tree . /f` in pwsh to get all the page lists.

2. Read all docs under `設計文件`, `功能需求`, `標準規範` or other documents to get the full view of the project.

3. Plan the content for the wiki page about the user's specified topic. ${input:what-to-write-in-this-page}.

4. Include a mermaid diagram on the page if there is suitable content for it.

5. If the user doesn't specify a location, find an appropriate category and path for this page.

6. Write the page in 正體中文.

7. Add this page to the `.order` file in the same directory.

8. Add this page to the category's markdown file (e.g., if under `標準規範/`, update `標準規範.md`).

9. Review whether the Azure DevOps Wiki page is well-written; refine it to improve quality.

10. Git commit with a good message body.

11. Summarize what was done.

## Wiki Writing Guidelines

- Write in simple, concise language.
- Follow a consistent format across all pages.
- Break up sections with headlines, subheads, and text boxes.
- Enrich pages with mermaid diagrams and links.
- Include a list of FAQs in each section.
