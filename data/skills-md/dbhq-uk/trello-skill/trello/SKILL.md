---
name: trello
description: Manage Trello boards, lists, and cards - find a board, read, create, move, label, comment on and archive cards. Trigger on phrases like "trello", "my boards", "my trello board", "create card", "move card", "add a card to trello". Not for sorting a shopping list into aisle order - that is store-sort.
---

# Trello Board Management

Manage Trello boards, lists, and cards via the Trello REST API.

## Labels - keep a labelled board labelled

**On a board that uses labels, every card on a list you touch carries one.** A board uses labels when its cards carry them: `trello-cards.sh list-json <list-id>` shows each card's labels. On such a board, whenever you create a card or sort or organise a list, make sure every card on the lists you touched has a label - not only the few you moved. A board whose cards carry no labels stays that way unless the user asks for labels.

- Reuse the board's own labels (`trello-boards.sh labels <board-id>`). Do not invent a parallel set, and do not create a label the user did not ask for.
- `trello-cards.sh` reads **and** writes labels: `labels` to show them, `label-add <card-id> <label-id>` and `label-remove` to change them. Label IDs come from `trello-boards.sh labels <board-id>`. The scripts send the key and token in a request header fed to curl on stdin, so neither ever reaches a command line or `ps` output.
- When you create a card on a labelled board, label it in the same pass.
- After organising a labelled board, check that no card on the lists you touched is left without a label.
- On a shopping list the emoji at the start of each card's title is its category, so shopping cards carry no labels. That holds even on a board whose other lists use labels. store-sort sets that emoji.

## Prerequisites

- Credentials configured in `~/.dbhq/trello/` (run setup if not done)
- jq, curl installed

## Setup

If not configured, run:
```bash
${CLAUDE_SKILL_DIR}/scripts/trello-setup.sh
```

Setup asks for the API key and token at a terminal, and the user types them. Run from your shell, it has no terminal: it changes nothing, prints the command for the user and exits 3. Pass that on - the user types `! <path to trello-setup.sh>` at the Claude Code prompt, or runs the path in a terminal of their own. Never ask the user to paste the key or token into the chat, and never pass them to a script.

Setup offers a read-only token, which is all board-digest and due-radar need, and a token that expires after 1 day, 30 days (the default) or never. With a read-only token any change fails with HTTP 401. An expired token answers `invalid token` to everything. The fix for both is to run setup again.

## Board & List Operations

```bash
# List all boards
${CLAUDE_SKILL_DIR}/scripts/trello-boards.sh boards

# Find board by name
${CLAUDE_SKILL_DIR}/scripts/trello-boards.sh find "Shopping"

# Get board details
${CLAUDE_SKILL_DIR}/scripts/trello-boards.sh board <board-id>

# List all lists in a board
${CLAUDE_SKILL_DIR}/scripts/trello-boards.sh lists <board-id>

# Get list details
${CLAUDE_SKILL_DIR}/scripts/trello-boards.sh list <list-id>

# List a board's labels with their ids (for label-add and label-remove)
${CLAUDE_SKILL_DIR}/scripts/trello-boards.sh labels <board-id>
```

### Creating boards, lists and labels

Each of these changes the user's Trello, so confirm the name first. Every one prints the new or changed item as `[id] name`.

```bash
# Create a board (Trello adds its own starter lists and six unnamed colour labels)
${CLAUDE_SKILL_DIR}/scripts/trello-boards.sh board-create "Life" "Optional description"

# Add a list to a board, at the bottom unless you say top
${CLAUDE_SKILL_DIR}/scripts/trello-boards.sh list-create <board-id> "Inbox" top

# Rename a list - prefer this to adding a list when one is already there
${CLAUDE_SKILL_DIR}/scripts/trello-boards.sh list-rename <list-id> "Today"

# Add a label to a board, with a colour or none (green, yellow, orange, red,
# purple, blue, sky, lime, pink, black)
${CLAUDE_SKILL_DIR}/scripts/trello-boards.sh label-create <board-id> "Health" green
```

## Card Operations

### Listing Cards

```bash
# List cards in a list
${CLAUDE_SKILL_DIR}/scripts/trello-cards.sh list <list-id>

# List more cards (the default is 50, and the output says when it left some out)
${CLAUDE_SKILL_DIR}/scripts/trello-cards.sh list <list-id> 100

# Get JSON output (for scripting/sorting)
${CLAUDE_SKILL_DIR}/scripts/trello-cards.sh list-json <list-id>

# Read full card details
${CLAUDE_SKILL_DIR}/scripts/trello-cards.sh read <card-id>
```

### Creating & Updating Cards

```bash
# Create a card
${CLAUDE_SKILL_DIR}/scripts/trello-cards.sh create <list-id> "Card title" "Optional description"

# Update card field (name, desc, due, dueComplete, closed)
${CLAUDE_SKILL_DIR}/scripts/trello-cards.sh update <card-id> name "New title"

# Tick a card's due date as done (false to untick)
${CLAUDE_SKILL_DIR}/scripts/trello-cards.sh update <card-id> dueComplete true

# Move card to another list
${CLAUDE_SKILL_DIR}/scripts/trello-cards.sh move <card-id> <list-id>
```

### Due dates

Trello stores every due date in UTC. The scripts show it in the user's local time: `read` prints `Due: 2026-09-26 00:30 local time (2026-09-25T23:30:00.000Z)`, and due-radar and board-digest show local date and time with the zone named once in the header.

**Always write a due date as a full ISO 8601 time with an offset.** Never a bare day: that leaves the hour and the zone to Trello. When the user gives only a day, use 09:00 their local time. Get the offset from their machine rather than guessing it, because it changes with summer time:

```bash
# GNU date (Linux): prints 2026-09-26T09:00:00+01:00 in UK summer time
date -d '2026-09-26 09:00' --iso-8601=seconds

${CLAUDE_SKILL_DIR}/scripts/trello-cards.sh update <card-id> due "2026-09-26T09:00:00+01:00"
```

On macOS, `date -j -f '%Y-%m-%d %H:%M' '2026-09-26 09:00' +%Y-%m-%dT%H:%M:%S%z` gives the same time with the offset as `+0100`; write it as `+01:00`. After setting a due date, `read` the card and check the local time it shows is the one the user asked for.

### Positioning Cards

```bash
# Move card to top of list
${CLAUDE_SKILL_DIR}/scripts/trello-cards.sh top <card-id>

# Move card to bottom of list
${CLAUDE_SKILL_DIR}/scripts/trello-cards.sh bottom <card-id>

# Set specific position (number or 'top'/'bottom')
${CLAUDE_SKILL_DIR}/scripts/trello-cards.sh position <card-id> 12345
```

### Comments

```bash
# Add comment
${CLAUDE_SKILL_DIR}/scripts/trello-cards.sh comment <card-id> "Comment text"

# List comments
${CLAUDE_SKILL_DIR}/scripts/trello-cards.sh comments <card-id>
```

### Archive & Delete

**Never delete a card unless the user names that card and asks for it to be deleted.** Prefer `archive`: it takes the card off the board and `unarchive` brings it back. A delete cannot be undone, and it takes the card's comments and checklists with it. When the user says "remove", "clear" or "get rid of", archive. Never delete cards in a batch, and never delete to tidy up after yourself.

```bash
# Archive card
${CLAUDE_SKILL_DIR}/scripts/trello-cards.sh archive <card-id>

# Restore archived card
${CLAUDE_SKILL_DIR}/scripts/trello-cards.sh unarchive <card-id>

# Delete permanently - only a card the user named and asked to delete
${CLAUDE_SKILL_DIR}/scripts/trello-cards.sh delete <card-id>
```

### Card Details

```bash
# Show labels
${CLAUDE_SKILL_DIR}/scripts/trello-cards.sh labels <card-id>

# Apply a board label, or take it off - label ids come from the board's `labels` above
${CLAUDE_SKILL_DIR}/scripts/trello-cards.sh label-add <card-id> <label-id>
${CLAUDE_SKILL_DIR}/scripts/trello-cards.sh label-remove <card-id> <label-id>

# Show assigned members
${CLAUDE_SKILL_DIR}/scripts/trello-cards.sh members <card-id>

# Show checklists, with each checklist's id and each item's id
${CLAUDE_SKILL_DIR}/scripts/trello-cards.sh checklist <card-id>

# Add a checklist (prints its id), then an item to it
${CLAUDE_SKILL_DIR}/scripts/trello-cards.sh checklist-add <card-id> "Steps"
${CLAUDE_SKILL_DIR}/scripts/trello-cards.sh checkitem-add <checklist-id> "First step"

# Tick an item - the item id comes from `checklist`
${CLAUDE_SKILL_DIR}/scripts/trello-cards.sh checkitem-done <card-id> <item-id>
```

## Sorting a whole list

This skill has no sorting workflow of its own. To put a shopping list into a supermarket's aisle order, use the **store-sort** skill, which carries the store preset. To order a life-manager board by category, use **life-manager**'s `sort`. To move one card, use `top`, `bottom` or `position` above.

## Workflow: Adding Items

Always confirm before creating:

1. Parse user's request for: list, card title, optional description
2. Find the appropriate board/list if not specified
3. Show proposed card details to user
4. Create card only after explicit approval

## Error Handling

Every script exits non-zero and prints Trello's HTTP status and message on stderr when a request fails. Long lists (a board's cards, its activity, a card's comments) are fetched page by page, so nothing is cut at Trello's 1000-result limit; if a result is ever still incomplete, stderr says "capped at N" and you must tell the user it is partial. Read that before telling the user anything: an error is never an empty result, and "No cards found." means Trello returned an empty list. An unknown verb prints usage on stderr and exits 2; `help` prints it on stdout.

- **Invalid credentials** (HTTP 401, `invalid key` or `invalid token`): the token has expired or been revoked. Ask the user to run setup again (it needs their terminal)
- **HTTP 401 on a change only, while reads work**: the token is read only. Ask the user to run setup again and choose read and write
- **Board/list not found**: Check ID or use find command
- **Rate limited** (HTTP 429): the scripts already retry three times, waiting 2, 4 and 8 seconds. If the error still reaches you, wait before trying again, and do not loop over many boards in one go (300 req/10s per key)

## Notes

- Board/List/Card IDs can be found in Trello URLs or via list commands
- A read-write token can change anything the user's Trello account can - keep the key and token secret
- Rate limits: 300 requests per 10 seconds per API key; 100 requests per 10 seconds per token
