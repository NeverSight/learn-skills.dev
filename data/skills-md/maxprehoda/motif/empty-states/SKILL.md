---
name: empty-states
description: "Finds lists, tables, search results and dashboards that show nothing, or just a bare line of text, when there's no data. Works out why each one would be empty, then builds an empty state with a short explanation and one action. Use after the design-system pipeline, or when an app looks broken before it has any data."
---

# Empty States

Find places that show nothing when there's no data, and give each one a proper empty state.

## Step 1: Find them

```bash
# loops over data
grep -rn -E '\{#each|\.map\(|v-for=' src --include="*.svelte" --include="*.tsx" --include="*.vue" | head -40

# bare "no items" text
grep -rn -iE '"(no |empty|nothing |none )' src --include="*.svelte" --include="*.tsx" | head -30

# checks for an empty list
grep -rn -E '\.length\s*===?\s*0|\.length\s*<\s*1|!\w+\.length' src --include="*.svelte" --include="*.tsx" | head -30
```

Sort what you find into three groups:

1. **Nothing at all.** Shows an empty box. The user can't tell it apart from something that failed to load.
2. **Bare text.** Something like `<p>No items</p>`. It says it's empty, but not why or what to do next.
3. **Already done.** Has an icon, an explanation and an action. Leave these alone.

Fix the ones most people see first. The list a new user sees right after signing up comes before a filtered admin screen.

## Step 2: Work out why it's empty

Why it's empty decides what it should say. The wrong message contradicts what the user just did.

| Type | Why it's empty | What to show |
|---|---|---|
| First use | New account, nothing created yet | What the feature does, and a button to create the first item |
| Cleared | The user finished or deleted everything | Acknowledge it. Don't explain the feature again |
| No results | A search or filter matched nothing | Repeat what they searched for, and offer to clear it |
| Error or no access | The request failed, or they don't have permission | What happened, and how to fix it |

For example, showing a "get started" message to someone who just cleared their list makes it look like the product forgot what they did.

## Step 3: Build it

Four parts, in this order:

1. **Icon.** 32 to 48px, in `text-muted-foreground`, from the project's icon library.
2. **Headline.** Say what's missing, in a neutral way. "No projects yet", not "Empty".
3. **Explanation.** One line on what this feature does. Skip it for cleared states.
4. **Action.** One button that fixes the situation. For no results, that's clearing the search or filter, not creating something new.

Rules:

- Use existing components: the same buttons, font sizes and spacing as the rest of the app.
- Center it vertically, and keep the text narrow with `max-w-sm`.
- Only one action.
- Describe problems as facts, not as the user's fault. "No results for 'xyz'", not "You didn't find anything".
- While data is loading, show a loading skeleton. Only show the empty state once the data has come back empty. Showing it while a request is still running tells the user something that isn't true.

## Step 4: Make a shared component if it repeats

If there are three or more, make one shared `<EmptyState>` component that takes an icon, title, description and action. With fewer than three, keep them inline.

## Report

For each empty state: the file, its type, and what it showed before. List the components you used and confirm none of them are new. Point out any message that needs the product's own voice instead of placeholder wording.
