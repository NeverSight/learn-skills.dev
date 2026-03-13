---
name: quiz-game-mechanics
description: Implement quiz game logic including game creation, player turn management, score calculation, answer validation, and game completion. Use when building game flows, turn-based mechanics, and scoring algorithms.
license: MIT
metadata:
  author: dev-quiz-battle
  version: "1.0"
---

# Quiz Game Mechanics

This skill covers the core game logic and mechanics for dev-quiz-battle.

## Step-by-step instructions

### 1. Game Creation

Create a game with initial state:

```typescript
export const createGame = mutation({
  args: {
    creatorId: v.id("users"),
    language: v.string(),
    maxRounds: v.number(),
  },
  handler: async (ctx, args) => {
    const code = generateUniqueGameCode(6);
    const gameId = await ctx.db.insert("games", {
      code,
      creatorId: args.creatorId,
      status: "waiting",
      language: args.language,
      players: [args.creatorId],
      currentRound: 0,
      maxRounds: args.maxRounds,
      createdAt: Date.now(),
    });
    return { gameId, code };
  },
});
```

### 2. Player Management

Add and remove players from game:

```typescript
export const joinGame = mutation({
  args: { gameCode: v.string(), playerId: v.id("users") },
  handler: async (ctx, args) => {
    const game = await ctx.db
      .query("games")
      .filter((q) => q.eq(q.field("code"), args.gameCode))
      .first();

    if (!game) throw new Error("Game not found");
    if (game.status !== "waiting") throw new Error("Game already started");

    await ctx.db.patch(game._id, {
      players: [...game.players, args.playerId],
    });

    return game._id;
  },
});
```

### 3. Turn Management

Handle player turns:

```typescript
export const startNextRound = mutation({
  args: { gameId: v.id("games") },
  handler: async (ctx, args) => {
    const game = await ctx.db.get(args.gameId);
    if (!game) throw new Error("Game not found");

    const nextRound = game.currentRound + 1;
    if (nextRound > game.maxRounds) {
      // Game is finished
      await ctx.db.patch(args.gameId, { status: "finished" });
      return { status: "finished" };
    }

    // Generate questions for this round
    const questions = await generateQuestionsForRound(
      game.language,
      game.players.length
    );

    await ctx.db.patch(args.gameId, {
      currentRound: nextRound,
      status: "in-progress",
      currentQuestions: questions.map((q) => q._id),
    });

    return { status: "in-progress", round: nextRound };
  },
});
```

### 4. Score Calculation

Calculate points based on correctness and speed:

```typescript
const calculateScore = (
  isCorrect: boolean,
  timeMs: number,
  difficulty: "easy" | "medium" | "hard"
): number => {
  if (!isCorrect) return 0;

  const baseScore = { easy: 10, medium: 20, hard: 30 }[difficulty];
  const timeBonus = Math.max(0, 30 - Math.floor(timeMs / 1000));
  return baseScore + timeBonus;
};

export const submitAnswer = mutation({
  args: {
    gameId: v.id("games"),
    playerId: v.id("users"),
    questionId: v.id("questions"),
    answer: v.string(),
    timeMs: v.number(),
  },
  handler: async (ctx, args) => {
    const question = await ctx.db.get(args.questionId);
    if (!question) throw new Error("Question not found");

    const isCorrect = question.correctAnswer === args.answer;
    const score = calculateScore(isCorrect, args.timeMs, question.difficulty);

    const answerId = await ctx.db.insert("answers", {
      gameId: args.gameId,
      playerId: args.playerId,
      questionId: args.questionId,
      answer: args.answer,
      isCorrect,
      timeMs: args.timeMs,
      scoreEarned: score,
      submittedAt: Date.now(),
    });

    return { answerId, isCorrect, scoreEarned: score };
  },
});
```

### 5. Game Completion

Handle game ending and winner determination:

```typescript
export const completeGame = mutation({
  args: { gameId: v.id("games") },
  handler: async (ctx, args) => {
    const game = await ctx.db.get(args.gameId);
    if (!game) throw new Error("Game not found");

    // Get all answers for this game
    const answers = await ctx.db
      .query("answers")
      .filter((q) => q.eq(q.field("gameId"), args.gameId))
      .collect();

    // Calculate final scores
    const playerScores = new Map<string, number>();
    answers.forEach((answer) => {
      const current = playerScores.get(answer.playerId) || 0;
      playerScores.set(answer.playerId, current + answer.scoreEarned);
    });

    const winner = Array.from(playerScores.entries()).sort(
      ([, a], [, b]) => b - a
    )[0];

    // Update user stats
    await ctx.db.patch(game._id, {
      status: "finished",
      winnerId: winner?.[0],
      finalScores: Object.fromEntries(playerScores),
    });

    return {
      winnerId: winner?.[0],
      finalScores: Object.fromEntries(playerScores),
    };
  },
});
```

## Common Edge Cases

- **Simultaneous submissions**: Last submission wins
- **Disconnected players**: Mark as inactive, don't count answers
- **Time validation**: Reject answers submitted after round timeout
- **Language validation**: Ensure selected language matches available questions
- **Tie handling**: Multiple players with same score

## Scoring Rules

- Easy questions: 10 points base + time bonus
- Medium questions: 20 points base + time bonus
- Hard questions: 30 points base + time bonus
- Time bonus: +1 point per second remaining (max 30 seconds)
- Incorrect answers: 0 points

See [Game Balance Reference](references/GAME_BALANCE.md) for tuning parameters.
