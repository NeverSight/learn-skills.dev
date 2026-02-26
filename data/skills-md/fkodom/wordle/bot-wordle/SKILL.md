---
name: bot-wordle
description: Solve the daily NYT Wordle puzzle automatically using a near-optimal bot. Use when the user wants to play or solve today's Wordle (or a past Wordle) without spending time on it, get a shareable emoji grid result, or simulate Wordle games for any date. Triggers on requests like "solve today's Wordle", "play Wordle for me", "get my Wordle score", "bot-wordle", or any mention of automating Wordle gameplay.
---

# Bot Wordle

Automatically fetch and solve the daily NYT Wordle puzzle, producing a shareable emoji grid. The solver achieves ~99.8% win rate with an average of ~3.6 turns.

## Installation

```bash
pip install git+https://github.com/fkodom/wordle.git
```

Requires Python 3.7+. Installs `colorama` and `gdown` as dependencies.

## Usage

```bash
# Solve today's Wordle
bot-wordle

# Solve a specific date
bot-wordle --date 2024-06-15

# Use win-percentage optimization (starts with RALPH instead of SLATE)
bot-wordle --mode win-percentage
```

### Arguments

| Argument | Default | Description |
|----------|---------|-------------|
| `--date` | today | Puzzle date in `YYYY-MM-DD` format |
| `--mode` | `turns-to-win` | `turns-to-win` (fewest guesses) or `win-percentage` (highest win rate) |

### Output

A shareable Wordle emoji grid printed to stdout:

```
Wordle 1234 3/6

🟩🟨⬛⬛⬛
🟩🟩⬛🟨🟨
🟩🟩🟩🟩🟩
```

## How It Works

1. Fetches the puzzle solution from the public NYT API (`nytimes.com/svc/wordle/v2/{date}.json`)
2. Simulates a 6-guess game using `WordleSolver` with a hybrid strategy:
   - **>128 remaining words**: Rank by letter probability
   - **17-128 remaining words**: Maximize information via split analysis
   - **<=16 remaining words** (win-percentage mode): Exhaustive search
3. Default starting word: **SLATE** (turns-to-win) or **RALPH** (win-percentage)
4. Formats the result as a standard shareable emoji grid

## Other Available Commands

The same package also provides interactive play and solver-assisted modes:

| Command | Description |
|---------|-------------|
| `solve-wordle` | Interactive solver that recommends guesses as you play |
| `play-wordle` | Play Wordle in the terminal |
| `play-dordle` / `play-quordle` / `play-octordle` | Multi-word variants |
| `solve-dordle` / `solve-quordle` / `solve-octordle` | Solver for multi-word variants |
