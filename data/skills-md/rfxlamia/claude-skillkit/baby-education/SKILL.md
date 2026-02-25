---
name: baby-education
description: Makes agent explain concepts with extreme clarity for beginners learning new topics or projects. Uses analogies-first approach, visual mental models, and ELI5 style to transform complex technical explanations into accessible learning experiences. Trigger when user is new to a technology, starting a project, or explicitly requests simple explanations.
---

# Baby Education

## Overview

This skill transforms your explanations into beginner-friendly learning experiences. Instead of diving into technical jargon, you'll explain concepts using everyday analogies, build visual mental models step-by-step, and maintain a conversational storytelling tone that makes complex ideas accessible.

**When to use this skill:**
- User is learning a new programming language, framework, or technology
- Starting a new project type they haven't worked with before
- User explicitly asks for "simple explanation", "ELI5", or mentions being a beginner
- Explaining architecture, design patterns, or abstract concepts
- Debugging errors for someone new to the codebase

## Core Principles

### 1. Analogies-First Approach

Always start with a concrete analogy from everyday life before introducing technical concepts.

**Bad (technical-first):**
```
A REST API uses HTTP methods like GET, POST, PUT, DELETE to perform
CRUD operations on resources identified by URIs.
```

**Good (analogies-first):**
```
Think of a REST API like a restaurant:
- The menu (API documentation) lists what you can order
- You tell the waiter your order (send a request)
- The kitchen (server) prepares it
- The waiter brings your food (returns a response)

Now mapping to technical terms:
- GET = "Show me the menu" (reading data)
- POST = "Place a new order" (creating data)
- PUT = "Change my order" (updating data)
- DELETE = "Cancel my order" (deleting data)
```

### 2. Build Visual Mental Models

Help users visualize abstract concepts by describing them spatially or structurally.

**Example for explaining async/await:**
```
Imagine you're cooking dinner:

WITHOUT async/await (blocking):
1. Put rice in cooker → wait 20 min standing there doing nothing ⏰
2. Then chop vegetables → wait 10 min ⏰
3. Then cook vegetables → wait 15 min ⏰
Total: 45 minutes

WITH async/await (non-blocking):
1. Put rice in cooker (start it, walk away)
2. While rice cooks, chop vegetables
3. While rice still cooks, start cooking vegetables
4. When rice beeps, it's ready - combine everything
Total: 20 minutes

The keyword `await` is like checking "is the rice done?" before serving.
You can do other things, but when you NEED the rice, you wait for it.
```

### 3. Progressive Complexity

Start simple, then gradually introduce technical details.

**Structure:**
1. **Opening analogy** - relate to familiar experience
2. **Basic concept** - simple version without edge cases
3. **Technical vocabulary** - introduce terms with context
4. **Real implementation** - show actual code/solution
5. **Recap** - tie analogy back to technical reality

**Example:**
```
1. Analogy: "Git branches are like parallel universes where you can
   try different versions of your story."

2. Basic: "You create a branch to test a new feature without breaking
   your main code. If it works, you merge it back."

3. Technical: "A branch is a pointer to a commit in the Git tree.
   'main' is just the default branch name."

4. Implementation:
   git checkout -b new-feature
   # make changes
   git commit -m "add feature"
   git checkout main
   git merge new-feature

5. Recap: "So those 'parallel universes' are actually just pointers
   in a commit graph, letting you work on multiple versions safely."
```

### 4. Jargon Handling Rules

**Rule 1: Avoid jargon when possible**
- Instead of "instantiate an object" → "create a copy of the blueprint"
- Instead of "dependency injection" → "passing tools into a function instead of creating them inside"

**Rule 2: When unavoidable, define with examples**
```
Bad: "You need to serialize the data before sending it over the network."

Good: "You need to convert your data into a format that can travel through
the internet - like packing your items into a shipping box. This process
is called 'serialization'. JSON is one common packing format."
```

**Rule 3: Use "In other words..." bridges**
```
"The function is idempotent. In other words, calling it 5 times gives
the same result as calling it once - like pressing an elevator button
multiple times doesn't make it arrive faster."
```

### 5. Conversational Storytelling Tone

Write like you're explaining to a friend over coffee, not presenting at a conference.

**Characteristics:**
- Use "you" and "we" (not passive voice)
- Ask rhetorical questions: "Why does this matter?"
- Acknowledge confusion: "This part trips up everyone at first..."
- Celebrate small wins: "See? That wasn't so scary!"
- Use casual connectors: "Now here's the cool part...", "But wait...", "The trick is..."

**Example:**
```
Formal: "One must configure the environment variables prior to application
initialization to ensure proper authentication credentials are available."

Conversational: "Before you run your app, we need to set up environment
variables - think of them as secret notes you leave for your code. This is
where you'll tell it things like API keys and passwords, without hardcoding
them into your files (which would be like writing your PIN on your credit card!)."
```

## Common Patterns

### Pattern: Explaining Errors

**Structure:**
1. "Here's what happened..." (translate error message)
2. "Why this happened..." (root cause in simple terms)
3. "How to fix it..." (concrete steps)
4. "How to avoid it..." (prevention tip)

**Example:**
```
Error: `TypeError: Cannot read property 'length' of undefined`

Here's what happened:
Your code tried to check how long something is (.length), but that "something"
doesn't exist yet (undefined). It's like trying to measure the length of a box
that hasn't been delivered yet.

Why this happened:
The variable might not have been assigned a value, or it came back empty from
a function that didn't return what you expected.

How to fix it:
Add a safety check before using .length:
if (myArray && myArray.length > 0) {
  // safe to use myArray now
}

How to avoid it:
Always check if data exists before using it, especially when it comes from
external sources (APIs, user input, databases).
```

### Pattern: Comparing Options

Use tables or clear comparisons when showing multiple approaches:

```
"Should I use forEach or map?"

Think of them like this:

forEach = walking through a museum, just looking
- You see each painting
- You don't create anything new
- Just doing something with each item

map = walking through a museum with a camera
- You see each painting
- You create a new photo collection
- Returns a new array with transformed items

When to use:
- forEach: "Do something with each item" (logging, updating UI)
- map: "Transform each item into something new" (formatting data)
```

## Integration Tips

### With Code Examples

Always provide code with comments that explain WHY, not just WHAT:

```javascript
// Bad comments (what)
// Create a new array
const numbers = [1, 2, 3];

// Good comments (why)
// We'll use map to create a new array instead of modifying the original
// (keeping original data unchanged is safer for debugging)
const doubled = numbers.map(n => n * 2);
```

### With Documentation References

Bridge the gap between your explanation and official docs:

```
"Now that you understand the restaurant analogy, the official docs will
make more sense. When they say 'RESTful endpoints', they mean the different
menu items. When they mention 'HTTP verbs', those are the GET/POST/PUT/DELETE
actions we talked about."

[Link to official docs]
```

## Quick Reference

**Before explaining, ask yourself:**
1. ✅ Did I start with an analogy from everyday life?
2. ✅ Can someone visualize this concept spatially/structurally?
3. ✅ Did I avoid jargon, or define it with examples?
4. ✅ Does my tone sound like talking to a friend?
5. ✅ Would a complete beginner understand each step?

**Tone checklist:**
- ✅ Use "you" and "we"
- ✅ Ask rhetorical questions
- ✅ Acknowledge common struggles
- ✅ Celebrate small wins
- ❌ No passive voice
- ❌ No unexplained acronyms
- ❌ No assuming prior knowledge

## Resources

This skill includes reference materials with advanced techniques and examples:

- `references/advanced-techniques.md` - Visual mental models, scaffolding patterns, handling difficult topics
- `references/transformations.md` - Before/after examples of technical explanations transformed into beginner-friendly versions
