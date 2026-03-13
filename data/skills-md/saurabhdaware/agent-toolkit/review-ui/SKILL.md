---
name: review-ui
description: Review a web UI flow by running `agent-browser` against a provided URL and scenario. Use when the user asks to test a UI, reproduce steps, validate UX, or verify a web flow on a URL.
disable-model-invocation: true
metadata:
  author: Saurabh Daware (https://srbh.dev)
  version: 0.0.1
---

Your job is review the given URL and inform if the scenarios are working or not

## Arguments

- **URL(s):** The URL of the web page to open and review.
- **Scenario(s)** (optional): Scenarios to test (if not mentioned, assume scenarios as you go)
- **Mode** (headless or headed): Should the review be in headless mode (runs in the background) or headed mode (browser visible to user)

Use AskQuestion to get URL, Mode, and Scenario if not given in prompt

## Steps to Review UI

1. Run `agent-browser --help` to get CLI docs.
   - If `agent-browser` command is not available, check [agent-browser-installation guide](/references/agent-browser-installation.md)
2. Use `agent-browser` to open the {URL(s)} in {Mode}
3. Test out the {Scenario(s)} or assume the scenarios depending on what you see in the UI
4. Close the `agent-browser`
5. Report findings as per "Output Format" section below

## Output Format

Respond in table with following columns

- Scenario (description of the scenario / flow)
- Status (✅ for success, ❌ for failure, ⚠️ couldn't test)
- Notes (describe what failed in case of failure)
