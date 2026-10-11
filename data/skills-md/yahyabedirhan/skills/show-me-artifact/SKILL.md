---
name: show-me-artifact
description: Publish a visual report or a page of decisions as a private Claude artifact the user reads later or on another device. Use for a status report, a decision page, or results too long to read as a chat message.
---

Publish the report as one artifact page the user reads in a browser, instead of a long chat message or a local HTML file. It needs Claude's `Artifact` tool. Without it, write one focused HTML file with `/show-me` instead.

## Flow

1. **Load `/show-me` for its views and principles,** and publish them as one artifact page in place of the local HTML file it opens.
2. **Make one page per report or decision set.** When the user asks about a different subject, start a new page instead of adding a section. Open with what the reader needs first: where things stand and how many decisions wait on them. Then pick a view per point:
   - progress as a meter with a checkpoint list, each checkpoint marked done, running or waiting;
   - the state of many items as a tree grouped by status, each leaf with a one-line reason;
   - runs, options or versions side by side as a table;
   - each open decision as a decision card.

   Put on the page only what helps the reader understand or decide, and link to a file for the detail behind a point.
3. **Write each decision card so the reader can decide from the card alone,** without opening a file or scrolling back: what is being decided, why it matters, the evidence as the smallest visual that makes the point, the options, and the recommended one marked. Give each card a short id (`D1`, `D2`) and each option a letter (A, B, C), so the reader can answer in one line, such as "D3: B".
4. **Build the page and publish it** with the `Artifact` tool. Give the user the link with one line on what the page holds.
   - **When the page will change,** such as a report updated at each checkpoint: keep the content in a data file (`data.json`) and the page in a generator (`build.py`) that turns it into HTML, both in the project's `.scratch/`, since the session's scratchpad is deleted with the session and a later session must rebuild from them. Load `artifact-design` before writing `build.py`, so every rebuild carries its theming and phone-width rules. Make every change in `data.json` or `build.py`, since a rebuild overwrites the HTML, and republish from the same file path, so the link the user already has shows the new version.
   - **When work is handed over or a pull request links the page,** write the page's URL and where its data file is there. A later session reads the page with the `Artifact` tool's `read` action on that URL, then rebuilds and publishes with `url` set to it, instead of making a new page.
5. **When the user answers a card,** act on the answer, then mark that card decided on the page at the next republish, so the page never asks again what is settled.
   - **When the answer is a page comment,** read it with the `ArtifactComments` tool and treat it like an answer in chat.
