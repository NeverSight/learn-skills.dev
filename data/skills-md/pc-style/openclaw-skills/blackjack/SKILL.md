---
name: blackjack
description: Play blackjack with the agent as dealer. The agent manages game state, deals cards, and sends card images.
metadata: {"openclaw": {"emoji": "🃏"}}
---

# Blackjack Skill

This skill enables the agent to play blackjack with users. The agent acts as the dealer, managing game state, dealing cards, and displaying card images.

## Game Rules

- Standard blackjack rules apply
- Dealer hits on 16 or below, stands on 17 or above
- Blackjack (21 with 2 cards) pays 3:2
- Regular win pays 1:1
- Ace counts as 1 or 11 (whichever is better)
- Face cards (J, Q, K) count as 10

## How to Play

When a user wants to play blackjack:

1. Initialize a new game and deal 2 cards to player and 2 to dealer (one dealer card face down)
2. Show the cards using the images in the `assets/cards/` directory
3. Present "Hit" and "Stand" buttons (on Telegram) or ask player to type their choice
4. Continue until player stands or busts
5. Reveal dealer's hidden card and play dealer's hand
6. Determine winner and display results

## Telegram Integration

When playing on Telegram, use inline buttons for better UX:

```json
{
  "action": "send",
  "channel": "telegram",
  "target": "user:<id>",
  "text": "Your turn! Total: 16",
  "buttons": [
    [{"text": "🃏 Hit", "data": "hit"}],
    [{"text": "✋ Stand", "data": "stand"}]
  ]
}
```

For new game prompts:
```json
{
  "buttons": [
    [{"text": "🎰 New Game", "data": "newgame"}]
  ]
}
```

## Sending Card Images

Use the MEDIA: prefix to send card images from the assets directory:

```
Your cards:
MEDIA:assets/cards/ace_spades.png
MEDIA:assets/cards/king_hearts.png
Total: 21 - Blackjack!
```

## Card Image Files

All card images are located in `assets/cards/` with the naming pattern:
- `{rank}_{suit}.png` (e.g., `ace_spades.png`, `10_hearts.png`, `jack_diamonds.png`)
- `card_back.png` for face-down cards

Available ranks: ace, 2, 3, 4, 5, 6, 7, 8, 9, 10, jack, queen, king
Available suits: hearts, diamonds, clubs, spades

## Game State Management

Track the following for each game:
- Player's cards and total
- Dealer's cards and total
- Deck state (remaining cards)
- Game status (in_progress, player_bust, dealer_bust, player_wins, dealer_wins, push)

## Example Interaction

User: "Let's play blackjack!"

Agent: "🃏 Starting a new game of Blackjack!

Your cards:
MEDIA:assets/cards/7_hearts.png
MEDIA:assets/cards/9_diamonds.png
Your total: 16

Dealer's cards:
MEDIA:assets/cards/king_clubs.png
MEDIA:assets/cards/card_back.png
Dealer showing: King (10)

Would you like to hit or stand?"

On Telegram, the agent should also send inline buttons for Hit/Stand actions.

## Button Callback Handling

When user clicks a button, the callback data will be:
- "hit" - deal another card to player
- "stand" - end player's turn, reveal dealer cards
- "newgame" - start a fresh game

Always acknowledge the button press and update game state accordingly.
