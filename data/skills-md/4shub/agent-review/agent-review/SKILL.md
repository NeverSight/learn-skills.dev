---
name: agent-review
description: Request interactive code review from users using the agent-review CLI tool. Automatically captures user feedback on code changes.
---

# Code Review Skill

Use this skill when you need to get human feedback on code changes you've made.

## When to Use This Skill

- After implementing features or fixes
- Before committing significant changes
- When you want user feedback on your approach
- When the user explicitly asks you to review your code

## Installation

If agent-review isn't installed:

```bash
npm install -g agent-review
# or run directly: npx agent-review
```

## How to Use


### Step 1: Run the Code Review Tool

**CRITICAL:** Always run agent-review **inline** (not in background) with a long timeout:

```typescript
Bash({
  command: "npx agent-review", 
  description: "Start code review session",
  timeout: 600000,  // 10 minutes - user needs time to review
})
```

**DO NOT:**
- ❌ Use `run_in_background: true`
- ❌ Use default timeout (2 minutes is too short)
- ❌ Poll bash output with BashOutput

**WHY:**
- The tool blocks until user submits review
- Running inline means you automatically get output when done
- User needs time to review code and add comments
- Feedback is printed to stdout when complete

### Step 2: Automatically Read the Review Feedback

After the tool completes, read the structured JSON feedback:

```typescript
Read({
  file_path: "/path/to/project/.agent-review/latest-review.json"
})
```

This gives you structured data with:
- Line-by-line comments (file, line number, comment text)
- General feedback
- Review statistics

### Step 3: Act on the Feedback

Process the review feedback:

1. **Read line comments** - Address each specific suggestion
2. **Read general feedback** - Consider overall recommendations
3. **Make changes** - Implement requested fixes
4. **Explain** - Tell the user what you changed and why

## Example Workflow

```typescript
// 1. Run code review (inline, long timeout)
const result = await Bash({
  command: "npx agent-review",
  description: "Request code review from user",
  timeout: 600000,  // 10 min
});

// 2. Read structured feedback
const reviewData = await Read({
  file_path: ".agent-review/latest-review.json"
});

// 3. Parse and process
const review = JSON.parse(reviewData);

// 4. Address feedback
for (const comment of review.feedback.lineComments) {
  console.log(`${comment.file}:${comment.line} - ${comment.comment}`);
  // Make changes based on comment
}

// 5. Report back to user
"I've addressed your feedback:
- Fixed the issue in src/app.ts:42 (using const instead of let)
- Updated error handling as suggested
..."
```

## Review Data Structure

The `.agent-review/latest-review.json` file contains:

```json
{
  "id": "review-1234567890",
  "timestamp": "2026-02-03T17:23:33.377Z",
  "diff": { /* full git diff data */ },
  "feedback": {
    "timestamp": "2026-02-03T17:23:33.377Z",
    "lineComments": [
      {
        "file": "src/app.ts",
        "line": 42,
        "oldLine": 41,
        "comment": "Consider using const instead of let",
        "context": "let x = calculateTotal();"
      }
    ],
    "generalFeedback": "Overall looks good!",
    "stats": {
      "filesReviewed": 5,
      "commentsAdded": 3
    }
  }
}
```

## Best Practices

1. **Always run inline** - Never use background mode
2. **Use long timeout** - 600000ms (10 min) minimum
3. **Auto-read feedback** - Don't ask user to tell you the feedback
4. **Address all comments** - Go through each line comment
5. **Summarize changes** - Tell user what you fixed

## Common Mistakes to Avoid

❌ **Running in background:**
```typescript
// WRONG - you won't get the output automatically
Bash({
  command: "npx agent-review",
  run_in_background: true
})
```

❌ **Short timeout:**
```typescript
// WRONG - will timeout before user finishes
Bash({
  command: "npx agent-review",
  timeout: 120000  // 2 min too short
})
```

❌ **Asking user for feedback:**
```typescript
// WRONG - feedback is already in the JSON file!
"What feedback do you have?"
```

✅ **Correct usage:**
```typescript
// RIGHT - inline, long timeout, auto-read
await Bash({
  command: "npx agent-review",
  timeout: 600000
});

const review = await Read({
  file_path: ".agent-review/latest-review.json"
});
```

## Tips

- **Before review:** Tell user what changed: "I've implemented X feature across 5 files. Ready for review?"
- **During review:** The tool auto-opens browser and waits for user
- **After review:** Process feedback immediately and show user your changes
- **Commit option:** User can choose to commit during review - check the bash output


**Remember:** Always run inline with long timeout, then auto-read the JSON feedback!
