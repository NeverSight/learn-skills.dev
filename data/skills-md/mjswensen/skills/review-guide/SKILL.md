---
name: review-guide
description: A brief description of what this skill does
---

# review-guide

Generate a beautiful code review guide that illustrates and summarizes the nature of the requested changes (can be unstaged changes, staged changes, commit ID, branch diff, pull request, etc.). Boilerplate code can be ignored. Include the substantive portions of the changes alongside explanations of what they are doing and why. Those portions can be abbreviated to the core concepts if necessary. The output should be a single self-contained interactive HTML file (with JavaScript and CSS embedded inline).

## When to use

Use this skill when the user requests a greater understanding of a given set of code changes to aid them in providing a high-quality code review.

## Instructions

1. Read the diff of the requested code change.
2. Organize the consequential bits of the code changes into logical sections that unfold naturally from start to finish. Boilerplate code such as `import` statements can be ignored.
3. If available, collect the context/impetus of the code change (such as a chat conversation or issue tracking ticket) to guide the construction of your review guide.
4. Create an interactive single-file HTML page that tells the story of the requested code change. Use animations, prose, diagrams, interactivity, and any other educational tools to teach the user enough detail about the change that they can then confidently provide the code change author with an accurate review. Embed CSS and any required JavaScript inline.
