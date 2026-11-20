---
name: presentation
description: "Build an HTML slide deck with hand-drawn Excalidraw-style diagrams and an animated Clawd on every slide. With a prompt, the deck covers that topic. With no prompt, it gives a helicopter view of the user's merged work from the last two weeks. Use for /presentation, 'make a presentation', 'make slides', or 'show what I did the last two weeks'."
license: MIT
compatibility: "Requires a browser with internet access to show the deck, because the deck loads Rough.js from a CDN. The default two-week deck needs an authenticated GitHub CLI. Headless Chrome or another screenshot tool is needed to check the slides."
---

# Presentation

Build a short slide deck that people with no context can follow: a few slides, each with one outcome, one drawing and Clawd.

## Scope

- With a prompt, the deck is about that topic. Collect the facts from the sources the prompt names, the repository, and the conversation.
- With no prompt, the deck shows the user's work of the last 14 days, ending today.
- Write the deck to a new folder outside the repository, by default `~/Desktop/<short-name>/`. Use another place only when the user names one. Never commit the deck.
- Ask the user only when the topic of a prompt is unclear. Do not ask about layout, order or wording. Build a first version and let the user correct it.

## 1. Collect the facts

For the default two-week deck:

```bash
gh pr list --author @me --state merged --search "merged:>=YYYY-MM-DD" --limit 300 \
  --json number,title,mergedAt,additions,deletions
gh pr list --author @me --state open --json number,title,isDraft
```

Pass `-R owner/repo` when the checkout's remote is not the GitHub repository. Read the description of each large or unclear pull request with `gh pr view <number> --json title,body`. If a ticket tracker is connected, use it for context, not for counts. If GitHub access is unavailable, say so and build the deck from the git log and the conversation.

Group the pull requests into three to six features. Put all bug fixes in one group. For each feature, write down what changed for a user or for the team, and the numbers the sources state.

Use only numbers you read in a source. When a drawing needs an example value that you made up, tell the user in the final message. Do not name a customer unless the user did.

## 2. Plan the slides

Use this order:

1. Title: the topic and the dates, with the presenter's name under it. No pull request or ticket counts on this slide.
2. Helicopter view: one drawing of the product's main flow, with each feature marked on the step it changed. Put work that is outside the flow in a frame under it.
3. One slide for each feature.
4. Bug fixes: the title "Backlog cleared 😎", one line that states how many bugs got fixed, and one short line for each fix that says what it now does. No before and after here.
5. Questions.

Do not add a "what's next" slide unless the user asks for one.

Rules for every slide:

- The title states the outcome in plain words, on one line. "A buyer now pays on one page", not "Checkout refactor".
- Explain each term the audience may not know in one short line, once.
- Prefer a drawing to text. A feature slide is a drawing, plus at most three numbers under it.
- A before and now comparison works for one flow or for one real text example. It reads badly as a table of many rows, so do not use it for a list.
- Write in short sentences with common words. Leave out filler and metaphors.

## 3. Build the deck

Copy the [deck template](assets/deck/index.html) folder, `assets/deck/`, to the output folder. It has no build step. It loads Rough.js, which draws the hand-drawn shapes, from a CDN, so the deck needs internet access when it is shown. Change only two files:

- `index.html`: one `<section class="slide">` for each slide.
- `content.js`: the drawings (`SCENES`) and the Clawd walks (`TOURS`).

The [deck format reference](references/deck-format.md) lists the slide layouts, the shape kinds, the colors and the Clawd modes. The template is an example deck about a made-up bookshop. Replace all of its content.

Give every slide a Clawd with its own tour. Clawd reacts to the content: tired or confused in the "before" part, then happy on the result. Use different modes on different slides. Keep the speech bubbles short and a little funny.

## 4. Check every slide

Take a screenshot of each slide and look at it. With Chrome:

```bash
"<chrome>" --headless=new --hide-scrollbars --window-size=1440,810 \
  --virtual-time-budget=9000 --screenshot=<out>/s<N>.png \
  "file://<deck>/index.html?still&at=30000#<N>"
```

`?still` turns off the fade and `at=30000` jumps to the end of the Clawd tour, so the screenshot shows Clawd's last pose. Fix these before you finish:

- text that leaves its box, or a title on two lines
- a drawing that overlaps the numbers under it
- Clawd or its speech bubble on top of text in the last pose

If no screenshot tool is available, say that the slides were not checked.

## Completion

Open `index.html` in the user's browser. In the final message, give the path, list the slides in one line each, and name every value you made up and every claim you did not verify. Keep the message short.

## Example

The user runs `/presentation` with no prompt. You read their 33 merged pull requests of the last two weeks, group them into five features and one group of 12 bug fixes, and build a ten-slide deck in `~/Desktop/two-weeks/`. You check all ten screenshots, open the deck, and tell the user which example values are invented.

The user runs `/presentation explain the new pay page to the support team`. You build a five-slide deck on that topic from the repository and the pull requests that the user names.
