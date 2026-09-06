---
name: code
description: Implements a feature in a codebase
---

# Code

This skill is a step of feature development. 
This skill actually implements a *Feature* or a *Fix* in the codebase. 

**Terminology:**
- A *Feature* is an new capability provided by the project. It **must** always be described in its own **markdown file** in the codebase.
- An *Fix* refers to something that needs to be changed in the codebase. It is more granular than a Feature, it is **not** described in its own markdown file and is often related to something that was either left behind or a bug that was noticed. It **must always** be linked to a Github issue.

---

## Starting point

The starting point is **always** either a *Feature* or an *Fix* and a **Plan** consisting of a **list of Tasks** for the implementation. 
You **MUST** have all of these to proceed with any implementation. 

**Checklist to begin:**
If this checklist is not **all** satisfied you **must not and are not allowed** to start the implementation: 
- [ ] You have a *Feature* or a *Fix* to work on. 
- [ ] You have a plan with a list of tasks related to what needs to be implemented. 
- [ ] You know which **codebase** (project, repo) you are working on. 
- [ ] You know which Github issue you are working against

---

## The Workflow

You **must always strictly** follow this workflow when implementing a feature:

1. Read the task list (plan) that is your starting point. 
2. Take one task at a time, starting from those that depend on no other tasks and proceeding according to dependencies. 
    2.1. Implement the task
        - If the task is related to building (or changing) a frontend (UI) component, use the `frontend-development` skill. You **must** use this skill. 
        - If the task is related to building (or changing) a backend microservice, a function (method) or a component that is not a frontend (UI) component, you **MUST**: 
            - [ ] use the `test-driven-development` skill. You **must** use this skill
            - [ ] **read and follow** the coding guidelines for microservices available at the repo `nicolasances/sdlc-agent-specs/coding-standards/toto-microservice-development.md`. You **MUST** follow these guidelines.
    2.2. Commit. 
3. Make a report of the implemented tasks. 

---

## Rules 

**Structure of the final report:**
| Task | Short Description | Commit Id |

**Rules for implementation:**
- You **MUST** always code in the feature branch you have created in the previous phase.
- Whenever the task (implementation) involves a change to the project `toto-react` you **MUST** follow this worklow: 
    1. Switch the frontend that uses `toto-react` to **Local Mode**. You **MUST** use the `switching-toto-react-mode` skill for that. 
    2. Implement the changes
    3. Switch back to **Package Mode**. Again, you **MUST** use the `switching-toto-react-mode` skill for that. 

**Adhere to my Coding Standards**: 
- When coding in python, you **MUST** first read the `coding-standards/python-coding-standards.md` instructions in the `nicolasances/sdlc-agent-specs` GitHub repo.
- When coding in typescript (NodeJS), you **MUST** first read the `coding-standards/node-coding-standards.md` instructions in the `nicolasances/sdlc-agent-specs` GitHub repo.
- When building a microservice (i.e. a backend microservice), you **MUST** first read the `coding-standards/toto-microservice-development.md` instructions in the `nicolasances/sdlc-agent-specs` GitHub repo.

---

## Acceptance Criteria 
- [ ] You have used either the `front-end-development` skill or the `test-driven-development` skill to implement the feature, **or both**, depending on the type of change you're making.
- [ ] If making changes to `toto-react`, you have used the `switch-toto-react-mode` skill.
- [ ] You have made the final report on implemented tasks. All tasks have a commit Id.

**RED FLAGS**: 
- You are modifying frontend UI code without using the `front-end-development` skill
- You are modifying backend code or frontend non-UI code (e.g. core logic) without implmenting tests using the `test-driven-development` skill
- You are building a backend microservice without having read the `coding-standards/toto-microservice-development.md` instructions in the `nicolasances/sdlc-agent-specs` GitHub repo.
- You have a single big commit that contains all the changes for an issue instead of multiple smaller commits that each represent a logical increment of work.
- You are making a change to `toto-react` without having used the `switch-toto-react-mode` skill.
- There is no final report
