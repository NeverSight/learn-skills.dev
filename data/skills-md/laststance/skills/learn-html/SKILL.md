---
name: learn-html
description: Use when the user asks to learn or understand a topic, concept, API, or "how does X work?" question that isn't tied to a specific diff. Produces a rich interactive HTML explainer.
argument-hint: "[topic or question]"
---

# Learn

Please make me a rich, interactive explanation of the topic or question I asked about.

Explaining a diff is easy mode: a diff is a bounded artifact, and the answer is sitting in the repo. A general question has no such anchor, so **the research step below is the part that makes this skill worth running.** Skip it and you produce a beautiful page full of plausible-sounding details recalled from memory.

## Research first — mandatory, not a tip

Before writing a single line of HTML, establish where each claim will come from. Every factual claim in the explanation must have one of these provenances:

- **Library / framework / browser / platform API** → look it up with `Context7`. Use `WebSearch` / `WebFetch` for spec-level detail (MDN, WHATWG, RFCs, release notes) that Context7 doesn't cover. Your training data may be stale or subtly wrong about ordering, defaults, and deprecations — exactly the details a reader will act on.
- **Anything empirically checkable** → measure it, don't recall it. Run the snippet, drive the browser, print the event order, check the actual output. A measured fact outranks a documented one when they disagree; if they disagree, say so in the page, that contradiction is usually the most interesting thing you'll find.
- **Anything about the user's codebase** → grep and read the real usages before claiming what the code does.

Anything you could not verify gets **flagged inline in the HTML** — a visible "unverified" callout naming what you'd need to check it. Never smooth an uncertain claim into confident prose.

## Sections

- **Background**: Explain the surrounding landscape the topic sits in. We don't know how much the reader already knows, so include a deep background for beginners (note that it can be skipped if the reader is already familiar), and then a narrow background directly relevant to the question.
- **Intuition**: Explain the core intuition. The focus here is the essence, not the full details. Use concrete examples with toy data. Use figures and diagrams liberally.
- **Mechanics**: The concrete how — API surface, event/call ordering, state transitions, edge cases, failure modes. This is where the researched and measured facts land, and it is the section a reader will act on, so cite as you go: link the doc, name the file and line, or show the measurement that produced the claim.
- **In this codebase** *(conditional)*: If the topic actually appears in the current repo, show where and how it's used, and what the local conventions are. Grep first. If the question is generic and the repo has nothing to say about it, **omit this section entirely** — don't manufacture a connection.
- **Quiz**: Five interactive multiple-choice questions, tied to the **Mechanics** section so they test the verified substance rather than trivia. Medium difficulty: hard enough that you need to have actually understood the material, but not gotchas. When the reader clicks, tell them whether they were correct and give feedback.

## Format

- Output a single self-contained HTML file which includes CSS and JavaScript. Make the whole thing one long page with section headers and a table of contents. Don't use tabs for the top-level structure. Basic responsive styling so you can view it on a phone is nice too. Put the file in a global place on my computer outside of the code repo, and make sure the filename always starts with today's date in `YYYY-MM-DD-` format, because it helps keep the files time-sorted and out of version control. For example: /tmp/2026-01-12-learn-<slug>.html
- **Write in the language the question was asked in.** 「compositionend について教えて」 gets a Japanese page; an English question gets an English page. (The global "English for code/docs" rule is about code and documentation — this is a reading artifact.) Code, identifiers, and API names stay verbatim either way.
- Please write with the clarity and flow of Martin Kleppmann, making it engaging and written in classic style. Transitions between sections should be smooth.
- Some tips on diagrams. Ideally, you should pick a small number of diagram families that can be reused throughout the explanation to explain various cases. Some useful kinds of diagrams:
  - A timeline or sequence diagram showing what happens in what order — especially for anything event-driven or asynchronous.
  - A state diagram showing the states a thing can be in and what moves it between them.
  - A system diagram showing data flow or communication between components. Make sure to include example data here!
- Don't use ASCII diagrams. Always use simple HTML designs for your diagrams, HTML lists for lists of things, etc.
  - For code blocks, always use `<pre>` tags. If you use a custom styled div instead, it **must** have
    `white-space: pre-wrap` in its CSS, or the browser will collapse all newlines into a single line.
    Before saving the file, scan each code block in the HTML source and confirm its CSS includes
    `white-space: pre` or `pre-wrap`.
- Use callouts for key concepts or definitions, important edge cases, common misconceptions, and anything you couldn't verify.
