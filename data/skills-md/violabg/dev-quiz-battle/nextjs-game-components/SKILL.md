---
name: nextjs-game-components
description: Build interactive React components for the quiz game UI using Next.js 16, React 19, TypeScript, and Tailwind CSS v4. Use when creating game lobby, question display, scoreboard, player standings, and game result components.
license: MIT
metadata:
  author: dev-quiz-battle
  version: "1.0"
---

# Next.js Game Components

This skill covers creating React components for the dev-quiz-battle game interface.

## Step-by-step instructions

### 1. Component Structure

Use functional components with TypeScript:

```typescript
import { type ReactNode } from "react";

type GameComponentProps = {
  gameCode: string;
  playerCount: number;
  currentRound: number;
};

export const GameComponent = ({
  gameCode,
  playerCount,
  currentRound,
}: GameComponentProps) => {
  return <div>Game Content</div>;
};
```

### 2. Using Tailwind CSS v4

Follow Tailwind v4 syntax with utility classes:

```typescript
export const Button = ({ onClick, children }: ButtonProps) => {
  return (
    <button
      className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
      onClick={onClick}
    >
      {children}
    </button>
  );
};
```

### 3. Implementing Game Lobby

The game lobby shows waiting players and start game button:

```typescript
export const GameLobby = ({ gameCode, players, onStartGame }: Props) => {
  return (
    <div className="p-6 rounded-lg border border-gray-200">
      <h2 className="text-2xl font-bold mb-4">Game Lobby</h2>
      <p className="text-gray-600 mb-4">Code: {gameCode}</p>
      <div className="space-y-2 mb-6">
        {players.map((player) => (
          <div key={player.id} className="flex items-center gap-2">
            <div className="w-2 h-2 bg-green-500 rounded-full" />
            <span>{player.name}</span>
          </div>
        ))}
      </div>
      <button
        onClick={onStartGame}
        className="w-full bg-green-500 text-white py-2 rounded-lg"
      >
        Start Game
      </button>
    </div>
  );
};
```

### 4. Question Display

Show question with multiple choice options:

```typescript
export const QuestionDisplay = ({
  question,
  options,
  onAnswerSelect,
  selectedAnswer,
}: Props) => {
  return (
    <div className="space-y-4">
      <h3 className="text-lg font-semibold">{question}</h3>
      <div className="grid gap-2">
        {options.map((option, index) => (
          <button
            key={index}
            onClick={() => onAnswerSelect(option)}
            className={`p-3 text-left border rounded-lg transition-colors ${
              selectedAnswer === option
                ? "bg-blue-500 text-white border-blue-500"
                : "border-gray-300 hover:border-gray-400"
            }`}
          >
            {option}
          </button>
        ))}
      </div>
    </div>
  );
};
```

### 5. Scoreboard Component

Display player scores:

```typescript
export const GameScoreboard = ({ players, currentRound, maxRounds }: Props) => {
  const sorted = [...players].sort((a, b) => b.score - a.score);
  return (
    <div className="space-y-3">
      <div className="flex justify-between text-sm text-gray-600">
        <span>
          Round {currentRound}/{maxRounds}
        </span>
      </div>
      {sorted.map((player, index) => (
        <div
          key={player.id}
          className="flex justify-between items-center p-2 bg-gray-50 rounded"
        >
          <span className="font-semibold">
            #{index + 1} {player.name}
          </span>
          <span className="text-blue-600">{player.score}</span>
        </div>
      ))}
    </div>
  );
};
```

### 6. Theme Support

Use next-themes for dark mode:

```typescript
"use client";

import { useTheme } from "next-themes";

export const ThemedComponent = () => {
  const { theme } = useTheme();
  return (
    <div
      className={
        theme === "dark" ? "bg-gray-900 text-white" : "bg-white text-black"
      }
    >
      Content
    </div>
  );
};
```

## Common Edge Cases

- **Loading states**: Show spinners while fetching game data
- **Disabled buttons**: Disable submit button when answer not selected
- **Responsive design**: Test on mobile, tablet, desktop
- **Theme switching**: Ensure colors work in light and dark modes
- **Real-time updates**: Handle Convex subscription updates

## Component Files

Key components in the project:

- `components/game/game-lobby.tsx` - Waiting room
- `components/game/question-display.tsx` - Question UI
- `components/game/game-scoreboard.tsx` - Score tracking
- `components/game/players-standing.tsx` - Final standings
