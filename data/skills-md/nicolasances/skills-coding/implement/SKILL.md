---
name: implement
description: Implements a feature or a fix that has been documented in a Github issue
---


## Before Starting

- [ ] Make sure the user has specified which Github issue for the feature or fix to be implemented. If you do not have a Github issue **you cannot proceed** and **must** quit.

## Methodology

You **strictly** follow this methodology when implementing a fix. 

```
Prepare and Plan > Implement feature using TDD > Build & Ship
```

1. **Prepare and Plan**. In this phase, you will prepare for the development of the Fix. For this, you **MUST** use the `prepare` skill. 
2. **Implement fix using TDD**. In this phase, you will code. You will implement the Fix. For this, you **MUST** use the `code` skill.
3. **Build and Ship**. In this phase, you will build and ship the implemented code. For this, you **MUST** use the `build-and-ship` skill.

## Acceptance Criteria

- [ ] You have used the `prepare` skill
- [ ] You have used the `code` skill
- [ ] You have used the `build-and-ship` skill
- [ ] You have committed the changed code. If you have not done that, **you must understand why and make sure you do**. 
- [ ] You have pushed the change to the right branch. 
- [ ] You are not done until **ALL three phases** (prepare → code → build-and-ship) have been executed. Only report to the user after build-and-ship is complete.