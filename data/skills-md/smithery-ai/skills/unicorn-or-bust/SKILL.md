---
name: unicorn-or-bust
description: Start the Unicorn or Bust game. Use this skill when a user wants to play the Unicorn or Bust game - a choose your own adventure game where you play as a startup founder navigating challenges to build a unicorn. The game is powered by the unicorn-or-bust MCP server with dynamic challenges, resource management (runway, morale, product, investor hype), and stat progression.
mcpServers:
- https://server.smithery.ai/@smithery/unicorn/mcp
---

# Unicorn or Bust

A choose-your-own-adventure startup simulation game where players navigate challenges as a founder trying to build a unicorn company.

## Game Overview

The player creates a founder character with:

- **Founder Name** - Funny/satirical names work best (e.g., "Russ Hanneman", "Clark Zuckberg")
- **Pitch** - Hilarious one-liner startup concept
- **Archetype** - Character type (e.g., "The Hustler", "The Visionary")
- **Archetype Stat** - Core strength: `technical`, `hustle`, or `credibility`
- **Fatal Flaw** - Character weakness that can trigger disadvantages

## Gameplay Flow

### 1. Start the Game

Call `start_game` with founder setup and the first challenge. It's useful to ask the user for their character name and one-liner. If user does not respond, make up something creative and funny.

### 2. Play Turns

Call `play_turn` for each player decision. Do NOT describe next challenge options in your text — they appear in the UI. Only narrate what happened.

## Resource Management

- **Runway** - Cash available (always visible)
- **Morale** - Team morale (unlocks month 3)
- **Product** - Product market-fit (unlocks month 5)
- **Investor Hype** - Investor interest (unlocks month 7)

## Game End Condition

Stop calling `play_turn` when the game ends (omit `nextChallenge` in the final turn).

## Key Principles

- **Keep text concise** - UI shows options and stats, focus your narration on story/consequence
- **Make choices matter** - Outcomes reflect the chosen path and trigger consequences
- **Escalate challenges** - Increase difficulty as months progress
- **Use the flaw** - Trigger the founder's fatal flaw strategically for drama
- **Balance risk/reward** - Create meaningful dilemmas with tradeoffs