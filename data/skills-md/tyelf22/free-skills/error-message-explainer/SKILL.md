---
name: error-message-explainer
description: "Paste a confusing error or stack trace and get a plain-English explanation of what it means, the most likely cause, and the first thing to try. Use when the user asks for \"Error Message Explainer\" or provides paste the error message or stack trace."
metadata:
  author: "skillvize"
  version: "v1.0"
  source: "https://www.skillvize.com/skills/tech-error-explainer"
---

# Error Message Explainer

Paste a confusing error or stack trace and get a plain-English explanation of what it means, the most likely cause, and the first thing to try.

`{{input}}` in the steps below is the user's input (Paste the error message or stack trace).

## Steps

### 1. Translate the error

Explain in plain English what {{input}} actually means, including which line or location it points to.

### 2. Diagnose the likely cause

Give the most probable cause given the error type and context, in one or two sentences.

### 3. Give the first fix to try

Recommend the single most likely fix, with a concrete code or config change.

### 4. Offer a fallback

If the first fix doesn't work, suggest the next most likely cause to check.

## Example

**Paste the error message or stack trace:** TypeError: Cannot read properties of undefined (reading 'map') at UserList (UserList.jsx:14)

**Output:**

```
ERROR EXPLAINED

WHAT IT MEANS
You called `.map()` on something that's `undefined` — at UserList.jsx line 14, the value you expected to be an array isn't there yet.

MOST LIKELY CAUSE
The data (e.g. `users`) hasn't loaded when the component first renders, so it's undefined on the first pass.

FIRST THING TO TRY
Guard it: `(users ?? []).map(...)` or render a loading state until the data arrives.

IF THAT'S NOT IT
Check that the prop/state is actually named and passed correctly.
```
